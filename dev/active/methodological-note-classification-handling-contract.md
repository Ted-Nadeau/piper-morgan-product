# Methodological Note: Classification-Handling Contract Gap

**Date**: 2026-03-16
**Author**: Lead Developer
**For discussion with**: Chief Architect, CIO
**Triggered by**: #915, #916, #917, #918, #919 — five bugs discovered in Phase 2 quality verification testing

---

## Observation

Four user-facing bugs and one security issue discovered during the first round of manual quality verification share a common structural root cause. This note captures the systemic pattern for architectural discussion.

## The Pattern: "Extend Without Verifying"

All five issues follow the same meta-pattern:

1. A **new capability** was added at one layer (classification patterns, user-scoped auth)
2. The **downstream layer** was not updated to match (handler implementation, legacy auth removal)
3. A **silent fallback** absorbed the gap (stub responses, global keychain key)
4. No **contract or test** existed to detect the mismatch
5. The system appeared to work until a human sent a real query

### Evidence

| Bug | Layer extended | Layer not updated | Silent fallback |
|-----|---------------|-------------------|-----------------|
| #915 | Pre-classifier: CALENDAR_QUERY_PATTERNS (#901) | _handle_query_intent: no scheduling action | `week_calendar` default action → raw data dump |
| #916 | Pre-classifier: ANALYSIS_PATTERNS (#901) | _handle_analysis_intent: no analyze_blockers branch | `"Analysis processed: {action}"` stub |
| #918 | Pre-classifier: detect_multiple_intents (#901) | Orchestrator: can't handle QUERY category | Apology message from failure aggregation |
| #917 | Keychain: user-scoped keys (#734, #843) | Legacy global key not removed | Falls back to another user's token |
| #919 | Pre-classifier: CALENDAR_QUERY overlaps TEMPORAL | No exclusion logic in multi-intent detection | Phantom multi-intent triggers both paths |

### Scale

A codebase audit found:
- **3 pre-classifier actions** that fall to generic stubs today
- **8+ pattern overlaps** between CALENDAR_QUERY and TEMPORAL in multi-intent detection
- **Zero tests** that verify user-facing response quality (all tests verify routing correctness only)
- **Multiple legacy fallback patterns** in security-sensitive paths (calendar adapter, notion adapter, trust stage defaults)

## Root Causes (Structural)

### 1. No contract between classification and handling layers

The pre-classifier emits action strings. The handler chain matches them with if/elif chains. There is no registry, no type check, no compile-time or test-time verification that every emitted action has a corresponding handler. New patterns can be added to the pre-classifier without touching the handler layer, and the system silently degrades.

### 2. Tests verify routing, not response quality

Every test in the intent service suite asserts on classification correctness: "did this message route to the right category/action?" None assert on what the user actually sees. A handler could return `"Analysis processed: analyze_blockers"` and all tests would pass. The test suite is optimized for classification accuracy, not user experience.

### 3. Silent stubs instead of loud failures

When a handler doesn't know what to do with an action, it returns a generic message to the user instead of raising an error or logging a warning. This makes gaps invisible — the system appears functional until a human reads the response.

### 4. Legacy fallbacks preserved without risk analysis

When new user-scoped mechanisms replace legacy global ones, the legacy path is kept "for backward compatibility" without asking "what happens when both are live?" The answer, in the calendar case, is credential leakage.

## Possible Interventions (For Discussion)

These are starting points for architectural discussion, not recommendations:

1. **Action registry**: A shared data structure that maps every pre-classifier action to its handler. If a pattern emits an action not in the registry, fail loudly at startup or test time.

2. **Response quality smoke tests**: For each pre-classifier pattern, a test that sends the example query through the full stack and asserts the response doesn't contain known stub phrases (`"processed:"`, `"not yet implemented"`, `"I wasn't able to"`).

3. **Fail-loud stubs**: Replace silent stub responses with structured log warnings + floor routing. If a handler doesn't have a real implementation for an action, route to the conversational floor with context rather than returning a bare label.

4. **Legacy removal discipline**: When adding user-scoped mechanisms, the legacy fallback gets a removal date, not a "backward compatibility" justification. Or: no fallback — if the new path fails, fail cleanly.

5. **Multi-intent deduplication**: `detect_multiple_intents()` should share the same priority/exclusion logic as `pre_classify()`, or they should be unified into one path.

## Relationship to Excellence Flywheel

This gap maps to specific flywheel stages:
- **Adversarial validation**: Not applied to pre-classifier extensions. Nobody typed the new patterns to see what response came back.
- **Layer-by-layer DDD**: Classification layer was extended independently from handler layer, violating the contract.
- **TDD unless reason not to**: No test was written for "what does the user see?" — only "does the router route?"

---

*This note is for discussion. No fixes should be applied without PM/Architect review of the structural interventions.*
