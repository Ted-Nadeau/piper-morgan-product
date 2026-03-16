# Template Stub & Boilerplate Inventory

**Date**: 2026-03-15
**Scope**: All user-facing stub/template responses in the codebase

---

## HIGH SEVERITY: "Implementation Pending" Stubs (3)

These return raw dev language directly to users:

| File | Line | Text | Handler |
|------|------|------|---------|
| `intent_service.py` | 5713 | `"Synthesis capability ready for '{action}'. Specific implementation pending."` | Synthesis fallback |
| `intent_service.py` | 7615 | `"Strategy capability ready for '{action}'. Specific implementation pending."` | Strategy fallback |
| `intent_service.py` | 8815 | `"Learning capability ready for '{action}'. Specific implementation pending."` | Learning fallback |

## HIGH SEVERITY: "I Can't Do X Yet" Messages (8)

In `_get_contextual_fallback()` (intent_service.py lines 4840-4902):

| Line | Trigger | Message |
|------|---------|---------|
| 4840 | schedule/meeting | "I can't create calendar events yet — that's coming soon..." |
| 4848 | remind me | "I can't set reminders yet..." |
| 4855 | create doc/document | "I can't create documents yet..." |
| 4871 | batch create issues | "I can't batch-create issues from a meeting yet..." |
| 4879 | close + issue | "I can't close issues yet..." |
| 4887 | post + slack/channel | "I can't post to Slack channels yet..." |
| 4895 | complete + todo | "I can't mark todos complete yet..." |
| 4902 | upload + file | "I can't accept file uploads yet..." |

**Note**: Line 4895 ("can't mark todos complete") is NOW WRONG — #904 implemented todo completion.

## MEDIUM SEVERITY: Hardcoded Identity/Greeting Templates (8)

| File | Line | Text |
|------|------|------|
| `canonical_handlers.py` | 402 | "I'm Piper Morgan, your AI Product Management assistant..." |
| `canonical_handlers.py` | 413 | "Think of me as your intelligent PM partner!" |
| `canonical_handlers.py` | 289 | "Here's what I can help you with:" |
| `degradation.py` | 165 | "Hello! I'm Piper Morgan, your AI-powered Product Management Assistant..." |
| `slack/response_handler.py` | 667 | "🤖 I'm Piper Morgan, your AI Product Management Assistant..." |
| `slack/response_handler.py` | 687 | "🤖 I'm Piper Morgan, your AI Product Management Assistant..." |
| `slack_adapter.py` | 77 | "Hi! I'm Piper, your PM assistant..." |
| `onboarding/portfolio_handler.py` | 236 | "Hello! I'm Piper Morgan, your PM assistant..." |

## MEDIUM SEVERITY: Chitchat Catch-All Templates (2)

| File | Line | Text |
|------|------|------|
| `conversation_consciousness.py` | 122-124 | "I'm doing well, thanks for asking! I've been keeping an eye on your projects..." |
| `conversation_handler.py` | 79-83 | Array of 3 hardcoded chitchat responses |

## LOW SEVERITY: Query/Analysis Not-Yet-Supported (2)

| File | Line | Text |
|------|------|------|
| `orchestration/engine.py` | 180 | "Query action '{action}' not yet supported by QueryRouter" |
| `orchestration/engine.py` | 238 | "Analysis action '{action}' is not yet fully implemented..." |
