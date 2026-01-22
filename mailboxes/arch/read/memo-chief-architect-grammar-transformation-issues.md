# Memo: Grammar Transformation Issues - Placement Decision

**To**: Chief Architect
**From**: Lead Developer (Claude Code Opus)
**Date**: 2026-01-20
**Re**: Placement of Grammar Transformation Issues (#619-627)

---

## Summary

Following completion of #404 (MUX-VISION-GRAMMAR-CORE), the grammar compliance audit identified 15 features needing transformation. Per PM direction, I've created issues for the 9 highest priority features. These issues need architectural placement.

---

## Issues Created

### Critical Priority (4 issues)
| Issue | Feature | Current State |
|-------|---------|---------------|
| #619 | Intent Classification | Partial |
| #620 | Slack Integration | Partial |
| #621 | GitHub Integration | Partial |
| #622 | Todo Management | Flattened |

### Important Priority (5 issues)
| Issue | Feature | Current State |
|-------|---------|---------------|
| #623 | Feedback System | Partial |
| #624 | Calendar Integration | Partial |
| #625 | Conversation Handler | Partial |
| #626 | Onboarding System | Partial |
| #627 | Personality System | Partial |

---

## Question for Chief Architect

How should these 9 issues be organized? Options:

### Option A: Quality Gates
- Attach to existing feature work as quality gates
- Transformation happens when feature is touched for other reasons
- Pro: Opportunistic, no dedicated bandwidth
- Con: Inconsistent timing, may never complete

### Option B: Dedicated Transformation Epic
- Create new epic: "GRAMMAR-TRANSFORMATION" or similar
- Schedule as dedicated work
- Pro: Systematic completion, clear ownership
- Con: Requires dedicated bandwidth

### Option C: Attach to MUX-VISION Epic (#401)
- Add as children of existing MUX-VISION epic
- Continues the grammar work started in #399/#404
- Pro: Logical grouping, clear lineage
- Con: MUX-VISION may become too large

### Option D: Hybrid Approach
- Critical (4) → Dedicated work or MUX-VISION
- Important (5) → Quality gates for future work
- Pro: Prioritizes high-impact while managing scope
- Con: Two different tracking mechanisms

---

## Context for Decision

**What exists now**:
- MUX infrastructure: 302 tests (#399)
- 5 application patterns: Pattern-050 through 054 (#404)
- Transformation guide with worked example (#404)
- Consciousness philosophy document (#400)
- PR review consciousness checklist (#400)

**All tools exist to do the transformation work**. The question is when and how it gets scheduled.

---

## Recommendation

I lean toward **Option D (Hybrid)** but defer to architectural judgment:
- Critical features touch every user interaction
- Important features can be uplifted opportunistically

---

## Related Issues

- #399 MUX-VISION-OBJECT-MODEL (complete)
- #400 MUX-VISION-CONSCIOUSNESS (complete)
- #401 MUX-VISION Epic
- #404 MUX-VISION-GRAMMAR-CORE (complete)

---

**Awaiting architectural decision on issue placement.**

---

*Memo created: 2026-01-20*
