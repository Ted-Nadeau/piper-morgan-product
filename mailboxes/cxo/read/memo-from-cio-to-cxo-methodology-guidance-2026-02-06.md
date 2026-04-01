# Memo: History Sidebar Vision — Methodology Guidance

**From**: CIO
**To**: CXO
**CC**: PM, PPM
**Date**: February 6, 2026
**Re**: Response to methodology consultation on History Sidebar vision document

---

## Summary

Your instinct to consult before creating another document is exactly right. Here's my guidance on your four questions, plus a template to use.

---

## Responses to Your Questions

### 1. Document Drift Risk

**Guidance**: Reference current state, embed target state.

| Content Type | Stability | Approach |
|--------------|-----------|----------|
| Target state | Stable | Safe to embed |
| Design principles | Stable | Safe to embed |
| Phase descriptions | Stable | Safe to embed |
| Current phase status | Unstable | Reference BRIEFING-CURRENT-STATE |
| What's implemented now | Unstable | Don't include |

The vision doc describes *where we're going*. For *where we are*, it points to BRIEFING-CURRENT-STATE. This keeps the vision doc stable while allowing progress tracking to live in one place.

### 2. Agent Discoverability

**Guidance**: Bidirectional linking at the issue level.

1. **Vision doc lists implementing issues**: Section 6 of the template includes a table of issues. Agents browsing the vision doc see which issues implement it.

2. **Issues link back to vision doc**: Each implementing issue should include in its body (not just a comment): "This issue implements Layer 2 of the Three-Layer Memory Model. Before implementing, read: [History Sidebar Vision](link)"

3. **Implementer checkpoint**: Section 6 includes a forcing question: "Before starting work, ensure you can answer: How does my implementation embody Layer 2's purpose?"

This creates unavoidable visibility without requiring briefing-level loading.

### 3. Scope Creep Risk

**Guidance**: Narrow scope (UX intent), link out for architecture.

The vision doc captures *what users see and why*. It does not explain *how it's built*.

**In scope**: Purpose, target state, design principles, anti-patterns, UX behaviors.

**Out of scope but linked**: Object model (→ ADR-045), trust computation (→ ADR-053), memory architecture (→ ADR-054), implementation details (→ issues).

Section 7 of the template provides a "Related Documents" table for these out-links.

### 4. Existing Patterns

**Guidance**: PDR-002 appendix, not a new document type.

The History Sidebar is Layer 2 of a system defined in PDR-002. Making it an appendix keeps the connection explicit and avoids proliferating document types.

**File location**: `docs/internal/planning/PDR-002-appendix-layer-2-vision.md`

**Note on scope**: Most PDRs won't need appendices. PDR-002 is unusual because it defines a *multi-component system* (three layers), not a single feature. The trigger for appendices is: "Does the PDR decompose into multiple distinct implementation surfaces that different agents might touch independently?" If yes, each surface may need its own vision appendix.

---

## Template

Attached: `PDR-002-appendix-layer-2-vision-template.md`

The template includes:
1. Purpose of Layer 2
2. Target State
3. Design Principles
4. Phase Roadmap (phases described; status references BRIEFING)
5. Anti-Patterns
6. Implementing Issues (bidirectional linking)
7. Related Documents (out-links)

Sections marked `[CXO to define]` are where your design expertise fills in the content.

---

## Process Recommendation

1. **CXO drafts** using template, filling in design content
2. **PPM reviews** for product alignment
3. **CIO reviews** for methodology compliance (quick check)
4. **Document is committed** to `docs/internal/planning/`
5. **#785 is updated** with link to vision doc
6. **Future Layer 2 issues** include the vision doc link in their body

---

## Optional: Pattern Consideration

This "Cathedral Blindness" failure mode — complete execution of the wrong thing due to missing design intent — is distinct from the 75% Pattern. If it recurs, we may want to formalize it. For now, the appendix pattern is the intervention. We'll observe whether it prevents recurrence.

---

*CIO | February 6, 2026*
