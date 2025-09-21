# GitHub Reporting Service Extension Proposal

**Date**: 2025-09-13
**Status**: Draft
**Context**: Pragmatic CSV generation script → Proper architectural integration

## Background

A one-off script (`scripts/generate_issues_csv.py`) successfully generated GitHub issues CSV using existing `GitHubAgent` methods. This proposal outlines how to properly integrate this functionality into Piper's architecture following established patterns.

## Current State Analysis

### What Works Well

- ✅ **Existing Methods Sufficient**: `get_recent_issues()` + `get_closed_issues()` covered 93 issues
- ✅ **No Core Modifications Needed**: Leveraged existing GitHub integration patterns
- ✅ **Domain Service Pattern**: `GitHubDomainService` provides proper abstraction layer
- ✅ **Configuration Integration**: Uses established `PiperConfigLoader` patterns

### Architectural Gaps Identified

- ❌ **No Reporting Domain**: No dedicated service for data export/reporting operations
- ❌ **Script Isolation**: Functionality exists only as standalone script
- ❌ **Limited Pagination**: Current methods don't handle full repository history
- ❌ **Fixed Output Format**: Only CSV, no flexibility for other formats

## Proposed Architecture Extension

### 1. Create Reporting Domain Service

**File**: `services/domain/reporting_domain_service.py`

```python
class ReportingDomainService:
    """Domain service for data export and reporting operations"""

    def __init__(
        self,
        github_service: Optional[GitHubDomainService] = None,
        notion_service: Optional[NotionDomainService] = None
    ):
        self.github_service = github_service or GitHubDomainService()
        self.notion_service = notion_service or NotionDomainService()

    async def generate_github_issues_report(
        self,
        format: str = 'csv',
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate GitHub issues report in specified format"""

    async def generate_project_status_report(self) -> Dict[str, Any]:
        """Cross-service project status report"""
```

### 2. Extend GitHub Domain Service (Minimal)

**File**: `services/domain/github_domain_service.py`

Add single method for comprehensive issue fetching:

```python
async def get_issues_for_reporting(
    self,
    include_closed: bool = True,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Get issues optimized for reporting (combines existing methods)"""
    # Uses existing get_recent_issues() + get_closed_issues()
    # Handles deduplication and sorting
    # No new GitHub agent methods needed
```

### 3. Add CLI Command

**File**: `cli/commands/report.py`

```python
@click.group()
def report():
    """Generate reports from Piper data"""
    pass

@report.command()
@click.option('--format', default='csv', help='Output format')
@click.option('--output', help='Output file path')
async def github_issues(format, output):
    """Generate GitHub issues report"""
    reporting_service = ReportingDomainService()
    await reporting_service.generate_github_issues_report(format, output)
```

### 4. Add API Endpoint (Optional)

**File**: `services/api/reporting_routes.py`

```python
@router.get("/reports/github/issues")
async def get_github_issues_report(
    format: str = Query("json", enum=["json", "csv"]),
    reporting_service: ReportingDomainService = Depends()
):
    """API endpoint for GitHub issues report"""
```

## Implementation Strategy

### Phase 1: Domain Service Creation (Low Risk)

1. Create `ReportingDomainService` with GitHub issues method
2. Migrate script logic into domain service
3. Add comprehensive error handling and logging
4. Create unit tests for domain service

### Phase 2: CLI Integration (Medium Risk)

1. Add `cli/commands/report.py` with GitHub issues command
2. Update CLI main to include report commands
3. Add integration tests for CLI functionality

### Phase 3: API Integration (Optional)

1. Add reporting routes if API access needed
2. Add API documentation and examples

## Benefits of This Approach

### Architectural Alignment

- ✅ **Domain-Driven Design**: Reporting as distinct domain concern
- ✅ **Service Mediation**: Uses existing domain services, no direct integration access
- ✅ **Dependency Injection**: Follows established patterns for service composition
- ✅ **Error Handling**: Consistent with existing domain service patterns

### Extensibility

- ✅ **Multiple Formats**: Easy to add JSON, Excel, etc.
- ✅ **Cross-Service Reports**: Can combine GitHub + Notion + Calendar data
- ✅ **Configurable Output**: Different report types for different stakeholders
- ✅ **API Integration**: Can expose as web service if needed

### Maintenance

- ✅ **Testable**: Domain service can be unit tested independently
- ✅ **Reusable**: CLI and API can both use same domain service
- ✅ **Discoverable**: Part of standard CLI help and API documentation

## Migration Path

### Step 1: Extract Core Logic

Move business logic from script to `ReportingDomainService`:

- Issue fetching and deduplication
- CSV formatting and file writing
- Error handling and logging

### Step 2: Update Script

Convert script to thin wrapper around domain service:

```python
# scripts/generate_issues_csv.py becomes:
async def main():
    reporting_service = ReportingDomainService()
    await reporting_service.generate_github_issues_report('csv', 'docs/planning/issues.csv')
```

### Step 3: Add CLI Command

Provide user-friendly CLI interface:

```bash
python -m cli report github-issues --format csv --output docs/planning/issues.csv
```

## Risks and Mitigations

### Risk: Over-Engineering

**Mitigation**: Start with minimal domain service, add features incrementally

### Risk: Breaking Existing Patterns

**Mitigation**: Follow exact patterns from `GitHubDomainService` and `StandupOrchestrationService`

### Risk: Performance Impact

**Mitigation**: Use existing GitHub agent methods, no additional API calls

## Success Criteria

1. ✅ **Functionality Preserved**: Same CSV output as current script
2. ✅ **Architecture Compliance**: Follows DDD and domain service patterns
3. ✅ **Extensibility**: Easy to add new report types and formats
4. ✅ **Discoverability**: Available through CLI help and documentation
5. ✅ **Testability**: Comprehensive unit and integration test coverage

## Recommendation

**Implement Phase 1 immediately** - The domain service extraction is low-risk and provides immediate architectural benefits while preserving all existing functionality.

**Consider Phase 2 for next sprint** - CLI integration makes the functionality more discoverable and user-friendly.

**Defer Phase 3** - API integration only if external systems need programmatic access to reports.

---

_This proposal transforms a pragmatic one-off script into a proper architectural component while maintaining Piper's established patterns and principles._
