# Gameplan: #701 DOCS-GLOSSARY-GUIDED-PROCESS

**Issue**: #701 - Update glossary with Guided Process terminology
**Date**: 2026-01-26
**Author**: Lead Developer

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Glossary file: `knowledge/piper-morgan-glossary-v1.1.md`
- [x] Source of truth: ADR-049 (now ACCEPTED)
- [x] Implementation reference: `services/process/` (just created)

**My understanding of the task**:
- Add 3 new glossary terms (Guided Process, Process Registry, Process Type)
- Clarify 3 existing terms (Workflow, StandupConversation, PortfolioOnboardingSession)
- Proofread for errors

### Part A.2: Work Characteristics Assessment

**Worktree Assessment**:
- [ ] Multiple agents in parallel - NO
- [ ] Task duration >30 min - NO (estimate: 15 min)
- [ ] Multi-component work - NO
- [ ] Exploratory/risky changes - NO

**Assessment**: ☑️ **SKIP WORKTREE** - Single agent, documentation-only, ~15 min estimate

### Part B: PM Verification

**What actually exists**:
```bash
ls knowledge/piper-morgan-glossary-v1.1.md
# File exists, 500+ lines
```

**Task type**:
- [x] Add to existing documentation

### Part C: Decision

- [x] **PROCEED** - Understanding correct, task straightforward

---

## Phase 0: Investigation

### GitHub Issue Verification
- [x] Issue #701 exists and is properly formatted (audit-cascade applied)
- [x] ADR-049 is ACCEPTED (source of definitions)
- [x] `services/process/` implementation exists (reference for accuracy)

### Current Glossary State

Terms to verify exist before updating:
- [ ] Workflow - exists? needs update
- [ ] StandupConversation - exists?
- [ ] PortfolioOnboardingSession - exists?

---

## Phase 0.5-0.8: N/A

These phases do not apply:
- Phase 0.5 (Frontend-Backend Contract): No UI work
- Phase 0.6 (Data Flow): No multi-layer code
- Phase 0.7 (Conversation Design): No conversational feature
- Phase 0.8 (Post-Completion): No database/state changes

---

## Phase 1: Add New Terms

**Objective**: Add three new glossary entries in alphabetical order

**Tasks**:
1. [ ] Add **Guided Process** definition
2. [ ] Add **Process Registry** definition
3. [ ] Add **Process Type** definition

**Definitions** (from ADR-049 and implementation):

```markdown
### Guided Process
A multi-turn conversation where Piper maintains control until completion or exit.
Has defined states and transitions. Guided processes are checked BEFORE intent
classification to prevent derailment. Examples: portfolio onboarding, standup,
planning (future), feedback (future). See ADR-049.

### Process Registry
The singleton system that tracks active guided processes per session. Located at
`services/process/registry.py`. Checks all registered processes in priority order
before intent classification. See ADR-049.

### Process Type
A category of guided process with its own state machine and handler. Defined in
`ProcessType` enum. Current types: ONBOARDING, STANDUP. Future (Advanced Layer):
PLANNING, FEEDBACK, CLARIFICATION. See ADR-049, #698, #699, #700.
```

**Deliverable**: 3 new entries added

---

## Phase 2: Clarify Existing Terms

**Objective**: Update related terms to reference Guided Process pattern

**Tasks**:
1. [ ] Clarify **Workflow** - distinguish from Guided Process
2. [ ] Update **StandupConversation** - add "See also: Guided Process"
3. [ ] Update **PortfolioOnboardingSession** - add "See also: Guided Process"

**Clarifications**:

```markdown
### Workflow (clarification to add)
Note: Workflows are distinct from Guided Processes. Workflows are sequences of
steps Piper executes (may be non-interactive). Guided Processes are interactive
multi-turn conversations with user participation. See: Guided Process.

### StandupConversation (addition)
[existing content]
This is a type of Guided Process. See: Guided Process, Process Registry.

### PortfolioOnboardingSession (addition)
[existing content]
This is a type of Guided Process. See: Guided Process, Process Registry.
```

**Deliverable**: 3 existing entries clarified

---

## Phase 3: Validation

**Objective**: Ensure quality and consistency

**Tasks**:
1. [ ] Proofread all changes for spelling/grammar
2. [ ] Verify alphabetical ordering maintained
3. [ ] Cross-check definitions against ADR-049
4. [ ] Verify code references are accurate (`services/process/`)

**Deliverable**: Error-free, consistent glossary update

---

## Verification Gates

- [ ] Phase 1 complete: 3 new terms added
- [ ] Phase 2 complete: 3 existing terms updated
- [ ] Phase 3 complete: Proofread with zero errors
- [ ] Evidence: `git diff` of glossary changes

---

## Phase Z: Completion

**Tasks**:
1. [ ] Update #701 completion matrix
2. [ ] Add evidence (diff of changes)
3. [ ] Update session log
4. [ ] Request PM review

---

## Agent Deployment

**Agent Type**: Haiku (simple documentation task)
**Estimated Time**: 15 minutes
**Supervision**: Minimal - clear instructions, bounded scope

---

## STOP Conditions

- Glossary file structure changed unexpectedly
- Existing term definitions conflict with proposed changes
- ADR-049 wording differs significantly from planned definitions

---

## Success Criteria

- [ ] 3 new terms added (Guided Process, Process Registry, Process Type)
- [ ] 3 existing terms updated (Workflow, StandupConversation, PortfolioOnboardingSession)
- [ ] No spelling/grammar errors
- [ ] Alphabetical order maintained
- [ ] Consistent with ADR-049
- [ ] Session log updated

---

*Gameplan ready for audit against template.*
