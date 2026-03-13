# Piper Morgan Object Model: Conceptual Foundations Brief v2

**Date**: November 27, 2025 (Thanksgiving)
**Session**: CXO Object Model Exploration + Sketching
**Status**: Phase 1 (Conceptual Architecture) substantially complete
**Audience**: Chief of Staff (Weekly Ship), Chief Architect (Convergence Planning)

---

## Executive Summary

Through systematic decision-making and hands-on sketching, we've established the conceptual foundations for Piper Morgan's object model. The core insight is a grammar: **"Entities experience Moments in Places."** This foundation is ready to inform interaction design and aligns cleanly with existing MVP priorities—the current UI is a placeholder, so there's no conflict between sprint work and UX 2.0 goals.

---

## The Core Grammar

> **ENTITIES experience MOMENTS in PLACES.**
>
> MOMENTS are contained by SITUATIONS.
>
> SITUATIONS are sequences of MOMENTS with time as backbone.

This grammar drives everything else. It's verb-forward (experience, contain) rather than noun-heavy. It positions the Moment—not the task or document—as the unit of meaningful work.

---

## Substrate Model (What Piper Perceives)

### Two Primary Substrates

| Substrate | What It Is | Examples |
|-----------|-----------|----------|
| **Entities** | Actors with identity and agency | People, AI agents (including Piper), teams, projects, workflows, documents |
| **Places** | Contexts where action happens | Offices, channels, repos, conference rooms (physical/virtual/hybrid) |

**Key insight**: The boundary between Entity and Place is a spectrum, not binary. A *project* is an Entity when it "ships" or "fails" (active verb). The same project is a Place when work happens "in" it.

### Two Temporal Structures

| Structure | What It Is | Characteristics |
|-----------|-----------|-----------------|
| **Moments** | Bounded significant occurrences | Unity of time (less than a day), unity of place, momentous (not every meeting is a Moment) |
| **Situations** | Sequences of Moments | Time as backbone/index, the frame that gives Moments meaning |

**Key insight**: A Moment is when something *happened* that matters—a decision made, a milestone met, a key meeting. The theatrical unities apply: one time, one place, one action.

### Anatomy of a Moment (The Shoebox Model)

A Moment is a bounded scene containing:

| Component | Contents |
|-----------|----------|
| **POLICY** | Governance, goals (aspirational) |
| **PROCESS** | Workflows, entities doing their thing |
| **PEOPLE** | Human team members + AI assistants (+1 over the sapience line) |
| **OUTCOMES** | What actually happened (the delta from goals = learning) |

---

## Ownership Model (Piper's Relationship to Objects)

| Category | Piper's Role | Metaphor | Examples |
|----------|--------------|----------|----------|
| **Native** | Creates, owns, maintains | Piper's Mind | Sessions, Memories, Concerns, Trust States, Journals |
| **Federated** | Observes, queries, acts upon | Piper's Senses | GitHub Issues, Slack Messages, Google Docs, Notion |
| **Synthetic** | Constructs through reasoning | Piper's Understanding | Assembled Projects, Inferred Risks, Learned Patterns |

**Key insight**: Piper is an Entity, not just a lens. Piper is a player with identity, participating in situations alongside the Principal and other entities.

---

## Perceptual Lenses (How Piper Sees)

Eight candidate lenses for viewing any substrate (list in flux, being refined):

| Lens | Icon | What It Illuminates |
|------|------|---------------------|
| Hierarchy | 🔲 org tree | Containment, levels, reporting |
| Temporal | ⏱️ clock | Time, sequence, history |
| Priority | P1 marker | Urgency, importance, rank |
| Collaborative | 👥 figures | Who's involved, who cares |
| Flow | 〰️ waves | Movement, sequence, state changes |
| Quantitative | 📊 grid | Measurable data, metrics |
| Causal | 🎱→⚪⚪ | One cause, multiple effects (divergence) |
| Contextual | 🔲∈🔲 nested | Which containing context applies |

**Emerging distinction**:
- **Static lenses**: See the arrangement (Hierarchy, Contextual)
- **Dynamic lenses**: See the change (Flow, Causal, Temporal)

**Held open**: The relationship between these Perceptual lenses and the Orientation queries (Identity, Temporal, Spatial, Capability, Predictive) and Judgment frameworks (Deontological, Consequentialist, Virtue, Contextual). These may be three faculties of Piper's cognition, not one list.

---

## Lifecycle Model (How Objects Evolve)

### Eight Stages

| Stage | Icon | What It Means |
|-------|------|---------------|
| **Emergent** | ? | Potential, not yet defined |
| **Derived** | fn= | Calculated/connected from other things |
| **Noticed** | 💡 | Awareness dawns (not "Inferred"—more human) |
| **Proposed** | 💬 | Surfaced to conversation |
| **Ratified** | ☑️ | Confirmed by user |
| **Deprecated** | 🌅 | Sunset, superseded |
| **Archived** | 📦 | Stored away |
| **Composted** | 🌱 | Decomposed into learnings, ready to feed new Emergent |

### Cycle Shapes (Metadata)

Not every object follows the same path. The *shape* of a lifecycle is meaningful:

| Shape | What It Represents |
|-------|-------------------|
| Closed circle | Full cycle, returns to beginning |
| Spiral | Returns but at different level—learning accumulated |
| Arc (in play) | Still unfolding, not yet complete |
| Cradle to grave | One-way, terminates without composting |
| Parallel arcs | Multiple things cycling simultaneously |
| Overlapping curves | Cycles interact, influence each other |

---

## Metadata Model (What Piper Knows About Things)

Six universal dimensions applying across all objects:

| Dimension | What It Captures |
|-----------|------------------|
| **Provenance** | Where from? Source, confidence, freshness |
| **Relevance** | Why now? Connection to current context |
| **Attention State** | Seen? Needs attention? |
| **Confidence** | How certain is Piper? |
| **Relations** | What's connected? Graph position |
| **Journal** | History of Piper's interaction (audit trail, temporal anchor) |

### Entity-Specific Metadata

For entities specifically, Piper may also track:

| Dimension | Icon | What It Captures |
|-----------|------|------------------|
| People | 👑 + 👥 | Primary owner + associated people (fluid vocabulary—DACI/RACI/local dialect) |
| Purpose | ↑ | What is this entity for? |
| Predict | 🔮 | What does Piper expect to happen? |
| Value | 💥 | Product value—why does it matter? |
| Ethos | ⚖️ | Ethical alignment status |
| Quality | (measure) | How good is it? (may not apply to persons) |

---

## User Model (How Piper Understands Humans)

| Level | Who | Model Depth |
|-------|-----|-------------|
| **Principal** | Account holder (👑) | Deep: wants, fears, preferences, patterns, trust grants, goals, stress |
| **Team** | Direct collaborators | Medium: role, relationship, communication style |
| **Stakeholders** | Referenced in context | Light: wants, fears (stakeholder mapping shorthand) |
| **Mentioned** | Names appearing | Minimal: identity and context |

**Core heuristic**: "What do they want?" + "What are they afraid of?"

**Antidote to creepy**: Transparent, correctable, forthright, bounded. Kind, not just nice.

---

## Journaling Model (How Piper Remembers)

| Layer | Visibility | Purpose |
|-------|------------|---------|
| **Session Journal** | User can query | What happened, what was produced—audit trail |
| **Insight Journal** | Surfaces when ready | Patterns noticed, premonitions, connections (outputs of dreaming/composting) |

---

## Collaboration Model (Human + Piper)

The Human-Centered sketch revealed the collaboration loop:

```
PRINCIPAL (in situation)
    ↓
observes: processes, places, people
    ↓
senses: "something needs to be captured"
    ↓                          ↓
    ↓                     PIPER (observing same)
    ↓                          ↓
    ↓                     senses: "I think I know what"
    ↓                          ↓
    └──── COMMUNICATION ───────┘
              ↓
         AGREEMENT
              ↓
         PIPER DELIVERS
    (formatted for audience)
```

**Key insight**: Not command→execute. Both parties have impressions; they align; then Piper acts. The trust gradient governs how much checking happens at each stage.

---

## Visual Language (Emerging)

Through sketching, an icon vocabulary emerged:

| Concept | Icon |
|---------|------|
| Principal | 👑 crown |
| Piper | 🐬 dolphin with tablet |
| Situation | 🎲 die (composed of moments + uncertainty) |
| Moment | shoebox/cutaway room |
| Lifecycle stage | (8 icons as above) |
| Lenses | (8 icons as above) |

---

## AI Diagramming Tool Findings

Tested three approaches:

| Tool | Result | Verdict |
|------|--------|---------|
| **Whimsical** | Accurate transcription, hierarchical | Useful for documentation, no discovery |
| **Eraser.io** | Jumped to database schema | Lost conceptual meaning entirely |
| **Gemini** | Beautiful gestalt, overlapping regions | Captured structure, worth combining with hand-drawn insights |

**Recommendation**: Use Gemini's visual style for polished diagrams, but human sketching remains essential for discovery. Consider combining Gemini's overlapping ownership regions with the hand-drawn grammar and icon vocabulary.

---

## What This Enables

With these foundations, Piper has:

- **A way to perceive** (substrates + lenses)
- **A grammar** ("Entities experience Moments in Places")
- **A way to know itself** (Piper as Entity, not just lens)
- **A way to understand relationships** (Native/Federated/Synthetic)
- **A way to track anything** (6 metadata dimensions + entity-specific)
- **A way to understand change** (lifecycle with composting + cycle shapes)
- **A way to remember** (two journal layers)
- **A way to understand humans** (user model with wants/fears)
- **A way to collaborate** (communication → agreement → delivery)
- **A visual vocabulary** (emerging icon set)

---

## Alignment with Current Priorities

| Current MVP Work | UX 2.0 Work | Conflict? |
|------------------|-------------|-----------|
| Spatial intelligence (8 dimensions) | Perceptual lenses | ✅ Same thing, now named as Perception |
| Canonical queries | Orientation queries | ✅ Same thing, now framed as self-awareness |
| Ethical consensus | Judgment frameworks | ✅ Same thing, now positioned in cognitive model |
| Intent classification | Recognition interfaces | ✅ Intent = recognizing what user means |
| Current UI | Placeholder | ✅ No conflict—UI redesign is additive |

**Bottom line**: Existing sprint work is building the *engine*. UX 2.0 work is designing how the engine *appears* and *feels*. They're complementary, not competing.

---

## Next Steps

### Immediate (Ready Now)
- Brief Chief of Staff for Weekly Ship
- Brief Chief Architect for convergence planning
- Document icon vocabulary for future reference

### Phase 2: Interaction Vocabulary (When Ready)
- Define recognition interface patterns
- Design trust gradient mechanics
- Specify transitions and notifications
- Map canonical queries to interface states

### Future Sketching (If Needed)
- Trust gradient visualization
- Recognition interface patterns
- Notification/surfacing mechanics

---

## Process Reflection

This session demonstrated the value of:

1. **Systematic decision-making**: One question at a time, recommendation + rationale, decide and move on
2. **Holding things open**: Not forcing precision before understanding emerges
3. **Sketching as discovery**: The hand found things the mind hadn't articulated (Situation as container, "Noticed" vs "Inferred", cycle shapes as metadata)
4. **Human + AI comparison**: AI tools transcribe well but don't discover. Human sketching remains essential for conceptual work.

The fractal insight applies: at some point you've elaborated enough that remaining decisions become less load-bearing. We're approaching that point for the conceptual model.

---

**Document Status**: Phase 1 substantially complete
**Next Phase**: Interaction Vocabulary (when ready to proceed)
**Blocking Issues**: None

---

*Captured: November 27, 2025, 10:18 PM Pacific*
*Session Duration: ~10 hours (with breaks)*
