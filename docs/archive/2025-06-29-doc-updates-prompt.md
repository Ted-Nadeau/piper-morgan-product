# PM-011 Documentation Updates Prompt for CA

## Objective
Update architectural documentation to capture important patterns and decisions discovered during PM-011 GitHub integration implementation.

## Instructions
Work through each documentation file below, making the specified updates. Show me the changes with clear before/after context so I can review before you save.

### 1. Update `docs/architecture/pattern-catalog.md`

**Add Pattern #13: Repository Domain Model Conversion**
```markdown
## Pattern #13: Repository Domain Model Conversion

**Context**: Repositories interface between database models and business logic.

**Pattern**: All repository methods MUST return domain models, never database models.

**Implementation**:
```python
# Correct - Repository returns domain model
async def get_by_id(self, project_id: str) -> Optional[Project]:  # Domain type
    db_project = await self.session.get(ProjectDB, project_id)
    if db_project:
        return db_project.to_domain()  # Convert to domain
    return None

# Wrong - Leaks database model
async def get_by_id(self, project_id: str) -> Optional[ProjectDB]:  # DB type
    return await self.session.get(ProjectDB, project_id)  # No conversion
```

**Benefits**:
- Clean architectural boundaries
- Business logic doesn't depend on ORM
- Easier testing with domain models

**Discovered**: PM-011 - Repository returning ProjectDB caused AttributeError
```

**Add Pattern #14: Async Relationship Eager Loading**
```markdown
## Pattern #14: Async Relationship Eager Loading

**Context**: Async SQLAlchemy cannot lazy-load relationships outside session context.

**Pattern**: Always eager load relationships that will be accessed after query.

**Implementation**:
```python
from sqlalchemy.orm import selectinload

# Eager load integrations with project
result = await self.session.execute(
    select(ProjectDB)
    .options(selectinload(ProjectDB.integrations))
    .where(ProjectDB.id == project_id)
)
```

**Benefits**:
- Prevents "greenlet_spawn has not been called" errors
- All data available for domain conversion
- Better performance (single query)

**Discovered**: PM-011 - Lazy loading caused async context errors
```

### 2. Update `docs/architecture/architecture.md`

**In Docker Services section, add:**
```markdown
### Docker Best Practices

**Named Volumes (Recommended)**:
```yaml
volumes:
  piper_postgres_data:
    name: piper_postgres_data_v1  # Explicit versioned name
```

**Benefits**:
- Survives directory renames
- Managed by Docker
- Explicit versioning
- No path dependencies

**Avoid Bind Mounts for Databases**:
- Fragile with directory changes
- Path-dependent
- Can be lost during refactoring

**Lesson Learned**: PM-011 - Directory rename caused data loss with bind mounts
```

### 3. Update `docs/architecture/technical-spec.md`

**In Workflow Execution section, add:**
```markdown
### Workflow Execution Return Structure

The `execute_workflow` method returns a dictionary (not WorkflowResult object):

```python
{
    "id": "workflow-uuid",
    "type": "CREATE_TICKET",
    "status": "completed",  # or "failed", "pending"
    "tasks": [
        {
            "id": "task-uuid",
            "type": "GITHUB_CREATE_ISSUE",
            "status": "completed",
            "result": {
                "output_data": {
                    "issue_number": 7,
                    "issue_url": "https://github.com/owner/repo/issues/7",
                    "issue_data": {...}
                }
            }
        }
    ],
    "context": {},
    "error": null,
    "created_at": "2025-06-29T...",
    "updated_at": "2025-06-29T..."
}
```

**Success Check**: Use `result["status"] == "completed"` (no `success` field)
```

### 4. Update `docs/architecture/data-model.md`

**Add clarification section:**
```markdown
## Model Distinctions

### Product vs Project
- **Product**: What you're building/managing (domain concept)
- **Project**: PM workspace with tool integrations (configuration)

### Database vs Domain Models
- **ProjectDB**: SQLAlchemy ORM model for persistence
- **Project**: Domain model for business logic
- Always convert via `.to_domain()` at repository boundary

### Relationship Loading
- Async SQLAlchemy requires eager loading
- Use `selectinload()` for one-to-many relationships
- Load all needed relationships in repository methods
```

### 5. Update `docs/architecture/api-reference.md`

**Add to Orchestration section:**
```markdown
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

**Note**: Returns dict, not WorkflowResult object as might be expected.
```

## Verification Steps

After each update:
1. Show me the diff/changes
2. Confirm the update captures the lesson correctly
3. Check for consistency with existing documentation
4. Save only after my approval

## Remember
- These patterns were discovered through TDD during PM-011
- Each represents a real issue we encountered and solved
- Documentation helps future developers avoid these pitfalls
