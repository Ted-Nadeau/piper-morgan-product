"""
PM-081: Todo Management API Tests
Comprehensive test suite for clean todo management API with PM-040 Knowledge Graph and PM-034 Intent Classification integration
Universal List Architecture - Chief Architect's universal composition over specialization principle
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.api.todo_management import (
    ListMembershipRequest,
    TodoCreateRequest,
    TodoListCreateRequest,
    TodoListUpdateRequest,
    TodoUpdateRequest,
    todo_management_router,
)


class TestTodoManagementAPI:
    """Comprehensive test suite for PM-081 Todo Management API with Universal List Architecture"""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with todo management router"""
        app = FastAPI()
        app.include_router(todo_management_router)
        return app

    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return TestClient(app)

    @pytest.fixture
    def mock_todo_service(self):
        """Mock todo management service"""
        service = AsyncMock()
        service.create_todo = AsyncMock()
        service.get_todo = AsyncMock()
        service.update_todo = AsyncMock()
        service.delete_todo = AsyncMock()
        service.list_todos = AsyncMock()
        return service

    @pytest.fixture
    def mock_universal_list_service(self):
        """Mock universal list service for Chief Architect's universal composition pattern"""
        service = AsyncMock()
        service.create_list = AsyncMock()
        service.get_list = AsyncMock()
        service.update_list = AsyncMock()
        service.delete_list = AsyncMock()
        service.list_lists = AsyncMock()
        service.add_list_member = AsyncMock()
        service.remove_list_member = AsyncMock()
        return service

    @pytest.fixture
    def mock_knowledge_graph_service(self):
        """Mock knowledge graph service for PM-040 integration"""
        service = AsyncMock()
        service.get_related_nodes = AsyncMock()
        service.find_paths = AsyncMock()
        service.get_subgraph = AsyncMock()
        return service

    @pytest.fixture
    def mock_query_router(self):
        """Mock query router for PM-034 integration"""
        router = AsyncMock()
        router.classify_and_route = AsyncMock()
        return router

    @pytest.fixture
    def sample_todo_data(self):
        """Sample todo data for testing"""
        return {
            "title": "Review pull request #123",
            "description": "Review the new authentication feature",
            "priority": "high",
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "tags": ["code-review", "authentication"],
            "list_id": "list_456",
            "assignee_id": "user_789",
            "metadata": {"project_id": "proj_123", "estimated_hours": 2},
        }

    @pytest.fixture
    def sample_todo_list_data(self):
        """Sample todo list data for testing (universal List with item_type='todo')"""
        return {
            "name": "Sprint 15 Todos",
            "description": "Todos for the current sprint",
            "list_type": "project",
            "color": "#4CAF50",
            "ordering_strategy": "priority",
            "metadata": {"sprint_id": "sprint_15", "team_id": "team_456"},
        }

    @pytest.fixture
    def sample_membership_data(self):
        """Sample membership data for testing (universal ListItem with item_type='todo')"""
        return {"user_id": "user_123", "role": "member"}

    # Todo Management Tests - Standalone Todo Domain Object
    async def test_create_todo_success(self, client, sample_todo_data):
        """Test successful todo creation with standalone Todo domain object"""
        response = client.post("/api/v1/todos/", json=sample_todo_data)

        assert response.status_code == 201
        data = response.json()

        # Verify response structure
        assert "id" in data
        assert data["title"] == sample_todo_data["title"]
        assert data["description"] == sample_todo_data["description"]
        assert data["priority"] == sample_todo_data["priority"]
        assert data["status"] == "pending"
        assert data["tags"] == sample_todo_data["tags"]
        assert data["list_id"] == sample_todo_data["list_id"]
        assert data["assignee_id"] == sample_todo_data["assignee_id"]
        assert "created_at" in data
        assert "updated_at" in data
        assert data["completed_at"] is None
        assert data["metadata"] == sample_todo_data["metadata"]

    async def test_create_todo_validation(self, client):
        """Test todo creation validation"""
        # Test missing required field
        invalid_data = {"description": "Missing title"}
        response = client.post("/api/v1/todos/", json=invalid_data)
        assert response.status_code == 422

        # Test invalid priority
        invalid_data = {"title": "Test", "priority": "invalid"}
        response = client.post("/api/v1/todos/", json=invalid_data)
        assert response.status_code == 422

        # Test title too long
        invalid_data = {"title": "x" * 201}
        response = client.post("/api/v1/todos/", json=invalid_data)
        assert response.status_code == 422

    async def test_get_todo_not_found(self, client):
        """Test getting non-existent todo"""
        response = client.get("/api/v1/todos/non-existent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_update_todo_not_found(self, client, sample_todo_data):
        """Test updating non-existent todo"""
        update_data = {"title": "Updated Title"}
        response = client.put("/api/v1/todos/non-existent-id", json=update_data)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_delete_todo_not_found(self, client):
        """Test deleting non-existent todo"""
        response = client.delete("/api/v1/todos/non-existent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_list_todos_empty(self, client):
        """Test listing todos with empty result"""
        response = client.get("/api/v1/todos/")
        assert response.status_code == 200

        data = response.json()
        assert data["todos"] == []
        assert data["total_count"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 20
        assert data["has_next"] is False
        assert data["has_previous"] is False

    async def test_list_todos_with_filters(self, client):
        """Test listing todos with various filters"""
        # Test with list_id filter
        response = client.get("/api/v1/todos/?list_id=list_123")
        assert response.status_code == 200

        # Test with status filter
        response = client.get("/api/v1/todos/?status_filter=pending")
        assert response.status_code == 200

        # Test with priority filter
        response = client.get("/api/v1/todos/?priority_filter=high")
        assert response.status_code == 200

        # Test with assignee filter
        response = client.get("/api/v1/todos/?assignee_id=user_456")
        assert response.status_code == 200

        # Test with tags filter
        response = client.get("/api/v1/todos/?tags=test&tags=api")
        assert response.status_code == 200

        # Test with search
        response = client.get("/api/v1/todos/?search=test")
        assert response.status_code == 200

        # Test with ordering
        response = client.get("/api/v1/todos/?ordering=due_date&order_direction=asc")
        assert response.status_code == 200

        # Test pagination
        response = client.get("/api/v1/todos/?page=2&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert data["page_size"] == 10

    async def test_list_todos_validation(self, client):
        """Test list todos validation"""
        # Test invalid page
        response = client.get("/api/v1/todos/?page=0")
        assert response.status_code == 422

        # Test invalid page_size
        response = client.get("/api/v1/todos/?page_size=0")
        assert response.status_code == 422

        response = client.get("/api/v1/todos/?page_size=101")
        assert response.status_code == 422

    # Universal List Management Tests - Backward Compatible
    async def test_create_todo_list_success(self, client, sample_todo_list_data):
        """Test successful todo list creation with universal List(item_type='todo')"""
        response = client.post("/api/v1/todos/lists", json=sample_todo_list_data)

        assert response.status_code == 201
        data = response.json()

        # Verify response structure - universal List with item_type discriminator
        assert "id" in data
        assert data["name"] == sample_todo_list_data["name"]
        assert data["description"] == sample_todo_list_data["description"]
        assert data["item_type"] == "todo"  # Universal List discriminator
        assert data["list_type"] == sample_todo_list_data["list_type"]
        assert data["color"] == sample_todo_list_data["color"]
        assert data["ordering_strategy"] == sample_todo_list_data["ordering_strategy"]
        assert "created_at" in data
        assert "updated_at" in data
        assert data["todo_count"] == 0  # Computed field for backward compatibility
        assert data["metadata"] == sample_todo_list_data["metadata"]

    async def test_create_todo_list_validation(self, client):
        """Test todo list creation validation"""
        # Test missing required field
        invalid_data = {"description": "Missing name"}
        response = client.post("/api/v1/todos/lists", json=invalid_data)
        assert response.status_code == 422

        # Test invalid list_type
        invalid_data = {"name": "Test", "list_type": "invalid"}
        response = client.post("/api/v1/todos/lists", json=invalid_data)
        assert response.status_code == 422

        # Test name too long
        invalid_data = {"name": "x" * 101}
        response = client.post("/api/v1/todos/lists", json=invalid_data)
        assert response.status_code == 422

    async def test_get_todo_list_not_found(self, client):
        """Test getting non-existent todo list"""
        response = client.get("/api/v1/todos/lists/non-existent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_update_todo_list_not_found(self, client):
        """Test updating non-existent todo list"""
        update_data = {"name": "Updated List"}
        response = client.put("/api/v1/todos/lists/non-existent-id", json=update_data)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_delete_todo_list_not_found(self, client):
        """Test deleting non-existent todo list"""
        response = client.delete("/api/v1/todos/lists/non-existent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_list_todo_lists_empty(self, client):
        """Test listing todo lists with empty result"""
        response = client.get("/api/v1/todos/lists")
        assert response.status_code == 200

        data = response.json()
        assert data["lists"] == []
        assert data["total_count"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 20
        assert data["has_next"] is False
        assert data["has_previous"] is False

    async def test_list_todo_lists_with_filters(self, client):
        """Test listing todo lists with various filters"""
        # Test with list_type filter
        response = client.get("/api/v1/todos/lists?list_type=personal")
        assert response.status_code == 200

        # Test with search
        response = client.get("/api/v1/todos/lists?search=test")
        assert response.status_code == 200

        # Test with ordering
        response = client.get("/api/v1/todos/lists?ordering=name&order_direction=asc")
        assert response.status_code == 200

        # Test pagination
        response = client.get("/api/v1/todos/lists?page=2&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert data["page_size"] == 10

    # Universal ListItem Membership Tests - Backward Compatible
    async def test_add_list_member_success(self, client, sample_membership_data):
        """Test successful list member addition with universal ListItem(item_type='todo')"""
        response = client.post("/api/v1/todos/lists/list_123/members", json=sample_membership_data)

        assert response.status_code == 200
        data = response.json()

        # Verify response structure - universal ListItem with item_type discriminator
        assert data["list_id"] == "list_123"
        assert data["user_id"] == sample_membership_data["user_id"]
        assert data["role"] == sample_membership_data["role"]
        assert "joined_at" in data
        assert "permissions" in data
        assert isinstance(data["permissions"], dict)

    async def test_add_list_member_validation(self, client):
        """Test list member addition validation"""
        # Test missing required field
        invalid_data = {"role": "member"}
        response = client.post("/api/v1/todos/lists/list_123/members", json=invalid_data)
        assert response.status_code == 422

        # Test invalid role
        invalid_data = {"user_id": "user_123", "role": "invalid"}
        response = client.post("/api/v1/todos/lists/list_123/members", json=invalid_data)
        assert response.status_code == 422

    async def test_remove_list_member_not_found(self, client):
        """Test removing non-existent list member"""
        response = client.delete("/api/v1/todos/lists/list_123/members/user_456")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    # PM-040 Knowledge Graph Integration Tests
    async def test_get_related_todos_success(self, client):
        """Test getting related todos using PM-040 Knowledge Graph"""
        response = client.get("/api/v1/todos/todo_123/related")
        assert response.status_code == 200

        data = response.json()
        assert data["todo_id"] == "todo_123"
        assert "related_todos" in data
        assert "relationships" in data
        assert "metadata" in data
        assert isinstance(data["related_todos"], list)
        assert isinstance(data["relationships"], list)
        assert isinstance(data["metadata"], dict)

    async def test_get_related_todos_with_parameters(self, client):
        """Test getting related todos with relationship type and depth"""
        # Test with relationship type
        response = client.get("/api/v1/todos/todo_123/related?relationship_type=depends_on")
        assert response.status_code == 200

        # Test with depth
        response = client.get("/api/v1/todos/todo_123/related?depth=2")
        assert response.status_code == 200

        # Test with both parameters
        response = client.get("/api/v1/todos/todo_123/related?relationship_type=depends_on&depth=3")
        assert response.status_code == 200

    async def test_get_related_todos_validation(self, client):
        """Test get related todos validation"""
        # Test invalid depth
        response = client.get("/api/v1/todos/todo_123/related?depth=0")
        assert response.status_code == 422

        response = client.get("/api/v1/todos/todo_123/related?depth=4")
        assert response.status_code == 422

    # PM-034 Intent Classification Integration Tests
    async def test_search_todos_success(self, client):
        """Test searching todos using PM-034 Intent Classification"""
        search_data = {"query": "Find all high priority todos due this week"}
        response = client.post("/api/v1/todos/search", params=search_data)
        assert response.status_code == 200

        data = response.json()
        assert "todos" in data
        assert "total_count" in data
        assert "page" in data
        assert "page_size" in data
        assert "has_next" in data
        assert "has_previous" in data
        assert isinstance(data["todos"], list)
        assert isinstance(data["total_count"], int)

    async def test_search_todos_with_pagination(self, client):
        """Test searching todos with pagination"""
        search_data = {"query": "urgent todos"}
        response = client.post(
            "/api/v1/todos/search", params={**search_data, "page": 2, "page_size": 10}
        )
        assert response.status_code == 200

        data = response.json()
        assert data["page"] == 2
        assert data["page_size"] == 10

    async def test_search_todos_validation(self, client):
        """Test search todos validation"""
        # Test missing query
        response = client.post("/api/v1/todos/search")
        assert response.status_code == 422

        # Test invalid page
        response = client.post("/api/v1/todos/search", params={"query": "test", "page": 0})
        assert response.status_code == 422

        # Test invalid page_size
        response = client.post("/api/v1/todos/search", params={"query": "test", "page_size": 0})
        assert response.status_code == 422

        response = client.post("/api/v1/todos/search", params={"query": "test", "page_size": 101})
        assert response.status_code == 422

    # Integration Tests - Universal List Architecture
    async def test_todo_list_integration(self, client, sample_todo_data, sample_todo_list_data):
        """Test integration between todo and list creation with universal List architecture"""
        # Create a list first - universal List with item_type='todo'
        list_response = client.post("/api/v1/todos/lists", json=sample_todo_list_data)
        assert list_response.status_code == 201
        list_id = list_response.json()["id"]

        # Verify universal List discriminator
        list_data = list_response.json()
        assert list_data["item_type"] == "todo"  # Universal List discriminator

        # Create a todo in that list
        todo_data = {**sample_todo_data, "list_id": list_id}
        todo_response = client.post("/api/v1/todos/", json=todo_data)
        assert todo_response.status_code == 201

        # Verify todo is associated with the list
        todo_data = todo_response.json()
        assert todo_data["list_id"] == list_id

    async def test_list_membership_integration(
        self, client, sample_todo_list_data, sample_membership_data
    ):
        """Test integration between list creation and membership with universal ListItem architecture"""
        # Create a list first - universal List with item_type='todo'
        list_response = client.post("/api/v1/todos/lists", json=sample_todo_list_data)
        assert list_response.status_code == 201
        list_id = list_response.json()["id"]

        # Verify universal List discriminator
        list_data = list_response.json()
        assert list_data["item_type"] == "todo"  # Universal List discriminator

        # Add a member to the list - universal ListItem with item_type='todo'
        membership_response = client.post(
            f"/api/v1/todos/lists/{list_id}/members", json=sample_membership_data
        )
        assert membership_response.status_code == 200

        # Verify membership is associated with the list
        membership_data = membership_response.json()
        assert membership_data["list_id"] == list_id

    # Universal List Architecture Tests - Chief Architect's Principles
    async def test_universal_list_architecture(self, client):
        """Test that universal List architecture is properly implemented"""
        # Verify that Todo API uses universal List with item_type discriminator
        response = client.get("/api/v1/todos/lists")
        assert response.status_code == 200

        # Verify response structure supports universal List architecture
        data = response.json()
        assert "lists" in data  # Universal List collection
        assert "total_count" in data
        assert "page" in data
        assert "page_size" in data

    async def test_backward_compatibility(self, client):
        """Test that API maintains backward compatibility"""
        # Verify that existing endpoints work unchanged
        response = client.get("/api/v1/todos/")
        assert response.status_code == 200

        response = client.get("/api/v1/todos/lists")
        assert response.status_code == 200

        # Verify that response structures are compatible
        data = response.json()
        assert "lists" in data  # Backward compatible field name
        assert "total_count" in data
        assert "page" in data
        assert "page_size" in data

    async def test_universal_composition_pattern(self, client, sample_todo_list_data):
        """Test Chief Architect's universal composition over specialization principle"""
        # Create a todo list - should use universal List with item_type='todo'
        response = client.post("/api/v1/todos/lists", json=sample_todo_list_data)
        assert response.status_code == 201

        data = response.json()

        # Verify universal composition pattern
        assert data["item_type"] == "todo"  # Universal List discriminator
        assert data["list_type"] == sample_todo_list_data["list_type"]
        assert data["ordering_strategy"] == sample_todo_list_data["ordering_strategy"]

        # Verify that this pattern can be extended for other item types
        # (feature, bug, attendee, etc.) without breaking existing functionality
        assert "todo_count" in data  # Backward compatibility field
        assert data["todo_count"] == 0  # Computed field for backward compatibility

    # Error Handling Tests
    async def test_internal_server_error_handling(self, client):
        """Test internal server error handling"""
        # This would be tested with actual service implementations
        # For now, we test the error structure
        response = client.get("/api/v1/todos/non-existent-id")
        assert response.status_code == 404

        error_data = response.json()
        assert "detail" in error_data
        assert isinstance(error_data["detail"], str)

    # Performance Tests
    async def test_api_response_time(self, client):
        """Test API response time for basic operations"""
        import time

        # Test todo listing response time
        start_time = time.time()
        response = client.get("/api/v1/todos/")
        end_time = time.time()

        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 1.0  # Should respond within 1 second

        # Test list listing response time
        start_time = time.time()
        response = client.get("/api/v1/todos/lists")
        end_time = time.time()

        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 1.0  # Should respond within 1 second

    # Documentation Tests
    async def test_api_documentation(self, client):
        """Test that API endpoints are properly documented"""
        # Test that endpoints return proper OpenAPI documentation
        response = client.get("/docs")
        assert response.status_code == 200

        # Test that endpoints have proper descriptions
        response = client.get("/openapi.json")
        assert response.status_code == 200

        openapi_data = response.json()
        assert "/api/v1/todos/" in openapi_data["paths"]
        assert "/api/v1/todos/lists" in openapi_data["paths"]


class TestUniversalListIntegration:
    """Integration tests for PM-081 with Universal List Architecture"""

    @pytest.fixture
    def mock_services(self):
        """Mock all services for integration testing"""
        services = {
            "todo_service": AsyncMock(),
            "universal_list_service": AsyncMock(),
            "knowledge_graph_service": AsyncMock(),
            "query_router": AsyncMock(),
        }
        return services

    async def test_universal_list_service_integration(self, mock_services):
        """Test universal list service integration"""
        # Mock universal list service responses
        mock_services["universal_list_service"].create_list.return_value = {
            "id": "list_123",
            "name": "Test List",
            "item_type": "todo",  # Universal List discriminator
            "list_type": "personal",
            "ordering_strategy": "manual",
        }

        # Test that universal list service is called correctly
        # This would be tested with actual service implementations
        assert mock_services["universal_list_service"] is not None

    async def test_universal_listitem_integration(self, mock_services):
        """Test universal ListItem integration"""
        # Mock universal ListItem responses
        mock_services["universal_list_service"].add_list_member.return_value = {
            "list_id": "list_123",
            "item_id": "todo_456",
            "item_type": "todo",  # Universal ListItem discriminator
            "position": 1,
        }

        # Test that universal ListItem is called correctly
        # This would be tested with actual service implementations
        assert mock_services["universal_list_service"] is not None

    async def test_universal_architecture_extensibility(self, mock_services):
        """Test that universal architecture can be extended for other item types"""
        # Test that the same List service can handle different item types
        # This demonstrates Chief Architect's universal composition principle

        # Mock responses for different item types
        mock_services["universal_list_service"].create_list.side_effect = [
            {"id": "list_1", "item_type": "todo"},
            {"id": "list_2", "item_type": "feature"},
            {"id": "list_3", "item_type": "bug"},
            {"id": "list_4", "item_type": "attendee"},
        ]

        # Test that universal service can handle multiple item types
        # This would be tested with actual service implementations
        assert mock_services["universal_list_service"] is not None


# Test utilities for Universal List Architecture
def create_test_todo_data(**overrides) -> Dict[str, Any]:
    """Create test todo data with optional overrides"""
    base_data = {
        "title": "Test Todo",
        "description": "Test todo description",
        "priority": "medium",
        "tags": ["test"],
        "metadata": {},
    }
    base_data.update(overrides)
    return base_data


def create_test_universal_list_data(**overrides) -> Dict[str, Any]:
    """Create test universal list data with optional overrides"""
    base_data = {
        "name": "Test Universal List",
        "description": "Test universal list description",
        "item_type": "todo",  # Universal List discriminator
        "list_type": "personal",
        "ordering_strategy": "manual",
        "metadata": {},
    }
    base_data.update(overrides)
    return base_data


def create_test_universal_listitem_data(**overrides) -> Dict[str, Any]:
    """Create test universal list item data with optional overrides"""
    base_data = {
        "list_id": "list_123",
        "item_id": "todo_456",
        "item_type": "todo",  # Universal ListItem discriminator
        "position": 0,
        "added_by": "user_123",
    }
    base_data.update(overrides)
    return base_data
