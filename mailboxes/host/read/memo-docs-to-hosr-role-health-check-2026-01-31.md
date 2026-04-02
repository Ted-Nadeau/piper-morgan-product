# Memo: Role Health Check Operationalization

**From**: Documentation Management Specialist
**To**: Head of Sapient Resources (HoSR)
**Date**: January 31, 2026
**Subject**: Defining and operationalizing the Role Health Check audit
**Response-Requested**: yes

---

## Context

Per the staggered audit calendar (`docs/internal/operations/staggered-audit-calendar-2026.md`), Role Health Checks are scheduled every 4 weeks. The first was due January 20, 2026 (now 11 days overdue).

The calendar defines the **schedule** but not the **methodology**. The current template is a skeleton:

```markdown
### Active Roles Assessed
| Role | Last Session | Drift Risk | Notes |
|------|--------------|------------|-------|

### Checklist
- [ ] All active roles had session in past 2 weeks
- [ ] Briefing documents current
- [ ] No role drift detected
- [ ] Succession plans documented
- [ ] Prompt templates current
```

This raises questions that need answers before we can operationalize:

---

## Questions Requiring HoSR Input

### 1. What is "Role Health"?

The checklist mentions "drift risk" but doesn't define it. Possible dimensions:
- **Session recency**: Has the role been activated recently?
- **Briefing currency**: Are the BRIEFING-ESSENTIAL-* docs up to date?
- **Identity stability**: Does the role maintain consistent behavior across sessions?
- **Workload appropriateness**: Is the role being used for its intended purpose?
- **Succession readiness**: Could another agent pick up this role if needed?

**Question**: Which dimensions matter most? Are there others?

### 2. How Do We Measure Drift Risk?

Current options (Low/Med/High) are subjective. Possible operationalizations:
- **Low**: Session in past 2 weeks, briefing updated in past 30 days
- **Medium**: Session in past 4 weeks, OR briefing >30 days stale
- **High**: No session in 4+ weeks, OR briefing >60 days stale, OR identity confusion observed

**Question**: Are these thresholds appropriate? What triggers escalation?

### 3. Which Roles Are "Active"?

The current roster includes many roles. Not all are equally active:
- **High frequency**: Lead Developer, Chief of Staff, Communications
- **Medium frequency**: Chief Architect, PPM, CXO
- **Low frequency/dormant**: CIO, HoSR, Ted Nadeau

**Question**: Should we track all roles equally, or tier them by expected activity?

### 4. What's the Remediation Path?

If a role shows drift, what happens?
- Update briefing docs?
- Run a "recalibration session"?
- Escalate to PM?
- Something else?

**Question**: What's the escalation ladder?

---

## Proposal: Two-Phase Operationalization

### Phase 1: Define the Methodology (with PM + HoSR)

Deliverable: `docs/internal/operations/role-health-check-methodology.md`

Contents:
1. Definition of role health dimensions
2. Drift risk scoring criteria (objective where possible)
3. Active role roster with expected cadence
4. Remediation playbook
5. Audit checklist (expanded from current skeleton)

### Phase 2: Set Up the Workflow

Once methodology is defined:
1. Create GitHub workflow (like pattern-sweep.yml and weekly-docs-audit.yml)
2. Add calendar update instruction to closing checklist
3. Update staggered audit calendar with accurate tracking

---

## Recommended Next Step

Schedule a brief session (30 min) with PM to answer the questions above. Once we have answers, I can help draft the methodology document and workflow.

The Jan 20 and Feb 17 checks are technically overdue/upcoming, but it's better to define the process correctly than to run an undefined audit.

---

**Action Requested**: Please coordinate with PM to schedule methodology definition session, or provide answers to the questions above via return memo.

---

*Memo prepared by Docs Management Specialist*
*January 31, 2026*
