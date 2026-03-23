# Memo: Navigation Hierarchy Gut-Check — Product as First-Class Nav Item

**To**: CXO
**CC**: PM (xian), PPM
**From**: Lead Developer
**Date**: 2026-03-22
**Re**: Does Product belong in top-level navigation for M2?

---

## Context

PPM made product modeling decisions for #717. One decision needs your experience perspective before we implement:

**Decision 5 (PPM's call)**: Product should be a first-class navigation item — visible in top-level nav alongside Projects and Todos.

**PPM's rationale**: "Product is the highest-level organizing concept — hiding it behind conversation-only access makes it invisible to users who are visually scanning their workspace."

**Minimum viable for M2**:
- **Product List**: "Show my products" → list with name, lifecycle state, feature count, project count
- **Product Detail**: Click into a product → features, related projects, health summary
- **Product in Chat**: "What products am I working on?" via intent classification

---

## The Question

PPM flagged this for your gut-check: **Does Product at the top level make sense from the user's perspective, or is it clutter for users who only have one product?**

Consider:
- Many early alpha users will have exactly one product. Does a "Products" nav item feel useful or bureaucratic when there's only one?
- The current nav has: Home, Projects, Todos, Settings. Adding Products creates: Home, Products, Projects, Todos, Settings. Does that hierarchy read clearly?
- Alternative: Product could be a section *within* Projects (a grouping header) rather than a peer nav item. Less prominent, but avoids the "one item in a list" problem.
- Another alternative: Show Product nav only when the user has >1 product. Adaptive UI.

---

## What I Need

Your recommendation on where Product should live in the navigation hierarchy. The three options as I see them:

**(A) First-class nav item** (PPM's recommendation) — always visible, peer of Projects
**(B) Section within Projects** — Products as group headers, Projects nested under them
**(C) Adaptive** — show Product nav only when user has multiple products

Any of these is implementable. I'm asking which one feels right for a user looking at their workspace.

---

*Lead Developer | March 22, 2026*
