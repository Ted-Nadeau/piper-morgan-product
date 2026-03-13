# Gameplan: MUX-399-P0 Investigation & Pattern Discovery

**GitHub Issue**: #[TBD - to be created]
**Parent Epic**: #399 MUX-VISION-OBJECT-MODEL
**Type**: Investigation (no code changes)
**Estimated Effort**: Medium (5 hours)
**Created**: 2026-01-19

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (verified in previous investigation)
- [x] Spatial infrastructure: Methods within integration classes, NOT separate dimension classes
- [x] Morning Standup: `services/conversation/` with handlers
- [x] B1 FTUX specs: `docs/internal/design/specs/`
- [x] ADRs: `docs/internal/architecture/current/adrs/`

**My understanding of the task**:
- This is INVESTIGATION ONLY - no code changes
- We are extracting patterns from existing implementations
- Deliverables are analysis documents, not code
- This enables informed implementation in P1

**Infrastructure verified in earlier session**:
- ADR-045 exists and is ACCEPTED (Nov 28, 2025)
- ADR-055 is next available number
- Spatial dimensions implemented as methods in `services/intelligence/spatial/notion_spatial.py` (pattern: `self.dimensions = {...}`)
- Slack spatial uses granular `spatial_*.py` files

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work
- [ ] Exploratory/risky changes where easy rollback is valuable

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work

**Assessment:**
- [x] **SKIP WORKTREE** - Investigation phase produces documentation only, no code changes requiring branch isolation

### Part B: PM Verification Required

**PM, please confirm**:

1. **What actually exists** (verified earlier today):
   - Morning Standup: `services/conversation/` ✓
   - Spatial: `services/intelligence/spatial/`, `services/integrations/spatial/` ✓
   - B1 FTUX specs: `docs/internal/design/specs/` ✓
   - ADRs: `docs/internal/architecture/current/adrs/` ✓

2. **Actual task needed?**
   - [x] Investigation/research only
   - [ ] Create new feature
   - [ ] Fix broken functionality
   - [ ] Refactor existing code

3. **Critical context**:
   - Morning Standup is the PRIMARY source material
   - ADR-045 is the original object model (ACCEPTED)
   - ADR-055 will be the implementation spec (to be created in P1)

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding is correct, investigation can begin
- [ ] **REVISE** - Need different approach
- [ ] **CLARIFY** - Need more context

---

## Phase 0: GitHub Issue & Orientation

### Required Actions

1. **GitHub Issue Creation** (PM will do after gameplan approval)
   - Title: `MUX-399-P0: Investigation & Pattern Discovery`
   - Body: From `mux-399-p0-compliant.md`
   - Labels: `MUX`, `investigation`, `foundation`
   - Milestone: MUX-V1
   - Parent: #399

2. **Codebase Orientation**
   ```bash
   # Verify key locations exist
   ls -la services/conversation/
   ls -la services/intelligence/spatial/
   ls -la services/integrations/spatial/
   ls -la docs/internal/design/specs/
   ls -la docs/internal/architecture/current/adrs/
   ```

3. **Create Session Log**
   ```bash
   # Session log for investigation work
   # File: dev/2026/01/19/2026-01-19-HHMM-inv-code-log.md
   ```

---

## Phase 0.5, 0.6, 0.7, 0.8: NOT APPLICABLE

These phases are for implementation work:
- Phase 0.5 (Frontend-Backend Contract): No UI work
- Phase 0.6 (Data Flow): No data flow changes
- Phase 0.7 (Conversation Design): No conversation features
- Phase 0.8 (Post-Completion Integration): No system changes

**This is investigation-only work.**

---

## Phase 1: Morning Standup Analysis

### Objective
Extract consciousness patterns from the reference implementation.

### Required Actions

1. **Read Morning Standup Implementation Completely**
   ```bash
   # Find all standup-related code
   find services/ -name "*standup*" -type f
   grep -r "standup" services/ --include="*.py" -l
   ```

   Key files to analyze:
   - Standup conversation handler
   - Standup-related intent handlers
   - Calendar/GitHub integration for standup

2. **Document Grammar Embodiment**

   For each component, answer:
   - What Entities are involved?
   - What Moments are captured?
   - What Places are perceived?
   - How does Piper experience (not just process)?

3. **Identify Consciousness Patterns**

   Look for:
   - Language that sounds conscious ("I notice...", "I see...")
   - Time perception (present moment awareness)
   - Relationship awareness (knowing who is involved)
   - Context sensitivity (adapting to situation)

4. **Extract Replicable Patterns**

   Document patterns that should be used elsewhere:
   - How standup frames its observations
   - How it handles uncertainty
   - How it connects related items
   - How it respects user context

### Deliverables
- `dev/2026/01/19/p0-morning-standup-analysis.md` (1-2 pages)
- List of extractable consciousness patterns

### Evidence Required
- Specific code snippets showing grammar embodiment
- Quoted examples of consciousness language
- File paths and line numbers for reference

---

## Phase 2: Spatial Infrastructure Audit

### Objective
Document what actually exists vs what was assumed.

### Required Actions

1. **Audit Notion Pattern** (`services/intelligence/spatial/`)
   ```bash
   ls -la services/intelligence/spatial/
   cat services/intelligence/spatial/notion_spatial.py
   # Document the dimensions dict pattern
   # Note: 8D as methods, not classes
   ```

2. **Audit Per-Integration Pattern** (`services/integrations/spatial/`)
   ```bash
   ls -la services/integrations/spatial/
   # Document each adapter
   ```

3. **Audit Slack Granular Pattern** (`services/integrations/slack/spatial_*.py`)
   ```bash
   ls -la services/integrations/slack/spatial_*.py
   # Document the granular file approach
   ```

4. **Document 8D Dimension Implementations**

   For each integration, document:
   | Integration | Temporal | Hierarchy | Priority | Collaborative | Flow | Quantitative | Causal | Contextual |
   |-------------|----------|-----------|----------|---------------|------|--------------|--------|------------|
   | Notion      | method   | method    | method   | method        | method | method      | method | method     |
   | Calendar    | ?        | ?         | ?        | ?             | ?    | ?            | ?      | ?          |
   | GitHub      | ?        | ?         | ?        | ?             | ?    | ?            | ?      | ?          |
   | Slack       | file     | file      | file     | file          | file | file         | file   | file       |

5. **Gap Analysis**

   Compare:
   - What `8d-spatial-to-lens-mapping.md` assumed exists
   - What actually exists in the codebase
   - What P1 will need to create vs wrap

### Deliverables
- `dev/2026/01/19/p0-spatial-infrastructure-audit.md`
- Table showing actual dimension implementations per integration
- Gap analysis: assumed vs actual

### Evidence Required
- File listings with actual paths
- Code snippets showing dimension implementations
- Clear documentation of what doesn't exist

---

## Phase 3: B1 FTUX Spec Review

### Objective
Document how existing specs implicitly use Entity/Moment/Place thinking.

### Required Actions

1. **Review Empty State Voice Guide**
   ```bash
   cat docs/internal/design/specs/empty-state-voice-guide-v1.md
   ```

   Document:
   - How does it frame Piper's voice? (Entity awareness)
   - What moments does it anticipate? (Moment thinking)
   - How does it describe empty contexts? (Place atmosphere)

2. **Review Cross-Session Greeting Specs**
   ```bash
   find docs/internal/design/specs/ -name "*greeting*" -o -name "*cross-session*"
   cat [found files]
   ```

   Document:
   - How does it handle memory across sessions? (Temporal continuity)
   - How does it personalize? (Entity relationship)

3. **Review Contextual Hint UX Spec**
   ```bash
   cat docs/internal/design/specs/contextual-hint-ux-spec-v1.md
   ```

   Document:
   - How does it decide when to hint? (Situation awareness)
   - What contexts trigger hints? (Place awareness)

4. **Create Implicit Grammar Mapping Table**

   | Spec | Entity Concepts | Moment Concepts | Place Concepts | Situation Concepts |
   |------|-----------------|-----------------|----------------|-------------------|
   | Empty State | ? | ? | ? | ? |
   | Cross-Session | ? | ? | ? | ? |
   | Contextual Hints | ? | ? | ? | ? |

### Deliverables
- `dev/2026/01/19/p0-b1-ftux-grammar-mapping.md`
- Mapping table for each spec

### Evidence Required
- Quoted text from specs showing implicit grammar usage
- Clear mapping to Entity/Moment/Place/Situation concepts

---

## Phase 4: ADR Connection Mapping

### Objective
Understand how existing ADRs connect to the object model.

### Required Actions

1. **Review ADR-038** (Spatial Intelligence Patterns)
   ```bash
   cat docs/internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md
   ```

   Document:
   - What 3 patterns are documented?
   - How do they relate to 8D dimensions?
   - What's the connection to lenses?

2. **Review ADR-045** (Object Model - Original)
   ```bash
   cat docs/internal/architecture/current/adrs/adr-045-object-model.md
   ```

   Document:
   - What's already accepted?
   - What implementation guidance exists?
   - What gaps remain for ADR-055?

3. **Review ADR-050** (Conversation-as-Graph)
   ```bash
   cat docs/internal/architecture/current/adrs/adr-050-conversation-as-graph.md
   ```

   Document:
   - How does graph model relate to Moments?
   - How does it relate to Journal infrastructure?
   - What overlaps exist?

4. **Create Connection Map**

   ```
   ADR-038 (Spatial) ←→ ADR-045 (Object Model) ←→ ADR-050 (Graph)
         ↓                      ↓                      ↓
   [Lenses]              [Grammar]              [Journal]
   ```

### Deliverables
- `dev/2026/01/19/p0-adr-connection-map.md`
- Visual/textual map of ADR relationships
- Gaps identified for ADR-055

### Evidence Required
- ADR summaries with key points
- Clear relationship mapping
- Identified gaps/overlaps

---

## Phase Z: Completion & Handoff

### Required Actions

1. **Compile All Findings**
   - Verify all 4 analysis documents complete
   - Cross-reference findings for consistency
   - Identify any conflicts or surprises

2. **Write Experience Checkpoint**

   One paragraph explaining how this investigation honors "Entities experience Moments in Places":
   - How did we (as investigators) experience this work?
   - What moments of understanding emerged?
   - What places in the codebase revealed the grammar?

3. **Prepare P1 Recommendations**

   Based on findings:
   - Confirm or revise P1 scope
   - Identify any STOP conditions for P1
   - Document decisions needed from PM

4. **Update GitHub Issue**
   ```bash
   gh issue edit [ISSUE_NUMBER] --body "
   ## Status: Complete - Awaiting PM Review

   ### Deliverables
   - [x] Morning Standup Analysis: dev/2026/01/19/p0-morning-standup-analysis.md
   - [x] Spatial Infrastructure Audit: dev/2026/01/19/p0-spatial-infrastructure-audit.md
   - [x] B1 FTUX Grammar Mapping: dev/2026/01/19/p0-b1-ftux-grammar-mapping.md
   - [x] ADR Connection Map: dev/2026/01/19/p0-adr-connection-map.md
   - [x] Experience Checkpoint: [in session log]

   ### Key Findings
   [Summary of most important discoveries]

   ### P1 Implications
   [Any scope changes recommended]

   ### Ready for PM Review
   "
   ```

5. **Session Log Completion**
   - Update session log with all work done
   - Include evidence references
   - Note any discoveries that affect later phases

### Success Criteria
- [ ] Morning Standup analysis complete with consciousness pattern extraction
- [ ] Spatial infrastructure audit complete with accurate file paths
- [ ] B1 FTUX specs reviewed and mapped to grammar
- [ ] ADR connections documented
- [ ] Experience checkpoint written
- [ ] All file paths in audit verified to exist
- [ ] No speculation - only documented observations

### Evidence Required
- All 4 analysis documents exist
- Each document has specific code/text references
- No assumptions carried forward unverified

---

## STOP Conditions

**STOP immediately and escalate if**:
- Morning Standup implementation significantly different than expected
- Core assumptions from memos are fundamentally wrong
- ADR-045 conflicts with implementation plans
- Scope of P1 needs significant revision based on findings
- Cannot find expected files/code

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Multi-Agent Deployment

### Recommendation: Single Agent

**Rationale**:
- Investigation work is sequential (read, analyze, document)
- No parallel implementation paths
- Findings from each phase inform the next
- Low risk of merge conflicts (documentation only)

**Agent**: Claude Code (Lead Developer role)
- Broad investigation capabilities
- Pattern discovery across codebase
- Can deploy subagents for parallel file reading if beneficial

### Optional Subagent Deployment

If beneficial, subagents could parallelize:
- Phase 1 + Phase 2 (standup analysis + spatial audit)
- Phase 3 + Phase 4 (FTUX specs + ADR review)

But sequential is acceptable given the investigation nature.

---

## Acceptance Criteria

### Functionality
- [ ] Morning Standup analysis complete with consciousness pattern extraction
- [ ] Spatial infrastructure audit complete with accurate file paths
- [ ] B1 FTUX specs reviewed and mapped to grammar
- [ ] ADR connections documented

### Quality
- [ ] All findings verified against actual code (not assumptions)
- [ ] No speculation - only documented observations
- [ ] Clear distinction between "exists" and "was assumed to exist"

### Documentation
- [ ] Investigation findings in session log
- [ ] Separate analysis documents for each area
- [ ] Experience checkpoint written

---

## Completion Matrix

| Deliverable | Status | Evidence |
|-------------|--------|----------|
| Morning Standup analysis | ⬜ | |
| Spatial infrastructure audit | ⬜ | |
| B1 FTUX grammar mapping | ⬜ | |
| ADR connection map | ⬜ | |
| Experience checkpoint | ⬜ | |
| P1 recommendations | ⬜ | |

---

## Related Documentation

- Issue spec: `dev/2026/01/19/mux-399-p0-compliant.md`
- Parent epic: #399
- Memos: PPM guidance, Chief Architect guidance, CXO design principles
- Supporting: `dev/active/adr-055-object-model-draft.md`, `dev/active/8d-spatial-to-lens-mapping.md`

---

*Gameplan created: 2026-01-19*
*Template version: v9.3*
