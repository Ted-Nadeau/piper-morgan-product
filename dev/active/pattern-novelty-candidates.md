# Pattern Novelty Candidates
**Period**: November 20 - December 26, 2025
**Generated**: 2025-12-27
**Agent**: Agent C (Novelty Detector)
**Source Data**: late-nov-pattern-sweep.json, early-dec-pattern-sweep.json, late-dec-pattern-sweep.json, omnibus logs, session logs

---

## Executive Summary

**Total Candidates Evaluated**: 8 major pattern clusters
**TRUE EMERGENCE Candidates**: 2
**PATTERN COMBINATIONS**: 2
**PATTERN EVOLUTIONS**: 4
**FALSE POSITIVE TEST**: PASSED ✅

All patterns flagged in sweep data were cross-referenced against the 44-pattern library index. Known patterns (75% pattern/Pattern-045, verification-first/Pattern-006, multi-agent coordination/Pattern-029) were correctly identified as existing.

---

## TRUE EMERGENCE Candidates

### Candidate 1: "Beads Completion Discipline"
**First Appearance**: November 13-14, 2025
**Evidence**: 104 files mention "Beads", "bd-safe", "issue closure discipline"
**Not in Library Because**: No pattern in library covers systematic issue closure discipline with workflow wrapper tools

**Description**: A completion discipline pattern enforcing 100% acceptance criteria fulfillment before issue closure. Uses `bd-safe` wrapper for validation and prevents "expedience rationalization" (claiming work is "optional" or "nice-to-have" to avoid completing it).

**Key Components**:
1. **Session Start Protocol**: `bd ready --json`, `bd list`, `bd status`
2. **Proactive Issue Creation**: Discover work mid-task → `bd create` immediately
3. **Completion Criteria Enforcement**: Every criterion met OR explicit `@PM-approval-needed` tag
4. **No Expedience Rationalization**: PM decides priority, not agent
5. **Session End Protocol ("Landing the Plane")**: File remaining work, run quality gates, close only completed issues, sync database, verify no orphaned children

**Evidence Trail**:
- `docs/proposals/beads-integration-proposal.md` (Nov 13-14)
- `docs/dev-tips/landing-the-plane-checklist.md` (148 files mention "Landing the Plane")
- CLAUDE.md "BEADS COMPLETION DISCIPLINE" section (Nov 13+)
- `.serena/memories/beads-discovered-work-discipline.md`

**Proposed Classification**: **TRUE EMERGENCE**
**Recommendation**: Catalog as **DRAFT-pattern-045** (Development & Process category)

**Why This Is Novel**:
- Goes beyond Pattern-006 (Verification-First) by adding workflow tooling
- More specific than Pattern-009 (GitHub Issue Tracking) - adds completion discipline
- Distinct from Pattern-010 (Cross-Validation Protocol) - focuses on closure, not validation

---

### Candidate 2: "Time Lord Alert" - Face-Saving Escalation Signal
**First Appearance**: November 27, 2025
**Evidence**: 10 files mention "Time Lord Alert", "escape hatch", "face-saving"
**Not in Library Because**: No pattern covers agent-initiated uncertainty signaling

**Description**: A designated escape hatch phrase ("Time Lord Alert") that agents use to signal uncertainty without explicitly admitting lack of knowledge. Enables productive pause for discussion without undermining agent credibility.

**Key Components**:
1. Agent says "Time Lord Alert" when uncertain about decision
2. PM pauses for discussion
3. Face-saving mechanism - avoids direct "I don't know"
4. Reduces completion bias pressure

**Evidence Trail**:
- CLAUDE.md: "Time Lord Alert escape hatch" section
- `dev/2025/11/27/2025-11-27-0600-grat-opus-log.md`
- Referenced in anti-completion-bias protocol

**Proposed Classification**: **TRUE EMERGENCE**
**Recommendation**: Catalog as **DRAFT-pattern-046** (Development & Process category)

**Why This Is Novel**:
- Not covered by Pattern-010 (Cross-Validation) - that's about evidence, not escalation
- Not covered by Pattern-021 (Development Session Management) - that's logging, not communication
- Unique communication protocol pattern for human-agent collaboration

---

## PATTERN COMBINATIONS Detected

### Combination 1: "Systematic Debugging Framework" + "Five Whys"
**Patterns Combined**: Pattern-042 (Investigation-Only Protocol) + external methodology (Five Whys)
**Novel Aspect**: Integration of root cause analysis into multi-phase investigation protocol
**Context**: Dec 20 overnight canonical query debugging session

**Description**: The existing Investigation-Only Protocol (Pattern-042) was enhanced with Five Whys methodology to create a systematic debugging process enforced in CLAUDE.md:

1. **Root cause investigation** (BEFORE fixes)
2. **Pattern analysis** (find working examples)
3. **Hypothesis and testing** (minimal changes)
4. **Implementation rules** (simplest failing test)

**Evidence**: CLAUDE.md "Systematic debugging process" section (24 mentions of "Five Whys"), pattern-045-green-tests-red-user.md

**Classification**: **PATTERN COMBINATION**
**Action**: Update Pattern-042 to reference Five Whys integration

---

### Combination 2: "Phase -1" Infrastructure Verification
**Patterns Combined**: Pattern-006 (Verification-First) + gameplan structure
**Novel Aspect**: Dedicated pre-Phase-0 infrastructure verification gate
**Context**: Nov 23+, 425+ file mentions

**Description**: "Phase -1" (also called "Phase Zero", "VERIFY FIRST") is a mandatory infrastructure verification step added BEFORE any gameplan Phase 0. Agents must verify codebase matches gameplan assumptions before proceeding.

**Key Requirements**:
- Check file/directory existence
- Verify pattern consistency
- Confirm infrastructure assumptions
- STOP if mismatch found

**Evidence**: CLAUDE.md "INFRASTRUCTURE VERIFICATION FIRST" section, 425+ files in codebase

**Classification**: **PATTERN COMBINATION**
**Action**: This is an evolution of Pattern-006 (Verification-First) - consider documenting as Pattern-006 variant

---

## PATTERN EVOLUTION Detected

### Evolution 1: Pattern-029 (Multi-Agent Coordination) → Evidence Requirements
**Original Pattern**: Multi-Agent Coordination (workflow, collaboration)
**Evolution**: Added mandatory evidence format and handoff protocol
**First Detected**: December 24, 2025
**Evidence**: CLAUDE.md "Multi-Agent Coordination Protocol" updates

**What Changed**:
- **Before**: General coordination principles
- **After**: Specific evidence requirements (test count, file locations, verification commands, user verification steps)
- **New Requirement**: Every issue closure MUST include implementation evidence block

**Quote**:
```
Every issue closure MUST include:
- Tests: X tests added/modified in [file]
- Verification: `pytest path/to/tests -v` (all passing)
- Files: [list of modified files]
- User verification: [how to test as user]
```

**Classification**: **PATTERN EVOLUTION**
**Action**: Update Pattern-029 documentation with evidence requirements

---

### Evolution 2: Pattern-006 (Verification-First) → "Done Means User-Verified"
**Original Pattern**: Verification-First Development
**Evolution**: Expanded definition of "Done" to require user verification
**First Detected**: December 3-7, 2025 (Green Tests, Red User incidents)
**Evidence**: pattern-045-green-tests-red-user.md

**What Changed**:
- **Before**: "Write verification before implementation"
- **After**: "Done = user can accomplish task" (not "tests pass")
- **New Practice**: Browser verification, fresh install testing, complete user journey

**Quote**:
> "The discipline is to mark it 'done' when a user can use it." - Lead Developer, Dec 3

**Classification**: **PATTERN EVOLUTION**
**Action**: Pattern-045 (Green Tests, Red User) already documents this - consider cross-reference in Pattern-006

---

### Evolution 3: Pattern-045 (Green Tests, Red User) → Established Anti-Pattern
**Status Change**: From emergent practice (Dec 7) to documented anti-pattern (Dec 25)
**Evolution**: Codified prevention strategies and detection signals
**Evidence**: `dev/active/pattern-045-green-tests-red-user.md`

**What Changed**:
- **Dec 7**: First instance (UUID type mismatch, 24-hour debug)
- **Dec 17-18**: Second instance (FK violations)
- **Dec 20**: Third instance (Intent classification)
- **Dec 25**: Formalized as anti-pattern with prevention strategies

**Now Includes**:
- Integration testing requirements
- Schema validation on startup
- Fresh install testing protocol
- E2E scenario testing
- Critical path smoke tests

**Classification**: **PATTERN EVOLUTION**
**Action**: Pattern-045 is now established - no further action needed

---

### Evolution 4: Session End Protocol → "Landing the Plane" Checklist
**Original**: General session discipline
**Evolution**: Formalized 5-step checklist for session endings
**First Detected**: November 2025+
**Evidence**: 148 files mention "Landing the Plane", `docs/dev-tips/landing-the-plane-checklist.md`

**5-Step Protocol**:
1. File all remaining work as issues
2. Run quality gates (if code changed)
3. Close completed issues only
4. Sync database (bd sync, git status clean)
5. Verify no open children

**Classification**: **PATTERN EVOLUTION**
**Action**: This is part of Beads Discipline (Candidate 1) - will be documented there

---

## False Positive Prevention

**Verified against library - patterns CORRECTLY identified as existing**:

| Pattern Name | Library Status | Verification |
|--------------|----------------|--------------|
| "75% pattern" / completion bias | ✅ Pattern-045 | Documented Dec 25, 2025 |
| "verification-first" | ✅ Pattern-006 | Core Architecture category |
| "multi-agent coordination" | ✅ Pattern-029 | AI & Intelligence category |
| "AsyncSessionFactory" | ✅ ADR-047 | Architectural insight (not pattern) |
| "WorkflowFactory" | ✅ Mentioned in codebase | Implementation, not pattern |
| "completion matrix" | ✅ Part of gameplans | Tool, not pattern |
| "spatial intelligence" | ✅ Pattern-020/022 | MCP+Spatial Integration |
| "boundary enforcement" | ✅ Pattern-043 | Defense-in-Depth Prevention |
| "cross-validation" | ✅ Pattern-010/037 | Cross-Validation Protocol |
| "evidence-based" | ✅ Pattern-029 evolution | See Evolution 1 above |
| "parallel execution" | ✅ Pattern-029 | Multi-Agent Coordination |

**FALSE POSITIVE TEST RESULT**: ✅ **PASSED** - All known patterns correctly identified

---

## Patterns NOT Selected (Usage, Not Emergence)

These patterns appeared frequently in sweep data but are **PATTERN USAGE**, not novelty:

1. **"Archaeological investigation"** - Standard Pattern-042 application (Investigation-Only)
2. **"Systematic verification"** - Standard Pattern-006 usage (Verification-First)
3. **"Handoff pattern"** - Part of Pattern-029 (Multi-Agent Coordination)
4. **"CODE ≠ DATA"** - Principle, not pattern (from ADR discussions)
5. **"Anti-80% Protocol"** - Another name for Pattern-045 (Green Tests, Red User)
6. **"Phase -1"** - See Combination 2 above (Pattern-006 variant)

---

## Recommendations

### Immediate Actions
1. **Catalog Beads Completion Discipline** as Pattern-046 (Development & Process)
2. **Catalog Time Lord Alert** as Pattern-047 (Development & Process)
3. **Update Pattern-029** with evidence requirements (Evolution 1)
4. **Cross-reference Pattern-006** with Pattern-045 (Evolution 2)
5. **Document Phase -1** as Pattern-006 variant or standalone pattern

### Pattern Library Maintenance
- Total patterns after additions: 46 (44 existing + 2 new)
- No duplicates detected
- Library coverage validated against 6-week period

### Future Sweep Improvements
- ✅ Pattern library awareness working
- ✅ False positive prevention effective
- ✅ 5-tier classification helpful
- Consider: Automated pattern signature extraction from library

---

## Appendix: Classification Tier Definitions

1. **TRUE EMERGENCE** - Genuinely new pattern never seen before (2 candidates)
2. **PATTERN EVOLUTION** - Variation or refinement of existing pattern (4 detected)
3. **PATTERN COMBINATION** - Novel mixing of known patterns (2 detected)
4. **PATTERN USAGE** - Standard application of existing pattern (6+ observed)
5. **ANTI-PATTERN** - Degradation or misuse of pattern (Pattern-045 now documented)

---

*Analysis completed: December 27, 2025, 11:30 AM PT*
*Methodology: Pattern Sweep 2.0 Framework*
*Source files analyzed: 600+ (omnibus logs, session logs, active docs, pattern library)*
*Confidence: HIGH (library cross-reference + multi-source validation)*
