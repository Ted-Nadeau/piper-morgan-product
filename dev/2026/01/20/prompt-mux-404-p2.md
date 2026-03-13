# Agent Prompt: MUX-404 Phase 2 (Application Pattern Catalog)

## Your Identity
You are Claude Code (Sonnet), a development agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #404 MUX-VISION-GRAMMAR-CORE
- **Epic**: #399 complete (302 MUX tests)
- **Gameplan**: `dev/2026/01/20/gameplan-mux-404.md`
- **Prerequisite**: Phase 0-1 complete (grammar audit)

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase 2 of issue #404. Your work enables the Transformation Guide (Phase 3).

### Your Acceptance Criteria
- [ ] 5+ application patterns extracted from Morning Standup
- [ ] Each pattern documented in catalog format
- [ ] Grammar application templates created
- [ ] Patterns reference MUX infrastructure correctly
- [ ] Pattern files created in `docs/internal/architecture/current/patterns/`

### Evidence You MUST Provide
1. **Pattern count**: "5 patterns documented"
2. **File locations**: `ls -la` showing pattern files exist
3. **Pattern format**: Each follows catalog format
4. **Cross-references**: Links to MUX implementation verified

### Your Handoff Format
```
## MUX-404 P2 Completion Report
**Status**: Complete/Partial/Blocked

**Patterns Created**: X patterns

**Pattern List**:
1. pattern-0XX-[name].md - [description]
2. pattern-0XX-[name].md - [description]
...

**Files Created**:
- docs/internal/architecture/current/patterns/pattern-0XX-*.md (+X lines each)
- docs/internal/architecture/current/patterns/grammar-application-patterns.md (+X lines)

**Verification**:
$ ls -la docs/internal/architecture/current/patterns/pattern-0*
[output]

**Blockers** (if any):
- [description]
```

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

```bash
# Verify Phase 0-1 complete
ls -la docs/internal/architecture/current/grammar-compliance-audit.md
# Expected: File exists

# Verify pattern catalog location
ls -la docs/internal/architecture/current/patterns/
# Note existing patterns

# Check next available pattern number
ls docs/internal/architecture/current/patterns/pattern-*.md | tail -5
# Find highest pattern number

# Verify Morning Standup exists
ls -la services/features/morning_standup.py
# Expected: File exists

# Verify P0 analysis
ls -la dev/2026/01/19/p0-morning-standup-analysis.md
# Expected: File exists
```

**If ANY verification fails**: STOP and report with evidence.

---

## Mission

**Phase 2**: Extract and formalize reusable application patterns from Morning Standup

**Scope Boundaries**:
- This prompt covers ONLY: Pattern extraction and documentation
- NOT in scope: Grammar audit (Phase 1), transformation guide (Phase 3)
- Separate prompts handle: Phases 0-1, 3, Z

---

## Context

- **GitHub Issue**: #404 MUX-VISION-GRAMMAR-CORE
- **Current State**: Grammar audit complete, patterns not yet formalized
- **Target State**: 5+ reusable patterns in catalog format
- **Dependencies**: Phase 0-1 complete, P0 analysis available
- **Infrastructure Verified**: Yes (from gameplan Phase -1)

---

## Session Log Management

**IMPORTANT**: Check for existing log before creating new one!

```bash
# Check if log exists today
ls -la dev/2026/01/20/*-prog-code-*-log.md

# If log exists: APPEND to it, don't create new
# If no log exists: Create dev/2026/01/20/YYYY-MM-DD-HHMM-prog-code-sonnet-log.md
```

---

## Implementation Approach

### Step 2.0: Review Source Materials

```bash
# Read P0 Morning Standup analysis
cat dev/2026/01/19/p0-morning-standup-analysis.md

# Read Morning Standup implementation
cat services/features/morning_standup.py

# Review grammar compliance audit
cat docs/internal/architecture/current/grammar-compliance-audit.md

# Check existing pattern format
cat docs/internal/architecture/current/patterns/pattern-001-*.md | head -50
```

**Extract from P0 analysis**:
- Context Dataclass Pair pattern
- Parallel Place Gathering pattern
- Personality Bridge pattern
- Warmth Calibration pattern
- Honest Failure with Suggestion pattern

### Step 2.1: Determine Pattern Numbers

```bash
# Find highest existing pattern number
ls docs/internal/architecture/current/patterns/pattern-*.md | sort | tail -1
# Use next sequential numbers
```

### Step 2.2: Create Pattern Documents

For each pattern, create `docs/internal/architecture/current/patterns/pattern-0XX-[name].md`:

**Pattern Document Structure**:
```markdown
# Pattern-0XX: [Pattern Name]

## Category
Grammar Application

## Problem
[What problem does this pattern solve?]

## Context
[When should this pattern be used?]

## Solution
[How does the pattern work?]

## Implementation

### Structure
[Code structure or pseudocode]

### Example from Morning Standup
```python
[Actual code from morning_standup.py]
```

## Consequences
### Benefits
- [Benefit 1]
- [Benefit 2]

### Trade-offs
- [Trade-off 1]

## Related Patterns
- [Related pattern references]

## MUX Integration
- Uses: [MUX components used]
- Protocols: [Which protocols apply]
- Lenses: [Which lenses apply]

## References
- Morning Standup: `services/features/morning_standup.py`
- MUX Implementation Guide: `docs/internal/development/mux-implementation-guide.md`
```

### Step 2.3: Pattern 1 - Context Dataclass Pair

**Pattern-0XX: Context Dataclass Pair**

Extract from Morning Standup:
- `StandupContext` - input context dataclass
- `StandupResult` - output result dataclass
- Clean separation of concerns
- Type safety and documentation

### Step 2.4: Pattern 2 - Parallel Place Gathering

**Pattern-0XX: Parallel Place Gathering**

Extract from Morning Standup:
- Gather from Calendar, GitHub, etc. concurrently
- Place-aware aggregation
- Per-place error handling
- Graceful degradation per source

### Step 2.5: Pattern 3 - Personality Bridge

**Pattern-0XX: Personality Bridge**

Extract from Morning Standup:
- Transform raw data → warm narrative
- Piper's voice and perspective
- Entity awareness (user, Piper)
- Moment framing (past/present/future)

### Step 2.6: Pattern 4 - Warmth Calibration

**Pattern-0XX: Warmth Calibration**

Extract from Morning Standup:
- Adjust tone based on context
- Time-of-day awareness
- Urgency modulation
- Atmosphere inheritance from Place

### Step 2.7: Pattern 5 - Honest Failure with Suggestion

**Pattern-0XX: Honest Failure with Suggestion**

Extract from Morning Standup:
- Graceful degradation
- "I couldn't reach X, but..."
- Recovery suggestions
- Maintain warmth in failure

### Step 2.8: Create Grammar Application Templates Overview

Create `docs/internal/architecture/current/patterns/grammar-application-patterns.md`:

```markdown
# Grammar Application Patterns

## Overview
Patterns extracted from Morning Standup for applying the MUX grammar
"Entities experience Moments in Places" to features.

## Pattern Index
1. [Pattern-0XX: Context Dataclass Pair](pattern-0XX-context-dataclass-pair.md)
2. [Pattern-0XX: Parallel Place Gathering](pattern-0XX-parallel-place-gathering.md)
3. [Pattern-0XX: Personality Bridge](pattern-0XX-personality-bridge.md)
4. [Pattern-0XX: Warmth Calibration](pattern-0XX-warmth-calibration.md)
5. [Pattern-0XX: Honest Failure](pattern-0XX-honest-failure.md)

## Grammar Application Templates

### Entity Awareness Template
[How to track identity through flow]

### Moment Framing Template
[How to use PerceptionMode: NOTICING, REMEMBERING, ANTICIPATING]

### Place Atmosphere Template
[How context affects presentation]

### Situation Container Template
[How to group related moments with dramatic tension]

## When to Apply

| Situation | Recommended Patterns |
|-----------|---------------------|
| Multi-source data gathering | Parallel Place Gathering |
| User-facing responses | Personality Bridge, Warmth Calibration |
| Error handling | Honest Failure |
| Complex feature input/output | Context Dataclass Pair |

## MUX Integration
- Protocols: `services/mux/protocols.py`
- Lenses: `services/mux/lenses/`
- Implementation Guide: `docs/internal/development/mux-implementation-guide.md`

## Related
- Grammar Compliance Audit: `docs/internal/architecture/current/grammar-compliance-audit.md`
- ADR-055: Object Model Implementation
```

---

## Success Criteria

- [ ] Infrastructure verified (Phase 1 complete)
- [ ] 5+ patterns extracted and documented
- [ ] Each pattern follows catalog format
- [ ] Grammar application overview created
- [ ] Patterns reference MUX infrastructure correctly
- [ ] Files exist at correct paths
- [ ] Pattern numbers don't conflict with existing

---

## STOP Conditions

Stop and escalate if:
- Phase 0-1 not complete
- Morning Standup implementation missing
- P0 analysis not available
- Pattern number conflict with existing catalog
- Morning Standup patterns can't be generalized

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Did I verify Phase 0-1 is complete?
2. Did I create 5+ pattern documents?
3. Does each pattern follow the catalog format?
4. Did I create the grammar-application-patterns.md overview?
5. Do patterns correctly reference MUX infrastructure?
6. Can I show `ls -la` evidence the files exist?
7. Did I use correct pattern numbers (no conflicts)?
8. Did I provide handoff in the required format?

---

## Deliverables

1. **Session log**: Append to existing or create new
2. **Pattern documents**: 5+ files in `docs/internal/architecture/current/patterns/`
3. **Overview document**: `docs/internal/architecture/current/patterns/grammar-application-patterns.md`
4. **Handoff report**: Completion status with evidence

---

*Prompt Version: Based on template v10.2*
*Created: 2026-01-20*
*Issue: #404 Phase 2*
