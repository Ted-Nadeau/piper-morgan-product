# Memo: Offer System Design — Architectural Guidance

**From**: Chief Architect
**To**: Lead Developer
**Date**: February 25, 2026
**Re**: Response to offer system design question
**Priority**: Guidance for next sprint

---

## Summary

Option C is correct, but the framing needs sharpening. The distinction isn't "real vs rhetorical" — it's **actionable vs contextual**. I'm providing a bright-line rule that makes the boundary concrete.

---

## The Bright-Line Rule

> **If "yes" should invoke a named workflow, use `action_required`.**
> **If "yes" means "continue/elaborate," let the LLM handle it contextually.**

This is the decision point when writing any handler that includes "Would you like...":

| Question to Ask | Answer | Action |
|-----------------|--------|--------|
| Does "yes" start a specific, predefined workflow? | Yes | Use `action_required` with workflow type |
| Does "yes" mean "tell me more" or "continue"? | Yes | No `action_required`, LLM handles it |

---

## Applying the Rule to Your 11 Sites

Let me classify them:

| Site | Offer Text | Classification | Rationale |
|------|------------|----------------|-----------|
| Line 2542 | "explain what information to include for each project?" | **Contextual** | "yes" = continue explaining |
| Line 2557 | "explain more about how Piper uses project context?" | **Contextual** | "yes" = elaborate |
| Line 2625 | "guidance on setting up a specific integration?" | **Contextual** | "yes" = provide guidance (conversation) |
| Line 4392 | "search for something else?" | **Contextual** | "yes" = prompt for new search term |
| Line 4428 | "explore more of our history?" | **Contextual** | "yes" = show more history |
| Line 4693 | "add one?" (projects) | **Actionable** | "yes" = start `add_project` workflow |
| Line 4733 | "list your projects?" | **Contextual** | "yes" = display list (no workflow) |
| Line 4773 | "list your projects?" | **Contextual** | Same as above |
| Line 4810 | "list your archived projects?" | **Contextual** | "yes" = display filtered list |
| Line 4842 | "see all your projects?" | **Contextual** | "yes" = display list |
| intent_service 1319 | "continue where you left off, or start fresh?" | **Actionable** | "yes/continue" = resume workflow |

**Result**: Only 2 of 11 are actionable. The rest are contextual continuations that should NOT have `action_required` — they're conversational, and the LLM should handle them.

---

## The Actual Gap

Your analysis is right that the LLM handling is "a coin flip." But the fix isn't to make everything structured — it's to improve the LLM's contextual handling.

**Current problem**: When user says "yes" after a contextual offer, the LLM classifier sees bare "yes" with no context about what was just offered.

**Solution**: Enhance `ConversationContext` to track the last offer:

```python
class ConversationContext:
    # ... existing fields ...
    last_offer: Optional[LastOffer] = None

class LastOffer:
    offer_type: Literal["actionable", "contextual"]
    offer_text: str  # The "Would you like..." text
    continuation_hint: Optional[str]  # What "yes" should do
```

When the LLM sees a bare affirmative ("yes", "sure", "okay") and `last_offer.offer_type == "contextual"`, it should interpret the response as "user wants the offered continuation" rather than classifying from scratch.

This is a small extension to the M0 lens/context work.

---

## Why Not Option A or B

**Option A** (retrofit all to structured) forces conversational language into system contracts. We'd invent phantom workflows like `explain_project_context` just to satisfy the type system. That's not what workflows are for.

**Option B** (text-based detection) couples system behavior to prose patterns. "Would you like" vs "Want me to" vs "Should I" — we'd be playing regex whack-a-mole forever. Fragile architecture.

**Option C with bright-line rule** keeps the structured system clean (`action_required` = workflow trigger) while acknowledging that some offers are just conversation. The LLM is good at conversation — we just need to give it the context.

---

## Recommended Actions

### 1. Don't retrofit the 11 sites

Most are contextual. Review the two I flagged as potentially actionable:
- Line 4693 ("add one?") — should this have `action_required: "add_project"`?
- intent_service 1319 ("continue where you left off") — should this have `action_required: "resume_workflow"`?

If yes, add them. If they're working via LLM context already, leave them.

### 2. Create one issue for contextual continuation improvement

**Title**: CONV-CONTEXT-OFFER: Track last offer for contextual continuation

**Scope**:
- Add `last_offer` to ConversationContext
- Populate it when response contains contextual offer (can use simple heuristic or handler annotation)
- Enhance LLM classifier to check `last_offer` when processing bare affirmatives
- Tests for "yes after contextual offer" scenarios

**Effort**: 2-3 days
**Sprint**: M1 or polish track

### 3. Document the rule

Add to `conversational-glue-implementation-guide.md` or create Pattern-062 (Offer Classification):

- Bright-line rule
- Examples of actionable vs contextual
- When to use `action_required`
- How contextual offers flow through LLM

### 4. No ADR needed

This is guidance-level, not architectural decision. A pattern or implementation guide section is sufficient.

---

## The Principle

The underlying principle is **separation of concerns**:

- **Structured system** handles workflow invocation (machine-readable, deterministic)
- **LLM** handles conversational flow (contextual, flexible)

Offers that trigger workflows belong in the structured system. Offers that continue conversation belong in the LLM's domain. Mixing them creates the fuzzy boundary you identified.

The bright-line rule makes the boundary concrete: **Does "yes" start a workflow?** If you can name the workflow, use `action_required`. If you can't, it's contextual.

---

## Questions?

If the two potentially-actionable sites (4693, 1319) need discussion, let me know. Otherwise, I think the path forward is clear:

1. Leave most sites alone (contextual, LLM handles)
2. Create issue for contextual continuation improvement
3. Document the rule

No whack-a-mole. One structural improvement that handles the category.

---

*Chief Architect, 2026-02-25*
