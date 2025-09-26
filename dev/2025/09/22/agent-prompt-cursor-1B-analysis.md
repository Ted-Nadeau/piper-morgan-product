# Phase 0: CORE-GREAT-1B Connection Point Analysis

## Mission
Analyze specific connection points in the orchestration pipeline to identify exactly where integration needs to happen between Intent classification, OrchestrationEngine, and QueryRouter.

## Prerequisites  
- GREAT-1A complete: QueryRouter `get_query_router()` method exists
- Focus: Specific file analysis for connection points
- Goal: Identify exact integration requirements

## GitHub Progress Tracking
**Update issue #186 checkboxes as you analyze (PM will validate):**

```markdown
## Connection Analysis
- [ ] web/app.py orchestration usage analyzed
- [ ] OrchestrationEngine initialization verified
- [ ] QueryRouter connection points identified
- [ ] Async session patterns confirmed
- [ ] Bug #166 concurrency issues located
```

## Your Role: Focused Connection Analysis

### Step 1: Analyze web/app.py Integration
```bash
# How does the web layer use orchestration?
grep -n -A 5 -B 5 "OrchestrationEngine" web/app.py
grep -n "intent" web/app.py | head -10

# Check for GitHub issue creation endpoints
grep -n -A 10 "github" web/app.py
```

### Step 2: Verify OrchestrationEngine Connection
```bash
# Check current QueryRouter integration
sed -n '90,120p' services/orchestration/engine.py
grep -n "get_query_router" services/orchestration/engine.py

# Verify initialization sequence
grep -n -A 5 "__init__" services/orchestration/engine.py
```

### Step 3: Check Session Management Integration
```bash
# Ensure async session patterns are used correctly
grep -n -A 10 "AsyncSessionFactory" services/orchestration/engine.py
grep -n "session_scope" services/orchestration/engine.py
```

### Step 4: Analyze Bug #166 (UI hang)
```bash
# Look for concurrent request handling issues
grep -n -A 5 -B 5 "concurrent\|multiple\|async" web/app.py
grep -n "await.*orchestrat" web/app.py
```

## Evidence Required
- Exact line numbers for connection points
- Current vs required integration patterns
- Specific files needing modification
- Bug #166 technical root cause

## Success: Precise Integration Requirements
Know exactly which lines in which files need changes.

## Test Scope
**Unit tests**: Individual method connections
**Integration tests**: Component interaction verification

## Coordination  
Provide specific connection requirements to Code for broader integration planning.
