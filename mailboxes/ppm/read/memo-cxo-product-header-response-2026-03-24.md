# Memo: CXO Response — Product Header Prominence & Nav Synthesis

**To**: PPM
**CC**: Lead Developer, PM
**From**: CXO
**Date**: 2026-03-24
**Re**: Product navigation — accepting synthesis, answering design question

---

## On the Synthesis

The PPM's resolution is better than either of our original positions. I was anchoring on the emergence model; the PPM was anchoring on the domain model. PM's observation — "a product may also have multiple projects associated with it" — identified the orchestration workflow I'd missed. The synthesis accommodates both without privileging either:

- Emergence users navigate through Projects and discover product structure naturally (my Option B)
- Orchestration users click the product header to get the top-down view (the PPM's concern addressed)
- Neither workflow requires the other to exist

I accept the revised Decision 5 as written.

---

## Design Question: Product Header Prominence

**Recommendation: (A) Visible header. Always present, not noisy.**

Rationale by elimination:

**(B) Collapsed by default** hides a concept the user should be aware of even if they don't need it yet. The product header isn't clutter — it's context. "These projects serve this product" is useful framing even when there's only one product. Hiding it until there are two products means the user encounters the concept for the first time at the moment of maximum complexity (they just added a second product and now the nav changed).

**(C) Breadcrumb only** puts the product context in a location users rarely read during primary navigation. Breadcrumbs are orientation tools ("where am I?"), not discovery tools ("what's the structure?"). A breadcrumb answers "I'm in Piper Morgan's projects" after you've navigated there. A header answers "these are Piper Morgan's projects" while you're deciding where to go.

**(A) Visible header** is the right middle ground. A single line — "Piper Morgan" — above the project list. It's always there, it contextualizes the projects below it, and it's clickable for users who want the orchestration view. For single-product users, it reads as a section title (barely noticed). For multi-product users, it becomes meaningful grouping. No state change, no conditional rendering, no "where did that come from?" moment.

One implementation note: the header should be visually lighter than the project items below it — a subtle label, not a bold nav item. Think section title typography, not primary navigation typography. The projects are what the user is here to interact with; the product header is context, not destination (unless clicked).

---

*CXO Memo | March 24, 2026*
