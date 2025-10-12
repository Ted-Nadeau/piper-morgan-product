# Phase 3: Content Generation Requirements Study

**Date**: October 11, 2025, 1:50 PM
**Handler**: `_handle_generate_content`
**Purpose**: Part 1 - Study content generation requirements thoroughly

---

## Executive Summary

**Mission**: Implement first SYNTHESIS handler (`_handle_generate_content`) that creates new content artifacts vs ANALYSIS handlers that read/analyze data.

**Key Finding**: Substantial content generation infrastructure already exists in the codebase with 3 different approaches:
1. **Template-based** (issue_generator.py) - Simple, fast
2. **LLM-based** (content_generator.py) - Sophisticated, flexible
3. **Data-driven** (morning_standup.py) - Integrates multiple sources

**Decision**: Will use **hybrid approach** - template-based for speed with data integration from Phase 2C analysis results.

---

## Critical Questions Answered

### Question 1: What types of content should this generate?

**Recommended from prompt**: status_report, readme_section, issue_template

**Analysis of Each Type**:

#### A. Status Report
- **Purpose**: Generate markdown status report from repository data
- **Data Source**: Phase 2C `_handle_analyze_data` results (repository_metrics, activity_trends, contributor_stats)
- **Template**: Markdown with sections for metrics, trends, insights
- **Example Output**:
```markdown
# Status Report: test-org/test-repo

## Activity Overview (Last 7 Days)
- **Total Activity**: 45 events
- **Commits**: 30 (66.7%)
- **Pull Requests**: 8 (17.8%)
- **Issues Created**: 4 (8.9%)
- **Issues Closed**: 3 (6.7%)

## Activity Trends
- Most active in commits
- Issue closure rate: 75.0%
- Commit velocity: 4.3 commits/day

## Contributors
- 3 total contributors
- Alice (most active: 20 commits)
- Active collaboration across commits, PRs, issues
```

#### B. README Section
- **Purpose**: Generate README.md section (e.g., "## Installation", "## Usage")
- **Data Source**: Section type + optional context
- **Template**: Markdown with section-specific structure
- **Example Output**:
```markdown
## Installation

### Prerequisites
- Python 3.9+
- pip or poetry
- Git

### Quick Start
\`\`\`bash
git clone https://github.com/org/repo.git
cd repo
pip install -r requirements.txt
\`\`\`

### Verification
\`\`\`bash
python -m pytest tests/
\`\`\`
```

#### C. Issue Template
- **Purpose**: Generate GitHub issue template (.github/ISSUE_TEMPLATE/)
- **Data Source**: Template type (bug_report, feature_request, custom)
- **Template**: YAML frontmatter + markdown body
- **Example Output**:
```yaml
---
name: Bug Report
about: Report a bug to help us improve
title: "[BUG] "
labels: ["bug", "needs-triage"]
---

## Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., macOS 14.0]
- Python: [e.g., 3.9.6]
- Version: [e.g., 1.0.0]
```

**Decision**: Implement all 3 types for comprehensive SYNTHESIS capability.

---

### Question 2: What inputs are needed?

**Required Parameters**:
1. **content_type** (required) - Enum: "status_report", "readme_section", "issue_template"
2. **repository** (optional for status_report, not used for others)
3. Type-specific parameters:
   - status_report: `days` (default 7), `data_type` (default "repository_metrics")
   - readme_section: `section_type` (required) - "installation", "usage", "contributing", "testing"
   - issue_template: `template_type` (required) - "bug_report", "feature_request", "custom"

**Optional Parameters**:
- `title` - Custom title override
- `include_metadata` - Boolean (default True)

**Validation Rules**:
- `content_type` is required - return `requires_clarification=True` if missing
- Type-specific parameters validated per content type
- Unknown content_type returns `clarification_type="unsupported_content_type"`

---

### Question 3: How is content generated?

**Generation Approach**: Template-based with data integration (hybrid)

**Why Template-Based?**
1. **Fast**: No LLM calls needed (~100ms vs ~2-5 seconds)
2. **Deterministic**: Same inputs = same outputs (testable)
3. **Reliable**: No API failures, no hallucinations
4. **Maintainable**: Templates are readable and editable

**Why Not LLM-Based?**
- Slower (2-5 seconds per generation)
- Non-deterministic (hard to test)
- Requires API keys and network
- Can hallucinate incorrect information
- More complex error handling

**Generation Flow**:
```
1. Validate content_type and parameters
2. Route to appropriate helper method:
   - _generate_status_report()
   - _generate_readme_section()
   - _generate_issue_template()
3. Helper gathers data (if needed)
4. Helper applies template with data
5. Return IntentProcessingResult with generated content
```

**Data Integration**:
- **Status Report**: Calls Phase 2C `_handle_analyze_data` to get real metrics
- **README Section**: Uses predefined templates per section type
- **Issue Template**: Uses GitHub-standard YAML + markdown format

**Quality Checks**:
- Validate content is not empty
- Validate markdown formatting (if applicable)
- Ensure all placeholders are filled
- Check content length (warn if > 10KB)

---

### Question 4: What should the output contain?

**IntentProcessingResult Structure**:

```python
IntentProcessingResult(
    success=True,
    message="Generated status_report for test-org/test-repo",
    intent_data={
        "category": "SYNTHESIS",
        "action": "generate_content",
        "content_type": "status_report",
        "repository": "test-org/test-repo",
        "generated_content": "# Status Report...",  # THE ACTUAL CONTENT
        "content_length": 1234,
        "generation_time_ms": 150,
        "data_source": "repository_metrics",
        "metadata": {
            "generated_at": "2025-10-11T13:45:00Z",
            "days_analyzed": 7,
            "total_activity": 45
        }
    },
    workflow_id=workflow_id,
    requires_clarification=False,  # Success = False, NOT True
    # No clarification_type on success
)
```

**Key Fields**:
1. **generated_content** (string) - The actual content created (NOT placeholder)
2. **content_length** (int) - Character count of generated content
3. **generation_time_ms** (int) - How long generation took
4. **metadata** (dict) - Type-specific metadata about generation

**Success Criteria**:
- ✅ `requires_clarification=False` (not True!)
- ✅ `generated_content` contains real content (not "implementation in progress")
- ✅ Content is properly formatted (markdown/YAML)
- ✅ Content is not empty
- ✅ Metadata is populated

**Error Response**:
```python
IntentProcessingResult(
    success=False,
    message="Failed to generate content: missing content_type",
    intent_data={
        "category": "SYNTHESIS",
        "action": "generate_content"
    },
    workflow_id=workflow_id,
    error="Missing required parameter: content_type",
    error_type="ValidationError"
)
```

---

## Existing Content Generation Infrastructure

### 1. issue_generator.py (125 lines)

**Location**: `services/integrations/github/issue_generator.py`

**Approach**: Simple template-based generation

**Key Features**:
- Creates `IssueContent` dataclass (title, body, labels)
- Uses heuristics for label inference (bug/feature keywords)
- Generates structured markdown body with sections
- Fast and deterministic

**Relevance**: Good model for template-based approach

**Code Example**:
```python
def _generate_body(self, description: str, context: Dict[str, Any]) -> str:
    body_parts = []
    body_parts.append("## Description")
    body_parts.append(description)
    body_parts.append("")
    body_parts.append("## Acceptance Criteria")
    body_parts.append("- [ ] Issue is reproducible")
    # ...
    return "\n".join(body_parts)
```

---

### 2. content_generator.py (349 lines)

**Location**: `services/integrations/github/content_generator.py`

**Approach**: LLM-based generation with structured prompts

**Key Features**:
- Uses `LLMClient` for content generation
- Sophisticated prompt engineering
- JSON response format with validation
- Fallback to template-based on LLM failure
- Sanitization and validation

**Relevance**: Good for understanding LLM approach (NOT using for Phase 3)

**Code Example**:
```python
async def generate_issue_content(
    self, user_request: str, project_context: Optional[ProjectContext] = None
) -> Dict[str, Any]:
    prompt = self._build_content_generation_prompt(user_request, project_context)
    response = await self.llm_client.complete(
        task_type="github_content_generation",
        prompt=prompt,
        response_format="json"
    )
    content = self._parse_llm_response(response)
    return self._validate_and_sanitize(content)
```

---

### 3. morning_standup.py (612 lines)

**Location**: `services/features/morning_standup.py`

**Approach**: Data-driven generation with multiple integrations

**Key Features**:
- Generates `StandupResult` with multiple sections
- Integrates GitHub, session context, preferences
- Multiple generation methods (with_documents, with_issues, with_calendar)
- Rich metadata and performance tracking
- Graceful degradation on service failures

**Relevance**: Excellent model for data integration approach

**Code Example**:
```python
async def _generate_standup_content(
    self, user_id: str, session_context: Dict[str, Any],
    github_activity: Dict[str, Any], start_time: float
) -> StandupResult:
    yesterday_accomplishments = []
    for commit in github_activity.get("commits", []):
        yesterday_accomplishments.append(f"✅ {commit.get('message', '')}")

    today_priorities = []
    for repo in session_context.get("active_repos", ["piper-morgan"]):
        today_priorities.append(f"🎯 Continue work on {repo}")

    return StandupResult(
        user_id=user_id,
        generated_at=datetime.now(),
        yesterday_accomplishments=yesterday_accomplishments,
        today_priorities=today_priorities,
        # ...
    )
```

---

## Template Infrastructure

**Finding**: No dedicated template files exist in project root (only in .venv)

**Decision**: Implement templates inline within helper methods

**Why Inline?**
- Simpler for initial implementation
- Easier to test (no file I/O)
- Keeps code self-contained
- Can refactor to external files later if needed

**Template Storage Locations** (Future):
```
templates/
  synthesis/
    status_report.md.j2
    readme/
      installation.md.j2
      usage.md.j2
      contributing.md.j2
      testing.md.j2
    issue_templates/
      bug_report.yml
      feature_request.yml
```

---

## Design Decisions Summary

### ✅ Template-Based Generation
**Decision**: Use template-based approach with data integration
**Rationale**: Fast, deterministic, testable, reliable
**Trade-off**: Less flexible than LLM, but acceptable for structured content

### ✅ Three Content Types
**Decision**: Implement status_report, readme_section, issue_template
**Rationale**: Covers diverse use cases, demonstrates SYNTHESIS capability
**Trade-off**: More code to write, but comprehensive coverage

### ✅ Inline Templates
**Decision**: Implement templates as inline strings in helper methods
**Rationale**: Simpler for initial implementation, can refactor later
**Trade-off**: Less separation of concerns, but acceptable for MVP

### ✅ Data Integration
**Decision**: Leverage Phase 2C analysis for status reports
**Rationale**: Reuses existing functionality, demonstrates integration
**Trade-off**: Dependency on Phase 2C, but that's production-ready

### ✅ Comprehensive Metadata
**Decision**: Include rich metadata in intent_data
**Rationale**: Useful for debugging, monitoring, user feedback
**Trade-off**: Larger response size, but marginal

---

## Implementation Structure

### Main Handler: `_handle_generate_content`

**Location**: `services/intent/intent_service.py` (replace lines 1259-1283)

**Structure**:
```python
async def _handle_generate_content(
    self, intent: Intent, workflow_id: str
) -> IntentProcessingResult:
    """Handle content generation requests - SYNTHESIS category."""
    try:
        # 1. Validate content_type (required)
        content_type = intent.context.get("content_type")
        if not content_type:
            return IntentProcessingResult(
                success=False,
                message="Content type is required for content generation.",
                requires_clarification=True,
                clarification_type="content_type_required",
                # ...
            )

        # 2. Validate content_type is supported
        valid_types = ["status_report", "readme_section", "issue_template"]
        if content_type not in valid_types:
            return IntentProcessingResult(
                success=False,
                message=f"Unsupported content type: {content_type}",
                requires_clarification=True,
                clarification_type="unsupported_content_type",
                # ...
            )

        # 3. Route to appropriate helper
        start_time = time.time()

        if content_type == "status_report":
            result = await self._generate_status_report(intent, workflow_id)
        elif content_type == "readme_section":
            result = await self._generate_readme_section(intent, workflow_id)
        elif content_type == "issue_template":
            result = await self._generate_issue_template(intent, workflow_id)

        # 4. Add generation timing
        generation_time_ms = int((time.time() - start_time) * 1000)
        result.intent_data["generation_time_ms"] = generation_time_ms

        return result

    except Exception as e:
        self.logger.error(f"Failed to generate content: {e}", exc_info=True)
        return IntentProcessingResult(
            success=False,
            message=f"Content generation failed: {str(e)}",
            error=str(e),
            error_type="SynthesisError",
            # ...
        )
```

---

### Helper Method 1: `_generate_status_report`

**Purpose**: Generate status report from repository metrics

**Parameters**:
- repository (optional, default from user config)
- days (optional, default 7)
- data_type (optional, default "repository_metrics")

**Flow**:
1. Get repository from context or user config
2. Call `_handle_analyze_data` with repository and data_type
3. Extract metrics from analysis result
4. Apply status report template
5. Return IntentProcessingResult with generated markdown

**Expected Lines**: ~120-150

---

### Helper Method 2: `_generate_readme_section`

**Purpose**: Generate README.md section

**Parameters**:
- section_type (required) - "installation", "usage", "contributing", "testing"
- repository (optional, for context)

**Flow**:
1. Validate section_type
2. Select appropriate template based on section_type
3. Apply template (may include repository name)
4. Return IntentProcessingResult with generated markdown

**Expected Lines**: ~100-120

---

### Helper Method 3: `_generate_issue_template`

**Purpose**: Generate GitHub issue template

**Parameters**:
- template_type (required) - "bug_report", "feature_request", "custom"
- repository (optional, for context)

**Flow**:
1. Validate template_type
2. Select appropriate template
3. Apply template with YAML frontmatter + markdown body
4. Return IntentProcessingResult with generated content

**Expected Lines**: ~120-150

---

## Total Implementation Estimate

### Code Changes
- Main handler: ~100 lines
- Helper 1 (status_report): ~130 lines
- Helper 2 (readme_section): ~110 lines
- Helper 3 (issue_template): ~130 lines
- **Total**: ~470 lines

### Test Changes
- Test file: `tests/intent/test_synthesis_handlers.py` (new)
- Tests needed: ~12-15 tests
- Expected lines: ~800-1000 lines

### Documentation
- Part 1: Requirements study (this document) - ✅ DONE
- Part 2: Scope definition - PENDING
- Part 3: Test summary - PENDING
- Part 6: Completion report - PENDING

---

## Quality Requirements

### No Placeholders ✅
- All success responses return `requires_clarification=False`
- No "implementation in progress" messages
- No "handler ready" messages
- Real generated content in `generated_content` field

### Comprehensive Testing ✅
- Test handler existence
- Test validation (missing content_type, unknown content_type)
- Test all 3 content types with success paths
- Test edge cases (empty data, missing optional params)
- Test no placeholder responses
- Test content quality (not empty, proper format)

### Pattern Consistency ✅
- Follow ANALYSIS pattern from Phases 2, 2B, 2C
- Try/except wrapper
- Local service imports
- Parameter validation first
- Comprehensive error handling
- Logging with exc_info=True
- Specific error types

### Content Quality ✅
- Generated content is not empty
- Content is properly formatted (markdown/YAML)
- Content contains expected sections
- Metadata is accurate and complete

---

## Integration Points

### Phase 2C Integration
- **Helper**: `_handle_analyze_data`
- **Used By**: `_generate_status_report`
- **Purpose**: Get repository metrics for status report content
- **Validated**: Phase 2C is production-ready (100% tested)

### GitHubDomainService
- **May Use**: For additional repository metadata
- **Optional**: Not required for MVP
- **Future**: Can enhance with commit messages, PR titles, etc.

---

## Risk Assessment

### Low Risk ✅
- Template-based approach (simple, proven)
- Reuses Phase 2C functionality (tested)
- No external dependencies (LLM, APIs)
- Deterministic output (testable)

### Medium Risk ⚠️
- Content quality subjective (solved with tests)
- Template maintenance (inline for now, can refactor)

### High Risk 🚫
- None identified

---

## Next Steps

**Part 1**: ✅ COMPLETE (requirements study)
**Part 2**: Define content types and generation strategy (45 min)
**Part 3**: Write comprehensive tests - TDD red phase (45 min)
**Part 4**: Implement handler thoroughly (60-90 min)
**Part 5**: Run tests thoroughly - TDD green phase (30 min)
**Part 6**: Evidence collection (30 min)

---

## Questions Answered

✅ **Question 1**: What types of content should this generate?
**Answer**: status_report, readme_section, issue_template

✅ **Question 2**: What inputs are needed?
**Answer**: content_type (required), type-specific parameters (validated per type)

✅ **Question 3**: How is content generated?
**Answer**: Template-based with data integration (hybrid approach)

✅ **Question 4**: What should the output contain?
**Answer**: IntentProcessingResult with generated_content, metadata, timing

---

**Status**: Part 1 - ✅ COMPLETE
**Time**: 1:50 PM (11 minutes for Part 1)
**Next**: Part 2 - Define content types and generation strategy
**Ready**: Yes - all critical questions answered, existing capabilities understood
