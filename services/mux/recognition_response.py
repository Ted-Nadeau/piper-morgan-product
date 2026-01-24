"""
Recognition Response Service.

Formats recognition options for user presentation across different channels.
Part of #411 MUX-INTERACT-RECOGNITION.

This service builds on the RecognitionOptions from #410's orientation system
to create the user-facing recognition experience.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple

from services.mux.orientation import (
    ArticulationConfig,
    ChannelType,
    RecognitionOption,
    RecognitionOptions,
)


class SelectionResult(Enum):
    """Result of attempting to match a user selection."""

    MATCHED = "matched"  # Successfully matched an option
    NONE_OF_THESE = "none"  # User explicitly chose "none of these"
    NO_MATCH = "no_match"  # Couldn't match selection to any option
    NUMERIC_OUT_OF_RANGE = "numeric_out_of_range"  # Number doesn't match option count


@dataclass
class SelectionMatch:
    """Result of selection matching."""

    result: SelectionResult
    matched_option: Optional[RecognitionOption] = None
    intent_hint: Optional[str] = None


class RecognitionResponseService:
    """
    Service for formatting recognition options and handling user selections.

    Recognition > Recall: ~50% of users struggle to articulate precise queries.
    This service helps them recognize from context-aware options.

    CXO Guidance (2026-01-23):
    - Use Option C (narrative) framing
    - 2-4 options max
    - Include escape hatch at Stage 1-2
    - Use open language ("Which feels most useful?" not "Select one")
    """

    # Phrases that indicate "none of these"
    NONE_OF_THESE_PHRASES = [
        "none",
        "something else",
        "none of these",
        "neither",
        "other",
        "different",
        "not these",
        "nope",
        "no thanks",
    ]

    # Trust-aware language patterns
    TRUST_STAGE_LANGUAGE = {
        # Stage 1-2: More cautious, explicit offering
        1: {
            "intro_prefix": "I can help with a few things:",
            "call_to_action": "Which would be helpful?",
            "selection_ack": "Got it!",
            "none_response": "Sure! What would be most helpful right now?",
        },
        2: {
            "intro_prefix": "I can help with a few things:",
            "call_to_action": "Which would be helpful?",
            "selection_ack": "Got it!",
            "none_response": "Sure! What would be most helpful right now?",
        },
        # Stage 3-4: More confident, assumptive
        3: {
            "intro_prefix": "I see a few things that might help:",
            "call_to_action": "Which feels most useful?",
            "selection_ack": "On it.",
            "none_response": "What would help most?",
        },
        4: {
            "intro_prefix": "Here's what I'm seeing:",
            "call_to_action": "Want me to start with one of these?",
            "selection_ack": "On it.",
            "none_response": "What did you have in mind?",
        },
    }

    @classmethod
    def format_for_channel(
        cls,
        recognition: RecognitionOptions,
        config: Optional[ArticulationConfig] = None,
    ) -> str:
        """
        Format recognition options based on channel type.

        Delegates to channel-specific formatters.
        """
        if config is None:
            config = ArticulationConfig()

        if config.channel == ChannelType.SLACK:
            return cls.format_for_slack(recognition, config)
        elif config.channel == ChannelType.CLI:
            return cls.format_for_cli(recognition, config)
        else:
            # Web and API use full narrative format
            return cls.format_for_web(recognition, config)

    @classmethod
    def format_for_web(
        cls,
        recognition: RecognitionOptions,
        config: Optional[ArticulationConfig] = None,
    ) -> str:
        """
        Format for web interface - full narrative with explanation.

        Example:
        "I can help with a few things:

        • Your standup status (meeting in 45 min)
        • The API PR waiting for review
        • Your todo list for today

        Which would be helpful? Or something else entirely?"
        """
        if config is None:
            config = ArticulationConfig()

        trust_stage = min(config.trust_stage, 4)  # Cap at 4
        language = cls.TRUST_STAGE_LANGUAGE.get(trust_stage, cls.TRUST_STAGE_LANGUAGE[1])

        # Build the response
        parts = []

        # Use narrative frame if provided, otherwise use trust-appropriate intro
        if recognition.narrative_frame:
            parts.append(recognition.narrative_frame)
        else:
            parts.append(language["intro_prefix"])

        parts.append("")  # Blank line

        # Add options as bullet points
        for option in recognition.options:
            if option.description:
                parts.append(f"• {option.label} ({option.description})")
            else:
                parts.append(f"• {option.label}")

        parts.append("")  # Blank line

        # Add call to action
        cta = recognition.call_to_action or language["call_to_action"]

        # Add escape hatch if appropriate
        if config.should_include_escape_hatch and recognition.escape_hatch:
            parts.append(f"{cta} {recognition.escape_hatch}")
        else:
            parts.append(cta)

        return "\n".join(parts)

    @classmethod
    def format_for_slack(
        cls,
        recognition: RecognitionOptions,
        config: Optional[ArticulationConfig] = None,
    ) -> str:
        """
        Format for Slack - compressed format with numbered options.

        Example:
        "I can check a few things:
        1. Standup status (meeting soon)
        2. API PR (waiting for review)
        3. Today's todos

        Which? (or something else)"
        """
        if config is None:
            config = ArticulationConfig(channel=ChannelType.SLACK)

        trust_stage = min(config.trust_stage, 4)
        language = cls.TRUST_STAGE_LANGUAGE.get(trust_stage, cls.TRUST_STAGE_LANGUAGE[1])

        parts = []

        # Compressed intro
        if recognition.narrative_frame:
            # Shorten the narrative frame for Slack
            frame = recognition.narrative_frame
            if len(frame) > 50:
                frame = frame[:47] + "..."
            parts.append(frame)
        else:
            parts.append(language["intro_prefix"])

        # Numbered options (Slack users can type number to select)
        for i, option in enumerate(recognition.options, 1):
            if option.description:
                # Shorter description for Slack
                desc = option.description
                if len(desc) > 30:
                    desc = desc[:27] + "..."
                parts.append(f"{i}. {option.label} ({desc})")
            else:
                parts.append(f"{i}. {option.label}")

        parts.append("")

        # Compressed CTA with escape hatch
        if config.should_include_escape_hatch and recognition.escape_hatch:
            parts.append(f"Which? ({recognition.escape_hatch.strip()})")
        else:
            parts.append("Which?")

        return "\n".join(parts)

    @classmethod
    def format_for_cli(
        cls,
        recognition: RecognitionOptions,
        config: Optional[ArticulationConfig] = None,
    ) -> str:
        """
        Format for CLI - similar to Slack, numbered for easy selection.
        """
        if config is None:
            config = ArticulationConfig(channel=ChannelType.CLI)

        # CLI uses same format as Slack
        return cls.format_for_slack(recognition, config)

    @classmethod
    def handle_selection(
        cls,
        selection: str,
        options: RecognitionOptions,
    ) -> SelectionMatch:
        """
        Handle user selection from recognition options.

        Matches:
        - Exact option label match
        - Partial match (prefix)
        - Numeric selection ("1", "2", etc.)
        - "None of these" phrases

        Returns SelectionMatch with result and matched option if found.
        """
        selection_clean = selection.strip().lower()

        # Empty input is no match
        if not selection_clean:
            return SelectionMatch(result=SelectionResult.NO_MATCH)

        # Check for "none of these" first
        if cls._is_none_of_these(selection_clean):
            return SelectionMatch(result=SelectionResult.NONE_OF_THESE)

        # Check for numeric selection
        numeric_match = cls._match_numeric(selection_clean, options)
        if numeric_match:
            return numeric_match

        # Check for text match (exact or partial)
        text_match = cls._match_text(selection_clean, options)
        if text_match:
            return text_match

        # No match found
        return SelectionMatch(result=SelectionResult.NO_MATCH)

    @classmethod
    def _is_none_of_these(cls, selection: str) -> bool:
        """Check if selection indicates 'none of these'."""
        return any(phrase in selection for phrase in cls.NONE_OF_THESE_PHRASES)

    @classmethod
    def _match_numeric(
        cls,
        selection: str,
        options: RecognitionOptions,
    ) -> Optional[SelectionMatch]:
        """Match numeric selection to option."""
        # Match single digit or number
        match = re.match(r"^(\d+)$", selection)
        if not match:
            return None

        num = int(match.group(1))

        # Check if in range (1-indexed)
        if num < 1 or num > len(options.options):
            return SelectionMatch(result=SelectionResult.NUMERIC_OUT_OF_RANGE)

        matched_option = options.options[num - 1]
        return SelectionMatch(
            result=SelectionResult.MATCHED,
            matched_option=matched_option,
            intent_hint=matched_option.intent_hint,
        )

    @classmethod
    def _match_text(
        cls,
        selection: str,
        options: RecognitionOptions,
    ) -> Optional[SelectionMatch]:
        """
        Match text selection to option.

        Tries:
        1. Exact label match
        2. Label starts with selection
        3. Selection starts with label word
        """
        # Exact match
        for option in options.options:
            if selection == option.label.lower():
                return SelectionMatch(
                    result=SelectionResult.MATCHED,
                    matched_option=option,
                    intent_hint=option.intent_hint,
                )

        # Partial match - label starts with selection
        for option in options.options:
            if option.label.lower().startswith(selection):
                return SelectionMatch(
                    result=SelectionResult.MATCHED,
                    matched_option=option,
                    intent_hint=option.intent_hint,
                )

        # Partial match - selection contains key word from label
        for option in options.options:
            label_words = option.label.lower().split()
            # Match if selection contains first significant word (skip articles)
            for word in label_words:
                if word in ("a", "an", "the", "my", "your"):
                    continue
                if word in selection or selection in word:
                    return SelectionMatch(
                        result=SelectionResult.MATCHED,
                        matched_option=option,
                        intent_hint=option.intent_hint,
                    )

        return None

    @classmethod
    def handle_none_of_these(
        cls,
        config: Optional[ArticulationConfig] = None,
    ) -> str:
        """
        Generate response for "none of these" selection.

        Prompts for clarification without penalizing trust.
        """
        if config is None:
            config = ArticulationConfig()

        trust_stage = min(config.trust_stage, 4)
        language = cls.TRUST_STAGE_LANGUAGE.get(trust_stage, cls.TRUST_STAGE_LANGUAGE[1])

        return language["none_response"]

    @classmethod
    def get_selection_acknowledgment(
        cls,
        matched_option: RecognitionOption,
        config: Optional[ArticulationConfig] = None,
    ) -> str:
        """
        Generate acknowledgment for successful selection.

        Brief acknowledgment before routing to handler.
        """
        if config is None:
            config = ArticulationConfig()

        trust_stage = min(config.trust_stage, 4)
        language = cls.TRUST_STAGE_LANGUAGE.get(trust_stage, cls.TRUST_STAGE_LANGUAGE[1])

        # Brief ack + label reference
        ack = language["selection_ack"]
        return f"{ack} Let me check on {matched_option.label.lower()}."

    @classmethod
    def format_reshow_options(
        cls,
        recognition: RecognitionOptions,
        config: Optional[ArticulationConfig] = None,
    ) -> str:
        """
        Format for re-showing options (e.g., after empty input).

        Slightly different framing to avoid sounding robotic.
        """
        if config is None:
            config = ArticulationConfig()

        # Use shorter intro for re-show
        parts = ["Here are those options again:"]
        parts.append("")

        for i, option in enumerate(recognition.options, 1):
            parts.append(f"{i}. {option.label}")

        parts.append("")
        parts.append("Just let me know which, or tell me what else would help.")

        return "\n".join(parts)
