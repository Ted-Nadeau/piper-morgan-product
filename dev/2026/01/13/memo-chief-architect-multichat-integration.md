# Memo: MultiChat Integration Recommendations

**To**: Chief Architect
**From**: Lead Developer
**Date**: January 13, 2026
**Re**: Ted Nadeau's MultiChat Repository Analysis and Integration Path

---

## Summary

I've completed analysis of Ted Nadeau's MultiChat repository (`external/ted-multichat/`). The repository contains a **comprehensive proof-of-concept** that directly implements the vision from PDR-101 (Multi-Entity Conversation Support).

**Recommendation**: Accept Ted's work as the **specification and reference implementation** for Piper's multi-entity conversation capability. Integration should follow PDR-101's Participant-First strategy, beginning after MUX-V1 stabilizes.

---

## Repository Contents

| Artifact | Size | Purpose |
|----------|------|---------|
| `multichat_prd_v1.md` | 80KB | Complete product requirements |
| `multichat_uiux_v1.md` | 37KB | Detailed UI/UX specifications |
| `project_architecture.md` | 5KB | Technical architecture guide |
| `poc/` | Next.js app | Working proof-of-concept |
| `use_cases/` | 5 scenarios | Validation scripts |
| `configuration_screens_spec.md` | 18KB | Agent/conversation config |

---

## Architectural Assessment

### Alignment with Existing Architecture

**Strong alignment with**:
- **ADR-046 (Moment.type)**: Ted's NodeTypes (message, task, whisper) map directly to Moment.types
- **ADR-045 (Object Model)**: Graph model extends "Entities experience Moments in Places" grammar
- **PDR-101**: POC implements exactly what PDR-101 describes

**New concepts requiring ADR**:
- **ConversationLink**: Explicit relationships between elements (I've drafted ADR-050)
- **Graph projections**: Multiple views over same data (timeline, thread, tasks)
- **Whispers**: Private AI suggestions per participant

### Technical Stack Assessment

Ted's POC uses Next.js 14 / TypeScript / React Context. **Do not merge this code** - the stack differs from Piper's Python/FastAPI backend.

**Instead**: Extract the data model and UI patterns. The POC serves as a reference implementation showing how the model works in practice.

---

## Proposed Integration Timing

Based on Roadmap v12.3:

| Phase | Timing | Rationale |
|-------|--------|-----------|
| **Phase 0** (Foundation) | Late January | After v0.8.4 stabilizes |
| **Phase 1** (Participant Mode) | February | Parallel to MUX-V1 |
| **Phase 2** (Host Mode) | March-April | After MUX integration |
| **Phase 3** (Personal Agents) | Post-beta | Feature expansion |

**Why not sooner**: MUX-V1 is the current priority. Multi-entity conversation builds on MUX's conceptual foundation (Object Model, Grammar). Starting Phase 1 infrastructure work in February allows parallel progress without blocking MUX.

---

## Deliverables Created

1. **ADR-050**: Conversation-as-Graph Model (`docs/internal/architecture/current/adrs/adr-050-conversation-as-graph-model.md`)
2. **Integration Gameplan**: 13 tickets across 3 phases (`dev/2026/01/13/gameplan-multichat-integration.md`)
3. **Session Log**: Full analysis trail (`dev/active/2026-01-13-1011-spec-code-opus-log.md`)

---

## Action Requested

1. **Review ADR-050** for architectural soundness
2. **Approve Phase 0** tickets for backlog grooming
3. **Confirm timing** alignment with MUX phases
4. **Flag any concerns** about graph model vs. existing conversation architecture

---

## Risk Assessment

| Risk | My Assessment | Mitigation |
|------|---------------|------------|
| Schema migration | Medium | Design backward-compatible migration; existing ConversationTurn remains valid |
| UI complexity | Medium | Incremental rollout; timeline view remains default |
| Scope creep | High | Strict phase gates per PDR-101 |
| Ted sync drift | Low | Active advisor mailbox; clear contribution path |

---

## Conclusion

Ted's MultiChat work is **exactly what PDR-101 envisioned**, implemented to production quality. The architecture aligns well with our existing patterns. I recommend proceeding with Phase 0 (ADR review, schema design) this month, Phase 1 (Participant Mode) in February, with Host Mode following MUX stabilization.

---

*Lead Developer | January 13, 2026*
