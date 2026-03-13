# Phase 2: QueryRouter Surgical Implementation

## Mission
Make surgical fix in `services/orchestration/engine.py` to re-enable QueryRouter using AsyncSessionFactory pattern. Precise, minimal changes only.

## Prerequisites
- Phase 1 complete: Root cause = missing database session parameter
- Target: Lines 85-110 in engine.py
- Pattern: Use AsyncSessionFactory from lines 135-138

## GitHub Progress Tracking
**Update issue #185 checkboxes as you complete:**

```markdown
## Phase 2: Surgical Implementation
- [ ] Backup created
- [ ] AsyncSession pattern implemented
- [ ] QueryRouter initialization uncommented
- [ ] None placeholder removed
- [ ] Local import test passed
```

## Your Role: Surgical Fix in engine.py

### Step 1: Backup & Verify Current State
```bash
# Create backup
cp services/orchestration/engine.py services/orchestration/engine.py.backup.$(date +%Y%m%d-%H%M)

# Confirm target lines
sed -n '85,107p' services/orchestration/engine.py | head -5
grep -n "self.query_router = None" services/orchestration/engine.py
```

### Step 2: Study the Working Pattern
```bash
# See how AsyncSessionFactory is used successfully
sed -n '135,145p' services/orchestration/engine.py
```

### Step 3: Implement the Fix
Replace the commented synchronous code with async pattern:

**Current (broken):**
```python
# TODO: QueryRouter initialization temporarily disabled due to complex dependency chain
# self.project_repository = ProjectRepository()  # Missing session!
# self.file_repository = FileRepository()        # Missing session!
# self.query_router = QueryRouter(...)

# Temporary placeholder to prevent import errors
self.query_router = None
```

**Fix (using AsyncSessionFactory pattern):**
```python
# QueryRouter initialization using async session pattern
self.query_router = None  # Initialize async in startup method
```

Add async initialization method that follows the pattern from lines 135-138.

### Step 4: Verify Fix Works
```bash
# Test import works
python3 -c "
from services.orchestration.engine import OrchestrationEngine
engine = OrchestrationEngine()
print(f'✓ QueryRouter: {type(engine.query_router)}')
"
```

## Evidence Required
- Before/after code with line numbers
- Successful import test output
- Backup file confirmation

## Key Principle
**Use EXACTLY the AsyncSessionFactory pattern from lines 135-138.** Don't invent new approaches.

## Coordination
Complete implementation first, then Code will handle integration testing.
