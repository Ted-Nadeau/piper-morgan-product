# Gameplan: #684 MUX-NAV-PLACES - Places as Windows Design

**Issue**: #684
**Priority**: P1
**Sprint**: P1 (Navigation Paradigm)
**Epic**: #418 MUX-IMPLEMENT
**Created**: 2026-01-25

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Template engine: Jinja2 (confirmed)
- [x] Integrations: `services/integrations/` (GitHub, Slack, Calendar, Notion)
- [x] Spatial service: `services/spatial/` exists
- [x] Trust context: Available from #419
- [x] HardnessLevel: Enum in shared_types.py

**My understanding of the task**:
- I believe we need to: Create Place abstraction for inline "window" views of external sources
- I think this involves: Domain model, window component, 2 integration transformations, trust-gating
- I assume the current state is: Integrations exist but no Place abstraction or window component

### Part A.2: Work Characteristics Assessment

**Assessment:**
- [x] **SKIP WORKTREE** - Single Lead Dev, new paradigm but sequential phases
- Document rationale: New abstraction but builds on existing integrations, sequential implementation

### Part B: PM Verification

**What actually exists**:
```bash
# Integrations
ls -la services/integrations/

# Spatial service
ls -la services/spatial/

# Existing templates
ls -la templates/components/

# Trust types
grep -n "TrustStage\|HardnessLevel" services/shared_types.py
```

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding correct

---

## Phase 0: Initial Bookending

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 684
   ```

2. **Codebase Investigation**
   ```bash
   # Check existing integration patterns
   grep -rn "def get_" services/integrations/github/ --include="*.py" | head -10

   # Check calendar integration
   grep -rn "def get_" services/integrations/calendar/ --include="*.py" | head -10

   # Check spatial patterns
   ls -la services/spatial/
   ```

3. **Survey Window Component Patterns**
   - Cards in existing templates
   - Summary/expand patterns
   - Inline vs modal approaches

### STOP Conditions Check
- [x] Issue exists: #684 confirmed
- [x] GitHub integration exists: Yes
- [x] Calendar integration exists: Yes
- [x] #419 provides trust context: Yes

---

## Phase 0.5: Frontend-Backend Contract (Minimal)

### When to Apply
- [x] New UI component - YES (window)

### Required Actions
- Window component is client-side (Jinja2 template)
- May need PlaceService endpoint for data
- Trust context from template (from #419)

---

## Phases 1-5: Development Work

### Phase 1: Place Domain Model

**Objective**: Create Place abstraction in domain layer

**Tasks**:
- [ ] Add PlaceType enum to `services/shared_types.py`
- [ ] Add PlaceConfidence enum to `services/shared_types.py`
- [ ] Create Place dataclass in `services/domain/models.py`
- [ ] Write domain model tests

**PlaceType Enum**:
```python
class PlaceType(str, Enum):
    ISSUE_TRACKING = "issue_tracking"     # GitHub, Linear, Jira
    COMMUNICATION = "communication"        # Slack, Email
    TEMPORAL = "temporal"                  # Calendar, Scheduling
    DOCUMENTATION = "documentation"        # Notion, Confluence
```

**PlaceConfidence Enum**:
```python
class PlaceConfidence(str, Enum):
    HIGH = "high"       # Show summary inline
    MEDIUM = "medium"   # Offer to expand
    LOW = "low"         # Suggest visiting source
```

**Place Dataclass** (sketch):
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

**Verification**:
```bash
grep -n "PlaceType" services/shared_types.py
grep -n "class Place" services/domain/models.py
python -m pytest tests/unit/services/domain/test_place_model.py -v
```

### Phase 2: PlaceService & Window Component (IssueTracking)

**Objective**: Implement first Place type with window rendering

**Tasks**:
- [ ] Create `services/place/place_service.py`
- [ ] Implement GitHub → Place transformation
- [ ] Create `templates/components/place_window.html`
- [ ] Implement IssueTracking atmosphere styling
- [ ] Implement confidence-based display modes
- [ ] Add staleness indicator
- [ ] Write tests

**Atmosphere Styling** (IssueTracking):
- Color: Focused gray/blue
- Typography: Status-oriented
- Icons: Issue/PR glyphs

**Display Modes**:
| Confidence | Behavior |
|------------|----------|
| HIGH | Show summary inline ("3 PRs need review") |
| MEDIUM | Show summary + "Expand" button |
| LOW | Show link + "Check GitHub directly?" |

**Verification**:
```bash
ls -la services/place/
ls -la templates/components/place_window.html
python -m pytest tests/unit/services/test_place_service.py -v
```

### Phase 3: Temporal Place Type (Calendar)

**Objective**: Implement second Place type

**Tasks**:
- [ ] Implement Calendar → Place transformation
- [ ] Apply Temporal atmosphere styling
- [ ] Timeline-oriented display mode
- [ ] Conflict awareness display
- [ ] Write tests

**Atmosphere Styling** (Temporal):
- Color: Time-oriented warm tones
- Typography: Timeline-oriented
- Icons: Calendar/clock glyphs

**Verification**:
```bash
python -m pytest tests/unit/services/test_place_service.py::test_calendar -v
```

### Phase 4: Trust-Gated Visibility

**Objective**: Filter Places by trust stage

**Tasks**:
- [ ] Assign hardness to each Place type
- [ ] Filter visible Places by trust stage from #419
- [ ] Write visibility tests

**Visibility Matrix**:
| Place Type | Hardness | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|------------|----------|---------|---------|---------|---------|
| IssueTracking | HARD | ❌ | ❌ | ✅ | ✅ |
| Communication | MEDIUM | ❌ | ❌ | ✅ | ✅ |
| Temporal | HARD | ❌ | ❌ | ✅ | ✅ |
| Documentation | SOFT | ❌ | ❌ | ❌ | ✅ |

**Verification**:
```bash
python -m pytest tests/unit/services/test_place_visibility.py -v
```

### Phase 5: Home & Nav Integration

**Objective**: Wire Places into home state and nav

**Tasks**:
- [ ] Add Place summary cards to home (#419)
- [ ] Add Place items to nav (#420)
- [ ] Wire palette Place commands (#421)
- [ ] Write integration evidence

**Verification**:
```bash
grep -n "place" templates/home.html
grep -n "place" templates/components/nav_panel.html
```

---

## Phase Z: Final Bookending

### Required Actions

1. **Test Suite**
   ```bash
   python -m pytest tests/unit/ -v --tb=line | tail -20
   ```

2. **Acceptance Criteria Check**
   - [ ] PlaceType enum with 4 types
   - [ ] Place dataclass in domain
   - [ ] Window component renders
   - [ ] IssueTracking type working
   - [ ] Temporal type working
   - [ ] Confidence-based display
   - [ ] Trust-gated visibility

3. **GitHub Update**
   ```bash
   gh issue edit 684 --body "Status: Complete - Awaiting PM Approval"
   ```

---

## STOP Conditions

- Integration APIs unavailable
- Trust context unavailable (#419 incomplete)
- Atmosphere styling conflicts with brand
- Performance >500ms for Place fetch
- Anti-flattening test fails ("API returned" instead of "Piper sees")
- Tests fail for any reason

---

## Success Criteria

- [ ] All acceptance criteria met
- [ ] 30+ new tests
- [ ] No regressions
- [ ] 2 Place types working (IssueTracking, Temporal)
- [ ] PM approval

---

## Design Principles Reference

### The Core Insight
> "What if Places aren't links you click to leave Piper, but windows that show you what Piper sees there?"

### Atmosphere Belongs to Place-TYPE
- **IssueTracking**: Focused, status-oriented
- **Communication**: Conversational, time-sensitive
- **Temporal**: Timeline-oriented, conflict-aware
- **Documentation**: Reference-oriented, searchable

### FEDERATED Epistemology
- Piper *observes* these sources
- Piper *interprets* what she sees
- Piper *acknowledges* uncertainty ("This is what I saw 5 minutes ago")

### Anti-Flattening Language
- ✅ "I see 3 PRs waiting for review"
- ✅ "I noticed a calendar conflict"
- ❌ "API returned 3 pull requests"
- ❌ "Calendar data shows..."

---

*Gameplan created: 2026-01-25*
*Template version: v9.3*
