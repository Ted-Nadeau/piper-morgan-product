# Memo: CXO Review — M1 Sprint Completion Gate #926

**To**: Lead Developer
**CC**: PPM, PM
**From**: CXO
**Date**: 2026-03-22
**Re**: Gate #926 review — experience bar, smoke tests, and missing criteria

---

## Overall Assessment

This is a strong gate — significantly better than the M0 gate template. The Lead Dev's instinct to flag the self-assessment risk ("I built the system and wrote the gate") is exactly right, and the gate structure shows genuine effort to verify outcomes rather than ticket closure. The "DRAFT FOR REVIEW" banner and the explicit call for outside perspective are the right posture.

I have additions and modifications across Gates 1 and 2, a structural suggestion, and answers to the cross-cutting questions.

---

## Gate 1: Conversation Quality — Additions and Modifications

### The 5 smoke test queries are too friendly

Every query in the current Gate 1 table is something the floor should handle well — they're all read-only, reflective, and conversational. A real user won't be that polite. The gate needs queries that test the boundaries, not just the center.

**Add these 3 harder queries:**

| Query | Expected Behavior | Why It's Hard |
|-------|-------------------|---------------|
| "Help me plan a stakeholder presentation for next week" | Floor engages with presentation planning — asks about audience, key points, timeline. Offers to create issues for action items. Does NOT say "I don't have that capability." | Tests an entirely unhandled capability. This is the screenshot query that started the floor inversion. If this doesn't work, the floor hasn't solved the problem. |
| "That's wrong, the meeting is on Thursday not Wednesday" | Floor accepts the correction naturally, adjusts if possible, doesn't get defensive or confused. | Tests error recovery and conversational repair. Many systems handle initial queries fine but fall apart when corrected. A colleague says "Oh right, Thursday — let me adjust." |
| "OK" | Meaningful continuation, not a dead-end or non-sequitur. If there's a pending offer, accept it. If there's nothing pending, ask what the user wants to do next. | Tests the affirmation handling that #922 addressed. This was a specific QA failure from PM testing on Mar 17. Single-word inputs are the hardest for structured systems. |

### Modify the Colleague Test criterion

The current gate says "5 sample queries tested against 'Would a human colleague respond this way?'" — but now we have a formal Colleague Test document with a scoring rubric. Reference it explicitly:

**Replace**: "Colleague Test: 5 sample queries tested against 'Would a human colleague respond this way?' standard"

**With**: "Colleague Test: All 8 smoke test queries scored using the Colleague Test rubric (colleague-test.md). Each must score 7+ (Pass). Any query scoring 0 on a single dimension is an automatic gate failure."

This gives the gate teeth. A vague "would a colleague respond this way?" lets evaluators be generous. A scored rubric with an auto-fail threshold does not.

### Add a "Fresh Account" criterion

The M0 experience taught us that tests pass on developer accounts but fail on fresh accounts. Add:

- [ ] **Fresh Account Verification**: All Gate 1 smoke tests run on a fresh account with no pre-seeded data, no prior conversation history, and default configuration. This is B2 testing — Pattern-045 (Green Tests, Red User).

---

## Gate 2: Task Lifecycle Completeness — Additions

### The smoke tests are correct but incomplete

The three smoke tests (todo lifecycle, GitHub close, reminder) verify the happy path. They don't verify what happens when things go wrong. A colleague doesn't just complete tasks — they handle confusion, partial information, and mistakes gracefully.

**Add these 2 smoke tests:**

| Test | Steps | Expected Outcome |
|------|-------|-----------------|
| Ambiguous todo completion | 1. "Add a todo: review the PR" 2. "Add a todo: review the deployment plan" 3. "Complete the review todo" | Piper asks which one — "I see two 'review' todos: 'review the PR' and 'review the deployment plan.' Which one?" Does NOT silently complete the wrong one. |
| GitHub close with wrong number | 1. "Close issue #99999" | Piper reports the issue wasn't found. Does NOT error out or give a system message. Colleague-level: "I couldn't find issue #99999 — want me to check if the number is right?" |

### Add a "Multi-Turn Completion" criterion

The Lead Dev asked if there are interaction patterns being missed. Yes — multi-turn task flows where the user has to go back and forth:

- [ ] **Multi-Turn Task Completion**: At least one smoke test verifies a task that requires 3+ turns to complete (e.g., creating an issue with title, then adding labels, then confirming). The floor should maintain context across turns, not lose track of what's being built.

---

## Structural Suggestion: Add a "Canonical Retest" Gate Criterion

The Lead Dev dropped the "Intent Classification Accuracy" gate because the floor made most classifier issues moot. That was the right call — classifier accuracy for read-only queries doesn't matter much under floor-first routing. But the canonical retest itself is still the best single measurement of overall system quality.

**Add to Gate 1 or as a standalone criterion:**

- [ ] **Canonical Retest Baseline**: Run the full canonical retest (canonical-retest-884.py) on a fresh account. Record pass rate. Must exceed 85% on implemented queries. (The PPM projected ~90%+ from floor routing alone — 85% gives margin while still being a meaningful bar.)

This connects the gate to the empirical measurement the PPM recommended and gives us a before/after comparison with Run 4 (81.1%).

---

## Cross-Cutting Questions

### Are four gates the right number?

**Yes.** The M0 gate had three (persistence, anti-flattening, multi-tenancy). This gate has four that map to M1's actual concerns. Conversation Quality and Task Lifecycle are the two user-facing gates; Architectural Integrity and Bug Debt are the two infrastructure gates. Clean split. Don't add more — the gate should be passable in a focused day of testing, not a week-long audit.

### Is anything missing entirely?

**Two things worth considering, neither essential:**

1. **Error path testing.** The gate tests happy paths and one ambiguity case (if my additions are accepted). It doesn't test what happens when integrations are down — "Create a GitHub issue" when GitHub isn't configured, "Check my calendar" when Calendar isn't connected. These should produce helpful floor responses, not errors. I'd add one error-path smoke test to Gate 1:

| Query | Expected Behavior | Category Route |
|-------|-------------------|----------------|
| "Create a GitHub issue about testing" (GitHub not configured) | Piper explains GitHub isn't connected yet and offers to help set it up, or suggests an alternative. NOT a raw error or "integration not configured." | EXECUTION → handler → graceful degradation |

2. **Documentation quality** — the Lead Dev mentioned this as a potential gap. I'd skip it for the gate. Documentation quality is important but it's a continuous concern, not a sprint gate criterion. The gate should verify the product works, not the docs.

### Flag from March testing sessions not captured

The **affirmation handling** bug from PM's March 17 QA testing ("Sure" → no workflow entered, "OK" → non-sequitur) is the most important user-facing issue from my sessions. It's addressed by #922 but I want to see it explicitly tested in the gate. The "OK" query I added to Gate 1 covers this.

---

## Summary of CXO Additions

| Gate | Addition | Type |
|------|----------|------|
| Gate 1 | 3 harder smoke test queries (unhandled capability, correction, affirmation) | New queries |
| Gate 1 | Reference formal Colleague Test rubric with 7+ threshold and auto-fail | Tighten criterion |
| Gate 1 | Fresh account verification requirement | New criterion |
| Gate 1 | Canonical retest baseline (≥85% impl pass rate) | New criterion |
| Gate 1 | Error path smoke test (unconfigured integration) | New query |
| Gate 2 | 2 additional smoke tests (ambiguous todo, wrong issue number) | New tests |
| Gate 2 | Multi-turn task completion criterion | New criterion |

Total: 4 new smoke test queries, 3 new criteria, 1 rubric tightening.

The gate is good as-is. These additions make it harder to pass by accident.

---

*CXO Gate Review | March 22, 2026*
