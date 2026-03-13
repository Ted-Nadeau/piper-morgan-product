# Gameplan: #431 MUX-VISION-LEARN

**Issue**: #431 MUX-VISION-LEARN: Learning System Experience Design
**Type**: Design Exploration
**Priority**: Medium-High
**Estimated Effort**: 16 hours (per issue)

---

## Overview

This is a **design specification task**, not a coding implementation. The goal is to produce 7 design documents that define how users experience Piper's learning system—translating the technical architecture (composting, lifecycle, journals) into user experience patterns.

**Core Question**: How do users EXPERIENCE Piper learning?

**Risks if not addressed**:
- Opaque improvement (Piper gets better but users don't see/trust)
- Creepy emergence (patterns surface without explanation)
- Missed engagement (learning could be interactive)

---

## Dependencies Verified

| Dependency | Status | Location |
|------------|--------|----------|
| ADR-045 Object Model | ✅ Exists | `docs/internal/architecture/current/adrs/adr-045-object-model.md` |
| Object Model Brief v2 | ✅ Exists | `dev/2025/11/29/object-model-brief-v2.md` |
| ADR-053 Trust Gradient | ✅ Exists | `docs/internal/architecture/current/adrs/adr-053-trust-computation-architecture.md` |
| ADR-055 Implementation | ✅ Complete (302 tests) | `docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md` |
| Composting Architecture | ✅ Exists | `docs/internal/architecture/current/composting-learning-architecture.md` |
| MUX-VISION-LEARNING-UX | ✅ Exists (draft) | `docs/internal/design/mux/MUX-VISION-LEARNING-UX-updated.md` |

---

## Deliverables (7 Total)

Each deliverable is a design specification document.

### D1: Learning Visibility Specification
**Question**: When and how do learnings appear to users?
**Output**: `docs/internal/design/mux/learning-visibility-spec.md`
**Content**:
- Trust-gated visibility matrix (what each level sees)
- Default vs opt-in visibility settings
- Timing rules (when learnings surface)
- UI placement options

### D2: Control Interface Patterns
**Question**: How do users correct, delete, inspect, and reset learnings?
**Output**: `docs/internal/design/mux/learning-control-patterns.md`
**Content**:
- Correction flow ("You think I prefer X, but actually Y")
- Deletion flow ("Forget what you learned about Z")
- Inspection flow ("Show me what you've learned about [topic]")
- Reset flow (with confirmation + consequences)
- Discoverability requirements

### D3: Composting Experience Design
**Question**: What do users see when objects decompose into learnings?
**Output**: `docs/internal/design/mux/composting-experience-design.md`
**Content**:
- "Filing dreams" metaphor application
- Reflection summary format
- Language patterns (reflective, not surveillant)
- Batch vs individual notification rules
- Quiet hours configuration

### D4: Insight Journal Surfacing Rules
**Question**: When does Piper push, pull, or passively display insights?
**Output**: `docs/internal/design/mux/insight-surfacing-rules.md`
**Content**:
- Pull mode triggers and responses
- Passive mode UI patterns
- Push mode thresholds (confidence, relevance, trust level)
- Push language patterns ("Can I share something?")
- Context-sensitivity rules

### D5: Provenance Display Patterns
**Question**: When and how does Piper cite its learnings?
**Output**: `docs/internal/design/mux/provenance-display-patterns.md`
**Content**:
- "Colleague test" application
- When to cite (user asks, uncertain, surprising)
- When NOT to cite (obvious, natural application)
- Citation format patterns
- Seeking confirmation patterns

### D6: Journal Architecture Specification
**Question**: How do Session Journal and Insight Journal work together?
**Output**: `docs/internal/design/mux/journal-architecture-spec.md`
**Content**:
- Session Journal: purpose, structure, access rules (trust level 4+)
- Insight Journal: purpose, structure, user interaction
- Extraction rules (Session → Insight via composting)
- Confidence thresholds for promotion
- Topical organization with recency weighting

### D7: Trust-Based Access Rules
**Question**: What can each trust level see and do with learning?
**Output**: `docs/internal/design/mux/trust-learning-access-rules.md`
**Content**:
- Stage 1: Minimal visibility, pull-only
- Stage 2: On-request summaries
- Stage 3: Periodic reflections, passive browsing
- Stage 4: Full access, proactive insights, queryable history
- Progression implications for learning features

---

## Phases

### Phase 0: Setup & Orientation (1 hour)
- [ ] Read existing MUX-VISION-LEARNING-UX-updated.md thoroughly
- [ ] Create output directory structure
- [ ] Create deliverable templates

### Phase 1: Core Visibility & Control (4 hours)
- [ ] D1: Learning Visibility Specification
- [ ] D2: Control Interface Patterns

**STOP Condition**: If visibility rules conflict with existing trust gradient documentation, escalate.

### Phase 2: Composting & Surfacing (4 hours)
- [ ] D3: Composting Experience Design
- [ ] D4: Insight Journal Surfacing Rules

**STOP Condition**: If "filing dreams" metaphor doesn't work for all scenarios, escalate for alternative framing.

### Phase 3: Provenance & Architecture (4 hours)
- [ ] D5: Provenance Display Patterns
- [ ] D6: Journal Architecture Specification

**STOP Condition**: If Session vs Insight separation creates UX confusion, escalate.

### Phase 4: Trust Integration & Review (3 hours)
- [ ] D7: Trust-Based Access Rules
- [ ] Cross-reference all 7 documents for consistency
- [ ] Update #431 description with deliverable links
- [ ] PM review

**STOP Condition**: If any deliverable conflicts with another, resolve before closing.

---

## Anti-Patterns to Avoid

From the research, these must be avoided in all deliverables:

1. **Surveillance framing** - Never imply continuous monitoring
2. **Notification spam** - Batch updates, not per-event
3. **Unexplained behavior** - Always be ready to explain
4. **False certainty** - Present as hypotheses, not facts
5. **Creepy specificity** - "I've found that..." not "I noticed you always..."
6. **Journal confusion** - Never mix audit (Session) with insights (Insight)

---

## Success Criteria

From #431:
- [ ] Users understand that Piper learns (not opaque)
- [ ] Users feel in control of learnings (not creepy)
- [ ] Learning surfaces feel like colleague reflection (not surveillance)
- [ ] Trust gradient governs learning visibility consistently
- [ ] Correction/deletion mechanisms are discoverable and effective
- [ ] Clear distinction between audit (Session) and insights (Insight)
- [ ] Composting process feels natural and trustworthy

---

## Completion Matrix

| Deliverable | Status | Evidence |
|-------------|--------|----------|
| D1: Visibility Spec | ✅ | `learning-visibility-spec.md` (7,222 bytes) |
| D2: Control Patterns | ✅ | `learning-control-patterns.md` (10,843 bytes) |
| D3: Composting Experience | ✅ | `composting-experience-design.md` (11,261 bytes) |
| D4: Surfacing Rules | ✅ | `insight-surfacing-rules.md` (12,240 bytes) |
| D5: Provenance Patterns | ✅ | `provenance-display-patterns.md` (11,273 bytes) |
| D6: Journal Architecture | ✅ | `journal-architecture-spec.md` (14,071 bytes) |
| D7: Trust Access Rules | ✅ | `trust-learning-access-rules.md` (13,259 bytes) |
| Cross-reference check | ✅ | `431-cross-reference-check.md` |
| #431 description updated | ⏸️ | Awaiting PM review |

---

## Output Location

All deliverables go to: `docs/internal/design/mux/`

---

## Notes

- This is design work, not implementation
- Each deliverable should be standalone but cross-referenced
- Language matters - use consciousness-preserving framing
- Test all patterns against "colleague test" and "creepiness test"

---

## Questions for PM Approval

1. **Section omissions**: The issue template has Testing Strategy, Evidence Section, etc. that don't apply to design exploration work. OK to omit these from the deliverables?

2. **Prototype mockups**: Issue mentions "Prototype mockups: 2h" - should these be wireframes, text descriptions, or both?

3. **Format**: Should deliverables be markdown specs, or is there a specific design doc format preferred?

4. **Review process**: Should each deliverable be reviewed individually, or all 7 together at Phase 4?

---

*Gameplan created: 2026-01-22*
*Ready for PM review*
