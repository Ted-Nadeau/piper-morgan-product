"""
Tests for PlaceService (#684 MUX-NAV-PLACES).

Tests:
- GitHub transformation to Place
- Calendar transformation to Place
- Trust-gated filtering
- Confidence handling on errors
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.place.place_service import PlaceService
from services.shared_types import HardnessLevel, PlaceConfidence, PlaceType, TrustStage


class TestPlaceServiceInit:
    """Test PlaceService initialization."""

    def test_init_without_integrations(self):
        """Service can be initialized without integrations."""
        service = PlaceService()
        assert service.github_router is None
        assert service.calendar_service is None

    def test_init_with_github(self):
        """Service accepts GitHub router."""
        mock_router = MagicMock()
        service = PlaceService(github_router=mock_router)
        assert service.github_router is mock_router

    def test_init_with_calendar(self):
        """Service accepts Calendar service."""
        mock_calendar = MagicMock()
        service = PlaceService(calendar_service=mock_calendar)
        assert service.calendar_service is mock_calendar


class TestGitHubPlace:
    """Test GitHub -> Place transformation."""

    @pytest.fixture
    def mock_github_router(self):
        """Create mock GitHub router."""
        router = MagicMock()
        router.get_open_issues = AsyncMock(
            return_value=[
                {"number": 1, "title": "Issue 1"},
                {"number": 2, "title": "Issue 2"},
                {"number": 3, "title": "Issue 3"},
            ]
        )
        return router

    @pytest.mark.asyncio
    async def test_github_place_created(self, mock_github_router):
        """GitHub data transforms to Place object."""
        service = PlaceService(github_router=mock_github_router)
        place = await service.get_github_place()

        assert place is not None
        assert place.place_type == PlaceType.ISSUE_TRACKING

    @pytest.mark.asyncio
    async def test_github_place_has_name(self, mock_github_router):
        """GitHub Place has human-readable name."""
        service = PlaceService(github_router=mock_github_router)
        place = await service.get_github_place("test-repo")

        assert "test-repo" in place.name
        assert "repository" in place.name

    @pytest.mark.asyncio
    async def test_github_place_summary_uses_pipers_perspective(self, mock_github_router):
        """Summary uses 'I see' not API language."""
        service = PlaceService(github_router=mock_github_router)
        place = await service.get_github_place()

        assert "I see" in place.summary
        assert "3" in place.summary or "issues" in place.summary.lower()
        # Anti-flattening: no API language
        assert "returned" not in place.summary.lower()
        assert "api" not in place.summary.lower()

    @pytest.mark.asyncio
    async def test_github_place_no_issues(self, mock_github_router):
        """Summary handles zero issues."""
        mock_github_router.get_open_issues = AsyncMock(return_value=[])
        service = PlaceService(github_router=mock_github_router)
        place = await service.get_github_place()

        assert "no open issues" in place.summary.lower()

    @pytest.mark.asyncio
    async def test_github_place_single_issue(self, mock_github_router):
        """Summary handles one issue (singular)."""
        mock_github_router.get_open_issues = AsyncMock(
            return_value=[{"number": 1, "title": "Single"}]
        )
        service = PlaceService(github_router=mock_github_router)
        place = await service.get_github_place()

        assert "1 open issue" in place.summary

    @pytest.mark.asyncio
    async def test_github_place_high_confidence_on_success(self, mock_github_router):
        """Successful fetch has HIGH confidence."""
        service = PlaceService(github_router=mock_github_router)
        place = await service.get_github_place()

        assert place.confidence == PlaceConfidence.HIGH

    @pytest.mark.asyncio
    async def test_github_place_low_confidence_on_error(self, mock_github_router):
        """Error results in LOW confidence."""
        mock_github_router.get_open_issues = AsyncMock(side_effect=Exception("Connection failed"))
        service = PlaceService(github_router=mock_github_router)
        place = await service.get_github_place()

        assert place is not None
        assert place.confidence == PlaceConfidence.LOW
        assert "couldn't reach" in place.summary.lower()

    @pytest.mark.asyncio
    async def test_github_place_has_source_url(self, mock_github_router):
        """GitHub Place has source URL for linking."""
        service = PlaceService(github_router=mock_github_router)
        place = await service.get_github_place()

        assert "github.com" in place.source_url

    @pytest.mark.asyncio
    async def test_github_place_returns_none_without_router(self):
        """Returns None if no GitHub router configured."""
        service = PlaceService()
        place = await service.get_github_place()

        assert place is None


class TestCalendarPlace:
    """Test Calendar -> Place transformation."""

    @pytest.fixture
    def mock_calendar_service(self):
        """Create mock Calendar service."""
        service = MagicMock()
        service.get_todays_events = AsyncMock(
            return_value=[
                {"title": "Standup", "time": "9:00 AM"},
                {"title": "Sprint Planning", "time": "2:00 PM"},
            ]
        )
        return service

    @pytest.mark.asyncio
    async def test_calendar_place_created(self, mock_calendar_service):
        """Calendar data transforms to Place object."""
        service = PlaceService(calendar_service=mock_calendar_service)
        place = await service.get_calendar_place()

        assert place is not None
        assert place.place_type == PlaceType.TEMPORAL

    @pytest.mark.asyncio
    async def test_calendar_place_summary_uses_pipers_perspective(self, mock_calendar_service):
        """Summary uses 'I see' not API language."""
        service = PlaceService(calendar_service=mock_calendar_service)
        place = await service.get_calendar_place()

        assert "I see" in place.summary
        assert "meeting" in place.summary.lower()

    @pytest.mark.asyncio
    async def test_calendar_place_no_events(self, mock_calendar_service):
        """Summary handles zero events."""
        mock_calendar_service.get_todays_events = AsyncMock(return_value=[])
        service = PlaceService(calendar_service=mock_calendar_service)
        place = await service.get_calendar_place()

        assert "no meetings" in place.summary.lower()

    @pytest.mark.asyncio
    async def test_calendar_place_returns_none_without_service(self):
        """Returns None if no Calendar service configured."""
        service = PlaceService()
        place = await service.get_calendar_place()

        assert place is None


class TestGetAllPlaces:
    """Test getting all Places."""

    @pytest.mark.asyncio
    async def test_returns_empty_without_integrations(self):
        """Returns empty list without integrations."""
        service = PlaceService()
        places = await service.get_all_places()

        assert places == []

    @pytest.mark.asyncio
    async def test_returns_github_when_configured(self):
        """Includes GitHub Place when configured."""
        mock_router = MagicMock()
        mock_router.get_open_issues = AsyncMock(return_value=[])
        service = PlaceService(github_router=mock_router)
        places = await service.get_all_places()

        assert len(places) == 1
        assert places[0].place_type == PlaceType.ISSUE_TRACKING

    @pytest.mark.asyncio
    async def test_returns_both_when_configured(self):
        """Includes both Places when both configured."""
        mock_router = MagicMock()
        mock_router.get_open_issues = AsyncMock(return_value=[])
        mock_calendar = MagicMock()
        mock_calendar.get_todays_events = AsyncMock(return_value=[])

        service = PlaceService(github_router=mock_router, calendar_service=mock_calendar)
        places = await service.get_all_places()

        assert len(places) == 2
        types = {p.place_type for p in places}
        assert PlaceType.ISSUE_TRACKING in types
        assert PlaceType.TEMPORAL in types


class TestTrustFiltering:
    """Test trust-gated visibility."""

    @pytest.fixture
    def sample_places(self):
        """Create sample Places with different hardness."""
        from services.domain.models import Place

        return [
            Place(
                id="hard-1",
                place_type=PlaceType.ISSUE_TRACKING,
                name="GitHub",
                confidence=PlaceConfidence.HIGH,
                summary="test",
                source_url="https://github.com",
                hardness=HardnessLevel.HARD,  # Stage 3+
            ),
            Place(
                id="soft-1",
                place_type=PlaceType.DOCUMENTATION,
                name="Docs",
                confidence=PlaceConfidence.HIGH,
                summary="test",
                source_url="https://notion.so",
                hardness=HardnessLevel.SOFT,  # Stage 4+
            ),
        ]

    def test_stage_1_sees_nothing_hard(self, sample_places):
        """Stage 1 (NEW) doesn't see HARD Places."""
        service = PlaceService()
        visible = service.filter_by_trust(sample_places, TrustStage.NEW)

        # HARD requires Stage 3, SOFT requires Stage 4
        assert len(visible) == 0

    def test_stage_3_sees_hard(self, sample_places):
        """Stage 3 (ESTABLISHED) sees HARD but not SOFT."""
        service = PlaceService()
        visible = service.filter_by_trust(sample_places, TrustStage.ESTABLISHED)

        assert len(visible) == 1
        assert visible[0].hardness == HardnessLevel.HARD

    def test_stage_4_sees_all(self, sample_places):
        """Stage 4 (TRUSTED) sees all Places."""
        service = PlaceService()
        visible = service.filter_by_trust(sample_places, TrustStage.TRUSTED)

        assert len(visible) == 2


class TestGetVisiblePlaces:
    """Test combined get + filter convenience method."""

    @pytest.mark.asyncio
    async def test_get_visible_places(self):
        """Combines get_all_places and filter_by_trust."""
        mock_router = MagicMock()
        mock_router.get_open_issues = AsyncMock(return_value=[])

        service = PlaceService(github_router=mock_router)
        visible = await service.get_visible_places(TrustStage.ESTABLISHED)

        # GitHub (HARD) visible at Stage 3
        assert len(visible) == 1
        assert visible[0].place_type == PlaceType.ISSUE_TRACKING


class TestPlaceHardnessMapping:
    """Test the hardness configuration."""

    def test_issue_tracking_is_hard(self):
        """ISSUE_TRACKING requires Stage 3+."""
        service = PlaceService()
        hardness = service.PLACE_HARDNESS[PlaceType.ISSUE_TRACKING]
        assert hardness == HardnessLevel.HARD

    def test_temporal_is_hard(self):
        """TEMPORAL requires Stage 3+."""
        service = PlaceService()
        hardness = service.PLACE_HARDNESS[PlaceType.TEMPORAL]
        assert hardness == HardnessLevel.HARD

    def test_documentation_is_soft(self):
        """DOCUMENTATION requires Stage 4+."""
        service = PlaceService()
        hardness = service.PLACE_HARDNESS[PlaceType.DOCUMENTATION]
        assert hardness == HardnessLevel.SOFT
