# Haiku 4.5 Test Protocol for Sprint A8

## Objective
Test if Claude Haiku 4.5 can replace Sonnet 4.5 for Code agent tasks while maintaining quality and achieving 90% cost reduction.

## Test Setup

### 1. Create Parallel Test Environment
```bash
# In Claude Code, configure dual model access:
export ANTHROPIC_MODEL_DEFAULT="claude-3-5-sonnet-20241022"
export ANTHROPIC_MODEL_TEST="claude-3-5-haiku-20241022"
```

### 2. Select Test Tasks from Sprint A8
Choose 3 task categories of varying complexity:

**Simple (Expected: Haiku handles well)**
- Writing test cases
- Creating documentation
- Generating boilerplate code
- Formatting/linting fixes

**Medium (Expected: Haiku probably sufficient)**
- Implementing straightforward features
- Bug fixes with clear requirements
- API endpoint creation
- Configuration updates

**Complex (Expected: Might need Sonnet)**
- Architectural decisions
- Complex debugging
- Performance optimization
- Multi-file refactoring

## Test Protocol

### Phase 1: Baseline (Day 1)
1. Select one task from each category
2. Complete with Sonnet 4.5 (current approach)
3. Record:
   - Time to completion
   - Number of iterations needed
   - Quality of output
   - Token usage and cost

### Phase 2: Haiku Test (Day 1-2)
1. Select similar tasks from each category
2. Complete with Haiku 4.5
3. Record same metrics
4. Note any specific failures or quality issues

### Phase 3: Hybrid Approach (Day 2-3)
Test intelligent routing:
- Start with Haiku 4.5 for all tasks
- Escalate to Sonnet only if:
  - Haiku fails twice on same task
  - Output quality clearly insufficient
  - Complex reasoning required

## Evaluation Metrics

### Quantitative
- **Cost reduction**: Target 80%+ savings
- **Speed**: Haiku should be 2x faster
- **Success rate**: Accept 90% success rate
- **Iteration count**: Max 1 additional iteration vs Sonnet

### Qualitative
- **Code quality**: Must pass all tests
- **Documentation clarity**: Must be comprehensible
- **Edge case handling**: Should identify major issues
- **Following instructions**: Must respect gameplan constraints

## Decision Matrix

| Scenario | Action |
|----------|--------|
| Haiku succeeds on 90%+ tasks | Switch Code agent to Haiku |
| Haiku succeeds on 70-89% | Use hybrid routing approach |
| Haiku succeeds on 50-69% | Keep for simple tasks only |
| Haiku succeeds on <50% | Stay with Sonnet |

## Implementation Recommendations

### If Haiku Proves Viable:

**Immediate Changes:**
1. Update Code agent default model
2. Implement task complexity detection
3. Add model fallback logic

**Configuration Example:**
```python
# In Piper's config
MODEL_ROUTING = {
    "simple": "claude-3-5-haiku-20241022",
    "medium": "claude-3-5-haiku-20241022",
    "complex": "claude-3-5-sonnet-20241022",
    "critical": "claude-3-opus-20240229"
}

# Prompt caching for repeated patterns
ENABLE_PROMPT_CACHE = True  # 90% cost reduction
CACHE_PATTERNS = [
    "gameplan_template",
    "test_structure",
    "documentation_format"
]
```

**For Piper's User-Facing Logic:**
```python
def select_model(task_complexity, user_preference):
    if user_preference == "cost_optimize":
        return "haiku" if task_complexity < 0.7 else "sonnet"
    elif user_preference == "quality_first":
        return "sonnet" if task_complexity > 0.3 else "haiku"
    else:  # balanced
        return "haiku" if task_complexity < 0.5 else "sonnet"
```

## Cost Analysis

### Current (Sonnet 4.5 only):
- Input: $3/M tokens
- Output: $15/M tokens
- Daily Sprint A8 estimate: $30-50

### With Haiku 4.5 (90% replacement):
- Haiku: $1/M input, $5/M output
- 90% of tasks on Haiku: ~$5
- 10% critical on Sonnet: ~$5
- **Daily total: $10 (70-80% reduction)**

### With Prompt Caching:
- Additional 90% reduction on repeated patterns
- Potential daily cost: $2-5

## Risk Mitigation

1. **Always keep Sonnet fallback** for critical decisions
2. **Run parallel for first day** to ensure no quality degradation
3. **Monitor closely** for subtle quality issues
4. **Keep human oversight** for architectural decisions

## Timeline

- **Oct 24-25**: Run parallel tests
- **Oct 26**: Analyze results, make decision
- **Oct 27-28**: Implement routing if viable
- **Oct 29**: Deploy for alpha with smart routing

---

*Note: Haiku 4.5 reportedly matches Sonnet 4.0 performance. Given our success with Sonnet 4.0 throughout September, this should be sufficient for most Code agent tasks.*
