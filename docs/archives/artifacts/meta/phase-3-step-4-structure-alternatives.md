# Phase 3 Step 4: Structure Design with Alternatives

**Created**: September 17, 2025
**Method**: Evidence-based design of three alternative structures
**Purpose**: Present options for models-architecture.md organization

## Option A: Layered Reference Format (Based on domain-models.md pattern)

**Based on**: Current domain-models.md structure (lines 1-480) - proven successful
**Primary Organization**: Technical architecture layers with detailed subsections

### Structure Outline
```markdown
# Models Architecture

## Quick Reference
[Categorized model lists by layer - enables fast scanning]

## Pure Domain Models (8 models)
⚠️ DDD Purity: No infrastructure dependencies allowed

### Product
**Business Purpose**: Core entity for product management
**Business Tags**: #pm #core
[Full field documentation with types and defaults]
[Relationships section]
[Usage examples]

### Feature
[Same detailed format for all 8 models]

## Supporting Domain Models (7 models)
⚠️ DDD Purity: Business concepts with structural needs

[7 models with same detailed format]

## Integration & Transfer Models (15 models)
⚠️ DDD Purity: External system contracts and DTOs

[15 models with same detailed format]

## Infrastructure Models (8 models)
⚠️ DDD Purity: System mechanisms only

[8 models with same detailed format]

## Cross-Reference Guide
[Links to dependency diagrams and related docs]
```

### Pros (Evidence-Based)
- **Proven pattern**: domain-models.md uses this successfully (479 lines, comprehensive)
- **User requirement match**: "layers first" explicitly requested (7:05 PM)
- **Search optimized**: Each model gets dedicated heading for Ctrl+F
- **Complete details**: Full field documentation as requested

### Cons (Evidence-Based)
- **Length concern**: 38 models × ~30 lines = 1,140 lines (approaching limit)
- **Scrolling required**: Must navigate through all layers to find specific model
- **Redundancy**: Similar format repeated 38 times

---

## Option B: Compact Matrix Format (Based on ADR conciseness)

**Based on**: ADR-028's structured problem/solution format (178 lines for complex topic)
**Primary Organization**: Layers with compressed model documentation

### Structure Outline
```markdown
# Models Architecture

## Architecture Overview
[Visual layer diagram with model counts]

## Model Inventory by Layer

### Pure Domain Models (8)
| Model | Purpose | Business Tags | Key Fields |
|-------|---------|--------------|------------|
| Product | Product management entity | #pm | name, vision, strategy |
| Feature | Product capabilities | #pm | hypothesis, acceptance_criteria |
[Table continues for all 8]

### Supporting Domain Models (7)
[Same table format]

### Integration & Transfer Models (15)
[Same table format]

### Infrastructure Models (8)
[Same table format]

## Model Details

### Pure Domain Models

#### Product
```python
@dataclass
class Product:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    vision: str = ""
    # ... compressed field listing
```
**Relationships**: features, stakeholders
**Integration Points**: [Link to dependency diagram]

[Compressed details for all 38 models]

## Integration Guide
[Cross-references and update instructions]
```

### Pros (Evidence-Based)
- **Efficient overview**: Tables provide quick scanning (domain-models-index.md uses this)
- **Manageable size**: ~800 lines total (well under limit)
- **Progressive disclosure**: Overview first, details second
- **Easy comparison**: Side-by-side model comparison in tables

### Cons (Evidence-Based)
- **Less detail**: Compressed format may miss "full details" requirement
- **Two-step lookup**: Must check table then jump to details
- **Table maintenance**: Harder to update tables than sections

---

## Option C: Hub Navigation Format (Based on domain-models-index.md)

**Based on**: domain-models-index.md hub pattern + data-model.md distinctions approach
**Primary Organization**: Navigation-first with categorized deep dives

### Structure Outline
```markdown
# Models Architecture

## Navigation Hub

### By Layer
- [Pure Domain Models](#pure-domain-models) (8) - Business concepts only
- [Supporting Domain Models](#supporting-domain-models) (7) - Business + structure
- [Integration & Transfer Models](#integration-transfer-models) (15) - External contracts
- [Infrastructure Models](#infrastructure-models) (8) - System mechanisms

### By Business Function
- [#pm - Product Management](#pm-models) (12 models)
- [#workflow - Process Orchestration](#workflow-models) (8 models)
- [#knowledge - Information Management](#knowledge-models) (9 models)
- [#spatial - Spatial Intelligence](#spatial-models) (5 models)
- [#ethics - Safety & Boundaries](#ethics-models) (2 models)
- [#system - Infrastructure](#system-models) (8 models)

### Quick Lookup
[Alphabetical model index with layer and tags]

## Layer Documentation

### Pure Domain Models
⚠️ **DDD Purity Warning**: No infrastructure dependencies

These models represent core business concepts without technical concerns:

#### Model Catalog
- **Product** - Product management entity [#pm]
- **Feature** - Product capabilities [#pm]
- **Stakeholder** - Product stakeholders [#pm]
[List continues with business purpose]

#### Model Specifications

##### Product
**Purpose**: Core product management entity
**Layer**: Pure Domain
**Tags**: #pm #core

**Field Structure**:
```python
id: str                    # Unique identifier
name: str                  # Product name
vision: str                # Product vision statement
strategy: str              # Strategic approach
created_at: datetime       # Creation timestamp
updated_at: datetime       # Last modification
```

**Relationships**:
- `features`: List of associated Feature entities
- `stakeholders`: List of Stakeholder entities
- `work_items`: Associated WorkItem entities

**Usage Pattern**:
```python
product = Product(
    name="Piper Morgan",
    vision="AI-powered PM assistant",
    strategy="Autonomous task execution"
)
```

**Cross-References**:
- Dependency: [Product Service Diagram](dependency-diagrams.md#product-service)
- Database: [ProductDB mapping](data-model.md#productdb)
- ADR: [Domain Model Design](adr/adr-xyz.md)

[Pattern continues for all models]

## Business Function Views
[Alternative organization by business function]

## Maintenance Guide
[How to update when models change]
```

### Pros (Evidence-Based)
- **Multiple navigation paths**: By layer AND business function as requested
- **Hub pattern proven**: domain-models-index.md successfully uses this approach
- **Progressive detail**: Overview → Catalog → Specifications
- **Cross-reference rich**: Multiple connection points to other docs
- **User requirement match**: Addresses all 16 documented requirements

### Cons (Evidence-Based)
- **More complex structure**: Three levels of navigation
- **Potential redundancy**: Models appear in multiple organizations
- **Longer document**: ~1,200 lines with full navigation

---

## Recommendation Based on Evidence

**Recommended: Option C - Hub Navigation Format**

### Evidence Supporting Decision

1. **User requirement match**: "layers first, business tags, full details, x-ref diagrams" (7:05 PM)
   - ✅ Layers are primary organization
   - ✅ Business tags included with dual navigation
   - ✅ Full details in specification sections
   - ✅ Cross-references throughout

2. **Local pattern match**: domain-models-index.md uses hub successfully
   - Same navigation-first approach
   - Proven to work in this codebase
   - Users familiar with pattern

3. **Data compatibility**: Handles all 38 models from Phase 2
   - Each model gets full specification section
   - Relationships documented explicitly
   - Business tags from categorization included

4. **Maintenance evidence**: Progressive structure supports updates
   - Quick lookup for finding models
   - Clear sections for additions
   - Separates navigation from content

5. **Navigation evidence**: Multiple access paths reduce friction
   - By layer (technical audience)
   - By business function (domain audience)
   - Alphabetical (quick lookup)

### Rejected Options

**Option A (Layered Reference)**: Too long, single navigation path
- Would exceed comfortable length with 38 detailed models
- No business function navigation as requested

**Option B (Compact Matrix)**: Insufficient detail
- Tables don't provide "full details" as requested
- Harder to maintain with field changes

## Next Steps

With Option C selected based on evidence:
1. Proceed to Step 5: Design detailed content templates
2. Ensure templates handle all Phase 2 categorization data
3. Plan integration with existing documentation
