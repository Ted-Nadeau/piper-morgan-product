# MUX-VISION-LEARNING-UX: Learning System Experience Design

**Track**: MUX (Embodied UX)
**Epic**: VISION
**Type**: Design Exploration
**Priority**: Medium-High
**Dependencies**: Object Model Brief v2, ADR-045

---

## Context

The Object Model establishes mechanics for learning:
- **Composting**: Archived objects decompose into learnings (lifecycle stage 8)
- **Insight Journal**: Surfaces patterns noticed, premonitions, connections
- **Goals→Outcomes gap**: Where learning happens within Moments

However, we haven't defined *how users experience Piper learning*. This gap risks:
- Opaque improvement (Piper gets better but users don't see/trust it)
- Creepy emergence (patterns surface without explanation)
- Missed engagement (learning could be interactive, not just background)

---

## Design Questions

### 1. Visibility: What do users see?

**Principle**: Layered visibility aligned with trust gradient.

| Trust Level | Default Visibility |
|-------------|-------------------|
| Stage 1-2 | Pull only (user asks) |
| Stage 3 | Pull + periodic summaries |
| Stage 4 | Pull + proactive surfacing when relevant |

**Open question**: Should users be able to opt into "pushier" settings at any trust level?

### 2. Control: How do users correct/modify learnings?

**Principle**: Forthright, transparent, correctable.

Required capabilities:
- **Correction**: "You seem to think I prefer X, but actually Y"
- **Deletion**: "Forget what you learned about Z"
- **Inspection**: "Show me what you've learned about [topic]"
- **Reset**: Delete all learnings (with confirmation + clarity about effect)

**Design consideration**: Reset is significant. Should trigger confirmation and explicit statement of consequences. May indicate broken trust worth understanding.

### 3. Composting Experience: What happens when objects decompose?

**Principle**: Composting is reflection, not surveillance.

**Recommended framing**: "Filing dreams" metaphor.
- Composting happens during Piper's "rest" periods (background processing)
- Surfaces as reflection: "Having had some time to reflect, it occurs to me..."
- NOT framed as "while you were away" (implies continuous monitoring)

**Options considered**:
- ❌ Nothing (too opaque)
- ❌ Per-item notification (too noisy)
- ✅ Periodic reflection summaries (batched, natural, colleague-like)

### 4. Insight Journal UX: Push/Pull/Passive

**Principle**: All three modes, context-dependent.

| Mode | When | Trust Implication |
|------|------|-------------------|
| **Pull** | User queries directly | Available at all levels |
| **Passive** | Browsable in Piper's space | Available at all levels |
| **Push** | Proactive surfacing | Stage 3+ only, high-confidence/relevance |

**Push language**: Should feel like colleague interruption.
- ✅ "Can I share something that might be relevant?"
- ❌ "ALERT: Pattern detected"

### 5. Learning Provenance: When does Piper cite its learnings?

**Principle**: Colleague test—explain when asked or when non-obvious.

| Situation | Cite? |
|-----------|-------|
| User asks why | Yes |
| Applying pattern naturally | No (over-explaining is annoying) |
| Uncertain inference | Yes (seeking confirmation) |
| User seems surprised | Yes (explain reasoning) |

---

## Trust Gradient Integration

Background processing (dreaming, composting, scheduled tasks) must respect the same trust gradient as interactive behaviors:

| Trust Level | Background Processing Visibility |
|-------------|----------------------------------|
| Stage 1 | Minimal. User should barely notice. |
| Stage 2 | On-request summaries only. |
| Stage 3 | Periodic reflection summaries. |
| Stage 4 | Proactive insights + queryable history. |

**Key insight**: Users must both (a) trust that Piper handles their data responsibly AND (b) believe that Piper handles their data responsibly. Architecture and legibility both matter.

---

## Anti-Patterns to Avoid

1. **Surveillance framing**: Avoid language implying continuous monitoring
2. **Notification spam**: Learning updates should be batched, not per-event
3. **Unexplained behavior**: If Piper acts on a learning, be ready to explain
4. **False certainty**: Present learnings as hypotheses, not facts
5. **Creepy specificity**: "I noticed you always..." feels surveillant; "I've found that..." feels reflective

---

## Deliverables

1. **Learning visibility specification**: When and how learnings appear
2. **Control interface patterns**: Correction, deletion, inspection, reset flows
3. **Composting experience design**: What users see when objects decompose
4. **Insight Journal surfacing rules**: Push/pull/passive triggers
5. **Provenance display patterns**: When and how to cite learnings

---

## Connections

- **VISION-JOURNAL-LAYERS (#409)**: Insight Journal is subset of this work
- **INTERACT-DELEGATION (#414)**: Learning informs delegation confidence
- **INTERACT-RECOGNITION (#413)**: Learnings shape what Piper recognizes
- **Object Model Brief v2**: Composting lifecycle stage
- **ADR-045**: Foundational grammar

---

## Success Criteria

- [ ] Users understand that Piper learns (not opaque)
- [ ] Users feel in control of learnings (not creepy)
- [ ] Learning surfaces feel like colleague reflection (not surveillance)
- [ ] Trust gradient governs learning visibility consistently
- [ ] Correction/deletion mechanisms are discoverable and effective

---

*Drafted*: November 29, 2025
*Session*: CXO Object Model + Learning Integration
