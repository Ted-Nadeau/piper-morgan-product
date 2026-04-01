# PPM Review: Conversation Lifecycle Spec (#858)

**From**: Principal Product Manager
**To**: Lead Developer
**CC**: CXO, PM
**Date**: March 1, 2026
**Re**: Review of Draft v1 — Conversation Lifecycle Specification

---

## Summary

**Recommendation: APPROVE with minor notes.**

This is a well-executed spec that thoroughly incorporates the CXO and PPM guidance from February 28. The Lead Dev has delivered exactly what we asked for — a specification that establishes invariants, preserves architectural intent, and provides implementation-ready test cases.

---

## Verification Against Guidance

### CXO Guidance (Feb 28) — All Addressed ✅

| CXO Requirement | Spec Section | Status |
|-----------------|--------------|--------|
| User-visible states simpler than internal | 2.2 | ✅ Clear table mapping internal → user-visible |
| Right sidebar = entity surface | P2, 5.2 | ✅ Explicit design principle + section |
| Naming by topic, not state | P4, T15-T16 | ✅ Principle + tests |
| New day = new conversation | 7.2 | ✅ Calendar day boundary, cleanly specified |
| Multi-entity compatible language | P3 | ✅ Table with avoid/use-instead pairs |
| Keep #715 in M2 | Appendix A | ✅ Sequencing confirmed: spec first, then implementation |

### PPM Guidance (Feb 28) — All Addressed ✅

| PPM Requirement | Spec Section | Status |
|-----------------|--------------|--------|
| Design Principles section | Section 1 | ✅ Six principles including anti-flattening checklist |
| Calendar day boundary (not 24-48 hours) | 7.2 | ✅ "After midnight (local time)" |
| "Continue yesterday" affordances | 7.2 | ✅ Options A, B, C all documented with sequencing |
| Anti-flattening checklist | P6 | ✅ Six-item checklist |
| Extensible boundaries | P5, 7.4 | ✅ Principle + explicit "branching and forking" section |
| 8-section structure | Sections 1-8 | ✅ Matches suggested outline |

---

## Strong Points

### 1. Design Principles Section

Section 1 establishes the "why" before the "what." This is exactly what prevents future implementers from flattening the design. P2 (Entity Surface, Not Conversation Archive) is the critical anti-flattening instruction, and it's prominent.

### 2. State Machine Simplicity

The four-state model (ACTIVE → ARCHIVED → COMPOSTED, with DELETED as terminal) is simple enough to understand and implement correctly. The distinction between internal states and user-visible states (Section 2.2) is clean.

### 3. Calendar Day Boundary

Section 7.2 specifies exactly what we asked for: "After midnight (local time), the next user interaction starts a new conversation." The 11:59 PM / 12:01 AM example makes the behavior unambiguous.

### 4. Continue Yesterday Options

All three options from the PPM memo are documented with appropriate sequencing:
- **Option A** (explicit sidebar action): MVP, available now
- **Option B** (Piper prompt): Future polish
- **Option C** (magic continuation): Already handled by M0 Conversational Glue

This preserves the architectural intent without over-engineering MVP.

### 5. Representation Inventory

Section 6 is exactly what we needed — an honest inventory of the three ConversationTurn representations and two ConversationContext classes, with clear mapping and *no premature unification*. The recommendation to rename rather than merge is correct.

### 6. Test Specifications

Section 8 provides 16 test specifications that translate directly to pytest. T14 (end-to-end) is particularly valuable — it exercises the complete lifecycle path in a single test.

---

## Minor Notes (Non-Blocking)

### 1. COMPOSTED Transition Timing

Section 2.3 specifies "configurable period (default: 30 days)" for ARCHIVED → COMPOSTED.

**Question**: Is 30 days the right default? This affects how long conversations remain searchable. I'd suggest 90 days as a more generous default, but this is a tunable parameter so it's not blocking.

### 2. API Naming for Entity Surface

Section 5.4 suggests `/api/v1/conversations?state=active,archived` for the right sidebar. Section 5.2 notes the sidebar will eventually surface other entity types.

**Consideration**: Should we spec `/api/v1/history` now as the future endpoint name, with `/api/v1/conversations` as the current implementation? This is forward-thinking but may be premature. Non-blocking — current spec is fine.

### 3. T14 Scope Note

T14 is comprehensive (7 steps). It might be worth noting this is the "happy path" integration test; edge cases are covered in T1-T13.

---

## Ready for Architect Review

With CXO and PPM aligned on this draft, the next step is Chief Architect review for technical feasibility and ADR-050 compatibility verification.

**Specifically, Architect should verify**:
- Domain model changes (Section 2.4) align with existing models.py structure
- Migration path (Appendix B) is sound
- API changes don't conflict with existing routes
- Test specifications are implementable with current test infrastructure

---

## Approval

**PPM Approval**: ✅ APPROVED

This spec establishes the foundation for #715 implementation. The Lead Dev has done excellent work translating product and experience guidance into a technical specification.

---

*PPM review of #858 Draft v1 — March 1, 2026*
