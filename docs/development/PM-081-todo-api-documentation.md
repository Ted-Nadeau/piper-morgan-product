# PM-081 Todo Management API Documentation

**Project**: PM-081 Todo Management
**Date**: August 5, 2025
**Status**: ✅ API Foundation Complete

## Overview

The PM-081 Todo Management API provides clean user-facing todo management capabilities with integration to PM-040 Knowledge Graph and PM-034 Intent Classification. This API is completely separate from the existing workflow Task system, providing semantic clarity and optimal integration opportunities.

## Architecture Separation

### Clean Separation from Existing Systems

**Existing Task System**: Workflow orchestration tasks (system automation)

- `TaskType.ANALYZE_REQUEST`, `EXTRACT_REQUIREMENTS`, `CREATE_WORK_ITEM`
- `TaskStatus.PENDING`, `RUNNING`, `COMPLETED`, `FAILED`, `SKIPPED`
- Purpose: Internal workflow orchestration

**PM-081 Todo System**: User-facing task management

- `TodoPriority`: `low`, `medium`, `high`, `urgent`
- `TodoStatus`: `pending`, `in_progress`, `completed`, `cancelled`
- Purpose: User task management and organization

**Zero Breaking Changes**: The Todo system operates independently without affecting existing workflow orchestration.

## Base URL

```
/api/v1/todos
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

## Todo Management Endpoints

### Create Todo

**POST** `/api/v1/todos/`

Create a new todo with PM-040 Knowledge Graph integration.

**Request Body:**

```json
{
  "title": "Review authentication PR",
  "description": "Review the new OAuth implementation",
  "priority": "high",
  "due_date": "2025-08-15T23:59:59Z",
  "tags": ["code-review", "authentication"],
  "list_id": "list_123",
  "assignee_id": "user_456",
  "metadata": {
    "project_id": "proj_789",
    "estimated_hours": 2
  }
}
```

**Response:**

```json
{
  "id": "todo_abc123",
  "title": "Review authentication PR",
  "description": "Review the new OAuth implementation",
  "priority": "high",
  "status": "pending",
  "due_date": "2025-08-15T23:59:59Z",
  "tags": ["code-review", "authentication"],
  "list_id": "list_123",
  "assignee_id": "user_456",
  "created_at": "2025-08-05T12:30:00Z",
  "updated_at": "2025-08-05T12:30:00Z",
  "completed_at": null,
  "metadata": {
    "project_id": "proj_789",
    "estimated_hours": 2
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

### Get Todo

**GET** `/api/v1/todos/{todo_id}`

Retrieve a specific todo with PM-040 Knowledge Graph context.

**Response:**

```json
{
  "id": "todo_abc123",
  "title": "Review authentication PR",
  "description": "Review the new OAuth implementation",
  "priority": "high",
  "status": "in_progress",
  "due_date": "2025-08-15T23:59:59Z",
  "tags": ["code-review", "authentication"],
  "list_id": "list_123",
  "assignee_id": "user_456",
  "created_at": "2025-08-05T12:30:00Z",
  "updated_at": "2025-08-05T14:15:00Z",
  "completed_at": null,
  "metadata": {
    "project_id": "proj_789",
    "estimated_hours": 2
  }
}
```

### Update Todo

**PUT** `/api/v1/todos/{todo_id}`

Update a todo with PM-040 Knowledge Graph integration.

**Request Body:**

```json
{
  "title": "Updated todo title",
  "status": "completed",
  "completed_at": "2025-08-05T16:00:00Z"
}
```

**Response:** Same as Get Todo

### Delete Todo

**DELETE** `/api/v1/todos/{todo_id}`

Delete a todo and remove from PM-040 Knowledge Graph.

**Response:** 204 No Content

### List Todos

**GET** `/api/v1/todos/`

List todos with advanced filtering and PM-040 Knowledge Graph integration.

**Query Parameters:**

- `page` (int): Page number (default: 1, min: 1)
- `page_size` (int): Items per page (default: 20, min: 1, max: 100)
- `list_id` (string): Filter by list ID
- `status_filter` (string): Filter by status (`pending`, `in_progress`, `completed`, `cancelled`)
- `priority_filter` (string): Filter by priority (`low`, `medium`, `high`, `urgent`)
- `assignee_id` (string): Filter by assignee ID
- `tags` (array): Filter by tags
- `search` (string): Search in todo title and description
- `ordering` (string): Order by field (`created_at`, `due_date`, `priority`, `title`)
- `order_direction` (string): Order direction (`asc`, `desc`)

**Example Request:**

```
GET /api/v1/todos/?list_id=list_123&priority_filter=high&page=1&page_size=10
```

**Response:**

```json
{
  "todos": [
    {
      "id": "todo_abc123",
      "title": "Review authentication PR",
      "description": "Review the new OAuth implementation",
      "priority": "high",
      "status": "pending",
      "due_date": "2025-08-15T23:59:59Z",
      "tags": ["code-review", "authentication"],
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

## Todo List Management Endpoints

### Create Todo List

**POST** `/api/v1/todos/lists`

Create a new todo list with PM-040 Knowledge Graph integration.

**Request Body:**

```json
{
  "name": "Sprint 15 Todos",
  "description": "Todos for the current sprint",
  "list_type": "project",
  "color": "#4CAF50",
  "ordering_strategy": "priority",
  "metadata": {
    "sprint_id": "sprint_15",
    "team_id": "team_456"
  }
}
```

**Response:**

```json
{
  "id": "list_123",
  "name": "Sprint 15 Todos",
  "description": "Todos for the current sprint",
  "list_type": "project",
  "color": "#4CAF50",
  "ordering_strategy": "priority",
  "created_at": "2025-08-05T12:30:00Z",
  "updated_at": "2025-08-05T12:30:00Z",
  "todo_count": 0,
  "metadata": {
    "sprint_id": "sprint_15",
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

### Get Todo List

**GET** `/api/v1/todos/lists/{list_id}`

Retrieve a specific todo list with PM-040 Knowledge Graph context.

**Response:** Same as Create Todo List

### Update Todo List

**PUT** `/api/v1/todos/lists/{list_id}`

Update a todo list with PM-040 Knowledge Graph integration.

**Request Body:**

```json
{
  "name": "Updated list name",
  "color": "#33FF57"
}
```

**Response:** Same as Create Todo List

### Delete Todo List

**DELETE** `/api/v1/todos/lists/{list_id}`

Delete a todo list and remove from PM-040 Knowledge Graph.

**Response:** 204 No Content

### List Todo Lists

**GET** `/api/v1/todos/lists`

List todo lists with filtering and PM-040 Knowledge Graph integration.

**Query Parameters:**

- `page` (int): Page number (default: 1, min: 1)
- `page_size` (int): Items per page (default: 20, min: 1, max: 100)
- `list_type` (string): Filter by list type
- `search` (string): Search in list name and description
- `ordering` (string): Order by field (`created_at`, `name`, `todo_count`)
- `order_direction` (string): Order direction (`asc`, `desc`)

**Response:**

```json
{
  "lists": [
    {
      "id": "list_123",
      "name": "Sprint 15 Todos",
      "description": "Todos for the current sprint",
      "list_type": "project",
      "color": "#4CAF50",
      "ordering_strategy": "priority",
      "created_at": "2025-08-05T12:30:00Z",
      "updated_at": "2025-08-05T12:30:00Z",
      "todo_count": 5,
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

**POST** `/api/v1/todos/lists/{list_id}/members`

Add a member to a todo list with PM-040 Knowledge Graph integration.

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

**DELETE** `/api/v1/todos/lists/{list_id}/members/{user_id}`

Remove a member from a todo list.

**Response:** 204 No Content

## PM-040 Knowledge Graph Integration Endpoints

### Get Related Todos

**GET** `/api/v1/todos/{todo_id}/related`

Get related todos using PM-040 Knowledge Graph.

**Query Parameters:**

- `relationship_type` (string): Type of relationship to explore
- `depth` (int): Depth of relationship exploration (default: 1, min: 1, max: 3)

**Example Request:**

```
GET /api/v1/todos/todo_abc123/related?relationship_type=depends_on&depth=2
```

**Response:**

```json
{
  "todo_id": "todo_abc123",
  "related_todos": [
    {
      "id": "todo_def456",
      "title": "Prerequisite todo",
      "relationship": "depends_on",
      "distance": 1
    },
    {
      "id": "todo_ghi789",
      "title": "Another related todo",
      "relationship": "blocks",
      "distance": 2
    }
  ],
  "relationships": [
    {
      "source": "todo_abc123",
      "target": "todo_def456",
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

### Search Todos

**POST** `/api/v1/todos/search`

Search todos using PM-034 Intent Classification and PM-040 Knowledge Graph.

**Query Parameters:**

- `query` (string): Natural language search query (required)
- `page` (int): Page number (default: 1, min: 1)
- `page_size` (int): Items per page (default: 20, min: 1, max: 100)

**Example Request:**

```
POST /api/v1/todos/search?query=Find all high priority todos due this week
```

**Response:**

```json
{
  "todos": [
    {
      "id": "todo_abc123",
      "title": "Review authentication PR",
      "description": "Review the new OAuth implementation",
      "priority": "high",
      "status": "pending",
      "due_date": "2025-08-15T23:59:59Z",
      "tags": ["code-review", "authentication"],
      "list_id": "list_123",
      "assignee_id": "user_456",
      "created_at": "2025-08-05T12:30:00Z",
      "updated_at": "2025-08-05T12:30:00Z",
      "completed_at": null,
      "metadata": {},
      "relevance_score": 0.95,
      "search_context": {
        "intent": "search_high_priority_todos",
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
    "query": "Find all high priority todos due this week",
    "intent_classified": true,
    "knowledge_graph_used": true,
    "response_time_ms": 150
  }
}
```

## Usage Examples

### Basic Todo Management

```python
import requests

# Create a todo
todo_data = {
    "title": "Review pull request #123",
    "description": "Review the new authentication feature",
    "priority": "high",
    "tags": ["code-review", "authentication"],
    "list_id": "list_456"
}

response = requests.post(
    "https://api.example.com/api/v1/todos/",
    json=todo_data,
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

todo = response.json()
print(f"Created todo: {todo['title']}")

# Update todo status
update_data = {"status": "completed"}
response = requests.put(
    f"https://api.example.com/api/v1/todos/{todo['id']}",
    json=update_data,
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
```

### List Management

```python
# Create a project list
list_data = {
    "name": "Sprint 15 Todos",
    "description": "Todos for the current sprint",
    "list_type": "project",
    "color": "#4CAF50",
    "ordering_strategy": "priority"
}

response = requests.post(
    "https://api.example.com/api/v1/todos/lists",
    json=list_data,
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

project_list = response.json()

# Add team members
members = ["user_123", "user_456", "user_789"]
for user_id in members:
    membership_data = {"user_id": user_id, "role": "member"}
    requests.post(
        f"https://api.example.com/api/v1/todos/lists/{project_list['id']}/members",
        json=membership_data,
        headers={"Authorization": "Bearer YOUR_API_KEY"}
    )
```

### Natural Language Search

```python
# Search for urgent todos
search_query = "Show me all urgent todos that are blocking other work"
response = requests.post(
    "https://api.example.com/api/v1/todos/search",
    params={"query": search_query},
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

results = response.json()
for todo in results["todos"]:
    print(f"Found todo: {todo['title']} (relevance: {todo['relevance_score']})")
```

### Knowledge Graph Integration

```python
# Find related todos
response = requests.get(
    "https://api.example.com/api/v1/todos/todo_abc123/related",
    params={"relationship_type": "depends_on", "depth": 2},
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

related = response.json()
for todo in related["related_todos"]:
    print(f"Related: {todo['title']} ({todo['relationship']})")
```

### Advanced Filtering

```python
# Get high priority todos due this week
params = {
    "priority_filter": "high",
    "status_filter": "pending",
    "ordering": "due_date",
    "order_direction": "asc",
    "page": 1,
    "page_size": 50
}

response = requests.get(
    "https://api.example.com/api/v1/todos/",
    params=params,
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

todos = response.json()
print(f"Found {todos['total_count']} high priority pending todos")
```

## Error Codes

| Code                | Description                    |
| ------------------- | ------------------------------ |
| `VALIDATION_ERROR`  | Request data validation failed |
| `NOT_FOUND`         | Resource not found             |
| `PERMISSION_DENIED` | Insufficient permissions       |
| `RATE_LIMITED`      | Too many requests              |
| `INTERNAL_ERROR`    | Server error                   |

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

- Todos and Lists are automatically added to the knowledge graph
- Relationships between todos are discovered and stored
- Related todos can be found using graph traversal algorithms
- Metadata is preserved for enhanced search capabilities

### PM-034 Intent Classification Integration

- Natural language queries are classified using LLM intent classification
- Search results are enhanced with semantic understanding
- Query context is preserved for improved relevance
- A/B testing is used for continuous improvement

### Clean Separation from Existing Systems

- **Zero Impact**: Existing workflow Task system remains unchanged
- **Semantic Clarity**: Todo semantics are distinct from workflow tasks
- **Independent Evolution**: Todo system can evolve without affecting workflows
- **Integration Bridges**: Can reference existing WorkItems when needed

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
