# Canonical Handlers Architecture

**Last Updated**: October 6, 2025
**Epic**: GREAT-4C - Remove Hardcoded User Context
**Status**: Production Ready

---

## Overview

The 5 canonical handlers provide natural language query responses for standup/basic queries with multi-user support, spatial intelligence, and robust error handling. They form the core of Piper Morgan's conversational interface for common user queries.

---

## Handler Capabilities

### 1. Identity Handler (\_handle_identity_query)

**Purpose**: "Who are you?" queries
**Spatial patterns**: EMBEDDED (brief) to GRANULAR (full capabilities)
**Data source**: Static identity info
**Error handling**: Always available (no external dependencies)

**Response Examples**:

- **EMBEDDED**: "Piper Morgan, AI PM Assistant" (29 chars)
- **GRANULAR**: Full capabilities list with features (509 chars)
- **DEFAULT**: Moderate introduction with key features

### 2. Temporal Handler (\_handle_temporal_query)

**Purpose**: "What day is it?" / time queries
**Spatial patterns**: Date only (EMBEDDED) to full calendar (GRANULAR)
**Data sources**: System time + calendar integration
**Error handling**: Works without calendar service

**Response Examples**:

- **EMBEDDED**: "Monday, October 06, 2025" (24 chars)
- **GRANULAR**: Full calendar breakdown with meetings (111 chars)
- **DEFAULT**: Date, time, and basic calendar info

**Error Handling**:

```python
try:
    calendar_data = await calendar_adapter.get_temporal_summary()
    # Process calendar data
except Exception as e:
    logger.warning(f"Calendar service unavailable: {e}")
    if spatial_pattern != "EMBEDDED":
        message += "\n\nNote: I couldn't access your calendar right now."
```

### 3. Status Handler (\_handle_status_query)

**Purpose**: "What am I working on?" queries
**Spatial patterns**: Brief list (EMBEDDED) to detailed status (GRANULAR)
**Data source**: User's PIPER.md projects
**Error handling**: Graceful fallback if PIPER.md missing

**Response Examples**:

- **EMBEDDED**: "3 active projects" (brief count)
- **GRANULAR**: Detailed project breakdown with context
- **DEFAULT**: Project list with moderate detail

**Error Handling**:

```python
try:
    user_context = await user_context_service.get_user_context(session_id)
except Exception as e:
    return {
        "message": "I'm having trouble accessing your configuration right now. "
                   "Your PIPER.md file may be missing or unreadable. "
                   "Would you like help setting it up?",
        "error": "config_unavailable",
        "action_required": "setup_piper_config"
    }
```

### 4. Priority Handler (\_handle_priority_query)

**Purpose**: "What's my top priority?" queries
**Spatial patterns**: Single priority (EMBEDDED) to full breakdown (GRANULAR)
**Data source**: User's PIPER.md priorities
**Error handling**: Offers to help configure if empty

**Response Examples**:

- **EMBEDDED**: "Complete GREAT-4C" (brief priority)
- **GRANULAR**: Priority breakdown with context and reasoning
- **DEFAULT**: Top priority with supporting details

**Empty Data Handling**:

```python
if not priorities:
    return {
        "message": "You don't have any priorities configured in your PIPER.md yet. "
                   "Would you like me to help you set up your priority list?",
        "action_required": "configure_priorities"
    }
```

### 5. Guidance Handler (\_handle_guidance_query)

**Purpose**: "What should I focus on?" queries
**Spatial patterns**: Brief (EMBEDDED) to comprehensive guidance (GRANULAR)
**Data sources**: Time of day + user context
**Error handling**: Falls back to generic time-based guidance

**Response Examples**:

- **EMBEDDED**: "Focus: Deep work" (16 chars)
- **GRANULAR**: Comprehensive guidance with timeframes (500 chars)
- **DEFAULT**: Time-based guidance with user context

**Fallback Pattern**:

```python
user_context = None
try:
    user_context = await user_context_service.get_user_context(session_id)
except Exception as e:
    logger.warning(f"Using generic guidance, user context unavailable: {e}")

# Provide time-based guidance with or without user context
if user_context and user_context.organization:
    focus = f"Morning work - focus on {user_context.organization} priorities"
else:
    focus = "Morning work - perfect time for deep focus and complex problem-solving"
```

---

## Multi-User Architecture

Each handler uses `UserContextService` to load user-specific data:

```python
user_context = await user_context_service.get_user_context(session_id)
# Returns: organization, projects, priorities for this user
```

**Key Principles**:

- **No hardcoded assumptions** - all context comes from user's PIPER.md
- **Session isolation** - each user gets their own context
- **Configuration-driven** - behavior adapts to user's setup

**Before GREAT-4C (WRONG)**:

```python
# This broke multi-user support!
if config and "VA" in str(config.values()):
    focus = "VA Q4 onramp implementation"
```

**After GREAT-4C (CORRECT)**:

```python
# This works for any user!
if user_context and user_context.organization:
    focus = f"Focus on {user_context.organization} priorities"
```

---

## Spatial Intelligence

Handlers adjust response detail based on spatial pattern:

```python
spatial_pattern = intent.spatial_context.get('pattern') if hasattr(intent, 'spatial_context') else None

if spatial_pattern == "GRANULAR":
    return detailed_response  # 450-550 chars
elif spatial_pattern == "EMBEDDED":
    return brief_response  # 15-30 chars
else:
    return standard_response  # 100-350 chars
```

**Use Cases**:

- **EMBEDDED**: Slack thread responses (brief, contextual)
- **GRANULAR**: Standalone detailed queries (comprehensive)
- **DEFAULT**: Helpful standard interactions (moderate detail)

**Performance Impact**:

- Reduces unnecessary verbosity in constrained contexts
- Provides comprehensive detail when requested
- Adapts to user's interaction mode automatically

---

## Error Handling

All handlers gracefully degrade with three main patterns:

### 1. Service Failures

Continue with fallback data when external services fail:

```python
try:
    external_data = await external_service.call()
    # Use external data
except Exception as e:
    logger.warning(f"Service unavailable: {e}")
    # Continue with basic response
```

### 2. Missing Data

Offer to help configure when user data is missing:

```python
if not user_data:
    return {
        "message": "You don't have X configured. Would you like help setting it up?",
        "action_required": "configure_X"
    }
```

### 3. Context Unavailable

Provide generic responses when user context fails:

```python
user_context = None
try:
    user_context = await get_context()
except Exception:
    pass  # Continue with generic response

# Adapt response based on context availability
if user_context:
    return personalized_response()
else:
    return generic_response()
```

**User Experience Benefits**:

- **No crashes**: System remains functional during failures
- **Helpful guidance**: Clear next steps for configuration issues
- **Graceful degradation**: Core functionality preserved

---

## Caching

Two-layer cache reduces file I/O and improves performance:

### 1. File-level (PiperConfigLoader)

- **TTL**: 5 minutes
- **Hit rate**: 91.67%
- **Scope**: Raw PIPER.md file content

### 2. Session-level (UserContextService)

- **TTL**: Infinite (per session)
- **Hit rate**: 81.82%
- **Scope**: Parsed user context objects

**Performance Impact**:

- **Combined improvement**: ~98% for cached requests
- **Response time**: 3ms → 0.02ms (cached)
- **File I/O reduction**: Significant decrease in disk reads

**Cache Monitoring**:

```bash
# Check cache performance
curl http://localhost:8001/api/admin/piper-config-cache-metrics
```

---

## Testing

Comprehensive test coverage across all dimensions:

### Spatial Intelligence Tests

- **10 pattern checks** across all handlers
- **Response length validation** for each spatial pattern
- **Content appropriateness** for context

### Error Handling Tests

- **8 failure scenarios** covered
- **Service unavailable** conditions
- **Missing configuration** handling
- **Empty data** validation

### Multi-User Tests

- **Context isolation** between users
- **No hardcoded references** validation
- **Configuration independence** testing

### Cache Performance Tests

- **Hit rate validation** for both cache layers
- **Performance improvement** measurement
- **Metrics endpoint** functionality

**Test Execution**:

```bash
# Run all handler tests
pytest tests/intent/test_handler_error_handling.py -v
python3 dev/2025/10/06/test_all_handlers_spatial.py
```

---

## Implementation Details

### Handler Registration

Handlers are registered in the `CanonicalHandlers` class:

```python
async def handle(self, intent: Intent, session_id: str) -> Dict:
    """Route to appropriate canonical handler"""
    if intent.category == IntentCategoryEnum.IDENTITY:
        return await self._handle_identity_query(intent, session_id)
    elif intent.category == IntentCategoryEnum.TEMPORAL:
        return await self._handle_temporal_query(intent, session_id)
    # ... etc
```

### Response Format

All handlers return consistent response structure:

```python
{
    "message": "User-facing response text",
    "intent": {
        "category": "handler_category",
        "action": "handler_action",
        "confidence": 1.0,
        "context": {
            # Handler-specific context data
        }
    },
    "spatial_pattern": "GRANULAR|EMBEDDED|None",
    "requires_clarification": False,
    # Handler-specific fields (error, action_required, etc.)
}
```

### Performance Characteristics

- **Response time**: 0.02ms (cached) to 3ms (uncached)
- **Memory usage**: Minimal (context objects are lightweight)
- **Scalability**: Handles multiple concurrent users
- **Reliability**: Graceful degradation under load

---

## Related Documentation

- **[User Context Service](user-context-service.md)** - Multi-user context management
- **[Intent Classification Guide](intent-classification-guide.md)** - Universal intent enforcement
- **Session Logs**: `dev/2025/10/06/` - Implementation details
- **Test Files**: `tests/intent/` - Comprehensive test coverage

---

## Future Enhancements

### Potential Improvements

1. **Enhanced PIPER.md Parsing**: Structured parsing with schema validation
2. **Dynamic Handler Registration**: Plugin-based handler system
3. **Advanced Spatial Patterns**: More granular response control
4. **Predictive Caching**: Pre-load likely queries based on patterns

### Monitoring Recommendations

1. **Handler Performance**: Track response times by handler
2. **Error Rates**: Monitor failure scenarios and recovery
3. **Cache Effectiveness**: Optimize cache policies based on usage
4. **User Satisfaction**: Gather feedback on response quality

---

**Status**: ✅ Production ready - All handlers validated and tested

**Last Updated**: October 6, 2025 (GREAT-4C completion)
