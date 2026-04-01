# Memo: UX Guidance Needed — Guided Workflow "Hijack" Pattern

**From**: Lead Developer (via PM)
**To**: CXO, PPM
**Date**: 2026-03-12
**Re**: Issues #888, #889 — Onboarding and Standup workflow session capture
**Priority**: Blocking M1 sprint progress

---

## The Problem

During M1 canonical testing (#884), we discovered that two guided workflows — **Onboarding** and **Standup** — capture the user's conversation session and never release it. Once either workflow activates, ALL subsequent user messages are routed to that workflow regardless of what the user says.

**Example**: If a user triggers standup (`/standup`), then asks "What's on my calendar?" — the calendar question gets swallowed by the standup handler instead of reaching the intent classifier.

This is the same root cause in both cases: the `ProcessRegistry` checks for active workflows before classification, and active workflows always claim messages.

## What We Need From You

The engineering fix is straightforward (add escape/release mechanisms to ProcessRegistry). But the **user experience** requires design decisions:

### 1. Escape Mechanism — How should users exit a workflow?

Options to consider:
- **Explicit command**: User says "exit", "cancel", "stop", or "skip"
- **Intent detection**: System detects off-topic messages and offers to pause/exit
- **Auto-timeout**: Workflow expires after N turns of no progress or N minutes of inactivity
- **Combination**: Timeout + explicit command + off-topic detection

### 2. Re-entry — What happens after escape?

- Does the workflow remember progress and offer to resume later?
- Does it start fresh next time?
- Should there be a visual indicator that a workflow is paused?

### 3. Activation — Should workflows require explicit invocation?

Currently onboarding auto-activates for new users. Should it?
- **Auto-activate**: Onboarding starts on first interaction (current behavior)
- **Offer-first**: "I see you're new! Want me to walk you through setup?" (user opts in)
- **On-demand only**: User must explicitly start onboarding

### 4. Standup Scope — When does standup end?

- After all three questions (yesterday/today/blockers)?
- When the user says "done" or "that's it"?
- Should partial standups be saved if interrupted?

## Impact

These two issues account for **8 of the remaining test failures** in the canonical retest. They also represent the most visible user-facing bugs — a user who can't escape onboarding will have a terrible first impression.

## Engineering Timeline

Once we have design direction, implementation is estimated at 1-2 days. The ProcessRegistry changes are well-scoped and the test infrastructure is already in place.

---

*Please reply to PM mailbox or comment on GitHub issues #888 / #889 with your guidance.*
