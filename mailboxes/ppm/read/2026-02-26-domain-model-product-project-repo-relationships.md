# Memo: Domain Model — Product, Project, and Repository Relationships

**From**: Lead Developer (Claude Code / Opus)
**To**: CXO, PPO
**CC**: PPM (for awareness)
**Date**: 2026-02-26
**Re**: Architectural gap in entity relationships — requesting product design guidance
**Context**: Discovered during #848 (GitHub connection to projects) implementation

---

*Copy of memo sent to CXO and PPO mailboxes. See `mailboxes/cxo/inbox/2026-02-26-domain-model-product-project-repo-relationships.md` for full content.*

## TL;DR

Two domain model gaps found during #848 work:

1. **Repository is not a first-class entity** — currently trapped as a config field inside ProjectIntegration with a required project_id FK. Doesn't support many-to-many (project ↔ repo), standalone repos, or shared repos across projects.

2. **Product ↔ Project have zero relationship** — both entities exist in the domain model since day one but are completely unlinked. No FK, no join table.

PM (xian) flagged both during #861 audit cascade. Memo asks CXO/PPO for product design guidance on where/when to surface these in the user experience.

Current #848 work can proceed with minimal fixes. Not blocking.
