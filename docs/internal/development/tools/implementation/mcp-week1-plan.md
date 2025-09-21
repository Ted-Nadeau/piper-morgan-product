# MCP Week 1 Implementation Plan - Real Content Search

**Date:** 2025-07-17
**Duration:** 5 days
**Approach:** Test-Driven Development + Domain-Driven Design
**Status:** Feature Flag Protected (`ENABLE_MCP_FILE_SEARCH=false`)

## Executive Summary

Transform MCP POC from "fake content search" (filename matching) to **real content-based file search** using disciplined TDD/DDD practices. Focus on core value proposition: users can find files by their actual content, not just filenames.

## Domain Analysis

### Bounded Contexts Affected

```
┌─────────────────────────────────────────────────────────────┐
│                    File Search Context                     │
├─────────────────────────────────────────────────────────────┤
│ Aggregates:                                                 │
│ • FileSearchSession (root)                                  │
│ • ContentSearchResult                                       │
│ • SearchQuery                                               │
│                                                             │
│ Value Objects:                                              │
│ • ContentMatch                                              │
│ • RelevanceScore                                            │
│ • SearchParameters                                          │
└─────────────────────────────────────────────────────────────┘
                                │
                                │ integrates with
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                 MCP Integration Context                     │
├─────────────────────────────────────────────────────────────┤
│ Aggregates:                                                 │
│ • MCPConnectionPool (root)                                  │
│ • MCPResourceCatalog                                        │
│                                                             │
│ Domain Services:                                            │
│ • ContentExtractionService                                  │
│ • MCPConfigurationService                                   │
│                                                             │
│ Value Objects:                                              │
│ • MCPResource                                               │
│ • ContentExtract                                            │
│ • ConnectionPoolStatus                                      │
└─────────────────────────────────────────────────────────────┘
```

### Domain Events

```python
@dataclass
class ContentSearchRequested:
    """User requested content-based search"""
    session_id: str
    query: SearchQuery
    timestamp: datetime
    search_context: Dict[str, Any]

@dataclass
class ContentExtracted:
    """Content successfully extracted from file"""
    file_id: str
    content_extract: ContentExtract
    extraction_method: str  # "mcp" | "fallback"
    timestamp: datetime

@dataclass
class SearchResultsGenerated:
    """Search completed with results"""
    session_id: str
    query: SearchQuery
    results: List[ContentSearchResult]
    performance_metrics: Dict[str, float]
    timestamp: datetime

@dataclass
class MCPConnectionPoolStatusChanged:
    """Connection pool status changed"""
    pool_id: str
    old_status: ConnectionPoolStatus
    new_status: ConnectionPoolStatus
    timestamp: datetime
```

### Key Aggregates & Value Objects

```python
# Domain Model Structure
services/domain/
├── content_search/
│   ├── models.py              # SearchQuery, ContentSearchResult
│   ├── services.py            # ContentSearchService (domain service)
│   └── events.py              # Domain events
├── mcp_integration/
│   ├── models.py              # MCPResource, ContentExtract
│   ├── connection_pool.py     # MCPConnectionPool aggregate
│   └── configuration.py       # MCPConfigurationService
└── shared/
    └── value_objects.py       # RelevanceScore, ContentMatch
```

## TDD Implementation Sequence

### Test-First Development Order

```
1. Domain Model Tests → Domain Models
2. Domain Service Tests → Domain Services
3. Repository Tests → Repository Implementation
4. Integration Tests → Infrastructure Integration
5. End-to-End Tests → API Integration
```

**Rule: No production code without failing test first**

## Week 1 Scope Definition

### MUST HAVE (Week 1)

#### 1. Real Content Extraction ⭐ **CRITICAL**
- Extract actual text content from uploaded files
- Support text files (.txt, .md), PDFs, Word docs initially
- Return actual content matches, not filename matches
- **Success Criteria**: Search for "project timeline" finds documents containing those words

#### 2. Connection Pooling ⭐ **CRITICAL**
- Singleton MCPConnectionPool managing connections
- Prevent resource leaks from POC
- Handle connection failures gracefully
- **Success Criteria**: Only 1 connection per process, automatic retry logic

#### 3. Centralized Configuration ⭐ **IMPORTANT**
- MCPConfigurationService replacing scattered feature flag checks
- Single source of truth for MCP settings
- Environment-based configuration with validation
- **Success Criteria**: Change feature flag in one place, affects entire system

#### 4. Performance Monitoring ⭐ **IMPORTANT**
- Structured metrics for content extraction time
- Search latency tracking with P95/P99 metrics
- Connection pool health monitoring
- **Success Criteria**: <500ms total search latency maintained

### EXPLICITLY DEFERRED (Future Weeks)
- Multiple file format support beyond basic text/PDF
- Advanced relevance scoring algorithms
- Multiple MCP server support
- Complex authentication mechanisms
- UI feedback indicators
- A/B testing infrastructure

## Daily Implementation Breakdown

### Day 1: Domain Models + Content Extraction Core
**TDD Focus: Content extraction domain logic**

**Morning (3h): Domain Model Design**
```bash
# Test files to create
tests/domain/content_search/test_search_query.py
tests/domain/content_search/test_content_search_result.py
tests/domain/mcp_integration/test_content_extract.py

# Implementation files
services/domain/content_search/models.py
services/domain/mcp_integration/models.py
```

**Test Cases**:
```python
def test_search_query_validates_minimum_length():
    # Query must be at least 3 characters

def test_content_extract_calculates_relevance_score():
    # Given content and query, calculates TF-IDF score

def test_content_search_result_ranks_by_relevance():
    # Results automatically sort by relevance score
```

**Afternoon (4h): Content Extraction Service**
```bash
# Test files
tests/domain/content_search/test_content_extraction_service.py

# Implementation
services/domain/content_search/content_extraction_service.py
```

**Test Cases**:
```python
def test_extract_content_from_text_file():
    # Can extract plain text content

def test_extract_content_from_pdf():
    # Can extract text from PDF files

def test_handles_unsupported_file_types():
    # Gracefully handles binary files

def test_content_extraction_timeout():
    # Times out large files appropriately
```

**Exit Criteria**: Content can be extracted from basic file types with proper domain modeling

### Day 2: Connection Pooling + MCP Client Enhancement
**TDD Focus: Connection management and pooling**

**Morning (3h): MCPConnectionPool Aggregate**
```bash
# Test files
tests/domain/mcp_integration/test_mcp_connection_pool.py
tests/infrastructure/mcp/test_pooled_mcp_client.py

# Implementation
services/domain/mcp_integration/connection_pool.py
services/infrastructure/mcp/pooled_client.py
```

**Test Cases**:
```python
def test_connection_pool_singleton_behavior():
    # Only one pool instance per process

def test_connection_pool_manages_max_connections():
    # Respects connection limits

def test_connection_pool_handles_failures():
    # Removes failed connections, creates new ones

def test_pooled_client_reuses_connections():
    # Doesn't create new connection per request
```

**Afternoon (4h): Integration with Existing MCP Code**
```bash
# Refactor existing MCP client to use pool
services/mcp/client.py  # Enhance existing
services/mcp/resources.py  # Update to use pooled client
```

**Test Cases**:
```python
def test_mcp_resource_manager_uses_pool():
    # ResourceManager gets connections from pool

def test_pool_cleanup_on_shutdown():
    # Properly closes all connections on cleanup
```

**Exit Criteria**: All MCP operations use connection pooling, resource leaks eliminated

### Day 3: FileRepository Integration + Real Content Search
**TDD Focus: Repository layer with real content search**

**Morning (3h): Enhanced Repository Methods**
```bash
# Test files
tests/repositories/test_content_search_repository.py

# Implementation
services/repositories/content_search_repository.py
# Enhance existing FileRepository
services/repositories/file_repository.py
```

**Test Cases**:
```python
def test_search_by_content_returns_matching_files():
    # Search "budget analysis" finds files containing those words

def test_content_search_excludes_irrelevant_files():
    # Doesn't return files that only match filename

def test_content_search_with_relevance_scoring():
    # Results ordered by content relevance, not just filename

def test_content_search_fallback_behavior():
    # Falls back to filename search when content extraction fails
```

**Afternoon (4h): Integration with Content Extraction**
```bash
# Wire together: Repository → ContentExtractionService → MCPClient → Files
```

**Test Cases**:
```python
def test_end_to_end_content_search():
    # Upload file with content, search finds it by content

def test_mixed_results_filename_and_content():
    # Combines filename matches and content matches appropriately

def test_performance_under_load():
    # Handles multiple concurrent content searches
```

**Exit Criteria**: Users can search for actual content in files, not just filenames

### Day 4: Configuration Service + Error Handling
**TDD Focus: Centralized configuration and robust error handling**

**Morning (3h): MCPConfigurationService**
```bash
# Test files
tests/domain/mcp_integration/test_mcp_configuration_service.py

# Implementation
services/domain/mcp_integration/configuration_service.py
```

**Test Cases**:
```python
def test_configuration_validates_mcp_settings():
    # Validates URLs, timeouts, etc.

def test_configuration_provides_feature_flags():
    # Single source for ENABLE_MCP_FILE_SEARCH

def test_configuration_environment_overrides():
    # Environment variables override defaults

def test_configuration_change_propagation():
    # Configuration changes propagate to all components
```

**Afternoon (4h): Replace Scattered Feature Flag Checks**
```bash
# Refactor all files using os.getenv("ENABLE_MCP_FILE_SEARCH")
# to use MCPConfigurationService instead
services/repositories/file_repository.py
services/file_context/file_resolver.py
services/queries/file_queries.py
```

**Test Cases**:
```python
def test_all_components_use_centralized_config():
    # No more scattered os.getenv() calls

def test_config_service_injection():
    # All components receive config via dependency injection
```

**Exit Criteria**: Single configuration source, no scattered feature flag checks

### Day 5: Performance Optimization + Monitoring
**TDD Focus: Performance optimization and comprehensive monitoring**

**Morning (3h): Performance Optimization**
```bash
# Test files
tests/performance/test_content_search_performance.py

# Implementation - fix N+1 queries and add caching
services/repositories/file_repository.py  # Batch operations
services/infrastructure/mcp/content_cache.py  # New caching layer
```

**Test Cases**:
```python
def test_batch_file_content_extraction():
    # Extracts content from multiple files in single operation

def test_content_caching_reduces_repeat_extractions():
    # Same file content not extracted multiple times

def test_search_latency_under_500ms():
    # Total search time < 500ms for typical queries

def test_memory_usage_stays_bounded():
    # Memory doesn't grow unbounded with cache
```

**Afternoon (4h): Monitoring & Metrics**
```bash
# Test files
tests/infrastructure/test_mcp_metrics.py

# Implementation
services/infrastructure/monitoring/mcp_metrics.py
```

**Test Cases**:
```python
def test_metrics_track_search_latency():
    # P50, P95, P99 latency tracking

def test_metrics_track_content_extraction_success_rate():
    # Success/failure rates for content extraction

def test_metrics_track_connection_pool_health():
    # Pool size, active connections, failures
```

**Exit Criteria**: Production-ready performance and comprehensive monitoring

## Test Strategy

### Test Structure

```
tests/
├── unit/
│   ├── domain/
│   │   ├── content_search/
│   │   │   ├── test_search_query.py
│   │   │   ├── test_content_search_result.py
│   │   │   └── test_content_extraction_service.py
│   │   └── mcp_integration/
│   │       ├── test_mcp_connection_pool.py
│   │       ├── test_content_extract.py
│   │       └── test_mcp_configuration_service.py
│   └── repositories/
│       └── test_content_search_repository.py
├── integration/
│   ├── test_mcp_content_search_integration.py
│   ├── test_connection_pool_integration.py
│   └── test_configuration_service_integration.py
├── performance/
│   ├── test_content_search_performance.py
│   └── test_connection_pool_performance.py
└── contracts/
    ├── test_file_query_service_api.py
    └── test_mcp_client_contracts.py
```

### Test Pyramid

```
                    ▲
                   /E2E\
                  /  5  \
                 /______\
                /        \
               /Integration\
              /     20     \
             /______________\
            /                \
           /      Unit        \
          /        75         \
         /____________________\
```

**Unit Tests (75%)**:
- Fast, isolated, test domain logic
- Mock all external dependencies
- Focus on business rules and edge cases

**Integration Tests (20%)**:
- Test component interactions
- Real database connections
- Verify contract compliance

**End-to-End Tests (5%)**:
- Full workflow validation
- Real MCP server interactions
- Performance validation

### Test Quality Gates

**Every test must**:
- ✅ Run in <100ms (unit) or <5s (integration)
- ✅ Be deterministic (no flaky tests)
- ✅ Test behavior, not implementation
- ✅ Have clear arrange/act/assert structure
- ✅ Include both happy path and error cases

**Definition of Done**:
- All tests pass
- Code coverage >85%
- No performance regressions
- Feature flag allows safe rollback

## Technical Specification

### New Classes/Interfaces

#### Domain Layer
```python
# services/domain/content_search/models.py
@dataclass
class SearchQuery:
    text: str
    session_id: str
    search_type: SearchType = SearchType.HYBRID
    max_results: int = 10

    def validate(self) -> List[str]:
        """Return validation errors"""

@dataclass
class ContentSearchResult:
    file_id: str
    filename: str
    content_matches: List[ContentMatch]
    relevance_score: RelevanceScore
    search_source: SearchSource  # FILENAME | CONTENT | HYBRID

# services/domain/content_search/services.py
class ContentExtractionService:
    async def extract_text_content(self, file_path: str) -> ContentExtract:
        """Extract searchable text from file"""

    async def calculate_relevance_score(self, content: str, query: SearchQuery) -> RelevanceScore:
        """Calculate TF-IDF based relevance score"""

# services/domain/mcp_integration/connection_pool.py
class MCPConnectionPool:
    def __init__(self, max_connections: int = 5):
        """Singleton connection pool"""

    async def get_connection(self) -> MCPConnection:
        """Get connection from pool"""

    async def return_connection(self, connection: MCPConnection):
        """Return connection to pool"""

    async def health_check(self) -> ConnectionPoolStatus:
        """Check pool health"""

# services/domain/mcp_integration/configuration_service.py
class MCPConfigurationService:
    def is_mcp_enabled(self) -> bool:
        """Single source of truth for MCP enablement"""

    def get_connection_config(self) -> ConnectionConfig:
        """Get connection configuration"""

    def get_performance_budgets(self) -> PerformanceBudgets:
        """Get performance limits"""
```

#### Infrastructure Layer
```python
# services/infrastructure/mcp/pooled_client.py
class PooledMCPClient:
    def __init__(self, connection_pool: MCPConnectionPool):
        """MCP client using connection pool"""

    async def search_content(self, query: str) -> List[MCPResource]:
        """Search content using pooled connection"""

# services/infrastructure/mcp/content_cache.py
class MCPContentCache:
    async def get_content(self, file_id: str) -> Optional[str]:
        """Get cached content"""

    async def set_content(self, file_id: str, content: str, ttl: int = 3600):
        """Cache content with TTL"""

# services/infrastructure/monitoring/mcp_metrics.py
class MCPMetrics:
    def record_search_latency(self, duration_ms: float):
        """Record search latency"""

    def record_extraction_success(self, file_type: str, success: bool):
        """Record extraction success/failure"""

    def record_pool_stats(self, active: int, available: int):
        """Record connection pool statistics"""
```

### Enhanced Existing Classes

```python
# services/repositories/file_repository.py - Enhanced methods
class FileRepository:
    async def search_files_by_content(
        self,
        query: SearchQuery
    ) -> List[ContentSearchResult]:
        """NEW: Real content-based search using domain services"""

    async def batch_extract_content(
        self,
        file_ids: List[str]
    ) -> Dict[str, ContentExtract]:
        """NEW: Batch content extraction to eliminate N+1 queries"""

# services/queries/file_queries.py - Enhanced methods
class FileQueryService:
    def __init__(
        self,
        file_repository: FileRepository,
        config_service: MCPConfigurationService,
        metrics: MCPMetrics
    ):
        """ENHANCED: Dependency injection for config and metrics"""
```

### Performance Budget

| Operation | Budget | Measurement |
|-----------|--------|-------------|
| Total search latency | <500ms | P95 |
| Content extraction | <200ms per file | P95 |
| Connection pool checkout | <10ms | P99 |
| Database query batch | <100ms | P95 |
| Cache hit ratio | >80% | Average |
| Memory usage (cache) | <100MB | Peak |

### Rollback Plan

**Immediate Rollback** (< 1 minute):
```bash
# Environment variable change
export ENABLE_MCP_FILE_SEARCH=false
# Restart services (if needed)
```

**Code Rollback** (< 15 minutes):
```bash
# Git revert to previous known-good commit
git revert <commit-range>
# Deploy previous version
```

**Monitoring Triggers for Rollback**:
- Search latency P95 > 500ms for 5 minutes
- Error rate > 5% for 3 minutes
- Memory usage > 200MB for 10 minutes
- Connection pool health < 80% for 5 minutes

## Success Criteria & Definition of Done

### Week 1 Success Metrics

**Functional Requirements**:
- ✅ Search for "project timeline" finds documents containing those exact words (not just filenames)
- ✅ Content extraction works for .txt, .md, .pdf files
- ✅ Connection pool maintains exactly 1-5 connections max
- ✅ All configuration centralized in MCPConfigurationService
- ✅ Performance budget maintained: <500ms search latency

**Technical Requirements**:
- ✅ Test coverage >85% for all new code
- ✅ All tests pass in CI/CD pipeline
- ✅ No memory leaks detected in 24h run
- ✅ Feature flag allows instant disable/enable
- ✅ Comprehensive monitoring and alerting

**Quality Requirements**:
- ✅ Code review approved by 2+ developers
- ✅ Architecture review approved by tech lead
- ✅ Performance testing shows no regressions
- ✅ Security review shows no new vulnerabilities
- ✅ Documentation updated and reviewed

### Risk Mitigation

**High Risk**: Content extraction performance
- **Mitigation**: Async processing, caching, file size limits
- **Fallback**: Disable content search, keep filename search

**Medium Risk**: Connection pool complexity
- **Mitigation**: Start with simple implementation, iterate
- **Fallback**: Fall back to per-request connections temporarily

**Low Risk**: Configuration service refactoring
- **Mitigation**: Gradual migration, keep old code parallel
- **Fallback**: Revert to environment variable approach

## Dependencies & Assumptions

**External Dependencies**:
- Python 3.9.6 (current - MCP SDK requires 3.10+ but we have simulation)
- PostgreSQL database (existing)
- Redis for caching (existing)
- File system access for content extraction

**Internal Dependencies**:
- Existing AsyncSessionFactory pattern (continue using)
- Current file upload mechanism (unchanged)
- Feature flag infrastructure (enhanced)

**Key Assumptions**:
- File upload volume remains manageable for content extraction
- Users primarily search text-based documents
- Content extraction can be done synchronously within performance budget
- MCP simulation mode sufficient for Week 1 (real MCP in future)

## Communication Plan

**Daily Standups**:
- Progress against daily milestones
- Blockers and assistance needed
- Test coverage and performance metrics

**Mid-week Check (Day 3)**:
- Demo real content search working
- Performance metrics review
- Scope adjustment if needed

**Week End Demo (Day 5)**:
- Live demonstration of content-based search
- Performance metrics presentation
- Production readiness assessment

---

**This plan prioritizes shipping working, tested, maintainable code over feature completeness. Week 1 success means users can actually search file content - everything else builds from there.**
