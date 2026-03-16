# Routing Architecture Investigation Report: Floor Inversion

**Date**: 2026-03-15
**Investigator**: Architecture Investigator (Claude Code)
**Scope**: Research only — no code modifications

---

## 1. Current Architecture Summary

### Flow Diagram

```
User Message
      |
      v
[Pre-checks: soft offer, contextual continuation, guided process, pending onboarding, /standup, ethics]
      |
      v
[Multi-Intent Classifier] ──classify_multiple()──> MultiIntentResult
      |
      ├── 2+ substantive intents ──> IntentOrchestrator (parallel execution)
      ├── greeting + 1 substantive ──> primary intent + greeting prefix
      └── single intent ──> primary intent
      |
      v
[Canonical Handler Gate]
      |
      ├── intent.category in {IDENTITY, DISCOVERY, TEMPORAL, STATUS, PRIORITY,
      │    GUIDANCE, TRUST, MEMORY, PORTFOLIO, CONVERSATION}
      │         |
      │         v
      │    canonical_handlers.handle(intent)
      │         |
      │         v
      │    [Generic Response Check] ── _is_generic_canonical_response()
      │         |                              |
      │         ├── NOT generic ──> return     ├── IS generic ──> ConversationalFloor
      │         │   canonical result           │
      │
      ├── intent.category == QUERY ──> _handle_query_intent()
      │         (standup, projects, calendar, issues, PRs, etc.)
      │
      ├── intent.category == EXECUTION ──> _handle_execution_intent()
      │         (create issue, todos, etc.)
      │         └── unhandled action ──> _get_contextual_fallback()
      │              └── generic fallback ──> ConversationalFloor
      │
      ├── intent.category == ANALYSIS ──> _handle_analysis_intent()
      ├── intent.category == SYNTHESIS ──> _handle_synthesis_intent()
      ├── intent.category == STRATEGY ──> _handle_strategy_intent()
      ├── intent.category == LEARNING ──> _handle_learning_intent()
      │
      └── intent.category == UNKNOWN ──> ConversationalFloor (directly)
```

### The Signature-Matching Problem

`_GENERIC_CANONICAL_SIGNATURES` currently has only 3 entries. Any canonical handler that returns a template not on this list serves the template instead of routing to the floor. This is the whack-a-mole.

---

## 2. Design Doc Summary

### ADR-039: Canonical Handler Fast-Path Pattern (Oct 2025)
**Original intent**: Canonical handlers exist for SPEED. "Who are you?" should respond in ~1ms via config lookup, not 2-3s via LLM. Decision criteria: responses must be deterministic, simple data retrieval, no LLM needed.

**Reality vs. intent**: Many canonical handlers now violate these criteria. GUIDANCE synthesizes calendar + projects + priorities + time-of-day. STATUS fetches GitHub metadata. TEMPORAL calls the Calendar API. These are not ~1ms deterministic lookups.

### PDR-002: Conversational Glue (Jan 2026)
Key principle: "Piper is always at least as good as a well-prompted LLM with context. Structured handlers make it better, not different." This directly supports floor inversion.

### Conversational Glue Design Brief (Dec 2025)
Documents the "Current vs. Desired" gap. Current: "I can help you with various tasks." Desired: contextual, specific responses. The floor can deliver the desired experience. The canonical handlers deliver the current (bad) experience.

---

## 3. Handler Classification Table

| Category | What It Does | Actions? | Classification | Rationale |
|----------|-------------|----------|---------------|-----------|
| **IDENTITY** | Returns name, role, capabilities | READ only | **FLOOR WITH CONTEXT** | Floor can answer "who are you?" if given identity config |
| **DISCOVERY** | Lists capabilities from plugin registry | READ only | **FLOOR WITH CONTEXT** | Inject capability list; floor gives conversational response |
| **TEMPORAL** | datetime + calendar API | READ (calendar API) | **SPLIT** | Pure time → keep canonical. Calendar-heavy → floor with context |
| **STATUS** | Projects from DB, GitHub metadata | READ (DB + GitHub) | **FLOOR WITH CONTEXT** | Already slow. "No projects" → keep (triggers onboarding) |
| **PRIORITY** | Priorities from config, GitHub issues | READ (config + GitHub) | **FLOOR WITH CONTEXT** | Same as STATUS |
| **GUIDANCE** | Synthesizes calendar + projects + priorities | READ (multiple APIs) | **FLOOR WITH CONTEXT** | Worst offender. Template for ANY guidance query |
| **TRUST** | Trust profile from DB | READ (DB) | **FLOOR WITH CONTEXT** | Floor could handle with trust data injected |
| **MEMORY** | Conversation history | READ (memory/DB) | **FLOOR WITH CONTEXT** | Floor handles "what do you remember" more naturally |
| **PORTFOLIO** | Add/archive/delete/restore/search projects | **WRITE** (DB mutations) | **KEEP CANONICAL** | Takes real actions. Floor cannot do this |
| **CONVERSATION** | Greetings, farewells, thanks, chitchat | MIXED | **SPLIT** | Greeting with onboarding = KEEP. Chitchat/farewell/thanks = FLOOR |

### Summary
- **KEEP canonical**: PORTFOLIO (full), CONVERSATION (greeting/onboarding), STATUS (no-projects trigger), TEMPORAL (pure time)
- **FLOOR with context**: IDENTITY, DISCOVERY, TEMPORAL (calendar), STATUS (with projects), PRIORITY, GUIDANCE, TRUST, MEMORY
- **FLOOR pure**: CONVERSATION (chitchat, farewell, thanks)

---

## 4. Inversion Proposal

### Architecture: Floor-First with Canonical Bypass

```
User Message
      |
      v
[Pre-checks: guided process, pending offers, ethics, etc.]
      |
      v
[Classifier] ──> intent (category, action, confidence)
      |
      v
[Action Gate] ── Does this intent require a SIDE EFFECT?
      |                    (DB write, API call that changes state,
      |                     starting a multi-turn process)
      |
      ├── YES ──> Canonical/Workflow Handler (unchanged)
      │            - PORTFOLIO mutations
      │            - EXECUTION (create issue, manage todos)
      │            - Onboarding triggers
      │            - Slot filling
      │
      └── NO ──> [Context Assembler]
                       |
                       v
                  Gather relevant data based on intent category:
                  - IDENTITY: Piper config, plugin capabilities
                  - TEMPORAL: datetime, calendar summary
                  - STATUS: project list, GitHub metadata
                  - PRIORITY: priority list, high-priority issues
                  - GUIDANCE: calendar + projects + priorities
                  - TRUST: trust profile data
                  - MEMORY: conversation history
                  - CONVERSATION: conversation history, user prefs
                  - QUERY (read-only): query-specific data
                  - UNKNOWN: conversation history only
                       |
                       v
                  [Conversational Floor]
                  System prompt = Piper identity
                                + floor guidelines
                                + assembled context data
                                + conversation history
                       |
                       v
                  LLM generates response
```

### Key Design Decisions

1. **Action Gate replaces generic-response detector.** Decide BEFORE execution whether the handler is needed. Question: "Does this intent require a side effect the LLM cannot perform?"

2. **Context Assembler is the new abstraction.** Each category gets `gather_context()` returning structured data for injection into the floor prompt.

3. **Floor prompt must not parrot its instructions.** Rewrite to be directive about behavior without quotable self-description phrases.

4. **Canonical handlers shrink to action-only.** PORTFOLIO, EXECUTION, CONVERSATION greeting stay. Everything else becomes context-gathering feeding the floor.

### Migration Path

- **Phase 1**: GUIDANCE (worst offender, most generic)
- **Phase 2**: IDENTITY, DISCOVERY, TRUST, MEMORY (low-risk, no side effects)
- **Phase 3**: STATUS, PRIORITY, TEMPORAL-calendar (data-heavy, higher risk)
- **Phase 4**: CONVERSATION refactor (keep greeting/onboarding, floor the rest)

---

## 5. Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| 1 | Latency regression for simple queries | HIGH | MEDIUM | Accept for most (already make API calls). Keep fast-path for pure time queries |
| 2 | LLM cost increase | HIGH | LOW-MED | Already paying for classification. Floor can use cheaper model |
| 3 | Response quality inconsistency | MEDIUM | MEDIUM | Acceptable for conversation. Context injection ensures data accuracy |
| 4 | Context assembler misses data | MEDIUM | HIGH | Implement incrementally, mirror current handler reads |
| 5 | Onboarding/action triggers lost | HIGH | HIGH | Action Gate checks state-dependent triggers, not just category |
| 6 | Floor prompt parroting | MEDIUM | MEDIUM | Rewrite prompt to "do X" not "you are X" |
| 7 | Breaking existing tests (126+) | HIGH | MEDIUM | Known migration cost, tests need updating |
| 8 | Regression on TEMPORAL sub-handlers | MEDIUM | MEDIUM | Keep agenda/retrospective/duration canonical short-term |

---

## 6. Open Questions (Need PM/Leadership Input)

1. **Speed vs. quality for IDENTITY**: "Who are you?" is currently instant. Is 2s LLM acceptable?
2. **Context assembler scope**: How much data per category? Too little = vague. Too much = slow + costly.
3. **Floor model selection**: Same model as classification, or cheaper/faster?
4. **Monitoring/rollback**: How do we measure floor responses are better? Need quality signal.
5. **CONVERSATION onboarding detection**: Where do action-trigger checks live in new architecture?
6. **Multi-intent orchestration**: If handlers become floor calls, does orchestration still work?
7. **Contextual fallback copy** (`_get_contextual_fallback()`): "I can't do X but can do Y" — keep hardcoded or let floor generate?

---

## Key Files Referenced

| File | Description |
|------|-------------|
| `services/intent/intent_service.py` | Main router, 9400+ lines |
| `services/intent_service/canonical_handlers.py` | All canonical handlers, 5571 lines |
| `services/intent_service/conversational_floor.py` | Floor implementation, 272 lines |
| `services/conversation/conversation_handler.py` | CONVERSATION handler with onboarding |
| `services/shared_types.py` | IntentCategory enum (18 categories) |
| `docs/internal/architecture/current/adrs/adr-039-canonical-handler-pattern.md` | ADR for dual-path design |
| `docs/internal/product/pdr/PDR-002-conversational-glue.md` | Conversational glue as first-class |
| `docs/internal/design/briefs/conversational-glue-design-brief.md` | UX gap documentation |
