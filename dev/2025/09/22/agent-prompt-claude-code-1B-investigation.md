# Phase 0: CORE-GREAT-1B Orchestration Integration Investigation

## Mission
Investigate the orchestration pipeline from Intent → OrchestrationEngine → QueryRouter and identify what needs to be connected to enable end-to-end GitHub issue creation through chat.

## Prerequisites
- GREAT-1A complete: QueryRouter enabled and initializing successfully
- Focus: Connection points and integration flow
- Goal: Prepare for end-to-end orchestration pipeline

## GitHub Progress Tracking
**Update issue #186 checkboxes as you investigate (PM will validate):**

```markdown
## Investigation Phase
- [ ] OrchestrationEngine QueryRouter connection analyzed
- [ ] Intent → Orchestration flow mapped
- [ ] Chat interface connection points identified
- [ ] Bug #166 UI hang root cause found
- [ ] Integration test requirements defined
```

## Your Role: Pipeline Investigation & Flow Mapping

### Step 1: Trace the Flow
```bash
# How does chat interface connect to orchestration?
grep -r "OrchestrationEngine" web/ --include="*.py"
grep -r "intent" web/ --include="*.py" | head -10

# Where does GitHub issue creation happen?
grep -r "create.*github.*issue" . --include="*.py" | head -10
grep -r "GitHubAgent" . --include="*.py"
```

### Step 2: Check QueryRouter Integration
```bash
# How is QueryRouter supposed to be used?
grep -A 10 -B 5 "get_query_router" services/orchestration/engine.py
grep -r "query_router" services/ --include="*.py" | head -15

# What calls OrchestrationEngine?
grep -r "OrchestrationEngine(" . --include="*.py"
```

### Step 3: Investigate Bug #166 (UI hang)
```bash
# Look for multiple request handling
grep -r "multiple.*prompt" . --include="*.py"
grep -r "concurrent" web/ --include="*.py"
grep -r "async.*def" web/app.py | head -10
```

### Step 4: Map Integration Points
```bash
# Find all the connection points that need wiring
grep -r "create_workflow_from_intent" . --include="*.py"
grep -r "execute_workflow" . --include="*.py"
```

## Evidence Required
- Complete flow diagram (Intent → Chat → Orchestration → QueryRouter → GitHub)
- Missing connection points identified
- Bug #166 root cause analysis
- Performance bottleneck locations

## Success: Clear Integration Plan
Understand exactly what connections need to be made for end-to-end flow.

## Test Scope Specificity
**Unit tests**: Individual component connections
**Integration tests**: End-to-end flow through orchestration  
**Performance tests**: <500ms target validation

## Coordination
Working with Cursor on targeted connection implementation.
