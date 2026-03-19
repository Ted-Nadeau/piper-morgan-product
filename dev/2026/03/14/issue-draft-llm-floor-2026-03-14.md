# LLM-FLOOR - Conversational Floor: Route Unmatched Queries to LLM with Context

**Priority**: P0
**Labels**: `enhancement`, `ux`, `M1`
**Milestone**: M1 (Foundation)
**Epic**: N/A — standalone, cross-cutting
**Related**: #888 (onboarding hijack), #889 (standup hijack), #884 (canonical retest), PDR-001, Pattern-062 (Assembly Assumption)

---

## Problem Statement

### Current State

When a user's message doesn't match any structured handler, Piper responds with a canned deflection:

> "I don't have that capability yet, but I'm learning! Try asking 'What can you do?' to see what I can help with."

This makes Piper **worse than a generic ChatGPT wrapper** for any request outside pre-built handlers. A zero-investment wrapper with a one-line system prompt ("You are a helpful PM assistant") would at least engage conversationally — ask clarifying questions, suggest frameworks, think through the problem with the user.

The current routing:

```
Message → Pre-classifier (regex) → [match?] → Canonical Handler
                                 → [no match?] → LLM Classifier
                                     → [known category + handler] → Workflow Handler
                                     → [UNKNOWN] → "I can't do that" ← THE WALL
```

The LLM is used to *classify* the message but not to *respond* to it. We spend LLM tokens deciding we can't help, then don't use the LLM to actually help.

### Impact
- **Blocks**: Every query outside structured handlers produces a dead-end experience
- **User Impact**: Critical — first-impression killer for new users. A user who asks a reasonable PM question and gets "I can't do that" will not come back to discover the structured handlers.
- **Technical Debt**: The longer this exists, the more it undermines the value of everything else we've built. The structured handlers are excellent — but users never reach them if their first unhandled query drives them away.

### Strategic Context

This issue was identified through a leadership roundtable on March 14, 2026 (PM, PPM, CXO, Chief Architect, CIO). All four leadership memos independently diagnosed the same problem and recommended the same fix. Convergence was unanimous — the strongest consensus signal since Ship #033's "Governance at Speed."

The diagnosis: **we built the ceiling (structured handlers) without the floor (LLM conversation).** The structured system should enhance a conversational baseline, not replace it. This is Pattern-062 (Assembly Assumption) manifesting at the product level — individually correct components (classifier, handlers, ProcessRegistry) composing into an incorrect experience for unmatched queries.

**Decision document**: `memo-ppm-roundtable-synthesis-2026-03-14.md` in project knowledge.

---

## Goal

**Primary Objective**: When no structured handler matches a user's message, Piper engages conversationally using the LLM with full user context — never producing a deflection or "I can't do that" response.

**Example User Experience**:
```
BEFORE:
User: "Can you help me manage the agents working on a coding assignment for me?"
Piper: "I don't have that capability yet! Try asking 'What can you do?'"

AFTER:
User: "Can you help me manage the agents working on a coding assignment for me?"
Piper: [Engages conversationally — asks about the assignment, suggests coordination
        approaches, offers to think through task breakdown, draws on PM knowledge.
        Responds as a knowledgeable PM colleague, not a tool with a menu.]
```

**Not In Scope** (explicitly):
- ❌ Learning intake loop (Piper grows new capabilities from unhandled queries) — that's M2–M3
- ❌ Fallback policy for partially-matched handlers (when a handler matches but can't complete) — separate design work, PPM/CXO to draft
- ❌ Changes to intent classification, pre-classifier, canonical handlers, or ProcessRegistry
- ❌ The LLM floor taking actions or calling integrations (see constraint below)
- ❌ New UI or visual indicators

---

## What Already Exists

### Infrastructure ✅
- LLM integration (Anthropic API) — already used for intent classification
- User context (conversation memory, user config, project data)
- Piper personality/voice system (system prompt, formality calibration)
- Ethics pipeline (CORE super ethics, trust computation, boundary checking)
- Intent classification pipeline with UNKNOWN category routing

### What's Missing ❌
- A conversational response path when UNKNOWN is the classification result
- Context injection into an unstructured LLM response (user profile, project state, conversation history, integration awareness)
- Instrumentation to track how often the floor is reached and what queries trigger it

---

## Requirements

### Phase 0: Investigation
**Objective**: Assess the current `_handle_generic_query` path and determine implementation approach.

**Tasks**:
- [ ] Examine current UNKNOWN routing — what code path executes when no handler matches?
- [ ] Assess what user context is available at the point where the deflection occurs (conversation history, user profile, project data, integration status)
- [ ] Confirm that the ethics/trust pipeline can wrap a general LLM response (not just structured handler output)
- [ ] Estimate engineering effort based on findings

**Deliverables**:
- Brief investigation note (comment on this issue) with findings and revised effort estimate

### Phase 1: LLM Conversational Floor
**Objective**: Replace the UNKNOWN deflection with a contextual LLM response.

**Tasks**:
- [ ] Create the LLM conversational response path as a new terminal node in the routing graph
- [ ] Route through the existing ethics and trust pipeline (non-negotiable — see constraints)
- [ ] Inject available context: user profile, conversation history, project data, configured integrations
- [ ] Craft system prompt for the floor path — Piper's PM identity, personality, and voice; honest about what it can and can't do; collaborative framing
- [ ] Ensure the floor does NOT take actions or call integrations (non-negotiable — see constraints)

**Deliverables**:
- Working LLM floor — any UNKNOWN query gets a conversational response
- System prompt for the floor path (for review)

### Phase 2: Instrumentation
**Objective**: Track floor usage to inform future handler development.

**Tasks**:
- [ ] Log when the floor is reached (query text, classification result, user context)
- [ ] Log floor response quality signals if available (conversation continued vs. abandoned)
- [ ] Ensure logging doesn't expose sensitive user data

**Deliverables**:
- Instrumentation in place — we can answer "how often do users hit the floor?" and "what are they asking?"

### Phase 3: Verification
**Objective**: Confirm the floor works correctly and doesn't introduce regressions.

**Tasks**:
- [ ] Test with queries from the canonical test suite that currently hit UNKNOWN
- [ ] Test with the specific screenshot query: "Can you help me manage the agents working on a coding assignment for me?"
- [ ] Verify ethics pipeline is active on the floor path (test with a query that should be refused)
- [ ] Verify no actions/integrations are triggered from the floor path
- [ ] Run full canonical retest to confirm no regressions on existing handlers
- [ ] Verify existing structured handlers still take priority over the floor (classifier match → handler, not floor)

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] Documentation updated (BRIEFING-CURRENT-STATE, architecture docs if relevant)
- [ ] GitHub issue fully updated
- [ ] Session log completed

---

## Non-Negotiable Constraints

### 1. Ethics Pipeline
**The LLM floor must route through the same CORE ethics, trust computation, and boundary checking pipeline as structured handlers.** The fallback path must not bypass these layers. This is an acceptance criterion, not an enhancement. A direct LLM API call that skips the ethics pipeline is a jailbreak vector and is not acceptable regardless of implementation convenience.

### 2. No Actions
**The LLM floor reasons conversationally — it does not take actions or call integrations.** The floor is "Piper thinking with you." Structured handlers are "Piper doing things for you." This constraint keeps scope bounded and preserves the clean distinction. If a user asks the floor to create a GitHub issue, Piper should discuss the issue with them and suggest they use the specific command/handler for that — not attempt to call the GitHub API.

---

## Acceptance Criteria

### Functionality
- [ ] Queries that currently produce "I don't have that capability" instead receive a contextual conversational response
- [ ] The floor response uses Piper's voice and personality (not generic LLM output)
- [ ] The floor response incorporates available user context (not a cold, context-free reply)
- [ ] Queries that match structured handlers still route to those handlers (floor doesn't intercept)
- [ ] The floor does not take actions, call integrations, or execute commands

### Safety
- [ ] The floor path routes through the existing ethics/trust pipeline
- [ ] A query that should be refused by ethics boundaries IS refused on the floor path
- [ ] No sensitive user data exposed in floor response logging

### Testing
- [ ] Screenshot query ("Can you help me manage the agents working on a coding assignment?") produces useful engagement
- [ ] Canonical retest shows no regressions on existing handlers
- [ ] At least 3 diverse UNKNOWN-category queries tested with useful responses

### Instrumentation
- [ ] Floor-hit events are logged (query, classification, timestamp)
- [ ] Data is available to answer "how often do users hit the floor?"

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| UNKNOWN → LLM routing | ⏸️ | |
| Ethics pipeline integration | ⏸️ | |
| Context injection | ⏸️ | |
| System prompt | ⏸️ | |
| No-actions constraint verified | ⏸️ | |
| Instrumentation | ⏸️ | |
| Canonical retest (no regression) | ⏸️ | |
| Screenshot query test | ⏸️ | |

---

## Testing Strategy

### Unit Tests
- Floor path returns LLM response (not deflection) for UNKNOWN category
- Floor path receives user context (conversation history, user profile)
- Floor path does not trigger action/integration calls
- Structured handlers still take priority when classifier matches

### Integration Tests
- End-to-end: unmatched query → classifier → UNKNOWN → LLM floor → response with context
- End-to-end: ethics boundary query → classifier → UNKNOWN → LLM floor → ethics refusal
- End-to-end: matched query → classifier → handler (not floor)

### Manual Testing Checklist
**Scenario 1**: The screenshot query
1. [ ] Send "Can you help me manage the agents working on a coding assignment for me?"
2. [ ] Verify response is conversational, contextual, and useful (not a deflection)

**Scenario 2**: Ethics boundary
1. [ ] Send a query that should be refused by Piper's ethics framework
2. [ ] Verify the floor path refuses appropriately (ethics pipeline active)

**Scenario 3**: Structured handler still works
1. [ ] Send a known canonical query (e.g., standup, project status)
2. [ ] Verify it routes to the structured handler, not the floor

**Scenario 4**: No actions from floor
1. [ ] Send "Create a GitHub issue for fixing the login page"
2. [ ] Verify Piper discusses the issue conversationally but does not attempt to call GitHub API

---

## Success Metrics

### Quantitative
- 0 queries produce "I don't have that capability" (or equivalent deflection)
- No regression in canonical test pass rate (currently 81.1% on implemented queries)
- Floor instrumentation operational and producing data

### Qualitative
- Piper feels like a knowledgeable PM colleague for any topic, not just pre-built handlers
- Alpha testers report Piper is "always useful, sometimes exceptional" (the CXO's formulation)

---

## STOP Conditions

**STOP immediately and escalate if**:
- The ethics pipeline cannot wrap a general LLM response path (architecture doesn't support it)
- Context injection requires changes to the core dispatch architecture (scope creep signal)
- The floor path is intercepting queries that should go to structured handlers (priority inversion)
- Performance of the floor path is significantly worse than structured handlers in ways that affect user experience
- Any indication that the floor bypasses trust/ethics boundaries

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Medium (architecturally bounded, but context injection and prompt work require care)

**Breakdown by Phase**:
- Phase 0 (Investigation): Small — assess existing code path
- Phase 1 (LLM Floor): Medium — routing change + context injection + system prompt
- Phase 2 (Instrumentation): Small — logging additions
- Phase 3 (Verification): Small-Medium — canonical retest + manual scenarios
- Documentation: Small

**Complexity Notes**: The routing change itself is bounded. The quality of the floor depends on the system prompt and how much context can be injected at the fallback point. The Lead Dev's Phase 0 investigation will determine whether context is readily available or requires plumbing work.

---

## Dependencies

### Required (Must be complete first)
- [ ] None — this can proceed immediately

### Beneficial (improves quality but doesn't block)
- [ ] #888 (onboarding hijack fix) — reduces noise in testing
- [ ] #889 (standup hijack fix) — same

---

## Related Documentation

- **Decision**: `memo-ppm-roundtable-synthesis-2026-03-14.md` — roundtable synthesis (ratified)
- **Input memos**: PPM, CXO, Architect, CIO roundtable memos (2026-03-14)
- **Architecture**: ADR-049 (conversational state), current routing in OrchestrationEngine
- **Patterns**: Pattern-062 (Assembly Assumption) — this is the product-level manifestation
- **Product**: PDR-001 (FTUX as First Recognition) — the floor is how Piper meets users who haven't triggered a handler yet
- **Principle**: "Piper is always at least as good as a well-prompted LLM with context. Structured handlers make it better, not different."

---

## Notes for Implementation

The Architect's routing diagram shows the change point clearly:

```
Current:  [UNKNOWN] → "I can't do that"
Proposed: [UNKNOWN] → LLM Conversational Response (with context, through ethics pipeline)
```

The floor is additive — it doesn't change any existing routing. It replaces a terminal dead-end with a terminal LLM call. Everything upstream (pre-classifier, LLM classifier, canonical handlers, ProcessRegistry) is untouched.

The system prompt for the floor path should establish Piper as a PM colleague who can think through any PM-related topic. It should NOT apologize for not having a specialized workflow. It should NOT suggest the user ask "What can you do?" It should just... help. The way a human colleague would.

CXO will provide voice guidance for floor responses (pending — how Piper distinguishes "thinking with you" from "doing for you"). Until that's available, use Piper's existing personality prompt and err toward collaborative, honest engagement.

---

**Remember**:
- Quality over speed (Time Lord philosophy)
- Evidence required for all claims
- No 80% completions
- PM closes issues after approval

---

_Issue created: March 14, 2026_
_Decision authority: PPM roundtable synthesis (ratified by PM)_
_Last updated: March 14, 2026_
