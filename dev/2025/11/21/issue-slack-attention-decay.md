# GitHub Issue: SLACK-ATTENTION-DECAY

**Title**: SLACK-ATTENTION-DECAY: Implement pattern learning for attention models

**Labels**: `slack`, `learning-system`, `enhancement`, `attention`

**Milestone**: Enhancement (Post-Alpha)

**Priority**: P3

---

## Context

Deferred from SLACK-SPATIAL Phase 4 (Issue #361) during alpha preparation. This feature requires the learning system (Roadmap Phase 3) which is not available for alpha.

**Related Issue**: #361 (SLACK-SPATIAL)
**Deferred Date**: November 21, 2025
**Reason**: Requires learning system integration
**Blocked By**: Learning system (Roadmap Phase 3)

---

## Description

Add time-decay and pattern learning to the attention scoring system. Currently, attention is calculated statically per-message based on mentions, reactions, and thread activity. With pattern learning, the system should:

1. **Decay attention over time** - Messages should lose attention as they age
2. **Learn user patterns** - Understand which types of messages the user actually responds to
3. **Predict attention** - Proactively score new messages based on learned patterns
4. **Adapt over time** - Improve accuracy as more interaction data accumulates

---

## Current Behavior

**Static Attention Scoring**:
- Attention calculated at message creation time
- Based on: mentions, reactions, thread depth, channel importance
- Score doesn't change over time
- Doesn't learn from user behavior
- Same types of messages always get same scores

**Limitations**:
- Old messages stay "high attention" forever
- Can't predict what user will find important
- Doesn't adapt to user's changing interests
- Treats all users the same way

**Example**:
> Message with @mention gets high attention score
>
> User ignores it for 3 days
>
> System still shows it as high attention (doesn't decay)
>
> User repeatedly ignores @mentions from certain channels
>
> System still scores those @mentions as high attention (doesn't learn)

---

## Desired Behavior

**Dynamic Attention with Learning**:
- Attention decays over time (configurable decay rate)
- System learns which message patterns user responds to
- Predictive scoring based on learned patterns
- Attention model adapts to user behavior changes

**Example with Learning**:
> Message with @mention starts at attention 0.9
>
> After 1 hour: decays to 0.85 (user hasn't responded)
>
> After 1 day: decays to 0.7 (user still hasn't responded)
>
> System learns: "User ignores @mentions in #random"
>
> Next @mention in #random: starts at 0.5 (learned pattern applied)
>
> But @mention in #urgent: still starts at 0.9 (user responds to those)

---

## Requirements

### Functional Requirements

1. **Time-Based Decay**
   - Configurable decay functions (linear, exponential, logarithmic)
   - Per-message decay tracking
   - Decay rate varies by message type
   - User can configure decay preferences

2. **Pattern Learning**
   - Track user interactions (reads, responses, ignores)
   - Identify patterns in user attention
   - Build user-specific attention model
   - Update model as behavior changes

3. **Predictive Scoring**
   - Score new messages using learned patterns
   - Combine static factors with learned patterns
   - Confidence scores for predictions
   - Explanation of why message scored high/low

4. **Adaptation Over Time**
   - Model improves with more data
   - Detects behavior changes
   - Re-learns when patterns shift
   - Handles cold-start (new users)

5. **User Control**
   - View learned patterns
   - Adjust decay rates
   - Reset learning
   - Provide feedback on scores

### Technical Requirements

1. **Learning System Integration**
   - Interface with Piper learning system
   - Store attention interaction data
   - Train attention models
   - Deploy updated models

2. **Decay Algorithm**
   - Efficient decay calculation
   - Background jobs for decay updates
   - Decay state persistence
   - Performance optimization

3. **Pattern Storage**
   - User attention profiles
   - Learned pattern database
   - Pattern versioning
   - Privacy-preserving storage

4. **Model Training**
   - Batch training pipeline
   - Incremental learning
   - A/B testing for model changes
   - Model performance metrics

---

## Test Coverage

**Skipped Test**: `test_attention_decay_models_with_pattern_learning`
- **Location**: `tests/unit/services/integrations/slack/test_spatial_system_integration.py`
- **What it tests**: Attention decay behavior and pattern learning over time
- **Why skipped**: Requires learning system infrastructure
- **Status**: Test exists but marked as skipped

**Additional Tests Needed**:
- Decay function accuracy
- Pattern learning convergence
- Prediction accuracy
- Adaptation to behavior changes
- Cold-start handling
- Performance under scale

---

## Implementation Approach

### Phase 1: Time Decay (4-6 weeks)
**Goal**: Messages lose attention over time

**Components**:
- Decay function implementation
- Background decay job
- Decay state storage
- UI showing decayed attention

**Deliverables**:
- Configurable decay rates
- Automatic attention updates
- Test coverage for decay

### Phase 2: Basic Pattern Learning (6-8 weeks)
**Goal**: Learn simple patterns (channel importance, user importance)

**Components**:
- Interaction tracking
- Simple pattern detection
- Basic prediction model
- Pattern visualization

**Deliverables**:
- User-specific channel importance
- User-specific sender importance
- Improved attention accuracy

### Phase 3: Advanced Learning (8-12 weeks)
**Goal**: Multi-factor learning with adaptation

**Components**:
- Multi-dimensional patterns
- Temporal patterns (time-of-day, day-of-week)
- Behavior change detection
- A/B testing framework

**Deliverables**:
- Sophisticated attention model
- Real-time adaptation
- Model performance monitoring
- User feedback integration

---

## Success Criteria

**Feature is complete when**:
- ✅ Attention decays over time appropriately
- ✅ System learns from user interactions
- ✅ Predictions improve accuracy over baseline
- ✅ User can view and control learned patterns
- ✅ `test_attention_decay_models_with_pattern_learning` passes
- ✅ Measurable improvement in attention accuracy (>15%)
- ✅ System adapts to behavior changes within 1 week

---

## Metrics for Success

**Attention Accuracy**:
- Baseline: Current static scoring
- Target: +15% accuracy (user responds to high-attention items)
- Measure: Precision/recall of attention predictions

**User Satisfaction**:
- Baseline: Alpha user feedback on attention
- Target: 80%+ users say "attention is accurate"
- Measure: User surveys

**Model Performance**:
- Decay latency: <1 second
- Prediction latency: <100ms
- Training time: <1 hour for full retrain
- Model size: <10MB per user

---

## Dependencies

**Blocked By**:
- **Learning System** (Roadmap Phase 3) - Core dependency
- User interaction tracking infrastructure
- Background job system for decay
- Model storage and serving infrastructure

**Blocks**:
- Advanced attention features
- Personalized notifications
- Proactive assistance
- User behavior analytics

---

## Estimated Effort

**Size**: X-Large (4-6 months total)

**Breakdown**:
- Phase 1 (Decay): 4-6 weeks
- Phase 2 (Basic Learning): 6-8 weeks
- Phase 3 (Advanced Learning): 8-12 weeks
- Testing and refinement: 2-4 weeks

---

## Priority Justification

**P3 (Enhancement)**:
- Improves core feature but not required
- Alpha can function with static attention
- Requires significant infrastructure investment
- Long development timeline

**Not P0/P1/P2**:
- Static attention sufficient for alpha/beta
- Learning system not yet available
- Can be added incrementally post-alpha
- Users can manually adjust attention

**High Value**:
- Significant UX improvement when complete
- Differentiator vs. other tools
- Enables proactive assistance
- Foundation for advanced features

---

## Research Questions

1. **Decay Functions**: Which decay function works best for message attention?
   - Linear vs exponential vs logarithmic
   - User preferences for decay rates
   - Domain-specific decay patterns

2. **Learning Approach**: What learning algorithm is most effective?
   - Supervised learning from explicit feedback
   - Reinforcement learning from implicit signals
   - Hybrid approach

3. **Cold Start**: How to handle new users with no interaction data?
   - Default to static scoring
   - Bootstrap from similar users
   - Explicit user preferences

4. **Privacy**: How to preserve privacy while learning?
   - On-device learning vs server-side
   - Differential privacy techniques
   - User data controls

---

## References

- **Parent Issue**: #361 (SLACK-SPATIAL)
- **Gameplan**: `gameplan-slack-spatial-phase4-final.md`
- **Test**: `tests/unit/services/integrations/slack/test_spatial_system_integration.py::test_attention_decay_models_with_pattern_learning`
- **Milestone**: Enhancement (Post-Alpha)
- **Learning System**: Roadmap Phase 3

---

## Notes

This is a foundational enhancement that will significantly improve Piper's intelligence over time. While not required for alpha, it represents the kind of adaptive behavior that makes AI assistants truly helpful.

**Alpha Impact**: Not required - static attention sufficient
**Long-term Impact**: Critical for advanced intelligence

The test exists and documents expected behavior. Implementation requires learning system infrastructure from Roadmap Phase 3.
