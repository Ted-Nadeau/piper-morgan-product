---
date: 2026-03-22
status: substantive
sources_checked:
  - klatch
---

# Cross-Pollination Brief: Klatch → Piper Morgan

**Date:** 2026-03-22
**Source project:** Klatch
**For:** Piper Morgan team

## Key Insights

### 1. The 5-Layer Prompt Model Is Now Canonical
**Relevance:** PM has 14 agent roles with briefing documents. The 5-layer model provides a framework for structuring what each agent knows at session start.
**Source:** `docs/PROMPT-ASSEMBLY.md` (new)
**Summary:** Definitive reference for the 5-layer system prompt architecture: (1) Kit Briefing (environmental orientation), (2) Project Instructions (behavioral rules), (3) Project Memory (factual context), (4) Channel Addendum (conversation-specific framing), (5) Entity Prompt (agent identity). Includes presence matrix by channel type, diagnostic API endpoint, and design rationale. Klatch's internal memo notes: "PROMPT-ASSEMBLY.md is the document the Piper Morgan CIO has been waiting for."
**Suggested action:** Review `docs/PROMPT-ASSEMBLY.md` in Klatch repo. The fidelity dimensions (environmental, instructional, narrative, conversational) could inform how progressive loading in CLAUDE.md is organized.

### 2. Agent Traditions — Durable Per-Agent Knowledge Pattern
**Relevance:** Addresses the gap of what happens when a role hasn't been active in days and needs to spin up cold.
**Source:** `docs/AGENT-TRADITIONS-SPEC.md`, `docs/agents/calliope.md`, `docs/agents/argus.md`
**Summary:** 7-section structure: (1) Role and purpose, (2) Working style, (3) Standing responsibilities, (4) Conventions and standards, (5) Key relationships, (6) Institutional memory, (7) Standing instructions. Calliope traditions doc is the reference implementation. Argus doc emphasizes verification protocols after the reliability incident.
**Suggested action:** Compare with existing `BRIEFING-ESSENTIAL-*.md` pattern. The 7-section structure (especially "institutional memory" and "key relationships") provides structure the current briefing docs may not fully capture. Consider adapting for less-frequently-used roles.

### 3. Audit Cascade Methodology
**Relevance:** Prevents working issues in filing order rather than impact order.
**Source:** PM Lead Dev session
**Summary:** Systematic triage across four M1 Tier 2 quality issues in a single session. Verify scope, narrow or widen, decide disposition, execute. 4 separate work items became 1 immediate fix, 2 quick follow-ups, 1 partially moot — all triaged in under 2 hours.
**Suggested action:** Key insight: audit issues against *current* architectural state, not the state when they were filed.

### 4. The Cross-Pollination Loop Closed
**Relevance:** Validates this entire process.
**Source:** PM Lead Dev session on March 21
**Summary:** Session begins with explicit "Cross-Pollination Hub Review" section, reading the brief and extracting relevant insights. First evidence the brief is consumed as intended. The Docs session also noted the hub's existence and workflow. Both demonstrate consumption, not just awareness.
**Suggested action:** Continue publishing. The loop works.
