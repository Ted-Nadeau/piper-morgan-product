# Domain Models Documentation Rewrite Methodology

**Created**: September 17, 2025
**Purpose**: Systematic approach to completely rewrite domain-models.md to reflect current reality

## User Requirements
- **Complete rewrite** (vs incremental) due to significant drift
- **Technical layers first** with business function tags/labels
- **Full field details** for complete reference documentation
- **Cross-reference** to dependency diagrams (avoid duplication/drift)
- **Update dependency diagrams after** domain models complete

## 6-Phase Systematic Method

### Phase 1: Current State Analysis (15 min)
**Goal**: Extract complete, accurate inventory from models.py

1. **Model Inventory**: Extract all @dataclass definitions from models.py
2. **Field Analysis**: Document field types, defaults, and optional status for each model
3. **Relationship Mapping**: Identify all relationship fields and their directions
4. **Import Dependencies**: Note all shared_types enums and external imports
5. **Architecture Pattern Analysis**: Identify layering patterns (Core, Service, Integration, etc.)

**Deliverable**: Complete model inventory with field counts and layer classification

**Quality Check**: Can I generate a complete model list with field counts? Do I understand the layering structure?

### Phase 2: Technical Layer Categorization (10 min)
**Goal**: Organize models by technical architecture layers with DDD purity levels

1. **Pure Domain Models**: ⚠️ No database imports, no infrastructure concerns
   - Core business concepts and rules
2. **Supporting Domain Models**: ⚠️ Business concepts that need structured data
   - Domain concepts with data structure needs
3. **Integration & Transfer Models**: ⚠️ External system contracts and DTOs
   - Adapters and external system models
4. **Infrastructure Models**: ⚠️ System mechanism support
   - Events, conversations, validation utilities
5. **Business Function Tags**: Add secondary labels (PM, Knowledge, Spatial, etc.)

**Deliverable**: Categorized model list with primary layer + business tags

**Quality Check**: Would a new developer understand the layering logic and where to find models?

### Phase 3: Documentation Structure Design (10 min)
**Goal**: Create consistent, developer-friendly format

1. **Template Design**: Consistent format for each model section
   - Model purpose and business context
   - Full field listing with types and defaults
   - Relationship documentation
   - Business function tags
2. **Navigation Design**: Layer-based table of contents with business function index
3. **Cross-Reference Strategy**: Links to patterns, dependency diagrams, shared_types
4. **Code Example Strategy**: Realistic usage examples per layer

**Deliverable**: Documentation template and structure plan

**Quality Check**: Does the structure serve both quick reference and deep study needs?

### Phase 4: Content Generation (60 min)
**Goal**: Systematically document all models with full accuracy

1. **Layer-by-Layer Documentation**: Work through each technical layer in order
2. **Model Deep Dive**: For each model:
   - Purpose and business context
   - Complete field listing with types, defaults, optionality
   - Relationship fields with directions and cardinality
   - Business function tags
3. **Usage Examples**: Layer-appropriate code examples
4. **Cross-Reference Integration**: Links to related documentation

**Deliverable**: Complete model documentation organized by technical layers

**Quality Check**: Spot-check 3 random models against actual models.py source - do fields, types, and defaults match exactly?

### Phase 5: Accuracy Verification (15 min)
**Goal**: Ensure 100% accuracy with current implementation

1. **Field Verification**: Confirm all fields match current models.py implementation
2. **Type Verification**: Check all type annotations are correct
3. **Import Verification**: Ensure all referenced shared_types exist
4. **Relationship Verification**: Confirm bidirectional relationships are accurate
5. **Example Verification**: Test that code examples are syntactically correct

**Deliverable**: Verified, accurate documentation

**Quality Check**: Would this documentation help a developer implement correctly without consulting source code?

### Phase 6: Integration & Polish (10 min)
**Goal**: Professional finish and integration with existing docs

1. **Metadata Update**: Set current date, status, accurate file references
2. **Cross-Reference Links**: Add links to dependency diagrams, patterns, ADRs
3. **Business Function Index**: Create searchable tags for business contexts
4. **Format Consistency**: Clean markdown, consistent styling
5. **Final Review**: Complete read-through for clarity and flow

**Deliverable**: Publication-ready domain models documentation

**Quality Check**: Does this documentation meet the standard of other high-quality docs in the project?

## Success Criteria
- **100% Model Coverage**: All models in models.py documented
- **Accurate Field Details**: Every field with correct type, default, optionality
- **Clear Layering**: Technical architecture clearly communicated
- **Business Context**: Function tags help developers find relevant models
- **Developer-Friendly**: Serves both reference and learning needs
- **Cross-Referenced**: Integrated with broader documentation ecosystem

## Validation Checklist
- [ ] All @dataclass models from models.py included
- [ ] Field listings match source exactly
- [ ] Layer categorization is logical and complete
- [ ] Business function tags are helpful and accurate
- [ ] Cross-references work and add value
- [ ] Code examples are syntactically correct
- [ ] Documentation serves both quick reference and deep study
- [ ] Integration with existing docs is seamless

---
*Methodology for reusable, systematic documentation updates*
