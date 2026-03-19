# Memo: Chief Architect Response to M0 Retro / M1 Planning

**From**: Chief Architect
**To**: PM, PPM, CXO
**Date**: March 10, 2026
**Re**: M1 Planning Recommendations

---

## Summary

M0's 3.9x expansion (7 → 27 issues) resulted from the Assembly Assumption at the planning layer: every feature assumed infrastructure existed that didn't. M1 should learn from this by (1) deferring high-expansion-risk items, (2) formalizing the spec pipeline, and (3) addressing M0 velocity debt before it compounds.

---

## The 5 Recommendations

### 1. Defer #557 WebSocket to M2

**Rationale**: WebSocket is horizontal infrastructure touching frontend, backend, deployment, and testing. Nothing in M1 requires it. No user-facing urgency (PM confirmed).

**Action**: Remove from M1 scope. If desired later, split into spike (M1) + implementation (M2).

### 2. Defer or Deprioritize #482 KMS

**Rationale**: AWS migrations cascade. No external compliance pressure (PM confirmed). "Inherited enterprise conventional wisdom" is not a forcing function.

**Action**: Move to M2, or keep in M1 backlog as stretch goal only.

### 3. Formalize Spec Pipeline for Epics

**Rationale**: #858 same-day pipeline worked. Pattern should be required, not optional.

**Process for M1 epics (#470, #706, #717)**:
1. CXO guidance memo (UX implications)
2. PPM scope confirmation (acceptance criteria)
3. Architect technical review (integration points, risks)
4. Lead Dev implementation begins

**Action**: Add this as gate requirement before epic implementation starts.

### 4. Include M0 Velocity Debt

Two items should be in M1:

| Issue | Effort | Why Now |
|-------|--------|---------|
| ARCH-LAZY-WORKFLOW | 2-3 hrs | Semantic confusion compounds; async work coming |
| #876 Error Humanization | ~9 hrs | 54+ raw errors still leak; user-facing quality |

**Action**: Add both to M1. Can run in parallel with other work.

### 5. Add Test Infrastructure Hardening

**Rationale**: #868 revealed shadowed `__init__.py` causing 90+ test failures. 21 directories still at risk.

**Action**: File TEST-INIT-SHADOW issue, include in M1 testing track.

---

## Revised Risk Assessment

| Issue | PPM Risk | Architect Risk | Recommendation |
|-------|----------|----------------|----------------|
| #557 WebSocket | High | Very High | **Defer to M2** |
| #482 KMS | (implied bounded) | Medium-High | **Defer to M2** |
| #470 RBAC | High | High | Keep, but require spec pipeline |
| #472 Slack OAuth | Medium | High | Keep, expect 2x expansion |
| #372 Learning | Medium | High | Keep, expect unknowns |
| Testing (#190, #247, #352, #738, #739) | Low | Low | Keep, bounded scope |
| #542 Token Revocation | Low | Low | Keep, quick win — do first |

---

## Proposed M1 Sequencing

**Week 1-2: Quick Wins + Debt**
- #542 Token Revocation (builds momentum)
- ARCH-LAZY-WORKFLOW (2-3 hrs)
- TEST-INIT-SHADOW (new issue)
- Testing issues can start in parallel

**Week 2-3: Spec Pipeline for Epics**
- #470 RBAC: CXO → PPM → Architect review before implementation
- #706/#717 MUX: Same pipeline

**Week 3-4: Implementation**
- Epic implementation after specs approved
- #876 Error Humanization (can parallelize)
- #472 Slack OAuth (expect expansion)

**Deferred to M2**:
- #557 WebSocket
- #482 KMS
- #372 Learning (consider — high unknown risk)

---

## Issues to Add

| Issue | Title | Effort | Track |
|-------|-------|--------|-------|
| ARCH-LAZY-WORKFLOW | Defer workflow creation to async handlers | 2-3 hrs | Architecture |
| TEST-INIT-SHADOW | Audit remaining `__init__.py` shadowing risk | 1-2 hrs | Testing |

---

## ADRs to Draft in M1

| ADR | Purpose | When |
|-----|---------|------|
| ADR-058: Error Contract Standard | Codify `safe_intent_handler`, response envelope | Before #876 implementation |
| ADR-059: Real-Time Architecture | Document WebSocket pattern | Before M2 WebSocket work |

---

## Open for Discussion

1. **#372 Learning**: I marked it high risk (new subsystem). Should it defer to M2 alongside WebSocket?

2. **Sprint duration**: M0 was estimated 13-22 days, took 17 total (3 core + 14 polish). Should M1 plan for similar timeline with explicit wiring pass phase?

3. **CXO B2 gate**: Should we require CXO testing earlier in M1, not just at gate? Perhaps after each epic completes?

---

*Memo prepared: March 10, 2026, 10:35 PM*
