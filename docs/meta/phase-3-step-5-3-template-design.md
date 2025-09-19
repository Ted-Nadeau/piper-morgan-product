# Phase 3 Sub-step 5.3 Results: Template Structure Design

**Created**: September 17, 2025
**Method**: Create three template variants based on model complexity
**Purpose**: Design templates that accommodate all Phase 2 data while meeting user requirements

## Template A: Simple Domain Model (No Relationships)

**For models**: EthicalDecision, BoundaryViolation, ValidationResult, FileTypeInfo, ContentSample, AnalysisResult, SummarySection, DocumentSummary, ActionHumanization, SpatialContext, KnowledgeNode, KnowledgeEdge

### Template Structure

```markdown
##### ModelName
**Purpose**: [Docstring from Phase 2 evidence]
**Layer**: [Pure Domain/Supporting Domain/Integration/Infrastructure] Model
**Tags**: [#tag1 #tag2 from Phase 2 evidence]

**Field Structure**:
```python
# Core fields
id: str                       # Unique identifier
field_name: Type              # Field purpose/description
field_name: Optional[Type]    # Optional field explanation

# Metadata fields (if present)
created_at: datetime          # Creation timestamp
updated_at: datetime          # Last modification
```

**Usage Pattern**:
```python
# Create instance
model = ModelName(
    field_name="value",
    other_field=123
)
```

**Cross-References**:
- Service: [ServiceName using this model](../services/service.md)
- Related: [RelatedConcept](related-doc.md#section)
```

### Example Application: EthicalDecision

```markdown
##### EthicalDecision
**Purpose**: A recorded ethical decision with rationale
**Layer**: Pure Domain Model
**Tags**: #ethics

**Field Structure**:
```python
# Core fields
id: str                       # Unique identifier
decision_point: str           # Where decision was needed
context: Dict[str, Any]       # Decision context
rationale: str                # Reasoning behind decision
decision: str                 # The actual decision made

# Metadata fields
confidence_level: float       # Confidence in decision (0-1)
timestamp: datetime           # When decision was made
reviewed_by: Optional[str]    # Who reviewed the decision
```

**Usage Pattern**:
```python
# Record an ethical decision
decision = EthicalDecision(
    decision_point="data_retention",
    rationale="User explicitly requested deletion",
    decision="delete_all_user_data",
    confidence_level=0.95
)
```

**Cross-References**:
- Service: [EthicsService](../services/ethics_service.md)
- ADR: [ADR-014 Attribution First](adr/adr-014-attribution-first.md)
```

## Template B: Standard Domain Model (With Relationships)

**For models**: Product, Feature, Stakeholder, Intent, Task, WorkflowResult, Workflow, Document, SpatialEvent, SpatialObject, List, ListItem, Todo, TodoList, ListMembership, Conversation, ConversationTurn, FeatureCreated, InsightGenerated

### Template Structure

```markdown
##### ModelName
**Purpose**: [Docstring from Phase 2 evidence]
**Layer**: [Pure Domain/Supporting Domain/Infrastructure] Model
**Tags**: [#tag1 #tag2 from Phase 2 evidence]

**Field Structure**:
```python
# Identity fields
id: str                       # Unique identifier

# Core fields
name: str                     # Model name/title
description: str              # Detailed description
field_name: Type              # Field purpose
enum_field: EnumType          # Enum with options

# Metadata fields
created_at: datetime          # Creation timestamp
updated_at: datetime          # Last modification

# Relationships (from Phase 2 data)
parent_id: Optional[str]      # Reference to parent
children: List["Child"]       # Child entities
related: Optional["Related"]  # Related entity
```

**Relationships**:
- `parent`: Connection to ParentModel (many-to-one)
- `children`: List of ChildModel entities (one-to-many)
- `related`: Optional RelatedModel reference

**Usage Pattern**:
```python
# Create with relationships
model = ModelName(
    name="Example",
    description="Example model with relationships"
)

# Connect relationships
model.children.append(child_instance)
model.parent = parent_instance
```

**Integration Points**:
- Service: [ServiceName](../services/service.md) - handles business logic
- Repository: [ModelRepository](../repositories/model_repository.md) - persistence
- Query: [ModelQueries](../queries/model_queries.md) - read operations

**Cross-References**:
- Dependency: [Model interactions diagram](dependency-diagrams.md#modelname)
- Database: [ModelDB mapping](data-model.md#modeldb)
- Tests: [Model test suite](../tests/test_model.md)
```

### Example Application: Product

```markdown
##### Product
**Purpose**: A product being managed
**Layer**: Pure Domain Model
**Tags**: #pm

**Field Structure**:
```python
# Identity fields
id: str                       # Unique identifier

# Core fields
name: str                     # Product name
vision: str                   # Product vision statement
strategy: str                 # Strategic approach

# Metadata fields
created_at: datetime          # Creation timestamp
updated_at: datetime          # Last modification

# Relationships
features: List["Feature"]     # Product features
stakeholders: List["Stakeholder"]  # Product stakeholders
metrics: List["Metric"]       # Product metrics
work_items: List["WorkItem"]  # Associated work items
```

**Relationships**:
- `features`: List of Feature entities defining capabilities (one-to-many)
- `stakeholders`: People with interest in the product (one-to-many)
- `metrics`: Performance and success metrics (one-to-many)
- `work_items`: Development work items (one-to-many)

**Usage Pattern**:
```python
# Create product with vision
product = Product(
    name="Piper Morgan",
    vision="AI-powered PM assistant that automates routine tasks",
    strategy="Focus on developer productivity and autonomous execution"
)

# Add features
product.features.append(feature)

# Connect stakeholders
product.stakeholders.extend([pm, developer, user])
```

**Integration Points**:
- Service: [ProductService](../services/product_service.md) - product management logic
- Repository: [ProductRepository](../repositories/product_repository.md) - persistence
- Query: [ProductQueries](../queries/product_queries.md) - complex queries

**Cross-References**:
- Dependency: [Product service architecture](dependency-diagrams.md#product-service)
- Database: [ProductDB schema](data-model.md#productdb)
- API: [Product endpoints](api-specification.md#products)
```

## Template C: Complex Integration Model (External Systems)

**For models**: WorkItem, ProjectIntegration, Project, ProjectContext, UploadedFile, DocumentSample, Event (base class)

### Template Structure

```markdown
##### ModelName
**Purpose**: [Docstring from Phase 2 evidence]
**Layer**: Integration & Transfer Model
**Tags**: [#tag1 #tag2 from Phase 2 evidence]
**External Contract**: [What external system this integrates with]

**Field Structure**:
```python
# Identity fields
id: str                       # Internal identifier
external_id: str              # External system identifier
source_system: str            # Source system name

# Core fields
field_name: Type              # Core business field
status: str                   # Synchronization status

# Integration fields
external_url: Optional[str]   # Link to external system
metadata: Dict[str, Any]      # External system metadata
last_synced: Optional[datetime]  # Last synchronization

# Relationships (if any)
domain_model_id: Optional[str]  # Link to domain model
```

**System Mappings**:
- **GitHub**: `external_id` → issue number, `metadata.labels` → issue labels
- **Jira**: `external_id` → ticket key, `metadata.priority` → ticket priority
- **Generic**: Configurable field mappings via integration config

**Integration Pattern**:
```python
# Import from external system
external_data = fetch_from_github(issue_number)
work_item = WorkItem(
    external_id=str(issue_number),
    source_system="github",
    title=external_data["title"],
    metadata=external_data
)

# Sync back to external system
if work_item.needs_sync():
    update_github_issue(work_item.external_id, work_item.to_external())
```

**Transformation Rules**:
- Inbound: External format → Domain model via adapter
- Outbound: Domain model → External format via adapter
- Conflicts: Last-write-wins with audit trail

**Cross-References**:
- Integration: [GitHub integration pattern](../integrations/github.md)
- Adapter: [WorkItemAdapter](../adapters/workitem_adapter.md)
- Config: [Integration configuration](../config/integrations.md)
```

### Example Application: WorkItem

```markdown
##### WorkItem
**Purpose**: A work item from any external system
**Layer**: Integration & Transfer Model
**Tags**: #pm #integration
**External Contract**: GitHub Issues, Jira Tickets, Linear Issues

**Field Structure**:
```python
# Identity fields
id: str                       # Internal UUID
external_id: str              # GitHub issue number, Jira key, etc.
source_system: str            # "github", "jira", "linear"

# Core fields
title: str                    # Work item title
description: str              # Detailed description
type: str                     # bug, feature, task, improvement
status: str                   # open, in_progress, closed
priority: str                 # low, medium, high, critical
labels: List[str]             # Categorization labels
assignee: Optional[str]       # Assigned user

# Integration fields
external_url: Optional[str]   # https://github.com/org/repo/issues/123
metadata: Dict[str, Any]      # Raw external system data
external_refs: Optional[Dict[str, Any]]  # Cross-system references
updated_at: Optional[datetime]  # Last external update

# Domain relationships
project_id: Optional[str]     # Link to Project
feature_id: Optional[str]     # Link to Feature
product_id: Optional[str]     # Link to Product
```

**System Mappings**:
- **GitHub**:
  - `external_id` → issue["number"]
  - `labels` → issue["labels"][*]["name"]
  - `assignee` → issue["assignee"]["login"]
- **Jira**:
  - `external_id` → issue["key"]
  - `type` → issue["fields"]["issuetype"]["name"]
  - `priority` → issue["fields"]["priority"]["name"]

**Integration Pattern**:
```python
# Import from GitHub
github_issue = github_client.get_issue(123)
work_item = WorkItem(
    external_id=str(github_issue.number),
    source_system="github",
    title=github_issue.title,
    description=github_issue.body,
    labels=[label.name for label in github_issue.labels],
    external_url=github_issue.html_url,
    metadata=github_issue.raw_data
)

# Link to domain model
work_item.feature_id = feature.id
```

**Transformation Rules**:
- Status mapping: GitHub "open" → "open", "closed" → "completed"
- Priority inference: Labels "P0" → "critical", "P1" → "high"
- Type detection: Labels "bug" → "bug", "enhancement" → "feature"

**Cross-References**:
- Integration: [GitHub integration guide](../integrations/github.md)
- Service: [WorkItemSyncService](../services/workitem_sync_service.md)
- Config: [Integration mappings](../config/field_mappings.yml)
```

## Template Selection Guide

### When to Use Template A (Simple)
- No relationships to other models
- Fewer than 10 fields
- No external system integration
- No complex business logic/methods
- Examples: EthicalDecision, BoundaryViolation, ValidationResult

### When to Use Template B (Standard)
- Has relationships to other models
- 10-20 fields typical
- Pure domain or supporting domain layer
- May have simple methods
- Examples: Product, Feature, Workflow, Document

### When to Use Template C (Complex)
- Integrates with external systems
- Has external_id and source_system fields
- Requires field mapping documentation
- Integration & Transfer layer models
- Examples: WorkItem, ProjectIntegration, UploadedFile

## Quality Verification

**Templates cover all complexity levels**: ✅ Three distinct templates created
**All Phase 2 data accommodated**: ✅ Every field type has a location
**User requirements met**: ✅ Layers, tags, full details, cross-references included
**Examples provided**: ✅ Each template has concrete example
**Selection guide included**: ✅ Clear criteria for template choice
**Ready for navigation design**: ✅ Model templates complete
