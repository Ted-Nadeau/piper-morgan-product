# Plan: ALPHA_KNOWN_ISSUES.md Restructure

**Date**: January 31, 2026
**Author**: Docs Management Specialist
**Status**: Awaiting PM Approval

---

## Problem Statement

The current `ALPHA_KNOWN_ISSUES.md` is 624 lines. The actual "Known Issues" section doesn't appear until line 394 (63% through the document).

**Current structure** (by line count):
| Section | Lines | % of Doc | Purpose |
|---------|-------|----------|---------|
| Header | 1-8 | 1% | Version info |
| ✅ What Works | 9-305 | 48% | Feature list (BLOAT) |
| 🗣️ Chat Capabilities | 306-391 | 14% | Query matrix (BLOAT) |
| ⚠️ Known Issues | 392-416 | 4% | **Actual purpose** |
| 🚧 Experimental | 417-452 | 6% | Needs testing |
| 📋 Planned for Beta | 453-501 | 8% | Roadmap (belongs elsewhere) |
| 🐛 How to Report | 502-528 | 4% | Useful |
| 📊 Completeness Matrix | 529-557 | 5% | Feature list (BLOAT) |
| 🎯 Testing Goals | 558-596 | 6% | Useful |
| Footer | 597-624 | 4% | Links, updates |

**Core issue**: 67% of the doc is feature marketing, not issue documentation.

---

## Guiding Principle

> "The goal of a doc like this is to save alpha tester's time testing things we know do not yet work and reporting bugs we are already aware of or against unfinished features."

Alpha testers should be able to quickly answer:
1. What's broken right now? (Don't waste time on these)
2. What's known-incomplete? (Expect rough edges)
3. What needs testing? (Focus here)

---

## Proposed Structure

### New Order (Known Issues FIRST)

```
1. Header (version, date, quick summary)
2. ⚠️ KNOWN ISSUES (the actual issues — P0/P1/P2 by severity)
3. 🚧 Partially Complete / Experimental (expect rough edges)
4. 🧪 Needs Testing (where to focus alpha effort)
5. ✅ What's Believed Working (brief summary, not exhaustive)
6. 📋 Planned for Beta (brief, links to roadmap)
7. 🐛 How to Report Issues
8. See Also / Footer
```

### Target: Under 200 lines

| Section | Target Lines | Content |
|---------|--------------|---------|
| Header | 10 | Version, date, one-line summary |
| Known Issues | 40-60 | Actual bugs, by severity |
| Partially Complete | 20-30 | Features with gaps |
| Needs Testing | 20-30 | Where to focus |
| What Works | 30-40 | Brief summary, NOT exhaustive list |
| Planned for Beta | 15-20 | Brief, link to roadmap |
| How to Report | 15-20 | Streamlined |
| Footer | 10 | Links |
| **Total** | ~160-200 | Down from 624 |

---

## What Gets Cut vs. Moved

### CUT (remove entirely)
- Detailed feature descriptions in "What Works" (this is a guide, not issues doc)
- Issue numbers for resolved issues (historical, not useful to testers)
- Feature Completeness Matrix (redundant with What Works)
- Detailed chat capabilities matrix (move to separate doc or testing guide)

### MOVED (to other docs)
| Content | Move To |
|---------|---------|
| Detailed feature list | New `ALPHA_FEATURE_GUIDE.md` (optional, discuss with PM) |
| Chat capabilities matrix | `docs/internal/testing/canonical-query-test-matrix.md` (already exists) |
| Detailed roadmap items | `docs/internal/planning/roadmap/roadmap.md` |

### KEPT (condensed)
- Known issues (expanded with current state)
- Experimental/needs testing
- Brief "what works" summary (1-2 lines per category, not per feature)
- How to report
- Testing goals (condensed)

---

## Known Issues: Current State Research

Before restructuring, I need to verify current known issues. Sources to check:

1. **GitHub Issues** - Open bugs labeled `bug` or `alpha-feedback`
2. **Recent omnibus logs** - Issues mentioned Jan 28-30
3. **This doc's current Known Issues section** - What's listed

### From current doc (lines 394-416):
- Cosmetic: Settings/Personality layout (fixed?)
- Missing breadcrumbs (fixed?)
- Placeholder pages: Advanced Privacy, GitHub OAuth
- Note: "All P0/P1 issues resolved as of November 23, 2025"

### From recent omnibus logs (Jan 28-30):
- #728: Projects not saving during onboarding (FIXED Jan 30)
- #731: Conversation persistence (FIXED Jan 29)
- #733: Projects saving (FIXED Jan 30)
- #734: Multi-tenancy calendar token leak (FIXED Jan 30 - 94 tests)
- #735: History sidebar (FIXED Jan 30)
- #736: Projects unique constraint (FIXED Jan 30)
- #737: Portfolio onboarding routing (FIXED Jan 30)

**Observation**: The doc says "All P0/P1 resolved Nov 23" but several P0s were found and fixed Jan 28-30. The doc is stale.

---

## Execution Steps

### Phase 1: Research (before restructure)
- [ ] Query GitHub for open bugs: `gh issue list --label bug --state open`
- [ ] Query for alpha feedback: `gh issue list --label alpha-feedback --state open`
- [ ] Check if "fixed" items in doc are actually closed
- [ ] Compile current known issues list

### Phase 2: Restructure
- [ ] Create new structure with Known Issues first
- [ ] Write brief "What Works" summary (category-level, not feature-level)
- [ ] Condense other sections
- [ ] Remove redundant content
- [ ] Update version/date

### Phase 3: Validate
- [ ] Doc under 200 lines
- [ ] Known Issues appears in first 20% of doc
- [ ] All listed issues verified against GitHub
- [ ] Links work

### Phase 4: Runbook Update
- [ ] Add guidance to release runbook for maintaining this doc
- [ ] Define what belongs here vs. elsewhere

---

## Questions for PM

1. **Feature Guide**: Should I create a separate `ALPHA_FEATURE_GUIDE.md` for the detailed "what works" content, or just cut it? (My lean: cut it — testers can discover features; they need to know what's broken)

2. **Chat Capabilities Matrix**: The canonical query matrix already exists at `docs/internal/testing/canonical-query-test-matrix.md`. Remove from this doc entirely, or keep a one-line reference?

3. **Severity Levels**: Should Known Issues use P0/P1/P2 or simpler categories like "Blocking / Annoying / Cosmetic"?

---

## Approval Request

Please review this plan. Once approved, I'll execute the restructure.

---

*Plan prepared by Docs Management Specialist*
*January 31, 2026*
