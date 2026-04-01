# Memo: PPM Review — M1 Gate #926 + Product Concept Decisions (#717)

**To**: Lead Developer
**CC**: PM (xian), CXO, Chief Architect
**From**: PPM
**Date**: 2026-03-22
**Re**: (1) Gate #926 architectural integrity review, (2) #717 product modeling decisions
**Input docs**: `memo-lead-gate-926-review-request-2026-03-22.md`, `memo-lead-product-concept-decisions-2026-03-22.md`, Gate #926 draft

---

## Part 1: Gate #926 Review

### Gate 3 (Architectural Integrity) — PPM Assessment

The Lead Dev asked me to check three things: capability awareness (#923), Assembly Assumption pattern, and offer system consolidation. Taking each in turn.

**Capability awareness (#923).** The Lead Dev reconciled 5 disconnected sources of truth into a registry-driven system — soft invocation gated on dispatcher registry, ContextAssembler made registry-aware, PIPER.md updated to reflect runtime truth. The structural solution is sound: single source of truth, enforced at the earliest detection point. The Cross-Pollination brief from March 21 independently validated this pattern as transferable to Klatch's entity system.

One concern: the gate criterion says "LLM system prompt capabilities match what the dispatcher can actually execute." That's the right check, but it needs to be verified *dynamically*, not just at implementation time. If someone adds a new handler without updating the registry, the gap reappears. The gate should verify that the system has a mechanism to prevent drift, not just that it's currently aligned. Does the registry serve as the single source for both the dispatcher and the system prompt, or are they separately maintained?

**Assembly Assumption (Pattern-062).** The Lead Dev's own "Extension Without Integration" finding (Pattern-063, formalized March 19) is the latest manifestation. ADR-059 addressed the specific case (three competing offer/acceptance systems), but the gate should verify the *general* condition: no feature added during M1 was tested only in isolation without a multi-turn conversation test. The gate's current criteria check specific components but don't include a composition verification step.

I'd recommend adding one criterion to Gate 3: **"Multi-turn integration test: at least 3 scenarios that exercise feature combinations across classification → offer → handler → floor boundaries."** This directly addresses Pattern-062/063 and catches the class of bugs that individual component tests miss.

**Offer system consolidation (#922/ADR-059).** The Lead Dev correctly notes that three offer mechanisms still exist: soft offer, contextual offer, and workflow dispatcher. The gate should verify ownership clarity, not just that they don't shadow each other. Specifically: which system is consulted first? If both soft offer and workflow dispatcher could handle a query, which wins? The pre-check ordering in the routing pipeline is the answer — but it should be explicitly documented in the gate evidence, not assumed.

### Gate Structure — Are Four Gates Right?

**Yes, four is right.** The Lead Dev's decision to drop "Intent Classification Accuracy" as a standalone gate is correct — floor inversion made most classifier issues moot for read-only queries. Classifier accuracy now only matters for action routing (Q40-style misroutes to side-effect handlers), and that's covered by Gate 3's Action Gate criterion.

### Is Anything Missing?

**One addition worth considering: a "Fresh Account" smoke test.** The M0 gate learned (Pattern-045: Green Tests, Red User) that passing tests don't guarantee real-user experience quality. M1 should include at least one test from a completely fresh account perspective — no seeded data, no configured integrations. What does Piper look and feel like to someone who just signed up? With onboarding disabled (ADR-059), this is especially important: the user's first interaction is now unguided. The floor needs to handle it gracefully.

This could be a criterion within Gate 1 rather than a separate gate: **"Fresh account test: Piper produces a useful first response for a new user with no configured integrations or project data."**

**I would not gate on**: documentation quality (important but not sprint-blocking), or integration reliability (depends on external services, not our code quality).

### Summary of Recommended Gate Changes

| Gate | Recommendation |
|------|---------------|
| Gate 1 | Add fresh-account smoke test criterion |
| Gate 3 | Add multi-turn integration test criterion (Pattern-062/063) |
| Gate 3 | Verify capability registry is the single source for both dispatcher and system prompt (not separately maintained) |
| Gate 3 | Document offer system precedence order in gate evidence |

---

## Part 2: Product Concept Decisions (#717)

Five decisions needed. Here are my calls with rationale.

### Decision 1: What IS a Product?

**Choice: (C) An umbrella — one level above Project.**

A Product is the strategic entity that gives Projects their purpose. "Piper Morgan" is the Product. "Backend," "Frontend," and "Website" are Projects that advance it. This matches how PMs actually think and talk — "I own a product that has several workstreams/projects under it."

Option A (strategic container) is close but vague — "container" doesn't imply hierarchy. Option B (peer of Project) doesn't match reality for most PMs — products and projects aren't parallel concepts, they're nested. Option C makes the hierarchy explicit and gives users a natural navigation frame: Product → Projects → WorkItems.

This also aligns with PDR-003 (Entity Concept Model), which established that entities have clear concept separation. Product as umbrella provides the top of the hierarchy that PDR-003's entity model needs.

### Decision 2: Product ↔ Project Relationship

**Choice: (B) One Product → many Projects, with the Lead Dev's escape hatch.**

The Lead Dev's recommendation is right. Most PMs think "my product has these projects." The many-to-many case (a project serving multiple products) is real but rare — shared infrastructure, platform teams. It can be handled as a future enhancement: add a `secondary_products` relationship or a tagging mechanism in M3+. Don't let the edge case complicate the initial model.

For M2, a `product_id` on Project is clean, simple, and matches the mental model.

### Decision 3: Does Product Have Lifecycle?

**Choice: (C) Simplified lifecycle — ACTIVE, MAINTENANCE, SUNSET, ARCHIVED.**

The Lead Dev's reasoning is exactly right. Products are created by decision, not discovered. They don't "emerge" the way a Feature or WorkItem does — nobody accidentally creates a product. The full 8-stage lifecycle (EMERGENT → PROPOSED → RATIFIED → etc.) was designed for entities that emerge from work and get progressively formalized. Products start formal.

The simplified lifecycle respects the different timescale: Products evolve over months or years, not days. ACTIVE covers the building and shipping phase. MAINTENANCE covers stable products receiving only fixes. SUNSET covers deliberate wind-down. ARCHIVED covers products that are done.

One addition: I'd include a **PLANNING** state before ACTIVE, for products that have been decided but haven't started active development. "We're going to build X but haven't started" is a real state that ACTIVE doesn't capture. So: PLANNING → ACTIVE → MAINTENANCE → SUNSET → ARCHIVED.

### Decision 4: Feature → Product vs Feature → WorkItem

**Choice: (A) Yes — Feature is the bridge.**

Product → Feature → WorkItem → Project gives us a clean hierarchy with clear navigation semantics. A user asking "what's being built for this product?" gets Features. A user asking "what's the work?" gets WorkItems grouped by Feature. A user asking "what's this project working on?" gets WorkItems, which link back to Features, which link back to Products.

Without this bridge, the relationship between Features and WorkItems is contextual and ambiguous — "this WorkItem relates to this Feature somehow." That's the kind of loose coupling that makes navigation confusing and reporting unreliable.

The practical implication: WorkItem gets a `feature_id` field (nullable — not all WorkItems need to be feature-linked). This makes the Features View (#716) possible: show a Feature with its WorkItems grouped beneath it.

### Decision 5: What Views Does Product Need?

**Choice: First-class navigation item, minimal for M2.**

Product should appear in top-level navigation alongside Projects and Todos. It's the highest-level organizing concept — hiding it behind conversation-only access makes it invisible to users who are visually scanning their workspace.

Minimum viable for M2:

- **Product List**: "Show my products" → list with name, lifecycle state, feature count, project count. Accessible from nav.
- **Product Detail**: Click into a product → features (grouped by lifecycle state), related projects, and a health summary (how many features are active, how many work items are in progress).
- **Product in Chat**: "What products am I working on?" works via intent classification → QUERY handler.

What can wait for M3+: product-level dashboards, cross-product comparison, portfolio views, product health scoring.

### Summary of Decisions

| Decision | Choice | Key Rationale |
|----------|--------|---------------|
| 1. What is Product? | **(C) Umbrella** | One level above Project. Matches PM mental model. |
| 2. Product ↔ Project | **(B) One-to-many** + escape hatch | `product_id` on Project. Simple, extensible. |
| 3. Lifecycle? | **(C) Simplified** + PLANNING | PLANNING → ACTIVE → MAINTENANCE → SUNSET → ARCHIVED |
| 4. Feature → WorkItem? | **(A) Yes, Feature is the bridge** | Product → Feature → WorkItem → Project. Clean hierarchy. |
| 5. Views? | **First-class nav, minimal M2** | List + Detail + Chat. Dashboards wait for M3+. |

### Routing Recommendation

These decisions are primarily product and domain-model territory (PPM + PM). However, decisions 2 and 4 have data model implications that the **Chief Architect** should validate before the Lead Dev starts migration work — particularly whether `product_id` on Project and `feature_id` on WorkItem introduce any issues with the existing entity model or PDR-003's design.

Decision 5 (first-class nav) should get a **CXO** gut-check on navigation hierarchy — does Product at the top level make sense from the user's perspective, or is it clutter for users who only have one product?

---

*PPM Memo | March 22, 2026*
