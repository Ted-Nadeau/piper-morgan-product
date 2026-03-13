# Cursor Agent Prompt: Issue #288 - Learning System Investigation

## Your Identity
You are Cursor Agent, a specialized investigation and documentation agent working on the Piper Morgan project. Your role is to explore code, test systems, and create clear documentation.

## Essential Context
Read these briefing documents first:
- `docs/briefing/PROJECT.md` - What Piper Morgan is
- `docs/briefing/BRIEFING-CURRENT-STATE.md` - Current epic and focus
- `docs/briefing/BRIEFING-ESSENTIAL-AGENT.md` - Your role requirements

---

## Task Overview

**Issue**: #288 - CORE-ALPHA-LEARNING-INVESTIGATION
**Type**: Investigation + Documentation
**Priority**: P3 (Quality Improvement)
**Estimated Effort**: 3 hours

**Problem**: Learning system behavior is unclear. Not recording patterns during testing.

**Goal**: Document how the learning system works, how to activate it, and how to verify it's working.

---

## Background

During alpha testing preparation, it's unclear:
- What triggers pattern recording?
- Is learning automatic or manual?
- Does it behave differently for API vs web UI?
- What configuration flags exist?
- What's the expected latency for pattern recording?

**PM wants to know**: How does the learning system actually work, and how can alpha testers verify it's learning?

---

## Investigation Plan

### Phase 1: Code Review (1 hour)

**Objective**: Understand the learning system architecture

**Files to Investigate**:

1. **Learning System Entry Points**:
```bash
# Find learning-related files
find . -name "*learn*" -type f | grep -v ".pyc" | grep -v "__pycache__"

# Find pattern-related files
find . -name "*pattern*" -type f | grep -v ".pyc" | grep -v "__pycache__"

# Search for learning imports
grep -r "learning" services/ --include="*.py" | head -20
```

2. **Key Areas to Explore**:
- `services/learning/` - Core learning implementation
- `services/context/` - Context that might feed learning
- `services/conversation/` - Where conversations are processed
- Database models for pattern storage
- Configuration files for learning settings

3. **Questions to Answer from Code**:
- [ ] What classes/modules implement learning?
- [ ] What triggers pattern recording?
- [ ] What data gets stored?
- [ ] Is it automatic or requires activation?
- [ ] What configuration options exist?
- [ ] Any API endpoints for learning?

**Document Structure**:
```markdown
## Code Architecture

### Core Classes
- [List main classes with brief descriptions]

### Trigger Points
- [When/how does learning activate]

### Data Storage
- [What tables/models store learning data]

### Configuration
- [What settings control learning]
```

---

### Phase 2: Documentation Review (30 minutes)

**Objective**: Find existing documentation about learning

**Search for Documentation**:
```bash
# Check existing docs
grep -r "learning" docs/ README.md

# Check ADRs
grep -r "learning" docs/decisions/

# Check patterns
grep -r "learning" docs/patterns/

# Check knowledge docs
grep -r "learning" knowledge/
```

**Questions to Answer**:
- [ ] What's already documented?
- [ ] What's missing?
- [ ] Any outdated information?
- [ ] User-facing documentation exists?

**Document Gaps**:
```markdown
## Existing Documentation

### What Exists
- [List files with learning documentation]

### What's Missing
- [Gaps that need filling]

### What's Outdated
- [Documentation needing updates]
```

---

### Phase 3: Runtime Testing (1 hour)

**Objective**: Test learning system in actual operation

**Test Scenarios**:

**Test 1: Basic Pattern Recording**
```bash
# Start Piper Morgan
python main.py

# Interact through web UI
# 1. Have a conversation
# 2. Create some tasks
# 3. Upload a document
# 4. Ask questions

# Check database for recorded patterns
psql -U piper -d piper_morgan -c "SELECT * FROM [learning_table] LIMIT 10;"
# Replace [learning_table] with actual table name
```

**Test 2: API vs Web UI**
```bash
# Test via API
curl -X POST http://localhost:8001/api/chat \
  -H "Authorization: Bearer [token]" \
  -d '{"message": "Test learning"}'

# Compare: Are patterns recorded?

# Test via Web UI
# Navigate to http://localhost:8001
# Send same message

# Compare: Different behavior?
```

**Test 3: Configuration Changes**
```bash
# Check current configuration
python main.py status | grep -i learn

# Try toggling learning settings (if they exist)
# Document what changes
```

**Test 4: Pattern Retrieval**
```python
# Create test script: test_learning_retrieval.py
import asyncio
from services.learning import [LearningService]  # Use actual import

async def test_retrieval():
    """Test if learning system retrieves patterns"""
    # Get a pattern
    # Use a pattern
    # Verify it influenced behavior
    pass

# Run test, document results
```

**Questions to Answer from Testing**:
- [ ] Does learning activate automatically?
- [ ] How long until patterns appear?
- [ ] Can patterns be retrieved?
- [ ] Does learning affect behavior?
- [ ] Any errors or issues?

**Document Test Results**:
```markdown
## Runtime Testing Results

### Test 1: Basic Recording
- Status: [Working/Not Working]
- Patterns found: [Count]
- Latency: [Time to record]

### Test 2: API vs Web
- API behavior: [Description]
- Web behavior: [Description]
- Differences: [Any differences]

### Test 3: Configuration
- Default state: [On/Off/Unknown]
- Configuration options: [List]
- How to change: [Steps]

### Test 4: Retrieval
- Can retrieve: [Yes/No]
- Affects behavior: [Yes/No]
- Evidence: [Description]
```

---

### Phase 4: Create Documentation (30 minutes)

**Objective**: Create comprehensive user-facing documentation

**Document 1**: `docs/features/learning-system-guide.md`

```markdown
# Learning System User Guide

**Version**: 0.8.0
**Status**: Alpha
**Last Updated**: November 12, 2025

---

## What is the Learning System?

[High-level description of what the learning system does]

---

## How Learning Works

### Automatic vs Manual

[Is it automatic? Or does user need to enable it?]

### What Gets Learned

[What patterns does it recognize?]
- Conversation patterns
- Task creation patterns
- Document handling patterns
- [etc.]

### When Patterns Are Recorded

[Triggers for learning]
- After every conversation?
- On specific actions?
- Batch processing?

### Expected Latency

[How long until learning appears?]
- Immediate?
- Next conversation?
- Daily processing?

---

## Activating Learning

### For Alpha Testers

[Step-by-step activation if needed]

```bash
# Example commands
python main.py [command to enable learning]
```

### Configuration Options

[Available settings]
- `learning.enabled`: [true/false]
- `learning.threshold`: [number]
- [etc.]

**Location**: [Where to set these]

---

## Verifying Learning is Working

### Step 1: Check Status

```bash
python main.py status | grep -i learn
```

Expected output:
```
Learning System: ✓ Active
Patterns Recorded: 42
Last Updated: 2 minutes ago
```

### Step 2: Database Check

```sql
-- Check learning tables
SELECT COUNT(*) FROM [learning_patterns_table];
-- Expected: > 0

SELECT * FROM [learning_patterns_table] LIMIT 5;
-- Expected: Recent patterns
```

### Step 3: Behavior Check

[How to verify learning affects Piper's behavior]
1. [Do specific action repeatedly]
2. [Observe if Piper adapts]
3. [Check for personalization]

---

## Troubleshooting

### Learning Not Recording Patterns

**Symptoms**: No patterns in database after interactions

**Possible Causes**:
1. Learning disabled in configuration
2. Insufficient interactions (need threshold)
3. Database connection issue
4. [etc.]

**Solutions**:
1. Check `python main.py status`
2. Verify configuration settings
3. Check database connectivity
4. [etc.]

### Patterns Recorded But Not Used

**Symptoms**: Patterns in DB but behavior unchanged

**Possible Causes**:
1. Retrieval not working
2. Threshold not met
3. Pattern confidence too low
4. [etc.]

**Solutions**:
[Steps to fix]

---

## API vs Web UI Differences

[Document any differences in behavior]

**API**: [Behavior description]
**Web UI**: [Behavior description]

---

## For Developers

### Architecture Overview

[Brief technical overview]
- Entry point: [File/class]
- Storage: [Database tables]
- Retrieval: [How patterns are used]

### Key Classes

- `[LearningService]`: [Description]
- `[PatternRecognizer]`: [Description]
- `[PatternStorage]`: [Description]

### Configuration

See: `config/PIPER.user.md` for settings

---

## Known Limitations (Alpha)

[Current limitations]
- [Limitation 1]
- [Limitation 2]
- [etc.]

---

## Feedback Needed

We need alpha testers to report:
- [ ] Is learning recording patterns?
- [ ] How long until you see personalization?
- [ ] Does learning improve your experience?
- [ ] Any unexpected behavior?
- [ ] Feature requests?

---

_Last Updated: November 12, 2025_
_Issue: #288_
```

**Document 2**: `docs/features/learning-system-verification-tests.md`

```markdown
# Learning System Verification Tests

**For**: Alpha testers and developers
**Purpose**: Verify learning system is working correctly

---

## Quick Verification (5 minutes)

### Test 1: Is Learning Active?

```bash
python main.py status | grep -i learn
```

✓ **Expected**: "Learning System: Active" or similar
✗ **Problem**: If shows "Inactive" or not found

### Test 2: Are Patterns Being Recorded?

```bash
# Check database
psql -U piper -d piper_morgan -c \
  "SELECT COUNT(*) FROM [learning_patterns_table];"
```

✓ **Expected**: Count > 0 after interactions
✗ **Problem**: If count = 0 after multiple conversations

---

## Comprehensive Verification (30 minutes)

### Scenario 1: Conversation Pattern Learning

**Steps**:
1. Have 3 conversations about the same topic (e.g., project management)
2. Wait [expected latency]
3. Have 4th conversation about same topic
4. Observe if Piper references previous conversations

**Expected Result**:
- Piper shows awareness of repeated topic
- Responses become more personalized
- [etc.]

**Verification**:
```sql
-- Check for patterns
SELECT * FROM [learning_patterns_table]
WHERE type = 'conversation'
ORDER BY created_at DESC LIMIT 5;
```

### Scenario 2: Task Pattern Learning

**Steps**:
1. Create 5 similar tasks (e.g., "Review PR #123")
2. Wait [expected latency]
3. Create 6th similar task
4. Observe if Piper suggests related info

**Expected Result**:
[Description of expected behavior]

### Scenario 3: Document Handling Pattern

**Steps**:
1. Upload 3 PDF documents
2. Ask for summaries each time
3. Wait [expected latency]
4. Upload 4th PDF
5. Observe if Piper anticipates summary request

**Expected Result**:
[Description of expected behavior]

---

## Debugging Tests

[Tests for when things go wrong]

---

_Created: November 12, 2025_
_Issue: #288_
```

---

## Deliverables

### 1. Investigation Report

**File**: `dev/investigations/learning-system-investigation-288.md`

**Contents**:
- Code architecture findings
- Configuration options discovered
- Runtime behavior observed
- API vs Web UI differences
- Current gaps identified
- Recommendations

### 2. User Guide

**File**: `docs/features/learning-system-guide.md`

**Contents**:
- What learning system does
- How to activate it
- How to verify it's working
- Troubleshooting steps
- Known limitations

### 3. Verification Tests

**File**: `docs/features/learning-system-verification-tests.md`

**Contents**:
- Quick verification steps
- Comprehensive test scenarios
- Expected results
- Debugging procedures

### 4. Session Log

**File**: `dev/2025/11/12/2025-11-12-[time]-cursor-log.md`

**Contents**:
- Investigation process
- Findings from each phase
- Test results
- Time spent on each phase
- Issues encountered

---

## Acceptance Criteria

### Investigation Complete
- [x] Code architecture documented
- [x] Configuration options identified
- [x] Runtime behavior tested
- [x] API vs Web differences documented
- [x] Documentation gaps identified

### Documentation Complete
- [x] User guide created
- [x] Verification tests documented
- [x] Troubleshooting steps included
- [x] Developer notes included

### Quality Checks
- [x] Activation mechanism clear
- [x] Expected behavior documented
- [x] Verification steps testable
- [x] All questions answered
- [x] Alpha testers can follow guide

---

## Success Criteria

**Investigation Successful If**:
- Alpha testers can determine if learning is working
- Clear steps to activate learning (if needed)
- Verification tests are actionable
- Documentation closes knowledge gaps

**Red Flags**:
- Can't determine if learning is active
- No way to verify patterns are recording
- Configuration options unclear
- Behavior unpredictable

---

## Timeline

**Phase 1** (Code Review): 1 hour
**Phase 2** (Documentation Review): 30 minutes
**Phase 3** (Runtime Testing): 1 hour
**Phase 4** (Create Documentation): 30 minutes

**Total**: 3 hours

---

## Communication

**Progress Updates**:
- After Phase 1: "Code review complete, [key findings]"
- After Phase 2: "Documentation reviewed, [gaps identified]"
- After Phase 3: "Runtime testing done, [behavior observed]"
- After Phase 4: "Documentation created, ready for review"

**Final Report**:
```markdown
## Investigation #288 Complete ✅

**Duration**: [X] hours

**Key Findings**:
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

**Documentation Created**:
- ✅ User guide: docs/features/learning-system-guide.md
- ✅ Verification tests: docs/features/learning-system-verification-tests.md
- ✅ Investigation report: dev/investigations/learning-system-investigation-288.md

**Recommendations**:
[Any recommendations for PM or alpha testers]

**Session Log**: [link]
```

---

## Resources

**Issue**: #288 - CORE-ALPHA-LEARNING-INVESTIGATION
**Priority**: P3
**Template**: agent-prompt-template.md v10.2

---

## Critical Reminders

1. **Be thorough**: This investigation informs alpha testing
2. **Document everything**: Alpha testers need clear guidance
3. **Test comprehensively**: Verify behavior, don't assume
4. **Write for users**: Documentation should be accessible
5. **Note unknowns**: If something's unclear, document that too

---

**Execute**: Investigate learning system, document how it works, create user guides! 🔍📚
