# Agent Prompt: MUX-406 Phase 0 (Setup & Template)

## Your Identity
You are Claude Code (Haiku), a development agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #406 MUX-VISION-FEATURE-MAP
- **Epic**: MUX-VISION (#401)
- **Gameplan**: `dev/2026/01/20/gameplan-mux-406.md`
- **Prerequisite**: #404, #405 complete

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. STOP - Do not continue working
2. REPORT - Summarize what was just completed
3. ASK - "Should I proceed to next task?"
4. WAIT - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase 0 of issue #406. Your work creates the template and gathers the feature list.

### Your Acceptance Criteria
- [ ] Feature list extracted from grammar compliance audit (16 features)
- [ ] Per-feature mapping template created
- [ ] Document structure ready for Phase 1-2

### Evidence You MUST Provide
1. **Feature list**: All 16 features with compliance levels
2. **Template**: Mapping template format
3. **Document skeleton**: Initial structure created

### Your Handoff Format
```
## MUX-406 Phase 0 Completion Report
**Status**: Complete

**Feature List** (from grammar-compliance-audit.md):
1. Morning Standup - Conscious (Reference)
2. Intent Classification - Partial
3. [etc...]

**Mapping Template**:
[show template structure]

**Document Created**: docs/internal/architecture/current/feature-object-model-map.md
- Initial structure with template
- Ready for Phase 1-2 to populate

**Blockers** (if any):
- [description]
```

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

```bash
# Verify grammar compliance audit exists
ls -la docs/internal/architecture/current/grammar-compliance-audit.md
# Expected: File exists

# Verify ownership metaphors exists
ls -la docs/internal/architecture/current/ownership-metaphors.md
# Expected: File exists

# Verify MUX implementation guide exists
ls -la docs/internal/development/mux-implementation-guide.md
# Expected: File exists

# Verify prerequisites complete
gh issue view 404 --json state -q '.state'
gh issue view 405 --json state -q '.state'
# Expected: Both CLOSED
```

**If ANY verification fails**: STOP and report with evidence.

---

## Mission

**Phase 0**: Create mapping template and gather feature list

**Scope Boundaries**:
- This prompt covers ONLY: Template creation and setup
- NOT in scope: Actual feature mapping (Phases 1-2)
- Separate prompts handle: Reference mapping, bulk mapping, integration

---

## Context

- **GitHub Issue**: #406 MUX-VISION-FEATURE-MAP
- **Current State**: Prerequisites complete, no mapping document
- **Target State**: Document structure ready for mapping
- **Dependencies**: #404 (audit), #405 (metaphors)

---

## Session Log Management

**IMPORTANT**: Check for existing log before creating new one!

```bash
ls -la dev/2026/01/20/*-lead-code-opus-log.md
# If log exists: APPEND to it, don't create new
```

---

## Implementation Approach

### Step 0.1: Extract Feature List

Read grammar compliance audit:
```bash
cat docs/internal/architecture/current/grammar-compliance-audit.md | grep -A 20 "Feature Compliance Matrix"
```

Extract all 16 features with their compliance levels.

### Step 0.2: Read MUX Grammar Elements

Read implementation guide for grammar elements:
```bash
cat docs/internal/development/mux-implementation-guide.md | head -100
```

Note: Entity, Moment, Place, Lenses, Ownership elements.

### Step 0.3: Create Mapping Template

Design per-feature template:

```markdown
## Feature: [Name]

**File**: `[path]`
**Compliance**: [Conscious/Partial/Flattened]
**Priority**: [Reference/High/Medium/Low]

### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | [who/what actors] | [target] |
| **Moment** | [what occurrences] | [target] |
| **Place** | [where/context] | [target] |
| **Lenses** | [which apply] | [target] |
| **Ownership** | [N/F/S classification] | [target] |

### Canonical Queries

| Query Example | Substrate | Lenses | Ownership |
|---------------|-----------|--------|-----------|
| [query] | Entity/Moment/Place | [list] | N/F/S |

### Transformation Notes
- [what needs to change]
- [see grammar-transformation-guide.md section X]

---
```

### Step 0.4: Create Document Structure

Create `docs/internal/architecture/current/feature-object-model-map.md`:

```markdown
# Feature Object Model Map

## Purpose

This document maps all 16 Piper Morgan features to the MUX object model grammar:
**"Entities experience Moments in Places"**

Each feature is mapped to show:
- Current state (how it works now)
- Target state (how it SHOULD work per grammar)
- Canonical queries with lens/substrate tagging (per CXO request)

---

## How to Use This Document

1. **Transforming a feature?** Find its section, review target state
2. **Adding a new feature?** Use the template to ensure grammar compliance
3. **Reviewing a PR?** Check if changes maintain or improve compliance

---

## Feature Summary

| # | Feature | Compliance | Priority |
|---|---------|------------|----------|
| 1 | Morning Standup | Conscious | Reference |
| 2 | Intent Classification | Partial | High |
| [etc...] |

---

## Reference Implementation

[Phase 1 will populate Morning Standup]

---

## Feature Mappings

[Phase 2 will populate remaining 15 features]

---

## Related Documentation

- Grammar Compliance Audit: `grammar-compliance-audit.md`
- MUX Implementation Guide: `mux-implementation-guide.md`
- Ownership Metaphors: `ownership-metaphors.md`
- Grammar Transformation Guide: `grammar-transformation-guide.md`
- Consciousness Philosophy: `consciousness-philosophy.md`

---

*Document created: 2026-01-20*
*Issue: #406 MUX-VISION-FEATURE-MAP*
```

---

## Success Criteria

- [ ] Infrastructure verified (prerequisites complete)
- [ ] All 16 features extracted from audit
- [ ] Mapping template created
- [ ] Document skeleton created at correct path
- [ ] Ready for Phase 1-2 to populate

---

## STOP Conditions

Stop and escalate if:
- Grammar compliance audit missing
- Feature list unclear
- Can't determine template structure

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Did I verify infrastructure first?
2. Did I extract all 16 features?
3. Did I create a mapping template?
4. Did I create the document skeleton?
5. Is the document ready for Phase 1-2?
6. Did I provide handoff in required format?

---

## Deliverables

1. **Session log**: Append to existing
2. **Feature list**: All 16 features with compliance
3. **Document skeleton**: `feature-object-model-map.md`

---

*Prompt Version: Based on template v10.2*
*Created: 2026-01-20*
*Issue: #406 Phase 0*
