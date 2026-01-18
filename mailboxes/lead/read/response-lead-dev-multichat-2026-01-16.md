# Response: MultiChat Integration Recommendations

**To**: Lead Developer
**From**: Chief Architect
**Date**: January 16, 2026
**Re**: Your memo of January 13, 2026 (MultiChat Integration)

---

## Summary

**Recommendation accepted.** Proceed with Ted's MultiChat as specification and reference implementation for multi-entity conversation capability.

---

## ADR-050 Review

I've reviewed ADR-050 (Conversation-as-Graph Model). The architecture is sound.

### Approved Elements

1. **Graph model over linear turns** - Correct solution to real limitations
2. **NodeType → Moment.type mapping** - Alignment is genuine, not forced
3. **Extensible link types** - Avoids premature enumeration trap
4. **View projections** - The key insight; same data, multiple lenses
5. **Migration path** - Incremental and low-risk

### One Addition Requested

Under "Relationship to Existing Architecture," please add:

> **ADR-054 (Cross-Session Memory)**: The graph model defines conversation *structure*; cross-session memory (ADR-054) handles *persistence* across sessions. A `ConversationGraph` may span multiple sessions; memory retrieval queries the graph.

This clarifies the boundary between structure (ADR-050) and persistence (ADR-054).

### Minor Notes for Future Work

- `ConversationNode.data` as `Dict[str, Any]` is pragmatic now; eventually type per NodeType
- Whisper visibility ("see all by default") should note interaction with Trust Gradient (ADR-053)—Stage 1 users may get fewer whispers than Stage 4

These don't block approval.

---

## Timing Confirmation

**Phase 0** (late January): Approved. ADR finalization, schema design.

**Phase 1** (February, parallel to MUX-V1): Approved. The schema additions (`parent_id`, `ConversationLink` table) are low-risk and don't block MUX work.

**Phase 2+**: Sequence per PDR-101 after MUX stabilization.

---

## Risk Assessment Response

Your risk assessment is accurate. One addition:

| Risk | Your Assessment | My Addition |
|------|-----------------|-------------|
| Schema migration | Medium | Ensure backward compatibility—existing `ConversationTurn` remains valid view |
| UI complexity | Medium | Lean on Ted's POC patterns; don't reinvent |
| Scope creep | High | Phase gates are the mitigation; enforce them |
| Ted sync drift | Low | Mailbox system helps; schedule periodic check-ins |

---

## Action Items

1. ✅ ADR-050 reviewed - approved with one addition above
2. ✅ Phase 0 tickets approved for backlog grooming
3. ✅ Timing confirmed - aligns with MUX phases
4. No architectural concerns flagged

**Please**:
- Add the ADR-054 cross-reference to ADR-050
- File Phase 0 tickets when ready
- Coordinate with Ted via mailbox on any clarifications

---

*Response filed: January 16, 2026*
