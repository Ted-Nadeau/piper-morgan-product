# Memo: Entity Tokens Guidance Added — #818 Unblocked

**From**: Documentation Management Specialist (Docs Agent)
**To**: Lead Developer
**Date**: February 21, 2026
**Re**: Entity token vs parrot confirmation guidance now in implementation guide
**Reference**: Chief Architect prompt, #818

---

## Summary

Per the Chief Architect's instructions, I've added section **5.8 Entity Names vs. Parrot Confirmations** to the Conversational Glue Implementation Guide.

**File**: `docs/internal/planning/conversational-glue/conversational-glue-implementation-guide.md`

---

## What Was Added

The new section clarifies the distinction that was causing audit ambiguity:

- **Entity name echo** (acceptable): "I couldn't find a project called 'Q3 Roadmap'"
- **Parrot confirmation** (not acceptable): "You said 'schedule meeting with Sarah Tuesday'"

Key guidance:
- Entity names are identifiers, not user input to paraphrase
- Use single quotes around entity names in prose
- Gate 2 audit should NOT flag entity echoing as parrot behavior

---

## Impact on #818

This documentation update should unblock #818 by providing clear guidance that the anti-flattening verification (Gate 2) can reference when distinguishing acceptable entity echoing from robotic parrot confirmations.

The guidance explicitly states: "Entity name echoing should NOT be flagged as parrot behavior during anti-flattening verification."

---

## Action Requested

Please verify this unblocks #818 completion. If the M0 sprint gate requires additional work beyond this documentation, let me know.

---

*Docs Agent*
