# Agent Prompt: #701 DOCS-GLOSSARY-GUIDED-PROCESS

## Your Identity
You are a Haiku agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

---

## Mission
Update the glossary (`knowledge/piper-morgan-glossary-v1.1.md`) with Guided Process terminology. This is a documentation-only task with no code changes.

**Scope Boundaries**:
- This prompt covers ONLY: Glossary file edits
- NOT in scope: Code changes, ADR edits, test changes
- Source of truth: ADR-049 (ACCEPTED)

---

## Context
- **GitHub Issue**: #701 - DOCS-GLOSSARY-GUIDED-PROCESS
- **Current State**: Glossary exists but lacks Guided Process terminology
- **Target State**: 3 new terms added, 3 existing terms clarified
- **Dependencies**: ADR-049 (ACCEPTED), `services/process/` (implemented)
- **User Data Risk**: None (documentation only)
- **Infrastructure Verified**: Yes - glossary file exists

---

## Phase 0: Verification (STOP if any fail)

```bash
# 1. Verify glossary file exists
ls -la knowledge/piper-morgan-glossary-v1.1.md

# 2. Verify ADR-049 is ACCEPTED (source of definitions)
grep -i "status" docs/internal/architecture/current/adrs/adr-049-*.md | head -1

# 3. Check existing terms to update
grep -i "workflow\|standup\|onboarding" knowledge/piper-morgan-glossary-v1.1.md
```

**STOP if**:
- [ ] Glossary file doesn't exist
- [ ] ADR-049 is not ACCEPTED
- [ ] Existing terms not found where expected

---

## Implementation Steps

### Step 1: Add New Terms (in alphabetical order)

Add these three new glossary entries:

#### Guided Process
```markdown
### Guided Process
A multi-turn conversation where Piper maintains control until completion or exit.
Has defined states and transitions. Guided processes are checked BEFORE intent
classification to prevent derailment. Examples: portfolio onboarding, standup,
planning (future), feedback (future). See ADR-049.
```

#### Process Registry
```markdown
### Process Registry
The singleton system that tracks active guided processes per session. Located at
`services/process/registry.py`. Checks all registered processes in priority order
before intent classification. See ADR-049.
```

#### Process Type
```markdown
### Process Type
A category of guided process with its own state machine and handler. Defined in
`ProcessType` enum. Current types: ONBOARDING, STANDUP. Future (Advanced Layer):
PLANNING, FEEDBACK, CLARIFICATION. See ADR-049, #698, #699, #700.
```

**Validation**: Verify terms inserted in correct alphabetical position.

### Step 2: Clarify Existing Terms

#### Workflow
Add clarification note:
```markdown
Note: Workflows are distinct from Guided Processes. Workflows are sequences of
steps Piper executes (may be non-interactive). Guided Processes are interactive
multi-turn conversations with user participation. See: Guided Process.
```

#### StandupConversation
Add to existing entry:
```markdown
This is a type of Guided Process. See: Guided Process, Process Registry.
```

#### PortfolioOnboardingSession
Add to existing entry:
```markdown
This is a type of Guided Process. See: Guided Process, Process Registry.
```

**Validation**: Verify existing definitions preserved and additions appended.

### Step 3: Proofread

1. [ ] Check spelling/grammar of all changes
2. [ ] Verify alphabetical ordering maintained
3. [ ] Cross-check definitions against ADR-049
4. [ ] Verify code references are accurate (`services/process/`)

---

## Success Criteria

- [ ] 3 new terms added (Guided Process, Process Registry, Process Type)
- [ ] 3 existing terms updated (Workflow, StandupConversation, PortfolioOnboardingSession)
- [ ] No spelling/grammar errors
- [ ] Alphabetical order maintained
- [ ] Consistent with ADR-049

---

## Evidence Requirements

Provide these in your completion report:
1. `git diff knowledge/piper-morgan-glossary-v1.1.md` showing all changes
2. Confirmation alphabetical order correct
3. Confirmation spelling/grammar checked

---

## Deliverables

1. **Modified file**: `knowledge/piper-morgan-glossary-v1.1.md`
2. **Evidence**: git diff of changes
3. **Validation**: Proofread confirmation

---

## Handoff Format

Return your work with this structure:
```
## Issue #701 Completion Report
**Status**: Complete/Partial/Blocked

**Changes Made**:
- [list of terms added/updated]

**Verification**:
[git diff output]

**Proofread Confirmation**:
- Spelling checked: Yes/No
- Grammar checked: Yes/No
- Alphabetical order verified: Yes/No
- ADR-049 consistency verified: Yes/No

**Blockers** (if any):
- [description]
```

---

## STOP Conditions

- Glossary file structure changed unexpectedly
- Existing term definitions conflict with proposed changes
- ADR-049 wording differs significantly from planned definitions
- Cannot verify alphabetical positioning

---

*Prompt Version: 1.0*
*Task: Documentation update (no code)*
*Estimated Effort: Small*
