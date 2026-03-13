# Memo: CXO Response — M0 Retrospective & M1 Planning

**To**: Principal Product Manager, PM
**From**: Chief Experience Officer
**Date**: March 10, 2026
**Re**: M1 Planning Input (Response to PPM Briefing)

---

## Summary

Five recommendations from the UX lens, plus specific answers to PPM's questions.

---

## Recommendations

### 1. Institutionalize Fresh-Account Testing as Gate Requirement

**Learning from M0**: My Mar 1 testing found 4 bugs that passed 6,088 tests. The pattern was consistent: developer accounts hide edge cases that fresh users hit immediately.

**Recommendation**: Every sprint gate should include at least one fresh-account testing pass. Not just "CXO tests" — define it as a gate criterion with specific scenarios.

**For M1**: Create a "Fresh Account Test Matrix" listing the core journeys to verify. This prevents the gate from becoming a formality.

---

### 2. Error Path UX Deserves Explicit Attention

**Learning from M0**: The #876 discovery (56 raw error messages leaking to users) and my testing (Action Humanizer gaps, workflow timeouts) reveal a systemic pattern: happy paths get tested, error paths get forgotten.

**For M1 high-risk issues**:
- **#557 WebSocket**: Connection failures, reconnection states, timeout handling — all need conversational treatment, not technical messages
- **#472 Slack OAuth**: OAuth failures need clear user guidance ("Your Slack connection expired — want to reconnect?")
- **#470 RBAC**: Permission denials must feel explanatory, not blocky

**Colleague Test for errors**: A colleague doesn't say "Error 401: Unauthorized." They say "I can't access that — it looks like it belongs to a different workspace."

---

### 3. Prioritize #706 (MUX-OBJECTS-VIEWS) for User Journey Completeness

**Current state**: The right sidebar is still just conversations. The Feb 28 conversation lifecycle spec established the sidebar as "entity surface" — but we haven't delivered on that vision.

**Why this matters**: Users will encounter the right sidebar and wonder why it's nearly identical to the left sidebar. The differentiation exists in spec but not in experience.

**Recommendation**: #706 should be treated as UX-critical, not just infrastructure. It completes a user journey M0 started but didn't finish.

---

### 4. Mark #557 (WebSocket) and #372 (Learning) as Wiring Pass Candidates

**Pattern-062 (Assembly Assumption)**: Individual components working ≠ composed experience working.

**#557 WebSocket** is classic wiring territory:
- Backend sends events
- Frontend receives events
- UI updates accordingly
- Connection state is managed

Each layer can pass its tests while the composed experience fails. Explicit wiring pass required.

**#372 Learning** has similar risk:
- Learning subsystem captures patterns
- Patterns inform Piper's responses
- Users perceive (or don't perceive) the learning

The gap between "learning works" and "users feel Piper learns" is a wiring problem.

---

### 5. Add UI Polish Issue to M1 Scope

**Context**: Yesterday I noted Piper's chat interface could benefit from fit-and-finish cleanup — grid alignment, spacing, layout rules.

**Recommendation**: Create a bounded "UI Polish" issue for M1:
- Scope: Chat interface layout, spacing, typography consistency
- NOT a full redesign — strictly fit-and-finish
- Can run in parallel with feature work
- Low expansion risk if bounded properly

This raises the baseline UX quality without blocking feature work.

---

## Specific Answers to PPM Questions

### Q1: B2 Testing Learnings to Carry Forward

| Learning | Application to M1 |
|----------|-------------------|
| Fresh accounts reveal hidden bugs | Gate requirement |
| Error paths under-tested | Explicit error scenario coverage |
| "Detection works, response broken" | Test full user-facing path, not just classification |
| Calendar integration fragile | Integration stability pass before features |

### Q2: User Journey Gaps from M0

| Gap | M1 Issue | Status |
|-----|----------|--------|
| Right sidebar = entity surface | #706 MUX-OBJECTS-VIEWS | In scope |
| Product/Project modeling | #717 MUX-PRODUCT-MODELING | In scope |
| Conversation lifecycle UI | #715 (M2) | Not in M1 — spec done, impl waiting |

**Note**: #715 (conversation lifecycle wiring) was kept in M2 per my recommendation. The spec (#858) is complete. If M1 has capacity, promoting #715 would complete the M0 → M1 handoff cleanly.

### Q3: Colleague Test Risk

| Issue | Risk | Why |
|-------|------|-----|
| **#557 WebSocket** | High | Connection state changes ("Reconnecting...") feel very un-colleague-like if handled technically |
| **#372 Learning** | Medium | If Piper's learning becomes visible, it must feel observational, not surveillance-like. "I noticed you prefer..." not "I have recorded that you..." |
| **#470 RBAC** | Medium | Permission errors can feel blocky. "Access denied" vs "I can't help with that project — it's in a different workspace" |
| **#472 Slack** | Low-Medium | OAuth prompts are familiar to users; less UX risk than WebSocket |

### Q4: Wiring Pass Candidates

| Issue | Wiring Pass? | Rationale |
|-------|--------------|-----------|
| **#706 MUX-OBJECTS-VIEWS** | ✅ Yes | Epic connecting UI to backend entity states — classic Pattern-062 territory |
| **#557 WebSocket** | ✅ Yes | Infrastructure affecting many surfaces |
| **#472 Slack OAuth** | ✅ Yes | Integration surface with known gaps from M0 |
| **#372 Learning** | ✅ Yes | New subsystem where "works" ≠ "users perceive it" |
| Testing issues | ❌ No | Bounded scope, fixing existing tests |

### Q5: Anything Else

1. **UI Polish issue** (see Recommendation #5) — should be added to M1

2. **#715 Conversation Lifecycle** — Consider promoting from M2 if capacity allows. Spec is done; implementation would complete the M0 vision.

3. **Action Humanizer audit** — M0 found the Action Humanizer wasn't transforming all error paths. Before M1 adds new features that can error, verify the humanizer covers existing paths.

---

## Issues to Add, Remove, or Re-sequence

| Action | Issue | Rationale |
|--------|-------|-----------|
| **Add** | UI Polish (new) | Fit-and-finish, parallel track |
| **Consider promoting** | #715 from M2 | Spec done, completes M0 vision |
| **Sequence early** | #706 | User journey completion |
| **Sequence late** | #557 | High expansion risk; do after lower-risk issues |

---

## Risk Concerns Not Captured in Briefing

1. **WebSocket + Learning interaction**: If both #557 and #372 are in M1, they could interact poorly. Real-time updates + learning visibility = complex UX. Consider sequencing them apart.

2. **Testing issues may be deceptively "bounded"**: #247 (AsyncSessionFactory) and #738 (Attention System) touch infrastructure. They could expand like M0's "simple" issues did.

3. **Slack OAuth expansion**: M0's keychain audit found 15 non-scoped sites. #472 may discover more during implementation.

---

*CXO input for M1 planning — March 10, 2026*
