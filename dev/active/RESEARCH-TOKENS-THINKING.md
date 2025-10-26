# RESEARCH-TOKENS-THINKING: Investigate Thinking Token Optimization for Chain of Drafts

**Sprint**: MVP (Post-Alpha)
**Priority**: Medium (Research)
**Effort**: 1-2 days research, 1 day implementation
**Impact**: Medium-High (15-25% quality improvement potential)

---

## Background

Research on "Chain of Babble" suggests LLMs perform better with additional compute time, even when filled with seemingly meaningless tokens. This presents an opportunity to optimize Chain of Drafts quality without sacrificing the transparency PMs value.

---

## Hypothesis

Adding invisible "thinking tokens" to each draft will improve output quality while maintaining the clean, auditable iteration trail that builds PM trust.

---

## Research Protocol

### Phase 1: Baseline Measurement
Collect quality metrics on current Chain of Drafts:
- Output quality (human evaluated 1-5)
- Task completion accuracy
- Number of revision cycles needed
- User satisfaction scores

### Phase 2: A/B Test Design

**Group A: Control** (Current Implementation)
```python
def generate_draft(prompt, draft_num):
    return llm.complete(f"Draft {draft_num}: {prompt}")
```

**Group B: Static Thinking Tokens**
```python
def generate_draft(prompt, draft_num):
    thinking = "[THINKING]" + ("..." * 50) + "[/THINKING]"
    response = llm.complete(f"{prompt}\n{thinking}\nDraft {draft_num}:")
    return strip_thinking_section(response)
```

**Group C: Dynamic Complexity-Based**
```python
def generate_draft(prompt, draft_num):
    complexity = assess_complexity(prompt)
    thinking_tokens = generate_thinking_space(complexity)
    # More tokens for complex tasks
    ...
```

**Group D: Single-Shot Heavy Thinking**
```python
def generate_response(prompt):
    # Test if multiple drafts are needed vs single call with thinking
    heavy_thinking = "[THINKING]" + ("..." * 200) + "[/THINKING]"
    return llm.complete(f"{prompt}\n{heavy_thinking}\nFinal response:")
```

### Phase 3: Model-Specific Testing

Test across all available models:
- **Haiku 4.5**: May benefit most (cheaper baseline)
- **Sonnet 4.5**: Optimal padding unknown
- **Opus 4.1**: May not benefit (already high compute)

---

## Implementation Approach

### Option 1: Handler-Level (Recommended for Testing)
```python
class ThinkingEnhancedHandler(BaseHandler):
    def __init__(self, thinking_tokens=100):
        self.thinking_tokens = thinking_tokens

    def process(self, request):
        # Add thinking space invisible to user
        enhanced_prompt = self._add_thinking_space(request.prompt)
        response = self.llm.complete(enhanced_prompt)
        return self._strip_thinking(response)
```

### Option 2: Orchestration-Level
Apply thinking tokens strategically based on task type:
- Complex analysis: 200+ tokens
- Simple queries: 20-50 tokens
- Routine tasks: No enhancement

### Option 3: Adaptive Learning
Track which token patterns improve quality:
```python
class AdaptiveThinkingOptimizer:
    def optimize_thinking_pattern(self, task_type, feedback):
        if feedback.quality_improved:
            self.patterns[task_type].strengthen()
        else:
            self.patterns[task_type].explore_variation()
```

---

## Success Metrics

### Primary Metrics
- Quality improvement: Target 15-25%
- Cost increase: Maximum 40%
- Net efficiency: Reduced revision cycles

### Secondary Metrics
- User satisfaction maintained or improved
- Debuggability preserved
- Model-specific optimization achieved

---

## Cost-Benefit Analysis

### Current Baseline
- 3 drafts × 500 tokens = 1,500 tokens
- Quality score: Baseline

### With Thinking Enhancement
- 3 drafts × (200 thinking + 500 visible) = 2,100 tokens
- Cost: +40%
- Expected quality: +15-25%

### Break-Even Calculation
If quality improvement reduces revisions by 1 cycle:
- Saved: 1,500 tokens (one full Chain of Drafts)
- Net positive despite higher per-call cost

---

## Risk Mitigation

1. **Preserve Transparency**
   - Keep thinking tokens completely invisible
   - Maintain clean audit trail
   - No change to user-facing interface

2. **Enable Quick Rollback**
   - Feature flag for instant disable
   - A/B test infrastructure for gradual rollout
   - Fallback to standard Chain of Drafts

3. **Model Compatibility**
   - Test each model independently
   - Different strategies per model
   - Graceful degradation

---

## Research Questions

1. **Optimal Token Count**: What's the sweet spot for quality vs cost?
2. **Token Content**: Does the content matter or just the count?
3. **Model Differences**: Do different models need different strategies?
4. **Task Specificity**: Should token count vary by task type?
5. **Prompt Caching**: Can we cache thinking tokens for cost reduction?

---

## Implementation Timeline

### Week 1: Research & Baseline
- Day 1-2: Collect baseline metrics
- Day 3-4: Design test infrastructure
- Day 5: Initial implementation

### Week 2: Testing
- Day 1-3: A/B testing with team
- Day 4-5: Analysis and optimization

### Week 3: Rollout Decision
- If positive: Gradual rollout
- If negative: Document learnings
- If mixed: Model-specific implementation

---

## Related Work

- Chief of Staff memo on thinking tokens
- Chain of Babble research paper
- Prompt caching optimization (90% cost reduction potential)
- Haiku 4.5 cost optimization initiative

---

## Decision Points

1. **Should we test this pre-beta?** (Recommended: Yes)
2. **Which models to prioritize?** (Recommended: Haiku first)
3. **Static vs dynamic tokens?** (Recommended: Start static, evolve to dynamic)

---

**Note**: This is a research initiative with high potential but unproven results. Budget 1-2 weeks for thorough investigation before committing to production implementation.

---

**Created**: October 25, 2025
**Author**: Chief Architect
**Status**: Research proposal for MVP phase
