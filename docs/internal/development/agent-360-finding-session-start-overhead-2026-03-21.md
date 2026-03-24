# Agent 360 Finding: Session-Start Orientation Overhead

**Documented by**: HOSR
**Date**: March 21, 2026
**Source**: Agent 360 responses (9 roles, March 19, 2026)

---

## The Problem

Every role reported spending 5-15 minutes at session start figuring out "what happened since I was last here." This overhead compounds across the 10+ agent roles and reduces productive work time.

## What Agents Need at Session Start

| Category | Description | Roles Citing |
|----------|-------------|--------------|
| **Delta** | Events since last session, memos waiting, decisions made | All 9 |
| **State** | Current sprint status, pass rates, blockers, release version | CXO, PPM, Lead Dev, Architect, CoS |
| **Role-specific** | Open items, publication status, pending reviews, mailbox contents | Comms, CIO, CoS, CXO |

## Current Mechanisms and Their Limits

| Mechanism | Good For | Bad For |
|-----------|----------|---------|
| Briefings | Stable role context | "What's happening now" — goes stale within weeks |
| BRIEFING-CURRENT-STATE | Sprint position, metrics | Also goes stale; indirection helps but doesn't solve |
| Omnibus logs | Comprehensive record | Requires reading 1-7 days of material; high context cost |
| Handoff memos | Excellent orientation | One-time snapshot; stale within hours of fast-moving work |
| PM verbal briefing | Works | Consumes PM attention; not systematized |

## Agent-Proposed Solutions

| Solution | Proposed By | Complexity |
|----------|-------------|------------|
| "Here's what you missed" summary at session start | CIO (Hooks Phase 1.5) | Medium |
| "Project pulse" — single always-current page | CoS | Low-Medium |
| Live test results / canonical pass rate access | CXO, PPM, Lead Dev | Low (tooling) |
| Self-serve editorial calendar | Comms | Low (infrastructure) |
| Persistent open-items tracker | CIO, CoS | Low |
| Session-start checklist with human network scan | HOSR | Low |

## Connection to Klatch Five-Layer Model

Klatch is developing a systematic approach to context injection with a five-layer prompt architecture. The pace-layering analogy applies:

- **Slow context**: Role definition, methodology, project philosophy — changes rarely
- **Fast context**: What happened yesterday, what's blocking now, what memos are waiting — changes daily

The briefing system handles slow context reasonably well. Fast context is where we're losing time.

**Cross-pollination opportunity**: Request Calliope (Klatch Comms) write up the five-layer model for Piper team evaluation.

## Recommended Next Steps

1. **Near-term**: Create persistent open-items tracker (CoS can maintain)
2. **Near-term**: Add live test pass rate to BRIEFING-CURRENT-STATE or make queryable
3. **Medium-term**: Evaluate "project pulse" concept — single page with sprint status, open items, metrics, blockers
4. **Medium-term**: Evaluate Klatch five-layer model for adaptation to briefing architecture

---

*Agent 360 Synthesis — Session-Start Orientation*
