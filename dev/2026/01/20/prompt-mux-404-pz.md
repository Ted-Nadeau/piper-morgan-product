# Agent Prompt: MUX-404 Phase Z (Integration & Onboarding)

## Your Identity
You are Claude Code, a development agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #404 MUX-VISION-GRAMMAR-CORE
- **Epic**: #399 complete (302 MUX tests)
- **Gameplan**: `dev/2026/01/20/gameplan-mux-404.md`
- **Prerequisite**: Phases 0-3 complete

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase Z (final phase) of issue #404.

### Your Acceptance Criteria
- [ ] ADR-045 updated with implementation references
- [ ] ADR-055 updated with pattern links
- [ ] Developer onboarding checklist created
- [ ] All deliverables cross-referenced
- [ ] Issue #404 ready for PM closure

### Evidence You MUST Provide
1. **ADR updates**: Show diffs or key additions
2. **Checklist created**: `ls -la` showing file exists
3. **Cross-references**: All links verified working
4. **Completion matrix**: 6/6 = 100%

### Your Handoff Format
```
## MUX-404 Phase Z Completion Report
**Status**: Complete/Partial/Blocked

**ADR Updates**:
- ADR-045: [what was added]
- ADR-055: [what was added]

**Onboarding Checklist**: Created at [path]

**Completion Matrix**:
| Component | Status | Evidence |
|-----------|--------|----------|
| Grammar compliance audit | ✅ | [path] |
| Application patterns (5+) | ✅ | [path] |
| Transformation guide | ✅ | [path] |
| Worked example | ✅ | [included in guide] |
| Onboarding checklist | ✅ | [path] |
| ADR updates | ✅ | [paths] |

**6/6 = 100% COMPLETE**

**Files Modified/Created**:
- [list with line counts]

**Ready for PM Closure**: Yes

**Blockers** (if any):
- [description]
```

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

```bash
# Verify Phase 1 complete
ls -la docs/internal/architecture/current/grammar-compliance-audit.md
# Expected: File exists

# Verify Phase 2 complete
ls docs/internal/architecture/current/patterns/pattern-04*.md 2>/dev/null | wc -l
# Expected: 5+

# Verify Phase 3 complete
ls -la docs/internal/development/grammar-transformation-guide.md
# Expected: File exists

# Verify ADR locations
ls -la docs/internal/architecture/current/adrs/adr-045-*.md
ls -la docs/internal/architecture/current/adrs/adr-055-*.md
# Expected: Both exist

# Verify MUX docs
ls -la docs/internal/development/mux-*.md
# Expected: implementation-guide, experience-tests
```

**If ANY verification fails**: STOP and report with evidence.

---

## Mission

**Phase Z**: Complete integration, cross-references, and onboarding documentation

**Scope Boundaries**:
- This prompt covers ONLY: ADR updates, onboarding checklist, final integration
- NOT in scope: Creating new patterns or guide content
- This is the FINAL phase

---

## Context

- **GitHub Issue**: #404 MUX-VISION-GRAMMAR-CORE
- **Current State**: All content phases complete (0-3)
- **Target State**: Fully integrated documentation, ready for PM closure
- **Dependencies**: Phases 0-3 complete
- **Infrastructure Verified**: Yes

---

## Session Log Management

**IMPORTANT**: Check for existing log before creating new one!

```bash
# Check if log exists today
ls -la dev/2026/01/20/*-prog-code-*-log.md

# If log exists: APPEND to it, don't create new
```

---

## Implementation Approach

### Step Z.1: Update ADR-045

Read current ADR-045:
```bash
cat docs/internal/architecture/current/adrs/adr-045-*.md
```

Add section (or update existing):
```markdown
## Implementation References

### MUX Infrastructure (#399)
- Protocols: `services/mux/protocols.py`
- Lenses: `services/mux/lenses/`
- Ownership: `services/mux/ownership.py`
- Lifecycle: `services/mux/lifecycle.py`
- Metadata: `services/mux/metadata.py`

### Grammar Application (#404)
- Grammar Compliance Audit: `docs/internal/architecture/current/grammar-compliance-audit.md`
- Application Patterns: `docs/internal/architecture/current/patterns/grammar-application-patterns.md`
- Transformation Guide: `docs/internal/development/grammar-transformation-guide.md`
- Implementation Guide: `docs/internal/development/mux-implementation-guide.md`
- Experience Tests: `docs/internal/development/mux-experience-tests.md`

### Anti-Flattening Tests
- Location: `tests/unit/services/mux/test_anti_flattening.py`
- Tests: 40 tests verifying consciousness preservation
```

### Step Z.2: Update ADR-055

Read current ADR-055:
```bash
cat docs/internal/architecture/current/adrs/adr-055-*.md
```

Add/update references to patterns:
```markdown
## Application Patterns

The following patterns were extracted from Morning Standup for general use:

1. **Context Dataclass Pair** - Input/output separation
2. **Parallel Place Gathering** - Multi-source data collection
3. **Personality Bridge** - Data to narrative transformation
4. **Warmth Calibration** - Tone adjustment
5. **Honest Failure** - Graceful degradation

See: `docs/internal/architecture/current/patterns/grammar-application-patterns.md`

## Developer Resources

- **Getting Started**: `docs/internal/development/grammar-onboarding-checklist.md`
- **Transformation Guide**: `docs/internal/development/grammar-transformation-guide.md`
- **Pattern Catalog**: `docs/internal/architecture/current/patterns/`
```

### Step Z.3: Create Developer Onboarding Checklist

Create `docs/internal/development/grammar-onboarding-checklist.md`:

```markdown
# Grammar Onboarding Checklist

## For Developers New to MUX Grammar

This checklist helps you get up to speed with applying "Entities experience Moments in Places" to Piper features.

---

## Required Reading (In Order)

### 1. Understand the Vision
- [ ] Read ADR-045: Object Model (`docs/internal/architecture/current/adrs/adr-045-object-model.md`)
- [ ] Understand the grammar: "Entities experience Moments in Places"

### 2. Understand the Implementation
- [ ] Read MUX Implementation Guide (`docs/internal/development/mux-implementation-guide.md`)
- [ ] Review the 3 Protocols: Entity, Moment, Place
- [ ] Review the 8 Lenses: Temporal, Priority, Collaborative, Flow, Hierarchy, Quantitative, Causal, Contextual

### 3. Study the Reference
- [ ] Read Morning Standup implementation (`services/features/morning_standup.py`)
- [ ] Identify how it uses grammar elements

### 4. Learn the Patterns
- [ ] Read Grammar Application Patterns (`docs/internal/architecture/current/patterns/grammar-application-patterns.md`)
- [ ] Understand the 5 patterns from Morning Standup

### 5. Learn to Transform
- [ ] Read Transformation Guide (`docs/internal/development/grammar-transformation-guide.md`)
- [ ] Study the worked example
- [ ] Review anti-patterns

---

## First Task Suggestions

After completing the reading, try one of these:

### Easy: Add Grammar Language to Existing Response
- Find a response that says "Found X results"
- Transform to "I notice X things that..."
- No code changes, just language

### Medium: Apply One Pattern
- Find a feature in the grammar audit marked "Partial"
- Apply the Personality Bridge pattern
- Test with experience language check

### Harder: Transform a Flattened Feature
- Choose from the transformation priorities in the audit
- Apply full grammar transformation
- Verify with anti-flattening mindset

---

## Verification

Before considering yourself onboarded:
- [ ] Can you explain Entity/Moment/Place in your own words?
- [ ] Can you identify which lens applies to a given query?
- [ ] Can you spot "flattened" language and fix it?
- [ ] Do you understand why we compost rather than delete?

---

## Quick Reference

| If You Need To... | Look At... |
|-------------------|------------|
| Understand the philosophy | ADR-045 |
| Use protocols/lenses | MUX Implementation Guide |
| Apply patterns | Grammar Application Patterns |
| Transform a feature | Transformation Guide |
| Check compliance | Grammar Compliance Audit |
| Write experience tests | Experience Tests doc |

---

## Getting Help

- **Architecture questions**: Check ADRs first, then ask
- **Pattern questions**: Check catalog, look at Morning Standup
- **Stuck on transformation**: Follow the decision tree in the guide

---

## Related Documentation
- ADR-045: Object Model
- ADR-055: Implementation
- MUX Implementation Guide
- Experience Tests
- Grammar Compliance Audit
- Grammar Application Patterns
- Transformation Guide
```

### Step Z.4: Verify All Cross-References

```bash
# Check all links in documents exist
grep -r "docs/internal" docs/internal/development/grammar-*.md | while read line; do
  path=$(echo "$line" | grep -oP 'docs/internal[^\)]+')
  if [ -f "$path" ]; then
    echo "✅ $path"
  else
    echo "❌ MISSING: $path"
  fi
done
```

### Step Z.5: Update Completion Matrix

Verify all 6 deliverables:

| Component | Status | Evidence |
|-----------|--------|----------|
| Grammar compliance audit | ? | `docs/internal/architecture/current/grammar-compliance-audit.md` |
| Application patterns (5+) | ? | `docs/internal/architecture/current/patterns/grammar-application-patterns.md` |
| Transformation guide | ? | `docs/internal/development/grammar-transformation-guide.md` |
| Worked example | ? | Included in transformation guide |
| Onboarding checklist | ? | `docs/internal/development/grammar-onboarding-checklist.md` |
| ADR updates | ? | ADR-045, ADR-055 |

---

## Success Criteria

- [ ] Infrastructure verified (Phases 0-3 complete)
- [ ] ADR-045 updated with implementation references
- [ ] ADR-055 updated with pattern links
- [ ] Onboarding checklist created
- [ ] All cross-references verified
- [ ] Completion matrix shows 6/6 = 100%
- [ ] Ready for PM closure

---

## STOP Conditions

Stop and escalate if:
- Any Phase 0-3 deliverable missing
- ADR files not found or can't be updated
- Cross-references broken and unfixable

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Did I verify all Phases 0-3 are complete?
2. Did I update ADR-045 with references?
3. Did I update ADR-055 with pattern links?
4. Did I create the onboarding checklist?
5. Are all cross-references working?
6. Is the completion matrix 6/6 = 100%?
7. Is issue #404 ready for PM closure?
8. Did I provide handoff in the required format?

---

## Deliverables

1. **Session log**: Append to existing
2. **ADR-045**: Updated with implementation references
3. **ADR-055**: Updated with pattern links
4. **Onboarding checklist**: `docs/internal/development/grammar-onboarding-checklist.md`
5. **Final handoff report**: Completion status with 6/6 matrix

---

## Final Note

This is the completion phase. After this:
- Issue #404 should be ready for PM review and closure
- All documentation should be interconnected
- New developers should have a clear path to learn the grammar

**Remember**: PM closes issues after approval. Provide evidence, request review.

---

*Prompt Version: Based on template v10.2*
*Created: 2026-01-20*
*Issue: #404 Phase Z*
