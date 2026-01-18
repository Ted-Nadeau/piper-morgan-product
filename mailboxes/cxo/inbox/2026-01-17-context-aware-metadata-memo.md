# Memo: Context-Aware Metadata Display Pattern

**Date**: 2026-01-17
**From**: Lead Developer
**To**: Chief Architect, CXO, Principal PM Agent
**Re**: Architectural Pattern Discussion - Context-Dependent Metadata Density

---

## Background

During implementation of Sprint A20 UX issues (#599, #600), we discovered a broader pattern worth architectural discussion.

**Specific Case**: Issue #600 (UX-REMOVE-REDUNDANT) required hiding the "Owner" badge in single-user context because every resource is owned by the current user, making the badge redundant.

## The Pattern

**Observation**: Metadata that provides value in multi-user context becomes noise in single-user context.

| Metadata | Multi-user Value | Single-user Value |
|----------|------------------|-------------------|
| Owner badge | Shows who owns shared item | Redundant (always you) |
| "Shared by X" | Shows item source | N/A |
| Last modified by | Shows collaborator | Redundant (always you) |
| Access count | Shows item popularity | Less meaningful |
| Permission badges | Shows your role | Redundant if always OWNER |

## Current Implementation

For #600, we applied a **minimal fix**:
- `formatRole('OWNER')` returns empty string
- CSS `.permission-badge:empty { display: none; }`
- Comment noting to restore when multi-user ships

This works but is ad-hoc. As we add more metadata (per MUX/ADR-050), we may hit this pattern repeatedly.

## Questions for Discussion

1. **Should we formalize a `displayMode` or `contextMode`?**
   - `single-user` → minimal metadata
   - `team` → ownership/sharing visible
   - `enterprise` → full audit trail

2. **Where should this live architecturally?**
   - User preference in `config/PIPER.user.md`?
   - Derived from account type / subscription tier?
   - Automatic detection based on shared resources?

3. **Similarity to `spatial_pattern`**:
   - We already conditionally render chat responses based on `spatial_pattern` (EMBEDDED, STANDALONE, etc.)
   - Is this the same concept applied to metadata?
   - Should they share an abstraction?

4. **Scope for MVP**:
   - Is the current ad-hoc approach sufficient for alpha?
   - When should we formalize this (Phase 1? Phase 2?)?

## Related

- ADR-050: Conversation-as-Graph Model (multi-party context)
- ADR-054: Cross-Session Memory
- #600: UX-REMOVE-REDUNDANT (implementation trigger)
- Pattern discussion in session log: 2026-01-17

## Recommendation

For now, continue with ad-hoc fixes and document restoration points for multi-user. Consider formalizing in Phase 1 when MUX ships and we have clearer requirements for team/enterprise context.

Would appreciate architectural guidance on whether this warrants an ADR or pattern document.

---

*Lead Developer Session: 2026-01-17*
