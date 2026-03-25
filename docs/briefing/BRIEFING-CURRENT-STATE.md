# BRIEFING-CURRENT-STATE.md - Where We Are Right Now

> **For current system state** (intent categories, plugins, patterns, architecture):
> **Use Serena symbolic queries instead of reading this file.**
> See `CLAUDE.md` "Live System State" section for query patterns.
> **This file focuses on sprint/epic position and methodology context.**

---

## STATUS BANNER

**Current Position**: 4.4.2 - M1 Sprint Active (Foundation) — Approaching Gate
**Version**: v0.8.6 (pyproject.toml source of truth)
**Last Updated**: March 24, 2026
**Current Focus**: M1 gate closure — Tiers 1-3 complete, gate #926 filed, PM-led items remaining
**Next Phase**: M1 gate execution → M2 (MVP Activation)

---

## Inchworm Position

```
1. ✅ The Great Refactor (GREAT)
2. ✅ CORE functionality
3. ✅ ALPHA testing (v0.8.0 → v0.8.4)
4. 🎯 Complete build of MVP
   4.1. ✅ B1 - Beta Enablers (v0.8.3.1, v0.8.3.2) - COMPLETE Jan 11
   4.2. ✅ A20 - Alpha Testing round 2 (v0.8.4.x) - COMPLETE Jan 18
   4.3. ✅ MUX: Modeled User Experience - COMPLETE Jan 27
   4.4. 🎯 MVP: Minimum Valuable Product (M0-M6) ← CURRENT
        ✅ M0: Conversational Glue — COMPLETE (v0.8.6, shipped Mar 4)
        🎯 M1: Foundation — APPROACHING GATE (~95%)
5. Beta testing on 0.9
6. Launch 1.0
```

---

## Recent Progress

### Mar 22-23 (M1 Tier 3 Complete + Product Concept)
- **Mar 22**: **M1 Tier 3 complete** — 4 capability issues closed in single Lead Dev session (#902 GitHub close/reopen, #903 reminders, #904 todo completion, #883 lazy workflow deferral). 76 new tests, 1325 total passing. Gate #926 filed. CXO + PPM independently reviewed gate criteria (fresh-account testing, Colleague Test rubric, 9 smoke queries). E2E + AAXT testing proposal written, 4 issues filed (#927-#930). **PDR-004 Experience Philosophy** ratified. Docs: agent-log CSV migration (877 sessions indexed), Ship process guide v1.1, publishing workflow one-pager.
- **Mar 23**: **#717 Product concept closed** — 4-role coordination chain (Architect validates schema, CXO recommends nav Option B, PPM revises to both-models approach, Lead consolidates and writes product-concept-model.md). Weekly docs audit: NAVIGATION.md refreshed, 5 indexes corrected, 2 broken links fixed. dev/active/ cleaned (deliverables filed to docs/).

### Mar 17-21 (Documentation + Automation)
- **Mar 17**: Briefing architecture repaired (8/12 files fixed — root cause: hardcoded counts instead of CURRENT-STATE refs). Publish-to-blog skill battle-tested (v0.2). Medium repatriation completed: 268/268 posts (100%) local. #922 conversation continuity bug filed.
- **Mar 18**: dev/active/ sort completed (80→12 files). Blog image matching: 134/168 posts matched (87% coverage). Memo delivery (7 memos + CIO questionnaire to 8 inboxes).
- **Mar 19**: **All 9 agent roles active** (first time). ADR-059 (Workflow Dispatcher) drafted, reviewed, approved, and implemented in one morning. ADR-060 (Floor-First Routing) created. Mailbox v3 built and validated same-day. Agent 360 questionnaire: 9/9 response rate. Blog pipeline: 269/269 posts with imageSlug (100%).
- **Mar 20**: 3 parallel sessions. Lead Dev M1 capability audits (#923 filed + closed, #924 filed + closed). Docs created `/create-omnibus` skill. Blog image localization: 175/269 (65%) — CDN rate-limited at 22 requests.
- **Mar 21**: Omnibus automation pilot (Dispatch v3→v4 eval loop). Retro omnibus eval completed (5 historical dates). Blog images: 269/269 localized (100%, 0 CDN). CoS proposals 2 & 3 applied.

### Mar 12-16 (M1 Sprint Execution)
- **Mar 12**: M1 kickoff. #884 canonical retest: impl pass rate 53.7%→81.1% via wiring fixes alone. Klatch AX testing piloted (ETA role). Chief of Staff chat retired (34 days).
- **Mar 13**: **Highest-activity day** — 12 sessions, 10 roles. Workflow hijack design sprint (CXO→PPM→Architect→impl in one day). #888/#889 closed. #886 contextual fallbacks. Lead Dev: 7 issues closed, 80+ new tests.
- **Mar 14**: "Are we doing it backwards?" roundtable. 4 leadership roles independently converged on identical diagnosis (layer inversion). LLM floor implemented same-day. E2E test infrastructure created (#352). Todo completion lifecycle (#904).
- **Mar 15**: Floor inversion investigation — PM testing revealed handlers catch messages before floor. Phase 1 GUIDANCE routing implemented. Comms 2-month chat retired. CIO methodology audit (10 recommendations).
- **Mar 16**: "Extend without verifying" systemic pattern discovered via PM QA. Action Registry (34 pairs) created. Leadership floor synthesis cycle. Editorial calendar unified (304 rows). 9 issues closed.

### Mar 10-11 (M1 Planning)
- **Mar 10**: M0 retrospective (7→27 issues, 3.9x expansion). M1 scope refined: #557 WebSocket deferred M2, #482 KMS deferred M2. Spec pipeline formalized.
- **Mar 11**: M1 sequenced into 4 phases. #715 promoted to M1. 4 issues created (#883-#886).

### Mar 3-9 (Post-M0 Consolidation)
- **Mar 4**: M0 gate #779 + GLUE epic #762 closed. v0.8.6 released (56-commit merge)
- **Mar 5-7**: Recovery period
- **Mar 8-9**: Ship #033, GitHub wiki (14 pages), dev/active/ cleaned

---

## SYSTEM CAPABILITY

> **Use Serena for live state**: `mcp__serena__find_symbol`, `mcp__serena__list_dir`

### Current Capabilities (March 2026)

**Intent Classification**: 19 categories
```python
# From services/shared_types.py IntentCategory enum
EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, PLANNING, REVIEW, LEARNING,
QUERY, CONVERSATION, IDENTITY, DISCOVERY, TEMPORAL, STATUS, PRIORITY,
GUIDANCE, TRUST, MEMORY, PORTFOLIO, UNKNOWN
```

**Active Integrations**: 7 plugins
- Slack (OAuth from Settings)
- GitHub (PAT configuration)
- Notion (API key in setup wizard)
- Google Calendar (OAuth from Settings)
- MCP (Model Context Protocol)
- Spatial (spatial intelligence)
- Demo (reference implementation)

**Architecture (M1 changes)**:
- **Floor-First Routing** (ADR-060): LLM conversational floor is default; canonical handlers handle actions. "Piper is always at least as good as a well-prompted LLM with context."
- **Workflow Dispatcher** (ADR-059): Registry-based dispatch replaces 3 competing offer/acceptance systems. Onboarding disabled (Gall's Law).
- **Action Registry**: 34 (category, action) pairs cataloged with `ActionDisposition` enum (CANONICAL, FLOOR, HANDLER, WORKFLOW)

**Pattern Catalog**: 63 patterns (001-062) across 8 families
- Completion Theater (045-049) - quality discipline
- Investigation & Root Cause (006, 041-043, 060) - debugging methodology
- Grammar Application (050-058) - consciousness, ownership, warmth
- Multi-Agent Coordination (029, 059, 010, 021, 037) - orchestration
- Core Architecture, Data & Query, AI & Intelligence, Integration & Platform

**ADRs**: 63 architectural decision records (ADR-059 through ADR-060 newest, plus adr-039 appendix removed)

**Skills**: 9 skills
- create-session-log, check-mailbox, close-issue-properly, audit-cascade, discovered-work-capture
- create-omnibus (new Mar 20), deliver-mail (new Mar 19), publish-to-blog (new Mar 16), narrative-verification

---

## What's Next: M1 Completion → M2

### M1 — IN PROGRESS (~80%)

**Completed M1 work** (Mar 12-16 sprint):
- #884 canonical retest (diagnostic baseline: 81.1% impl pass rate)
- #888/#889 workflow hijack fixes (escape commands, timeout, offer-first)
- #886 contextual fallbacks (8 CXO-authored messages)
- #901 classifier keywords (5 disambiguation fixes)
- #902 fuzzy close/reopen
- #904 todo completion lifecycle
- #907 conversational floor (LLM with assembled context)
- #911 floor inversion Phase 1 (GUIDANCE routing)
- #913 continuation rate (Phase 2 fixes)
- #914-#920 various wiring and infrastructure fixes
- #922 diagnosed (conversation continuity — ADR-059 implemented)
- #923 capability awareness gap (filed + closed)
- #924 chat avatars (filed + closed)
- ADR-059 (Workflow Dispatcher) + ADR-060 (Floor-First Routing) approved and implemented

**M1 Tier Status**:
- **Tier 1** (Architecture): ✅ Complete (#923 capability registry, #911 floor inversion, #907 conversational floor)
- **Tier 2** (Quality): ✅ Complete (#908 generic signaling, #909/#910/#898 audited and closed)
- **Tier 3** (Capabilities): ✅ Complete (#902 close/reopen, #903 reminders, #904 todo completion, #883 lazy workflow)
- **Tier 4** (PM-led): 🎯 In progress (#706 objects discovery — PM consolidation, #375 preference QA, #717 ✅ closed)
- **Gate**: #926 filed, CXO + PPM reviewed, 9 smoke queries defined

**Remaining for M1 closure** (3 items):
- #706 Objects & Views Discovery — PM-led consolidation of existing material
- #375 Preference Detection — manual testing with running server
- #926 Sprint Completion Gate — run gates, collect evidence, sign-offs

**Other open issues** (not M1-gated):
- #925 Floor inversion Phase 3-4 (STATUS/PRIORITY floor-first)
- #921 Framework upgrade (FastAPI/Starlette/httpx)
- #927-#930 E2E + AAXT testing track (filed Mar 22)

### MVP Milestones Overview

| Milestone | Focus | Status |
|-----------|-------|--------|
| M0 | Conversational Glue | ✅ COMPLETE (v0.8.6) |
| M1 | MVP Foundation | ~95% (gate #926 filed, 3 PM-led items remain) |
| M2 | MVP Activation | 4% |
| M3-M6 | Advanced Features | Backlog |
| DIST | Distribution | 0% (after M6) |

---

## Open Items by Priority

### Ready for Action
- #926 M1 Sprint Completion Gate — run gates, collect evidence
- #706 Objects & Views Discovery — PM consolidation
- #375 Preference Detection — manual QA
- #925 Floor inversion Phase 3-4

### Planning/Strategy
- IA Conference talk (April 17, Philadelphia) — 16-slide deck drafted
- Omnibus automation workflow (Dispatch pilot — Docs evaluating v3/v4 retro iterations)
- Weekly Ship process guide completed (v1.1, CoS piloting with Ship #036)
- Publishing workflow: blog-first migration planned (one-pager at `docs/internal/planning/comms/publishing-workflow-target.md`)
- E2E + AAXT testing: 4 issues filed (#927-#930), proposal written
- #717 Product concept: ✅ closed, design doc ready for M2

### Deferred
- #557 WebSocket (deferred to M2 per Architect)
- #482 KMS (deferred to M2)
- Mobile PoC (paused)
- DIST epic (#828 and children — after M6)

---

## Metrics Snapshot (March 24, 2026)

### Quality
- **Pattern Count**: 63 (001-062)
- **ADR Count**: 63 (through ADR-060, includes meta and field-mapping)
- **PDR Count**: 6 (001-004, 101)
- **Methodology Count**: 23 (00-22)
- **Skill Count**: 9
- **Test Suite**: ~6,538 tests collected, 1,325 intent service tests passing
- **Omnibus Logs**: Through Mar 23 (continuous daily coverage, 290 total)
- **Agent Sessions Indexed**: 877 (Jul 2025 – Mar 2026, 17 roles)

### Infrastructure (new since Mar 10)
- **Mailbox v3**: 10-role infrastructure with `/deliver-mail` skill
- **Blog Pipeline**: 269/269 posts (100% local, 0 CDN), `/publish-to-blog` skill v0.2
- **Omnibus Automation**: Dispatch pilot validated, `/create-omnibus` skill created
- **Agent 360**: First deployment complete (9/9 response rate), 7 cross-cutting themes identified

### Version History (Recent)
| Version | Date | Milestone |
|---------|------|-----------|
| v0.8.6 | Mar 4, 2026 | M0 Conversational Glue, 27 issues |
| v0.8.5.3 | Feb 11, 2026 | Windows compat, setup UX, 14 issues |
| v0.8.5.2 | Feb 6, 2026 | Alpha bug fixes, timezone alignment |
| v0.8.5.1 | Feb 1, 2026 | Timezone cascade fixes |
| v0.8.5 | Jan 27, 2026 | MUX-IMPLEMENT complete |

---

## Alpha Testing Focus

### What's Stable
- Setup wizard (GUI and CLI)
- Login/authentication
- Chat interface with 19 intent categories
- Conversational floor (LLM with assembled context for unmatched queries)
- Lists, todos, projects, files CRUD
- Integration Settings (Slack, Calendar, GitHub, Notion)
- Trust-appropriate proactivity
- Workflow escape commands and timeout

### What Changed (M1)
- Floor-first routing: unmatched queries get LLM conversational response instead of "I can't do that"
- Onboarding wizard disabled (Gall's Law — was hijacking sessions)
- Contextual fallback messages for unimplemented capabilities
- Action Registry gates which intents trigger handlers vs floor

### Known Issues
- #925 STATUS/PRIORITY still routed to canonical handlers instead of floor (Phase 3-4)
- #927-#930 E2E + AAXT testing track (filed, not yet started)

---

## Key Documents

**Roadmap**: `docs/internal/planning/roadmap/roadmap.md` (v14.3)
**Patterns**: `docs/internal/architecture/current/patterns/` (63 patterns)
**ADRs**: `docs/internal/architecture/current/adrs/` (63 ADRs, newest: ADR-059, ADR-060)
**PDRs**: `docs/internal/product/pdr/` (6 PDRs, newest: PDR-004 Experience Philosophy)
**Skills**: `.claude/skills/` (9 skills)
**Omnibus Logs**: `docs/omnibus-logs/` (continuous through Mar 23, 290 total)
**Mailbox Directory**: `mailboxes/DIRECTORY.md`
**Wiki**: `https://github.com/mediajunkie/piper-morgan-product/wiki`
**CITATIONS**: `docs/references/CITATIONS.md` (updated Mar 3)
**Glossary**: `knowledge/piper-morgan-glossary-v1.1.md`

---

*Last Updated: March 24, 2026*
*Source: Omnibus logs Mar 10-23, GitHub issue list, session logs, weekly audit #931*
