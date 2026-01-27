# Draft: CLAUDE.md Discovered Work Discipline Section

**Purpose**: Proposed addition to CLAUDE.md to inline discovered-work capture requirements
**Location**: After line 115 (after current "Completion Discipline" section)
**Impact**: ~30 lines added

---

## Proposed Text

```markdown
### Discovered Work Discipline (Pattern-046 Detail)

When you discover issues during development—test failures, bugs, missing features—you MUST create a tracking issue immediately. No exceptions.

**Triggers (ANY of these = MUST create issue)**:
1. Pre-existing test failure (even if "not your changes")
2. Bug you notice but aren't fixing now
3. Missing feature needed for another feature
4. Tech debt you observe
5. Spend >15 minutes on untracked "small" task

**Workflow**:
```bash
bd create "Descriptive title of discovered issue"
bd dep add <new-issue> <current-issue> --type discovered-from
# Then continue your current work
```

**Anti-patterns**:
- ❌ "Not related to my changes" → Create issue anyway
- ❌ "I'll mention it in the commit" → Create issue anyway
- ❌ "It's small" → Create issue anyway
- ❌ "I'll remember to file it later" → Create issue NOW

**Session wrap-up MUST include**:
- [ ] List of discovered issues filed this session (or "None" if none)

**Why this matters**: PM decides priority, not agent. Untracked work is invisible work. The discomfort of creating "small" issues is working as designed.
```

---

## Insertion Point

**Current CLAUDE.md** (lines 111-115):
```markdown
### Completion Discipline (Patterns 045, 046, 047)
- Tests passing ≠ users succeeding
- Cannot skip work by rationalizing it as "optional"
- If tempted to defer → STOP and ask PM first
- "Time Lord Alert" = permission to pause and discuss uncertainty
```

**After edit** (lines 111-145):
```markdown
### Completion Discipline (Patterns 045, 046, 047)
- Tests passing ≠ users succeeding
- Cannot skip work by rationalizing it as "optional"
- If tempted to defer → STOP and ask PM first
- "Time Lord Alert" = permission to pause and discuss uncertainty

### Discovered Work Discipline (Pattern-046 Detail)

[... new section as above ...]
```

---

## Rationale for Each Element

| Element | Rationale |
|---------|-----------|
| 5 explicit triggers | Removes ambiguity about "what counts" |
| `bd` workflow | Executable, not advisory |
| Anti-patterns with ❌ | Directly addresses today's "not my changes" rationalization |
| Wrap-up checklist item | Makes omission visible in session logs |
| "Why this matters" | Connects to PM authority principle |

---

## What This Does NOT Change

- Pattern-046 remains the authoritative reference
- Serena memory `beads-discovered-work-discipline` remains for detailed examples
- `completion-discipline.md` protocol remains for agents who load it
- No existing guidance is removed

---

## Monitoring Plan

**Week 1-2**: Daily check of Lead Dev session logs for:
- [ ] "Discovered Issues" section present in wrap-up
- [ ] No "not my problem" rationalizations
- [ ] Issues created for noticed-but-not-fixed items

**Success criteria**: Zero missed discovered-work incidents for 14 consecutive days

**Rollback trigger**: If inline guidance causes confusion or unintended behavior, revert CLAUDE.md; external docs remain as fallback

---

*Draft prepared by Documentation Management Specialist*
*January 25, 2026*
