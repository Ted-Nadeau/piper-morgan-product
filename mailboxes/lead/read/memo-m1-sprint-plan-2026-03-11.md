# Memo: M1 Sprint Plan — Order of Attack

**To**: Chief Experience Officer, Chief Architect, Lead Developer
**From**: Principal Product Manager
**Date**: March 11, 2026
**Re**: M1 Sprint Sequencing and Process

---

## Summary

Following the M0 retrospective and input from CXO and Chief Architect, we've finalized the M1 sprint plan. This memo documents the scope, sequencing, and process changes for M1.

---

## M1 Scope Summary

**Theme**: Foundation (Security + Testing + MUX Wiring)

### Issues Remaining (16 total)

| Track | Issues |
|-------|--------|
| **Diagnostics** | #884 CANONICAL-RETEST, #885 TEST-INIT-SHADOW |
| **Quick Wins / Debt** | #542 Token Revocation, #883 ARCH-LAZY-WORKFLOW |
| **Testing** | #190, #247, #352, #738, #739 |
| **MUX Wiring** | #705, #706, #717 |
| **Security** | #470 RBAC epic |
| **Slack** | #472 OAuth TDD Gaps |
| **UX** | #886 UI-POLISH |
| **QA** | #375 Manual Testing |

### Scope Changes from Original M1

| Action | Issues | Rationale |
|--------|--------|-----------|
| **Removed** | #557 WebSocket | High expansion risk; defer to M2 |
| **Removed** | #482 KMS | No external pressure; defer to M2 |
| **Removed** | #372 Learning | Thematically fits M3 (Skills) |
| **Added** | #715 Conversation Lifecycle | Promoted from M2; spec done, completes M0 vision |
| **Added** | #883 ARCH-LAZY-WORKFLOW | M0 debt; 2-3 hrs |
| **Added** | #884 CANONICAL-RETEST | Diagnostic; measures M0 impact |
| **Added** | #885 TEST-INIT-SHADOW | Latent risk from #868 |
| **Added** | #886 UI-POLISH | Bounded fit-and-finish |

---

## Suggested Order of Attack

### Phase 1: Diagnostics + Quick Wins (Week 1)

*Goal: Gather information, build momentum, clear debt before epic work*

| Order | Issue | Title | Effort | Rationale |
|-------|-------|-------|--------|-----------|
| 1 | #884 | CANONICAL-RETEST | 2-4 hrs | **Do first** — results inform rest of sprint |
| 2 | #885 | TEST-INIT-SHADOW | 1-2 hrs | Clear latent risk before adding tests |
| 3 | #542 | SEC Token Revocation | Quick | Builds momentum |
| 4 | #883 | ARCH-LAZY-WORKFLOW | 2-3 hrs | Clear M0 semantic debt |
| 5 | #739 | TEST-FIX: Complex Mocking | Bounded | Test reliability before features |
| 6 | #738 | TEST-INFRA: Time Simulation | Bounded | Test reliability before features |

**Parallel track** (can run alongside Phase 1):
- #886 UI-POLISH (4-6 hrs) — doesn't block anything
- #375 QA Manual Testing — human work, no code dependencies

---

### Phase 2: Spec Pipeline for Epics (Week 1-2 transition)

*Goal: CXO → PPM → Architect review before implementation begins*

**Process** (formalized from M0's #858 success):
1. CXO guidance memo (UX implications)
2. PPM scope confirmation (acceptance criteria)
3. Architect technical review (integration points, risks)
4. Lead Dev implementation begins only after all three sign off

| Epic | Spec Pipeline Status | Notes |
|------|---------------------|-------|
| #706 MUX-OBJECTS-VIEWS | Needs spec | CXO: "sequence early" — completes user journey |
| #717 MUX-PRODUCT-MODELING | Needs spec | Defines Product concept |
| #470 SEC-RBAC Phases 4-5 | Needs spec | High expansion risk — bound scope in spec |

Run spec reviews in parallel. Implementation doesn't start until approved.

---

### Phase 3: Epic Implementation + Testing Infrastructure (Week 2-3)

*Goal: Implement spec-approved epics, strengthen test foundation*

| Order | Issue | Title | Notes |
|-------|-------|-------|-------|
| 7 | #706 | MUX-OBJECTS-VIEWS | After spec approval; B2 test after completion |
| 8 | #717 | MUX-PRODUCT-MODELING | After spec approval; B2 test after completion |
| 9 | #705 | MUX-LIFECYCLE-UI-B | Wiring work, follows #706/#717 |
| 10 | #715 | Conversation Lifecycle | Promoted from M2; spec done (#858) |
| 11 | #470 | SEC-RBAC Phases 4-5 | After spec approval; B2 test after completion |
| 12 | #190 | TEST-QUALITY | Strengthens foundation for remaining work |
| 13 | #352 | TEST-SMOKE-E2E | Core journey tests — inform wiring pass |
| 14 | #247 | BUG-TEST-ASYNC | CXO flagged as potentially deceptive — do after other test fixes |

---

### Phase 4: High-Risk + Wiring Pass (Week 3-4)

*Goal: Tackle expansion-prone item, then integration testing*

| Order | Issue | Title | Notes |
|-------|-------|-------|-------|
| 15 | #472 | Slack OAuth TDD Gaps | **Last feature work** — expect 2x expansion |
| 16 | — | Wiring Pass | Pattern-062; verify composed experience |
| 17 | — | Fresh Account B2 Testing | Full sprint gate verification |

---

## Visual Timeline

```
Week 1          Week 2          Week 3          Week 4
─────────────────────────────────────────────────────────
[Diagnostics]   [Spec Pipeline] [Implementation] [Wiring]
#884 #885       #706 spec       #706 impl        #472
[Quick Wins]    #717 spec       #717 impl        Wiring Pass
#542 #883       #470 spec       #705 #715        B2 Testing
#739 #738                       #470 impl
                                #190 #352 #247
─────────────────────────────────────────────────────────
        [UI-POLISH #886 + QA #375 — parallel throughout]
```

---

## Process Changes for M1

Based on M0 learnings and role input:

### 1. Spec Pipeline Required for Epics

Before any epic implementation begins:
- CXO memo on UX implications
- PPM scope confirmation
- Architect technical review
- All three must approve

### 2. Fresh Account Test Matrix

Gate requirement, not optional. After each epic completes:
- Fresh account testing pass
- Core journeys verified
- Issues logged immediately, not batched

### 3. B2 Testing After Each Epic

Don't wait for sprint gate. Test after:
- #706 completes
- #717 completes
- #470 completes
- #472 completes

### 4. Explicit Wiring Pass (Week 4)

Pattern-062 (Assembly Assumption) is built into the plan:
- Week 4 reserved for integration testing
- Wiring pass verifies composed experience
- Bug fixes before gate, not after

---

## Key Risks to Watch

| Issue | Risk Level | Mitigation |
|-------|------------|------------|
| #472 Slack OAuth | High (expect 2x expansion) | Sequence last; bounded by preceding stable work |
| #470 RBAC epic | High | Spec pipeline required; scope in spec |
| #706/#717 MUX epics | Medium | Wiring pass candidates |
| #247 AsyncSessionFactory | Medium | CXO flagged as "deceptively bounded" |

---

## Open Items

1. **#715 Conversation Lifecycle** — Added to Phase 3 as MUX wiring work. Confirm placement is correct.

2. **ADR drafting** — Architect recommended ADR-058 (Error Contract) and ADR-059 (Real-Time Architecture). Should these be M1 deliverables or pre-M2 work?

3. **Sprint duration** — M0 was 3 days core + 14 days polish. M1 planned for 4 weeks with explicit wiring phase. Adjust if needed based on early progress.

---

## Next Steps

1. **Lead Developer**: Begin Phase 1 when ready (#884 CANONICAL-RETEST first)
2. **CXO**: Prepare spec input for #706, #717 when Phase 2 begins
3. **Architect**: Prepare technical review for epics; confirm ADR timing
4. **PM**: Track progress, facilitate spec pipeline, coordinate B2 testing

---

*M1 Sprint Plan — March 11, 2026*
*Prepared by PPM with input from CXO and Chief Architect*
