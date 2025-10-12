# Phase 2C: ANALYSIS Pattern Study

**Date**: October 11, 2025, 1:00 PM
**Purpose**: Thoroughly understand ANALYSIS pattern before implementing _handle_analyze_data

---

## Existing ANALYSIS Handlers

### 1. `_handle_analyze_commits` (Phase 2) - Lines 652-747

**Parameters Accepted**:
- `repository` (required) - Repository name
- `days` (optional, default 7) - Number of days to analyze
- `timeframe` (optional) - Human-readable timeframe description

**Validation**:
- Validates repository is present
- Returns `success=False` with `requires_clarification=True` if missing
- Provides helpful error message: "Cannot analyze commits: repository not specified"

**Services Used**:
- `GitHubDomainService` (local import)
- `github_service._github_agent.get_recent_activity(days)`

**Data Processing**:
- Extracts commits from activity dict
- Analyzes authors (count per author)
- Extracts commit messages (first 100 chars, first 5 saved)
- Handles zero commits gracefully

**Response Structure**:
```python
IntentProcessingResult(
    success=True,
    message="Analyzed X commits in {repo}...",
    intent_data={
        "category": "analysis",
        "action": "analyze_commits",
        "confidence": 0.90,
        "repository": "repo-name",
        "commit_count": 45,
        "timeframe": "last 7 days",
        "days": 7,
        "authors": {"Alice": 30, "Bob": 15},
        "recent_messages": ["msg1", "msg2", ...]
    },
    workflow_id="test-123",
    requires_clarification=False  # ← Key: False for success
)
```

**Error Handling**:
- Try/except wraps everything
- Logs error with `exc_info=True` for stack trace
- Returns `IntentProcessingResult` with `success=False`, `error=str(e)`, `error_type="AnalysisError"`

**Key Characteristics**:
- **READS** data (doesn't modify)
- Provides **insights** from data (author distribution)
- Returns **structured analysis** (counts, summaries)
- **No placeholder markers** in success response

---

### 2. `_handle_generate_report` (Phase 2B) - Lines 749-895

**Parameters Accepted**:
- `repository` (required) - Repository name
- `report_type` (optional, default "commit_analysis") - Type of report
- `days` (optional, default 7) - Number of days to analyze
- `timeframe` (optional) - Human-readable timeframe description

**Validation**:
- Same pattern as analyze_commits
- Validates repository is present
- Returns `success=False` with `requires_clarification=True` if missing

**Services Used**:
- Same as analyze_commits: `GitHubDomainService`
- `github_service._github_agent.get_recent_activity(days)`

**Data Processing**:
- Reuses same data source as analyze_commits
- **Adds helper method**: `_format_commit_report()` (lines 847-895)
- Formats data as markdown report (not just raw data)
- Sections: title, metadata, summary, contributors, recent commits

**Response Structure**:
```python
IntentProcessingResult(
    success=True,
    message="Generated commit_analysis report for {repo}...",
    intent_data={
        "category": "analysis",
        "action": "generate_report",
        "confidence": 0.90,
        "repository": "repo-name",
        "report_type": "commit_analysis",
        "timeframe": "last 7 days",
        "days": 7,
        "commit_count": 45,
        "content": "# Report...",  # ← Markdown formatted
        "format": "markdown",
        "generated_at": "2025-10-11T12:00:00"
    },
    workflow_id="test-123",
    requires_clarification=False
)
```

**Error Handling**:
- Same pattern as analyze_commits
- `error_type="ReportError"` (specific to reports)

**Key Characteristics**:
- **READS** data (doesn't modify)
- **FORMATS** data for presentation (markdown)
- Uses **helper methods** for clean code separation
- Returns **human-readable output** (not just metrics)

---

### 3. `_handle_analyze_data` (Current Placeholder) - Lines 246-275

**Current State**:
```python
async def _handle_analyze_data(self, intent: Intent, workflow_id: str):
    """Handle general data analysis requests."""
    try:
        # Route to appropriate analysis based on context
        data_type = intent.context.get("data_type", "unknown")

        return IntentProcessingResult(
            success=True,
            message=f"Data analysis handler ready for {data_type} analysis",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "data_type": data_type,
            },
            workflow_id=workflow_id,
            requires_clarification=True,  # ← Placeholder marker
            clarification_type="analysis_parameters",
        )
    except Exception as e:
        self.logger.error(f"Failed to analyze data: {e}")
        return IntentProcessingResult(
            success=False,
            message=f"Failed to analyze data: {str(e)}",
            workflow_id=workflow_id,
            error=str(e),
            error_type="AnalysisError",
        )
```

**What Needs to Change**:
1. Remove `requires_clarification=True` placeholder marker
2. Add real data analysis logic
3. Support multiple data types (broader than just commits)
4. Return meaningful metrics and insights
5. Follow same pattern as Phase 2 & 2B

---

## ANALYSIS Pattern Summary

### Common Pattern Elements

**1. Structure**:
```python
async def _handle_[action](self, intent: Intent, workflow_id: str):
    """Docstring with FULLY IMPLEMENTED marker"""
    try:
        from services.domain.github_domain_service import GitHubDomainService

        # Extract and validate parameters
        required_param = intent.context.get("required_param")
        if not required_param:
            return IntentProcessingResult(
                success=False,
                message="Cannot [action]: [param] not specified...",
                intent_data={...},
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="[param]_required"
            )

        # Get optional parameters with defaults
        days = intent.context.get("days", 7)

        # Get service
        service = GitHubDomainService()

        # Fetch data
        data = await service.method()

        # Analyze/process data
        results = self._analyze_data(data)

        # Build response message
        message = f"[Summary of what was done]"

        # Return success
        return IntentProcessingResult(
            success=True,
            message=message,
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": intent.confidence,
                # ... analysis results ...
            },
            workflow_id=workflow_id,
            requires_clarification=False  # ← CRITICAL
        )

    except Exception as e:
        self.logger.error(f"Failed to [action]: {e}", exc_info=True)
        return IntentProcessingResult(
            success=False,
            message=f"Failed to [action]: {str(e)}",
            intent_data={...},
            workflow_id=workflow_id,
            error=str(e),
            error_type="[Category]Error"
        )
```

**2. Validation Pattern**:
- Extract required parameters first
- Check if present
- If missing: return `success=False`, `requires_clarification=True`
- Helpful error messages (guide user to fix)

**3. Service Pattern**:
- Local import of service (inside try block)
- Instantiate service
- Call async service methods
- Extract data from service response

**4. Analysis Pattern**:
- Process raw data into insights
- Calculate metrics (counts, averages, distributions)
- Extract meaningful information
- Use helper methods for complex processing

**5. Response Pattern**:
- `success=True` for successful analysis
- `requires_clarification=False` for completed work
- Rich `intent_data` with analysis results
- Human-readable `message` summarizing results

**6. Error Pattern**:
- Try/except wraps everything
- Log errors with stack trace
- Return `success=False` with error details
- Specific error types

---

## What Makes ANALYSIS vs EXECUTION?

### ANALYSIS Characteristics:
- **READS data** (doesn't modify state)
- **ANALYZES patterns** (finds insights)
- **AGGREGATES information** (summaries, counts, trends)
- **RETURNS insights** (not just confirmation)
- **Multiple outputs**: metrics, trends, insights, summaries

### EXECUTION Characteristics:
- **CREATES/UPDATES resources** (modifies state)
- **PERFORMS actions** (creates issues, updates tickets)
- **RETURNS confirmation** (what was done)
- **Single outcome**: resource created/updated

---

## Phase 2C Requirements

### What `_handle_analyze_data` Should Do:

**Broader scope than previous ANALYSIS handlers**:
1. Handle multiple data types (not just commits):
   - repository_metrics (issues, PRs, stats)
   - commit_stats (commit patterns)
   - issue_stats (issue trends)
2. Provide comprehensive analysis (not single-focus)
3. Support flexible queries
4. Return structured metrics

**Following the pattern**:
- Same validation approach
- Same service usage
- Same response structure
- Same error handling
- Add helper methods for different analysis types

**Quality requirements**:
- Thorough validation
- Helpful error messages
- Comprehensive logging
- Edge case handling
- No placeholder markers

---

## Critical Questions Answered

**1. What type of data?**
- GitHub repository data (issues, PRs, commits, stats)
- Multiple types supported via `data_type` parameter

**2. Where does data come from?**
- Same source as Phase 2/2B: `get_recent_activity()`
- Could expand to other service methods as needed

**3. What analysis?**
- Aggregation (counts, totals, averages)
- Trends (increasing/decreasing patterns)
- Distribution (how data is spread)

**4. What output?**
- Structured metrics dictionary
- Optional trends dictionary
- Optional insights list

**5. How different from analyze_commits?**
- **Broader scope**: Multiple data types vs single focus
- **Flexible**: data_type parameter determines analysis
- **Comprehensive**: Can analyze issues, PRs, commits together
- **Extensible**: Easy to add new data types

---

**Pattern Study Complete**: 1:05 PM
**Next**: Part 2 - Define data analysis scope in detail
**Status**: Ready to proceed with thorough design
