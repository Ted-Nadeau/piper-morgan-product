# Memo: Unified Formality System — Design Decisions

**From**: Chief Architect
**To**: Lead Developer
**Date**: February 21, 2026
**Re**: Response to #823 design questions
**GitHub Issue**: #823

---

## Summary

Your analysis is correct: three independent formality systems is the "assembly assumption" at the UX layer. Here are my decisions on your design questions.

---

## Design Decisions

### 1. Authoritative Source

**Decision**: User preference (PersonalityProfile) is the **baseline**; context (WarmthCalibration) **modulates** around it.

User preference is never overridden, only adjusted within their comfort band. This respects user agency while allowing situational adaptation.

### 2. Unified Model

**Decision**: Continuous scale with presentation labels.

```python
# Core model
formality = baseline + adjustment
# baseline: user preference (0.0-1.0), from PersonalityProfile
# adjustment: context modifier (-0.2 to +0.2), from WarmthCalibration
# result: clamped to [0.0, 1.0]

# Presentation labels (for string-based systems)
def formality_label(value: float) -> str:
    if value < 0.33:
        return "warm"      # casual, friendly
    elif value < 0.67:
        return "balanced"  # conversational, neutral
    else:
        return "professional"  # formal, business
```

The 3-tier strings (OnboardingNarrativeBridge) and 4-tier enums (WarmthCalibration) become presentation views over this continuous scale. No need to change existing enums — just map them to the unified scale.

### 3. Data Flow

**Decision**: Load at request boundary, pass through pipeline.

`RequestContext` already carries `user_id`. Add `formality_baseline: Optional[float]` there. Subsystems receive it and apply local adjustments.

```python
# At request boundary (e.g., in middleware or handler entry)
context.formality_baseline = await personality_service.get_formality(user_id)

# In subsystems
effective_formality = context.formality_baseline + local_adjustment
```

If `formality_baseline` is None (user hasn't set preference), default to 0.5 (balanced).

### 4. Conflict Resolution

**Decision**: Context modulates around baseline, never overrides.

Example scenarios:
| User Baseline | Context Adjustment | Result | Interpretation |
|---------------|-------------------|--------|----------------|
| 0.8 (professional) | +0.15 (warmth needed) | 0.65 | Still professional-leaning, slightly softened |
| 0.2 (warm) | -0.1 (serious context) | 0.30 | Still warm, slightly more measured |
| 0.5 (balanced) | +0.2 (error recovery) | 0.70 | Shifts toward professional empathy |

The adjustment range (±0.2) ensures context can shift tone noticeably but never flip a user's entire preference.

### 5. Persistence

**Decision**: Yes — onboarding formality selection should persist to PersonalityProfile.

Wire this during onboarding completion:
```python
# When onboarding completes with formality selection
personality_profile.formality_preference = selected_tier_to_float(tier)
await personality_repo.save(personality_profile)
```

Mapping:
- "warm" → 0.2
- "conversational" → 0.5
- "professional" → 0.8

---

## Priority & Placement

| Priority | Rationale |
|----------|-----------|
| **P3 for alpha** | Current state is inconsistent but not broken |
| **P1 for beta** | Before diverse user preferences matter |

**Recommended sprint**: M1 or M2

---

## Proposed Issue

Create a single issue for the unified framework:

**Title**: FORM-UNIFIED: Implement unified formality framework

**Acceptance Criteria**:
- [ ] `FormattedContext` or `RequestContext` carries `formality_baseline`
- [ ] PersonalityProfile consumed at request boundary
- [ ] OnboardingNarrativeBridge persists selection to PersonalityProfile
- [ ] WarmthCalibration reads baseline, applies adjustment
- [ ] SoftInvocationDetector uses formality (not hardcoded warm)
- [ ] SlotFillingManager uses formality (not hardcoded generic)
- [ ] Mapping functions between continuous scale and tier labels
- [ ] Tests for conflict resolution scenarios

**Effort**: 3-5 days

---

## Action Items

1. **Close #823** with this memo as resolution (design decision made, implementation deferred)
2. **Create FORM-UNIFIED issue** for M1/M2 sprint
3. **No code changes needed now** — alpha can ship with current inconsistency

---

*Architecture decision recorded. Thank you for the thorough analysis.*
