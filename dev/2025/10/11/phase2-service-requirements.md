# Phase 2: Service Requirements Analysis

**Date**: October 11, 2025, 11:35 AM
**Handler**: `_handle_analyze_commits`
**Duration**: 15 minutes

---

## Service Investigation Results

### Existing Services Checked

**GitHubDomainService** (`services/domain/github_domain_service.py`):
- ❌ No `get_commits()` method
- ❌ No `analyze_commits()` method
- ✅ Has `get_recent_issues()` but not commits

**GitHubIntegrationRouter** (`services/integrations/github/github_integration_router.py`):
- ✅ Has `get_recent_activity(days=7)` (line 314-326)
- Returns: `Dict[str, List[Dict[str, Any]]]` with **commits, PRs, issues**
- Already used by: `standup_orchestration_service.py`
- Routes to spatial or legacy GitHub integration

---

## Decision: Use Existing `get_recent_activity()`

### Rationale

1. **Already Working**: Used by standup service, proven to work
2. **Returns Commits**: Returns Dict with 'commits' key containing commit data
3. **No New Service Needed**: Avoids creating new methods (would take >30 min)
4. **Time Efficient**: Can proceed immediately to implementation

### Implementation Plan

```python
# In _handle_analyze_commits():
from services.domain.github_domain_service import GitHubDomainService

github_service = GitHubDomainService()

# Get recent activity (includes commits)
activity = await github_service._github_agent.get_recent_activity(days=7)

# Extract commits from activity
commits = activity.get('commits', [])

# Analyze commits
commit_count = len(commits)
authors = {}
for commit in commits:
    author = commit.get('author', {}).get('name', 'Unknown')
    authors[author] = authors.get(author, 0) + 1

# Return analysis
return IntentProcessingResult(
    success=True,
    message=f"Analyzed {commit_count} commits",
    intent_data={
        "commit_count": commit_count,
        "authors": authors,
        "commits": commits[:10]  # First 10
    },
    requires_clarification=False
)
```

### Alternative (If get_recent_activity doesn't work)

**Option B**: Add `get_commits()` to GitHubDomainService
- Estimated time: 30-45 minutes
- Would require testing
- Cleaner separation of concerns

**Decision**: Try Option A first, fall back to Option B if needed

---

## Next Steps

✅ **Proceed to Part 3**: Write tests first (TDD red phase)
- Test that commits are actually fetched
- Test that analysis is performed
- Test that no placeholder response is returned

---

*Service requirements analysis complete: 11:35 AM*
