# Memo: What We Could Learn From Gas Town

**To**: xian (CEO)
**From**: Chief Innovation Officer
**Date**: January 15, 2026
**Re**: Mechanisms worth adapting from Yegge's orchestration system (without adopting the philosophy)

---

## Overview

Steve Yegge's Gas Town article describes an orchestration system for running 20-30 Claude Code instances simultaneously. His philosophy prioritizes throughput over quality ("fish fall out of the barrel, more fish will come"), which conflicts directly with our verification-first methodology.

However, several of his mechanisms solve problems we share. This memo identifies what's worth adapting vs. what conflicts with our approach.

---

## Philosophy Conflict (Why We Can't Just Adopt Gas Town)

| Gas Town | Piper Morgan |
|----------|--------------|
| "Vibe coding" — never looks at code | Verification-first, evidence-based |
| Fish fall out of barrel, more come | Completion discipline, no work lost |
| Speed/throughput optimized | Quality/cathedral optimized |
| "Some bugs get fixed 2-3 times" | Pattern-045 says this IS the problem |
| 100% vibe coded | Jan 9 showed 7-layer bug chain from insufficient verification |

Yegge explicitly says: "Work in Gas Town can be chaotic and sloppy... You might not be 100% efficient, but you are flying."

This is the **inverse** of our philosophy. We cannot adopt Gas Town wholesale. But we can learn from his solutions to shared problems.

---

## High-Value Mechanisms

### 1. Persistent Agent Identity with Explicit State
**Severity of Gap**: Medium-High

**What Yegge Does**:
- Agent = a Bead (Git-backed data object), not a session
- Sessions are "cattle" (ephemeral); agents have durable identity
- Agent state includes: role, history, current work hook, administrative metadata
- State survives crashes, compactions, restarts

**What We Currently Have**:
- Role definitions (briefings) that describe who an agent is
- Session logs that document what happened
- No first-class state object that persists across sessions

**The Gap**:
Our agents have identity through briefings, but not explicit state tracking. When a session ends, the next agent must re-derive state from logs rather than inheriting it.

**Potential Adaptation**:
Create role-specific state files that track:
- Current work assignment
- Key decisions since last handoff
- Pending items
- Last session summary
- Status flags (blocked, waiting, active)

*Note: This is covered in the Context Continuity brief (Task 3).*

---

### 2. Molecules/Formulas as Workflow Representation
**Severity of Gap**: Medium

**What Yegge Does**:
- Molecules = workflows expressed as chains of Beads (issues)
- Protomolecules = templates for molecules
- Formulas = source form (TOML) that "cooks" into protomolecules
- Workflows are durable because they're Git-backed data, not instructions

**What We Currently Have**:
- Methodology documents that describe how to work
- Issue templates that provide structure
- No formal workflow representation that agents "walk through"

**The Gap**:
Our workflows exist as documentation that agents interpret. Yegge's exist as data structures that agents traverse.

**Potential Adaptation**:
Could our key workflows be expressed as molecules?

| Workflow | Molecule Potential |
|----------|-------------------|
| Inchworm Protocol | Could be a molecule with gates between phases |
| Release Process | Already somewhat procedural; good candidate |
| Pattern Sweep | Steps could be beads in a chain |
| Epic completion | Work items already in GitHub; could formalize dependencies |

**The Question**:
Would formalizing workflows as traversable structures help, or would it add bureaucracy without benefit?

**Recommendation**: Worth a small experiment. Pick one workflow (release process is cleanest), express it as a molecule-like structure, see if it improves agent execution. If yes, consider broader application.

---

### 3. Wisps (Ephemeral Orchestration Data)
**Severity of Gap**: Low-Medium

**What Yegge Does**:
- Wisps = ephemeral Beads that aren't persisted to Git
- Used for high-velocity orchestration (patrols, swarm coordination)
- "Burned" at end of run; optionally squashed into summary
- Distinguishes "needs permanent record" from "transient orchestration noise"

**What We Currently Have**:
- Everything goes in session logs
- All logs become part of institutional memory
- No distinction between durable insights and ephemeral coordination

**The Gap**:
Our logs can get cluttered with orchestration details that don't need permanent preservation.

**Potential Adaptation**:
Could distinguish:
- **Durable**: Decisions, insights, completed work, patterns observed
- **Ephemeral**: Coordination mechanics, tool invocations, status checks

**Practical Implementation**:
- Session logs already summarize; maybe that's sufficient
- Omnibus synthesis already compresses; maybe that handles it
- Or: explicit "ephemeral notes" section that gets dropped in synthesis

**Recommendation**: Lower priority. Our current summarization + omnibus synthesis may already solve this adequately. Monitor for log bloat before investing.

---

### 4. The "Hook" Mechanism for Continuity
**Severity of Gap**: Medium-High

**What Yegge Does**:
- Every agent has a "hook" where work is hung
- GUPP: "If there is work on your hook, YOU MUST RUN IT"
- New sessions automatically check hook and continue
- Creates automatic continuity across session boundaries

**What We Currently Have**:
- Human-mediated continuity (xian explains "where we left off")
- No automatic work resumption
- Context must be re-established each session

**The Gap**:
Same as #1 (persistent agent identity). The hook is part of the state that persists.

**Potential Adaptation**:
*Covered in Context Continuity brief (Task 3).*

**The Dreaming Connection**:
The hook mechanism could also inform Piper's learning architecture. If Piper has a "learning hook" with pending composting work, it processes that on idle cycles—similar concept to GUPP but for learning rather than task execution.

---

### 5. The "Is It Done?" Framing
**Severity of Gap**: None (we already do this)

**What Yegge Does**:
Reframes orchestration comparison:
- Kubernetes asks "Is it running?" (uptime)
- Gas Town asks "Is it done?" (completion)

**What We Already Have**:
This is exactly our verification-first philosophy. Pattern-045/046/047 are about ensuring work is actually done, not just apparently done.

**Value**:
No adaptation needed. But the framing is good for our articulation work—we should steal this language when explaining our methodology.

---

## Lower-Priority Items (Worth Noting, Not Acting On)

### Convoys
What it is: Work-order system that packages tasks into trackable delivery units.
Why deprioritize: We have GitHub issues and epics. Similar enough. Not a gap.

### Deacon Patrol Pattern
What it is: Daemon agent that runs maintenance loops with exponential backoff.
Why deprioritize: Interesting for fully autonomous systems. We're human-orchestrated by design.

### Dogs as Helpers
What it is: Helper agents that handle grungy work for patrol agents.
Why deprioritize: We use subagents similarly. Not a gap.

---

## Summary Recommendations

| Mechanism | Priority | Action |
|-----------|----------|--------|
| Persistent agent identity | **High** | Pursue via Context Continuity brief |
| Hook mechanism | **High** | Same (part of identity) |
| Molecules/Formulas | **Medium** | Small experiment: molecule-ify release process |
| Wisps | **Low** | Monitor for need; current summarization may suffice |
| "Is it done?" framing | **None** | Already doing; use language in articulation |

---

## Connection to Other Initiatives

- **Context Continuity Brief** (Task 3): Addresses #1 and #4 directly
- **Methodology Articulation** (Task 2): Can use #5 framing; molecules concept might inform visual representation
- **Unihemispheric Dreaming** (from Jan 11): Hook mechanism could inform learning cycle triggers

---

*This analysis extracted mechanisms worth adapting while explicitly rejecting the throughput-over-quality philosophy that underlies Gas Town.*

— CIO
