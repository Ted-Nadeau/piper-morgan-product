# Code Agent Prompt: VALID-2 - MVP Integration Testing

**Date**: October 14, 2025, 3:50 PM
**Phase**: VALID-2 (Integration Testing)
**Agent**: Code Agent
**Philosophy**: Inchworm - just keep doing what's next until it's done

---

## Mission

Test MVP workflows to understand what's implemented and what gaps exist. This is **discovery**, not validation - we're curious about what actually works end-to-end!

**Context**: VALID-1 confirmed all components exist (99%+ verified). Now let's see what happens when we actually run workflows.

**Mindset**: "Let's see what we've got!" Not "Does it meet requirements?" - just genuine curiosity about current state.

---

## Approach: Discovery Through Testing

We'll test workflows in natural order, documenting what works and what doesn't. No rush, no deadlines - just systematic exploration.

### What Success Looks Like
- Clear understanding of what's working
- Clear documentation of what's not yet implemented
- No judgment, just facts
- Honest assessment for MVP planning

---

## Category 1: Chitchat Workflows

### Test 1: Greeting
**What we're testing**: Does Piper respond to greetings?

```python
# Test basic greeting
async def test_greeting():
    response = await process_query("Hello Piper!")
    # What actually happens?
    # - Does it classify as GREETING?
    # - Does it respond warmly?
    # - Is there a handler for this?
```

**Document**:
- Intent classification result
- Actual response
- Handler path taken (canonical vs custom)
- Any errors or issues

### Test 2: Help/Menu
**What we're testing**: Can users ask what Piper can do?

```python
# Test help request
async def test_help():
    response = await process_query("What can you help me with?")
    # What actually happens?
    # - Does it classify as GUIDANCE?
    # - Is there a menu/capabilities list?
    # - Or just a generic response?
```

**Document**:
- Classification result
- Response content
- Whether menu exists or needs creation
- MVP readiness assessment

---

## Category 2: Knowledge Workflows

### Test 3: File Operations
**What we're testing**: Can Piper work with files?

Try these queries:
- "Summarize this file: [content]"
- "Analyze this document"
- "Extract key points from..."

```python
# Test file summarization
async def test_file_summarization():
    test_content = "Long document content here..."
    response = await process_query(f"Summarize: {test_content}")
    # What actually happens?
    # - Does it classify as SYNTHESIS?
    # - Does summarization actually work?
    # - Or is it just echoing back?
```

**Document**:
- Whether file operations work
- Quality of summarization (if any)
- What's implemented vs placeholder
- Gap list for MVP

---

## Category 3: Integration Workflows

### Test 4: GitHub Integration
**What we're testing**: Can Piper interact with GitHub?

**Priority tests** (GitHub most likely to work):
```python
# Test 1: Create issue
async def test_github_create_issue():
    response = await process_query("Create GitHub issue: Test bug")
    # What happens?
    # - Does it route to EXECUTION?
    # - Does it actually call GitHub API?
    # - Or just acknowledge the request?

# Test 2: List issues
async def test_github_list_issues():
    response = await process_query("Show my GitHub issues")
    # What happens?
    # - Does it route to ANALYSIS?
    # - Does it fetch real data?
    # - Or return placeholder?

# Test 3: Search code
async def test_github_search():
    response = await process_query("Search GitHub for QueryRouter")
    # What happens?
```

**Document**:
- What GitHub operations work
- What needs API credentials
- What's not yet implemented
- MVP gaps

### Test 5: Slack Integration
**What we're testing**: Can Piper work with Slack?

```python
async def test_slack_operations():
    # Test message sending
    response1 = await process_query("Send Slack message to #general")

    # Test channel listing
    response2 = await process_query("List my Slack channels")

    # What actually works?
```

**Document**:
- Slack operation status
- Spatial intelligence integration
- MVP readiness

### Test 6: Other Integrations
**Quick checks for**:
- Notion: Can it create/read pages?
- Calendar: Can it show/create events?

**Document whatever we find** - no expectations!

---

## Category 4: Performance Validation

### Test 7: Performance Baselines
**What we're testing**: Do the documented baselines hold under real usage?

```python
# Quick performance spot checks
async def test_performance():
    # Classification speed
    start = time()
    for i in range(100):
        await classify("What time is it?")
    elapsed = time() - start
    avg_ms = (elapsed / 100) * 1000
    # Is it <1.2ms as documented?

    # Throughput (if easy to test)
    # Cache hit rate (if observable)
```

**Document**:
- Whether baselines hold
- Any performance issues noticed
- Areas needing optimization

---

## Category 5: System-Level Workflows

### Test 8: End-to-End Pipeline
**What we're testing**: Does the full pipeline work?

**Test diverse intents**:
```python
test_cases = [
    "What time is it?",           # TEMPORAL
    "Create GitHub issue: Bug",   # EXECUTION
    "Summarize last week",        # SYNTHESIS
    "Show my calendar",           # ANALYSIS
    "Hello!",                     # GREETING
    "Help me with X",             # GUIDANCE
]

for query in test_cases:
    result = await process_query(query)
    # Document:
    # - Classification result
    # - Handler invoked
    # - Actual response
    # - Whether it worked as expected
```

**Document**:
- Pipeline flow
- Where things break (if anywhere)
- What works smoothly
- Surprise findings

---

## How to Test (Practical Guide)

### Option 1: Use Existing Tests
If integration tests exist:
```bash
# Find integration tests
find tests/ -name "*integration*" -o -name "*e2e*"

# Run them
pytest tests/integration/ -v

# Document results
```

### Option 2: Interactive Testing
Start Piper and try things:
```bash
# Start the server
python main.py

# In another terminal, send requests
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello Piper!"}'

# Or use the CLI if available
python -m piper.cli "What can you help me with?"
```

### Option 3: Write Quick Test Scripts
Create simple test scripts:
```python
# test_mvp_workflows.py
import asyncio
from services.orchestration.engine import OrchestrationEngine

async def test_workflow(query):
    engine = OrchestrationEngine()
    result = await engine.handle_query_intent(query)
    print(f"Query: {query}")
    print(f"Intent: {result.intent}")
    print(f"Response: {result.message}")
    print("---")

async def main():
    queries = [
        "Hello!",
        "What can you do?",
        "Create GitHub issue: Test",
        "What time is it?",
    ]
    for q in queries:
        await test_workflow(q)

asyncio.run(main())
```

---

## Documentation Format

For each workflow tested, document:

```markdown
### Workflow: [Name]

**Query Tested**: "[actual query]"

**Classification Result**:
- Intent: [GREETING/EXECUTION/etc]
- Confidence: [if available]
- Handler: [canonical/custom]

**Actual Behavior**:
- [What actually happened]
- [Was it successful?]
- [Any errors?]

**Assessment**:
- ✅ Working - [description]
- ⚠️ Partial - [what works, what doesn't]
- ❌ Not implemented - [gap for MVP]

**Notes**: [Any observations or surprises]
```

---

## Output: MVP Readiness Report

Create: `dev/2025/10/14/valid-2-mvp-integration-report.md`

**Structure**:
```markdown
# VALID-2: MVP Integration Testing Report

## Executive Summary
[What works, what doesn't, overall readiness]

## Workflows Tested
[List of all workflows tested]

## Working Features ✅
[Everything that works end-to-end]

## Partially Implemented ⚠️
[Features that exist but need work]

## Not Yet Implemented ❌
[Clear gaps for MVP planning]

## Performance Validation
[Whether baselines hold]

## Surprise Findings
[Anything unexpected - good or bad!]

## MVP Recommendations
[Priority work for MVP readiness]

## Next Steps
[What to tackle first]
```

---

## What NOT to Worry About

- ❌ Don't fix anything (this is discovery, not development)
- ❌ Don't judge quality (just document what is)
- ❌ Don't worry about time (inchworm pace)
- ❌ Don't force things to work (document gaps honestly)
- ❌ Don't create mock data (test what's real)

## What TO Do

- ✅ Test honestly (try to actually use it)
- ✅ Document thoroughly (what works, what doesn't)
- ✅ Note surprises (good and bad)
- ✅ Be curious (discover what we've built)
- ✅ Think MVP (what's needed for real use)

---

## The Inchworm Approach

We'll test workflows one by one:
1. **Try a workflow** - See what happens
2. **Document findings** - Write it down
3. **Move to next** - Keep going
4. **No rush** - Take the time needed
5. **Stay curious** - Discover what we've got!

When we're done, we'll have a clear picture of:
- What's working ✅
- What needs work ⚠️
- What's missing ❌
- What to build for MVP 🎯

---

## Context: Why This Matters

**From VALID-1**: We know all the pieces exist (99%+ verified components)

**VALID-2 Question**: Do the pieces work together? What's the actual user experience?

**Goal**: Honest assessment of MVP readiness - not proving success, just discovering reality

**Philosophy**: "Verification without judgment, discovery without deadline"

---

**Start Time**: Whenever you're ready
**End Time**: When we're done discovering
**Method**: Systematic workflow testing with curious documentation

**LET'S DISCOVER WHAT WE'VE BUILT!** 🔍✨

---

*"The inchworm doesn't rush. It just keeps moving until it arrives."*
*- VALID-2 Philosophy*
