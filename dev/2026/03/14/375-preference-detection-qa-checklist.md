# Manual QA Checklist: Preference Detection System (#375)

**For**: PM (xian)
**Related**: Epic #248 (CONV-LEARN-PREF)
**Date**: 2026-03-14

---

## System Overview

The preference detection system automatically detects user personality preferences from natural conversation and suggests applying them. Instead of editing configuration, users say things like "I'd like more detailed technical explanations" and the system detects, suggests, and applies these preferences.

**Four personality dimensions:**
1. **Warmth Level** (0.0 = professional → 1.0 = friendly/warm)
2. **Confidence Display Style** (NUMERIC, DESCRIPTIVE, CONTEXTUAL, or HIDDEN)
3. **Action Orientation** (HIGH = always next steps, MEDIUM = when relevant, LOW = minimal)
4. **Technical Depth** (DETAILED, BALANCED, SIMPLIFIED)

**User interaction flow:**
- Detection is **automatic** in chat — no special commands
- System suggests preferences via UI components (not forced)
- Users see "Accept" / "Dismiss" buttons
- Accepted preferences apply immediately

---

## Pre-Testing Setup

- [ ] Fresh test user (no prior preference history)
- [ ] Clear browser cache
- [ ] Backend running on port 8001
- [ ] PostgreSQL running on port 5433

---

## Section 1: Detection Accuracy

**1.1 Detect warmth preference**
- [ ] Send: "I really appreciate your friendly approach and love the casual conversation style"
- [ ] Verify: Preference suggestion appears for "warmth_level"

**1.2 Detect technical depth**
- [ ] Send: "I want more information about the architecture and code implementation"
- [ ] Verify: Suggestion for "technical_depth" → "detailed"

**1.3 Detect professionalism**
- [ ] Send: "Please keep responses professional, concise, and efficient"
- [ ] Verify: Suggestion for lower warmth

**1.4 Detect action orientation**
- [ ] Send: "Let's execute immediately. What are the next steps?"
- [ ] Verify: Suggestion for "action_orientation" → "high"

**1.5 No false positives**
- [ ] Send: "What's the weather like today?"
- [ ] Verify: No preference suggestion appears

**1.6 Multiple preferences in one message**
- [ ] Send: "I love the casual approach. Please explain the architecture in detail with immediate action steps"
- [ ] Verify: Multiple suggestions appear (≥2 dimensions)

---

## Section 2: Confidence Thresholds

**2.1 High confidence (≥0.9) — auto-apply**
- [ ] Send explicit: "I prefer technical detail"
- [ ] Verify: No suggestion UI — preference auto-applied
- [ ] Verify: Next response uses updated depth

**2.2 Medium confidence (0.4–0.9) — show suggestion**
- [ ] Send implicit: "That was interesting—more analysis would be helpful"
- [ ] Verify: Suggestion appears with accept/dismiss buttons

**2.3 Low confidence (<0.4) — hidden**
- [ ] Send vague: "the response was ok"
- [ ] Verify: No suggestion visible

---

## Section 3: Accept Flow

- [ ] Click "Accept" on a suggestion
- [ ] Verify: Profile updates (check `/api/v1/preferences/profile`)
- [ ] Verify: Next chat response reflects the new preference
- [ ] Verify: Preference persists after page reload
- [ ] Accept multiple preferences in sequence — both apply correctly

---

## Section 4: Dismiss Flow

- [ ] Click "Dismiss" on a suggestion
- [ ] Verify: Suggestion disappears
- [ ] Verify: Profile NOT updated
- [ ] Send similar message again — verify preference is re-detected (not permanently blocked)

---

## Section 5: Response Enhancement

**5.1 Warmth applied**
- [ ] With high warmth: responses use friendly language, greetings
- [ ] With low warmth: responses are concise, professional

**5.2 Technical depth applied**
- [ ] Detailed: technical terms, code examples, deeper explanations
- [ ] Simplified: high-level summaries, less jargon

**5.3 Action orientation applied**
- [ ] High: "Next steps:" section, explicit action items
- [ ] Low: analysis only, minimal direction

**5.4 Confidence style applied**
- [ ] Numeric: "87% confident"
- [ ] Contextual: "Based on patterns..."
- [ ] Hidden: no confidence statements

---

## Section 6: Personality Profile Page

- [ ] Load `/assets/personality-preferences.html`
- [ ] All 4 dimensions display current values
- [ ] Sliders/radio buttons work and update live preview
- [ ] "Save Preferences" persists changes
- [ ] "Reset to Defaults" restores: warmth=0.7, confidence=contextual, action=high, depth=balanced
- [ ] "Test Enhancement" shows sample output with current settings

---

## Section 7: Full E2E Flow

- [ ] Fresh session → send preference signal → suggestion appears → accept → profile updated → next response uses it → persists across sessions

---

## Section 8: Edge Cases

- [ ] Conflicting preferences: second overrides first cleanly
- [ ] Missing auth: API returns 401, no data leakage
- [ ] Different users: preferences are isolated per user

---

## Key Files for Reference

| What | Where |
|------|-------|
| Core logic | `services/personality/preference_detection.py` |
| Detection | `services/personality/conversation_analyzer.py` |
| API routes | `web/api/routes/preferences.py` |
| Unit tests (27) | `tests/unit/services/personality/test_preference_detection.py` |
| UI page | `web/assets/personality-preferences.html` |
| Guide | `docs/guides/preference-detection-guide.md` |

---

## What's Already Tested Automatically

Data structures, confidence scoring, language patterns, session storage, application logic — all have passing unit/integration tests (27+).

## What Needs Manual Testing

Real conversation flows, UI interactions, cross-session persistence, visual clarity, and actual end-user experience quality.

---

_Checklist prepared: 2026-03-14_
_Issue: #375_
