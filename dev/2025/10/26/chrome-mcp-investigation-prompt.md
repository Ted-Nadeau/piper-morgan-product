# Chrome DevTools MCP Integration - Investigation & Setup

**Agent**: Cursor (Code Agent)
**Task**: Investigate and configure Chrome DevTools MCP for automated web UI testing
**Priority**: Medium (nice-to-have tooling, not blocking current testing)
**Time Box**: 45-60 minutes
**Date**: Sunday, October 26, 2025, 10:43 AM PT

---

## MISSION

Investigate why Chrome DevTools MCP integration failed in previous attempt (a few weeks ago) and either:
1. **Get it working** with clear setup instructions, OR
2. **Document why it won't work** and what blockers exist

**Goal**: Enable automated web UI testing for Piper Morgan at localhost:8001

---

## CONTEXT

### What We're Testing
- **Piper Morgan web interface**: localhost:8001
- **Current approach**: Human manually interacts with web UI
- **Desired**: Assistant can automate UI testing via Chrome MCP

### Previous Attempt
- Tried to set up Chrome DevTools MCP a few weeks ago
- **Failed** - specific error unknown
- **Deprioritized** as non-blocking nice-to-have
- No documentation of what went wrong

### Current Status
- Phase 2 E2E testing starting NOW (10:43 AM)
- Human will manually test web UI initially
- If you solve this during testing window, we can use it immediately
- If not, we proceed with manual testing (totally fine!)

---

## INVESTIGATION AREAS

### Area 1: Chrome DevTools MCP Overview [15 MIN]

**Research Questions**:
1. What is Chrome DevTools MCP?
   - Official repo/documentation?
   - What does it provide?
   - How does it integrate with Claude/MCP?

2. What are the prerequisites?
   - Chrome version requirements?
   - Node.js/npm versions?
   - MCP server requirements?
   - Operating system considerations?

3. What capabilities does it provide?
   - Can it interact with localhost:8001?
   - Can it take screenshots?
   - Can it fill forms?
   - Can it click buttons?
   - Can it read page content?

**Deliverable**: Summary document with:
- Official documentation links
- Capability matrix
- Prerequisites list

---

### Area 2: Installation & Configuration [20 MIN]

**Tasks**:
1. Find official installation instructions
2. Document exact setup steps
3. Identify configuration requirements
4. Note any environment variables needed

**Specific Questions**:
- How to install the MCP server?
- How to connect it to Claude?
- How to configure for localhost access?
- Any security/permission requirements?

**Test Setup** (if possible):
```bash
# Document actual commands needed
# Example structure:
npm install -g @modelcontextprotocol/chrome-devtools
# OR
git clone <repo>
cd <repo>
npm install
# Configure...
```

**Deliverable**: Step-by-step installation guide

---

### Area 3: Common Issues & Troubleshooting [10 MIN]

**Research**:
1. Known issues with Chrome DevTools MCP
2. Common setup failures
3. Platform-specific problems (macOS focus)
4. Localhost access issues

**Questions**:
- Does it work with localhost?
- Any CORS issues?
- Chrome security restrictions?
- Firewall/permission issues?

**Deliverable**: Troubleshooting guide with known issues

---

### Area 4: Testing & Verification [15 MIN]

**If Installation Successful**:

Try to connect to Piper Morgan:
```bash
# Assuming system running at localhost:8001
# Test basic operations:
1. Can MCP connect to Chrome?
2. Can it navigate to localhost:8001?
3. Can it read page content?
4. Can it take screenshot?
5. Can it interact with elements?
```

**Test Scenarios**:
```javascript
// Example test (adjust to actual MCP API)
1. Navigate to localhost:8001
2. Take screenshot of landing page
3. Find chat input field
4. Enter text: "Hello, this is a test"
5. Click send button
6. Read response
7. Take screenshot of response
```

**Deliverable**: Test results with evidence

---

## DECISION TREE

### Scenario A: Installation Successful ✅

**Document**:
1. ✅ Complete installation steps (with screenshots)
2. ✅ Configuration file (with comments)
3. ✅ Test results showing it works
4. ✅ Example usage for Piper Morgan testing
5. ✅ Quick start guide for PM to use immediately

**Format**: `chrome-mcp-setup-guide-WORKING.md`

---

### Scenario B: Installation Failed with Known Issue ⚠️

**Document**:
1. ❌ What failed (exact error messages)
2. 🔍 Why it failed (root cause analysis)
3. 🛠️ Attempted fixes (what you tried)
4. ⏳ Potential solutions (if you have ideas)
5. 📋 Blockers (what's preventing success)

**Recommendation**: Document for future revisit

**Format**: `chrome-mcp-investigation-BLOCKED.md`

---

### Scenario C: Works But Not for Localhost ⚠️

**Document**:
1. ✅ Installation successful for external sites
2. ❌ Localhost access blocked
3. 🔍 Why localhost blocked (CORS, security, etc.)
4. 🛠️ Workaround attempts
5. 💡 Alternative approaches

**Recommendation**: Document workarounds or alternatives

**Format**: `chrome-mcp-localhost-limitation.md`

---

### Scenario D: Not Worth the Effort ❌

**Document**:
1. ⚠️ Too complex/fragile
2. 📊 Effort vs benefit analysis
3. ✅ Manual testing is fine
4. 💭 Recommendation to skip

**Recommendation**: Don't pursue further, manual testing sufficient

**Format**: `chrome-mcp-not-recommended.md`

---

## OUTPUT REQUIREMENTS

### Required Deliverables

**Investigation Report**:
```markdown
# Chrome DevTools MCP Investigation Report

**Date**: October 26, 2025
**Agent**: Cursor
**Duration**: [actual time]
**Result**: WORKING / BLOCKED / LIMITED / NOT RECOMMENDED

## TL;DR
[2-3 sentence summary: Can we use it? Why or why not?]

## Investigation Summary

### Area 1: Overview
[What is it? What does it do?]

### Area 2: Installation
[How to install? Did it work?]

### Area 3: Issues Found
[What problems encountered?]

### Area 4: Testing Results
[If successful, what works?]

## Decision

**Can Use for Piper Morgan Testing**: YES / NO / PARTIALLY

**Reasoning**: [Why?]

**Next Steps**: [What to do?]

## Appendix

### Links
- Official docs: [URL]
- Repo: [URL]
- Issues: [URLs]

### Commands
```bash
[Installation commands if successful]
```

### Configuration
```json
[Config files if successful]
```

### Screenshots
[If you got it working, show proof]
```

---

## STOP CONDITIONS

### Stop Immediately If:
1. **Can't find official documentation** (>15 min searching)
   → Document that it may not exist or be unmaintained

2. **Installation fails repeatedly** (>30 min troubleshooting)
   → Document error, recommend manual testing

3. **Works but can't access localhost** (>15 min trying workarounds)
   → Document limitation, manual testing is fine

### Time Box: 60 Minutes Maximum
- Don't spend more than 1 hour total
- This is nice-to-have, not critical
- Manual testing works fine
- Document and move on if stuck

---

## SUCCESS CRITERIA

### Minimum Success (Good Outcome):
- [ ] Clear answer: Can we use it or not?
- [ ] Documentation of findings
- [ ] Installation guide (if it works)
- [ ] OR clear blocker explanation (if it doesn't)

### Ideal Success (Best Outcome):
- [ ] Working Chrome MCP connection
- [ ] Can access localhost:8001
- [ ] Can take screenshots
- [ ] Can interact with page elements
- [ ] Quick start guide for PM
- [ ] Example test scenario working

### Acceptable Outcome (Also Fine):
- [ ] Clear documentation of why it won't work
- [ ] Recommendation to continue manual testing
- [ ] Time not wasted on unsolvable problems

---

## NOTES FOR CURSOR

### Context You Should Know

**Piper Morgan Architecture**:
- Web server runs on localhost:8001
- Built with FastAPI (Python)
- Frontend likely simple HTML/JS/CSS
- No complex SPA frameworks (probably)
- Focus: Testing the chat interface

**Testing Needs**:
- Send messages to chat
- Verify responses appear
- Take screenshots for evidence
- Verify UI elements render
- Check error handling

**Current Manual Process**:
1. Human opens browser → localhost:8001
2. Human types message in chat input
3. Human clicks send
4. Human screenshots response
5. Repeat for all test scenarios

**What Automation Would Save**:
- Screenshot automation
- Faster test execution
- Repeatable test scenarios
- Evidence collection
- But: Not critical, manual works fine

### Investigation Strategy

**Recommended Approach**:
1. **Quick research** (10 min): Find official docs, understand what it is
2. **Fast attempt** (20 min): Try to install and run basic test
3. **Decision point** (30 min mark):
   - Working? → Document and provide guide
   - Not working? → Document blocker and recommend manual
4. **Wrap up** (10 min): Create deliverable report

**Don't Get Stuck On**:
- Complex debugging (>15 min on single issue)
- Obscure configuration (if docs unclear)
- Workarounds that seem fragile
- Anything that feels "hacky"

**Remember**: Manual testing is totally fine! This is bonus tooling.

---

## EXAMPLE OUTPUT (If Working)

```markdown
# Chrome DevTools MCP - Setup Guide

## Quick Start

### Install
```bash
npm install -g @modelcontextprotocol/chrome-devtools
```

### Configure
```json
{
  "mcpServers": {
    "chrome": {
      "command": "chrome-devtools-mcp",
      "args": ["--allow-localhost"]
    }
  }
}
```

### Test
```bash
# In Claude
"Navigate to localhost:8001 and take a screenshot"
```

### Success! ✅
[Screenshot showing it working]

## Usage for Piper Morgan Testing

Use these commands during Phase 2 testing:

1. **Navigate**: "Open localhost:8001 in Chrome"
2. **Screenshot**: "Take a screenshot of the current page"
3. **Interact**: "Click the chat input and enter 'test message'"
4. **Verify**: "Check if response appeared and screenshot it"

---

Ready to use immediately! 🚀
```

---

## EXAMPLE OUTPUT (If Not Working)

```markdown
# Chrome DevTools MCP - Investigation Report

## TL;DR
❌ Cannot get Chrome DevTools MCP working for localhost testing.

## Issue Found
Chrome DevTools MCP requires Chrome to be started with specific flags that conflict with normal Chrome usage. Additionally, localhost access has CORS restrictions that are not easily resolved.

## Attempted
- Installed MCP server (successful)
- Configured for localhost (failed - CORS)
- Tried --allow-localhost flag (didn't help)
- Researched workarounds (none reliable)

## Recommendation
✅ **Continue with manual web UI testing.**

Manual testing works well for Phase 2 needs:
- Human can easily interact with localhost:8001
- Screenshots are simple (Command+Shift+4)
- Evidence collection straightforward
- No complex automation needed for 4-6 hour test session

## Future Revisit?
Maybe post-Alpha when we need automated regression testing. For now, not worth the complexity.

---

Manual testing is perfectly fine! ✅
```

---

## READY TO INVESTIGATE!

**Start Time**: 10:43 AM
**Time Box**: 60 minutes max
**End Time**: ~11:45 AM (or earlier if clear answer found)

**Remember**:
- Quick research → Fast attempt → Clear decision
- Don't get stuck on unsolvable problems
- Manual testing works great!
- Document your findings clearly

**Good luck!** 🚀

---

*Investigation Prompt Version: 1.0*
*Created: October 26, 2025, 10:43 AM PT*
*Non-blocking tooling investigation*
*Success = Clear answer (works or doesn't)*
