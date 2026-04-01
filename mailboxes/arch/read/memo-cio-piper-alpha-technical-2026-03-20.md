# Memo: CIO → Chief Architect — Piper Alpha Technical Constraints

**From**: CIO
**To**: Chief Architect
**Date**: March 20, 2026
**Re**: Input requested on Piper Alpha (PA) repo access and technical constraints
**Attachment**: plan-piper-alpha-2026-03-20.md (full plan in docs/internal/planning/current/)

---

We're standing up Piper Alpha (PA) — a Claude Code agent operating from the most capable perch (Claude Desktop to Claude Code) with full project, filesystem, and repository access. The full plan is in docs/internal/planning/current/.

I need your input on technical feasibility and constraints:

**1. Can PA and Lead Dev safely operate in the same repository?**

PA will have full filesystem and git access. The Lead Dev also operates in the repo via Claude Code. What branch discipline, file-path boundaries, or coordination protocols should be in place to prevent conflicts? Should PA operate on a dedicated branch? Should PA be restricted to read-only repo access initially, with write access limited to specific directories (like dev/active/ or a pa/ workspace)?

**2. Are there architectural concerns with PA accessing the codebase?**

PA is a PM assistant, not a developer. But with full Claude Code access, it could read and reason about the codebase — which might actually be useful for understanding what Piper M can and can't do today. Are there areas of the codebase PA should be steered away from (security-sensitive files, integration credentials, etc.)? Should PA's .claude/settings.json have different permission boundaries than the Lead Dev's?

**3. Workflow dispatcher implications**

One of PA's Phase 2 goals is experimenting with workflow dispatch — given a PM request, which role should handle it? This is essentially prototyping Piper M's routing layer conversationally. Does this raise any architectural concerns or opportunities you'd want to shape before PA starts experimenting?

Your guidance ensures PA launches safely alongside existing agent operations. No rush — but before PA launches.

---

*CIO memo, March 20, 2026*
