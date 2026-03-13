# Claude Code Prompt: MUX-399-P0 Investigation & Pattern Discovery

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- BRIEFING-CURRENT-STATE.md - Current epic and focus
- BRIEFING-ESSENTIAL-AGENT.md - Your role requirements

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

**DO NOT**:
- ❌ Read old context files to self-direct
- ❌ Assume you should continue
- ❌ Start working on next task without authorization

**This is critical**. After compaction, get your bearings first.

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete a GitHub Issue. Your work is part of a multi-agent coordination chain.

### Your Acceptance Criteria Format
When you receive acceptance criteria, they will look like:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]

**Every checkbox must be addressed in your handoff.**

### Evidence You MUST Provide
1. **Analysis documents**: Complete path to each deliverable
2. **File verification**: `ls -la` showing documents exist
3. **Evidence references**: Specific file paths and line numbers for all claims
4. **How to verify**: Where to find evidence for each finding

### Your Handoff Format
Return your work with this structure:
```
## Issue #XXX Completion Report
**Status**: Complete/Partial/Blocked

**Deliverables**:
- Morning Standup Analysis: [path] - [X pages]
- Spatial Infrastructure Audit: [path] - [X pages]
- B1 FTUX Grammar Mapping: [path] - [X pages]
- ADR Connection Map: [path] - [X pages]

**Key Findings**:
[Summary of most important discoveries]

**P1 Implications**:
[Any scope changes or concerns for P1]

**Evidence**:
[File listings, code references]

**Blockers** (if any):
- [Blocker description and why it prevents completion]
```

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Gameplan Assumptions FIRST
**Before doing ANYTHING else, verify these locations exist**:

```bash
# Morning Standup code
ls -la services/conversation/
find services/ -name "*standup*" -type f

# Spatial infrastructure
ls -la services/intelligence/spatial/
ls -la services/integrations/spatial/
ls -la services/integrations/slack/spatial_*.py

# B1 FTUX specs
ls -la docs/internal/design/specs/

# ADRs
ls -la docs/internal/architecture/current/adrs/
ls docs/internal/architecture/current/adrs/ | grep -E "038|045|050"
```

**If any location doesn't exist**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised instructions**

---

## Mission
Complete the investigation and pattern discovery for MUX-399-P0, producing 4 analysis documents that enable informed implementation in P1.

**Scope Boundaries**:
- This prompt covers: Investigation and documentation ONLY
- NOT in scope: Any code changes, implementations, or modifications
- Deliverables: 4 markdown analysis documents + experience checkpoint

---

## Context
- **GitHub Issue**: #[TBD] MUX-399-P0: Investigation & Pattern Discovery
- **Parent Epic**: #399 MUX-VISION-OBJECT-MODEL
- **Current State**: ADR-045 accepted, spatial dimensions exist as methods, lens infrastructure doesn't exist yet
- **Target State**: 4 analysis documents complete, P1 can proceed with informed implementation
- **Dependencies**: None - this is the starting point
- **User Data Risk**: None - investigation only, no changes

---

## Phase 0: Mandatory Verification

```bash
# 1. Verify GitHub issue exists (when created)
gh issue view [ISSUE-NUMBER]

# 2. Verify key locations
ls -la services/conversation/
ls -la services/intelligence/spatial/
ls -la docs/internal/design/specs/
ls -la docs/internal/architecture/current/adrs/

# 3. Check for Morning Standup specifically
grep -r "standup" services/ --include="*.py" -l | head -20

# 4. Verify ADRs exist
cat docs/internal/architecture/current/adrs/adr-045-object-model.md | head -50
```

**STOP if**:
- Issue doesn't exist or isn't assigned
- Expected directories don't exist
- ADR-045 cannot be found

---

## Implementation Approach

### Step 1: Morning Standup Analysis (Phase 1)

**Objective**: Extract consciousness patterns from the reference implementation.

**Actions**:
1. Find all standup-related code:
   ```bash
   find services/ -name "*standup*" -type f
   grep -r "standup" services/ --include="*.py" -l
   ```

2. Read each file completely, noting:
   - How does it embody "Entities experience Moments in Places"?
   - What language sounds conscious vs mechanical?
   - What patterns should be replicated elsewhere?

3. Create analysis document:
   ```bash
   # Create: dev/2026/01/19/p0-morning-standup-analysis.md
   ```

**Deliverable Content**:
```markdown
# Morning Standup Pattern Analysis

## Grammar Embodiment
[How standup implements "Entities experience Moments in Places"]

## Consciousness Patterns Identified
1. [Pattern 1 with code example]
2. [Pattern 2 with code example]
...

## Extractable Patterns for Reuse
[Patterns that should be used in other features]

## Evidence
[File paths and line numbers for all claims]
```

**Evidence Required**:
- Specific code snippets with file:line references
- Quoted examples of consciousness language
- At least 3 extractable patterns identified

---

### Step 2: Spatial Infrastructure Audit (Phase 2)

**Objective**: Document what actually exists vs what was assumed.

**Actions**:
1. Audit Notion pattern:
   ```bash
   cat services/intelligence/spatial/notion_spatial.py
   # Note the dimensions dict pattern
   ```

2. Audit per-integration pattern:
   ```bash
   ls -la services/integrations/spatial/
   # Document each adapter
   ```

3. Audit Slack granular pattern:
   ```bash
   ls -la services/integrations/slack/spatial_*.py
   ```

4. Create audit document:
   ```bash
   # Create: dev/2026/01/19/p0-spatial-infrastructure-audit.md
   ```

**Deliverable Content**:
```markdown
# Spatial Infrastructure Audit

## Actual Implementation Pattern
[Document how 8D dimensions are implemented as methods]

## Integration-by-Integration Audit

### Notion
- Location: [path]
- Pattern: dimensions dict with 8 methods
- Methods: [list all 8]

### Calendar
- Location: [path]
- Pattern: [what exists]
- Methods: [list]

### GitHub
- Location: [path]
- Pattern: [what exists]
- Methods: [list]

### Slack
- Location: [path]
- Pattern: granular files
- Files: [list spatial_*.py files]

## Dimension Implementation Table
| Integration | TEMPORAL | HIERARCHY | PRIORITY | COLLABORATIVE | FLOW | QUANTITATIVE | CAUSAL | CONTEXTUAL |
|-------------|----------|-----------|----------|---------------|------|--------------|--------|------------|
| Notion      | ✅ method | ✅ method | ... | ... | ... | ... | ... | ... |
| Calendar    | ? | ? | ? | ? | ? | ? | ? | ? |
| GitHub      | ? | ? | ? | ? | ? | ? | ? | ? |
| Slack       | ✅ file | ✅ file | ... | ... | ... | ... | ... | ... |

## Gap Analysis
### What 8d-spatial-to-lens-mapping.md Assumed
[Document assumptions]

### What Actually Exists
[Document reality]

### Implication for P1
[What P1 needs to create vs wrap]
```

**Evidence Required**:
- Actual file paths verified with `ls -la`
- Code snippets showing dimension implementations
- Clear gap analysis with specific differences

---

### Step 3: B1 FTUX Spec Review (Phase 3)

**Objective**: Document implicit Entity/Moment/Place thinking in specs.

**Actions**:
1. Read empty state voice guide:
   ```bash
   cat docs/internal/design/specs/empty-state-voice-guide-v1.md
   ```

2. Find and read cross-session greeting specs:
   ```bash
   find docs/internal/design/specs/ -name "*greeting*" -o -name "*cross-session*"
   ```

3. Read contextual hint spec:
   ```bash
   cat docs/internal/design/specs/contextual-hint-ux-spec-v1.md
   ```

4. Create mapping document:
   ```bash
   # Create: dev/2026/01/19/p0-b1-ftux-grammar-mapping.md
   ```

**Deliverable Content**:
```markdown
# B1 FTUX Implicit Grammar Mapping

## Methodology
[How we identified implicit grammar usage]

## Spec-by-Spec Analysis

### Empty State Voice Guide
**Entity Concepts**: [how spec treats Piper as an entity]
**Moment Concepts**: [how spec frames occurrences]
**Place Concepts**: [how spec describes contexts]
**Key Quotes**: [quoted text showing implicit grammar]

### Cross-Session Greeting
**Entity Concepts**: [...]
**Moment Concepts**: [...]
**Place Concepts**: [...]
**Key Quotes**: [...]

### Contextual Hints
**Entity Concepts**: [...]
**Moment Concepts**: [...]
**Place Concepts**: [...]
**Key Quotes**: [...]

## Grammar Mapping Table
| Spec | Entity Examples | Moment Examples | Place Examples | Situation Examples |
|------|-----------------|-----------------|----------------|-------------------|
| Empty State | "Piper's voice..." | "first time..." | "empty workspace" | "onboarding moment" |
| Cross-Session | [...] | [...] | [...] | [...] |
| Contextual Hints | [...] | [...] | [...] | [...] |

## Observations
[What this reveals about implicit grammar usage in design]
```

**Evidence Required**:
- Quoted text from specs with page/section references
- Clear mapping to grammar concepts
- At least 2 examples per spec

---

### Step 4: ADR Connection Mapping (Phase 4)

**Objective**: Understand how existing ADRs connect to object model.

**Actions**:
1. Read ADR-038 (Spatial Intelligence):
   ```bash
   cat docs/internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md
   ```

2. Read ADR-045 (Object Model):
   ```bash
   cat docs/internal/architecture/current/adrs/adr-045-object-model.md
   ```

3. Read ADR-050 (Conversation-as-Graph):
   ```bash
   cat docs/internal/architecture/current/adrs/adr-050-conversation-as-graph.md
   ```

4. Create connection map:
   ```bash
   # Create: dev/2026/01/19/p0-adr-connection-map.md
   ```

**Deliverable Content**:
```markdown
# ADR Connection Map

## ADR Summaries

### ADR-038: Spatial Intelligence Patterns
**Status**: [Accepted/Proposed]
**Key Points**:
- [Point 1]
- [Point 2]
**Relation to Object Model**: [how it connects]

### ADR-045: Object Model
**Status**: Accepted (Nov 28, 2025)
**Key Points**:
- [Point 1]
- [Point 2]
**What's Already Decided**: [list]
**What Remains for ADR-055**: [list gaps]

### ADR-050: Conversation-as-Graph
**Status**: [Accepted/Proposed]
**Key Points**:
- [Point 1]
- [Point 2]
**Relation to Object Model**: [how it connects]

## Connection Map

```
┌─────────────────────────────────────────────────────────────┐
│                     ADR RELATIONSHIP MAP                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ADR-038 (Spatial)  ←──────→  ADR-045 (Object Model)      │
│        │                              │                     │
│        │ 8D Dimensions                │ Grammar            │
│        │ become Lenses                │ E/M/P/S            │
│        ↓                              ↓                     │
│   [Perception]                  [Substrate]                 │
│                                       │                     │
│                           ADR-050 (Graph) ──────────────→  │
│                                │                            │
│                                │ Journal structure          │
│                                │ Conversation as Moments    │
│                                ↓                            │
│                          [Metadata/Journal]                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Gaps for ADR-055
[What ADR-055 needs to address that isn't covered by existing ADRs]

## Potential Conflicts
[Any conflicts or tensions between ADRs]
```

**Evidence Required**:
- ADR status and key decisions summarized
- Clear relationship mapping
- Specific gaps identified for ADR-055

---

### Step 5: Experience Checkpoint & Completion (Phase Z)

**Objective**: Complete investigation and prepare handoff.

**Actions**:
1. Verify all 4 documents exist:
   ```bash
   ls -la dev/2026/01/19/p0-*.md
   ```

2. Write experience checkpoint (in session log):
   ```markdown
   ## Experience Checkpoint

   How this investigation honored "Entities experience Moments in Places":

   [One paragraph describing:
   - How we (as investigators) experienced this work
   - What moments of understanding emerged
   - What places in the codebase revealed the grammar]
   ```

3. Prepare P1 recommendations:
   - Confirm or revise P1 scope
   - Identify any STOP conditions for P1
   - Document decisions needed from PM

4. Update GitHub issue with completion status

---

## Success Criteria
- [ ] Morning Standup analysis complete with consciousness pattern extraction
- [ ] Spatial infrastructure audit complete with accurate file paths
- [ ] B1 FTUX specs reviewed and mapped to grammar
- [ ] ADR connections documented
- [ ] Experience checkpoint written
- [ ] All file paths verified to exist
- [ ] No speculation - only documented observations

---

## STOP Conditions
If ANY of these occur, STOP and escalate:
1. Morning Standup implementation significantly different than expected
2. Core assumptions from memos are fundamentally wrong
3. ADR-045 conflicts with implementation plans
4. Scope of P1 needs significant revision based on findings
5. Cannot find expected files/code

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Constraints & Requirements

1. **Investigation ONLY**: Do NOT modify any code
2. **Evidence Required**: Every claim needs file:line references
3. **No Speculation**: Only documented observations
4. **Preserve Original**: Do not edit existing files, only create new analysis documents
5. **Session Log Management**:
   ```bash
   # Check first - do you already have a log today?
   ls -la dev/2026/01/19/*-inv-*-log.md
   ```
   - If none exists: Create `dev/2026/01/19/2026-01-19-HHMM-inv-code-log.md`
   - If exists: Append to existing log (don't create new one)

---

## Self-Check Before Claiming Complete

### Ask Yourself:
1. Do all 4 analysis documents exist?
2. Does each document have specific evidence (file paths, line numbers, quotes)?
3. Is there any speculation vs documented observation?
4. Have I verified all file paths I referenced?
5. Is the experience checkpoint written?
6. Are P1 recommendations documented?

### If Uncertain:
- Run verification commands
- Show actual output, not expected output
- Acknowledge what's unclear
- Ask for help if stuck

---

## Related Documentation
- Issue spec: `dev/2026/01/19/mux-399-p0-compliant.md`
- Gameplan: `dev/2026/01/19/gameplan-mux-399-p0.md`
- Parent epic: #399
- Memos: PPM guidance, Chief Architect guidance, CXO design principles
- Supporting: `dev/active/adr-055-object-model-draft.md`, `dev/active/8d-spatial-to-lens-mapping.md`

---

## REMINDER: Methodology Cascade
This prompt carries our methodology forward. You are responsible for:
1. Verifying infrastructure FIRST
2. Checking what exists NEXT
3. Providing evidence for EVERY claim
4. Stopping when assumptions are needed
5. Creating analysis documents in dev/2026/01/19/
6. Updating GitHub with progress

**This is investigation-only work. NO CODE CHANGES.**

---

*Prompt Version: 1.0*
*Template Version: 10.2*
*Created: 2026-01-19*
