# Memo: CXO Response — Product Navigation Hierarchy

**To**: Lead Developer
**CC**: PPM, PM
**From**: CXO
**Date**: 2026-03-23
**Re**: Where Product belongs in navigation for #717

---

## Recommendation: Option B (Section within Projects), with a growth path to A

Neither the PPM's Option A nor the Lead Dev's Option C. Here's why.

---

## The Deciding Factor

PDR-003 says this explicitly: **"Products emerge from Projects, not the other way around. Users start with Projects (the concrete work). Products (the organizational container) emerge as users recognize patterns."**

That sentence answers the navigation question. If Products emerge from Projects in the user's mental model, then Products should emerge from Projects in the navigation. Putting Product as a peer of Projects inverts the mental model — it says "Product is a thing you define first, then organize Projects under it." That's the domain modeler's perspective, not the user's.

---

## Why Not Option A (First-Class Nav Item)

The PPM's rationale is sound in the abstract — Product is the highest-level organizing concept in the domain model. But domain model hierarchy ≠ navigation hierarchy. Navigation should reflect how users think about their work, not how the database organizes it.

Apply the Colleague Test: a PM with one product doesn't think "let me check my Products list." They think "let me check my projects." Product is a container they don't need until they have enough things to organize. A Products nav item with one entry feels like enterprise software — bureaucratic overhead for a concept the user hasn't yet needed.

Concretely: Home, **Products**, Projects, Todos, Settings reads like five top-level categories. A user scanning that list has to decide "do I click Products or Projects?" when their mental model doesn't distinguish them yet. That's cognitive overhead with no payoff for single-product users.

---

## Why Not Option C (Adaptive/Conditional)

Adaptive UI (show Product nav only with multiple products) solves the clutter problem but creates a different one: **the navigation changes shape when the user adds a second product.** A new nav item appearing is disorienting — "where did that come from?" Adaptive nav also means the user can't discover the Product concept until they've already created a second one, which creates a chicken-and-egg problem: how do they know to create a second product if they've never seen the Product concept?

Adaptive UI works when the hidden element is non-essential (progressive disclosure). Product isn't non-essential — it's how the user will eventually organize their work. Hiding it until they accidentally need it isn't progressive disclosure, it's concealment.

---

## Why Option B Works

**Projects as the primary nav item, with Product as a grouping context within it.**

The user clicks Projects and sees their work. If they have one product, the product context is present but unobtrusive — a header, a breadcrumb, a subtle grouping label. If they have multiple products, the grouping becomes meaningful: projects organized under product headers, with the ability to filter or switch between them.

This matches the mental model from PDR-003: you start with projects, and product structure emerges as you accumulate enough work to need it. The navigation reflects that emergence rather than front-loading a concept the user hasn't needed yet.

**What this looks like in practice:**

Single product (most alpha users):
```
Projects
  ├── M1 Sprint
  ├── Website Redesign
  ├── Content Pipeline
  └── Alpha Program
```
Product context visible as a subtle header or breadcrumb ("Piper Morgan") but not requiring interaction. The user never has to "manage products" — they just see their projects.

Multiple products (future):
```
Projects
  Piper Morgan
    ├── M1 Sprint
    ├── Website Redesign
    └── Alpha Program
  Klatch
    ├── v0.9 Release
    └── Entity System
```
Product headers become meaningful groupings. The user can collapse, filter, or navigate between product contexts. No new nav item appeared — the structure just gained depth.

---

## The Growth Path to A

If and when users routinely work across multiple products, Product may earn its own top-level nav item. The signal would be: users are switching between product contexts frequently enough that the Projects view feels crowded. At that point, a top-level Product nav item provides a portfolio overview ("all my products and their health") that's distinct from the per-project detail view.

But that's a signal-driven promotion, not a launch decision. Ship B, observe usage, promote to A if the data says so.

---

## Chat Access

Regardless of nav placement, "What products am I working on?" should work via intent classification and the floor. This is independent of where Product lives in the sidebar.

---

## Summary

| Option | Verdict | Rationale |
|--------|---------|-----------|
| A (First-class nav) | Not now | Inverts user mental model; bureaucratic for single-product users |
| B (Section within Projects) | **Recommended** | Matches PDR-003's emergence model; scales naturally from 1 to N products |
| C (Adaptive) | Not recommended | Disorienting when nav changes shape; conceals rather than progressively discloses |

---

*CXO Memo | March 23, 2026*
