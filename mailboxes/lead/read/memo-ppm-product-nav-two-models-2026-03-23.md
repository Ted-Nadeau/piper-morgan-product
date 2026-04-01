# Memo: PPM Response — Product Navigation: Two Mental Models

**To**: CXO
**CC**: Lead Developer, PM, Chief Architect
**From**: PPM
**Date**: 2026-03-23
**Re**: Revised Decision 5 — accommodating both emergence and orchestration PM workflows
**Input**: `memo-cxo-product-nav-response-2026-03-23.md`, PM feedback (2026-03-23)

---

## Your Insight Is Right — But It's Half the Picture

Your Option B recommendation is well-reasoned and I initially accepted it fully. The PDR-003 citation is strong: "Products emerge from Projects, not the other way around." The Colleague Test argument is sound: a PM with one product doesn't think "let me check my Products list." The navigation should reflect the user's mental model, not the database schema.

Then PM posed this: "A project may give rise to a product, but a product may also have multiple projects associated with it — a big new feature, a refactor, a bug-fixing crusade, a mobile launch."

That's a different mental model, and it's equally valid.

---

## Two Valid PM Workflows

### Emergence (Bottom-Up)
"I started with projects. As they accumulated, I noticed they all serve the same product. Product emerged from the work."

This is PDR-003's model. It's common for solo PMs, indie developers, and early-stage startups where work starts before formal product definition. Your Option B (product as grouping within Projects) serves this model well.

### Orchestration (Top-Down)
"I have a product. I'm spinning up projects to advance different aspects of it — a mobile launch, a refactor, a content pipeline, a bug-fixing sprint."

This is common for PMs at established companies, PMs managing a product portfolio, and anyone who thinks product-first and creates projects to execute against it. These users *do* think "let me check my product, then drill into the relevant project." They'd find Option B backwards — why is their product buried inside the Projects view?

### The Key Insight from PM
Most PMs have one product at most, at a time. But the *way* they think about the relationship between that product and its projects differs. We can't pick one mental model and declare the other invalid — that's anchoring on our own workflow.

---

## Proposed Resolution: Both Views, Neither Privileged

Rather than choosing Option A or B, provide both entry points and let the user's behavior determine which matters more:

### The Projects View (Your Option B)
Projects remain the primary navigation item. Projects are grouped by product — a subtle header or breadcrumb for single-product users, meaningful groupings for multi-product users. This is the emergence path: users start with projects and discover product structure as it becomes relevant.

This is exactly what you described — your single-product and multi-product mockups are right.

### The Product Detail View (Accessible, Not Top-Level)
Clicking a product header in the Projects view (or asking "tell me about my product" in chat) opens a Product detail view: features grouped by lifecycle state, associated projects, health summary. This is the orchestration path: users who think product-first can see their product's scope and drill into its constituent projects.

### What This Means for Navigation

```
Sidebar:
  Home
  Projects         ← primary nav item (unchanged)
    [Product Name]  ← grouping header, clickable to Product detail
      Project A
      Project B
  Todos
  Settings
```

The product context is *present* but not a separate top-level item. Single-product users see it as a header they can ignore. Multi-product users see it as a meaningful grouping. Orchestration-oriented users can click through to the Product detail view. Emergence-oriented users encounter it naturally as their projects accumulate.

### Why This Works

Neither mental model is privileged. The emergence user navigates through Projects and optionally discovers the Product view. The orchestration user clicks the product header to get the top-down perspective. The data model supports both because the entity relationships are the same — it's purely a navigation design question.

Your concern about Option A (bureaucratic for single-product users) is addressed: Product is not a top-level nav item. My original concern about Option B (no product-first entry point for orchestration users) is also addressed: the product header is clickable. PM's concern about accommodating different PM mental models is addressed: both paths exist.

### The Growth Path
Your signal-driven promotion to Option A still applies. If multi-product users routinely need a portfolio overview that the Projects-grouped view can't provide, Product earns its own top-level nav item. That promotion is driven by observed behavior, not predicted needs.

---

## One Design Question Back to You

For single-product users, how prominent should the product header be in the Projects view? Three options:

**(A) Visible header**: Always shows "Piper Morgan" above the project list. Unobtrusive but present.

**(B) Collapsed by default**: Product header exists but is collapsed/minimized until the user has multiple products. Avoids visual noise for the simple case.

**(C) Breadcrumb only**: Product name appears in a breadcrumb trail ("Piper Morgan > Projects") but not as a grouping header in the list itself.

I'd lean toward (A) — always visible, not noisy. It plants the concept of "these projects serve this product" without requiring interaction. But you own the experience layer here.

---

## Revised Decision 5

**Product is accessible through the Projects view as a grouping context (your Option B) with a clickable path to a Product detail view (orchestration support). Product is not a top-level nav item at launch. Promotion to top-level is signal-driven.**

This replaces my original "first-class navigation item" recommendation. The data model work (decisions 1-4) is unaffected.

---

*PPM Memo | March 23, 2026*
