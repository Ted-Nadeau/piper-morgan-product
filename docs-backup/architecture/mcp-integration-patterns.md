# MCP Integration Patterns

**Date:** 2025-07-17
**Status:** Complete
**Implementation:** POC Phase Complete

## Overview

This document outlines the integration patterns used for Model Context Protocol (MCP) integration in Piper Morgan, ensuring clean separation of concerns, graceful degradation, and maintainable code.

## Core Integration Patterns

### 1. Feature Flag Pattern

**Purpose:** Safe rollout with immediate disable capability

```python
# Environment-based feature flag
mcp_enabled = os.getenv("ENABLE_MCP_FILE_SEARCH", "false").lower() == "true"

if not mcp_enabled:
    logger.debug("MCP content search disabled, returning filename matches only")
    return filename_matches[:limit]
```

**Benefits:**
- Zero-risk deployment
- Immediate rollback capability
- A/B testing support
- Performance isolation

### 2. Graceful Degradation Pattern

**Purpose:** Maintain functionality when MCP fails

```python
try:
    # Attempt MCP operation
    mcp_results = await mcp_manager.enhanced_file_search(query)
    return combine_results(mcp_results, filename_matches)
except Exception as e:
    logger.error(f"MCP search failed: {e}, falling back to filename search")
    return filename_matches[:limit]
```

**Benefits:**
- No user-facing failures
- Transparent fallback
- Maintains user experience
- Comprehensive error logging

### 3. Lazy Import Pattern

**Purpose:** Avoid import errors when MCP is disabled

```python
# Import MCP components only if enabled to avoid import errors
try:
    from services.mcp.resources import MCPResourceManager
    # Use MCP functionality
except ImportError:
    logger.warning("MCP not available, using fallback")
    return fallback_results
```

**Benefits:**
- No dependency requirements when disabled
- Cleaner error handling
- Reduced memory usage
- Optional feature isolation

### 4. Circuit Breaker Pattern

**Purpose:** Prevent cascading failures

```python
class MCPCircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = "closed"  # closed, open, half-open
        self.last_failure_time = None
```

**Benefits:**
- Prevents resource exhaustion
- Automatic recovery
- Configurable thresholds
- Performance protection

### 5. Composite Search Pattern

**Purpose:** Combine multiple search strategies

```python
# Combine results: content matches first, then filename matches
# Remove duplicates while preserving order
seen_ids = set()
combined_results = []

# Add content matches first (higher priority)
for file in content_matches:
    if file.id not in seen_ids:
        combined_results.append(file)
        seen_ids.add(file.id)

# Add filename matches that aren't already included
for file in filename_matches:
    if file.id not in seen_ids:
        combined_results.append(file)
        seen_ids.add(file.id)
```

**Benefits:**
- Enhanced search relevance
- No duplicate results
- Priority-based ranking
- Seamless integration

## Architecture Integration Points

### FileRepository Enhancement

**Pattern:** Extend existing methods with MCP capabilities

```python
async def search_files_with_content(self, session_id: str, query: str, limit: int = 10):
    """Enhanced search combining filename and content search"""
    # Get filename matches first (always available)
    filename_matches = await self.search_files_by_name(session_id, query)

    # Try MCP content search if enabled
    if mcp_enabled:
        mcp_results = await self._get_mcp_results(query, session_id)
        return self._combine_results(mcp_results, filename_matches, limit)

    return filename_matches[:limit]
```

**Benefits:**
- Backward compatibility
- Clear separation of concerns
- Consistent API
- Maintainable codebase

### FileResolver Scoring Enhancement

**Pattern:** Conditional scoring factor addition

```python
def _calculate_score(self, file: UploadedFile, intent: Intent) -> float:
    """Multi-factor scoring algorithm with optional content relevance"""
    if mcp_enabled:
        # With MCP: adjust weights to include content relevance
        # Factor 5: Content relevance (max 0.2) - NEW
        content_score = self._calculate_content_score(file, intent)
        total_score += content_score * 0.2
    else:
        # Without MCP: use original scoring weights
        # Original 4-factor scoring

    return min(total_score, 1.0)
```

**Benefits:**
- Weighted scoring approach
- Feature flag awareness
- Maintains scoring consistency
- Enhanced relevance when enabled

### FileQueryService Integration

**Pattern:** Service layer orchestration

```python
async def search_files(self, session_id: str, query: str, limit: int = 10):
    """Enhanced file search with content awareness"""
    try:
        # Use enhanced search method from FileRepository
        # This method handles MCP integration and fallback automatically
        files = await self.file_repository.search_files_with_content(
            session_id, query, limit
        )

        return {
            "success": True,
            "files": file_results,
            "search_type": "enhanced" if self._is_mcp_enabled() else "filename_only"
        }
    except Exception as e:
        logger.error(f"File search failed: {e}")
        return {"success": False, "error": str(e)}
```

**Benefits:**
- Consistent API response format
- Automatic MCP integration
- Comprehensive error handling
- Clear success/failure indication

## Performance Patterns

### 1. Timeout Management

```python
client_config = {
    "url": "stdio://./scripts/mcp_file_server.py",
    "timeout": 5.0  # 5-second timeout
}
```

### 2. Connection Pooling

```python
# Resource caching with TTL
self.resource_cache: Dict[str, Any] = {}
self.cache_ttl = 300  # 5 minutes
```

### 3. Performance Monitoring

```python
# Performance tracking
start_time = time.time()
search_duration = time.time() - search_start
total_duration = time.time() - start_time

logger.info(f"MCP search completed in {search_duration:.3f}s")
logger.info(f"Total duration: {total_duration:.3f}s")
```

## Error Handling Patterns

### 1. Comprehensive Logging

```python
logger.info(f"Starting MCP enhanced search for query: '{query}'")
logger.info(f"MCP content search completed in {search_duration:.3f}s, found {len(content_results)} results")
logger.error(f"MCP enhanced search failed after {duration:.3f}s: {e}")
```

### 2. Error Classification

```python
class MCPConnectionError(Exception):
    """MCP connection failed"""
    pass

class MCPTimeoutError(Exception):
    """MCP operation timed out"""
    pass

class MCPResourceNotFoundError(Exception):
    """MCP resource not found"""
    pass
```

### 3. Graceful Error Responses

```python
# Operations should handle disconnected state
resources = await client.list_resources()
assert resources == [], "List resources should return empty list when disconnected"

content = await client.get_resource("file://test")
assert content is None, "Get resource should return None when disconnected"
```

## Testing Patterns

### 1. Feature Flag Testing

```python
# Test with MCP disabled
with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "false"}):
    results = await repo.search_files_with_content("session123", "test query")
    assert isinstance(results, list)

# Test with MCP enabled but failing
with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "true"}):
    # Test failure scenarios
```

### 2. Mock-based Testing

```python
with patch("services.mcp.resources.MCPResourceManager") as mock_manager_class:
    mock_manager = Mock()
    mock_manager.initialize = AsyncMock(return_value=False)
    mock_manager_class.return_value = mock_manager

    # Test fallback behavior
```

### 3. Performance Testing

```python
# Latency benchmarks
MAX_ADDITIONAL_LATENCY = 0.5  # 500ms
MAX_FALLBACK_LATENCY = 0.1    # 100ms

# Test against success criteria
assert max_mcp_time <= MAX_ADDITIONAL_LATENCY
assert avg_fallback_time <= MAX_FALLBACK_LATENCY
```

## Configuration Patterns

### Environment Variables

```bash
# MCP Configuration (POC)
ENABLE_MCP_FILE_SEARCH=false
MCP_SERVER_URL=stdio://./scripts/mcp_file_server.py
MCP_TIMEOUT_SECONDS=5
```

### Default Configuration

```python
self.client_config = client_config or {
    "url": "stdio://./scripts/mcp_file_server.py",
    "timeout": 5.0
}
```

## Success Metrics

### Performance Benchmarks

- **Connection success rate**: >95%
- **Additional latency**: <500ms
- **Fallback latency**: <100ms
- **Search quality**: Improved relevance

### Error Handling

- **Graceful degradation**: 100% fallback success
- **Error response time**: <1s
- **Resource cleanup**: Complete on failure
- **User experience**: No failures visible to users

## Future Enhancements

### 1. Content Caching

```python
# Add content caching for frequently accessed files
self.content_cache: Dict[str, Tuple[str, float]] = {}  # uri -> (content, timestamp)
```

### 2. Advanced Scoring

```python
# Implement TF-IDF or other advanced scoring algorithms
def _calculate_advanced_relevance_score(self, content: str, query: str) -> float:
    # TF-IDF implementation
    pass
```

### 3. Multi-server Support

```python
# Support multiple MCP servers
self.mcp_servers = [
    {"url": "stdio://./scripts/mcp_file_server.py", "priority": 1},
    {"url": "tcp://localhost:8080", "priority": 2}
]
```

## Conclusion

The MCP integration patterns provide a robust, maintainable foundation for enhanced file search capabilities while maintaining backward compatibility and operational safety. The feature flag approach allows for safe experimentation and gradual rollout, while the comprehensive error handling ensures system stability.

**Key Principles:**
- **Safety First**: Feature flags and graceful degradation
- **Clean Code**: Clear separation of concerns
- **Performance**: Monitoring and optimization
- **Maintainability**: Consistent patterns and documentation
