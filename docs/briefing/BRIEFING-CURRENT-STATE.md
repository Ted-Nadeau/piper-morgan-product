# BRIEFING-CURRENT-STATE.md - Where We Are Right Now

> **For current system state** (intent categories, plugins, patterns, architecture):
> **Use Serena symbolic queries instead of reading this file.**
> See `CLAUDE.md` "Live System State" section for query patterns.
> **This file focuses on sprint/epic position and methodology context.**

---

## STATUS BANNER

**Current Position**: 4.4.2 - M1 Sprint Active (Foundation)
**Version**: v0.8.6 (pyproject.toml source of truth)
**Last Updated**: March 21, 2026
**Current Focus**: M1 Sprint — Wiring fixes, floor-first routing, canonical handler completion
**Next Phase**: M1 gate closure → M2 (MVP Activation)

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
        🎯 M1: Foundation — IN PROGRESS (~80%)
5. Beta testing on 0.9
6. Launch 1.0
```

---

## Recent Progress

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

**ADRs**: 61 architectural decision records (ADR-059 and ADR-060 are newest)

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

**Remaining M1 issues** (3 open with M1 label):
- #902 CANONICAL-GITHUB-CLOSE
- #903 CANONICAL-REMINDERS
- #904 CANONICAL-TODO-COMPLETE

**Other open issues** (not M1-gated but tracked):
- #925 Floor inversion Phase 3-4 (STATUS/PRIORITY floor-first)
- #921 Framework upgrade (FastAPI/Starlette/httpx)
- #910 Pre-existing test failure
- #909 Hardcoded user name removal
- #908 Generic response signaling
- #898 Classifier edge cases (9 misroutes)
- #883 ARCH-LAZY-WORKFLOW

### MVP Milestones Overview

| Milestone | Focus | Status |
|-----------|-------|--------|
| M0 | Conversational Glue | ✅ COMPLETE (v0.8.6) |
| M1 | MVP Foundation | ~80% (3 canonical issues remain) |
| M2 | MVP Activation | 4% |
| M3-M6 | Advanced Features | Backlog |
| DIST | Distribution | 0% (after M6) |

---

## Open Items by Priority

### Ready for Implementation
- M1 remaining canonical handler issues (#902, #903, #904)
- #925 Floor inversion Phase 3-4

### Planning/Strategy
- IA Conference talk (April 17, Philadelphia) — 16-slide deck drafted
- Omnibus automation workflow (Dispatch pilot validated, calibration needed for HIGH-COMPLEXITY days)
- Weekly Ship process documentation (CoS Proposal 4)

### Deferred
- #557 WebSocket (deferred to M2 per Architect)
- #482 KMS (deferred to M2)
- Mobile PoC (paused)
- DIST epic (#828 and children — after M6)

---

## Metrics Snapshot (March 21, 2026)

### Quality
- **Pattern Count**: 63 (001-062)
- **ADR Count**: 61 (through ADR-060)
- **Skill Count**: 9
- **Test Suite**: ~6,190 tests (228 skipped — onboarding on ice per ADR-059)
- **Omnibus Logs**: Through Mar 20 (continuous daily coverage, 286 total)

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
- #922 Conversation continuity (affirmations/follow-ups misrouted — ADR-059 addresses)
- #925 STATUS/PRIORITY still routed to canonical handlers instead of floor
- #910 Pre-existing test failure (test_expired_token_returns_401)
- #898 9 classifier edge cases

---

## Key Documents

**Roadmap**: `docs/internal/planning/roadmap/roadmap.md` (v14.3)
**Patterns**: `docs/internal/architecture/current/patterns/` (63 patterns)
**ADRs**: `docs/internal/architecture/current/adrs/` (61 ADRs, newest: ADR-059, ADR-060)
**Skills**: `.claude/skills/` (9 skills)
**Omnibus Logs**: `docs/omnibus-logs/` (continuous through Mar 20)
**Mailbox Directory**: `mailboxes/DIRECTORY.md`
**Wiki**: `https://github.com/mediajunkie/piper-morgan-product/wiki`
**CITATIONS**: `docs/references/CITATIONS.md` (updated Mar 3)
**Glossary**: `knowledge/piper-morgan-glossary-v1.1.md`

---

*Last Updated: March 21, 2026*
*Source: Omnibus logs Mar 10-20, GitHub issue list, session log, Serena symbolic index*
