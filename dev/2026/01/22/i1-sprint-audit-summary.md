# Sprint I1 Issue Audit Summary

**Date**: 2026-01-22
**Auditor**: Lead Developer (Claude Code)
**Purpose**: Research and audit all I1 sprint issues before implementation

---

## Executive Summary

| Category | Count | Notes |
|----------|-------|-------|
| **Ready to implement** | 2 | #551, #488 - have full bodies |
| **Need issue body written** | 10 | Stub issues with only titles |
| **Have body, need audit** | 3 | #558, #561, #567, #569 |
| **Total I1 issues** | 15 | |

**Key Finding**: 10 of 15 issues are stubs requiring research before implementation.

---

## Issue-by-Issue Assessment

### Tier 1: Ready to Implement (Have Bodies)

#### #551 ARCH-COMMANDS: Command Parity Across Interfaces
- **Status**: Complete body, detailed phases
- **Template Compliance**: ~90%
- **Research**: Deep command inventory (Phase 1 only = research)
- **Recommendation**: Ready for Phase 1 execution
- **Effort**: Phase 1 = Medium (research only)

#### #488 MUX-INTERACT-DISCOVERY: Discovery-Oriented Intent Architecture
- **Status**: Complete gameplan structure
- **Template Compliance**: ~95%
- **Research**: `_get_dynamic_capabilities()` exists, patterns ready
- **Recommendation**: Ready for implementation
- **Dependencies**: None blocking
- **Effort**: Medium

---

### Tier 2: Need Issue Bodies Written (Stubs)

#### #413 TRUST-LEVELS: Define trust gradient mechanics
- **Current Body**: Empty
- **Research Complete**: YES
- **What Exists**:
  - ADR-053: Complete trust computation architecture (PROPOSED, not implemented)
  - PDR-002: Trust gradient model spec (4 stages, thresholds, regression rules)
  - ProactivityGate logic designed but not coded
- **What's Missing**:
  - TrustComputationService (no code)
  - Database table `user_trust_profiles`
  - Outcome classification heuristics
- **Dependencies**: None - foundational for #414, #415
- **Recommended Scope**: Implement ADR-053 (4 phases)
- **Effort**: Large (database + service + background jobs)

#### #411 RECOGNITION: Design "did you mean..." interface patterns
- **Current Body**: Empty
- **Research Complete**: YES
- **What Exists**:
  - `fuzzy_matcher.py` with typo correction (0.8 cutoff)
  - `honest_failure.py` with warmth-calibrated follow-ups
  - Low-confidence detection (<0.3) in classifier
  - Multi-intent decomposition (#595)
- **What's Missing**:
  - Proactive suggestion generation (top-3 alternatives)
  - Suggestion ranking/presentation
  - Cross-intent disambiguation UI
- **Dependencies**: Feeds into #412 INTENT-BRIDGE
- **Recommended Scope**: Enhance HonestFailureHandler with suggestions
- **Effort**: Medium

#### #412 INTENT-BRIDGE: Bridge current intent classification to recognition
- **Current Body**: Empty
- **Research Complete**: YES
- **What Exists**:
  - 2-stage classification (pre-classifier → LLM)
  - 16 IntentCategory values
  - Grammar-conscious `IntentUnderstanding` (NEW in intent_types.py)
  - PlaceDetector for spatial context
- **What's Missing**:
  - Classification → Understanding transformation
  - Place/ownership tagging integration
  - Multi-intent strategy implementation
- **Dependencies**: #411 RECOGNITION, #619 GRAMMAR-TRANSFORM
- **Recommended Scope**: Integrate grammar-conscious classification
- **Effort**: Medium-Large

#### #410 CANONICAL-ENHANCE: Evolve canonical queries to orientation system
- **Current Body**: Empty
- **Research Complete**: YES
- **What Exists**:
  - ADR-039: Canonical Handler Pattern (APPROVED)
  - 6 canonical categories, 25 query patterns
  - `canonical_handlers.py` (4,072 lines)
  - Pattern-025: Canonical Query Extension
- **What's Missing**:
  - Query relationship mapping
  - Orientation context layer
  - Suggestion system for adjacent queries
- **Dependencies**: Foundation for #488 DISCOVERY
- **Recommended Scope**: Add orientation metadata to canonical responses
- **Effort**: Medium

#### #414 DELEGATION: System-initiated vs user-initiated patterns
- **Current Body**: Empty
- **Research Complete**: YES
- **What Exists**:
  - `autonomous_executor.py` with safety levels
  - `user_approval_system.py` for approval workflows
  - `predictive_assistant.py` (passive predictions)
  - ADR-053 defines ProactivityGate logic
- **What's Missing**:
  - Centralized ProactivityGate service
  - Delegation decision logging
  - Trust-aware proactivity integration
- **Dependencies**: REQUIRES #413 TRUST-LEVELS
- **Recommended Scope**: Implement ProactivityGate + decision log
- **Effort**: Medium

#### #415 PREMONITION: When/how Piper surfaces insights
- **Current Body**: Empty
- **Research Complete**: YES
- **What Exists**:
  - `insight-surfacing-rules.md` (D4) - Complete spec
  - Three modes: Pull/Passive/Push
  - Push thresholds (0.75+, 24h throttle, Stage 3+ trust)
  - `learning_handler.py` with pattern detection
- **What's Missing**:
  - Push mode implementation
  - Context relevance matching
  - Feedback loop for surfacing quality
- **Dependencies**: REQUIRES #413 TRUST-LEVELS, relates to #414
- **Recommended Scope**: Implement push mode per D4 spec
- **Effort**: Medium

#### #416 WORKSPACE: How Piper navigates between contexts
- **Current Body**: Empty
- **Research Complete**: YES
- **What Exists**:
  - ADR-051: RequestContext with `workspace_id` (future)
  - ADR-045: Place concept ("Entities experience Moments in Places")
  - Spatial adapters (5 implementations)
  - Pattern-011: Context Resolution
- **What's Missing**:
  - Navigation UI patterns
  - Context switching mechanisms
  - Place listing/discovery
- **Dependencies**: MUX-V1 grammar complete
- **Recommended Scope**: Design patterns for Place navigation
- **Effort**: Medium (design-heavy)

#### #417 ATTENTION: Attention algorithms based on spatial metaphors
- **Current Body**: Empty
- **Research Complete**: YES
- **What Exists**:
  - `attention_model.py` (1,141 lines) - sophisticated scoring
  - Multi-factor algorithm (urgency, relevance, proximity, decay)
  - AttentionLevel enum (5 levels)
  - `attention_decay_job.py` for background processing
  - 8-dimensional spatial analysis
- **What's Missing**:
  - Calibration framework
  - Cross-integration validation
  - MUX PriorityLens integration
- **Dependencies**: Spatial infrastructure exists
- **Recommended Scope**: Document + calibrate existing algorithms
- **Effort**: Medium

#### #418 MOMENT-UI: How Moments appear in interface
- **Current Body**: Empty
- **Research Complete**: YES
- **What Exists**:
  - ADR-045/050/055: Moment definitions
  - `MomentProtocol` in protocols.py
  - `Moment.type` architecture (6 types)
  - ConversationNodeType (aligns with Moments)
- **What's Missing**:
  - NO Moment display UI components
  - NO Moment API endpoints
  - NO experience-framing in UI
- **Dependencies**: #427 MUX-IMPLEMENT-CONVERSE-MODEL
- **Recommended Scope**: UI specification for Moment display
- **Effort**: Medium (design-heavy)

---

### Tier 3: Have Bodies, Need Template Audit

#### #558 STANDUP-CONVERSE: LLM-based preference extraction
- **Status**: Has body
- **Template Compliance**: ~70%
- **Key Info**: P3 priority, trigger-based activation
- **Note**: "When accuracy drops below 70%" - not active yet
- **Recommendation**: Skip for I1 (trigger not met)

#### #561 FTUX-CONVERSE: Complete portfolio onboarding conversation flow
- **Status**: Has body
- **Template Compliance**: ~75%
- **Key Info**: Polish work on existing #490 implementation
- **Recommendation**: Include in I1 (UX polish)

#### #567 CONV-SEARCH: Search within portfolio
- **Status**: Has body (minimal)
- **Template Compliance**: ~40%
- **Key Info**: Beta feature, deferred from MVP
- **Recommendation**: Needs body expansion

#### #569 PORTFOLIO-DEL: Delete/archive projects from portfolio
- **Status**: Has body (minimal)
- **Template Compliance**: ~40%
- **Key Info**: Beta feature, deferred from MVP
- **Recommendation**: Needs body expansion

---

## Dependency Graph

```
                    ┌─────────────────┐
                    │ #413 TRUST-LEVELS│ (Foundation)
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ #414 DELEGATION │  │#415 PREMONITION│  │ #410 CANONICAL │
└────────────────┘  └────────────────┘  └───────┬────────┘
                                                │
                                                ▼
                                        ┌────────────────┐
                                        │ #488 DISCOVERY │
                                        └────────────────┘

┌────────────────┐     ┌────────────────┐
│ #411 RECOGNITION│────▶│ #412 INTENT    │
└────────────────┘     │    BRIDGE      │
                       └────────────────┘

┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│ #416 WORKSPACE │     │ #417 ATTENTION │     │ #418 MOMENT-UI │
└────────────────┘     └────────────────┘     └────────────────┘
   (Independent)          (Independent)           (Design-heavy)
```

---

## Recommended I1 Sprint Ordering

### Phase A: Foundation & Ready Issues
1. **#551 ARCH-COMMANDS Phase 1** (Research only - command inventory)
2. **#488 DISCOVERY** (Ready to implement)
3. **#413 TRUST-LEVELS** (Foundation for delegation/premonition)

### Phase B: Trust-Dependent Issues
4. **#414 DELEGATION** (Requires #413)
5. **#415 PREMONITION** (Requires #413)

### Phase C: Intent Evolution
6. **#411 RECOGNITION** (Suggestion patterns)
7. **#412 INTENT-BRIDGE** (Requires #411)
8. **#410 CANONICAL-ENHANCE** (Orientation system)

### Phase D: Design-Heavy Issues
9. **#416 WORKSPACE** (Navigation design)
10. **#417 ATTENTION** (Algorithm calibration)
11. **#418 MOMENT-UI** (UI specification)

### Phase E: Conversational Polish
12. **#561 FTUX-CONVERSE** (Onboarding polish)
13. **#567 CONV-SEARCH** (If time)
14. **#569 PORTFOLIO-DEL** (If time)

### Skip for I1
- **#558 STANDUP-CONVERSE** (Trigger not met - accuracy threshold)

---

## PM Decisions (2026-01-22 4:09 PM)

1. **#413 Scope**: Defer scoping until after #551 and #488 complete. Then treat #413 as mini-epic: inventory full ADR-053 implementation, rank/triage/phase the work.

2. **#417 Calibration**: Time to unskip those tests and validate attention algorithms.

3. **#416/#418 Design**: Design-spec outputs expected. When we reach these, evaluate against MUX-IMPLEMENT issues that follow. If not covered by implementation issues, add implementation scope.

4. **Parallel Work**: YES - design issues can run parallel to #413 chain.

5. **ADR-053**: Foundational, time to implement is NOW.

---

## Next Steps

For each stub issue, the cascade is:
1. ✅ Research complete (this document)
2. ⬜ Write issue body based on research
3. ⬜ Audit against issue template
4. ⬜ Write gameplan
5. ⬜ Audit against gameplan template
6. ⬜ Write subagent prompts
7. ⬜ Audit against subagent prompt template

**Recommendation**: Discuss ordering and scope before writing all 10 issue bodies.
