"""
Service for handling simple conversational queries
"""


class ConversationQueryService:
    """Handles simple, stateless conversational queries."""

    async def get_greeting(self) -> str:
        """Returns a simple greeting message."""
        return "Hello there! How can I help you today?"

    async def get_help(self) -> str:
        """Returns a basic help message."""
        # This can be expanded later
        return "I can help you with product management tasks. Try asking me to list projects or create a GitHub issue."

    async def get_status(self) -> str:
        """Returns a status message."""
        return "I'm operating normally. All systems are go!"

    async def get_initial_contact(self) -> str:
        """Handles a user's initial greeting."""
        return "Hello to you too!"
