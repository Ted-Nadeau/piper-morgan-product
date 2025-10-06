# Prompt for Both Agents: GREAT-4C Phase 0 - Remove Hardcoded User Context

## Context

5 canonical handlers exist with hardcoded single-user assumptions. Discovery found:
- Hardcoded "VA/Kind Systems" string matching in handlers
- Single-user hacks that will break with multiple users
- **This is blocking for multi-user/alpha release**

## Mission

Remove all hardcoded user context and implement proper multi-user capable context service.

## Session Logs

- Code: Continue `dev/2025/10/05/2025-10-05-2020-prog-code-log.md`
- Cursor: Continue `dev/2025/10/05/2025-10-05-1540-prog-cursor-log.md`

---

## Code Agent Tasks

### Task 1: Audit Hardcoded References

Create audit script: `scripts/audit_hardcoded_context.py`

```python
"""Find all hardcoded user context in handlers."""
import re
from pathlib import Path

def audit_hardcoded_context():
    """Find hardcoded user references."""

    patterns = [
        r'"VA"',
        r"'VA'",
        r'"Kind Systems"',
        r"'Kind Systems'",
        r'if.*"VA".*in',
        r'config.*"VA"',
    ]

    handlers_file = Path("services/intent_service/canonical_handlers.py")
    content = handlers_file.read_text()

    findings = []
    for i, line in enumerate(content.split('\n'), 1):
        for pattern in patterns:
            if re.search(pattern, line):
                findings.append({
                    'line': i,
                    'content': line.strip(),
                    'pattern': pattern
                })

    return findings

if __name__ == "__main__":
    findings = audit_hardcoded_context()
    print(f"Found {len(findings)} hardcoded references:")
    for f in findings:
        print(f"  Line {f['line']}: {f['content']}")
```

Run it:
```bash
python3 scripts/audit_hardcoded_context.py
```

### Task 2: Create User Context Service

Create: `services/user_context_service.py`

```python
"""User context service for multi-user support."""
from typing import Dict, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

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

class UserContextService:
    """Manages user-specific context without hardcoding."""

    def __init__(self):
        self.cache = {}
        logger.info("UserContextService initialized")

    async def get_user_context(self, session_id: str) -> UserContext:
        """
        Get user context from session.

        Args:
            session_id: Session identifier

        Returns:
            UserContext with user-specific data
        """
        # Check cache first
        if session_id in self.cache:
            return self.cache[session_id]

        # Load from session/database
        # For now, load from PIPER.md based on session
        context = await self._load_context_from_config(session_id)

        # Cache it
        self.cache[session_id] = context
        return context

    async def _load_context_from_config(self, session_id: str) -> UserContext:
        """Load user context from PIPER.md configuration."""
        from services.configuration.piper_config_loader import piper_config_loader

        try:
            config = piper_config_loader.load_config()

            # Extract user context from config
            # (This is session-specific PIPER.md, not hardcoded)
            context = UserContext(
                user_id=session_id,  # TODO: Get actual user_id from session
                organization=self._extract_organization(config),
                projects=self._extract_projects(config),
                priorities=self._extract_priorities(config)
            )

            return context

        except Exception as e:
            logger.warning(f"Could not load user context: {e}")
            # Return empty context
            return UserContext(user_id=session_id)

    def _extract_organization(self, config: Dict) -> Optional[str]:
        """Extract organization from config."""
        # Look for organization mentions in config
        for key, value in config.items():
            if "organization" in key.lower():
                return str(value)
        return None

    def _extract_projects(self, config: Dict) -> list:
        """Extract projects from config."""
        projects = []
        for key, value in config.items():
            if "project" in key.lower():
                # Parse project list from config
                if isinstance(value, list):
                    projects.extend(value)
                elif isinstance(value, str):
                    # Parse from text
                    lines = value.split('\n')
                    projects.extend([l.strip() for l in lines if l.strip()])
        return projects

    def _extract_priorities(self, config: Dict) -> list:
        """Extract priorities from config."""
        priorities = []
        for key, value in config.items():
            if "priorit" in key.lower():
                if isinstance(value, list):
                    priorities.extend(value)
                elif isinstance(value, str):
                    lines = value.split('\n')
                    priorities.extend([l.strip() for l in lines if l.strip()])
        return priorities

# Singleton instance
user_context_service = UserContextService()
```

### Task 3: Update Handlers to Use Context Service

Edit: `services/intent_service/canonical_handlers.py`

Find hardcoded sections like:
```python
# BEFORE - Hardcoded:
if config and "VA" in str(config.values()):
    focus = "Morning development work - perfect time for deep focus on VA Q4 onramp"
```

Replace with:
```python
# AFTER - Dynamic:
from services.user_context_service import user_context_service

async def _handle_guidance_query(self, intent, session_id):
    # Get user-specific context
    user_context = await user_context_service.get_user_context(session_id)

    current_time = datetime.now()
    current_hour = current_time.hour

    # Use user's actual organization/projects
    if 6 <= current_hour < 9:
        if user_context.organization:
            focus = f"Morning development work - perfect time for deep focus on {user_context.organization} priorities."
        else:
            focus = "Morning development work - perfect time for deep focus."
    # ... continue pattern
```

Apply this pattern to ALL handlers that reference:
- "VA"
- "Kind Systems"
- Any hardcoded user-specific data

### Task 4: Test Multi-User Support

Create: `dev/2025/10/05/test_multi_user_context.py`

```python
"""Test that different users get different contexts."""
import asyncio
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.classifier import Intent

async def test_multi_user():
    """Verify no hardcoded user assumptions."""

    handlers = CanonicalHandlers()

    # Simulate User 1 query
    user1_intent = Intent(
        text="What should I focus on?",
        category="GUIDANCE"
    )
    user1_response = await handlers._handle_guidance_query(user1_intent, "user1_session")

    # Simulate User 2 query
    user2_intent = Intent(
        text="What should I focus on?",
        category="GUIDANCE"
    )
    user2_response = await handlers._handle_guidance_query(user2_intent, "user2_session")

    print("User 1 Response:")
    print(user1_response.get("message", ""))
    print("\nUser 2 Response:")
    print(user2_response.get("message", ""))

    # Verify no hardcoded "VA" or "Kind Systems" in responses
    # (unless that's actually in the user's PIPER.md)
    assert "VA Q4" not in user2_response.get("message", ""), \
        "User 2 should not see User 1's hardcoded context"

    print("\n✅ Multi-user test passed - no hardcoded context")

if __name__ == "__main__":
    asyncio.run(test_multi_user())
```

Run test:
```bash
python3 dev/2025/10/05/test_multi_user_context.py
```

---

## Cursor Agent Tasks

### Task 1: Document User Context Service

Create: `docs/guides/user-context-service.md`

```markdown
# User Context Service

## Purpose
Provides user-specific context without hardcoding assumptions.
Enables multi-user support in handlers.

## Usage

```python
from services.user_context_service import user_context_service

async def my_handler(intent, session_id):
    # Get user context
    context = await user_context_service.get_user_context(session_id)

    # Access user-specific data
    org = context.organization  # User's organization
    projects = context.projects  # User's active projects
    priorities = context.priorities  # User's priorities

    # Use in response
    return f"Your top priority: {priorities[0] if priorities else 'None set'}"
```

## UserContext Object

```python
@dataclass
class UserContext:
    user_id: str
    organization: Optional[str]
    projects: list
    priorities: list
    preferences: Dict[str, Any]
```

## Data Source

Context is loaded from session-specific PIPER.md configuration.
Each user has their own PIPER.md with their data.

## Caching

User context is cached per session to avoid repeated file reads.
Cache is invalidated when session ends.

## Migration from Hardcoded Context

**Before (WRONG)**:
```python
if "VA" in config:
    do_va_specific_thing()
```

**After (CORRECT)**:
```python
context = await user_context_service.get_user_context(session_id)
if "VA" in context.organization:
    do_org_specific_thing()
```
```

### Task 2: Create Validation Tests

Create: `tests/intent/test_no_hardcoded_context.py`

```python
"""Ensure no hardcoded user context in handlers."""
import pytest
from pathlib import Path
import re

def test_no_hardcoded_va_references():
    """Handlers should not contain hardcoded VA references."""
    handlers_file = Path("services/intent_service/canonical_handlers.py")
    content = handlers_file.read_text()

    # Check for hardcoded strings
    forbidden_patterns = [
        r'"VA Q4"',
        r"'VA Q4'",
        r'"Kind Systems"',
        r"'Kind Systems'",
        r'if.*"VA".*in.*str\(',  # Pattern: if "VA" in str(config)
    ]

    violations = []
    for pattern in forbidden_patterns:
        matches = re.findall(pattern, content)
        if matches:
            violations.extend(matches)

    assert len(violations) == 0, \
        f"Found {len(violations)} hardcoded references: {violations}"

def test_user_context_service_imported():
    """Handlers should import user context service."""
    handlers_file = Path("services/intent_service/canonical_handlers.py")
    content = handlers_file.read_text()

    assert "user_context_service" in content, \
        "Handlers must import user_context_service"
```

Run tests:
```bash
pytest tests/intent/test_no_hardcoded_context.py -v
```

---

## Success Criteria

- [ ] Audit script identifies all hardcoded references
- [ ] UserContextService created
- [ ] All handlers updated to use context service
- [ ] Multi-user test passes
- [ ] Validation tests pass (no hardcoded strings remain)
- [ ] Documentation complete
- [ ] Session logs updated

---

## Evidence Format

```bash
$ python3 scripts/audit_hardcoded_context.py
Found 8 hardcoded references:
  Line 145: if config and "VA" in str(config.values()):
  Line 172: focus = "VA Q4 onramp implementation"
  ...

$ python3 dev/2025/10/05/test_multi_user_context.py
User 1 Response:
Morning development work - focus on your organization priorities.

User 2 Response:
Morning development work - focus on your organization priorities.

✅ Multi-user test passed - no hardcoded context

$ pytest tests/intent/test_no_hardcoded_context.py -v
test_no_hardcoded_va_references PASSED
test_user_context_service_imported PASSED
```

---

**Effort**: Medium (critical architectural fix)
**Priority**: CRITICAL (blocks multi-user)
**Time**: ~1 hour
