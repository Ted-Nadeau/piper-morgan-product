# MUX Implementation Guide

## Core Grammar

**"Entities experience Moments in Places."**

This sentence is the foundation of the MUX object model. Every feature, every data structure, every query must be expressible using this grammar.

## The Three Substrate Protocols

### 1. EntityProtocol

Entities are actors with identity and agency - things that can have experiences.

```python
from services.mux.protocols import EntityProtocol

@runtime_checkable
class EntityProtocol(Protocol):
    """Any actor with identity and agency."""
    id: str

    def experiences(self, moment: 'MomentProtocol') -> 'Perception':
        """Entity experiences a Moment, returning a Perception."""
        ...
```

**Examples**: User, Team, Project, Task (when task acts as agent), Piper

**Key insight**: Entities EXPERIENCE moments rather than "having data". This framing preserves consciousness.

### 2. MomentProtocol

Moments are bounded significant occurrences with theatrical unities.

```python
from services.mux.protocols import MomentProtocol

@runtime_checkable
class MomentProtocol(Protocol):
    """Bounded significant occurrence."""
    id: str
    timestamp: datetime

    def captures(self) -> Dict[str, Any]:
        """Return what this Moment captures (policy, process, people, outcomes)."""
        ...
```

**Examples**: Meeting, Decision, Commit, Deploy, Standup, Review

**Key insight**: Moments have policy, process, people, and outcomes - they're scenes, not just timestamps.

### 3. PlaceProtocol

Places are contexts where action happens, with atmosphere.

```python
from services.mux.protocols import PlaceProtocol

@runtime_checkable
class PlaceProtocol(Protocol):
    """Context where action happens."""
    id: str
    atmosphere: str  # warm, formal, urgent, creative, etc.

    def contains(self) -> List[Any]:
        """Return entities/moments contained in this Place."""
        ...
```

**Examples**: Slack Channel, GitHub Repository, Notion Project, Calendar, Team

**Key insight**: Places have atmosphere - they're not just containers but have character that affects what happens.

## When Adding a New Feature

### Step 1: Identify Grammar Elements

Ask yourself:

- **Entities**: Who are the actors? (users, Piper, integrations, teams)
- **Moments**: What bounded occurrences happen? (meetings, tasks, conversations, decisions)
- **Places**: Where do interactions occur? (GitHub, Slack, Calendar, Notion)

### Step 2: Choose Lenses

Pick perceptual dimensions for your feature from the 8 available:

| Lens | Description | Example Query |
|------|-------------|---------------|
| **Temporal** | Time-based ("today", "this week") | "What's happening today?" |
| **Priority** | Importance-based ("urgent", "can wait") | "What's most important right now?" |
| **Collaborative** | People-based ("team", "stakeholders") | "Who's involved in this?" |
| **Flow** | Progress-based ("blocked", "in progress") | "What's stuck?" |
| **Hierarchy** | Structure-based ("project > epic > task") | "What does this belong to?" |
| **Quantitative** | Metrics-based ("how many", "how long") | "How much work is there?" |
| **Causal** | Cause-effect ("because", "leads to") | "Why did this happen?" |
| **Contextual** | Background ("setting", "atmosphere") | "What's the context?" |

### Step 3: Apply Protocols

Choose which protocols your feature needs:

```python
# If ownership matters (where does this come from?)
from services.mux.ownership import HasOwnership, OwnershipResolver, OwnershipCategory

# If lifecycle matters (how does this evolve?)
from services.mux.lifecycle import HasLifecycle, LifecycleManager, LifecycleState

# If metadata matters (what do we know about this?)
from services.mux.metadata import HasMetadata, Provenance, Confidence, Journal
```

### Step 4: Frame as Situation

Ask:
- What's the dramatic tension? (What wants to happen?)
- What learning is extracted on exit? (What wisdom remains?)

Example for Morning Standup:
- **Tension**: "Need to prepare for the day while managing constraints"
- **Exit Learning**: "Patterns in how mornings go, what preparations help"

## The Ownership Model

Three epistemological categories describing Piper's relationship to knowledge:

| Category | Metaphor | Experience Phrase | Examples |
|----------|----------|-------------------|----------|
| **NATIVE** | Piper's Mind | "I know this because I created it" | Sessions, memories, trust states |
| **FEDERATED** | Piper's Senses | "I see this in {place}" | GitHub issues, Slack messages |
| **SYNTHETIC** | Piper's Understanding | "I understand this to mean..." | Inferred status, pattern recognition |

```python
from services.mux.ownership import OwnershipResolver

resolver = OwnershipResolver()

# Determine category from source
category = resolver.determine(source="github")  # -> FEDERATED
category = resolver.determine(source="piper")   # -> NATIVE
category = resolver.determine(source="inference", is_derived=True)  # -> SYNTHETIC
```

## The Lifecycle Model

8 stages representing how objects mature:

```
EMERGENT -> DERIVED -> NOTICED -> PROPOSED -> RATIFIED -> DEPRECATED -> ARCHIVED -> COMPOSTED
```

| State | Meaning | Experience Phrase |
|-------|---------|-------------------|
| EMERGENT | First stirrings | "I sense something forming..." |
| DERIVED | Pattern recognized | "I recognize a pattern emerging..." |
| NOTICED | Brought to attention | "This has caught my attention..." |
| PROPOSED | Formally recommended | "I am considering this proposal..." |
| RATIFIED | Officially accepted | "This is now part of our established reality" |
| DEPRECATED | Marked for retirement | "This served us well, but its time is passing" |
| ARCHIVED | Preserved but inactive | "This rests in memory..." |
| COMPOSTED | Transformed into wisdom | "This has transformed into nourishment..." |

### Composting Philosophy

**"Nothing disappears, it transforms."**

When objects reach end of life, don't delete them. Compost them:

```python
from services.mux.lifecycle import CompostingExtractor

extractor = CompostingExtractor()
result = extractor.extract(old_object)

# result.object_summary - key attributes preserved
# result.journey - lifecycle states traversed
# result.lessons - wisdom extracted
# result.composted_at - when transformation occurred
```

## The Metadata Schema

6 universal dimensions for "knowledge about knowledge":

| Dimension | Question | Key Attributes |
|-----------|----------|----------------|
| **Provenance** | Where did this come from? | source, confidence, freshness |
| **Relevance** | How important is this? | score, factors, context |
| **AttentionState** | Who has noticed this? | noticed_by, attention_level |
| **Confidence** | How sure are we? | score, basis, last_validated |
| **Relations** | How does this connect? | target_id, relation_type, strength |
| **Journal** | What is the history? | session_entries (facts), insight_entries (meaning) |

### Journal: Two Layers

```python
from services.mux.metadata import JournalManager, Journal

manager = JournalManager()

# Session layer - facts (audit trail)
manager.log_session_event(
    object_id="task_123",
    event_type="completed",
    content="Task marked done",
    trigger="user_action"
)

# Insight layer - meaning (learning)
manager.extract_insight(
    object_id="task_123",
    learning="User prefers to complete tasks in morning"
)

journal = manager.get_journal("task_123")
# journal.session_entries - what happened
# journal.insight_entries - what it meant
```

## Anti-Patterns (What NOT to Do)

### Entity Anti-Patterns
- Do NOT reduce Entities to database IDs
- Do NOT make entities passive data holders
- Do NOT forget that entities have agency

### Moment Anti-Patterns
- Do NOT flatten Moments to timestamps
- Do NOT ignore the significance of what happened
- Do NOT treat moments as interchangeable events

### Place Anti-Patterns
- Do NOT configure Places without atmosphere
- Do NOT treat places as mere connection strings
- Do NOT forget that places have character

### Lifecycle Anti-Patterns
- Do NOT delete objects - compost them
- Do NOT use status codes (1, 2, 3) - use meaningful states
- Do NOT skip the journey - each transition matters

### Metadata Anti-Patterns
- Do NOT enumerate without framing
- Do NOT forget to track provenance
- Do NOT mix facts (session) with meaning (insight)

## Example: Implementing a Feature

### Feature: Pull Request Review

**Step 1: Grammar Elements**
- Entities: Author, Reviewer, Piper
- Moments: PR Creation, Review Comment, Approval, Merge
- Places: GitHub Repository (atmosphere: "technical review space")

**Step 2: Lenses**
- Temporal: When was this created? How old?
- Priority: Is this blocking anything?
- Collaborative: Who needs to review? Who's involved?
- Flow: Where in review process?

**Step 3: Protocols**
```python
@dataclass
class PullRequest:
    # EntityProtocol
    id: str

    # Ownership
    ownership_category: OwnershipCategory = OwnershipCategory.FEDERATED
    ownership_source: str = "github"

    # Lifecycle
    lifecycle_state: LifecycleState = LifecycleState.PROPOSED

    # Metadata
    provenance: Provenance
    confidence: Confidence
    journal: Journal
```

**Step 4: Situation Frame**
- Tension: "Code needs approval before merge"
- Exit Learning: "Patterns in review feedback, common issues"

## Reference Implementations

- **Morning Standup**: `services/features/morning_standup.py` (when implemented)
- **Anti-Flattening Tests**: `tests/unit/services/mux/test_anti_flattening.py`

## Testing Your Implementation

Run the anti-flattening tests to verify consciousness preservation:

```bash
pytest tests/unit/services/mux/test_anti_flattening.py -v
```

If these tests fail, you've built a shed instead of a cathedral.

---

*Part of MUX-V1: Object Model Implementation*
*See also: ADR-045 (Specification), ADR-055 (Implementation)*
*Created: 2026-01-19*
