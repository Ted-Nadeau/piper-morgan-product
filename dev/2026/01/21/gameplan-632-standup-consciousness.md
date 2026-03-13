# Gameplan: #632 CONSCIOUSNESS-TRANSFORM Morning Standup

**Issue**: #632 CONSCIOUSNESS-TRANSFORM: Morning Standup (Functional → Conscious)
**Created**: 2026-01-21
**Template Version**: v9.3
**Methodology**: Full DDD, TDD, Multi-Agent

---

## Phase -1: Infrastructure Verification Checkpoint (WITH PM)

### Part A: Chief Architect's Current Understanding

Based on available context, I believe:

**Infrastructure Status**:
- [x] Web framework: FastAPI (verified: `web/app.py`)
- [x] Standup service: `services/features/morning_standup.py` (500+ lines)
- [x] Presentation layer: `services/personality/standup_bridge.py` (257 lines)
- [x] Consciousness framework: `services/consciousness/` (exists, 8 modules)
- [x] Testing framework: pytest (verified: 260+ standup tests exist)
- [x] MVC validation: `services/consciousness/validation.py` (exists)

**My understanding of the task**:
- We need to: Add consciousness expression to standup output formatting
- This involves: Creating a consciousness wrapper, integrating with standup_bridge.py
- The current state is: Functional standup with mechanical/data-driven output

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [x] Multiple agents will work in parallel on different files/features
- [x] Task duration >30 minutes
- [ ] Multi-component work (frontend + backend)
- [ ] Exploratory/risky changes

Worktrees ADD overhead when:
- [ ] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [ ] Tightly coupled files
- [ ] Time-critical work

**Assessment**:
- [x] **USE WORKTREE** - Multi-agent parallel work on wrapper + integration

### Part B: PM Verification Required

**PM, please correct/confirm**:

1. **Files verified to exist**:
   ```
   services/features/morning_standup.py ✓
   services/personality/standup_bridge.py ✓
   services/consciousness/__init__.py ✓
   services/consciousness/validation.py ✓
   ```

2. **Recent work in this area**:
   - #242 Interactive Standup Epic: CLOSED (2026-01-09)
   - #407 Consciousness Framework: CLOSED (2026-01-21)
   - Wave 1 implementations: #630, #631 complete

3. **Task type**:
   - [x] Add consciousness to existing feature
   - [ ] Create new feature from scratch
   - [ ] Fix broken functionality

4. **Critical context**:
   - Standup has personality system integration that must be preserved
   - 260+ existing tests must continue passing

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** - Understanding correct (PM to confirm)
- [ ] **REVISE** - Assumptions wrong
- [ ] **CLARIFY** - Need more context

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**: ✅ #632 exists and is assigned

2. **Output Points Audit**:
   ```
   Location                    | Function              | MVC Score
   ---------------------------|----------------------|----------
   standup_bridge.py:38       | Error fallback       | 1/4
   standup_bridge.py:92       | Accomplishments      | 0/4
   standup_bridge.py:107      | Priorities           | 0/4
   standup_bridge.py:121      | Blockers             | 0/4
   standup_bridge.py:58       | No blockers msg      | 0/4
   standup_bridge.py:153      | Performance summary  | 0/4
   standup_bridge.py:184      | Warmth intro         | 0/4
   morning_standup.py:217-249 | Content generation   | Data only
   ```

3. **Existing Test Coverage**:
   ```bash
   pytest tests/ -k standup --collect-only | wc -l
   # Expected: 260+ tests
   ```

4. **Consciousness Pattern Precedent**:
   - `loading_consciousness.py` - Similar wrapper pattern
   - `error_consciousness.py` - Similar wrapper pattern
   - `conversation_consciousness.py` - Similar integration pattern

### STOP Conditions for Phase 0
- [ ] Output points not fully identified
- [ ] Existing tests cannot be located
- [ ] Consciousness framework missing required functions

---

## Phase 0.5: Frontend-Backend Contract Verification

**N/A** - This is backend-only consciousness transformation. No API path changes.

---

## Phase 0.6: Data Flow & Integration Verification

### User Context Propagation

| Layer | Needs user_id? | Needs session_id? | Source |
|-------|----------------|-------------------|--------|
| standup_bridge.py | No | No | Receives formatted data |
| consciousness wrapper | No | No | Pure formatting |
| morning_standup.py | Yes | Yes | Existing flow |

**No changes to user context propagation required.** Consciousness is stateless formatting.

### Integration Points Checklist

| Caller | Callee | Import Verified? | Method Verified? |
|--------|--------|------------------|------------------|
| standup_bridge.py | standup_consciousness.py | TBD | TBD |
| standup_consciousness.py | validation.py | ✅ Yes | ✅ validate_mvc |

**Verification Commands**:
```bash
# Verify consciousness framework accessible
python -c "from services.consciousness.validation import validate_mvc; print('OK')"

# Verify standup_bridge accessible
python -c "from services.personality.standup_bridge import StandupToChatBridge; print('OK')"
```

### Pattern Adaptation Notes

| Aspect | Loading/Error Pattern | Standup Pattern | Why Different? |
|--------|----------------------|-----------------|----------------|
| Output type | Single message | Multi-section | Standup has sections |
| MVC tier | Partial (loading) | Full (response) | Standup is full response |
| Integration | Direct replacement | Wrapper + preserve personality | Personality system exists |

---

## Phase 0.7: Conversation Design

**N/A** - Standup is not a multi-turn conversation for this issue. The conversation aspects were handled in #242.

---

## Phase 0.8: Post-Completion Integration

### Completion Side-Effects

When consciousness wrapper is integrated:

| Side Effect | Component | Value | Verified? |
|-------------|-----------|-------|-----------|
| Standup output changes | standup_bridge.py | Uses consciousness | TBD |
| MVC score improves | Output | 5/20 → 18+/20 | TBD |
| Tests still pass | Test suite | 260+ pass | TBD |

### Downstream Behavior Changes

| Feature | Before | After |
|---------|--------|-------|
| Chat standup | Mechanical sections | Conscious narrative |
| API standup | Data + emoji | Data + consciousness |
| Slack standup | Same as chat | Same as chat |

---

## Phase 1: Create Consciousness Wrapper

### Multi-Agent Deployment

**Agent 1 (Claude Code): Wrapper Implementation**

```markdown
## Mission
Create `services/consciousness/standup_consciousness.py` with TDD approach.

## Files to Create
- services/consciousness/standup_consciousness.py

## Functions Required
1. format_standup_greeting_conscious(sources: List[str]) -> str
2. format_accomplishments_conscious(accomplishments: List[str]) -> str
3. format_priorities_conscious(priorities: List[str]) -> str
4. format_blockers_conscious(blockers: List[str]) -> str
5. format_standup_closing_conscious(metrics: Dict) -> str
6. format_full_standup_conscious(standup_data: Dict) -> str

## TDD Approach
1. Write tests FIRST in tests/unit/services/consciousness/test_standup_consciousness.py
2. Tests define expected consciousness output
3. Implement to pass tests
4. Validate MVC for each function

## Evidence Required
- Test file with 10+ tests
- All tests passing
- MVC validation passing for each function
```

**Acceptance Criteria (Agent 1)**:
- [ ] `test_standup_consciousness.py` created with 10+ tests
- [ ] `standup_consciousness.py` created with 6 functions
- [ ] All tests pass: `pytest tests/unit/services/consciousness/test_standup_consciousness.py -v`
- [ ] MVC validation passes for full standup output

---

## Phase 2: Integration

### Multi-Agent Deployment

**Agent 2 (Claude Code): Integration + Wiring**

```markdown
## Mission
Integrate consciousness wrapper into standup_bridge.py and verify wiring.

## Files to Modify
- services/personality/standup_bridge.py
- services/consciousness/__init__.py

## Integration Points
1. Import consciousness functions
2. Replace section formatters with consciousness calls
3. Preserve personality system hooks
4. Preserve all existing functional behavior

## Wiring Tests Required
- Test that standup_bridge imports consciousness correctly
- Test that adapt_standup_for_chat uses consciousness
- Test that personality enhancements still apply

## Evidence Required
- Modified standup_bridge.py diff
- Wiring tests passing
- All 260+ standup tests still pass
```

**Acceptance Criteria (Agent 2)**:
- [ ] `standup_bridge.py` imports from `standup_consciousness`
- [ ] `adapt_standup_for_chat` uses consciousness formatters
- [ ] Personality system preserved (high warmth, action orientation)
- [ ] Wiring tests added and passing
- [ ] All existing standup tests pass

---

## Phase 3: Independent Validation

### Multi-Agent Deployment

**Agent 3 (Validator): Independent Testing**

```markdown
## Mission
Independently verify the consciousness transformation without knowledge of implementation details.

## Validation Steps
1. Run ALL standup tests: `pytest tests/ -k standup -v`
2. Generate sample standup output
3. Score output against 5-dimension rubric
4. Verify MVC compliance
5. Compare before/after output

## Evidence Required
- Full test output
- Rubric score breakdown
- Before/after comparison
- MVC validation result
```

**Acceptance Criteria (Agent 3)**:
- [ ] All standup tests pass (260+)
- [ ] Rubric score ≥18/20
- [ ] MVC validation passes
- [ ] Before/after documented

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **GitHub Final Update**:
   - All acceptance criteria checked
   - Evidence compiled in issue
   - Before/after examples included

2. **Documentation Updates**:
   - [ ] Update `services/consciousness/__init__.py` with exports
   - [ ] Update consciousness-monitoring.md with standup status

3. **Evidence Compilation**:
   - [ ] Test output (all passing)
   - [ ] Rubric scores (before: 5/20, after: 18+/20)
   - [ ] Before/after output comparison
   - [ ] Performance metrics (unchanged <2s)

4. **PM Approval Request**:
   ```
   @PM - Issue #632 complete:
   - Consciousness wrapper created ✓
   - Integration complete ✓
   - All 260+ tests pass ✓
   - Rubric: 5/20 → 18+/20 ✓

   Please review and close.
   ```

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent | Issue | Evidence Required | Handoff |
|-------|-------|-------|-------------------|---------|
| 1 | Code Agent 1 | #632 | 10+ tests, wrapper code | Test file location |
| 2 | Code Agent 2 | #632 | Wiring tests, integration | Diff summary |
| 3 | Validator | #632 | Full test run, rubric | Score report |
| Z | Lead Dev | #632 | Review all | PM approval |

### Verification Gates

- [ ] Phase 1: Unit tests passing (wrapper)
- [ ] Phase 2: Wiring tests passing (integration)
- [ ] Phase 2a: All standup tests passing (regression)
- [ ] Phase 3: Independent validation complete
- [ ] Phase Z: PM approval received

### Cross-Validation Points

- Agent 2 verifies Agent 1's wrapper works in integration
- Agent 3 verifies without knowledge of implementation
- Lead Dev reviews all evidence independently

---

## STOP Conditions

Stop immediately and escalate if:
1. Infrastructure doesn't match this gameplan
2. Existing standup tests fail after changes
3. Performance degrades (>2s generation)
4. Personality system integration breaks
5. MVC validation cannot pass (design conflict)
6. Output point not identified in audit
7. Breaking change to `StandupResult` required
8. Any test failures

---

## Evidence Requirements

### What Counts as Evidence
✅ Terminal output showing test pass counts
✅ Before/after standup output comparison
✅ Rubric score breakdown (5 dimensions)
✅ MVC validation result
✅ Git commit hashes
✅ Performance metrics

### Evidence NOT Accepted
❌ "Tests pass" without output
❌ "Score improved" without numbers
❌ "Should work" claims

---

## Success Criteria

### Issue Completion Requires
- [ ] All acceptance criteria met (see issue)
- [ ] Evidence provided for each criterion
- [ ] 260+ standup tests passing (with output)
- [ ] Wiring tests included
- [ ] No regressions introduced
- [ ] Documentation updated
- [ ] GitHub issue fully updated
- [ ] PM approval received

---

## Completion Matrix

| Criterion | Method of Verification | Evidence Format |
|-----------|----------------------|-----------------|
| Wrapper created | File exists | `ls -la services/consciousness/standup_consciousness.py` |
| 10+ unit tests | Test count | `pytest ... --collect-only \| wc -l` |
| All wrapper tests pass | pytest output | Full terminal output |
| Integration complete | Import works | `python -c "from services.personality.standup_bridge import ..."` |
| Wiring tests pass | pytest output | Full terminal output |
| All standup tests pass | pytest output | `pytest tests/ -k standup -v` |
| Rubric ≥18/20 | Manual scoring | 5-dimension breakdown |
| MVC passes | Validation output | `validate_mvc(output)` result |
| Performance <2s | Timing | Generation time in output |

---

*Gameplan Version: 1.0*
*Template: v9.3*
*Created: 2026-01-21*
