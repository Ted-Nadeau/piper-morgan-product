# Haiku 4.5 Test Protocol for Sprint A8 (REVISED)

**Version**: 2.0
**Last Updated**: October 24, 2025, 12:19 PM PDT
**Revised By**: Claude Code (prog-code)
**Approved By**: PM (xian)

---

## Objective

Test if **Claude Haiku 4.5** can replace **Sonnet 4.5** for Claude Code agent tasks while maintaining quality and achieving significant cost reduction (~70-80%).

**Scope**: This protocol tests **Claude Code agent** (external coding tool) performance only. Piper Morgan's internal model routing is a separate concern and not covered here.

---

## Test Setup

### Model Selection (CORRECTED)

Claude Code uses **CLI flags** for model selection, not environment variables.

**To test with Haiku:**
```bash
claude --model haiku
# Uses: claude-3-5-haiku-20241022
```

**To test with Sonnet (baseline/fallback):**
```bash
claude --model sonnet
# Uses: claude-sonnet-4-5-20250929 (current default)
```

**With fallback enabled:**
```bash
claude --model haiku --fallback-model sonnet
# Automatically falls back to Sonnet if Haiku is overloaded
```

**Current Version**: Claude Code 2.0.26

---

## Task Selection (Sprint A8 Real Work)

Use actual Sprint A8 tasks to get work done while collecting test data.

### Simple Complexity: Alpha Onboarding Documentation
**Task**: Create alpha tester onboarding materials
- User guides
- Setup instructions
- Feature documentation
- Known issues list

**Expected**: Haiku should excel here
- Writing-focused
- Clear requirements
- Low technical risk
- Easy to validate quality

### Medium Complexity: Thinking Token Optimization
**Task**: Optimize extended thinking token usage in codebase
- Analyze current usage patterns
- Identify optimization opportunities
- Implement token reduction strategies
- Measure performance impact

**Expected**: Haiku should handle this
- Focused scope
- Clear success metric (token count)
- Requires code analysis but not architectural changes
- Medium technical complexity

### Complex Complexity: Knowledge Graph Upgrade
**Task**: Upgrade knowledge graph implementation
- Multi-file coordination (10+ files)
- Integration with ethics/boundary systems
- High-stakes (can't break existing functionality)
- Architectural decisions required

**Expected**: Haiku might struggle
- Complex reasoning required
- System-wide implications
- Risk of breaking existing features
- Good test for "when to escalate"

**Decision**: Execute this task **last**, and only attempt with Haiku if earlier tasks showed strong performance.

---

## Execution Protocol

### Strategy: Hybrid Approach with Work Priority

**Primary Goal**: Complete Sprint A8 work efficiently
**Secondary Goal**: Collect model performance test data

**Approach**: Start with Haiku, escalate to Sonnet if needed, with explicit STOP conditions for visibility.

### Task Sequencing (Adaptive)

**Phase 1: Build Confidence (Simple Task)**
```
Task: Alpha Onboarding Documentation
Model: Haiku 4.5
Goal: Quick win, low risk
Outcome: Builds confidence in Haiku OR identifies immediate issues
```

**Phase 2: Test Limits (Medium Task)**
```
Task: Thinking Token Optimization
Model: Haiku 4.5 (start) → Sonnet 4.5 (if STOP triggered)
Goal: Test Haiku on real complexity
Outcome: Determines if Haiku ~= Sonnet 4.0 capability
```

**Phase 3: Make Informed Decision (Complex Task)**
```
Task: Knowledge Graph Upgrade
Model: Decision based on Phase 1-2 results
  - If Haiku excelled → Try with Haiku
  - If Haiku struggled → Use Sonnet directly
  - Don't waste time on risky test
Goal: Complete critical work efficiently
```

### STOP Conditions (Escalation Triggers)

When working with Haiku, **PAUSE and check in** if any of these occur:

⚠️ **Failure Count**: Haiku fails **twice** on the same subtask
- Example: Two incorrect implementations of same function
- Example: Repeated misunderstanding of requirements

⚠️ **Quality Issues**: Haiku produces code that **breaks existing tests**
- Regressions in test suite
- Introduces new bugs
- Fails validation checks

⚠️ **Architectural Confusion**: Haiku clearly **misunderstands architecture**
- Suggests changes that violate existing patterns
- Proposes solutions incompatible with system design
- Shows lack of context about codebase structure

⚠️ **Time Stall**: After **30 minutes** with no meaningful progress
- Spinning on same problem
- Multiple iterations without improvement
- Unclear next steps

**At STOP:**
1. ⏸️ **Pause work** immediately
2. 📝 **Document** what went wrong (error type, context, attempts made)
3. 💬 **Check in** with PM: "Switch to Sonnet or continue with Haiku?"
4. 🎯 **Decide** based on context (urgency, learning value, risk)

---

## Baseline Data (Sprints A4-A7)

Historical performance data from recent sprints using **Sonnet 4.5**:

### Sprint A4: Standup Epic (Oct 19-20)
- **Issues**: 4 issues
- **Duration**: ~1 day
- **Complexity**: Medium (handler implementation, API integration)
- **Success**: 100% completion, 0 regressions

### Sprint A5: Learning System (Oct 20-21)
- **Issues**: 5 issues
- **Duration**: ~6 hours total
- **Complexity**: High (new system architecture, multiple services)
- **Success**: 100% completion, exceptional leverage (2.4:1 ratio)
- **Quality**: 32/32 tests passing, production-ready

### Sprint A6: User Infrastructure (Oct 21-22)
- **Issues**: 6 issues
- **Duration**: Varied by complexity
- **Complexity**: High (database migrations, security, multi-user)
- **Success**: 100% completion, production hardening

### Sprint A7: Polish & Buffer (Oct 23)
- **Issues**: 7 issues (Groups 1-2 by Code agent, Groups 3-4 by Cursor)
- **Duration**: Groups 1-2 in ~1.5 hours (5 issues)
- **Complexity**: Mixed (bug fixes, migrations, CLI tools)
- **Success**: 100% completion, 0 regressions

**Key Metrics (Sonnet 4.5 Baseline)**:
- **Average time per issue**: 30-90 min (varies by complexity)
- **Success rate**: 100% (all issues completed)
- **Test pass rate**: 100% (no regressions introduced)
- **Self-correction**: ~4 errors per sprint, all fixed without user intervention
- **Leverage ratio**: 2.4:1 to 3.2:1 (existing:new code)

**Expected Haiku Performance**:
- **Speed**: 2x faster response time
- **Cost**: 70-80% reduction
- **Quality**: Acceptable if maintains 90%+ success rate
- **Iterations**: Max 1 additional iteration vs Sonnet

---

## Evaluation Metrics

### Quantitative Measures

**Cost Reduction**:
- Current (Sonnet 4.5): $3/M input, $15/M output
- Target (Haiku 4.5): $1/M input, $5/M output
- **Goal**: 70-80% cost savings

**Speed**:
- Haiku should be ~2x faster than Sonnet
- Measure: wall-clock time per task

**Success Rate**:
- **Accept**: 90%+ success rate
- **Reject**: <90% success rate

**Iteration Count**:
- **Accept**: Max 1 additional iteration vs Sonnet
- **Reject**: 2+ additional iterations required

### Qualitative Measures

**Code Quality**:
- Must pass all existing tests
- No regressions introduced
- Follows project patterns and conventions

**Documentation Clarity**:
- Must be comprehensible
- Accurate technical content
- Appropriate detail level

**Edge Case Handling**:
- Should identify major issues
- Appropriate error handling
- Security considerations addressed

**Following Instructions**:
- Respects gameplan constraints
- Adheres to project methodology (Inchworm Protocol)
- Uses existing infrastructure appropriately

---

## Decision Matrix

Based on test results, take action according to this matrix:

| Success Rate | Cost Savings | Action |
|--------------|--------------|--------|
| 90%+ | 70%+ | ✅ **Switch Code agent default to Haiku** |
| 70-89% | 50-70% | 🔀 **Use hybrid routing** (simple→Haiku, complex→Sonnet) |
| 50-69% | Any | 📝 **Keep for simple tasks only** (docs, boilerplate) |
| <50% | Any | ❌ **Stay with Sonnet** (Haiku not viable) |

**Additional Considerations**:
- If Haiku performs well but hits STOP frequently → Hybrid routing
- If Haiku quality inconsistent → Stay with Sonnet for now
- If time waste from failures > cost savings → Not worth it

---

## Expected Timeline

**Day 1 (Oct 24)**:
- Morning: Documentation task with Haiku (2-3 hours)
- Afternoon: Thinking token optimization with Haiku (2-4 hours)
- Evening: Initial analysis of results

**Day 2 (Oct 25)**:
- Morning: Knowledge graph task (model TBD based on Day 1)
- Afternoon: Comprehensive analysis and decision

**Day 3 (Oct 26)** (if needed):
- Final validation
- Document findings
- Implement routing if warranted

---

## Implementation Recommendations

### If Haiku Proves Viable (90%+ success):

**Immediate Action**:
```bash
# Set Haiku as default for future sessions
claude --model haiku

# Keep Sonnet available for complex work
claude --model sonnet
```

**Document Decision**:
- Update session logs with performance data
- Create ADR (Architecture Decision Record) if adopting hybrid routing
- Communicate findings to Chief of Staff

### If Hybrid Approach Needed (70-89% success):

**Task Complexity Detection** (manual for now):
- **Simple tasks**: Use Haiku (docs, tests, boilerplate)
- **Medium tasks**: Try Haiku, escalate if STOP triggered
- **Complex tasks**: Start with Sonnet (architecture, multi-file refactoring)

**Future Enhancement** (separate project):
Could develop automated routing in Piper Morgan's orchestration layer, but that's beyond this test scope.

### If Haiku Insufficient (<70% success):

**Stay with Sonnet**:
- Current approach works well
- Cost is acceptable for quality
- Wait for Haiku improvements or price changes

---

## Cost Analysis

### Current State (Sonnet 4.5 only):
- **Input**: $3/M tokens
- **Output**: $15/M tokens
- **Daily Sprint A8 estimate**: $30-50
- **Monthly estimate** (active development): $600-1000

### With Haiku 4.5 (90% replacement):
- **Haiku costs**: $1/M input, $5/M output
- **90% of tasks on Haiku**: ~$5/day
- **10% critical on Sonnet**: ~$5/day
- **Daily total**: ~$10 **(70-80% reduction)**
- **Monthly total**: ~$200-300

### With Hybrid Routing (70% replacement):
- **70% on Haiku**: ~$4/day
- **30% on Sonnet**: ~$12/day
- **Daily total**: ~$16 **(~50% reduction)**
- **Monthly total**: ~$320-480

**Break-even Analysis**:
- If Haiku adds 1 extra hour/day of work → cost savings lost
- If Haiku quality issues require rework → not worth it
- Need to maintain >80% efficiency vs Sonnet to be worthwhile

---

## Risk Mitigation

### Always Keep Sonnet Fallback
- Critical decisions
- Architectural work
- Multi-file refactoring
- When speed matters more than cost

### Monitor Closely for Quality Issues
- Run full test suite after Haiku work
- Check for subtle regressions
- Validate architectural decisions
- Review complex code more carefully

### Human Oversight
- PM should review architectural decisions regardless of model
- STOP conditions ensure visibility
- Check-ins prevent waste

### Abort if Not Working
- If Haiku causes 2+ hours of wasted time → Stop testing
- If quality issues appear in production → Revert to Sonnet
- If stress/confusion increases → Not worth the savings

---

## Success Criteria

Test is **successful** if:
- ✅ Haiku completes 90%+ of tasks successfully
- ✅ No regressions introduced
- ✅ Cost reduction of 70%+
- ✅ Time efficiency maintained (±20% of Sonnet)
- ✅ Quality remains production-ready

Test is **partially successful** if:
- 🔀 Haiku completes 70-89% successfully → Use hybrid routing
- 🔀 Clear simple/complex divide → Route by complexity

Test is **unsuccessful** if:
- ❌ Success rate <70%
- ❌ Quality issues persist
- ❌ Time waste > cost savings
- ❌ Cognitive load increases significantly

---

## Notes

### Key Insight from Chief of Staff
> "Haiku 4.5 reportedly matches Sonnet 4.0 performance. Given our success with Sonnet 4.0 throughout September, this should be sufficient for most Code agent tasks."

**Validation Strategy**:
- Compare Haiku 4.5 to historical Sonnet 4.0 work (September baseline)
- Compare Haiku 4.5 to recent Sonnet 4.5 work (Sprints A4-A7)
- Both comparisons should show Haiku is viable for 70%+ of work

### Test Philosophy
- **Work first, test second** - Don't sacrifice Sprint A8 progress for pure testing
- **Adaptive approach** - Use early results to inform later decisions
- **Explicit visibility** - STOP conditions ensure PM awareness
- **No pure A/B testing** - Use historical data as baseline, real work as test

### Lessons from Protocol Revision
1. ✅ Configuration method matters (CLI flags, not env vars)
2. ✅ Test scope clarity matters (Claude Code vs Piper Morgan)
3. ✅ Real work > synthetic tests (get value while testing)
4. ✅ Risk management matters (STOP conditions, task sequencing)
5. ✅ Historical baseline > parallel testing (efficiency)

---

## Appendix: Changes from Original Protocol

**What Changed:**
1. **Configuration**: Fixed to use `--model` CLI flags (not env vars)
2. **Tasks**: Specified Sprint A8 real work (not generic examples)
3. **Sequencing**: Added adaptive task ordering (simple → medium → complex)
4. **STOP Conditions**: Explicit escalation triggers with check-in requirement
5. **Baseline**: Expanded to Sprints A4-A7 (not just parallel testing)
6. **Scope**: Removed Piper Morgan code (focus on Claude Code only)
7. **Strategy**: Changed to "work first, test second" (was pure testing)

**Why Changed:**
- Original assumed wrong configuration mechanism
- Original lacked concrete test tasks
- Original didn't account for risk management
- Original scope confused Claude Code vs Piper Morgan
- Original required duplicate work (inefficient)

**Result**: More practical, executable protocol that delivers value while testing.

---

**Protocol Status**: ✅ APPROVED
**Ready for Execution**: Yes
**Next Step**: Begin Phase 1 (Documentation with Haiku) when ready
**Created**: October 24, 2025, 12:19 PM PDT
