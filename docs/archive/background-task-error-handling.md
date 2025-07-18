# Background Task Error Handling

## Overview
Background tasks in FastAPI run after the response is sent, making them invisible to standard middleware error handling. This document describes our pattern for safe background task execution.

## Problem Statement

### The Challenge
- **Background tasks execute post-response**: FastAPI background tasks run after the HTTP response is sent
- **Middleware can't catch errors**: ErrorHandlingMiddleware only catches exceptions during request processing
- **Uncaught exceptions can crash**: Background task failures can cause uncaught exceptions that terminate the application

### Before Implementation
```python
# PROBLEMATIC: Uncaught exceptions in background tasks
background_tasks.add_task(engine.execute_workflow, workflow_id)
```

When `engine.execute_workflow` raised a `TaskFailedError`, it would propagate uncaught, potentially crashing the application.

## Solution: Safe Wrapper Pattern

### Implementation
**Location**: `main.py` lines 93-102

```python
async def safe_execute_workflow(engine, workflow_id: str) -> None:
    """Safely execute workflow in background, catching and logging errors."""
    try:
        await engine.execute_workflow(workflow_id)
    except TaskFailedError as e:
        logger.error(f"Background workflow {workflow_id} failed with TaskFailedError: {e}")
        # Error is logged but not propagated - prevents uncaught exception
    except Exception as e:
        logger.error(f"Background workflow {workflow_id} failed unexpectedly: {e}")
        # Catch-all for any other errors
```

### Usage Pattern
```python
# Instead of: background_tasks.add_task(risky_operation, args)
# Use: background_tasks.add_task(safe_wrapper, risky_operation, args)

# Example:
background_tasks.add_task(safe_execute_workflow, engine, workflow_id)
```

## Current Coverage

### Implemented Locations
- **Intent processing workflows** (`main.py` line ~355)
- **File disambiguation workflows** (`main.py` line ~442)

### Background Task Inventory
- ✅ **Line 355**: Main intent processing workflow execution - **FIXED**
- ✅ **Line 442**: File disambiguation workflow execution - **FIXED**
- ✅ **Line 679**: Clarification handler (unused BackgroundTasks parameter - no action needed)

## Error Handling Strategy

### Principle: Log but Don't Propagate
1. **Catch specific errors**: Handle known error types (TaskFailedError) explicitly
2. **Log comprehensively**: Ensure all errors are logged with context
3. **Prevent propagation**: Don't re-raise exceptions that would crash the application
4. **Maintain visibility**: Error logging preserves debugging information

### Error Types Handled
- **TaskFailedError**: Controlled workflow failures with structured error information
- **Exception**: Catch-all for unexpected errors

## Testing

### Test Coverage
- **Test file**: `tests/test_error_handling_integration.py`
- **Test method**: `test_workflow_task_failed_error`
- **Status**: ✅ **PASSING** - Validates proper background task error handling

### Test Validates
1. API returns 200 initially (workflow started successfully)
2. Background task failures are handled gracefully
3. Error logging occurs but doesn't crash the application

## Architecture Benefits

### Before Implementation
- Background task failures could crash the application
- Errors were invisible to standard error handling
- No consistent pattern for background task safety

### After Implementation
- ✅ **Application stability**: Background task failures don't crash the app
- ✅ **Error visibility**: Comprehensive logging of all background task failures
- ✅ **Consistent pattern**: Standardized approach for all background tasks
- ✅ **Maintainability**: Clear pattern for future background task implementations

## Future Work

### For New Background Tasks
Any new background tasks should follow this established pattern:

1. **Create a safe wrapper function** for the risky operation
2. **Handle specific error types** that the operation might raise
3. **Log errors comprehensively** with context
4. **Use the wrapper in background_tasks.add_task()**

### Extension Pattern
```python
async def safe_execute_other_operation(operation, *args, **kwargs) -> None:
    """Safely execute other operations in background, catching and logging errors."""
    try:
        await operation(*args, **kwargs)
    except SpecificError as e:
        logger.error(f"Background operation failed with SpecificError: {e}")
    except Exception as e:
        logger.error(f"Background operation failed unexpectedly: {e}")
```

## Related Documentation

- **ADR-006**: AsyncSession Management (infrastructure error handling)
- **Pattern Catalog**: Repository Pattern #1 (error handling in data layer)
- **Test Strategy**: Integration test patterns for error handling

## Monitoring and Alerting

### Error Monitoring
- All background task failures are logged with ERROR level
- Monitoring systems should alert on repeated TaskFailedError occurrences
- Unexpected exceptions should trigger immediate investigation

### Log Format
```
ERROR: Background workflow {workflow_id} failed with TaskFailedError: {error_details}
ERROR: Background workflow {workflow_id} failed unexpectedly: {error_details}
```

## Conclusion

The safe wrapper pattern provides a simple, elegant solution to background task error handling in FastAPI applications. By catching and logging errors without propagation, we maintain application stability while preserving error visibility for debugging and monitoring.

This pattern should be considered the standard approach for all background task implementations in the Piper Morgan system.
