# Gameplan: MUX-399-P4.5 Canonical Query Lens/Substrate Tagging

**GitHub Issue**: #617
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Dependencies**: #613 (P1 - Complete), #614 (P2 - Complete), #615 (P3 - Complete), #616 (P4 - Complete)
**Estimated Effort**: ~3 hours
**Template Version**: v9.3

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Canonical query test matrix exists (`docs/internal/testing/canonical-query-test-matrix-v2.md`)
- [x] 63 queries documented across 14 categories
- [x] P1 Lens infrastructure complete (8 lenses in `services/mux/protocols.py`)
- [x] P1 Substrate protocols complete (Entity, Moment, Place)
- [x] ADR-045 grammar definition exists

**My understanding of the task**:
- Map all 63 canonical queries to lenses and substrates
- Validate that the grammar can express existing functionality
- Calculate coverage percentage (80% = PPM Tier 2 success)
- Document gaps and provide recommendations
- Update ADR-055 with appendix containing full mapping table

**Critical distinction**: This is ANALYSIS/DOCUMENTATION, not implementation.

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel (single agent)
- [ ] Task duration >30 minutes (3 hours, but analytical)
- [ ] Multi-component work (documentation only)
- [ ] Exploratory/risky changes (no code changes)

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits
- [x] No code changes - only documentation

**Assessment:**
- [x] **SKIP WORKTREE** - Single agent, documentation-only task. No code changes, only ADR appendix and analysis docs.

### Part B: PM Verification Required

**Verification Commands (Agent will run):**
```bash
# Verify canonical query matrix exists
ls -la docs/internal/testing/canonical-query-test-matrix-v2.md

# Verify P1 lenses exist (count them)
grep -E "class.*Lens" services/mux/protocols.py | wc -l

# Verify substrates exist
grep -E "@runtime_checkable" services/mux/protocols.py | head -5

# Verify ADR-055 exists for appendix addition
ls -la docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md

# Count queries in matrix
grep -E "^\| [0-9]+ \|" docs/internal/testing/canonical-query-test-matrix-v2.md | wc -l
```

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Canonical query matrix verified (63 queries), P1 lenses verified (8), ADR-055 exists for appendix

---

## Phase 0: Initial Bookending - GitHub Investigation

**Skip**: Issue #617 already verified as open and ready for analysis.

### Phase 0.5-0.8: Conditional Phases

**Phase 0.5 (Frontend-Backend Contract)**: N/A - No UI work
**Phase 0.6 (Data Flow)**: N/A - Documentation only
**Phase 0.7 (Conversation Design)**: N/A - Analysis task
**Phase 0.8 (Post-Completion)**: N/A - No code changes

---

## Phase 1: Query Inventory

**Objective**: Compile complete list of canonical queries organized by category

**Tasks**:
- [ ] Read canonical query test matrix v2
- [ ] Extract all 63 query patterns
- [ ] Group by functional area (14 categories)
- [ ] Create structured inventory document

**Deliverables**:
- Query inventory organized by category
- Count verification: 63 queries total

**Verification Command**:
```bash
# Verify count matches matrix
grep -E "^\| [0-9]+ \|" docs/internal/testing/canonical-query-test-matrix-v2.md | wc -l
```

---

## Phase 2: Lens Mapping

**Objective**: Map each query to primary and secondary lenses

**The 8 Available Lenses (from P1)**:
1. **Temporal** - Time-based perception
2. **Hierarchy** - Structure/containment
3. **Priority** - Urgency/importance
4. **Collaborative** - People/teams
5. **Flow** - Progress/state
6. **Quantitative** - Metrics/counts
7. **Causal** - Cause/effect
8. **Contextual** - Background/setting

**Tasks**:
- [ ] For each of 63 queries, identify primary lens
- [ ] Identify secondary lenses where applicable
- [ ] Document rationale for each mapping
- [ ] Flag queries that don't map cleanly

**Expected Distribution**:
- Temporal: ~30% (time is central to PM work)
- Priority: ~20% (urgency/importance common)
- Flow: ~15% (progress tracking)
- Collaborative: ~15% (team coordination)
- Others: ~20% combined

**Deliverables**:
- Query-to-lens mapping table
- Rationale for ambiguous mappings
- Flagged gaps

---

## Phase 3: Substrate Mapping

**Objective**: Map each query to primary substrate and Place type

**The 4 Substrates (from P1)**:
1. **Entity** - Actors/agents
2. **Moment** - Bounded occurrences
3. **Place** - Contexts/locations
4. **Situation** - Frames combining multiple elements

**Place Types** (from integrations):
- Calendar (Google Calendar)
- GitHub
- Slack
- Notion
- Local (filesystem)

**Tasks**:
- [ ] For each of 63 queries, identify substrate
- [ ] Identify Place type where applicable
- [ ] Document rationale for each mapping
- [ ] Flag queries that don't map cleanly

**Deliverables**:
- Query-to-substrate mapping table
- Place type annotations
- Flagged gaps

---

## Phase 4: Coverage Analysis

**Objective**: Calculate and assess coverage metrics

**Coverage Categories**:
- **Clean**: Maps directly to grammar without forcing
- **Caveat**: Maps but requires explanation/judgment
- **Gap**: Doesn't map - requires grammar concept that doesn't exist

**Tasks**:
- [ ] Count total queries analyzed (target: 63)
- [ ] Count clean mappings
- [ ] Count caveat mappings
- [ ] Count gaps
- [ ] Calculate coverage percentage
- [ ] Assess against 80% threshold (PPM Tier 2 requirement)

**Success Threshold**: 80% (50/63 queries) = Clean or Caveat

**Deliverables**:
- Coverage statistics
- Threshold assessment
- List of gaps with rationale

---

## Phase 5: Gap Analysis & Recommendations

**Objective**: Analyze gaps and provide actionable recommendations

**Gap Categories**:
- Missing lens type?
- Missing substrate type?
- Grammar too restrictive?
- Query actually ambiguous?

**Tasks**:
- [ ] For each gap, analyze why grammar doesn't express it
- [ ] Categorize gaps by type
- [ ] Provide recommendations (document only, NOT implement)
- [ ] Identify patterns in gaps

**Deliverables**:
- Gap analysis document
- Recommendations (documented, not implemented)
- Patterns observed

---

## Phase 6: ADR-055 Appendix D

**Objective**: Create appendix with full mapping table

**Appendix Structure**:
```markdown
## Appendix D: Canonical Query Grammar Mapping (P4.5)

### Overview
P4.5 validates the lens/substrate grammar against 63 canonical queries.

### Coverage Summary
- Total Queries: 63
- Clean Mappings: X (Y%)
- Caveat Mappings: X (Y%)
- Gaps: X (Y%)
- Overall Coverage: Z% (threshold: 80%)

### Full Mapping Table
| # | Query | Primary Lens | Secondary Lens(es) | Substrate | Place Type | Coverage | Notes |
|---|-------|-------------|-------------------|-----------|------------|----------|-------|

### Gap Analysis
[gaps and recommendations]

### Lens Distribution
[pie chart data or table]

### Substrate Distribution
[distribution data]
```

**Tasks**:
- [ ] Create appendix section in ADR-055
- [ ] Include complete mapping table
- [ ] Include coverage statistics
- [ ] Include gap summary
- [ ] Include lens/substrate distribution

**Deliverables**:
- ADR-055 Appendix D complete

---

## Phase Z: Completion & Handoff

### Verification Commands
```bash
# Verify ADR-055 updated
grep -A 5 "Appendix D" docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md

# Count lines added to ADR
wc -l docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md

# Verify mapping table exists
grep -c "^\|" docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md
```

### Completion Matrix

| Deliverable | Target | Status |
|-------------|--------|--------|
| Query inventory (63 queries) | 1 | Pending |
| Lens mapping table | 1 | Pending |
| Substrate mapping table | 1 | Pending |
| Coverage analysis | 1 | Pending |
| Gap analysis | 1 | Pending |
| ADR-055 Appendix D | 1 | Pending |

**TOTAL: 0/6 = 0% (starting point)**
**Only claim complete when 6/6 = 100%**

### Handoff Format
```markdown
## P4.5 Complete - Evidence

**Analysis Results:**
- Total Queries Analyzed: 63
- Clean Mappings: X (Y%)
- Caveat Mappings: X (Y%)
- Gaps: X (Y%)
- **Overall Coverage: Z%** (threshold: 80%)

**ADR-055 Updated:**
- Appendix D added with full mapping table
- +N lines added

**Gap Categories:**
- [category]: X queries
- [category]: Y queries

**Recommendations:**
- [documented recommendations]

**TOTAL: 6/6 = 100%**
```

---

## Multi-Agent Coordination

### Agent Deployment Map

| Phase | Agent | Focus | Verification Gate |
|-------|-------|-------|-------------------|
| 1-6 | Analysis Agent | Full P4.5 analysis | 6/6 deliverables |

**Single Agent Justification**: This is analytical/documentation work that doesn't parallelize well. Sequential analysis of 63 queries is more coherent as single-agent work.

### Cross-Validation
- PM reviews mapping rationale
- No code tests needed (documentation only)

---

## STOP Conditions

**STOP immediately and escalate if**:
1. Coverage below 60% (grammar fundamentally broken)
2. Major feature areas completely unmapped (e.g., all GitHub queries are gaps)
3. Lens or substrate concepts appear fundamentally wrong
4. Analysis reveals P1 implementation needs revision
5. Significant scope creep into implementation territory

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Evidence Requirements

**For each phase, provide:**
- Count of queries analyzed
- Clear categorization (Clean/Caveat/Gap)
- Rationale for ambiguous mappings
- Coverage percentage calculation

**Final Evidence:**
- Complete mapping table (63 rows)
- Coverage statistics
- Gap analysis with recommendations
- ADR-055 appendix

---

## Related Documentation

- **P1**: `services/mux/protocols.py` - Lenses and Protocols
- **Canonical Queries**: `docs/internal/testing/canonical-query-test-matrix-v2.md`
- **ADR-045**: Object Model specification
- **ADR-055**: Implementation details (add Appendix D)
- **PPM Memo**: 80% coverage = Tier 2 success

---

_Gameplan created: 2026-01-19_
_Template version: v9.3_
