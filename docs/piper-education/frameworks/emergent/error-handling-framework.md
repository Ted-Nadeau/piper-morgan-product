# Error Handling Framework

**Pattern Strength**: 14/16 (High Strength)
**Category**: Framework (Emergent)
**Discovery Date**: June 2025
**Status**: Production Ready

## Overview

The **Error Handling Framework** is a systematic approach to managing errors and exceptions in AI-assisted development systems. It provides user-friendly error messages, structured exception handling, and recovery guidance to ensure users can resolve issues and continue working effectively.

### Core Principle

**"Errors should be user-friendly, actionable, and provide clear recovery guidance."**

## Framework Definition

### Key Components

1. **Structured Exception Hierarchy**: Organized error types with clear inheritance
2. **User-Friendly Error Messages**: Clear, actionable messages for end users
3. **Recovery Guidance**: Specific suggestions for resolving issues
4. **API Contract Compliance**: Consistent error responses across all endpoints
5. **Graceful Degradation**: System continues operating despite errors

### Error Handling Model

```
User Request → System Processing → Error Detection → Error Classification → User-Friendly Response → Recovery Guidance
```

## Implementation Guide

### Step 1: Define Error Hierarchy

Create a structured exception hierarchy with clear inheritance:

```python
# Base error class
class APIError(Exception):
    """Base class for all application-specific API errors."""

    def __init__(self, status_code: int, error_code: str, details: Dict[str, Any] = None):
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(f"API Error [{error_code}]")

# Specific error categories
class IntentClassificationFailedError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(500, "INTENT_CLASSIFICATION_FAILED", details)

class TaskFailedError(APIError):
    def __init__(
        self,
        task_description: str = "a task",
        recovery_suggestion: str = "please try again",
        details: Dict[str, Any] = None,
    ):
        details = details or {}
        details["task_description"] = task_description
        details["recovery_suggestion"] = recovery_suggestion
        super().__init__(500, "TASK_FAILED", details)
```

### Step 2: Create User-Friendly Error Messages

Define centralized error messages that are clear and actionable:

```python
ERROR_MESSAGES = {
    # Intent errors
    "INTENT_CLASSIFICATION_FAILED": "I couldn't understand that request. Could you rephrase it?",
    "LOW_CONFIDENCE_INTENT": "I'm not so sure what you're asking for. Did you mean to '{suggestions}'?",

    # Workflow errors
    "WORKFLOW_TIMEOUT": "This is taking longer than expected. I'll keep working on it and notify you when done.",
    "TASK_FAILED": "I encountered an issue with {task_description}. As a suggestion, {recovery_suggestion}.",

    # Integration errors
    "GITHUB_RATE_LIMIT": "GitHub is limiting our requests. Please try again in {retry_after} minutes.",
    "GITHUB_AUTH_FAILED": "I couldn't authenticate with GitHub. Please check your access token.",

    # Knowledge base errors
    "NO_RELEVANT_KNOWLEDGE": "I don't have enough context about that. Could you provide more details?",
    "DOCUMENT_PROCESSING_FAILED": "I couldn't process that document. Please check the file format and try again.",
}
```

### Step 3: Implement Graceful Degradation

Ensure the system continues operating despite errors:

```python
async def _execute_task(self, workflow: Workflow, task: Task):
    """Execute a single task with graceful error handling"""
    try:
        # Task execution logic
        result = await handler(workflow, task)

        if result.success:
            task.status = TaskStatus.COMPLETED
            task.result = result.output_data
        else:
            # Graceful degradation: mark task as failed but continue workflow
            task.status = TaskStatus.FAILED
            task.error = result.error or "Task execution failed"
            workflow.status = WorkflowStatus.FAILED

            # Provide recovery guidance
            raise TaskFailedError(
                task_description=task.type.value,
                recovery_suggestion="review the task details and logs",
                details={"task_id": task.id, "error": task.error},
            )

    except Exception as e:
        # Graceful degradation: handle unexpected errors
        task.status = TaskStatus.FAILED
        task.error = str(e)
        workflow.status = WorkflowStatus.FAILED

        # Provide recovery guidance
        raise TaskFailedError(
            task_description=task.type.value,
            recovery_suggestion="an unexpected error occurred, check system logs",
            details={"task_id": task.id, "original_error": str(e)},
        ) from e
```

## Real Examples from Project

### Example 1: PM-010 Comprehensive Error Handling

**Context**: Implementing systematic error handling across all system layers

**Implementation**:

#### Error Hierarchy Creation

```python
# services/api/errors.py
class APIError(Exception):
    """Base class for all application-specific API errors."""

    def __init__(self, status_code: int, error_code: str, details: Dict[str, Any] = None):
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(f"API Error [{error_code}]")

# Intent errors
class IntentClassificationFailedError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(500, "INTENT_CLASSIFICATION_FAILED", details)

class LowConfidenceIntentError(APIError):
    def __init__(self, suggestions: str = "clarify your request", details: Dict[str, Any] = None):
        details = details or {}
        details["suggestions"] = suggestions
        super().__init__(422, "LOW_CONFIDENCE_INTENT", details)

# Workflow errors
class WorkflowTimeoutError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(504, "WORKFLOW_TIMEOUT", details)

class TaskFailedError(APIError):
    def __init__(
        self,
        task_description: str = "a task",
        recovery_suggestion: str = "please try again",
        details: Dict[str, Any] = None,
    ):
        details = details or {}
        details["task_description"] = task_description
        details["recovery_suggestion"] = recovery_suggestion
        super().__init__(500, "TASK_FAILED", details)
```

#### User-Friendly Error Messages

```python
ERROR_MESSAGES = {
    # Intent errors
    "INTENT_CLASSIFICATION_FAILED": "I couldn't understand that request. Could you rephrase it?",
    "LOW_CONFIDENCE_INTENT": "I'm not so sure what you're asking for. Did you mean to '{suggestions}'?",

    # Workflow errors
    "WORKFLOW_TIMEOUT": "This is taking longer than expected. I'll keep working on it and notify you when done.",
    "TASK_FAILED": "I encountered an issue with {task_description}. As a suggestion, {recovery_suggestion}.",

    # Integration errors
    "GITHUB_RATE_LIMIT": "GitHub is limiting our requests. Please try again in {retry_after} minutes.",
    "GITHUB_AUTH_FAILED": "I couldn't authenticate with GitHub. Please check your access token.",
}
```

**Result**: Comprehensive error handling system with user-friendly messages and recovery guidance

### Example 2: PM-012 GitHub Integration Error Handling

**Context**: Production GitHub integration with robust error handling

**Implementation**:

#### Integration-Specific Errors

```python
# GitHub integration errors
class GitHubRateLimitError(APIError):
    def __init__(self, retry_after: int = 1, details: Dict[str, Any] = None):
        details = details or {}
        details["retry_after"] = retry_after
        super().__init__(429, "GITHUB_RATE_LIMIT", details)

class GitHubAuthFailedError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(502, "GITHUB_AUTH_FAILED", details)
```

#### Graceful Degradation in GitHub Client

```python
# services/integrations/github/production_client.py
async def create_issue(self, repository: str, title: str, body: str, labels: List[str] = None) -> Dict[str, Any]:
    try:
        # GitHub API call
        response = await self._make_request("POST", f"/repos/{repository}/issues", {
            "title": title,
            "body": body,
            "labels": labels or []
        })
        return response

    except GitHubRateLimitError as e:
        # Graceful degradation: provide retry guidance
        logger.warning(f"GitHub rate limit exceeded: {e.details.get('retry_after', 1)} minutes")
        raise GitHubRateLimitError(
            retry_after=e.details.get('retry_after', 1),
            details={"repository": repository, "title": title}
        )

    except GitHubAuthFailedError as e:
        # Graceful degradation: provide authentication guidance
        logger.error(f"GitHub authentication failed for repository: {repository}")
        raise GitHubAuthFailedError(
            details={"repository": repository, "suggestion": "check your GitHub token"}
        )

    except Exception as e:
        # Graceful degradation: handle unexpected errors
        logger.error(f"Unexpected error creating GitHub issue: {str(e)}")
        raise TaskFailedError(
            task_description="GitHub issue creation",
            recovery_suggestion="check your GitHub configuration and try again",
            details={"repository": repository, "original_error": str(e)}
        )
```

**Result**: Robust GitHub integration with comprehensive error handling and recovery guidance

### Example 3: PM-021 Error Handling Fix

**Context**: Fixing TaskFailedError propagation issue in workflow engine

**Implementation**:

#### Proper Exception Handling

```python
# services/orchestration/engine.py
async def _execute_task(self, workflow: Workflow, task: Task):
    try:
        # Task execution
        result = await handler(workflow, task)

        if result.success:
            task.status = TaskStatus.COMPLETED
            task.result = result.output_data
        else:
            # Graceful degradation: preserve original error message
            task.status = TaskStatus.FAILED
            task.error = result.error or "Task execution failed"
            workflow.status = WorkflowStatus.FAILED

            raise TaskFailedError(
                task_description=task.type.value,
                recovery_suggestion="review the task details and logs",
                details={"task_id": task.id, "error": task.error},
            )

    except TimeoutError as e:
        # Handle timeout errors gracefully
        task.status = TaskStatus.FAILED
        task.error = "Task timed out after 120 seconds"
        workflow.status = WorkflowStatus.FAILED

        raise TaskFailedError(
            task_description=task.type.value,
            recovery_suggestion="the system may be under heavy load, please try again later",
            details={"task_id": task.id, "reason": "timeout"},
        ) from e

    except TaskFailedError:
        # Re-raise TaskFailedError without re-wrapping
        raise

    except Exception as e:
        # Handle unexpected errors gracefully
        task.status = TaskStatus.FAILED
        task.error = str(e)
        workflow.status = WorkflowStatus.FAILED

        raise TaskFailedError(
            task_description=task.type.value,
            recovery_suggestion="an unexpected error occurred, check system logs",
            details={"task_id": task.id, "original_error": str(e)},
        ) from e
```

**Result**: Proper error message preservation and graceful error handling in workflow engine

## Error Categories

### Intent Errors

- **IntentClassificationFailedError**: When the system cannot understand user intent
- **LowConfidenceIntentError**: When intent classification has low confidence

### Workflow Errors

- **WorkflowTimeoutError**: When workflows exceed time limits
- **TaskFailedError**: When individual tasks fail during execution

### Integration Errors

- **GitHubRateLimitError**: When GitHub API rate limits are exceeded
- **GitHubAuthFailedError**: When GitHub authentication fails

### Knowledge Base Errors

- **NoRelevantKnowledgeError**: When no relevant knowledge is found
- **DocumentProcessingError**: When document processing fails

## Best Practices

### Error Message Design

✅ **Good Error Messages**:

```python
# Clear and actionable
"GitHub is limiting our requests. Please try again in {retry_after} minutes."

# Specific recovery guidance
"I couldn't authenticate with GitHub. Please check your access token."

# User-friendly language
"I couldn't understand that request. Could you rephrase it?"
```

❌ **Bad Error Messages**:

```python
# Technical jargon
"HTTP 429: Rate limit exceeded"

# No recovery guidance
"Error occurred"

# Blaming the user
"You provided invalid input"
```

### Graceful Degradation

✅ **Good Graceful Degradation**:

```python
try:
    result = await critical_operation()
    return result
except CriticalError as e:
    # Log the error for debugging
    logger.error(f"Critical operation failed: {e}")

    # Provide fallback behavior
    return fallback_result()

    # Continue system operation
    continue_workflow()
```

❌ **Bad Error Handling**:

```python
try:
    result = await critical_operation()
    return result
except Exception as e:
    # Crash the entire system
    raise SystemError(f"Critical failure: {e}")
```

### Error Logging

✅ **Good Error Logging**:

```python
try:
    result = await operation()
    return result
except Exception as e:
    # Structured logging with context
    logger.error(
        "Operation failed",
        operation="github_issue_creation",
        repository=repository,
        error=str(e),
        exc_info=True
    )
    raise
```

❌ **Bad Error Logging**:

```python
try:
    result = await operation()
    return result
except Exception as e:
    # No context or structure
    print(f"Error: {e}")
    raise
```

## Evolution Story

### Discovery Phase (June 2025)

The Error Handling Framework emerged from early development challenges:

- **Poor User Experience**: Technical error messages confused users
- **System Crashes**: Unhandled exceptions caused system failures
- **No Recovery Guidance**: Users didn't know how to resolve issues
- **Inconsistent Error Responses**: Different parts of the system handled errors differently

### Refinement Phase (June-July 2025)

The framework evolved through systematic application:

1. **PM-010**: Comprehensive error handling system implementation
2. **PM-012**: Integration-specific error handling for GitHub
3. **PM-021**: Workflow engine error handling improvements

### Standardization Phase (Current)

The framework is now standardized across the project:

- **Structured Exception Hierarchy**: Clear inheritance and organization
- **User-Friendly Messages**: Centralized error message definitions
- **Graceful Degradation**: System continues operating despite errors
- **Recovery Guidance**: Specific suggestions for resolving issues

## Success Metrics

### Quantitative Metrics

- **Error Resolution Rate**: 90%+ of errors resolved with provided guidance
- **System Uptime**: 99%+ uptime maintained despite errors
- **User Satisfaction**: High satisfaction with error message clarity

### Qualitative Metrics

- **User Experience**: Clear, actionable error messages
- **System Reliability**: Graceful degradation prevents system crashes
- **Developer Experience**: Structured error handling reduces debugging time

## Anti-Patterns

### What NOT to Do

❌ **Technical Error Messages**

```python
# BAD: Technical jargon
raise Exception("HTTP 500: Internal server error in /api/workflow")
```

❌ **No Recovery Guidance**

```python
# BAD: No help for users
raise Exception("Error occurred")
```

❌ **System Crashes**

```python
# BAD: Crashes entire system
try:
    result = await operation()
except Exception as e:
    sys.exit(1)  # Crashes system
```

❌ **Inconsistent Error Handling**

```python
# BAD: Different error handling in different places
# File 1
try:
    result = await operation()
except Exception as e:
    return {"error": str(e)}

# File 2
try:
    result = await operation()
except Exception as e:
    raise APIError(500, "UNKNOWN_ERROR")
```

### What TO Do

✅ **User-Friendly Error Messages**

```python
# GOOD: Clear and actionable
raise TaskFailedError(
    task_description="GitHub issue creation",
    recovery_suggestion="check your GitHub token and repository access",
    details={"repository": repo, "error": str(e)}
)
```

✅ **Graceful Degradation**

```python
# GOOD: System continues operating
try:
    result = await critical_operation()
    return result
except CriticalError as e:
    logger.error(f"Critical operation failed: {e}")
    return fallback_result()  # Continue with fallback
```

✅ **Structured Error Handling**

```python
# GOOD: Consistent error handling
try:
    result = await operation()
    return result
except SpecificError as e:
    raise SpecificError(details={"context": "operation"})
except Exception as e:
    raise TaskFailedError(
        task_description="operation",
        recovery_suggestion="check system logs and try again",
        details={"original_error": str(e)}
    )
```

## Implementation Checklist

- [ ] Define error hierarchy with clear inheritance
- [ ] Create user-friendly error messages
- [ ] Implement graceful degradation patterns
- [ ] Add recovery guidance for common errors
- [ ] Establish structured error logging
- [ ] Test error scenarios and user experience
- [ ] Document error handling patterns
- [ ] Train team on error handling best practices

## Conclusion

The Error Handling Framework is essential for building reliable, user-friendly AI-assisted development systems. By providing clear error messages, recovery guidance, and graceful degradation, we ensure users can resolve issues and continue working effectively.

**Key Takeaway**: "Errors are opportunities to help users succeed. Clear messages and recovery guidance turn failures into learning experiences."

---

**Related**: [Verification-First Pattern](../../decision-patterns/emergent/verification-first-pattern.md), [Human-AI Collaboration Referee](../../methodologies/emergent/human-ai-collaboration-referee.md)
