# Personality Enhancement API

## Base URL
`http://localhost:8001/api/`

## Overview
The Personality Enhancement API provides endpoints for managing user personality preferences and enhancing responses with warm, confident, actionable communication patterns.

## Endpoints

### GET /api/personality/profile/{user_id}
Retrieve user's personality preferences

**URL**: `http://localhost:8001/api/personality/profile/{user_id}`
**Method**: GET
**Authentication**: None required

**Parameters**:
- `user_id` (path): User identifier (default: "default")

**Example Request**:
```bash
curl -X GET "http://localhost:8001/api/personality/profile/default" | jq '.'
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "warmth_level": 0.7,
    "confidence_style": "contextual",
    "action_orientation": "medium",
    "technical_depth": "balanced"
  },
  "user_id": "default"
}
```

**Error Response**:
```json
{
  "status": "error",
  "error": "Configuration not found",
  "user_id": "invalid_user"
}
```

---

### PUT /api/personality/profile/{user_id}
Update user's personality preferences

**URL**: `http://localhost:8001/api/personality/profile/{user_id}`
**Method**: PUT
**Authentication**: None required
**Content-Type**: application/json

**Parameters**:
- `user_id` (path): User identifier

**Request Body**:
```json
{
  "warmth_level": 0.8,
  "confidence_style": "contextual",
  "action_orientation": "high",
  "technical_depth": "balanced"
}
```

**Field Validation**:
- `warmth_level`: Float 0.0-1.0
- `confidence_style`: "numeric", "descriptive", "contextual", "hidden"
- `action_orientation`: "high", "medium", "low"
- `technical_depth`: "detailed", "balanced", "simplified"

**Example Request**:
```bash
curl -X PUT "http://localhost:8001/api/personality/profile/default" \
  -H "Content-Type: application/json" \
  -d '{
    "warmth_level": 0.8,
    "confidence_style": "contextual",
    "action_orientation": "high",
    "technical_depth": "balanced"
  }'
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "warmth_level": 0.8,
    "confidence_style": "contextual",
    "action_orientation": "high",
    "technical_depth": "balanced"
  },
  "user_id": "default",
  "message": "Personality preferences updated successfully"
}
```

---

### POST /api/personality/enhance
Test personality enhancement on content

**URL**: `http://localhost:8001/api/personality/enhance`
**Method**: POST
**Authentication**: None required
**Content-Type**: application/json

**Request Body**:
```json
{
  "content": "Task completed successfully",
  "user_id": "default",
  "confidence": 0.8
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8001/api/personality/enhance" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Analysis completed successfully",
    "user_id": "default",
    "confidence": 0.8
  }'
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "original_content": "Analysis completed successfully",
    "enhanced_content": "Perfect! Analysis completed successfully (based on recent patterns)—ready for the next step!",
    "personality_config": {
      "warmth_level": 0.7,
      "confidence_style": "contextual",
      "action_orientation": "medium",
      "technical_depth": "balanced"
    },
    "confidence": 0.8
  }
}
```

---

### GET /api/standup?personality=true
Get personality-enhanced standup

**URL**: `http://localhost:8001/api/standup?personality=true&format=human-readable`
**Method**: GET
**Authentication**: None required

**Parameters**:
- `personality` (query): Enable personality enhancement (boolean)
- `format` (query): "raw" or "human-readable"

**Example Request**:
```bash
curl -X GET "http://localhost:8001/api/standup?personality=true&format=human-readable" | jq '.'
```

**Response** (with personality enhancement):
```json
{
  "status": "success",
  "data": {
    "generation_time_ms": 4500,
    "time_saved_minutes": 15,
    "yesterday_accomplishments": [
      "Perfect! Enhanced standup system with personality integration—ready for the next step!"
    ],
    "today_priorities": [
      "Great! Focus on manual testing validation (based on recent patterns)"
    ],
    "blockers": [],
    "context_source": "github",
    "github_activity": {
      "commits": 5,
      "issues": 2
    },
    "user_id": "default",
    "personality_enhanced": true,
    "personality_config": {
      "warmth_level": 0.7,
      "confidence_style": "contextual",
      "action_orientation": "high",
      "technical_depth": "balanced"
    }
  },
  "metadata": {
    "generated_at": "2025-09-11T21:30:00Z",
    "source": "api",
    "version": "1.0",
    "format": "human-readable",
    "performance": {
      "target_ms": 10000,
      "status": "✅ FAST",
      "vs_cli_baseline": "faster"
    }
  }
}
```

## Configuration Integration

Personality settings are configurable via `config/PIPER.user.md`:

```yaml
personality:
  profile:
    warmth_level: 0.7              # 0.0-1.0: Emotional warmth in responses
    confidence_style: "contextual" # "numeric", "descriptive", "contextual", "hidden"
    action_orientation: "medium"   # "high", "medium", "low"
    technical_depth: "balanced"    # "detailed", "balanced", "simplified"

  performance:
    max_response_time_ms: 70       # Maximum enhancement time
    enable_circuit_breaker: true   # Auto-disable on performance issues
    cache_ttl_seconds: 1800        # Profile cache time-to-live
```

## Performance Characteristics

- **Enhancement Latency**: <70ms (validated in production testing)
- **Cache Hit Rate**: 93-100% (LRU with 1800 second TTL)
- **Concurrent Requests**: Supports 10+ simultaneous users
- **Circuit Breaker**: Activates after 5 failures in 60 seconds
- **Graceful Degradation**: Falls back to original content on enhancement failure

## Error Handling

All endpoints provide graceful error handling:

- **Configuration errors**: Return default personality settings
- **Enhancement failures**: Return original content unchanged
- **Performance timeouts**: Circuit breaker activation with fallback
- **Invalid input**: Validation errors with helpful messages

## Integration Examples

### CLI Integration
```bash
# Show current personality
PYTHONPATH=. python cli/commands/personality.py show

# Update personality via CLI
PYTHONPATH=. python cli/commands/personality.py set --warmth 0.8
```

### Web UI Integration
- Personality preferences: `http://localhost:8081/personality-preferences`
- Enhanced standup: `http://localhost:8081/standup`
- Main chat with personality: `http://localhost:8081/`

## Testing

### Unit Testing
```bash
PYTHONPATH=. python -m pytest tests/services/personality/ -v
```

### Integration Testing
```bash
# Test API endpoints
curl -X GET "http://localhost:8001/api/personality/profile/default"
curl -X POST "http://localhost:8001/api/personality/enhance" -d '{"content": "Test message"}'
```

### Performance Testing
```bash
# Measure enhancement latency
time curl -X POST "http://localhost:8001/api/personality/enhance" \
  -H "Content-Type: application/json" \
  -d '{"content": "Performance test", "confidence": 0.8}'
```
