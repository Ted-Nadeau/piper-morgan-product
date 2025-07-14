# services/intent_service/classifier.py
import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import structlog

from services.api.errors import (
    IntentClassificationFailedError,
    LowConfidenceIntentError,
    NoRelevantKnowledgeError,
)
from services.api.serializers import intent_to_dict
from services.domain.models import Intent, IntentCategory
from services.intent_service.pre_classifier import PreClassifier
from services.intent_service.prompts import INTENT_CLASSIFICATION_PROMPT
from services.knowledge_graph import get_ingester
from services.llm.clients import llm_client
from shared.events import EventBus

logger = structlog.get_logger()


class IntentClassifier:
    def __init__(self, event_bus: Optional[EventBus] = None):
        self.llm = llm_client  # Use your global client instance
        self.event_bus = event_bus
        self.knowledge_hierarchy = [
            "pm_fundamentals",  # Your book, PM best practices
            "business_context",  # Client/domain specific
            "product_context",  # Specific product details
            "task_context",  # Current task specifics
        ]

    async def classify(
        self,
        message: str,
        context: Optional[Dict] = None,
        session: Optional[Any] = None,
    ) -> Intent:
        # Stage 1: Pre-classification
        pre_intent = PreClassifier.pre_classify(message)
        if pre_intent:
            logger.info(
                "intent_classification",
                source="PRE_CLASSIFIER",
                action=pre_intent.action,
                message_length=len(message),
                message_preview=message[:50],
            )  # First 50 chars for debugging
            return pre_intent

        # Stage 2: LLM classification
        logger.info(
            "intent_classification_attempt",
            source="LLM",
            message_length=len(message),
            message_preview=message[:50],
        )

        # Check for file references
        has_file_reference = PreClassifier.detect_file_reference(message)

        # Prepare file context
        file_context = ""
        if session and has_file_reference:
            recent_files = session.get_recent_files()
            if recent_files:
                file_context = f"Recent uploads: {[f['filename'] for f in recent_files]}"

        # Capture input context for learning
        classification_context = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "available_knowledge": self._assess_available_knowledge(context),
            "user_context": context or {},
            "has_file_reference": has_file_reference,
            "file_context": file_context,
        }

        try:
            # Perform classification with confidence scoring
            intent, reasoning = await self._classify_with_reasoning(message, context, file_context)

            # Check for truly vague intents that need clarification
            # Lower confidence threshold to avoid overriding legitimate classifications
            if intent.confidence < 0.3 or self._seems_vague(intent):
                logger.info("Low confidence or vague intent detected, requesting clarification")
                return Intent(
                    category=IntentCategory.CONVERSATION,
                    action="clarification_needed",
                    confidence=intent.confidence,
                    context={
                        "original_classification": intent_to_dict(intent),
                        "trigger": (
                            "low_confidence" if intent.confidence < 0.3 else "vague_pattern"
                        ),
                    },
                )

            # Identify learning opportunities
            intent.learning_signals = self._identify_learning_signals(message, intent, reasoning)

            # Emit event for future learning system if event bus is available
            if self.event_bus:
                await self.event_bus.emit(
                    "intent.classified",
                    {
                        "intent_id": intent.id,
                        "classification_context": classification_context,
                        "intent": intent_to_dict(intent),
                        "reasoning": reasoning,
                        "learning_signals": intent.learning_signals,
                    },
                )

            # After successful LLM classification
            logger.info(
                "intent_classification",
                source="LLM",
                action=intent.action,
                message_length=len(message),
                confidence=intent.confidence,
            )

            return intent

        except LowConfidenceIntentError:
            # Re-raise to be caught by the middleware
            raise
        except Exception as e:
            logger.error(f"Classification failed: {e}", exc_info=True)
            # Raise a structured error instead of falling back
            raise IntentClassificationFailedError(details={"original_error": str(e)})

    async def _classify_with_reasoning(
        self, message: str, context: Optional[Dict] = None, file_context: str = ""
    ) -> Tuple[Intent, Dict[str, Any]]:
        """Classify intent with detailed reasoning"""
        # Prepare context for LLM
        context_info = ""
        if context:
            context_info = f"\nContext: {json.dumps(context, indent=2)}"

        # Build prompt with context
        prompt = INTENT_CLASSIFICATION_PROMPT.format(
            user_message=message, context_info=context_info, file_context=file_context
        )

        try:
            # Use your task-based routing with "intent_classification" task type
            response = await self.llm.complete(
                task_type="intent_classification", prompt=prompt, context=context
            )

            # Parse JSON response
            # Extract the first JSON object from the response
            json_match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                parsed = json.loads(json_str)
            else:
                raise ValueError("No valid JSON object found in response")

            intent = Intent(
                category=IntentCategory(parsed["category"].lower()),
                action=parsed["action"],
                confidence=parsed["confidence"],
                context={
                    "original_message": message,
                    "knowledge_used": parsed.get("knowledge_used", []),
                },
            )

            reasoning = {
                "classification_reasoning": parsed["reasoning"],
                "helpful_knowledge_domains": parsed.get("knowledge_domains", []),
                "ambiguity_notes": parsed.get("ambiguity_notes", []),
                "knowledge_used": parsed.get("knowledge_used", []),
            }

            return intent, reasoning

        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse or read LLM response: {e}", raw_response=response)
            raise IntentClassificationFailedError(
                details={
                    "reason": "LLM response was malformed",
                    "raw_response": response[:200],
                }
            )

    def _identify_learning_signals(self, message: str, intent: Intent, reasoning: Dict) -> Dict:
        """Identify what learning opportunities this interaction presents"""

        signals = {
            "confidence_level": intent.confidence,
            "knowledge_gaps": [],
            "clarification_needed": [],
            "pattern_matches": [],
        }

        # Low confidence suggests learning opportunity
        if intent.confidence < 0.7:
            signals["knowledge_gaps"].append(
                {
                    "type": "uncertain_classification",
                    "domain": reasoning.get("helpful_knowledge_domains", []),
                }
            )

        # Check for ambiguous language
        ambiguity_markers = [
            "something like",
            "maybe",
            "not sure",
            "could you",
            "might",
            "possibly",
        ]
        if any(marker in message.lower() for marker in ambiguity_markers):
            signals["clarification_needed"].append("ambiguous_request")

        # Check knowledge hierarchy needs
        for domain in reasoning.get("helpful_knowledge_domains", []):
            if domain not in self.knowledge_hierarchy:
                signals["knowledge_gaps"].append({"type": "missing_domain", "domain": domain})

        return signals

    def _assess_available_knowledge(self, context: Dict) -> List[str]:
        """Determine what knowledge is currently available"""
        # For now, return empty list
        # Later: Query knowledge graph for available domains
        return []

    def _fallback_classify(self, message: str) -> Intent:
        """Simple keyword-based classification as fallback"""
        message_lower = message.lower()

        # Explicit project query mappings
        if "how many projects" in message_lower or (
            "how many" in message_lower and "project" in message_lower
        ):
            category = IntentCategory.QUERY
            action = "count_projects"
        elif "default project" in message_lower:
            category = IntentCategory.QUERY
            action = "get_default_project"
        elif "find project" in message_lower:
            category = IntentCategory.QUERY
            action = "find_project"
        elif "project details" in message_lower:
            category = IntentCategory.QUERY
            action = "get_project_details"
        elif "get project" in message_lower and "id" in message_lower:
            category = IntentCategory.QUERY
            action = "get_project"
        elif any(word in message_lower for word in ["create", "make", "build", "add", "new"]):
            category = IntentCategory.EXECUTION
            action = "create_item"
        elif any(word in message_lower for word in ["analyze", "check", "review", "look at"]):
            category = IntentCategory.ANALYSIS
            action = "analyze_data"
        elif any(word in message_lower for word in ["summarize", "document", "write", "report"]):
            category = IntentCategory.SYNTHESIS
            action = "generate_content"
        elif any(word in message_lower for word in ["plan", "strategy", "prioritize", "decide"]):
            category = IntentCategory.STRATEGY
            action = "strategic_planning"
        elif any(
            word in message_lower
            for word in ["list", "show", "get", "find", "what", "which", "how many"]
        ):
            category = IntentCategory.QUERY
            action = "list_items"
        else:
            category = IntentCategory.LEARNING
            action = "learn_pattern"

        return Intent(
            category=category,
            action=action,
            confidence=0.5,  # Lower confidence for fallback
            context={"original_message": message, "method": "fallback"},
        )

    def _seems_vague(self, intent: Intent) -> bool:
        """Detects if the intent/action is vague/underspecified."""
        vague_actions = {
            "clarification_needed",
            "unknown",
            "get_greeting",
            "get_help",
            "get_info",
            "get_something",
        }
        # Removed "problem", "issue", "bug", "fix" as these are legitimate in bug reports
        # Removed "improve", "change", "update" as these are legitimate in feature requests
        # Only keep truly vague words that indicate unclear intent
        vague_keywords = ["thing", "something", "it", "this", "that", "help"]
        # If action is a known vague action
        if intent.action in vague_actions:
            return True
        # If action or context contains vague keywords (as whole words)
        import re

        action_lower = (intent.action or "").lower()
        for word in vague_keywords:
            # Use word boundaries to avoid false positives like "it" in "create_item"
            if re.search(r"\b" + re.escape(word) + r"\b", action_lower):
                return True
        # If ambiguity notes are present in context
        ambiguity_notes = intent.context.get("ambiguity_notes") if intent.context else None
        if ambiguity_notes and any(isinstance(note, str) and note for note in ambiguity_notes):
            return True
        return False


# Create a singleton instance without event bus for backward compatibility
classifier = IntentClassifier()
