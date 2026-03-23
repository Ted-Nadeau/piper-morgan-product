# Proposal: E2E Automated Testing + AAXT for Piper Morgan

**Author**: Lead Developer
**Date**: 2026-03-22
**Status**: Draft for PM review

---

## Executive Summary

We have solid unit test infrastructure (1325+ tests) and a working canonical retest script, but no automated end-to-end conversation testing. This proposal covers two complementary tracks:

1. **E2E Test Routines** — Deterministic, repeatable tests that verify task completion through the real HTTP API
2. **AAXT (Automated Agent-Experience Testing)** — LLM-as-judge evaluation of conversational quality, personality, and capability honesty

Together, they answer two different questions: "Does the system work?" (E2E) and "Is the system good?" (AAXT).

---

## Part 1: E2E Automated Test Routines

### What We Have

| Component | Status |
|-----------|--------|
| `tests/e2e/` — 7 test files using httpx AsyncClient + ASGI | Working |
| `canonical-retest-884.py` — 63 queries against live server | Working (manual) |
| CI pipeline — smoke gate → full suite → classification accuracy | Working |
| PostgreSQL test isolation via transaction rollback | Working |
| `e2e_client()`, `e2e_test_user()`, `e2e_auth_headers()` fixtures | Working |

### What's Missing

No E2E tests verify **multi-turn task completion**. Existing E2E tests check single request/response pairs (health, auth, project CRUD). Nobody tests: "Can a user create a todo, list it, complete it, and see it marked done — all through the chat endpoint?"

### Proposed E2E Test Routines

#### Routine 1: Task Lifecycle Smoke Tests

Tests that exercise full CRUD cycles through `/api/v1/intent`:

```
test_todo_lifecycle_e2e:
  1. POST "Add a todo: review deployment plan" → assert success, extract todo reference
  2. POST "Show my todos" → assert "review deployment plan" in response
  3. POST "Complete the deployment plan todo" → assert completion confirmed
  4. POST "Show all my todos" → assert marked as done

test_github_close_e2e:
  1. POST "Close issue #[test-issue]" → assert confirmation prompt with title
  2. POST "Yes, close #[test-issue]" → assert closed confirmation

test_reminder_e2e:
  1. POST "Remind me to check deploys tomorrow" → assert reminder confirmed
  2. Verify todo created in DB with reminder_date set
```

**Implementation**: Extend existing `e2e_client` fixture. Each test creates an isolated user, runs the conversation, verifies outcomes in both the API response AND the database.

**Cost**: Zero runtime cost (no LLM calls needed for verification). Runs in seconds via ASGI transport.

#### Routine 2: Canonical Conversation Suite (Automated)

Convert the manual `canonical-retest-884.py` into a proper pytest suite:

```
tests/e2e/test_canonical_conversations.py

@pytest.mark.parametrize("query,expected_category,expected_behavior", CANONICAL_QUERIES)
async def test_canonical_query(e2e_client, query, expected_category, expected_behavior):
    response = await e2e_client.post("/api/v1/intent", json={"message": query})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"]["category"] == expected_category
    # Behavior-specific assertions per query
```

**Why**: The canonical retest currently requires manually starting a server. As a pytest suite with ASGI transport, it runs in CI automatically.

#### Routine 3: Floor Routing Regression Tests

Verify that floor-routed categories actually produce LLM responses (not templates):

```
test_floor_produces_natural_response:
  For each floor-native category (GUIDANCE, DISCOVERY, TRUST, MEMORY, CONVERSATION):
    1. POST a representative query
    2. Assert response does NOT contain known template signatures
    3. Assert response length > 50 chars (not a stub)
    4. Assert response references context when available
```

#### Routine 4: Capability Boundary Tests

Verify Piper doesn't promise things it can't do:

```
test_unregistered_capability_honest_response:
  1. POST "Can you book me a flight?" → assert no offer to book flights
  2. POST "Send a Slack message to the team" → assert honest capability limitation
  3. POST "Deploy the latest build" → assert redirects, doesn't promise
```

### E2E Implementation Plan

| Phase | Work | Effort | Dependency |
|-------|------|--------|------------|
| **Phase 1** | Task lifecycle smoke tests (Routine 1) | 1 day | None — uses existing fixtures |
| **Phase 2** | Automated canonical suite (Routine 2) | 1 day | Extract query list from retest script |
| **Phase 3** | Floor regression + capability boundary (3-4) | 1 day | None |
| **Phase 4** | CI integration — add to GitHub Actions | 0.5 day | Phases 1-3 |

---

## Part 2: AAXT — Automated Agent-Experience Testing

### The Problem E2E Can't Solve

E2E tests verify *mechanics* (did the todo get created?). They can't verify *quality* (did Piper sound like a colleague? Was the response helpful? Did the conversation flow naturally?). That's what AAXT addresses.

### What AAXT Is

Using a second LLM ("the judge") to evaluate Piper's conversational quality against defined rubrics. The judge reads Piper's response and scores it on dimensions like naturalness, helpfulness, and personality consistency.

This isn't speculative — it's an established pattern. DeepEval, Promptfoo, and Langfuse all support it. Amazon, Anthropic, and most LLM-powered products use LLM-as-judge evaluation.

### Recommended Tool Stack

| Layer | Tool | Why |
|-------|------|-----|
| **Multi-turn evaluation** | DeepEval | Richest conversation eval support. Has `ConversationCompletenessMetric`, `RoleAdherenceMetric`, `KnowledgeRetentionMetric`. Pytest-native. |
| **Fast PR-level regression** | Promptfoo | Declarative YAML. Native GitHub Actions. Cheap (Haiku as judge). |
| **Production monitoring** | Langfuse (later) | Open-source tracing + async evaluation on real conversations. Phase 4. |

### AAXT Dimensions (Mapped to B1 Quality Rubric)

| Dimension | What It Tests | Judge Type |
|-----------|---------------|------------|
| **Flow** | Context retention across turns, pronoun resolution, topic tracking | LLM judge (multi-turn) |
| **Task Completion** | Can a simulated user achieve a goal? How many turns? Retries needed? | Agent-as-judge (simulated conversation) |
| **Recovery** | No dead ends. When user goes off-script, Piper offers alternatives | LLM judge (adversarial scenarios) |
| **Voice** | Personality consistency across domains (todos, GitHub, calendar, standup) | LLM judge (rubric-scored) |
| **Capability Honesty** | Only offers things in the dispatcher registry. Honest about limitations | Deterministic (cross-ref registry) + LLM judge |
| **Trust Awareness** | Proactivity matches trust stage. New users get less pushy behavior | LLM judge (persona-specific) |

### Concrete AAXT Test Scenarios

#### Scenario 1: Context Retention (Flow)
```
Turn 1: "What's the status of issue 42?"
Turn 2: [Piper responds about issue 42]
Turn 3: "Can you close that?"
Judge: Did Piper understand "that" = issue 42?
       Did Piper ask for the issue number again? (failure)
       Score: PASS if resolved correctly, FAIL if asked for clarification
```

#### Scenario 2: Full Lifecycle Simulation (Task Completion)
```
User simulator goal: "Create a todo, list todos, complete it"
User simulator persona: "Casual PM, uses natural language, no command syntax"

Simulated conversation runs 5-8 turns.

Judge evaluates:
  - Goal achieved? (binary)
  - Turns to completion? (count — fewer is better)
  - Unnecessary clarifications? (count — fewer is better)
  - Natural conversation flow? (1-5 scale)
```

#### Scenario 3: Mid-Flow Interruption (Recovery)
```
Turn 1: "Add a todo"
Turn 2: [Piper asks what the todo should say]
Turn 3: "Actually, what meetings do I have tomorrow?"
Judge: Did Piper handle the topic switch?
       Was the original flow recoverable?
       Did the user hit a dead end?
```

#### Scenario 4: Cross-Domain Voice (Personality)
```
Collect responses from 5 different domains:
  - Todo: "Add a todo: review PRs"
  - GitHub: "Show me open issues"
  - Calendar: "What's on my schedule?"
  - Guidance: "What should I focus on?"
  - Greeting: "Good morning"

Judge (single evaluation across all 5):
  Does Piper sound like the same person across all responses?
  Consistent warmth, professionalism, brevity?
  Any response sound robotic or like a different system?
```

#### Scenario 5: Capability Honesty (#923)
```
Turn 1: "Can you set up my Jira integration?"

Judge (cross-references dispatcher registry):
  Did Piper offer to set up Jira? (should not — not registered)
  Did Piper acknowledge the limitation honestly?
  Did Piper suggest alternatives?
```

### Cost Model

| Tier | When | Cost per run | Coverage |
|------|------|-------------|----------|
| **Deterministic** | Every PR | ~$0 | Mechanics, routing, classification |
| **Promptfoo + Haiku judge** | PRs touching conversation code | ~$1-5 | Intent regression, basic quality |
| **DeepEval + Sonnet judge** | Nightly | ~$5-20 | Full B1 rubric, multi-turn scenarios |
| **Full simulation + Opus judge** | Pre-release | ~$20-50 | Comprehensive experience validation |

### AAXT Implementation Plan

| Phase | Work | Effort | Dependency |
|-------|------|--------|------------|
| **Phase 1** | Install DeepEval, write 5 golden single-turn scenarios with B1 rubric metrics | 2 days | B1 rubric finalized |
| **Phase 2** | Add Promptfoo YAML configs for intent classification regression | 1 day | Canonical query list |
| **Phase 3** | Write 5 multi-turn simulation scenarios (lifecycle, interruption, recovery) | 3 days | Phase 1 |
| **Phase 4** | Capability honesty judge (cross-ref dispatcher registry) | 1 day | #923 registry |
| **Phase 5** | CI integration — Promptfoo on PRs, DeepEval nightly | 1 day | Phases 1-3 |
| **Phase 6** | Langfuse production tracing (deferred, needs user consent framework) | Future | Privacy framework |

---

## Recommendation

### Start With

1. **E2E Routine 1** (task lifecycle smoke tests) — immediate value, zero cost, uses existing infrastructure. This directly supports Gate 2 of #926.

2. **E2E Routine 2** (automated canonical suite) — converts manual retest into CI-gated regression. Supports Gate 3.

3. **AAXT Phase 1** (DeepEval + 5 golden scenarios) — gets LLM-as-judge infrastructure in place. Even 5 scenarios with a Sonnet judge will catch personality regressions and dead ends.

### Defer

- Langfuse production tracing (needs privacy/consent framework)
- Full simulation with user personas (wait until B1 rubric is battle-tested)
- Trust-stage-aware testing (complex, needs trust infrastructure to stabilize)

### Total Effort for "Start With" Items

~4-5 days of focused work. Could be spread across sessions.

---

## References

- [DeepEval Multi-Turn Evaluation Guide](https://deepeval.com/guides/guides-multi-turn-evaluation)
- [Promptfoo GitHub Action](https://www.promptfoo.dev/docs/integrations/github-action/)
- [Agent-as-a-Judge (arXiv)](https://arxiv.org/abs/2410.10934)
- [Anthropic Bloom — Behavioral Evaluation](https://github.com/safety-research/bloom)
- [Amazon: Evaluating Agentic Systems](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/)
- [LLM-as-a-Judge Guide — Evidently AI](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)
- [Langfuse LLM-as-Judge](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)
