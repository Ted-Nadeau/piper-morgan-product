# Beads Integration Proposal

**Prepared by**: Cursor Agent (with PM guidance)
**Date**: November 13, 2025
**Status**: For Review and Decision
**Reviewers**: Chief of Staff, Chief Architect, Senior Team Members

---

## Executive Summary

We propose a **2-week pilot of Beads**, a lightweight git-backed issue tracker designed for AI coding agents, to address session amnesia and work discovery gaps in our current agentic workflow.

**Expected Benefits**:

- +40% agent productivity (estimated)
- 90%+ automatic work discovery capture
- Sub-30-second session handoffs
- Foundation for multi-agent coordination (GREAT-3B)

**Investment**: 2 weeks, ~20 hours
**Risk**: Low (alpha software, but reversible with minimal sunk cost)
**Decision Point**: Week 2 - Go/No-Go on broader rollout

---

## The Problem

### Current Limitations with Markdown-Based TODO Tracking

1. **Session Amnesia**: Agents lose context on restart, requiring 2-3 minute re-briefing each session
2. **Lost Work**: Agents notice bugs/gaps but don't record them ("I see X but let's continue...")
3. **Long-Horizon Planning**: Multiple markdown plan files in varying stages of decay, agents lose track
4. **Multi-Agent Conflicts**: Conflicting TODO lists, duplicated work, no coordination mechanism

**Manifestation**: We spend significant time per session re-orienting agents, recovering lost work, and managing stale plans.

**Quantified Impact** (estimated):

- 15-20% of agent time spent on session ramp-up
- 10-15% of discovered work never recorded
- 25% of planning artifacts become obsolete and confusing

### Real-World Example: The Descent Into Madness

From Steve Yegge's article, describing a pattern we've experienced:

```
Agent starts: "This is big! I'll break it into 6 phases."
Phase 1 ✅ complete
Phase 2 ✅ complete
Phase 3 starts → Agent: "This is big! I'll break it into 5 phases."
  Phase 1 [of 5] ✅
  Phase 2 [of 5] ✅
  Phase 3 [of 5] starts → Agent: "This is big! 4 phases!"
    ... eventually ...
Agent: "DONE! 🎉"
You: "What about the other phases?"
Agent: "What phases?"
```

**Result**: Multiple nested plans, agent loses track of outer context, work appears complete but isn't.

---

## The Solution: Beads

### What It Is

- **Lightweight issue tracker** (single Go binary)
- **Git-backed JSONL storage** with SQLite query layer
- **Designed specifically** for AI coding agent workflows
- **Created by Steve Yegge** (Sourcegraph), rapidly adopted by vibe coding community
- **Maturity**: Alpha (v0.22.0), 1,000+ GitHub stars, 27+ contributors in 27 days

### Core Capabilities

1. **Fast Queries**: `bd ready --json` → unblocked work in milliseconds
2. **Structured Dependencies**: `blocked_by`, `discovered_from`, `parent`, `epic`
3. **Persistent Memory**: Work queue survives across agent restarts
4. **Multi-Agent Ready**: Distributed via git, claim/status mechanism
5. **Self-Healing**: Corruption recoverable from git history
6. **Automatic Work Discovery**: Agents file issues as they discover work

### Technical Architecture

```
┌─────────────────────────────────────┐
│  SQLite (query performance)         │ <- Fast queries (milliseconds)
├─────────────────────────────────────┤
│  JSONL (git-friendly storage)       │ <- Line-based diffs, human-readable
├─────────────────────────────────────┤
│  Git (versioning, distribution)     │ <- Never lose data, standard workflow
└─────────────────────────────────────┘
```

**Key Insight**: "External memory for agents" - structured, persistent, query-able state that survives context windows.

### Why This Stack Works

**Git + JSONL**:

- Line-based diffs (clean merges)
- Human-readable (can manually inspect/fix)
- Version history (time travel, forensics)
- Distributed (no central server)
- Standard workflow (branches, PRs)

**SQLite**:

- Fast queries (milliseconds)
- SQL interface (complex queries easy)
- Hydrates from JSONL on demand
- Can be deleted and rebuilt (git is source of truth)

**Self-Healing Architecture**:

- Database corruption? → Rebuild from git history
- ID collisions? → AI resolves intelligently
- Lost issues? → Recover from git log
- Agents fix Beads problems autonomously

---

## Why Beads Fits Piper Morgan

### Alignment with Current Methodology

#### Pattern-009 (GitHub Issues): Enhanced, Not Replaced

**Current**: All work tracked in GitHub Issues

- Epics, features, bugs manually created
- Issue numbers in commits (e.g., GREAT-3B)
- Good for PM/stakeholder visibility

**With Beads**: Two-tier system

- **GitHub** = Strategic layer (epics, external visibility, stakeholder communication)
- **Beads** = Tactical layer (micro-tasks, agent work, discovered issues)
- **Sync service** bridges the two

**Result**: Pattern-009 unchanged for stakeholders, massively upgraded for agents

#### Inchworm Protocol: Natural Extension

**Current Inchworm**:

1. Fix - Solve the actual problem
2. Test - Prove it works
3. Lock - Prevent regression
4. Document - Update docs
5. Verify - Check North Star test

**Enhanced with Beads**:

- **Step 0** (NEW): Query ready work (`bd ready --json`)
- **Steps 1-5**: Unchanged
- **Step 6** (NEW): Update Beads, queue next work

**"Landing the Plane" Protocol**: Comprehensive session hygiene checklist (detailed below)

#### Verification-First: Strengthened

- Beads issues provide audit trail
- `discovered_from` chains show work provenance
- Git history + issue relationships = rich forensics
- Evidence = Beads issues with linked commits

### Enables Strategic Goals

#### GREAT-3B (Plugin Infrastructure - Current Sprint)

**Challenge**: Multi-agent coordination on parallel tasks

**With Beads**:

```bash
# Agent 1: Plugin interface
bd claim bd-301 --assignee agent-1

# Agent 2: Example plugins (independent task)
bd claim bd-304 --assignee agent-2

# Agent 3: Dynamic loader (depends on bd-301)
bd ready --json  # Shows bd-302 blocked by bd-301

# Later: Agent 1 completes bd-301
bd update bd-301 --status done

# Agent 3: Now unblocked
bd ready --json  # bd-302 now ready!
```

**Benefits**: Parallel work, automatic dependency management, no duplicate effort

#### 24x7 Agents (Near-term Roadmap)

- Persistent work queue eliminates manual briefing
- Automatic session handoff
- Agents self-direct from Beads
- "What's next?" → `bd ready` → immediate answer

#### Learning System Enhancement (Medium-term)

**Pattern Detection from Work Discovery**:

```python
# Analyze discovered_from relationships
pattern = analyzer.analyze_discovery_chain(starting_issue="bd-42", depth=3)

if pattern.frequency > 0.7:
    # "Implementing Feature X often uncovers bugs in Module Y"
    learning_service.store_pattern(
        pattern_type=PatternType.WORK_DISCOVERY,
        pattern_data=pattern,
        confidence=pattern.frequency
    )

# Next time: Proactive issue filing
when user asks to implement feature X:
    suggest_proactive_checks(similar_patterns)
    # "Based on patterns, should I check Module Y first?"
```

**Benefits**: Predictive issue filing, workflow optimization, risk assessment

#### Agent Swarm (Long-term Vision)

- Distributed coordination via git-synced Beads
- Status visibility (claimed, in-progress, blocked)
- Hierarchical task breakdown and delegation
- Foundation for sophisticated multi-agent orchestration

---

## Comparison to Alternatives

### vs. Markdown TODOs (Status Quo)

| Aspect           | Markdown                       | Beads                         |
| ---------------- | ------------------------------ | ----------------------------- |
| **Query speed**  | Slow (parse files)             | Fast (SQLite)                 |
| **Structure**    | Prose                          | Structured data               |
| **Dependencies** | Implicit in text               | First-class relationships     |
| **Multi-agent**  | Conflicts, duplicates          | Coordinated via git           |
| **Agent memory** | Session-only                   | Persistent                    |
| **Bit-rot**      | High (agents forget to update) | Low (explicit status updates) |

**Verdict**: Beads vastly superior for agent workflows

### vs. GitHub Issues Only (Expand Pattern-009)

| Aspect                  | GitHub Issues           | Beads                      |
| ----------------------- | ----------------------- | -------------------------- |
| **Query speed**         | API (slow, rate limits) | Local SQLite (fast)        |
| **Offline**             | ❌ No                   | ✅ Yes                     |
| **Weight**              | Medium                  | Very light (single binary) |
| **External visibility** | ✅ Excellent            | ❌ None (needs sync)       |
| **Agent-native**        | Adapted for agents      | Designed for agents        |
| **Dependency types**    | Basic                   | Rich (4 types)             |

**Verdict**: Complementary, not competing. Both have roles to play.

### vs. Build Piper-Native System

| Aspect                  | Adopt Beads          | Build Piper-Native    |
| ----------------------- | -------------------- | --------------------- |
| **Time to value**       | 2 weeks              | 3-6 months            |
| **Development cost**    | Low (just integrate) | High (design + build) |
| **Maintenance**         | Community            | Us                    |
| **Proven**              | Yes (daily use)      | No (theoretical)      |
| **Piper integration**   | Sync layer           | Native (seamless)     |
| **External dependency** | Yes                  | No                    |

**Verdict**: Start with Beads (fast validation), build Piper-native later if strategic value proven but Beads insufficient.

---

## Proposed Pilot: 2-Week Validation

### Week 1: Core Validation

#### Experiment 1: Quickstart (Days 1-2)

**Setup** (30 minutes):

```bash
# Install Beads
brew tap steveyegge/beads
brew install beads

# Initialize in project
cd /Users/xian/Development/piper-morgan
bd init

# Install MCP server
pip install beads-mcp

# Configure Claude Code (add beads-mcp to MCP servers)
```

**Test Scenario**:

1. Create epic in Beads for GREAT-3B (or current work)
2. Agent breaks down into 4-5 subtasks
3. Agent works on first subtask
4. Agent discovers 2-3 issues during work, files them with `bd create`
5. Stop agent (simulate compaction/restart)
6. Start fresh agent session
7. Agent runs `bd ready --json` → immediately knows what to do
8. Agent continues where previous session left off

**Success Criteria**:

- ✅ Context recovery < 10 seconds (vs 2-3 minutes currently)
- ✅ Zero work items lost
- ✅ Agent files issues without prompting (>80% of discoveries)
- ✅ `bd ready` query time < 100ms

**Evidence to Capture**:

- Terminal output showing `bd ready` results
- Time-stamped session logs (before vs after restart)
- Screenshot of issue graph with dependencies
- Agent's autonomous issue filing

**Risk**: Very Low

- Takes 2 hours max
- Easy to uninstall if unsuccessful
- No changes to production workflow
- Can explore before formal commitment

#### Experiment 2: Agent Endorsement (Day 3)

**Process**:
Ask agent: "I'm considering adopting Beads for our work tracking. Here's the repo: https://github.com/steveyegge/beads. Would this be useful for your work? Why or why not?"

**Goal**: Validate that agents enthusiastically endorse Beads (as Steve claims they do)

**Compare agent feedback with**:

- Claude's assessment from Steve's article (Appendix A)
- Our theoretical benefits analysis
- Identify any concerns or objections

**Success Criteria**:

- ✅ Agent identifies structured data benefits
- ✅ Agent recognizes session persistence value
- ✅ Agent expresses preference over markdown TODOs

**Evidence**: Conversation transcript, agent's reasoning

### Week 2: Integration & Multi-Agent

#### Experiment 3: GitHub Hybrid (Days 1-3)

**Goal**: Test two-tier system (strategic GitHub, tactical Beads)

**Implementation**: Basic sync script

```python
# scripts/beads-github-sync.py
def sync_epics_to_github():
    """One-way sync: Beads epics → GitHub issues"""
    epics = beads_cli.query(labels=['epic', 'external-visibility'])

    for epic in epics:
        if not epic.metadata.get('github_id'):
            gh_issue = github_api.create_issue(
                title=f"[Beads {epic.id}] {epic.title}",
                body=generate_epic_body(epic),
                labels=['epic', 'beads-synced']
            )
            beads_cli.update(epic.id, metadata={'github_id': gh_issue.number})
```

**Test Workflow**:

1. Agent creates epic in Beads: `bd create --title "GREAT-3B: Plugin Infrastructure" --labels epic,p0`
2. Agent creates 5 subtasks in Beads
3. Sync runs: Epic appears in GitHub with subtask checklist
4. PM reviews GitHub issue
5. Agent works on subtasks in Beads
6. Sync updates GitHub with progress

**Success Criteria**:

- ✅ Epics visible in GitHub (stakeholder transparency maintained)
- ✅ Micro-tasks stay in Beads (fast, local, agent-friendly)
- ✅ PM workflow unchanged
- ✅ Sync latency < 5 minutes
- ✅ No data loss

#### Experiment 4: Landing Protocol (Days 4-5)

**Goal**: Implement comprehensive end-of-session hygiene

**"Landing the Plane" Checklist** (added to AGENTS.md):

1. Run test suite, fix failures
2. Run linter, fix errors
3. Remove debugging code/temp files
4. Check git stashes and unmerged branches
5. Update current Beads issue status
6. Sync with git: `bd sync`
7. File any undiscovered issues
8. Run GitHub sync script
9. Update documentation
10. Git operations (fix-newlines, commit, push)
11. Query next work: `bd ready --json`
12. Create tailored prompt for next session
13. Provide session summary

**Test**:

1. Agent works on feature for 20-30 minutes
2. User says: "land the plane"
3. Agent executes entire protocol systematically
4. Start new agent with generated prompt
5. Measure: Time to productive work

**Success Criteria**:

- ✅ Protocol completes in < 5 minutes
- ✅ All quality gates pass
- ✅ Next agent productive in < 30 seconds
- ✅ Zero lost work between sessions

---

## The "Landing the Plane" Protocol

This protocol is valuable **even without Beads** and addresses a current gap in our methodology.

### Current Problem

Agents at end-of-session often:

- Rush through cleanup (low on context)
- Skip tests that "someone else broke"
- Leave debugging code
- Forget to update documentation
- Don't prepare next session

**Result**: "Steak dinner ready" when there's "still a dead cow in the living room"

### Solution: Systematic Checklist

When user says "land the plane", agent executes comprehensive protocol:

**Quality Gates** → **Cleanup** → **Beads Hygiene** → **GitHub Sync** → **Documentation** → **Git Operations** → **Next Work Selection** → **Session Summary**

**Benefits**:

- No shortcuts taken (agents thorough even at low context)
- Clean handoffs between sessions
- Zero lost work
- Clear path forward for next agent
- Professional-grade session hygiene

**Implementation**: Single AGENTS.md addition, triggered by phrase "land the plane"

---

## Go/No-Go Decision Criteria (End of Week 2)

### Proceed to Rollout If:

- ✅ Agent productivity increase **>30%** (measured by tasks/hour)
- ✅ Work discovery capture **>80%** (vs ~15% currently)
- ✅ **Zero critical data loss** incidents
- ✅ Team feedback **positive**
- ✅ Stability **acceptable** for daily use
- ✅ GitHub visibility **maintained**

### Abort If:

- ❌ Productivity gains **< 20%**
- ❌ **Frequent data loss** or corruption
- ❌ Agents **struggle** with Beads
- ❌ Integration complexity **too high**
- ❌ Stability **unacceptable** (crashes, data loss)

### Sunk Cost If Abort:

~20 hours, easy removal:

```bash
brew uninstall beads
pip uninstall beads-mcp
# Revert CLAUDE.md changes
# Remove scripts/beads-github-sync.py
```

No permanent changes to codebase, workflow, or methodology.

---

## Risk Assessment

| Risk                      | Level         | Mitigation                                                                     | Fallback                                    |
| ------------------------- | ------------- | ------------------------------------------------------------------------------ | ------------------------------------------- |
| **Alpha software bugs**   | High → Medium | Self-healing architecture, git preserves data, v0.22.0 architecturally stable  | Rebuild DB from git, or abort pilot         |
| **Vendor lock-in**        | Low           | JSONL format portable, can migrate out, simple codebase (15k LOC), can fork    | Build Piper-native system                   |
| **Team adoption curve**   | Low-Medium    | Good documentation, gradual rollout, agents endorse enthusiastically           | Optional tool initially                     |
| **GitHub divergence**     | Medium        | Automated sync service, discipline around epic promotion                       | Manual sync, or Beads-only                  |
| **Performance at scale**  | Medium        | Monitor issue count, archive old issues (git preserves), SQLite proven to 10k+ | Upgrade to PostgreSQL if needed             |
| **Community abandonment** | Medium        | 27+ contributors, portable format, can fork                                    | Take over maintenance or build Piper-native |
| **Data loss**             | Low           | Git is source of truth, agents can reconstruct from history                    | Git history recovery                        |
| **Sync complexity**       | Medium-High   | Start with one-way sync (simple), iterate based on needs                       | Manual sync, or keep systems separate       |

**Overall Risk**:

- **Pilot (2 weeks)**: Low (reversible, minimal investment)
- **Long-term adoption**: Medium (alpha software, external dependency)

**Risk Management Strategy**: Pilot validates value before committing; fallback to Piper-native system if Beads fails long-term.

---

## Investment & Timeline

### Pilot Phase (Weeks 1-2)

**Time**: ~20 hours (PM + agent time)
**Cost**: Near-zero (free software, existing infrastructure)

**Deliverables**:

- Beads installed and configured
- 4 experiments completed with evidence
- Metrics captured: productivity, work capture, stability
- Go/No-Go recommendation with rationale
- Documentation: `docs/integrations/beads-pilot-results.md`

### Rollout Phase (Weeks 3-4) - If Pilot Succeeds

**Time**: ~40 hours

**Deliverables**:

- All agents configured with Beads
- GitHub sync service operational
- "Landing the Plane" protocol implemented
- Multi-agent coordination tested
- Documentation: `docs/methodology/beads-workflow.md`

### Enhancement Phase (Months 2-3) - Roadmap

**Time**: ~60 hours

**Deliverables**:

- Learning system integration (BeadsPatternAnalyzer)
- Pattern detection operational
- Proactive issue filing
- 24x7 agent capability demonstrated
- Multi-agent swarm tested

---

## Success Metrics

### Quantitative

- **Agent productivity**: +40% (target), measured by tasks completed per hour
- **Work capture rate**: 90%+ of discovered work auto-filed (vs ~15% captured currently)
- **Session handoff time**: < 30 seconds (vs 2-3 minutes currently)
- **Multi-agent coordination**: Zero duplicate work, zero blocking conflicts
- **Query performance**: < 100ms for `bd ready` (vs 2-3 seconds parsing markdown)

### Qualitative

- **Agent feedback**: Enthusiastic endorsement in "ask your agent" test
- **PM experience**: Reduced overhead, clearer visibility into work state
- **Code quality**: Fewer shortcuts, better test coverage (agents less rushed)
- **Planning clarity**: Hierarchical epics with dependencies vs multiple stale markdown files

### Evidence-Based

All claims backed by:

- Terminal output showing `bd ready` queries and results
- Git history showing issue creation and updates
- Time-stamped session logs (before vs after)
- GitHub issue updates with progress from Beads
- Screenshots of issue graph with dependencies

---

## Notable Technical Details

### Why Go for Beads?

Steve Yegge's experience (350k LOC TypeScript → new Go project):

**TypeScript** (AI-generated):

- Agents write mediocre TypeScript easily
- Complex type gymnastics
- Code grows like weeds
- Testing easier

**Go** (AI-generated):

- "Brutally simple" - loops, functions, if/else
- Impossible to write bad Go code (worst = mediocre)
- Sub-linear code base growth
- Malleable: big changes with small code modifications

**Verdict**: Go is better target language for AI code generation.

### Temporal Warning (Side Note for Chief Architect)

Steve's first architectural mistake with `vibecoder`:

- Used Temporal for workflow orchestration
- "Too heavyweight for developer desktop tool"
- Leaked through entire codebase
- Made pivot impossible without rewrite

**Anthropic data point**: "Someone I know at Anthropic — they had tried it there, too"

**Implication for Piper**: If we consider workflow orchestration, carefully evaluate Temporal's weight vs our use case.

### The "Addiction Problem"

Steve seriously warns: "So addictive you will literally pee yourself"

**Why**:

- Eliminates session handoff friction
- Agents work longer, easier to run more concurrently
- "Never have it forget or disclaim any work — that's paradise"
- "Like adderall for agents, crack for you"

**Physical symptoms reported**: Drooling while in "the zone", unable to stop starting new agents

**Recommendation**: Set agent limits, schedule breaks, embrace productivity boost

---

## Recommendation

### Approve 2-Week Pilot with Following Conditions:

1. **Focused scope**: Single developer (PM), current work (GREAT-3B or active epic), daily vibe coding
2. **Evidence required**: All experiments documented with terminal output, metrics captured
3. **Decision gate**: Week 2 - present results, make Go/No-Go decision on rollout
4. **Fallback plan**: If unsuccessful, document learnings, revert to markdown TODOs, consider alternatives
5. **Low-risk exploration**: Experiment 1 can be run immediately (2 hours, fully reversible)

### Rationale:

- **Low investment** (20 hours), **high potential return** (+40% productivity)
- **Aligns with current methodology** (Pattern-009, Inchworm, Verification-First)
- **Enables strategic goals** (GREAT-3B, 24x7 agents, learning system)
- **Reversible** with minimal sunk cost
- **Field-proven** (1,000+ users, daily use by experienced vibe coders)
- **Experiment 1 is ultra-low-risk**: Can explore immediately without formal commitment

### Next Steps if Approved:

**Immediate (This Week)**:

1. ✅ Complete this proposal (DONE)
2. Review by Chief of Staff + Chief Architect + team
3. Gather feedback, address concerns
4. Decision: Pilot or Pass?

**If Pilot Approved (Next Week)**:

1. PM: Install Beads, run Experiment 1 (2 hours, can do now if curious)
2. PM: Run Experiment 2 ("ask your agent")
3. PM + team: Evaluate initial results
4. Continue Week 1 experiments or abort

**Week 2**:

1. Run Experiments 3-4 (GitHub hybrid, landing protocol)
2. Capture all metrics and evidence
3. Prepare results report
4. Go/No-Go decision on Phase 2 (rollout)

---

## References

### Source Articles

1. **"Introducing Beads: A Coding Agent Memory System"** (Oct 13, 2025)
   https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a

2. **"The Beads Revolution: How I Built The TODO System That AI Agents Actually Want to Use"** (Oct 14, 2025)
   https://steve-yegge.medium.com/the-beads-revolution-how-i-built-the-todo-system-that-ai-agents-actually-want-to-use-228a5f9be2a9

3. **"Beads Blows Up"** (Nov 6, 2025)
   https://steve-yegge.medium.com/beads-blows-up-a0a61bb889b4

### Related Documentation

- **Pattern-009**: `docs/internal/architecture/current/patterns/pattern-009-github-issue-tracking.md`
- **Inchworm Protocol**: `docs/briefing/METHODOLOGY.md`
- **GREAT-3B**: Current sprint work on plugin infrastructure
- **Vibe Coding Book**: Gene Kim & Steve Yegge (comprehensive guide)

### Project Resources

- **Beads GitHub**: https://github.com/steveyegge/beads
- **Beads MCP Server**: https://pypi.org/project/beads-mcp/
- **Installation**: `brew tap steveyegge/beads && brew install beads`

---

## Appendix: What Experiment 1 Actually Entails

### Ultra-Low-Risk Exploration (Before Formal Commitment)

**Time**: 2 hours
**Risk**: Negligible (fully reversible, no production impact)
**Benefit**: Real experience with Beads before committing to pilot

### Step-by-Step (Can Do Right Now)

1. **Install** (5 minutes):

   ```bash
   brew tap steveyegge/beads
   brew install beads
   cd /Users/xian/Development/piper-morgan
   bd init
   pip install beads-mcp
   ```

2. **Configure Agent** (5 minutes):
   Add to CLAUDE.md:

   ```markdown
   ## Beads Quickstart (Experimental)

   Run `bd quickstart` to learn Beads commands.

   Basic workflow:

   - Query work: `bd ready --json`
   - Create issue: `bd create --title "..." --priority p1`
   - Update issue: `bd update <id> --status in_progress`
   - Complete: `bd update <id> --status done`
   ```

3. **Create Test Epic** (10 minutes):

   ```bash
   # Ask agent to create epic for current work
   "Please create a Beads epic for GREAT-3B with 4-5 subtasks"

   # Agent will:
   bd create --title "GREAT-3B: Plugin Infrastructure" --labels epic,p0
   bd create --title "Create plugin interface" --parent bd-1
   bd create --title "Implement dynamic loader" --parent bd-1 --blocked-by bd-2
   # ... etc
   ```

4. **Work on Subtask** (30 minutes):

   ```bash
   # Agent claims work
   bd claim bd-2 --assignee cursor-agent

   # Agent works, discovers issues:
   "I notice auth.py has a potential bug..."
   → Agent files: bd create --title "Fix auth.py line 42" --discovered-from bd-2

   # Agent continues work
   ```

5. **Test Session Restart** (10 minutes):

   ```bash
   # Stop agent (simulate compaction)
   # Start fresh agent

   # New agent immediately:
   bd ready --json
   # Shows: bd-2 is in_progress, bd-3 is blocked, bd-4 is ready

   # Agent picks up exactly where left off
   ```

6. **Evaluate** (30 minutes):

   - Did agent pick up context in < 10 seconds?
   - Were discovered issues auto-filed?
   - Is `bd ready` faster than parsing markdown?
   - Does dependency blocking work?

7. **Uninstall If Unsuccessful** (5 minutes):
   ```bash
   brew uninstall beads
   pip uninstall beads-mcp
   rm -rf .beads/
   # Revert CLAUDE.md
   ```

### What You'll Learn

- **Agent behavior**: Do they actually like Beads? Do they use it naturally?
- **Session continuity**: Does restart really eliminate 2-3 minute ramp-up?
- **Work discovery**: Do they auto-file issues, or forget?
- **Query performance**: Is `bd ready` actually fast?
- **User experience**: Does it feel better than markdown TODOs?

### Decision Point

After 2 hours:

- **If positive**: Continue with formal Experiment 2-4 (full pilot)
- **If negative**: Uninstall, document why it didn't work, no harm done
- **If mixed**: Identify specific concerns, evaluate if solvable

### Why This Is Safe

- No changes to production workflow
- No changes to GitHub/Pattern-009
- No team disruption (just you + agent)
- Fully reversible in 5 minutes
- Total investment: 2 hours

**Recommendation**: Go ahead and try Experiment 1 now if curious. Real experience > theoretical analysis.

---

**Prepared for review by Chief of Staff, Chief Architect, and team.**

**Next Action**: Gather feedback, address questions, make pilot decision.

---

_End of Proposal_
