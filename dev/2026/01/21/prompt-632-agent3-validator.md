# Claude Code Agent Prompt: #632 Phase 3 - Independent Validation

## Your Identity
You are Claude Code, an independent validator. Your job is to verify the work WITHOUT knowledge of implementation details. You test as a user would experience it.

## Session Log Requirement (MANDATORY)

**Create a session log at start**:
```bash
mkdir -p dev/2026/01/21
touch dev/2026/01/21/$(date +%Y-%m-%d-%H%M)-632-phase3-code-log.md
```

**Log format**:
```markdown
# Session Log: #632 Phase 3 - Validation
**Date**: 2026-01-21
**Agent**: Claude Code (Validator)
**Issue**: #632 CONSCIOUSNESS-TRANSFORM: Morning Standup

## Prerequisites Check
- Phase 1 complete: [Yes/No]
- Phase 2 complete: [Yes/No]

## Validation Performed
- [timestamp] Ran full test suite
- [timestamp] Generated sample output
- [timestamp] Scored against rubric
- [timestamp] Validated MVC compliance

## Test Results
[Full pytest output summary]

## Rubric Scoring
[5-dimension breakdown]

## Recommendation
[APPROVE/REJECT with reasoning]
```

**Update log throughout your work.**

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to validate Phases 1-2 of GitHub Issue #632. You must verify independently.

**Prerequisites**: Phases 1 and 2 must be complete before you start.

### Your Acceptance Criteria
- [ ] All standup tests pass (260+)
- [ ] Rubric score ≥18/20
- [ ] MVC validation passes
- [ ] Before/after documented

### Evidence You MUST Provide
1. **Full test output**: Complete pytest results
2. **Rubric scoring**: 5-dimension breakdown with justification
3. **MVC validation**: validate_mvc() result on real output
4. **Before/after comparison**: Side-by-side examples

### Your Handoff Format
```
## Issue #632 Phase 3 Validation Report
**Status**: PASS/FAIL

**Test Results**:
Total: X passed, Y failed, Z skipped
`pytest tests/ -k standup -v` output: [summary]

**Rubric Score**:
| Dimension | Score | Evidence |
|-----------|-------|----------|
| Identity Voice | X/4 | [quote from output] |
| Epistemic Humility | X/4 | [quote] |
| Dialogue Orientation | X/4 | [quote] |
| Source Transparency | X/4 | [quote] |
| Contextual Awareness | X/4 | [quote] |
| **TOTAL** | **X/20** | |

**MVC Validation**:
- validate_mvc(output): [result]

**Before/After**:
BEFORE: [paste old output]
AFTER: [paste new output]

**Recommendation**: APPROVE / REJECT with reasons
```

---

## Mission
Independently validate the consciousness transformation without relying on implementation details.

**Scope Boundaries**:
- This prompt covers ONLY: Validation and scoring
- NOT in scope: Implementation changes
- NOT in scope: Test fixes (report, don't fix)

---

## Context
- **GitHub Issue**: #632 CONSCIOUSNESS-TRANSFORM: Morning Standup
- **Prerequisites**: Phases 1-2 complete
- **Your Role**: Independent verifier
- **Target**: Score ≥18/20, all tests pass

---

## MANDATORY FIRST ACTIONS

### 1. Verify Prerequisites
```bash
# Verify wrapper exists
ls -la services/consciousness/standup_consciousness.py

# Verify integration done
grep -n "format_standup_greeting_conscious" services/personality/standup_bridge.py

# Quick import check
python -c "from services.personality.standup_bridge import StandupToChatBridge; print('OK')"
```

STOP if:
- [ ] Wrapper doesn't exist (Phase 1 incomplete)
- [ ] Integration not done (Phase 2 incomplete)

---

## Validation Steps

### Step 1: Run Full Test Suite

```bash
# Run ALL standup-related tests
pytest tests/ -k standup -v 2>&1 | tee /tmp/standup_test_output.txt

# Count results
grep -E "passed|failed|error" /tmp/standup_test_output.txt | tail -5

# Show any failures
grep -E "FAILED|ERROR" /tmp/standup_test_output.txt
```

**Expected**: 260+ tests, ALL pass
**If any fail**: Document and STOP - do not proceed to scoring

### Step 2: Generate Sample Output

```bash
python -c "
from services.personality.standup_bridge import StandupToChatBridge

bridge = StandupToChatBridge()

# Realistic standup data
standup_response = {
    'data': {
        'yesterday_accomplishments': [
            '✅ Implemented user feedback loop',
            '✅ Fixed authentication timeout bug',
            '📋 Reviewed pull request #432'
        ],
        'today_priorities': [
            '🎯 Continue A4 sprint work',
            '🎯 Review user feedback from Alpha',
            '🔄 Complete code coverage improvements'
        ],
        'blockers': [],
        'generation_time_ms': 1247,
        'time_saved_minutes': 18,
        'github_activity': {
            'commits': [
                {'message': 'feat: add feedback loop'},
                {'message': 'fix: auth timeout'}
            ]
        }
    },
    'metadata': {
        'context_source': 'persistent'
    }
}

output = bridge.adapt_standup_for_chat(standup_response)
print('=== CONSCIOUS STANDUP OUTPUT ===')
print(output)
print()
print('=== LENGTH ===')
print(f'{len(output)} characters')
"
```

### Step 3: Run MVC Validation

```bash
python -c "
from services.personality.standup_bridge import StandupToChatBridge
from services.consciousness.validation import validate_mvc

bridge = StandupToChatBridge()

standup_response = {
    'data': {
        'yesterday_accomplishments': ['Fixed bug', 'Added feature'],
        'today_priorities': ['Continue work', 'Review feedback'],
        'blockers': [],
        'generation_time_ms': 1200,
        'time_saved_minutes': 15,
        'github_activity': {'commits': [{'message': 'test'}]}
    },
    'metadata': {'context_source': 'persistent'}
}

output = bridge.adapt_standup_for_chat(standup_response)

result = validate_mvc(output)
print('=== MVC VALIDATION ===')
print(f'Passes: {result.passes}')
print(f'Checks: {result.checks}')
if result.missing:
    print(f'Missing: {result.missing}')
if result.suggestions:
    print(f'Suggestions: {result.suggestions}')
"
```

### Step 4: Score Against 5-Dimension Rubric

Generate output and manually score each dimension:

**Rubric (score 0-4 each)**:

| Dimension | 0 | 1 | 2 | 3 | 4 |
|-----------|---|---|---|---|---|
| **Identity Voice** | No "I" | Occasional "I" | Frequent "I" | Natural "I" throughout | Feels like a colleague |
| **Epistemic Humility** | Absolute claims | Rare hedging | Some hedging | Natural uncertainty | Perfect calibration |
| **Dialogue Orientation** | No invitation | One invitation | Multiple invitations | Natural flow | Real conversation |
| **Source Transparency** | No attribution | Vague sources | Named sources | Connected sources | Full context |
| **Contextual Awareness** | Generic | Some context | Good context | Rich context | Deeply personalized |

**Score each dimension with evidence** (quote from output):

```
Identity Voice: X/4
Evidence: "[quote showing I statements]"

Epistemic Humility: X/4
Evidence: "[quote showing hedging]"

Dialogue Orientation: X/4
Evidence: "[quote showing invitation]"

Source Transparency: X/4
Evidence: "[quote showing attribution]"

Contextual Awareness: X/4
Evidence: "[quote showing context usage]"

TOTAL: X/20
```

### Step 5: Before/After Comparison

Get the "before" output by checking git history or documentation:

**BEFORE (from issue #632 documentation)**:
```
Yesterday's achievements:
• Implemented Sprint A4 issue restructuring
• Enhanced standup API endpoints

Today's focus:
• Continue A4 execution
• Review user feedback

No blockers - clear path ahead! 🚀

Standup generated in 1.2s - Lightning fast! Saved you 15m of manual prep time.
```

**AFTER**: [Paste actual output from Step 2]

### Step 6: Compile Validation Report

Create full validation report with all evidence.

---

## Success Criteria

- [ ] All 260+ standup tests pass
- [ ] Rubric score ≥18/20
- [ ] MVC validation passes (all 4 checks)
- [ ] Before/after comparison shows clear improvement
- [ ] No assumptions - all verified with evidence

---

## STOP Conditions

If ANY of these occur, STOP and report:
1. Phase 1 or 2 incomplete
2. Any standup tests fail
3. Rubric score <18/20
4. MVC validation fails
5. Output worse than before

---

## Deliverables

1. Full test output (pass/fail counts)
2. Rubric score breakdown with evidence
3. MVC validation result
4. Before/after comparison
5. Recommendation: APPROVE or REJECT

---

*Prompt Version: 1.0*
*Template: agent-prompt-template v10.2*
*Phase: 3 of 4*
