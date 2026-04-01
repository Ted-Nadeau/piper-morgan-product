# Architect Memo: Unified Formality System

**From**: Lead Developer (M0 Sprint)
**To**: Chief Architect
**Date**: 2026-02-18
**Re**: Three independent formality systems needing unification
**GitHub Issue**: #823

---

## Context

During M0 (Conversational Glue), three features were built that each independently handle tone/formality:

| System | Source | Model | Persistent? | Connected? |
|--------|--------|-------|-------------|------------|
| **OnboardingNarrativeBridge** (#766) | 3-tier dict (warm/conversational/professional) | String key | No | Onboarding only |
| **WarmthCalibration** (#619) | 4-tier enum + continuous gentleness (0.0-1.0) | Context-computed | No | Error handling, classifier |
| **PersonalityProfile** (#262) | Float 0.0-1.0 | DB-persisted | Yes | **Orphaned — built but unused** |

Additionally, **SoftInvocationDetector** (#767) and **SlotFillingManager** (#765) hardcode warm tone universally with no formality awareness.

## What Works

Each system functions correctly in isolation. No user-facing failures. The fragmentation is a UX inconsistency (P3), not a broken seam.

## What Doesn't Work

1. **Onboarding preference is lost** — user selects formality tier during onboarding but it's not persisted to PersonalityProfile
2. **PersonalityProfile is orphaned** — exists in DB, maps questionnaire answers to structured preferences, but no M0 code consumes it
3. **No authoritative source** — three competing models (string, enum, float) with no "source of truth"
4. **Context vs. preference conflict** — WarmthCalibration says "low confidence → more warmth" but PersonalityProfile might say "user prefers professional"

## Design Questions Needing Architect Input

1. **Authoritative source**: Should formality derive from user preference (PersonalityProfile), context (WarmthCalibration), or both? If both, what's the priority?

2. **Unified model**: How do we reconcile 3 strings, 4 enums, and 1 float? Proposal needed for a shared formality representation.

3. **Data flow**: Should formality be loaded at request boundary and passed through the pipeline, or computed on-demand per subsystem?

4. **Conflict resolution**: When context suggests warmth but user preference suggests cool — user always wins? Context modulates around user baseline? Different strategies for different systems?

5. **Persistence**: Should onboarding's formality selection persist to PersonalityProfile? Should WarmthCalibration's context adjustments be informed by the persisted baseline?

## Recommendation

This is a design-level decision, not a code fix. Acceptable for alpha at P3. Required before production if heterogeneous user preferences are expected. Recommend architect review to establish the unified formality framework that all M0 systems can adopt.

## Files Involved

- `services/onboarding/narrative_bridge.py` (3-tier, unconnected)
- `services/intent_service/warmth_calibration.py` (4-tier, context-driven)
- `services/personality/personality_profile.py` (float, persistent, orphaned)
- `services/intent_service/soft_invocation.py` (hardcoded warm)
- `services/slot_filling/slot_filling_manager.py` (hardcoded generic)
