# Memo: PPM Confirmation — Product Data Model Decisions

**To**: Lead Developer
**CC**: Chief Architect, PM
**From**: PPM
**Date**: 2026-03-23
**Re**: Confirming product concept decisions with Architect validation notes addressed
**Input**: `memo-arch-product-model-validation-2026-03-23.md`

---

## Status: All Decisions Confirmed — Proceed with Migrations

The Architect has validated both schema changes as architecturally sound. This memo confirms the PPM decisions, answers the Architect's open questions, and gives the Lead Dev a clean go-ahead.

---

## Decisions Confirmed

### Decision 1: Product as Umbrella
Confirmed as stated. No architectural questions raised.

### Decision 2: 1:N with Escape Hatch
Confirmed. The Architect's recommendation to comment the migration with the PDR-003 divergence note is adopted:

```python
# product_id is nullable FK (1:N) per PPM decision 2026-03-22.
# PDR-003 specifies M:N via product_projects junction table.
# Migration path: add junction table, migrate FK values, drop column.
```

The Architect also correctly notes: keep Product ↔ Project queries in the repository layer so the migration surface is contained when M:N arrives. Lead Dev should enforce this during implementation.

### Decision 3: Simplified Lifecycle
Confirmed: PLANNING → ACTIVE → MAINTENANCE → SUNSET → ARCHIVED (5 states).

### Decision 4: Feature as Bridge
Confirmed. The Architect's cascade behavior recommendation is adopted:

| Relationship | Cascade Behavior | Rationale |
|-------------|-----------------|-----------|
| Product → Feature | CASCADE | Features are owned by Product |
| Feature → WorkItem | SET NULL on `feature_id` | WorkItems survive Feature deletion — they're real work |
| Project → Product | SET NULL on `product_id` | Projects survive Product deletion |

This prevents the scenario the Architect flagged: deleting a Product should not cascade through Feature → WorkItem and destroy work items that belong to projects under a different Product.

**Lead Dev action**: Verify whether the `features` table exists in the actual database or is dataclass-only. If dataclass-only, create the Alembic migration. The domain model has the structure; the DB may not.

### Decision 5: Navigation
**Under revision.** The CXO recommended Option B (product as section within Projects) over my original Option A (first-class nav). I've accepted the CXO's emergence insight but identified a gap in the model — see separate memo to CXO. A revised Decision 5 will follow once the CXO responds. This does not block the data model work.

---

## Architect's Open Questions — PPM Answers

**Q: Are missing `vision` and `strategy` fields intentional?**

Yes, intentional. Lean Product entity for M2. The domain model dataclass can carry `vision` and `strategy` as in-memory fields; the database schema starts minimal. We add columns when there's a demonstrated user need for persisting these fields, not preemptively. This follows the same Gall's Law principle we applied to onboarding — start simple, add when demand is clear.

**Q: `is_default` field on Product?**

Not for M2. PDR-003's emergence principle is relevant here — products emerge from projects, and a "default product" implies the opposite (projects auto-associate upward). If users signal that they want unassigned projects to auto-group, we can add `is_default` later. For now, `product_id = NULL` on a project simply means "not yet associated with a product."

---

## Summary for Lead Dev

You have green lights on everything except Decision 5 (navigation), which is under discussion and doesn't block schema work. Proceed with:

1. Create `products` table: `id`, `name`, `description`, `lifecycle_state` (enum), `owner_id`, `created_at`, `updated_at`
2. Add nullable `product_id` FK to `projects` table with PDR-003 divergence comment
3. Verify `features` table exists in DB; create if needed
4. Add nullable `feature_id` FK to `work_items` table
5. Set cascade behavior per the table above
6. Keep Product ↔ Project queries in the repository layer

---

*PPM Confirmation | March 23, 2026*
