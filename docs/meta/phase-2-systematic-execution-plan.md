# Phase 2 Systematic Execution Plan: Model Categorization with Evidence

**Created**: September 17, 2025
**Purpose**: Reliable method for categorizing models with verifiable evidence for all claims

## Problem Analysis

**Previous Failure Pattern**: Made assumptions based on model names rather than reading actual source code
**Root Cause**: Pattern-matching instead of evidence-based categorization
**Solution**: Systematic source reading with documented evidence for every classification decision

## Evidence-Based Categorization Method

### Step 1: Extract Model Documentation (20 minutes)
**For each of the 38 models, systematically extract:**

1. **Read model definition starting from @dataclass line**
2. **Extract exact docstring** (the triple-quoted string immediately after class definition)
3. **Document first 5-10 fields** to understand data concerns vs business logic
4. **Note any imports** that suggest infrastructure dependencies
5. **Record any methods** that suggest behavior vs pure data

**Evidence Template for Each Model**:
```markdown
### ModelName
**Source Line**: [line number in models.py]
**Docstring**: "[exact docstring]"
**First 5 Fields**: [list actual field names and types]
**Methods Present**: [yes/no and list if yes]
**Infrastructure Imports**: [database, external service references]
**Initial Assessment**: [one sentence based on evidence]
```

**Quality Check**: Can I point to specific code lines and quotes for every assessment?

### Step 2: Architectural Layer Assignment (15 minutes)
**Using extracted evidence, assign to layers based on specific criteria:**

#### Pure Domain Models
**Criteria** (all must be true):
- Docstring describes business concept/rule
- No database/infrastructure field types
- Contains business logic methods OR business state fields
- No external system references

**Evidence Required**: Quote docstring + cite business-focused fields

#### Supporting Domain Models
**Criteria** (business concept + data structure needs):
- Docstring describes business concept
- But has structural/data-heavy fields (coordinates, embeddings, etc.)
- Mix of business logic and data structure concerns

**Evidence Required**: Quote docstring + cite structural fields

#### Integration & Transfer Models
**Criteria**:
- Docstring mentions "external", "integration", "contract", "DTO"
- Fields focused on external system communication
- Little/no business logic, mostly data transfer

**Evidence Required**: Quote docstring + cite external system fields

#### Infrastructure Models
**Criteria**:
- Docstring mentions "system", "mechanism", "infrastructure"
- Fields for system operations (events, conversations, etc.)
- Support application functionality, not business concepts

**Evidence Required**: Quote docstring + cite system operation fields

### Step 3: Business Function Tagging (10 minutes)
**Based on documented evidence, assign business function tags:**

**Tag Assignment Criteria**:
- `#pm`: Docstring/fields mention products, features, stakeholders, work items
- `#workflow`: Docstring/fields mention processes, tasks, orchestration
- `#knowledge`: Docstring/fields mention documents, analysis, learning, graphs
- `#spatial`: Docstring/fields mention territories, rooms, positions
- `#ai`: Docstring/fields mention enhancement, intelligence, insights
- `#ethics`: Docstring/fields mention decisions, boundaries, safety
- `#system`: Docstring/fields mention infrastructure, events, conversations

**Evidence Required**: Quote specific docstring phrases or field names that support each tag

### Step 4: Create Verification Report (10 minutes)
**For each model, create evidence summary**:

```markdown
## ModelName Classification Report
**Layer**: [Pure Domain/Supporting Domain/Integration/Infrastructure]
**Evidence**: "Docstring says '[quote]' and fields include [specific examples]"
**Business Tags**: #tag1 #tag2
**Tag Evidence**: "Fields [x, y, z] indicate [business function]"
**Confidence**: High/Medium/Low based on clarity of evidence
```

### Step 5: Quality Assurance (5 minutes)
**Review classifications for**:
- **Consistency**: Similar evidence → similar classification
- **Completeness**: Every model has documented evidence
- **Accuracy**: Can defend each classification with specific quotes
- **No Assumptions**: Every claim backed by actual source code

## Validation Protocol

### Before Declaring Phase 2 Complete
- [ ] All 38 models have evidence templates filled out
- [ ] Can quote specific docstring for every layer assignment
- [ ] Can cite specific fields for every business tag
- [ ] No classification based on model name alone
- [ ] Spot-check 5 random models by re-reading source
- [ ] All evidence is verifiable by independent reviewer

### Red Flags to Reject Work
- Any classification without quoted evidence
- Using model name as primary categorization reason
- Vague evidence like "seems like" or "probably"
- Unable to cite specific source lines
- Inconsistent criteria application

## Deliverable Format

```markdown
# Phase 2 Results: Evidence-Based Model Categorization

## Pure Domain Models (X models)
### ModelName
**Evidence**: "Docstring: '[exact quote]'. Business fields: [field1, field2]"
**Business Tags**: #tag1 #tag2 (Fields: [field_supporting_tag])

## Supporting Domain Models (X models)
[Same format with evidence]

## Integration & Transfer Models (X models)
[Same format with evidence]

## Infrastructure Models (X models)
[Same format with evidence]

## Verification Summary
- Total models processed: 38
- Evidence documented: 38/38
- Verifiable classifications: 38/38
- Assumptions made: 0
```

## Success Criteria
1. **100% Evidence-Based**: Every classification supported by quoted source
2. **Independently Verifiable**: Another person could validate each decision
3. **Consistent Criteria**: Same evidence leads to same classifications
4. **No Assumptions**: All claims traced to actual code
5. **Systematic Coverage**: All 38 models processed with same rigor

---

**Next Step**: Await approval of this systematic approach before execution
