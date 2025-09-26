# Agent Prompt: Cursor - ADR-032 Documentation Quality Review

**Date**: September 23, 2025, 5:10 PM  
**Agent**: Cursor  
**Task**: Review ADR-032 implementation status documentation for quality and completeness  
**Session Log**: Continue your existing log (`2025-09-23-1624-prog-cursor-log.md`) - update after each phase  
**Cross-Validation Partner**: Claude Code

---

## CURSOR CONTEXT (CRITICAL)

1. **Read CLAUDE.md** for methodology requirements
2. **Check ADR structure** - ADRs follow specific format
3. **Verify against template** - Implementation Status sections have standards
4. **STOP if assumptions needed** - Ask Code for evidence

---

## MANDATORY FIRST ACTIONS

### 1. Understand ADR-032 Current Content
```bash
# ADR-032 is in project knowledge base
# Review current structure to understand where Implementation Status fits
# Check other ADRs for Implementation Status section patterns

cd /Users/xian/Development/piper-morgan

# Look for ADR examples with Implementation Status
find . -name "*.md" -type f -exec grep -l "Implementation Status" {} \; 2>/dev/null

# If found, study their format
```

### 2. Verify Cross-Validation Data from Code
```bash
# Wait for Code to provide:
# - Verification evidence (grep, pytest outputs)
# - Proposed Implementation Status text
# - Git history proving dates
# - File paths and line numbers

# Your job: Verify this documentation is accurate, clear, complete
```

---

## Mission

Review Claude Code's proposed ADR-032 Implementation Status section for:
1. **Technical Accuracy** - Claims match evidence
2. **Documentation Quality** - Clear, well-structured, complete
3. **ADR Standards** - Follows ADR format conventions
4. **Completeness** - Nothing important missing

**Scope**: Documentation review ONLY - Code handles technical verification

---

## Context

- **GitHub Issue**: CORE-GREAT-1C (#187) - Documentation Phase
- **Checkbox**: "Update ADR-032 implementation status"  
- **Current State**: Code is drafting Implementation Status section
- **Target State**: High-quality, accurate, complete documentation
- **Your Role**: Documentation quality gate
- **Infrastructure Verified**: Yes - ADR location confirmed

---

## Evidence Requirements (CRITICAL)

### For EVERY Claim You Make:

**"Documentation is clear"** → Provide specific examples of clarity
**"Section is complete"** → Show what would be missing if you removed anything
**"Format follows standards"** → Reference specific ADR conventions
**"Technical claims verified"** → Confirm you checked Code's evidence

### Completion Bias Prevention:
- **Never approve without reading Code's evidence**
- **NO "looks good"** - Only "verified X, Y, Z are accurate"  
- **NO assumptions about technical details** - Verify with Code
- **Quality gate rigor, not rubber stamp**

---

## Task Breakdown

### Phase 1: Receive and Review Code's Draft (10 min)

**Wait for Code to provide:**
1. Verification evidence (terminal outputs)
2. Proposed Implementation Status markdown
3. Evidence mapping (which claims match which outputs)
4. Any uncertainties or questions

**Your review checklist:**
```markdown
Documentation Quality Review:

STRUCTURE:
- [ ] Section title appropriate ("Implementation Status")
- [ ] Subsections logical and well-organized
- [ ] Flows naturally from ADR's existing content
- [ ] Placement in ADR makes sense

CLARITY:
- [ ] Technical terms explained when needed
- [ ] Dates and milestones clear
- [ ] Evidence references easy to find
- [ ] No ambiguous statements

COMPLETENESS:
- [ ] All GREAT-1 components mentioned (1A, 1B, 1C)
- [ ] Current capabilities documented
- [ ] Known limitations acknowledged
- [ ] Evidence properly cited

ACCURACY:
- [ ] Dates match Code's git history
- [ ] File paths match Code's verification
- [ ] Test counts match Code's pytest output
- [ ] No exaggerated claims
```

### Phase 2: Verify Technical Claims (15 min)

**Cross-check Code's evidence:**

```bash
# Verify Code's claims by checking their evidence
cd /Users/xian/Development/piper-morgan

# If Code says "QueryRouter enabled on line 97":
grep -n "query_router" services/orchestration/engine.py | grep -v "^#"

# If Code says "9 lock tests":
python -m pytest tests/regression/test_queryrouter_lock.py --collect-only | grep "test_"

# If Code says "completed September 22":
git log --oneline --since="2025-09-21" --until="2025-09-23" | grep -i "great-1\|queryrouter"
```

**Create verification report:**
```markdown
Technical Verification Report:

VERIFIED ACCURATE:
- [ ] QueryRouter enablement claim (line numbers match)
- [ ] Lock test count (actual count matches claim)
- [ ] Completion dates (git history confirms)
- [ ] File paths (all files exist at claimed locations)
- [ ] Integration points (code shows claimed connections)

CONCERNS/QUESTIONS:
- [List any discrepancies found]
- [List any unverifiable claims]
- [List any missing evidence]
```

### Phase 3: Documentation Improvement Suggestions (10 min)

**Provide constructive feedback:**

```markdown
Documentation Improvement Suggestions:

CRITICAL (must fix):
- [Issues that make documentation incorrect or misleading]

RECOMMENDED (should improve):
- [Clarity improvements]
- [Completeness additions]
- [Structure enhancements]

OPTIONAL (nice to have):
- [Minor polish items]
- [Additional context that could help]
```

### Phase 4: Final Approval or Revision Request (5 min)

**Decision point:**

```markdown
APPROVAL STATUS:

If all critical items resolved:
✅ APPROVED - Implementation Status section ready
   - All technical claims verified
   - Documentation quality meets standards
   - No blocking issues remain
   - Evidence: [list specific verifications you did]

If critical items remain:
❌ REVISION NEEDED - Issues must be addressed:
   - [Specific issues with evidence]
   - [Specific suggestions for fixes]
   - [What you need from Code to approve]
```

---

## Success Criteria

- [ ] Received Code's draft and evidence
- [ ] Verified all technical claims against Code's evidence  
- [ ] Checked documentation quality (structure, clarity, completeness)
- [ ] Verified ADR format conventions followed
- [ ] Provided specific feedback (not generic approval)
- [ ] Made final approval/revision decision with evidence

---

## STOP Conditions

- If Code hasn't provided evidence for claims (can't verify)
- If technical claims contradict your verification (need discussion)
- If documentation has serious quality issues (need revision)
- If you can't understand Code's evidence (need clarification)

---

## Cross-Validation Protocol

### Request from Code:
1. "Show me your verification commands and outputs"
2. "Which evidence supports which claim in your draft?"
3. "What uncertainties do you have?"
4. "What did you verify and how?"

### Provide to Code:
1. Your technical verification results
2. Your documentation quality assessment
3. Specific improvement suggestions
4. Approval status with reasoning

### Resolution:
- Discuss any discrepancies you found
- Request clarification on unclear evidence
- Suggest specific documentation improvements
- Reach consensus before final approval

---

## Deliverables

1. **Technical Verification Report**: What you verified and results
2. **Documentation Quality Assessment**: Structure, clarity, completeness review
3. **Improvement Suggestions**: Categorized by priority (critical/recommended/optional)
4. **Final Decision**: Approval with evidence OR revision request with specifics

---

## Example Feedback Format

```markdown
## Cursor's Review of ADR-032 Implementation Status

### Technical Verification ✅
- Verified QueryRouter enabled: `grep` output shows line 97 non-commented
- Verified 9 lock tests: `pytest --collect-only` shows 9 test functions
- Verified dates: `git log` shows GREAT-1C completion Sept 22
- Verified file paths: All claimed files exist

### Documentation Quality ✅  
- Structure: Follows ADR convention, placed correctly after Consequences
- Clarity: Technical terms clear, dates specific, evidence well-cited
- Completeness: All three GREAT-1 phases covered, limitations noted

### Suggestions
RECOMMENDED:
- Add specific commit hash for QueryRouter re-enablement (helps future reference)
- Clarify "application layer issues" in limitations (link to CORE-QUERY-1 if exists)

### Decision: ✅ APPROVED
Ready for PM to update knowledge base. All claims verified, quality meets standards.
```

---

*Quality gate, not rubber stamp. Verify, don't just approve.*
