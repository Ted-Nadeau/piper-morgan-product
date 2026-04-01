# Special Assignment: History Sidebar Design Archaeology

**From**: Principal Product Manager
**To**: Special Assignments Agent
**Date**: February 1, 2026
**Priority**: Medium (informs upcoming MVP planning)
**Deliverable**: Design Intent Report

---

## Assignment Overview

We have two sidebar features in the web interface:
1. **Left sidebar**: Conversation list with date grouping (working)
2. **Right History sidebar** (#425/#735): Search, date grouping, privacy toggle (recently mounted)

PM observation: "the tab for opening and closing the chat history sidebar works just fine" — which raises the question of whether these are duplicate functionality or serve distinct purposes.

**Your mission**: Conduct archaeological research to surface the original design intent, trace execution through MUX sprints, identify any flattening or gaps, and produce a report that informs MVP planning.

---

## Research Questions

### 1. Design Intent (What Was Intended?)

- What was the **original design vision** for the right History sidebar?
- How does it differ conceptually from the left conversation list?
- Was there MUX design deliberation about screen real estate allocation?
- Does the MUX grammar ("Entities experience Moments in Places") inform sidebar purpose?

**Hypothesis to test**: PM intuition is that the right sidebar may be intended for **emergent entity surfacing** (objects moving through lifecycle stages) rather than simple conversation navigation. Is there evidence for or against this?

### 2. Execution Trace (What Was Built?)

Trace these issues through implementation:
- **#425**: History Sidebar (original issue)
- **#565**: Conversation History Sidebar (Jan 10 implementation)
- **#574**: Conversation history panel switching (bug fix)
- **#729, #732, #735**: Recent History button fixes

For each, extract:
- Original issue description and acceptance criteria
- Implementation decisions made
- Any scope changes or cuts during execution

### 3. MUX Design Documentation

Search for and review:
- MUX-INTERACT sprint documentation
- Any design sketches or wireframes mentioning sidebars
- ADR-054 (Cross-Session Memory Architecture) — does it reference sidebar UI?
- CXO session logs from MUX design work (late 2025)
- Object model docs mentioning UI surface areas

### 4. Gap Analysis

Identify:
- **Flattening**: Where did rich design concepts get reduced to simpler implementations?
- **Incomplete alignment**: Where does current implementation diverge from stated intent?
- **Undocumented decisions**: What got built without clear rationale?
- **Missing pieces**: What was intended but never implemented?

---

## Deliverable Format

Please produce a report with these sections:

### A. Design Intent Summary
What the sidebars were *supposed* to do, with evidence citations.

### B. Implementation Reality
What was actually built, with issue/commit references.

### C. Gap Matrix

| Aspect | Intended | Built | Gap |
|--------|----------|-------|-----|
| Left sidebar purpose | ? | ? | ? |
| Right sidebar purpose | ? | ? | ? |
| Relationship between them | ? | ? | ? |
| Emergent entity surfacing | ? | ? | ? |
| Lifecycle visibility | ? | ? | ? |

### D. Design Questions for CXO

Questions that emerged from research requiring design input.

### E. Implications for MVP Planning

How findings affect upcoming MVP sprint planning.

---

## Source Locations

Start your search in:
- `/docs/internal/architecture/current/adrs/` — ADR-054, ADR-055
- `/docs/internal/development/` — MUX implementation guides
- GitHub issues #425, #565, #574, #729, #732, #735
- MUX-INTERACT sprint issues
- CXO session logs (search for "sidebar", "history", "panel")
- Original MUX sketches (if accessible)

---

## Context for This Assignment

This research feeds into MVP planning. We need to determine whether:
- **Option A**: Right sidebar is redundant → deprecate or merge
- **Option B**: Right sidebar has distinct purpose → document and align UI affordances
- **Option C**: Right sidebar was placeholder for emergent entity surface → redesign with intent

The PM, PPM, and CXO will convene after receiving your report to make intentional design choices about screen real estate and user mental model.

---

## Timeline

- **Requested by**: February 3, 2026 (before MVP planning sessions)
- **Estimated effort**: 2-3 hours

---

*Filed by PPM, February 1, 2026*
