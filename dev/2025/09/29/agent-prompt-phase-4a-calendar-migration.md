# Claude Code Prompt: Phase 4A - Calendar Service Migration

## Mission: Migrate Calendar Services to Router Pattern

**Context**: All three integration routers are complete and verified. Phase 4 migrates services from direct adapter imports to router imports. Starting with Calendar services following inchworm methodology - one service at a time with verification.

**Objective**: Replace direct GoogleCalendarMCPAdapter imports with CalendarIntegrationRouter in 2 Calendar services, verify functionality preserved.

## Services to Migrate

### Service 1: canonical_handlers.py
**Location**: `services/intent_service/canonical_handlers.py`
**Expected Import**: `from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter`
**Replace With**: `from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter`

### Service 2: morning_standup.py
**Location**: `services/features/morning_standup.py`
**Expected Import**: `from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter`
**Replace With**: `from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter`

## Implementation Tasks

### Task 1: Verify Current State

Before making changes, document current imports:

```bash
# Check current imports in both services
echo "=== canonical_handlers.py Calendar imports ==="
grep -n "GoogleCalendarMCPAdapter\|google_calendar" services/intent_service/canonical_handlers.py || echo "No matches found"

echo "=== morning_standup.py Calendar imports ==="
grep -n "GoogleCalendarMCPAdapter\|google_calendar" services/features/morning_standup.py || echo "No matches found"

# Check how these services instantiate the adapter
echo "=== Calendar adapter usage patterns ==="
grep -A 3 -B 3 "GoogleCalendarMCPAdapter()" services/intent_service/canonical_handlers.py services/features/morning_standup.py || echo "No direct instantiation found"
```

**Document**: What imports exist, how adapter is instantiated, any usage patterns

### Task 2: Check Existing Tests

```bash
# Look for tests related to these services
echo "=== Testing Calendar services ==="
find . -name "*test*" -type f | xargs grep -l "canonical_handlers\|morning_standup" 2>/dev/null | head -10

# Check if there are pytest files
find . -name "*test*.py" -exec grep -l "calendar" {} \; 2>/dev/null | head -10
```

**Document**: What tests exist for these services

### Task 3: Service 1 Migration - canonical_handlers.py

```python
# Before making changes, create backup
cp services/intent_service/canonical_handlers.py services/intent_service/canonical_handlers.py.backup

# Make the migration:
# 1. Replace import statement
# 2. Replace any instantiation calls
# 3. Ensure method calls remain the same (router delegates transparently)
```

**Migration Pattern**:
```python
# OLD:
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter
calendar_adapter = GoogleCalendarMCPAdapter()

# NEW:
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
calendar_adapter = CalendarIntegrationRouter()
```

**Verify Change**:
```bash
# Show the diff
git diff services/intent_service/canonical_handlers.py

# Verify new import works
python -c "
from services.intent_service.canonical_handlers import *
print('✅ canonical_handlers imports successfully')
"
```

### Task 4: Test Service 1

```python
# Test that service still works
python -c "
import asyncio
from services.intent_service.canonical_handlers import *

# Try to instantiate classes/functions from this service
async def test_service():
    # Basic import and instantiation test
    print('✅ Service imports and instantiates correctly')

    # If there's a main class, try to instantiate it
    # (Adapt based on actual service structure)

asyncio.run(test_service())
"
```

If tests exist, run them:
```bash
# Run any tests related to canonical_handlers
pytest -xvs -k "canonical_handlers" || echo "No specific tests found"
pytest -xvs services/intent_service/ || echo "No service tests found"
```

**Commit Service 1**:
```bash
git add services/intent_service/canonical_handlers.py
git commit -m "Phase 4A: Migrate canonical_handlers.py to CalendarIntegrationRouter

- Replace GoogleCalendarMCPAdapter import with CalendarIntegrationRouter
- Preserve all method calls (router provides transparent delegation)
- Verified service imports and initializes correctly"

git log --oneline -1
```

### Task 5: Service 2 Migration - morning_standup.py

Repeat same pattern for morning_standup.py:

```python
# Backup
cp services/features/morning_standup.py services/features/morning_standup.py.backup

# Migrate import and instantiation
# Verify changes with git diff
# Test service functionality
```

**Test Service 2**:
```python
python -c "
import asyncio
from services.features.morning_standup import *

async def test_standup():
    print('✅ morning_standup imports and instantiates correctly')

asyncio.run(test_standup())
"
```

**Commit Service 2**:
```bash
git add services/features/morning_standup.py
git commit -m "Phase 4A: Migrate morning_standup.py to CalendarIntegrationRouter

- Replace GoogleCalendarMCPAdapter import with CalendarIntegrationRouter
- Preserve all method calls (router provides transparent delegation)
- Verified service imports and initializes correctly"

git log --oneline -1
```

### Task 6: Verification Tests

```bash
# Verify both services still import the router correctly
python -c "
import sys
import importlib

services = [
    'services.intent_service.canonical_handlers',
    'services.features.morning_standup'
]

for service in services:
    try:
        mod = importlib.import_module(service)
        print(f'✅ {service} imports successfully')
    except Exception as e:
        print(f'❌ {service} failed: {e}')
"

# Check that no direct GoogleCalendarMCPAdapter imports remain in these services
echo "=== Checking for remaining direct imports ==="
grep -r "from.*google_calendar_adapter import\|from.*GoogleCalendarMCPAdapter" services/intent_service/canonical_handlers.py services/features/morning_standup.py || echo "✅ No direct imports found"
```

## Evidence Requirements

Document completion with:

```markdown
# Phase 4A: Calendar Service Migration Report

## Services Migrated: 2/2

### canonical_handlers.py
- **Location**: services/intent_service/canonical_handlers.py
- **Import Changed**: ✅ GoogleCalendarMCPAdapter → CalendarIntegrationRouter
- **Git Diff**: [show diff output]
- **Testing**: [show test results or functional verification]
- **Commit**: [show commit hash and message]

### morning_standup.py
- **Location**: services/features/morning_standup.py
- **Import Changed**: ✅ GoogleCalendarMCPAdapter → CalendarIntegrationRouter
- **Git Diff**: [show diff output]
- **Testing**: [show test results or functional verification]
- **Commit**: [show commit hash and message]

## Verification Results
- **Both services import successfully**: ✅
- **No direct adapter imports remain**: ✅
- **Router delegation working**: ✅

## Ready for Phase 4B (Notion Migration): YES/NO
```

## Update Requirements

After completing both Calendar service migrations:

1. **Update Session Log**: Add Phase 4A completion with evidence
2. **Update GitHub Issue #199**: Add comment with Calendar migration completion evidence
3. **Tag Lead Developer**: Request checkbox approval before Phase 4B

## Critical Success Factors

- **One service at a time**: Complete and verify Service 1 before starting Service 2
- **Backup before changes**: Copy original files in case rollback needed
- **Test after each**: Don't proceed if service doesn't work after migration
- **Transparent replacement**: Router should be drop-in replacement (same method calls)
- **Commit after each**: Git history shows progression

## STOP Conditions

- If service imports fail after migration
- If service functionality breaks after router replacement
- If router doesn't have expected methods service needs

---

**Your Mission**: Successfully migrate 2 Calendar services to router pattern with full verification. Foundation for remaining 4 service migrations.

**Quality Standard**: Each service must work identically after migration - router provides transparent delegation.
