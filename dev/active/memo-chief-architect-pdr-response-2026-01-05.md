# Memo: Chief Architect Response to PDR Package

**To**: Principal Product Manager
**From**: Chief Architect
**Date**: January 5, 2026
**Re**: Response to PDR Package, ADR Requests, and Coordination Items

---

## Executive Summary

All three PDRs are architecturally feasible and well-aligned with existing infrastructure. The FTUX Gap Analysis (delivered today) has clarified immediate priorities. This response addresses your 9 requests and proposes concrete next steps.

---

## Part 1: PDR Architectural Feasibility

### PDR-001: First Contact is First Recognition ✅ FEASIBLE

**Architectural assessment**: The vision is achievable with existing infrastructure.

| Requirement | Infrastructure Status | Notes |
|-------------|----------------------|-------|
| Trust level initialization | ✅ UserPreferences model exists | Needs trust_stage field |
| Hybrid form/conversation | ⚠️ Setup wizard exists, needs conversational wrapper | Gap Analysis P0 item |
| User preference storage | ✅ 75-80% complete per tech assessment | Personality system solid |
| Cross-session greeting | ⚠️ Time-of-day only currently | Issue #102 addresses this |

**Recommendation**: P0 quick wins (Piper intro, empty states) can be implemented immediately. Larger FTUX redesign is Phase 2.

### PDR-002: Conversational Glue ✅ FEASIBLE

**Architectural assessment**: Core infrastructure exists; gaps are well-defined.

| Requirement | Infrastructure Status | Notes |
|-------------|----------------------|-------|
| Cross-session memory | ⚠️ Partial (session state exists, persistence incomplete) | Issue #314 addresses |
| Trust computation | ❌ Not implemented | See ADR discussion below |
| Anaphoric resolution | ⚠️ Basic entity tracking exists | Enhancement needed |
| Proactivity triggers | ✅ Standup, calendar integration exist | Pattern extensible |

**Recommendation**: B1 sprint items (#314, #488, #491) address the critical gaps. Trust computation can be implemented incrementally.

### PDR-101: Multi-Entity Conversation ✅ FEASIBLE (Phased)

**Architectural assessment**: Participant-first strategy is correct. Phase 1 (Slack enhancement) extends existing integration.

| Phase | Feasibility | Dependencies |
|-------|-------------|--------------|
| Phase 0: Methodology continues | ✅ Already happening | None |
| Phase 1: Participant Mode MVP | ✅ Feasible | Slack integration exists |
| Phase 2: Host Mode Foundation | ⚠️ Requires Ted sync | Data model decisions |
| Phase 3: Personal Agents | ❓ Future scope | Phase 2 learnings |

**Recommendation**: Schedule Ted architectural review before Phase 2 design. Phase 1 can proceed independently.

---

## Part 2: ADR Decisions

### ADR-047 & ADR-048 Status

Note: ADR-047 (Async Event Loop Awareness) and ADR-048 (Service Container Lifecycle) have already been drafted for different architectural decisions. Your request for Trust Computation and Cross-Session Memory would be **ADR-049** and **ADR-050**.

### ADR-049: Trust Computation Architecture

**Recommendation**: DEFER formal ADR until implementation begins.

**Rationale**:
- PDR-002 defines the *what* clearly (interaction outcomes, stage thresholds, regression rules)
- The *how* will emerge during implementation
- Creating an ADR now risks over-specifying before we learn from implementation

**Alternative approach**:
1. Add `trust_stage` field to UserPreferences model
2. Implement basic +1/0/-1 tracking in IntentService
3. Document architectural decisions as they emerge
4. Formalize ADR when patterns stabilize

**If you prefer an ADR now**: I can draft a lightweight version capturing PDR-002's requirements as architectural constraints, leaving implementation flexible.

### ADR-050: Cross-Session Memory Architecture

**Recommendation**: DEFER - covered by existing patterns.

**Rationale**:
- Session state management exists (ADR-006, ADR-047)
- UserPreferences model handles persistence
- Issue #314 (CONV-UX-PERSIST) will drive implementation
- ADR needed only if #314 reveals novel architectural decisions

### ADR-051: Multi-Entity Conversation Architecture

**Recommendation**: DRAFT AFTER Ted sync.

**Rationale**:
- Ted's PRD v0.3 contains detailed data model
- Architectural review needed to assess compatibility with Piper patterns
- ADR should document integration decisions, not duplicate Ted's work

**Proposed timeline**:
1. Ted architectural sync (this week or next)
2. ADR-051 draft (captures integration decisions)
3. Phase 2 design proceeds

---

## Part 3: Measurement Infrastructure Status

| Metric | Current Capability | Gap |
|--------|-------------------|-----|
| Time to first recognition | ❌ Not instrumented | Needs frontend event |
| Configuration completion | ✅ Setup wizard tracks | In place |
| Unprompted discovery | ❌ Not tracked | Needs capability usage events |
| Cross-session reference accuracy | ❌ Not measured | Needs evaluation framework |
| Anaphoric resolution success | ❌ Not measured | Needs test harness |
| Proactive suggestion acceptance | ⚠️ Partial (can track clicks) | Needs hint system first |
| Trust progression | ❌ Needs trust system | Blocked on implementation |

**Recommendation**:
- Implement hint system (#491) first - this enables suggestion acceptance tracking
- Add capability usage events as part of #488 (Discovery Architecture)
- Trust metrics follow trust implementation
- Formal measurement infrastructure is v1.0 scope, not blocking for alpha/beta

---

## Part 4: Personalization Infrastructure Validation

The 75-80% complete assessment appears accurate based on my review:

**Complete (75-80%)**:
- ✅ 4-dimension personality system (warmth, confidence, action, depth)
- ✅ Web UI at /personality-preferences
- ✅ Preference detection service (37 tests)
- ✅ UserPreferences model and persistence
- ✅ Intent service integration

**Incomplete (20-25%)**:
- ❌ Learning → Suggestion bridge (infrastructure exists, end-to-end incomplete)
- ❌ Preference change audit trail
- ❌ Privacy/Advanced settings ("Coming soon" placeholder)
- ❌ PIPER.user.md auto-generation

**Assessment**: Sufficient for PDR-001 FTUX implementation. Gaps are polish, not blockers.

---

## Part 5: Ted Nadeau Coordination

### Pattern Compliance Requirements

Ted's code must follow:

1. **Repository Pattern** (Pattern-001): Data access via repository classes
2. **Service Layer** (Pattern-002, Pattern-008): Business logic in services
3. **DDD Principles**: Domain models separate from persistence
4. **Router Architecture**: Integration access via routers (proven in #322)
5. **Test Requirements**: Unit tests for all new code

### Data Model Review Approach

**Recommendation**: Review via PR, not pre-ADR.

**Rationale**:
- Ted's PostgreSQL schema is detailed
- Integration decisions best made seeing actual code
- PR review catches compatibility issues
- ADR-051 documents decisions that emerge from review

### Integration Points

Ted's PRD references Calendar, GitHub, Jira, Notion, Google Docs. Current mapping:

| Ted's Integration | Piper Status | Notes |
|-------------------|--------------|-------|
| Calendar | ✅ Integrated | CalendarIntegrationRouter |
| GitHub | ✅ Integrated | GitHubIntegrationRouter |
| Notion | ✅ Integrated | NotionIntegrationRouter |
| Jira | ❌ Not implemented | Tech debt #546 |
| Google Docs | ❌ Not implemented | Future scope |

### Scope Boundary

**Where Ted's feature ends and Piper core begins**:
- Ted's multi-entity conversation is a **feature** within Piper
- It uses Piper's existing integration routers, intent service, and session management
- The conversation-as-graph model is **new capability**, not replacement of existing chat
- Interface: Ted's feature receives `ServiceContainer`, returns structured responses

---

## Part 6: Backlog Alignment

### Gap Analysis → B1 Mapping

| Gap | Severity | B1 Coverage | Action Needed |
|-----|----------|-------------|---------------|
| Gap 1: Form-First Setup | Critical | ❌ None | **New issue: FTUX-PIPER-INTRO** |
| Gap 3: Generic Empty States | Critical | Partial (#491) | **New issue: FTUX-EMPTY-STATES** |
| Gap 5: No Cross-Session Greeting | Significant | ✅ #102 | None |
| Gap 6: No Contextual Hints | Significant | Partial (#491) | Validate #491 scope |
| Gap 7: Preferences Not in FTUX | Significant | Partial (#490) | Validate #490 scope |
| Discovery Architecture | Critical | ✅ #488 | None |
| Context Persistence | Significant | ✅ #314 | None |

### Proposed B1 Additions

Three new issues to address P0 quick wins:

1. **FTUX-PIPER-INTRO** (1-2 hours): Piper greeting before setup Step 1
2. **FTUX-EMPTY-STATES** (2-3 hours): Voice guide templates in empty states
3. **FTUX-POST-SETUP** (2-3 hours): Orientation after setup completion

Total additional effort: ~7 hours. High impact on B1 quality rubric scores.

### Grooming Session Recommendation

**Not required** - current B1 issues + 3 new issues align well with PDR priorities. Suggest:
1. Create 3 new issues
2. Add to B1 sprint
3. Sequence: P0 quick wins first (raise floor), then feature work

---

## Part 7: B1 Quality Gate Operationalization

**Recommendation**: Option 2 (Alpha tester feedback threshold) for beta, evolving to Option 3 for v1.0+.

### Proposed B1 Gate Process

1. **Pre-Gate Evaluation**: PM + CXO assess against rubric (qualitative)
2. **Alpha Tester Sessions**: 2-3 testers complete 30-min evaluation per CXO spec
3. **Threshold**:
   - No dimension at 🔴 (0)
   - Total score ≥7/10
   - Alpha tester average ≥4/5 on "conversational naturalness"
4. **Decision**: PM makes final call with CXO input

### Evidence Requirements

Each B1 feature must demonstrate:
- Rubric dimension it addresses
- Before/after comparison (if applicable)
- Alpha tester feedback (if available)

---

## Summary: Action Items

| # | Item | Owner | Timeline |
|---|------|-------|----------|
| 1 | Create 3 P0 quick win issues | Chief Architect (this session) | Today |
| 2 | Validate #490, #491 scope against gaps | Lead Developer | B1 planning |
| 3 | Schedule Ted architectural sync | PM | This week |
| 4 | Draft ADR-051 after Ted sync | Chief Architect | Post-sync |
| 5 | Add trust_stage field to UserPreferences | Lead Developer | B1 |
| 6 | Implement hint system foundation | Lead Developer | B1 (#491) |

---

## Attachments

- FTUX Gap Analysis Report (January 5, 2026)
- ADR-047: Async Event Loop Awareness (approved)
- ADR-048: Service Container Lifecycle (accepted)

---

*Response prepared by Chief Architect*
*January 5, 2026, 9:00 PM PT*
