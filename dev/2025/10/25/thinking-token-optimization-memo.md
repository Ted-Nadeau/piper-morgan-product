# MEMO: Thinking Token Optimization Strategy

**To**: Chief Architect, Lead Developer
**From**: Chief of Staff
**Date**: October 24, 2025
**Re**: Under-the-Hood Compute Optimization via Thinking Tokens

## Background

Recent research on "Chain of Babble" reveals that LLM reasoning improves with additional compute time, even when filled with seemingly meaningless tokens. This suggests an opportunity to optimize Piper's Chain of Drafts implementation without sacrificing its visible, auditable iteration that PMs value.

## Current State

Chain of Drafts provides:
- Visible iterative refinement (3 drafts typical)
- Debuggable reasoning path
- User trust through transparency
- Cost: 3x single-shot approach

## Proposed Hybrid Approach

Maintain visible Chain of Drafts while optimizing each draft's internal computation:

```python
class EnhancedDraftHandler:
    def generate_draft(self, prompt, draft_number):
        # Add invisible thinking tokens for compute time
        thinking_prompt = f"""
        {prompt}

        [THINKING SPACE - not shown to user]
        Let me consider this carefully... hmm... analyzing the requirements...
        considering edge cases... evaluating alternatives...
        ... (generated padding based on complexity)
        [END THINKING]

        Now, here's Draft {draft_number}:
        """

        response = llm.complete(thinking_prompt)
        # Strip thinking section before returning
        return extract_visible_draft(response)
```

## Implementation Options

### Option 1: Static Thinking Tokens
- Add fixed "reasoning space" to each draft
- Simple to implement
- Predictable cost increase (20-30%)

### Option 2: Dynamic Complexity-Based
- Analyze task complexity
- Add proportional thinking tokens
- More complex: 100-200 tokens
- Simple tasks: 20-50 tokens

### Option 3: Learning-Based Optimization
- Track which token patterns improve output
- Evolve optimal "babble" over time
- Requires feedback loop and storage

## Test Protocol

### A/B Test Design (Sprint A8)
```
Group A: Current Chain of Drafts
- 3 drafts, no padding
- Baseline cost and quality

Group B: Thinking-Enhanced Drafts
- 3 drafts with thinking tokens
- ~30% cost increase expected
- Quality improvement to measure

Group C: Single-Shot with Heavy Thinking
- 1 call with extensive thinking tokens
- Cost comparable to Group A
- Tests if drafts add value beyond compute
```

### Metrics to Track
- Output quality score (human evaluated)
- Task completion accuracy
- Cost per task
- Time to completion
- Debuggability score

## Preserving PM Value

**Critical**: Keep thinking tokens invisible to users
- PMs need clean audit trail
- Thinking tokens are implementation detail
- Visible output remains professional

```python
# What PM sees:
Draft 1: Initial requirements analysis...
Draft 2: Refined with edge cases...
Draft 3: Final version with polish...

# What happens internally:
Draft 1: [200 thinking tokens] + visible output
Draft 2: [150 thinking tokens] + visible output
Draft 3: [100 thinking tokens] + visible output
```

## Cost-Benefit Analysis

### Current Approach
- 3 drafts × 500 tokens = 1,500 tokens total
- Cost: Standard

### With Thinking Tokens
- 3 drafts × (200 thinking + 500 visible) = 2,100 tokens
- Cost: +40%
- Expected quality gain: 15-25% (based on research)

### Break-even Calculation
If quality improvement reduces revision cycles by 1 round:
- Saved: 1 full Chain of Drafts iteration (1,500 tokens)
- Net efficiency gain despite higher per-call cost

## Architectural Considerations

1. **Where to implement:**
   - Handler level (each draft)
   - Orchestration level (strategic padding)
   - Both with different strategies

2. **Model-specific tuning:**
   - Haiku 4.5: May need more padding
   - Sonnet 4.5: Optimal padding unclear
   - Opus: May not benefit (already high compute)

3. **Prompt caching interaction:**
   - Thinking tokens could be cached
   - 90% cost reduction on repeated patterns
   - Amortizes padding cost

## Recommendations

1. **Immediate**: Test in Sprint A8 with Code agent
2. **Short-term**: Implement Option 1 (static tokens) if tests positive
3. **Long-term**: Evolve to Option 3 (learning-based) post-alpha

## Risk Mitigation

- Keep thinking tokens separate from user-visible content
- Maintain ability to disable for debugging
- Monitor for quality degradation
- Ensure compatibility with all models

## Decision Required

Should we allocate 2-3 hours in Sprint A8 to test thinking token enhancement? Low risk, potentially high reward, and aligns with our evidence-based methodology.

---

*Note: This optimization is invisible to users and preserves all benefits of Chain of Drafts while potentially improving quality at marginal cost increase.*
