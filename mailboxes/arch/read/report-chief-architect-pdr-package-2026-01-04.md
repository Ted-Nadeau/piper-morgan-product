# Report: Product Decisions Requiring Architectural Review

**To**: Chief Architect
**From**: Principal Product Manager
**Date**: January 4, 2026
**Re**: PDR Package, ADR Requests, Measurement Infrastructure, Backlog Alignment

---

## Executive Summary

Three Product Decision Records have been drafted today, establishing foundational product principles for FTUX, conversational continuity, and multi-entity conversations. Each has architectural implications requiring review and potential ADR work.

Additionally, this report covers:
- Measurement infrastructure gaps for success criteria
- Canonical query tier alignment with roadmap
- Ted Nadeau's contribution path and architectural compliance expectations
- B2 quality gate establishment
- Suggested backlog reordering based on PDR priorities

**Action requested**: Review for feasibility, identify ADR needs, confirm infrastructure status.

---

## Part 1: PDR Package

Three PDRs are attached. Summary of architectural implications:

### PDR-001: First Contact is First Recognition (Draft v3)

**Product decision**: FTUX embodies recognition interface from moment zero. Not a wizard before the "real" experience.

**Architectural implications**:

| Area | Requirement | Current State? |
|------|-------------|----------------|
| Trust level initialization | Persist trust level from first interaction | Unknown |
| Hybrid form/conversation | Conversational wrapper around credential entry | Partial (setup wizard exists) |
| User preference storage | Name personalization, personality dimensions | ~75-80% per tech assessment |
| Cross-session greeting | Emotional context detection (abandonment signals) | New requirement |

**New feature flagged**: User rename capability (user can rename "Piper")—where does this live?

### PDR-002: Conversational Glue (Draft v2)

**Product decision**: Conversational continuity is first-class product feature. Three components: Discovery Glue, Context Glue, Proactivity Glue.

**Architectural implications**:

| Area | Requirement | Current State? |
|------|-------------|----------------|
| Cross-session memory | User preferences, project state, conversation history, trust level | Partial? |
| Trust computation | +1/0/-1 interaction outcomes, stage thresholds, regression | **ADR needed** |
| Anaphoric resolution | "It," "that," "the thing" → specific entities | Unknown |
| Proactivity triggers | Calendar events, GitHub activity, pattern recognition | Partial (standup exists) |

**Trust computation flagged for ADR** (see Part 2).

### PDR-101: Multi-Entity Conversation Support (Draft v2)

**Product decision**: Piper supports multi-entity conversations in two modalities—Host and Participant. Strategic stance: Participant-first.

**Architectural implications**:

| Area | Requirement | Current State? |
|------|-------------|----------------|
| Conversation-as-graph | Ted's element_nodes + element_links model | Not implemented |
| Multi-participant input | Handling input from multiple humans | Not implemented |
| Personal context per participant | What each person contributed/sees | Not implemented |
| Slack participation enhancement | Context ingestion, appropriate response, state persistence | Partial (basic Slack exists) |

**Ted's PRD (v0.3)** contains detailed PostgreSQL schema and data model. This needs architectural review before implementation. See Part 5.

---

## Part 2: ADR Requests

Based on PDR implications, three ADRs may be needed:

### ADR-047: Trust Computation Architecture (Priority: High)

**Triggered by**: PDR-002 v2

**Decision needed**: How is trust level computed, stored, and queried?

**Key requirements from PDR**:
- Interaction outcomes: +1 (successful), 0 (neutral), -1 (negative)
- Stage thresholds: ~10 for Stage 2, ~50 for Stage 3, extended history for Stage 4
- Regression: 3 consecutive negatives → drop one stage; 90-day inactivity → drop one stage (floor at Stage 2)
- Visibility: Computed, stored, queryable—but NOT surfaced in UI
- Discussable: If user asks "why did you do that?", Piper can explain trust-based behavior

**Questions for ADR**:
1. Where does trust live? UserContextService? New TrustService?
2. How do we detect "successful" vs "negative" interactions? What signals?
3. Is this per-user (global) or per-user-per-context?
4. For multi-entity (PDR-101): Is trust per-participant or per-conversation?

### ADR-048: Cross-Session Memory Architecture (Priority: High)

**Triggered by**: PDR-002 v2, PDR-001 v3

**Decision needed**: What persists between sessions? How long? How retrieved?

**Key requirements from PDR**:
- User preferences (communication style, technical depth, etc.)
- Project state (active integrations, recent activity)
- Conversation history (what was discussed, decided)
- Trust level (covered by ADR-047)
- Emotional context (session ended with frustration? abandonment?)

**Questions for ADR**:
1. What's the storage model? Key-value? Document? Structured?
2. What's the retention policy? Forever? Time-decay? User-controlled?
3. How do we distinguish "helpful memory" from "creepy surveillance"? (CXO "thoughtful colleague" test)
4. Privacy mode: Can user say "don't remember this session"?
5. Multi-device: If user switches devices mid-task, how does context transfer?

### ADR-049: Multi-Entity Conversation Architecture (Priority: Medium—depends on PDR-101 timeline)

**Triggered by**: PDR-101 v2, Ted's PRD v0.3

**Decision needed**: How does Piper implement conversation-as-graph model?

**Key questions**:
1. Is Ted's PostgreSQL schema compatible with Piper's existing data model?
2. Do we adopt, adapt, or parallel-implement?
3. How do personal agents (per-user) interact with facilitator agent (shared)?
4. What's the integration path for "one model, many views"?

**Recommendation**: Schedule architectural review session with Ted before ADR. His PRD is rich but needs translation to our patterns.

---

## Part 3: Measurement Infrastructure

PDR success criteria require metrics we may not currently collect. Please confirm status:

### From PDR-001 (FTUX)

| Metric | Target | Can We Measure Today? |
|--------|--------|----------------------|
| Time to first recognition pattern | < 30 seconds | Unknown |
| Configuration completion | > 80% minimum viable | Probably (setup wizard) |
| Unprompted discovery (30-day) | ≥ 3 features | Unknown |

### From PDR-002 (Conversational Glue)

| Metric | Target | Can We Measure Today? |
|--------|--------|----------------------|
| Cross-session reference accuracy | > 90% | Unknown |
| Anaphoric resolution success | > 85% | Unknown |
| Proactive suggestion acceptance | > 30% Stage 2, > 50% Stage 3 | Unknown |
| Trust progression | 50% reach Stage 2 within 30 days | Unknown (needs trust computation) |

### From CXO UX Report (B2 Quality Gate)

| Metric | Target | Can We Measure Today? |
|--------|--------|----------------------|
| "What can you help with?" satisfaction | > 4/5 | No (needs survey) |
| Dead-end recovery success | > 60% continue | Unknown |
| Feature tour skip rate | N/A | N/A (no feature tour) |

**Question**: What instrumentation exists today? What's needed? Is this blocking for alpha, or can we add incrementally?

---

## Part 4: Current Infrastructure Validation

The personalization technical assessment (Jan 4, 2026) indicated several gaps. Please confirm status:

| Area | Assessment Finding | Needs Validation |
|------|-------------------|------------------|
| Personalization system | ~75-80% complete | Is this accurate? What's the 20%? |
| Learning → Suggestion bridge | Infrastructure exists, end-to-end incomplete | What's missing? |
| Preference history | No audit trail of changes | Is this needed for trust computation? |
| Privacy/Advanced settings | "Coming soon" placeholder | Timeline? |
| PIPER.user.md | File-based config, not auto-generated | Part of onboarding flow? |

**Question**: Is personalization infrastructure sufficient for PDR-001 FTUX implementation, or are there blockers?

---

## Part 5: Ted Nadeau Coordination

Ted is empowered as a "small team" contributor with the following path:

```
Ted's internal docs (with ChatGPT)
    ↓
Translation to our vernacular (PPM helps)
    ↓
Architectural review ← YOU ARE HERE
    ↓
Vibe-coding / AI-assisted implementation
    ↓
PR submission
    ↓
Compliance check (Chief Architect)
    ↓
Integration
```

**Ted's PRD v0.3** includes:
- Full PostgreSQL schema (`users`, `conversations`, `element_node`, `message_links`, etc.)
- Detailed user stories with acceptance criteria
- Open design questions (versioning model, conflict resolution, LLM orchestration)

**Questions for you**:

1. **Pattern compliance**: What architectural patterns must Ted's code follow? DDD? Repository pattern? Service layer?

2. **Data model review**: Should we create an ADR from Ted's schema before he starts coding? Or review via PR?

3. **Integration points**: Ted's PRD references Calendar, GitHub, Jira, Notion, Google Docs. How do these map to our existing plugin architecture?

4. **Scope boundaries**: Where does "Ted's multi-entity feature" end and "Piper core" begin? Is there a clear interface?

**Recommendation**: 30-minute sync with Ted to review his PRD through architectural lens, before he proceeds to implementation.

---

## Part 6: Canonical Query Tiers & Backlog Alignment

Earlier today, we established canonical query tiers based on product priorities:

| Tier | Name | Queries | Current | Target |
|------|------|---------|---------|--------|
| 1 | Minimum Valuable PM Assistant | 14 | 86% | Alpha ✅ |
| 2 | Conversational Foundation | 8 | 25% | Beta (B2) |
| 3 | Integration Utility | 15 | 73% | Beta/v1.0 |
| 4 | Proactive Intelligence | 9 | 0% | v1.0/v1.1 |
| 5 | Team & Synthesis | 8 | 0% | v1.1+ |

**Key insight**: Tier 4 (proactive) depends on Tier 2 (discovery). Proactive features without conversational discovery feel intrusive.

### Backlog Alignment Observations

Looking at the current roadmap (screenshots reviewed):

**B2 - Beta Enablers** section aligns well with PDR-002:
- CONV-UX-GREET → Cross-session greeting (PDR-001/002)
- CONV-UX-PERSIST → Context Glue
- MUX-INTERACT-DISCOVERY → Discovery Glue
- FTUX-CONCIERGE → PDR-001 "onboarding IS the primer"

**Potential reordering considerations**:

1. **INTERACT-TRUST-LEVELS** appears in MUX-INTERACT (after B2), but trust gradient is foundational to B2 items. Should it move earlier?

2. **FTUX-CONCIERGE** may need scope revision—PDR-001 reframes this as "recognition pattern from moment zero," not a separate concierge feature.

3. **MUX-INTERACT-DISCOVERY** (#488) is correctly in B2—this is the discovery-oriented intent architecture that PDR-002 depends on.

**Question**: Should we schedule a backlog grooming session to align roadmap with PDR priorities? Or is current ordering sufficient?

---

## Part 7: B2 Quality Gate Definition

The CXO UX work established "B2" as a quality threshold, not just a milestone. PDR-002 codifies this:

> **B2 is a release criterion**: Features that work technically but fail the B2 conversational test are not ready for users.

**B2 Quality Assessment** (qualitative, not checklist):
- Does conversation feel natural or stilted?
- Does Piper remember what matters?
- Are proactive suggestions helpful or annoying?
- Can users discover capabilities without documentation?

**Question**: How do we operationalize this for release decisions?

Options:
1. **PM judgment call** with CXO input
2. **Alpha tester feedback threshold** (e.g., >4/5 on conversational quality)
3. **Formal B2 review gate** before features merge to production

**Recommendation**: Option 2 for alpha/beta, evolving to Option 3 for v1.0+.

---

## Summary of Requests

| # | Request | Priority | Response Needed |
|---|---------|----------|-----------------|
| 1 | Review PDRs for architectural feasibility | High | This week |
| 2 | Confirm ADR-047 (trust computation) needed | High | Yes/No + scope |
| 3 | Confirm ADR-048 (cross-session memory) needed | High | Yes/No + scope |
| 4 | Advise on ADR-049 (multi-entity) timing | Medium | Ted sync first? |
| 5 | Measurement infrastructure status | Medium | What exists today? |
| 6 | Personalization infrastructure validation | Medium | Confirm 75-80% |
| 7 | Ted coordination expectations | Medium | Pattern requirements |
| 8 | Backlog alignment recommendation | Low | Grooming session? |
| 9 | B2 quality gate operationalization | Low | PM call vs formal gate |

---

## Attachments

- PDR-001-ftux-as-first-recognition-v3.md
- PDR-002-conversational-glue-v2.md
- PDR-101-multi-entity-conversation-v2.md
- PDRs-README.md (new directory structure)
- Ted's NewApp PRD v0.3 (separate email)

---

*Looking forward to your review. The PDRs establish clear product direction—now we need architectural validation to proceed.*

— PPM
