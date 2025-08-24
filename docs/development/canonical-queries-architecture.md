# Canonical Queries Architecture

## Overview

The Canonical Queries Architecture provides a systematic, extensible pattern for implementing intelligent query systems across Piper Morgan. This architecture enables consistent user experiences while allowing specialized implementations for different domains (issues, morning standups, etc.).

## Architecture Principles

### 1. Canonical Pattern Consistency
- All query engines implement consistent interfaces
- Standardized response structures preserve compatibility
- Enhancement is additive - original functionality never broken

### 2. Delegation Over Duplication
- New engines delegate to existing canonical handlers
- Core logic preserved in `CanonicalHandlers`
- Extensions add intelligence without reimplementation

### 3. Graceful Enhancement
- Failures in enhancement don't break core functionality
- Original responses always returned, enhancements are additive
- Clean degradation when external services unavailable

## Core Architecture

### Base Components

```
services/intent_service/canonical_handlers.py
├── CanonicalHandlers (Core Logic)
│   ├── handle() - Main delegation point
│   ├── _handle_identity_query() - "What's your name?"
│   ├── _handle_temporal_query() - "What day is it?"
│   ├── _handle_status_query() - "What am I working on?"
│   ├── _handle_priority_query() - "What's my top priority?"
│   └── _handle_guidance_query() - "What should I focus on?"
```

### Extension Pattern

```
services/features/issue_intelligence.py
├── IssueIntelligenceCanonicalQueryEngine (Extension)
│   ├── enhance_canonical_query() - Main enhancement point
│   ├── create_issue_intelligence_context() - Context builder
│   ├── _gather_issue_intelligence() - Data aggregation
│   └── _enhance_message_with_issues() - Message enhancement
├── IssueIntelligenceContext (Data Container)
└── IssueIntelligenceResult (Enhanced Response)
```

## Implementation Pattern

### 1. Core Canonical Handler (Unchanged)

The existing `CanonicalHandlers` class remains the source of truth:

```python
class CanonicalHandlers:
    async def handle(self, intent: Intent, session_id: str) -> Dict:
        # Core logic unchanged
        # Delegates based on intent.category
        # Returns standardized response structure
```

### 2. Enhancement Engine (New)

Enhancement engines extend functionality without modification:

```python
class IssueIntelligenceCanonicalQueryEngine:
    def __init__(self, github_integration, canonical_handlers, session_manager):
        self.canonical_handlers = canonical_handlers  # Delegate target
        self.github_integration = github_integration  # Enhancement data

    async def enhance_canonical_query(self, intent, session_id) -> IssueIntelligenceResult:
        # Step 1: Get original response (delegation)
        original_response = await self.canonical_handlers.handle(intent, session_id)

        # Step 2: Gather enhancement intelligence
        issue_intelligence = await self._gather_issue_intelligence(intent)

        # Step 3: Enhance message with additional context
        enhanced_message = await self._enhance_message_with_issues(
            original_response["message"], issue_intelligence, intent
        )

        # Step 4: Return enhanced result
        return IssueIntelligenceResult(
            original_response=original_response,      # Preserved
            enhanced_message=enhanced_message,        # Enhanced
            issue_intelligence=issue_intelligence     # Additional data
        )
```

### 3. Data Structures

**Context Object**: Contains enhancement data
```python
@dataclass
class IssueIntelligenceContext:
    user_id: str
    priority_level: str
    priority_issues: List[Dict[str, Any]]
    open_issues_count: int
    closed_issues_count: int
    assignee_context: Dict[str, Any]
```

**Result Object**: Contains enhanced response
```python
@dataclass
class IssueIntelligenceResult:
    original_response: Dict[str, Any]      # From CanonicalHandlers
    enhanced_message: str                  # With additional context
    issue_intelligence: Dict[str, Any]     # Enhancement data
    context_source: str = "github_integration"
    enhancement_time_ms: Optional[int] = None
```

## Extension Guidelines

### Creating New Canonical Query Extensions

1. **Implement Enhancement Engine**:
   ```python
   class YourCanonicalQueryEngine:
       def __init__(self, data_source, canonical_handlers, session_manager):
           self.canonical_handlers = canonical_handlers  # Always delegate
           self.data_source = data_source                # Your enhancement data

       async def enhance_canonical_query(self, intent, session_id):
           # Always delegate first
           original = await self.canonical_handlers.handle(intent, session_id)
           # Add your enhancements
           return YourEnhancedResult(...)
   ```

2. **Create Context and Result Objects**:
   ```python
   @dataclass
   class YourContext:
       # Your enhancement context data
       pass

   @dataclass
   class YourResult:
       original_response: Dict[str, Any]  # Always preserve original
       enhanced_message: str              # Your enhanced message
       your_intelligence: Dict[str, Any]  # Your additional data
   ```

3. **Implement Enhancement Logic**:
   ```python
   async def _gather_your_intelligence(self, intent: Intent) -> Dict[str, Any]:
       # Gather data based on intent category
       if intent.category == IntentCategory.PRIORITY:
           # Add priority-relevant enhancements
       elif intent.category == IntentCategory.STATUS:
           # Add status-relevant enhancements
       # Always handle gracefully
   ```

### Integration Points

**CLI Integration**:
```python
# cli/commands/your_feature.py
from services.features.your_feature import YourCanonicalQueryEngine

engine = YourCanonicalQueryEngine(
    data_source=your_data_source,
    canonical_handlers=canonical_handlers,
    session_manager=session_manager
)
```

**API Integration**:
```python
# Canonical queries work through any interface
intent = Intent(category=IntentCategory.PRIORITY, ...)
result = await engine.enhance_canonical_query(intent, session_id)

# Use enhanced_message for user display
print(result.enhanced_message)

# Access additional intelligence
analysis = result.your_intelligence
```

## Testing Strategy

### Test-Driven Development Pattern

1. **Write Failing Tests First**:
   ```python
   # tests/features/test_your_feature.py
   from services.features.your_feature import YourCanonicalQueryEngine

   async def test_enhancement_preserves_original():
       # Test that original response is preserved exactly
       assert result.original_response == expected_original

   async def test_enhancement_adds_intelligence():
       # Test that enhancements are additive
       assert result.enhanced_message != result.original_response["message"]
       assert result.your_intelligence is not None
   ```

2. **Test Graceful Degradation**:
   ```python
   async def test_enhancement_handles_failures():
       # Mock data source failure
       mock_data_source.side_effect = Exception("Service unavailable")

       # Verify original functionality still works
       result = await engine.enhance_canonical_query(intent, session_id)
       assert result.original_response is not None
       # Enhancement should gracefully indicate unavailability
   ```

3. **Test Integration Points**:
   ```python
   async def test_canonical_handlers_integration():
       # Verify delegation works correctly
       mock_canonical_handlers.handle.assert_called_once_with(intent, session_id)
   ```

### Test Coverage Requirements

- ✅ Original functionality preservation
- ✅ Enhancement addition without breaking changes
- ✅ Graceful degradation on data source failures
- ✅ Proper delegation to canonical handlers
- ✅ Context creation and data gathering
- ✅ Message enhancement logic

## Performance Considerations

### Response Time Optimization

**Target**: <150ms total response time for enhanced queries

**Strategy**:
1. **Parallel Processing**: Gather enhancement data while canonical handler executes
2. **Graceful Degradation**: Don't wait for slow enhancement data
3. **Caching**: Cache frequently accessed enhancement data
4. **Metrics**: Track enhancement time separately from core response time

**Implementation**:
```python
async def enhance_canonical_query(self, intent, session_id):
    start_time = time.time()

    # Run core and enhancement in parallel when possible
    original_task = self.canonical_handlers.handle(intent, session_id)
    enhancement_task = self._gather_enhancement_data(intent)

    original_response = await original_task
    try:
        enhancement_data = await asyncio.wait_for(enhancement_task, timeout=0.1)
    except asyncio.TimeoutError:
        enhancement_data = {"error": "Enhancement data temporarily unavailable"}

    enhancement_time_ms = int((time.time() - start_time) * 1000)
    # ... rest of enhancement logic
```

### Memory Management

- Use dataclasses with `field(default_factory=dict)` for efficient memory usage
- Clean up large enhancement data after response creation
- Stream data for large result sets rather than loading entirely into memory

## Security Considerations

### Data Access Controls

**GitHub Integration**:
- Respect repository access permissions
- Use appropriate token scopes (read-only when possible)
- Handle authentication failures gracefully
- Rate limit API calls to prevent abuse

**User Data**:
- Enhancement data should not expose sensitive information
- Filter out private repository data in multi-tenant deployments
- Respect user privacy preferences in learning systems

### Input Validation

```python
async def enhance_canonical_query(self, intent: Intent, session_id: str):
    # Validate inputs before processing
    if not isinstance(intent, Intent):
        raise ValueError("Invalid intent object")
    if not session_id or not isinstance(session_id, str):
        raise ValueError("Invalid session ID")

    # Sanitize any user-provided data in enhancement
```

## Monitoring and Observability

### Key Metrics

- **Response Time Distribution**: Core vs enhanced response times
- **Enhancement Success Rate**: Percentage of successful enhancements
- **Data Source Health**: Availability of enhancement data sources
- **User Adoption**: Usage patterns across different enhancement types

### Logging Standards

```python
import structlog
logger = structlog.get_logger(__name__)

async def enhance_canonical_query(self, intent, session_id):
    logger.info("Enhancement started",
                intent_category=intent.category.value,
                session_id=session_id)

    try:
        # Enhancement logic
        logger.info("Enhancement completed",
                    enhancement_time_ms=enhancement_time_ms,
                    data_sources_used=data_sources)
    except Exception as e:
        logger.error("Enhancement failed",
                     error=str(e),
                     fallback_used=True)
```

## Future Extensions

### Planned Canonical Extensions

1. **Project Intelligence**: Enhance queries with cross-project insights
2. **Time Intelligence**: Add time-based context and scheduling intelligence
3. **Team Intelligence**: Include team collaboration and capacity insights
4. **Performance Intelligence**: Add system health and performance context

### Extension API Evolution

The canonical query architecture is designed for evolution:

- **Backward Compatibility**: Original canonical handlers never change interface
- **Composable Enhancements**: Multiple enhancement engines can work together
- **Plugin Architecture**: Future extensions can be loaded dynamically
- **Cross-Feature Learning**: Enhancement engines can share learned patterns

## Migration Guide

### From Direct Canonical Handler Usage

**Before** (Direct usage):
```python
canonical_handlers = CanonicalHandlers()
response = await canonical_handlers.handle(intent, session_id)
```

**After** (Enhanced usage):
```python
github_agent = GitHubAgent()
canonical_handlers = CanonicalHandlers()
engine = IssueIntelligenceCanonicalQueryEngine(
    github_integration=github_agent,
    canonical_handlers=canonical_handlers,
    session_manager=session_manager
)
result = await engine.enhance_canonical_query(intent, session_id)
```

**Compatibility**: Original `response` structure available in `result.original_response`

### Adding Enhancement to Existing Features

1. Create enhancement engine following the pattern
2. Update CLI/API integration points to use enhancement engine
3. Preserve backward compatibility by ensuring original response available
4. Add comprehensive tests covering both enhanced and fallback scenarios

---

## Summary

The Canonical Queries Architecture provides a robust, extensible foundation for building intelligent query systems. By following the delegation pattern and enhancement principles, new capabilities can be added without breaking existing functionality, ensuring system reliability while enabling continuous improvement.

**Key Benefits**:
- **Consistency**: Uniform interface across all query types
- **Reliability**: Original functionality always preserved
- **Extensibility**: New capabilities easily added
- **Performance**: Optimal response times through parallel processing
- **Testability**: Clear separation enables comprehensive testing

This architecture has been proven with Issue Intelligence implementation and is ready for additional canonical query extensions.
