"""
Tests for Document Query Handlers.

Issue #522: Canonical Query #40 - "Update the X document"

Test categories:
1. Pre-classifier routing integration tests (verify full path)
2. Handler unit tests (verify handler logic)
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


class TestPreClassifierDocumentRouting:
    """Test pre-classifier routes document update queries correctly.

    Issue #521 learning: Routing integration tests verify the full path
    from pre-classifier → intent service → handler.
    """

    @pytest.mark.parametrize(
        "query",
        [
            "update the README document",
            "update the project plan doc",
            "edit the meeting notes document",
            "modify the status document",
            "change the spec doc",
        ],
    )
    def test_document_update_queries_route_to_update_action(self, query):
        """Verify document update queries reach correct classification."""
        pre_classifier = PreClassifier()
        intent = pre_classifier.pre_classify(query)

        assert intent is not None, f"Query '{query}' should be classified"
        assert intent.category == IntentCategory.QUERY
        assert intent.action == "update_document_query"

    @pytest.mark.parametrize(
        "query",
        [
            "add to the notes document new items",
            "append to the log doc",
        ],
    )
    def test_document_add_queries_route_correctly(self, query):
        """Verify 'add to document' queries route correctly."""
        pre_classifier = PreClassifier()
        intent = pre_classifier.pre_classify(query)

        assert intent is not None, f"Query '{query}' should be classified"
        assert intent.category == IntentCategory.QUERY
        assert intent.action == "update_document_query"

    @pytest.mark.parametrize(
        "query",
        [
            "update project plan with new deadline",
            "edit the report with corrections",
        ],
    )
    def test_document_update_with_content_routes_correctly(self, query):
        """Verify update queries with content route correctly."""
        pre_classifier = PreClassifier()
        intent = pre_classifier.pre_classify(query)

        assert intent is not None, f"Query '{query}' should be classified"
        assert intent.category == IntentCategory.QUERY
        assert intent.action == "update_document_query"


class TestDocumentQueryParsingHelper:
    """Test the _parse_document_update_query helper method."""

    @pytest.fixture
    def intent_service(self):
        """Create IntentService instance for testing helper."""
        from services.intent.intent_service import IntentService

        return IntentService()

    def test_parse_update_document_with_content(self, intent_service):
        """Test parsing 'update X document with Y'."""
        doc_name, content = intent_service._parse_document_update_query(
            "update the project plan document with the new deadline"
        )
        assert doc_name == "project plan"
        assert content == "the new deadline"

    def test_parse_update_document_no_content(self, intent_service):
        """Test parsing 'update X document' without content."""
        doc_name, content = intent_service._parse_document_update_query(
            "update the README document"
        )
        assert doc_name == "readme"
        assert content is None

    def test_parse_edit_document(self, intent_service):
        """Test parsing 'edit X doc'."""
        doc_name, content = intent_service._parse_document_update_query(
            "edit the meeting notes doc"
        )
        assert doc_name == "meeting notes"
        assert content is None

    def test_parse_add_to_document(self, intent_service):
        """Test parsing 'add to X document Y'."""
        doc_name, content = intent_service._parse_document_update_query(
            "add to the notes document new action items"
        )
        assert doc_name == "notes"
        assert content == "new action items"

    def test_parse_empty_query_returns_none(self, intent_service):
        """Test that empty/unrecognized queries return None."""
        doc_name, content = intent_service._parse_document_update_query("what is the weather")
        assert doc_name is None
        assert content is None


class TestUpdateDocumentNotConfigured:
    """Test graceful degradation when Notion is not configured."""

    @pytest.fixture
    def intent_service(self):
        """Create IntentService instance."""
        from services.intent.intent_service import IntentService

        return IntentService()

    @pytest.fixture
    def mock_intent(self):
        """Create mock intent for testing."""
        return Intent(
            category=IntentCategory.QUERY,
            action="update_document_query",
            confidence=1.0,
            context={"original_message": "update the README document"},
        )

    @pytest.mark.asyncio
    async def test_not_configured_returns_graceful_message(self, intent_service, mock_intent):
        """Test handler returns helpful message when Notion not configured."""
        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = False
            MockRouter.return_value = mock_router

            result = await intent_service._handle_update_document_notion(
                mock_intent, "workflow-123", "session-456"
            )

            assert result.success is True
            assert "Notion isn't configured" in result.message
            assert result.implemented is False


class TestUpdateDocumentNotFound:
    """Test handling when document is not found."""

    @pytest.fixture
    def intent_service(self):
        """Create IntentService instance."""
        from services.intent.intent_service import IntentService

        return IntentService()

    @pytest.fixture
    def mock_intent(self):
        """Create mock intent for testing."""
        return Intent(
            category=IntentCategory.QUERY,
            action="update_document_query",
            confidence=1.0,
            context={"original_message": "update the nonexistent document"},
        )

    @pytest.mark.asyncio
    async def test_document_not_found_returns_clarification(self, intent_service, mock_intent):
        """Test handler asks for clarification when document not found."""
        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = True
            mock_router.connect = AsyncMock()
            mock_router.search_notion = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router

            result = await intent_service._handle_update_document_notion(
                mock_intent, "workflow-123", "session-456"
            )

            assert result.success is True
            assert "No document found" in result.message
            assert result.requires_clarification is True


class TestUpdateDocumentMultipleMatches:
    """Test handling when multiple documents match."""

    @pytest.fixture
    def intent_service(self):
        """Create IntentService instance."""
        from services.intent.intent_service import IntentService

        return IntentService()

    @pytest.fixture
    def mock_intent(self):
        """Create mock intent for testing."""
        return Intent(
            category=IntentCategory.QUERY,
            action="update_document_query",
            confidence=1.0,
            context={"original_message": "update the project document"},
        )

    @pytest.mark.asyncio
    async def test_multiple_matches_asks_for_clarification(self, intent_service, mock_intent):
        """Test handler asks which document when multiple match."""
        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = True
            mock_router.connect = AsyncMock()
            mock_router.search_notion = AsyncMock(
                return_value=[
                    {
                        "id": "page-1",
                        "url": "https://notion.so/page-1",
                        "properties": {"title": {"title": [{"text": {"content": "Project Plan"}}]}},
                    },
                    {
                        "id": "page-2",
                        "url": "https://notion.so/page-2",
                        "properties": {
                            "title": {"title": [{"text": {"content": "Project Notes"}}]}
                        },
                    },
                ]
            )
            MockRouter.return_value = mock_router

            result = await intent_service._handle_update_document_notion(
                mock_intent, "workflow-123", "session-456"
            )

            assert result.success is True
            assert "Found 2 documents" in result.message
            assert "Project Plan" in result.message
            assert "Project Notes" in result.message
            assert result.requires_clarification is True
            assert result.clarification_type == "multiple_matches"


class TestUpdateDocumentSuccess:
    """Test successful document update flow."""

    @pytest.fixture
    def intent_service(self):
        """Create IntentService instance."""
        from services.intent.intent_service import IntentService

        return IntentService()

    @pytest.fixture
    def mock_intent_with_content(self):
        """Create mock intent with update content."""
        return Intent(
            category=IntentCategory.QUERY,
            action="update_document_query",
            confidence=1.0,
            context={"original_message": "update the README document with new instructions"},
        )

    @pytest.mark.asyncio
    async def test_single_match_proceeds_to_update(self, intent_service, mock_intent_with_content):
        """Test handler proceeds to update when single document found."""
        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = True
            mock_router.connect = AsyncMock()
            mock_router.search_notion = AsyncMock(
                return_value=[
                    {
                        "id": "page-123",
                        "url": "https://notion.so/readme",
                        "properties": {"title": {"title": [{"text": {"content": "README"}}]}},
                    }
                ]
            )
            mock_router.update_page = AsyncMock(return_value={"id": "page-123"})
            MockRouter.return_value = mock_router

            result = await intent_service._handle_update_document_notion(
                mock_intent_with_content, "workflow-123", "session-456"
            )

            assert result.success is True
            assert "Updated" in result.message or "README" in result.message
            assert result.intent_data.get("document_title") == "README"
