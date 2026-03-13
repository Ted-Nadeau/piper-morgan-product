# Agent Prompt: MUX-404 Phase 3 (Transformation Guide & Worked Example)

## Your Identity
You are Claude Code (Sonnet), a development agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #404 MUX-VISION-GRAMMAR-CORE
- **Epic**: #399 complete (302 MUX tests)
- **Gameplan**: `dev/2026/01/20/gameplan-mux-404.md`
- **Prerequisite**: Phases 0-2 complete (audit + patterns)

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase 3 of issue #404. Your work enables Phase Z (Integration).

### Your Acceptance Criteria
- [ ] Step-by-step transformation guide created
- [ ] Worked example with before/after comparison
- [ ] Protocol/Lens usage demonstrated
- [ ] Anti-patterns documented
- [ ] Guide enables independent developer work
- [ ] Document at `docs/internal/development/grammar-transformation-guide.md`

### Evidence You MUST Provide
1. **Guide created**: `ls -la` showing file exists
2. **Content complete**: All sections present
3. **Worked example**: Clear before/after with code
4. **Word/section count**: Approximate content size

### Your Handoff Format
```
## MUX-404 P3 Completion Report
**Status**: Complete/Partial/Blocked

**Guide Sections**:
1. Identifying Grammar Elements - ✅
2. Refactoring Flattened Code - ✅
3. Using Protocols and Lenses - ✅
4. Anti-patterns and Fixes - ✅
5. Decision Tree - ✅
6. Worked Example - ✅

**Files Created**:
- docs/internal/development/grammar-transformation-guide.md (+X lines)

**Worked Example**:
- Feature transformed: [name]
- Before: [brief description]
- After: [brief description]

**Verification**:
$ ls -la docs/internal/development/grammar-transformation-guide.md
[output]

**Blockers** (if any):
- [description]
```

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

```bash
# Verify Phase 1 complete (grammar audit)
ls -la docs/internal/architecture/current/grammar-compliance-audit.md
# Expected: File exists

# Verify Phase 2 complete (patterns)
ls -la docs/internal/architecture/current/patterns/grammar-application-patterns.md
# Expected: File exists

# Count patterns created
ls docs/internal/architecture/current/patterns/pattern-04*.md 2>/dev/null | wc -l
# Expected: 5+

# Verify MUX implementation guide exists (reference)
ls -la docs/internal/development/mux-implementation-guide.md
# Expected: File exists

# Verify intent service exists (for worked example)
ls -la services/intent/intent_service.py
# Expected: File exists
```

**If ANY verification fails**: STOP and report with evidence.

---

## Mission

**Phase 3**: Create transformation guide enabling developers to apply grammar independently, with a complete worked example

**Scope Boundaries**:
- This prompt covers ONLY: Transformation guide and worked example
- NOT in scope: Pattern extraction (Phase 2), ADR updates (Phase Z)
- Separate prompts handle: Phases 0-2, Z

---

## Context

- **GitHub Issue**: #404 MUX-VISION-GRAMMAR-CORE
- **Current State**: Patterns documented, no transformation guide
- **Target State**: Complete guide enabling independent grammar application
- **Dependencies**: Phases 0-2 complete
- **Infrastructure Verified**: Yes

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

### Step 3.0: Review Prerequisites

```bash
# Read grammar compliance audit (transformation priorities)
cat docs/internal/architecture/current/grammar-compliance-audit.md

# Read pattern catalog
cat docs/internal/architecture/current/patterns/grammar-application-patterns.md

# Read MUX implementation guide (reference)
cat docs/internal/development/mux-implementation-guide.md

# Read experience tests (what to aim for)
cat docs/internal/development/mux-experience-tests.md
```

### Step 3.1: Create Transformation Guide Structure

Create `docs/internal/development/grammar-transformation-guide.md`:

```markdown
# Grammar Transformation Guide

## Purpose
Step-by-step guide for transforming flattened features to express the MUX grammar:
"Entities experience Moments in Places"

## Prerequisites
- Read: MUX Implementation Guide (`docs/internal/development/mux-implementation-guide.md`)
- Read: Grammar Application Patterns (`docs/internal/architecture/current/patterns/grammar-application-patterns.md`)
- Understand: The 3 substrates (Entity, Moment, Place) and 8 Lenses

---

## Part 1: Identifying Grammar Elements

### Step 1: Find the Entities
Questions to ask:
- Who are the actors? (User, Piper, team members, integrations)
- What has identity that persists?
- What can have agency (take action)?

**Checklist**:
- [ ] User identified and tracked by identity (not just session)
- [ ] Piper is present as an entity (not just a function)
- [ ] Other actors named (not just IDs)

### Step 2: Find the Moments
Questions to ask:
- What bounded occurrences happen?
- What has significance beyond a timestamp?
- What has a beginning, middle, end?

**Checklist**:
- [ ] Events have descriptions (not just timestamps)
- [ ] Temporal language used (today, yesterday, upcoming)
- [ ] Moments have significance framing

### Step 3: Find the Places
Questions to ask:
- Where do interactions occur?
- What contexts have atmosphere?
- How does location affect presentation?

**Checklist**:
- [ ] Places named with character (not just config strings)
- [ ] Atmosphere affects how data is presented
- [ ] Place modality acknowledged (chat, calendar, repo)

### Step 4: Frame the Situation
Questions to ask:
- What's the dramatic tension?
- What wants to happen?
- What learning is extracted?

---

## Part 2: Refactoring Flattened Code

### The Transformation Process

1. **Identify flattening** - Where is mechanical language used?
2. **Map to grammar** - Which elements apply?
3. **Apply patterns** - Which patterns from the catalog?
4. **Verify consciousness** - Does it pass experience tests?

### Example Transformations

#### Before (Flattened):
```python
def get_tasks():
    tasks = db.query(Task).filter(due_date=today).all()
    return {"tasks": [t.to_dict() for t in tasks]}
```

#### After (Grammar-Applied):
```python
def perceive_todays_moments(user: Entity) -> Perception:
    """
    User experiences today's task Moments through Temporal lens.
    """
    with Situation(
        entities=[user, piper],
        tension="What needs attention today?"
    ) as situation:
        # Gather Moments from Place
        tasks = gather_from_place(
            place=workspace,
            lens=TemporalLens(mode=PerceptionMode.NOTICING)
        )

        # Frame with consciousness
        return Perception(
            framing="I notice you have {} things that want attention today".format(len(tasks)),
            moments=tasks,
            situation=situation
        )
```

---

## Part 3: Using Protocols and Lenses

### When to Use Each Protocol

| Protocol | Use When | Example |
|----------|----------|---------|
| EntityProtocol | Tracking actors | User, Piper, teammates |
| MomentProtocol | Bounded occurrences | Meetings, commits, messages |
| PlaceProtocol | Contexts with atmosphere | GitHub, Slack, Calendar |

### When to Use Each Lens

| Lens | Use When | Question Answered |
|------|----------|-------------------|
| Temporal | Time-based queries | "What's happening today?" |
| Priority | Importance filtering | "What matters most?" |
| Collaborative | People-based | "Who's involved?" |
| Flow | Progress tracking | "What's blocked?" |
| Hierarchy | Structure navigation | "What does this belong to?" |
| Quantitative | Metrics queries | "How much work?" |
| Causal | Cause-effect | "Why did this happen?" |
| Contextual | Background | "What's the context?" |

### PerceptionMode

- **NOTICING**: Present awareness ("I notice...")
- **REMEMBERING**: Past reference ("I remember...")
- **ANTICIPATING**: Future awareness ("I anticipate...")

---

## Part 4: Anti-Patterns and Fixes

### Anti-Pattern 1: Query Language in Responses
❌ "Query returned 3 results"
✅ "I notice 3 things that need your attention"

### Anti-Pattern 2: Timestamps Without Context
❌ "Created: 2026-01-20 14:30:00"
✅ "From earlier today, when you were working on the API"

### Anti-Pattern 3: IDs Instead of Names
❌ "User 123 commented"
✅ "Alex commented on your PR"

### Anti-Pattern 4: Config Strings as Places
❌ "Source: github.com/repo/123"
✅ "Over in GitHub, in the piper-morgan repository"

### Anti-Pattern 5: Mechanical Error Messages
❌ "Error: Connection timeout"
✅ "I couldn't reach GitHub just now, but here's what I remember from earlier"

---

## Part 5: Decision Tree

```
Start: New feature or transformation?
│
├─ Is there user-facing output?
│  ├─ Yes → Apply Personality Bridge pattern
│  └─ No → Focus on Entity/Moment/Place identification
│
├─ Does it gather from multiple sources?
│  ├─ Yes → Apply Parallel Place Gathering pattern
│  └─ No → Single-place interaction
│
├─ What's the primary lens?
│  ├─ Time-related → Temporal lens
│  ├─ Priority-related → Priority lens
│  ├─ People-related → Collaborative lens
│  └─ Progress-related → Flow lens
│
└─ Can it fail gracefully?
   ├─ Yes → Apply Honest Failure pattern
   └─ No → Ensure hard failures are rare
```

---

## Part 6: Worked Example

[WORKED EXAMPLE GOES HERE - See Step 3.2]

---

## Verification Checklist

Before declaring transformation complete:
- [ ] All entities identified and tracked
- [ ] Moments have significance (not just timestamps)
- [ ] Places have atmosphere (not just config)
- [ ] At least one lens applied
- [ ] Situation frames the interaction
- [ ] Language passes experience test ("Piper noticed..." not "Query returned...")
- [ ] Error handling uses Honest Failure pattern

---

## Related Documentation
- MUX Implementation Guide: `docs/internal/development/mux-implementation-guide.md`
- Experience Tests: `docs/internal/development/mux-experience-tests.md`
- Grammar Application Patterns: `docs/internal/architecture/current/patterns/grammar-application-patterns.md`
- Grammar Compliance Audit: `docs/internal/architecture/current/grammar-compliance-audit.md`
```

### Step 3.2: Create Worked Example

Choose a feature from the grammar audit that's marked as "flattened" (suggestion: intent classification responses).

**Document in the guide**:

1. **Current (flattened) state**
   - Read the actual code
   - Show specific flattened patterns
   - Note mechanical language

2. **Grammar analysis**
   - Entities: User, Piper
   - Moments: The query, the classification, the response
   - Places: The channel/interface
   - Lenses: Depends on intent type

3. **Transformed design**
   - Show how to apply grammar
   - Use patterns from catalog
   - Include actual code changes (or pseudocode)

4. **Before/After comparison**
   - Response examples
   - Clear improvement visible

5. **Lessons learned**
   - What was harder than expected
   - Reusable insights

---

## Success Criteria

- [ ] Infrastructure verified (Phases 0-2 complete)
- [ ] Guide has all 6 parts
- [ ] Worked example is complete with before/after
- [ ] Anti-patterns documented with fixes
- [ ] Decision tree is usable
- [ ] File exists at correct path
- [ ] A developer could follow without asking questions

---

## STOP Conditions

Stop and escalate if:
- Phases 0-2 not complete
- Intent classification transformation proves infeasible
- Guide becomes too abstract (no practical examples)
- Can't find good flattened feature for worked example

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Did I verify Phases 0-2 are complete?
2. Does the guide have all 6 parts?
3. Is the worked example complete with before/after?
4. Are anti-patterns documented with fixes?
5. Could a new developer follow this independently?
6. Can I show `ls -la` evidence the file exists?
7. Did I provide handoff in the required format?

---

## Deliverables

1. **Session log**: Append to existing or create new
2. **Transformation guide**: `docs/internal/development/grammar-transformation-guide.md`
3. **Handoff report**: Completion status with evidence

---

*Prompt Version: Based on template v10.2*
*Created: 2026-01-20*
*Issue: #404 Phase 3*
