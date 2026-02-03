# M0 — Conversational Glue Sprint Issues

**Sprint**: M0 - Conversational Glue
**Milestone**: MVP
**Labels**: `glue`, `mvp-critical`, `pdr-002`
**Total Effort**: 13-22 days (reduced from 15-25 — #595 complete)
**Reference**: PDR-002 v3.1, conversational-glue-implementation-guide.md
**Reviews**: ✅ CXO Approved | ✅ Architect Approved

---

## Epic: GLUE - Conversational Glue Implementation

**Title**: EPIC: GLUE - Conversational Glue Implementation
**Type**: Epic
**Priority**: P0

### Description

Implement conversational glue patterns per PDR-002 v3 to enable natural conversation flow. This is the MVP critical path that transforms Piper from "chatbot with features" to "conversational colleague."

**Vision**: Users should be able to start a chat with Piper and converse naturally. Workflows should emerge from conversation; commands are shortcuts, not requirements.

**Success Criteria**:
- B2 quality gate passes (naturalness ≥4/5 from alpha testers)
- Follow-up queries resolve correctly >90%
- Compound queries handled coherently >85%
- No explicit commands required for core tasks

**Child Issues**:
- [ ] GLUE-FOLLOWUP
- [ ] GLUE-MULTIINTENT
- [ ] GLUE-SLOTFILL
- [ ] GLUE-MAINPROJ
- [ ] GLUE-SOFTINVOKE

---

## Issue 1: GLUE-FOLLOWUP

**Title**: GLUE-FOLLOWUP: Follow-up recognition with lens inheritance
**Type**: Feature
**Priority**: P0
**Effort**: 3-5 days
**Labels**: `glue`, `mvp-critical`, `pdr-002`

### Description

Implement robust follow-up recognition that carries forward the conversational "lens" (what aspect the user is asking about), not just the topic.

**Current State**:
- Pattern-011 provides partial anaphoric reference resolution
- #427 MUX-IMPLEMENT-CONVERSE-MODEL Phase 2 addresses follow-ups
- Current implementation loses lens across turns

**Problem Examples**:
```
User: "What's on my calendar tomorrow?"
Piper: "You have 3 meetings: standup at 9, 1:1 at 11, planning at 2."
User: "What about Thursday?"
Current: "What would you like to know about Thursday?"  ← WRONG
Expected: Shows Thursday's calendar  ← RIGHT
```

**Requirements**:

1. **Lens Tracking**
   - Track current conversational lens (calendar, issues, projects, etc.)
   - Carry lens forward until explicitly changed
   - Support multiple active lenses for compound contexts

2. **Reference Types to Handle**
   - Pronouns: "it," "that," "the meeting"
   - Elliptical phrases: "And Sarah?" → "What about Sarah's availability?"
   - Comparative queries: "What about tomorrow instead?"
   - Temporal references: "earlier," "next week," "the one before that"

3. **Implementation**
   - Extend `ConversationContext` with `current_lens` field
   - Add lens inference from previous turn
   - Integrate with intent classification to bias interpretation

**Acceptance Criteria**:
- [ ] "What about X?" queries inherit lens from previous turn >90%
- [ ] Elliptical phrases expand correctly >85%
- [ ] Comparative queries resolve to correct comparison >85%
- [ ] Lens persists across at least 3 follow-up turns
- [ ] Explicit topic change resets lens appropriately
- [ ] **Passes Colleague Test**: Would a colleague respond this way?

**Related Work**:
- #427 MUX-IMPLEMENT-CONVERSE-MODEL (Phase 2)
- Pattern-011 Context Resolution
- ADR-049 Intent Architecture

---

## Issue 2: GLUE-MULTIINTENT

**Title**: GLUE-MULTIINTENT: Multi-intent handling enhancements
**Type**: Feature
**Priority**: P0
**Effort**: 3-5 days (reduced — #595 provides foundation)
**Labels**: `glue`, `mvp-critical`, `pdr-002`

### Description

Extend the multi-intent infrastructure from #595 to handle more complex compound queries with execution planning and response aggregation.

**Foundation from #595** (COMPLETE):
- ✅ `MultiIntentResult` dataclass with primary/secondary intent separation
- ✅ `detect_multiple_intents()` in PreClassifier (scans all pattern groups)
- ✅ `classify_multiple()` in IntentClassifier
- ✅ Handle-all strategy in IntentService
- ✅ 27 tests in `test_multi_intent.py`
- ✅ Pattern-055 documented

**What #595 handles well**:
```
"Hi Piper! What's on my agenda?" → Greeting + Calendar (working)
```

**What needs extension**:
```
"Update the sprint status and check if we're on track for the deadline"
"What's my calendar look like, and did the PR get merged?"
```

These require:
- Multiple substantive intents (not just greeting + substantive)
- Dependency ordering between intents
- Aggregated response from multiple handlers

### Requirements (Building on #595)

Per Chief Architect guidance: **Use Orchestration Layer approach** (handlers stay single-intent)

1. **Orchestration Layer** (NEW)
   ```python
   class IntentOrchestrator:
       async def execute(self, result: MultiIntentResult) -> AggregatedResponse:
           plan = self.create_execution_plan(result.intents)
           results = await self.execute_plan(plan)
           return self.aggregate_responses(results)
   ```

2. **Execution Planning**
   - Identify parallel vs. sequential execution needs
   - Handle cases where intents share context
   - Cap at reasonable limit (3-4 intents max)

3. **Response Aggregation**
   - Single coherent response (not sequential outputs)
   - Natural transitions between intent responses
   - Clear indication if any part failed

### Acceptance Criteria
- [ ] "X and Y" with two substantive intents handled correctly >90%
- [ ] Execution order respects dependencies
- [ ] Single coherent response returned
- [ ] Partial failures handled gracefully
- [ ] Performance impact <200ms additional latency
- [ ] **Passes Colleague Test**: Would a colleague respond this way?

### Related Work
- #595 Multi-intent handling ✅ COMPLETE — foundation
- Pattern-055 Multi-Intent Decomposition ✅ Documented
- ADR-049 Intent Architecture

---

## Issue 3: GLUE-SLOTFILL

**Title**: GLUE-SLOTFILL: Natural slot filling without interrogation
**Type**: Feature
**Priority**: P0
**Effort**: 3-5 days
**Labels**: `glue`, `mvp-critical`, `pdr-002`

### Description

Transform slot filling from sequential interrogation to natural conversation that accepts multi-slot input and only asks for genuinely missing information.

**Current State**:
- Slot filling asks questions in rigid sequence
- Ignores information already provided
- Creates "interrogation" feel

**Problem Examples**:
```
BAD (current):
User: "Set up a meeting with Sarah Tuesday at 2pm"
Piper: "What's the meeting about?"
User: "Q3 planning"
Piper: "Who should attend?"  ← Already said Sarah!
User: "Sarah"
Piper: "When should it be?"  ← Already said Tuesday 2pm!

GOOD (expected):
User: "Set up a meeting with Sarah Tuesday at 2pm"
Piper: "Got it—meeting with Sarah, Tuesday at 2pm. What's the topic?"
User: "Q3 planning"
Piper: "Done—Q3 planning with Sarah, Tuesday at 2pm."
```

**Requirements**:

1. **Multi-Slot Input Parsing**
   - Accept any number of slots in any order
   - Parse natural language to slot values
   - Handle partial and complete specifications

2. **Skip Filled Slots**
   - Track which slots are filled from input
   - Only prompt for genuinely missing required slots
   - Accept slot updates mid-conversation

3. **Grouped Prompting**
   - Group related missing slots logically
   - Never more than 2-3 questions at a time
   - Use implicit confirmation: "Got X and Y. What about Z?"

**Acceptance Criteria**:
- [ ] Multi-slot input parsed correctly >90%
- [ ] Never re-asks for provided information
- [ ] Maximum 2-3 questions per exchange
- [ ] Slot updates accepted after initial fill
- [ ] Implicit confirmation default (explicit for high-stakes only)
- [ ] **Passes Colleague Test**: Would a colleague respond this way?

**Related Work**:
- Pattern-053 Warmth Calibration
- ADR-049 Intent Architecture
- Existing workflow definitions (Project Setup, etc.)

---

## Issue 4: GLUE-MAINPROJ

**Title**: GLUE-MAINPROJ: Fix "Is that your main project?" repeated question
**Type**: Bug
**Priority**: P0
**Effort**: 1-2 days
**Labels**: `glue`, `bug`, `quick-win`

### Description

Fix the project setup workflow that asks "Is that your main project?" after every project entry. This is a known anti-pattern that makes Piper feel robotic.

**Current State**:
- Project setup asks same question repeatedly
- "Is that your main project?" asked for each project
- They can't all be "main" — primitive robotic parrotry

**Problem**:
```
User: "Add Project Alpha"
Piper: "Is that your main project?" [1st time - OK]
User: "Yes"
User: "Add Project Beta"
Piper: "Is that your main project?" [2nd time - ???]
User: "No"
User: "Add Project Gamma"
Piper: "Is that your main project?" [3rd time - annoying]
```

**Solution Options**:

1. **Ask once at end**: "Which of these would you call your main focus right now?"
2. **Infer from signals**: First mentioned = likely main (can be overridden)
3. **Don't ask at all**: Let user indicate if they want to designate primary

**General Principle**: Questions should be contextually appropriate, not templated.

**Acceptance Criteria**:
- [ ] "Main project" question asked maximum once per session
- [ ] Question timing is contextually appropriate
- [ ] User can designate/change main project at any time
- [ ] No repeated templated questions in any workflow
- [ ] **Passes Colleague Test**: Would a colleague respond this way?

**Related Work**:
- Project setup workflow
- Pattern-053 Warmth Calibration
- conversational-glue-implementation-guide.md Section 5.3

---

## Issue 5: GLUE-SOFTINVOKE

**Title**: GLUE-SOFTINVOKE: Soft workflow invocation from natural language
**Type**: Feature
**Priority**: P0
**Effort**: 3-5 days
**Labels**: `glue`, `mvp-critical`, `pdr-002`

### Description

Enable Piper to recognize implicit workflow triggers in natural language, offering to help rather than requiring explicit commands.

**Current State**:
- Workflows require explicit invocation ("/standup", "start project setup")
- Natural expressions of need don't trigger relevant capabilities
- Users must learn Piper's "language"

**Problem Examples**:
```
Current:
User: "I need to get the team together Tuesday"
Piper: Generic response or misroute

Expected:
User: "I need to get the team together Tuesday"
Piper: "Sounds like a meeting might help. Want me to find a time with the team?"

Current:
User: "This project is getting complicated"
Piper: ???

Expected:
User: "This project is getting complicated"
Piper: "I could help organize it. Want to set up some structure?"
```

**Requirements**:

1. **Intent Pattern Expansion**
   - Map natural expressions to workflow intents
   - "I need to..." → Offer relevant capability
   - "Help me..." → Offer relevant assistance
   - "I'm worried about..." → Surface relevant information

2. **Graceful Offering (Not Assuming)**
   - Offer, don't auto-invoke: "Want me to...?"
   - Make declining easy: "Or I can just..."
   - Respect user intent if they just wanted to chat

3. **Context-Aware Surfacing**
   - Surface relevant capabilities based on conversation topic
   - Don't overwhelm with options
   - Respect throttling rules (max 2 suggestions per 5 exchanges)

**Acceptance Criteria**:
- [ ] 10+ natural expressions map to workflow offers
- [ ] Offers include easy decline path
- [ ] Accepting offer starts workflow naturally
- [ ] Declining doesn't break conversation flow
- [ ] No more than 2 unsolicited offers per 5 exchanges
- [ ] **Passes Colleague Test**: Would a colleague respond this way?

**Related Work**:
- PDR-002 Discovery Glue
- #488 MUX-INTERACT-DISCOVERY
- Pattern-012 LLM Adapter

---

## P1 Issues (Post-M0)

These support the M0 work but can follow in M1:

| Issue | Title | Effort | Sprint |
|-------|-------|--------|--------|
| GLUE-CONFIDENCE | Confidence-tiered responses | 3-5d | M1 |
| GLUE-REPAIR | Repair strategy hierarchy | 5-8d | M1 |
| GLUE-ERRORS | Error-specific recovery | 5-8d | M1 |
| GLUE-PARROT | Anti-parrot audit + fixes | 2-3d | M1 |
| GLUE-ACKNOWLEDGE | Acknowledgment variation | 2-3d | M1 |

---

## Verification Checklist

Before closing M0, verify:

- [ ] All P0 issues complete with evidence
- [ ] B2 quality gate assessment performed
- [ ] Alpha testers confirm naturalness improvement
- [ ] No regression in existing functionality
- [ ] Implementation guide patterns followed
- [ ] Anti-flattening safeguards verified
- [ ] **Every issue passes Colleague Test**

---

## Post-M0 Cross-Functional Review (CXO Requirement)

**What**: CXO, PPM, and implementation leads reconvene to assess whether vision survived implementation.

**When**: After M0 sprint completion, before declaring B2 achieved.

**Why**: The implementation guide is 4500 words. By the time it becomes code, it will have been interpreted multiple times. Each interpretation is an opportunity for flattening. This review catches flattening before we move on.

**Agenda**:
1. Walk through each GLUE issue's implementation
2. Apply Colleague Test to real outputs
3. Compare implementation to original vision
4. Identify any vision erosion
5. Decide: ready for B2 declaration or needs revision?

---

*M0 Issues - Ready for GitHub Creation*
*February 1, 2026 | Updated with CXO/Architect feedback*
