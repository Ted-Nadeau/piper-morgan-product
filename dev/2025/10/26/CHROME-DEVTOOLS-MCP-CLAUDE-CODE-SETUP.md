# Chrome DevTools MCP: Setting Up for Claude Code (CLI)
**Date**: October 26, 2025
**Status**: Investigation Complete
**Goal**: Make Chrome DevTools MCP available to Claude Code CLI

---

## The Challenge

Claude Code (the CLI tool) and Claude Desktop (the GUI app) have different MCP configuration systems:

- **Claude Desktop**: Uses `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Claude Code (CLI)**: Doesn't currently have built-in MCP server configuration

---

## Current Situation

### What's Working
✅ Chrome DevTools MCP is installed and working in Claude Desktop
✅ Cursor Agent has access to Chrome DevTools
✅ Setup guide is complete and tested

### What's Not Working for Claude Code
❌ Claude Code doesn't read Claude Desktop's MCP configuration
❌ No native MCP configuration system in Claude Code
❌ No `mcp_servers` property in `.claude/settings.json`

---

## Options to Make It Available to Claude Code

### Option 1: Use Claude Desktop as Intermediary (Current Best Practice)
**Status**: Working now
**How it works**:
- Chrome DevTools MCP runs in Claude Desktop/Cursor
- Claude Code can ask you (the human) to use Cursor for browser-based testing
- Results are communicated back to Claude Code

**Pros**:
- No configuration needed
- Works immediately
- Can mix CLI testing + visual testing

**Cons**:
- Requires switching between tools
- Not fully automated from Claude Code

### Option 2: Create Standalone MCP Server (Future)
**Status**: Would require architecture change
**How it would work**:
- Run Chrome DevTools MCP as a persistent background service
- Claude Code connects to it via HTTP/websocket
- Multiple tools can share the same browser instance

**Pros**:
- Fully automated
- Single source of truth for browser state
- Works from CLI

**Cons**:
- Requires new service architecture
- Additional setup complexity
- Service management needed

### Option 3: Environment-Based MCP Discovery (Not Yet Supported)
**Status**: Proposed but not implemented in Claude Code
**How it would work**:
- Export MCP servers to environment variables
- Claude Code reads and initializes them
- Standard MCP protocol

**Pros**:
- Clean separation of concerns
- Follows MCP standards

**Cons**:
- Requires Claude Code update
- May not be on Anthropic's roadmap

---

## Recommended Approach for You Now

### Use Cursor + Claude Code Partnership

Since Cursor has the Chrome DevTools MCP working, here's how to leverage it:

**For Automated E2E Testing**:
1. **Claude Code** (CLI) - Handles all Python/backend testing
2. **Cursor** with Chrome DevTools MCP - Handles UI/browser testing
3. **Communication**: Claude Code requests browser tests from you, Cursor performs them

**Example Workflow**:
```
Claude Code: "Now we need to test the chat interface. Can you:
1. Navigate to localhost:8001
2. Take a screenshot
3. Send a test message
4. Verify the response appears"

You (in Cursor): [Use Chrome DevTools to perform the test]

You: "Screenshot attached. Response appeared correctly in 2.3 seconds."

Claude Code: [Continues with next tests]
```

---

## Future: Making Chrome DevTools MCP Available to Claude Code

If you want Claude Code to directly access browser automation in the future:

### Step 1: Run Chrome DevTools MCP as a Service

```bash
# Keep this running in background
npx chrome-devtools-mcp@latest \
  --executablePath=/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --isolated \
  --port=3000
```

### Step 2: Create a Proxy Service

Create a simple Python service in Piper Morgan that Claude Code can call:

```python
# services/browser/chrome_devtools_client.py
import asyncio
from aiohttp import ClientSession

class ChromeDevToolsClient:
    def __init__(self, mcp_port=3000):
        self.base_url = f"http://localhost:{mcp_port}"

    async def take_screenshot(self, url: str) -> bytes:
        """Take screenshot via Chrome DevTools MCP"""
        async with ClientSession() as session:
            async with session.post(
                f"{self.base_url}/screenshot",
                json={"url": url}
            ) as resp:
                return await resp.read()

    async def navigate(self, url: str) -> bool:
        """Navigate to URL"""
        async with ClientSession() as session:
            async with session.post(
                f"{self.base_url}/navigate",
                json={"url": url}
            ) as resp:
                return resp.status == 200
```

### Step 3: Add to Claude Code Permissions

Update `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "mcp__chrome_devtools__*",
      "Bash(npx chrome-devtools-mcp:*)"
    ]
  }
}
```

---

## What You Should Do Now

### Immediate (Next 15 minutes)
1. Verify Chrome DevTools MCP works in Cursor by taking a screenshot
2. Test it with localhost:8001 to confirm Piper Morgan testing capability
3. Document the workflow for future reference

### Short-term (This week)
1. Use Cursor + Claude Code partnership for Phase 2 testing
2. Collect evidence from Cursor (screenshots, interactions)
3. Share results with Claude Code for analysis

### Long-term (Post-Alpha)
1. Consider dedicated browser automation service for Claude Code
2. Evaluate if full integration is needed based on usage patterns
3. Decide between option 2 (service) or option 3 (protocol support)

---

## Current Working Architecture

```
Your Development Machine
├── Claude Code (CLI)
│   ├── Python testing ✅
│   ├── Backend validation ✅
│   └── Browser testing ❌ (can request from Cursor)
│
├── Cursor Agent (GUI)
│   ├── Code editing ✅
│   ├── Chrome DevTools MCP ✅
│   └── Browser automation ✅
│
└── Piper Morgan Server
    ├── localhost:8001 ✅
    ├── PostgreSQL ✅
    └── All services ✅
```

---

## Key Insight

**The Chrome DevTools MCP is already working in Cursor.** The question isn't "how do we set it up" - it's "how do we integrate it with Claude Code's workflow."

The cleanest approach for now is to use them as complementary tools:
- **Claude Code**: Handles server-side testing and orchestration
- **Cursor**: Handles browser-based UI testing
- **Communication**: You bridge the two by running commands in Cursor and reporting back

This is actually quite efficient because:
1. No context switching between test frameworks
2. Each tool focuses on its strength
3. You maintain full visibility and control
4. Results are immediately documented

---

## Next Steps for You

1. **Confirm** Cursor + Chrome DevTools MCP works at localhost:8001
2. **Document** the workflow and any findings
3. **Use** this for Phase 2 UI testing if needed
4. **Decide** if full Claude Code integration is needed for post-alpha

---

**Status**: Chrome DevTools MCP is available in Cursor and ready to use.
**Recommendation**: Leverage it from there for now, plan deeper integration if needed later.
