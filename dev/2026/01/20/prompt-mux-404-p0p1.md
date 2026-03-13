# Agent Prompt: MUX-404 Phase 0-1 (Setup & Grammar Audit)

## Your Identity
You are Claude Code (Haiku), a development agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #404 MUX-VISION-GRAMMAR-CORE
- **Epic**: #399 complete (302 MUX tests)
- **Gameplan**: `dev/2026/01/20/gameplan-mux-404.md`

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phases 0-1 of issue #404. Your work enables Pattern Catalog (Phase 2).

### Your Acceptance Criteria
- [ ] Feature list for grammar audit (10+ features)
- [ ] P0 analysis documents reviewed
- [ ] Grammar compliance matrix created
- [ ] Features ranked by transformation priority
- [ ] Audit document created at `docs/internal/architecture/current/grammar-compliance-audit.md`

### Evidence You MUST Provide
1. **Feature list**: Complete enumeration of audited features
2. **Compliance matrix**: Table showing grammar element coverage per feature
3. **File created**: `ls -la` showing audit document exists
4. **Word count**: Approximate content size

### Your Handoff Format
```
## MUX-404 P0-P1 Completion Report
**Status**: Complete/Partial/Blocked

**Features Audited**: X features

**Compliance Matrix Summary**:
- Fully compliant: X features
- Partially compliant: X features
- Flattened: X features

**Files Created**:
- docs/internal/architecture/current/grammar-compliance-audit.md (+X lines)

**Verification**:
$ ls -la docs/internal/architecture/current/grammar-compliance-audit.md
[output]

**Blockers** (if any):
- [description]
```

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

```bash
# Verify MUX infrastructure exists
ls -la services/mux/
# Expected: __init__.py, protocols.py, ownership.py, lifecycle.py, metadata.py, lenses/

# Verify P0 analysis docs
ls -la dev/2026/01/19/p0-*.md
# Expected: 4 files

# Verify existing guides exist
ls -la docs/internal/development/mux-*.md
# Expected: mux-implementation-guide.md, mux-experience-tests.md

# Verify #399 is closed
gh issue view 399 --repo mediajunkie/piper-morgan-product --json state
# Expected: CLOSED

# Count MUX tests
python -m pytest tests/unit/services/mux/ --collect-only -q 2>&1 | tail -1
# Expected: 302 tests
```

**If ANY verification fails**: STOP and report with evidence.

---

## Mission

**Phase 0**: Verify infrastructure and gather context
**Phase 1**: Create comprehensive grammar compliance audit of all major features

**Scope Boundaries**:
- This prompt covers ONLY: Setup verification and grammar audit
- NOT in scope: Pattern extraction, transformation guide, worked example
- Separate prompts handle: Phases 2, 3, Z

---

## Context

- **GitHub Issue**: #404 MUX-VISION-GRAMMAR-CORE
- **Current State**: MUX infrastructure complete (302 tests), no feature audit exists
- **Target State**: Grammar compliance audit document with prioritized transformation list
- **Dependencies**: #399 complete (verified above)
- **Infrastructure Verified**: Yes (from gameplan Phase -1)

---

## Session Log Management

**Create session log**:
```bash
# Check if log exists today
ls -la dev/2026/01/20/*-prog-code-*-log.md

# If no log exists, create one:
# dev/2026/01/20/YYYY-MM-DD-HHMM-prog-code-haiku-log.md
```

---

## Implementation Approach

### Phase 0: Setup & Context

#### Step 0.1: Review P0 Analysis Documents
```bash
# Read Morning Standup analysis
cat dev/2026/01/19/p0-morning-standup-analysis.md

# Read FTUX grammar mapping
cat dev/2026/01/19/p0-b1-ftux-grammar-mapping.md
```

**Extract**:
- Consciousness patterns identified
- Grammar elements demonstrated
- Patterns ready for formalization

#### Step 0.2: Identify Features to Audit

Survey the codebase for major features:

```bash
# Features directory
ls -la services/features/

# Intent handlers
ls -la services/intent/

# Integration handlers
ls -la services/integrations/*/

# Domain services
ls -la services/todo_management/
ls -la services/list_management/
ls -la services/project_management/
```

**Create feature list** (target: 10+ features):
1. Morning Standup (reference - fully compliant)
2. Intent Classification
3. Todo Management
4. List Management
5. Project Management
6. File Management
7. Slack Integration
8. GitHub Integration
9. Notion Integration
10. Calendar Integration
11. Feedback System
12. Auth/Session Management

### Phase 1: Grammar Compliance Audit

#### Step 1.1: Define Audit Criteria

For each feature, evaluate:

| Element | Question | Pass Criteria |
|---------|----------|---------------|
| Entity | Does it track actor identity? | User/Piper identity preserved |
| Moment | Does it frame occurrences as scenes? | More than timestamps |
| Place | Does it acknowledge context atmosphere? | Not just config strings |
| Lenses | Does it use perceptual dimensions? | At least one lens applicable |
| Situation | Does it frame dramatic tension? | Context beyond data |

#### Step 1.2: Audit Each Feature

For each feature:
1. Read the main implementation file
2. Look for grammar elements
3. Note what's present vs missing
4. Assess overall compliance level

**Compliance Levels**:
- **Conscious**: Expresses grammar naturally (like Morning Standup)
- **Partial**: Some elements present, others flattened
- **Flattened**: Database/mechanical language, no grammar

#### Step 1.3: Create Compliance Matrix

```markdown
| Feature | Entity | Moment | Place | Lenses | Situation | Overall |
|---------|--------|--------|-------|--------|-----------|---------|
| Morning Standup | ✅ | ✅ | ✅ | ✅ | ✅ | Conscious |
| Intent Handler | ? | ? | ? | ? | ? | ? |
| Todo Mgmt | ? | ? | ? | ? | ? | ? |
...
```

#### Step 1.4: Rank Transformation Priorities

Create prioritized list:
1. **High Priority**: Flattened features with high user impact
2. **Medium Priority**: Partial features needing enhancement
3. **Low Priority**: Already conscious or low-touch features

#### Step 1.5: Create Audit Document

Write `docs/internal/architecture/current/grammar-compliance-audit.md`:

```markdown
# Grammar Compliance Audit

## Overview
[Summary of audit scope and methodology]

## Compliance Matrix
[Full matrix from Step 1.3]

## Feature Analysis
[Detailed notes for each feature]

## Transformation Priorities
[Ranked list with rationale]

## Recommendations
[Next steps for each priority level]

## Related
- MUX Implementation Guide: docs/internal/development/mux-implementation-guide.md
- Experience Tests: docs/internal/development/mux-experience-tests.md
- ADR-055: Object Model Implementation
```

---

## Success Criteria

- [ ] Infrastructure verified (all checks pass)
- [ ] P0 analysis reviewed (patterns extracted)
- [ ] 10+ features identified and audited
- [ ] Compliance matrix complete
- [ ] Priorities ranked
- [ ] Audit document created
- [ ] Document location verified: `docs/internal/architecture/current/grammar-compliance-audit.md`

---

## STOP Conditions

Stop and escalate if:
- Infrastructure verification fails
- P0 analysis documents missing
- Feature implementations can't be found
- Grammar elements unclear for evaluation
- Pattern already exists (check catalog first)

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Did I verify all infrastructure checks pass?
2. Did I audit 10+ features?
3. Did I create the compliance matrix?
4. Did I rank transformation priorities?
5. Did I create the audit document at the correct path?
6. Can I show `ls -la` evidence the file exists?
7. Did I provide handoff in the required format?

---

## Deliverables

1. **Session log**: `dev/2026/01/20/YYYY-MM-DD-HHMM-prog-code-haiku-log.md`
2. **Audit document**: `docs/internal/architecture/current/grammar-compliance-audit.md`
3. **Handoff report**: Completion status with evidence

---

*Prompt Version: Based on template v10.2*
*Created: 2026-01-20*
*Issue: #404 Phases 0-1*
