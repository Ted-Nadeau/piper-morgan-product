# Architect Note: Entity Tokens in Response Templates

**From**: Lead Developer (M0 Sprint)
**To**: Chief Architect
**Date**: 2026-02-18
**Re**: Establishing a pattern for entity names in response templates
**GitHub Issue**: #818

---

## Context

During the anti-flattening audit for M0 (Sprint Gate #779, Gate 2), we examined parrot confirmation patterns — responses that echo user input verbatim.

Several handler responses include project names in output:
- "I couldn't find any projects matching '{search_terms}'"
- "I couldn't find a project called '{project_name}'"
- Confirmation: "Are you sure you want to delete '{project.name}'?"

## Assessment

These are **not** parrot confirmations. Project names are identifiers that shouldn't be paraphrased — they need to be echoed exactly so the user knows which entity is being referenced. This is similar to how a colleague would say "You mean the Henderson account?" not "You mean the thing you mentioned."

## Recommendation

Consider establishing a pattern/guideline for **entity tokens** in response templates:

1. **Entity names** (projects, people, meetings) should always be reflected exactly
2. This is distinct from echoing the user's full message as confirmation
3. Entity tokens may need special formatting (quotes, bold) to distinguish them from surrounding prose
4. This pattern should be documented so future Gate 2 audits don't flag it as parrot behavior

## Related

- PDR-002 Conversational Glue
- Pattern-045 Anti-Flattening
- M0 Sprint Gate #779

---

*Filed as architectural discussion item during M0 sprint gate verification.*
