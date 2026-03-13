# MUX-TECH-PHASE3-OWNERSHIP: Implement Ownership Model

**Track**: MUX (Embodied UX)
**Epic**: TECH (Technical Implementation)
**Type**: Implementation
**Priority**: High
**Dependencies**: MUX-TECH-PHASE1-GRAMMAR, VISION-METAPHORS
**Estimated Effort**: 8 hours

---

## Context

The audit found no distinction between objects Piper creates (Native), observes (Federated), or infers (Synthetic). Everything is stored the same way, making it impossible to track provenance or confidence. The ownership model establishes Piper's relationship to every object using the Mind/Senses/Understanding metaphor.

**Anti-Flattening Check**: A flattened version would be a "created_by" field. The real version tracks how Piper relates to information - what it creates, perceives, and understands.

---

## Specification

### 1. Create Ownership Types (2h)
```python
class OwnershipType(Enum):
    """Piper's relationship to objects - discovered through CXO sketching."""
    NATIVE = "native"        # Piper's Mind - what Piper creates/maintains
    FEDERATED = "federated"  # Piper's Senses - what Piper observes externally
    SYNTHETIC = "synthetic"  # Piper's Understanding - what Piper constructs

class OwnershipMetadata:
    """Track ownership with confidence and transformation history."""
    ownership_type: OwnershipType
    confidence: float  # 0.0 to 1.0

    # Provenance
    source: str  # Where this came from
    created_at: datetime
    last_verified: Optional[datetime]

    # Transformations
    derived_from: List[str]  # If synthetic, what sources?
    transformation_chain: List[str]  # How did we get here?

    # Trust implications
    requires_verification: bool  # Federated often needs checking
    user_visible: bool  # Should users see this directly?
    can_modify: bool  # Can Piper change this?
```

### 2. Apply to All Domain Models (3h)
Add to every model in models.py:
```python
# Universal addition to all models
ownership: Optional[OwnershipMetadata] = None

# Examples of application:
@dataclass
class Session:
    # ... existing fields ...
    ownership: OwnershipMetadata = field(
        default_factory=lambda: OwnershipMetadata(
            ownership_type=OwnershipType.NATIVE,  # Piper creates sessions
            confidence=1.0,
            source="piper-core",
            can_modify=True
        )
    )

@dataclass
class GitHubIssue:
    # ... existing fields ...
    ownership: OwnershipMetadata = field(
        default_factory=lambda: OwnershipMetadata(
            ownership_type=OwnershipType.FEDERATED,  # Observed from GitHub
            confidence=0.9,  # API might be stale
            source="github-api",
            requires_verification=True,
            can_modify=False  # Can't change GitHub's truth
        )
    )

@dataclass
class InferredRisk:
    # ... existing fields ...
    ownership: OwnershipMetadata = field(
        default_factory=lambda: OwnershipMetadata(
            ownership_type=OwnershipType.SYNTHETIC,  # Piper inferred this
            confidence=0.7,  # Inference confidence
            source="risk-analysis",
            derived_from=["issue-123", "commit-456"],
            transformation_chain=["pattern-match", "risk-score"],
            requires_verification=True
        )
    )
```

### 3. Create Ownership Transitions (2h)
```python
class OwnershipTransition:
    """How objects move between ownership types."""

    @staticmethod
    def federated_to_synthetic(federated_obj, transformation: str) -> Any:
        """When Piper creates understanding from observations."""
        synthetic_obj = transform(federated_obj, transformation)
        synthetic_obj.ownership = OwnershipMetadata(
            ownership_type=OwnershipType.SYNTHETIC,
            confidence=federated_obj.ownership.confidence * 0.9,
            source=f"synthesized-from-{federated_obj.id}",
            derived_from=[federated_obj.id],
            transformation_chain=[transformation]
        )
        return synthetic_obj

    @staticmethod
    def synthetic_to_native(synthetic_obj, user_confirmation: bool) -> Any:
        """When user confirms Piper's inference, it becomes native."""
        if user_confirmation:
            synthetic_obj.ownership.ownership_type = OwnershipType.NATIVE
            synthetic_obj.ownership.confidence = 1.0
            synthetic_obj.ownership.requires_verification = False
        return synthetic_obj
```

### 4. Implement Ownership-Aware Queries (1h)
```python
class OwnershipAwareRepository:
    """Repository pattern that respects ownership."""

    def get_native_objects(self) -> List[Any]:
        """Get everything Piper owns."""
        return [obj for obj in self.all()
                if obj.ownership.ownership_type == OwnershipType.NATIVE]

    def get_high_confidence(self, min_confidence=0.8) -> List[Any]:
        """Get objects Piper is confident about."""
        return [obj for obj in self.all()
                if obj.ownership.confidence >= min_confidence]

    def get_needs_verification(self) -> List[Any]:
        """Get objects requiring verification."""
        return [obj for obj in self.all()
                if obj.ownership.requires_verification]
```

---

## Acceptance Criteria

- [ ] OwnershipType enum with Native/Federated/Synthetic
- [ ] All models have ownership metadata
- [ ] Sessions are Native, GitHub issues are Federated
- [ ] Synthetic objects track their derivation chain
- [ ] Confidence scores affect visibility/behavior
- [ ] Ownership transitions are traceable
- [ ] Queries can filter by ownership type

---

## Verification

### Ownership Test
Given a GitHub issue that Piper analyzes to identify a risk:
- GitHub issue: FEDERATED (observed)
- Risk analysis: SYNTHETIC (inferred)
- User confirmation: Transforms to NATIVE

Can you trace the ownership chain?

### Anti-Flattening Test
- Is ownership about relationship, not just creator? (Must be relational)
- Does metadata include confidence, not just type? (Must have nuance)
- Can ownership transition based on validation? (Must be dynamic)

---

## References

- Object Model Brief v2: Native/Federated/Synthetic metaphors
- CXO sketches: Mind/Senses/Understanding
- VISION-METAPHORS: Formal metaphor documentation
- Audit Report: "No ownership model" finding

---

## Notes from PM

The metaphors matter:
- **Native = Mind**: What Piper thinks, knows, remembers
- **Federated = Senses**: What Piper sees, hears, observes
- **Synthetic = Understanding**: What Piper figures out, deduces, assembles

This isn't about data ownership in the legal sense - it's about consciousness knowing what's internal vs external vs constructed.

---

*Estimated Effort*: 8 hours
*Priority*: Enables trust gradient and confidence-based behavior
