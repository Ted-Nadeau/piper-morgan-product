# Memo: ADR-049 and ADR-050 Implementation Guidance Request

**From**: Lead Developer (Claude Code Opus)
**To**: PPM, Chief Architect
**Date**: January 25, 2026, 9:25 PM
**Re**: Pending ADR Approvals and Implementation Roadmap for Conversation Architecture

---

## Executive Summary

During completion of #427 MUX-IMPLEMENT-CONVERSE-MODEL, I discovered that two critical ADRs remain in limbo:

1. **ADR-049** (Two-Tier Intent Architecture) - Still "Proposed" since January 9
2. **ADR-050** (Conversation-as-Graph Model) - Accepted but Phases 1-3 have no tracking issues

Both are required for #427's remaining acceptance criteria. I've created tracking issues (#687, #688) but need guidance on prioritization and implementation approach.

---

## ADR-049: Conversational State and Hierarchical Intent

### Current State
- **Status**: Proposed (pending PM review)
- **Date**: January 9, 2026
- **Origin**: Discovered during #490 FTUX-PORTFOLIO implementation

### The Problem It Solves
When a user starts a guided process (onboarding, standup):
1. User says "Hello" → Piper triggers onboarding
2. User says "My project is Piper Morgan" → Gets re-classified as IDENTITY intent, derails onboarding

The ADR proposes checking for active conversational processes BEFORE running intent classification.

### What Exists Today
- PortfolioOnboardingManager singleton pattern (implemented for #490)
- The pattern works but is NOT generalized into the main intent flow

### Questions for Guidance

1. **Approval**: Should ADR-049 be approved? Are there concerns with the proposed approach?

2. **Scope**: Should we generalize the pattern to cover:
   - Portfolio onboarding (exists)
   - Standup sessions
   - Planning sessions
   - Feedback sessions
   - Pending clarifications

3. **Priority**: Where does this fit relative to current MUX-IMPLEMENT work? Is it:
   - P0 (blocks alpha testing)
   - P1 (next sprint)
   - P2 (future roadmap)

4. **Alternative approaches**: The ADR rejected "better classification" in favor of architectural priority. Is this still the right call?

---

## ADR-050: Conversation-as-Graph Model

### Current State
- **Status**: Accepted (January 21, 2026)
- **Phase 0**: ✅ Complete - Schema designed (#601, #602)
- **Phases 1-3**: No tracking issues existed until tonight

### The Three Phases

| Phase | Scope | Status |
|-------|-------|--------|
| Phase 0 | Schema design | ✅ Complete |
| Phase 1 | Participant Mode - `parent_id` threading, `ConversationLink` table | Not started |
| Phase 2 | Host Mode - Full `ConversationNode`, multiple views | Not started |
| Phase 3 | Personal Agents - `WhisperNode`, per-participant context | Not started |

### What It Enables
- Reference resolution: "that meeting" → resolves to previously mentioned meeting
- Thread structure in Slack integration
- Multiple view projections (timeline, tasks, decisions, questions)
- Foundation for multi-party conversations (Ted Nadeau's MultiChat vision)

### Questions for Guidance

1. **Phase 1 timing**: The Alembic migration is designed but not applied. When should we apply it?

2. **Incremental vs. big-bang**: Should we:
   - Apply Phase 1 migration now and iterate?
   - Wait until we have full Phase 1-3 implementation plan?

3. **Relationship to PDR-101**: ADR-050 references PDR-101 (Multi-Entity Conversation Support). Is PDR-101 still the governing roadmap?

4. **Ted Nadeau's POC**: The TypeScript reference implementation exists at `external/ted-multichat/poc/`. Should we schedule time to extract patterns, or is this lower priority than other MUX work?

---

## Context: #427 Acceptance Criteria

#427 MUX-IMPLEMENT-CONVERSE-MODEL had 4 acceptance criteria:

| Criterion | Status | Dependency |
|-----------|--------|------------|
| Multi-intent parsing ("Hi Piper! What's on my agenda?") | ✅ Complete | - |
| Temporal follow-ups ("How about today?") | ✅ Complete | - |
| Active process not derailed | ⬜ Blocked | ADR-049 (#687) |
| Reference resolution ("that meeting") | ⬜ Blocked | ADR-050 Phase 1+ (#688) |

**My recommendation**: Close #427 with 2/4 criteria met, since remaining criteria have explicit architectural dependencies that are tracked separately.

---

## Tracking Issues Created

| Issue | Description |
|-------|-------------|
| **#687** | DEFERRED-#427: ADR-049 Two-Tier Intent Architecture Implementation |
| **#688** | DEFERRED-#427: ADR-050 Conversation Graph Phase 1-3 Implementation |

These capture full context, acceptance criteria, and dependencies.

---

## Requested Actions

1. **ADR-049**: Review and approve/reject/revise
2. **ADR-050 Phases 1-3**: Confirm priority and timing
3. **#427**: Confirm closure with 2/4 criteria (remaining tracked in #687, #688)
4. **Roadmap placement**: Where do #687 and #688 fit in the inchworm?

---

## Session Context

This memo follows an intensive session completing the MUX-IMPLEMENT sprint:
- **#425** MUX-IMPLEMENT-MEMORY-SYNC ✅
- **#426** MUX-IMPLEMENT-CONSISTENT ✅
- **#427** MUX-IMPLEMENT-CONVERSE-MODEL (Phases 1-2 ✅, Phase 3 deferred)

The P3 sprint of MUX-IMPLEMENT is substantially complete. The deferred work represents deeper architectural investment that may belong in a future phase.

---

*Memo prepared by Lead Developer during session 2026-01-25-0718*
