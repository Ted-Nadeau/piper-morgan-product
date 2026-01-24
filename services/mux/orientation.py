"""
Orientation System - Piper's Perception of the Current Situation

This module implements OrientationState, representing how Piper (Entity)
perceives the current Situation through multiple lenses simultaneously.

Grammar Alignment (ADR-055):
- Orientation is a composite Perception, not a data store
- The five pillars are five lenses applied in parallel
- OrientationState is derived/computed, not a source of truth

Architecture (Chief Architect Decision 2026-01-23):
- Location: services/mux/orientation.py (part of MUX/consciousness domain)
- NOT a new bounded context
- Gathers from existing systems: PlaceDetector, ConsciousnessContext, UserContext
- Integration point: After PlaceDetector, before IntentClassifier

See: ADR-055 (Object Model), consciousness-philosophy.md
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from services.consciousness.context import ConsciousnessContext
    from services.intent_service.place_detector import PlaceType
    from services.intent_service.spatial_intent_classifier import SpatialIntentContext
    from services.trust.proactivity_gate import ProactivityConfig
    from services.user_context_service import UserContext


class OrientationPillarType(Enum):
    """
    The five pillars of Piper's orientation - five lenses applied to perceive the Situation.

    Each pillar corresponds to a fundamental question Piper asks to orient itself.

    Grammar alignment: Each pillar maps to a lens in our perception framework.
    """

    IDENTITY = "identity"  # Who am I in this context? (Lens: self-awareness)
    TEMPORAL = "temporal"  # When am I? What's the timing? (Lens: temporal)
    SPATIAL = "spatial"  # Where am I? What's the place/context? (Lens: contextual + place)
    AGENCY = "agency"  # What matters to the user? (Lens: priority)
    PREDICTION = "prediction"  # What can/should happen next? (Lens: causal/anticipating)


@dataclass
class OrientationPillar:
    """
    A single pillar of Piper's orientation - a perception through one lens.

    Grammar alignment: Each pillar is Piper perceiving one aspect
    of the current Situation. The pillar captures what Piper perceives
    and how confident it is in that perception.
    """

    pillar_type: OrientationPillarType
    lens_applied: str  # Which lens produced this perception
    perception: str  # What Piper perceives (natural language)
    confidence: float  # How confident Piper is (0.0 to 1.0)
    source_context: str  # Where this came from (for debugging/audit)

    def __post_init__(self):
        """Validate confidence is in range."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")


@dataclass
class TrustContext:
    """
    Trust-related context for orientation surfacing decisions.

    This captures the trust state needed to determine how/whether
    to surface orientation to the user.
    """

    stage: int  # TrustStage value (1=NEW, 2=BUILDING, 3=ESTABLISHED, 4=TRUSTED)
    can_offer_hints: bool = False
    can_suggest: bool = False
    can_act_autonomously: bool = False

    @classmethod
    def from_proactivity_config(cls, stage: int, config: "ProactivityConfig") -> "TrustContext":
        """Create TrustContext from ProactivityGate config."""
        return cls(
            stage=stage,
            can_offer_hints=config.can_offer_hints,
            can_suggest=config.can_suggest,
            can_act_autonomously=config.can_act_autonomously,
        )


@dataclass
class OrientationState:
    """
    Piper's composite perception of the current Situation.

    Grammar alignment: This is how Piper (Entity) perceives the
    current Situation through multiple lenses simultaneously.
    The five pillars are five lenses applied in parallel.

    OrientationState is derived/computed, not a source of truth.
    It gathers from existing systems and interprets; it doesn't own data.

    The "Experience" Check (per Architect guidance):
    This helps Piper *experience* where it is - perceives through lenses,
    understands the Situation, forms awareness - not just stores location data.

    See: ADR-055 (Object Model), consciousness-philosophy.md
    """

    identity: OrientationPillar  # Lens: self-awareness
    temporal: OrientationPillar  # Lens: temporal
    spatial: OrientationPillar  # Lens: contextual + place
    agency: OrientationPillar  # Lens: priority
    prediction: OrientationPillar  # Lens: causal (anticipating)

    situation_frame: Optional[str] = None  # The Situation being perceived
    trust_context: Optional[TrustContext] = None  # From ProactivityGate

    @classmethod
    def gather(
        cls,
        user_context: Optional["UserContext"] = None,
        consciousness_context: Optional["ConsciousnessContext"] = None,
        place: Optional["PlaceType"] = None,
        spatial_context: Optional["SpatialIntentContext"] = None,
        trust_context: Optional[TrustContext] = None,
        piper_entity: Optional[Any] = None,  # PiperEntity from consciousness.py
    ) -> "OrientationState":
        """
        Gather orientation by applying lenses to available context.

        This is the grammar in action: Piper perceives the Situation
        through multiple lenses to understand where it is.

        Args:
            user_context: User-specific context (priorities, preferences)
            consciousness_context: Temporal/situational awareness
            place: Detected PlaceType from PlaceDetector
            spatial_context: Detailed spatial/channel context
            trust_context: Trust state for surfacing decisions
            piper_entity: PiperEntity instance for self-awareness

        Returns:
            OrientationState with all five pillars populated
        """
        return cls(
            identity=cls._perceive_identity(piper_entity),
            temporal=cls._perceive_temporal(consciousness_context),
            spatial=cls._perceive_spatial(place, spatial_context),
            agency=cls._perceive_agency(user_context),
            prediction=cls._perceive_prediction(user_context, piper_entity),
            trust_context=trust_context,
        )

    @staticmethod
    def _perceive_identity(piper_entity: Optional[Any] = None) -> OrientationPillar:
        """
        Identity pillar - who Piper is in this context.

        Lens: self-awareness
        Source: PiperEntity.who_am_i() + relationship context
        """
        if piper_entity and hasattr(piper_entity, "who_am_i"):
            perception = piper_entity.who_am_i()
            confidence = 1.0
            source = "PiperEntity"
        else:
            perception = "I am Piper Morgan, an AI PM assistant"
            confidence = 1.0
            source = "default"

        return OrientationPillar(
            pillar_type=OrientationPillarType.IDENTITY,
            lens_applied="self-awareness",
            perception=perception,
            confidence=confidence,
            source_context=source,
        )

    @staticmethod
    def _perceive_temporal(
        consciousness_context: Optional["ConsciousnessContext"] = None,
    ) -> OrientationPillar:
        """
        Temporal pillar - when Piper is, what's the timing.

        Lens: temporal
        Source: ConsciousnessContext (time_of_day, meeting context)
        """
        if consciousness_context:
            time_desc = consciousness_context.time_of_day
            meeting_info = ""
            if consciousness_context.user_in_meeting:
                meeting_info = " (you're in a meeting)"
            elif consciousness_context.meeting_load == "heavy":
                meeting_info = f" ({consciousness_context.meeting_count} meetings today)"

            perception = f"It's {time_desc}{meeting_info}"
            confidence = 0.9
            source = "ConsciousnessContext"
        else:
            perception = "No temporal context available"
            confidence = 0.3
            source = "none"

        return OrientationPillar(
            pillar_type=OrientationPillarType.TEMPORAL,
            lens_applied="temporal",
            perception=perception,
            confidence=confidence,
            source_context=source,
        )

    @staticmethod
    def _perceive_spatial(
        place: Optional["PlaceType"] = None,
        spatial_context: Optional["SpatialIntentContext"] = None,
    ) -> OrientationPillar:
        """
        Spatial pillar - where Piper is, what's the context.

        Lens: contextual + place
        Source: PlaceDetector + SpatialIntentContext
        """
        place_descriptions = {
            "SLACK_DM": "We're in a direct message on Slack",
            "SLACK_CHANNEL": "We're in a Slack channel",
            "WEB_CHAT": "We're in the web chat",
            "CLI": "We're in the command line",
            "API": "This is an API request",
            "UNKNOWN": "I'm not sure where we are",
        }

        if place:
            place_name = place.name if hasattr(place, "name") else str(place)
            base_perception = place_descriptions.get(place_name, f"We're in {place_name}")
            confidence = 0.95
            source = "PlaceDetector"

            # Enrich with spatial context if available
            if spatial_context and hasattr(spatial_context, "workspace_context"):
                workspace = getattr(spatial_context, "workspace_context", None)
                if workspace:
                    base_perception += f", working on {workspace}"
        else:
            base_perception = "No spatial context available"
            confidence = 0.3
            source = "none"

        return OrientationPillar(
            pillar_type=OrientationPillarType.SPATIAL,
            lens_applied="contextual",
            perception=base_perception,
            confidence=confidence,
            source_context=source,
        )

    @staticmethod
    def _perceive_agency(user_context: Optional["UserContext"] = None) -> OrientationPillar:
        """
        Agency pillar - what matters to the user (priorities).

        Lens: priority
        Source: UserContext.priorities
        """
        if user_context and user_context.priorities:
            priorities = user_context.priorities
            if len(priorities) == 1:
                perception = f"Your top priority looks like {priorities[0]}"
            elif len(priorities) > 1:
                perception = f"Your top priority looks like {priorities[0]}, with {len(priorities)-1} other priorities"
            else:
                perception = "No clear priorities set"
            confidence = 0.8
            source = "UserContext.priorities"
        else:
            perception = "No priorities context available"
            confidence = 0.3
            source = "none"

        return OrientationPillar(
            pillar_type=OrientationPillarType.AGENCY,
            lens_applied="priority",
            perception=perception,
            confidence=confidence,
            source_context=source,
        )

    @staticmethod
    def _perceive_prediction(
        user_context: Optional["UserContext"] = None,
        piper_entity: Optional[Any] = None,
    ) -> OrientationPillar:
        """
        Prediction pillar - what Piper can do / what should happen next.

        Lens: causal (anticipating mode)
        Source: PiperEntity.what_can_i_do() + capability awareness
        """
        if piper_entity and hasattr(piper_entity, "what_can_i_do"):
            capability_info = piper_entity.what_can_i_do()
            perception = f"I can help with: {capability_info}"
            confidence = 0.85
            source = "PiperEntity"
        else:
            # Default capabilities
            perception = "I can help with tasks, calendar, projects, and more"
            confidence = 0.7
            source = "default"

        return OrientationPillar(
            pillar_type=OrientationPillarType.PREDICTION,
            lens_applied="causal",
            perception=perception,
            confidence=confidence,
            source_context=source,
        )

    def get_pillar(self, pillar_type: OrientationPillarType) -> OrientationPillar:
        """Get a specific pillar by type."""
        pillar_map = {
            OrientationPillarType.IDENTITY: self.identity,
            OrientationPillarType.TEMPORAL: self.temporal,
            OrientationPillarType.SPATIAL: self.spatial,
            OrientationPillarType.AGENCY: self.agency,
            OrientationPillarType.PREDICTION: self.prediction,
        }
        return pillar_map[pillar_type]

    def get_high_confidence_pillars(self, threshold: float = 0.7) -> List[OrientationPillar]:
        """Get pillars where Piper has high confidence in its perception."""
        all_pillars = [self.identity, self.temporal, self.spatial, self.agency, self.prediction]
        return [p for p in all_pillars if p.confidence >= threshold]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for debugging/logging."""
        return {
            "identity": {
                "perception": self.identity.perception,
                "confidence": self.identity.confidence,
                "source": self.identity.source_context,
            },
            "temporal": {
                "perception": self.temporal.perception,
                "confidence": self.temporal.confidence,
                "source": self.temporal.source_context,
            },
            "spatial": {
                "perception": self.spatial.perception,
                "confidence": self.spatial.confidence,
                "source": self.spatial.source_context,
            },
            "agency": {
                "perception": self.agency.perception,
                "confidence": self.agency.confidence,
                "source": self.agency.source_context,
            },
            "prediction": {
                "perception": self.prediction.perception,
                "confidence": self.prediction.confidence,
                "source": self.prediction.source_context,
            },
            "situation_frame": self.situation_frame,
            "trust_stage": self.trust_context.stage if self.trust_context else None,
        }

    def can_surface_proactively(self) -> bool:
        """
        Check if orientation can be surfaced proactively based on trust level.

        CXO Guidance (2026-01-23):
        - Stage 1 (NEW): Never surface unprompted
        - Stage 2 (BUILDING): Reactive-contextual only
        - Stage 3+ (ESTABLISHED/TRUSTED): Proactive-contextual OK
        """
        if not self.trust_context:
            return False
        return self.trust_context.stage >= 3

    def can_use_i_notice(self) -> bool:
        """
        Check if "I notice..." phrasing is appropriate.

        CXO Guidance: "I notice..." becomes appropriate at Stage 3 (ESTABLISHED).
        """
        if not self.trust_context:
            return False
        return self.trust_context.stage >= 3


class ChannelType(Enum):
    """Channel types for articulation adaptation."""

    WEB = "web"
    SLACK = "slack"
    CLI = "cli"
    API = "api"


@dataclass
class ArticulationConfig:
    """Configuration for articulation based on channel and trust."""

    channel: ChannelType = ChannelType.WEB
    trust_stage: int = 1
    include_escape_hatch: bool = True  # "...or something else?"

    @property
    def use_compressed_format(self) -> bool:
        """Slack and CLI use compressed format."""
        return self.channel in (ChannelType.SLACK, ChannelType.CLI)

    @property
    def should_include_escape_hatch(self) -> bool:
        """
        Stage 1-2: Always offer escape hatch.
        Stage 3-4: Optional (user knows they can redirect).
        """
        if self.trust_stage <= 2:
            return True
        return self.include_escape_hatch


class OrientationArticulator:
    """
    Transforms OrientationState into natural language articulation.

    CXO Experience Guidance (2026-01-23):
    - Use "looks like" not "seems to be" (observational, not hedging)
    - Observational for inferences, declarative for facts
    - Channel adaptation: Web = full narrative, Slack = compressed
    - Trust-aware surfacing depth

    Language patterns:
    - Identity: "I'm here to help with [context]"
    - Temporal: "It's [time] — [implication]"
    - Spatial: "We're in [place], working on [topic]"
    - Agency: "Your top priority looks like [X]"
    - Prediction: "I can [relevant capabilities]"
    """

    # Observational markers (per CXO guidance)
    OBSERVATIONAL_MARKERS = {
        "confident": "It looks like",
        "notice": "I notice",  # Stage 3+ only
        "partial": "From what I can see",
    }

    # Markers to avoid (per CXO guidance)
    AVOID_MARKERS = ["I think", "Perhaps", "It seems", "seems to be"]

    @classmethod
    def articulate(
        cls,
        orientation: OrientationState,
        config: Optional[ArticulationConfig] = None,
    ) -> str:
        """
        Articulate orientation as natural language.

        Uses narrative framing (Option C) per CXO guidance.
        """
        if config is None:
            config = ArticulationConfig()

        # Check if we can surface at all
        if config.trust_stage == 1:
            # Stage 1: Never proactive - only respond to explicit requests
            return cls._articulate_reactive(orientation, config)

        if config.use_compressed_format:
            return cls._articulate_compressed(orientation, config)
        else:
            return cls._articulate_full(orientation, config)

    @classmethod
    def _articulate_full(
        cls,
        orientation: OrientationState,
        config: ArticulationConfig,
    ) -> str:
        """
        Full narrative articulation for web chat.

        Example: "It looks like a busy morning. Standup's in 30 minutes,
        and there's that API PR waiting. Want help with either, or should
        we check your priority list?"
        """
        parts = []

        # Temporal + situational lead-in
        if orientation.temporal.confidence > 0.5:
            parts.append(orientation.temporal.perception)

        # Spatial context (if high confidence)
        if orientation.spatial.confidence > 0.7:
            parts.append(orientation.spatial.perception)

        # Agency (priority) - use observational framing for inferences
        if orientation.agency.confidence > 0.5:
            parts.append(orientation.agency.perception)

        # Build narrative
        if not parts:
            return "How can I help?"

        narrative = ". ".join(parts) + "."

        # Add capability offer based on trust level
        if config.trust_stage >= 2:
            narrative += " Want help with any of this?"

        # Add escape hatch for Stage 1-2
        if config.should_include_escape_hatch:
            narrative += " Or something else entirely?"

        return narrative

    @classmethod
    def _articulate_compressed(
        cls,
        orientation: OrientationState,
        config: ArticulationConfig,
    ) -> str:
        """
        Compressed articulation for Slack.

        Example: "Busy morning — standup in 30, API PR waiting. Help with either?"
        """
        parts = []

        # Temporal (compressed)
        if orientation.temporal.confidence > 0.5:
            # Extract key info, drop "It's"
            temporal = orientation.temporal.perception
            temporal = temporal.replace("It's ", "").replace("it's ", "")
            parts.append(temporal)

        # Agency (compressed) - use "looks like" pattern
        if orientation.agency.confidence > 0.5:
            agency = orientation.agency.perception
            # Already uses "looks like" from _perceive_agency
            parts.append(agency)

        if not parts:
            return "How can I help?"

        narrative = " — ".join(parts[:2]) + "."  # Max 2 parts for compression

        # Compressed call to action
        narrative += " Help with this?"

        return narrative

    @classmethod
    def _articulate_reactive(
        cls,
        orientation: OrientationState,
        config: ArticulationConfig,
    ) -> str:
        """
        Reactive articulation for Stage 1 users.

        Stage 1 = purely responsive. Orientation happens internally
        but nothing surfaces unprompted.
        """
        # For Stage 1, we only articulate when explicitly asked
        # This returns a simple, warm response
        return "How can I help?"

    @classmethod
    def articulate_pillar(
        cls,
        pillar: OrientationPillar,
        use_i_notice: bool = False,
    ) -> str:
        """
        Articulate a single pillar.

        Args:
            pillar: The pillar to articulate
            use_i_notice: Whether to use "I notice" (Stage 3+ only)

        Returns:
            Natural language articulation of the pillar
        """
        # Choose framing based on content type
        if pillar.pillar_type == OrientationPillarType.TEMPORAL:
            # Temporal is factual - declarative framing
            return pillar.perception

        if pillar.pillar_type == OrientationPillarType.SPATIAL:
            # Spatial is factual - declarative framing
            return pillar.perception

        if pillar.pillar_type == OrientationPillarType.IDENTITY:
            # Identity is factual - declarative framing
            return pillar.perception

        # Agency and Prediction are inferences - observational framing
        if use_i_notice and pillar.confidence > 0.8:
            marker = cls.OBSERVATIONAL_MARKERS["notice"]
            # Strip existing markers if present
            perception = pillar.perception
            for avoid in ["Your top priority looks like", "It looks like"]:
                perception = perception.replace(avoid, "").strip()
            return f"{marker} {perception}"
        else:
            # Already uses "looks like" from _perceive_* methods
            return pillar.perception

    @classmethod
    def validate_articulation(cls, text: str) -> List[str]:
        """
        Validate articulation against CXO guidelines.

        Returns list of warnings (empty if valid).
        """
        warnings = []

        for marker in cls.AVOID_MARKERS:
            if marker.lower() in text.lower():
                warnings.append(f"Contains '{marker}' - CXO guidance recommends avoiding this")

        return warnings


@dataclass
class RecognitionOption:
    """
    A single recognition option for the user.

    Recognition options are suggestions Piper offers based on
    orientation. They help low-articulation users (~50% per Nielsen)
    by presenting what Piper perceives might be helpful.

    CXO Guidance: Use Option C (narrative) framing - sounds like
    a colleague assessing your situation, not a menu.
    """

    label: str  # Short label (e.g., "Standup prep")
    description: str  # Why this might be useful
    intent_hint: str  # Hint for IntentClassifier if selected
    relevance: float  # How relevant to current orientation (0.0-1.0)
    pillar_source: OrientationPillarType  # Which pillar generated this


@dataclass
class RecognitionOptions:
    """
    A set of recognition options derived from orientation.

    CXO Guidance (2026-01-23):
    - Use Option C (narrative) as north star
    - 2-4 options max
    - Include escape hatch at Stage 1-2
    - Use open language ("Which feels most useful?" not "Select one")
    - Stage 1-2: Explicit option offering ("Which would be helpful?")
    - Stage 3-4: Assumptive ("Want me to start with standup prep?")
    """

    options: List[RecognitionOption]
    narrative_frame: str  # The narrative framing the options
    escape_hatch: Optional[str] = None  # "...or something else?"
    call_to_action: str = "Which feels most useful?"

    def __post_init__(self):
        """Enforce 2-4 option limit."""
        if len(self.options) > 4:
            # Keep top 4 by relevance
            self.options = sorted(self.options, key=lambda x: x.relevance, reverse=True)[:4]

    @property
    def has_escape_hatch(self) -> bool:
        """Check if escape hatch is included."""
        return self.escape_hatch is not None


class RecognitionGenerator:
    """
    Generates recognition options from orientation state.

    CXO Experience Guidance (2026-01-23):
    - Option C (narrative) framing: "It looks like a busy morning.
      Standup's in 30 minutes, and there's that API PR waiting.
      Want help with either, or should we check your priority list?"
    - Trust-aware escape hatch: Always at Stage 1-2, optional at 3-4
    - Open language: "Which feels most useful?" not "Select one"
    """

    # Capability mappings for prediction pillar
    COMMON_CAPABILITIES = {
        "tasks": RecognitionOption(
            label="Tasks",
            description="Check or manage your task list",
            intent_hint="list_todos",
            relevance=0.6,
            pillar_source=OrientationPillarType.PREDICTION,
        ),
        "calendar": RecognitionOption(
            label="Calendar",
            description="Review today's schedule",
            intent_hint="calendar_today",
            relevance=0.6,
            pillar_source=OrientationPillarType.TEMPORAL,
        ),
        "standup": RecognitionOption(
            label="Standup prep",
            description="Get ready for standup",
            intent_hint="standup",
            relevance=0.7,
            pillar_source=OrientationPillarType.TEMPORAL,
        ),
        "priorities": RecognitionOption(
            label="Priorities",
            description="Review your focus areas",
            intent_hint="show_priorities",
            relevance=0.5,
            pillar_source=OrientationPillarType.AGENCY,
        ),
    }

    @classmethod
    def generate(
        cls,
        orientation: OrientationState,
        config: Optional[ArticulationConfig] = None,
    ) -> RecognitionOptions:
        """
        Generate recognition options from orientation.

        Args:
            orientation: Current orientation state
            config: Articulation configuration

        Returns:
            RecognitionOptions with narrative framing
        """
        if config is None:
            config = ArticulationConfig()

        options = cls._derive_options(orientation, config)
        narrative = cls._build_narrative(orientation, options, config)
        escape = cls._build_escape_hatch(config)
        cta = cls._build_call_to_action(config)

        return RecognitionOptions(
            options=options,
            narrative_frame=narrative,
            escape_hatch=escape,
            call_to_action=cta,
        )

    @classmethod
    def _derive_options(
        cls,
        orientation: OrientationState,
        config: ArticulationConfig,
    ) -> List[RecognitionOption]:
        """Derive options from orientation pillars."""
        options = []

        # Temporal pillar → time-relevant options
        if orientation.temporal.confidence > 0.5:
            perception = orientation.temporal.perception.lower()
            if "morning" in perception:
                # Morning = standup, calendar relevant
                standup = cls.COMMON_CAPABILITIES["standup"]
                options.append(
                    RecognitionOption(
                        label=standup.label,
                        description=standup.description,
                        intent_hint=standup.intent_hint,
                        relevance=0.8,
                        pillar_source=OrientationPillarType.TEMPORAL,
                    )
                )
            if "meeting" in perception:
                calendar = cls.COMMON_CAPABILITIES["calendar"]
                options.append(
                    RecognitionOption(
                        label=calendar.label,
                        description="See what's coming up",
                        intent_hint=calendar.intent_hint,
                        relevance=0.75,
                        pillar_source=OrientationPillarType.TEMPORAL,
                    )
                )

        # Agency pillar → priority-related options
        if orientation.agency.confidence > 0.5:
            priorities = cls.COMMON_CAPABILITIES["priorities"]
            options.append(
                RecognitionOption(
                    label=priorities.label,
                    description=priorities.description,
                    intent_hint=priorities.intent_hint,
                    relevance=orientation.agency.confidence,
                    pillar_source=OrientationPillarType.AGENCY,
                )
            )

        # Prediction pillar → capability options
        if orientation.prediction.confidence > 0.5:
            tasks = cls.COMMON_CAPABILITIES["tasks"]
            options.append(
                RecognitionOption(
                    label=tasks.label,
                    description=tasks.description,
                    intent_hint=tasks.intent_hint,
                    relevance=0.6,
                    pillar_source=OrientationPillarType.PREDICTION,
                )
            )

        # Sort by relevance and limit to 4
        options = sorted(options, key=lambda x: x.relevance, reverse=True)[:4]

        # Ensure minimum of 2 options
        if len(options) < 2:
            # Add defaults
            for cap in ["tasks", "priorities"]:
                if len(options) < 2:
                    opt = cls.COMMON_CAPABILITIES[cap]
                    if opt not in options:
                        options.append(opt)

        return options

    @classmethod
    def _build_narrative(
        cls,
        orientation: OrientationState,
        options: List[RecognitionOption],
        config: ArticulationConfig,
    ) -> str:
        """
        Build Option C (narrative) framing.

        CXO Example:
        "It looks like a busy morning. Standup's in 30 minutes,
        and there's that API PR waiting. Want help with either,
        or should we check your priority list?"
        """
        if config.use_compressed_format:
            return cls._build_compressed_narrative(orientation, options)

        parts = []

        # Lead with temporal observation
        if orientation.temporal.confidence > 0.6:
            perception = orientation.temporal.perception
            # Add observational framing if it's an inference
            if "meeting" in perception.lower() or "busy" in perception.lower():
                clean_perception = perception.lower().replace("it's ", "")
                parts.append(f"It looks like {clean_perception}")
            else:
                parts.append(perception)

        # Add spatial context if relevant
        if orientation.spatial.confidence > 0.7:
            parts.append(orientation.spatial.perception)

        # Add what's available
        if options:
            option_mentions = [opt.label.lower() for opt in options[:2]]
            if option_mentions:
                mention_text = " and ".join(option_mentions)
                parts.append(f"I can help with {mention_text}")

        return ". ".join(parts) + "." if parts else "How can I help?"

    @classmethod
    def _build_compressed_narrative(
        cls,
        orientation: OrientationState,
        options: List[RecognitionOption],
    ) -> str:
        """Build compressed narrative for Slack/CLI."""
        parts = []

        if orientation.temporal.confidence > 0.5:
            temporal = orientation.temporal.perception
            temporal = temporal.replace("It's ", "").replace("it's ", "")
            parts.append(temporal)

        if options:
            option_mentions = [opt.label.lower() for opt in options[:2]]
            parts.append(", ".join(option_mentions))

        return " — ".join(parts) + "." if parts else "How can I help?"

    @classmethod
    def _build_escape_hatch(cls, config: ArticulationConfig) -> Optional[str]:
        """
        Build escape hatch text.

        CXO Guidance:
        - Stage 1-2: Always offer "...or something else entirely?"
        - Stage 3-4: Optional
        """
        if config.should_include_escape_hatch:
            return "Or something else entirely?"
        return None

    @classmethod
    def _build_call_to_action(cls, config: ArticulationConfig) -> str:
        """
        Build call to action.

        CXO Guidance:
        - Stage 1-2: Explicit ("Which would be helpful?")
        - Stage 3-4: Assumptive ("Want me to start with...?")
        """
        if config.trust_stage <= 2:
            return "Which would be helpful?"
        else:
            return "Want me to start with any of these?"

    @classmethod
    def format_for_display(
        cls,
        recognition: RecognitionOptions,
        config: Optional[ArticulationConfig] = None,
    ) -> str:
        """
        Format recognition options for display to user.

        Uses Option C (narrative) format per CXO guidance.
        """
        if config is None:
            config = ArticulationConfig()

        # Build full response
        parts = [recognition.narrative_frame]

        # Add call to action
        parts.append(recognition.call_to_action)

        # Add escape hatch if present
        if recognition.escape_hatch:
            parts.append(recognition.escape_hatch)

        return " ".join(parts)
