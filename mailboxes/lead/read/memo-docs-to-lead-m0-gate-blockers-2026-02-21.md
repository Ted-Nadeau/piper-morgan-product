# Memo: M0 Sprint Gate Blockers — 4 Issues Remaining

**From**: Documentation Management Specialist (via PM)
**To**: Lead Developer
**Date**: February 21, 2026
**Re**: Issues blocking M0 gate approval (#779)
**Priority**: High — PM wants to close M0 gate this weekend

---

## Summary

The M0 Conversational Glue sprint is at **78% completion** (18/23 issues done). Four issues remain before PM can approve gate #779.

---

## Blocking Issues

| Issue | Title | Type | Notes |
|-------|-------|------|-------|
| **#813** | Bug: test_get_conversation_summary fails — coroutine mock issue | Bug | Test failure blocking CI |
| **#814** | Explicit setup requests should trigger interactive onboarding | Feature | User says "help me set up" → should start wizard |
| **#818** | Architect note: entity tokens in response templates | Docs/Code | **UNBLOCKED** — guidance added to implementation guide (see separate memo) |
| **#823** | Formality/warmth system not unified across features | Architecture | Architect memo pending PM decision |

---

## Issue Details

### #813 — Test Failure (Bug)
`test_get_conversation_summary` fails due to coroutine mock issue. This is a test infrastructure problem, not a feature bug. Should be quick to fix.

### #814 — Interactive Onboarding Trigger (Feature)
When user explicitly says "help me set up Slack" or similar, Piper should trigger the interactive setup wizard rather than giving static guidance. This connects the conversational layer to the existing setup wizard.

### #818 — Entity Tokens (Docs/Code)
The Architect clarified that echoing entity names (e.g., "I couldn't find 'Q3 Roadmap'") is acceptable and should NOT be flagged as parrot behavior. I've added section 5.8 to the Conversational Glue Implementation Guide with this guidance.

**Action needed**: Review whether any code changes are needed, or if documentation alone closes this issue.

### #823 — Unified Formality System (Architecture)
The Architect proposed unifying the formality/warmth system. This may need PM decision on scope — could be a quick wiring fix or a larger refactor. Check the Architect memo for details.

---

## Recommended Priority

1. **#813** (test fix) — Quick win, unblocks CI
2. **#818** (entity tokens) — May be closeable with docs-only if no code changes needed
3. **#814** (onboarding trigger) — Feature work but well-scoped
4. **#823** (formality system) — Check with PM on scope

---

## Gate Closure

Once these 4 issues are Done, PM can approve #779 (M0-GLUE Sprint Completion Gate) and we can formally close the M0 sprint.

---

*Docs Agent, on behalf of PM*
