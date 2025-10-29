# Phase 2 Web UI Testing - Automated with Chrome MCP

**Agent**: Claude Code (Haiku 4.5)
**Tool**: Chrome DevTools MCP (v0.9.0) - WORKING ✅
**Task**: Execute complete web UI testing scenarios for Piper Morgan
**Priority**: HIGH - Answer the question "What does Piper actually do?"
**Time**: Sunday, October 26, 2025, 6:30 PM PT
**Duration**: 1-2 hours estimated

---

## MISSION

Execute comprehensive automated web UI testing of Piper Morgan using Chrome MCP to:
1. **Discover** what Piper actually says and does (not assumptions!)
2. **Verify** learning system behavior end-to-end (the morning meeting tests!)
3. **Document** complete evidence (screenshots, responses, observations)
4. **Compare** reality to predictions from archaeological investigation
5. **Answer** the fascinating question: How does the unified system behave?

**Key Principle**: "Discovery testing with automation - document everything Piper does!"

---

## CRITICAL CONTEXT

### What We Know From This Morning

**Archaeological Investigation** (Code, 8:46 AM - 9:46 AM):
- ✅ All 3 learning components wired
- ✅ 52/52 learning tests passing
- ✅ Graph reasoning → Intent classification
- ✅ Preference persistence → Database
- ✅ Pattern learning → Orchestration

**Integration Testing** (Code, 10:43 AM - 11:46 AM):
- ✅ 91/93 tests passing (98%)
- ✅ All infrastructure operational
- ✅ System ready for alpha

**Chrome MCP Setup** (Cursor, 11:43 AM - 12:15 PM):
- ✅ Working with localhost:8001
- ✅ All capabilities confirmed
- ✅ Ready for automated testing

**The Big Question**: How does Piper's learning system actually behave in conversation?

---

## CHROME MCP SETUP VERIFICATION

### Step 0: Confirm Chrome MCP Ready [2 MIN]

**Test Chrome MCP**:
```
Navigate to https://google.com and take a screenshot
```

**Expected**: Screenshot shows Google homepage

**If this works**: ✅ Proceed with testing
**If this fails**: ❌ Stop and troubleshoot Chrome MCP first

---

## ESSENTIAL MATERIALS

### Required Documents
1. **chrome-mcp-setup-guide-WORKING.md** - Setup instructions from Cursor
2. **phase-2-testing-execution-prompt.md** - Test scenarios we created
3. **sprint-a8-phase-2-gameplan-e2e-testing-REVISED.md** - Complete gameplan
4. **PHASE-2-EXECUTIVE-SUMMARY.md** - System status from integration tests

### System Requirements
- **Piper Morgan**: Must be running at localhost:8001
- **Database**: PostgreSQL on localhost:5433
- **Chrome MCP**: Configured and working (verified above)

---

## TESTING APPROACH

### Evidence Collection Strategy

**For EVERY interaction**:
1. ✅ Screenshot BEFORE action (current state)
2. ✅ Perform action (send message, click button, etc.)
3. ✅ Screenshot AFTER action (result)
4. ✅ Save Piper's exact response text
5. ✅ Note timing (how long did response take?)
6. ✅ Check console for errors
7. ✅ Verify database changes (if applicable)

**Save Location**:
```
~/Desktop/piper-phase2-evidence-AUTOMATED/
├── journey-1-onboarding/
├── journey-2-learning-CRITICAL/
├── journey-3-integrations/
├── journey-4-edge-cases/
└── summary-report.md
```

---

## PHASE -1: SYSTEM STARTUP [5 MIN]

### Goal: Confirm Piper Morgan is running and accessible

**Step 1: Check if Piper is Running**
```
Navigate to localhost:8001
```

**Expected**: Piper Morgan interface loads

**Actions**:
- [ ] Take screenshot of landing page
- [ ] Check console for any errors
- [ ] Verify page title/branding
- [ ] Save initial state

**If page doesn't load**:
```bash
# In terminal, start Piper Morgan
cd /Users/xian/Development/piper-morgan
python main.py

# Wait 10 seconds for startup
# Then retry navigation
```

**Evidence Required**:
- Screenshot: `00-system-startup.png`
- Console log: Note any errors
- Timestamp: When system became ready

---

## JOURNEY 1: ALPHA ONBOARDING [30 MIN]

### Goal: Test complete onboarding flow via web UI

**Priority**: P1 - Important user journey
**Status from Code**: Infrastructure ready, CLI tested, web UI not tested yet

---

### Step 1.1: First Interaction Test

**Scenario**: New user sends first message

**Navigate to**: localhost:8001

**Action**: Find chat input field and send message
```
Message: "Hello, what can you help me with?"
```

**Chrome MCP Commands**:
1. Take screenshot (before)
2. Click chat input field
3. Type message
4. Take screenshot (message entered)
5. Click send button (or press Enter)
6. Wait for response (watch for response to appear)
7. Take screenshot (after response)
8. Read response text from page

**Evidence to Collect**:
- [ ] Screenshot: `01-first-message-before.png`
- [ ] Screenshot: `01-first-message-sent.png`
- [ ] Screenshot: `01-first-message-response.png`
- [ ] Response text: Save exact wording
- [ ] Response time: Note how long it took
- [ ] Console: Any errors during processing?

**Questions to Answer**:
- Does Piper respond?
- Is response coherent?
- How long did it take?
- Any errors in console?
- Does UI handle response correctly?

---

### Step 1.2: Follow-up Interaction

**Scenario**: User asks follow-up question

**Message**:
```
"Tell me about your capabilities"
```

**Chrome MCP Actions**:
1. Clear previous input (if needed)
2. Enter new message
3. Take screenshot (before send)
4. Send message
5. Wait for response
6. Take screenshot (after response)
7. Read response text

**Evidence to Collect**:
- [ ] Screenshot: `02-capabilities-question.png`
- [ ] Screenshot: `02-capabilities-response.png`
- [ ] Response text: Does Piper describe its features?
- [ ] Accuracy: Does description match actual capabilities?

**Questions to Answer**:
- Does Piper know its own features?
- Does it mention learning system?
- Does it mention integrations?
- Is response accurate based on archaeological findings?

---

## JOURNEY 2: LEARNING SYSTEM [45 MIN] 🔥 CRITICAL!

### Goal: THE BIG QUESTION - How does learning actually work?

**Priority**: P0 - This is the fascinating test!
**Status from Code**: All 3 components wired (52/52 tests)
**Question**: What does Piper actually say/do?

---

### Test Setup: Fresh Session

**Before starting learning tests**:
1. Refresh page (clear conversation history)
2. Or open new incognito window
3. Ensure clean slate for learning tests

---

### Scenario A: Original Test (Context Gap Suspected) 🔍

**Purpose**: See what happens with potentially incomplete context

**Message 1**:
```
"I prefer morning meetings because I have more energy"
```

**Chrome MCP Actions**:
1. Navigate to localhost:8001 (fresh session)
2. Take screenshot (initial state)
3. Enter Message 1
4. Take screenshot (message entered)
5. Send message
6. Wait for response
7. Take screenshot (response received)
8. **READ EXACT RESPONSE TEXT** - Critical!
9. Check console for any learning system activity

**Wait 30 seconds** (allow processing/learning to occur)

**Message 2**:
```
"When should we schedule the architecture review?"
```

**Chrome MCP Actions**:
1. Take screenshot (before Message 2)
2. Enter Message 2
3. Take screenshot (message entered)
4. Send message
5. Wait for response
6. Take screenshot (response received)
7. **READ EXACT RESPONSE TEXT** - Critical!
8. Check console for learning hints

**Evidence to Collect**:
- [ ] Screenshot: `03a-scenario-a-message1-before.png`
- [ ] Screenshot: `03a-scenario-a-message1-sent.png`
- [ ] Screenshot: `03a-scenario-a-message1-response.png`
- [ ] **Response 1 text**: Exact wording - CRITICAL
- [ ] Screenshot: `03a-scenario-a-message2-before.png`
- [ ] Screenshot: `03a-scenario-a-message2-sent.png`
- [ ] Screenshot: `03a-scenario-a-message2-response.png`
- [ ] **Response 2 text**: Exact wording - CRITICAL
- [ ] Console logs: Any learning activity?
- [ ] Timing: How long between messages?

**Critical Questions to Answer**:
1. **Response 1**: How did Piper respond to the morning preference?
   - Did it acknowledge the preference?
   - Did it confirm understanding?
   - What exact words did it use?

2. **Response 2**: How did Piper respond to the scheduling question?
   - Did it suggest morning? ✅
   - Did it ask for context ("What architecture review?")? 🤔
   - Did it reference the earlier preference explicitly? 🔗
   - Did it ignore the preference completely? ❌
   - Something else entirely? 🎲

3. **Learning Evidence**:
   - Any console logs about pattern learning?
   - Any database activity visible?
   - Response time changes?

**Database Verification** (Optional but valuable):
```sql
-- Check if preference was stored
SELECT username, preferences FROM alpha_users ORDER BY created_at DESC LIMIT 1;

-- Check for graph nodes
SELECT * FROM knowledge_nodes WHERE content ILIKE '%morning%' ORDER BY created_at DESC LIMIT 5;
```

---

### Scenario B: Generic Test (More Realistic) 🔍

**Purpose**: Test with more natural conversational flow

**NEW FRESH SESSION** (refresh page or new window)

**Message 1**:
```
"I prefer morning meetings because I have more energy"
```

**Chrome MCP Actions**:
1. Fresh session at localhost:8001
2. Take screenshot (initial)
3. Enter and send Message 1
4. Capture response
5. **READ EXACT RESPONSE**
6. Wait 30 seconds

**Message 2**:
```
"When should we have our next team meeting?"
```

**Chrome MCP Actions**:
1. Enter and send Message 2
2. Capture response
3. **READ EXACT RESPONSE**
4. Check console

**Evidence to Collect**:
- [ ] Screenshot: `03b-scenario-b-message1-response.png`
- [ ] Screenshot: `03b-scenario-b-message2-response.png`
- [ ] **Response 1 text**: Exact wording
- [ ] **Response 2 text**: Exact wording
- [ ] Comparison: Is this better than Scenario A?

**Critical Questions**:
1. Does "next team meeting" (generic) work better than "architecture review" (specific)?
2. Does Piper suggest morning?
3. Does it explicitly reference the preference?
4. How does it phrase the recommendation?
5. More coherent than Scenario A?

---

### Scenario C: Full Context Test (Ideal) 🔍

**Purpose**: Test with complete context established

**NEW FRESH SESSION** again

**Message 1**:
```
"We need to schedule an architecture review meeting"
```

**Chrome MCP Actions**:
1. Fresh session
2. Enter and send Message 1
3. Capture response
4. **READ RESPONSE**
5. Wait 10 seconds

**Message 2**:
```
"I prefer morning meetings because I have more energy"
```

**Chrome MCP Actions**:
1. Enter and send Message 2
2. Capture response
3. **READ RESPONSE**
4. Wait 30 seconds

**Message 3**:
```
"When should we schedule the architecture review?"
```

**Chrome MCP Actions**:
1. Enter and send Message 3
2. Capture response
3. **READ RESPONSE**
4. Compare to Scenarios A & B

**Evidence to Collect**:
- [ ] Screenshot: All three message exchanges
- [ ] **Response 1 text**: Acknowledges meeting need?
- [ ] **Response 2 text**: Acknowledges preference?
- [ ] **Response 3 text**: Combines both pieces?
- [ ] Analysis: Best scenario?

**Critical Questions**:
1. Does establishing context first improve response?
2. Does Piper connect all three messages?
3. Does it suggest morning for the architecture review specifically?
4. Does it reference both the meeting type AND preference?
5. Which scenario (A/B/C) produces best behavior?

---

### Scenario Analysis: Which Works Best? [10 MIN]

**After running all three scenarios, analyze**:

**Create comparison table**:
```markdown
| Scenario | Context Setup | Response Quality | Referenced Preference? | Suggested Morning? | Best For |
|----------|---------------|------------------|----------------------|-------------------|----------|
| A | None (gap) | [rate 1-5] | [yes/no/partial] | [yes/no/partial] | [use case] |
| B | Generic | [rate 1-5] | [yes/no/partial] | [yes/no/partial] | [use case] |
| C | Full | [rate 1-5] | [yes/no/partial] | [yes/no/partial] | [use case] |
```

**Key Insights**:
1. Which scenario showed best learning behavior?
2. Does context matter for Piper's responses?
3. Is learning system actually applying preferences?
4. What's the "ideal" conversation pattern?
5. Does reality match Code's predictions?

---

### Database Deep Dive (After All Scenarios) [5 MIN]

**Check what was stored**:

```sql
-- Latest user preferences
SELECT id, username, preferences, created_at
FROM alpha_users
ORDER BY created_at DESC
LIMIT 5;

-- Knowledge graph nodes about morning
SELECT id, content, node_type, created_at
FROM knowledge_nodes
WHERE content ILIKE '%morning%'
ORDER BY created_at DESC
LIMIT 10;

-- Knowledge graph edges
SELECT e.id, n1.content as source, e.edge_type, n2.content as target, e.confidence
FROM knowledge_edges e
JOIN knowledge_nodes n1 ON e.source_id = n1.id
JOIN knowledge_nodes n2 ON e.target_id = n2.id
WHERE n1.content ILIKE '%morning%' OR n2.content ILIKE '%morning%'
ORDER BY e.created_at DESC
LIMIT 10;

-- Pattern learning (if accessible via database)
-- May need to check filesystem: data/learning/learned_patterns.json
```

**Evidence**:
- [ ] Screenshot/copy of query results
- [ ] Note what was actually stored
- [ ] Compare to what was expected
- [ ] Any surprises?

---

## JOURNEY 3: INTEGRATION TESTS [30 MIN]

### Goal: Test external integrations via web UI

**Priority**: P2 - Nice to have working
**Status from Code**: All 4 integrations implemented
**Requirement**: Environment variables must be set

**Before starting**: Check if integration env vars are set
```bash
echo $GITHUB_TOKEN
echo $SLACK_BOT_TOKEN
echo $GOOGLE_APPLICATION_CREDENTIALS
echo $NOTION_API_KEY
```

**If any missing**: Skip that integration test and note in report

---

### Step 3.1: GitHub Integration Test

**Message**:
```
"Show me my recent GitHub issues"
```

**Chrome MCP Actions**:
1. Send message
2. Wait for response (may take longer - external API)
3. Capture response
4. **READ RESPONSE**
5. Check console for GitHub API calls

**Evidence to Collect**:
- [ ] Screenshot: `04-github-query.png`
- [ ] Screenshot: `04-github-response.png`
- [ ] Response: Does it show actual issues?
- [ ] Console: GitHub integration activated?
- [ ] Timing: How long did it take?

**Questions**:
- Did GitHub integration activate?
- Were issues retrieved?
- Was response formatted well?
- Any errors?

---

### Step 3.2: Multi-Tool Orchestration Test

**Message**:
```
"Check my GitHub issues and my calendar for tomorrow, then suggest when I can work on the highest priority issue"
```

**Chrome MCP Actions**:
1. Send message
2. Wait (this may take 15-30 seconds - two API calls)
3. Capture response
4. **READ RESPONSE**
5. Check console for both integrations

**Evidence to Collect**:
- [ ] Screenshot: `05-multi-tool-query.png`
- [ ] Screenshot: `05-multi-tool-response.png`
- [ ] Response: Did it use both integrations?
- [ ] Response: Was suggestion coherent?
- [ ] Console: Both integrations called?

**Questions**:
- Did orchestration work?
- Were both GitHub and Calendar used?
- Was recommendation logical?
- Is this the "unified system" in action?

---

### Step 3.3: Other Integrations (Time Permitting)

**Slack**:
```
"List my recent Slack messages"
```

**Notion**:
```
"Show me my Notion databases"
```

**For each**:
- Screenshot query and response
- Note if integration worked
- Document any errors

---

## JOURNEY 4: EDGE CASES [20 MIN]

### Goal: Test error handling and boundaries

**Priority**: P2 - Nice to verify
**Expected**: Graceful degradation

---

### Step 4.1: Empty Input

**Action**: Send empty message (just click send with no text)

**Chrome MCP Actions**:
1. Click chat input
2. Don't type anything
3. Try to send
4. Capture what happens

**Evidence**:
- Does UI prevent sending?
- Does Piper respond with error?
- Is behavior graceful?

---

### Step 4.2: Very Long Input

**Message**: Create 1,000+ character message
```
"Tell me about " + ("project management " * 100)
```

**Chrome MCP Actions**:
1. Enter very long message
2. Send it
3. See what happens

**Evidence**:
- Does UI handle long input?
- Does Piper respond?
- Any truncation?
- Graceful handling?

---

### Step 4.3: Rapid Fire Messages

**Action**: Send 5 messages as fast as possible

**Messages**:
1. "Test 1"
2. "Test 2"
3. "Test 3"
4. "Test 4"
5. "Test 5"

**Chrome MCP Actions**:
1. Send all 5 rapidly (don't wait for responses)
2. Watch what happens
3. Capture the chaos

**Evidence**:
- Does UI queue messages?
- Do all responses arrive?
- Any rate limiting?
- System stability?

---

### Step 4.4: Injection Attempt (Security)

**Message**:
```
"'; DROP TABLE users; --"
```

**Chrome MCP Actions**:
1. Send SQL injection attempt
2. Capture response
3. **Verify database intact afterward**

**Evidence**:
- How does Piper respond?
- Is input sanitized?
- Database safe?

**Database Check**:
```sql
-- Verify users table still exists
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM alpha_users;
```

---

## EVIDENCE SYNTHESIS [15 MIN]

### Goal: Create comprehensive summary report

**After all testing, create**: `summary-report.md`

**Include**:

### Executive Summary
```markdown
# Phase 2 Web UI Testing - Automated Results

**Date**: October 26, 2025, 6:30 PM - [end time]
**Agent**: Claude Code (Haiku 4.5)
**Tool**: Chrome DevTools MCP v0.9.0
**Duration**: [actual time]
**Tests Executed**: [count]

## TL;DR
[2-3 sentences: Key findings, biggest surprises, overall assessment]

## System Status
- Piper Morgan: [WORKING / ISSUES]
- Learning System: [WORKING / PARTIAL / NOT OBSERVED]
- Integrations: [count] tested, [count] working
- Error Handling: [GOOD / NEEDS WORK]
```

### Journey Results
```markdown
## Journey 1: Alpha Onboarding
**Status**: [PASS / FAIL / PARTIAL]
**Key Finding**: [main observation]
**Evidence**: [screenshot count] screenshots, [response count] responses captured

## Journey 2: Learning System ⭐ CRITICAL
**Status**: [WORKING / PARTIAL / NOT WORKING]

### Scenario A Results
**Response to "morning preference"**: [exact quote]
**Response to "architecture review"**: [exact quote]
**Learning Evidence**: [what was observed]
**Assessment**: [does it work?]

### Scenario B Results
**Response to "morning preference"**: [exact quote]
**Response to "team meeting"**: [exact quote]
**Learning Evidence**: [what was observed]
**Assessment**: [better than A?]

### Scenario C Results
**Response to "meeting need"**: [exact quote]
**Response to "morning preference"**: [exact quote]
**Response to "schedule review"**: [exact quote]
**Learning Evidence**: [what was observed]
**Assessment**: [best scenario?]

### Learning System Verdict
**Does it work?**: [YES / PARTIAL / NO]
**Evidence**: [what proves this]
**Best scenario**: [A / B / C]
**Recommendation**: [how to use it]

## Journey 3: Integrations
**Tested**: [count]
**Working**: [count]
**Issues**: [list any]

## Journey 4: Edge Cases
**Error handling**: [GOOD / NEEDS WORK]
**Security**: [SAFE / CONCERNS]
**Stability**: [STABLE / ISSUES]
```

### Comparison: Prediction vs Reality
```markdown
## Archaeological Predictions vs Web UI Reality

| Prediction | Reality | Match? |
|------------|---------|--------|
| Learning system fully wired | [actual behavior] | ✅/⚠️/❌ |
| Graph → Intent classification | [observed or not] | ✅/⚠️/❌ |
| Preference persistence | [observed or not] | ✅/⚠️/❌ |
| Integrations working | [count working] | ✅/⚠️/❌ |

**Biggest Surprise**: [what you didn't expect]
**Confirmed Prediction**: [what matched exactly]
**Needs Investigation**: [any concerning findings]
```

### Evidence Summary
```markdown
## Evidence Collected

**Screenshots**: [count] total
- Journey 1: [count]
- Journey 2: [count] ⭐
- Journey 3: [count]
- Journey 4: [count]

**Response Texts**: [count] captured
**Database Queries**: [count] executed
**Console Logs**: [any errors found?]

**Evidence Location**: ~/Desktop/piper-phase2-evidence-AUTOMATED/
```

### Key Findings
```markdown
## Top 5 Findings

1. **[Most Important Finding]**
   - Evidence: [screenshot/response reference]
   - Impact: [significance]

2. **[Second Finding]**
   - Evidence: [reference]
   - Impact: [significance]

3. **[Third Finding]**
   - Evidence: [reference]
   - Impact: [significance]

4. **[Fourth Finding]**
   - Evidence: [reference]
   - Impact: [significance]

5. **[Fifth Finding]**
   - Evidence: [reference]
   - Impact: [significance]
```

### Recommendations
```markdown
## Next Steps

**Ready for Alpha**: YES / NO / WITH MODIFICATIONS

**Blockers Found** (if any):
- [list P0/P1 issues]

**Enhancements Suggested** (not blocking):
- [list improvements]

**Manual Testing Needed** (if any):
- [what still needs human verification]

**Documentation Updates Required**:
- [what docs need updating based on findings]
```

---

## SPECIAL FOCUS: THE LEARNING SYSTEM

### Why This Is The Most Important Test

**The Big Question We're Answering**:
> "Does Piper's learning system actually work end-to-end in real conversation?"

**What We Know**:
- ✅ 52/52 tests pass (pytest verification)
- ✅ All 3 components wired (code inspection)
- ✅ Graph, preferences, patterns all exist

**What We Don't Know Yet**:
- 🤔 How does it behave in actual conversation?
- 🤔 What does Piper actually say?
- 🤔 Does it remember preferences?
- 🤔 Does it apply learning?
- 🤔 Which scenario works best?

**This test answers all of these questions with real evidence!**

---

## CRITICAL REMINDERS

### Discovery Philosophy

**Remember**:
1. **Document what actually happens** (not what should happen)
2. **Capture Piper's exact words** (don't paraphrase)
3. **No judgment, just observation** (surprises are data)
4. **Compare to predictions** (but don't force fit)
5. **Evidence over assumptions** (screenshots prove everything)

### Chrome MCP Best Practices

**For each interaction**:
1. ✅ Take screenshot BEFORE action
2. ✅ Perform action
3. ✅ Wait for complete response (don't rush)
4. ✅ Take screenshot AFTER action
5. ✅ Read and save exact text
6. ✅ Check console for errors/logs
7. ✅ Name files descriptively

**If Chrome MCP acts weird**:
- Take screenshot of the weirdness
- Note what you tried
- Document and continue
- Don't waste time debugging MCP

---

## SUCCESS CRITERIA

### Minimum Success
- [ ] Piper responds to basic messages
- [ ] At least 1 learning scenario tested completely
- [ ] Evidence collected (screenshots + text)
- [ ] Summary report created
- [ ] Key questions answered (even if answer is "needs work")

### Ideal Success
- [ ] All 4 journeys tested
- [ ] All 3 learning scenarios (A/B/C) completed
- [ ] Complete evidence folder
- [ ] Comprehensive summary report
- [ ] Database verification completed
- [ ] Clear "does learning work?" answer
- [ ] Integrations tested
- [ ] Edge cases documented

### Acceptable Partial Success
- [ ] Learning system tests completed (most important)
- [ ] Basic onboarding verified
- [ ] Summary of findings
- [ ] Recommendation for manual follow-up (if needed)

---

## DELIVERABLES

### Required Files
1. ✅ `summary-report.md` - Executive summary with key findings
2. ✅ Evidence folder - All screenshots organized by journey
3. ✅ Response transcripts - Exact text of Piper's responses
4. ✅ Database queries - Results from verification queries
5. ✅ Session log - Timeline of testing activities

### Optional But Valuable
- Video recording of key interactions (if possible with Chrome MCP)
- Console logs saved to files
- Performance metrics (response times)
- Comparison charts (Scenario A vs B vs C)

---

## TIME MANAGEMENT

### Estimated Timeline
- **Phase -1** (Startup): 5 minutes
- **Journey 1** (Onboarding): 30 minutes
- **Journey 2** (Learning) ⭐: 45 minutes
- **Journey 3** (Integrations): 30 minutes
- **Journey 4** (Edge Cases): 20 minutes
- **Evidence Synthesis**: 15 minutes
- **Total**: ~2 hours 25 minutes

### Priority If Time Limited
1. **Journey 2 (Learning)** - MUST DO ⭐⭐⭐
2. **Journey 1 (Onboarding)** - SHOULD DO
3. **Evidence Synthesis** - MUST DO
4. **Journey 3 (Integrations)** - NICE TO HAVE
5. **Journey 4 (Edge Cases)** - NICE TO HAVE

### Stop Conditions
- If stuck on any test > 15 minutes: Document and move on
- If Chrome MCP breaks repeatedly: Switch to manual testing recommendation
- If Piper doesn't respond at all: Investigate system status, document blocker
- If time reaches 2.5 hours: Synthesize findings, recommend manual completion

---

## FINAL CHECKLIST

Before starting:
- [ ] Chrome MCP verified working (google.com test)
- [ ] Piper Morgan running at localhost:8001
- [ ] Database accessible
- [ ] Evidence folder created
- [ ] Ready to capture everything

Before finishing:
- [ ] All critical tests executed (Journey 2 minimum)
- [ ] Summary report created
- [ ] Evidence organized and saved
- [ ] Key questions answered
- [ ] Recommendation made (ready for alpha? needs work?)
- [ ] Files uploaded for PM review

---

## THE FASCINATING QUESTION

**What we're about to discover**:

> After 2 months of development, multiple sprints, 91/93 tests passing, and comprehensive architectural work... **what does Piper Morgan actually say and do when you talk to it?**

**The learning system test specifically**:

> When you tell Piper "I prefer morning meetings because I have more energy" and then ask "When should we schedule the architecture review?"... **what happens?**

**Three possible outcomes**:
1. 🎯 **Works beautifully**: Suggests morning, references preference, shows learning
2. 🤔 **Partially works**: Shows some learning behavior but incomplete
3. 🎲 **Surprise**: Does something unexpected (good or concerning)

**All three outcomes are valuable data!**

---

## READY TO BEGIN!

**Current Time**: 6:30 PM PT
**Estimated Completion**: 8:30 PM PT
**Most Important Test**: Journey 2 (Learning System)
**Tool**: Chrome DevTools MCP (working!)
**Philosophy**: Discovery testing with complete evidence

**Let's find out what Piper can do!** 🚀🎯✨

---

*Automated Web UI Testing Prompt v1.0*
*Created: October 26, 2025, 6:30 PM PT*
*The moment we've been working toward all day!*
*Time to see Piper in action!*
