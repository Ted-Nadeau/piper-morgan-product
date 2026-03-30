---
from: Piper Alpha (PA)
to: Lead Developer
date: 2026-03-30
subject: PR #856 cherry-pick — Ted Nadeau's design docs ready for review
priority: low
---

# PR #856 Cherry-Pick: Ted Nadeau's Design Docs

## Context

PR #856 from Ted Nadeau (Feb 25) has been open for 33 days. PM and I reviewed it today. The PR bundles several valuable design documents with some infrastructure changes and artifacts that shouldn't be merged as-is (`.pyc` files, `dump.rdb`, messy merge structure).

PM has approved cherry-picking the design docs. I've placed the files in the working tree on the `pa/first-session` branch. They need your review before merging to main.

## Files Cherry-Picked (5 docs)

1. **`docs/internal/design/piper-morgan-by-analogy.md`** — Positioning doc comparing Piper to Jira. "Same domain, different paradigm: Colleague vs Tool." Strong framing: Piper sits *upstream* of where Jira shines — clarifying the why, shaping roadmap, determining MVP scope.

2. **`docs/internal/design/piper-morgan-prfaq.md`** — Amazon Working Backwards PR/FAQ format. Customer-centric product narrative with press release, FAQ, and internal FAQ sections. Well-written and consistent with our positioning.

3. **`docs/internal/design/questions-for-technical-system-architect.md`** — Discussion questions for the Chief Architect about system design tradeoffs.

4. **`suggestions/README.md`** — Framework for pre-issue ideas and change requests.

5. **`suggestions/SUGGESTIONS_ted.md`** — Ted's specific suggestions: LangChain consideration, LLM adapter observability, and ER diagram/data dictionary request.

## Files NOT Cherry-Picked (correctly excluded)

- `.pyc` compiled Python files (should never be in VCS)
- `data/redis/dump.rdb` (binary, shouldn't be committed)
- `Dockerfile` changes (Windows CRLF fix — valid but needs separate review)
- Alembic migration (creates features table — valid but needs separate review)
- `NAVIGATION.md` changes (references the new docs — we can add these when merging)
- Briefing position updates (automated GitHub Action commits caught in the merge)

## What's Needed

1. **Review the 5 docs** for accuracy and alignment with current architecture
2. **Decide on the Dockerfile fix and alembic migration** — these are legitimate fixes but should be reviewed independently
3. Once docs are approved, update `NAVIGATION.md` to reference them
4. PM will close PR #856 with a note to Ted explaining the cherry-pick approach

## Notes

- The `by-analogy` doc is particularly useful — its "upstream vs atoms" framing may inform the Vision doc V2 that PM has assigned to me.
- Ted's suggestions (LangChain, observability, ER diagram) are worth discussing at the next architecture review.
- Ted has also shared additional spec and process docs that PM wants to review with him — separate from this PR.

No urgency — this is available work while M1 gate testing is pending.
