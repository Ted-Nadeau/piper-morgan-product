# Chief Architect Handoff Memo

**From**: Chief Architect (Outgoing)
**To**: Chief Architect (Successor)
**Date**: March 30, 2026
**Re**: Role Handoff — Tooling/Account Migration
**Chat Lifetime**: ~17 days (March 13-30, 2026), 8 sessions

---

## Context

PM is completing a tooling and account migration. You are receiving this handoff to ensure continuity. The PM will brief you on immediate priorities (including pending user acceptance testing); this memo provides architectural context and institutional knowledge from this chat's lifetime.

---

## Current State

### Where We Are

- **M0 (Conversational Glue)**: COMPLETE — v0.8.6, shipped March 4
- **M1 (Foundation)**: ~95% — Gates 3-4 verified, Gates 1-2 (UAT) pending
- **M2 (MVP Activation)**: Scoping — Product concept (#717) fully specified, Alembic migration pending
- **Roadmap**: Check BRIEFING-CURRENT-STATE.md for latest version

### M1 Gate Status

| Gate | Status | Notes |
|------|--------|-------|
| Gate 1 (User Acceptance) | PENDING | PM-led testing, not engineering |
| Gate 2 (User Acceptance) | PENDING | PM-led testing, not engineering |
| Gate 3 (Architectural Integrity) | 4/5 PASSED | G3.5 (multi-turn integration test) deferred to #927/#929 |
| Gate 4 (Bug Debt + Test Health) | PASSED | 6,310 tests, 0 failures, 228 skipped (onboarding per ADR-059) |

### Active Architectural Work

| Item | Status | Notes |
|------|--------|-------|
| Floor-first routing (ADR-060) | Phases 1-2 complete | Phases 3-4 deferred post-M1 (optimization) |
| Workflow dispatcher (ADR-059) | Implemented | Onboarding removed, dispatcher live, meeting slot-filling working |
| Product concept (#717) | Specified | Ready for M2 implementation (Alembic migration) |
| Piper Alpha (PA) | Briefing v0.2 ready | Launch-ready pending PM go-ahead |

---

## Key Architectural Decisions (This Chat's Lifetime)

### Created

| ADR/Document | Decision | Date |
|-------------|----------|------|
| ADR-060 | Floor-First Routing — LLM floor is default, handlers for side effects only | Mar 19 |
| ADR-059 review | Workflow Dispatcher — approved, 3 questions answered | Mar 19 |
| Product data model | 1:N Product↔Project approved, Feature bridge approved, cascade behavior specified | Mar 23 |
| PA technical constraints | Branch discipline, read-only codebase, conversational dispatch only | Mar 21 |

### Annotated

| Document | Annotation | Date |
|----------|-----------|------|
| ADR-039 | Routing philosophy superseded by ADR-060; infrastructure retained | Mar 19 |
| ADR-049 | Pending review; onboarding patterns on hold per ADR-059 | Mar 19 |

### Proposed (Not Yet Created)

| Item | Notes |
|------|-------|
| Pattern-063: Extension Without Integration | Sub-pattern of Assembly Assumption (062). Six bugs from same cause. Cross-pollination brief validates as structural. |
| ADR-049 amendment | Deferred until post-ADR-059 architecture stabilizes. Escape command infrastructure still needed for #889. |

---

## Patterns to Know

### ADR-060: Floor-First Routing ("The LLM is the floor, not the ceiling")

The most important architectural decision from this chat. The structured handlers (intent classification, canonical handlers, workflow factory) are the *ceiling* — they make specific interactions better than a generic LLM. But the *floor* is the LLM with full user context. When nothing structured matches, the user gets a conversational response, not a deflection.

**Action Gate criterion**: "Does this intent require an operation the LLM cannot perform within the floor response?" Three cases go to handlers: state mutations, multi-turn process initiation, narrow deterministic fast-path.

**Context Assembler**: Per-category `gather_context()` feeding the floor prompt. Declarative, fail-graceful, cached at assembler level (Redis with per-type TTLs).

### ADR-059: Workflow Dispatcher

Three independent offer/acceptance systems were racing for control of user affirmations. #922 was the symptom. The fix: remove onboarding (Gall's Law), add a thin registry-based dispatcher, consolidate. Onboarding disabled (228 tests skipped), `workflow_dispatcher.py` created.

**Onboarding is removed, not permanently deleted.** It may return in substantially redesigned form. The offer-first pattern from #888 is still the right activation model for when it comes back.

### Pattern-062: Assembly Assumption

Still the most load-bearing insight in the project. Individually correct components ≠ correct composition. The wiring pass is a required sprint phase. Extension Without Integration (proposed Pattern-063) is the specific mechanism by which this recurs.

---

## Working with the PM

xian values:
- **"Don't glaze me"** — honest assessment over agreement
- **Inchworm philosophy** — complete each phase 100% before advancing
- **Cathedral building** — quality over speed
- **Careful planning** — "I'd rather carefully talk it through, make a plan, and then execute it methodically"
- **Date boundary discipline** — one session log per calendar day, no exceptions
- **Coverage window discipline** — workstream memos must be strictly scoped to their window; date leakage is a recurring error to catch

The escape hatch is **"Time Lord alert!"** — use it when uncomfortable pushing back directly.

---

## Working with Other Roles

### Lead Developer
Primary implementation partner. Writes thorough proposals with clear questions. One pattern to watch: cross-references to other in-flight work sometimes missing from proposals (I flagged #888 overlap in ADR-059 review, and PDR-003 divergence in the #717 validation). Worth checking explicitly.

### PPM (Principal Product Manager)
Owns product direction. Strong synthesizer — the PPM roundtable synthesis memos are reliably accurate. PPM should take final pass on guidance memos to Lead Dev (product experience framing is more important than architectural precision for implementation guidance).

### CXO (Chief Experience Officer)
UX decisions. Productive disagreements are healthy (the #717 navigation debate produced a better outcome). The Colleague Test is now formalized as a methodology document.

### CIO (Chief Innovation Officer)
Innovation and methodology. Sent the PA technical constraints memo this chat received. Cross-pollination hub at designinproduct.com/internal/ is CIO territory.

### Chief of Staff (exec)
Coordinates across roles. Receives workstream reports. Synthesizes weekly Ships. Fact-checks claims against source logs — good quality gate.

---

## Pending Items

| Item | Status | Owner | Notes |
|------|--------|-------|-------|
| M1 Gates 1-2 (UAT) | Pending | PM | Not engineering — PM-led testing |
| Floor Phases 3-4 | Deferred post-M1 | Lead Dev | STATUS, PRIORITY, TEMPORAL-calendar, CONVERSATION |
| Post-migration canonical retest | After Phases 2-3 | Lead Dev | Validates ~90%+ floor routing pass rate projection |
| ADR-049 amendment | Deferred | Architect | Awaiting post-ADR-059 stabilization |
| Pattern-063 formalization | Proposed | Architect or CIO | Extension Without Integration |
| Product entity Alembic migration | M2 | Lead Dev | Schema approved, cascade behavior specified |
| Piper Alpha launch | Ready | PM | Briefing v0.2 complete, technical constraints approved |
| Older omnibus log review | Planned | Architect | Historical context — never got to this |
| Adaptive thinking evaluation | New | CIO or Lead Dev | From cross-pollination brief — effort parameter for floor routing |
| AXT adaptation for briefing fidelity | New | CIO or HOSR | From cross-pollination brief — Klatch methodology |

---

## Documents to Read First

1. **BRIEFING-ESSENTIAL-ARCHITECT.md** — Role briefing (updated March 19, includes floor-first routing)
2. **BRIEFING-CURRENT-STATE.md** — Project state (refreshed regularly)
3. **ADR-060** (`adr-060-floor-first-routing.md`) — The defining architectural decision of the current period
4. **ADR-059** (`adr-059-workflow-dispatcher-offer-consolidation.md`) — Workflow dispatch consolidation
5. **roadmap.md** — Current authoritative roadmap

---

## What Made This Chat Work

Eight sessions across 17 days. The most productive pattern: fast architectural review with clear yes/no answers and specific implementation guidance. The Lead Dev writes good proposals — don't spend time on things they've already thought through. Focus your reviews on what they might have missed (cross-references to other in-flight work, cascade implications, PDR divergences).

The roundtable pattern (parallel independent input → synthesis) is the project's strongest coordination mechanism. When it fires (March 14 floor roundtable, March 23 product model chain), decisions move from question to implementation in hours, not days.

Good luck with the UAT and the M2 transition.

---

*Chief Architect Handoff — March 30, 2026*
*Chat lifetime: 17 days, 8 sessions*
