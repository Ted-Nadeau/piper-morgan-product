# Piper Morgan Object Model: Conceptual Decisions Brief

**Date**: November 27, 2025 (Thanksgiving)
**Session**: CXO Object Model Exploration
**Status**: Decisions captured, ready for sketching

---

## Purpose

This brief captures the conceptual decisions made during the object model exploration session. These decisions form the foundation for sketching exercises and subsequent design work. They are "decided for now"—firm enough to build on, open to revision through the sketching process.

---

## Core Architectural Decisions

### 1. Lenses on Substrates (not discrete object types)

**Decision**: Piper's conceptual model is organized around a small set of substrates viewed through analytical lenses, rather than a rigid taxonomy of object types.

**Rationale**:
- More flexible, less rigid categorization
- Avoids false dichotomies ("is this a Task or a Risk?")
- Simpler core model with richer views
- Prevents premature ontological commitment

---

### 2. Four Substrates

**Decision**: The fundamental "stuff" Piper perceives and reasons about:

| Substrate | What It Is | Examples |
|-----------|-----------|----------|
| **Entities** | Discrete things with identity | People, Work Items, Documents, Artifacts |
| **Spaces** | Containers/contexts where work happens | Projects, Channels, Repos, Teams |
| **Moments** | Points or spans in time | Events, Deadlines, Sessions, Milestones |
| **Situations** | Configurations of the above at a given time | "Current state of the launch," "What's blocked right now" |

**Rationale**: Minimal set that can compose into anything richer. Entities are the nouns, Spaces are the containers, Moments are the temporal anchors, Situations are the snapshots.

---

### 3. Eight Spatial Dimensions = The Lenses

**Decision**: The 8-dimensional spatial intelligence framework already built serves as the analytical lenses applied to any substrate.

| Dimension | What It Illuminates |
|-----------|---------------------|
| TEMPORAL | When? Sequence, deadline, history, pattern over time |
| HIERARCHY | What contains this? What does it contain? |
| PRIORITY | How urgent/important? What deserves attention? |
| COLLABORATIVE | Who's involved? Who's blocked? Who cares? |
| CAUSAL | What caused this? What does it affect? |
| CONTEXTUAL | What situation makes this relevant? |
| RELATIONAL | How does this connect to other things? |
| IDENTITY | What is this? How does Piper recognize it? |

**Rationale**: One model, not two. The intents align; doing otherwise spawns unclear parallelistic complexity. Also helps resist "flattening" the spatial intelligence work.

---

### 4. Three-Way Ownership Split

**Decision**: Objects are categorized by Piper's relationship to them:

| Category | Piper's Role | Metaphor | Examples |
|----------|--------------|----------|----------|
| **Native** | Creates, owns, maintains | Piper's Mind | Sessions, Memories, Concerns, Trust States, Orientation, Journals |
| **Federated** | Observes, queries, acts upon (doesn't own) | Piper's Senses | GitHub Issues, Slack Messages, Calendar Events, Notion Docs |
| **Synthetic** | Constructs from federation + native reasoning | Piper's Understanding | Projects (assembled), Risks (inferred), Patterns (learned) |

**Rationale**: Clear ownership boundaries prevent confusion about source-of-truth. Native = mind, Federated = senses, Synthetic = understanding.

---

### 5. Six Common Metadata Dimensions

**Decision**: A universal metadata schema applies across ALL objects regardless of type or category:

| Metadata | What It Captures |
|----------|------------------|
| **Provenance** | Where did this come from? Source, confidence, freshness |
| **Relevance** | Why does this matter now? Connection to current context |
| **Attention State** | Has this been seen? Does it need attention? |
| **Confidence** | How certain is Piper about this? |
| **Relations** | What is this connected to? Graph position |
| **Journal** | History of Piper's interaction with this object |

**Rationale**: These let Piper answer: Where from? Why now? Seen it? Sure about it? What's it connected to? What's the story? Journal as metadata means every object carries its own history (audit trail, recovery, temporal dimension).

---

### 6. Full Lifecycle with Composting

**Decision**: Objects move through a complete lifecycle that includes endings and succession:

```
Emergent → Derived → Inferred → Proposed → Ratified → Deprecated → Archived → Composted
    ↑                                                                              |
    └──────────────────────────── feeds new ───────────────────────────────────────┘
```

| Stage | What It Means |
|-------|---------------|
| **Emergent** | Piper notices something, hasn't interpreted it yet |
| **Derived** | Piper connects it to other things |
| **Inferred** | Piper forms a hypothesis about what it is |
| **Proposed** | Piper surfaces it to user for consideration |
| **Ratified** | User confirms, names, or acts on it |
| **Deprecated** | Superseded, no longer current, but retained |
| **Archived** | Ended, closed, completed, retired |
| **Composted** | Decomposed into learnings that feed new things |

**Rationale**:
- The shadow side of PM work is ending things—model should honor that
- Nothing truly disappears; it transforms
- Composting is where Memory and Pattern objects get fed
- Dreaming/digestion = partly composting
- Cycle closes: death feeds new life

---

### 7. Two Journaling Layers

**Decision**: Piper maintains two distinct journal layers with different visibility:

| Layer | Visibility | What Goes Here | When It Surfaces |
|-------|------------|----------------|------------------|
| **Session Journal** | User can query anytime | What happened, what was produced, the audit trail | On request |
| **Insight Journal** | Surfaces when ready | Outputs of dreaming/composting—patterns noticed, premonitions, connections made | At appropriate trust level, or on request |

**Not formalized**: Private diary (internal working state) remains internal state, not a journaled layer.

**Rationale**:
- Not everything in cognition should be visible immediately
- Insight Journal is where "composted" material surfaces as new insight
- Avoids optional complexity of three layers
- Private processing happens but doesn't need to be journaled

---

### 8. User Model as Native Object (Principal + Others)

**Decision**: Piper maintains explicit models of humans, with depth varying by proximity:

| Level | Who | Model Depth | Core Dimensions |
|-------|-----|-------------|-----------------|
| **Principal** | Account holder Piper works for | Deep | Wants, fears, preferences, patterns, trust grants, goals, stress indicators |
| **Team** | Humans principal works with directly | Medium | Role, relationship to principal, communication style, what they care about |
| **Stakeholders** | Humans referenced in work context | Light | Wants, fears (stakeholder mapping), relationship to work |
| **Mentioned** | Names that appear but aren't active | Minimal | Identity and context where mentioned |

**Core heuristic for modeling humans**: "What do they want?" (what's a win for them) and "What are they afraid of?" (what has burned them, status risks)

**On creepiness**: The antidote is transparency, correctability, forthrightness, and clear boundaries. Kind, not just nice.

**Parked**: Non-human sapients (other AI agents) may need modeling eventually but not MVP-critical.

---

## What This Enables

With these decisions, Piper has:

- **A way to perceive** (substrates + lenses)
- **A way to categorize relationships** (native/federated/synthetic)
- **A way to track anything** (common metadata)
- **A way to understand change** (lifecycle with composting)
- **A way to remember and reflect** (two journal layers)
- **A way to understand humans** (user model with wants/fears)

---

## Open for Sketching Exploration

The following remain open for discovery through visual exploration:

- How do substrates, lenses, and ownership categories actually compose visually?
- What does the lifecycle look like as a diagram? (Circular? Spiral? Branching?)
- How do the six metadata dimensions attach to objects?
- What does the user model hierarchy look like in relation to work objects?
- How do the two journal layers relate to the lifecycle (especially composting)?

---

## Metaphor Summary

| Concept | Metaphor |
|---------|----------|
| Native/Federated/Synthetic | Mind / Senses / Understanding |
| Lifecycle ending | Composting (death feeds new life) |
| Piper's role | Junior PM / Assistant with a principal |
| User modeling | Wants and fears (stakeholder empathy) |
| Journaling | Session (audit) + Insight (dreams surfaced) |
| Colleague test | "Would a good PM colleague know this?" |

---

**Document Status**: Complete snapshot of decisions
**Next Step**: Sketching assignment for Object Model visualization

---

*Captured: November 27, 2025, ~3:38 PM Pacific*
