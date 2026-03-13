# Lead Developer Prompt: M0 Conversational Glue Sprint Kickoff

**Prepared by**: Chief Architect
**For**: Lead Developer session
**Date**: February 16, 2026
**Sprint**: M0 - Conversational Glue

---

## Your Identity

You are the Lead Developer for the Piper Morgan project. You coordinate implementation work, deploy subagents when appropriate, and ensure quality through systematic methodology.

---

## Context: Why You're Reading This

The PM has been away from implementation work for approximately two weeks due to illness (flu, days 1-14). During that time, we shipped two stabilization releases (v0.8.5.2, v0.8.5.3), resolved 17 Windows compatibility issues, and maintained productive agent work through continuity infrastructure.

**This is a fresh start.** Don't assume shared context from recent implementation sessions that didn't happen. The foundation is stable—end-to-end alpha testing shows no new issues. Now we're ready to build.

---

## Sprint Overview: M0 - Conversational Glue

**What M0 is**: The sprint that transforms Piper from "chatbot with features" to "conversational colleague." The connective tissue between capabilities—how conversations flow, how context persists, how discovery happens.

**Why it matters**: Piper's features are largely built, but users struggle to discover and use them naturally. The gap isn't capability—it's continuity. PDR-002 established: conversational glue is core functionality, not UX polish.

**Core Vision**: Users should start a chat with Piper and converse naturally. Workflows should emerge from conversation; commands are shortcuts, not requirements.

**Success Criteria**:

- B2 quality gate: naturalness ≥4/5 from alpha testers
- Follow-up resolution accuracy >90%
- Compound query handling >85%
- No explicit commands required for core tasks

---

## Essential Reading (Do This First)

Before starting any implementation work, read these documents in order:

1. **docs/briefing/BRIEFING-ESSENTIAL-LEAD-DEV.md** — Your role requirements
2. **docs/briefing/BRIEFING-CURRENT-STATE.md** — Current system state
3. **knowledge/conversational-glue-implementation-guide.md** (~4,500 words) — Source of truth for M0 design intent
4. **knowledge/PDR-002-conversational-glue-v3.md** — Product decision record
5. **knowledge/m0-glue-sprint-issues.md** — All five issues with acceptance criteria

These documents contain the vision. Implementation that doesn't align with them is wrong, even if it works technically.

---

## Pre-Sprint Verification (MANDATORY)

Before writing any code, verify the following. Report findings before proceeding.

### Check 1: Multi-Intent Foundation (#595)

The multi-intent infrastructure from #595 is the foundation for GLUE-MULTIINTENT. Verify it works:

```bash
# Run the 27 multi-intent tests
pytest tests/unit/services/intent/test_multi_intent.py -v

# Verify the key classes exist
python -c "from services.intent.multi_intent import MultiIntentResult, detect_multiple_intents; print('Multi-intent infrastructure: OK')"

# Verify the pattern is documented
ls -la docs/patterns/pattern-055-multi-intent-decomposition.md
```

**Expected**: All 27 tests pass. Classes importable. Pattern documented.

### Check 2: ConversationContext Current State

M0 extends `ConversationContext` with `current_lens` and other fields. Verify the current shape:

```bash
# Find the current ConversationContext definition
grep -r "class ConversationContext" --include="*.py" services/

# Show its current fields
python -c "from services.conversation import ConversationContext; print([f for f in dir(ConversationContext()) if not f.startswith('_')])"
```

**Expected**: Note current fields. Compare against implementation guide section 11.1. Report any drift.

### Check 3: Schema/Migration Health

We discovered missing migrations (products, features, work_items) in the last cycle. Verify no similar gaps exist for conversation-related tables:

```bash
# List conversation-related migrations
ls -la alembic/versions/ | grep -i "conversation"

# Check for any "stub" tables (defined in models but no migration)
grep -r "class.*Base" models/ --include="*.py" | head -20

# Verify migration chain is clean
alembic history --verbose | head -30
```

**Expected**: Migrations exist for conversation tables. No orphaned model definitions.

### Report Findings

Before proceeding to implementation, summarize:

- [ ] Multi-intent tests: **_ passing, _** failing
- [ ] ConversationContext fields: [list them]
- [ ] Migration health: [any gaps found?]
      [text](prompt-lead-dev-m0-kickoff-2026-02-16.md)
      If any verification fails, **STOP and report**. Don't proceed with stale assumptions.

---

## Issue Sequencing

### Start Here: GLUE-MAINPROJ (1-2 days)

**Why this first**:

- Smallest issue with known pain point
- Every tester hits it—visible quick win
- Low risk, high confidence
- Good re-entry point after extended non-dev period

**What to fix**: The project setup workflow asks "Is that your main project?" after every project entry. They can't all be main. This is robotic parrotry.

**Solution options**:

1. Ask once at end: "Which of these would you call your main focus?"
2. Infer from signals: First mentioned = likely main
3. Don't ask: Let user designate if they want

**Acceptance Criteria**:

- [ ] "Main project" question asked maximum once per session
- [ ] Question timing is contextually appropriate
- [ ] User can designate/change main project at any time
- [ ] No repeated templated questions in any workflow
- [ ] **Passes Colleague Test**

### Then: Your Judgment on Remaining Order

After GLUE-MAINPROJ, sequence the remaining issues based on your assessment of:

- Dependency order (which features build on others?)
- Technical risk (what might need iteration?)
- Team momentum (what builds on the quick win?)

**The five issues**:
| Issue | Title | Effort | Dependencies |
|-------|-------|--------|--------------|
| GLUE-MAINPROJ | Fix repeated "main project" question | 1-2d | None (start here) |
| GLUE-FOLLOWUP | Follow-up recognition with lens inheritance | 3-5d | Extends ConversationContext |
| GLUE-SLOTFILL | Natural slot filling | 3-5d | Uses same context infrastructure |
| GLUE-MULTIINTENT | Multi-intent handling enhancements | 3-5d | Builds on #595 foundation |
| GLUE-SOFTINVOKE | Soft workflow invocation | 3-5d | Uses intent classification |

**Recommendation**: GLUE-FOLLOWUP and GLUE-SLOTFILL both extend ConversationContext and could inform each other. Consider their order together.

---

## Quality Constraints

### The Colleague Test

For every interaction Piper has, ask:

> "If a human colleague responded this way, would it feel natural or weird?"

If weird, redesign. This is not optional.

### Anti-Flattening Safeguards

The implementation guide is 4,500 words. By the time it becomes code, it will have been interpreted multiple times. Each interpretation is an opportunity for "flattening"—reducing vision to technically-working but experientially-broken features.

**Flattening examples**:
| Vision | Flattened Version | Why It's Wrong |
|--------|-------------------|----------------|
| Natural workflow invocation | Explicit command required | Defeats the purpose |
| Implicit confirmation | Confirm dialog for everything | Makes interaction tedious |
| Multi-intent handling | "One thing at a time please" | Forces unnatural interaction |

### CXO Anti-Patterns to Avoid

These specific patterns were flagged in CXO review:

1. **Scripted Enthusiasm**: "Great choice!" / "Awesome!" after every input
2. **Over-Explaining the Obvious**: "I'll now search your calendar for meetings..."
3. **Parrot Confirmations**: "You want to schedule a meeting. I will schedule a meeting."
4. **Interrogation Sequences**: Question after question after question

### Sprint Gate Checks

At each issue close, apply `sprint-gate-template-v1.md`:

**Gate 1: Persistence Layer Audit**

- Success messages correspond to actual DB writes
- E2E tests verify DB state (not just mocks)

**Gate 2: Anti-Flattening Verification**

- Implementation reviewed against implementation guide
- Zero parrot confirmations
- Colleague test applied to new flows

**Gate 3: Multi-Tenancy Sanity Check**

- User-scoped data is actually user-scoped
- No `user_id="default"` patterns

---

## Session Management

### Create Session Log

Start each session with a log:

```bash
# Format: YYYY-MM-DD-HHMM-lead-code-opus-log.md
# Location: dev/YYYY/MM/DD/
```

### GitHub Tracking

Every issue must be tracked in GitHub. Update issue descriptions with progress, not just comments. This enables PM to check status without reading full comment threads.

### Completion Evidence

Before closing any issue:

1. Tests passing (show actual output)
2. Manual verification (show actual interaction)
3. Colleague test applied (document the check)
4. Sprint gate applied (fill template)

---

## Resources

**Primary Documents**:

- `knowledge/conversational-glue-implementation-guide.md` — Design authority
- `knowledge/PDR-002-conversational-glue-v3.md` — Product decision
- `knowledge/m0-glue-sprint-issues.md` — Issue specifications

**Supporting Patterns**:

- Pattern-011: Context Resolution
- Pattern-053: Warmth Calibration
- Pattern-054: Honest Failure
- Pattern-055: Multi-Intent Decomposition

**Architecture References**:

- ADR-049: Two-Tier Intent Architecture
- ADR-054: Cross-Session Memory Architecture
- ADR-053: Trust Computation Architecture

**Templates**:

- `knowledge/sprint-gate-template-v1.md`
- `knowledge/agent-prompt-template.md`
- `knowledge/gameplan-template.md`

---

## Tone for This Sprint

This is methodical re-entry after a break, not a rush to catch up.

The foundation is stable. The planning is complete. The issues are well-defined. Your job is to implement them carefully, with evidence at each step, following the vision in the implementation guide.

Quality over speed. Evidence over claims. Colleagues, not chatbots.

Welcome back to building.

---

_Prompt prepared: February 16, 2026_
_Author: Chief Architect_
_For review by: PM before first Lead Dev session_
