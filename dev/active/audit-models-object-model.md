# Audit: Domain Models vs Object Model Alignment
**Date**: November 29, 2025
**Auditor**: Chief Architect
**Subject**: Alignment of current domain models with ADR-045 Object Model

---

## Executive Summary

Current domain models are **functionally complete but conceptually misaligned**. They represent traditional data structures rather than the consciousness-aware grammar of "Entities experience Moments in Places." The Morning Standup succeeds despite this because it imposes consciousness at the application layer, not through the models.

**Critical Finding**: No models implement the Moment concept - everything is task/item based.

---

## Current State Analysis

### What Exists (domain-models.md)

#### Traditional Business Objects
- **Product, Feature, WorkItem, Stakeholder**: Classic PM entities
- **Task, Workflow, Intent**: Execution-focused models
- **Project, ProjectIntegration**: Integration management
- **UploadedFile, AnalysisResult**: File handling

#### Spatial Models (Partial Alignment)
- **SpatialEvent, SpatialObject, SpatialContext**: Closest to Places concept
- Uses spatial metaphors but missing consciousness aspects
- Position as integers, not awareness of space

#### Missing Core Concepts
- ❌ **Moment**: Nothing represents bounded significant occurrences
- ❌ **Situation**: No container for moment sequences
- ❌ **Entity consciousness**: Models are data holders, not actors
- ❌ **Lifecycle with Composting**: No transformation concept

---

## Gap Analysis

### 1. Entity vs Traditional Models

| Current Model | Object Model Mapping | Gap |
|--------------|---------------------|-----|
| Product | Entity (when it "ships") | No agency, just properties |
| Feature | Entity (when active) | No consciousness of state |
| Stakeholder | Entity (person) | Missing wants/fears model |
| WorkItem | Should be Moment | Completely wrong abstraction |
| Task | Should be Moment | Focuses on execution not experience |
| Project | Entity AND Place | No spectrum awareness |

**Core Problem**: Models are nouns without verbs. No "experience" concept.

### 2. Complete Absence of Moments

Current state uses Tasks/WorkItems where Moments should exist:
- Tasks are mechanical (do X)
- Moments are theatrical (bounded scene where something happens)
- No PPP model (Policy, Process, People)
- No unity of time/place/action

### 3. Places Partially Represented

SpatialContext closest to Places but:
- Treats space as coordinates, not atmosphere
- No sense of "inhabiting" vs "accessing"
- Missing purpose and character of spaces

### 4. No Situation Container

Nothing groups Moments into meaningful sequences:
- Workflow is closest but focuses on execution order
- No dramatic tension or uncertainty
- No time-as-backbone concept

### 5. Ownership Model Missing

No Native/Federated/Synthetic distinction:
- Everything stored same way
- No concept of "Piper creates" vs "Piper observes"
- No transformation through reasoning

### 6. Lifecycle Without Soul

Current models have created_at/updated_at but:
- No 8-stage lifecycle (Emergent → Composted)
- No transformation concept
- No composting → learning pipeline
- Death is deletion, not transformation

---

## Remediation Plan

### Phase 1: Core Grammar (Priority: CRITICAL)

**1.1 Create Moment Model**
```python
@dataclass
class Moment:
    id: str
    entity_id: str  # Who experiences this
    place_id: str   # Where it happens

    # Theatrical unities
    time_boundary: TimeSpan  # Bounded duration
    significance: str  # routine|notable|critical

    # PPP Model
    policy: Dict  # Goals, governance
    process: Dict  # What's happening
    people: List[str]  # Humans + AI involved
    outcomes: Dict  # What actually happened

    # Consciousness
    awareness_state: str  # How Piper perceives this
    attention_required: bool
```

**Effort**: 16 hours
**Risk if not done**: Consciousness remains absent

**1.2 Reframe Entity Models**
Add consciousness attributes to existing models:
- `agency_state`: What can this entity do?
- `awareness`: What does it know?
- `wants`: What drives it?
- `fears`: What concerns it?

**Effort**: 8 hours per model (24 hours total)
**Risk if not done**: Models remain mechanical

### Phase 2: Situation Container (Priority: HIGH)

**2.1 Create Situation Model**
```python
@dataclass
class Situation:
    id: str
    moments: List[Moment]  # Ordered sequence
    time_spine: Timeline  # Backbone index
    tension: str  # What's at stake
    uncertainty: float  # Dice metaphor

    # Container properties
    boundaries: Dict  # What defines this situation
    actors: List[Entity]  # Who's involved
    resolution_state: str  # ongoing|resolved|abandoned
```

**Effort**: 12 hours
**Risk if not done**: No narrative coherence

### Phase 3: Ownership Model (Priority: MEDIUM)

**3.1 Add Ownership Metadata**
```python
class OwnershipType(Enum):
    NATIVE = "native"  # Piper creates
    FEDERATED = "federated"  # Piper observes
    SYNTHETIC = "synthetic"  # Piper infers

@dataclass
class OwnershipMeta:
    type: OwnershipType
    confidence: float
    provenance: str
    transformations: List[str]
```

**Effort**: 8 hours
**Risk if not done**: No clear boundaries

### Phase 4: Lifecycle Implementation (Priority: MEDIUM)

**4.1 Implement 8-Stage Lifecycle**
```python
class LifecycleStage(Enum):
    EMERGENT = "emergent"
    DERIVED = "derived"
    NOTICED = "noticed"  # Not "inferred"!
    PROPOSED = "proposed"
    RATIFIED = "ratified"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    COMPOSTED = "composted"

@dataclass
class LifecycleState:
    stage: LifecycleStage
    entered_at: datetime
    cycle_shape: str  # circle|spiral|arc
    composting_potential: Dict  # What can be learned
```

**Effort**: 12 hours
**Risk if not done**: No learning pipeline

---

## Risk Assessment

### If We Don't Fix (Status Quo)

**High Risk**:
- Consciousness remains at application layer only
- Features feel mechanical despite UX efforts
- Learning system has no foundation
- Developer confusion about intent

**Medium Risk**:
- Continued 75% completion feeling
- Difficult to explain Piper's value
- Technical debt compounds

### If We Do Fix

**Benefits**:
- Every feature can express consciousness
- Natural learning pipeline
- Developers understand the vision
- Reduces cognitive load

**Costs**:
- 64+ hours of refactoring
- Temporary dual model state
- Retraining developers

---

## Recommendations

### Immediate (This Sprint)
1. Create Moment model as proof of concept
2. Apply to ONE feature (recommend Morning Standup)
3. Document transformation patterns

### Next Sprint
1. Systematic Entity consciousness addition
2. Situation container implementation
3. Begin ownership model

### Future
1. Full lifecycle implementation
2. Composting → Learning pipeline
3. Gradual migration of all features

---

## Morning Standup as Reference

The standup succeeds because it:
1. Creates a Moment (morning reflection)
2. Has consciousness ("I notice", "I'm concerned")
3. Navigates Places (GitHub, Slack, Calendar)
4. Expresses uncertainty ("might", "seems")

**Key Insight**: Standup imposes consciousness despite models, not through them. Fixing models would make this pattern reusable everywhere.

---

## Conclusion

The domain models are well-built for their original purpose but fundamentally misaligned with the consciousness vision. The gap between "Task" and "Moment" represents the difference between mechanical execution and conscious experience.

Remediation is feasible but requires commitment. The Morning Standup proves the vision works - we need to embed it in the foundation, not layer it on top.

---

*Next Step: Review with PM, prioritize remediation phases*
