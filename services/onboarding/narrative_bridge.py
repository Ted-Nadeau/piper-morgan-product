"""
Onboarding Narrative Bridge - Transform context into relationship-building phrases.

This module transforms onboarding context into warm, welcoming phrases that
establish Piper's relationship with the user. Onboarding is the FIRST MEETING -
a significant moment deserving conscious, warm communication.

Issue #626: GRAMMAR-TRANSFORM: Onboarding System
Phase 2: Narrative Bridge
"""

from dataclasses import dataclass
from typing import List, Optional

from services.onboarding.grammar_context import OnboardingGrammarContext, OnboardingStage


@dataclass
class OnboardingNarrativeBridge:
    """Transform onboarding context into relationship-building phrases.

    In MUX grammar: this bridges onboarding state to human expression,
    treating onboarding as the significant first meeting it is.
    """

    # Welcome messages - first meeting, relationship establishment
    WELCOME_MESSAGES = {
        "warm": (
            "Hi there! I'm Piper, and I'm really glad to meet you. "
            "I'm here to help you stay organized and on top of your projects."
        ),
        "conversational": (
            "Hello! I'm Piper, your PM assistant. "
            "I'm here to help you stay organized with your projects."
        ),
        "professional": (
            "Hello. I'm Piper, your project management assistant. "
            "I can help you track and organize your work."
        ),
    }

    # Place atmosphere - welcoming to workspace
    PLACE_ATMOSPHERE = {
        "warm": (
            "Since we're just getting to know each other, I'd love to learn "
            "about what you're working on."
        ),
        "conversational": (
            "To get started, could you tell me about the projects you're " "working on?"
        ),
        "professional": ("To begin, please share the projects you'd like me to help track."),
    }

    # Project acknowledgments - genuine interest, not just data capture
    FIRST_PROJECT_ACKNOWLEDGMENTS = {
        "warm": (
            "That sounds like a great project! I'd love to help you stay " "on track with it."
        ),
        "conversational": ("Nice! I'll help you stay organized with that."),
        "professional": ("Noted. I'll track that for you."),
    }

    ADDITIONAL_PROJECT_ACKNOWLEDGMENTS = {
        "warm": ("Oh, that's interesting too! I'm excited to help with both."),
        "conversational": ("Got it - I'll keep track of that one too."),
        "professional": ("Added. I'll track both projects."),
    }

    # Prompts for more projects
    MORE_PROJECTS_PROMPTS = {
        "warm": (
            "Are there any other projects you'd like me to know about? "
            "I'm happy to help with as many as you'd like."
        ),
        "conversational": ("Any other projects you're working on, or is that your main focus?"),
        "professional": ("Are there additional projects to add?"),
    }

    # Confirmation prompts
    CONFIRMATION_PROMPTS_SINGLE = {
        "warm": (
            "Should I add {project} to your portfolio? "
            "I'm looking forward to helping you with it!"
        ),
        "conversational": ("Should I save {project} to your portfolio?"),
        "professional": ("Confirm: Add {project} to portfolio?"),
    }

    CONFIRMATION_PROMPTS_MULTIPLE = {
        "warm": (
            "Should I add {projects} to your portfolio? "
            "I'm excited to help you with all of them!"
        ),
        "conversational": ("Should I save {projects} to your portfolio?"),
        "professional": ("Confirm: Add {projects} to portfolio?"),
    }

    # Completion celebrations - relationship established!
    COMPLETION_MESSAGES = {
        "warm": (
            "Wonderful! I've added {projects} to your portfolio. "
            "I'm really looking forward to working together - "
            "I'll help you stay on track with planning, coordination, and more. "
            "What would you like to focus on first?"
        ),
        "conversational": (
            "All set! I've added {projects} to your portfolio. "
            "I'll help you with planning, tracking, and coordination. "
            "What would you like to work on?"
        ),
        "professional": (
            "Portfolio updated with {projects}. "
            "I can assist with project planning and tracking. "
            "How can I help?"
        ),
    }

    # Decline handling - warm, door open
    DECLINE_MESSAGES = {
        "warm": (
            "No rush at all - I'll be here whenever you're ready! "
            "In the meantime, is there anything else I can help you with?"
        ),
        "conversational": (
            "No problem! Just let me know when you'd like to set things up. "
            "What can I help you with today?"
        ),
        "professional": (
            "Understood. You can set up your portfolio anytime. " "How can I assist you?"
        ),
    }

    # Decline with projects already captured
    DECLINE_WITH_PROJECTS_MESSAGES = {
        "warm": (
            "No worries - I won't save those for now. "
            "Whenever you're ready to set up your portfolio, just let me know. "
            "What else can I help you with today?"
        ),
        "conversational": (
            "Okay, I won't save those. Let me know if you change your mind. "
            "What can I help you with?"
        ),
        "professional": (
            "Projects not saved. Portfolio setup available anytime. " "How can I help?"
        ),
    }

    # Session lost recovery - warm error handling
    SESSION_LOST_MESSAGES = {
        "warm": (
            "I'm sorry, I seem to have lost track of where we were. "
            "Would you like to start fresh? I'm still here to help!"
        ),
        "conversational": (
            "I lost our conversation - my apologies. " "Would you like to start over?"
        ),
        "professional": ("Session interrupted. Would you like to restart?"),
    }

    # Nudge for at least one project
    NEED_PROJECT_MESSAGES = {
        "warm": (
            "I'd really like to help you with at least one project - "
            "what are you working on or building right now?"
        ),
        "conversational": (
            "Could you tell me about at least one project? " "What are you working on?"
        ),
        "professional": ("Please provide at least one project to continue."),
    }

    def get_welcome_message(self, ctx: OnboardingGrammarContext) -> str:
        """Get warm welcome message for first meeting.

        Args:
            ctx: Onboarding context

        Returns:
            Welcome message appropriate for formality
        """
        formality = ctx.get_formality()
        welcome = self.WELCOME_MESSAGES.get(formality, self.WELCOME_MESSAGES["conversational"])
        atmosphere = self.PLACE_ATMOSPHERE.get(formality, self.PLACE_ATMOSPHERE["conversational"])

        return f"{welcome} {atmosphere}"

    def acknowledge_project(
        self,
        ctx: OnboardingGrammarContext,
        project_name: str,
    ) -> str:
        """Acknowledge project with genuine interest.

        Args:
            ctx: Onboarding context
            project_name: Name of the project

        Returns:
            Acknowledgment with project name
        """
        formality = ctx.get_formality()

        # First project vs additional
        if ctx.projects_captured <= 1:
            ack = self.FIRST_PROJECT_ACKNOWLEDGMENTS.get(
                formality, self.FIRST_PROJECT_ACKNOWLEDGMENTS["conversational"]
            )
        else:
            ack = self.ADDITIONAL_PROJECT_ACKNOWLEDGMENTS.get(
                formality, self.ADDITIONAL_PROJECT_ACKNOWLEDGMENTS["conversational"]
            )

        # Include project name in warm responses
        if formality == "warm":
            return f"{project_name} - {ack.lower()}"
        else:
            return f"{project_name}. {ack}"

    def get_more_projects_prompt(self, ctx: OnboardingGrammarContext) -> str:
        """Get prompt asking about additional projects.

        Args:
            ctx: Onboarding context

        Returns:
            Prompt for more projects
        """
        formality = ctx.get_formality()
        return self.MORE_PROJECTS_PROMPTS.get(
            formality, self.MORE_PROJECTS_PROMPTS["conversational"]
        )

    def get_confirmation_prompt(self, ctx: OnboardingGrammarContext) -> str:
        """Get confirmation prompt for captured projects.

        Args:
            ctx: Onboarding context with project info

        Returns:
            Confirmation prompt
        """
        formality = ctx.get_formality()
        project_summary = ctx.get_project_summary()

        if ctx.is_single_project():
            template = self.CONFIRMATION_PROMPTS_SINGLE.get(
                formality, self.CONFIRMATION_PROMPTS_SINGLE["conversational"]
            )
            return template.format(project=project_summary)
        else:
            template = self.CONFIRMATION_PROMPTS_MULTIPLE.get(
                formality, self.CONFIRMATION_PROMPTS_MULTIPLE["conversational"]
            )
            return template.format(projects=project_summary)

    def celebrate_completion(self, ctx: OnboardingGrammarContext) -> str:
        """Celebrate successful onboarding - relationship established!

        Args:
            ctx: Onboarding context with project info

        Returns:
            Celebration message
        """
        formality = ctx.get_formality()
        project_summary = ctx.get_project_summary()

        template = self.COMPLETION_MESSAGES.get(
            formality, self.COMPLETION_MESSAGES["conversational"]
        )
        return template.format(projects=project_summary)

    def handle_decline(self, ctx: OnboardingGrammarContext) -> str:
        """Handle decline with warmth and open door.

        Args:
            ctx: Onboarding context

        Returns:
            Warm decline message
        """
        formality = ctx.get_formality()

        if ctx.has_projects():
            messages = self.DECLINE_WITH_PROJECTS_MESSAGES
        else:
            messages = self.DECLINE_MESSAGES

        return messages.get(formality, messages["conversational"])

    def get_session_lost_message(self, ctx: OnboardingGrammarContext) -> str:
        """Get warm message for session recovery.

        Args:
            ctx: Onboarding context

        Returns:
            Session lost recovery message
        """
        formality = ctx.get_formality()
        return self.SESSION_LOST_MESSAGES.get(
            formality, self.SESSION_LOST_MESSAGES["conversational"]
        )

    def get_need_project_message(self, ctx: OnboardingGrammarContext) -> str:
        """Get message asking for at least one project.

        Args:
            ctx: Onboarding context

        Returns:
            Nudge for project info
        """
        formality = ctx.get_formality()
        return self.NEED_PROJECT_MESSAGES.get(
            formality, self.NEED_PROJECT_MESSAGES["conversational"]
        )

    def narrate_stage(self, ctx: OnboardingGrammarContext) -> str:
        """Get description of current stage for debugging/logging.

        Args:
            ctx: Onboarding context

        Returns:
            Human-readable stage description
        """
        stage_descriptions = {
            OnboardingStage.WELCOME: "first meeting - introducing Piper",
            OnboardingStage.GATHERING: "learning about user's projects",
            OnboardingStage.CONFIRMING: "confirming project portfolio",
            OnboardingStage.COMPLETE: "onboarding complete - relationship established",
            OnboardingStage.DECLINED: "user declined - door remains open",
        }

        return stage_descriptions.get(ctx.stage, "unknown stage")

    def get_add_more_prompt(self, ctx: OnboardingGrammarContext) -> str:
        """Get prompt when user wants to add more projects.

        Args:
            ctx: Onboarding context

        Returns:
            Prompt for additional project
        """
        formality = ctx.get_formality()

        prompts = {
            "warm": "Sure! What other project would you like to tell me about?",
            "conversational": "Great! What's the next project?",
            "professional": "Please provide the additional project.",
        }

        return prompts.get(formality, prompts["conversational"])

    def get_unclear_response_prompt(self, ctx: OnboardingGrammarContext) -> str:
        """Get prompt when user response is unclear during confirmation.

        Args:
            ctx: Onboarding context

        Returns:
            Clarification prompt
        """
        formality = ctx.get_formality()
        project_summary = ctx.get_project_summary()

        prompts = {
            "warm": (
                f"I have {project_summary} noted. "
                "Should I save these to your portfolio? "
                "Just say 'yes' to confirm, or let me know if you'd like to add more!"
            ),
            "conversational": (
                f"I have {project_summary}. "
                "Should I save these? Say 'yes' to confirm or 'add more' for more projects."
            ),
            "professional": (f"Confirm {project_summary}? Reply 'yes' to save or 'add' for more."),
        }

        return prompts.get(formality, prompts["conversational"])
