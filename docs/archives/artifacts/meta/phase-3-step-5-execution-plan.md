# Phase 3 Step 5 Execution Plan: Content Template Design

**Created**: September 17, 2025
**Purpose**: Systematic plan for creating evidence-based content templates for Option C (Hub Navigation Format)
**Method**: Same rigorous approach that succeeded in previous steps

## Problem Analysis

**Challenge**: Create content templates that accommodate all Phase 2 categorization data while meeting user requirements and technical constraints

**Requirements to Address**:
1. Must handle all 38 models from Phase 2 results
2. Must include all categorization evidence (layer, tags, purpose)
3. Must provide "full details" as requested by user
4. Must enable cross-references to dependency diagrams
5. Must support maintenance and updates

**Evidence Needed**:
- Actual field structures from Phase 2 evidence
- Successful template patterns from existing docs
- Navigation patterns that work in GitHub markdown

## Step 5 Execution Method

### Sub-step 5.1: Template Component Analysis (15 minutes)

**Extract successful component patterns from existing documentation**

#### Evidence Collection Tasks:
1. **Read domain-models.md model sections** (lines 53-256)
   - How are fields documented?
   - How are relationships shown?
   - What code examples included?

2. **Read ADR implementation sections** (e.g., ADR-028 lines 60-84)
   - How is code integrated with explanation?
   - What level of detail provided?

3. **Read data-model.md entity sections** (lines 30-50+)
   - How are domain vs database distinctions shown?
   - What comparison patterns used?

4. **Extract working patterns**:
   - Field documentation format
   - Relationship notation style
   - Code block integration approach
   - Cross-reference patterns

**Evidence Template**:
```markdown
### Component: [Field Documentation]
**Source**: domain-models.md lines [X-Y]
**Pattern**: [actual format used]
**Effectiveness**: [evidence of usage]
**Adaptation Needed**: [for our requirements]
```

**Quality Check**: Can I show exact examples of each component pattern from existing docs?

### Sub-step 5.2: Phase 2 Data Integration Mapping (20 minutes)

**Map all Phase 2 categorization data to template locations**

#### Mapping Tasks:

1. **Extract from Phase 2 results** for each model:
   - Model name and docstring (evidence line reference)
   - Layer assignment with evidence quote
   - Business tags with field evidence
   - Field list from evidence extraction
   - Relationships noted in evidence

2. **Create data requirement matrix**:
```markdown
| Data Element | Phase 2 Source | Template Location | Format |
|--------------|----------------|-------------------|---------|
| Model name | evidence line X | Heading | ### ModelName |
| Docstring | "exact quote" | Purpose section | **Purpose**: |
| Layer | categorization result | Header warning | ⚠️ DDD Purity: |
| Business tags | #tag evidence | Tags line | **Tags**: #pm #core |
| Fields | extraction doc | Field Structure | code block |
| Relationships | if noted | Relationships section | bullet list |
```

3. **Verify coverage**: All 38 models have complete data
4. **Identify gaps**: What Phase 2 data might be missing?

**Quality Check**: Does template accommodate every piece of Phase 2 data?

### Sub-step 5.3: Template Structure Design (25 minutes)

**Create three template variants based on model complexity**

#### Template A: Simple Domain Model (no relationships)
For models like: EthicalDecision, BoundaryViolation

```markdown
##### ModelName
**Purpose**: [Docstring from Phase 2]
**Layer**: [From categorization]
**Tags**: [From Phase 2 evidence]

**Field Structure**:
```python
field_name: Type              # Field purpose/description
field_name: Optional[Type]    # Optional field explanation
```

**Usage Pattern**:
```python
[Minimal example showing instantiation]
```

**Cross-References**:
- [Relevant link if applicable]
```

#### Template B: Standard Domain Model (with relationships)
For models like: Product, Feature, Workflow

```markdown
##### ModelName
**Purpose**: [Docstring from Phase 2]
**Layer**: [From categorization]
**Tags**: [From Phase 2 evidence]

**Field Structure**:
```python
# Core fields
field_name: Type              # Field purpose/description
field_name: Optional[Type]    # Optional field explanation

# Metadata fields
created_at: datetime          # Standard timestamp
updated_at: datetime          # Standard timestamp
```

**Relationships**:
- `relationship_name`: Connection to RelatedModel
- `other_relationship`: List of OtherModel entities

**Usage Pattern**:
```python
[Example showing instantiation and relationship usage]
```

**Integration Points**:
- Service: [Link to service using this model]
- Repository: [Link to repository pattern]

**Cross-References**:
- Dependency: [Link to dependency diagram section]
- Database: [Link to DB model if exists]
```

#### Template C: Complex Integration Model (external systems)
For models like: WorkItem, ProjectIntegration

```markdown
##### ModelName
**Purpose**: [Docstring from Phase 2]
**Layer**: [From categorization]
**Tags**: [From Phase 2 evidence]
**External Contract**: [What system this integrates with]

**Field Structure**:
```python
# Identity fields
id: str                       # Internal identifier
external_id: str              # External system ID
source_system: str            # System identifier

# Core fields
field_name: Type              # Field purpose/description

# Integration fields
metadata: Dict[str, Any]      # External system data
```

**Relationships**:
- `relationship_name`: Connection to domain model

**Integration Pattern**:
```python
[Example showing external system mapping]
```

**System Mappings**:
- GitHub: `external_id` maps to issue number
- Jira: `external_id` maps to ticket key

**Cross-References**:
- Integration: [Link to integration pattern doc]
- API: [Link to API specification]
```

**Quality Check**: Do templates handle simple, standard, and complex cases?

### Sub-step 5.4: Navigation Template Design (15 minutes)

**Create templates for navigation sections**

#### Hub Navigation Template
```markdown
## Navigation Hub

### By Layer
- [Pure Domain Models](#pure-domain-models) ([X] models) - [Description]
[Generated from Phase 2 categorization counts]

### By Business Function
- [#tag - Description](#tag-models) ([X] models)
[Generated from Phase 2 business tags]

### Quick Lookup
[Alphabetical list generated from all 38 models]
```

#### Layer Section Template
```markdown
### Layer Name
⚠️ **DDD Purity Warning**: [Specific warning for this layer]

[Layer description paragraph]

#### Model Catalog
- **ModelName** - [Purpose from docstring] [#tags]
[List all models in this layer]

#### Model Specifications
[Model templates inserted here]
```

#### Business Function Section Template
```markdown
### #tag Models
Models supporting [business function description]:

| Model | Layer | Purpose |
|-------|-------|---------|
[Table generated from Phase 2 data]

See detailed specifications:
- [ModelName](#modelname) in [Layer Section](#layer)
[Links for each model]
```

**Quality Check**: Does navigation support all three access patterns (layer, function, alphabetical)?

### Sub-step 5.5: Template Validation Protocol (10 minutes)

**Create validation checklist for template completeness**

#### Pre-Implementation Checklist
- [ ] All 38 models have assigned template type (A, B, or C)
- [ ] Phase 2 data mapped to specific template fields
- [ ] Navigation paths verified for all models
- [ ] Cross-reference patterns identified
- [ ] DDD warnings appropriate for each layer

#### Template Field Coverage
For each model verify:
- [ ] Model name from Phase 2
- [ ] Docstring quoted accurately
- [ ] Layer assignment with warning
- [ ] Business tags with evidence
- [ ] All fields from evidence extraction
- [ ] Relationships if noted
- [ ] At least one usage example
- [ ] At least one cross-reference

#### Random Validation Sample
Select 5 random models and verify:
1. Model #8: __________ - Full template population check
2. Model #17: _________ - Full template population check
3. Model #25: _________ - Full template population check
4. Model #31: _________ - Full template population check
5. Model #38: _________ - Full template population check

**Quality Check**: Can someone else verify template population using Phase 2 data?

### Sub-step 5.6: Template Testing (15 minutes)

**Test templates with actual Phase 2 data**

#### Testing Protocol

1. **Select 3 test models** (one from each template type):
   - Simple: EthicalDecision (Pure Domain)
   - Standard: Product (Pure Domain with relationships)
   - Complex: WorkItem (Integration & Transfer)

2. **Populate templates with actual Phase 2 data**:
   - Use exact docstrings from evidence extraction
   - Apply categorization from Phase 2 results
   - Include actual field lists
   - Add real business tags

3. **Verify rendering**:
   - Create test markdown file
   - Check anchor generation
   - Verify code syntax highlighting
   - Test cross-reference links

4. **Measure results**:
   - Line count per model
   - Readability assessment
   - Navigation functionality
   - Search optimization

**Test Results Template**:
```markdown
### Model: [Name]
- Template Type Used: [A/B/C]
- Lines Required: [X]
- Phase 2 Data Coverage: [X/Y fields included]
- Rendering Issues: [None/List issues]
- Navigation Works: [Yes/No]
```

**Quality Check**: Do populated templates meet all user requirements?

## Success Criteria

### Must Achieve
1. **100% Phase 2 Data Integration**: Every categorization decision represented
2. **Template Coverage**: All 38 models have appropriate template
3. **Navigation Completeness**: Three access patterns all functional
4. **Cross-Reference Accuracy**: Links to correct sections/files
5. **User Requirement Match**: All 16 requirements addressed

### Quality Indicators
- Templates can be populated without consulting models.py
- Navigation enables finding any model in <3 clicks
- Cross-references connect to actual documentation
- DDD warnings clear and appropriate
- Examples help understanding

### Red Flags to Reject
- Any model without complete Phase 2 data
- Templates requiring information not in evidence
- Navigation paths that don't resolve
- Cross-references to non-existent docs
- Missing user requirements

## Deliverable Format

```markdown
# Phase 3 Step 5 Results: Content Template Design

## Template Component Analysis
[Evidence of successful patterns from existing docs]

## Phase 2 Data Integration Mapping
[Complete mapping matrix for all 38 models]

## Template Designs

### Template A: Simple Domain Model
[Complete template with example]

### Template B: Standard Domain Model
[Complete template with example]

### Template C: Complex Integration Model
[Complete template with example]

## Navigation Templates
[All navigation section templates]

## Validation Results
[Checklist completion and test results]

## Ready for Implementation
- All 38 models mapped to templates
- Phase 2 data fully integrated
- Navigation patterns verified
- Cross-references validated
```

## Time Estimate

- Sub-step 5.1: Component Analysis - 15 minutes
- Sub-step 5.2: Data Mapping - 20 minutes
- Sub-step 5.3: Template Design - 25 minutes
- Sub-step 5.4: Navigation Design - 15 minutes
- Sub-step 5.5: Validation Protocol - 10 minutes
- Sub-step 5.6: Template Testing - 15 minutes

**Total: 100 minutes of systematic, careful work**

---

**Next Step**: Execute this plan methodically, creating evidence-based templates that accommodate all Phase 2 data while meeting user requirements
