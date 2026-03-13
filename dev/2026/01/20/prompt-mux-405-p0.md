# Agent Prompt: MUX-405 Phase 0 (Source Material Gathering)

## Your Identity
You are Claude Code (Haiku), a development agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #405 MUX-VISION-METAPHORS
- **Epic**: MUX-VISION (#401)
- **Gameplan**: `dev/2026/01/20/gameplan-mux-405.md`
- **Prerequisite**: #399, #400, #404 complete

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. STOP - Do not continue working
2. REPORT - Summarize what was just completed
3. ASK - "Should I proceed to next task?"
4. WAIT - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase 0 of issue #405. Your work gathers source material for the philosophy document.

### Your Acceptance Criteria
- [ ] Ownership code reviewed and key concepts extracted
- [ ] Ownership tests reviewed for examples
- [ ] ADR-045 ownership section reviewed
- [ ] CXO origin materials located (if they exist)
- [ ] Source material summary created

### Evidence You MUST Provide
1. **Code concepts**: Key classes, enums, methods from ownership.py
2. **Test examples**: Representative test cases showing usage
3. **ADR content**: What ADR-045 says about ownership
4. **Origin notes**: Any CXO sketches or origin documents

### Your Handoff Format
```
## MUX-405 Phase 0 Completion Report
**Status**: Complete/Partial/Blocked

**Source Material Summary**:

### From ownership.py
- OwnershipCategory enum values: [list]
- Key classes: [list]
- Metaphor mapping found: [yes/no, details]

### From ownership tests
- Number of tests: [count]
- Example patterns:
  - Native example: [description]
  - Federated example: [description]
  - Synthetic example: [description]

### From ADR-045
- Ownership table content: [summary]
- Metaphor explanations: [what exists]

### From CXO/Origin Materials
- Found: [yes/no]
- Location: [path if found]
- Key insights: [summary]

**Gaps Identified**:
- [what's missing that Phase 1-2 must create]

**Blockers** (if any):
- [description]
```

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

```bash
# Verify ownership code exists
ls -la services/mux/ownership.py
# Expected: File exists

# Verify ownership tests exist
ls -la tests/unit/services/mux/test_ownership.py
# Expected: File exists

# Verify ADR-045 exists
ls -la docs/internal/architecture/current/adrs/adr-045-*.md
# Expected: File exists

# Verify prerequisites complete
gh issue view 399 --json state -q '.state'
gh issue view 400 --json state -q '.state'
gh issue view 404 --json state -q '.state'
# Expected: All CLOSED
```

**If ANY verification fails**: STOP and report with evidence.

---

## Mission

**Phase 0**: Gather source material for ownership metaphor philosophy document

**Scope Boundaries**:
- This prompt covers ONLY: Reading and summarizing existing materials
- NOT in scope: Writing the philosophy document (Phase 1-2)
- Separate prompts handle: Philosophy creation, integration

---

## Context

- **GitHub Issue**: #405 MUX-VISION-METAPHORS
- **Current State**: Issue described, gameplan created
- **Target State**: Source materials gathered for Phase 1-2
- **Dependencies**: #399, #400, #404 complete
- **Infrastructure Verified**: Yes

---

## Session Log Management

**IMPORTANT**: Check for existing log before creating new one!

```bash
# Check if log exists today
ls -la dev/2026/01/20/*-lead-code-opus-log.md

# If log exists: APPEND to it, don't create new
```

---

## Implementation Approach

### Step 0.1: Read Ownership Code

```bash
cat services/mux/ownership.py
```

Extract:
- OwnershipCategory enum values
- Class definitions
- Metaphor mappings (Mind/Senses/Understanding)
- Any docstrings explaining WHY

### Step 0.2: Read Ownership Tests

```bash
cat tests/unit/services/mux/test_ownership.py
```

Extract:
- Test count
- Example of Native/Mind usage
- Example of Federated/Senses usage
- Example of Synthetic/Understanding usage

### Step 0.3: Read ADR-045 Ownership Section

```bash
grep -A 20 "ownership\|Ownership\|NATIVE\|Native" docs/internal/architecture/current/adrs/adr-045-*.md
```

Extract:
- Ownership table content
- Any narrative about WHY these metaphors

### Step 0.4: Search for CXO Origin Materials

```bash
# Search for CXO sketches mentioning mind/senses
grep -r -i "cxo.*mind\|cxo.*senses\|mind.*senses.*understanding" docs/ --include="*.md"
grep -r "Piper's Mind\|Piper's Senses\|Piper's Understanding" docs/ --include="*.md"
```

Document what exists and where.

### Step 0.5: Create Source Material Summary

Compile findings into handoff format showing:
- What exists (with quotes/references)
- What gaps need filling in Phase 1-2

---

## Success Criteria

- [ ] Infrastructure verified (prerequisites complete)
- [ ] Ownership code read and concepts extracted
- [ ] Ownership tests reviewed for examples
- [ ] ADR-045 content summarized
- [ ] CXO materials search completed
- [ ] Gaps identified for Phase 1-2
- [ ] Handoff report in required format

---

## STOP Conditions

Stop and escalate if:
- Prerequisites not complete (#399, #400, #404)
- Ownership code doesn't have Mind/Senses/Understanding mapping
- Can't locate ADR-045

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Did I verify infrastructure first?
2. Did I read the full ownership.py file?
3. Did I find examples of all 3 ownership types in tests?
4. Did I extract the ADR-045 ownership content?
5. Did I search for CXO origin materials?
6. Did I identify gaps for Phase 1-2?
7. Did I provide handoff in required format?

---

## Deliverables

1. **Session log**: Append to existing
2. **Source material summary**: In handoff format
3. **Gap analysis**: What Phase 1-2 must create

---

*Prompt Version: Based on template v10.2*
*Created: 2026-01-20*
*Issue: #405 Phase 0*
