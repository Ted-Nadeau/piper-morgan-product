# Conversational Glue Gap Analysis

**Document Type**: Gap Analysis
**Status**: DRAFT v1
**Created**: February 1, 2026
**Related**: conversational-glue-implementation-guide.md, PDR-002

---

## Purpose

This document maps the Conversational Glue Implementation Guide requirements against Piper Morgan's current state to identify specific gaps that need to be addressed for MVP.

---

## Executive Summary

| Category | Requirements | Implemented | Partial | Gap | MVP Priority |
|----------|-------------|-------------|---------|-----|--------------|
| Dialogue Management | 8 | 2 | 3 | 3 | **P0** |
| State/Memory | 6 | 1 | 2 | 3 | **P1** |
| Workflow Transitions | 6 | 1 | 2 | 3 | **P0** |
| Anti-Robotics | 6 | 0 | 2 | 4 | **P1** |
| Proactivity/Trust | 5 | 2 | 1 | 2 | **P2** |
| Repair/Recovery | 4 | 0 | 1 | 3 | **P1** |
| Personality/Voice | 4 | 1 | 2 | 1 | **P2** |
| **TOTAL** | **39** | **7** | **13** | **19** | |

**Key Finding**: 19 requirements have significant gaps. The most critical gaps are in:
1. **Confidence-tiered responses** (affects all interactions)
2. **Multi-intent handling** (blocks natural compound queries)
3. **Follow-up/reference resolution** (blocks conversational continuity)
4. **Anti-parrot patterns** (affects perceived naturalness)

---

## Detailed Gap Analysis

### 1. Dialogue Management

#### 1.1 Confidence-Tiered Response Selection

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Pre-classifier confidence scores | Numeric 0-1 | Binary match/no-match | **MAJOR** |
| LLM classifier confidence | Numeric with reasoning | Returns category only | **MAJOR** |
| Tiered response logic | 4 tiers (α/β/γ) | Not implemented | **MAJOR** |
| Per-action-type thresholds | Configurable | N/A | **MAJOR** |

**Gap Assessment**: 🔴 Not implemented
**MVP Priority**: P0
**Effort Estimate**: 3-5 days

**What Needs to Be Built**:
1. Add confidence scoring to `pre_classifier.py`
2. Modify LLM classifier to return confidence
3. Create `ConfidenceTierService` with threshold logic
4. Integrate into response generation path

#### 1.2 Multi-Intent Handling

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Detect multiple intents | Yes | Single intent only | **MAJOR** |
| Execution planning | Dependency ordering | N/A | **MAJOR** |
| Coherent multi-response | Single response | N/A | **MAJOR** |

**Gap Assessment**: 🔴 Not implemented
**MVP Priority**: P0
**Effort Estimate**: 5-8 days

**What Needs to Be Built**:
1. Extend `IntentClassificationResult` to `List[Intent]`
2. Create `ExecutionPlanService`
3. Modify handlers to accept batched intents
4. Response aggregation logic

**Related Existing Work**: #595 Multi-intent handling (compound Moment pattern) — check status

#### 1.3 Follow-Up Recognition

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Pronoun resolution | "it," "that," "the meeting" | Partial (Pattern-011) | **PARTIAL** |
| Lens inheritance | Carry forward query aspect | Not implemented | **MAJOR** |
| Elliptical phrases | "And Sarah?" | Not implemented | **MAJOR** |
| Comparative queries | "What about tomorrow?" | Not implemented | **MAJOR** |

**Gap Assessment**: 🟡 Partially implemented
**MVP Priority**: P0
**Effort Estimate**: 3-5 days

**What Needs to Be Built**:
1. Extend anaphoric resolution (Pattern-011)
2. Add lens tracking to conversation context
3. Implement ellipsis detection and expansion
4. Comparative query handling

**Related Existing Work**: #427 MUX-IMPLEMENT-CONVERSE-MODEL (Phase 2: Follow-ups)

#### 1.4 Topic Shift Handling

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Topic shift detection | Yes | Not implemented | **MAJOR** |
| Workflow parking | Yes | Not implemented | **MAJOR** |
| Context restoration | Yes | Not implemented | **MAJOR** |

**Gap Assessment**: 🔴 Not implemented
**MVP Priority**: P2 (deferrable for MVP)
**Effort Estimate**: 5-8 days

---

### 2. State Architecture & Memory

#### 2.1 Hierarchical Memory Model

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Short-term (session) | Verbatim recent turns | In context window | ✅ Implemented |
| Medium-term (24-72h) | Summarized sessions | Designed (ADR-054) | **MAJOR** |
| Long-term (all time) | Extracted entities | Designed (ADR-054) | **MAJOR** |
| Token budget allocation | Configurable split | N/A | **MAJOR** |

**Gap Assessment**: 🟡 Partially designed
**MVP Priority**: P1
**Effort Estimate**: 8-10 days (full ADR-054 implementation)

**What Needs to Be Built**:
1. Implement `ConversationalMemoryService`
2. Implement summarization at session end
3. Entity extraction pipeline
4. Context assembly with budget allocation

#### 2.2 Entity Tracking

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Per-turn extraction | Yes | Not implemented | **MAJOR** |
| Entity linking | To known objects | Not implemented | **MAJOR** |
| Reference resolution | Using entity history | Partial | **PARTIAL** |

**Gap Assessment**: 🔴 Not implemented
**MVP Priority**: P1
**Effort Estimate**: 5-8 days

#### 2.3 Conversation vs. Task State

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Separate state tracking | Yes | Conflated | **MODERATE** |
| Workflow parking | Yes | Not implemented | **MAJOR** |
| State restoration | Yes | Not implemented | **MAJOR** |

**Gap Assessment**: 🔴 Not implemented
**MVP Priority**: P2
**Effort Estimate**: 3-5 days

---

### 3. Natural Workflow Transitions

#### 3.1 Soft Workflow Invocation

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Explicit invocation | Commands, /slash | ✅ Working | None |
| Implicit triggers | Natural language | Limited patterns | **MODERATE** |
| Graceful offering | "Want me to...?" | Not implemented | **MODERATE** |

**Gap Assessment**: 🟡 Partially implemented
**MVP Priority**: P0
**Effort Estimate**: 3-5 days

**What Needs to Be Built**:
1. Expand intent patterns for natural expressions
2. Add "offer" response type vs "execute" response type
3. Contextual relevance scoring

#### 3.2 Context-Aware Tool Surfacing

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Topic detection | From conversation | Not implemented | **MAJOR** |
| Capability relevance | Per-context | Not implemented | **MAJOR** |
| Hint throttling | 2/5 max | Not implemented | **MAJOR** |

**Gap Assessment**: 🔴 Not implemented
**MVP Priority**: P1
**Effort Estimate**: 5-8 days

#### 3.3 Progressive Disclosure

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Layered workflows | Defaults → customize | Not implemented | **MAJOR** |
| 2-3 question limit | Per exchange | Not enforced | **MODERATE** |
| Simple path first | Yes | Not implemented | **MAJOR** |

**Gap Assessment**: 🔴 Not implemented
**MVP Priority**: P1
**Effort Estimate**: 5-8 days per workflow

#### 3.4 Natural Slot Filling

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Multi-slot input | Yes | Limited | **MODERATE** |
| Skip filled slots | Yes | Not implemented | **MODERATE** |
| Grouped questions | Yes | Sequential only | **MODERATE** |

**Gap Assessment**: 🟡 Partially implemented
**MVP Priority**: P0
**Effort Estimate**: 3-5 days

---

### 4. Anti-Robotics Patterns

#### 4.1 Eliminate Parrot Confirmations

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| No verbatim repeats | Zero instances | Unknown | **AUDIT NEEDED** |
| Action-focused confirms | "Done—[result]" | Mixed | **MODERATE** |

**Gap Assessment**: 🟡 Needs audit
**MVP Priority**: P1
**Effort Estimate**: 2-3 days (audit + fixes)

**Action Required**: Audit all response templates and handler outputs

#### 4.2 Vary Acknowledgment Language

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Phrase pool | 6+ variations | Limited | **MODERATE** |
| Repetition tracking | Per conversation | Not implemented | **MAJOR** |
| Context-appropriate | Casual vs formal | Not implemented | **MAJOR** |

**Gap Assessment**: 🟡 Partially implemented
**MVP Priority**: P1
**Effort Estimate**: 2-3 days

#### 4.3 "Is that your main project?" Fix

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Contextual questions | Yes | Templated | **MAJOR** |
| Ask once patterns | Yes | Repeats | **MAJOR** |

**Gap Assessment**: 🔴 Known problem
**MVP Priority**: P0
**Effort Estimate**: 1-2 days (project setup specific)

**Action Required**: Review and fix project setup workflow

#### 4.4 Button Language → Conversational

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Natural phrasing | Throughout | Mixed | **MODERATE** |

**Gap Assessment**: 🟡 Needs audit
**MVP Priority**: P2
**Effort Estimate**: 1-2 days

#### 4.5 Forward Momentum

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| No dead ends | Always offer path | Mixed | **MODERATE** |
| Helpful alternatives | On error | Limited | **MODERATE** |

**Gap Assessment**: 🟡 Partially implemented
**MVP Priority**: P1
**Effort Estimate**: 3-5 days

---

### 5. Proactivity & Trust Integration

#### 5.1 Trust-Based Proactivity

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Trust computation | 4 stages | ✅ ADR-053 (453 tests) | None |
| Proactivity levels | Per trust stage | Not wired | **MAJOR** |
| Trust-action mapping | Configurable | Not implemented | **MAJOR** |

**Gap Assessment**: 🟡 Trust computed, not used
**MVP Priority**: P2
**Effort Estimate**: 3-5 days

#### 5.2 Inner Thoughts Pattern

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Continuous reasoning | Yes | Not implemented | **MAJOR** |
| Surfacing gates | Yes | Not implemented | **MAJOR** |

**Gap Assessment**: 🔴 Not implemented
**MVP Priority**: P3 (post-MVP)
**Effort Estimate**: 8-10 days

#### 5.3 Proactivity Guardrails

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Never-proactive list | Defined | Not implemented | **MODERATE** |
| Always-confirm list | Defined | Partial | **MINOR** |
| Trust-gated actions | Stage 4 autonomy | Not implemented | **MODERATE** |

**Gap Assessment**: 🟡 Partially designed
**MVP Priority**: P2
**Effort Estimate**: 2-3 days

#### 5.4 Proactivity Decay

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Acceptance tracking | Yes | Not implemented | **MAJOR** |
| Frequency adjustment | Yes | Not implemented | **MAJOR** |
| Explicit stop handling | Yes | Not implemented | **MAJOR** |

**Gap Assessment**: 🔴 Not implemented
**MVP Priority**: P3 (post-MVP)
**Effort Estimate**: 3-5 days

---

### 6. Repair & Recovery

#### 6.1 Repair Strategy Hierarchy

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Options-first | 2-3 alternatives | Limited | **MAJOR** |
| Explain understanding | What was heard | Not implemented | **MAJOR** |
| Partial completion | Continue what worked | Not implemented | **MAJOR** |
| Graceful degradation | Alternative paths | Limited | **MODERATE** |

**Gap Assessment**: 🔴 Not implemented
**MVP Priority**: P1
**Effort Estimate**: 5-8 days

#### 6.2 Error-Specific Recovery

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Intent unclear | Offer interpretations | Generic error | **MAJOR** |
| Entity not found | Suggest similar | Generic error | **MAJOR** |
| Service down | Offer alternative | Error message | **MAJOR** |

**Gap Assessment**: 🔴 Not implemented
**MVP Priority**: P1
**Effort Estimate**: 5-8 days

---

### 7. Personality & Voice

#### 7.1 Colleague Persona

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Warm but professional | Defined tone | ✅ Pattern-053 | Mostly implemented |
| Competent | PM domain knowledge | ✅ Working | None |
| Proactive helpfulness | Contextual | Not wired | **MODERATE** |

**Gap Assessment**: 🟢 Mostly implemented
**MVP Priority**: P2
**Effort Estimate**: 2-3 days (refinement)

#### 7.2 Voice Guidelines

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| First person singular | Yes | Mostly | **MINOR** |
| Contractions | Yes | Mixed | **MINOR** |
| No filler phrases | Yes | Unknown | **AUDIT NEEDED** |

**Gap Assessment**: 🟡 Needs audit
**MVP Priority**: P2
**Effort Estimate**: 1-2 days

#### 7.3 Transparent Reasoning

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Show thinking | For complex decisions | Limited | **MODERATE** |
| When to show | Guidelines | Not implemented | **MODERATE** |

**Gap Assessment**: 🟡 Partially implemented
**MVP Priority**: P2
**Effort Estimate**: 2-3 days

#### 7.4 Emotional Attunement

| Aspect | Required | Current State | Gap |
|--------|----------|---------------|-----|
| Tone detection | From user input | Not implemented | **MAJOR** |
| Response adjustment | Based on tone | Not implemented | **MAJOR** |

**Gap Assessment**: 🔴 Not implemented
**MVP Priority**: P3 (post-MVP)
**Effort Estimate**: 5-8 days

---

## MVP Gap Prioritization

### P0 — Must Have for MVP

| Gap | Effort | Impact |
|-----|--------|--------|
| Follow-up recognition (#427 Phase 2) | 3-5d | Conversational continuity |
| Multi-intent handling (#595) | 5-8d | Natural compound queries |
| Natural slot filling | 3-5d | Workflow usability |
| "Main project" fix | 1-2d | Immediate pain point |
| Soft workflow invocation | 3-5d | Natural-to-structured transitions |

**Total P0 Effort**: 15-25 days

### P1 — Should Have for MVP

| Gap | Effort | Impact |
|-----|--------|--------|
| Confidence-tiered responses | 3-5d | Confirmation appropriateness |
| Repair strategy hierarchy | 5-8d | Error recovery |
| Error-specific recovery | 5-8d | Error recovery |
| Anti-parrot audit + fixes | 2-3d | Perceived naturalness |
| Acknowledgment variation | 2-3d | Perceived naturalness |
| Forward momentum | 3-5d | No dead ends |

**Total P1 Effort**: 20-32 days

### P2 — Nice to Have for MVP

| Gap | Effort | Impact |
|-----|--------|--------|
| Trust-proactivity wiring | 3-5d | Proactive features |
| Context-aware tool surfacing | 5-8d | Capability discovery |
| Progressive disclosure | 5-8d/workflow | Workflow usability |
| ADR-054 memory implementation | 8-10d | Cross-session memory |

### P3 — Post-MVP

| Gap | Effort | Impact |
|-----|--------|--------|
| Topic shift handling | 5-8d | Advanced conversational |
| Inner thoughts pattern | 8-10d | Sophisticated proactivity |
| Emotional attunement | 5-8d | Tone matching |
| Proactivity decay | 3-5d | Suggestion tuning |

---

## Existing Issues to Link/Update

| Issue | Relevance | Action |
|-------|-----------|--------|
| #427 MUX-IMPLEMENT-CONVERSE-MODEL | Phase 2 follow-ups directly relevant | Update scope with this guidance |
| #595 Multi-intent handling | Core gap | Verify status, update if needed |
| #688 ADR-050 Phases 1-3 | Conversation graph foundation | Reference for P1/P2 work |
| #698-700 Guided Process types | Workflow patterns | Inform with progressive disclosure |

---

## Recommended Next Steps

1. **Create M0 (Glue Sprint) issues** from P0 gaps
2. **Update #427** with implementation guide requirements
3. **Review #595** multi-intent status
4. **Conduct anti-parrot audit** of existing templates
5. **Review project setup workflow** for "main project" fix
6. **Update PDR-002** with this gap analysis

---

*Document Version: 1.0*
*Last Updated: February 1, 2026*
