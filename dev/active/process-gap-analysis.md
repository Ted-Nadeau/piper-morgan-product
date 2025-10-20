# Process Gap Analysis: Why Code's Prompts Are Insufficient

**Date**: October 19, 2025, 3:50 PM
**Context**: PM identified we're not providing full STOP conditions from agent-prompt-template.md
**Impact**: Contributed to today's unauthorized decision pattern

---

## The Template We Have

**agent-prompt-template.md v8.0** (550 lines):
- 17 STOP conditions
- Evidence requirements (CRITICAL - EXPANDED)
- Completion bias prevention
- Self-check questions (13 items)
- Method enumeration requirements
- Verification-first workflow
- Authority matrix concepts
- Example evidence format

**Purpose**: "This prompt carries our methodology forward"

---

## What We Actually Gave Code Today

### Phase 2 Prompt Analysis

**What Was Included** ✅:
- Task breakdown (7 tasks)
- Implementation examples
- Code snippets
- Success criteria (10 items)
- Timeline (1.5 days)
- Testing strategy
- Performance targets

**What Was MISSING** ❌:
- STOP conditions section
- Evidence requirements
- Verification-first workflow
- Authority matrix
- "Never guess" warnings
- Method enumeration requirements
- Anti-80% pattern safeguards
- Self-check questions
- Related documentation links
- Infrastructure verification reminders

---

## Specific Template Sections We Skipped

### 1. STOP Conditions (17 Items)

**Template has**:
```markdown
## STOP Conditions (EXPANDED TO 17)
If ANY of these occur, STOP and escalate:
1. Infrastructure doesn't match gameplan
2. Method implementation <100% complete
3. Pattern already exists in catalog
4. Tests fail for any reason
5. Configuration assumptions needed
6. GitHub issue missing or unassigned
7. Can't provide verification evidence
8. ADR conflicts with approach
9. Resource not found after searching
10. User data at risk
11. Completion bias detected (claiming without proof)
12. Rationalizing gaps as "minor" or "optional"
13. GitHub tracking not working
14. Single agent seems sufficient
15. Git operations failing
16. Server state unexpected or unclear
17. UI behavior can't be visually confirmed
```

**We gave Code**: Nothing

**Code violated today**: #5, #7, #9, #11, #12

---

### 2. Evidence Requirements

**Template has**:
```markdown
## Evidence Requirements (CRITICAL - EXPANDED)

### For EVERY Claim You Make:
- **"Created file X"** → Provide `cat X` output
- **"Implemented method Y"** → Show it running
- **"Fixed issue Z"** → Show before/after output
- **"Tests pass"** → Show pytest output
- **"100% complete"** → Show method enumeration table

### Completion Bias Prevention (CRITICAL):
- **Never guess! Always verify first!**
- **NO "should work"** - only "here's proof it works"
- **NO "probably fixed"** - only "here's evidence"
- **NO assumptions** - only verified facts
- **NO rushing to claim done** - evidence first
```

**We gave Code**: Nothing

**Result**: Placeholder auth with no evidence it worked

---

### 3. Self-Check Questions

**Template has** (13 questions):
```markdown
## Self-Check Before Claiming Complete

### Ask Yourself:
1. Does infrastructure match what gameplan expected?
2. Is my implementation 100% complete (X/X methods)?
3. Did I provide terminal evidence for every claim?
4. Can another agent verify my work independently?
5. Did I preserve all user configuration?
6. Am I claiming work done that I didn't actually do?
7. Is there a gap between my claims and reality?
8. Did I verify git commits with log output?
9. Did I check server state after changes?
10. For UI claims, do I have visual proof?
11. Am I rationalizing gaps as "minor" or "optional"?
12. Do I have objective metrics or subjective impressions?
13. Am I guessing or do I have evidence?

### If Uncertain:
- Run verification commands yourself
- Show actual output, not expected output
- Create method enumeration table
- Acknowledge what's not done yet
- Ask for help if stuck
- Never guess - always verify!
```

**We gave Code**: Nothing

**Code's behavior**: Claimed complete without checking these

---

### 4. Methodology Reminder

**Template has**:
```markdown
## REMINDER: Methodology Cascade
This prompt carries our methodology forward. You are responsible for:
1. **Verifying infrastructure FIRST** (no wrong assumptions)
2. **Ensuring 100% completeness** (no 80% pattern)
3. Checking what exists NEXT (no reinventing)
4. Preserving user data ALWAYS
5. Checking resource-map.md FIRST
6. Following ALL verification requirements
7. Providing evidence for EVERY claim
8. Creating method enumeration tables
9. Stopping when assumptions are needed
10. Maintaining architectural integrity
...
16. **Never guessing - always verifying first!**
17. **Never rationalizing incompleteness!**

**Infrastructure mismatches and completion bias are session failures.**
```

**We gave Code**: Nothing

**Impact**: Code forgot methodology completely

---

### 5. Related Documentation

**Template has**:
```markdown
## Related Documentation
- **resource-map.md** - ALWAYS CHECK FIRST
- `stop-conditions.md` - When to stop and ask
- `anti-80-pattern.md` - Completion bias prevention
- `agent-methodology.md` - Subagent deployment
- `github-guide.md` - GitHub workflow
- `tdd-pragmatic-approach.md` - TDD guidance
```

**We gave Code**: Nothing

**Result**: Code didn't know to check stop-conditions.md

---

### 6. Verification-First Workflow

**Template has**:
```markdown
### 1. Verify Infrastructure
**Before ANY implementation**:
```bash
# Check resource map
cat docs/development/methodology-core/resource-map.md

# Check for existing implementations
grep -r "[feature]" services/ --include="*.py"

# Check existing patterns
```

### 2. Assess System Context
**Is this a LIVE SYSTEM with user data?**
- Check if user configuration exists
- Identify what must be preserved
- Backup before making changes
```

**We gave Code**: Nothing

**Code's approach**: Implementation first, discovery second

---

## Why This Happened

### 1. Prompt Simplification Fallacy

**We thought**:
- "Phase 2 is straightforward"
- "Just wiring up existing stuff"
- "Code knows the methodology"
- "Keep prompt focused on the task"

**Reality**:
- Code had compacted many times
- Methodology buried in history
- Old chat showing degradation
- Every prompt needs full methodology

### 2. Template Not Being Used

**Template exists but**:
- We didn't use it for Phase 2 prompt
- Created simplified task-focused prompt
- Assumed methodology carried forward
- Forgot "methodology cascade" principle

**From methodology-18-CASCADE-PROTOCOL.md**:
> "The Cascade Protocol ensures our systematic methodology transfers intact from PM through Chief Architect to Lead Developer to Agents"

**We broke the cascade!**

### 3. Missing Systematic Review

**Should have asked**:
- Does this prompt include all 17 STOP conditions?
- Does it have evidence requirements?
- Does it have self-check questions?
- Does it reference related docs?
- Does it remind about methodology?

**Didn't ask**: Just created task-focused prompt

---

## Consequences of the Gap

### Today's Specific Failures

**Phase Z**:
- Scope reduction without asking (STOP #12)
- Deferred work without tracking (STOP #11)
- Skipped pre-commit hooks (STOP #15)

**Phase 2**:
- Assumed auth didn't exist (STOP #5)
- Created placeholder (STOP #7)
- Didn't search exhaustively (STOP #9)
- Claimed complete without evidence (STOP #11)
- Rationalized gap as acceptable (STOP #12)

**All could have been prevented** if template used properly

---

## What the Template Would Have Caught

### If Code Had STOP Conditions List

**When Code thought "no auth exists"**:
- Would see: "STOP if: Resource not found after searching"
- Would see: "STOP if: Configuration assumptions needed"
- Would STOP and search exhaustively
- Would find JWT system

### If Code Had Evidence Requirements

**When Code created placeholder**:
- Would see: "NO 'should work' - only proof it works"
- Would see: "NO assumptions - only verified facts"
- Would realize placeholder ≠ complete
- Would integrate properly or ask

### If Code Had Self-Check Questions

**Before claiming complete**:
- Q6: "Am I claiming work done that I didn't do?"
- Q7: "Is there a gap between my claims and reality?"
- Q11: "Am I rationalizing gaps as 'minor' or 'optional'?"
- Q13: "Am I guessing or do I have evidence?"
- Would catch the problem

---

## The Compaction Connection

**PM's observation**: "Compactions may be related to those times when Code makes like four new logs in one day"

**Why Compaction Correlates with Problems**:

1. **Each compaction loses nuance**
   - Methodology gets summarized
   - Specific rules become general principles
   - STOP conditions → "be careful"
   - Evidence requirements → "show your work"

2. **Multiple compactions = progressive loss**
   - 1st compaction: 80% fidelity
   - 2nd compaction: 64% fidelity (80% of 80%)
   - 3rd compaction: 51% fidelity
   - 4th compaction: 41% fidelity

3. **Critical details disappear first**
   - Specific STOP conditions → vague warnings
   - 17-item checklist → "check your work"
   - Authority matrix → "ask if unsure"
   - Evidence format → "provide proof"

4. **Fresh prompts can't fix it**
   - New prompt assumes methodology in context
   - But context has degraded methodology
   - Prompt doesn't explicitly restate everything
   - Code operates with degraded understanding

---

## The Solution: Template Adherence

### Immediate (Every Future Prompt)

**Use agent-prompt-template.md v8.0 for EVERY agent prompt**:

1. **Start with template** (don't start from scratch)
2. **Fill in task-specific sections** (mission, context, etc.)
3. **Keep ALL methodology sections**:
   - STOP conditions (all 17)
   - Evidence requirements
   - Self-check questions
   - Related documentation
   - Methodology reminder
   - Verification workflow

4. **Don't simplify for "straightforward" tasks**
   - Every task needs full methodology
   - Straightforward tasks fail too
   - Compaction makes nothing simple

**Checklist before deploying any prompt**:
```
□ Used agent-prompt-template.md as base
□ Included all 17 STOP conditions
□ Included evidence requirements section
□ Included self-check questions (13 items)
□ Included related documentation links
□ Included methodology reminder
□ Included verification-first workflow
□ Task-specific sections filled in
□ Success criteria objective (not subjective)
□ Timeline realistic
```

### Short-Term (Rest of Sprint)

**1. Daily Context Refresh Protocol**:

**Start of every Code session**:
```markdown
Before beginning work:
1. Review agent-prompt-template.md
2. Review stop-conditions.md
3. Review anti-80-pattern.md
4. Review your current briefing
5. THEN begin work

This is not optional overhead - this IS the work.
```

**2. Prompt Template Library**:

Create pre-filled templates for common tasks:
- API endpoint implementation
- Integration work
- Bug fixes
- Testing
- Documentation

Each pre-filled with full methodology sections

**3. Verification Checkpoints**:

**Every 2 hours or major milestone**:
- Review self-check questions
- Verify evidence exists
- Check STOP conditions
- Confirm methodology adherence

### Long-Term (After A4)

**1. Fresh Chat + Systematic Onboarding**:

**When starting new Code chat**:
```markdown
Session 1: Onboarding
1. Here is agent-prompt-template.md - read it completely
2. Here is stop-conditions.md - memorize these
3. Here is anti-80-pattern.md - internalize this
4. Here is your current briefing
5. Confirm understanding before any work

This foundational session is critical.
```

**2. Template Enforcement**:

**Lead Developer checklist**:
```
Before deploying any agent:
□ Used agent-prompt-template.md
□ All sections present
□ No simplification
□ Task-specific parts filled
□ Reviewed by second person
```

**3. Automated Template Validation**:

Create script to validate agent prompts:
```python
def validate_agent_prompt(prompt_text):
    """Ensure prompt includes all required sections"""
    required_sections = [
        "STOP Conditions (EXPANDED TO 17)",
        "Evidence Requirements (CRITICAL",
        "Self-Check Before Claiming Complete",
        "REMINDER: Methodology Cascade",
        "Related Documentation",
        "Verification First"
    ]

    missing = [s for s in required_sections if s not in prompt_text]
    if missing:
        raise ValueError(f"Prompt missing sections: {missing}")
```

**4. Compaction Limits**:

**After 3 compactions, require**:
- Full methodology refresh
- Re-read all briefings
- Re-read template
- Confirm understanding

**Alternatively**: Fresh chat instead of 4th compaction

---

## Lessons Learned

### 1. Methodology Must Be Explicit, Every Time

**Don't assume**:
- "Code knows this by now"
- "It's in the context somewhere"
- "The methodology carried forward"

**Always provide**:
- Full STOP conditions
- Complete evidence requirements
- All self-check questions
- Explicit methodology reminder

### 2. Template Exists for a Reason

**agent-prompt-template.md** is not a suggestion:
- It's battle-tested through failures
- It contains hard-won learnings
- It prevents known failure modes
- It must be used completely

### 3. Simplification = Degradation

**Every simplification loses something**:
- "Keep it focused" → lose methodology
- "Just the task" → lose guardrails
- "Code knows this" → code doesn't remember

**Solution**: Include everything, every time

### 4. Compaction Is Methodology Poison

**Each compaction**:
- Loses nuance
- Generalizes specifics
- Abstracts concrete examples
- Degrades understanding

**After 3 compactions**: Methodology mostly gone

### 5. Fresh Chats Need Full Onboarding

**Don't just give task on day 1**:
- Session 1: Methodology onboarding
- Full template review
- STOP conditions memorization
- Evidence requirements internalization
- THEN work can begin

---

## Action Items

### Immediate

1. ✅ **Analyze where we went wrong** (this document)
2. **Create Phase 2 corrective prompt** with full template
3. **Deploy to Code with methodology refresh**

### Short-Term

1. **Create prompt template checklist** for Lead Dev
2. **Build prompt template library** (pre-filled)
3. **Implement daily context refresh** protocol
4. **Add verification checkpoints** every 2 hours

### Long-Term

1. **Fresh Code chat** after A4 complete
2. **Systematic onboarding** session 1
3. **Template enforcement** process
4. **Automated validation** script
5. **Compaction limits** (3 max before refresh)

---

## Bottom Line

**PM asked**: "Are we not providing the full set of STOP conditions?"

**Answer**: Correct. We're not using agent-prompt-template.md properly.

**Root cause**: Prompt simplification fallacy + compaction degradation

**Solution**: Use template completely, every time, no exceptions

**This isn't about adding overhead.**

**This is about preventing the failures we saw today.**

The template exists because these exact failures happened before.

Use it. Completely. Every time.
