# Memo: Domain Model — Product, Project, and Repository Relationships

**From**: Lead Developer (Claude Code / Opus)
**To**: CXO, PPO
**Date**: 2026-02-26
**Re**: Architectural gap in entity relationships — requesting product design guidance
**Context**: Discovered during #848 (GitHub connection to projects) implementation

---

## Summary

While building the project-repo linking infrastructure (#848 mini-epic), we identified two domain model gaps that need product design guidance before we build further UI on top of them.

## Gap 1: Repository as a First-Class Entity

**Current model**: A GitHub repository is stored as a `config` field inside `ProjectIntegration`, which has a required `project_id` FK. This means:
- A repository **cannot exist** without being attached to a project
- A repository **cannot be shared** across projects (without duplicating the integration row)
- The API currently **blocks** multiple GitHub repos per project (409 duplicate check)

**Real-world reality**: Piper Morgan itself has a product repo and a separate website repo. Customers will have similar patterns:
- One project may have multiple repos (frontend, backend, docs)
- Two projects may reference the same repo (shared library, monorepo)
- A user may want to register a repo before deciding which project it belongs to

**Question for product design**: Should we introduce Repository as an independent, first-class entity with many-to-many links to Projects? If so, where in the user journey do we surface repo management (onboarding, settings, conversational, all three)?

## Gap 2: Product ↔ Project Relationship

**Current model**: Both `Product` and `Project` exist in the domain model (since day one), but they have **zero relationship** to each other — no FK, no join table, no reference in either direction.

- `Product` (domain: `services/domain/models.py:182-197`, DB: `services/database/models.py:273-291`) — has name, vision, strategy, features, stakeholders, metrics, work_items
- `Project` (domain: `services/domain/models.py:345-419`, DB: `services/database/models.py:503-565`) — has owner, name, integrations, shared_with, lifecycle_state

**Real-world reality**: Products and projects have a many-to-many relationship:
- A product may have zero, one, or many projects (e.g., "Piper Morgan" product → main repo project, website project, docs project)
- A project may involve zero, one, or more products (e.g., a shared infrastructure project serves multiple products)

**Question for product design**: Where and when should Piper ask about the customer's product(s)?
- During onboarding (setup wizard)?
- In settings (post-setup)?
- Conversationally (Piper notices project patterns and suggests product groupings)?
- All of the above at different depths?

## Impact on Current Work

The #848 mini-epic children (#861 Settings UI, #862 Conversational Handler, #863 Portfolio Onboarding) can proceed with the current `ProjectIntegration` model as-is, with a minor fix to allow multiple repos per project. But the UI patterns we build now will need to evolve once the entity relationships are properly modeled.

We can ship incrementally — the current model works for the common case (one project, one repo) — but the PM has flagged that we should design for the many-to-many reality from the start, even if we build it progressively.

## Requested Guidance

1. **Repository entity**: Should we create a proper `Repository` entity now, or continue with `ProjectIntegration` and refactor later?
2. **Product ↔ Project**: When should this relationship be introduced in the user experience? What's the MVP scope?
3. **Onboarding flow**: Should the setup wizard ask about products, or is that a post-MVP concern?

---

*Filed during #848 implementation. No blocking action required — current work can proceed with minimal fixes. This memo is for strategic product design alignment.*
