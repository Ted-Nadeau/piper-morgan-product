# Project Instructions Migration Plan

## Elements to Preserve from Current Instructions

### 1. Add to ARCHITECT.md

**Infrastructure Verification Process** (the detailed two-stage dance):
```markdown
## Infrastructure Verification Process (MANDATORY)

Stage 1: Pre-Gameplan Verification
1. Review architecture docs in knowledge
2. Check assumptions against known constants
3. Fill out Infrastructure Verification in gameplan-template.md
4. STOP and ask PM for verification

Stage 2: PM Verification Required
[Include the full verification script request]
```

**No Implementation Artifacts Rule**:
```markdown
## Critical Rule
NEVER create implementation artifacts - Use agent coordination
If you find yourself writing code in artifacts, STOP immediately
```

**Artifact Usage Rules**:
```markdown
## Deliverable Locations
- Prompts go in artifacts named: agent-prompt-[task].md
- Reports go in session logs
- Code changes tracked in GitHub only
```

### 2. Add to METHODOLOGY.md

**Session Satisfaction Protocol**:
```markdown
## Session Satisfaction Protocol

Before ending any session:
1. Complete 5-point assessment in session log
2. Ask PM each metric, compare answers:
   - Value: What got shipped?
   - Process: Did methodology work smoothly?
   - Feel: How was the cognitive load?
   - Learned: Any key insights?
   - Tomorrow: Clear next steps?
   - Overall: 😊 / 🙂 / 😐 / 😕 / 😞
3. GitHub issue emoji close (🎉 great, ✅ good, 🤔 meh, 😤 rough)

Reference: session-log-instructions.md
```

**Session Failure Conditions**:
```markdown
## Session Failure Conditions

The session has failed our standards if:
- Architect creates gameplan without PM verification
- Architect creates implementation artifacts
- Agents proceed without verification
- Work happens outside GitHub tracking
- Assumptions made without checking
- Lead Developer skips 00-START-HERE
```

**Success Metrics**:
```markdown
## Success Metrics

Per Session:
- Setup time: <15 minutes
- Infrastructure verification: 100%
- GitHub tracking: 100% complete
- Manual reminders needed: <5

Per Week:
- Methodology compliance: >90%
- Cross-validation performed: 100%
- Documentation current: Always
```

### 3. Keep Template References

Preserve all references to:
- `gameplan-template.md` (v6.0+ with verification)
- `agent-prompt-template.md`
- `00-START-HERE-LEAD-DEV.md`
- `cross-validation-protocol.md`
- `github-guide.md`
- `stop-conditions.md`
- `session-log-instructions.md`

### 4. Historical Evidence (Optional Appendix)

Consider creating `LESSONS-LEARNED.md`:
```markdown
# Historical Evidence of Assumption Failures

## Sept 7: Routes Structure Assumption
- Assumed routes/ and templates/ structure
- Reality: Single app.py file
- Cost: 2 hours wasted on wrong gameplan

## Sept 8: Template Variables Issue
- Created gameplan for template variables
- Reality: Issue was field names
- Pattern: Assuming enterprise structure when MVP simplicity exists
```

## Minimal Viable Project Instructions

After preserving the above, the Claude.ai project instructions become:

```markdown
# Piper Morgan Development

You are working on Piper Morgan, an intelligent PM assistant.

## Essential Briefing Documents

Search knowledge for these documents (no folders, use search):
1. BRIEFING-CURRENT-STATE - Where we are right now
2. BRIEFING-[YOUR-ROLE] - Your specific role guide
3. BRIEFING-METHODOLOGY - How we work
4. BRIEFING-PROJECT - What Piper Morgan is

Your role determines which briefing to read:
- Chief Architect → BRIEFING-ROLE-ARCHITECT
- Lead Developer → BRIEFING-ROLE-LEAD-DEV
- Programmer → BRIEFING-ROLE-PROGRAMMER

## Critical Rules

1. If you cannot find briefing documents, STOP and ask PM
2. Lead Developer: Always read 00-START-HERE-LEAD-DEV first
3. Never create implementation in artifacts - coordinate agents instead
4. All work requires GitHub issue number

## Current Focus

See BRIEFING-CURRENT-STATE for current epic and priorities.

---
*If these instructions seem minimal, that's intentional.
Full context is in the briefing documents.*
```

---

Does this preservation plan look right?
