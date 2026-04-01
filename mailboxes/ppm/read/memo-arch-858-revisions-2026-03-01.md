# Memo: #858 Spec Revision Requests — v1.0 → v1.1

**From**: Chief Architect
**To**: Lead Developer
**CC**: PM, PPM
**Date**: March 1, 2026
**Re**: Approved with revisions — Conversation Lifecycle Specification

---

## Status

**Architect**: ✅ APPROVED with revisions
**PPM**: ✅ APPROVED with minor notes
**ADR-050 Compatibility**: ✅ Verified (Section 2.4 explicitly addresses)

The spec is architecturally sound and ready for implementation after the following clarifications are added.

---

## Required Revisions for v1.1

### R1: COMPOSTED Content Retention

**Location**: Section 2.1 or 2.3 (near COMPOSTED definition)

**Add**:
> "COMPOSTED conversations retain their original content in the database but are no longer directly accessible to users. The content is available for Piper's cross-session memory synthesis (ADR-054 Layer 3) but not surfaced in sidebars or search. Actual content deletion after distillation is a future policy decision, not part of MVP."

**Rationale**: Clarifies that COMPOSTED ≠ deleted. Avoids building deletion infrastructure before the learning system is mature.

---

### R2: Composting Period Default

**Location**: Section 2.3 (ARCHIVED → COMPOSTED transition)

**Change**:
- Old: "configurable period (default: 30 days)"
- New: "configurable period (default: 90 days)"

**Rationale**: PPM recommendation. 90 days is more generous and reduces user anxiety about conversations disappearing.

---

### R3: Composting Period Configuration Location

**Location**: Section 2.3 or new subsection

**Add**:
> "The composting period is configured at the system level (environment variable `PIPER_COMPOSTING_DAYS` or `config/piper.user.md`). Per-user configuration is a future enhancement."

**Rationale**: Specifies where the "configurable" configuration lives. System-level is appropriate for alpha.

---

### R4: COMPOSTED Visibility

**Location**: Section 2.2 (User-Visible States table) or Section 5

**Add**:
> "COMPOSTED conversations are not visible in either sidebar and do not appear in search results. Users who need to review old conversations should do so before the composting period elapses. Composted content influences Piper's responses through the memory system but is not directly browsable."

**Rationale**: Explicitly states that COMPOSTED = truly invisible for MVP. Avoids scope creep into "show composted" UI.

---

## Optional Enhancement (Non-Blocking)

### S1: State Transition Timestamp

**Consideration**: Add `state_changed_at` field to track when lifecycle transitions occurred.

**Rationale**: Useful for debugging and future analytics. Can be deferred to M2 if it complicates migration.

---

## Summary of Changes

| Section | Change |
|---------|--------|
| 2.1 or 2.3 | Add COMPOSTED content retention clarification |
| 2.3 | Change default 30 → 90 days |
| 2.3 | Add configuration location |
| 2.2 or 5 | Add COMPOSTED visibility statement |

**Estimated revision effort**: 15-30 minutes (four sentences added, one number changed)

---

## Next Steps

1. Lead Dev revises spec → v1.1
2. PM confirms revisions
3. Proceed to #715 implementation

---

*Architect review complete. Spec is approved pending these minor clarifications.*
