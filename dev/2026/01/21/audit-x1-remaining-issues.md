# Audit: X1 Sprint Remaining Issues (#435, #568, #595)

**Date**: 2026-01-21 7:25 AM
**Auditor**: Lead Developer (Claude Code Opus)

---

## Executive Summary

| Issue | Title | Original Est | V1 Overlap | Remaining Est | Priority |
|-------|-------|--------------|------------|---------------|----------|
| #435 | PHASE3-OWNERSHIP | 8h | **~95%** | **1-2h** | High |
| #568 | PORTFOLIO-ACROSS | Beta | N/A | **Defer** | Low |
| #595 | INTENT-MULTI bug | ? | 0% | **4-8h** | Medium |

**Key Finding**: #435 is almost entirely done. #568 should be deferred. #595 is real work.

---

## #435 MUX-TECH-PHASE3-OWNERSHIP

### What Already Exists

| Spec Requirement | Status | Evidence |
|------------------|--------|----------|
| OwnershipType enum (NATIVE/FEDERATED/SYNTHETIC) | ✅ **EXISTS** | `ownership.py:20` - OwnershipCategory |
| OwnershipMetadata | ✅ **EXISTS** | `ownership.py:118` - OwnershipResolution (confidence, reasoning, source) |
| Ownership transitions | ✅ **EXISTS** | `ownership.py:342` - OwnershipTransformation |
| Valid transformation paths | ✅ **EXISTS** | `ownership.py:321` - _VALID_TRANSFORMATIONS |
| Transformation descriptions | ✅ **EXISTS** | `ownership.py:329` - _TRANSFORMATION_DESCRIPTIONS |
| OwnershipResolver | ✅ **EXISTS** | `ownership.py:140` - Full resolver with determine/resolve |
| HasOwnership protocol | ✅ **EXISTS** | `ownership.py:74` - Runtime checkable protocol |
| Tests | ✅ **EXISTS** | 25 tests passing |

### What's Missing

| Spec Requirement | Status | Gap |
|------------------|--------|-----|
| Apply to ALL domain models | ❌ MISSING | No `ownership` field in domain models |
| OwnershipAwareRepository | ❌ MISSING | No repository pattern |

### Assessment

**#435 is ~95% complete.** The core ownership model, resolver, transitions, and tests all exist. The only gaps are:

1. **Domain model integration**: Add `ownership: Optional[OwnershipResolution]` to domain models (same pattern as #433 lifecycle integration)
2. **OwnershipAwareRepository**: Optional - could be deferred as it's a query pattern, not core model

### Recommended Action

**Close #435 with minimal work:**
- Add ownership field to 2-3 key domain models (similar to #433)
- Create 4-6 integration tests
- Estimated: **1-2 hours**

---

## #568 MUX-CORE-PORTFOLIO-ACROSS

### Issue Analysis

```
Description: Enable sharing portfolio information across different channels
Deferred From: MVP phase of #314
Priority: Beta feature - not blocking MVP
```

### Assessment

This is explicitly marked as a **Beta feature** deferred from MVP. The acceptance criteria are:
- Portfolio data persists across channels
- User can reference portfolio in different contexts
- Consistent portfolio state across all touchpoints

This requires **cross-channel infrastructure** that doesn't exist yet.

### Recommended Action

**Defer from X1 sprint.** This issue should not be part of MUX-GATE-2:
1. It's labeled "Beta feature - not blocking MVP"
2. It requires infrastructure that doesn't exist
3. It's not part of the core MUX technical foundation

**Suggest**: Move to a future sprint or close as "won't fix for X1"

---

## #595 MUX-INTENT-MULTI Bug

### Bug Summary

**Problem**: "Hi Piper! What's on my agenda for tomorrow?" only handles the greeting, ignoring the calendar query.

**Root Cause** (per issue):
1. Intent classifier returns single intent, not multiple
2. No logic to handle compound messages
3. Greeting patterns match first, stopping further classification

### Technical Analysis

The intent service (`services/intent/intent_service.py` - 319KB!) has a single-intent architecture. The fix options are:

1. **Pre-MUX workaround**: Strip greetings before classification (fragile)
2. **Multi-intent parsing**: Detect and handle multiple intents
3. **LLM layer handling**: Let MUX/LLM handle compound messages

### Assessment

This is **real bug work** that requires changes to the intent classification system. It's not about implementing new MUX models - it's about fixing existing behavior.

**Complexity factors**:
- Large file (319KB intent_service.py)
- May require architectural changes for multi-intent
- Need to avoid breaking existing intent handling

### Recommended Action

**Include in X1 but scope carefully:**
- Phase 1: Investigate current intent flow (2h)
- Phase 2: Implement greeting stripping OR multi-intent (4-6h)
- Test: Verify both greeting and query handled

**Estimated**: 4-8 hours

**Alternative**: If MUX LLM layer would handle this naturally, could defer to that implementation.

---

## Revised X1 Sprint Scope

| Issue | Status | Action | Est Hours |
|-------|--------|--------|-----------|
| #433 | ✅ CLOSED | Done | 0 |
| #434 | ✅ Audited | Execute | 16h |
| #435 | ✅ Audited | Execute (minimal) | 2h |
| #568 | ✅ Audited | **Defer/Remove** | 0 |
| #595 | ✅ Audited | Execute | 6h |
| #532 | Gate | Verify all above | 1h |

**Total remaining**: ~25 hours (vs original ~40h estimate)

---

## PM Decision Points

1. **#568**: Remove from X1 sprint? (Recommended: Yes)
2. **#595**: Include in X1 or defer to LLM layer work?
3. **Execution order**: #434 → #435 → #595 → #532?

---

*Audit complete: 2026-01-21 7:25 AM*
