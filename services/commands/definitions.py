"""
Command definitions for CommandRegistry.

Issue #551: ARCH-COMMANDS
ADR-057: CommandRegistry

This module defines all commands that can be registered with the CommandRegistry.
Commands are defined once here and made available across all interfaces.
"""

from .registry import (
    CommandCategory,
    CommandDefinition,
    CommandInterface,
    CommandRegistry,
    InterfaceConfig,
)

# =============================================================================
# STANDUP COMMANDS
# =============================================================================

STANDUP_COMMAND = CommandDefinition(
    name="standup",
    display_name="Daily Standup",
    description="Generate your daily standup report",
    category=CommandCategory.STANDUP,
    interfaces={
        CommandInterface.ALL: InterfaceConfig(
            enabled=True,
            aliases=["standup", "daily"],
            slack_response_type="in_channel",
            cli_group="standup",
            url_path="/api/v1/standup/generate",
        )
    },
    handler_module="services.standup.standup_service",
    handler_name="generate_standup",
    examples=["show standup", "/standup", "what's my standup?"],
    keywords=["standup", "daily", "yesterday", "today", "blockers"],
    requires_integration=None,
    execution_type="query",
)


# =============================================================================
# CALENDAR COMMANDS
# =============================================================================

CALENDAR_TODAY_COMMAND = CommandDefinition(
    name="calendar_today",
    display_name="Today's Calendar",
    description="Show your meetings for today",
    category=CommandCategory.CALENDAR,
    interfaces={
        CommandInterface.WEB_CHAT: InterfaceConfig(enabled=True),
        CommandInterface.CLI: InterfaceConfig(enabled=True, cli_group="cal"),
        CommandInterface.SLACK: InterfaceConfig(
            enabled=True,
            aliases=["cal", "today"],
            description_override="Show today's calendar via /piper calendar",
        ),  # Issue #551 Phase 4: Gap closed
        CommandInterface.URL: InterfaceConfig(enabled=True, url_path="/api/v1/calendar/today"),
    },
    handler_module="services.intent_service.canonical_handlers",
    handler_name="_handle_temporal_query",
    examples=["what meetings do I have today?", "cal today", "show calendar"],
    keywords=["calendar", "meetings", "today", "schedule"],
    requires_integration="calendar",
    execution_type="query",
)

CALENDAR_WEEK_COMMAND = CommandDefinition(
    name="calendar_week",
    display_name="This Week's Calendar",
    description="Show your meetings for this week",
    category=CommandCategory.CALENDAR,
    interfaces={
        CommandInterface.WEB_CHAT: InterfaceConfig(enabled=True),
        CommandInterface.CLI: InterfaceConfig(enabled=True, cli_group="cal"),
        CommandInterface.SLACK: InterfaceConfig(
            enabled=True,
            aliases=["week"],
            description_override="Show this week's calendar via /piper calendar week",
        ),  # Issue #551 Phase 4: Gap closed
        CommandInterface.URL: InterfaceConfig(enabled=False),
    },
    handler_module="services.intent_service.query_handlers",
    handler_name="_handle_week_calendar_query",
    examples=["what's my week look like?", "meetings this week"],
    keywords=["calendar", "meetings", "week", "schedule"],
    requires_integration="calendar",
    execution_type="query",
)


# =============================================================================
# IDENTITY/DISCOVERY COMMANDS
# =============================================================================

IDENTITY_COMMAND = CommandDefinition(
    name="identity",
    display_name="Who Am I",
    description="Learn about Piper Morgan",
    category=CommandCategory.IDENTITY,
    interfaces={
        CommandInterface.WEB_CHAT: InterfaceConfig(enabled=True),
        CommandInterface.SLACK: InterfaceConfig(enabled=True),
    },
    handler_module="services.intent_service.canonical_handlers",
    handler_name="_handle_identity_query",
    examples=["who are you?", "what's your name?"],
    keywords=["identity", "name", "who", "about"],
    execution_type="query",
)

DISCOVERY_COMMAND = CommandDefinition(
    name="discovery",
    display_name="Capabilities",
    description="Discover what Piper can do",
    category=CommandCategory.DISCOVERY,
    interfaces={
        CommandInterface.WEB_CHAT: InterfaceConfig(enabled=True),
        CommandInterface.SLACK: InterfaceConfig(enabled=True),
    },
    handler_module="services.intent_service.canonical_handlers",
    handler_name="_handle_discovery_query",
    examples=["what can you do?", "show me your capabilities"],
    keywords=["capabilities", "features", "help", "what can"],
    execution_type="query",
)


# =============================================================================
# STATUS/PRIORITY COMMANDS
# =============================================================================

STATUS_COMMAND = CommandDefinition(
    name="status",
    display_name="Project Status",
    description="Check your current project status",
    category=CommandCategory.STATUS,
    interfaces={
        CommandInterface.WEB_CHAT: InterfaceConfig(enabled=True),
        CommandInterface.CLI: InterfaceConfig(enabled=True),
        CommandInterface.SLACK: InterfaceConfig(
            enabled=True,
            aliases=["projects"],
            description_override="Check project status via /piper status",
        ),  # Issue #551 Phase 4: Gap closed
    },
    handler_module="services.intent_service.canonical_handlers",
    handler_name="_handle_status_query",
    examples=["what am I working on?", "project status"],
    keywords=["status", "projects", "working on"],
    execution_type="query",
)

PRIORITY_COMMAND = CommandDefinition(
    name="priority",
    display_name="Top Priority",
    description="Get your top priority item",
    category=CommandCategory.PRIORITY,
    interfaces={
        CommandInterface.WEB_CHAT: InterfaceConfig(enabled=True),
        CommandInterface.SLACK: InterfaceConfig(
            enabled=True,
            aliases=["focus", "top"],
            description_override="Get your top priority via /piper priority",
        ),  # Issue #551 Phase 4: Gap closed
    },
    handler_module="services.intent_service.canonical_handlers",
    handler_name="_handle_priority_query",
    examples=["what's my top priority?", "what should I focus on?"],
    keywords=["priority", "focus", "important", "top"],
    execution_type="query",
)


# =============================================================================
# HELP COMMANDS
# =============================================================================

HELP_COMMAND = CommandDefinition(
    name="help",
    display_name="Help",
    description="Get help with Piper commands",
    category=CommandCategory.HELP,
    interfaces={
        CommandInterface.WEB_CHAT: InterfaceConfig(enabled=True),
        CommandInterface.SLACK: InterfaceConfig(
            enabled=True,
            aliases=["piper help"],
        ),
        CommandInterface.CLI: InterfaceConfig(enabled=False),  # CLI has --help
    },
    handler_module="services.commands.registry",
    handler_name="get_help",
    examples=["/piper help", "help"],
    keywords=["help", "commands", "how to"],
    execution_type="query",
)


# =============================================================================
# REGISTRATION
# =============================================================================

ALL_COMMANDS = [
    STANDUP_COMMAND,
    CALENDAR_TODAY_COMMAND,
    CALENDAR_WEEK_COMMAND,
    IDENTITY_COMMAND,
    DISCOVERY_COMMAND,
    STATUS_COMMAND,
    PRIORITY_COMMAND,
    HELP_COMMAND,
]


def register_all_commands() -> int:
    """
    Register all command definitions with the CommandRegistry.

    Returns:
        Number of commands registered.
    """
    for command in ALL_COMMANDS:
        CommandRegistry.register(command)

    CommandRegistry.mark_initialized()
    return len(ALL_COMMANDS)


def get_parity_gaps() -> dict:
    """
    Identify commands with interface parity gaps.

    Returns a dict mapping command names to lists of disabled interfaces.
    """
    gaps = {}
    for command in ALL_COMMANDS:
        disabled = []
        for interface in CommandInterface:
            if interface == CommandInterface.ALL:
                continue
            config = command.interfaces.get(interface)
            if config and not config.enabled:
                disabled.append(interface.value)
        if disabled:
            gaps[command.name] = disabled
    return gaps
