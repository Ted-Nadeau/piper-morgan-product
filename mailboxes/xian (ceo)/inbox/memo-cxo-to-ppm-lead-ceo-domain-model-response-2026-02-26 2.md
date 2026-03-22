# Memo: CXO Response — Product, Project, and Repository Relationships

**From**: Chief Experience Officer
**To**: Principal Product Manager
**CC**: Lead Developer, PM
**Date**: February 26, 2026
**Re**: UX guidance on entity relationships — responding to Lead Dev memo
**Context**: Domain model gaps discovered during #848 implementation

---

## Summary Position

**Build the right domain model now. Surface it progressively in UX.**

The architecture should support the full many-to-many reality. But the user experience should introduce complexity only when users need it — starting simple, letting structure emerge through use.

---

## The Core UX Question

The technical question is "what entities exist and how do they relate?" But the UX question is: **What mental model do users bring, and how do we meet them where they are?**

Most PMs think in terms of:
- "The thing I'm shipping" (product)
- "The work I'm doing" (project)
- "Where the code lives" (repo)

But these map differently for different users:

| User Type | Mental Model |
|-----------|--------------|
| Solo PM | One product, one project, one repo — often treated as the same thing |
| Startup PM | One product, multiple projects (phases, streams), multiple repos |
| Enterprise PM | Multiple products, shared projects, shared repos, complex ownership |

**Design goal**: A model that works for all three without requiring the solo PM to understand enterprise complexity.

---

## Gap 1: Repository as First-Class Entity

### CXO Recommendation: Yes — implement now

**Rationale**: Users think of repos as independent things. "I want to connect my repo" is a natural utterance. "I want to connect my ProjectIntegration" is not.

The current model (repo as config inside ProjectIntegration) creates friction:
- Can't connect a repo without having a project first
- Can't share a repo across projects
- Forces artificial constraints that don't match user mental models

### UX Surfacing (Progressive Disclosure)

| Context | Behavior |
|---------|----------|
| **Onboarding** | "Want to connect a GitHub repo?" → Connect one, optionally link to project |
| **Settings** | Full repo management — see all connected repos, link/unlink from projects |
| **Conversational** | "Connect my frontend repo to the Piper Morgan project" → Piper handles it |
| **Project view** | "Repos" section showing linked repos with ability to add more |

### Key UX Principles

1. **You can connect a repo without having a project.** The repo exists independently.
2. **You can have a project without having a repo.** Not all projects involve code.
3. **The link between them is optional and many-to-many.** A repo can serve multiple projects; a project can have multiple repos.

### Default Behavior

When a user connects a repo *during* project setup, auto-link it to that project. But don't *require* the link — the user might be connecting a repo they'll use across multiple projects.

---

## Gap 2: Product ↔ Project Relationship

### CXO Recommendation: Introduce late, make optional, let Piper suggest

"Product" is a loaded term with different meanings across contexts. Forcing users to define it upfront adds friction without clear value for most users.

### Why Introduce Late?

- New users are overwhelmed by too many concepts at once
- Many users only have one "product" (even if they don't call it that)
- Forcing product definition upfront adds friction for unclear value
- The value of "product" as a concept is organizational, not functional

### Why Make It Optional?

- Solo PMs may never need the concept
- You can do everything with projects alone; products are for grouping
- Requiring products would break the "colleague" metaphor — a colleague doesn't ask you to define your org chart before helping

### Why Let Piper Suggest?

This is where the conversational glue vision applies:

- Piper observes patterns: "You have 3 projects that all seem related to Piper Morgan — want me to group them as a product?"
- This is colleague behavior: noticing patterns and offering to help organize
- It validates the concept through use: if users accept suggestions, the model is useful; if they decline, we learn

### UX Surfacing (Progressive)

| Phase | Behavior |
|-------|----------|
| **MVP (now)** | Product exists in domain model but is not surfaced in UI |
| **M1 or M2** | Settings page allows creating/editing products and linking projects |
| **Later** | Piper suggests product groupings conversationally |
| **Much later** | Onboarding asks "Are you working on one product or several?" — only if data shows it helps |

### The Emergence Principle

**Products emerge from projects, not the other way around.**

Let users start with the concrete (projects, repos) and discover the abstract (products) through use. Don't require them to define the container before they have something to put in it.

---

## Onboarding Flow Recommendation

### Don't ask about products in onboarding. Not yet.

**Current flow**: Account → Projects → (optionally) Integrations → Done

**Proposed evolution**:

| Step | Current | Near-term | Future |
|------|---------|-----------|--------|
| 1 | Account creation | Account creation | Account creation |
| 2 | "What projects?" | "What projects?" | "What are you working on?" (natural language) |
| 3 | Add integrations (optional) | "Connect repos?" (first-class) | Piper infers integrations from context |
| 4 | Done | Done | "These might be one product — want to group them?" (only if multiple projects) |

The near-term change is making repos first-class in the flow. Products come later, conversationally.

---

## Answering Lead Dev's Specific Questions

| Question | CXO Recommendation |
|----------|-------------------|
| Create Repository entity now or continue with ProjectIntegration? | **Now** — it's the right model and enables many-to-many cleanly |
| When introduce Product ↔ Project in UX? | **Late** — settings first (M1/M2), then conversational, then maybe onboarding |
| Should setup wizard ask about products? | **No** — not MVP, possibly not ever. Let products emerge from use. |

---

## Connection to Colleague Framing

The progressive disclosure approach aligns with how a human colleague would work:

- A colleague doesn't ask you to explain your entire organizational structure before helping you
- They start with what you're working on *right now*
- They learn the bigger picture over time
- They offer to help organize when they notice patterns

Piper should behave the same way: start with projects (the concrete), learn the relationships, and offer product-level organization when it would help — not before.

---

## For PPM Consideration

1. Does this phasing align with product strategy?
2. Are there user research signals suggesting earlier product introduction?
3. Any concerns about building the full domain model before surfacing it in UX?

---

*CXO response to Lead Developer memo dated February 26, 2026*
