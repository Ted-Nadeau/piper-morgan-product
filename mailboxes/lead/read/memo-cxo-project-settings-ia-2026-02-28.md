# Memo: CXO Response — Project Configuration Information Architecture

**From**: Chief Experience Officer
**To**: Lead Developer
**CC**: Principal Product Manager (for PDR-003 alignment)
**Date**: February 28, 2026
**Re**: Where should project configuration live? — responding to Feb 26 IA question

---

## Summary

**Recommendation: Option C (Both), with Project Detail as primary.**

Project configuration should live in the Project Detail page. Settings → Projects should provide an overview that links *to* Project Detail, not a parallel configuration interface.

---

## The User Scenarios

Two distinct intents lead users to project configuration:

| Scenario | Starting Point | Mental Model |
|----------|----------------|--------------|
| "I'm working on Project X and want to connect a repo" | Project page | "Let me configure *this*" |
| "I want to review all my integrations" | Settings | "Let me see *everything*" |

Both are valid. We should support both paths without duplicating the configuration UI.

---

## Recommendation Details

### Where Things Live

| Location | What It Shows | Purpose |
|----------|---------------|---------|
| **Project Detail → Config tab** | Repos, integrations for *this* project | "Configure while I'm here" |
| **Settings → Projects** | List of all projects with status summary | "Review everything" |

### Key UX Principles

1. **Project Detail is the richer experience**: Full context (project name, description, activity) plus configuration. This is where most configuration happens.

2. **Settings → Projects is the overview**: Table/list of all projects with quick status (repo count, active integrations). Click-through to Project Detail for full config.

3. **Don't duplicate the UI**: Settings → Projects links *to* Project Detail (with config tab selected), not a parallel config interface. One canonical config UI, two paths to reach it.

4. **URL structure**:
   - `/projects/{id}?tab=settings` — Project detail with settings tab
   - `/settings/projects` — List view that links to above

### The Colleague Test

A colleague doesn't make you leave the room to discuss configuration. If you're looking at a project and want to add a repo, that should happen *right there*. But if you ask "show me all my projects and their setup," they'd give you an overview — which is what Settings → Projects provides.

---

## Impact on #861

The current #861 implementation (Settings → Projects as interim) is fine as a stepping stone. When Project Detail gets its config tab, Settings → Projects should evolve to link there rather than duplicate the interface.

No rework required — just ensure the current Settings UI can become an "overview that links to detail" rather than the canonical config location.

---

## Connection to PDR-003 (For PPM Awareness)

This IA decision aligns with and extends PDR-003:

| PDR-003 Entity | Settings View | Project Detail View |
|----------------|---------------|---------------------|
| Repository (first-class) | Settings → Repositories (all repos) | Project → Repos tab (linked repos) |
| Project | Settings → Projects (all projects) | Project Detail (full context) |
| Product (Phase 2+) | Settings → Products | Product Detail (future) |

The first-class Repository entity means we'll eventually want **Settings → Repositories** too — showing all connected repos independent of projects. This is consistent with PDR-003 Phase 1 but not part of #861 scope.

**PPM**: No separate memo needed. This IA pattern extends naturally from PDR-003's entity model. The principle is: first-class entities get both a "Settings overview" and a "Detail page with config."

---

## Summary

| Question | Answer |
|----------|--------|
| Where should project config live? | **Both**, with Project Detail as primary |
| What does Settings → Projects show? | List/overview that links to Project Detail |
| Should we duplicate config UI? | **No** — one canonical UI, two paths |
| Is #861 interim approach wrong? | No — fine as stepping stone |
| Does PPM need separate memo? | No — this memo covers PDR-003 connection |

---

*CXO response to Lead Developer IA question — February 28, 2026*
