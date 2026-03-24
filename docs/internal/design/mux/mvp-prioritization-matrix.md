# MVP Prioritization Matrix

**Issue**: #706 MUX-OBJECTS-VIEWS (Phase 3)
**Created**: 2026-03-24
**Status**: Draft — needs PM review and product judgment calls

---

## Scoring Criteria

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **User Value** | 3x | Does a PM need this to do their job? |
| **Effort** | 2x | How much work to implement? (Low=3, Med=2, High=1) |
| **Dependencies** | 1x | Is infrastructure ready? (Ready=3, Partial=2, Missing=1) |

---

## Object × View Prioritization

### Tier 1: MVP Essential (M2)

Combinations that users will expect and that unblock the product narrative.

| Object | View | User Value | Effort | Dependencies | Score | Notes |
|--------|------|-----------|--------|-------------|-------|-------|
| **Product** | Projects list (grouping header) | 3 | 3 (UI only) | 3 (schema approved) | **24** | #717 decisions made, CXO nav approved |
| **Product** | Product detail (click-through) | 3 | 2 | 3 | **21** | Orchestration entry point |
| **Feature** | Product detail (nested list) | 2 | 2 | 2 (verify DB table) | **16** | Feature list within Product detail |
| **Todo** | Lifecycle indicators in Todos view | 2 | 3 (component exists) | 3 (lifecycle wired) | **21** | Just wire existing component |
| **Project** | Lifecycle indicators in Projects view | 2 | 3 | 3 | **21** | Same — wire existing component |

### Tier 2: High Value (M2-M3)

Meaningful but not blocking the core product experience.

| Object | View | User Value | Effort | Dependencies | Score | Notes |
|--------|------|-----------|--------|-------------|-------|-------|
| **WorkItem** | Project detail (linked items) | 2 | 2 | 3 | **17** | WorkItems already have lifecycle UI |
| **Repository** | Project detail (repo health) | 2 | 2 | 3 | **17** | GitHub integration exists |
| **Feature** | Feature detail page | 2 | 2 | 2 | **16** | New page, but model exists |
| **Conversation** | Conversation archive/search | 2 | 1 | 2 | **12** | Needs search infrastructure |
| **Place** | Calendar view | 2 | 1 | 2 | **12** | Depends on calendar integration maturity |

### Tier 3: Nice to Have (M3+)

Enhancement quality, not blocking anything.

| Object | View | User Value | Effort | Dependencies | Score | Notes |
|--------|------|-----------|--------|-------------|-------|-------|
| **KnowledgeNode** | Graph visualization | 1 | 1 | 2 | **9** | Complex rendering |
| **UserTrustProfile** | Trust dashboard | 1 | 2 | 3 | **13** | Internal diagnostic, not user-facing |
| **Document** | Document analysis improvements | 1 | 2 | 2 | **11** | Existing view adequate |
| **List** | List lifecycle/archiving | 1 | 2 | 2 | **11** | Low user demand signal |

---

## MVP Recommendation

### Must Ship (M2)

1. **Product entity in database** — migration ready, architect-approved
2. **Product grouping header in Projects view** — CXO Option B, visible header, lighter typography
3. **Product detail view** — accessible via header click, shows features + projects
4. **Lifecycle indicators on Todos and Projects** — components exist, just need wiring

### Should Ship (M2 stretch)

5. **Feature list within Product detail** — verify DB table exists first
6. **WorkItem lifecycle in Project detail** — already partially wired

### Defer

- Knowledge graph visualization (M3+)
- Calendar view (depends on integration)
- Conversation archive (search infrastructure needed)
- Trust dashboard (internal tool)

---

## PM Decisions (2026-03-24)

1. **Lifecycle indicators on Todos**: PENDING/COMPLETED status is sufficient for MVP. MUX lifecycle indicators deferred.

2. **Feature detail**: Start as expandable section within Product detail. Graduate to dedicated page when user signal justifies it (same pattern as Product nav promotion).

3. **Product detail scope**: Full scope defined below with MVP minimum, ranked stretch, and deferred items.

---

## Product Detail View — Full Scope

### MVP Minimum (Must ship in M2)

| Element | Description | Effort |
|---------|-------------|--------|
| Product name + lifecycle state badge | Header with PLANNING/ACTIVE/etc. indicator | Small |
| Project list | Projects belonging to this product, with status/health | Small |
| Product description | Editable text field | Small |
| Breadcrumb navigation | Projects → [Product Name] | Small |

This is the "it exists and is useful" bar. A PM can see their product, its state, and its projects.

### Stretch Tier 1 (High value, do if time allows in M2)

| Rank | Element | Description | Effort | Signal to include |
|------|---------|-------------|--------|-------------------|
| S1 | Feature list (expandable) | Features grouped by lifecycle state, expandable to show work items | Medium | Core product-thinking feature |
| S2 | Project count + feature count summary | Quick stats in product header | Small | Low effort, high polish |
| S3 | Health summary | Derived from project/feature states — "2 active features, 1 at risk" | Medium | Requires health calculation logic |

### Stretch Tier 2 (Nice to have, M2 if everything else is done)

| Rank | Element | Description | Effort | Signal to include |
|------|---------|-------------|--------|-------------------|
| S4 | Work item counts per feature | "Feature X: 3 open, 2 closed" | Small | Needs feature→work item query |
| S5 | Product lifecycle state transition | UI to change state (PLANNING→ACTIVE, etc.) | Medium | Needs state machine + confirmation |
| S6 | Product edit form | Edit name, description, lifecycle inline | Medium | CRUD completeness |

### Deferred (M3+)

| Element | Reason |
|---------|--------|
| Feature detail as dedicated page | Wait for user signal that expandable section is insufficient |
| Feature risks and dependencies | Complex domain model, low alpha user need |
| Feature acceptance criteria editing | Needs rich text / checklist UI |
| Product health dashboard (portfolio-level) | Needs multiple products to be meaningful |
| Feature work item timeline | Needs temporal visualization infrastructure |

---

## Phasing Document

### M2: Product Foundation

**Must ship:**
1. Product entity in database (migration ready, architect-approved)
2. Product grouping header in Projects view (CXO Option B, visible, lighter typography)
3. Product detail view (MVP minimum: name, lifecycle, description, project list)
4. Chat access: "What products am I working on?" via intent classification

**Stretch (ranked):**
1. Feature list (expandable) within Product detail
2. Summary stats in product header
3. Health summary

### M2: Lifecycle Polish

**Must ship:**
1. Lifecycle indicators on Work Items (already wired)
2. Lifecycle indicators on Projects view (component exists, needs wiring)

**Deferred:**
- Lifecycle indicators on Todos (PENDING/COMPLETED status sufficient per PM)
- Lifecycle indicators on Features (wait for Feature list to ship first)

### M3+: Depth

- Feature detail as dedicated page (signal-driven promotion)
- Knowledge graph visualization
- Conversation archive and search
- Trust dashboard (internal diagnostic)
- Product portfolio view (multi-product users)

---

*Finalized with PM decisions 2026-03-24*
