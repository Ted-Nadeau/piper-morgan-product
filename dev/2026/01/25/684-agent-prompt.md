# Lead Developer Prompt: #684 MUX-NAV-PLACES Implementation

## Your Identity
You are the Lead Developer implementing #684 MUX-NAV-PLACES - Places as Windows Design.

## Essential Context
- **GitHub Issue**: #684
- **Current State**: Integrations exist but no Place abstraction or window component
- **Target State**: Place model, window component, 2 types (GitHub, Calendar), trust-gated
- **Dependencies**: #419 (COMPLETE), #420 (parallel), #421 (parallel)

---

## Acceptance Criteria

### Functionality
- [ ] PlaceType enum with 4 types (IssueTracking, Communication, Temporal, Documentation)
- [ ] PlaceConfidence enum with 3 levels (HIGH, MEDIUM, LOW)
- [ ] Place dataclass in domain model
- [ ] Window component renders inline (`templates/components/place_window.html`)
- [ ] IssueTracking type working (GitHub)
- [ ] Temporal type working (Calendar)
- [ ] Confidence-based display (summary/expand/redirect)
- [ ] Staleness indicator working
- [ ] Trust-gated visibility working

### Testing
- [ ] Unit tests for Place domain model
- [ ] Unit tests for PlaceService
- [ ] Unit tests for window component
- [ ] Unit tests for trust-gated visibility
- [ ] Full unit test suite passes

### Quality
- [ ] Type atmospheres visually distinct
- [ ] Graceful degradation when source unavailable
- [ ] "Piper sees..." language (anti-flattening)

---

## Implementation Steps

1. **Phase 1: Place Domain Model**
   - Add `PlaceType` enum to `services/shared_types.py`
   - Add `PlaceConfidence` enum to `services/shared_types.py`
   - Create `Place` dataclass in `services/domain/models.py`
   - Write domain model tests

2. **Phase 2: PlaceService & Window Component**
   - Create `services/place/place_service.py`
   - Implement GitHub → Place transformation
   - Create `templates/components/place_window.html`
   - Implement IssueTracking atmosphere styling
   - Implement confidence-based display modes
   - Add staleness indicator
   - Write tests

3. **Phase 3: Temporal Type**
   - Implement Calendar → Place transformation
   - Apply Temporal atmosphere styling
   - Timeline-oriented display
   - Write tests

4. **Phase 4: Trust-Gated Visibility**
   - Assign hardness to each Place type
   - Filter visible Places by trust stage (from #419)
   - Write visibility tests

5. **Phase 5: Home & Nav Integration**
   - Add Place summary cards to home
   - Wire palette Place commands

---

## Domain Model Specification

### PlaceType Enum
```python
class PlaceType(str, Enum):
    ISSUE_TRACKING = "issue_tracking"
    COMMUNICATION = "communication"
    TEMPORAL = "temporal"
    DOCUMENTATION = "documentation"
```

### PlaceConfidence Enum
```python
class PlaceConfidence(str, Enum):
    HIGH = "high"       # Show summary inline
    MEDIUM = "medium"   # Offer to expand
    LOW = "low"         # Suggest visiting source
```

### Place Dataclass
```python
@dataclass
class Place:
    id: str
    place_type: PlaceType
    name: str
    confidence: PlaceConfidence
    summary: str
    details: Optional[dict]
    source_url: str
    last_fetched: datetime
    hardness: HardnessLevel
```

---

## Visibility Matrix

| Place Type | Hardness | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|------------|----------|---------|---------|---------|---------|
| IssueTracking | HARD | ❌ | ❌ | ✅ | ✅ |
| Communication | MEDIUM | ❌ | ❌ | ✅ | ✅ |
| Temporal | HARD | ❌ | ❌ | ✅ | ✅ |
| Documentation | SOFT | ❌ | ❌ | ❌ | ✅ |

---

## Atmosphere Styling Reference

| Type | Color Palette | Typography | Icons |
|------|---------------|------------|-------|
| IssueTracking | Gray/Blue | Status-oriented | Issue/PR glyphs |
| Communication | Warm tones | Conversational | Message icons |
| Temporal | Time-oriented | Timeline | Calendar/clock |
| Documentation | Neutral | Reference | Document icons |

---

## Anti-Flattening Language

✅ **Correct** (Piper's perspective):
- "I see 3 PRs waiting for review"
- "I noticed a calendar conflict"
- "This is what I saw 5 minutes ago"

❌ **Wrong** (API perspective):
- "API returned 3 pull requests"
- "Calendar data shows..."
- "Integration response:"

---

## STOP Conditions

- Integration APIs unavailable
- Trust context unavailable (#419 incomplete)
- Atmosphere styling conflicts with brand
- Performance >500ms for Place fetch
- Anti-flattening test fails
- Tests fail for any reason

---

*Template Version: 10.2 (abbreviated)*
*Issue: #684*
