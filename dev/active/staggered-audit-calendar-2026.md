# Staggered Audit Calendar 2026

**Proposed**: January 3, 2026
**Purpose**: Prevent "audit week" clustering by offsetting recurring reviews
**Owner**: Chief of Staff (tracking), respective owners (execution)

---

## Audit Types & Cadences

| Audit Type | Cadence | Duration | Owner |
|------------|---------|----------|-------|
| Pattern Sweep | 6 weeks | ~1 day | Lead Dev + specialized agents |
| Methodology Audit | 6-8 weeks | ~2 hours | CIO (xian acting) |
| Documentation Audit | 4 weeks | ~1 hour | CoS / Doc Manager |
| Workstream Review | Weekly | ~1 hour | CoS + PM |
| Role Health Check | 4 weeks | ~30 min | HOSR (when active) / CoS |

---

## 2026 Calendar (Staggered)

### Q1 2026

| Week | Mon | Pattern Sweep | Methodology | Doc Audit | Role Health |
|------|-----|---------------|-------------|-----------|-------------|
| 1 | Jan 6 | | | | |
| 2 | Jan 13 | | | ✓ | |
| 3 | Jan 20 | | | | ✓ |
| 4 | Jan 27 | | | | |
| 5 | Feb 3 | ✓ | | | |
| 6 | Feb 10 | | | ✓ | |
| 7 | Feb 17 | | ✓ | | ✓ |
| 8 | Feb 24 | | | | |
| 9 | Mar 3 | | | ✓ | |
| 10 | Mar 10 | | | | |
| 11 | Mar 17 | ✓ | | | ✓ |
| 12 | Mar 24 | | | ✓ | |
| 13 | Mar 31 | | | | |

### Q2 2026

| Week | Mon | Pattern Sweep | Methodology | Doc Audit | Role Health |
|------|-----|---------------|-------------|-----------|-------------|
| 14 | Apr 6 | | ✓ | | |
| 15 | Apr 13 | | | | ✓ |
| 16 | Apr 20 | | | ✓ | |
| 17 | Apr 27 | ✓ | | | |
| 18 | May 4 | | | | |
| 19 | May 11 | | | ✓ | ✓ |
| 20 | May 18 | | | | |
| 21 | May 25 | | ✓ | | |
| 22 | Jun 1 | | | ✓ | |
| 23 | Jun 8 | ✓ | | | ✓ |
| 24 | Jun 15 | | | | |
| 25 | Jun 22 | | | ✓ | |
| 26 | Jun 29 | | | | |

---

## Offset Logic

**Pattern Sweep** (anchor): Weeks 5, 11, 17, 23, 29, 35, 41, 47
- 6-week intervals starting Feb 3

**Methodology Audit**: Weeks 7, 14, 21, 28, 35, 42, 49
- ~7-week intervals, offset 2 weeks from Pattern Sweep
- Never same week as Pattern Sweep

**Documentation Audit**: Weeks 2, 6, 9, 12, 16, 19, 22, 25...
- 3-4 week intervals
- Lighter lift, more frequent

**Role Health Check**: Weeks 3, 7, 11, 15, 19, 23...
- 4-week intervals
- Offset 1 week from Doc Audit
- Critical for HOSR function

---

## Maximum Audit Load Per Week

**Design Principle**: No more than 2 audits in any given week.

**Worst Case**: Doc Audit + Role Health (both lightweight, ~1.5 hours total)

**Best Case**: Most weeks have 0-1 audits

---

## GitHub Workflow Implementation

### Pattern Sweep Workflow
```yaml
# .github/workflows/pattern-sweep-reminder.yml
name: Pattern Sweep Reminder
on:
  schedule:
    # Every 6 weeks on Monday at 9am UTC
    # Starting Feb 3, 2026
    - cron: '0 9 3 2 *'   # Feb 3
    - cron: '0 9 17 3 *'  # Mar 17
    - cron: '0 9 27 4 *'  # Apr 27
    - cron: '0 9 8 6 *'   # Jun 8
    # ... continue for year
```

### Documentation Audit Workflow
```yaml
# .github/workflows/doc-audit-reminder.yml
name: Documentation Audit Reminder
on:
  schedule:
    # Every 3-4 weeks on Monday at 9am UTC
    - cron: '0 9 13 1 *'  # Jan 13
    - cron: '0 9 10 2 *'  # Feb 10
    - cron: '0 9 3 3 *'   # Mar 3
    # ... continue for year
```

### Role Health Check Workflow
```yaml
# .github/workflows/role-health-reminder.yml
name: Role Health Check Reminder
on:
  schedule:
    # Every 4 weeks on Monday at 9am UTC
    - cron: '0 9 20 1 *'  # Jan 20
    - cron: '0 9 17 2 *'  # Feb 17
    - cron: '0 9 17 3 *'  # Mar 17
    # ... continue for year
```

---

## Issue Templates for Each Audit

### Pattern Sweep Issue Template
```markdown
---
name: Pattern Sweep
about: 6-week pattern analysis
labels: pattern-sweep, methodology
---

## Pattern Sweep: [Date Range]

**Period**: [Start] - [End]
**Lead**: Lead Developer (Specialist Instance)

### Checklist
- [ ] Pattern library index updated
- [ ] Usage analysis complete
- [ ] Novelty candidates identified
- [ ] Evolution tracking complete
- [ ] Meta-synthesis complete
- [ ] FALSE POSITIVE test passed
- [ ] Leadership summary prepared
- [ ] Ratification decisions documented

### Deliverables
- [ ] pattern-sweep-results-YYYY-MM-DD.md
- [ ] pattern-sweep-leadership-summary.md
- [ ] DRAFT-pattern-XXX.md (if any)
```

### Documentation Audit Issue Template
```markdown
---
name: Documentation Audit
about: Monthly documentation health check
labels: documentation, audit
---

## Documentation Audit: [Date]

**Owner**: Chief of Staff / Doc Manager

### Checklist
- [ ] Broken links scan (target: <30)
- [ ] Stale documents identified (>90 days unchanged)
- [ ] README coverage verified (target: 100%)
- [ ] Navigation docs current
- [ ] Knowledge folder aligned with filesystem

### Metrics
- Broken links: ___ (previous: ___)
- Stale docs: ___
- Coverage: ___%
```

### Role Health Check Issue Template
```markdown
---
name: Role Health Check
about: Monthly agent role health assessment
labels: sapient-resources, audit
---

## Role Health Check: [Date]

**Owner**: HOSR / Chief of Staff (interim)

### Active Roles Assessed
| Role | Last Session | Drift Risk | Notes |
|------|--------------|------------|-------|
| Chief of Staff | | Low/Med/High | |
| Chief Architect | | | |
| Lead Developer | | | |
| Communications Director | | | |

### Checklist
- [ ] All active roles had session in past 2 weeks
- [ ] Briefing documents current
- [ ] No role drift detected
- [ ] Succession plans documented
- [ ] Prompt templates current
```

---

## Tracking Dashboard

CoS to maintain simple tracking:

| Audit Type | Last Completed | Next Due | Status |
|------------|----------------|----------|--------|
| Pattern Sweep | Dec 27, 2025 | Feb 3, 2026 | ✅ On track |
| Methodology | TBD | Feb 17, 2026 | ⏳ Schedule |
| Documentation | Dec 25, 2025 | Jan 13, 2026 | ✅ On track |
| Role Health | N/A | Jan 20, 2026 | 🆕 New |

---

## Adjustment Protocol

If an audit needs to slip:
1. Move by 1 week maximum
2. Don't create collision with other audits
3. Document reason in tracking dashboard
4. Don't skip entirely - defer to next slot

If project phase requires pause (e.g., major release):
1. PM can suspend non-critical audits (Doc, Role Health)
2. Pattern Sweep and Methodology should still run
3. Document suspension and resume date

---

## Success Metrics

**After 3 months**:
- No week with >2 audits
- All audits completed within 1 week of scheduled date
- Pattern library growing (target: 50+ patterns by Q2)
- Documentation health: <30 broken links sustained
- Role drift incidents: <2 per quarter

---

*Calendar proposed by Chief of Staff*
*January 3, 2026*
*For implementation via GitHub Actions*
