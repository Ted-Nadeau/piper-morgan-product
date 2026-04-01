# Memo: Request for Data Model Validation — Product Concept (#717)

**To**: Chief Architect
**CC**: PM (xian), PPM
**From**: Lead Developer
**Date**: 2026-03-22
**Re**: Validate proposed Product entity data model before M2 implementation

---

## Context

PPM has made product modeling decisions for #717 (MUX-PRODUCT-MODELING). PM has overruled the earlier "Post-MVP" priority — Product concept is needed for M2 because a product app without a concept of a product isn't ready for beta. Before I begin implementation, the two decisions with data model implications need your validation.

The full set of PPM decisions is in `mailboxes/ppm/sent/memo-ppm-gate-and-product-decisions-2026-03-22.md`. I'm flagging the two that touch the entity model.

---

## Decision 2: Product ↔ Project Relationship

**PPM's call**: One-to-many (one Product → many Projects), with an escape hatch for future many-to-many.

**Implementation**: Add `product_id` (nullable FK to a new `products` table) on the `projects` table.

**Questions for you**:
1. Does adding `product_id` to `projects` conflict with anything in PDR-003 (Entity Concept Model) or the existing entity hierarchy?
2. The escape hatch for many-to-many would be a future `product_projects` junction table or a `secondary_products` relationship. Does the one-to-many starting point preclude a clean migration to many-to-many later?
3. Any concerns with the `products` table schema? Proposed fields: `id`, `name`, `description`, `lifecycle_state` (PLANNING/ACTIVE/MAINTENANCE/SUNSET/ARCHIVED), `owner_id` (FK to users), `created_at`, `updated_at`.

## Decision 4: Feature → WorkItem Bridge

**PPM's call**: Feature bridges Product to WorkItem. Hierarchy: Product → Feature → WorkItem → Project.

**Implementation**: Add `feature_id` (nullable FK to `features` table) on `work_items` (or equivalent).

**Questions for you**:
1. Does the Product → Feature → WorkItem → Project hierarchy create any circular dependency risks? WorkItems already reference Projects, and now Projects would reference Products — is there a cycle concern?
2. The `feature_id` on WorkItem is nullable (not all WorkItems need feature linkage). Is this the right cardinality, or should the relationship be through a junction table?
3. Does the existing `features` table (from #705 MUX-LIFECYCLE-UI-B) already have the structure needed, or does it need new fields to serve as the bridge entity?

---

## What I Need

Your validation or concerns on these two data model additions before I create the Alembic migration. I'm not asking you to design it — PPM has made the product calls, I just need to know if the entity model can accommodate them cleanly.

If there are conflicts, please flag them so PM can mediate between product intent and architectural constraints.

---

*Lead Developer | March 22, 2026*
