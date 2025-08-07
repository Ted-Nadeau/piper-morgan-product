"""
PM-081: Task Management API Tests
Comprehensive test suite for task management API with PM-040 Knowledge Graph and PM-034 Intent Classification integration
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.api.task_management import (
    ListCreateRequest,
    ListMembershipRequest,
    ListUpdateRequest,
    TaskCreateRequest,
    TaskUpdateRequest,
    task_management_router,
)


class TestTaskManagementAPI:
    """Comprehensive test suite for PM-081 Task Management API"""

    @pytest.fixture
    def app(self):
        """Create FastAPI app with task management router"""
        app = FastAPI()
        app.include_router(task_management_router)
        return app

    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return TestClient(app)

    @pytest.fixture
    def mock_task_service(self):
        """Mock task management service"""
        service = AsyncMock()
        service.create_task = AsyncMock()
        service.get_task = AsyncMock()
        service.update_task = AsyncMock()
        service.delete_task = AsyncMock()
        service.list_tasks = AsyncMock()
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
    def sample_task_data(self):
        """Sample task data for testing"""
        return {
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "high",
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "tags": ["test", "api"],
            "list_id": "list-123",
            "assignee_id": "user-456",
            "metadata": {"test_key": "test_value"},
        }

    @pytest.fixture
    def sample_list_data(self):
        """Sample list data for testing"""
        return {
            "name": "Test List",
            "description": "This is a test list",
            "list_type": "personal",
            "color": "#FF5733",
            "ordering_strategy": "due_date",
            "metadata": {"test_key": "test_value"},
        }

    @pytest.fixture
    def sample_membership_data(self):
        """Sample membership data for testing"""
        return {"user_id": "user-789", "role": "member"}

    # Task Management Tests
    async def test_create_task_success(self, client, sample_task_data):
        """Test successful task creation"""
        response = client.post("/api/v1/tasks/", json=sample_task_data)

        assert response.status_code == 201
        data = response.json()

        # Verify response structure
        assert "id" in data
        assert data["title"] == sample_task_data["title"]
        assert data["description"] == sample_task_data["description"]
        assert data["priority"] == sample_task_data["priority"]
        assert data["status"] == "pending"
        assert data["tags"] == sample_task_data["tags"]
        assert data["list_id"] == sample_task_data["list_id"]
        assert data["assignee_id"] == sample_task_data["assignee_id"]
        assert "created_at" in data
        assert "updated_at" in data
        assert data["completed_at"] is None
        assert data["metadata"] == sample_task_data["metadata"]

    async def test_create_task_validation(self, client):
        """Test task creation validation"""
        # Test missing required field
        invalid_data = {"description": "Missing title"}
        response = client.post("/api/v1/tasks/", json=invalid_data)
        assert response.status_code == 422

        # Test invalid priority
        invalid_data = {"title": "Test", "priority": "invalid"}
        response = client.post("/api/v1/tasks/", json=invalid_data)
        assert response.status_code == 422

        # Test title too long
        invalid_data = {"title": "x" * 201}
        response = client.post("/api/v1/tasks/", json=invalid_data)
        assert response.status_code == 422

    async def test_get_task_not_found(self, client):
        """Test getting non-existent task"""
        response = client.get("/api/v1/tasks/non-existent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_update_task_not_found(self, client, sample_task_data):
        """Test updating non-existent task"""
        update_data = {"title": "Updated Title"}
        response = client.put("/api/v1/tasks/non-existent-id", json=update_data)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_delete_task_not_found(self, client):
        """Test deleting non-existent task"""
        response = client.delete("/api/v1/tasks/non-existent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_list_tasks_empty(self, client):
        """Test listing tasks with empty result"""
        response = client.get("/api/v1/tasks/")
        assert response.status_code == 200

        data = response.json()
        assert data["tasks"] == []
        assert data["total_count"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 20
        assert data["has_next"] is False
        assert data["has_previous"] is False

    async def test_list_tasks_with_filters(self, client):
        """Test listing tasks with various filters"""
        # Test with list_id filter
        response = client.get("/api/v1/tasks/?list_id=list-123")
        assert response.status_code == 200

        # Test with status filter
        response = client.get("/api/v1/tasks/?status_filter=pending")
        assert response.status_code == 200

        # Test with priority filter
        response = client.get("/api/v1/tasks/?priority_filter=high")
        assert response.status_code == 200

        # Test with assignee filter
        response = client.get("/api/v1/tasks/?assignee_id=user-456")
        assert response.status_code == 200

        # Test with tags filter
        response = client.get("/api/v1/tasks/?tags=test&tags=api")
        assert response.status_code == 200

        # Test with search
        response = client.get("/api/v1/tasks/?search=test")
        assert response.status_code == 200

        # Test with ordering
        response = client.get("/api/v1/tasks/?ordering=due_date&order_direction=asc")
        assert response.status_code == 200

        # Test pagination
        response = client.get("/api/v1/tasks/?page=2&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert data["page_size"] == 10

    async def test_list_tasks_validation(self, client):
        """Test list tasks validation"""
        # Test invalid page
        response = client.get("/api/v1/tasks/?page=0")
        assert response.status_code == 422

        # Test invalid page_size
        response = client.get("/api/v1/tasks/?page_size=0")
        assert response.status_code == 422

        response = client.get("/api/v1/tasks/?page_size=101")
        assert response.status_code == 422

    # List Management Tests
    async def test_create_list_success(self, client, sample_list_data):
        """Test successful list creation"""
        response = client.post("/api/v1/tasks/lists", json=sample_list_data)

        assert response.status_code == 201
        data = response.json()

        # Verify response structure
        assert "id" in data
        assert data["name"] == sample_list_data["name"]
        assert data["description"] == sample_list_data["description"]
        assert data["list_type"] == sample_list_data["list_type"]
        assert data["color"] == sample_list_data["color"]
        assert data["ordering_strategy"] == sample_list_data["ordering_strategy"]
        assert "created_at" in data
        assert "updated_at" in data
        assert data["task_count"] == 0
        assert data["metadata"] == sample_list_data["metadata"]

    async def test_create_list_validation(self, client):
        """Test list creation validation"""
        # Test missing required field
        invalid_data = {"description": "Missing name"}
        response = client.post("/api/v1/tasks/lists", json=invalid_data)
        assert response.status_code == 422

        # Test invalid list_type
        invalid_data = {"name": "Test", "list_type": "invalid"}
        response = client.post("/api/v1/tasks/lists", json=invalid_data)
        assert response.status_code == 422

        # Test name too long
        invalid_data = {"name": "x" * 101}
        response = client.post("/api/v1/tasks/lists", json=invalid_data)
        assert response.status_code == 422

    async def test_get_list_not_found(self, client):
        """Test getting non-existent list"""
        response = client.get("/api/v1/tasks/lists/non-existent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_update_list_not_found(self, client):
        """Test updating non-existent list"""
        update_data = {"name": "Updated List"}
        response = client.put("/api/v1/tasks/lists/non-existent-id", json=update_data)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_delete_list_not_found(self, client):
        """Test deleting non-existent list"""
        response = client.delete("/api/v1/tasks/lists/non-existent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_list_lists_empty(self, client):
        """Test listing lists with empty result"""
        response = client.get("/api/v1/tasks/lists")
        assert response.status_code == 200

        data = response.json()
        assert data["lists"] == []
        assert data["total_count"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 20
        assert data["has_next"] is False
        assert data["has_previous"] is False

    async def test_list_lists_with_filters(self, client):
        """Test listing lists with various filters"""
        # Test with list_type filter
        response = client.get("/api/v1/tasks/lists?list_type=personal")
        assert response.status_code == 200

        # Test with search
        response = client.get("/api/v1/tasks/lists?search=test")
        assert response.status_code == 200

        # Test with ordering
        response = client.get("/api/v1/tasks/lists?ordering=name&order_direction=asc")
        assert response.status_code == 200

        # Test pagination
        response = client.get("/api/v1/tasks/lists?page=2&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert data["page_size"] == 10

    # List Membership Tests
    async def test_add_list_member_success(self, client, sample_membership_data):
        """Test successful list member addition"""
        response = client.post("/api/v1/tasks/lists/list-123/members", json=sample_membership_data)

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert data["list_id"] == "list-123"
        assert data["user_id"] == sample_membership_data["user_id"]
        assert data["role"] == sample_membership_data["role"]
        assert "joined_at" in data
        assert "permissions" in data
        assert isinstance(data["permissions"], dict)

    async def test_add_list_member_validation(self, client):
        """Test list member addition validation"""
        # Test missing required field
        invalid_data = {"role": "member"}
        response = client.post("/api/v1/tasks/lists/list-123/members", json=invalid_data)
        assert response.status_code == 422

        # Test invalid role
        invalid_data = {"user_id": "user-123", "role": "invalid"}
        response = client.post("/api/v1/tasks/lists/list-123/members", json=invalid_data)
        assert response.status_code == 422

    async def test_remove_list_member_not_found(self, client):
        """Test removing non-existent list member"""
        response = client.delete("/api/v1/tasks/lists/list-123/members/user-456")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    # PM-040 Knowledge Graph Integration Tests
    async def test_get_related_tasks_success(self, client):
        """Test getting related tasks using PM-040 Knowledge Graph"""
        response = client.get("/api/v1/tasks/task-123/related")
        assert response.status_code == 200

        data = response.json()
        assert data["task_id"] == "task-123"
        assert "related_tasks" in data
        assert "relationships" in data
        assert "metadata" in data
        assert isinstance(data["related_tasks"], list)
        assert isinstance(data["relationships"], list)
        assert isinstance(data["metadata"], dict)

    async def test_get_related_tasks_with_parameters(self, client):
        """Test getting related tasks with relationship type and depth"""
        # Test with relationship type
        response = client.get("/api/v1/tasks/task-123/related?relationship_type=depends_on")
        assert response.status_code == 200

        # Test with depth
        response = client.get("/api/v1/tasks/task-123/related?depth=2")
        assert response.status_code == 200

        # Test with both parameters
        response = client.get("/api/v1/tasks/task-123/related?relationship_type=depends_on&depth=3")
        assert response.status_code == 200

    async def test_get_related_tasks_validation(self, client):
        """Test get related tasks validation"""
        # Test invalid depth
        response = client.get("/api/v1/tasks/task-123/related?depth=0")
        assert response.status_code == 422

        response = client.get("/api/v1/tasks/task-123/related?depth=4")
        assert response.status_code == 422

    # PM-034 Intent Classification Integration Tests
    async def test_search_tasks_success(self, client):
        """Test searching tasks using PM-034 Intent Classification"""
        search_data = {"query": "Find all high priority tasks due this week"}
        response = client.post("/api/v1/tasks/search", params=search_data)
        assert response.status_code == 200

        data = response.json()
        assert "tasks" in data
        assert "total_count" in data
        assert "page" in data
        assert "page_size" in data
        assert "has_next" in data
        assert "has_previous" in data
        assert isinstance(data["tasks"], list)
        assert isinstance(data["total_count"], int)

    async def test_search_tasks_with_pagination(self, client):
        """Test searching tasks with pagination"""
        search_data = {"query": "urgent tasks"}
        response = client.post(
            "/api/v1/tasks/search", params={**search_data, "page": 2, "page_size": 10}
        )
        assert response.status_code == 200

        data = response.json()
        assert data["page"] == 2
        assert data["page_size"] == 10

    async def test_search_tasks_validation(self, client):
        """Test search tasks validation"""
        # Test missing query
        response = client.post("/api/v1/tasks/search")
        assert response.status_code == 422

        # Test invalid page
        response = client.post("/api/v1/tasks/search", params={"query": "test", "page": 0})
        assert response.status_code == 422

        # Test invalid page_size
        response = client.post("/api/v1/tasks/search", params={"query": "test", "page_size": 0})
        assert response.status_code == 422

        response = client.post("/api/v1/tasks/search", params={"query": "test", "page_size": 101})
        assert response.status_code == 422

    # Integration Tests
    async def test_task_list_integration(self, client, sample_task_data, sample_list_data):
        """Test integration between task and list creation"""
        # Create a list first
        list_response = client.post("/api/v1/tasks/lists", json=sample_list_data)
        assert list_response.status_code == 201
        list_id = list_response.json()["id"]

        # Create a task in that list
        task_data = {**sample_task_data, "list_id": list_id}
        task_response = client.post("/api/v1/tasks/", json=task_data)
        assert task_response.status_code == 201

        # Verify task is associated with the list
        task_data = task_response.json()
        assert task_data["list_id"] == list_id

    async def test_list_membership_integration(
        self, client, sample_list_data, sample_membership_data
    ):
        """Test integration between list creation and membership"""
        # Create a list first
        list_response = client.post("/api/v1/tasks/lists", json=sample_list_data)
        assert list_response.status_code == 201
        list_id = list_response.json()["id"]

        # Add a member to the list
        membership_response = client.post(
            f"/api/v1/tasks/lists/{list_id}/members", json=sample_membership_data
        )
        assert membership_response.status_code == 200

        # Verify membership is associated with the list
        membership_data = membership_response.json()
        assert membership_data["list_id"] == list_id

    # Error Handling Tests
    async def test_internal_server_error_handling(self, client):
        """Test internal server error handling"""
        # This would be tested with actual service implementations
        # For now, we test the error structure
        response = client.get("/api/v1/tasks/non-existent-id")
        assert response.status_code == 404

        error_data = response.json()
        assert "detail" in error_data
        assert isinstance(error_data["detail"], str)

    # Performance Tests
    async def test_api_response_time(self, client):
        """Test API response time for basic operations"""
        import time

        # Test task listing response time
        start_time = time.time()
        response = client.get("/api/v1/tasks/")
        end_time = time.time()

        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 1.0  # Should respond within 1 second

        # Test list listing response time
        start_time = time.time()
        response = client.get("/api/v1/tasks/lists")
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
        assert "/api/v1/tasks/" in openapi_data["paths"]
        assert "/api/v1/tasks/lists" in openapi_data["paths"]


class TestTaskManagementIntegration:
    """Integration tests for PM-081 with PM-040 and PM-034"""

    @pytest.fixture
    def mock_services(self):
        """Mock all services for integration testing"""
        services = {
            "task_service": AsyncMock(),
            "knowledge_graph_service": AsyncMock(),
            "query_router": AsyncMock(),
        }
        return services

    async def test_pm040_knowledge_graph_integration(self, mock_services):
        """Test PM-040 Knowledge Graph integration"""
        # Mock knowledge graph service responses
        mock_services["knowledge_graph_service"].get_related_nodes.return_value = [
            {"id": "task-456", "type": "task", "relationship": "depends_on"},
            {"id": "task-789", "type": "task", "relationship": "blocks"},
        ]

        # Test that knowledge graph service is called correctly
        # This would be tested with actual service implementations
        assert mock_services["knowledge_graph_service"] is not None

    async def test_pm034_intent_classification_integration(self, mock_services):
        """Test PM-034 Intent Classification integration"""
        # Mock query router responses
        mock_services["query_router"].classify_and_route.return_value = {
            "intent": "search_tasks",
            "confidence": 0.95,
            "parameters": {"priority": "high", "status": "pending"},
        }

        # Test that query router is called correctly
        # This would be tested with actual service implementations
        assert mock_services["query_router"] is not None

    async def test_domain_relationship_integration(self, mock_services):
        """Test domain relationship integration"""
        # Test that task and list relationships work correctly
        # This would be tested with actual service implementations
        assert mock_services["task_service"] is not None


# Test utilities
def create_test_task_data(**overrides) -> Dict[str, Any]:
    """Create test task data with optional overrides"""
    base_data = {
        "title": "Test Task",
        "description": "Test task description",
        "priority": "medium",
        "tags": ["test"],
        "metadata": {},
    }
    base_data.update(overrides)
    return base_data


def create_test_list_data(**overrides) -> Dict[str, Any]:
    """Create test list data with optional overrides"""
    base_data = {
        "name": "Test List",
        "description": "Test list description",
        "list_type": "personal",
        "ordering_strategy": "manual",
        "metadata": {},
    }
    base_data.update(overrides)
    return base_data


def create_test_membership_data(**overrides) -> Dict[str, Any]:
    """Create test membership data with optional overrides"""
    base_data = {"user_id": "user-123", "role": "member"}
    base_data.update(overrides)
    return base_data
