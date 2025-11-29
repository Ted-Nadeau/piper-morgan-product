# Session Logging Workflow Proposal

## Overview

**Problem**: Need both complete audit trail (raw logs) and structured knowledge (summaries)

**Solution**: Two-tier logging system with clear lifecycle

---

## Two-Tier System

### Tier 1: Raw Logs (Automatic via `tee`)

**Location**: `dev/archive/YYYY/MM/DD/YYYY-MM-DD-HHMM-prog-code-raw.txt`

**Content**: Verbatim terminal output
- All tool calls (including XML formatting)
- Complete command output
- Timing information
- Token usage warnings
- Agent "thinking" blocks

**Lifecycle**:
1. **Created**: Automatically via `cc-prog` alias during terminal sessions
2. **Stored**: Permanently in archive (never deleted)
3. **Accessed**: Only when debugging "what happened?" questions
4. **Not reviewed**: By chief of staff (too noisy)

**Example filename**: `dev/archive/2025/11/20/2025-11-20-0647-prog-code-raw.txt`

---

### Tier 2: Summary Logs (LLM-written, selective)

**Location**: `dev/active/YYYY-MM-DD-HHMM-<role>-code-log.md`

**Content**: Structured narrative
- What was accomplished
- Key decisions made
- Findings and recommendations
- Evidence (test results, benchmarks)
- Next steps

**Lifecycle**:
1. **Created**: Only for significant sessions (not every 5-min fix)
2. **Stored**: Initially in `dev/active/` during work-in-progress
3. **Promoted**: Move to `knowledge/` or `docs/briefing/` when complete
4. **Reviewed**: By chief of staff for decision-making
5. **Referenced**: By future agents via Serena memory system

**Example filename**: `dev/active/2025-11-20-0647-tool-code-log.md` (this session)

---

## When to Create Each Type

### Raw Logs (Tier 1): ALWAYS

**Start every terminal Claude Code session with:**
```bash
cc-prog  # alias for: claude-code | tee dev/archive/...
```

**Purpose**: Safety net - you never know when you'll need to replay what happened

---

### Summary Logs (Tier 2): SELECTIVELY

**Create summary log when:**
- ✅ Exploratory work with findings to document
- ✅ Architecture decisions made
- ✅ Multiple hours spent on complex task
- ✅ Novel patterns discovered
- ✅ Methodology changes proposed
- ✅ Integration testing completed
- ✅ Chief of staff needs briefing

**Skip summary log when:**
- ❌ Quick bug fix (<15 min)
- ❌ Routine tasks with no learnings
- ❌ Following existing gameplan with no deviations
- ❌ Just running tests without investigation

---

## Integration with Existing Workflow

### Current State (Manual)
1. Start `claude-code` in terminal
2. Agent creates session log with Write tool
3. PM manually copies interesting bits
4. Incomplete record

### Proposed State (Hybrid)
1. Start `cc-prog` in terminal → **raw log automatically captured**
2. At end of session, PM decides: "Was this significant?"
3. If yes → Agent creates summary log with Write tool
4. If no → Raw log sufficient (archived automatically)

**Result**: Complete audit trail + curated knowledge base

---

## File Organization

```
dev/
├── active/                          # Work-in-progress summary logs
│   ├── 2025-11-20-0647-tool-code-log.md     # This session (summary)
│   └── 2025-11-20-0900-prog-code-log.md     # Next session (summary)
│
├── archive/                         # Complete raw logs
│   └── 2025/
│       └── 11/
│           └── 20/
│               ├── 2025-11-20-0647-tool-code-raw.txt   # Raw tee output
│               └── 2025-11-20-0900-prog-code-raw.txt   # Raw tee output
│
└── 2025/                           # Alternative structure (if using date hierarchy)
    └── 11/
        └── 20/
            └── summaries/          # Summaries go here
                └── ...
```

**Cleanup rules**:
- `dev/active/`: Move to knowledge/ when session complete
- `dev/archive/`: Never delete (disk is cheap, debugging is expensive)
- Raw logs older than 90 days: Optionally compress with `gzip`

---

## Shell Setup Instructions

### 1. Add aliases to your shell config

```bash
# Open your shell config
nano ~/.zshrc  # or ~/.bashrc for bash

# Add these lines (from shell-aliases-for-claude-code.sh):
alias cc-prog='claude-code | tee ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'
alias cc-logs='ls -lah ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/'
alias cc-last='tail -n 100 $(ls -t ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/*.txt | head -1)'

# Save and reload
source ~/.zshrc
```

### 2. Create archive directory structure

```bash
# One-time setup
cd ~/Development/piper-morgan
mkdir -p dev/archive/2025/11/20

# Or automate it (add to your .zshrc):
alias setup-today='mkdir -p ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)'
```

### 3. Start using it

```bash
# Before starting terminal Claude Code session:
setup-today    # Ensure today's archive directory exists
cc-prog        # Start Claude Code with automatic logging

# Now work normally - everything is captured to:
# dev/archive/2025/11/20/2025-11-20-HHMM-prog-code-raw.txt
```

---

## CLAUDE.md Updates Needed

### Section: "Session Discipline"

**Add subsection: "Session Logging - Hybrid Approach"**

```markdown
## Session Logging - Hybrid Approach

### Raw Logs (Automatic)
Start every terminal session with `cc-prog` alias for automatic logging:
- Location: `dev/archive/YYYY/MM/DD/YYYY-MM-DD-HHMM-prog-code-raw.txt`
- Content: Complete verbatim transcript
- Purpose: Forensic audit trail

### Summary Logs (Selective)
Create structured summary for significant sessions:
- Location: `dev/active/YYYY-MM-DD-HHMM-<role>-code-log.md`
- Content: Narrative with findings/decisions/recommendations
- Purpose: Knowledge base for chief of staff and future agents
- When: Multi-hour sessions, exploratory work, architecture decisions

### Cursor Sessions
- Raw logs: Not applicable (no stdout to capture)
- Summary logs: Agent creates with Write tool (same as terminal)
- Use case: Exploratory conversations, quick questions, PM interventions
```

---

## Example: Today's Session

### What we created:
- ✅ **Summary log**: `dev/active/2025-11-20-0647-tool-code-log.md`
  - Structured comparison of terminal vs. Cursor
  - Integration test results
  - Recommendations for hybrid approach
  - Perfect for chief of staff review

### What we would have captured (if using `tee`):
- ❌ **Raw log**: `dev/archive/2025/11/20/2025-11-20-0647-tool-code-raw.txt`
  - Complete verbatim conversation
  - All tool calls with XML formatting
  - Exact pytest output with ANSI codes
  - Token usage warnings

**Why both matter**:
- Summary → "Here's what we learned about tooling integration"
- Raw → "Wait, exactly what command did we run for that pytest test?"

---

## Benefits of Hybrid Approach

### For PM (xian):
1. **Zero-effort audit trail** - Never lose context
2. **Curated knowledge base** - Chief of staff gets signal, not noise
3. **Debugging safety net** - Can always replay what happened
4. **Methodology compliance** - Raw logs prove evidence collection

### For Chief of Staff:
1. **Readable summaries** - No XML formatting or tool call noise
2. **Decision context** - Understands reasoning, not just actions
3. **Time-efficient review** - Read 2-page summary, not 200-page transcript
4. **Reference library** - Past summaries inform future decisions

### For Future Agents:
1. **Serena memory system** - Summaries become searchable knowledge
2. **Pattern discovery** - "How did we solve X last time?"
3. **Methodology evolution** - Learn from past session insights
4. **Context inheritance** - Understand project history quickly

---

## Questions for PM

1. **Approve hybrid approach?**
   - Raw logs automatic (every terminal session)
   - Summary logs selective (significant sessions only)

2. **File organization preference?**
   - Option A: `dev/archive/YYYY/MM/DD/` (proposed above)
   - Option B: `dev/YYYY/MM/DD/raw/` and `dev/YYYY/MM/DD/summaries/`
   - Option C: Different structure?

3. **Archive retention policy?**
   - Keep raw logs forever?
   - Compress raw logs older than 90 days?
   - Delete raw logs older than 1 year?

4. **Summary log promotion workflow?**
   - When to move from `dev/active/` to `knowledge/`?
   - Auto-promote after session ends?
   - Manual review before promotion?

5. **Shell alias preferences?**
   - `cc-prog` for "Claude Code programmer with logging"?
   - Different naming convention?
   - Additional aliases needed?

---

## Next Steps

1. [ ] PM reviews this proposal
2. [ ] PM adds aliases to `~/.zshrc` or `~/.bashrc`
3. [ ] Test `cc-prog` alias in one terminal session
4. [ ] Update CLAUDE.md with hybrid logging section
5. [ ] Document in knowledge/ for chief of staff
6. [ ] Create Serena memory for future agents

---

_Proposal ready for PM review and chief of staff feedback._
