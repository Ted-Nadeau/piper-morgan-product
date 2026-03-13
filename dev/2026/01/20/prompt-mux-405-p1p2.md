# Agent Prompt: MUX-405 Phases 1-2 (Philosophy Document)

## Your Identity
You are Claude Code (Sonnet), a development agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #405 MUX-VISION-METAPHORS
- **Epic**: MUX-VISION (#401)
- **Gameplan**: `dev/2026/01/20/gameplan-mux-405.md`
- **Prerequisite**: Phase 0 complete (source materials gathered)

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. STOP - Do not continue working
2. REPORT - Summarize what was just completed
3. ASK - "Should I proceed to next task?"
4. WAIT - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phases 1-2 of issue #405. Your work creates the ownership metaphor philosophy document.

### Your Acceptance Criteria
- [ ] Philosophy document at `docs/internal/architecture/current/ownership-metaphors.md`
- [ ] WHY section explains choice of Mind/Senses/Understanding
- [ ] Decision tree for ownership classification
- [ ] At least 3 worked examples with reasoning
- [ ] Common mistakes section
- [ ] Edge cases section

### Evidence You MUST Provide
1. **Document created**: `ls -la` showing file exists
2. **Content complete**: All sections present
3. **Word count**: Approximate content size
4. **Example count**: At least 3 worked examples

### Your Handoff Format
```
## MUX-405 P1-P2 Completion Report
**Status**: Complete/Partial/Blocked

**Philosophy Document Created**: docs/internal/architecture/current/ownership-metaphors.md

**Sections**:
1. Introduction - ✅
2. Why These Metaphors (Mind/Senses/Understanding) - ✅
3. The Three Relationships - ✅
4. Decision Tree - ✅
5. Worked Examples - ✅ (count: X)
6. Common Mistakes - ✅
7. Edge Cases - ✅

**Word Count**: ~X words

**Verification**:
$ ls -la docs/internal/architecture/current/ownership-metaphors.md
[output]

**Blockers** (if any):
- [description]
```

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

```bash
# Verify Phase 0 complete (check session log for P0 handoff)
ls -la dev/2026/01/20/*-lead-code-opus-log.md
grep -A 30 "Phase 0" dev/2026/01/20/*-lead-code-opus-log.md

# Verify ownership code exists (for reference)
ls -la services/mux/ownership.py

# Verify consciousness philosophy exists (to avoid duplication)
ls -la docs/internal/architecture/current/consciousness-philosophy.md

# Verify ADRs exist (will cross-reference)
ls -la docs/internal/architecture/current/adrs/adr-045-*.md
ls -la docs/internal/architecture/current/adrs/adr-055-*.md
```

**If ANY verification fails**: STOP and report with evidence.

---

## Mission

**Phases 1-2**: Create the ownership metaphor philosophy document

**Scope Boundaries**:
- This prompt covers ONLY: Philosophy document creation (WHY + Decision Guide + Examples)
- NOT in scope: Code changes (ownership code already complete)
- NOT in scope: Cross-reference updates (Phase Z)
- NOT in scope: Consciousness pillars (covered in #400)
- Separate prompts handle: Phase 0 (gathering), Phase Z (integration)

---

## Context

- **GitHub Issue**: #405 MUX-VISION-METAPHORS
- **Current State**: Phase 0 complete, source materials gathered
- **Target State**: Complete philosophy document with decision guide
- **Dependencies**: Phase 0 complete, #400 consciousness-philosophy.md exists
- **Infrastructure Verified**: Yes

---

## Session Log Management

**IMPORTANT**: Check for existing log before creating new one!

```bash
# Check if log exists today
ls -la dev/2026/01/20/*-lead-code-opus-log.md

# If log exists: APPEND to it, don't create new
```

---

## Implementation Approach

### Step 1.1: Create Document Structure

Create `docs/internal/architecture/current/ownership-metaphors.md`:

```markdown
# Ownership Metaphors: Mind, Senses, Understanding

## Introduction

[Why this document exists. Connection to consciousness philosophy.]

---

## Part 1: Why These Metaphors?

### The Question
Why "Mind" instead of "Memory"? Why "Senses" instead of "Inputs"? Why "Understanding" instead of "Inference"?

### The Answer
[Explain the embodied cognition principle - Piper isn't a database, Piper is an entity with cognitive faculties]

### Alternative Names We Rejected
| Rejected | Chosen | Why |
|----------|--------|-----|
| Memory/Storage | Mind | Mind implies agency, not just storage |
| Inputs/Feeds | Senses | Senses implies perception, not just data flow |
| Inference/Calculation | Understanding | Understanding implies wisdom, not just computation |

---

## Part 2: The Three Relationships

### Native (Piper's Mind)
**What it is**: Information Piper creates, owns, and maintains
**The metaphor**: Like your own thoughts - you created them, you can change them, you trust them completely
**Confidence**: Always 1.0 (Piper is certain about what it creates)

**Examples**:
- Sessions Piper creates
- Memories Piper forms
- Concerns Piper develops
- Trust states Piper maintains

**Experience language**: "I know this because I created it"

---

### Federated (Piper's Senses)
**What it is**: Information Piper observes from external sources
**The metaphor**: Like your eyes and ears - you perceive the world, but you don't control it
**Confidence**: Variable (external sources may be stale or incomplete)

**Examples**:
- GitHub issues (observed, not created)
- Slack messages (received, not sent)
- Calendar events (scheduled externally)

**Experience language**: "I sense this from [source]"

**Key characteristic**: `can_modify=False` - Piper can observe but not change the external truth

---

### Synthetic (Piper's Understanding)
**What it is**: Information Piper constructs through reasoning
**The metaphor**: Like your conclusions and insights - derived from what you know
**Confidence**: Variable (depends on reasoning quality and source confidence)

**Examples**:
- Inferred risks (constructed from patterns)
- Assembled projects (synthesized from multiple sources)
- Priority recommendations (derived from context)

**Experience language**: "I understand this because [reasoning]"

**Key characteristic**: `derived_from` - Always tracks what sources contributed

---

## Part 3: The Confidence Model

### Why Confidence Matters
Not all knowledge is equally certain. A thought you had is more certain than something you heard, which is more certain than a conclusion you drew.

| Category | Typical Confidence | Why |
|----------|-------------------|-----|
| Native | 1.0 | Piper created it, Piper is certain |
| Federated | 0.7-0.9 | External sources may be stale |
| Synthetic | 0.5-0.8 | Inference has uncertainty |

### Confidence Decay
Federated knowledge ages. A GitHub issue you saw 5 minutes ago is more reliable than one you cached yesterday.

---

## Part 4: Decision Tree

### How to Classify New Information

```
                    Start
                      │
                      ▼
        Did Piper CREATE this information?
                      │
              ┌───────┴───────┐
              │               │
             YES              NO
              │               │
              ▼               ▼
           NATIVE      Did Piper OBSERVE this
        (Piper's Mind)  from an external source?
                              │
                      ┌───────┴───────┐
                      │               │
                     YES              NO
                      │               │
                      ▼               ▼
                 FEDERATED      Did Piper DERIVE this
              (Piper's Senses)  through reasoning?
                                      │
                              ┌───────┴───────┐
                              │               │
                             YES              NO
                              │               │
                              ▼               ▼
                          SYNTHETIC      Error: Unknown
                     (Piper's Understanding)  ownership type
```

### Quick Classification Questions
1. **Can Piper change this at will?** → Native (Mind)
2. **Does this come from an API/external system?** → Federated (Senses)
3. **Did Piper figure this out from other information?** → Synthetic (Understanding)

---

## Part 5: Worked Examples

### Example 1: Session (Native/Mind)

**Entity**: A conversation session between user and Piper

**Classification reasoning**:
- Did Piper CREATE this? YES - Piper initiates and manages sessions
- Can Piper modify it? YES - Piper can update session state
- Source? Internal - no external system involved

**Result**: NATIVE (Piper's Mind)

**Code pattern**:
```python
ownership = OwnershipMetadata(
    category=OwnershipCategory.NATIVE,
    confidence=1.0,
    source="piper-core",
    can_modify=True
)
```

**Experience phrase**: "I created this session when we started talking"

---

### Example 2: GitHub Issue (Federated/Senses)

**Entity**: A GitHub issue retrieved via API

**Classification reasoning**:
- Did Piper CREATE this? NO - User created it in GitHub
- Does Piper OBSERVE this from external source? YES - GitHub API
- Can Piper modify GitHub's truth? NO - Piper can only read

**Result**: FEDERATED (Piper's Senses)

**Code pattern**:
```python
ownership = OwnershipMetadata(
    category=OwnershipCategory.FEDERATED,
    confidence=0.9,  # May be stale
    source="github-api",
    requires_verification=True,
    can_modify=False
)
```

**Experience phrase**: "I see this issue in your GitHub repository"

---

### Example 3: Inferred Project Risk (Synthetic/Understanding)

**Entity**: A risk assessment Piper constructs from multiple signals

**Classification reasoning**:
- Did Piper CREATE this? No - It's derived, not original
- Does Piper OBSERVE this externally? No - No API returns "risk level"
- Did Piper DERIVE this through reasoning? YES

**Result**: SYNTHETIC (Piper's Understanding)

**Code pattern**:
```python
ownership = OwnershipMetadata(
    category=OwnershipCategory.SYNTHETIC,
    confidence=0.7,  # Inference confidence
    source="risk-analysis",
    derived_from=["github-issue-123", "calendar-meeting-456"],
    transformation_chain=["pattern-match", "risk-score"]
)
```

**Experience phrase**: "I sense a risk here based on the stale PR and the approaching deadline"

---

## Part 6: Common Mistakes

### Mistake 1: Treating All External Data as Federated
**Wrong**: Caching a GitHub issue makes it Native
**Right**: The *truth* is still in GitHub; the cache is just a stale observation

### Mistake 2: Confusing Synthetic with Native
**Wrong**: Piper's risk assessment is Native because Piper "created" it
**Right**: Piper derived it from other information; it's Understanding, not Mind

### Mistake 3: Ignoring Confidence
**Wrong**: All information is equally trustworthy
**Right**: Native (1.0) > Federated (0.7-0.9) > Synthetic (0.5-0.8)

### Mistake 4: Forgetting Provenance
**Wrong**: Store only the final answer
**Right**: Store `derived_from` for Synthetic so Piper can explain reasoning

---

## Part 7: Edge Cases

### Edge Case 1: User-Provided Information
**Scenario**: User tells Piper "I'm on vacation next week"
**Analysis**: Piper didn't create this, didn't observe via API, didn't derive it
**Resolution**: FEDERATED from "user-message" - user is an external source

### Edge Case 2: Piper's Memory of a Federated Object
**Scenario**: Piper remembers seeing a GitHub issue yesterday
**Analysis**: The memory is Native (Piper created the memory), but the memory's subject is Federated
**Resolution**: Two objects - Native memory pointing to Federated issue

### Edge Case 3: Enriched External Data
**Scenario**: Piper fetches a GitHub issue, then adds sentiment analysis
**Analysis**: The raw issue is Federated; the sentiment is Synthetic (derived from issue text)
**Resolution**: Composite object with both ownership types tracked

---

## Connection to Consciousness Philosophy

This document explains the ownership metaphors (Mind/Senses/Understanding).
For the broader consciousness philosophy (Five Pillars), see:
`docs/internal/architecture/current/consciousness-philosophy.md`

The two documents complement each other:
- Consciousness Philosophy → WHY Piper has a soul (macro)
- Ownership Metaphors → HOW Piper relates to information (micro)

---

## Related Documentation

- **Consciousness Philosophy**: `docs/internal/architecture/current/consciousness-philosophy.md`
- **Implementation Guide**: `docs/internal/development/mux-implementation-guide.md`
- **ADR-045**: Object Model Vision
- **ADR-055**: Object Model Implementation
- **Code Reference**: `services/mux/ownership.py`

---

*Document created: 2026-01-20*
*Issue: #405 MUX-VISION-METAPHORS*
```

### Step 1.2-1.4: Fill in WHY Section

Review Phase 0 materials and write compelling explanation for metaphor choices.

### Step 2.1-2.4: Create Decision Guide and Examples

Use canonical examples from ADR-045 and ownership.py.

---

## Success Criteria

- [ ] Infrastructure verified (Phase 0 complete)
- [ ] Philosophy document created at correct path
- [ ] WHY section explains metaphor choice
- [ ] Decision tree present
- [ ] At least 3 worked examples
- [ ] Common mistakes documented
- [ ] Edge cases documented
- [ ] No duplication of #400 content

---

## STOP Conditions

Stop and escalate if:
- Phase 0 not complete
- Ownership code doesn't match expected patterns
- Duplicating #400 consciousness philosophy content
- Document becomes too abstract (stay grounded in code)

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Did I verify Phase 0 is complete?
2. Does the document have all 7 parts?
3. Did I explain WHY Mind/Senses/Understanding?
4. Did I create a decision tree?
5. Did I provide at least 3 worked examples?
6. Did I document common mistakes?
7. Did I cover edge cases?
8. Did I avoid duplicating #400 content?
9. Can I show `ls -la` evidence the file exists?
10. Did I provide handoff in the required format?

---

## Deliverables

1. **Session log**: Append to existing
2. **Philosophy document**: `docs/internal/architecture/current/ownership-metaphors.md`
3. **Handoff report**: Completion status with evidence

---

*Prompt Version: Based on template v10.2*
*Created: 2026-01-20*
*Issue: #405 Phases 1-2*
