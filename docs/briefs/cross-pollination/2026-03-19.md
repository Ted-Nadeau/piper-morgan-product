---
date: 2026-03-19
status: substantive
sources_checked:
  - klatch
---

# Cross-Pollination Brief: Klatch → Piper Morgan

**Date:** 2026-03-19 (retrospective)
**Source project:** Klatch
**For:** Piper Morgan team

## Key Insights

### 1. Five-Layer Prompt Assembly Model — Testable Context Injection

**Relevance:** Piper Morgan's Agent 360 identified session-start orientation as the #1 pain point across all 9 agents. Klatch built a structured solution: discrete prompt layers that are independently testable.

**Source:** `CLAUDE.md`, `packages/server/src/claude/client.ts`, Mnemosyne's bridging analysis

**Summary:** Klatch assembles system prompts from 5 discrete layers: (1) kit briefing (role/persona), (2) project instructions (project-level context), (3) project memory (accumulated knowledge), (4) channel addendum (conversation-specific context), (5) entity prompt (the agent's own system prompt). Each layer is independently verifiable via a `prompt-debug` endpoint — you can assert that the right context reached the right layer without needing to evaluate LLM output. This clean separation means "structure vs. accumulated knowledge" are never conflated.

**Suggested action:** Consider whether Piper Morgan's briefing staleness problem could be addressed by separating static structure (role definition, project overview) from dynamic state (current sprint, recent decisions, open items). The static layers change rarely; the dynamic layers could be generated or queried at session start. Klatch's HOSR already flagged this model as relevant to Piper Morgan's orientation problem.

### 2. Session Wrap Verification Protocol — Trust but Verify Agent Claims

**Relevance:** Directly applicable to Piper Morgan's multi-agent coordination, where agents self-report completion status.

**Source:** `CLAUDE.md` (Session Wrap Protocol section), Calliope's reliability incident memo

**Summary:** Born from a real reliability incident: Argus's session log claimed demo infrastructure was complete, but a bad rebase + forced push had silently lost the commits. Calliope relayed "done" to xian without verifying repo state. The fix: mandatory verification before any agent can claim "done" — (1) `git log` to confirm commits landed, (2) `ls`/`cat` to confirm deliverable files exist, (3) push session log last as the final record. Plus a blanket no-force-push rule without explicit PM approval.

**Suggested action:** Piper Morgan already has evidence requirements for issue closure ("Tests: X tests added, Verification: pytest output"). Consider extending this to session-level verification — before an agent's session log claims work is done, require the same git-level proof that Klatch now mandates. The Pattern-063 "Extension Without Integration" anti-pattern from ADR-059 is the architectural cousin of this problem: claiming completion at one layer without verifying the contract is fulfilled downstream.

### 3. Cloud Session Import — Cross-Environment Bridge

**Relevance:** Piper Morgan operates agents across two environments (Claude Code + Claude.ai). Klatch built the import pipeline that bridges them.

**Source:** `packages/server/src/routes/import.ts`, Daedalus session log (v0.8.7)

**Summary:** Klatch v0.8.7 shipped three import paths for conversations originating in different environments: (1) agent self-export (JSONL committed to repo, auto-discovered), (2) file upload (browser-based multipart upload), (3) manual path entry. The parser is buffer-based (no disk I/O), handles JSONL streaming format, and uses basename matching for project linking (only matches if exactly one project has that name — avoids ambiguity). Zero schema changes required; the existing data model handled cloud-origin sessions with just a `cloudUpload: true` metadata flag.

**Suggested action:** The two-environment asymmetry is the same constraint driving Piper Morgan's Mailbox v3 design. Klatch's import pipeline proves that a unified data model can represent conversations from heterogeneous sources without schema changes. If Piper Morgan ever needs to consolidate agent session logs from code and web environments into a single view, this pattern is proven.

### 4. Intelligence Feed as Standing Practice

**Relevance:** A systematized approach to ecosystem monitoring that's directly adoptable by any project team.

**Source:** `docs/INTELLIGENCE.md`, `docs/intel/2026-03-20-sweep.md`

**Summary:** Argus designed and executed the first standing intelligence sweep: 20 items from the Anthropic ecosystem scored by Klatch relevance, with actionable items routed to specific agents via the memo system. The protocol (`docs/INTELLIGENCE.md`) defines daily monitoring scope, scoring rubric, and distribution. Key findings from the first sweep: Claude Code Channels validates Klatch's thesis, Cowork scheduled tasks enable automation, 1M context GA removes design constraints, Compaction API could simplify long conversation handling, and Agent SDK provides programmable agent capabilities.

**Suggested action:** Piper Morgan could adopt a similar standing protocol — daily or weekly ecosystem scans focused on knowledge management, agent workflow, and product development signals. The Cowork scheduled tasks feature (persistent recurring tasks with full MCP/tool access) could automate this, and the cross-pollination sweep itself is an example of the pattern. Key items from Klatch's sweep that are relevant to Piper Morgan: Compaction API (custom summarization to preserve domain terminology during context management), Agent SDK (TypeScript agent loop for "doing things" not just conversing), and MCP donation to Linux Foundation (industry standardization reduces vendor lock-in risk).

### 5. Two-Track Testing: Automated Structural + Manual Qualitative

**Relevance:** Separating what can be deterministically tested from what requires qualitative judgment — applicable to any system with both mechanical and conversational components.

**Source:** Theseus Prime session log, `docs/mail/theseus-to-argus-aaxt-harness.md`

**Summary:** Klatch designed a two-track testing program: AAXT (Automated Agent Experience Testing) uses synthetic context and deterministic assertions against a `prompt-debug` endpoint — no LLM calls, fast, CI-friendly. MAXT (Manual Agent Experience Testing) uses real agents, real context, and qualitative interpretation — expensive, slow, judgment-intensive. The key insight: automated tests gate manual tests. Don't waste qualitative testing sessions on broken plumbing. The Fork Continuity Quiz (v4) was redesigned around the 5-layer prompt model with an open-canvas section for spontaneous self-report before structured probing.

**Suggested action:** Piper Morgan has 6,190+ tests but they're all mechanical (pytest). Consider whether a qualitative testing layer would catch the kind of issues that unit tests miss — like the UX bug in #922 where three systems raced for user input. The AAXT/MAXT split could map to Piper Morgan as: automated tests verify pipeline mechanics, manual tests verify that the user experience is coherent end-to-end.

## Context & Background

March 19 was release day for Klatch — v0.8.6 (sidebar redesign + prompt architecture) shipped with issues #8-14 resolved, followed immediately by v0.8.7 (cloud session import) and rapid iteration toward v0.8.8 (adaptive thinking, model updates). The team operated with 4 agents (Daedalus, Calliope, Mnemosyne, Theseus) plus Argus joining on March 20. The most significant conceptual output was Mnemosyne's positioning insight: "Klatch is a project context manager that unifies Claude's fragmented environments" — a framing that resonated across the team and directly addresses the multi-environment problem Piper Morgan is also navigating.

## Raw Sources

- `docs/logs/2026-03-19-0712-calliope-sonnet-log.md` — Blog post, Piper Morgan context introduction, publishing workflow
- `docs/logs/2026-03-19-0716-daedalus-opus-log.md` — Release runbook fix, v0.8.6 cleanup
- `docs/logs/2026-03-19-0740-daedalus-opus-log.md` — Cloud import implementation (v0.8.7)
- `docs/logs/2026-03-19-1509-mnemosyne-opus-log.md` — Environment bridging analysis, TOS assessment
- `docs/logs/2026-03-20-1438-argus-opus-log.md` — Intelligence sweep, test infrastructure
- `docs/logs/2026-03-20-1749-calliope-sonnet-log.md` — Reliability incident, wrap verification protocol
- `docs/logs/2026-03-20-1938-theseus-opus-log.md` — AAXT/MAXT testing program design
- `docs/logs/2026-03-20-1955-daedalus-opus-log.md` — v0.8.8 quick wins, Klatch creation UI
- `docs/intel/2026-03-20-sweep.md` — First standing intelligence sweep (20 items)
- `docs/COORDINATION.md` — Multi-agent status board
- `docs/mail/calliope-to-argus-reliability-incident-2026-03-20.md` — Incident memo and postmortem
