"""
Predictive assistance for intelligent automation.

Leverages learned patterns to predict next actions, suggest smart defaults,
and pre-populate fields.

Issue: #225 (CORE-LEARN-E)
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from services.domain.user_preference_manager import UserPreferenceManager
from services.learning.query_learning_loop import PatternType, QueryLearningLoop


@dataclass
class PredictionResult:
    """Result of a prediction."""

    action_type: str
    confidence: float
    suggested_params: Dict[str, Any]
    reasoning: str
    pattern_source: str  # Which pattern type was used


class PredictiveAssistant:
    """
    Predictive assistance for automation.

    Leverages existing infrastructure:
    - QueryLearningLoop (610 lines) for learned patterns
    - UserPreferenceManager (762 lines) for smart defaults

    Note: PatternRecognitionService integration available via database session
    when needed (requires AsyncSession parameter).
    """

    def __init__(self):
        self.learning_loop = QueryLearningLoop()
        self.preference_manager = UserPreferenceManager()

    async def predict_next_action(
        self, user_id: str, context: Dict[str, Any]
    ) -> Optional[PredictionResult]:
        """
        Predict the next likely action based on learned patterns.

        Args:
            user_id: User ID for personalized prediction
            context: Current context (e.g., current_task, recent_actions)

        Returns:
            PredictionResult if prediction found, None otherwise
        """
        # Try workflow patterns first (most specific)
        workflow_patterns = await self.learning_loop.get_patterns_for_feature(
            source_feature="automation", min_confidence=0.7
        )

        for pattern in workflow_patterns:
            if pattern.pattern_type != PatternType.WORKFLOW_PATTERN:
                continue

            # Check if pattern matches current context
            if self._matches_context(pattern.pattern_data, context):
                return PredictionResult(
                    action_type=pattern.pattern_data.get("next_action", "unknown"),
                    confidence=pattern.confidence,
                    suggested_params=pattern.pattern_data.get("params", {}),
                    reasoning=f"Based on workflow pattern: {pattern.pattern_data.get('description', 'learned sequence')}",
                    pattern_source="WORKFLOW_PATTERN",
                )

        # Try user preference patterns (personalized)
        user_patterns = await self.learning_loop.get_patterns_for_feature(
            source_feature="automation", min_confidence=0.6
        )

        for pattern in user_patterns:
            if pattern.pattern_type != PatternType.USER_PREFERENCE_PATTERN:
                continue

            if self._matches_context(pattern.pattern_data, context):
                return PredictionResult(
                    action_type=pattern.pattern_data.get("preferred_action", "unknown"),
                    confidence=pattern.confidence,
                    suggested_params=pattern.pattern_data.get("params", {}),
                    reasoning=f"Based on user preferences: {pattern.pattern_data.get('description', 'learned preference')}",
                    pattern_source="USER_PREFERENCE_PATTERN",
                )

        # No high-confidence prediction found
        return None

    async def suggest_smart_defaults(
        self, user_id: str, action_type: str, context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Suggest smart defaults for an action based on user preferences.

        Args:
            user_id: User ID for personalized defaults
            action_type: Type of action being performed
            context: Optional context for more specific defaults

        Returns:
            Dictionary of suggested default values
        """
        defaults = {}

        # Get user preferences for this action type
        # Use existing UserPreferenceManager infrastructure
        try:
            # Check for action-specific preferences
            pref_key = f"default_{action_type.lower()}_params"
            action_defaults = await self.preference_manager.get_preference(user_id, pref_key)

            if action_defaults:
                defaults.update(action_defaults)

        except Exception:
            # No preferences set, use learned patterns
            pass

        # Enhance with learned patterns
        patterns = await self.learning_loop.get_patterns_for_feature(
            source_feature="automation", min_confidence=0.7
        )

        for pattern in patterns:
            if pattern.pattern_type == PatternType.USER_PREFERENCE_PATTERN:
                pattern_action = pattern.pattern_data.get("action_type", "")
                if pattern_action.lower() == action_type.lower():
                    # Merge pattern defaults
                    pattern_defaults = pattern.pattern_data.get("defaults", {})
                    # Don't override explicitly set preferences
                    for key, value in pattern_defaults.items():
                        if key not in defaults:
                            defaults[key] = value

        return defaults

    async def pre_populate_fields(
        self,
        user_id: str,
        form_type: str,
        existing_values: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Pre-populate form fields based on learned patterns and preferences.

        Args:
            user_id: User ID for personalized pre-population
            form_type: Type of form (e.g., "github_issue", "slack_message")
            existing_values: Already-provided values (won't be overwritten)

        Returns:
            Dictionary of pre-populated field values
        """
        populated = existing_values.copy() if existing_values else {}

        # Get smart defaults for this form type
        defaults = await self.suggest_smart_defaults(
            user_id, form_type, context={"form_type": form_type}
        )

        # Apply defaults for unpopulated fields only
        for field, value in defaults.items():
            if field not in populated:
                populated[field] = value

        # Look for form-specific patterns
        patterns = await self.learning_loop.get_patterns_for_feature(
            source_feature="automation", min_confidence=0.7
        )

        for pattern in patterns:
            if pattern.pattern_type == PatternType.COMMUNICATION_PATTERN:
                # Check if this pattern applies to this form type
                if pattern.pattern_data.get("form_type") == form_type:
                    pattern_fields = pattern.pattern_data.get("fields", {})
                    for field, value in pattern_fields.items():
                        if field not in populated:
                            populated[field] = value

        return populated

    def _matches_context(self, pattern_data: Dict, context: Dict) -> bool:
        """
        Check if pattern matches current context.

        Args:
            pattern_data: Pattern data to check
            context: Current context

        Returns:
            True if pattern matches context, False otherwise
        """
        # Simple context matching - can be enhanced
        pattern_context = pattern_data.get("context", {})

        if not pattern_context:
            # No context requirement, always matches
            return True

        # Check if all pattern context keys match current context
        for key, value in pattern_context.items():
            if context.get(key) != value:
                return False

        return True


# Global predictive assistant instance
_predictive_assistant: Optional[PredictiveAssistant] = None


def get_predictive_assistant() -> PredictiveAssistant:
    """Get global predictive assistant instance."""
    global _predictive_assistant
    if _predictive_assistant is None:
        _predictive_assistant = PredictiveAssistant()
    return _predictive_assistant
