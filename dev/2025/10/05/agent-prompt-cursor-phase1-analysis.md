# Prompt for Cursor Agent: GREAT-4B Phase 1 - Medium Priority Analysis

## Context from Phase 0

Baseline complete:
- 6 medium priority bypasses (3 CLI + 3 web)
- Code handling high priority (5 items)
- Your task: Analyze medium priority for Phase 2 planning

## Session Log

Continue: `dev/2025/10/05/2025-10-05-1540-prog-cursor-log.md`

## Mission

**Analyze 6 medium-priority bypasses** to determine conversion strategy, effort, and dependencies for Phase 2.

---

## Phase 1: Medium Priority Analysis

### Step 1: Review Baseline Report

```bash
cat dev/2025/10/05/intent-baseline-report.md
```

Identify the 6 medium priority items (3 CLI + 3 web).

### Step 2: Analyze Each Bypass

For EACH of the 6 medium priority bypasses:

**Create analysis document**: `dev/2025/10/05/medium-priority-analysis.md`

```markdown
# Medium Priority Bypass Analysis

## CLI Command: [name]

**File**: cli/commands/[name].py
**Current State**: Direct service call
**Reason for Medium Priority**: [from baseline]

**Conversion Complexity**: Small/Medium/Large
**Estimated Effort**: 15min/30min/1hr
**Dependencies**: None / Requires X
**Slack Pattern Applicability**: Yes/No

**Conversion Approach**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Test Strategy**:
- [ ] Test point 1
- [ ] Test point 2

---

## Web Route: [path]

[Same analysis structure]

---

## Summary

Total medium priority items: 6
- CLI commands: 3
- Web routes: 3

Total estimated effort: X hours
Recommended approach: [Sequential/Parallel/Batched]
Dependencies: [List any]
```

### Step 3: Prioritize Within Medium

Rank the 6 items by conversion ease:

```markdown
## Conversion Priority Order

1. **[Item Name]** - Effort: Small, No dependencies
2. **[Item Name]** - Effort: Small, No dependencies
3. **[Item Name]** - Effort: Medium, Depends on #1
4. **[Item Name]** - Effort: Medium, No dependencies
5. **[Item Name]** - Effort: Large, Complex
6. **[Item Name]** - Effort: Large, Complex

Recommended Phase 2 sequence: 1 → 2 → 4 → 3 → 5 → 6
```

### Step 4: Document Slack Pattern Applicability

Study how Slack's pattern applies to each bypass:

```bash
# For CLI bypasses
grep -A 30 "execute" services/integrations/slack/[handler].py

# For Web bypasses
grep -A 30 "@app" services/integrations/slack/[handler].py
```

Document which pattern elements apply:
- Intent classification wrapper?
- Canonical handler routing?
- Direct intent endpoint redirect?

### Step 5: Create Phase 2 Recommendation

```markdown
# Phase 2 Conversion Recommendation

## Approach
[Sequential/Parallel/Hybrid]

## Grouping Strategy
- Group 1: [Items 1-2] - Quick wins (1 hour)
- Group 2: [Items 3-4] - Standard conversions (2 hours)
- Group 3: [Items 5-6] - Complex cases (2 hours)

Total Phase 2 estimate: 5 hours

## Risk Factors
- [Risk 1]: Mitigation
- [Risk 2]: Mitigation

## Success Metrics
- All 6 medium priority bypasses converted
- Bypass count reduced to exclusions only
- Detection tests all pass
```

---

## Success Criteria

- [ ] All 6 medium bypasses analyzed
- [ ] Conversion complexity estimated
- [ ] Priority order recommended
- [ ] Slack pattern applicability documented
- [ ] Phase 2 plan created
- [ ] Total effort estimated

---

## Deliverables

1. **Analysis Doc**: `medium-priority-analysis.md`
2. **Phase 2 Plan**: Conversion sequence and estimates
3. **Session Log**: Analysis process documented

---

*Estimated: 30-45 minutes for analysis*
