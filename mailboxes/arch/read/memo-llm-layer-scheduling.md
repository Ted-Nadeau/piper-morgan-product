# Memo: LLM Layer / Conversational Parsing Scheduling Question

**To**: Chief Architect, CXO, PPM
**From**: Lead Developer (Claude Code Opus)
**Date**: 2026-01-21
**Re**: Where is LLM-layer handling for multi-intent and conversational parsing scheduled?

---

## Context

While auditing the X1 sprint scope, we identified **#595 MUX-INTENT-MULTI** (multi-intent bug: "Hi Piper! What's on my agenda?" only handles greeting). The question arose: should we implement a proper fix now (~6h), or will upcoming LLM-layer work make that effort redundant?

---

## Investigation Findings

### Relevant Issues Identified

| Issue | Title | Status | Milestone |
|-------|-------|--------|-----------|
| **#427** | MUX-IMPLEMENT-CONVERSE-MODEL: Unified conversation model | OPEN | MVP |
| **#625** | GRAMMAR-TRANSFORM: Conversation Handler (Partial → Conscious) | OPEN | None |
| **#619** | GRAMMAR-TRANSFORM: Intent Classification (Partial → Conscious) | OPEN | None |
| **#488** | MUX-INTERACT-DISCOVERY: Discovery-Oriented Intent Architecture | OPEN | MVP |
| **#558** | MUX-STANDUP-CONVERSE: LLM-based preference extraction | OPEN | None |

### Key Architectural Documents

**ADR-049: Two-Tier Intent Architecture** (Status: Proposed, pending PM review)
- Tier 1 (Process-Level): Active conversations/processes checked FIRST
- Tier 2 (Turn-Level): Normal classification only if no active process
- This would help with onboarding derailment but NOT multi-intent

**ADR-050: Conversation-as-Graph Model** (Status: Proposed)
- ConversationNode types: MESSAGE, TASK, WHISPER, DECISION, QUESTION
- Enables multiple views: Timeline, Thread, Tasks, Decisions
- Infrastructure for richer conversation modeling

**ADR-045/046: Object Model & Moment.type Agents**
- Input decomposition into typed Moments → specialized listener agents
- This is the MUX grammar foundation we're implementing now

### Roadmap Position (v13.0)

```
Current Position: 4.2.1.1
4. MVP Track
   4.1. ✅ B1 - FTUX & Conversations (COMPLETE)
   4.2. 🎯 MUX-V1: Vision & Conceptual Architecture (NOW - X1 Sprint)
   4.3. MUX-V2: Integration & Learning
   4.4. MUX-INTERACT: Interaction Design  ← #488 DISCOVERY is here
   4.5. MUX-IMPLEMENT: UI Polish          ← #427 CONVERSE-MODEL is here
```

---

## The Gap

**#427 (Unified Conversation Model)** explicitly lists #595 as a related issue and identifies the same multi-intent problem:

> "Multi-intent messages: 'Hi Piper! What's on my agenda?' → only greeting handled"

**However**, #427 is in MUX-IMPLEMENT (Phase 4.5), which is several sprints away. The issue itself says:

> "Phase 1: Multi-Intent Parsing
> - Detect multiple intents in single message
> - Either handle all, chain handlers, or ask for clarification
> - Strip greeting phrases before classification (workaround) OR LLM decomposition"

So #427 envisions EITHER:
1. A workaround (greeting stripping) - could be done now
2. LLM decomposition - would come with full unified conversation model

---

## Options for #595

### Option A: Defer to #427 (MUX-IMPLEMENT phase)
- **Pro**: Proper LLM decomposition will handle this and many other cases
- **Con**: MUX-IMPLEMENT is 2-3 sprints away (Feb-March target per roadmap)
- **Con**: Bug persists for alpha testers during that time

### Option B: Implement Greeting Stripping Workaround Now
- **Pro**: Quick fix (2-3h), improves alpha experience immediately
- **Pro**: #427 mentions this as acceptable workaround
- **Con**: "Fragile" per #595 analysis
- **Con**: Technical debt that may be discarded when #427 lands

### Option C: Implement Proper Multi-Intent Parsing Now
- **Pro**: Solves the problem properly
- **Con**: Significant effort (6-8h) in large codebase (319KB intent_service.py)
- **Con**: May conflict with or be superseded by #427 architecture

### Option D: Close #595 as Duplicate of #427
- **Pro**: Acknowledges this is part of larger conversation model work
- **Pro**: Avoids wasted effort
- **Con**: Bug stays open in practice even if issue is closed/linked

---

## Questions for Leadership

1. **Scheduling**: When is MUX-INTERACT (#488 area) and MUX-IMPLEMENT (#427) scheduled to begin? The roadmap shows "February/March 2026 targets" but no specific sprint assignments.

2. **Priority**: Is the multi-intent bug impactful enough to warrant a workaround now, or can alpha testers tolerate it until #427?

3. **Architecture Direction**: Should #595 fixes align with ADR-049 (Two-Tier) or wait for full #427 implementation?

4. **Sprint Scope**: Should #595 remain in X1 (MUX-TECH), or be moved to a future sprint closer to #427 work?

---

## Recommendation

Based on investigation, my recommendation is:

**Option B + Linking**: Implement the simple greeting-stripping workaround (2-3h) to improve alpha UX, but explicitly link #595 to #427 and document that the proper fix comes with unified conversation model.

**Rationale**:
- Workaround is explicitly mentioned as acceptable in #427
- Effort is low (2-3h vs 6-8h for proper fix)
- Alpha testers get better experience now
- Full solution comes with #427 when scheduled
- No architectural debt since #427 will supersede this anyway

However, this is a PM/architecture decision that should be made by leadership rather than assumed at the implementation level.

---

## Additional Question: Conversational Glue

PM also asks: **Where is "conversational glue" planned?** Not just intent detection, but keeping the flow going naturally - the connective tissue that makes conversations feel coherent.

This may be broader than multi-intent and includes:
- Context carry-over between turns
- Natural follow-up handling ("How about today?" after asking about tomorrow)
- Graceful topic transitions
- Acknowledgment and confirmation patterns

**Potentially Related Issues**:
- #427 (Unified Conversation Model) - mentions turn-by-turn memory
- ADR-024 (Persistent Context Architecture) - preference hierarchy
- ADR-049 (Two-Tier Intent) - process-level context
- #625 (Conversation Handler Grammar Transform) - "lived dialogue" framing

**Request**: Please clarify where conversational glue work is scheduled, or if it needs explicit planning.

---

## Requested Decision

Please advise:
1. Should we proceed with workaround (Option B) or proper fix (Option C)?
2. Should #595 stay in X1 or move to a later sprint?
3. Any updates to scheduling for #427/MUX-INTERACT work?
4. Where is "conversational glue" in our plan?

---

## PM Initial Thoughts (7:51 AM)

- MUX-IMPLEMENT is the right sprint for #427 work
- Leaning toward **Option C** (proper multi-intent fix) - OK if superseded since it advances functionality
- Sharing memo with leadership for full reading
- Proceeding with clear work (#434, #435) while awaiting guidance

---

*Memo prepared: 2026-01-21 7:40 AM*
*Updated: 2026-01-21 7:51 AM with conversational glue question and PM initial thoughts*
