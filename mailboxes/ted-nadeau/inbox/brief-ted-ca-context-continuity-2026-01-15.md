# Brief: Context Continuity Tooling Proposal

**To**: Ted Nadeau (Architecture Advisor), Chief Architect
**From**: xian (CEO), Chief Innovation Officer
**Date**: January 15, 2026
**Re**: Automating agent context continuity as first tooling priority

---

## Background

Steve Yegge recently published details on "Gas Town," his multi-agent orchestration system. While we differ philosophically on throughput vs. quality optimization, several of Gas Town's mechanisms address problems we share.

The most compelling: **persistent agent identity with explicit state that survives sessions**.

We're not proposing to build Gas Town. We are proposing to gradually automate the manual coordination work that currently happens between xian and our AI agents. Context continuity is our nomination for where to start.

---

## The Problem We're Solving

### Current State: Human-Mediated Continuity

When an agent session ends (context exhaustion, handoff, interruption), continuity currently requires xian to:

1. **Download and preserve session logs** — manual file management
2. **Upload relevant context to new session** — copy/paste or file upload
3. **Explain "where we left off"** — natural language recap
4. **Re-establish working state** — the new agent rebuilds mental model from provided context

This works, but creates bottlenecks:
- xian's time becomes the limiting factor
- Context can be lost in the translation
- Agents must re-derive conclusions from evidence rather than inheriting state
- No machine-readable continuity between sessions

### Gas Town's Solution: GUPP (Gastown Universal Propulsion Principle)

Yegge's system treats agent identity as persistent data:
- Agent = a Bead (Git-backed data object), not a session
- Sessions are "cattle" (ephemeral); agents have durable identity
- Each agent has a "hook" where pending work lives
- New sessions automatically check their hook and continue

**GUPP**: "If there is work on your hook, YOU MUST RUN IT."

This creates automatic continuity. When an agent crashes or compacts, a new session picks up the hook and continues.

### What We'd Want (Different Emphasis)

We don't need Gas Town's throughput-focused chaos tolerance ("fish fall out of the barrel"). We need **reliable context transfer** that maintains our verification-first methodology.

A Piper-appropriate version might look like:

| Gas Town | Piper Morgan |
|----------|--------------|
| Hook = pending work | Context file = state + work + evidence |
| Sessions are cattle | Sessions are documented transitions |
| Automatic GUPP nudge | Structured handoff with verification |
| Nondeterministic idempotence | Completion discipline preserved |

---

## What We'd Automate

### Phase 1: Context Packaging (Low Complexity)

**Current**: xian manually downloads logs, uploads to new session, explains state.

**Automated**:
- Script captures session log at handoff
- Generates structured context file (role, current work, key decisions, blocking issues)
- Places in standardized location for next session

**Benefit**: Reduces manual overhead; creates consistent context format.

### Phase 2: Context Loading (Medium Complexity)

**Current**: New agent receives uploaded files, must parse and understand.

**Automated**:
- New session automatically receives predecessor's context file
- Structured format allows parsing, not just reading
- Agent can query: "What was I working on? What decisions were made? What's blocked?"

**Benefit**: Faster agent spin-up; less re-derivation work.

### Phase 3: Continuity Verification (Higher Complexity)

**Current**: xian judges whether new agent has "picked up" context correctly.

**Automated**:
- New session produces "context acknowledgment" summary
- Human reviews acknowledgment before work proceeds
- Discrepancies flagged for correction

**Benefit**: Verification without human having to re-explain; catch continuity failures early.

### Phase 4: Identity Persistence (Gas Town-Adjacent)

**Current**: Agents have role definitions (briefings) but not explicit state objects.

**Automated**:
- Each role has a persistent state file (like Gas Town's agent Beads)
- State includes: current work, recent decisions, pending items, last session summary
- State survives across sessions; sessions update state as they work

**Benefit**: Agents truly "remember" across sessions; xian can step away.

---

## Why Start Here

### Established Cowpath

Context continuity is a mature part of our organic process. We've been doing it manually for months. The pattern is stable—we're paving an existing path, not blazing a new one.

### High Leverage

xian's time is currently the bottleneck. Every session transition requires human mediation. Automating this would directly increase team capacity.

### Well-Defined Scope

Unlike broader automation ambitions, context continuity has clear inputs (session logs, role state), outputs (context files, acknowledgments), and success criteria (agent picks up correctly).

### Methodology-Compatible

This automation doesn't require adopting Yegge's "vibe coding" philosophy. We can maintain verification-first principles while reducing coordination overhead. The tooling would encode our completion discipline, not bypass it.

---

## Questions for Ted + Chief Architect

### Technical Feasibility

1. What's the simplest version of Phase 1 (context packaging)?
2. How would structured context files interact with our existing briefing document approach?
3. Is there overlap with existing session log or omnibus infrastructure?

### Architectural Fit

4. Does this align with the persistent context architecture (ADR-024)?
5. How would this interact with Piper's own session management (for when Piper is the product, not the dev environment)?
6. Is there reusable infrastructure here, or is this dev-environment-only tooling?

### Sequencing

7. What's a reasonable timeline for Phase 1?
8. What would block or accelerate this work?
9. Should this be a dedicated workstream or embedded in existing engineering work?

---

## Proposed Next Steps

1. **Ted + Chief Architect review this brief**
2. **xian facilitates planning conversation** (async or sync)
3. **Feasibility assessment** (what's trivial, what's hard, what's blocked)
4. **Scope decision** (how much of Phase 1-4 to attempt)
5. **Issue creation** (when scope is clear)

No rush. We're proposing this as a direction, not demanding immediate action.

---

*Context: This brief originated from CIO analysis of Steve Yegge's Gas Town article, identifying mechanisms worth adapting without adopting the underlying philosophy.*

— xian + CIO
