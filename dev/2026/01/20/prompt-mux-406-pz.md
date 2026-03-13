# Agent Prompt: MUX-406 Phase Z (Integration)

## Your Identity
You are Claude Code, a development agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #406 MUX-VISION-FEATURE-MAP
- **Epic**: MUX-VISION (#401)
- **Gameplan**: `dev/2026/01/20/gameplan-mux-406.md`
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

You are being deployed to complete Phase Z (final phase) of issue #406.

### Your Acceptance Criteria
- [ ] Cross-reference to transformation guide added
- [ ] Cross-reference to grammar compliance audit added
- [ ] ADR-055 Developer Resources updated
- [ ] Document verified complete (16/16 features)
- [ ] Issue #406 ready for PM closure

### Evidence You MUST Provide
1. **Cross-references**: Show additions
2. **Feature count**: 16/16 verified
3. **Completion matrix**: 6/6 = 100%

### Your Handoff Format
```
## MUX-406 Phase Z Completion Report
**Status**: Complete

**Cross-References Added**:
- grammar-transformation-guide.md: [reference added]
- grammar-compliance-audit.md: [reference added]
- ADR-055: [reference added]

**Document Verification**:
- Features mapped: 16/16
- Line count: X lines
- All sections populated: Yes

**Completion Matrix**:
| Component | Status | Evidence |
|-----------|--------|----------|
| Feature mapping document | ✅ | [line count] |
| Per-feature template | ✅ | Used for all 16 |
| Entity/Moment/Place IDs | ✅ | All 16 have mapping |
| Lens annotations | ✅ | All 16 have lenses |
| Ownership classification | ✅ | All 16 have N/F/S |
| Canonical query tagging | ✅ | [query count] tagged |

**6/6 = 100% COMPLETE**

**Ready for PM Closure**: Yes

**Blockers** (if any):
- [description]
```

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

```bash
# Verify Phases 0-2 complete (document populated)
ls -la docs/internal/architecture/current/feature-object-model-map.md
wc -l docs/internal/architecture/current/feature-object-model-map.md
# Expected: File exists, substantial content

# Verify related docs exist
ls -la docs/internal/development/grammar-transformation-guide.md
ls -la docs/internal/architecture/current/grammar-compliance-audit.md
ls -la docs/internal/architecture/current/adrs/adr-055-*.md
```

**If ANY verification fails**: STOP and report with evidence.

---

## Mission

**Phase Z**: Complete integration and cross-references

**Scope Boundaries**:
- This prompt covers ONLY: Cross-references, verification
- NOT in scope: Feature mapping content (Phases 1-2)
- This is the FINAL phase

---

## Context

- **GitHub Issue**: #406 MUX-VISION-FEATURE-MAP
- **Current State**: All 16 features mapped
- **Target State**: Fully integrated, ready for closure
- **Dependencies**: Phases 0-2 complete

---

## Session Log Management

```bash
ls -la dev/2026/01/20/*-lead-code-opus-log.md
# If log exists: APPEND to it, don't create new
```

---

## Implementation Approach

### Step Z.1: Add Cross-Reference to Transformation Guide

Read current guide:
```bash
cat docs/internal/development/grammar-transformation-guide.md | head -50
```

Add reference to feature map in appropriate section:

```markdown
## Feature Target States

For the target state of each feature (what it SHOULD look like after transformation):
- See: `docs/internal/architecture/current/feature-object-model-map.md`

This document shows:
- Current vs target state for all 16 features
- Entity/Moment/Place/Lenses/Ownership mappings
- Canonical query tagging (per CXO request)
```

### Step Z.2: Add Cross-Reference to Grammar Compliance Audit

Read current audit:
```bash
cat docs/internal/architecture/current/grammar-compliance-audit.md | head -50
```

Add reference linking to feature map:

```markdown
## Related Documentation

For detailed feature mappings showing target state:
- See: `docs/internal/architecture/current/feature-object-model-map.md`
```

### Step Z.3: Update ADR-055 Developer Resources

Read current ADR-055:
```bash
grep -A 20 "Developer Resources\|Related Documentation" docs/internal/architecture/current/adrs/adr-055-*.md
```

Add feature map reference:

```markdown
### Feature Object Model Map

For how each feature maps to Entity/Moment/Place/Lenses/Ownership:
- See: `docs/internal/architecture/current/feature-object-model-map.md`

This document supports MUX-GATE-3: "Existing features mapped to object model"
```

### Step Z.4: Verify Document Completeness

```bash
# Count features mapped
grep -c "^## [0-9]" docs/internal/architecture/current/feature-object-model-map.md
# Expected: 16

# Verify key sections exist
grep -E "Entity|Moment|Place|Lenses|Ownership" docs/internal/architecture/current/feature-object-model-map.md | wc -l
# Expected: Multiple per feature

# Verify canonical queries tagged
grep -c "Substrate" docs/internal/architecture/current/feature-object-model-map.md
# Expected: 16+ (one table per feature)
```

### Step Z.5: Verify All Cross-References

```bash
# Check transformation guide references feature map
grep "feature-object-model-map" docs/internal/development/grammar-transformation-guide.md

# Check audit references feature map
grep "feature-object-model-map" docs/internal/architecture/current/grammar-compliance-audit.md

# Check ADR-055 references feature map
grep "feature-object-model-map" docs/internal/architecture/current/adrs/adr-055-*.md
```

---

## Success Criteria

- [ ] Infrastructure verified (Phases 0-2 complete)
- [ ] Transformation guide cross-reference added
- [ ] Grammar audit cross-reference added
- [ ] ADR-055 cross-reference added
- [ ] 16/16 features verified mapped
- [ ] Completion matrix 6/6 = 100%
- [ ] Ready for PM closure

---

## STOP Conditions

Stop and escalate if:
- Feature map document incomplete
- Can't add cross-references
- Feature count != 16

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Did I verify Phases 0-2 are complete?
2. Did I add transformation guide cross-reference?
3. Did I add grammar audit cross-reference?
4. Did I update ADR-055?
5. Are 16/16 features mapped?
6. Is completion matrix 6/6?
7. Is issue #406 ready for PM closure?
8. Did I provide handoff in required format?

---

## Deliverables

1. **Session log**: Append to existing
2. **Cross-references**: Added to 3 documents
3. **Final handoff report**: Completion status with 6/6 matrix

---

## Final Note

This is the completion phase. After this:
- Issue #406 should be ready for PM review and closure
- Feature map should support MUX-GATE-3
- Transformation issues (#619-627) have target state reference

**Remember**: PM closes issues after approval. Provide evidence, request review.

---

*Prompt Version: Based on template v10.2*
*Created: 2026-01-20*
*Issue: #406 Phase Z*
