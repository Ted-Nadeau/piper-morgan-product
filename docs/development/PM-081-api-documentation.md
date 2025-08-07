# PM-081 Task Management API Documentation

**Project**: PM-081 Task Management
**Date**: August 5, 2025
**Status**: ✅ API Foundation Complete

## Overview

The PM-081 Task Management API provides comprehensive task and list management capabilities with integration to PM-040 Knowledge Graph and PM-034 Intent Classification. This API enables users to create, manage, and organize tasks with advanced features like natural language search and relationship discovery.

## Base URL

```
/api/v1/tasks
```

## Authentication

All endpoints require authentication. Include your API key in the request headers:

```
Authorization: Bearer YOUR_API_KEY
```

## Response Format

All API responses follow a consistent JSON format:

```json
{
  "data": {
    // Response data
  },
  "meta": {
    "timestamp": "2025-08-05T12:30:00Z",
    "request_id": "req_123456789"
  }
}
```

## Error Handling

The API uses standard HTTP status codes and returns error details in the response body:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": {
      "field": "title",
      "issue": "Title is required"
    }
  }
}
```

## Task Management Endpoints

### Create Task

**POST** `/api/v1/tasks/`

Create a new task with PM-040 Knowledge Graph integration.

**Request Body:**
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the new feature",
  "priority": "high",
  "due_date": "2025-08-15T23:59:59Z",
  "tags": ["documentation", "project"],
  "list_id": "list_123",
  "assignee_id": "user_456",
  "metadata": {
    "project_id": "proj_789",
    "estimated_hours": 4
  }
}
```

**Response:**
```json
{
  "id": "task_abc123",
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the new feature",
  "priority": "high",
  "status": "pending",
  "due_date": "2025-08-15T23:59:59Z",
  "tags": ["documentation", "project"],
  "list_id": "list_123",
  "assignee_id": "user_456",
  "created_at": "2025-08-05T12:30:00Z",
  "updated_at": "2025-08-05T12:30:00Z",
  "completed_at": null,
  "metadata": {
    "project_id": "proj_789",
    "estimated_hours": 4
  }
}
```

**Validation Rules:**
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters
- `priority`: Must be one of: `low`, `medium`, `high`, `urgent`
- `due_date`: Optional, ISO 8601 format
- `tags`: Optional array of strings
- `list_id`: Optional, must reference existing list
- `assignee_id`: Optional, must reference existing user
- `metadata`: Optional object

### Get Task

**GET** `/api/v1/tasks/{task_id}`

Retrieve a specific task with PM-040 Knowledge Graph context.

**Response:**
```json
{
  "id": "task_abc123",
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the new feature",
  "priority": "high",
  "status": "in_progress",
  "due_date": "2025-08-15T23:59:59Z",
  "tags": ["documentation", "project"],
  "list_id": "list_123",
  "assignee_id": "user_456",
  "created_at": "2025-08-05T12:30:00Z",
  "updated_at": "2025-08-05T14:15:00Z",
  "completed_at": null,
  "metadata": {
    "project_id": "proj_789",
    "estimated_hours": 4
  }
}
```

### Update Task

**PUT** `/api/v1/tasks/{task_id}`

Update a task with PM-040 Knowledge Graph integration.

**Request Body:**
```json
{
  "title": "Updated task title",
  "status": "completed",
  "completed_at": "2025-08-05T16:00:00Z"
}
```

**Response:** Same as Get Task

### Delete Task

**DELETE** `/api/v1/tasks/{task_id}`

Delete a task and remove from PM-040 Knowledge Graph.

**Response:** 204 No Content

### List Tasks

**GET** `/api/v1/tasks/`

List tasks with advanced filtering and PM-040 Knowledge Graph integration.

**Query Parameters:**
- `page` (int): Page number (default: 1, min: 1)
- `page_size` (int): Items per page (default: 20, min: 1, max: 100)
- `list_id` (string): Filter by list ID
- `status_filter` (string): Filter by status (`pending`, `in_progress`, `completed`, `cancelled`)
- `priority_filter` (string): Filter by priority (`low`, `medium`, `high`, `urgent`)
- `assignee_id` (string): Filter by assignee ID
- `tags` (array): Filter by tags
- `search` (string): Search in title and description
- `ordering` (string): Order by field (`created_at`, `due_date`, `priority`, `title`)
- `order_direction` (string): Order direction (`asc`, `desc`)

**Example Request:**
```
GET /api/v1/tasks/?list_id=list_123&priority_filter=high&page=1&page_size=10
```

**Response:**
```json
{
  "tasks": [
    {
      "id": "task_abc123",
      "title": "Complete project documentation",
      "description": "Write comprehensive documentation for the new feature",
      "priority": "high",
      "status": "pending",
      "due_date": "2025-08-15T23:59:59Z",
      "tags": ["documentation", "project"],
      "list_id": "list_123",
      "assignee_id": "user_456",
      "created_at": "2025-08-05T12:30:00Z",
      "updated_at": "2025-08-05T12:30:00Z",
      "completed_at": null,
      "metadata": {}
    }
  ],
  "total_count": 1,
  "page": 1,
  "page_size": 10,
  "has_next": false,
  "has_previous": false
}
```

## List Management Endpoints

### Create List

**POST** `/api/v1/tasks/lists`

Create a new list with PM-040 Knowledge Graph integration.

**Request Body:**
```json
{
  "name": "Project Alpha Tasks",
  "description": "Tasks for Project Alpha development",
  "list_type": "project",
  "color": "#FF5733",
  "ordering_strategy": "due_date",
  "metadata": {
    "project_id": "proj_789",
    "team_id": "team_456"
  }
}
```

**Response:**
```json
{
  "id": "list_123",
  "name": "Project Alpha Tasks",
  "description": "Tasks for Project Alpha development",
  "list_type": "project",
  "color": "#FF5733",
  "ordering_strategy": "due_date",
  "created_at": "2025-08-05T12:30:00Z",
  "updated_at": "2025-08-05T12:30:00Z",
  "task_count": 0,
  "metadata": {
    "project_id": "proj_789",
    "team_id": "team_456"
  }
}
```

**Validation Rules:**
- `name`: Required, 1-100 characters
- `description`: Optional, max 500 characters
- `list_type`: Must be one of: `personal`, `shared`, `project`
- `color`: Optional, hex color code
- `ordering_strategy`: Must be one of: `manual`, `due_date`, `priority`, `created`
- `metadata`: Optional object

### Get List

**GET** `/api/v1/tasks/lists/{list_id}`

Retrieve a specific list with PM-040 Knowledge Graph context.

**Response:** Same as Create List

### Update List

**PUT** `/api/v1/tasks/lists/{list_id}`

Update a list with PM-040 Knowledge Graph integration.

**Request Body:**
```json
{
  "name": "Updated list name",
  "color": "#33FF57"
}
```

**Response:** Same as Create List

### Delete List

**DELETE** `/api/v1/tasks/lists/{list_id}`

Delete a list and remove from PM-040 Knowledge Graph.

**Response:** 204 No Content

### List Lists

**GET** `/api/v1/tasks/lists`

List lists with filtering and PM-040 Knowledge Graph integration.

**Query Parameters:**
- `page` (int): Page number (default: 1, min: 1)
- `page_size` (int): Items per page (default: 20, min: 1, max: 100)
- `list_type` (string): Filter by list type
- `search` (string): Search in name and description
- `ordering` (string): Order by field (`created_at`, `name`, `task_count`)
- `order_direction` (string): Order direction (`asc`, `desc`)

**Response:**
```json
{
  "lists": [
    {
      "id": "list_123",
      "name": "Project Alpha Tasks",
      "description": "Tasks for Project Alpha development",
      "list_type": "project",
      "color": "#FF5733",
      "ordering_strategy": "due_date",
      "created_at": "2025-08-05T12:30:00Z",
      "updated_at": "2025-08-05T12:30:00Z",
      "task_count": 5,
      "metadata": {}
    }
  ],
  "total_count": 1,
  "page": 1,
  "page_size": 20,
  "has_next": false,
  "has_previous": false
}
```

## List Membership Endpoints

### Add List Member

**POST** `/api/v1/tasks/lists/{list_id}/members`

Add a member to a list with PM-040 Knowledge Graph integration.

**Request Body:**
```json
{
  "user_id": "user_789",
  "role": "member"
}
```

**Response:**
```json
{
  "list_id": "list_123",
  "user_id": "user_789",
  "role": "member",
  "joined_at": "2025-08-05T12:30:00Z",
  "permissions": {
    "read": true,
    "write": true,
    "admin": false
  }
}
```

**Validation Rules:**
- `user_id`: Required, must reference existing user
- `role`: Must be one of: `owner`, `admin`, `member`, `viewer`

### Remove List Member

**DELETE** `/api/v1/tasks/lists/{list_id}/members/{user_id}`

Remove a member from a list.

**Response:** 204 No Content

## PM-040 Knowledge Graph Integration Endpoints

### Get Related Tasks

**GET** `/api/v1/tasks/{task_id}/related`

Get related tasks using PM-040 Knowledge Graph.

**Query Parameters:**
- `relationship_type` (string): Type of relationship to explore
- `depth` (int): Depth of relationship exploration (default: 1, min: 1, max: 3)

**Example Request:**
```
GET /api/v1/tasks/task_abc123/related?relationship_type=depends_on&depth=2
```

**Response:**
```json
{
  "task_id": "task_abc123",
  "related_tasks": [
    {
      "id": "task_def456",
      "title": "Prerequisite task",
      "relationship": "depends_on",
      "distance": 1
    },
    {
      "id": "task_ghi789",
      "title": "Another related task",
      "relationship": "blocks",
      "distance": 2
    }
  ],
  "relationships": [
    {
      "source": "task_abc123",
      "target": "task_def456",
      "type": "depends_on",
      "metadata": {}
    }
  ],
  "metadata": {
    "total_related": 2,
    "max_depth": 2,
    "relationship_types": ["depends_on", "blocks"]
  }
}
```

## PM-034 Intent Classification Integration Endpoints

### Search Tasks

**POST** `/api/v1/tasks/search`

Search tasks using PM-034 Intent Classification and PM-040 Knowledge Graph.

**Query Parameters:**
- `query` (string): Natural language search query (required)
- `page` (int): Page number (default: 1, min: 1)
- `page_size` (int): Items per page (default: 20, min: 1, max: 100)

**Example Request:**
```
POST /api/v1/tasks/search?query=Find all high priority tasks due this week
```

**Response:**
```json
{
  "tasks": [
    {
      "id": "task_abc123",
      "title": "Complete project documentation",
      "description": "Write comprehensive documentation for the new feature",
      "priority": "high",
      "status": "pending",
      "due_date": "2025-08-15T23:59:59Z",
      "tags": ["documentation", "project"],
      "list_id": "list_123",
      "assignee_id": "user_456",
      "created_at": "2025-08-05T12:30:00Z",
      "updated_at": "2025-08-05T12:30:00Z",
      "completed_at": null,
      "metadata": {},
      "relevance_score": 0.95,
      "search_context": {
        "intent": "search_high_priority_tasks",
        "confidence": 0.92,
        "extracted_filters": {
          "priority": "high",
          "timeframe": "this_week"
        }
      }
    }
  ],
  "total_count": 1,
  "page": 1,
  "page_size": 20,
  "has_next": false,
  "has_previous": false,
  "search_metadata": {
    "query": "Find all high priority tasks due this week",
    "intent_classified": true,
    "knowledge_graph_used": true,
    "response_time_ms": 150
  }
}
```

## Usage Examples

### Basic Task Management

```python
import requests

# Create a task
task_data = {
    "title": "Review pull request #123",
    "description": "Review the new authentication feature",
    "priority": "high",
    "tags": ["code-review", "authentication"],
    "list_id": "list_456"
}

response = requests.post(
    "https://api.example.com/api/v1/tasks/",
    json=task_data,
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

task = response.json()
print(f"Created task: {task['title']}")

# Update task status
update_data = {"status": "completed"}
response = requests.put(
    f"https://api.example.com/api/v1/tasks/{task['id']}",
    json=update_data,
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
```

### List Management

```python
# Create a project list
list_data = {
    "name": "Sprint 15 Tasks",
    "description": "Tasks for the current sprint",
    "list_type": "project",
    "color": "#4CAF50",
    "ordering_strategy": "priority"
}

response = requests.post(
    "https://api.example.com/api/v1/tasks/lists",
    json=list_data,
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

project_list = response.json()

# Add team members
members = ["user_123", "user_456", "user_789"]
for user_id in members:
    membership_data = {"user_id": user_id, "role": "member"}
    requests.post(
        f"https://api.example.com/api/v1/tasks/lists/{project_list['id']}/members",
        json=membership_data,
        headers={"Authorization": "Bearer YOUR_API_KEY"}
    )
```

### Natural Language Search

```python
# Search for urgent tasks
search_query = "Show me all urgent tasks that are blocking other work"
response = requests.post(
    "https://api.example.com/api/v1/tasks/search",
    params={"query": search_query},
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

results = response.json()
for task in results["tasks"]:
    print(f"Found task: {task['title']} (relevance: {task['relevance_score']})")
```

### Knowledge Graph Integration

```python
# Find related tasks
response = requests.get(
    "https://api.example.com/api/v1/tasks/task_abc123/related",
    params={"relationship_type": "depends_on", "depth": 2},
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

related = response.json()
for task in related["related_tasks"]:
    print(f"Related: {task['title']} ({task['relationship']})")
```

### Advanced Filtering

```python
# Get high priority tasks due this week
params = {
    "priority_filter": "high",
    "status_filter": "pending",
    "ordering": "due_date",
    "order_direction": "asc",
    "page": 1,
    "page_size": 50
}

response = requests.get(
    "https://api.example.com/api/v1/tasks/",
    params=params,
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

tasks = response.json()
print(f"Found {tasks['total_count']} high priority pending tasks")
```

## Error Codes

| Code | Description |
|------|-------------|
| `VALIDATION_ERROR` | Request data validation failed |
| `NOT_FOUND` | Resource not found |
| `PERMISSION_DENIED` | Insufficient permissions |
| `RATE_LIMITED` | Too many requests |
| `INTERNAL_ERROR` | Server error |

## Rate Limiting

- **Standard endpoints**: 1000 requests per hour
- **Search endpoints**: 100 requests per hour
- **Knowledge Graph endpoints**: 500 requests per hour

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Integration Notes

### PM-040 Knowledge Graph Integration

- Tasks and lists are automatically added to the knowledge graph
- Relationships between tasks are discovered and stored
- Related tasks can be found using graph traversal algorithms
- Metadata is preserved for enhanced search capabilities

### PM-034 Intent Classification Integration

- Natural language queries are classified using LLM intent classification
- Search results are enhanced with semantic understanding
- Query context is preserved for improved relevance
- A/B testing is used for continuous improvement

### Performance Considerations

- All endpoints are designed for sub-200ms response times
- Pagination is implemented for large result sets
- Caching is used for frequently accessed data
- Background processing is used for knowledge graph updates

## SDK Support

Official SDKs are available for:
- Python
- JavaScript/TypeScript
- Go
- Java

See the [SDK Documentation](https://docs.example.com/sdks) for detailed usage examples.

## Support

For API support and questions:
- Email: api-support@example.com
- Documentation: https://docs.example.com/api
- Status page: https://status.example.com
