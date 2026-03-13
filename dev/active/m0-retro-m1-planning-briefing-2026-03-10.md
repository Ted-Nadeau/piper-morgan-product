# M0 Retrospective & M1 Planning Briefing

**To**: Chief Experience Officer, Chief Architect
**From**: Principal Product Manager
**Date**: March 10, 2026
**Re**: M0 Sprint Analysis + M1 Planning Input Request

---

## Purpose

M0 (Conversational Glue) shipped as v0.8.6 on March 4. Before we begin M1, we're conducting a brief retrospective to capture learnings and apply them to M1 planning.

**Request**: Please review this briefing and provide 3-5 recommendations from your role's perspective. PM will synthesize all inputs tomorrow morning.

---

## Part 1: M0 Retrospective

### Original Scope vs. Actual

| Metric | Planned | Actual | Ratio |
|--------|---------|--------|-------|
| Issues | 7 | 27 | 3.9x |
| Execution time | 13-22 days (est.) | 3 days (core) + 14 days (bugs/polish) | — |
| Tests added | — | 400+ | — |
| Commits merged | — | 56 | — |

### Original M0 Scope (7 issues)

```
✅ M0 - Conversational Glue - EPIC #762
   ├── ✅ GLUE-HISTORY-DIFF: Differentiate History sidebar from Conversation list
   ├── ✅ GLUE-FOLLOWUP: Follow-up recognition with lens inheritance
   ├── ✅ GLUE-MULTI: Multi-intent handling enhancements
   ├── ✅ GLUE-SLOT: Natural slot filling without interrogation
   ├── ✅ GLUE-PROJ: Fix "Is that your main project?" repeated question
   └── ✅ GLUE-SOFT: Soft workflow invocation from natural language
```

### How Issues Expanded (Assembly Assumption Pattern)

Each original issue discovered underlying infrastructure gaps. Here's the full expansion:

**GLUE-HISTORY-DIFF** expanded to:
- History Sidebar shows same data as Conversation List
- Bug: test_get_conversation_summary fails (coroutine mock)
- #858 SPEC: Conversation lifecycle specification (triggered 4-reviewer same-day approval)

**GLUE-FOLLOWUP** expanded to:
- In-memory stores keyed by session_id only, not user-scoped
- #854 SYSTEMIC: Cross-Turn State Continuity (became epic, 3 children)
- FORM-UNIFIED: Unified formality framework (80 tests)
- CONV-CONTEXT-OFFER: Track last offer for continuation
- Lens stack digression handling never called
- Lens extraction not wired into intent processing

**GLUE-MULTI** expanded to:
- Dead-end response patterns (no forward path)
- Lens issues (same as FOLLOWUP — shared root cause)
- #875 SYSTEMIC: Intent Pipeline Incompleteness (became epic)
  - BUG: Soft invocation not triggering (#767)
  - BUG: 'Open issues' classified as projects domain
  - GLUE-SOFTINVOKE: Pattern coverage gaps
  - INTENT-COVERAGE: Pre-classifier gaps
- BUG: 'Yes' confirmation interpreted as greeting
- UX: Tip suggests connecting already-connected integrations

**GLUE-SLOT** expanded to:
- Slot filling prompts not informed by lens context
- Slot filling module built but never integrated
- BUG: Slot-filling fails to extract entity name during onboarding

**GLUE-PROJ** expanded to:
- Architect note: entity tokens in response templates
- Bug: is_default not persisted during onboarding

**GLUE-SOFT** expanded to:
- Soft invocation confidence not boosted by lens context
- TrustStage hardcoded to BUILDING (real computation not connected)
- Soft invocation not applied to multi-intent responses
- BUG: Calendar settings showing connected for fresh account
- BUG: Calendar queries fail silently (led to #880)
- Soft offer accept/decline cycle not closed
- Formality/warmth system not unified
- Plus shared issues with MULTI

**New work discovered during implementation**:
- #848 EPIC: Repository as first-class domain entity (6 children)
  - Project integration CRUD API (#859)
  - Setup wizard repo-linking (#860)
  - Settings page integration management (#861)
  - Conversational handler for repo linking (#862)
  - Portfolio onboarding repo step (#863)
  - GitHub API repo validation (#867)
- #814: Setup requests trigger static guidance, not interactive onboarding

**Misc bugs found in testing** (late-stage discoveries):
- Dead-end response patterns
- TrustStage hardcoded
- BUG: Conversation not appearing in history sidebar (#840)
- 90+ failing unit tests from route refactoring (#868)
- Flaky test: test_verbosity_gradient (#870)
- BUG: Planning workflow returns raw error (#872)
- BUG: Workflow status surfaces raw timeout (#873)
- BUG: Issue soft invocation returns raw API error (#874)
- #875 SYSTEMIC: Nov 2025 refactor converted errors to HTTP 422
- #876 TECH-DEBT: 56 raw error messages leak to users (26 fixed)
- #878: Extraneous workflow polling (75 code paths, not 2)
- #879: create_issue() missing assignees parameter
- #880: Calendar credential 401 (16 fetch calls missing credentials)
- #849 SEC-KEYCHAIN: 15 non-scoped keychain paths

### Key Patterns Observed

1. **Assembly Assumption (Pattern-062)**: Individually correct components ≠ correct composition. Each "feature" contained 3-5 undiscovered infrastructure gaps.

2. **Green Tests, Red User (Pattern-045)**: 6,088 tests passed, but CXO B2 testing found 4 bugs on Mar 1. The gap between "tests pass" and "users succeed" is real.

3. **Audit Cascade Value**: When Lead Dev investigated #878 (appeared to be 2 code paths), they found 75. When they investigated #880 (appeared to be calendar), they found 16 fetch calls across 3 templates. Surface symptoms hide systemic issues.

4. **Same-Day Spec Approval**: #858 went through 4 reviewers (CXO → PPM → Architect → Lead Dev) in one day. Governance doesn't have to be slow.

---

## Part 2: M1 Current State

### Overview

| Metric | Value |
|--------|-------|
| Total issues | 29 |
| Done (cherry-picked from MUX/earlier) | 14 |
| Remaining | 15 |
| Blocked (deferred to M6) | 1 (#358 SEC-ENCRYPT-ATREST) |

### M1 Theme: Foundation (Security + Testing)

### Remaining Issues (15)

**Testing (5 issues)** — Bounded scope, lower expansion risk
| Issue | Title |
|-------|-------|
| #190 | TEST-QUALITY: Test Reliability for Production Confidence |
| #247 | BUG-TEST-ASYNC: AsyncSessionFactory event loop conflicts |
| #352 | TEST-SMOKE-E2E: Create core user journey smoke tests |
| #738 | TEST-INFRA: Enable Attention System Time Simulation Tests |
| #739 | TEST-FIX: Fix test_response_handler_observability |

**Security (3 issues)** — Medium expansion risk, #470 is an epic
| Issue | Title |
|-------|-------|
| #470 | EPIC: SEC-RBAC Phases 4-5 - Projects and Files Ownership |
| #482 | SEC-KMS-INTEGRATION: Migrate to AWS KMS |
| #542 | SEC: Implement actual token revocation on disconnect |

**Architecture (1 issue)** — High expansion risk, infrastructure change
| Issue | Title |
|-------|-------|
| #557 | ARCH: WebSocket Infrastructure for Real-Time Communication |

**MUX Follow-up (3 issues)** — Medium risk, depends on wiring
| Issue | Title |
|-------|-------|
| #705 | MUX-LIFECYCLE-UI-B: Feature.to_dict() lifecycle wiring |
| #706 | MUX-OBJECTS-VIEWS: Objects & Views Discovery Epic |
| #717 | MUX-PRODUCT-MODELING: Define Product Concept and Relationships |

**Slack (1 issue)** — Medium risk, OAuth gaps known from M0
| Issue | Title |
|-------|-------|
| #472 | EPIC: Slack Integration TDD Gaps - OAuth and Spatial Methods |

**Learning (1 issue)** — Medium risk, new subsystem
| Issue | Title |
|-------|-------|
| #372 | CORE-LEARN-PHASE-3: Implement Roadmap Phase 3 Learning Infrastructure |

**QA (1 issue)** — Low risk, manual work
| Issue | Title |
|-------|-------|
| #375 | QA: Manual testing for preference detection system |

### PPM's Preliminary Risk Assessment

**High expansion risk** (likely to follow M0's 4x pattern):
- **#557 WebSocket** — Infrastructure changes cascade. M0's #858 conversation lifecycle triggered the entire spec pipeline.
- **#470 RBAC epic** — Already scoped as epic. M0 taught us epics expand.

**Medium expansion risk**:
- **#472 Slack OAuth** — M0's keychain audit found 15 non-scoped sites. Slack was one. More may lurk.
- **#706, #717** — MUX epics have shown expansion patterns before.
- **#372 Learning** — New subsystem = unknown unknowns.

**Lower risk** (bounded scope):
- Testing issues (#190, #247, #352, #738, #739) — Fixing existing tests, not adding features
- #375 QA — Manual testing, bounded by definition

---

## Part 3: Questions for Role Reviews

### For Chief Experience Officer

From your UX and user experience lens:

1. **B2 Testing Learnings**: What did your Mar 1 testing reveal that we should carry forward? Which M1 issues are most likely to have "green tests, red user" gaps?

2. **User Journey Gaps**: Looking at M1's scope, are there user experience threads that M0 left incomplete? Should any M1 issues be re-prioritized based on what users will actually encounter?

3. **Colleague Test Risk**: Which M1 issues, if done wrong, would make Piper feel less like a colleague and more like a tool?

4. **Wiring Pass Candidates**: Which M1 features should get explicit wiring pass attention (Pattern-062) before we consider them done?

5. **Anything else** from your domain that M1 planning should account for?

### For Chief Architect

From your technical architecture and sustainability lens:

1. **Technical Debt from M0**: Did M0's velocity create architectural debt we should address in M1? Are there "we'll fix it later" decisions that are now blocking?

2. **Expansion Risk Assessment**: Do you agree with PPM's risk assessment above? Which issues do you see as most likely to expand, and why?

3. **Infrastructure Sequencing**: Should #557 (WebSocket) come early, late, or be split? What does it depend on, and what depends on it?

4. **Security Scope**: The security issues (#470, #482, #542) — are these bounded, or should we expect M0-style expansion?

5. **Architectural Guardrails**: What patterns or decisions from M0 should we lock in before M1 work begins? Any ADRs needed?

---

## Requested Output

Please provide a brief memo (can be informal) with:
- 3-5 recommendations for M1 planning from your role's perspective
- Any issues you'd add, remove, or re-sequence
- Specific concerns or risks you see that weren't captured above

PM will synthesize all inputs tomorrow morning for discussion.

---

*Briefing prepared by PPM, March 10, 2026*
