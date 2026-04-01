# CANONICAL-REMINDERS: Basic Reminder System

**Labels**: `enhancement`, `M1`, `canonical-queries`
**Priority**: P3 — Natural PM workflow with zero current coverage
**Discovered**: #884 Run 4, 2026-03-12
**Source**: CXO failure gap analysis

---

## Problem

"Remind me to X" (Q32) is a natural PM workflow with no implementation and no roadmap coverage. The query currently gets a graceful fallback, but reminders are a core expectation for any assistant-style product. Users who say "remind me to check in with the team tomorrow" expect something to happen.

## Affected Queries

| Query # | Input | Current Status |
|---------|-------|---------------|
| Q32 | "Remind me to review PRs tomorrow" | ❌ NOT_IMPL (graceful fallback) |

## Scope Options

**Minimum viable (recommended for M3):**
- User says "remind me to X" → Piper creates a todo with a time annotation
- At session start on the relevant day, Piper surfaces it: "You asked me to remind you to review PRs today"
- Leverages existing todo infrastructure + cross-session greeting logic

**Full implementation (M5+):**
- Time-based triggers (push notification, Slack ping)
- Recurring reminders
- Snooze/dismiss

## Acceptance Criteria (Minimum Viable)

- [ ] "Remind me to X" creates a time-annotated todo
- [ ] Reminder surfaces at next relevant session start
- [ ] User can see pending reminders ("show my reminders" or included in todo list)
- [ ] Graceful handling when time reference is ambiguous ("later" vs. "tomorrow at 3pm")

## Dependencies

- Todo persistence (must survive session boundaries)
- Cross-session greeting logic (existing — see `cross-session-greeting-ux-spec-v1.md`)

## Sprint Placement

M1 — Minimum viable approach builds on existing todo infrastructure + cross-session greeting logic. No M3/M5 dependencies. Full notification-based implementation remains M5.

---

*Drafted by CXO, 2026-03-13*
