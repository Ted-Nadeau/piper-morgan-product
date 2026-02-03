# MVP Sprint Issue Inventory

**Date**: February 1, 2026
**Purpose**: Master list for GitHub reorganization
**Action**: Create M0 issues, reassign existing issues to correct sprints

---

## M0 — Conversational Glue (NEW SPRINT)

**Theme**: Natural conversation flow
**Effort**: 15-25 days
**Status**: Issues to create

| Issue | Title | Effort | Action |
|-------|-------|--------|--------|
| NEW | GLUE-FOLLOWUP: Follow-up recognition with lens inheritance | 3-5d | CREATE |
| NEW | GLUE-MULTIINTENT: Multi-intent handling | 5-8d | CREATE |
| NEW | GLUE-SLOTFILL: Natural slot filling | 3-5d | CREATE |
| NEW | GLUE-MAINPROJ: Fix "main project" repeated question | 1-2d | CREATE |
| NEW | GLUE-SOFTINVOKE: Soft workflow invocation | 3-5d | CREATE |
| #102 | CONV-UX-GREET: Calendar scanning | - | MOVE to M0 |
| #488 | MUX-INTERACT-DISCOVERY | - | MOVE to M0 |

---

## M1 — MVP Foundation

**Theme**: Security + Testing + MUX fundamentals
**Status**: Reassign from current assignments

### Security (Keep in M1)
| Issue | Title | Notes |
|-------|-------|-------|
| #696 | BUG-AUTH: settings_integrations hardcoded user_id | P0 bug |
| #697 | BUG-AUTH: intent_service hardcoded user_id | P0 bug |
| #542 | SEC: Implement actual token revocation | |
| #470 | EPIC: SEC-RBAC Phases 4-5 | |
| #472 | EPIC: Slack Integration TDD Gaps | |

### Testing (Keep in M1)
| Issue | Title | Notes |
|-------|-------|-------|
| #190 | TEST-QUALITY: Test Reliability | |
| #352 | TEST-SMOKE-E2E: Core user journey | |
| #275 | TEST-SMOKE-BUG-BUS: ChromaDB/numpy | |
| #239 | BUG-TEST-CONFIG: Fix test_error_handling | |
| #247 | BUG-TEST-ASYNC: AsyncSessionFactory | |

### MUX Fundamentals (Keep in M1)
| Issue | Title | Notes |
|-------|-------|-------|
| #705 | MUX-LIFECYCLE-UI-B: Feature.to_dict() | |
| #706 | MUX-OBJECTS-VIEWS: Objects & Views | |
| #717 | MUX-PRODUCT-MODELING | |

### Infrastructure (Keep in M1)
| Issue | Title | Notes |
|-------|-------|-------|
| #305 | CORE-CONFIG-PIPER: PIPER.md config | |
| #306 | CONV-MCP-MEASURE: Token measurement | |
| #307 | CONV-UX-NAV: Global navigation | |
| #308 | INFR-DATA: Repository pattern | |
| #316 | UX-POLISH: Week 1 & 2 | |
| #317 | UX-TRANCHE3: Production polish | |
| #332 | DOCUMENTATION-STORED-PROCS | |
| #385 | INFR-MAINT-REFACTOR | |

### Defer to M6
| Issue | Title | Notes |
|-------|-------|-------|
| #358 | SEC-ENCRYPT-ATREST | MOVE to M6 (blocked) |
| #482 | SEC-KMS-INTEGRATION | MOVE to M6 (hardening) |

---

## M2 — MVP Activation

**Theme**: MUX Wiring + Infrastructure
**Status**: Reassign from current assignments

### MUX Wiring
| Issue | Title | Notes |
|-------|-------|-------|
| #683 | MUX-WIRE-DOD | Check if closed |
| #690 | WIRE-BOUNDARY | |
| #691 | WIRE-CANONICAL | |
| #692 | WIRE-SLACK | |
| #693 | WIRE-STANDUP | |
| #694 | WIRE-GITHUB | |
| #695 | WIRE-* (any remaining) | |
| #703 | MUX-LIFECYCLE-UI | |
| #707 | MUX lifecycle (check title) | |
| #714 | MUX lifecycle (check title) | |
| #715 | MUX lifecycle (check title) | |

### Infrastructure
| Issue | Title | Notes |
|-------|-------|-------|
| #557 | ARCH: WebSocket Infrastructure | Evaluate need |
| #167 | INFR-TEST (check status) | |

---

## M3 — MVP Skills

**Theme**: Canonical queries + Core skills
**Status**: Reassign from current assignments

| Issue | Title | Notes |
|-------|-------|-------|
| #704 | MUX-LIFECYCLE-UI-A: Morning Standup | After M0 architecture |
| #716 | MUX lifecycle (check title) | |
| #496 | Priority queries | #103 merged into this |
| #427 | MUX-IMPLEMENT-CONVERSE-MODEL | Phase 2 = follow-ups |
| #595 | Multi-intent handling | Verify status vs M0 |

### Skills-related
| Issue | Title | Notes |
|-------|-------|-------|
| TBD | Check for skills issues | |

---

## M4 — MVP Document Revolution

**Theme**: Document processing
**Status**: Keep as-is (coherent sprint)

| Issue | Title | Notes |
|-------|-------|-------|
| #712 | Document lifecycle (check title) | |
| #713 | Document lifecycle (check title) | |
| TBD | Check for other doc issues | |

---

## M5 — MVP Polish

**Theme**: Auth polish, Slack, remaining features
**Status**: Reassign from current assignments

| Issue | Title | Notes |
|-------|-------|-------|
| #146 | FLY-IMP: Three-tier pyramid | Check status |
| #147 | FLY-IMP: Handoff protocol | Check status |
| #148 | FLY-IMP: Configuration extraction | Check status |
| #143 | FLY-IMP: Performance benchmarking | May be closed |
| #118 | Multi-agent verification | Quick win |
| #304 | Notion Integration Activation | Quick win |
| #244 | (check title) | |
| #272 | (check title) | |
| #312 | (check title) | |

### Removed from M5 (deferred post-MVP)
| Issue | Title | Action |
|-------|-------|--------|
| #100 | Project Portfolio Awareness | DEFER post-MVP |
| #101 | Temporal Context System | DEFER post-MVP |
| #104 | Time Allocation Analysis | DEFER post-MVP |
| #106 | Strategic Recommendations | DEFER post-MVP |

### Merged
| Issue | Title | Action |
|-------|-------|--------|
| #103 | Priority Engine | MERGE into #496 |

---

## M6 — MVP Security Hardening

**Theme**: Security hardening + launch prep
**Status**: Collect deferred security issues

| Issue | Title | Notes |
|-------|-------|-------|
| #358 | SEC-ENCRYPT-ATREST | From M1 (blocked) |
| #482 | SEC-KMS-INTEGRATION | From M1 (hardening) |
| #372 | CORE-LEARN-PHASE-3 | |
| #375 | QA: Manual testing preference | |
| TBD | Launch blocker verification | |

---

## Post-MVP / Advanced Layer

**Theme**: Future enhancements
**Status**: Explicitly deferred

| Issue | Title | Notes |
|-------|-------|-------|
| #100 | Project Portfolio Awareness | From M5 |
| #101 | Temporal Context System | From M5 |
| #104 | Time Allocation Analysis | From M5 |
| #106 | Strategic Recommendations | From M5 |
| #688 | ADR-050 Phases 1-3 | Conversation graph |
| #698 | Guided Process: Planning | |
| #699 | Guided Process: Feedback | |
| #700 | Guided Process: Clarification | |
| #702 | MUX-LIFECYCLE-NOTIFICATIONS | |

---

## Quick Reference: Actions Summary

| Action | Count | Issues |
|--------|-------|--------|
| **CREATE** | 5 | M0 GLUE issues |
| **MOVE to M0** | 2 | #102, #488 |
| **MOVE to M6** | 2 | #358, #482 |
| **DEFER post-MVP** | 4 | #100, #101, #104, #106 |
| **MERGE** | 1 | #103 → #496 |
| **CLOSE** | 1 | #143 (verify) |
| **VERIFY STATUS** | ~10 | #683, #595, #146-148, etc. |

---

## Notes for Reorganization

1. **Create M0 sprint in GitHub** before creating issues
2. **Check issue statuses** before moving — some may already be closed
3. **Issues I couldn't definitively place** — come back for advice on these
4. **MUX lifecycle issues** (#703, #704, #705, etc.) — verify exact titles and dependencies
5. **#427 and #595** — may overlap with M0 work; verify scope

---

*Ready for GitHub reorganization*
*February 1, 2026*
