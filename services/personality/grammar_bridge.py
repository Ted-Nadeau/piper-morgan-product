"""
Personality Grammar Bridge - Transform context into grammar-conscious phrases.

This module provides situation-aware, personality-calibrated phrases
that make Piper's responses feel consistent and human.

Issue #627: GRAMMAR-TRANSFORM: Personality System
Phase 2: Narrative Bridge
"""

from dataclasses import dataclass
from typing import Optional

from services.personality.grammar_context import (
    GrammarLens,
    PersonalityGrammarContext,
    SituationType,
)


@dataclass
class PersonalityGrammarBridge:
    """Transform personality context into grammar-conscious phrases.

    In MUX grammar: this bridges personality preferences to human expression.
    The goal is consistent Piper voice that adapts to situation and preference.
    """

    # Greeting phrases by formality
    GREETINGS = {
        "warm": [
            "Hey there!",
            "Good to see you!",
            "Hi! Great to connect.",
        ],
        "conversational": [
            "Hi!",
            "Hello!",
            "Hey!",
        ],
        "professional": [
            "Hello.",
            "Good to hear from you.",
        ],
        "terse": [
            "Hi.",
        ],
    }

    # Situation acknowledgments
    SITUATION_PHRASES = {
        SituationType.SUCCESS: {
            "warm": "That worked out well!",
            "conversational": "That went through.",
            "professional": "Completed successfully.",
            "terse": "Done.",
        },
        SituationType.ERROR: {
            "warm": "I ran into something there.",
            "conversational": "Something went wrong.",
            "professional": "An error occurred.",
            "terse": "Error.",
        },
        SituationType.CLARIFICATION: {
            "warm": "I want to make sure I understand.",
            "conversational": "Let me clarify.",
            "professional": "For clarification:",
            "terse": "Clarify:",
        },
        SituationType.BUSY: {
            "warm": "I'll keep this quick.",
            "conversational": "Briefly:",
            "professional": "Summary:",
            "terse": "",  # No preamble when terse
        },
    }

    # Relationship phrases
    FIRST_INTERACTION_PHRASES = {
        "warm": "Nice to meet you! I'm Piper, your PM assistant.",
        "conversational": "Hi, I'm Piper. I'm here to help with PM tasks.",
        "professional": "I'm Piper, your project management assistant.",
        "terse": "I'm Piper.",
    }

    RETURNING_USER_PHRASES = {
        "warm": "Good to see you again!",
        "conversational": "Welcome back!",
        "professional": "Hello again.",
        "terse": "",
    }

    # Closing phrases
    CLOSING_PHRASES = {
        "warm": "Anything else I can help with?",
        "conversational": "Need anything else?",
        "professional": "Let me know if you need further assistance.",
        "terse": "",
    }

    # Error gentleness by warmth
    ERROR_PHRASES = {
        "warm": [
            "I want to help, but something's not quite right.",
            "Let me try to work through this.",
            "I'm having a bit of trouble there.",
        ],
        "conversational": [
            "Something went wrong.",
            "That didn't work as expected.",
            "I ran into an issue.",
        ],
        "professional": [
            "An error occurred.",
            "The operation was unsuccessful.",
            "A problem was encountered.",
        ],
        "terse": [
            "Error.",
            "Failed.",
        ],
    }

    # Confidence expressions
    CONFIDENCE_PHRASES = {
        "high": {  # >= 0.9
            "warm": "I'm pretty confident about this.",
            "conversational": "I'm fairly sure.",
            "professional": "With high confidence:",
            "terse": "",
        },
        "medium": {  # 0.7-0.9
            "warm": "I think this is right, but let me know if it seems off.",
            "conversational": "I believe this is correct.",
            "professional": "This appears to be accurate.",
            "terse": "",
        },
        "low": {  # < 0.7
            "warm": "I'm not entirely sure, but here's what I found.",
            "conversational": "I'm uncertain about this.",
            "professional": "This requires verification.",
            "terse": "Uncertain.",
        },
    }

    def get_greeting(self, ctx: PersonalityGrammarContext) -> str:
        """Get appropriate greeting for context.

        Examples:
            Warm + first interaction -> "Hey there! Nice to meet you!"
            Professional + returning -> "Hello again."
        """
        formality = ctx.get_formality()
        greetings = self.GREETINGS.get(formality, self.GREETINGS["conversational"])

        greeting = greetings[0]  # Use first option

        # Add relationship context
        if ctx.is_first_interaction:
            intro = self.FIRST_INTERACTION_PHRASES.get(formality, "")
            if intro:
                return f"{greeting} {intro}"
        else:
            returning = self.RETURNING_USER_PHRASES.get(formality, "")
            if returning:
                return returning

        return greeting

    def get_situation_phrase(self, ctx: PersonalityGrammarContext) -> str:
        """Get phrase appropriate for current situation.

        Examples:
            Error + warm -> "I ran into something there."
            Success + terse -> "Done."
        """
        formality = ctx.get_formality()
        situation_phrases = self.SITUATION_PHRASES.get(ctx.situation, {})

        return situation_phrases.get(formality, "")

    def get_error_phrase(self, ctx: PersonalityGrammarContext) -> str:
        """Get appropriately gentle error phrase.

        Error warmth is boosted in context, so this reflects
        the effective warmth level.
        """
        formality = ctx.get_formality()
        phrases = self.ERROR_PHRASES.get(formality, self.ERROR_PHRASES["conversational"])

        return phrases[0]  # Use first option

    def get_confidence_phrase(
        self,
        ctx: PersonalityGrammarContext,
        confidence: float,
    ) -> str:
        """Get confidence expression based on level and preferences.

        Args:
            ctx: Personality context
            confidence: Confidence level (0.0-1.0)

        Returns:
            Appropriate confidence phrase or empty string
        """
        # Hidden confidence style: don't express confidence
        from services.personality.personality_profile import ConfidenceDisplayStyle

        if ctx.confidence_style == ConfidenceDisplayStyle.HIDDEN:
            return ""

        formality = ctx.get_formality()

        if confidence >= 0.9:
            level_phrases = self.CONFIDENCE_PHRASES["high"]
        elif confidence >= 0.7:
            level_phrases = self.CONFIDENCE_PHRASES["medium"]
        else:
            level_phrases = self.CONFIDENCE_PHRASES["low"]

        return level_phrases.get(formality, "")

    def get_closing(self, ctx: PersonalityGrammarContext) -> str:
        """Get appropriate closing phrase.

        Examples:
            Warm -> "Anything else I can help with?"
            Terse -> ""
        """
        formality = ctx.get_formality()
        return self.CLOSING_PHRASES.get(formality, "")

    def get_lens_phrase(
        self,
        ctx: PersonalityGrammarContext,
        lens: GrammarLens,
    ) -> str:
        """Get phrase that reflects active lens.

        Args:
            ctx: Personality context
            lens: Grammar lens to reflect

        Returns:
            Lens-appropriate phrase or empty string
        """
        if not ctx.has_lens(lens):
            return ""

        formality = ctx.get_formality()

        lens_phrases = {
            GrammarLens.COLLABORATIVE: {
                "warm": "Working together on this,",
                "conversational": "Together,",
                "professional": "Collaboratively,",
                "terse": "",
            },
            GrammarLens.TEMPORAL: {
                "warm": "I know time is tight, so",
                "conversational": "Quickly,",
                "professional": "Given the time constraints,",
                "terse": "",
            },
            GrammarLens.EPISTEMIC: {
                "warm": "I want to be upfront about what I don't know -",
                "conversational": "To be clear,",
                "professional": "For clarity,",
                "terse": "",
            },
            GrammarLens.SPATIAL: {
                "warm": "Looking at the bigger picture,",
                "conversational": "In context,",
                "professional": "Considering the scope,",
                "terse": "",
            },
        }

        lens_options = lens_phrases.get(lens, {})
        return lens_options.get(formality, "")

    def narrate_relationship(self, ctx: PersonalityGrammarContext) -> str:
        """Describe the user-Piper relationship context.

        Examples:
            First interaction -> "first time chatting"
            Many interactions -> "we've worked together before"
        """
        if ctx.is_first_interaction:
            return "first time chatting"
        elif ctx.interaction_count >= 10:
            return "we've been working together a while"
        elif ctx.interaction_count >= 3:
            return "we've chatted a few times"
        else:
            return "we've talked before"

    def apply_personality_to_message(
        self,
        message: str,
        ctx: PersonalityGrammarContext,
        include_greeting: bool = False,
        include_closing: bool = False,
    ) -> str:
        """Apply personality context to a message.

        This is the main method for adding personality to any response.

        Args:
            message: The base message to enhance
            ctx: Personality context
            include_greeting: Whether to add greeting
            include_closing: Whether to add closing

        Returns:
            Personality-enhanced message
        """
        if not ctx.personality_available:
            return message

        parts = []

        # Add greeting if requested
        if include_greeting:
            greeting = self.get_greeting(ctx)
            if greeting:
                parts.append(greeting)

        # Add situation phrase if relevant
        if ctx.situation != SituationType.NORMAL:
            situation = self.get_situation_phrase(ctx)
            if situation:
                parts.append(situation)

        # Add the main message
        parts.append(message)

        # Add closing if requested
        if include_closing:
            closing = self.get_closing(ctx)
            if closing:
                parts.append(closing)

        return " ".join(filter(None, parts))
