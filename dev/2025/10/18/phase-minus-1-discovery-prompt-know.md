# Phase -1: Discovery - CORE-KNOW #99

**Agent**: Claude Code (Programmer)
**Issue**: #99 - CORE-KNOW
**Phase**: -1 (Discovery) - Understand current state
**Date**: October 18, 2025, 1:55 PM
**Duration**: ~30 minutes estimated

---

## Mission

Discover the current state of the Knowledge Graph infrastructure. Like Issue #197 (Ethics), we expect the Knowledge Graph is 75-95% built (PM-040 complete) but just not connected to conversation flow.

## Context

**Pattern from Ethics (#197)**:
- Found sophisticated system 95% complete
- Just needed architectural connection
- Result: 2.3 hours to activate vs 2-3 days estimate

**Expected for Knowledge Graph**:
- KnowledgeGraphService likely exists and works
- PostgreSQL backend probably operational
- Graph queries probably functional
- Just not connected to conversation flow

**Your Job**: Confirm what exists, find the gap, report findings.

---

## Investigation Strategy

Use Serena efficiently to understand the codebase without reading every file.

### Step 1: Find Knowledge Graph Components (10 minutes)

**Find the main service**:
```python
mcp__serena__find_symbol(
    name_regex="KnowledgeGraph.*",
    scope="services"
)

# Expected findings:
# - KnowledgeGraphService (main service)
# - KnowledgeGraph (data model)
# - KnowledgeGraphAdapter (database layer)
```

**Get overview of knowledge services**:
```python
mcp__serena__get_symbols_overview("services/knowledge/")

# Look for:
# - Service classes
# - Query methods
# - Integration points
# - TODO markers
```

**Check for existing queries**:
```python
mcp__serena__search_project(
    query="def query.*knowledge",
    file_pattern="services/knowledge/**/*.py"
)

# Expected:
# - query_projects()
# - query_relationships()
# - query_patterns()
# - etc.
```

### Step 2: Check Conversation Integration (10 minutes)

**Find conversation handling**:
```python
mcp__serena__find_symbol(
    name_regex="Conversation.*",
    scope="services"
)

# Looking for:
# - ConversationHandler
# - ConversationManager
# - ConversationService
```

**Check IntentService** (likely integration point):
```python
mcp__serena__get_symbols_overview("services/intent/intent_service.py")

# Check if KnowledgeGraph already integrated
# Look for knowledge_graph imports or calls
```

**Search for knowledge graph usage**:
```python
mcp__serena__search_project(
    query="knowledge.*graph",
    file_pattern="services/**/*.py"
)

# Find where (if anywhere) KG is currently used
```

### Step 3: Check Database & Infrastructure (5 minutes)

**Find PostgreSQL integration**:
```python
mcp__serena__search_project(
    query="knowledge.*postgres",
    file_pattern="services/**/*.py"
)

# Verify database backend exists
```

**Check for migrations**:
```python
# Look for database schema
mcp__serena__search_project(
    query="knowledge.*table",
    file_pattern="**/*.sql"
)
```

### Step 4: Find TODO Markers (5 minutes)

**Look for integration TODOs**:
```python
mcp__serena__search_project(
    query="TODO.*knowledge",
    file_pattern="services/**/*.py"
)

# Expected findings:
# - "TODO: Connect knowledge graph to conversation"
# - "TODO: Add boundary checking"
# - "TODO: Integrate with context system"
```

**Check for boundary TODOs** (Issue #230):
```python
mcp__serena__search_project(
    query="TODO.*boundary",
    file_pattern="services/knowledge/**/*.py"
)
```

---

## Expected Findings

Based on pattern from Ethics (#197), expect to find:

### ✅ Likely EXISTS (PM-040 complete)
- KnowledgeGraphService class
- PostgreSQL database schema
- Graph query methods
- Data models (Node, Edge, Relationship)
- Database adapter/connector

### ❌ Likely MISSING (needs connection)
- Integration with conversation flow
- Connection to IntentService or ConversationHandler
- Context enhancement logic
- Boundary enforcement (Issue #230)

### ⚠️ Likely PARTIAL
- Some test coverage (but not integrated tests)
- Some documentation (but not operational)
- Some configuration (but not activated)

---

## Discovery Report Format

After investigation, create a report with these sections:

### 1. What Exists ✅

```markdown
## Knowledge Graph Infrastructure

**Main Service**:
- Location: services/knowledge/knowledge_graph_service.py
- Status: [EXISTS / PARTIAL / MISSING]
- Key methods:
  - query_projects()
  - query_relationships()
  - [list other methods]

**Database**:
- Backend: PostgreSQL
- Schema: [EXISTS / NEEDS_UPDATE / MISSING]
- Tables: [list tables found]

**Tests**:
- Location: tests/knowledge/
- Count: [X tests]
- Status: [passing / failing / not run]
```

### 2. What's Missing ❌

```markdown
## Integration Gaps

**Conversation Connection**:
- Current: Knowledge Graph isolated
- Missing: Integration with conversation flow
- Needed: Wire to IntentService/ConversationHandler

**Context Enhancement**:
- Current: No context enrichment
- Missing: Method to enhance conversation context
- Needed: get_conversation_context() or similar

**Boundary Enforcement** (Issue #230):
- Current: [status]
- Missing: Depth limits, node limits, timeouts
- Needed: BoundaryEnforcer implementation
```

### 3. Integration Architecture Decision ⚙️

```markdown
## Recommended Integration Point

**Option A: IntentService** (like Ethics)
Pros:
- Consistent with Ethics pattern
- Universal entry point
- Already handling context

Cons:
- [list any cons found]

**Option B: ConversationHandler** (if exists)
Pros:
- [list pros]

Cons:
- [list cons]

**Option C: OrchestrationEngine**
Pros:
- [list pros]

Cons:
- [list cons]

**Recommendation**: [A/B/C]
**Rationale**: [explain why]
```

### 4. Implementation Estimate 📊

```markdown
## Work Required

**Phase 1: Integration Architecture** (30 min)
- [list tasks]

**Phase 2: Implementation** (1-2 hours)
- Create integration layer
- Wire to conversation flow
- Add feature flag
- [other tasks]

**Phase 3: Testing** (1 hour)
- Integration tests
- Performance tests
- Canonical query tests

**Total**: [estimate]
```

---

## Success Criteria

Phase -1 is complete when:

- [ ] Knowledge Graph Service located and understood
- [ ] Database infrastructure verified
- [ ] Integration gap identified
- [ ] Recommended integration point chosen
- [ ] Implementation estimate provided
- [ ] Discovery report created

---

## Important Notes

### Use Serena Efficiently

**Before reading full files**:
1. `find_symbol()` to locate components
2. `get_symbols_overview()` to understand structure
3. `search_project()` to find patterns
4. Read specific files only when needed

### Pattern Recognition

This is likely very similar to Ethics (#197):
- Sophisticated system already built
- Just needs architectural connection
- Feature flag for safe activation
- Quick win if we recognize the pattern

### Don't Over-Investigate

**30 minutes is enough** to:
- Find main components
- Identify the gap
- Recommend integration approach

**Don't spend time on**:
- Reading every line of code
- Understanding every method
- Optimizing existing code

**Goal**: Understand enough to connect it, not to rewrite it.

---

## Questions to Answer

1. **Does KnowledgeGraphService exist?** (Yes/No)
2. **Is PostgreSQL backend operational?** (Yes/No/Unknown)
3. **Where should we integrate?** (IntentService/ConversationHandler/Other)
4. **Are there existing TODOs pointing to the work?** (Yes/No)
5. **How much work to connect?** (Hours estimate)

---

## Deliverable

**File**: `dev/2025/10/18/phase-minus-1-discovery-report.md`

**Contents**:
- What exists (infrastructure)
- What's missing (integration)
- Recommended architecture
- Implementation estimate
- Any surprises or concerns

---

**Remember**: This is discovery, not implementation. Fast reconnaissance to plan the real work.

**Ready to investigate the Knowledge Graph!** 🔍
