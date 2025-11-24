# Preference Detection API Reference

**Base URL**: `/api/v1/preferences`

---

## Endpoints

### POST /hints/{hint_id}/accept

Accept a preference suggestion and apply it to the user's profile.

**Path Parameters**:
- `hint_id` (string, required): The ID of the preference hint to accept

**Request Body**:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "action": "accepted",
  "hint_id": "hint_1_abc123",
  "dimension": "warmth_level",
  "previous_value": 0.5,
  "new_value": 0.8,
  "message": "Preference updated! Your warmth_level setting is now 0.8"
}
```

**Error Response** (400 Bad Request):
```json
{
  "success": false,
  "error": "Preference suggestion not found or expired",
  "hint_id": "hint_1_abc123"
}
```

**Notes**:
- The preference is stored persistently in UserPreferenceManager
- Preference is logged to the learning system for future detection improvement
- Auto-apply preferences (confidence ≥ 0.9 + explicit source) apply silently without this endpoint

---

### POST /hints/{hint_id}/dismiss

Dismiss a preference suggestion without applying it.

**Path Parameters**:
- `hint_id` (string, required): The ID of the preference hint to dismiss

**Request Body**:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "action": "dismissed",
  "hint_id": "hint_1_abc123"
}
```

**Notes**:
- Dismissal is logged for learning system refinement
- Dismissed preferences may appear again in future conversations if signals persist

---

### GET /profile

Retrieve the user's current personality profile with all applied preferences.

**Response** (200 OK):
```json
{
  "warmth_level": 0.8,
  "confidence_style": "contextual",
  "action_orientation": "high",
  "technical_depth": "detailed",
  "is_default": false,
  "last_updated": "2025-11-22T16:30:00Z",
  "applied_from": [
    {
      "source": "user_configured",
      "updated_at": "2025-11-20T10:00:00Z"
    },
    {
      "source": "preference_detected",
      "updated_at": "2025-11-22T16:30:00Z"
    }
  ]
}
```

**Notes**:
- Returns merged profile from PIPER.user.md + detected preferences
- PIPER.user.md settings override detected preferences (explicit config is highest priority)
- All 4 dimensions always present in response

---

### GET /stats

Get statistics about user's preference history.

**Response** (200 OK):
```json
{
  "total_preferences_detected": 15,
  "total_preferences_applied": 8,
  "total_preferences_dismissed": 3,
  "total_preferences_auto_applied": 4,
  "last_preference_update": "2025-11-22T16:30:00Z",
  "first_preference_detection": "2025-11-15T08:00:00Z",
  "by_dimension": {
    "warmth_level": {
      "detected": 4,
      "applied": 3,
      "dismissed": 1,
      "auto_applied": 0
    },
    "confidence_style": {
      "detected": 3,
      "applied": 2,
      "dismissed": 0,
      "auto_applied": 1
    },
    "action_orientation": {
      "detected": 5,
      "applied": 2,
      "dismissed": 1,
      "auto_applied": 2
    },
    "technical_depth": {
      "detected": 3,
      "applied": 1,
      "dismissed": 1,
      "auto_applied": 1
    }
  },
  "detection_methods": {
    "language_patterns": 8,
    "behavioral_signals": 4,
    "explicit_feedback": 2,
    "response_analysis": 1
  }
}
```

---

### GET /health

Health check for the preference detection system.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-11-22T16:35:00Z",
  "components": {
    "analyzer": {
      "status": "healthy",
      "latency_ms": 12
    },
    "storage": {
      "status": "healthy",
      "latency_ms": 5
    },
    "learning_integration": {
      "status": "healthy",
      "latency_ms": 8
    },
    "preference_manager": {
      "status": "healthy",
      "latency_ms": 3
    }
  }
}
```

**Response** (503 Service Unavailable):
```json
{
  "status": "degraded",
  "timestamp": "2025-11-22T16:35:00Z",
  "components": {
    "analyzer": {
      "status": "healthy",
      "latency_ms": 12
    },
    "storage": {
      "status": "unhealthy",
      "error": "Connection timeout",
      "latency_ms": 5000
    },
    "learning_integration": {
      "status": "healthy",
      "latency_ms": 8
    }
  }
}
```

---

## Data Structures

### PreferenceHint

Structure representing a detected preference suggestion.

```json
{
  "id": "hint_1_abc123",
  "dimension": "warmth_level",
  "detected_value": 0.8,
  "current_value": 0.5,
  "confidence_score": 0.85,
  "confidence_level": "high",
  "detection_method": "language_patterns",
  "source_text": "I'd like you to be more friendly and casual",
  "explanation": "Detected preference for warmth based on use of friendly words",
  "is_ready_for_suggestion": true,
  "is_ready_for_auto_apply": false,
  "created_at": "2025-11-22T16:30:00Z",
  "expires_at": "2025-11-22T17:00:00Z"
}
```

**Fields**:
- `id`: Unique hint identifier (format: `hint_{counter}_{uuid}`)
- `dimension`: One of: `warmth_level`, `confidence_style`, `action_orientation`, `technical_depth`
- `detected_value`: The preference value detected from user message
- `current_value`: The user's current preference setting
- `confidence_score`: Float 0.0-1.0 indicating detection confidence
- `confidence_level`: One of: `VERY_HIGH` (≥0.9), `HIGH` (0.7-0.89), `MEDIUM` (0.4-0.69), `LOW` (<0.4)
- `detection_method`: One of: `language_patterns`, `behavioral_signals`, `explicit_feedback`, `response_analysis`
- `source_text`: The user message that triggered detection
- `explanation`: Human-readable explanation of why this preference was detected
- `is_ready_for_suggestion`: Boolean indicating if confidence ≥ 0.4
- `is_ready_for_auto_apply`: Boolean indicating if confidence ≥ 0.9 + explicit source
- `created_at`: Timestamp when hint was created
- `expires_at`: Timestamp when hint expires (30 minutes after creation)

### PreferenceConfirmation

Record of user acceptance/rejection of a preference.

```json
{
  "id": "confirm_abc123",
  "dimension": "warmth_level",
  "previous_value": 0.5,
  "new_value": 0.8,
  "hint_id": "hint_1_abc123",
  "confirmation_source": "user_accepted",
  "created_at": "2025-11-22T16:30:30Z"
}
```

---

## Error Responses

### 400 Bad Request

```json
{
  "error": "Invalid request",
  "message": "Session ID is required",
  "code": "INVALID_REQUEST"
}
```

### 404 Not Found

```json
{
  "error": "Not found",
  "message": "Preference hint hint_1_notfound not found",
  "code": "HINT_NOT_FOUND"
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal server error",
  "message": "Error confirming preference",
  "code": "INTERNAL_ERROR",
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## Authentication

All endpoints require user authentication via session or user_id.

- **Session-based**: Include `session_id` in request header or body
- **User-based**: Include `Authorization: Bearer <token>` header

---

## Rate Limiting

- Preference detection: 100 requests/minute per user
- Preference confirmation: 10 requests/minute per user
- Profile retrieval: Unlimited

---

## Response Headers

All responses include:

```
Content-Type: application/json
X-Request-Id: 550e8400-e29b-41d4-a716-446655440000
X-Process-Time: 45ms
Cache-Control: no-cache
```

---

## Examples

### Example 1: User Accepts Preference

**Request**:
```bash
curl -X POST http://localhost:8001/api/v1/preferences/hints/hint_1_abc123/accept \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

**Response**:
```json
{
  "success": true,
  "action": "accepted",
  "hint_id": "hint_1_abc123",
  "dimension": "warmth_level",
  "previous_value": 0.5,
  "new_value": 0.8,
  "message": "Preference updated! Your warmth_level setting is now 0.8"
}
```

### Example 2: Retrieve Current Profile

**Request**:
```bash
curl -X GET http://localhost:8001/api/v1/preferences/profile \
  -H "Authorization: Bearer user_token"
```

**Response**:
```json
{
  "warmth_level": 0.8,
  "confidence_style": "contextual",
  "action_orientation": "high",
  "technical_depth": "detailed",
  "is_default": false,
  "last_updated": "2025-11-22T16:30:00Z"
}
```

---

## Testing the API

### Using cURL

```bash
# Check health
curl http://localhost:8001/api/v1/preferences/health

# Get profile
curl -H "Cookie: session_id=your_session" \
  http://localhost:8001/api/v1/preferences/profile

# Accept preference
curl -X POST http://localhost:8001/api/v1/preferences/hints/hint_1_xyz/accept \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your_session"}'
```

### Using Python

```python
import requests

# Accept a preference
response = requests.post(
    "http://localhost:8001/api/v1/preferences/hints/hint_1_abc123/accept",
    json={"session_id": "550e8400-e29b-41d4-a716-446655440000"}
)
print(response.json())

# Get profile
response = requests.get(
    "http://localhost:8001/api/v1/preferences/profile",
    headers={"Authorization": "Bearer user_token"}
)
print(response.json())
```

---

**Last Updated**: November 22, 2025
**API Version**: v1
**Status**: Production Ready ✅
