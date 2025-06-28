# CQRS-lite Query Pattern - Developer Guide

## Quick Reference

### When to Use Queries vs Workflows

| Operation Type           | Use             | Example                                          |
| ------------------------ | --------------- | ------------------------------------------------ |
| **Data Retrieval**       | QueryRouter     | "List all projects", "Get project details"       |
| **Status Check**         | QueryRouter     | "What's the status of workflow X?"               |
| **Search**               | QueryRouter     | "Find projects with 'mobile' in name"            |
| **State Change**         | WorkflowFactory | "Create a ticket", "Update project settings"     |
| **Multi-step Process**   | WorkflowFactory | "Analyze metrics and generate report"            |
| **External Integration** | WorkflowFactory | "Create GitHub issue", "Send Slack notification" |

## Adding New Queries

### 1. Add Query Action to QueryRouter

```python
# In services/queries/query_router.py
async def route_query(self, intent: Intent) -> Any:
    if intent.action == "your_new_query":
        return await self.your_service.your_method()
    # ... existing actions
```

### 2. Add Method to Query Service

```python
# In services/queries/your_queries.py
class YourQueryService:
    async def your_method(self) -> List[YourDomainModel]:
        return await self.repo.your_repository_method()
```

### 3. Update Intent Classifier

Add query keywords to the fallback classifier:

```python
# In services/intent_service/classifier.py
elif any(word in message_lower for word in ["your", "query", "keywords"]):
    category = IntentCategory.QUERY
    action = "your_new_query"
```

### 4. Add Tests

```python
# In tests/test_your_queries.py
@pytest.mark.asyncio
async def test_your_new_query():
    # Test the query service method
    result = await query_service.your_method()
    assert len(result) > 0
```

## Common Patterns

### List Operations

```python
# Query Service
async def list_active_items(self) -> List[Item]:
    return await self.repo.list_active_items()

# Query Router
elif intent.action == "list_items":
    return await self.item_queries.list_active_items()
```

### Get by ID Operations

```python
# Query Service
async def get_item_by_id(self, item_id: str) -> Optional[Item]:
    return await self.repo.get_by_id(item_id)

# Query Router
elif intent.action == "get_item":
    item_id = intent.context.get("item_id")
    if not item_id:
        raise ValueError("get_item query requires item_id in context")
    return await self.item_queries.get_item_by_id(item_id)
```

### Search Operations

```python
# Query Service
async def find_items_by_name(self, name: str) -> List[Item]:
    return await self.repo.find_by_name(name)

# Query Router
elif intent.action == "find_items":
    name = intent.context.get("name")
    if not name:
        raise ValueError("find_items query requires name in context")
    return await self.item_queries.find_items_by_name(name)
```

## Error Handling

### Query Router Errors

```python
# Handle missing required context
if intent.action == "get_project":
    project_id = intent.context.get("project_id")
    if not project_id:
        raise ValueError("get_project query requires project_id in context")

# Handle unknown actions
else:
    raise ValueError(f"Unknown query action: {intent.action}")
```

### Query Service Errors

```python
# Let repository errors bubble up for proper handling
async def get_project_by_id(self, project_id: str) -> Optional[Project]:
    return await self.repo.get_by_id(project_id)  # May raise ProjectNotFoundError
```

## Testing

### Unit Tests

```python
@pytest.mark.asyncio
async def test_query_service_method():
    # Arrange
    mock_repo = Mock()
    mock_repo.list_active_projects.return_value = [project1, project2]
    query_service = ProjectQueryService(mock_repo)

    # Act
    result = await query_service.list_active_projects()

    # Assert
    assert len(result) == 2
    mock_repo.list_active_projects.assert_called_once()
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_query_router_integration():
    # Arrange
    intent = Intent(category=IntentCategory.QUERY, action="list_projects")
    query_router = QueryRouter(mock_query_service)

    # Act
    result = await query_router.route_query(intent)

    # Assert
    assert isinstance(result, list)
```

## Best Practices

1. **Keep Queries Simple**: Queries should be single-purpose and fast
2. **No Side Effects**: Query services should never modify data
3. **Use Domain Models**: Return domain objects, not raw database models
4. **Handle Errors Gracefully**: Provide meaningful error messages
5. **Test Thoroughly**: Both unit and integration tests for queries
6. **Document Actions**: Keep the supported query actions list updated

## Migration from Workflows

If you find a workflow that's actually a query:

1. **Create GitHub Issue**: Use the template for refactoring queries
2. **Add Query Service**: Implement the query logic in a service
3. **Update QueryRouter**: Add routing for the new query action
4. **Update Intent Classifier**: Add QUERY category recognition
5. **Remove from WorkflowFactory**: Remove the query from workflow registry
6. **Update Tests**: Move tests from workflow to query tests
7. **Update Documentation**: Update API docs and guides

## Troubleshooting

### Common Issues

**Query not being recognized as QUERY category:**

- Check intent classifier keywords
- Verify the LLM prompt includes QUERY category
- Test with fallback classifier

**QueryRouter not finding action:**

- Verify action is added to QueryRouter.route_query()
- Check action name matches intent.action exactly
- Add action to get_supported_queries() list

**Repository errors:**

- Ensure repository is properly injected
- Check database connection
- Verify repository method exists

### Debug Steps

1. Check intent classification: `print(intent.category, intent.action)`
2. Verify QueryRouter routing: Add logging to route_query method
3. Test query service directly: Call service method with test data
4. Check repository connection: Verify database is accessible

---
*Last Updated: June 27, 2025*

## Revision Log
- **June 27, 2025**: Added systematic documentation dating and revision tracking
