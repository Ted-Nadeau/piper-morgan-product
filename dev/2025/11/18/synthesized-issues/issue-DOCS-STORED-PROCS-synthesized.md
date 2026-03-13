# DOCS-STORED-PROCS - Document Application-Layer Stored Procedures Pattern (ADR)

**Priority**: P2 (Documentation/Architecture)
**Labels**: `documentation`, `architecture`, `adr`
**Milestone**: MVP Documentation
**Epic**: Architecture Documentation
**Related**: Ted Nadeau follow-up questions (stored procedures), ADR template

---

## Problem Statement

### Current State
When asked "Are there stored procedures in use?" the answer is nuanced and not documented:
- ❌ **No**: SQL stored procedures (no `CREATE PROCEDURE` in PostgreSQL)
- ✅ **Yes**: Application-layer "stored procedures" (Python workflows, orchestration)

This architectural pattern should be explicitly documented in an ADR to clarify confusion for:
- **New developers**: "Where do multi-step processes live?"
- **Architecture reviews**: "How are complex workflows implemented?"
- **External advisors** (like Ted Nadeau): "Are there stored procedures?"

### Current Implementation (Undocumented)
**Application-layer procedures exist but not documented as a pattern**:

1. **Orchestration Engine** (`services/orchestration/engine.py`)
   - Multi-step workflow coordination
   - State management across steps
   - Error handling & rollback/compensation

2. **Workflow Factory** (`services/workflows/`)
   - Template-based workflow instantiation
   - Parameterized workflows for different domains
   - Reusable workflow patterns

3. **Skills System** (`services/skills/`)
   - MCP-integrated capabilities
   - Learnable procedures (Piper discovers new skills)
   - User-defined and system-defined skills

4. **Intent Handlers** (`services/intent/intent_service.py`)
   - ~25 intent handler methods mapping intents → actions
   - Multi-turn stateful conversation workflows
   - Business logic routing and execution

### Impact
- **Knowledge gaps**: Developers don't know architectural patterns exist
- **Code discovery burden**: Must grep codebase to understand design
- **Onboarding friction**: New team members can't find documentation
- **External credibility**: Architecture reviews lack documented decisions

---

## Goal

**Primary Objective**: Create comprehensive ADR documenting why Piper uses application-layer stored procedures instead of database-layer procedures, with implementation examples and decision rationale.

**Expected Outcome**:
```
When asked "Are there stored procedures in use?"
Answer: "Yes, application-layer procedures (documented in ADR-XXX).
No SQL stored procedures. Here's why..."
```

**Not In Scope** (explicitly):
- ❌ Implementing new procedures (document existing pattern)
- ❌ Refactoring existing code (documentation only)
- ❌ Adding database-layer procedures (explicitly not recommended)
- ❌ Performance optimization (deferred to future)

---

## What Already Exists

### Infrastructure ✅
- Orchestration Engine fully implemented
- Workflow Factory in use
- Skills system functional
- Intent handlers established
- ADR template available

### What's Missing ❌
- ADR documenting this architectural choice
- Code examples showing the pattern
- Trade-offs analysis (Python vs SQL)
- Decision rationale for reviewers
- Guidance on when to reconsider

---

## Requirements

### Phase 1: Research & Analysis
**Objective**: Understand current stored procedure implementations

**Tasks**:
- [ ] Audit `services/orchestration/` for procedure patterns
- [ ] Audit `services/workflows/` for template patterns
- [ ] Audit `services/skills/` for skill composition
- [ ] Audit `services/intent/intent_service.py` for intent handlers
- [ ] Verify: No SQL stored procedures exist (no PL/pgSQL in migrations)
- [ ] Document current examples

**Deliverables**:
- List of existing procedures with line numbers
- Code snippets for each pattern
- Evidence of no database procedures

### Phase 2: ADR Creation
**Objective**: Write ADR documenting application-layer procedure pattern

**Tasks**:
- [ ] Create `docs/internal/architecture/current/adrs/adr-XXX-application-layer-stored-procedures.md`
- [ ] **Status section**: Accepted
- [ ] **Context section**:
  - Why Piper needs procedures (multi-step workflows)
  - Traditional alternatives (database vs application)
  - Trade-offs overview
- [ ] **Decision section**:
  - Use application-layer procedures (Python)
  - Reserve database for data/constraints
  - Avoid SQL stored procedures unless performance-critical
- [ ] **Rationale section**:
  - Testing benefits (pytest > pgTAP)
  - Version control benefits (Git tracks Python)
  - Type safety (mypy validation)
  - AI comprehension (LLMs read Python)
  - Debugging advantages
- [ ] **Consequences section**:
  - Positive: Testing, versioning, AI-friendly
  - Negative: Network overhead, limited atomic transactions
  - Mitigations: Use DB transactions where needed, batch operations
- [ ] **When to Reconsider section**:
  - Performance thresholds (<10ms latency required)
  - Complex aggregations (better in SQL)
  - Sharding (cross-database transactions)
  - DBA preference (database-centric architecture)

**Deliverables**:
- ADR file in correct location
- Follows ADR template format
- All sections complete

### Phase 3: Code Examples
**Objective**: Provide concrete examples of application-layer procedures

**Tasks**:
- [ ] Example 1: Architecture Review Workflow (multi-step process)
  - Parse questions → Research → Draft → Create artifacts → Request approval
- [ ] Example 2: Pattern Learning Workflow (learnable procedure)
  - Detect pattern → Validate → Store → Link in knowledge graph
- [ ] Example 3: Intent Handler (stateful workflow)
  - Receive intent → Resolve context → Execute action → Respond
- [ ] Contrasting Example: What database procedure would look like (with explanation why we don't do this)

**Deliverables**:
- 3-4 real code examples
- Inline comments explaining each step
- Contrast with hypothetical database procedure

### Phase 4: Trade-Offs Analysis
**Objective**: Document decision trade-offs clearly

**Tasks**:
- [ ] Python vs PL/pgSQL comparison table
- [ ] Testability comparison (pytest vs pgTAP)
- [ ] Version control comparison (Git vs migrations)
- [ ] Performance implications (network overhead)
- [ ] AI comprehension comparison (LLMs vs SQL parsing)

**Deliverables**:
- Comparison matrix
- Clear trade-off documentation
- Guidance for future decisions

### Phase 5: Review & Documentation Integration
**Objective**: Get ADR approved and linked from documentation

**Tasks**:
- [ ] Submit to Chief Architect for review
- [ ] Address feedback/revisions
- [ ] Add to `docs/internal/architecture/current/adrs/README.md` index
- [ ] Add reference to onboarding documentation
- [ ] Add reference to architecture overview
- [ ] Cross-link from related ADRs

**Deliverables**:
- Approved ADR
- Documentation index updated
- Onboarding docs updated

---

## Acceptance Criteria

### ADR Content
- [ ] Status: Clearly marked as "Accepted"
- [ ] Context: Explains why application-layer procedures are needed
- [ ] Decision: Explicitly states application-layer choice
- [ ] Rationale: Documents why (testing, versioning, AI, etc.)
- [ ] Consequences: Lists positive and negative outcomes
- [ ] Examples: 3+ real code examples from codebase
- [ ] Trade-offs: Clear comparison of alternatives
- [ ] When to Reconsider: Decision thresholds defined
- [ ] References: Links to relevant code and issues

### Examples
- [ ] Orchestration Engine example included
- [ ] Workflow Factory example included
- [ ] Skills system example included
- [ ] Intent handler example included
- [ ] All examples from actual codebase (real files)
- [ ] Code includes inline comments

### Review
- [ ] Chief Architect reviews and approves
- [ ] No technical inaccuracies
- [ ] Decision rationale is compelling
- [ ] Trade-offs are honestly presented

### Integration
- [ ] ADR indexed in README.md
- [ ] Referenced from onboarding docs
- [ ] Cross-linked from architecture overview
- [ ] Answers Ted Nadeau's question clearly

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Research complete | ❌ | [code audit] |
| ADR drafted | ❌ | [ADR file] |
| Code examples added | ❌ | [ADR sections] |
| Trade-offs documented | ❌ | [ADR section] |
| Chief Architect review | ❌ | [approval] |
| Documentation indexed | ❌ | [README updated] |
| Onboarding updated | ❌ | [doc file] |

**Definition of COMPLETE**:
- ✅ ADR approved by Chief Architect
- ✅ All sections complete and accurate
- ✅ Code examples are real (from codebase)
- ✅ Answers Ted Nadeau's stored procedure question
- ✅ Documentation properly indexed and linked

---

## Testing Strategy

No code testing needed (documentation only). Verification:
- [ ] ADR markdown renders correctly
- [ ] All code examples compile/run (if executable)
- [ ] All file paths are accurate
- [ ] All cross-references are valid links
- [ ] No broken references

---

## Success Metrics

### Quantitative
- ADR word count: 1500-2500 words (comprehensive)
- Code examples: 4+ real examples
- Trade-off factors: 5+ documented
- Cross-references: 10+ to code/related docs

### Qualitative
- Chief Architect finds decision rationale compelling
- New developers can understand pattern from ADR
- Architects can reference when explaining to external reviewers
- Clearly answers Ted Nadeau's question

---

## STOP Conditions

**STOP immediately and escalate if**:
- Chief Architect disagrees with application-layer choice
  - (If DBA says SQL procedures needed, update decision)
- Code examples don't compile or don't match codebase
  - (Use actual running code, not pseudocode)
- Trade-offs analysis is incomplete or biased
  - (Must honestly present both sides)
- ADR contradicts existing architectural decisions
  - (Cross-check with other ADRs)

**When stopped**: Document concern, propose revised decision, wait for PM approval.

---

## Effort Estimate

**Overall Size**: Small (Documentation only)

**Breakdown**:
- Phase 1 (Research): 1 hour
- Phase 2 (ADR writing): 2 hours
- Phase 3 (Code examples): 1.5 hours
- Phase 4 (Trade-off analysis): 1 hour
- Phase 5 (Review & integration): 1 hour

**Total**: 6.5 hours (< 1 day)

**Complexity Notes**:
- Low risk - documentation only, no code changes
- Research is straightforward (existing code audit)
- ADR template available to follow
- Chief Architect can provide quick feedback

---

## Dependencies

### Required (Must be complete first)
- [ ] Orchestration Engine code exists (`services/orchestration/`)
- [ ] Workflow Factory code exists (`services/workflows/`)
- [ ] Skills system code exists (`services/skills/`)
- [ ] Intent handlers code exists (`services/intent/`)
- [ ] ADR template available

### Optional (Nice to have)
- [ ] Performance benchmarks (network overhead)
- [ ] Comparison with other architecture patterns

---

## Related Documentation

- **Ted Nadeau's Question**: "Are there stored procedures in use?" (Nov 19, 2025)
- **Reply**: `dev/2025/11/20/ted-nadeau-follow-up-reply.md`
- **Issue #331**: Original documentation request
- **Issue #332**: Duplicate documentation request
- **ADR Template**: `docs/internal/architecture/current/adrs/adr-000-template.md`
- **Architecture Overview**: `docs/internal/architecture/current/README.md`

---

## Evidence Section

[This section is filled in during/after implementation]

### Research Findings
```
Orchestration Engine: services/orchestration/engine.py (456 lines)
  - execute_workflow() method: Application-layer procedure pattern

Workflow Factory: services/workflows/ (12 files)
  - WorkflowTemplate class: Parameterized procedures

Skills System: services/skills/ (8 files)
  - Skill composition: Learnable procedures

Intent Handlers: services/intent/intent_service.py (600+ lines)
  - 25 handler methods: Intent-triggered workflows

Database: alembic/versions/
  - Verified: No CREATE PROCEDURE in migrations
  - Verified: No PL/pgSQL code
```

### Code Examples (from actual codebase)
```python
# Example 1: services/orchestration/engine.py - Multi-step workflow
# Example 2: services/workflows/*.py - Workflow templates
# Example 3: services/skills/*.py - Skill composition
# Example 4: services/intent/intent_service.py - Intent handlers
```

---

## Completion Checklist

Before requesting PM review:
- [ ] ADR follows template structure ✅
- [ ] All sections complete ✅
- [ ] Code examples are from real codebase ✅
- [ ] Trade-offs honestly presented ✅
- [ ] Chief Architect has reviewed ✅
- [ ] Documentation index updated ✅
- [ ] Onboarding docs reference ADR ✅
- [ ] Answers Ted Nadeau's question ✅

**Status**: Not Started

---

## Notes for Implementation

**From Pair Issues #331 and #332**:
- Both issues requested same thing (stored procedures documentation)
- Synthesized into single ADR creation task
- Focus on application-layer pattern (not database procedures)
- Include real code examples from existing services

**For Chief Architect Review**:
- This documents an existing architectural choice
- Not proposing new direction, just formalizing existing practice
- Should take <1 hour for architect to review and approve

**Ted Nadeau Context**:
- His question about stored procedures prompted this documentation
- ADR will become our answer to future similar questions
- Demonstrates engineering maturity through documented decisions

---

**Remember**:
- Documentation quality matters as much as code quality
- Examples must be real (from actual codebase)
- Trade-offs should be honest (not one-sided)
- Future developers will use this ADR to understand architecture

---

_Issue created: November 20, 2025_
_Last updated: November 20, 2025_
_Synthesized from: #331 + #332_
