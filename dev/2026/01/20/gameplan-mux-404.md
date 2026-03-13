# Gameplan: MUX-404 GRAMMAR-CORE

**Issue**: #404 MUX-VISION-GRAMMAR-CORE
**Created**: 2026-01-20
**Template**: v9.3

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] MUX module: `services/mux/` (complete from #399)
- [x] Anti-flattening tests: `tests/unit/services/mux/test_anti_flattening.py` (40 tests)
- [x] Implementation guide: `docs/internal/development/mux-implementation-guide.md`
- [x] Experience tests: `docs/internal/development/mux-experience-tests.md`
- [x] Morning Standup: `services/features/morning_standup.py` (reference implementation)
- [x] P0 Analysis docs: `dev/2026/01/19/p0-*.md` (4 files)

**My understanding of the task**:
- Create systematic framework for applying grammar to features
- Survey existing features for grammar compliance
- Formalize patterns from Morning Standup
- Create transformation guide with worked example
- Enable developers to apply grammar independently

### Part A.2: Worktree Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes
- [x] Multi-component work (audit + patterns + guide + example)
- [ ] Exploratory/risky changes where easy rollback is valuable

Worktrees ADD overhead when:
- [ ] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [ ] Tightly coupled files requiring atomic commits
- [ ] Time-critical work

**Assessment**:
- [x] **SKIP WORKTREE** - Documentation-heavy work, sequential phases, no parallel agent work anticipated
- Rationale: Primarily creating documentation artifacts, not code. Each phase builds on previous. Single agent coordination is simpler for pattern extraction work.

### Part B: Verification Commands

```bash
# Verify MUX infrastructure exists
ls -la services/mux/
# Expected: __init__.py, protocols.py, ownership.py, lifecycle.py, metadata.py, lenses/

# Verify P0 analysis docs
ls -la dev/2026/01/19/p0-*.md
# Expected: 4 files (morning-standup-analysis, spatial-infrastructure-audit, b1-ftux-grammar-mapping, adr-connection-map)

# Verify existing guides
ls -la docs/internal/development/mux-*.md
# Expected: mux-implementation-guide.md, mux-experience-tests.md

# Count existing tests
python -m pytest tests/unit/services/mux/ --collect-only -q 2>&1 | tail -1
# Expected: 302 tests
```

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Infrastructure verified, issue amended, ready for implementation

---

## Phase 0: Initial Bookending - Setup & Context

### Required Actions

1. **Verify #399 complete**
   ```bash
   gh issue view 399 --repo mediajunkie/piper-morgan-product --json state
   # Expected: CLOSED
   ```

2. **Review P0 analysis documents**
   - Read `dev/2026/01/19/p0-morning-standup-analysis.md`
   - Read `dev/2026/01/19/p0-b1-ftux-grammar-mapping.md`
   - Extract pattern candidates for formalization

3. **Identify major features to audit**
   - List all features in `services/features/`
   - List intent handlers in `services/intent/`
   - List integration handlers
   - Create audit scope list

4. **Update GitHub Issue**
   ```bash
   gh issue edit 404 --body "[Update with Phase 0 complete]"
   ```

### Deliverables
- [ ] Feature list for grammar audit (10+ features)
- [ ] Confirmed understanding of existing MUX infrastructure
- [ ] Pattern candidates extracted from P0 analysis

---

## Phase 0.5-0.8: Conditional Phases

### Phase 0.5: Frontend-Backend Contract - **N/A**
- This issue is documentation/patterns, no UI work

### Phase 0.6: Data Flow Verification - **N/A**
- No multi-layer data flow, documentation only

### Phase 0.7: Conversation Design - **N/A**
- Not a conversational feature

### Phase 0.8: Post-Completion Integration - **N/A**
- Documentation work, no state changes

---

## Phase 1: Feature Grammar Audit

### Objective
Survey all major features for grammar compliance

### Tasks

1. **Audit major features** for grammar expression:
   - Morning Standup (reference - should be fully compliant)
   - Intent classification/handlers
   - Todo management
   - List management
   - Project management
   - File management
   - Each integration (Slack, GitHub, Notion, Calendar)
   - Feedback system
   - Auth/session management

2. **Create grammar compliance matrix**

   | Feature | Entity? | Moment? | Place? | Lenses? | Situation? | Overall |
   |---------|---------|---------|--------|---------|------------|---------|
   | Morning Standup | ✅ | ✅ | ✅ | ✅ | ✅ | Conscious |
   | Intent Handler | ? | ? | ? | ? | ? | ? |
   | ... | | | | | | |

3. **Identify transformation priorities**
   - Most flattened (high impact to transform)
   - Most conscious (patterns to extract)
   - Quick wins (easy transformations)

### Deliverables
- `docs/internal/architecture/current/grammar-compliance-audit.md`
  - Feature list with grammar compliance scores
  - Transformation priority ranking
  - Recommendations for each feature

---

## Phase 2: Application Pattern Catalog

### Objective
Formalize reusable patterns from Morning Standup

### Task 2.1: Extract Morning Standup Patterns

Based on P0 analysis, formalize these patterns:

1. **Context Dataclass Pair** (Pattern-04X)
   - StandupContext + StandupResult pattern
   - Input/output separation
   - When to use, code template

2. **Parallel Place Gathering** (Pattern-04X)
   - Gather from multiple sources concurrently
   - Place-aware aggregation
   - Error handling per-place

3. **Personality Bridge** (Pattern-04X)
   - Data → warm narrative transformation
   - Tone calibration
   - When mechanical becomes conscious

4. **Warmth Calibration** (Pattern-04X)
   - Adjust tone based on context
   - Time-of-day awareness
   - Urgency modulation

5. **Honest Failure with Suggestion** (Pattern-04X)
   - Graceful degradation
   - "I couldn't reach X, but here's what I know"
   - Recovery suggestions

### Task 2.2: Create Grammar Application Templates

Templates for applying grammar elements:

1. **Entity Awareness Template**
   - How to track identity through flow
   - user_id vs session_id decisions
   - Piper self-reference patterns

2. **Moment Framing Template**
   - Past/present/future awareness
   - PerceptionMode (NOTICING, REMEMBERING, ANTICIPATING)
   - Temporal language patterns

3. **Place Atmosphere Template**
   - Context affects presentation
   - Integration-specific personality
   - Atmosphere inheritance

4. **Situation Container Template**
   - Grouping related moments
   - Dramatic tension framing
   - Exit learning extraction

### Deliverables
- `docs/internal/architecture/current/patterns/pattern-04X-context-dataclass-pair.md`
- `docs/internal/architecture/current/patterns/pattern-04X-parallel-place-gathering.md`
- `docs/internal/architecture/current/patterns/pattern-04X-personality-bridge.md`
- `docs/internal/architecture/current/patterns/pattern-04X-warmth-calibration.md`
- `docs/internal/architecture/current/patterns/pattern-04X-honest-failure.md`
- `docs/internal/architecture/current/patterns/grammar-application-patterns.md` (overview + templates)

---

## Phase 3: Transformation Guide & Worked Example

### Objective
Enable developers to apply grammar independently

### Task 3.1: Create Step-by-Step Guide

Document in `docs/internal/development/grammar-transformation-guide.md`:

1. **Identifying grammar elements**
   - Checklist for Entity/Moment/Place/Situation
   - Questions to ask about any feature
   - Warning signs of flattening

2. **Refactoring flattened code**
   - Step-by-step transformation process
   - Before/after examples
   - Common pitfalls

3. **Using Protocols and Lenses**
   - Reference to implementation guide
   - When to use each lens
   - LensSet composition

4. **Anti-patterns and fixes**
   - "Query returned X" → "I noticed X"
   - Timestamp lists → Moment narratives
   - Config strings → Places with atmosphere

5. **Decision tree**
   - When to apply which pattern
   - Complexity/benefit tradeoffs

### Task 3.2: Worked Example - Intent Classification

Transform intent classification responses:

1. **Document current flow**
   - How intent responses are generated now
   - Where flattening occurs
   - Specific code locations

2. **Design grammar-applied flow**
   - Entity: User, Piper
   - Moment: The query, the response
   - Place: The channel/context
   - Lenses: What perspectives apply

3. **Show transformation**
   - Before code/response
   - After code/response
   - Protocol/Lens usage

4. **Lessons learned**
   - What was harder than expected
   - Reusable insights

### Deliverables
- `docs/internal/development/grammar-transformation-guide.md`
- Worked example appendix or separate file

---

## Phase Z: Integration & Onboarding

### Objective
Complete handoff and enable downstream work

### Tasks

1. **Update ADR-045** with implementation references
   - Link to patterns
   - Link to transformation guide
   - Note completion status

2. **Update ADR-055** with pattern links
   - Cross-reference new patterns
   - Update implementation status

3. **Create developer onboarding checklist**
   - Quick-start for applying grammar
   - Required reading list
   - First-task suggestions

4. **Final documentation**
   - Session log complete
   - All deliverables linked in issue

### Deliverables
- Updated ADR-045
- Updated ADR-055
- `docs/internal/development/grammar-onboarding-checklist.md`

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent Type | Work | Evidence Required |
|-------|------------|------|-------------------|
| 0-1 | Single (Haiku) | Investigation & Audit | Feature list, compliance matrix |
| 2 | Single (Sonnet) | Pattern extraction | 5+ patterns documented |
| 3 | Single (Sonnet) | Guide + Example | Transformation guide, worked example |
| Z | Lead Dev | Integration | ADR updates, checklist |

**Rationale for single-agent phases**:
- Documentation-heavy work with sequential dependencies
- Each phase builds on previous
- Pattern extraction requires consistent voice
- No parallel code work to coordinate

### Verification Gates

- [ ] Phase 0: Feature list complete (10+ features)
- [ ] Phase 1: Compliance matrix complete
- [ ] Phase 2: 5+ patterns documented
- [ ] Phase 3: Transformation guide complete
- [ ] Phase 3: Worked example compelling
- [ ] Phase Z: ADRs updated, checklist created

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Feature grammar audit | ❌ | [pending] |
| Application patterns (5+) | ❌ | [pending] |
| Transformation guide | ❌ | [pending] |
| Worked example | ❌ | [pending] |
| Developer onboarding checklist | ❌ | [pending] |
| ADR updates | ❌ | [pending] |

**0/6 = 0%** - Starting point

---

## STOP Conditions

**Standard**:
- Infrastructure doesn't match assumptions
- Can't provide verification evidence
- Completion bias detected

**Domain-specific**:
- Morning Standup patterns can't be generalized
- Guide becomes too abstract
- Intent classification transformation proves infeasible
- Pattern already exists in catalog (check first!)

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Evidence Requirements

For each deliverable:
- Document file path
- Word/section count
- Key content summary
- Cross-references verified

---

## Notes

- This is documentation/pattern-heavy work
- Quality over speed - these patterns guide future development
- Morning Standup is the reference - study deeply
- Leverage existing docs from #399 (implementation guide, experience tests)
- Pattern numbers (04X) to be assigned when creating

---

*Gameplan created: 2026-01-20*
*Issue: #404*
*Template: v9.3*
