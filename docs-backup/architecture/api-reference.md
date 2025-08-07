# Piper Morgan 1.0 - API Quick Reference

> **Complete Documentation:** See [api-design-spec.md](./api-design-spec.md) for comprehensive API contracts, error handling, and authentication details.

## Base URL

```
http://localhost:8001
```

## Core Endpoints

### Intent Processing

Process natural language requests and execute actions.

> **Note:** For workflows that require repository context (e.g., GitHub issue creation), the system automatically enriches the context with the repository if available from the project configuration. Users do not need to specify the repository explicitly.

```http
POST /api/v1/intent
Content-Type: application/json

{
    "message": "Create a bug ticket for the mobile login crash",
    "session_id": "optional-session-uuid",
    "context": {
        "project_id": "optional-explicit-project-id"
    }
}
```

**Response Types:**

- **Command** (creates workflow): Returns `workflow_id` for tracking
- **Query** (immediate data): Returns `data` object directly
- **Clarification** (ambiguous): Returns `clarification` with options

### Workflow Management

Track long-running operations like GitHub issue creation.

> **Note:** Workflow context will include the repository field if available, enabling downstream handlers to create issues in the correct repository automatically.

```http
# Get workflow status
GET /api/v1/workflows/{workflow_id}

# List recent workflows
GET /api/v1/workflows?limit=20&status=completed
```

### Execute Workflow

**Response Structure**:

```python
# Actual response (dict, not object)
response = await engine.execute_workflow(workflow_id)

# Check success:
if response["status"] == "completed":
    # Get task results:
    for task in response["tasks"]:
        if task["status"] == "completed":
            output = task["result"]["output_data"]
```

Note: Returns dict, not WorkflowResult object as might be expected.

### Project Management

Manage multi-project contexts.

```http
# List all projects
GET /api/v1/projects

# Get specific project
GET /api/v1/projects/{project_id}
```

### Knowledge Base

Upload and search organizational documents.

```http
# Upload document
POST /api/v1/knowledge/upload
Content-Type: multipart/form-data

# Search knowledge
POST /api/v1/knowledge/search
{
    "query": "mobile app performance metrics",
    "limit": 5
}
```

### System Health

Check service status.

```http
GET /api/v1/health
```

## Common Usage Patterns

### 1. Create GitHub Issue

```python
import requests

# Send natural language request
response = requests.post("http://localhost:8001/api/v1/intent", json={
    "message": "Create a bug ticket for login failing on iOS"
})

# For commands, get workflow ID and track progress
if response.json().get("workflow"):
    workflow_id = response.json()["workflow"]["id"]

    # Poll for completion
    status = requests.get(f"http://localhost:8001/api/v1/workflows/{workflow_id}")
    # The workflow context will include the repository if available
    print(status.json()["result"])
```

### 2. Query Projects

```python
# Direct query - immediate response
response = requests.post("http://localhost:8001/api/v1/intent", json={
    "message": "What projects are available?"
})

projects = response.json()["data"]["projects"]
```

### 3. Get Project Details

```python
# Get detailed project information including integrations
response = requests.post("http://localhost:8001/api/v1/intent", json={
    "message": "Get project details",
    "context": {"project_id": "proj-123"}
})

project_details = response.json()["data"]
print("Project:", project_details["name"])
print("Integrations:", project_details["integrations"])
print("Active integrations:", project_details["active_integrations"])
```

### 4. Handle Clarification

```python
response = requests.post("http://localhost:8001/api/v1/intent", json={
    "message": "Create a ticket for the mobile issue"
})

if response.json()["status"] == "clarification_needed":
    options = response.json()["clarification"]["options"]
    # Present options to user, then retry with explicit project_id
```

## Response Status Codes

| Code  | Meaning          | Usage                                       |
| ----- | ---------------- | ------------------------------------------- |
| `200` | Success          | Request processed successfully              |
| `422` | Validation Error | Missing required context (e.g., project_id) |
| `404` | Not Found        | Resource doesn't exist                      |
| `500` | Server Error     | Internal system error                       |

## Development Tools

### Interactive Documentation

- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

### Command Line Testing

```bash
# Quick health check
curl http://localhost:8001/api/v1/health

# Process intent
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "List all projects"}'

# Check workflow status
curl http://localhost:8001/api/v1/workflows/{workflow_id}
```

### Web Interface

Access the chat interface at: http://localhost:3000

## Intent Categories Reference

| Category    | Purpose                | Example Actions                          |
| ----------- | ---------------------- | ---------------------------------------- |
| `execution` | Create, update, modify | create_github_issue, update_project      |
| `query`     | Read, list, search     | list_projects, get_project, get_project_details, find_project, get_default_project, count_projects |
| `analysis`  | Analyze, assess        | analyze_metrics, review_performance      |
| `synthesis` | Generate, summarize    | create_report, summarize_meeting         |
| `strategy`  | Plan, prioritize       | plan_roadmap, prioritize_features        |

## GitHub-Specific Examples

### Example: Create GitHub Issue with Automatic Repository Context

```python
import requests

response = requests.post("http://localhost:8001/api/v1/intent", json={
    "message": "Create a bug ticket for the mobile login crash"
})

workflow_id = response.json()["workflow"]["id"]
status = requests.get(f"http://localhost:8001/api/v1/workflows/{workflow_id}")
workflow_context = status.json()["workflow"]["context"]

print("Repository used:", workflow_context.get("repository"))
print("Issue title:", workflow_context.get("title"))
```

### Example: Workflow Context for GitHub Issue

```json
{
  "project_id": "proj-123",
  "project_name": "Mobile App",
  "repository": "acme/mobile-app",
  "title": "Login fails on iOS",
  "body": "Steps to reproduce...",
  "labels": ["bug", "ios"]
}
```

## Error Handling

All errors return structured JSON responses. For detailed error codes and handling patterns, see the [complete API specification](./api-design-spec.md#error-handling).

**Common Error Example:**

```json
{
  "status": "error",
  "error": {
    "code": "PROJECT_NOT_FOUND",
    "message": "The specified project does not exist",
    "user_message": "I couldn't find that project. Try 'list projects' to see available options."
  }
}
```

## Integration Examples

### JavaScript/Frontend

```javascript
// Send request
const response = await fetch("/api/v1/intent", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: "Create a bug ticket" }),
});

const result = await response.json();

// Handle workflow tracking
if (result.workflow) {
  // Poll for completion
  const checkStatus = async () => {
    const status = await fetch(`/api/v1/workflows/${result.workflow.id}`);
    return status.json();
  };
}
```

### Python SDK Pattern

```python
class PiperMorganClient:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url

    def send_message(self, message, session_id=None):
        response = requests.post(f"{self.base_url}/api/v1/intent", json={
            "message": message,
            "session_id": session_id
        })
        return response.json()

    def get_workflow_status(self, workflow_id):
        response = requests.get(f"{self.base_url}/api/v1/workflows/{workflow_id}")
        return response.json()

# Usage
client = PiperMorganClient()
result = client.send_message("Create a ticket for the login bug")
```

---

**Next Steps:**

- See [api-design-spec.md](./api-design-spec.md) for complete API documentation
- Check [dev-guide.md](../development/dev-guide.md) for setup instructions
- Review [architecture.md](./architecture.md) for system design details

---

_Last Updated: June 28, 2025_

## Revision Log

- **June 28, 2025**: Added notes and examples for automatic repository context enrichment and GitHub integration patterns
