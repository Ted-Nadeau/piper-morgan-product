# MVP Backlog Freshness Audit Report

**Prepared by**: Special Assignments Agent
**Date**: February 1, 2026
**Requested by**: PPM
**Status**: Complete

---

## Executive Summary

Audited 18 issues flagged for potential staleness. Findings:

| Recommendation | Count | Issues |
|----------------|-------|--------|
| **KEEP** | 3 | #167, #190, #191 |
| **UPDATE** | 5 | #118, #244, #272, #304, #312 |
| **MERGE** | 1 | #103 (merge into #496) |
| **DEFER** | 4 | #100, #101, #104, #106 (move to post-MVP) |
| **CLOSE** | 1 | #143 (already closed) |
| **PM Decision** | 3 | #146, #147, #148 |

**Key findings**:
- The "CONV-FEAT" series (#100-106) represents aspirational vision - move to post-MVP for later reevaluation
- #304 Notion integration: 78% complete code exists, just needs activation
- Test quality issues (#167, #190, #191) remain relevant - pytest has collection errors
- FLY-VERIFY hierarchy (#146-148) has partial infrastructure in `methodology/` but unclear completion status

---

## Summary Table

| Issue | Title | Recommendation | Rationale |
|-------|-------|----------------|-----------|
| #100 | CONV-FEAT-PROJ: Project Portfolio Awareness | **DEFER** | Move to post-MVP; aspirational vision worth preserving |
| #101 | CONV-FEAT-TIME: Temporal Context System | **DEFER** | Move to post-MVP; partially addressed by `datetime_utils.py` for now |
| #103 | CONV-FEAT-PRIOR: Priority Calculation Engine | **MERGE** | Merge into #496 (canonical priority queries); spec informs future enhancement |
| #104 | CONV-FEAT-ALLOC: Time Allocation Analysis | **DEFER** | Move to post-MVP; depends on #100, #101 foundations |
| #106 | CONV-FEAT-STRAT: Strategic Recommendations | **DEFER** | Move to post-MVP; capstone requiring CONV-FEAT foundations |
| #118 | INFR-AGENT: Multi-Agent Coordinator | **UPDATE** | Scripts exist (`scripts/deploy_multi_agent_coordinator.sh`); needs status verification |
| #143 | INFR-CONFIG-PERF: Performance benchmarking | **CLOSE** | Already CLOSED per GitHub |
| #146 | FLY-VERIFY: Verification Pyramid | **PM DECISION** | `methodology/verification/` exists; unclear if complete |
| #147 | FLY-VERIFY-HAND: Mandatory Handoff Protocol | **PM DECISION** | `methodology/coordination/` exists; unclear if complete |
| #148 | FLY-VERIFY-CONFIG: Configuration Layer | **PM DECISION** | Infrastructure exists; status unclear |
| #167 | INFR-TEST: Regression testing gaps | **KEEP** | Still relevant; test gaps exist |
| #190 | TEST-QUALITY: Test Reliability | **KEEP** | Still relevant; pytest collection has errors |
| #191 | POST-TEST-E2E: Web UI E2E Testing | **KEEP** | Still relevant; explicit post-MVP scope |
| #244 | CONV-UX-SLACK: Interactive Slack Features | **UPDATE** | Slack code exists (`services/integrations/slack/`); needs scope refresh |
| #272 | RESEARCH-TOKENS-THINKING | **UPDATE** | Research may still be valuable; needs PM decision on priority |
| #304 | CONV-INFR-NOTN: Notion Integration | **UPDATE** | Code EXISTS (35KB + 25KB); truly just needs activation |
| #312 | CONV-UX-DESIGN: Design System | **UPDATE** | `tokens.css` doesn't exist; work not done but still needed |

---

## Detailed Findings

### Issues to DEFER (Move to Post-MVP)

#### #100: CONV-FEAT-PROJ: Project Portfolio Awareness
**Current state**: `services/portfolio/` doesn't exist. Spec describes comprehensive multi-source project tracking.

**What changed**: Project pivoted to more focused canonical queries (#496, #497) for MVP. The full portfolio vision remains valid for future.

**Recommendation**: Defer to post-MVP milestone. Aspirational vision worth preserving for later reevaluation.

---

#### #101: CONV-FEAT-TIME: Temporal Context System
**Current state**: `services/temporal/` doesn't exist, but `services/utils/datetime_utils.py` was recently created (Feb 1, 2026).

**What changed**: Basic datetime utilities now available. Full "temporal intelligence" vision (calendar integration, deadline tracking, etc.) is broader than MVP needs.

**Recommendation**: Defer to post-MVP milestone. Vision is valuable; MVP addressed by simpler utilities.

---

#### #103: CONV-FEAT-PRIOR: Priority Calculation Engine
**Current state**: No `PriorityCalculationEngine` exists. Detailed multi-factor scoring algorithm spec from early development.

**What changed**: #496 (canonical priority queries) addresses the same user need ("What's my top priority?") with simpler implementation for MVP.

**Recommendation**: Merge into #496 for MVP scope. The complex algorithm spec can inform future enhancement of #496.

---

#### #104: CONV-FEAT-ALLOC: Time Allocation Analysis
**Current state**: Not implemented. Depends on #100, #101, #103.

**What changed**: Dependencies aren't being built in their original form for MVP. Foundation work deferred.

**Recommendation**: Defer to post-MVP milestone. Will be relevant when #100, #101 foundations are built.

---

#### #106: CONV-FEAT-STRAT: Strategic Recommendations
**Current state**: Not implemented. Described as "capstone requiring all previous UX-001 components."

**What changed**: The UX-001 component series isn't being built as originally envisioned for MVP. Strategic recommendations require the full intelligence stack.

**Recommendation**: Defer to post-MVP milestone. Capstone work that follows foundation components.

---

### Issues to CLOSE

#### #143: INFR-CONFIG-PERF: Performance benchmarking
**Current state**: CLOSED in GitHub.

**Recommendation**: Already closed. Remove from audit list.

---

### Issues to UPDATE

#### #118: INFR-AGENT: Multi-Agent Coordinator
**Current state**: Scripts exist:
- `scripts/deploy_multi_agent_coordinator.sh` (31KB)
- `scripts/validate_multi_agent_operation.sh` (15KB)

**What changed**: Scripts were created Aug 22, 2025. Issue says "Deploy operationally" but unclear if deployment happened.

**Recommendation**: Update issue to reflect current state. Verify if scripts have been run and coordinator is operational. May already be complete.

---

#### #244: CONV-UX-SLACK: Interactive Slack Features
**Current state**: `services/integrations/slack/` exists with substantial code (15+ files).

**What changed**: Slack integration infrastructure exists. Issue scope may be outdated - focuses on UI components but infrastructure is further along than issue suggests.

**Recommendation**: Update to reflect current state. May need to redefine scope as "polish" rather than "implement."

---

#### #272: RESEARCH-TOKENS-THINKING
**Current state**: Research proposal from Oct 2025. No implementation.

**What changed**: Research hasn't been conducted. Still potentially valuable for cost optimization.

**Recommendation**: Update with PM decision on whether to pursue. If yes, timeline it. If no, close.

---

#### #304: CONV-INFR-NOTN: Notion Integration
**Current state**: Code EXISTS and is substantial:
- `services/integrations/mcp/notion_adapter.py` (35KB)
- `services/intelligence/spatial/notion_spatial.py` (25KB)

**What changed**: Issue correctly identifies this as "activation task, not development." The 78% complete claim is accurate.

**Recommendation**: Update acceptance criteria to simple activation checklist. This is 1-2 days of work, not weeks.

---

#### #312: CONV-UX-DESIGN: Unified Design System
**Current state**: `static/css/tokens.css` doesn't exist. Design system work NOT done.

**What changed**: Issue is still accurate - work needs to happen. But should verify scope against current UI state.

**Recommendation**: Update to reflect current UI patterns. May need to assess what design tokens exist vs. what's needed.

---

### Issues to KEEP

#### #167: INFR-TEST: Review regression testing for gaps
**Current state**: Issue identifies specific regression gaps. Test collection currently shows errors.

**Recommendation**: Keep. Test quality issues are real and ongoing. May need refresh of specific regressions to investigate.

---

#### #190: TEST-QUALITY: Test Reliability for Production Confidence
**Current state**: Issue identifies mock pattern issues, integration test alignment, cache test infrastructure. Pytest collection has errors.

**Recommendation**: Keep. These issues directly affect CI/CD reliability. Estimated 11-16 hours total.

---

#### #191: POST-TEST-E2E: Web UI End-to-End Testing
**Current state**: Explicitly scoped as post-MVP. E2E testing framework not yet implemented.

**Recommendation**: Keep. Scope is appropriate as post-MVP enhancement.

---

### Issues Needing PM Decision

#### #146, #147, #148: FLY-VERIFY Hierarchy
**Current state**: `methodology/` directory exists with subdirectories:
- `methodology/verification/`
- `methodology/coordination/`
- `methodology/integration/`
- `methodology/testing/`

Infrastructure exists but unclear:
1. Are the verification pyramid components fully implemented?
2. Is the mandatory handoff protocol operational?
3. Has the configuration layer been extracted?

**Recommendation**: PM should verify implementation status before deciding KEEP, UPDATE, or CLOSE. These may be 75% complete patterns that need finishing, or they may be complete.

---

## Cross-Reference: Overlapping Work

| Old Issue | Overlaps With | Resolution |
|-----------|--------------|------------|
| #103 (Priority Engine) | #496 (Priority Queries) | Merge #103 into #496 |
| #100 (Portfolio) | Portfolio onboarding work | Close #100 |
| #101 (Temporal) | `datetime_utils.py`, Calendar integration | Close #101 |

---

## Implications for MVP Planning

### Move to Post-MVP Milestone
- #100, #101, #104, #106: Aspirational vision preserved for later reevaluation
- #103: Merge into #496 for MVP; full spec informs future enhancement

### Activation Wins
- #304 (Notion): 1-2 days to activate existing code
- #118 (Multi-Agent): May already be operational - verify

### Test Quality Priority
- #167, #190: Blocking MVP confidence if not addressed
- Pytest collection errors need fixing

### PM Decisions Needed
- #146-148: Verify methodology framework completion status
- #272: Research priority decision

---

*Report prepared February 1, 2026*
