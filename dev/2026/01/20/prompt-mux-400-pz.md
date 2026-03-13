# Agent Prompt: MUX-400 Phase Z (Integration)

## Your Identity
You are Claude Code, a development agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #400 MUX-VISION-CONSCIOUSNESS
- **Epic**: MUX-VISION (#401)
- **Gameplan**: `dev/2026/01/20/gameplan-mux-400.md`
- **Prerequisite**: Phases 0-2 complete

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase Z (final phase) of issue #400.

### Your Acceptance Criteria
- [ ] ADR-045 updated with philosophy reference
- [ ] ADR-055 updated with philosophy reference
- [ ] Onboarding checklist updated to include philosophy
- [ ] Transformation guide updated to reference philosophy
- [ ] All cross-references verified
- [ ] Issue #400 ready for PM closure

### Evidence You MUST Provide
1. **ADR updates**: Show diffs or key additions
2. **Checklist update**: Show addition
3. **Guide update**: Show addition
4. **Completion matrix**: 4/4 = 100%

### Your Handoff Format
```
## MUX-400 Phase Z Completion Report
**Status**: Complete/Partial/Blocked

**ADR Updates**:
- ADR-045: [what was added]
- ADR-055: [what was added]

**Documentation Updates**:
- grammar-onboarding-checklist.md: [what was added]
- grammar-transformation-guide.md: [what was added]

**Completion Matrix**:
| Component | Status | Evidence |
|-----------|--------|----------|
| Vision archaeology | ✅ | [notes] |
| Five Pillars philosophy doc | ✅ | [path] |
| Soul preservation principles | ✅ | [in doc] |
| Cross-references updated | ✅ | [paths] |

**4/4 = 100% COMPLETE**

**Files Modified**:
- [list with what changed]

**Ready for PM Closure**: Yes

**Blockers** (if any):
- [description]
```

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

```bash
# Verify Phases 0-2 complete
ls -la docs/internal/architecture/current/consciousness-philosophy.md
# Expected: File exists

# Verify ADR locations
ls -la docs/internal/architecture/current/adrs/adr-045-*.md
ls -la docs/internal/architecture/current/adrs/adr-055-*.md
# Expected: Both exist

# Verify #404 docs exist (to update)
ls -la docs/internal/development/grammar-onboarding-checklist.md
ls -la docs/internal/development/grammar-transformation-guide.md
# Expected: Both exist
```

**If ANY verification fails**: STOP and report with evidence.

---

## Mission

**Phase Z**: Complete integration and cross-references

**Scope Boundaries**:
- This prompt covers ONLY: ADR updates, documentation cross-references
- NOT in scope: Creating philosophy content (Phases 1-2)
- This is the FINAL phase

---

## Context

- **GitHub Issue**: #400 MUX-VISION-CONSCIOUSNESS
- **Current State**: Philosophy document complete
- **Target State**: Fully integrated documentation, ready for PM closure
- **Dependencies**: Phases 0-2 complete
- **Infrastructure Verified**: Yes

---

## Session Log Management

**IMPORTANT**: Check for existing log before creating new one!

```bash
# Check if log exists today
ls -la dev/2026/01/20/*-prog-code-*-log.md

# If log exists: APPEND to it, don't create new
```

---

## Implementation Approach

### Step Z.1: Update ADR-045

Read current ADR-045:
```bash
cat docs/internal/architecture/current/adrs/adr-045-*.md
```

Add reference to philosophy document in appropriate section:

```markdown
## Consciousness Philosophy

The "why" behind the grammar is documented in the Consciousness Philosophy:
- **Location**: `docs/internal/architecture/current/consciousness-philosophy.md`
- **Content**: Five Pillars of Consciousness, Soul Preservation Principles
- **Purpose**: Ensures developers understand not just HOW but WHY

### The Five Pillars
1. Identity Awareness - Piper knows itself
2. Time Consciousness - Lived time, not clock time
3. Spatial Awareness - Digital spaces as places
4. Agency Recognition - Knows capabilities and limits
5. Predictive Modeling - Has premonitions and concerns

See the philosophy document for detailed guidance.
```

### Step Z.2: Update ADR-055

Read current ADR-055:
```bash
cat docs/internal/architecture/current/adrs/adr-055-*.md
```

Add reference in Developer Resources section (if it exists from #404) or create:

```markdown
## Consciousness Philosophy

For the philosophical foundation of WHY we preserve consciousness:
- See: `docs/internal/architecture/current/consciousness-philosophy.md`

This document explains:
- The Five Pillars of Consciousness
- Soul Preservation Principles
- Warning signs of flattening
- PR review consciousness checklist
```

### Step Z.3: Update Onboarding Checklist

Read current checklist:
```bash
cat docs/internal/development/grammar-onboarding-checklist.md
```

Add philosophy document to "Required Reading" section:

```markdown
### 0. Understand the Philosophy (NEW)
- [ ] Read Consciousness Philosophy (`docs/internal/architecture/current/consciousness-philosophy.md`)
- [ ] Understand the Five Pillars
- [ ] Review soul preservation principles
```

### Step Z.4: Update Transformation Guide

Read current guide:
```bash
cat docs/internal/development/grammar-transformation-guide.md
```

Add philosophy reference at the beginning:

```markdown
## Before You Begin

**Understand WHY before HOW**: Before transforming any feature, read the
Consciousness Philosophy (`docs/internal/architecture/current/consciousness-philosophy.md`)
to understand why we preserve consciousness.

The Five Pillars:
1. Identity Awareness
2. Time Consciousness
3. Spatial Awareness
4. Agency Recognition
5. Predictive Modeling

This guide shows HOW to transform. The philosophy explains WHY it matters.
```

### Step Z.5: Verify All Cross-References

```bash
# Check philosophy doc references correct files
grep -o "docs/internal[^)]*" docs/internal/architecture/current/consciousness-philosophy.md | while read path; do
  if [ -f "$path" ]; then
    echo "✅ $path"
  else
    echo "❌ MISSING: $path"
  fi
done

# Check ADRs reference philosophy
grep -l "consciousness-philosophy" docs/internal/architecture/current/adrs/*.md

# Check onboarding references philosophy
grep "consciousness-philosophy" docs/internal/development/grammar-onboarding-checklist.md

# Check guide references philosophy
grep "consciousness-philosophy" docs/internal/development/grammar-transformation-guide.md
```

### Step Z.6: Update Completion Matrix

Verify all 4 deliverables:

| Component | Status | Evidence |
|-----------|--------|----------|
| Vision archaeology | ? | Session log notes |
| Five Pillars philosophy doc | ? | `consciousness-philosophy.md` |
| Soul preservation principles | ? | Part 4-5 of philosophy doc |
| Cross-references updated | ? | ADR-045, ADR-055, checklist, guide |

---

## Success Criteria

- [ ] Infrastructure verified (Phases 0-2 complete)
- [ ] ADR-045 updated with philosophy reference
- [ ] ADR-055 updated with philosophy reference
- [ ] Onboarding checklist includes philosophy
- [ ] Transformation guide references philosophy
- [ ] All cross-references verified
- [ ] Completion matrix shows 4/4 = 100%
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
2. Did I update ADR-045 with philosophy reference?
3. Did I update ADR-055 with philosophy reference?
4. Did I update the onboarding checklist?
5. Did I update the transformation guide?
6. Are all cross-references working?
7. Is the completion matrix 4/4 = 100%?
8. Is issue #400 ready for PM closure?
9. Did I provide handoff in the required format?

---

## Deliverables

1. **Session log**: Append to existing
2. **ADR-045**: Updated with philosophy reference
3. **ADR-055**: Updated with philosophy reference
4. **Onboarding checklist**: Updated
5. **Transformation guide**: Updated
6. **Final handoff report**: Completion status with 4/4 matrix

---

## Final Note

This is the completion phase. After this:
- Issue #400 should be ready for PM review and closure
- Philosophy document should be connected to all related docs
- Developer journey should include philosophy as first step

**Remember**: PM closes issues after approval. Provide evidence, request review.

---

*Prompt Version: Based on template v10.2*
*Created: 2026-01-20*
*Issue: #400 Phase Z*
