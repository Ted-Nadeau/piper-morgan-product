# Fix: Project Create Contract Test Mock Configuration

**Issue**: `TestProjectCreateContract::test_create_project_accepts_json_body` was failing with `PydanticSerializationError: Unable to serialize unknown type: <class 'coroutine'>` (Bead: piper-morgan-ufj)

## Root Cause

The test mock was configured incorrectly:
- Mock setup: `mock_repo.create_project = AsyncMock(...)`
- Actual route call: `await project_repo.create(...)`

The mismatch meant the test was calling a non-existent method, leaving the actual `create()` method unmocked. This caused Pydantic to receive a coroutine object instead of a resolved value.

## Solution

Changed the mock method name from `create_project` to `create`:

```python
# Before (wrong)
mock_repo.create_project = AsyncMock(return_value=MagicMock(...))

# After (correct)
mock_repo.create = AsyncMock(return_value=MagicMock(...))
```

## Testing Pattern Applied

When mocking repository methods in tests:
1. **Match the actual method name** - Use `create()`, not `create_project()`, etc.
2. **Use AsyncMock for async methods** - Ensures the mock returns a coroutine
3. **Return actual domain objects** - Use `MagicMock` with required attributes
4. **Verify the signature** - Check the route/service code to see what method is called

## Files Changed

- `tests/unit/web/api/routes/test_create_endpoints_contract.py` - Fixed mock setup and added documentation

## Verification

All 4 tests in the contract test file pass:
- `TestListCreateContract::test_create_list_accepts_json_body` ✓
- `TestListCreateContract::test_create_list_name_only_json` ✓
- `TestTodoCreateContract::test_create_todo_accepts_json_body` ✓
- `TestProjectCreateContract::test_create_project_accepts_json_body` ✓
