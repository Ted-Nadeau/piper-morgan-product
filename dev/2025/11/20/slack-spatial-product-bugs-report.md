# Slack Spatial Integration - Product Code Bugs Report
**Date:** 2025-11-20 06:33 AM
**Session:** Test Suite Cleanup - P0 Quick Wins
**Prepared for:** Chief Architect & QA Lead

## Executive Summary

During P0 test cleanup, we fixed 13/13 tests in `test_event_spatial_mapping.py` but uncovered **8 product code bugs** in the webhook and OAuth integration layers. These are blocking 8 tests across 2 test files.

**Impact:**
- Webhook signature verification broken (security concern)
- OAuth spatial integration incomplete (4 flows broken)
- Estimated **4-6 hours** to fix all issues

---

## Bug #1: Webhook Signature Verification - Method Signature Mismatch 🔴 CRITICAL

**Priority:** P0 (Security)
**File:** `services/integrations/slack/webhook_router.py:233`
**Test:** `test_ngrok_webhook_flow.py::test_webhook_signature_verification`

### Problem
```python
# Line 233 - Calling with 3 arguments
return self._verify_slack_signature(signature, timestamp, body)

# But _verify_slack_signature() only accepts 2 arguments (self + 1)
TypeError: _verify_slack_signature() takes 2 positional arguments but 3 were given
```

### Root Cause
Method refactored but call sites not updated. Signature verification is **completely broken** in production.

### Security Impact
⚠️ **HIGH** - Slack webhook signatures cannot be validated, potentially allowing unauthorized requests.

### Recommended Fix
Check `_verify_slack_signature()` method signature and update all call sites to match. Likely should be:
```python
def _verify_slack_signature(self, request_data: dict) -> bool:
    # Extract signature, timestamp, body from request_data internally
```

Or update the method to accept 3 params:
```python
def _verify_slack_signature(self, signature: str, timestamp: str, body: str) -> bool:
```

**Estimated Time:** 30 minutes

---

## Bug #2-4: Webhook Flow Integration Failures

**Priority:** P1
**File:** `test_ngrok_webhook_flow.py`
**Tests Affected:** 3 tests

### Failing Tests
1. `test_webhook_event_processing_flow`
2. `test_webhook_error_handling`
3. `test_ngrok_webhook_end_to_end_flow`

### Problem
These tests depend on Bug #1 being fixed first. Once signature verification works, these will likely pass or reveal next-level integration issues.

### Recommended Approach
1. Fix Bug #1 first
2. Re-run these 3 tests
3. Triage any remaining failures

**Estimated Time:** 1-2 hours (after Bug #1 fixed)

---

## Bug #5-8: OAuth Spatial Integration Incomplete

**Priority:** P1
**File:** `test_oauth_spatial_integration.py`
**Tests Affected:** 4 tests

### Failing Tests
1. `test_oauth_scopes_affect_spatial_capabilities`
2. `test_oauth_token_refresh_updates_spatial_territory`
3. `test_oauth_state_validation_prevents_spatial_initialization`
4. `test_oauth_user_context_integration`

### Problem
These are TDD tests for OAuth + Spatial integration features that are **partially implemented**. Tests were written during Nov 20 Slack TDD session but implementation is incomplete.

### Root Cause
The tests expect:
- OAuth scopes to affect what spatial areas are accessible
- Token refresh to update spatial territory mappings
- OAuth state validation to prevent spatial initialization
- User context from OAuth to integrate with spatial system

**Current State:** Core OAuth works, but spatial integration layer is missing.

### Recommended Fix
This is **new feature work**, not a bug fix. Options:

**Option A - Skip Tests (Recommended)**
Mark these 4 tests as `@pytest.mark.skip(reason="Spatial OAuth integration - Phase 2 work")` and create backlog items.

**Option B - Complete Implementation**
Implement the spatial-aware OAuth layer. Estimated 3-4 hours of feature development.

**Estimated Time:**
- Option A: 15 minutes (skip + document)
- Option B: 3-4 hours (implement features)

---

## Summary Table

| Bug # | Test File | Severity | Type | Est. Time |
|-------|-----------|----------|------|-----------|
| 1 | ngrok_webhook | 🔴 P0 | Signature mismatch | 30 min |
| 2-4 | ngrok_webhook | P1 | Integration (depends on #1) | 1-2 hrs |
| 5-8 | oauth_spatial | P1 | Incomplete features | 3-4 hrs OR skip |

**Total Fix Time:** 5-6.5 hours (if implementing all) OR 2-2.5 hours (if skipping OAuth)

---

## Recommendations

### Immediate (This Sprint)
1. **Fix Bug #1** - Critical security issue with signature verification
2. **Re-test Bugs #2-4** after #1 is fixed
3. **Skip OAuth tests (#5-8)** with proper documentation

### Next Sprint
1. Decide if OAuth spatial integration is needed
2. If yes, create proper user stories/tasks
3. If no, remove the TDD tests

---

## What We Fixed Today (Context)

For comparison, we **successfully fixed** 13 tests in `test_event_spatial_mapping.py` by:
- Implementing missing `USER_JOINED`/`USER_LEFT` event handlers
- Fixing test attribute mismatches (`reaction` → `reaction_type`, `timestamp` → `event_time`, etc.)
- These were **test bugs** and **missing implementations**, not deep product issues

The remaining 8 are **product code bugs** requiring actual code changes, not test fixes.

---

## Files Referenced

**Product Code:**
- `services/integrations/slack/webhook_router.py`
- `services/integrations/slack/event_handler.py` (fixed today)
- `services/integrations/slack/spatial_mapper.py`

**Tests:**
- `tests/unit/services/integrations/slack/test_event_spatial_mapping.py` ✅ 13/13 passing
- `tests/unit/services/integrations/slack/test_ngrok_webhook_flow.py` ⚠️ 4/8 passing
- `tests/unit/services/integrations/slack/test_oauth_spatial_integration.py` ⚠️ 14/18 passing

**Current Status:** 31/39 passing (79% pass rate) in Slack spatial test suite
