# Handler Implementation Pattern

**Based on**: `_handle_create_issue` (working implementation in services/intent/intent_service.py:423-493)
**Date**: October 11, 2025
**Purpose**: Establish repeatable pattern for all 8 remaining placeholder handlers

---

## Pattern Structure

### 1. Method Signature

```python
async def _handle_X(
    self, intent: Intent, workflow_id: str, session_id: str = None
) -> IntentProcessingResult:
    """
    Handle [action_name] action.

    [Brief description of what this handler does]

    GREAT-4D Phase X: [Status - FULLY IMPLEMENTED]
    """
```

**Key Points**:
- Always `async def` (all handlers are async)
- Takes `intent: Intent` parameter (contains all request data)
- Takes `workflow_id: str` (for tracking)
- Optional `session_id: str` (for user context)
- Returns `IntentProcessingResult` (standardized response)
- Docstring includes implementation status

---

### 2. Overall Structure (Try/Except Wrapper)

```python
async def _handle_X(self, intent: Intent, workflow_id: str) -> IntentProcessingResult:
    """Handler for X"""
    try:
        # 1. Import service locally
        # 2. Create service instance
        # 3. Extract parameters
        # 4. Validate required parameters
        # 5. Call service method
        # 6. Return success result
    except Exception as e:
        # 7. Log error
        # 8. Return error result
```

**Pattern**: Everything inside try/except, even imports

---

### 3. Service Import and Instantiation

```python
try:
    from services.domain.github_domain_service import GitHubDomainService

    github_service = GitHubDomainService()
```

**Key Points**:
- Import service inside try block (not at module level)
- Create new service instance each call (stateless)
- Service handles its own initialization and configuration

**For other services**:
- `GitHubDomainService()` - for GitHub operations
- `SlackDomainService()` - for Slack operations (if needed)
- `NotionDomainService()` - for Notion operations (if needed)

---

### 4. Parameter Extraction

```python
# Extract issue details from intent
title = intent.context.get("title") or f"Issue: {intent.original_message[:50]}"
description = intent.context.get("description") or intent.original_message
repository = intent.context.get("repository") or intent.context.get("repo")
```

**Pattern**:
- Use `intent.context.get(key)` for optional parameters
- Use `intent.context.get(key) or default` for parameters with fallbacks
- Use `intent.original_message` as fallback for content (title, body, etc.)
- Support multiple parameter names (e.g., "repository" or "repo")

**Common parameters**:
- `intent.context.get("title")` - Issue/task title
- `intent.context.get("body")` or `intent.context.get("description")` - Content
- `intent.context.get("repository")` or `intent.context.get("repo")` - GitHub repo
- `intent.context.get("labels", [])` - Labels (default to empty list)
- `intent.context.get("assignees", [])` - Assignees (default to empty list)
- `intent.original_message` - The raw user message

---

### 5. Validation Pattern

```python
# Require repository
if not repository:
    return IntentProcessingResult(
        success=False,
        message="Cannot create issue: repository not specified. Please specify which repository.",
        intent_data={
            "category": intent.category.value,
            "action": intent.action,
        },
        workflow_id=workflow_id,
        requires_clarification=True,  # ← User needs to provide more info
        clarification_type="repository_required",
    )
```

**Validation Response Pattern**:
- `success=False` - Validation failed
- `message` - **User-friendly** explanation of what's missing
- `intent_data` - Always include category and action
- `requires_clarification=True` - **Only for validation errors** (legit use case!)
- `clarification_type` - Specific identifier for UI/client

**CRITICAL**: `requires_clarification=True` is **only** for genuine validation errors where user must provide more data. Never use it as a placeholder!

---

### 6. Service Method Call

```python
# Create issue
issue = await github_service.create_issue(
    repo_name=repository,
    title=title,
    body=description,
    labels=intent.context.get("labels", []),
    assignees=intent.context.get("assignees", []),
)
```

**Pattern**:
- `await` the service call (all service methods are async)
- Pass extracted parameters as named arguments
- Service returns domain object or dictionary

---

### 7. Success Response

```python
return IntentProcessingResult(
    success=True,
    message=f"Created issue #{issue.get('number')}: {issue.get('title')}",
    intent_data={
        "category": intent.category.value,
        "action": intent.action,
        "confidence": intent.confidence,
        "issue_number": issue.get("number"),
        "issue_url": issue.get("html_url"),
        "repository": repository,
    },
    workflow_id=workflow_id,
    requires_clarification=False,  # ← Success = no clarification needed
)
```

**Success Response Pattern**:
- `success=True`
- `message` - **User-friendly** success message with key details
- `intent_data` - **Always** include:
  - `category`: intent.category.value
  - `action`: intent.action
  - `confidence`: intent.confidence
  - **Plus** specific data from the operation (issue_number, url, etc.)
- `workflow_id` - Always pass through
- `requires_clarification=False` - **Explicitly False** for successes

---

### 8. Error Handling

```python
except Exception as e:
    self.logger.error(f"Failed to create issue: {e}")
    return IntentProcessingResult(
        success=False,
        message=f"Failed to create issue: {str(e)}",
        intent_data={
            "category": intent.category.value,
            "action": intent.action,
        },
        workflow_id=workflow_id,
        error=str(e),
        error_type="GitHubError",
    )
```

**Error Response Pattern**:
- `self.logger.error()` - **Always** log before returning
- `success=False`
- `message` - User-friendly error message
- `intent_data` - Minimal (category, action)
- `error` - Technical error message (`str(e)`)
- `error_type` - Categorized error type:
  - `"GitHubError"` - GitHub API errors
  - `"NotImplementedError"` - Handler not implemented
  - `"ValidationError"` - Parameter validation errors
  - `"TimeoutError"` - Operation timeout
  - `"ServiceUnavailable"` - Service not configured

---

## Complete Pattern Template

```python
async def _handle_X(
    self, intent: Intent, workflow_id: str, session_id: str = None
) -> IntentProcessingResult:
    """
    Handle [action_name] action.

    [Description of functionality]

    GREAT-4D Phase X: FULLY IMPLEMENTED
    """
    try:
        # 1. Import and instantiate service
        from services.domain.[service]_domain_service import [Service]DomainService

        service = [Service]DomainService()

        # 2. Extract parameters from intent
        param1 = intent.context.get("param1") or default_value
        param2 = intent.context.get("param2")
        required_param = intent.context.get("required_param")

        # 3. Validate required parameters
        if not required_param:
            return IntentProcessingResult(
                success=False,
                message="Cannot perform action: required parameter not specified.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="param_required",
            )

        # 4. Call service method
        result = await service.method_name(
            param1=param1,
            param2=param2,
            required_param=required_param,
        )

        # 5. Return success response
        return IntentProcessingResult(
            success=True,
            message=f"Successfully completed action: {result.key_field}",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": intent.confidence,
                "result_field1": result.get("field1"),
                "result_field2": result.get("field2"),
            },
            workflow_id=workflow_id,
            requires_clarification=False,
        )

    except Exception as e:
        # 6. Log and return error
        self.logger.error(f"Failed to perform action: {e}")
        return IntentProcessingResult(
            success=False,
            message=f"Failed to perform action: {str(e)}",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
            },
            workflow_id=workflow_id,
            error=str(e),
            error_type="ServiceError",
        )
```

---

## Key Principles

### ✅ Always Do
1. **Wrap everything in try/except** - No exceptions should escape
2. **Log all errors** - Use `self.logger.error()` before returning error
3. **Return IntentProcessingResult** - Always use the standard response structure
4. **Include workflow_id** - Required for tracking
5. **Include intent metadata** - Always include category, action, confidence
6. **Validate required parameters** - Check before calling service
7. **Use user-friendly messages** - Messages go directly to user
8. **Import services locally** - Inside try block, not module level
9. **Set requires_clarification=False on success** - Explicitly False for completions
10. **Use await for service calls** - All service methods are async

### ❌ Never Do
1. **Never return success=True without doing work** - Must call real service
2. **Never return requires_clarification=True as placeholder** - Only for validation
3. **Never skip error logging** - Always log before returning error
4. **Never let exceptions escape** - Catch all, log all, return error response
5. **Never hardcode success messages** - Include actual result data
6. **Never skip parameter extraction** - Even if using defaults
7. **Never assume services are configured** - They auto-configure
8. **Never use synchronous service calls** - All are async, use await

---

## Anti-Patterns to Avoid

### ❌ Sophisticated Placeholder Pattern (OLD - Don't copy!)
```python
# BAD - This is what we're replacing!
async def _handle_X(self, intent: Intent, workflow_id: str) -> IntentProcessingResult:
    return IntentProcessingResult(
        success=True,  # ← Lying about success
        message="Handler is ready. Implementation in progress.",  # ← Placeholder message
        intent_data={"category": intent.category.value, "action": intent.action},
        workflow_id=workflow_id,
        requires_clarification=True,  # ← Placeholder marker
        clarification_type="parameters",  # ← Generic placeholder
    )
```

**Why this is bad**:
- Returns `success=True` but does nothing
- Message admits it's not implemented
- Uses `requires_clarification` as placeholder
- No actual work performed
- No service called

### ✅ Real Implementation Pattern (NEW - Copy this!)
```python
# GOOD - This is what we want!
async def _handle_X(self, intent: Intent, workflow_id: str) -> IntentProcessingResult:
    try:
        from services.domain.service import Service
        service = Service()

        # Extract, validate, call, return
        param = intent.context.get("param")
        if not param:
            return IntentProcessingResult(
                success=False,  # ← Honest about validation failure
                message="Parameter required",
                intent_data={...},
                workflow_id=workflow_id,
                requires_clarification=True,  # ← Legitimate use
                clarification_type="param_required",
            )

        result = await service.do_work(param)  # ← Actually does work!

        return IntentProcessingResult(
            success=True,  # ← Honest about success
            message=f"Completed: {result.key}",  # ← Real result
            intent_data={...with result data...},
            workflow_id=workflow_id,
            requires_clarification=False,  # ← No clarification needed
        )
    except Exception as e:
        self.logger.error(f"Error: {e}")
        return IntentProcessingResult(success=False, ...)
```

---

## Comparison: Create vs Update Issue

### Similarities (Pattern Consistency)
- Same try/except structure
- Same service instantiation approach
- Same parameter extraction pattern
- Same validation pattern
- Same success response structure
- Same error handling approach

### Differences (Expected for Different Operations)

| Aspect | _handle_create_issue | _handle_update_issue |
|--------|---------------------|---------------------|
| **Required params** | repository, title/message | repository, issue_number |
| **Optional params** | labels, assignees | title, body, state, labels |
| **Service method** | `create_issue()` | `update_issue()` |
| **GitHub API** | POST /repos/{owner}/{repo}/issues | PATCH /repos/{owner}/{repo}/issues/{number} |
| **Success message** | "Created issue #123: Title" | "Updated issue #123" |
| **Result data** | issue_number, issue_url, repository | issue_number, title, state, updated_at |

---

## Usage Example: Implementing _handle_update_issue

Following this pattern, `_handle_update_issue` should look like this:

```python
async def _handle_update_issue(
    self, intent: Intent, workflow_id: str
) -> IntentProcessingResult:
    """
    Handle update_issue/update_ticket action.

    Updates existing GitHub issue using domain service.

    GREAT-4D Phase 1: FULLY IMPLEMENTED
    """
    try:
        from services.domain.github_domain_service import GitHubDomainService

        github_service = GitHubDomainService()

        # Extract parameters
        issue_number = intent.context.get("issue_number")
        repository = intent.context.get("repository") or intent.context.get("repo")
        title = intent.context.get("title")
        body = intent.context.get("body") or intent.context.get("description")
        state = intent.context.get("state")
        labels = intent.context.get("labels")

        # Validate required parameters
        if not issue_number:
            return IntentProcessingResult(
                success=False,
                message="Cannot update issue: issue number not specified.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="issue_number_required",
            )

        if not repository:
            return IntentProcessingResult(
                success=False,
                message="Cannot update issue: repository not specified.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="repository_required",
            )

        # Call service
        updated_issue = await github_service.update_issue(
            repo_name=repository,
            issue_number=issue_number,
            title=title,
            body=body,
            state=state,
            labels=labels,
        )

        # Return success
        return IntentProcessingResult(
            success=True,
            message=f"Updated issue #{updated_issue.get('number')}: {updated_issue.get('title')}",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": intent.confidence,
                "issue_number": updated_issue.get("number"),
                "title": updated_issue.get("title"),
                "state": updated_issue.get("state"),
                "issue_url": updated_issue.get("html_url"),
            },
            workflow_id=workflow_id,
            requires_clarification=False,
        )

    except Exception as e:
        self.logger.error(f"Failed to update issue: {e}")
        return IntentProcessingResult(
            success=False,
            message=f"Failed to update issue: {str(e)}",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
            },
            workflow_id=workflow_id,
            error=str(e),
            error_type="GitHubError",
        )
```

---

## Pattern Validation Checklist

Before considering a handler "complete", verify:

- [ ] Wrapped in try/except
- [ ] Service imported locally
- [ ] Service instantiated inside try
- [ ] Parameters extracted from intent.context
- [ ] Required parameters validated
- [ ] Validation errors return requires_clarification=True
- [ ] Service method called with await
- [ ] Success returns requires_clarification=False
- [ ] Success includes real result data
- [ ] Errors logged with self.logger.error()
- [ ] Error response includes error and error_type
- [ ] Returns IntentProcessingResult in all cases
- [ ] Includes workflow_id in all returns
- [ ] Message is user-friendly
- [ ] Docstring updated to "FULLY IMPLEMENTED"
- [ ] No placeholder text in messages
- [ ] No placeholder markers anywhere

---

**Pattern established**: October 11, 2025
**Source handler**: `_handle_create_issue` (services/intent/intent_service.py:423-493)
**For use in**: All 8 remaining GREAT-4D placeholder handlers
