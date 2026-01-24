"""
Tests for workspace detection.

Part of #658 WORKSPACE-DETECTION.

Tests cover:
- WorkspaceContext dataclass and factory method
- ContextSwitch dataclass
- detect_context_switch() function
- All switch scenarios (explicit, return)
- time_away calculation for returns
"""

from datetime import datetime, timedelta, timezone

import pytest

from services.mux.workspace_detection import ContextSwitch, WorkspaceContext, detect_context_switch
from services.shared_types import PlaceType

# =============================================================================
# Test Fixtures
# =============================================================================


def make_context(
    workspace_id: str = "workspace-1",
    workspace_type: str = "slack",
    friendly_name: str = "#general",
    place_type: PlaceType = PlaceType.SLACK_CHANNEL,
    hours_ago: float = 0,
    metadata: dict = None,
) -> WorkspaceContext:
    """Helper to create test WorkspaceContext instances."""
    return WorkspaceContext(
        workspace_id=workspace_id,
        workspace_type=workspace_type,
        friendly_name=friendly_name,
        last_active=datetime.now(timezone.utc) - timedelta(hours=hours_ago),
        place_type=place_type,
        metadata=metadata or {},
    )


# =============================================================================
# Test: WorkspaceContext
# =============================================================================


class TestWorkspaceContext:
    """Tests for the WorkspaceContext dataclass."""

    def test_creates_with_all_fields(self):
        """WorkspaceContext can be created with all fields."""
        ctx = make_context()
        assert ctx.workspace_id == "workspace-1"
        assert ctx.workspace_type == "slack"
        assert ctx.friendly_name == "#general"
        assert ctx.place_type == PlaceType.SLACK_CHANNEL

    def test_matches_same_workspace(self):
        """matches() returns True for same workspace_id."""
        ctx1 = make_context(workspace_id="ws-123")
        ctx2 = make_context(workspace_id="ws-123", friendly_name="#different")
        assert ctx1.matches(ctx2)

    def test_matches_different_workspace(self):
        """matches() returns False for different workspace_id."""
        ctx1 = make_context(workspace_id="ws-123")
        ctx2 = make_context(workspace_id="ws-456")
        assert not ctx1.matches(ctx2)


class TestWorkspaceContextFromSpatialContext:
    """Tests for WorkspaceContext.from_spatial_context() factory."""

    def test_slack_dm_extracts_workspace_id(self):
        """Slack DM extracts workspace_id from spatial_context."""
        spatial = {"workspace_id": "T12345", "is_dm": True}
        ctx = WorkspaceContext.from_spatial_context(spatial, PlaceType.SLACK_DM)

        assert ctx.workspace_id == "T12345"
        assert ctx.workspace_type == "slack"
        assert ctx.place_type == PlaceType.SLACK_DM

    def test_slack_channel_uses_team_id_fallback(self):
        """Slack channel falls back to team_id if no workspace_id."""
        spatial = {"team_id": "T99999", "channel": "general"}
        ctx = WorkspaceContext.from_spatial_context(spatial, PlaceType.SLACK_CHANNEL)

        assert ctx.workspace_id == "T99999"
        assert ctx.workspace_type == "slack"
        assert ctx.friendly_name == "#general"

    def test_slack_channel_generates_friendly_name(self):
        """Slack channel generates #channel-name friendly name."""
        spatial = {"workspace_id": "T12345", "channel": "random"}
        ctx = WorkspaceContext.from_spatial_context(spatial, PlaceType.SLACK_CHANNEL)

        assert ctx.friendly_name == "#random"

    def test_slack_channel_preserves_hash_prefix(self):
        """Slack channel doesn't double the # prefix."""
        spatial = {"workspace_id": "T12345", "channel": "#already-prefixed"}
        ctx = WorkspaceContext.from_spatial_context(spatial, PlaceType.SLACK_CHANNEL)

        assert ctx.friendly_name == "#already-prefixed"

    def test_web_chat_extracts_session_id(self):
        """Web chat extracts session_id from spatial_context."""
        spatial = {"session_id": "sess-abc123"}
        ctx = WorkspaceContext.from_spatial_context(spatial, PlaceType.WEB_CHAT)

        assert ctx.workspace_id == "sess-abc123"
        assert ctx.workspace_type == "web"
        assert ctx.friendly_name == "web chat"

    def test_web_chat_defaults_without_session(self):
        """Web chat defaults to 'web-chat' if no session_id."""
        spatial = {}
        ctx = WorkspaceContext.from_spatial_context(spatial, PlaceType.WEB_CHAT)

        assert ctx.workspace_id == "web-chat"

    def test_cli_always_cli_workspace(self):
        """CLI always uses 'cli' as workspace_id."""
        spatial = {"anything": "ignored"}
        ctx = WorkspaceContext.from_spatial_context(spatial, PlaceType.CLI)

        assert ctx.workspace_id == "cli"
        assert ctx.workspace_type == "cli"
        assert ctx.friendly_name == "terminal"

    def test_api_extracts_client_id(self):
        """API extracts client_id from spatial_context."""
        spatial = {"client_id": "my-api-client"}
        ctx = WorkspaceContext.from_spatial_context(spatial, PlaceType.API)

        assert ctx.workspace_id == "my-api-client"
        assert ctx.workspace_type == "api"
        assert ctx.friendly_name == "API"

    def test_unknown_place_type(self):
        """Unknown place type returns unknown workspace."""
        spatial = {}
        ctx = WorkspaceContext.from_spatial_context(spatial, PlaceType.UNKNOWN)

        assert ctx.workspace_id == "unknown"
        assert ctx.workspace_type == "unknown"
        assert ctx.friendly_name == "unknown context"

    def test_copies_metadata(self):
        """Factory copies spatial_context to metadata."""
        spatial = {"channel": "general", "custom": "value"}
        ctx = WorkspaceContext.from_spatial_context(spatial, PlaceType.SLACK_CHANNEL)

        assert ctx.metadata == spatial
        # Verify it's a copy, not the same dict
        spatial["new_key"] = "new_value"
        assert "new_key" not in ctx.metadata

    def test_custom_timestamp(self):
        """Factory accepts custom timestamp."""
        ts = datetime(2026, 1, 24, 10, 0, 0, tzinfo=timezone.utc)
        ctx = WorkspaceContext.from_spatial_context({}, PlaceType.CLI, timestamp=ts)

        assert ctx.last_active == ts

    def test_default_timestamp_is_now(self):
        """Factory defaults timestamp to current time."""
        before = datetime.now(timezone.utc)
        ctx = WorkspaceContext.from_spatial_context({}, PlaceType.CLI)
        after = datetime.now(timezone.utc)

        assert before <= ctx.last_active <= after


# =============================================================================
# Test: ContextSwitch
# =============================================================================


class TestContextSwitch:
    """Tests for the ContextSwitch dataclass."""

    def test_creates_with_required_fields(self):
        """ContextSwitch can be created with required fields."""
        from_ctx = make_context(workspace_id="ws-from")
        to_ctx = make_context(workspace_id="ws-to")

        switch = ContextSwitch(
            from_context=from_ctx,
            to_context=to_ctx,
            switch_type="explicit",
        )

        assert switch.from_context == from_ctx
        assert switch.to_context == to_ctx
        assert switch.switch_type == "explicit"
        assert switch.time_away is None

    def test_creates_with_time_away(self):
        """ContextSwitch can include time_away for returns."""
        from_ctx = make_context()
        to_ctx = make_context()

        switch = ContextSwitch(
            from_context=from_ctx,
            to_context=to_ctx,
            switch_type="return",
            time_away=timedelta(hours=2),
        )

        assert switch.time_away == timedelta(hours=2)

    def test_default_timestamp(self):
        """ContextSwitch defaults timestamp to now."""
        from_ctx = make_context()
        to_ctx = make_context()

        before = datetime.now(timezone.utc)
        switch = ContextSwitch(
            from_context=from_ctx,
            to_context=to_ctx,
            switch_type="explicit",
        )
        after = datetime.now(timezone.utc)

        assert before <= switch.timestamp <= after


# =============================================================================
# Test: detect_context_switch()
# =============================================================================


class TestDetectContextSwitch:
    """Tests for the detect_context_switch() function."""

    def test_no_switch_when_no_previous(self):
        """Returns None when there's no previous context."""
        current = make_context()
        result = detect_context_switch(current, None)
        assert result is None

    def test_no_switch_same_workspace(self):
        """Returns None when staying in same workspace."""
        current = make_context(workspace_id="ws-same")
        previous = make_context(workspace_id="ws-same")

        result = detect_context_switch(current, previous)
        assert result is None

    def test_explicit_switch_different_workspace(self):
        """Detects explicit switch to different workspace."""
        current = make_context(workspace_id="ws-new", friendly_name="#new-channel")
        previous = make_context(workspace_id="ws-old", friendly_name="#old-channel")

        result = detect_context_switch(current, previous)

        assert result is not None
        assert result.switch_type == "explicit"
        assert result.from_context == previous
        assert result.to_context == current
        assert result.time_away is None

    def test_return_switch_to_earlier_context(self):
        """Detects return to earlier context from history."""
        # Build history: ws-1 -> ws-2 -> ws-1 (return)
        ctx1_early = make_context(workspace_id="ws-1", hours_ago=2)
        ctx2 = make_context(workspace_id="ws-2", hours_ago=1)
        ctx1_now = make_context(workspace_id="ws-1", hours_ago=0)

        history = [ctx1_early, ctx2, ctx1_now]

        result = detect_context_switch(ctx1_now, ctx2, session_history=history)

        assert result is not None
        assert result.switch_type == "return"
        assert result.from_context == ctx2
        assert result.to_context == ctx1_now

    def test_time_away_calculation_for_returns(self):
        """Calculates time_away correctly for return switches."""
        # User was in ws-1 two hours ago, then ws-2, now returning to ws-1
        ctx1_early = make_context(workspace_id="ws-1", hours_ago=2)
        ctx2 = make_context(workspace_id="ws-2", hours_ago=1)
        ctx1_now = make_context(workspace_id="ws-1", hours_ago=0)

        history = [ctx1_early, ctx2, ctx1_now]

        result = detect_context_switch(ctx1_now, ctx2, session_history=history)

        assert result is not None
        # time_away should be approximately 2 hours
        assert result.time_away is not None
        hours_away = result.time_away.total_seconds() / 3600
        assert 1.9 < hours_away < 2.1

    def test_explicit_switch_when_not_in_history(self):
        """Returns explicit switch when target not in history."""
        ctx1 = make_context(workspace_id="ws-1", hours_ago=2)
        ctx2 = make_context(workspace_id="ws-2", hours_ago=1)
        ctx3 = make_context(workspace_id="ws-3", hours_ago=0)  # Never seen before

        history = [ctx1, ctx2, ctx3]

        result = detect_context_switch(ctx3, ctx2, session_history=history)

        assert result is not None
        assert result.switch_type == "explicit"

    def test_handles_empty_history(self):
        """Works correctly with empty session history."""
        current = make_context(workspace_id="ws-new")
        previous = make_context(workspace_id="ws-old")

        result = detect_context_switch(current, previous, session_history=[])

        assert result is not None
        assert result.switch_type == "explicit"

    def test_handles_none_history(self):
        """Works correctly with None session history."""
        current = make_context(workspace_id="ws-new")
        previous = make_context(workspace_id="ws-old")

        result = detect_context_switch(current, previous, session_history=None)

        assert result is not None
        assert result.switch_type == "explicit"


# =============================================================================
# Test: Integration with PlaceDetector concepts
# =============================================================================


class TestPlaceDetectorIntegration:
    """Tests verifying integration patterns with PlaceDetector."""

    def test_full_flow_slack_to_web(self):
        """Full detection flow: Slack channel -> Web chat."""
        # Simulate PlaceDetector outputs
        slack_spatial = {
            "workspace_id": "T12345",
            "channel": "general",
            "source": "slack",
        }
        web_spatial = {"session_id": "web-sess-1", "source": "web"}

        # Build contexts like call sites would
        slack_ctx = WorkspaceContext.from_spatial_context(slack_spatial, PlaceType.SLACK_CHANNEL)
        web_ctx = WorkspaceContext.from_spatial_context(web_spatial, PlaceType.WEB_CHAT)

        # Detect switch
        switch = detect_context_switch(web_ctx, slack_ctx)

        assert switch is not None
        assert switch.switch_type == "explicit"
        assert switch.from_context.friendly_name == "#general"
        assert switch.to_context.friendly_name == "web chat"

    def test_full_flow_return_to_slack(self):
        """Full detection flow: Slack -> Web -> Slack (return)."""
        slack_spatial = {"workspace_id": "T12345", "channel": "general"}
        web_spatial = {"session_id": "web-sess-1"}

        slack_ctx_early = WorkspaceContext.from_spatial_context(
            slack_spatial,
            PlaceType.SLACK_CHANNEL,
            timestamp=datetime.now(timezone.utc) - timedelta(hours=1),
        )
        web_ctx = WorkspaceContext.from_spatial_context(
            web_spatial,
            PlaceType.WEB_CHAT,
            timestamp=datetime.now(timezone.utc) - timedelta(minutes=30),
        )
        slack_ctx_now = WorkspaceContext.from_spatial_context(
            slack_spatial,
            PlaceType.SLACK_CHANNEL,
            timestamp=datetime.now(timezone.utc),
        )

        history = [slack_ctx_early, web_ctx, slack_ctx_now]
        switch = detect_context_switch(slack_ctx_now, web_ctx, session_history=history)

        assert switch is not None
        assert switch.switch_type == "return"
        assert switch.time_away is not None
        # About 1 hour since first Slack visit
        hours_away = switch.time_away.total_seconds() / 3600
        assert 0.9 < hours_away < 1.1
