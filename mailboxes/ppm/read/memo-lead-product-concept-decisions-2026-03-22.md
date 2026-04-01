# Memo: Product Concept — Design & Architecture Decisions Needed

**To**: PM (xian)
**From**: Lead Developer
**Date**: 2026-03-22
**Re**: #717 MUX-PRODUCT-MODELING — Decisions needed before M2 implementation
**Priority**: Blocking for M2

---

## Context

PM has overruled the earlier "Post-MVP" assignment for #717. A product app without a concept of Product isn't ready for beta. This memo identifies the design and architecture decisions needed so implementation can proceed in M2.

The domain model already has a basic `Product` class (name, vision, strategy, relationships to Feature/Stakeholder/Metric/WorkItem). What's missing is the *conceptual framework* — what Product means in Piper's world and how it relates to the entity grammar we've established.

---

## Decisions Needed

### 1. What IS a Product in Piper's world?

**Current state**: `Product` has `name`, `vision`, `strategy` fields and lists of features/stakeholders/metrics/work_items. It's a container, not much more.

**Decision needed**: Is a Product:

- **(A)** A strategic container — the top-level entity that gives meaning to everything else? ("Piper Morgan is a Product. It has Features, Projects contribute to it, WorkItems advance it.")
- **(B)** A peer of Project — a parallel organizing concept? ("I'm working on the Piper Morgan product across three projects: backend, frontend, deployment.")
- **(C)** An umbrella — one level above Project? ("The Acme Platform product contains the API project, the web project, and the mobile project.")

This matters because it determines the UI hierarchy and how users think about navigation.

### 2. Product ↔ Project Relationship

**Current state**: No explicit relationship in the model. Project has no `product_id`. Product has no `projects` list.

**Options**:

- **(A)** Many-to-many — A Product can span multiple Projects, a Project can serve multiple Products. (Most flexible, most complex UI.)
- **(B)** One Product → many Projects — A Product owns its Projects. (Clean hierarchy, may not match reality for shared infrastructure projects.)
- **(C)** Implicit via Features — Products have Features, Features generate WorkItems, WorkItems live in Projects. The relationship is indirect. (Elegant but hard to navigate.)

**Recommendation from Lead Dev**: Option B with an escape hatch. Most PMs think in terms of "my product has these projects." The few cases where a project serves multiple products can be handled as a future enhancement rather than blocking the initial model.

### 3. Does Product Have Lifecycle?

**Current state**: Product has no `lifecycle_state` field. Feature does.

**Options**:

- **(A)** Yes — Products are born (EMERGENT), get shaped (PROPOSED), get built (RATIFIED), get sunset (DEPRECATED), get archived (ARCHIVED). This matches the 8-stage model.
- **(B)** No — Products are always "active" or "retired." They don't go through the same lifecycle as Features/WorkItems. Their lifecycle is implicit in their Features' lifecycles.
- **(C)** Simplified — Products have a simpler lifecycle: ACTIVE, MAINTENANCE, SUNSET, ARCHIVED. Not the full 8-stage model.

**Recommendation from Lead Dev**: Option C. Products evolve on a different timescale than Features. The full 8-stage model was designed for things that emerge, get noticed, and get ratified. Products are more deliberate — they're created by decision, not discovered. A simplified lifecycle respects that difference.

### 4. Feature → Product vs Feature → WorkItem

**Current state**: Feature has `product_id` (linking to Product). WorkItem has no `feature_id`. The relationship is: Product → Feature (via product_id) and Product → WorkItem (via direct list), but Feature → WorkItem is not modeled.

**Decision needed**: Should Features own WorkItems?

- **(A)** Yes — Feature is the bridge: Product → Feature → WorkItem → Project. Clean hierarchy.
- **(B)** No — WorkItems belong to Projects, Features belong to Products, and the connection is contextual (a WorkItem might *relate to* a Feature but isn't owned by it).

This affects how we build the Features View (#716) and whether WorkItems show their Feature context.

### 5. What Views Does Product Need?

**Current state**: No Product view exists. No `/products` route or template.

**Minimum viable for M2**:

- **Product List** — "Show my products" → list with name, status, feature count, project count
- **Product Detail** — Click into a product → features, related projects, health summary
- **Product in Navigation** — Where does Product appear? Top-level nav? Sidebar? Only via chat?

**Decision needed**: Is Product a first-class navigation item (like Projects and Todos), or is it accessed through conversation only ("What products am I working on?")?

---

## What I Need Back

For each of the 5 decisions above: a clear choice (A/B/C) with brief rationale. If any need broader input (architect, CXO), please route accordingly. Once I have decisions, I can:

1. Update the domain model
2. Add database migrations if needed
3. Create the Product API endpoints
4. Build the Product views
5. Wire into the intent system ("What products am I working on?")

Estimated implementation: 1-2 days once decisions are made.

---

*Filed as memo, not issue comment, because these are design decisions that should involve stakeholders beyond the GitHub issue thread.*
