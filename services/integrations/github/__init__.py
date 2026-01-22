# GitHub integration exports
# Legacy GitHubAgent removed in Week 4 of deprecation timeline (CORE-INT #109)
# Use GitHubIntegrationRouter for all GitHub operations

from services.integrations.github.narrative_bridge import GitHubNarrativeBridge
from services.integrations.github.narrative_helpers import (
    narrate_issue_preview,
    narrate_issues_list,
    narrate_last_activity,
    narrate_open_issues_count,
    narrate_priority_issues,
    narrate_project_health,
)

# Issue #621: Grammar-conscious response components
from services.integrations.github.response_context import GitHubResponseContext

__all__ = [
    # Response context
    "GitHubResponseContext",
    "GitHubNarrativeBridge",
    # Narrative helpers for canonical handlers
    "narrate_issue_preview",
    "narrate_issues_list",
    "narrate_open_issues_count",
    "narrate_project_health",
    "narrate_last_activity",
    "narrate_priority_issues",
]
