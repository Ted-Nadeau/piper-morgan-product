"""
Personality-Enhanced Template System

Integrates with ResponsePersonalityEnhancer to provide warm, confident, actionable responses.
Built on existing TemplateRenderer with personality injection layer.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .action_humanizer import ActionHumanizer

# Import from existing template system
from .templates import DEFAULT_TEMPLATES, INTENT_BASED_TEMPLATES, WORKFLOW_BASED_TEMPLATES

logger = logging.getLogger(__name__)


@dataclass
class PersonalityConfig:
    """Basic personality configuration for template enhancement"""

    warmth_level: float = 0.7  # 0.0-1.0
    confidence_style: str = "contextual"  # numeric/descriptive/contextual/hidden
    action_orientation: str = "high"  # high/medium/low
    technical_depth: str = "balanced"  # detailed/balanced/simplified


class PersonalityEnhancedTemplates:
    """Enhanced templates with personality injection"""

    def __init__(self):
        # Enhanced templates with personality variants
        self.personality_enhanced_templates = {
            # ANALYSIS intents - warm, confident variations
            ("analysis", "investigate_issue"): {
                "professional": "Here's my analysis of the reported issue:",
                "warm": "I've analyzed this issue thoroughly—here's what I found:",
                "confident": "Based on the data, here's my comprehensive analysis:",
                "actionable": "I've investigated this issue and have clear recommendations:",
            },
            # EXECUTION intents - encouraging, action-oriented
            ("execution", "create_ticket"): {
                "professional": "✅ Successfully created GitHub issue #{issue_number}:",
                "warm": "✅ Perfect! I've created issue #{issue_number} and it's ready to go:",
                "confident": "✅ Issue #{issue_number} created successfully with all details:",
                "actionable": "✅ Created issue #{issue_number}—next step is to assign and prioritize:",
            },
            # QUERY intents - helpful, engaging
            ("query", "list_projects"): {
                "professional": "Here are your projects:",
                "warm": "Here are your projects—looking great!",
                "confident": "Based on your recent activity, here are your active projects:",
                "actionable": "Here are your projects with recommended next steps:",
            },
            # ERROR templates - supportive, solution-oriented
            ("error", "general"): {
                "professional": "I encountered an issue: {error}",
                "warm": "I ran into a small issue, but let me try a different approach: {error}",
                "confident": "I'm working through a temporary issue: {error}",
                "actionable": "I hit a snag ({error}), but here's what we can do next:",
            },
        }

    def get_personality_template(
        self, category: str, action: str, personality_config: PersonalityConfig
    ) -> str:
        """Get personality-enhanced template based on user preferences"""
        template_key = (category, action)

        # Check if we have personality variants for this template
        if template_key in self.personality_enhanced_templates:
            variants = self.personality_enhanced_templates[template_key]

            # Select variant based on personality configuration
            if personality_config.warmth_level >= 0.8:
                return variants.get("warm", variants.get("professional", ""))
            elif personality_config.action_orientation == "high":
                return variants.get("actionable", variants.get("professional", ""))
            elif personality_config.confidence_style in ["contextual", "descriptive"]:
                return variants.get("confident", variants.get("professional", ""))
            else:
                return variants.get("professional", "")

        # Fallback to original templates
        return INTENT_BASED_TEMPLATES.get(template_key, DEFAULT_TEMPLATES.get("success", ""))


class PersonalityTemplateRenderer:
    """Template renderer with personality enhancement integration"""

    def __init__(self, humanizer: Optional[ActionHumanizer] = None):
        self.humanizer = humanizer
        self.personality_templates = PersonalityEnhancedTemplates()

    async def render_with_personality(
        self,
        template_key: tuple,
        personality_config: PersonalityConfig,
        intent_action: str = "",
        intent_category: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Render template with personality enhancement"""

        category, action = template_key

        # Get personality-enhanced template
        template = self.personality_templates.get_personality_template(
            category, action, personality_config
        )

        # Add confidence indicators based on style
        if "confidence" in kwargs and personality_config.confidence_style != "hidden":
            confidence = kwargs.get("confidence", 0.5)
            confidence_text = self._format_confidence(
                confidence, personality_config.confidence_style
            )
            if confidence_text:
                template = f"{template} ({confidence_text})"

        # Humanize actions if needed
        if "{human_action}" in template and self.humanizer:
            human_action = await self.humanizer.humanize(intent_action, intent_category)
            kwargs["human_action"] = human_action

        # Always preserve original action
        kwargs["action"] = intent_action

        # Format template with provided data
        try:
            return template.format(**kwargs)
        except KeyError as e:
            logger.warning(f"Template formatting error: {e}, using fallback")
            return template

    def _format_confidence(self, confidence: float, style: str) -> str:
        """Format confidence indicator based on display style"""
        if style == "hidden":
            return ""
        elif style == "numeric":
            return f"{int(confidence * 100)}% confident"
        elif style == "descriptive":
            if confidence >= 0.8:
                return "high confidence"
            elif confidence >= 0.6:
                return "moderate confidence"
            else:
                return "limited visibility"
        elif style == "contextual":
            if confidence >= 0.8:
                return "based on recent patterns"
            elif confidence >= 0.6:
                return "from available data"
            else:
                return "with current information"
        return ""


# Enhanced template examples for different personality levels
PERSONALITY_EXAMPLES = {
    "warmth_0.3": {
        "analysis": "Analysis complete. Results attached.",
        "execution": "✅ Task completed successfully.",
        "error": "Error encountered: {error}",
    },
    "warmth_0.7": {
        "analysis": "I've analyzed this thoroughly—here's what I found:",
        "execution": "✅ Perfect! Your task is complete and ready for the next step.",
        "error": "I ran into an issue, but let me try a different approach: {error}",
    },
    "warmth_1.0": {
        "analysis": "Great question! I've dug into this and have some exciting insights:",
        "execution": "✅ Fantastic! Everything's done and looking great—you're all set!",
        "error": "Oops, hit a small bump ({error}), but no worries—I've got a backup plan!",
    },
}
