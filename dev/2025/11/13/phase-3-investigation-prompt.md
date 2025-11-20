# Investigation Prompt: Phase 3 Architecture Research
## Using Serena to Understand Existing Structure

**Date**: November 13, 2025, 3:35 PM PT
**From**: Lead Developer
**To**: Code Agent
**Purpose**: Research existing architecture for Phase 3 (Pattern Suggestions)

---

## Your Mission

Use Serena to investigate the existing codebase and answer specific questions about Phase 3 implementation. This is **research only** - no code changes.

**Duration**: 30 minutes maximum

---

## Questions to Answer

### 1. Frontend Architecture

**Question**: What frontend framework/structure exists for the web UI?

**Serena Queries**:
```python
# Find web UI structure
mcp__serena__list_dir("web", recursive=true)

# Check for React/Vue/etc
mcp__serena__find_files("web", patterns=["*.jsx", "*.vue", "*.ts", "*.tsx"])

# Find main app entry point
mcp__serena__find_symbol("app", "web", depth=2)

# Check templates if any
mcp__serena__list_dir("web/templates")
```

**What to report**:
- Framework used (React, Vue, templates, etc.)
- Main entry point files
- Component structure if any
- Where chat UI lives
- Example of existing UI components

---

### 2. Orchestration Response Structure

**Question**: How are orchestration responses currently structured? Where would suggestions fit?

**Serena Queries**:
```python
# Find orchestration engine
mcp__serena__get_symbols_overview("services/orchestration/orchestration_engine.py")

# Check response model
mcp__serena__find_symbol("OrchestrationResult", "services")

# Find where responses are built
mcp__serena__find_symbol("execute", "services/orchestration")
```

**What to report**:
- Current response structure (JSON shape)
- Where response is built
- Existing fields in response
- How to add new fields (like suggestions)
- Example response from code

---

### 3. Learning Handler Interface

**Question**: What methods does LearningHandler already have? Is `get_suggestions()` implemented?

**Serena Queries**:
```python
# Check LearningHandler methods
mcp__serena__get_symbols_overview("services/learning/learning_handler.py")

# Check if get_suggestions exists
mcp__serena__find_symbol("get_suggestions", "services/learning/learning_handler.py")

# Check what pattern retrieval exists
mcp__serena__find_symbol("get_patterns", "services/learning")
```

**What to report**:
- All methods in LearningHandler
- Does `get_suggestions()` exist? If yes, what's its signature?
- What pattern retrieval methods exist?
- How patterns are queried from database
- Example code showing pattern retrieval

---

### 4. Pattern Model Structure

**Question**: What fields does LearnedPattern have? What's in pattern_data?

**Serena Queries**:
```python
# Check LearnedPattern model
mcp__serena__find_symbol("LearnedPattern", "services/database/models.py", include_body=true)

# Check pattern types
mcp__serena__find_symbol("PatternType", "services/database/models.py")
```

**What to report**:
- All fields in LearnedPattern
- What's stored in pattern_data (JSONB structure)
- Pattern types available
- How confidence is calculated/stored
- Example pattern from database (if possible)

---

### 5. Intent Service Integration

**Question**: Where in IntentService should we check for patterns? What's the execution flow?

**Serena Queries**:
```python
# Check IntentService structure
mcp__serena__get_symbols_overview("services/intent/intent_service.py")

# Find where learning_handler is called
mcp__serena__find_symbol("capture_action", "services/intent")
mcp__serena__find_symbol("record_outcome", "services/intent")

# Check execute method
mcp__serena__find_symbol("execute", "services/intent/intent_service.py", include_body=true)
```

**What to report**:
- IntentService execution flow
- Where capture_action is called (already done in Phase 1)
- Where we should check for suggestions (before/after what?)
- How to integrate with existing flow
- Example execution sequence

---

### 6. Existing Suggestion UI (if any)

**Question**: Are there any existing suggestion/notification UI components we can reuse?

**Serena Queries**:
```python
# Find any suggestion components
mcp__serena__find_files("web", patterns=["*suggest*", "*notif*", "*toast*", "*banner*"])

# Check for modal/dialog components
mcp__serena__find_files("web", patterns=["*modal*", "*dialog*", "*popup*"])

# Find chat UI components
mcp__serena__find_symbol("chat", "web", depth=2)
mcp__serena__find_symbol("message", "web", depth=2)
```

**What to report**:
- Any existing suggestion UI components
- Notification/toast patterns used
- Chat message rendering code
- How to add interactive elements (buttons)
- Example UI component code

---

### 7. API Endpoint Structure

**Question**: How are existing learning API endpoints structured? Where would feedback endpoints fit?

**Serena Queries**:
```python
# Check learning routes
mcp__serena__get_symbols_overview("web/api/routes/learning.py")

# Find route patterns
mcp__serena__find_symbol("router", "web/api/routes/learning.py")

# Check request/response models
mcp__serena__find_symbol("LearningSettingsUpdate", "web/api/routes/learning.py")
```

**What to report**:
- Existing learning endpoints (we know 7 from Phase 2)
- Request/response model patterns
- Where to add new endpoints (feedback, suggestions)
- Authentication/user_id handling
- Example endpoint code

---

## Output Format

Create a markdown document: `dev/2025/11/13/phase-3-architecture-research.md`

**Structure**:
```markdown
# Phase 3 Architecture Research
## Investigation Results for Pattern Suggestions

**Date**: November 13, 2025
**Investigator**: Code Agent
**Duration**: [X] minutes
**Method**: Serena symbolic queries

---

## 1. Frontend Architecture

### Framework
[React/Vue/templates/etc]

### Structure
[directory tree]

### Chat UI Location
[file paths]

### Example Component
```[language]
[code]
```

---

## 2. Orchestration Response Structure

### Current Response Model
```python
[code showing OrchestrationResult]
```

### Where Response is Built
[file:line]

### How to Add Suggestions
[explanation + code snippet]

---

## 3. Learning Handler Interface

### Existing Methods
- capture_action(...)
- record_outcome(...)
- get_suggestions(...) [EXISTS/MISSING]
- [other methods]

### Pattern Retrieval
```python
[code showing how patterns are queried]
```

---

## 4. Pattern Model Structure

### LearnedPattern Fields
[list all fields with types]

### pattern_data Structure
```json
{
  "intent": "...",
  "context": {...},
  ...
}
```

### Example Pattern
[show actual pattern from code/tests]

---

## 5. Intent Service Integration

### Execution Flow
1. [step]
2. [step]
3. [suggested insertion point for pattern checking]
4. [step]

### Existing Integration Points
- capture_action: [location]
- record_outcome: [location]

### Recommended Integration Point
[where to add get_suggestions call]

---

## 6. Existing Suggestion UI

### Components Found
- [list any reusable components]
- [or "None found - need to create"]

### Chat Rendering
[code showing how messages are rendered]

### Interactive Elements
[how to add buttons/actions to messages]

---

## 7. API Endpoint Structure

### Existing Patterns
[show 2-3 example endpoints]

### Where to Add Feedback Endpoints
[recommendation with reasoning]

### Authentication Pattern
[how user_id is obtained]

---

## Phase 3 Implementation Recommendations

### Backend Changes Needed
1. [specific change]
2. [specific change]

### Frontend Changes Needed
1. [specific change]
2. [specific change]

### Integration Points
1. [where to hook in]
2. [where to hook in]

### Estimated Complexity
- Backend: [SMALL/MEDIUM/LARGE]
- Frontend: [SMALL/MEDIUM/LARGE]
- Overall: [SMALL/MEDIUM/LARGE]

---

## Questions for Lead Developer

1. [any ambiguities found]
2. [any decisions needed]
3. [any risks identified]

---

**Evidence Collected**: [N] Serena queries executed
**Files Investigated**: [N] files examined
**Confidence**: [HIGH/MEDIUM/LOW] that this research is accurate
```

---

## Success Criteria

**Minimum Requirements**:
- [ ] All 7 questions answered with evidence
- [ ] Serena queries shown for each answer
- [ ] Code examples provided where relevant
- [ ] Clear recommendations for Phase 3 implementation
- [ ] Document created in dev/2025/11/13/

**Quality Indicators**:
- [ ] No guessing - every answer backed by code
- [ ] File paths and line numbers provided
- [ ] Example code snippets from actual codebase
- [ ] Clear integration points identified
- [ ] Complexity estimates realistic

---

## STOP Conditions

**STOP if**:
- ❌ Can't find web frontend (may not exist yet)
- ❌ OrchestrationResult structure unclear
- ❌ Learning Handler doesn't exist (should exist from Phase 1)
- ❌ Can't understand pattern structure
- ❌ Integration points completely unclear

**If STOP triggered**:
1. Document what you DID find
2. List what's MISSING or UNCLEAR
3. Recommend escalation to Chief Architect

---

## Time Management

- **Serena queries**: 15 minutes (methodical, not rushed)
- **Analysis**: 10 minutes (understand what you found)
- **Documentation**: 5 minutes (write clear report)
- **Total**: 30 minutes

Don't spend more than 30 minutes on this. If you can't answer something, document that and move on.

---

## Remember

**This is research, not implementation**. You're gathering facts to inform Phase 3 implementation, not writing code yet.

**Use Serena extensively**. Every answer should be backed by a Serena query showing you the actual code.

**No assumptions**. If you can't find something, say "NOT FOUND" not "probably exists at..."

**Evidence required**. Show the code, don't paraphrase it.

---

**Status**: Ready for Code Agent deployment
**Expected Duration**: 30 minutes
**Deliverable**: phase-3-architecture-research.md with evidence

---

_"Always use Serena first"_
_"Evidence, not assumptions"_
_"Research before implementation"_
