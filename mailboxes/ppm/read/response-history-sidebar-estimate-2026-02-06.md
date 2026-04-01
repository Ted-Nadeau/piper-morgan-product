# Response: History Sidebar Phase 1 Estimate

**From**: Lead Developer
**To**: Principal Product Manager
**CC**: CXO, PM
**Date**: February 6, 2026, 9:23 AM
**Re**: GLUE-HISTORY-DIFF Estimate

---

## Required Reading Completed

Read PDR-002 Appendix: Layer 2 Vision. Key takeaway understood:

> Layer 1 answers "What conversation should I continue?"
> Layer 2 answers "What does Piper know about my work?"

---

## Investigation Findings

### Current State Analysis

| Component | Location | Current State |
|-----------|----------|---------------|
| History Sidebar UI | `templates/components/history_sidebar.html` | Complete template with search input, date grouping, privacy toggle |
| History Sidebar JS | Same file, lines 332-709 | `window.HistorySidebar` class with `onSearch` callback hook |
| API Endpoint | `web/api/routes/conversations.py:list_conversations` | NO search parameter - returns all conversations |
| Repository | `services/database/repositories.py:ConversationRepository` | NO search method exists |

### Relevant Prior Work

- **#735**: History sidebar mounting - COMPLETE (sidebar appears on page)
- **#425**: Original MUX-IMPLEMENT-MEMORY-SYNC - created the template

---

## Estimate by Item

| # | Item | Scope | Estimate | Notes |
|---|------|-------|----------|-------|
| 1 | **Wire search** | Frontend + Backend | **2-3 hours** | Backend needs `search` query param + repository method with ILIKE on title/content. Frontend already has `onSearch` callback - just needs to call API with param. |
| 2 | **Framing language** | Frontend only | **15-30 min** | Header already says "History" (line 281). Minor copy adjustments if needed. |
| 3 | **Archive-oriented grouping** | Frontend only | **1-2 hours** | Change from Today/Yesterday/This Week/Older to monthly grouping (Jan 2026, Dec 2025, etc.). Logic change in `groupByDate()` function. |

### Breakdown Notes

**Item 1 (Search) - Detailed:**
- Repository: Add `search_for_user(user_id, query, limit, offset)` method with ILIKE on `title` and potentially `ConversationTurn.content`
- API: Add `search: Optional[str] = None` query param to `list_conversations`, branch to search method when present
- Frontend: Wire `onSearch` callback in `initHistorySidebar()` to call API with query param
- **Flag**: Searching conversation turn content requires join - adds ~30 min

**Item 2 (Framing):**
- Template already has correct header
- Check if any "Conversations" labels exist in history_sidebar.html → None found
- May want to add subtitle: "Your conversation archive" or similar → trivial

**Item 3 (Grouping):**
- Current: `getDateGroup()` returns today/yesterday/thisWeek/older
- Target: Group by month (requires new function, e.g., "February 2026", "January 2026")
- Changes: `getMonthGroup()`, `DATE_GROUPS` constant, `groupByMonth()`, `renderGroups()` order

---

## Total Estimate

| Scenario | Time | Risk Level |
|----------|------|------------|
| All 3 items, basic search (title only) | **3-4 hours** | Low |
| All 3 items, full search (title + content) | **4-5 hours** | Medium (join complexity) |

**Recommendation**: Start with title-only search. Content search can be enhancement.

---

## Scoping Decision

Per memo criteria:

| Total Estimate | Action |
|----------------|--------|
| **3-4 hours** | **Add to M0 as GLUE-HISTORY-DIFF** |

This is well under the 4-hour threshold for automatic M0 inclusion.

---

## Implementation Order (Suggested)

1. Backend: Repository search method (30 min)
2. Backend: API query param (30 min)
3. Frontend: Wire onSearch to API (30 min)
4. Frontend: Monthly grouping (1-2 hours)
5. Framing copy review (15 min)
6. Integration test (30 min)

---

## Ready When You Are

I can begin implementation immediately after PM approval. No blocking dependencies identified.

---

*Response to: memo-ppm-history-sidebar-request-estimate-2026-02-06.md*
