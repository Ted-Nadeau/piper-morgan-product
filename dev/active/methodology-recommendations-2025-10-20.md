# Methodology Recommendations - October 20, 2025

**Context**: Learnings from Sprint A4 and Sprint A5 (CORE-LEARN-A)
**Source**: Lead Developer session observations
**Purpose**: Batch updates to agent templates and methodology documents

---

## 1. Post-Compaction Protocol (WORKING PERFECTLY ✅)

**Status**: Currently implicit, needs to be explicit in templates

**Current behavior** (proven effective):
```markdown
After compaction:
1. ⏸️ STOP - Do not continue working
2. 📋 REPORT - Summarize what was just completed
3. ❓ ASK - "Should I proceed to next task/phase?"
4. ⏳ WAIT - For explicit instructions
```

**Where to add**:

### A. Agent Prompt Template (`agent-prompt-template.md`)
Add as mandatory section after STOP Conditions:

```markdown
## Post-Compaction Protocol

**If you have just finished compacting your context**:

1. **STOP** - Do not continue with any work
2. **REPORT** - Provide a summary of what was completed:
   - What was accomplished
   - What tests pass
   - What files were created/modified
   - Current status
3. **ASK** - "Should I proceed to [next task/phase]?"
4. **WAIT** - Do not continue until you receive explicit instructions

**Why**: Compaction is a natural checkpoint. Pausing allows PM to review progress, catch issues early, and provide guidance before proceeding.

**Never skip this protocol.** Even if you have clear next steps, always pause after compaction for PM review.
```

### B. Essential Agent Briefing (`BRIEFING-ESSENTIAL-AGENT.md`)
Add to critical protocols section:

```markdown
### Post-Compaction Protocol

After compacting context: STOP → REPORT → ASK → WAIT

Never continue automatically after compaction. This is a mandatory checkpoint.
```

### C. Task Prompt Templates (all task prompts)
Add after "CRITICAL: Post-Compaction Protocol" section (already present in recent prompts):

Ensure this exact wording appears in ALL task prompt templates going forward.

---

## 2. "Under Duress" Protocol (NEW - FROM CORE-LEARN-A)

**Status**: Discovered during CORE-LEARN-A Phase 4

**Problem observed**:
- Code agent silently removed "API documentation" from todo list
- Prioritized fixing signature mismatches (correct decision)
- But didn't flag the change or return to deferred work
- PM had to notice the change in real-time

**Lesson**: Agents need explicit protocol for handling unexpected prioritization changes

**Required behavior**:

```markdown
## Prioritization Changes Protocol ("Under Duress")

When you encounter an unexpected critical issue that requires deprioritizing planned work:

### Required Steps:

1. **FLAG THE CHANGE** 🚨
   ```
   ⚠️ PRIORITIZATION CHANGE

   I need to pause [planned work X] to address [critical issue Y].
   ```

2. **EXPLAIN THE REASON**
   ```
   Reason: [Brief explanation of why this is critical path]
   Impact: [What breaks if not fixed]
   Scope: [Estimated time/complexity]
   ```

3. **ASK FOR GUIDANCE**
   ```
   How should I proceed?

   Option A: Fix critical issue now, return to deferred work after
   Option B: Fix critical issue now, defer work to separate task
   Option C: Different approach (please advise)
   ```

4. **TRACK DEFERRED WORK**
   - Mark todo item as `[DEFERRED]` - don't delete
   - Keep visible in todo list
   - Include in status reports

5. **RETURN OR ESCALATE**
   After resolving critical issue:
   ```
   ✅ Critical issue resolved: [brief summary]

   Returning to deferred work: [work description]

   OR

   ✅ Critical issue resolved: [brief summary]

   Should I return to deferred work [X], or close the task with [X] deferred?
   ```

### Key Principles:

- **Transparency over silence**: Always flag changes explicitly
- **No silent removals**: Never remove planned work without discussion
- **Track everything**: Deferred work must remain visible
- **Close the loop**: Either return to work or get approval to skip

### Anti-Patterns (DON'T DO):

❌ Silently removing todo items
❌ Making prioritization decisions without consultation
❌ Hiding changes in progress reports
❌ Forgetting deferred work after resolving critical issues
❌ Only explaining when PM asks

### Good Examples:

**Example 1: Critical Bug During Implementation**
```
⚠️ PRIORITIZATION CHANGE

I need to pause creating integration tests to fix signature mismatches between
API routes and QueryLearningLoop.

Reason: All tests are failing due to incompatible method signatures. This blocks
all verification work.
Impact: Cannot verify any functionality until signatures align.
Scope: Estimated 1-2 hours to fix across API/engine/tests.

How should I proceed?

Option A: Fix signatures now, return to integration tests after
Option B: Fix signatures now, defer integration tests to separate task
Option C: Different approach (please advise)

[DEFERRED] Create integration tests - waiting on signature fix
```

**Example 2: After Resolving Critical Issue**
```
✅ Critical issue resolved: Fixed signature mismatches across
API/QueryLearningLoop/tests. All interfaces now aligned.

Returning to deferred work: Creating integration tests
```

### When This Protocol Applies:

- Discovering blocking bugs during implementation
- Finding architectural issues requiring refactoring
- Encountering missing dependencies
- Hitting performance problems requiring optimization
- Any situation requiring deprioritizing planned work

### When This Protocol Does NOT Apply:

- Normal task progression (Phase 1 → Phase 2)
- Minor refactoring that doesn't affect timeline
- Code cleanup within same file
- Normal debugging within scope
```

**Where to add**:

### A. Agent Prompt Template (`agent-prompt-template.md`)
Add new section after "Post-Compaction Protocol":

Include full protocol as documented above.

### B. Essential Agent Briefing (`BRIEFING-ESSENTIAL-AGENT.md`)
Add to critical protocols:

```markdown
### Prioritization Changes Protocol

When deprioritizing work: FLAG → EXPLAIN → ASK → TRACK → RETURN

Never silently remove planned work. Always maintain visibility.
```

### C. Task Prompt Templates
Add reminder section:

```markdown
## Important: Prioritization Changes

If you encounter critical issues requiring prioritization changes:
- FLAG the change explicitly (don't silently remove todos)
- EXPLAIN why it's critical
- ASK for guidance on handling
- TRACK deferred work visibly
- RETURN to deferred work or ASK before skipping

See agent methodology for full "Under Duress Protocol".
```

### D. New Methodology Document
Create `methodology-19-UNDER-DURESS-PROTOCOL.md`:

Full protocol documentation with examples, anti-patterns, and guidance.

---

## 3. Natural Phase Boundaries (WORKING WELL ✅)

**Status**: Currently implicit, should be explicit

**Observed behavior** (correct):
- Code paused between Phase 1 (API) and Phase 2 (orchestration)
- Recognized logical stopping point
- Asked before proceeding

**Why this is good**:
- Allows PM review at natural checkpoints
- Prevents runaway work
- Enables course correction
- Facilitates incremental commits

**Recommendation**: Make explicit in templates

**Where to add**:

### Agent Prompt Template
Add guidance:

```markdown
## Natural Phase Boundaries

Recognize and respect natural stopping points in your work:

### When to Pause and Ask:

- Between major implementation phases
- After completing distinct functional areas
- Before switching to different file/service
- After resolving critical issues
- When approaching estimated time limits

### How to Pause:

```
✅ [Phase/Section] Complete

Summary:
- [What was accomplished]
- [What's working]
- [What remains]

Ready to proceed with [next phase]? Or pause here for review?
```

### Benefits:

- Allows PM to review incremental progress
- Enables early detection of issues
- Facilitates better commit messages
- Provides natural checkpoints for course correction

### This Does NOT Mean:

❌ Stopping after every file
❌ Asking for permission for minor decisions
❌ Breaking up cohesive work unnecessarily

Use judgment: pause at logical boundaries, not arbitrary points.
```

---

## 4. Evidence-First Reporting (WORKING WELL ✅)

**Status**: Working implicitly, should be reinforced

**Current behavior** (excellent):
- Shows actual test output
- Provides file locations
- Links to commits
- Includes verification commands

**Recommendation**: Reinforce as standard

**Where to add**:

### Task Prompt Templates
Reinforce in success criteria:

```markdown
## Evidence Requirements

For EVERY claim about completion:

- **"Tests pass"** → Show actual test output
- **"Feature works"** → Show demonstration/curl output
- **"File created"** → Show file path and line count
- **"Integration complete"** → Show end-to-end verification

Always provide:
- File locations (absolute paths)
- Commit hashes (when applicable)
- Test output (full or summarized)
- Verification commands (for PM to run)

Avoid unverifiable claims like:
❌ "Everything works"
❌ "Tests are good"
❌ "Done with that"

Instead:
✅ "All 9 tests passing (see output below)"
✅ "Created web/api/routes/learning.py (538 lines)"
✅ "Verified with: curl http://localhost:8001/api/v1/learning/health"
```

---

## 5. Todo List Management (NEEDS REINFORCEMENT)

**Status**: Partially working, needs explicit rules

**Problem**: Agents sometimes remove items silently

**Required behavior**:

```markdown
## Todo List Management

### Rules:

1. **Keep all todos visible** throughout the task
2. **Never delete todos silently** - always flag removals
3. **Mark deferred items** as [DEFERRED], don't remove
4. **Update status clearly**: ☐ → ☒ or [DEFERRED]
5. **Return to deferred items** or ask before skipping

### Status Indicators:

- `☐` - Not started
- `🔄` - In progress
- `☒` - Complete
- `[DEFERRED]` - Temporarily set aside
- `[SKIPPED]` - Deliberately not done (requires explanation)

### Examples:

**Good**:
```
☐ Create API endpoints
🔄 Fix signature mismatches (critical path)
[DEFERRED] Write integration tests - blocked by signatures
```

**Bad**:
```
☐ Create API endpoints
☐ Fix signature mismatches

(Integration tests silently removed from list)
```

### If You Need to Skip Work:

Don't remove silently. Instead:

```
[SKIPPED] Create API documentation

Reason: FastAPI auto-generates Swagger docs at /docs endpoint.
Formal docs in docs/public/api-reference/ would be nice-to-have but
not required for issue completion.

Should I:
A) Create formal docs now (1h)
B) Defer to separate issue
C) Skip entirely (auto-docs sufficient)
```
```

**Where to add**:

- Task prompt templates (todo management section)
- Agent prompt template (work tracking section)
- Essential briefings (quick reference)

---

## 6. Serena MCP Credit (DOCUMENTATION)

**Status**: Need to document Serena's impact

**What Serena enables**:
- Symbolic code index search (not just text)
- Understands classes, methods, imports, structure
- 4-minute architectural discovery (would be 30-45 min manual)
- Find existing infrastructure before building

**Recommendation**: Document in methodology

**Where to add**:

### Create New Document: `serena-mcp-discovery-guide.md`

```markdown
# Serena MCP Discovery Guide

## Overview

Serena MCP provides symbolic code index search capabilities that enable
rapid architectural discovery. Instead of manual grepping and file browsing,
Serena understands code structure and can find classes, methods, and
relationships in seconds.

## When to Use Serena

### Discovery Phase (Always)
Before implementing features:
1. Search for existing implementations
2. Find related services and patterns
3. Identify integration points
4. Assess code reuse opportunities

### During Implementation
When you need to:
- Find where a class is defined
- Locate all implementations of an interface
- Discover usage patterns
- Verify no duplication

## Key Commands

### find_symbol
Find class/method definitions:
```python
mcp__serena__find_symbol("LearningService|PatternRecognizer", scope="services")
```

### search_project
Search code with semantic understanding:
```python
mcp__serena__search_project("learning|pattern|preference", file_pattern="services/**/*.py")
```

## Impact

**Sprint A5 Example**:
- Traditional approach: 30-45 minutes discovery
- With Serena: 4 minutes
- Found: 4,252 lines of existing infrastructure
- Result: 6h task → 1h task (6x faster)

## Best Practices

1. **Always discovery first** - Don't build before searching
2. **Use symbolic search** - More accurate than grep
3. **Verify findings** - Confirm code works as documented
4. **Document leverage** - Report what was reused vs built

## See Also

- Sprint A4 discovery (95% infrastructure found)
- Sprint A5 discovery (90% infrastructure found)
- Pattern: Discovery → Wire → Ship
```

### Reference in Methodology
Add to `methodology-00-EXCELLENCE-FLYWHEEL.md`:

```markdown
### Discovery Tools

Serena MCP provides symbolic code index search:
- 10x faster than manual discovery
- Understands code structure, not just text
- Essential for finding existing infrastructure

Always use Serena for discovery phase before implementation.
```

---

## Implementation Checklist

### Immediate (Before Next Task)
- [ ] Add post-compaction protocol to current task prompts
- [ ] Add "under duress" protocol to current task prompts

### This Evening (Batch Updates)
- [ ] Update `agent-prompt-template.md` with all 5 protocols
- [ ] Update `BRIEFING-ESSENTIAL-AGENT.md` with quick references
- [ ] Create `methodology-19-UNDER-DURESS-PROTOCOL.md`
- [ ] Create `serena-mcp-discovery-guide.md`
- [ ] Update all task prompt templates (check /templates directory)
- [ ] Update `methodology-00-EXCELLENCE-FLYWHEEL.md` (Serena reference)

### Soon (Next Sprint)
- [ ] Review effectiveness of new protocols
- [ ] Gather feedback from agent behaviors
- [ ] Refine language based on what works
- [ ] Add examples from real situations

---

## Files to Create/Modify

### New Files
1. `methodology-19-UNDER-DURESS-PROTOCOL.md` (full protocol documentation)
2. `serena-mcp-discovery-guide.md` (Serena usage guide)

### Files to Modify
1. `agent-prompt-template.md` (add 5 protocol sections)
2. `BRIEFING-ESSENTIAL-AGENT.md` (add quick references)
3. `BRIEFING-ESSENTIAL-LEAD-DEV.md` (add quick references)
4. `BRIEFING-ESSENTIAL-ARCHITECT.md` (add quick references)
5. `methodology-00-EXCELLENCE-FLYWHEEL.md` (add Serena reference)
6. All task prompt templates in `/templates` directory

### Template Locations to Check
- `gameplan-template.md`
- `agent-prompt-template.md`
- `lead-developer-prompt-template.md`
- Any sprint/task-specific templates

---

## Success Criteria

These updates are complete when:

- [ ] All 6 protocols are documented in appropriate files
- [ ] Agent templates include all mandatory protocols
- [ ] Essential briefings include quick references
- [ ] Methodology documents include Serena guide
- [ ] Templates tested with next agent deployment
- [ ] Protocols prevent observed anti-patterns:
  - ✅ No silent todo removals
  - ✅ No prioritization changes without flagging
  - ✅ No skipping deferred work without asking
  - ✅ Always pause after compaction

---

**Date Created**: October 20, 2025
**Context**: Sprint A4 & A5 learnings
**Priority**: High (prevents quality issues)
**Effort**: ~2 hours batch updates

_These recommendations capture proven patterns that improve agent collaboration quality._
