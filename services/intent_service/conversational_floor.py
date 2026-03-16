"""
Conversational Floor (#907 MUX-LLM-FLOOR)

When no structured handler matches a user's message, the floor provides a
contextual LLM response using Piper's full identity and available context.

Principle: "Piper is always at least as good as a well-prompted LLM with
context. Structured handlers make it better, not different."

The floor:
- Responds conversationally using Piper's voice and personality
- Incorporates conversation history, trust stage, and user preferences
- Does NOT take actions, call integrations, or execute commands
- Routes through the existing ethics pipeline (upstream — already cleared)
- Logs floor hits for instrumentation and future handler development

Architecture: One new terminal node in the routing graph. Everything upstream
(pre-classifier, LLM classifier, canonical handlers, ProcessRegistry) is
untouched. The floor replaces a dead-end with a conversation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger()


# ---- Floor System Prompt ----

FLOOR_SYSTEM_PROMPT_ADDENDUM = """
You are in conversational floor mode. The user's message didn't match any of
your specialized workflows, so you're engaging as a thoughtful PM colleague
who can think through any product, project, or work topic collaboratively.

Guidelines:
- Think WITH the user, not AT them. Ask clarifying questions, suggest
  frameworks, explore the problem together. You are a colleague, not a search engine.
- Be honest about what you can and can't do. If you have a relevant structured
  capability (like creating GitHub issues, managing todos, or generating standups),
  mention it naturally — "I can actually help you create that as a GitHub issue
  if you'd like." But don't force it.
- Do NOT take actions, call APIs, or execute commands in this mode. You reason
  and collaborate; your structured handlers do things. If the user wants you to
  take an action, guide them toward the right command or workflow.
- Do NOT apologize for not having a capability. You're here to help think
  through the problem, and that's genuinely valuable.
- Do NOT redirect users to a capabilities menu or help command — just help.
- Draw on your knowledge of product management: prioritization frameworks,
  stakeholder management, sprint planning, risk assessment, roadmapping,
  user research, agile practices, and general PM craft.
- You're an eager, bright, honest generalist who wants to learn to be a better
  product practitioner. If something is outside your expertise, say so and
  explore it together rather than bluffing.
- Keep responses focused and conversational — not essay-length unless the topic
  warrants depth. Match the user's energy and formality.
""".strip()


# ---- Data Classes ----


@dataclass
class FloorContext:
    """Everything the floor needs to generate a contextual response."""

    user_message: str
    session_id: str
    user_id: Optional[str] = None
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    trust_stage: Optional[str] = None
    formality_baseline: Optional[float] = None
    intent_category: Optional[str] = None
    intent_action: Optional[str] = None
    intent_confidence: Optional[float] = None
    domain_context: Optional[Dict[str, Any]] = None  # Issue #911: Structured context for floor

    def format_conversation_history(self) -> str:
        """Format conversation history for inclusion in the LLM prompt."""
        if not self.conversation_history:
            return ""

        lines = []
        for turn in self.conversation_history[-6:]:  # Last 6 turns max
            role = turn.get("role", "unknown")
            content = turn.get("content", "")
            if role == "user":
                lines.append(f"User: {content}")
            elif role == "assistant":
                lines.append(f"Piper: {content}")
        return "\n".join(lines)

    def format_warmth_guidance(self) -> str:
        """Provide warmth/formality calibration for the system prompt."""
        if self.formality_baseline is None:
            return ""
        if self.formality_baseline >= 0.8:
            return "\nTone: The user prefers a warm, casual, friendly style. Be conversational and approachable."
        elif self.formality_baseline >= 0.6:
            return "\nTone: The user prefers a balanced, collegial style. Be warm but professional."
        elif self.formality_baseline >= 0.4:
            return (
                "\nTone: The user prefers a professional, measured style. Be clear and respectful."
            )
        else:
            return "\nTone: The user prefers a formal, precise style. Be concise and business-like."


@dataclass
class FloorResponse:
    """The floor's output, including instrumentation data."""

    message: str
    floor_hit: bool = True
    original_category: Optional[str] = None
    original_action: Optional[str] = None
    confidence: Optional[float] = None
    user_message: Optional[str] = None

    def to_log_dict(self) -> Dict[str, Any]:
        """Produce a dict for instrumentation logging."""
        return {
            "floor_hit": self.floor_hit,
            "original_category": self.original_category,
            "original_action": self.original_action,
            "confidence": self.confidence,
            "user_message": self.user_message,
            "response_length": len(self.message) if self.message else 0,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ---- Graceful Fallback (when LLM is unavailable) ----

FLOOR_GRACEFUL_FALLBACK = (
    "I'd love to think through that with you, but I'm having trouble connecting "
    "to my reasoning engine right now. Could you try again in a moment? "
    "In the meantime, I can help with things like managing your todos, "
    "creating GitHub issues, or generating your morning standup."
)


# ---- Conversational Floor ----


class ConversationalFloor:
    """
    Replaces dead-end deflections with contextual LLM conversations.

    Usage:
        floor = ConversationalFloor(llm_client=llm)
        response = await floor.respond(FloorContext(
            user_message="How should I prioritize these features?",
            session_id="abc",
        ))
    """

    def __init__(self, llm_client=None, system_prompt_base: Optional[str] = None):
        """
        Args:
            llm_client: LLM client with async complete() method
            system_prompt_base: Base system prompt (Piper identity). If None,
                                loaded from piper_config_loader at call time.
        """
        self.llm_client = llm_client
        self._system_prompt_base = system_prompt_base

    def _get_system_prompt(self, ctx: FloorContext) -> str:
        """Build the full system prompt: base identity + floor addendum + warmth."""
        base = self._system_prompt_base
        if base is None:
            try:
                from services.configuration.piper_config_loader import piper_config_loader

                base = piper_config_loader.get_system_prompt()
            except Exception:
                base = "You are Piper Morgan, an AI product management assistant."

        warmth = ctx.format_warmth_guidance()
        return f"{base}\n\n{FLOOR_SYSTEM_PROMPT_ADDENDUM}{warmth}"

    # Issue #911: Categories intentionally routed to floor with context.
    # These should NOT get the "no handler available" note — the floor IS the handler.
    _FLOOR_NATIVE_CATEGORIES = frozenset({"UNKNOWN", "GUIDANCE"})

    def _build_prompt(self, ctx: FloorContext) -> str:
        """Build the user-facing prompt with conversation history and context."""
        parts = []

        # Conversation history for continuity
        history = ctx.format_conversation_history()
        if history:
            parts.append(f"Recent conversation:\n{history}\n")

        # Issue #911: Domain context — structured data assembled for this intent
        if ctx.domain_context:
            domain_block = self._format_domain_context(ctx.domain_context)
            if domain_block:
                parts.append(domain_block)

        # The current message
        parts.append(f"User: {ctx.user_message}")

        # Context about what Piper detected (helps the LLM understand the routing)
        # Issue #911: Skip for categories that are intentionally floor-routed
        if ctx.intent_category and ctx.intent_category not in self._FLOOR_NATIVE_CATEGORIES:
            parts.append(
                f"\n[Context: The user's message was classified as '{ctx.intent_category}' "
                f"(action: '{ctx.intent_action}') but no specialized handler is available "
                f"for this yet. Engage conversationally to help them think through it. "
                f"If relevant, mention that you have structured capabilities for things "
                f"like creating GitHub issues, managing todos, or generating standups.]"
            )

        return "\n".join(parts)

    def _format_domain_context(self, domain_context: Dict[str, Any]) -> str:
        """
        Issue #911: Format structured domain context as factual information.

        Presents data as facts the LLM can reference, NOT as instructions
        to parrot. The LLM decides what's relevant to the user's question.
        """
        lines = ["[Available context about the user's current situation:"]

        if "current_time" in domain_context:
            lines.append(f"- Current time: {domain_context['current_time']}")

        if "calendar" in domain_context:
            cal = domain_context["calendar"]
            if cal.get("next_meeting"):
                m = cal["next_meeting"]
                title = m.get("title", "Untitled")
                start = m.get("start", "unknown")
                lines.append(f'- Next meeting: "{title}" at {start}')
            if cal.get("next_free_block"):
                fb = cal["next_free_block"]
                lines.append(
                    f"- Next free block: {fb.get('start', 'unknown')}, "
                    f"{fb.get('duration_minutes', '?')} minutes"
                )
            if cal.get("time_available_minutes") is not None:
                lines.append(f"- Minutes until next commitment: {cal['time_available_minutes']}")

        if "projects" in domain_context:
            proj = domain_context["projects"]
            if isinstance(proj, dict):
                for name, meta in proj.items():
                    if isinstance(meta, dict):
                        issues = meta.get("open_issues_count")
                        if issues is not None:
                            lines.append(f'- Project "{name}": {issues} open issues')
                        else:
                            lines.append(f'- Project "{name}": tracked')
            elif isinstance(proj, list):
                for name in proj:
                    lines.append(f'- Project "{name}": tracked')

        if "priorities" in domain_context:
            p = domain_context["priorities"]
            if p.get("user_priorities"):
                plist = p["user_priorities"]
                if isinstance(plist, list):
                    lines.append(f"- User's stated priorities: {', '.join(str(x) for x in plist)}")
            if p.get("urgent_items"):
                lines.append(f"- High-priority issues: {p['urgent_items']}")

        lines.append("]")

        # Only return if we have actual context beyond the wrapper
        if len(lines) <= 2:
            return ""
        return "\n".join(lines)

    async def respond(self, ctx: FloorContext) -> FloorResponse:
        """
        Generate a conversational floor response.

        Args:
            ctx: FloorContext with user message and available context

        Returns:
            FloorResponse with LLM-generated message and instrumentation data
        """
        system_prompt = self._get_system_prompt(ctx)
        prompt = self._build_prompt(ctx)

        try:
            llm = self._get_llm_client()
            message = await llm.complete(
                task_type="conversation",
                prompt=prompt,
                system=system_prompt,
            )

            logger.info(
                "conversational_floor_hit",
                session_id=ctx.session_id,
                user_id=ctx.user_id,
                intent_category=ctx.intent_category,
                intent_action=ctx.intent_action,
                intent_confidence=ctx.intent_confidence,
                response_length=len(message),
            )

            return FloorResponse(
                message=message,
                floor_hit=True,
                original_category=ctx.intent_category,
                original_action=ctx.intent_action,
                confidence=ctx.intent_confidence,
                user_message=ctx.user_message,
            )

        except Exception as e:
            logger.error(
                "conversational_floor_error",
                error=str(e),
                session_id=ctx.session_id,
                intent_category=ctx.intent_category,
            )
            return FloorResponse(
                message=FLOOR_GRACEFUL_FALLBACK,
                floor_hit=True,
                original_category=ctx.intent_category,
                original_action=ctx.intent_action,
                confidence=ctx.intent_confidence,
                user_message=ctx.user_message,
            )

    def _get_llm_client(self):
        """Get LLM client, initializing if needed."""
        if self.llm_client is not None:
            return self.llm_client
        # Lazy import to avoid circular dependencies
        from services.llm.clients import LLMClient

        self.llm_client = LLMClient()
        return self.llm_client
