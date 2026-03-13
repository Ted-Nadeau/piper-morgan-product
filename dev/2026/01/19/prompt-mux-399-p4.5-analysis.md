# Claude Code Agent Prompt: MUX-399-P4.5 Canonical Query Lens/Substrate Tagging

## Your Identity
You are Claude Code, a specialized analysis agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
The MUX module implements the Object Model Grammar: "Entities experience Moments in Places."
- **P1 Complete**: 101 tests - 8 Lenses (Temporal, Hierarchy, Priority, Collaborative, Flow, Quantitative, Causal, Contextual)
- **P1 Complete**: 3 Substrate Protocols (EntityProtocol, MomentProtocol, PlaceProtocol)
- **P4.5 (This Task)**: Validate grammar by mapping 63 canonical queries to lenses and substrates

**CRITICAL**: This is ANALYSIS/DOCUMENTATION work, NOT implementation. You will NOT write code.

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. **STOP** - Do not continue working
2. **REPORT** - Summarize what was just completed
3. **ASK** - "Should I proceed to next task?"
4. **WAIT** - For explicit instructions

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Verify Resources Exist
```bash
# 1. Verify canonical query matrix exists
ls -la docs/internal/testing/canonical-query-test-matrix-v2.md

# 2. Count queries in matrix
grep -E "^\| [0-9]+ \|" docs/internal/testing/canonical-query-test-matrix-v2.md | wc -l

# 3. Verify P1 lenses exist
grep -E "class.*Lens" services/mux/protocols.py

# 4. Verify ADR-055 exists
ls -la docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md
```

**Expected**: ~63 queries, 8 lenses, ADR-055 exists
**If queries not found**: STOP and report.

---

## Mission

Map all 63 canonical queries to the lens/substrate grammar to validate expressiveness.

**"If we can't express what we already do, we've over-complicated."**

**Success Threshold**: 80% coverage (50/63 queries) = PPM Tier 2 success

**Scope Boundaries**:
- This prompt covers: Query inventory, lens mapping, substrate mapping, coverage analysis, gap analysis, ADR appendix
- NOT in scope: Implementing new query handling, changing behavior, automated selection, code changes

---

## Context

- **GitHub Issue**: #617 MUX-399-P4.5: Canonical Query Lens/Substrate Tagging
- **Current State**: 63 canonical queries, 8 lenses, 3 substrates
- **Target State**: Full mapping table with coverage analysis
- **Dependencies**: P1 lens infrastructure
- **User Data Risk**: None - documentation only

---

## Evidence Requirements (CRITICAL)

### For EVERY Claim:
- **"Mapped X queries"** → Show count and sample mappings
- **"Coverage is Y%"** → Show calculation
- **"Found Z gaps"** → List specific queries that don't map

### Completion Matrix (Track Throughout)

| Deliverable | Target | Actual | Status |
|-------------|--------|--------|--------|
| Query inventory (63) | 1 | 0 | Pending |
| Lens mapping table | 1 | 0 | Pending |
| Substrate mapping table | 1 | 0 | Pending |
| Coverage analysis | 1 | 0 | Pending |
| Gap analysis | 1 | 0 | Pending |
| ADR-055 Appendix D | 1 | 0 | Pending |

**Only claim complete when 6/6 = 100%**

---

## The 8 Lenses (from P1)

Reference for mapping queries:

| Lens | Description | Example Queries |
|------|-------------|-----------------|
| **Temporal** | Time-based perception | "What day is it?", "What's on the agenda?" |
| **Hierarchy** | Structure/containment | "What projects are we working on?" |
| **Priority** | Urgency/importance | "What should I focus on?", "What needs attention?" |
| **Collaborative** | People/teams | "What did the team accomplish?" |
| **Flow** | Progress/state | "Show me stale PRs", "What's blocking?" |
| **Quantitative** | Metrics/counts | "How long have we been working?", "What's my productivity?" |
| **Causal** | Cause/effect | "What patterns do you see?" |
| **Contextual** | Background/setting | "What makes you different?" |

---

## The 4 Substrates (from P1)

Reference for mapping queries:

| Substrate | Description | Example |
|-----------|-------------|---------|
| **Entity** | Actors, agents | Users, Piper, team members |
| **Moment** | Bounded occurrences | Meetings, tasks, PRs, issues |
| **Place** | Contexts, locations | GitHub, Slack, Calendar, Notion |
| **Situation** | Frames combining elements | "Morning standup" (combines temporal + collaborative + Place) |

### Place Types
- Calendar (Google Calendar)
- GitHub
- Slack
- Notion
- Local (filesystem)

---

## Analysis Approach

### Phase 1: Query Inventory

**Read the canonical query matrix**:
```bash
cat docs/internal/testing/canonical-query-test-matrix-v2.md
```

**Extract all 63 queries organized by category**:
- Identity (5)
- Temporal (5)
- Spatial (4)
- Capability (5)
- Predictive (5)
- Conversational (5)
- Scheduling (5)
- Documents (5)
- GitHub Ops (8)
- Slack (5)
- Productivity (3)
- Todos (4)
- Calendar Extended (2)
- Knowledge (1)

**Deliverable**: Complete inventory list

---

### Phase 2: Lens Mapping

For EACH of the 63 queries, determine:
1. **Primary Lens**: The main perceptual dimension
2. **Secondary Lens(es)**: Additional dimensions if applicable
3. **Rationale**: Why this mapping

**Mapping Rules**:
- Choose the most natural fit, don't force
- Multiple lenses are fine for complex queries
- Flag queries that don't fit any lens

**Example Mappings**:
| Query | Primary Lens | Secondary | Rationale |
|-------|-------------|-----------|-----------|
| "What's on the agenda today?" | Temporal | Contextual | Time-bounded inquiry about schedule |
| "What should I focus on?" | Priority | Temporal | Urgency/importance with time context |
| "Show me stale PRs" | Flow | Temporal | Progress state + time decay |
| "What did we accomplish?" | Quantitative | Temporal | Measurement over time period |

**Deliverable**: 63-row lens mapping table

---

### Phase 3: Substrate Mapping

For EACH of the 63 queries, determine:
1. **Primary Substrate**: Entity, Moment, Place, or Situation
2. **Place Type**: If Place, which integration (GitHub, Slack, etc.)
3. **Rationale**: Why this mapping

**Mapping Rules**:
- Most queries about "things happening" → Moment
- Queries about "who" → Entity
- Queries about "where/context" → Place
- Complex queries combining elements → Situation

**Example Mappings**:
| Query | Substrate | Place Type | Rationale |
|-------|-----------|------------|-----------|
| "Create a GitHub issue" | Moment | GitHub | Creating bounded occurrence |
| "What projects are we working on?" | Situation | — | Frame combining project context |
| "Post update to team" | Moment | Slack | Bounded message occurrence |

**Deliverable**: 63-row substrate mapping table

---

### Phase 4: Coverage Analysis

**Coverage Categories**:
- **Clean**: Maps directly without forcing (both lens AND substrate clear)
- **Caveat**: Maps but requires explanation or judgment call
- **Gap**: Doesn't map cleanly - would need grammar concept that doesn't exist

**Calculate**:
```
Clean + Caveat = Expressible
Expressible / Total = Coverage %

Target: 80% coverage (50/63)
```

**Deliverable**: Coverage statistics with breakdown

---

### Phase 5: Gap Analysis

For EACH gap, analyze:
1. **Why** doesn't it map?
2. **Category**: Missing lens? Missing substrate? Grammar too restrictive? Query ambiguous?
3. **Recommendation**: Document (do NOT implement)

**Gap Categories**:
- Missing lens type needed
- Missing substrate type needed
- Grammar too restrictive
- Query is actually ambiguous/unclear
- Query is composite (needs decomposition)

**Deliverable**: Gap analysis with recommendations

---

### Phase 6: ADR-055 Appendix D

Create appendix in ADR-055 with:

```markdown
## Appendix D: Canonical Query Grammar Mapping (P4.5)

### Overview
P4.5 validates the lens/substrate grammar against 63 canonical queries.
"If we can't express what we already do, we've over-complicated."

### Coverage Summary
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Queries | 63 | 100% |
| Clean Mappings | X | Y% |
| Caveat Mappings | X | Y% |
| Gaps | X | Y% |
| **Overall Coverage** | X | **Y%** |

**Threshold Assessment**: [PASS/FAIL] (80% required for Tier 2)

### Full Mapping Table
| # | Query | Primary Lens | Secondary Lens(es) | Substrate | Place Type | Coverage | Notes |
|---|-------|-------------|-------------------|-----------|------------|----------|-------|
| 1 | What's your name and role? | Contextual | — | Entity | — | Clean | Identity query |
| 2 | ... | ... | ... | ... | ... | ... | ... |
[all 63 rows]

### Lens Distribution
| Lens | Primary Count | Secondary Count |
|------|--------------|-----------------|
| Temporal | X | Y |
| Priority | X | Y |
| ... | ... | ... |

### Substrate Distribution
| Substrate | Count |
|-----------|-------|
| Entity | X |
| Moment | X |
| Place | X |
| Situation | X |

### Gap Analysis
[For each gap, document why and recommendation]

### P4.5 Implementation Evidence
- **Analysis Date**: 2026-01-19
- **Queries Analyzed**: 63
- **Coverage**: X%
- **GitHub Issue**: #617
```

**Deliverable**: Complete ADR-055 Appendix D

---

## Phase Z: Completion & Handoff

**Verification Commands**:
```bash
# 1. Verify ADR-055 updated
grep -A 5 "Appendix D" docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md

# 2. Count mapping table rows
grep -c "^\| [0-9]" docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md

# 3. Check total ADR length
wc -l docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md
```

**Handoff Format**:
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

**Lens Distribution:**
- Temporal: X primary
- Priority: X primary
- [etc.]

**Gap Categories:**
- [category]: X queries
- [category]: Y queries

**TOTAL: 6/6 = 100%**
```

---

## STOP Conditions

**STOP immediately and escalate if:**
1. Coverage below 60% (grammar fundamentally broken)
2. Major feature areas completely unmapped (e.g., all GitHub queries are gaps)
3. Lens or substrate concepts appear fundamentally wrong
4. Analysis reveals P1 implementation needs revision
5. Scope creep into implementation territory

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Does the completion matrix show 6/6 = 100%?
2. Did I map all 63 queries?
3. Did I calculate coverage percentage correctly?
4. Is coverage at or above 80%? If not, did I explain why?
5. Is ADR-055 Appendix D complete with full table?
6. Did I document all gaps with rationale?
7. Am I claiming without evidence?
8. Did I accidentally write any code? (Should be documentation only)

---

## Related Documentation

- **P1**: `services/mux/protocols.py` - Lenses and Protocols
- **Canonical Queries**: `docs/internal/testing/canonical-query-test-matrix-v2.md`
- **ADR-045**: Object Model specification
- **ADR-055**: Implementation details (add Appendix D)
- **PPM Memo**: 80% coverage = Tier 2 success

---

_Prompt created: 2026-01-19_
_Template version: v10.2_
