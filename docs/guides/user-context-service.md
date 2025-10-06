# User Context Service

**Last Updated**: October 5, 2025  
**Epic**: GREAT-4C - Remove Hardcoded User Context  
**Status**: Multi-User Architecture Implementation

---

## Purpose

Provides user-specific context without hardcoding assumptions. Enables multi-user support in canonical handlers by loading context dynamically from session-specific configuration.

**Critical Fix**: Removes hardcoded "VA/Kind Systems" references that block multi-user deployment.

---

## Usage

### Basic Pattern

```python
from services.user_context_service import user_context_service

async def my_handler(intent, session_id):
    # Get user context dynamically
    context = await user_context_service.get_user_context(session_id)

    # Access user-specific data
    org = context.organization  # User's organization
    projects = context.projects  # User's active projects
    priorities = context.priorities  # User's priorities

    # Use in response
    if priorities:
        return f"Your top priority: {priorities[0]}"
    else:
        return "No priorities set in your configuration"
```

### Handler Integration

```python
async def _handle_guidance_query(self, intent, session_id):
    """Handle guidance queries with user-specific context."""
    # Get user-specific context (not hardcoded)
    user_context = await user_context_service.get_user_context(session_id)

    current_time = datetime.now()
    current_hour = current_time.hour

    # Use user's actual organization/projects
    if 6 <= current_hour < 9:
        if user_context.organization:
            focus = f"Morning development work - perfect time for deep focus on {user_context.organization} priorities."
        else:
            focus = "Morning development work - perfect time for deep focus."
    elif 9 <= current_hour < 12:
        if user_context.projects:
            focus = f"Mid-morning productivity - ideal for {', '.join(user_context.projects[:2])} work."
        else:
            focus = "Mid-morning productivity - ideal for project work."
    # ... continue pattern

    return {
        "message": focus,
        "context": {
            "user_organization": user_context.organization,
            "active_projects": user_context.projects
        }
    }
```

---

## UserContext Object

```python
@dataclass
class UserContext:
    """User-specific context data."""
    user_id: str
    organization: Optional[str] = None
    projects: list = None
    priorities: list = None
    preferences: Dict[str, Any] = None

    def __post_init__(self):
        if self.projects is None:
            self.projects = []
        if self.priorities is None:
            self.priorities = []
        if self.preferences is None:
            self.preferences = {}
```

### Properties

- **`user_id`**: Session identifier (will be actual user ID in future)
- **`organization`**: User's organization name (extracted from PIPER.md)
- **`projects`**: List of active projects from configuration
- **`priorities`**: List of current priorities from configuration
- **`preferences`**: Dictionary of user preferences and settings

---

## Data Source

### Configuration Loading

Context is loaded from **session-specific PIPER.md configuration**:

1. **Per-Session Loading**: Each session loads its own PIPER.md
2. **Dynamic Extraction**: Organization, projects, and priorities extracted from config
3. **No Hardcoding**: No assumptions about specific users or organizations

### Example PIPER.md Structure

```markdown
# User Configuration

## Organization

Kind Systems

## Current Projects

- Piper Morgan development
- Q4 onramp implementation
- Documentation updates

## Priorities

- Complete GREAT-4C multi-user support
- Finalize alpha release preparation
- Update architectural documentation
```

### Extraction Logic

```python
def _extract_organization(self, config: Dict) -> Optional[str]:
    """Extract organization from config."""
    for key, value in config.items():
        if "organization" in key.lower():
            return str(value)
    return None

def _extract_projects(self, config: Dict) -> list:
    """Extract projects from config."""
    projects = []
    for key, value in config.items():
        if "project" in key.lower():
            if isinstance(value, list):
                projects.extend(value)
            elif isinstance(value, str):
                lines = value.split('\n')
                projects.extend([l.strip() for l in lines if l.strip()])
    return projects
```

---

## Caching

### Performance Optimization

- **Per-Session Caching**: User context cached per session to avoid repeated file reads
- **Cache Invalidation**: Cache cleared when session ends
- **Memory Efficient**: Only active sessions cached

### Cache Implementation

```python
class UserContextService:
    def __init__(self):
        self.cache = {}  # session_id -> UserContext

    async def get_user_context(self, session_id: str) -> UserContext:
        # Check cache first
        if session_id in self.cache:
            return self.cache[session_id]

        # Load from configuration
        context = await self._load_context_from_config(session_id)

        # Cache it
        self.cache[session_id] = context
        return context
```

---

## Migration from Hardcoded Context

### The Problem

**Before (WRONG - Hardcoded)**:

```python
# This breaks multi-user support!
if config and "VA" in str(config.values()):
    focus = "Morning development work - perfect time for deep focus on VA Q4 onramp"
elif "Kind Systems" in str(config.values()):
    focus = "Morning development work - perfect time for deep focus on Kind Systems priorities"
```

**Issues with Hardcoded Approach**:

- ❌ Only works for specific hardcoded organizations
- ❌ Breaks when new users join
- ❌ Requires code changes for each new organization
- ❌ Not scalable for multi-user deployment

### The Solution

**After (CORRECT - Dynamic)**:

```python
# This works for any user!
context = await user_context_service.get_user_context(session_id)
if context.organization:
    focus = f"Morning development work - perfect time for deep focus on {context.organization} priorities"
else:
    focus = "Morning development work - perfect time for deep focus"
```

**Benefits of Dynamic Approach**:

- ✅ Works for any organization
- ✅ Scales to unlimited users
- ✅ No code changes needed for new users
- ✅ Configuration-driven, not code-driven

---

## Multi-User Support

### Session Isolation

Each session gets its own context:

```python
# User 1 session
user1_context = await user_context_service.get_user_context("session_123")
# Returns: UserContext(organization="Kind Systems", projects=["Piper Morgan"])

# User 2 session
user2_context = await user_context_service.get_user_context("session_456")
# Returns: UserContext(organization="Acme Corp", projects=["Product Launch"])
```

### No Cross-Contamination

- **Isolated Contexts**: Each user sees only their own data
- **Session-Specific**: Context loaded from user's own PIPER.md
- **No Hardcoded Assumptions**: System works for any organization/user

---

## Testing Multi-User Behavior

### Validation Test

```python
async def test_multi_user_isolation():
    """Verify different users get different contexts."""
    handlers = CanonicalHandlers()

    # User 1 query
    user1_response = await handlers._handle_guidance_query(
        intent, "user1_session"
    )

    # User 2 query
    user2_response = await handlers._handle_guidance_query(
        intent, "user2_session"
    )

    # Verify no hardcoded context leakage
    assert "VA Q4" not in user2_response.get("message", "")
    assert user1_response != user2_response  # Different contexts
```

### Regression Prevention

```python
def test_no_hardcoded_references():
    """Ensure no hardcoded user context remains."""
    handlers_file = Path("services/intent_service/canonical_handlers.py")
    content = handlers_file.read_text()

    forbidden_patterns = [
        r'"VA Q4"',
        r'"Kind Systems"',
        r'if.*"VA".*in.*str\(',
    ]

    for pattern in forbidden_patterns:
        assert not re.search(pattern, content), \
            f"Found hardcoded reference: {pattern}"
```

---

## Implementation Checklist

### Code Changes Required

- [ ] **Remove hardcoded strings**: "VA", "Kind Systems", "Q4 onramp"
- [ ] **Import UserContextService**: Add to canonical_handlers.py
- [ ] **Update all handlers**: Use `await user_context_service.get_user_context(session_id)`
- [ ] **Dynamic responses**: Use `context.organization`, `context.projects`, etc.
- [ ] **Fallback handling**: Graceful behavior when context is empty

### Testing Required

- [ ] **Multi-user test**: Different sessions get different contexts
- [ ] **Hardcoded detection**: No forbidden strings remain
- [ ] **Regression tests**: Existing functionality still works
- [ ] **Edge cases**: Empty config, missing sections, malformed data

---

## Troubleshooting

### Common Issues

**Context Not Loading**:

- Check PIPER.md file exists and is readable
- Verify configuration format matches expected structure
- Check logs for loading errors

**Hardcoded References Remain**:

- Run audit script: `python3 scripts/audit_hardcoded_context.py`
- Check all handler methods for string literals
- Verify imports are updated

**Multi-User Test Failing**:

- Ensure different sessions use different PIPER.md files
- Check cache isolation between sessions
- Verify no global state contamination

---

## Related Documentation

- **GREAT-4C Epic**: Multi-user context architecture
- **Canonical Handlers**: `services/intent_service/canonical_handlers.py`
- **Configuration Loading**: `services/configuration/piper_config_loader.py`
- **Testing Strategy**: `tests/intent/test_no_hardcoded_context.py`

---

**Status**: ✅ Architecture defined - Implementation in progress

**Critical for**: Multi-user deployment, alpha release readiness

**Last Updated**: October 5, 2025 (GREAT-4C Phase 0)
