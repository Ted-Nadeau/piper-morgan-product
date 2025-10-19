# Code Agent Prompt: Phase 1.6 - Systematic ServiceRegistry Cleanup

**Date**: October 16, 2025, 11:25 AM
**Sprint**: A2 - Notion & Errors (Day 2)
**Issue**: Foundation cleanup (enables #215 completion)
**Phase**: 1.6 - Eliminate ServiceRegistry Anti-Pattern
**Duration**: 45-60 minutes
**Agent**: Claude Code (with Serena)

---

## Mission

Systematically find and eliminate ALL uses of the old `ServiceRegistry.get_*()` static pattern in favor of the new DDD ServiceContainer. This completes the Phase 1.5 architectural refactor.

**Context**: Phase 1.5 implemented proper DDD ServiceContainer. During validation, discovered IntentClassifier still uses old `ServiceRegistry.get_llm()` pattern. Need to find ALL instances and migrate them.

**Philosophy**: "Fix the anti-pattern everywhere, not just where we see it."

---

## What We Discovered in Phase 1.5

### Fixed
- ✅ OrchestrationEngine - Now gets LLM from container

### Found Needs Fixing
- ❌ IntentClassifier - Uses `ServiceRegistry.get_llm()`

### Unknown
- ❓ How many other places use this anti-pattern?

**This phase**: Find them all, fix them all!

---

## Step 1: Use Serena to Find ALL Instances (10 min)

### Search for ServiceRegistry usage

**Pattern to find**:
```python
ServiceRegistry.get_llm()
ServiceRegistry.get_orchestration()
ServiceRegistry.get_intent()
ServiceRegistry.get_*()
```

**Use Serena's symbolic indexing**:
```bash
# Serena should search for:
# 1. Import statements: "from services.service_registry import ServiceRegistry"
# 2. Static calls: "ServiceRegistry.get"
# 3. Any ServiceRegistry usage outside services/container/

# Document all findings in dev/active/serviceregistry-usage-audit.md
```

### Create audit report

**File**: `dev/active/serviceregistry-usage-audit.md`

```markdown
# ServiceRegistry Usage Audit - Phase 1.6

**Date**: October 16, 2025, 11:30 AM
**Purpose**: Find all ServiceRegistry anti-pattern usage
**Tool**: Serena symbolic indexing

---

## Summary

**Total Files Found**: [count]
**Total Usages Found**: [count]
**Categories**:
- Import statements: [count]
- Static get calls: [count]
- Other usage: [count]

---

## Detailed Findings

### File 1: [path/to/file.py]
**Line [X]**: Import statement
```python
from services.service_registry import ServiceRegistry
```

**Line [Y]**: Usage
```python
llm = ServiceRegistry.get_llm()
```

**Migration Strategy**: [How to fix this specific case]

---

### File 2: [path/to/file.py]
[Repeat for each file]

---

## Migration Priority

### High Priority (Blocking functionality)
1. IntentClassifier - Discovered in Phase 1.5 validation
2. [Other files that directly impact core features]

### Medium Priority (Used but not blocking)
[Files that use pattern but aren't critical path]

### Low Priority (Tests, examples, deprecated)
[Files that might not need immediate migration]

---

## Migration Patterns

### Pattern 1: Direct Service Usage
**Before**:
```python
from services.service_registry import ServiceRegistry

class MyClass:
    def __init__(self):
        self.llm = ServiceRegistry.get_llm()
```

**After**:
```python
from services.container import ServiceContainer

class MyClass:
    def __init__(self, llm_service=None):
        # Accept via dependency injection OR get from container
        if llm_service is None:
            container = ServiceContainer()
            llm_service = container.get_service('llm')
        self.llm = llm_service
```

### Pattern 2: Service Usage in Methods
**Before**:
```python
def process(self):
    llm = ServiceRegistry.get_llm()
    return llm.chat(...)
```

**After**:
```python
def process(self):
    container = ServiceContainer()
    llm = container.get_service('llm')
    return llm.chat(...)
```

---

## Expected File Count

Based on Phase 1.5 discovery: 2-10 files likely

---

**Audit Complete**: [time]
**Ready for Migration**: YES/NO
```

**Save audit to**: `dev/active/serviceregistry-usage-audit.md`

---

## Step 2: Fix IntentClassifier (Known Issue) (15 min)

### Locate IntentClassifier

**File likely**: `services/integrations/intent/intent_classifier.py`

### Current pattern

```python
from services.service_registry import ServiceRegistry

class IntentClassifier:
    def __init__(self):
        self._llm = ServiceRegistry.get_llm()
```

### Updated pattern (Dependency Injection)

```python
from services.container import ServiceContainer

class IntentClassifier:
    def __init__(self, llm_service=None):
        """
        Initialize IntentClassifier.

        Args:
            llm_service: LLM service instance (optional, will get from container if not provided)
        """
        if llm_service is None:
            container = ServiceContainer()
            llm_service = container.get_service('llm')

        self._llm = llm_service
```

### Update callers

**Find where IntentClassifier is instantiated**:
- Likely in IntentService
- Update to pass LLM service if available

**Example**:
```python
# In IntentService.__init__
container = ServiceContainer()
llm_service = container.get_service('llm')
self.classifier = IntentClassifier(llm_service=llm_service)
```

---

## Step 3: Fix All Other Instances (20 min)

### Systematic approach

For each file in the audit report:

1. **Understand context** - What is this class/function doing?
2. **Choose pattern** - Dependency injection or container access?
3. **Update code** - Apply the migration pattern
4. **Update callers** - If using DI, update instantiation sites
5. **Test** - Ensure functionality unchanged

### Migration decision tree

```
Is it a class that's instantiated elsewhere?
├─ YES: Use dependency injection (preferred)
│  └─ Add service parameter to __init__
│     └─ Default to container.get_service() if None
│
└─ NO: Use direct container access
   └─ Get service from container when needed
```

### Document each change

In `dev/active/phase-1.6-migration-log.md`:

```markdown
# Phase 1.6 Migration Log

## File: services/integrations/intent/intent_classifier.py
**Changed**: Line 15 - __init__ method
**Before**: `self._llm = ServiceRegistry.get_llm()`
**After**: Dependency injection with container fallback
**Reason**: Allows testing with mock LLM
**Tested**: ✅ IntentService still functional

---

## File: [next file]
[Repeat for each migration]
```

---

## Step 4: Remove Old ServiceRegistry (If Possible) (10 min)

### Check if old ServiceRegistry still needed

**File**: `services/service_registry.py` (the OLD one, not container/service_registry.py)

**Questions**:
1. Is it still imported anywhere?
2. Are there any static methods still in use?
3. Can it be deleted or deprecated?

### Options

**Option A: Delete completely**
```bash
# If no references remain
git rm services/service_registry.py

# Update any imports that fail
# All should use services.container.ServiceContainer now
```

**Option B: Deprecate with clear error**
```python
# services/service_registry.py

class ServiceRegistry:
    """
    DEPRECATED: Use ServiceContainer instead.

    This class is deprecated as of Phase 1.5/1.6.
    Use: from services.container import ServiceContainer
    """

    @staticmethod
    def get_llm():
        raise DeprecationWarning(
            "ServiceRegistry.get_llm() is deprecated. "
            "Use ServiceContainer().get_service('llm') instead."
        )
```

**Option C: Keep for backwards compatibility**
```python
# If external code depends on it
# Wrap the new container

class ServiceRegistry:
    """Legacy wrapper around ServiceContainer for backwards compatibility."""

    @staticmethod
    def get_llm():
        from services.container import ServiceContainer
        container = ServiceContainer()
        return container.get_service('llm')
```

**Recommended**: Option A (delete) if possible, Option B (deprecate) if unsure

---

## Step 5: Update Tests (10 min)

### Find tests using ServiceRegistry

```bash
# Use Serena to find test files
# Search for: ServiceRegistry in tests/
```

### Update test imports

**Before**:
```python
from services.service_registry import ServiceRegistry
```

**After**:
```python
from services.container import ServiceContainer
```

### Update test mocking

**Before**:
```python
def test_something(mocker):
    mocker.patch('services.service_registry.ServiceRegistry.get_llm')
```

**After**:
```python
def test_something(mocker):
    mock_container = mocker.Mock()
    mock_container.get_service.return_value = mock_llm
    mocker.patch('services.container.ServiceContainer', return_value=mock_container)
```

---

## Step 6: Validation (10 min)

### Run all tests

```bash
# Run full test suite
pytest tests/ -v

# Expected: All tests still passing
# If failures: Fix related to ServiceRegistry migration
```

### Manual validation

```bash
# Kill existing server
pkill -f "python main.py" 2>/dev/null || true

# Start server
python main.py &
sleep 5

# Test intent endpoint (should still work!)
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": "show me the standup"}' \
  -w "\nHTTP Status: %{http_code}\n"

# Expected: HTTP 200 (not 422!)
```

### Validation report

**File**: `dev/active/phase-1.6-validation.md`

```markdown
# Phase 1.6 Validation Results

**Date**: October 16, 2025
**Time**: [completion time]

---

## ServiceRegistry Cleanup

**Files Migrated**: [count]
**Old Pattern Removed**: ✅ YES / ❌ NO
**Deprecation Added**: ✅ YES / ❌ NO / N/A

---

## Test Results

```bash
$ pytest tests/ -v
```
[Paste results]

**Status**: [All passing / X failures]

---

## Manual Testing

**Intent Endpoint**:
```bash
$ curl POST /api/v1/intent '{"intent": "show me standup"}'
```
**Result**: HTTP [code]
**Status**: [✅ Working / ❌ Failed]

---

## Conclusion

**ServiceRegistry Anti-Pattern**: [✅ Eliminated / ⚠️ Partially / ❌ Issues]
**System Functional**: [✅ YES / ❌ NO]
**Ready for Phase 2**: [YES / NO]
```

---

## Step 7: Commit Changes (5 min)

### Use pre-commit script

```bash
./scripts/commit.sh "refactor(services): eliminate ServiceRegistry anti-pattern (Phase 1.6)

Systematic Cleanup:
- Audit: Found [X] files using old ServiceRegistry.get_*() pattern
- Migrated: All instances to ServiceContainer pattern
- Fixed: IntentClassifier to use dependency injection
- Updated: [other classes] to use container
- Tests: Updated mocking to use ServiceContainer

Old Pattern (deprecated):
  ServiceRegistry.get_llm()

New Pattern:
  container = ServiceContainer()
  llm = container.get_service('llm')

Benefits:
- Proper dependency injection
- Easier testing (mock container)
- Consistent service access
- No static methods

Changes:
- [list files changed]

Testing:
- All unit tests passing
- All integration tests passing
- Intent endpoint validated (200 for valid, 422 for invalid)

Part of: Phase 1.5/1.6 DDD refactor, enables #215
Duration: [actual time]"
```

---

## Deliverables Phase 1.6

When complete, you should have:

- [ ] ServiceRegistry usage audit completed (with Serena)
- [ ] IntentClassifier migrated to container pattern
- [ ] All other instances migrated
- [ ] Old ServiceRegistry removed/deprecated
- [ ] Tests updated
- [ ] All tests passing
- [ ] Intent endpoint validated (200 for valid)
- [ ] Changes committed
- [ ] Migration log documented

---

## Success Criteria

**Phase 1.6 is complete when**:

- ✅ Zero references to old ServiceRegistry.get_*() pattern
- ✅ All services accessed through ServiceContainer
- ✅ All tests passing
- ✅ Intent endpoint returns 200 for valid requests
- ✅ System fully functional
- ✅ Anti-pattern eliminated

---

## Time Budget

**Target**: 45-60 minutes

- Serena audit: 10 min
- IntentClassifier fix: 15 min
- Other instances: 20 min
- Old ServiceRegistry: 10 min
- Test updates: 10 min
- Validation: 10 min
- Commit: 5 min

**Total**: ~80 minutes (with buffer)

---

## What NOT to Do

- ❌ Don't assume you found everything (use Serena!)
- ❌ Don't skip tests (must validate)
- ❌ Don't leave partially migrated code
- ❌ Don't break working functionality

## What TO Do

- ✅ Use Serena to find ALL instances
- ✅ Systematic migration (one file at a time)
- ✅ Document each change
- ✅ Test thoroughly
- ✅ Validate intent endpoint works

---

## STOP Conditions

Stop and escalate if:

- Can't find all ServiceRegistry usage with Serena
- Migration breaks critical functionality
- Tests fail in unexpected ways
- Intent endpoint stops working

---

**Phase 1.6 Start**: 11:30 AM
**Expected Done**: ~12:30 PM (1 hour)
**Status**: Ready to eliminate anti-pattern systematically!

**LET'S USE SERENA TO FIND THEM ALL!** 🔍

---

*"Find the pattern everywhere, fix it everywhere."*
*- Systematic Refactoring Philosophy*
