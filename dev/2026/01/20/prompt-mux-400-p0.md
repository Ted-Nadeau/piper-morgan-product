# Agent Prompt: MUX-400 Phase 0 (Vision Archaeology)

## Your Identity
You are Claude Code (Haiku), a development agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #400 MUX-VISION-CONSCIOUSNESS
- **Epic**: MUX-VISION (#401)
- **Gameplan**: `dev/2026/01/20/gameplan-mux-400.md`
- **Prerequisites**: #399 complete, #404 complete

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase 0 of issue #400. Your work enables the Philosophy Document (Phase 1).

### Your Acceptance Criteria
- [ ] PM-070 original vision document located OR alternatives identified
- [ ] Nov 25 gap analysis located OR alternatives identified
- [ ] Key consciousness concepts extracted
- [ ] Source material summary created

### Evidence You MUST Provide
1. **Document locations**: Exact file paths or "not found"
2. **Key quotes**: Relevant passages extracted
3. **Concepts identified**: List of consciousness concepts
4. **Handoff notes**: What Phase 1 needs to know

### Your Handoff Format
```
## MUX-400 P0 Completion Report
**Status**: Complete/Partial/Blocked

**Source Materials**:
- PM-070: [found at path OR not found - alternatives]
- Nov 25 Gap Analysis: [found at path OR not found - alternatives]
- Other relevant docs: [list]

**Key Consciousness Concepts Found**:
1. [concept with source]
2. [concept with source]
...

**Five Orientation Queries** (from original vision):
1. Identity: "Who am I?"
2. Temporal: "When am I?"
3. Spatial: "Where am I?"
4. Capability: "What can I do?"
5. Predictive: "What should happen?"

**Handoff Notes for Phase 1**:
- [key insight]
- [key insight]

**Blockers** (if any):
- [description]
```

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

```bash
# Verify #399 complete
gh issue view 399 --repo mediajunkie/piper-morgan-product --json state
# Expected: CLOSED

# Verify #404 complete
gh issue view 404 --repo mediajunkie/piper-morgan-product --json state
# Expected: CLOSED

# Verify existing documentation exists (from #404)
ls -la docs/internal/development/grammar-transformation-guide.md
ls -la docs/internal/development/grammar-onboarding-checklist.md
ls -la docs/internal/architecture/current/patterns/grammar-application-patterns.md
# Expected: All exist

# Verify Morning Standup exists (reference)
ls -la services/features/morning_standup.py
# Expected: File exists
```

**If ANY verification fails**: STOP and report with evidence.

---

## Mission

**Phase 0**: Locate and study original embodied AI vision documents

**Scope Boundaries**:
- This prompt covers ONLY: Finding source materials and extracting concepts
- NOT in scope: Writing the philosophy document (Phase 1)
- Separate prompts handle: Phases 1, 2, Z

---

## Context

- **GitHub Issue**: #400 MUX-VISION-CONSCIOUSNESS
- **Current State**: #399 and #404 complete, philosophy doc missing
- **Target State**: Source materials located, concepts extracted
- **Dependencies**: #399 complete, #404 complete
- **Infrastructure Verified**: Yes (from gameplan)

---

## Session Log Management

**IMPORTANT**: Check for existing log before creating new one!

```bash
# Check if log exists today
ls -la dev/2026/01/20/*-prog-code-*-log.md

# If log exists: APPEND to it, don't create new
# If no log exists: Create dev/2026/01/20/YYYY-MM-DD-HHMM-prog-code-haiku-log.md
```

---

## Implementation Approach

### Step 0.1: Search for PM-070

```bash
# Search for PM-070 references
find . -name "*PM-070*" -o -name "*pm-070*" -o -name "*pm070*" 2>/dev/null
grep -r "PM-070" docs/ knowledge/ dev/ --include="*.md" 2>/dev/null | head -30

# Search for July 2025 vision documents
find dev/ -path "*2025/07*" -name "*.md" 2>/dev/null
grep -r "embodied AI" docs/ knowledge/ --include="*.md" 2>/dev/null | head -20
grep -r "canonical queries" docs/ knowledge/ --include="*.md" 2>/dev/null | head -20
grep -r "orientation queries" docs/ knowledge/ --include="*.md" 2>/dev/null | head -20
```

**If PM-070 not found**: Document what was searched, note for PM.

### Step 0.2: Search for Nov 25 Gap Analysis

```bash
# Search for Nov 25 references
find dev/ -path "*2025/11/25*" -name "*.md" 2>/dev/null
grep -r "Nov 25" docs/ dev/ --include="*.md" 2>/dev/null | head -20
grep -r "CXO session" docs/ dev/ --include="*.md" 2>/dev/null | head -20
grep -r "consciousness.*flattened" docs/ dev/ --include="*.md" 2>/dev/null | head -20
grep -r "got flattened" docs/ dev/ --include="*.md" 2>/dev/null | head -20
```

**If Nov 25 doc not found**: Document what was searched, note for PM.

### Step 0.3: Search for Alternative Sources

If primary documents not found, look for:

```bash
# ADRs about consciousness/embodied AI
grep -r "embodied" docs/internal/architecture/current/adrs/ --include="*.md" | head -20
grep -r "consciousness" docs/internal/architecture/current/adrs/ --include="*.md" | head -20

# P0 analysis from #399 (already studied Morning Standup)
cat dev/2026/01/19/p0-morning-standup-analysis.md

# Any references to original vision
grep -r "original vision" docs/ dev/ --include="*.md" 2>/dev/null | head -20
grep -r "five.*queries" docs/ dev/ --include="*.md" 2>/dev/null | head -20
```

### Step 0.4: Extract Key Concepts

From whatever sources found, extract:

1. **Five Orientation Queries** (if found):
   - Identity: "Who am I?"
   - Temporal: "When am I?"
   - Spatial: "Where am I?"
   - Capability: "What can I do?"
   - Predictive: "What should happen?"

2. **Consciousness Indicators** (from #400 issue):
   - Use of "I" vs mechanical third-person
   - Expressions of uncertainty
   - Emotional markers
   - Contextual awareness
   - Predictive capability

3. **Key Quotes** about consciousness/embodied AI

### Step 0.5: Create Source Summary

Create a working document summarizing findings:
- What was found
- What wasn't found
- Key concepts extracted
- Recommendations for Phase 1

---

## Success Criteria

- [ ] Infrastructure verified (#399, #404 complete)
- [ ] PM-070 search complete (found or documented as not found)
- [ ] Nov 25 search complete (found or documented as not found)
- [ ] Alternative sources explored
- [ ] Key concepts extracted
- [ ] Handoff notes for Phase 1 created

---

## STOP Conditions

Stop and escalate if:
- #399 or #404 not complete (should be)
- No source materials can be located AND no alternatives exist
- Concepts unclear and need PM clarification

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Did I verify #399 and #404 are complete?
2. Did I search thoroughly for PM-070?
3. Did I search thoroughly for Nov 25 gap analysis?
4. Did I explore alternative sources?
5. Did I extract key concepts?
6. Did I create handoff notes for Phase 1?
7. Did I provide handoff in the required format?

---

## Deliverables

1. **Session log**: Append to existing or create new
2. **Source material summary**: Key findings documented
3. **Handoff report**: Completion status with evidence

---

*Prompt Version: Based on template v10.2*
*Created: 2026-01-20*
*Issue: #400 Phase 0*
