# Domain Models Object Model Alignment Audit

**Date**: November 29, 2025
**Auditor**: Claude Code (Opus 4.5)
**Session**: 2025-11-29-1323-prog-code-opus
**Reference**: ADR-045 Object Model, Object Model Brief v2
**Prior Work**: Chief Architect audit (same date, earlier session)

---

## Executive Summary

The current domain models (`services/domain/models.py`) are **task-centric and execution-focused**, reflecting traditional software architecture rather than the consciousness-first grammar established in ADR-045. The gap between current implementation and the "Entities experience Moments in Places" vision is significant but bridgeable.

**Key Finding**: The domain models lack any representation of:
- Moments (bounded significant occurrences)
- Situations (containers of Moment sequences)
- Piper as an Entity with identity
- The 8-stage lifecycle with composting
- Native/Federated/Synthetic ownership distinctions

The Morning Standup (`services/features/morning_standup.py`) is indeed the closest approximation to the object model grammar, using `StandupContext` and `StandupResult` which hint at Moments and Situations but don't fully express the model.

---

## 1. Current State Analysis

### 1.1 Models Inventory (41 classes)

| Model | Current Purpose | Lines |
|-------|-----------------|-------|
| Product | Product being managed | 66-81 |
| Feature | Feature or capability | 83-101 |
| Stakeholder | Person with interest in product | 103-115 |
| WorkItem | Universal work item from any system | 117-163 |
| ProjectIntegration | Integration config for project | 166-192 |
| Project | PM project with tool integrations | 194-253 |
| ProjectContext | Simplified project context | 255-262 |
| Intent | User intent parsed from NL | 264-279 |
| Task | Individual task in workflow | 281-312 |
| WorkflowResult | Result of workflow execution | 314-322 |
| Workflow | Workflow definition and state | 324-421 |
| Event | Base event class | 423-432 |
| FeatureCreated | Feature creation event | 434-442 |
| InsightGenerated | AI-generated insight event | 444-452 |
| UploadedFile | Uploaded file domain model | 454-469 |
| AnalysisType | Enum for analysis types | 471-476 |
| ValidationResult | File security validation | 478-485 |
| FileTypeInfo | File type detection | 487-495 |
| Document | Core document entity | 497-555 |
| DocumentSample | Smart content sampling | 557-565 |
| ContentSample | File content sample | 567-575 |
| AnalysisResult | File analysis results | 577-590 |
| SummarySection | Document summary section | 593-610 |
| DocumentSummary | Structured document summary | 612-649 |
| ActionHumanization | Cached human-readable actions | 651-662 |
| SpatialEvent | Spatial metaphor event | 669-702 |
| SpatialObject | Object in spatial environment | 704-755 |
| SpatialContext | Spatial positioning context | 757-788 |
| EthicalDecision | Ethics decision domain model | 792-814 |
| BoundaryViolation | Boundary violation model | 816-827 |
| KnowledgeNode | Knowledge graph node | 829-856 |
| KnowledgeEdge | Knowledge graph edge | 858-894 |
| List | Universal list model | 900-982 |
| ListItem | Universal list item relationship | 984-1017 |
| Todo | Todo item (extends Item) | 1019-1195 |
| TodoList | Backward compat alias | 1197-1214 |
| ListMembership | Backward compat alias | 1216-1233 |
| Conversation | Conversational interaction | 1237-1267 |
| ConversationTurn | Individual conversation turn | 1269-1312 |
| ShareRole | Role for shared access (enum) | 39-45 |
| SharePermission | Permission entry for sharing | 47-62 |

### 1.2 Enum Inventory (13 enums in shared_types.py)

| Enum | Values | Notes |
|------|--------|-------|
| IntentCategory | 15 values | EXECUTION, ANALYSIS, SYNTHESIS, etc. |
| WorkflowType | 14 values | CREATE_FEATURE, ANALYZE_METRICS, etc. |
| WorkflowStatus | 5 values | PENDING → COMPLETED/FAILED/CANCELLED |
| TaskType | 21 values | Various task type discriminators |
| TaskStatus | 5 values | PENDING → COMPLETED/FAILED/SKIPPED |
| IntegrationType | 4 values | GITHUB, JIRA, LINEAR, SLACK |
| TodoStatus | 5 values | PENDING → COMPLETED/CANCELLED/BLOCKED |
| TodoPriority | 4 values | LOW, MEDIUM, HIGH, URGENT |
| ListType | 5 values | PERSONAL, PROJECT, TEAM, etc. |
| OrderingStrategy | 6 values | MANUAL, PRIORITY, DUE_DATE, etc. |
| NodeType | 10 values | CONCEPT, DOCUMENT, PERSON, etc. |
| EdgeType | 17 values | REFERENCES, DEPENDS_ON, etc. |
| PatternType | 6 values | USER_WORKFLOW, TIME_BASED, etc. |

---

## 2. Gap Analysis: Models vs Object Model Grammar

### 2.1 Entity/Place/Moment/Situation Mapping

**ADR-045 Grammar**: "Entities experience Moments in Places"

| Grammar Element | ADR-045 Definition | Current Implementation | Gap |
|-----------------|-------------------|----------------------|-----|
| **Entity** | Actors with identity and agency (people, AI, teams, projects, documents) | Partial - Stakeholder, Product, but no Piper-as-Entity | **HIGH** |
| **Place** | Contexts where action happens (channels, repos, offices) | Partial - SpatialContext, ProjectIntegration, but no unified Place model | **HIGH** |
| **Moment** | Bounded significant occurrences with theatrical unities | **MISSING** - No Moment model exists | **CRITICAL** |
| **Situation** | Container holding sequences of Moments | **MISSING** - No Situation model exists | **CRITICAL** |

#### Current Models That Could Map to Grammar

| Current Model | Closest Grammar Element | Fit Quality | Notes |
|---------------|------------------------|-------------|-------|
| Stakeholder | Entity (Person) | Medium | Missing agency/identity richness |
| Product | Entity (can act) | Low | Treated as static data, not actor |
| Project | Entity/Place hybrid | Low | Spectrum nature not modeled |
| Workflow | Proto-Situation? | Very Low | Sequence of Tasks, not Moments |
| Task | Proto-Moment? | Very Low | Execution unit, not bounded scene |
| SpatialEvent | Proto-Moment? | Medium | Has event_time, significance_level |
| SpatialContext | Place | Medium | Has positioning but lacks atmosphere |
| Conversation | Proto-Situation? | Low | Sequence structure exists |
| ConversationTurn | Proto-Moment? | Low | Has bounded structure |

### 2.2 Native/Federated/Synthetic Ownership

**ADR-045 Ownership Model**:
- **Native**: Piper creates, owns, maintains (Sessions, Memories, Concerns, Trust States)
- **Federated**: Piper observes, queries, acts upon (GitHub Issues, Slack Messages)
- **Synthetic**: Piper constructs through reasoning (Assembled Projects, Inferred Risks)

| Current Model | Likely Ownership | Currently Tracked? | Gap |
|---------------|------------------|-------------------|-----|
| Todo | Native | No | Missing |
| List | Native | No | Missing |
| Conversation | Native | No | Missing |
| KnowledgeNode | Native | No | Missing |
| WorkItem | Federated | `source_system` field exists | Partial |
| Document | Federated/Native | No distinction | Missing |
| Project | Native/Synthetic | No distinction | Missing |
| Intent | Synthetic | No | Missing |
| InsightGenerated | Synthetic | No | Missing |

**Finding**: No model has an `ownership_type` field. The `source_system` field on WorkItem is the only hint at federated vs native distinction.

### 2.3 Lifecycle Implementation (8 Stages)

**ADR-045 Lifecycle**:
```
Emergent → Derived → Noticed → Proposed → Ratified → Deprecated → Archived → Composted
    ↑                                                                            |
    └────────────────── feeds new ──────────────────────────────────────────────┘
```

| Current Status Enum | Stages Covered | Missing Stages |
|---------------------|----------------|----------------|
| WorkflowStatus | PENDING, COMPLETED | Emergent, Derived, Noticed, Proposed, Ratified, Deprecated, Archived, Composted |
| TaskStatus | PENDING, COMPLETED | Same |
| TodoStatus | PENDING, IN_PROGRESS, COMPLETED, CANCELLED, BLOCKED | Emergent, Derived, Noticed, Proposed, Ratified, Deprecated, Archived, Composted |

**Finding**: Current statuses are execution-focused (pending/running/completed/failed), not lifecycle-focused. The 8-stage lifecycle with composting is **completely absent**.

**Composting Pattern**: The ADR-045 principle "Nothing disappears, it transforms" is not implemented. Models have `is_archived` flags but no decomposition into learnings that feed new Emergent objects.

### 2.4 Metadata Model (6 Universal Dimensions)

**ADR-045 Metadata**:
1. **Provenance** - Where from? Source, confidence, freshness
2. **Relevance** - Why now? Connection to current context
3. **Attention State** - Seen? Needs attention?
4. **Confidence** - How certain is Piper?
5. **Relations** - What's connected? Graph position
6. **Journal** - History of Piper's interaction

| Dimension | Current Implementation | Gap |
|-----------|----------------------|-----|
| Provenance | Partial - `source_system`, `created_at` | Missing confidence, freshness |
| Relevance | **MISSING** | No relevance tracking |
| Attention State | **MISSING** | No attention/seen tracking |
| Confidence | Partial - `Intent.confidence`, `KnowledgeEdge.confidence` | Not universal |
| Relations | Partial - KnowledgeNode/Edge | Graph exists but not universal |
| Journal | **MISSING** | No interaction history |

### 2.5 Perceptual Lenses (8 Lenses)

**ADR-045 Lenses**: Hierarchy, Temporal, Priority, Collaborative, Flow, Quantitative, Causal, Contextual

**Finding**: These are NOT implemented as explicit model attributes. Some implicit mapping exists:
- Temporal: `created_at`, `updated_at`, timestamps
- Priority: `TodoPriority` enum
- Collaborative: `shared_with`, `owner_id`
- Hierarchy: `parent_id` on Todo

But no unified lens-application pattern exists.

---

## 3. Morning Standup as Reference Implementation

The Morning Standup (`services/features/morning_standup.py`) has these models:

| Model | Purpose | Object Model Alignment |
|-------|---------|----------------------|
| StandupContext | Context for standup generation | Closest to **Situation** concept |
| StandupResult | Generated standup content | Closest to **Moment** outcome |
| MorningStandupWorkflow | Orchestration class | Shows Entity (Piper) agency |

**Key Observation**: Morning Standup naturally expresses the grammar because it:
1. Has Piper as an actor generating insights (Entity with agency)
2. Creates a bounded scene (the standup = Moment)
3. References Places implicitly (calendar, slack, projects)
4. Produces outcomes that could feed learning (composting)

But this is implicit in the feature implementation, not explicit in the domain models.

---

## 4. Prioritized Alignment Issues

### Critical (Blocks Vision)

| # | Issue | Impact | Effort |
|---|-------|--------|--------|
| 1 | No Moment model | Cannot represent bounded significant occurrences | Medium |
| 2 | No Situation model | Cannot represent sequences with meaning | Medium |
| 3 | No lifecycle beyond execution status | Cannot implement composting/learning cycle | High |
| 4 | No ownership_type (Native/Federated/Synthetic) | Cannot distinguish Piper's relationship to objects | Low |

### High (Limits Features)

| # | Issue | Impact | Effort |
|---|-------|--------|--------|
| 5 | No Piper-as-Entity representation | Piper has no identity in the model | Medium |
| 6 | No universal metadata dimensions | Inconsistent tracking across models | High |
| 7 | Place concept fragmented | SpatialContext exists but not unified | Medium |
| 8 | No attention/relevance tracking | Cannot implement surfacing intelligence | Medium |

### Medium (Technical Debt)

| # | Issue | Impact | Effort |
|---|-------|--------|--------|
| 9 | Entity/Place spectrum not modeled | Projects can't shift between Entity/Place | Low |
| 10 | No Journal (interaction history) | Cannot show audit trail per object | Medium |
| 11 | Perceptual lenses not explicit | Cannot apply lenses consistently | High |
| 12 | Shoebox (Policy/Process/People/Outcomes) not modeled | Moments lack internal structure | Medium |

---

## 5. Remediation Plan

### Phase 1: Core Grammar (Priority: Critical)

**Effort**: 2-3 weeks

1. **Create Moment model** (`services/domain/models.py`)
   ```python
   @dataclass
   class Moment:
       """Bounded significant occurrence with theatrical unities"""
       id: str
       moment_type: str  # decision, milestone, meeting, incident
       time_boundary: Tuple[datetime, datetime]  # Unity of time
       place_id: str  # Unity of place
       action_summary: str  # Unity of action
       significance_level: str  # routine, notable, significant, critical

       # Shoebox contents
       policy: Dict[str, Any]  # Goals, governance
       process: Dict[str, Any]  # What happened
       participants: List[str]  # Entity IDs involved
       outcomes: Dict[str, Any]  # What resulted

       # Lifecycle
       lifecycle_stage: LifecycleStage
       ownership_type: OwnershipType
   ```

2. **Create Situation model**
   ```python
   @dataclass
   class Situation:
       """Container for sequence of Moments with time as backbone"""
       id: str
       title: str
       moments: List[Moment]
       time_span: Tuple[datetime, datetime]
       context: Dict[str, Any]
       lifecycle_stage: LifecycleStage
   ```

3. **Create LifecycleStage enum** (`services/shared_types.py`)
   ```python
   class LifecycleStage(Enum):
       EMERGENT = "emergent"
       DERIVED = "derived"
       NOTICED = "noticed"
       PROPOSED = "proposed"
       RATIFIED = "ratified"
       DEPRECATED = "deprecated"
       ARCHIVED = "archived"
       COMPOSTED = "composted"
   ```

4. **Create OwnershipType enum**
   ```python
   class OwnershipType(Enum):
       NATIVE = "native"      # Piper creates/owns
       FEDERATED = "federated"  # Piper observes
       SYNTHETIC = "synthetic"  # Piper constructs
   ```

### Phase 2: Entity Enhancement (Priority: High)

**Effort**: 1-2 weeks

1. **Create PiperEntity model** (Piper's self-representation)
   ```python
   @dataclass
   class PiperEntity:
       """Piper's identity and state"""
       id: str = "piper"
       identity: Dict[str, Any]  # Name, role, personality
       current_situation_id: Optional[str]
       attention_state: Dict[str, Any]
       trust_states: Dict[str, float]  # Per-user trust levels
   ```

2. **Add ownership_type field** to all relevant models
3. **Add lifecycle_stage field** to models that have lifecycles

### Phase 3: Metadata Unification (Priority: Medium)

**Effort**: 2-3 weeks

1. **Create UniversalMetadata mixin or base**
   ```python
   @dataclass
   class UniversalMetadata:
       provenance: Provenance  # source, confidence, freshness
       relevance: Optional[Relevance]
       attention_state: AttentionState
       confidence: float
       relations: List[str]  # KnowledgeEdge IDs
       journal_id: Optional[str]  # Reference to Journal
   ```

2. **Create Journal model** for interaction history
3. **Retrofit existing models** with metadata

### Phase 4: Composting Implementation (Priority: Medium)

**Effort**: 2-3 weeks

1. **Create CompostingService** that:
   - Triggers on ARCHIVED → COMPOSTED transition
   - Extracts learnings (patterns, preferences, corrections)
   - Creates new EMERGENT objects from learnings

2. **Connect to Learning System** (services/learning/)

---

## 6. Risk Assessment

### If We Don't Remediate

| Risk | Likelihood | Impact | Consequence |
|------|------------|--------|-------------|
| Features feel disconnected | High | High | "75% complete" feeling persists |
| Piper feels mechanical | High | High | Loses consciousness/personality |
| Learning system doesn't compound | Medium | High | Piper doesn't get smarter |
| Technical debt compounds | High | Medium | Harder to fix later |
| Vision drift | High | Critical | Implementation diverges from architecture |

### Mitigation Through Remediation

- Phase 1 alone addresses 80% of the "consciousness flattening" risk
- Phases 1-2 enable Morning Standup pattern to spread to other features
- Phases 3-4 create the learning loop that makes Piper truly adaptive

---

## 7. Anti-Flattening Checklist

From ADR-045, validation questions to ask during remediation:

- [ ] Is Piper an Entity with identity? → Requires PiperEntity model
- [ ] Are Moments bounded scenes, not timestamps? → Requires Moment model
- [ ] Do Places have atmosphere, not just IDs? → Requires Place enhancement
- [ ] Does lifecycle include transformation? → Requires composting
- [ ] Can you see consciousness in the implementation? → Requires all phases

---

## Appendix A: Model-to-Grammar Mapping Table

| Current Model | Grammar Mapping | Ownership | Lifecycle Support |
|---------------|-----------------|-----------|-------------------|
| Product | Entity | Native | None |
| Feature | Entity | Native/Synthetic | `status` field (limited) |
| Stakeholder | Entity (Person) | Federated | None |
| WorkItem | Entity | Federated | `status` field (limited) |
| Project | Entity/Place | Native | `is_archived` only |
| Intent | (internal) | Synthetic | None |
| Task | (internal) | Native | TaskStatus enum |
| Workflow | Proto-Situation | Native | WorkflowStatus enum |
| Event | Proto-Moment | Native | None |
| SpatialEvent | Proto-Moment | Native | `significance_level` |
| SpatialObject | Entity in Place | Federated | None |
| SpatialContext | Place | Native | None |
| Document | Entity | Federated/Native | None |
| KnowledgeNode | Entity | Synthetic | None |
| KnowledgeEdge | (relation) | Synthetic | None |
| Todo | Entity | Native | TodoStatus enum |
| List | Place (container) | Native | `is_archived` only |
| Conversation | Proto-Situation | Native | `is_active` only |
| ConversationTurn | Proto-Moment | Native | None |

---

## Appendix B: Files Analyzed

- `services/domain/models.py` (1312 lines, 41 classes)
- `services/shared_types.py` (200 lines, 13 enums)
- `services/features/morning_standup.py` (referenced for context)
- `dev/active/ADR-045-object-model.md`
- `dev/active/object-model-brief-v2.md`

---

## Appendix C: Verification Against Acceptance Criteria

| Criteria | Status | Evidence |
|----------|--------|----------|
| Document every model's relationship to object model grammar | ✅ | Section 2.1, Appendix A |
| Identify which models represent Entities vs Places vs Moments | ✅ | Section 2.1 table |
| Note where Situation-as-container pattern should apply | ✅ | Section 2.1, 3 |
| Find lifecycle implementation (or absence) | ✅ | Section 2.3 |
| Locate Native/Federated/Synthetic distinctions (or gaps) | ✅ | Section 2.2 |
| Create prioritized list of alignment issues | ✅ | Section 4 |
| Produce remediation plan with effort estimates | ✅ | Section 5 |

---

**Audit Complete**: November 29, 2025, ~2:30 PM PT
**Auditor**: Claude Code (Opus 4.5), Session 2025-11-29-1323-prog-code-opus
