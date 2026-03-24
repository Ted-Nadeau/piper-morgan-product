# Memo: Data Model Validation — Product Concept (#717)

**To**: Lead Developer
**CC**: PM (xian), PPM
**From**: Chief Architect
**Date**: 2026-03-23
**Re**: Architectural validation of Product entity schema changes
**Input**: Lead Dev memo (2026-03-22), PDR-003, domain-models.md, domain-models-proposed-updates-2026-02-26.md
**Status**: APPROVED with notes

---

## Summary

Both schema changes are architecturally sound. The 1:N starting point for Product ↔ Project is a deliberate simplification of PDR-003's M:N design, and the migration path to M:N is clean. The Feature bridge creates no circular dependency. Proceed with the migrations.

---

## Decision 2: Product ↔ Project Relationship

### Q1: Does `product_id` on `projects` conflict with PDR-003?

**Technically yes, pragmatically no.**

PDR-003 explicitly specifies M:N via a `product_projects` join table. The proposed updates document (Feb 26) shows the same. A nullable `product_id` FK on `projects` is 1:N, not M:N.

However, the PPM has product authority and has deliberately chosen 1:N as the starting point with a documented escape hatch. This is a valid product decision — PDR-003's M:N design was based on the Enterprise PM archetype (multiple products, shared projects), which isn't the current user base. The Solo PM and Startup PM archetypes that make up the alpha testers work fine with 1:N.

**My recommendation**: Proceed with the FK, but add a comment in the migration noting the PDR-003 divergence and the intended migration path. Something like:

```python
# product_id is nullable FK (1:N) per PPM decision 2026-03-22.
# PDR-003 specifies M:N via product_projects junction table.
# Migration path: add junction table, migrate FK values, drop column.
```

This prevents a future developer from seeing the FK and assuming 1:N was the architectural intent. The design record stays honest.

### Q2: Does 1:N preclude clean migration to M:N?

**No. The migration is standard and non-destructive.**

The path:
1. Create `product_projects` junction table
2. For each project with a non-null `product_id`, insert a row into `product_projects`
3. Drop `product_id` column from `projects`
4. Update ORM relationships

This is a well-understood relational migration. The nullable FK is actually the safe starting point — it doesn't create data structures that are incompatible with M:N. A project with `product_id = NULL` simply has no entries in the junction table. A project with `product_id = X` gets one entry. When M:N arrives, projects can get additional entries.

One thing to plan for: any queries that join `projects.product_id` will need updating when the junction table arrives. Keep these queries in the repository layer (not scattered across services) so the migration surface is contained.

### Q3: Products table schema concerns?

**No concerns. The schema is clean.**

Proposed: `id`, `name`, `description`, `lifecycle_state`, `owner_id`, `created_at`, `updated_at`.

Notes:
- `lifecycle_state` enum (PLANNING/ACTIVE/MAINTENANCE/SUNSET/ARCHIVED) is appropriate and mirrors the lifecycle pattern already established for other entities.
- `owner_id` FK to users is consistent with the pattern on Project (SEC-RBAC Phase 3).
- Consider whether you need an `is_default` field (as exists on Project). PDR-003's emergence principle says "products emerge from projects" — but there may be a case for a default product that new projects auto-associate with. Not blocking; the Lead Dev or PPM can add this later if needed.
- No `vision` or `strategy` fields in the proposed schema, though the current domain model `Product` dataclass has both. This is fine if the PPM's intent is a leaner Product entity for M2 — the dataclass can carry fields the database doesn't yet store. But verify with PPM that this is intentional, not an oversight.

---

## Decision 4: Feature → WorkItem Bridge

### Q1: Circular dependency risks?

**No cycle in the FK sense. The relationships are semantically distinct.**

The graph you're describing is:

```
Product ---(1:N)--→ Feature
Feature ---(1:N)--→ WorkItem (via feature_id FK)
WorkItem ---(N:1)--→ Project (via project_id FK)
Project ---(N:1)--→ Product (via product_id FK)
```

This forms a loop in the entity relationship diagram: Product → Feature → WorkItem → Project → Product. But it's not a problematic cycle because:

1. **Each edge is a different semantic relationship.** Product *owns* Features (composition). WorkItems *reference* Features (categorization). WorkItems *belong to* Projects (organizational). Projects *belong to* Products (organizational). No single FK chain creates a cascade loop.

2. **No mutual required FKs.** `feature_id` on WorkItem is nullable. `product_id` on Project is nullable. The graph has no mandatory cycle — you can have a WorkItem with no Feature, or a Project with no Product.

3. **Delete cascades don't loop.** Deleting a Product doesn't cascade through Feature → WorkItem → Project → back to Product, because `project_id` on WorkItem is a reference, not a cascade-delete FK. Define cascade behavior explicitly: Product delete should cascade to Features but NOT cascade through WorkItem to Project.

**One thing to be careful about**: if you implement cascade delete on Product → Feature and also cascade delete on Feature → WorkItem, deleting a Product would delete its Features and their WorkItems — even if those WorkItems belong to Projects under a different Product. This is probably not the desired behavior. I'd recommend:
- Product → Feature: CASCADE (Features are owned by Product)
- Feature → WorkItem: SET NULL on `feature_id` (WorkItems survive Feature deletion)
- Project → Product: SET NULL on `product_id` (Projects survive Product deletion)

### Q2: Nullable FK vs. junction table for Feature → WorkItem?

**Nullable FK is correct here.**

The relationship is categorization, not association: a WorkItem optionally *belongs to* a Feature. It's semantically 1:N (one Feature has many WorkItems), not M:N (a WorkItem doesn't belong to multiple Features simultaneously). A junction table would be over-engineering.

If the relationship ever becomes M:N (a WorkItem contributing to multiple Features), the same migration pattern from Q2 above applies — add junction table, migrate FK values, drop column.

### Q3: Does the existing `features` table need changes?

The current Feature dataclass has: `id`, `name`, `description`, `hypothesis`, `acceptance_criteria`, `status`, `product_id`, `created_at`, `updated_at`, plus relationships to dependencies, risks, and work_items.

For the bridge role, Feature needs `product_id` (already has it) and WorkItem needs `feature_id` (already has it in the domain model — check if it's in the DB schema too). If both FKs already exist in the database, the bridge is already structurally in place — you're just using it.

Verify: does the `features` table exist in the actual database, or is it only a domain model dataclass? If it's dataclass-only, you'll need an Alembic migration to create the table. The domain model shows `product_id` on Feature and `feature_id` on WorkItem, but the database may not have caught up.

---

## One Architectural Note

The PPM's hierarchy — Product → Feature → WorkItem → Project — implies a navigational path: "show me the product, its features, the work items for each feature, and which projects those work items are in." This is a useful PM view. But it's a query path, not a data dependency. The entities should be independently queryable (give me all WorkItems for Project X, regardless of Feature or Product). Make sure the repository layer supports both navigational and direct queries.

---

## Decision Summary

| Question | Answer | Notes |
|----------|--------|-------|
| `product_id` FK on projects | Approved | Comment noting PDR-003 M:N divergence and migration path |
| 1:N → M:N migration feasibility | Clean | Standard junction table migration, non-destructive |
| Products table schema | Approved | Check with PPM on missing vision/strategy fields |
| Circular dependency | None | Semantically distinct edges, no cascade loop |
| Feature → WorkItem cardinality | Nullable FK (correct) | 1:N is the right starting cardinality |
| Features table changes | Verify DB schema | Domain model has structure; confirm DB matches |

**Verdict**: Proceed with migrations.

---

*Chief Architect | March 23, 2026*
