# Product Concept Model

**Issue**: #717 MUX-PRODUCT-MODELING
**Parent**: #706 MUX-OBJECTS-VIEWS
**Created**: 2026-03-23
**Authors**: PPM (decisions), Chief Architect (validation), CXO (navigation), Lead Developer (documentation)
**Status**: Approved — ready for M2 implementation

---

## What Is a Product?

A Product is the highest-level organizing concept in Piper Morgan. It represents something a PM is building and shipping — a software product, a service, a platform. Products contain Features (capabilities being built) and are served by Projects (work containers).

**Product is an umbrella, not a project.** A project is a bounded effort with a start and end. A product is an ongoing entity that persists across projects. "Piper Morgan" is a product. "M1 Sprint," "Website Redesign," and "Alpha Program" are projects that serve it.

**Source**: PPM Decision 1, validated by Chief Architect (2026-03-23).

---

## Relationships

### Product ↔ Project: One-to-Many (with escape hatch)

A Product has many Projects. A Project belongs to one Product (nullable — not all projects need product association).

```
Product "Piper Morgan"
  ├── Project: M1 Sprint
  ├── Project: Website Redesign
  ├── Project: Alpha Program
  └── Project: Content Pipeline
```

**Implementation**: Nullable `product_id` FK on the `projects` table.

**Why 1:N and not M:N**: PDR-003 specifies M:N, but the current user base (Solo PM, Startup PM archetypes) doesn't need shared projects across products. Starting with 1:N follows Gall's Law — simple system that works, with a documented migration path to M:N.

**Migration path to M:N**: Create `product_projects` junction table → migrate FK values → drop `product_id` column. Non-destructive, standard relational migration. All Product ↔ Project queries must be kept in the repository layer to contain the migration surface.

**PDR-003 divergence**: Documented in the Alembic migration per Chief Architect recommendation.

**Source**: PPM Decision 2, Architect validation Q1-Q2.

### Product ↔ Feature: One-to-Many (composition)

A Product owns its Features. Features are the capabilities being built within a product.

```
Product "Piper Morgan"
  ├── Feature: Conversational Floor
  ├── Feature: GitHub Integration
  ├── Feature: Todo Management
  └── Feature: Reminder System
```

**Implementation**: `product_id` FK on the `features` table (already exists in domain model).

**Cascade**: Deleting a Product deletes its Features (CASCADE). Features are compositionally owned by the Product.

**Source**: PPM Decision 4, Architect validation.

### Feature ↔ WorkItem: One-to-Many (categorization)

A Feature categorizes WorkItems. A WorkItem optionally belongs to a Feature.

```
Feature: Todo Management
  ├── WorkItem: #904 Todo Completion Lifecycle
  ├── WorkItem: #903 Basic Reminder System
  └── WorkItem: #285 Core Alpha Todo
```

**Implementation**: Nullable `feature_id` FK on the `work_items` table.

**Cascade**: Deleting a Feature sets `feature_id` to NULL on its WorkItems (SET NULL). WorkItems are real work that survives organizational restructuring.

**Source**: PPM Decision 4, Architect validation Q1-Q2.

### Full Hierarchy

```
Product → Feature → WorkItem → Project → Product
```

This forms a navigational loop in the entity graph, but **not a problematic cycle**:
- Each edge is a semantically distinct relationship (ownership, categorization, organizational membership)
- No mutual required FKs (all nullable)
- No cascade loop (Product→Feature CASCADE, Feature→WorkItem SET NULL, Project→Product SET NULL)

**Source**: Architect validation, Decision 4 Q1.

---

## Lifecycle

Products have a 5-state lifecycle:

| State | Meaning |
|-------|---------|
| **PLANNING** | Product is being conceived, not yet in active development |
| **ACTIVE** | Product is being actively built and/or shipped |
| **MAINTENANCE** | Product is stable, only receiving bug fixes and minor updates |
| **SUNSET** | Product is being wound down, approaching end-of-life |
| **ARCHIVED** | Product is no longer active, retained for historical reference |

**Implementation**: `lifecycle_state` enum column on the `products` table.

**Source**: PPM Decision 3.

---

## Database Schema (M2)

### New: `products` table

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID (PK) | |
| `name` | String (required) | |
| `description` | Text (nullable) | |
| `lifecycle_state` | Enum | PLANNING, ACTIVE, MAINTENANCE, SUNSET, ARCHIVED |
| `owner_id` | UUID (FK → users) | SEC-RBAC Phase 3 pattern |
| `created_at` | DateTime (UTC) | |
| `updated_at` | DateTime (UTC) | |

**Intentionally omitted**: `vision`, `strategy` (exist in domain model dataclass but not persisted in DB for M2. Add when user need is demonstrated. Per PPM: lean entity, Gall's Law.)

**Intentionally omitted**: `is_default` (PDR-003 emergence principle — products don't auto-capture unassigned projects.)

### Modified: `projects` table

Add: `product_id` UUID (nullable FK → products, SET NULL on delete)

```python
# product_id is nullable FK (1:N) per PPM decision 2026-03-22.
# PDR-003 specifies M:N via product_projects junction table.
# Migration path: add junction table, migrate FK values, drop column.
```

### Modified: `work_items` table (or equivalent)

Add: `feature_id` UUID (nullable FK → features, SET NULL on delete)

### Verify: `features` table

The `Feature` domain model dataclass exists with `product_id`, `lifecycle_state`, and relationships. **Lead Dev must verify whether a corresponding database table exists.** If not, create it as part of the M2 migration.

---

## Navigation (UI)

### Decision: Option B with orchestration path

Product appears as a **grouping context within the Projects view**, not as a top-level navigation item. Clickable product headers lead to a Product detail view.

**Two mental models accommodated**:

| Mental Model | User Behavior | Navigation Path |
|-------------|---------------|-----------------|
| **Emergence** (bottom-up) | "I started with projects; product structure emerged" | Projects view → notices product grouping |
| **Orchestration** (top-down) | "I have a product; I'm creating projects to serve it" | Projects view → clicks product header → Product detail |

**Single-product user**: Product header visible but unobtrusive. No interaction required.

**Multi-product user**: Product headers become meaningful groupings. Filter/collapse by product.

**Growth path**: If multi-product users signal frequent product-context switching, Product can be promoted to a top-level nav item. Signal-driven, not launch decision.

**Outstanding design question** (PPM → CXO): Prominence of product header for single-product users (visible header, collapsed, or breadcrumb). Does not block schema or implementation.

**Chat access**: "What products am I working on?" works via intent classification regardless of nav placement.

**Source**: CXO recommendation (Option B), PPM revision (two-models), PM endorsement.

---

## What This Unblocks

- **#716**: Features View — can now implement because Product → Feature relationship is defined
- **#706**: Objects & Views Discovery — Product is the missing piece in the object catalog
- **M2 implementation**: Schema migrations, repository layer, chat integration, UI views

---

## References

| Document | Role |
|----------|------|
| PPM memo: Product concept decisions (2026-03-22) | Original 5 decisions |
| Architect memo: Data model validation (2026-03-23) | Schema approval + cascade behavior |
| CXO memo: Navigation hierarchy (2026-03-23) | Option B recommendation |
| PPM memo: Two mental models (2026-03-23) | Revised Decision 5 |
| PPM memo: Model confirmation (2026-03-23) | Final go-ahead |
| PDR-003: Entity Concept Model | Architectural reference |
| ADR-059: Workflow Dispatcher | Gall's Law precedent |
