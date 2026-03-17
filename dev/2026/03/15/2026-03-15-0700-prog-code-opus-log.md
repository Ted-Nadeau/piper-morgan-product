# Session Log: Canonical Handler Generic Response Audit

**Date**: 2026-03-15
**Role**: Programmer (subagent)
**Task**: Audit all canonical handlers for generic template responses (#907)
**Branch**: claude/distracted-sammet

---

## Findings Summary

### Current Floor Routing Infrastructure

The `_is_generic_canonical_response()` method at line 9281 of `intent_service.py` currently catches **exactly one** signature:

```python
_GENERIC_CANONICAL_SIGNATURES = [
    "Based on your current priorities and the time of day:",
]
```

When detected, the response is rerouted to `_handle_unknown_intent()` which invokes the `ConversationalFloor`. This infrastructure is already in place and working for that single pattern.

---

## Per-Category Audit

### 1. GUIDANCE (lines 4242-4375) -- HAS GENERIC FALLBACK

**The problem handler.** For ANY GUIDANCE query that isn't a setup request, it:
1. Gets user context (or falls back to None)
2. Gets calendar context
3. Synthesizes a "focus recommendation"
4. Formats via `_format_standard_guidance()` (default path)

**Generic text** (line 2432):
```
"Based on your current priorities and the time of day:\n"
```

This fires for EVERY guidance query regardless of what was asked. "Can you help me manage agents working on a coding assignment?" gets the same priorities/time-of-day response as "What should I focus on?"

**Status**: Already caught by `_GENERIC_CANONICAL_SIGNATURES[0]`. Floor routing works for this one. However, the `_format_detailed_guidance` and `_format_consolidated_guidance` variants are NOT caught:
- `_format_detailed_guidance` (line 2284): `"Here's comprehensive guidance for your focus:\n"` -- same problem, different text
- `_format_consolidated_guidance` (line 2381-2394): Returns things like `"Focus: Deep work"`, `"Focus: Team coordination"` etc. -- generic time-based strings

**Verdict**: Partially fixed. Only the standard format is caught. GRANULAR and EMBEDDED variants also produce generic responses but aren't detected.

---

### 2. IDENTITY (lines 190-243) -- LOW RISK

Has specific sub-routing:
- `_detect_health_check_request()` -> dedicated handler
- `_detect_differentiation_request()` -> dedicated handler
- `_detect_help_request()` -> dedicated handler
- Default: Returns identity info ("I'm Piper Morgan...")

**Generic text**: The default response is always "I'm Piper Morgan, your AI Product Management assistant..." which is appropriate for identity queries. This IS the right answer for "Who are you?"

**Verdict**: No fix needed. The default response genuinely answers identity questions.

---

### 3. DISCOVERY (lines 245-282) -- LOW RISK

Returns dynamic capability list from PluginRegistry. Always answers "What can you do?" style queries.

**Generic text**: "Here's what I can help you with:" followed by capabilities list.

**Verdict**: No fix needed. This is appropriate -- it's answering the actual question.

---

### 4. TEMPORAL (lines 800-1000) -- LOW RISK

Has specific sub-routing:
- `_detect_agenda_request()` -> agenda handler
- `_detect_retrospective_request()` -> retrospective handler
- `_detect_last_activity_request()` -> last activity handler
- `_detect_duration_request()` -> duration handler
- Default: Returns current date/time + calendar info

**Generic text**: `"Today is {date} at {time}."` + calendar context

**Verdict**: No fix needed. Time/date is the correct response for temporal queries.

---

### 5. STATUS (lines 1251-1422) -- MODERATE RISK

Has specific sub-routing:
- `_detect_project_list_request()` -> project list handler
- `_detect_landscape_request()` -> landscape handler
- `_detect_status_report_request()` -> status report handler
- `_detect_project_specific_query()` -> project-specific handler
- No projects: Triggers onboarding flow
- Default: Returns project list with metadata

**Generic text** (default path, line 1402):
```
_format_standard_status() produces: "Here's what you're working on:\n" + project list
```

**Verdict**: Low risk but could swallow queries like "What's the status of the deployment pipeline?" if misclassified as STATUS. The response lists ALL projects rather than addressing the specific question. Worth monitoring but not high priority.

---

### 6. PRIORITY (lines 1681-1772) -- MODERATE RISK

Has specific sub-routing:
- `_detect_priority_recommendation_request()` -> recommendation handler
- No priorities: Returns setup prompt
- Default: Lists all priorities from PIPER.md

**Generic text** (line 1842):
```
"Your top priority today is: **{priorities[0]}**\n"
```

**Verdict**: Similar to STATUS. If a nuanced priority question ("How should I prioritize between X and Y?") gets classified as PRIORITY, it gets a simple list dump instead of actual guidance. Worth monitoring.

---

### 7. CONVERSATION (lines 5533-5558) -- MODERATE RISK

Delegates to `ConversationHandler.respond()` which uses:
- Greeting: `format_greeting_conscious()` - time-aware, calendar-aware. **Good.**
- Farewell: `format_farewell_conscious()` - static: "Take care! I'll keep an eye on things while you're away." **Acceptable for farewells.**
- Thanks: `format_thanks_conscious()` - static: "Happy to help! Is there anything else on your mind..." **Acceptable.**
- Chitchat (catch-all): `format_chitchat_conscious()` - static: "I'm doing well, thanks for asking! I've been keeping an eye on your projects. What's on your mind?" **PROBLEM.**

The chitchat catch-all fires for any CONVERSATION intent that isn't greeting/farewell/thanks. If a query like "Tell me about agile methodologies" gets classified as CONVERSATION/chitchat, it gets this non-answer.

**Static response arrays** in `ConversationHandler.RESPONSES` (lines 63-84) exist but are NOT used in the current code path -- the consciousness module overrides them. They're dead code.

**Verdict**: The chitchat catch-all is a generic swallowing risk. Should route to floor.

---

### 8. TRUST (lines 4377-4476) -- LOW RISK

Routes to `ExplanationHandler.try_handle()` which has actual query analysis. If ExplanationHandler doesn't recognize the query, falls back to:
```
"I'd be happy to explain how we work together. Our working relationship develops
over time as I learn your preferences and you see how I can help. What would you
like to know specifically?"
```

**Verdict**: The fallback is somewhat generic but asks for clarification. Could benefit from floor routing but low priority.

---

### 9. MEMORY (lines 4478-4645) -- LOW RISK

Has specific routing for search vs. history queries. Falls back gracefully with:
- No user_id: "I can help you explore our conversation history once you're signed in."
- No conversations: "We haven't had many conversations yet..."

**Verdict**: No fix needed. Fallbacks are contextually appropriate.

---

### 10. PORTFOLIO (lines 4647-5091) -- LOW RISK

Has comprehensive operation detection (add/list/archive/delete/restore/search). Fallback for unrecognized operations:
```
"I can help you manage your projects. You can ask me to:\n- Show your projects\n..."
```

**Verdict**: The fallback is a help menu, which is reasonable. Low priority for floor routing.

---

## Recommended Additions to `_GENERIC_CANONICAL_SIGNATURES`

Currently only catches 1 pattern. Should add:

| Signature | Handler | Priority |
|-----------|---------|----------|
| `"Based on your current priorities and the time of day:"` | GUIDANCE standard | Already caught |
| `"Here's comprehensive guidance for your focus:"` | GUIDANCE granular | HIGH |
| `"Focus: Deep work"` | GUIDANCE consolidated | HIGH |
| `"Focus: Team coordination"` | GUIDANCE consolidated | HIGH |
| `"Focus: Task execution"` | GUIDANCE consolidated | HIGH |
| `"Focus: Wrap-up and handoff"` | GUIDANCE consolidated | HIGH |
| `"Focus: Strategic planning"` | GUIDANCE consolidated | HIGH |
| `"I'm doing well, thanks for asking!"` | CONVERSATION chitchat | MEDIUM |

**Better approach**: Instead of string matching, add a `generic_response: bool` flag to the canonical handler return dict. Each handler knows best whether its response actually addressed the query.

---

## Effort Estimates

| Fix | Effort | Description |
|-----|--------|-------------|
| Add more signatures to `_GENERIC_CANONICAL_SIGNATURES` | S (30 min) | Quick but fragile |
| Add `generic_response` flag to canonical return dict | M (2-3 hr) | Better architecture, handlers self-report |
| GUIDANCE: Add query-relevance check before template response | L (4-6 hr) | Handler checks if query matches "focus/priority" semantics before using template |
| CONVERSATION: Route chitchat catch-all through floor | S (1 hr) | Simple conditional in ConversationHandler |
| TRUST: Route fallback through floor | S (1 hr) | Simple conditional |

---

## Trace: "Can you help me manage the agents?" through GUIDANCE

1. Classifier maps to `GUIDANCE` category
2. `can_handle()` returns True (GUIDANCE is in canonical set)
3. `_handle_guidance_query()` called
4. `_detect_setup_request()` checks for setup verbs + nouns -- "manage agents" doesn't match -- returns None
5. Gets user context, calendar context, project/priority metadata
6. Calls `_synthesize_focus_recommendation()` -- produces time-based recommendations
7. No spatial pattern -- falls into `else` branch (line 4312)
8. `_format_standard_guidance()` produces: `"Based on your current priorities and the time of day:\n**Right Now**: {time-based focus}\n**Today's Key Focus**: {priority_text}..."`
9. Back in `intent_service.py`, `_is_generic_canonical_response()` catches the signature
10. Routes to conversational floor -- **this specific case IS fixed by #907**

But if the spatial pattern is GRANULAR, the response starts with "Here's comprehensive guidance for your focus:" which is NOT caught.
