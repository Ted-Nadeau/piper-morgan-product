"""
Spatial Intent Classifier - Classify spatial events as intents
Classifies Slack spatial events into Piper Morgan intents with spatial context.

Analyzes spatial events to determine user intent and classify them appropriately
for workflow creation and processing.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from services.domain.models import Intent
from services.shared_types import IntentCategory

from .event_handler import EventProcessingResult
from .spatial_agent import NavigationDecision


@dataclass
class SpatialIntentPattern:
    """Pattern for classifying spatial events as intents"""

    pattern: str
    intent_category: IntentCategory
    action: str
    confidence: float
    spatial_context_required: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)


@dataclass
class IntentClassificationResult:
    """Result of spatial intent classification"""

    intent: Intent
    confidence: float
    spatial_context: Dict[str, Any]
    classification_reason: str
    patterns_matched: List[str] = field(default_factory=list)


class SpatialIntentClassifier:
    """Classifier for converting spatial events to intents"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.intent_patterns = self._create_intent_patterns()

    def _create_intent_patterns(self) -> List[SpatialIntentPattern]:
        """Create patterns for intent classification"""
        return [
            # Help requests
            SpatialIntentPattern(
                pattern=r"help|assist|support|need.*help|can.*help",
                intent_category=IntentCategory.EXECUTION,
                action="create_task",
                confidence=0.8,
                keywords=["help", "assist", "support", "need", "can"],
            ),
            # Bug reports
            SpatialIntentPattern(
                pattern=r"bug|error|issue|problem|broken|not.*working|failed",
                intent_category=IntentCategory.EXECUTION,
                action="create_ticket",
                confidence=0.9,
                keywords=["bug", "error", "issue", "problem", "broken", "failed"],
            ),
            # Feature requests
            SpatialIntentPattern(
                pattern=r"feature|enhancement|improvement|add.*feature|new.*feature",
                intent_category=IntentCategory.EXECUTION,
                action="create_feature",
                confidence=0.8,
                keywords=["feature", "enhancement", "improvement", "add", "new"],
            ),
            # Status updates
            SpatialIntentPattern(
                pattern=r"status|update|progress|done|completed|finished",
                intent_category=IntentCategory.ANALYSIS,
                action="generate_report",
                confidence=0.7,
                keywords=["status", "update", "progress", "done", "completed"],
            ),
            # Performance concerns
            SpatialIntentPattern(
                pattern=r"slow|performance|speed|optimize|optimization|metrics",
                intent_category=IntentCategory.ANALYSIS,
                action="analyze_metrics",
                confidence=0.8,
                keywords=["slow", "performance", "speed", "optimize", "metrics"],
            ),
            # Strategic discussions
            SpatialIntentPattern(
                pattern=r"strategy|plan|roadmap|vision|goals|objectives",
                intent_category=IntentCategory.PLANNING,
                action="plan_strategy",
                confidence=0.8,
                keywords=["strategy", "plan", "roadmap", "vision", "goals"],
            ),
            # Feedback and opinions
            SpatialIntentPattern(
                pattern=r"feedback|opinion|thoughts|suggest|recommend|like|dislike",
                intent_category=IntentCategory.ANALYSIS,
                action="analyze_feedback",
                confidence=0.7,
                keywords=["feedback", "opinion", "thoughts", "suggest", "recommend"],
            ),
            # Review requests
            SpatialIntentPattern(
                pattern=r"review|check|examine|look.*at|verify|validate",
                intent_category=IntentCategory.REVIEW,
                action="review_item",
                confidence=0.8,
                keywords=["review", "check", "examine", "verify", "validate"],
            ),
            # Learning and patterns
            SpatialIntentPattern(
                pattern=r"learn|pattern|trend|insight|discover|understand",
                intent_category=IntentCategory.LEARNING,
                action="learn_pattern",
                confidence=0.7,
                keywords=["learn", "pattern", "trend", "insight", "discover"],
            ),
            # Urgent requests
            SpatialIntentPattern(
                pattern=r"urgent|emergency|critical|asap|immediately|now",
                intent_category=IntentCategory.EXECUTION,
                action="create_ticket",
                confidence=0.9,
                keywords=["urgent", "emergency", "critical", "asap", "immediately"],
            ),
            # Questions
            SpatialIntentPattern(
                pattern=r"\?|question|what|how|why|when|where",
                intent_category=IntentCategory.ANALYSIS,
                action="generate_report",
                confidence=0.6,
                keywords=["?", "question", "what", "how", "why", "when", "where"],
            ),
        ]

    def classify_spatial_event(
        self,
        event_result: EventProcessingResult,
        navigation_decision: NavigationDecision,
        message_text: str = "",
    ) -> IntentClassificationResult:
        """Classify spatial event as intent"""
        try:
            # Extract text content from spatial event
            text_content = self._extract_text_content(event_result, message_text)

            # Find matching patterns
            best_pattern = self._find_best_pattern(text_content, event_result, navigation_decision)

            if not best_pattern:
                # Default classification for unknown patterns
                return self._create_default_classification(event_result, navigation_decision)

            # Create intent from pattern
            intent = self._create_intent_from_pattern(
                best_pattern, event_result, navigation_decision, text_content
            )

            # Create spatial context
            spatial_context = self._create_spatial_context(event_result, navigation_decision)

            return IntentClassificationResult(
                intent=intent,
                confidence=best_pattern.confidence,
                spatial_context=spatial_context,
                classification_reason=f"Matched pattern: {best_pattern.pattern}",
                patterns_matched=[best_pattern.pattern],
            )

        except Exception as e:
            self.logger.error(f"Error classifying spatial event: {e}")
            return self._create_default_classification(event_result, navigation_decision)

    def _extract_text_content(self, event_result: EventProcessingResult, message_text: str) -> str:
        """Extract text content from spatial event"""
        if message_text:
            return message_text.lower()

        # Try to extract from spatial changes
        if event_result.spatial_changes:
            for change in event_result.spatial_changes:
                if "content" in change:
                    return change["content"].lower()
                elif "content_preview" in change:
                    return change["content_preview"].lower()

        # Try to extract from spatial event
        if event_result.spatial_event and hasattr(event_result.spatial_event, "spatial_object"):
            spatial_object = event_result.spatial_event.spatial_object
            if hasattr(spatial_object, "content"):
                return spatial_object.content.lower()

        return ""

    def _find_best_pattern(
        self,
        text_content: str,
        event_result: EventProcessingResult,
        navigation_decision: NavigationDecision,
    ) -> Optional[SpatialIntentPattern]:
        """Find the best matching pattern for the text content"""
        best_pattern = None
        best_score = 0.0

        for pattern in self.intent_patterns:
            score = self._calculate_pattern_score(
                pattern, text_content, event_result, navigation_decision
            )

            if score > best_score:
                best_score = score
                best_pattern = pattern

        # Only return pattern if score is above threshold
        if best_score >= 0.5:
            return best_pattern

        return None

    def _calculate_pattern_score(
        self,
        pattern: SpatialIntentPattern,
        text_content: str,
        event_result: EventProcessingResult,
        navigation_decision: NavigationDecision,
    ) -> float:
        """Calculate how well a pattern matches the content"""
        score = 0.0

        # Pattern matching
        if re.search(pattern.pattern, text_content, re.IGNORECASE):
            score += 0.4

        # Keyword matching
        keyword_matches = sum(
            1 for keyword in pattern.keywords if keyword.lower() in text_content.lower()
        )
        if keyword_matches > 0:
            score += (keyword_matches / len(pattern.keywords)) * 0.3

        # Attention level bonus
        if event_result.attention_level.value == "high":
            score += 0.2

        # Navigation intent bonus
        if navigation_decision.intent.value in ["respond", "investigate"]:
            score += 0.1

        return min(score, 1.0)

    def _create_intent_from_pattern(
        self,
        pattern: SpatialIntentPattern,
        event_result: EventProcessingResult,
        navigation_decision: NavigationDecision,
        text_content: str,
    ) -> Intent:
        """Create intent from matched pattern"""
        context = {
            "original_message": text_content,
            "spatial_event_type": (
                event_result.spatial_event.event_type if event_result.spatial_event else "unknown"
            ),
            "attention_level": event_result.attention_level.value,
            "emotional_valence": event_result.emotional_valence.value,
            "navigation_intent": navigation_decision.intent.value,
            "pattern_matched": pattern.pattern,
            "classification_confidence": pattern.confidence,
        }

        return Intent(
            category=pattern.intent_category,
            action=pattern.action,
            context=context,
            confidence=pattern.confidence,
        )

    def _create_spatial_context(
        self, event_result: EventProcessingResult, navigation_decision: NavigationDecision
    ) -> Dict[str, Any]:
        """Create spatial context for classification result"""
        return {
            "spatial_event_type": (
                event_result.spatial_event.event_type if event_result.spatial_event else "unknown"
            ),
            "attention_level": event_result.attention_level.value,
            "emotional_valence": event_result.emotional_valence.value,
            "navigation_intent": navigation_decision.intent.value,
            "navigation_confidence": navigation_decision.confidence,
            "spatial_changes": event_result.spatial_changes,
            "classification_timestamp": datetime.now().isoformat(),
        }

    def _create_default_classification(
        self, event_result: EventProcessingResult, navigation_decision: NavigationDecision
    ) -> IntentClassificationResult:
        """Create default classification for unknown patterns"""
        intent = Intent(
            category=IntentCategory.UNKNOWN,
            action="process_spatial_event",
            context={
                "original_message": "Spatial event without clear intent",
                "spatial_event_type": (
                    event_result.spatial_event.event_type
                    if event_result.spatial_event
                    else "unknown"
                ),
                "attention_level": event_result.attention_level.value,
                "navigation_intent": navigation_decision.intent.value,
            },
            confidence=0.3,
        )

        spatial_context = self._create_spatial_context(event_result, navigation_decision)

        return IntentClassificationResult(
            intent=intent,
            confidence=0.3,
            spatial_context=spatial_context,
            classification_reason="No pattern matched, using default classification",
            patterns_matched=[],
        )

    def add_intent_pattern(self, pattern: SpatialIntentPattern):
        """Add a new intent pattern"""
        self.intent_patterns.append(pattern)
        self.logger.info(f"Added intent pattern: {pattern.pattern} -> {pattern.action}")

    def get_intent_patterns(self) -> List[SpatialIntentPattern]:
        """Get all intent patterns"""
        return self.intent_patterns.copy()

    def get_classification_stats(self) -> Dict[str, Any]:
        """Get statistics about intent classification patterns"""
        return {
            "total_patterns": len(self.intent_patterns),
            "intent_categories": list(
                set(pattern.intent_category.value for pattern in self.intent_patterns)
            ),
            "actions": list(set(pattern.action for pattern in self.intent_patterns)),
            "confidence_distribution": {
                "high": len([p for p in self.intent_patterns if p.confidence >= 0.8]),
                "medium": len([p for p in self.intent_patterns if 0.6 <= p.confidence < 0.8]),
                "low": len([p for p in self.intent_patterns if p.confidence < 0.6]),
            },
            "pattern_types": {
                "help_requests": len([p for p in self.intent_patterns if "help" in p.keywords]),
                "bug_reports": len(
                    [
                        p
                        for p in self.intent_patterns
                        if "bug" in p.keywords or "error" in p.keywords
                    ]
                ),
                "feature_requests": len(
                    [p for p in self.intent_patterns if "feature" in p.keywords]
                ),
                "status_updates": len(
                    [
                        p
                        for p in self.intent_patterns
                        if "status" in p.keywords or "update" in p.keywords
                    ]
                ),
                "questions": len(
                    [
                        p
                        for p in self.intent_patterns
                        if "?" in p.keywords or "question" in p.keywords
                    ]
                ),
            },
        }

    def classify_batch(
        self, events: List[Tuple[EventProcessingResult, NavigationDecision, str]]
    ) -> List[IntentClassificationResult]:
        """Classify multiple spatial events as intents"""
        results = []

        for event_result, navigation_decision, message_text in events:
            result = self.classify_spatial_event(event_result, navigation_decision, message_text)
            results.append(result)

        return results

    def create_spatial_context_from_event(
        self,
        spatial_event: Any,
        navigation_intent: str,
        user_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create spatial context dictionary from spatial event"""
        return {
            "event_type": spatial_event.event_type,
            "coordinates": {
                "room_id": spatial_event.coordinates.room_id,
                "territory_id": spatial_event.coordinates.territory_id,
                "path_id": getattr(spatial_event.coordinates, "path_id", None),
                "object_position": getattr(spatial_event.coordinates, "object_position", None),
            },
            "navigation_intent": navigation_intent,
            "user_context": user_context,
            "timestamp": (
                getattr(spatial_event, "event_time", datetime.now()).isoformat()
                if hasattr(getattr(spatial_event, "event_time", datetime.now()), "isoformat")
                else str(getattr(spatial_event, "event_time", datetime.now()))
            ),
        }

    def convert_spatial_context_to_dict(self, spatial_context: Dict[str, Any]) -> Dict[str, Any]:
        """Convert spatial context to dictionary format for IntentClassifier"""
        return {
            "room_id": spatial_context.get("coordinates", {}).get("room_id"),
            "territory_id": spatial_context.get("coordinates", {}).get("territory_id"),
            "path_id": spatial_context.get("coordinates", {}).get("path_id"),
            "spatial_event_type": spatial_context.get("event_type"),
            "navigation_intent": spatial_context.get("navigation_intent"),
            "user_context": spatial_context.get("user_context", {}),
        }
