# Phase 2C: Data Analysis Scope Definition

**Date**: October 11, 2025, 1:08 PM
**Purpose**: Define comprehensive scope for `_handle_analyze_data` implementation

---

## Part 2.1: Available Data Sources (Investigation Results)

### Primary Data Source: `get_recent_activity(days: int = 7)`

**Location**: `services/integrations/github/github_agent.py:509-599`

**Returns**: `Dict[str, List[Dict[str, Any]]]` with four data streams:

```python
{
    "commits": [
        {
            "sha": "abc12345",
            "message": "Commit message (first line)",
            "author": "Author Name",
            "date": "2025-10-11T10:00:00",
            "url": "https://github.com/..."
        },
        # ... up to 10 commits
    ],
    "prs": [
        {
            "number": 123,
            "title": "PR title",
            "state": "open|closed|merged",
            "author": "username",
            "updated_at": "2025-10-11T10:00:00",
            "url": "https://github.com/..."
        },
        # ... up to 5 PRs
    ],
    "issues_closed": [
        {
            "number": 456,
            "title": "Issue title",
            "state": "closed",
            "author": "username",
            "created_at": "2025-10-10T10:00:00",
            "url": "https://github.com/..."
        },
        # ... up to 10 issues
    ],
    "issues_created": [
        {
            "number": 789,
            "title": "Issue title",
            "state": "open",
            "author": "username",
            "created_at": "2025-10-11T10:00:00",
            "url": "https://github.com/..."
        },
        # ... up to 10 issues
    ]
}
```

**Characteristics**:
- Time-bounded (configurable days parameter)
- Already used by Phase 2 (`_handle_analyze_commits`) and Phase 2B (`_handle_generate_report`)
- Reliable, tested, production-ready
- Returns empty lists on error (graceful degradation)

### Secondary Data Sources (Available but not used in this phase)

**`get_development_context()`** - Location: `services/integrations/github/github_agent.py:348-381`
- Returns: active_prs, pending_reviews, recent_commits counts
- Could be used for real-time development state analysis
- Not included in Phase 2C scope (would be a different analysis type)

**`get_open_issues()`** - Location: `services/integrations/github/github_agent.py:205-253`
- Returns: detailed issue list with labels, assignees, body
- Could be used for issue categorization analysis
- Not included in Phase 2C scope (would be a different analysis type)

### Decision: Use `get_recent_activity()` as Primary Data Source

**Rationale**:
1. **Consistency**: Same source as Phase 2 and 2B
2. **Richness**: Four data streams (commits, PRs, issues_created, issues_closed)
3. **Proven**: Already validated in production
4. **Flexible**: Supports multiple analysis types from single source
5. **Efficient**: Single API call gets all data needed

---

## Part 2.2: Analysis Types (Design)

### Overview

`_handle_analyze_data` will support **three analysis types** via `data_type` parameter:

1. **`repository_metrics`** - Comprehensive repository activity metrics
2. **`activity_trends`** - Activity patterns and trends over time
3. **`contributor_stats`** - Contributor-focused analysis

Each type analyzes the same data source differently, returning different insights.

---

### Analysis Type 1: `repository_metrics`

**Purpose**: Comprehensive overview of repository activity

**Analysis Performed**:
- Total counts across all activity types
- Activity distribution (what percentage of activity is commits vs PRs vs issues)
- Summary statistics

**Input Parameters**:
- `repository` (required)
- `days` (optional, default 7)
- `data_type` = "repository_metrics"

**Output Structure**:
```python
{
    "category": "analysis",
    "action": "analyze_data",
    "confidence": 0.90,
    "repository": "owner/repo",
    "data_type": "repository_metrics",
    "timeframe": "last 7 days",
    "days": 7,
    "metrics": {
        "total_activity_count": 45,
        "commits_count": 30,
        "prs_count": 8,
        "issues_created_count": 4,
        "issues_closed_count": 3,
        "activity_distribution": {
            "commits": 66.7,      # percentage
            "prs": 17.8,
            "issues_created": 8.9,
            "issues_closed": 6.7
        }
    }
}
```

**Use Case**: "Analyze repository activity for piper-morgan over the last 7 days"

---

### Analysis Type 2: `activity_trends`

**Purpose**: Identify activity patterns and velocity

**Analysis Performed**:
- Daily activity breakdown (if data supports it)
- Activity type trends (what's most active)
- Velocity indicators

**Input Parameters**:
- `repository` (required)
- `days` (optional, default 7)
- `data_type` = "activity_trends"

**Output Structure**:
```python
{
    "category": "analysis",
    "action": "analyze_data",
    "confidence": 0.90,
    "repository": "owner/repo",
    "data_type": "activity_trends",
    "timeframe": "last 7 days",
    "days": 7,
    "metrics": {
        "total_activity_count": 45,
        "commits_count": 30,
        "prs_count": 8,
        "issues_created_count": 4,
        "issues_closed_count": 3
    },
    "trends": {
        "most_active_type": "commits",        # Type with highest count
        "issue_closure_rate": 75.0,           # closed / (created + closed) * 100
        "pr_activity": "8 PRs updated",
        "commit_velocity": "4.3 commits/day"  # commits / days
    },
    "insights": [
        "Repository is most active in commits (30 total)",
        "Strong issue closure rate (75.0%)",
        "Active PR development (8 PRs)"
    ]
}
```

**Use Case**: "What are the activity trends for piper-morgan this week?"

---

### Analysis Type 3: `contributor_stats`

**Purpose**: Analyze contributor patterns and collaboration

**Analysis Performed**:
- Author distribution across commits
- Contributor counts for PRs and issues
- Collaboration indicators

**Input Parameters**:
- `repository` (required)
- `days` (optional, default 7)
- `data_type` = "contributor_stats"

**Output Structure**:
```python
{
    "category": "analysis",
    "action": "analyze_data",
    "confidence": 0.90,
    "repository": "owner/repo",
    "data_type": "contributor_stats",
    "timeframe": "last 7 days",
    "days": 7,
    "metrics": {
        "total_contributors": 3,
        "commit_authors": 2,
        "pr_authors": 2,
        "issue_authors": 1
    },
    "contributors": {
        "commits": {
            "Alice": 20,
            "Bob": 10
        },
        "prs": {
            "Alice": 5,
            "Charlie": 3
        },
        "issues": {
            "Bob": 4
        }
    },
    "insights": [
        "3 total contributors across all activities",
        "Alice is most active committer (20 commits)",
        "Collaboration across commits, PRs, and issues"
    ]
}
```

**Use Case**: "Who has been contributing to piper-morgan this week?"

---

## Part 2.3: Response Structure Design

### Success Response (Common Structure)

All analysis types return:

```python
IntentProcessingResult(
    success=True,
    message="[Human-readable summary of analysis]",
    intent_data={
        "category": "analysis",
        "action": "analyze_data",
        "confidence": float,
        "repository": str,
        "data_type": str,
        "timeframe": str,
        "days": int,
        "metrics": dict,        # Always present - basic counts
        "trends": dict,         # Optional - for activity_trends
        "contributors": dict,   # Optional - for contributor_stats
        "insights": list        # Optional - human-readable insights
    },
    workflow_id=str,
    requires_clarification=False  # ← CRITICAL: False for success
)
```

### Error Response (Missing Repository)

```python
IntentProcessingResult(
    success=False,
    message="Cannot analyze data: repository not specified. Please specify which repository.",
    intent_data={
        "category": "analysis",
        "action": "analyze_data",
    },
    workflow_id=str,
    requires_clarification=True,
    clarification_type="repository_required"
)
```

### Error Response (Unknown Data Type)

```python
IntentProcessingResult(
    success=False,
    message="Cannot analyze data: unsupported data type 'xyz'. Supported types: repository_metrics, activity_trends, contributor_stats",
    intent_data={
        "category": "analysis",
        "action": "analyze_data",
        "data_type": "xyz"
    },
    workflow_id=str,
    requires_clarification=True,
    clarification_type="unsupported_data_type"
)
```

### Error Response (Exception)

```python
IntentProcessingResult(
    success=False,
    message=f"Failed to analyze data: {str(e)}",
    intent_data={
        "category": "analysis",
        "action": "analyze_data",
        "data_type": str
    },
    workflow_id=str,
    error=str(e),
    error_type="AnalysisError"
)
```

---

## Part 2.4: Implementation Design

### Main Handler Structure

```python
async def _handle_analyze_data(
    self, intent: Intent, workflow_id: str
) -> IntentProcessingResult:
    """
    Handle general data analysis requests.

    Analyzes repository data and returns structured insights based on data_type.
    Supports: repository_metrics, activity_trends, contributor_stats

    GREAT-4D Phase 2C: Third ANALYSIS handler - FULLY IMPLEMENTED
    """
    try:
        from services.domain.github_domain_service import GitHubDomainService

        # Extract and validate parameters
        repository = intent.context.get("repository")
        data_type = intent.context.get("data_type", "repository_metrics")

        # Validate required parameters
        if not repository:
            return IntentProcessingResult(...)  # Error response

        # Validate data_type
        supported_types = ["repository_metrics", "activity_trends", "contributor_stats"]
        if data_type not in supported_types:
            return IntentProcessingResult(...)  # Error response

        # Get timeframe parameters
        days = intent.context.get("days", 7)
        timeframe = intent.context.get("timeframe", f"last {days} days")

        # Get GitHub service and fetch data
        github_service = GitHubDomainService()
        activity = await github_service._github_agent.get_recent_activity(days=days)

        # Route to appropriate analysis helper
        if data_type == "repository_metrics":
            result_data = self._analyze_repository_metrics(activity, repository, days, timeframe, intent)
        elif data_type == "activity_trends":
            result_data = self._analyze_activity_trends(activity, repository, days, timeframe, intent)
        elif data_type == "contributor_stats":
            result_data = self._analyze_contributor_stats(activity, repository, days, timeframe, intent)

        # Return success
        return IntentProcessingResult(
            success=True,
            message=result_data["message"],
            intent_data=result_data["intent_data"],
            workflow_id=workflow_id,
            requires_clarification=False  # ← CRITICAL
        )

    except Exception as e:
        self.logger.error(f"Failed to analyze data: {e}", exc_info=True)
        return IntentProcessingResult(...)  # Error response
```

### Helper Method 1: Repository Metrics

```python
def _analyze_repository_metrics(
    self,
    activity: Dict[str, List[Dict[str, Any]]],
    repository: str,
    days: int,
    timeframe: str,
    intent: Intent
) -> Dict[str, Any]:
    """
    Analyze repository metrics from activity data.

    Helper method for _handle_analyze_data.
    Returns dict with 'message' and 'intent_data' keys.
    """
    # Extract counts
    commits = activity.get("commits", [])
    prs = activity.get("prs", [])
    issues_created = activity.get("issues_created", [])
    issues_closed = activity.get("issues_closed", [])

    commit_count = len(commits)
    pr_count = len(prs)
    issues_created_count = len(issues_created)
    issues_closed_count = len(issues_closed)
    total_activity = commit_count + pr_count + issues_created_count + issues_closed_count

    # Calculate distribution percentages
    distribution = {}
    if total_activity > 0:
        distribution = {
            "commits": round((commit_count / total_activity) * 100, 1),
            "prs": round((pr_count / total_activity) * 100, 1),
            "issues_created": round((issues_created_count / total_activity) * 100, 1),
            "issues_closed": round((issues_closed_count / total_activity) * 100, 1)
        }

    # Build message
    message = f"Analyzed repository metrics for {repository} over {timeframe}: {total_activity} total activities ({commit_count} commits, {pr_count} PRs, {issues_created_count} issues created, {issues_closed_count} issues closed)"

    # Build intent_data
    intent_data = {
        "category": intent.category.value,
        "action": intent.action,
        "confidence": intent.confidence,
        "repository": repository,
        "data_type": "repository_metrics",
        "timeframe": timeframe,
        "days": days,
        "metrics": {
            "total_activity_count": total_activity,
            "commits_count": commit_count,
            "prs_count": pr_count,
            "issues_created_count": issues_created_count,
            "issues_closed_count": issues_closed_count,
            "activity_distribution": distribution
        }
    }

    return {"message": message, "intent_data": intent_data}
```

### Helper Method 2: Activity Trends

```python
def _analyze_activity_trends(
    self,
    activity: Dict[str, List[Dict[str, Any]]],
    repository: str,
    days: int,
    timeframe: str,
    intent: Intent
) -> Dict[str, Any]:
    """
    Analyze activity trends from activity data.

    Helper method for _handle_analyze_data.
    Returns dict with 'message' and 'intent_data' keys.
    """
    # Extract counts (same as metrics)
    commits = activity.get("commits", [])
    prs = activity.get("prs", [])
    issues_created = activity.get("issues_created", [])
    issues_closed = activity.get("issues_closed", [])

    commit_count = len(commits)
    pr_count = len(prs)
    issues_created_count = len(issues_created)
    issues_closed_count = len(issues_closed)
    total_activity = commit_count + pr_count + issues_created_count + issues_closed_count

    # Analyze trends
    trends = {}
    insights = []

    # Most active type
    activity_types = {
        "commits": commit_count,
        "prs": pr_count,
        "issues_created": issues_created_count,
        "issues_closed": issues_closed_count
    }
    most_active = max(activity_types, key=activity_types.get) if total_activity > 0 else "none"
    trends["most_active_type"] = most_active

    # Issue closure rate
    total_issue_activity = issues_created_count + issues_closed_count
    if total_issue_activity > 0:
        closure_rate = (issues_closed_count / total_issue_activity) * 100
        trends["issue_closure_rate"] = round(closure_rate, 1)
        insights.append(f"Issue closure rate: {round(closure_rate, 1)}%")

    # Commit velocity
    if days > 0:
        commit_velocity = commit_count / days
        trends["commit_velocity"] = f"{round(commit_velocity, 1)} commits/day"
        insights.append(f"Commit velocity: {round(commit_velocity, 1)} commits/day")

    # PR activity
    if pr_count > 0:
        trends["pr_activity"] = f"{pr_count} PRs updated"
        insights.append(f"Active PR development ({pr_count} PRs)")

    # Most active insight
    if total_activity > 0:
        insights.insert(0, f"Most active in {most_active} ({activity_types[most_active]} total)")

    # Build message
    message = f"Analyzed activity trends for {repository} over {timeframe}: {total_activity} total activities, most active in {most_active}"

    # Build intent_data
    intent_data = {
        "category": intent.category.value,
        "action": intent.action,
        "confidence": intent.confidence,
        "repository": repository,
        "data_type": "activity_trends",
        "timeframe": timeframe,
        "days": days,
        "metrics": {
            "total_activity_count": total_activity,
            "commits_count": commit_count,
            "prs_count": pr_count,
            "issues_created_count": issues_created_count,
            "issues_closed_count": issues_closed_count
        },
        "trends": trends,
        "insights": insights
    }

    return {"message": message, "intent_data": intent_data}
```

### Helper Method 3: Contributor Stats

```python
def _analyze_contributor_stats(
    self,
    activity: Dict[str, List[Dict[str, Any]]],
    repository: str,
    days: int,
    timeframe: str,
    intent: Intent
) -> Dict[str, Any]:
    """
    Analyze contributor statistics from activity data.

    Helper method for _handle_analyze_data.
    Returns dict with 'message' and 'intent_data' keys.
    """
    commits = activity.get("commits", [])
    prs = activity.get("prs", [])
    issues_created = activity.get("issues_created", [])
    issues_closed = activity.get("issues_closed", [])

    # Analyze commit authors
    commit_authors = {}
    for commit in commits:
        author = commit.get("author", "Unknown")
        commit_authors[author] = commit_authors.get(author, 0) + 1

    # Analyze PR authors
    pr_authors = {}
    for pr in prs:
        author = pr.get("author", "Unknown")
        pr_authors[author] = pr_authors.get(author, 0) + 1

    # Analyze issue authors (created and closed)
    issue_authors = {}
    for issue in issues_created + issues_closed:
        author = issue.get("author", "Unknown")
        issue_authors[author] = issue_authors.get(author, 0) + 1

    # Get unique contributors
    all_contributors = set()
    all_contributors.update(commit_authors.keys())
    all_contributors.update(pr_authors.keys())
    all_contributors.update(issue_authors.keys())

    # Build insights
    insights = []
    total_contributors = len(all_contributors)
    insights.append(f"{total_contributors} total contributor{'s' if total_contributors != 1 else ''} across all activities")

    if commit_authors:
        top_committer = max(commit_authors, key=commit_authors.get)
        insights.append(f"{top_committer} is most active committer ({commit_authors[top_committer]} commits)")

    if len(all_contributors) > 1:
        insights.append("Collaboration across commits, PRs, and issues")

    # Build message
    message = f"Analyzed contributor stats for {repository} over {timeframe}: {total_contributors} total contributor{'s' if total_contributors != 1 else ''}"

    # Build intent_data
    intent_data = {
        "category": intent.category.value,
        "action": intent.action,
        "confidence": intent.confidence,
        "repository": repository,
        "data_type": "contributor_stats",
        "timeframe": timeframe,
        "days": days,
        "metrics": {
            "total_contributors": total_contributors,
            "commit_authors": len(commit_authors),
            "pr_authors": len(pr_authors),
            "issue_authors": len(issue_authors)
        },
        "contributors": {
            "commits": commit_authors,
            "prs": pr_authors,
            "issues": issue_authors
        },
        "insights": insights
    }

    return {"message": message, "intent_data": intent_data}
```

---

## Part 2.5: Quality Requirements

### Validation Requirements
- ✅ Repository parameter validation (required)
- ✅ Data type validation (must be in supported list)
- ✅ Helpful error messages for missing/invalid parameters
- ✅ Appropriate `requires_clarification` values

### Error Handling Requirements
- ✅ Try/except wrapper around all logic
- ✅ Logging with `exc_info=True` for stack traces
- ✅ Specific error types (`AnalysisError`)
- ✅ Graceful handling of empty data (no crashes)

### Response Requirements
- ✅ `success=True` for successful analysis
- ✅ `requires_clarification=False` for completed work (NOT TRUE!)
- ✅ Rich `intent_data` with analysis results
- ✅ Human-readable `message` summarizing results
- ✅ Consistent structure across all analysis types

### Code Quality Requirements
- ✅ Helper methods for different analysis types
- ✅ Clear separation of concerns
- ✅ No code duplication
- ✅ Comprehensive docstrings
- ✅ Type hints where appropriate

---

## Part 2.6: Test Strategy Preview

Tests will verify:

1. **Missing repository validation**
   - Returns `success=False`, `requires_clarification=True`
   - Helpful error message

2. **Unknown data type validation**
   - Returns `success=False`, `requires_clarification=True`
   - Lists supported types

3. **Repository metrics analysis**
   - Returns correct counts and distribution
   - `requires_clarification=False`

4. **Activity trends analysis**
   - Returns trends and insights
   - `requires_clarification=False`

5. **Contributor stats analysis**
   - Returns contributor breakdown
   - `requires_clarification=False`

6. **Empty data handling**
   - Graceful handling of zero activity
   - No crashes

7. **Exception handling**
   - Returns proper error response
   - Logs with stack trace

---

## Summary

**Scope Defined**: ✅

**Analysis Types**: 3
1. `repository_metrics` - Comprehensive activity overview
2. `activity_trends` - Activity patterns and velocity
3. `contributor_stats` - Contributor analysis

**Data Source**: `get_recent_activity()` from GitHubAgent

**Helper Methods**: 3
- `_analyze_repository_metrics()`
- `_analyze_activity_trends()`
- `_analyze_contributor_stats()`

**Response Structure**: Consistent across all types with `metrics`, optional `trends`, optional `contributors`, optional `insights`

**Quality Gates**: All validation, error handling, and quality requirements defined

**Next**: Part 3 - Write comprehensive tests (TDD red phase)

**Status**: Ready to proceed with thorough test writing

**Time**: 1:15 PM (30 minutes for Part 2)
