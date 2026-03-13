# Phase 3B Scope Definition: _handle_summarize Implementation

**Issue**: GREAT-4D Phase 3B - SYNTHESIS Handler (Summarization)
**Date**: 2025-10-11
**Duration**: Part 2 of 6 (Scope Definition - 45 min)

---

## Executive Summary

This document provides complete specifications for implementing `_handle_summarize` with 3 source types, 6 helper methods, and comprehensive test coverage. The implementation leverages existing LLM-based summarization infrastructure discovered in Part 1.

**Implementation Approach**: Orchestration handler that coordinates existing services (TextAnalyzer, GitHubDomainService, Phase 2C handlers) to create summaries from various sources.

---

## Table of Contents

1. [Source Type Specifications](#source-type-specifications)
2. [Helper Method Specifications](#helper-method-specifications)
3. [Main Handler Specification](#main-handler-specification)
4. [Test Specifications](#test-specifications)
5. [Integration Patterns](#integration-patterns)
6. [Implementation Checklist](#implementation-checklist)

---

## Source Type Specifications

### 1. GitHub Issue Summarization

#### Purpose
Summarize GitHub issue body and comments into concise format for quick understanding.

#### Parameters

**Required**:
```python
{
    "source_type": "github_issue",  # Literal
    "issue_url": str,                # Full GitHub URL
}
```

**OR**:
```python
{
    "source_type": "github_issue",
    "repository": str,               # Format: "owner/repo"
    "issue_number": int,             # Issue number
}
```

**Optional**:
```python
{
    "include_comments": bool = True,      # Include comments in summary
    "max_comments": int = 10,             # Maximum comments to include
    "length": str = "moderate",           # "brief" | "moderate" | "detailed"
    "format": str = "bullet_points",      # "bullet_points" | "paragraph" | "executive_summary"
}
```

#### Validation Rules

1. **issue_url XOR (repository + issue_number)**: One or the other required, not both
2. **issue_url format**: Must match `https://github.com/{owner}/{repo}/issues/{number}`
3. **repository format**: Must match `{owner}/{repo}` pattern
4. **issue_number**: Must be positive integer
5. **max_comments**: Must be >= 0, default 10
6. **include_comments**: Boolean, default True

#### Data Flow

```
User Request
    ↓
_handle_summarize
    ↓
_fetch_issue_content
    ├─ Extract issue_url OR repo/number
    ├─ Call GitHubDomainService.get_issue() or get_issue_by_url()
    ├─ Fetch issue: {title, body, comments, metadata}
    ├─ Filter comments (max_comments limit)
    └─ Format into content string
    ↓
_summarize_with_llm
    ├─ Build issue-specific prompt
    ├─ Call LLM with JSON mode
    ├─ Parse JSON → DocumentSummary
    └─ Return structured summary
    ↓
_format_summary
    ├─ Convert DocumentSummary → requested format
    └─ Return formatted string
    ↓
Build IntentProcessingResult
    └─ Return to user
```

#### Content Format (Input to LLM)

```markdown
# GitHub Issue Summary Request

**Issue**: #{issue_number} - {title}
**Repository**: {repository}
**Status**: {state}
**Created**: {created_at}
**Author**: {author}

## Issue Body

{body}

## Comments ({comment_count} total, showing {shown_count})

### Comment 1 by {author} ({created_at})
{comment_body}

### Comment 2 by {author} ({created_at})
{comment_body}

...
```

#### Expected Output Example

**bullet_points format**:
```markdown
## Summary: Issue #123 - API Performance Issues

### Key Points
- API response times increased 300% in production environment
- Root cause identified: N+1 database queries in user endpoint
- Proposed solution: Implement query optimization and Redis caching
- 3 team members confirmed experiencing the issue
- Priority: HIGH - actively affecting production users

### Discussion Highlights
- @alice suggested Redis caching layer (5 upvotes)
- @bob provided detailed profiling data showing query bottleneck
- Team consensus: implement fix in sprint 42
- @charlie volunteered to design caching architecture

### Next Steps
- Review profiling data in next team meeting
- Design document for caching layer due by Friday
- Implementation target: Sprint 42 (starts Oct 15)
```

#### Metadata

```python
{
    "source_metadata": {
        "issue_url": "https://github.com/owner/repo/issues/123",
        "issue_number": 123,
        "repository": "owner/repo",
        "issue_state": "open",
        "comment_count": 8,
        "comments_included": 8,
        "author": "username",
        "created_at": "2025-10-01T10:00:00Z",
    }
}
```

---

### 2. Commit Range Summarization

#### Purpose
Summarize multiple commit messages from a repository over a time period, categorizing by type (features, fixes, chores).

#### Parameters

**Required**:
```python
{
    "source_type": "commit_range",
    "repository": str,               # Format: "owner/repo"
}
```

**Optional**:
```python
{
    "days": int = 7,                      # Days to look back
    "timeframe": str = "last 7 days",     # Human-readable description
    "length": str = "moderate",           # "brief" | "moderate" | "detailed"
    "format": str = "bullet_points",      # "bullet_points" | "paragraph" | "executive_summary"
    "categorize": bool = True,            # Group by commit type (feat, fix, etc.)
}
```

#### Validation Rules

1. **repository**: Must match `{owner}/{repo}` pattern
2. **days**: Must be positive integer, reasonable range (1-90), default 7
3. **timeframe**: Optional string override for custom description
4. **categorize**: Boolean, default True (group commits by conventional commit types)

#### Data Flow

```
User Request
    ↓
_handle_summarize
    ↓
_fetch_commit_content
    ├─ Extract repository and timeframe
    ├─ Call _handle_analyze_commits (Phase 2C integration)
    ├─ Extract commit data from result
    ├─ Parse commit messages
    └─ Format into content string (categorized if requested)
    ↓
_categorize_commits (if enabled)
    ├─ Parse conventional commit prefixes (feat:, fix:, chore:, etc.)
    ├─ Group commits by category
    └─ Return categorized dict
    ↓
_summarize_with_llm
    ├─ Build commit-specific prompt
    ├─ Call LLM with JSON mode
    ├─ Parse JSON → DocumentSummary
    └─ Return structured summary
    ↓
_format_summary
    ├─ Convert DocumentSummary → requested format
    └─ Return formatted string
    ↓
Build IntentProcessingResult
    └─ Return to user
```

#### Content Format (Input to LLM)

**With Categorization** (default):
```markdown
# Commit Summary Request

**Repository**: owner/repo
**Timeframe**: Last 7 days
**Total Commits**: 25
**Authors**: alice (10), bob (8), charlie (7)

## Features (8 commits)
- feat(api): add user authentication endpoint
- feat(ui): implement dark mode toggle
- feat(search): add fuzzy search capability
...

## Bug Fixes (10 commits)
- fix(auth): resolve token expiration issue
- fix(api): handle null response in user endpoint
- fix(db): correct migration script for users table
...

## Chores (5 commits)
- chore(deps): update dependencies to latest versions
- chore(ci): add automated testing workflow
...

## Documentation (2 commits)
- docs(readme): update installation instructions
- docs(api): add API endpoint documentation
```

**Without Categorization**:
```markdown
# Commit Summary Request

**Repository**: owner/repo
**Timeframe**: Last 7 days
**Total Commits**: 25
**Authors**: alice (10), bob (8), charlie (7)

## Commits (chronological)
1. feat(api): add user authentication endpoint - alice - 2025-10-10
2. fix(auth): resolve token expiration issue - bob - 2025-10-10
3. feat(ui): implement dark mode toggle - charlie - 2025-10-09
...
```

#### Expected Output Example

**bullet_points format**:
```markdown
## Commit Summary: owner/repo (Last 7 Days)

### Overview
- 25 total commits from 3 contributors
- Primary focus: User authentication and UI improvements
- 8 new features, 10 bug fixes, 7 other changes

### Key Features Added
- User authentication system with JWT tokens
- Dark mode toggle for UI
- Fuzzy search capability across all content
- PDF export functionality

### Critical Bug Fixes
- Resolved token expiration causing logout issues
- Fixed null response handling in user endpoint
- Corrected database migration script

### Other Changes
- Updated dependencies to latest versions
- Added automated CI/CD testing workflow
- Improved API documentation

### Top Contributors
- alice: 10 commits (40%) - Primary focus on authentication
- bob: 8 commits (32%) - Bug fixes and infrastructure
- charlie: 7 commits (28%) - UI improvements
```

#### Metadata

```python
{
    "source_metadata": {
        "repository": "owner/repo",
        "commit_count": 25,
        "timeframe": "last 7 days",
        "days": 7,
        "authors": {
            "alice": 10,
            "bob": 8,
            "charlie": 7
        },
        "categories": {
            "feat": 8,
            "fix": 10,
            "chore": 5,
            "docs": 2
        }
    }
}
```

---

### 3. Text Summarization

#### Purpose
Summarize user-provided text or markdown content (general-purpose summarization).

#### Parameters

**Required**:
```python
{
    "source_type": "text",
    "content": str,                  # Text content to summarize
}
```

**Optional**:
```python
{
    "title": str = "Document",            # Title for the summary
    "document_type": str = "Text",        # Type hint (report, guide, etc.)
    "length": str = "moderate",           # "brief" | "moderate" | "detailed"
    "format": str = "bullet_points",      # "bullet_points" | "paragraph" | "executive_summary"
}
```

#### Validation Rules

1. **content**: Required, must be non-empty string
2. **content length**: Minimum 50 characters (too short to summarize)
3. **content length**: Maximum 10,000 characters (truncate if longer)
4. **title**: Optional string, default "Document"
5. **document_type**: Optional string, default "Text"

#### Data Flow

```
User Request
    ↓
_handle_summarize
    ↓
_extract_text_content
    ├─ Extract "content" from intent.context
    ├─ Validate content exists and meets minimum length
    ├─ Truncate if exceeds maximum length
    └─ Return content string
    ↓
_summarize_with_llm
    ├─ Build text-specific prompt
    ├─ Call LLM with JSON mode
    ├─ Parse JSON → DocumentSummary
    └─ Return structured summary
    ↓
_format_summary
    ├─ Convert DocumentSummary → requested format
    └─ Return formatted string
    ↓
Build IntentProcessingResult
    └─ Return to user
```

#### Content Format (Input to LLM)

```markdown
# Text Summary Request

**Title**: {title}
**Document Type**: {document_type}
**Length**: {char_count} characters

## Content

{content}
```

#### Expected Output Example

**bullet_points format**:
```markdown
## Summary: Project Requirements Document

### Key Points
- Project aims to build AI-powered task management system
- Target launch date: Q1 2026
- Budget allocated: $500K
- Team size: 5 developers, 2 designers, 1 PM

### Technical Requirements
- Backend: Python with FastAPI
- Frontend: React with TypeScript
- Database: PostgreSQL with Redis caching
- Deployment: AWS with Docker containers

### Success Criteria
- Support 10,000+ concurrent users
- 99.9% uptime SLA
- Response time < 200ms for 95th percentile
- Integration with 5+ third-party tools
```

#### Metadata

```python
{
    "source_metadata": {
        "title": "Project Requirements Document",
        "document_type": "Specification",
        "original_length": 5000,
        "provided_by": "user",
    }
}
```

---

## Helper Method Specifications

### 1. _fetch_issue_content

```python
async def _fetch_issue_content(
    self,
    context: Dict[str, Any]
) -> Tuple[str, Dict[str, Any]]:
    """
    Fetch and format GitHub issue content for summarization.

    Args:
        context: Intent context containing:
            - issue_url (str): Full GitHub issue URL
            OR
            - repository (str): Repository in "owner/repo" format
            - issue_number (int): Issue number

            Optional:
            - include_comments (bool): Include comments (default: True)
            - max_comments (int): Maximum comments to include (default: 10)

    Returns:
        Tuple of:
            - content (str): Formatted issue content for LLM
            - metadata (dict): Issue metadata (url, number, state, etc.)

    Raises:
        ValueError: If required parameters missing or invalid
        Exception: If GitHub API call fails

    Example:
        content, metadata = await self._fetch_issue_content({
            "issue_url": "https://github.com/owner/repo/issues/123",
            "include_comments": True,
            "max_comments": 5
        })
    """
    pass
```

**Implementation Steps**:
1. Extract parameters (issue_url OR repo/number)
2. Validate parameters format
3. Initialize GitHubDomainService
4. Fetch issue data (call get_issue_by_url or get_issue)
5. Extract issue fields (title, body, state, author, created_at)
6. Fetch comments if include_comments=True
7. Limit comments to max_comments
8. Format into markdown structure
9. Build metadata dict
10. Return (content, metadata)

**Error Handling**:
- Missing required parameters → ValueError
- Invalid URL format → ValueError
- GitHub API errors → Re-raise with context

---

### 2. _fetch_commit_content

```python
async def _fetch_commit_content(
    self,
    context: Dict[str, Any],
    workflow_id: str
) -> Tuple[str, Dict[str, Any]]:
    """
    Fetch and format commit data for summarization.

    Integrates with Phase 2C _handle_analyze_commits to get commit data.

    Args:
        context: Intent context containing:
            - repository (str): Repository in "owner/repo" format

            Optional:
            - days (int): Days to look back (default: 7)
            - timeframe (str): Human-readable timeframe
            - categorize (bool): Categorize commits by type (default: True)

        workflow_id: Current workflow ID for Phase 2C call

    Returns:
        Tuple of:
            - content (str): Formatted commit content for LLM
            - metadata (dict): Commit metadata (count, authors, categories, etc.)

    Raises:
        ValueError: If repository missing or invalid
        Exception: If Phase 2C call fails

    Example:
        content, metadata = await self._fetch_commit_content({
            "repository": "owner/repo",
            "days": 7,
            "categorize": True
        }, workflow_id)
    """
    pass
```

**Implementation Steps**:
1. Extract repository and timeframe parameters
2. Validate repository format
3. Build Intent for Phase 2C call
4. Call `self._handle_analyze_commits(intent, workflow_id)`
5. Extract commit data from result.intent_data
6. Get commits, authors, metadata
7. If categorize=True, call `_categorize_commits()`
8. Format into markdown structure (categorized or chronological)
9. Build metadata dict
10. Return (content, metadata)

**Error Handling**:
- Missing repository → ValueError
- Phase 2C call fails → Re-raise with context
- Empty commits → Return empty content with metadata

---

### 3. _extract_text_content

```python
def _extract_text_content(
    self,
    context: Dict[str, Any]
) -> Tuple[str, Dict[str, Any]]:
    """
    Extract and validate text content for summarization.

    Args:
        context: Intent context containing:
            - content (str): Text content to summarize

            Optional:
            - title (str): Title for summary (default: "Document")
            - document_type (str): Type hint (default: "Text")

    Returns:
        Tuple of:
            - content (str): Validated and possibly truncated content
            - metadata (dict): Content metadata (length, title, type)

    Raises:
        ValueError: If content missing, empty, or too short

    Example:
        content, metadata = self._extract_text_content({
            "content": "Long text to summarize...",
            "title": "Project Report",
            "document_type": "Report"
        })
    """
    pass
```

**Implementation Steps**:
1. Extract content from context
2. Validate content exists and is string
3. Check minimum length (>= 50 characters)
4. Truncate if > 10,000 characters (with warning log)
5. Extract optional title and document_type
6. Build metadata dict
7. Return (content, metadata)

**Error Handling**:
- Missing content → ValueError
- Empty content → ValueError
- Too short (< 50 chars) → ValueError
- Too long (> 10,000 chars) → Truncate and log warning

---

### 4. _summarize_with_llm

```python
async def _summarize_with_llm(
    self,
    content: str,
    source_type: str,
    length: str = "moderate",
    **kwargs
) -> DocumentSummary:
    """
    Summarize content using LLM with structured JSON output.

    Leverages existing summarization infrastructure (prompts, parser).

    Args:
        content: Formatted content to summarize
        source_type: Type of source ("github_issue", "commit_range", "text")
        length: Desired summary length ("brief", "moderate", "detailed")
        **kwargs: Additional metadata for prompt customization

    Returns:
        DocumentSummary: Structured summary with title, key_findings, sections

    Raises:
        Exception: If LLM call fails or parsing fails

    Example:
        doc_summary = await self._summarize_with_llm(
            content="Issue description and comments...",
            source_type="github_issue",
            length="moderate",
            issue_number=123,
            repository="owner/repo"
        )
    """
    pass
```

**Implementation Steps**:
1. Build source-specific prompt
   - For github_issue: Emphasize issue structure, discussions
   - For commit_range: Emphasize categorization, contributors
   - For text: Use general summarization prompt
2. Add length guidance to prompt
   - brief: 2-3 key points
   - moderate: 5-7 key points (default)
   - detailed: 10+ key points
3. Call LLM with JSON mode:
   ```python
   json_response = await self.llm_client.complete(
       task_type=TaskType.SUMMARIZE.value,
       prompt=prompt,
       response_format={"type": "json_object"}
   )
   ```
4. Parse JSON response with SummaryParser
5. Return DocumentSummary object

**Error Handling**:
- LLM call fails → Log error and re-raise
- JSON parsing fails → Log error and re-raise
- Invalid DocumentSummary → Log error and re-raise

---

### 5. _format_summary

```python
def _format_summary(
    self,
    doc_summary: DocumentSummary,
    format_type: str = "bullet_points"
) -> str:
    """
    Format DocumentSummary into requested output format.

    Args:
        doc_summary: Structured summary from LLM
        format_type: Output format ("bullet_points", "paragraph", "executive_summary")

    Returns:
        str: Formatted summary string

    Example:
        formatted = self._format_summary(doc_summary, "bullet_points")
        # Returns markdown with bullets

        formatted = self._format_summary(doc_summary, "paragraph")
        # Returns narrative paragraph
    """
    pass
```

**Implementation Steps**:

**bullet_points** (default):
- Use `doc_summary.to_markdown()` directly
- Already formatted as markdown with bullets

**paragraph**:
- Convert key_findings to narrative sentences
- Combine sections into flowing paragraphs
- Remove bullet points and headers
- Example:
  ```python
  sentences = []
  sentences.append(f"This document discusses {doc_summary.title}.")
  sentences.extend(doc_summary.key_findings)
  return " ".join(sentences)
  ```

**executive_summary**:
- Add executive structure:
  - Problem statement
  - Key findings
  - Recommendations
  - Next steps
- Use bold headers and structured format
- Example:
  ```markdown
  # Executive Summary: {title}

  ## Overview
  {first key finding}

  ## Key Points
  {remaining key findings as bullets}

  ## Recommendations
  {section points if available}
  ```

**Error Handling**:
- Unknown format_type → Default to bullet_points, log warning

---

### 6. _categorize_commits

```python
def _categorize_commits(
    self,
    commits: List[str]
) -> Dict[str, List[str]]:
    """
    Categorize commit messages by conventional commit type.

    Parses commit message prefixes according to Conventional Commits spec:
    - feat: New features
    - fix: Bug fixes
    - docs: Documentation changes
    - chore: Maintenance tasks
    - refactor: Code refactoring
    - test: Test additions/changes
    - style: Code style changes
    - perf: Performance improvements
    - ci: CI/CD changes

    Args:
        commits: List of commit messages

    Returns:
        Dict mapping category to list of commit messages
        Example: {
            "feat": ["feat(api): add endpoint", "feat: new feature"],
            "fix": ["fix(bug): resolve issue"],
            "other": ["update readme"]
        }

    Example:
        commits = [
            "feat(api): add user authentication",
            "fix(auth): resolve token issue",
            "update documentation"
        ]
        categories = self._categorize_commits(commits)
        # Returns: {
        #     "feat": ["feat(api): add user authentication"],
        #     "fix": ["fix(auth): resolve token issue"],
        #     "other": ["update documentation"]
        # }
    """
    pass
```

**Implementation Steps**:
1. Define category prefixes:
   ```python
   CATEGORIES = {
       "feat": "Features",
       "fix": "Bug Fixes",
       "docs": "Documentation",
       "chore": "Chores",
       "refactor": "Refactoring",
       "test": "Tests",
       "style": "Style",
       "perf": "Performance",
       "ci": "CI/CD"
   }
   ```
2. Initialize categories dict with empty lists
3. For each commit message:
   - Check if starts with `{category}:` or `{category}(`
   - If match, add to that category
   - If no match, add to "other" category
4. Return categories dict

**Error Handling**:
- Empty commits list → Return empty dict
- Malformed commits → Add to "other" category

---

## Main Handler Specification

### _handle_summarize

```python
async def _handle_summarize(
    self,
    intent: Intent,
    workflow_id: str
) -> IntentProcessingResult:
    """
    Handle summarization requests - FULLY IMPLEMENTED.

    Creates concise summaries of content from various sources. This is a SYNTHESIS
    operation that creates new condensed versions of existing content.

    Supported source_types:
        - 'github_issue': Summarize GitHub issue and comments
        - 'commit_range': Summarize commits from a time period
        - 'text': Summarize provided text content

    Args:
        intent: Intent object containing:
            - context: Dict with source_type and source-specific parameters
            - category: SYNTHESIS
            - action: "summarize"

        workflow_id: Current workflow ID for tracking

    Returns:
        IntentProcessingResult with:
            - success: True if summarization succeeded
            - message: Human-readable summary description
            - intent_data: Dict containing:
                - summary: The actual summary text
                - summary_format: Format type used
                - original_length: Original content length
                - summary_length: Summary length
                - compression_ratio: Ratio of summary to original
                - key_findings: List of key points
                - source_metadata: Source-specific metadata
            - requires_clarification: False (no placeholders)

    Example Usage:
        intent = Intent(
            original_message="summarize issue #123",
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            confidence=0.95,
            context={
                "source_type": "github_issue",
                "issue_url": "https://github.com/owner/repo/issues/123",
                "length": "moderate",
                "format": "bullet_points"
            }
        )

        result = await service._handle_summarize(intent, workflow_id)
        print(result.intent_data["summary"])  # Actual summary text

    Error Handling:
        - Missing source_type → requires_clarification
        - Unknown source_type → error response
        - Missing required parameters → requires_clarification
        - Content fetch fails → error response with details
        - LLM call fails → error response with details
        - Empty content → error response
    """
    try:
        # 1. VALIDATION
        source_type = intent.context.get("source_type")

        if not source_type:
            return IntentProcessingResult(
                success=False,
                message="Cannot summarize: source type not specified. Please specify 'github_issue', 'commit_range', or 'text'.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="source_type_required",
            )

        # Validate source_type
        valid_sources = ["github_issue", "commit_range", "text"]
        if source_type not in valid_sources:
            return IntentProcessingResult(
                success=False,
                message=f"Unknown source type '{source_type}'. Supported types: {', '.join(valid_sources)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "requested_source_type": source_type,
                },
                workflow_id=workflow_id,
                error=f"Unknown source type: {source_type}",
                error_type="ValidationError",
            )

        # 2. FETCH CONTENT based on source_type
        try:
            if source_type == "github_issue":
                content, source_metadata = await self._fetch_issue_content(intent.context)
            elif source_type == "commit_range":
                content, source_metadata = await self._fetch_commit_content(intent.context, workflow_id)
            elif source_type == "text":
                content, source_metadata = self._extract_text_content(intent.context)

            # Check for empty content
            if not content or len(content.strip()) < 50:
                return IntentProcessingResult(
                    success=False,
                    message=f"Content too short to summarize (< 50 characters). Please provide more content.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "source_type": source_type,
                    },
                    workflow_id=workflow_id,
                    error="Content too short",
                    error_type="ValidationError",
                )

        except ValueError as e:
            # Parameter validation errors
            return IntentProcessingResult(
                success=False,
                message=f"Validation error: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "source_type": source_type,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="parameter_validation",
                error=str(e),
                error_type="ValidationError",
            )

        # 3. SUMMARIZE with LLM
        length = intent.context.get("length", "moderate")

        doc_summary = await self._summarize_with_llm(
            content=content,
            source_type=source_type,
            length=length,
            **source_metadata
        )

        # 4. FORMAT summary
        format_type = intent.context.get("format", "bullet_points")
        formatted_summary = self._format_summary(doc_summary, format_type)

        # 5. CALCULATE metrics
        original_length = len(content)
        summary_length = len(formatted_summary)
        compression_ratio = summary_length / original_length if original_length > 0 else 0.0

        # 6. BUILD response
        return IntentProcessingResult(
            success=True,
            message=f"Summarized {source_type} successfully ({original_length} → {summary_length} chars, {compression_ratio:.1%} compression)",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": intent.confidence,

                # Summary content
                "summary": formatted_summary,
                "summary_format": format_type,
                "summary_length": summary_length,

                # Metrics
                "original_length": original_length,
                "compression_ratio": compression_ratio,

                # Structured data
                "title": doc_summary.title,
                "document_type": doc_summary.document_type,
                "key_findings": doc_summary.key_findings,

                # Source info
                "source_type": source_type,
                "source_metadata": source_metadata,

                # Timing
                "summarized_at": datetime.now().isoformat(),
            },
            workflow_id=workflow_id,
            requires_clarification=False,
        )

    except Exception as e:
        self.logger.error(f"Failed to summarize: {e}", exc_info=True)
        return IntentProcessingResult(
            success=False,
            message=f"Summarization failed: {str(e)}",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
            },
            workflow_id=workflow_id,
            error=str(e),
            error_type="SynthesisError",
        )
```

---

## Test Specifications

### Test File Location

**File**: `tests/intent/test_synthesis_handlers.py` (extend existing file from Phase 3)

### Test Structure

```python
class TestSynthesisHandlers:
    """Tests for SYNTHESIS category handlers."""

    # Phase 3 tests (already exist)
    # test_generate_content_* ...

    # Phase 3B tests (new)
    # test_summarize_* ...
```

### Test Cases

#### 1. test_summarize_handler_exists

```python
@pytest.mark.asyncio
async def test_summarize_handler_exists(mock_orchestration_engine):
    """Verify _handle_summarize exists and is not a placeholder."""
    service = IntentService(orchestration_engine=mock_orchestration_engine)

    # Handler should exist
    assert hasattr(service, "_handle_summarize")

    # Should be callable
    assert callable(service._handle_summarize)

    # Test with minimal intent
    intent = Intent(
        original_message="summarize this text",
        category=IntentCategory.SYNTHESIS,
        action="summarize",
        confidence=0.9,
        context={
            "source_type": "text",
            "content": "This is a test document with enough content to summarize properly."
        }
    )

    result = await service._handle_summarize(intent, "test_wf")

    # Should not be placeholder response
    assert result.requires_clarification is False
    assert "implementation in progress" not in result.message.lower()
    assert "summarization ready" not in result.message.lower()
```

#### 2. test_summarize_missing_source_type

```python
@pytest.mark.asyncio
async def test_summarize_missing_source_type(mock_orchestration_engine):
    """Test error handling when source_type is missing."""
    service = IntentService(orchestration_engine=mock_orchestration_engine)

    intent = Intent(
        original_message="summarize something",
        category=IntentCategory.SYNTHESIS,
        action="summarize",
        confidence=0.9,
        context={}  # No source_type
    )

    result = await service._handle_summarize(intent, "test_wf")

    assert result.success is False
    assert result.requires_clarification is True
    assert result.clarification_type == "source_type_required"
    assert "source type not specified" in result.message.lower()
```

#### 3. test_summarize_unknown_source_type

```python
@pytest.mark.asyncio
async def test_summarize_unknown_source_type(mock_orchestration_engine):
    """Test error handling for unsupported source type."""
    service = IntentService(orchestration_engine=mock_orchestration_engine)

    intent = Intent(
        original_message="summarize this",
        category=IntentCategory.SYNTHESIS,
        action="summarize",
        confidence=0.9,
        context={
            "source_type": "invalid_type"  # Unsupported
        }
    )

    result = await service._handle_summarize(intent, "test_wf")

    assert result.success is False
    assert result.error_type == "ValidationError"
    assert "unknown source type" in result.message.lower()
    assert "github_issue" in result.message  # Should list valid types
```

#### 4. test_summarize_github_issue_success

```python
@pytest.mark.asyncio
async def test_summarize_github_issue_success(mock_orchestration_engine, monkeypatch):
    """Test successful GitHub issue summarization."""
    service = IntentService(orchestration_engine=mock_orchestration_engine)

    # Mock GitHubDomainService
    mock_issue = {
        "number": 123,
        "title": "Test Issue",
        "body": "This is a test issue body with enough content to create a meaningful summary.",
        "state": "open",
        "user": {"login": "testuser"},
        "created_at": "2025-10-01T10:00:00Z",
        "comments": [
            {
                "user": {"login": "commenter1"},
                "body": "This is a test comment with some discussion about the issue.",
                "created_at": "2025-10-02T10:00:00Z"
            }
        ]
    }

    async def mock_get_issue(repo, number):
        return mock_issue

    monkeypatch.setattr(
        "services.domain.github_domain_service.GitHubDomainService.get_issue",
        mock_get_issue
    )

    # Mock LLM client
    mock_llm_response = {
        "title": "Test Issue Summary",
        "document_type": "GitHub Issue",
        "key_findings": [
            "Issue discusses test functionality",
            "User testuser reported the issue",
            "One comment provides additional context"
        ],
        "sections": []
    }

    async def mock_llm_complete(task_type, prompt, response_format=None):
        return json.dumps(mock_llm_response)

    service.llm_client = MagicMock()
    service.llm_client.complete = mock_llm_complete

    # Test intent
    intent = Intent(
        original_message="summarize issue #123",
        category=IntentCategory.SYNTHESIS,
        action="summarize",
        confidence=0.9,
        context={
            "source_type": "github_issue",
            "repository": "owner/repo",
            "issue_number": 123
        }
    )

    result = await service._handle_summarize(intent, "test_wf")

    # Verify success
    assert result.success is True
    assert result.requires_clarification is False

    # Verify summary content
    assert "summary" in result.intent_data
    assert len(result.intent_data["summary"]) > 0
    assert "test issue" in result.intent_data["summary"].lower()

    # Verify metadata
    assert result.intent_data["source_type"] == "github_issue"
    assert result.intent_data["source_metadata"]["issue_number"] == 123
    assert result.intent_data["compression_ratio"] < 1.0  # Summary is shorter
```

#### 5. test_summarize_commit_range_success

```python
@pytest.mark.asyncio
async def test_summarize_commit_range_success(mock_orchestration_engine, monkeypatch):
    """Test successful commit range summarization."""
    service = IntentService(orchestration_engine=mock_orchestration_engine)

    # Mock Phase 2C handler response
    mock_commit_result = IntentProcessingResult(
        success=True,
        message="Analyzed 5 commits",
        intent_data={
            "category": "analysis",
            "action": "analyze_commits",
            "commit_count": 5,
            "recent_messages": [
                "feat(api): add user endpoint",
                "fix(auth): resolve token issue",
                "docs: update readme",
                "feat(ui): add dark mode",
                "chore: update dependencies"
            ],
            "authors": {"alice": 3, "bob": 2}
        },
        workflow_id="test_wf"
    )

    async def mock_analyze_commits(intent, workflow_id):
        return mock_commit_result

    service._handle_analyze_commits = mock_analyze_commits

    # Mock LLM client
    mock_llm_response = {
        "title": "Commit Summary: owner/repo",
        "document_type": "Commit Range",
        "key_findings": [
            "5 commits in last 7 days",
            "2 new features added",
            "1 bug fix implemented",
            "Primary contributors: alice (3), bob (2)"
        ],
        "sections": []
    }

    async def mock_llm_complete(task_type, prompt, response_format=None):
        return json.dumps(mock_llm_response)

    service.llm_client = MagicMock()
    service.llm_client.complete = mock_llm_complete

    # Test intent
    intent = Intent(
        original_message="summarize commits from last week",
        category=IntentCategory.SYNTHESIS,
        action="summarize",
        confidence=0.9,
        context={
            "source_type": "commit_range",
            "repository": "owner/repo",
            "days": 7
        }
    )

    result = await service._handle_summarize(intent, "test_wf")

    # Verify success
    assert result.success is True
    assert result.requires_clarification is False

    # Verify summary
    assert "summary" in result.intent_data
    assert "5 commits" in result.intent_data["summary"].lower()

    # Verify metadata
    assert result.intent_data["source_type"] == "commit_range"
    assert result.intent_data["source_metadata"]["commit_count"] == 5
```

#### 6. test_summarize_text_success

```python
@pytest.mark.asyncio
async def test_summarize_text_success(mock_orchestration_engine):
    """Test successful text summarization."""
    service = IntentService(orchestration_engine=mock_orchestration_engine)

    # Mock LLM client
    mock_llm_response = {
        "title": "Project Requirements",
        "document_type": "Specification",
        "key_findings": [
            "Project aims to build task management system",
            "Target launch: Q1 2026",
            "Budget: $500K",
            "Team: 8 people"
        ],
        "sections": []
    }

    async def mock_llm_complete(task_type, prompt, response_format=None):
        return json.dumps(mock_llm_response)

    service.llm_client = MagicMock()
    service.llm_client.complete = mock_llm_complete

    # Test intent
    long_text = """
    This is a project requirements document for building an AI-powered task management system.
    The project is scheduled for launch in Q1 2026 with a total budget of $500,000.
    The team consists of 5 developers, 2 designers, and 1 project manager.
    The system must support 10,000+ concurrent users with 99.9% uptime SLA.
    """ * 10  # Make it longer

    intent = Intent(
        original_message="summarize this document",
        category=IntentCategory.SYNTHESIS,
        action="summarize",
        confidence=0.9,
        context={
            "source_type": "text",
            "content": long_text,
            "title": "Project Requirements",
            "document_type": "Specification"
        }
    )

    result = await service._handle_summarize(intent, "test_wf")

    # Verify success
    assert result.success is True
    assert result.requires_clarification is False

    # Verify summary
    assert "summary" in result.intent_data
    assert len(result.intent_data["summary"]) > 0
    assert len(result.intent_data["summary"]) < len(long_text)

    # Verify compression
    assert result.intent_data["compression_ratio"] < 1.0
```

#### 7. test_summarize_different_formats

```python
@pytest.mark.asyncio
async def test_summarize_different_formats(mock_orchestration_engine):
    """Test different output formats (bullet_points, paragraph, executive_summary)."""
    service = IntentService(orchestration_engine=mock_orchestration_engine)

    # Mock LLM response
    mock_llm_response = {
        "title": "Test Document",
        "document_type": "Test",
        "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
        "sections": []
    }

    async def mock_llm_complete(task_type, prompt, response_format=None):
        return json.dumps(mock_llm_response)

    service.llm_client = MagicMock()
    service.llm_client.complete = mock_llm_complete

    test_content = "This is test content. " * 50  # Make it long enough

    # Test bullet_points format
    intent_bullets = Intent(
        original_message="summarize",
        category=IntentCategory.SYNTHESIS,
        action="summarize",
        confidence=0.9,
        context={
            "source_type": "text",
            "content": test_content,
            "format": "bullet_points"
        }
    )

    result_bullets = await service._handle_summarize(intent_bullets, "test_wf")
    assert result_bullets.success is True
    assert result_bullets.intent_data["summary_format"] == "bullet_points"
    assert "- " in result_bullets.intent_data["summary"]  # Has bullet points

    # Test paragraph format
    intent_para = Intent(
        original_message="summarize",
        category=IntentCategory.SYNTHESIS,
        action="summarize",
        confidence=0.9,
        context={
            "source_type": "text",
            "content": test_content,
            "format": "paragraph"
        }
    )

    result_para = await service._handle_summarize(intent_para, "test_wf")
    assert result_para.success is True
    assert result_para.intent_data["summary_format"] == "paragraph"
    # Paragraph format should not have bullet points

    # Test executive_summary format
    intent_exec = Intent(
        original_message="summarize",
        category=IntentCategory.SYNTHESIS,
        action="summarize",
        confidence=0.9,
        context={
            "source_type": "text",
            "content": test_content,
            "format": "executive_summary"
        }
    )

    result_exec = await service._handle_summarize(intent_exec, "test_wf")
    assert result_exec.success is True
    assert result_exec.intent_data["summary_format"] == "executive_summary"
```

#### 8. test_summarize_empty_content

```python
@pytest.mark.asyncio
async def test_summarize_empty_content(mock_orchestration_engine):
    """Test error handling for empty or too-short content."""
    service = IntentService(orchestration_engine=mock_orchestration_engine)

    # Test empty content
    intent_empty = Intent(
        original_message="summarize",
        category=IntentCategory.SYNTHESIS,
        action="summarize",
        confidence=0.9,
        context={
            "source_type": "text",
            "content": ""
        }
    )

    result_empty = await service._handle_summarize(intent_empty, "test_wf")
    assert result_empty.success is False
    assert result_empty.error_type == "ValidationError"

    # Test too-short content
    intent_short = Intent(
        original_message="summarize",
        category=IntentCategory.SYNTHESIS,
        action="summarize",
        confidence=0.9,
        context={
            "source_type": "text",
            "content": "Too short"  # Less than 50 characters
        }
    )

    result_short = await service._handle_summarize(intent_short, "test_wf")
    assert result_short.success is False
    assert "too short" in result_short.message.lower()
```

---

## Integration Patterns

### Pattern 1: GitHub Service Integration

```python
# In _fetch_issue_content
from services.domain.github_domain_service import GitHubDomainService

github_service = GitHubDomainService()

# Option 1: Fetch by URL
if "issue_url" in context:
    issue = await github_service.get_issue_by_url(context["issue_url"])

# Option 2: Fetch by repo + number
elif "repository" in context and "issue_number" in context:
    issue = await github_service.get_issue(
        context["repository"],
        context["issue_number"]
    )
```

### Pattern 2: Phase 2C Integration

```python
# In _fetch_commit_content
from services.shared_types import IntentCategory

# Build intent for Phase 2C
commit_intent = Intent(
    original_message=f"analyze commits for {repository}",
    category=IntentCategory.ANALYSIS,
    action="analyze_commits",
    confidence=1.0,
    context={
        "repository": repository,
        "days": days
    }
)

# Call Phase 2C handler
commit_result = await self._handle_analyze_commits(commit_intent, workflow_id)

# Extract commit data
if commit_result.success:
    commits = commit_result.intent_data.get("recent_messages", [])
    authors = commit_result.intent_data.get("authors", {})
    commit_count = commit_result.intent_data.get("commit_count", 0)
```

### Pattern 3: LLM Summarization

```python
# In _summarize_with_llm
from services.prompts import get_json_summary_prompt
from services.analysis.summary_parser import SummaryParser
from services.shared_types import TaskType

# Build prompt
prompt_template = get_json_summary_prompt()
prompt = prompt_template.format(content=content[:3000])  # Truncate like TextAnalyzer

# Call LLM with JSON mode
json_response = await self.llm_client.complete(
    task_type=TaskType.SUMMARIZE.value,
    prompt=prompt,
    response_format={"type": "json_object"}
)

# Parse response
parser = SummaryParser()
doc_summary = parser.parse_json(json_response)

return doc_summary
```

---

## Implementation Checklist

### Phase 3B Implementation Tasks

- [ ] **Helper Method 1**: Implement `_fetch_issue_content`
- [ ] **Helper Method 2**: Implement `_fetch_commit_content`
- [ ] **Helper Method 3**: Implement `_extract_text_content`
- [ ] **Helper Method 4**: Implement `_summarize_with_llm`
- [ ] **Helper Method 5**: Implement `_format_summary`
- [ ] **Helper Method 6**: Implement `_categorize_commits`
- [ ] **Main Handler**: Implement `_handle_summarize` (replace placeholder)
- [ ] **Imports**: Add required imports at top of file
- [ ] **Logging**: Add structured logging for debugging
- [ ] **Error Handling**: Comprehensive try/except blocks

### Testing Tasks

- [ ] **Test 1**: `test_summarize_handler_exists`
- [ ] **Test 2**: `test_summarize_missing_source_type`
- [ ] **Test 3**: `test_summarize_unknown_source_type`
- [ ] **Test 4**: `test_summarize_github_issue_success`
- [ ] **Test 5**: `test_summarize_commit_range_success`
- [ ] **Test 6**: `test_summarize_text_success`
- [ ] **Test 7**: `test_summarize_different_formats`
- [ ] **Test 8**: `test_summarize_empty_content`
- [ ] **Run Tests**: Execute all tests and verify passing
- [ ] **Fix Bugs**: Iterate on any failures

### Documentation Tasks

- [ ] **Requirements Study**: ✅ COMPLETE (Part 1)
- [ ] **Scope Definition**: ✅ COMPLETE (Part 2)
- [ ] **Test Summary**: Create after Part 3
- [ ] **Completion Report**: Create after Part 6
- [ ] **Evidence Collection**: Sample outputs, metrics

---

## Conclusion

**Phase 3B Scope Definition is COMPLETE.**

This document provides complete specifications for:
- 3 source types (github_issue, commit_range, text)
- 6 helper methods with full signatures and docstrings
- 1 main handler with comprehensive logic
- 8 test cases covering all scenarios
- Integration patterns for existing infrastructure

**Ready to Proceed**: Part 3 (Write Comprehensive Tests - TDD Red Phase)

---

**Scope Definition Duration**: 45 minutes
**Status**: ✅ COMPLETE
**Next Part**: Part 3 - Write Tests (45 min)
