# Agent Prompt: MUX-405 Phase Z (Integration)

## Your Identity
You are Claude Code, a development agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #405 MUX-VISION-METAPHORS
- **Epic**: MUX-VISION (#401)
- **Gameplan**: `dev/2026/01/20/gameplan-mux-405.md`
- **Prerequisite**: Phases 0-2 complete

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. STOP - Do not continue working
2. REPORT - Summarize what was just completed
3. ASK - "Should I proceed to next task?"
4. WAIT - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase Z (final phase) of issue #405.

### Your Acceptance Criteria
- [ ] ADR-045 updated with ownership-metaphors.md reference
- [ ] ADR-055 updated with ownership-metaphors.md reference
- [ ] Experience tests updated with metaphor criteria
- [ ] Onboarding checklist updated to include metaphor reading
- [ ] All cross-references verified
- [ ] Issue #405 ready for PM closure

### Evidence You MUST Provide
1. **ADR updates**: Show diffs or key additions
2. **Experience tests update**: Show addition
3. **Onboarding update**: Show addition
4. **Completion matrix**: 6/6 = 100%

### Your Handoff Format
```
## MUX-405 Phase Z Completion Report
**Status**: Complete/Partial/Blocked

**ADR Updates**:
- ADR-045: [what was added]
- ADR-055: [what was added]

**Documentation Updates**:
- mux-experience-tests.md: [what was added]
- grammar-onboarding-checklist.md: [what was added]

**Completion Matrix**:
| Component | Status | Evidence |
|-----------|--------|----------|
| Ownership metaphor philosophy doc | ✅ | [path] |
| WHY explanation | ✅ | [section exists] |
| Decision tree | ✅ | [section exists] |
| Worked examples (3+) | ✅ | [count] |
| ADR cross-references | ✅ | [ADR-045, ADR-055] |
| Experience tests update | ✅ | [what added] |

**6/6 = 100% COMPLETE**

**Files Modified**:
- [list with what changed]

**Ready for PM Closure**: Yes

**Blockers** (if any):
- [description]
```

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

```bash
# Verify Phases 0-2 complete
ls -la docs/internal/architecture/current/ownership-metaphors.md
# Expected: File exists

# Verify ADR locations
ls -la docs/internal/architecture/current/adrs/adr-045-*.md
ls -la docs/internal/architecture/current/adrs/adr-055-*.md
# Expected: Both exist

# Verify experience tests exist
ls -la docs/internal/development/mux-experience-tests.md
# Expected: File exists

# Verify onboarding checklist exists
ls -la docs/internal/development/grammar-onboarding-checklist.md
# Expected: File exists
```

**If ANY verification fails**: STOP and report with evidence.

---

## Mission

**Phase Z**: Complete integration and cross-references

**Scope Boundaries**:
- This prompt covers ONLY: ADR updates, documentation cross-references
- NOT in scope: Creating metaphor content (Phases 1-2)
- This is the FINAL phase

---

## Context

- **GitHub Issue**: #405 MUX-VISION-METAPHORS
- **Current State**: Philosophy document complete
- **Target State**: Fully integrated documentation, ready for PM closure
- **Dependencies**: Phases 0-2 complete
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

### Step Z.1: Update ADR-045

Read current ADR-045:
```bash
cat docs/internal/architecture/current/adrs/adr-045-*.md
```

Add reference to ownership-metaphors.md in the ownership section (near the existing table):

```markdown
### Ownership Metaphors Deep Dive

For the complete philosophical foundation of Mind/Senses/Understanding:
- **Location**: `docs/internal/architecture/current/ownership-metaphors.md`
- **Content**: Why these metaphors, decision tree, worked examples
- **Purpose**: Helps developers correctly classify new information types

See the ownership metaphors document for:
- The cognitive rationale behind Mind/Senses/Understanding
- Decision tree for ownership classification
- Common mistakes to avoid
```

### Step Z.2: Update ADR-055

Read current ADR-055:
```bash
cat docs/internal/architecture/current/adrs/adr-055-*.md
```

Add reference in Developer Resources section:

```markdown
### Ownership Metaphors Philosophy

For understanding the Mind/Senses/Understanding metaphors:
- See: `docs/internal/architecture/current/ownership-metaphors.md`

This document explains:
- Why "Mind" not "Memory"
- Why "Senses" not "Inputs"
- Why "Understanding" not "Inference"
- Decision tree for classification
- Worked examples with code patterns
```

### Step Z.3: Update Experience Tests

Read current experience tests:
```bash
cat docs/internal/development/mux-experience-tests.md
```

Find the "Ownership Tests" section (around line 120) and add metaphor-specific criteria:

```markdown
### Ownership Metaphor Tests (3 tests)
Verify that ownership uses consciousness metaphors correctly.

**Pass criteria:**
- Native uses "Mind" metaphor in experience language
- Federated uses "Senses" metaphor in experience language
- Synthetic uses "Understanding" metaphor in experience language
- Classification follows decision tree from ownership-metaphors.md

**Fail indicators:**
- Generic ownership labels without metaphor connection
- Wrong category for information type
- Missing provenance for Synthetic
- Stale confidence for Federated
```

### Step Z.4: Update Onboarding Checklist

Read current checklist:
```bash
cat docs/internal/development/grammar-onboarding-checklist.md
```

Add ownership metaphors to required reading (after consciousness philosophy):

```markdown
### 1.5. Understand Ownership Metaphors
- [ ] Read Ownership Metaphors (`docs/internal/architecture/current/ownership-metaphors.md`)
- [ ] Understand why Mind/Senses/Understanding (not Memory/Inputs/Inference)
- [ ] Can use decision tree to classify new information
- [ ] Can explain confidence differences between categories
```

### Step Z.5: Verify All Cross-References

```bash
# Check metaphors doc references correct files
grep -o "docs/internal[^)]*" docs/internal/architecture/current/ownership-metaphors.md | while read path; do
  if [ -f "$path" ]; then
    echo "✅ $path"
  else
    echo "❌ MISSING: $path"
  fi
done

# Check ADRs reference metaphors doc
grep "ownership-metaphors" docs/internal/architecture/current/adrs/*.md

# Check experience tests reference metaphors
grep -i "metaphor" docs/internal/development/mux-experience-tests.md

# Check onboarding references metaphors
grep "ownership-metaphors" docs/internal/development/grammar-onboarding-checklist.md
```

### Step Z.6: Verify Completion Matrix

Verify all 6 deliverables:

| Component | Status | Evidence |
|-----------|--------|----------|
| Ownership metaphor philosophy doc | ? | `ownership-metaphors.md` exists |
| WHY explanation | ? | Part 1 of doc |
| Decision tree | ? | Part 4 of doc |
| Worked examples (3+) | ? | Part 5 of doc (count) |
| ADR cross-references | ? | ADR-045, ADR-055 updated |
| Experience tests update | ? | Metaphor tests added |

---

## Success Criteria

- [ ] Infrastructure verified (Phases 0-2 complete)
- [ ] ADR-045 updated with metaphors reference
- [ ] ADR-055 updated with metaphors reference
- [ ] Experience tests include metaphor criteria
- [ ] Onboarding checklist includes metaphors reading
- [ ] All cross-references verified
- [ ] Completion matrix shows 6/6 = 100%
- [ ] Ready for PM closure

---

## STOP Conditions

Stop and escalate if:
- Philosophy document missing
- ADR files can't be updated
- Cross-references broken and unfixable

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Did I verify Phases 0-2 are complete?
2. Did I update ADR-045 with metaphors reference?
3. Did I update ADR-055 with metaphors reference?
4. Did I update the experience tests?
5. Did I update the onboarding checklist?
6. Are all cross-references working?
7. Is the completion matrix 6/6 = 100%?
8. Is issue #405 ready for PM closure?
9. Did I provide handoff in the required format?

---

## Deliverables

1. **Session log**: Append to existing
2. **ADR-045**: Updated with metaphors reference
3. **ADR-055**: Updated with metaphors reference
4. **Experience tests**: Updated with metaphor criteria
5. **Onboarding checklist**: Updated
6. **Final handoff report**: Completion status with 6/6 matrix

---

## Final Note

This is the completion phase. After this:
- Issue #405 should be ready for PM review and closure
- Ownership metaphors should be connected to all related docs
- Developer journey should include metaphors after consciousness philosophy

**Remember**: PM closes issues after approval. Provide evidence, request review.

---

*Prompt Version: Based on template v10.2*
*Created: 2026-01-20*
*Issue: #405 Phase Z*
