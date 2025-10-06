# Gameplan: GREAT-4C - Intent Quality & Context Awareness

**Date**: October 5, 2025
**Epic**: GREAT-4C (Third sub-epic of GREAT-4)
**Context**: Performance solved, focus on handler quality and context
**Expected**: 219 handlers exist, some return generic responses

## Mission

Audit all 219 canonical handlers for response quality, implement context awareness for multi-turn conversations, enhance monitoring with decision explanations, and prepare learning feedback loops.

## Background from 4A/4B

- Performance: <1ms (excellent!)
- Accuracy: 92% (exceeds target!)
- Caching: Operational
- Missing: Context awareness, handler quality assurance

## Phase -1: Handler Discovery
**Lead Developer - ALWAYS DO FIRST**

Map what we're working with:
```bash
# Count canonical handlers
grep -r "async def _handle" services/intent_service/canonical_handlers.py | wc -l

# Find handler categories
grep -r "IntentCategory\." services/intent_service/canonical_handlers.py | sort -u

# Check for undefined responses
grep -r "I don't understand\|undefined\|generic" services/intent_service/ --include="*.py"

# Look for context tracking
grep -r "session\|context\|conversation" services/intent_service/ --include="*.py"
```

Document findings in `dev/2025/10/05/handler-audit-baseline.md`

## Phase 0: Quality Audit
**Both Agents - Medium task**

### Create Handler Audit Script
`scripts/audit_handler_responses.py`:
```python
import asyncio
from services.intent_service.canonical_handlers import CanonicalHandlers

async def audit_all_handlers():
    """Test each handler for quality responses."""

    handlers = CanonicalHandlers()
    results = {
        'total': 0,
        'quality': [],
        'generic': [],
        'undefined': [],
        'error': []
    }

    # Get all handler methods
    handler_methods = [m for m in dir(handlers) if m.startswith('_handle_')]

    for method_name in handler_methods:
        # Test with sample inputs
        # Check for generic responses
        # Verify meaningful content
        # Log results
        pass

    return results

# Generate audit report
```

### Quality Criteria
- Returns specific, actionable response
- No "I don't understand" fallbacks
- Handles edge cases gracefully
- Provides helpful context

## Phase 1: Fix Handler Responses
**Code Agent - Complex task**

### For Each Problematic Handler
```python
# Before (generic):
async def _handle_unknown_query(self, intent, session_id):
    return {
        "response": "I don't understand that query",
        "status": "error"
    }

# After (helpful):
async def _handle_unknown_query(self, intent, session_id):
    return {
        "response": f"I'm not sure how to help with '{intent.text}'. "
                   f"You might try rephrasing or I can help you with:\n"
                   f"- Creating issues (say 'create an issue')\n"
                   f"- Checking status (say 'what am I working on')\n"
                   f"- Schedule queries (say 'what's my schedule')",
        "suggestions": ["create issue", "show status", "view schedule"],
        "status": "needs_clarification"
    }
```

### Response Enhancement Pattern
1. Acknowledge the query
2. Explain limitation specifically
3. Offer alternatives
4. Provide examples

## Phase 2: Context Awareness
**Cursor Agent - Medium task**

### Create Context Manager
`services/intent_service/context_manager.py`:
```python
from typing import Dict, List, Optional
import time

class ConversationContext:
    """Manages conversation context for multi-turn interactions."""

    def __init__(self):
        self.sessions: Dict[str, SessionContext] = {}
        self.ttl = 3600  # 1 hour

    def get_or_create_session(self, session_id: str) -> 'SessionContext':
        """Get existing or create new session context."""
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionContext(session_id)

        session = self.sessions[session_id]
        session.last_accessed = time.time()
        return session

    def add_turn(self, session_id: str, intent, response):
        """Add conversation turn to session history."""
        session = self.get_or_create_session(session_id)
        session.add_turn(intent, response)

    def get_context(self, session_id: str) -> Optional[Dict]:
        """Get relevant context for current query."""
        if session_id not in self.sessions:
            return None

        session = self.sessions[session_id]
        return {
            'previous_intents': session.get_recent_intents(),
            'mentioned_entities': session.entities,
            'conversation_state': session.state
        }

class SessionContext:
    """Individual session context."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.turns: List[Dict] = []
        self.entities: Dict = {}
        self.state: str = 'active'
        self.created_at = time.time()
        self.last_accessed = time.time()

    def add_turn(self, intent, response):
        """Add turn to conversation history."""
        self.turns.append({
            'timestamp': time.time(),
            'intent': intent.category,
            'text': intent.text,
            'response': response
        })

        # Keep last 10 turns
        if len(self.turns) > 10:
            self.turns = self.turns[-10:]
```

### Integrate with Handlers
```python
# In canonical_handlers.py
async def _handle_followup_query(self, intent, session_id):
    # Get conversation context
    context = self.context_manager.get_context(session_id)

    if context and context['previous_intents']:
        # Use context for better response
        last_intent = context['previous_intents'][-1]
        return {
            "response": f"Following up on your {last_intent} query...",
            "context_aware": True
        }
```

## Phase 3: Enhanced Monitoring
**Code Agent - Medium task**

### Add Decision Explanations
`web/routes/metrics.py`:
```python
@router.get("/metrics/intent/detailed")
async def get_detailed_metrics():
    """Enhanced metrics with decision explanations."""

    return {
        "basic_metrics": {
            "total_classifications": metrics.total,
            "cache_hit_rate": metrics.cache_hit_rate,
            "avg_latency_ms": metrics.avg_latency
        },
        "classification_distribution": {
            "TEMPORAL": metrics.by_category["TEMPORAL"],
            "STATUS": metrics.by_category["STATUS"],
            "PRIORITY": metrics.by_category["PRIORITY"],
            # ... all categories
        },
        "confidence_distribution": {
            "high_confidence": metrics.confidence_high,  # >0.8
            "medium_confidence": metrics.confidence_med,  # 0.5-0.8
            "low_confidence": metrics.confidence_low      # <0.5
        },
        "handler_quality": {
            "successful_responses": metrics.handler_success,
            "generic_responses": metrics.handler_generic,
            "error_responses": metrics.handler_errors
        },
        "recent_classifications": [
            {
                "text": "What's my schedule?",
                "category": "TEMPORAL",
                "confidence": 0.95,
                "explanation": "Matched pattern 'schedule' with high confidence",
                "handler": "_handle_temporal_query",
                "response_quality": "specific"
            }
            # Last 10 with explanations
        ]
    }
```

## Phase 4: Learning Feedback
**Cursor Agent - Medium task**

### Create Feedback Capture
`services/intent_service/feedback_collector.py`:
```python
import json
from datetime import datetime

class FeedbackCollector:
    """Collects classification and response feedback for learning."""

    def __init__(self):
        self.feedback_file = "data/intent_feedback.jsonl"

    async def capture_classification(self, intent, classification, response):
        """Record classification for future training."""
        feedback = {
            "timestamp": datetime.utcnow().isoformat(),
            "input_text": intent.text,
            "classified_as": classification.category,
            "confidence": classification.confidence,
            "handler_used": classification.handler,
            "response_type": self._categorize_response(response),
            "session_id": intent.session_id
        }

        # Append to JSONL file for future ML training
        with open(self.feedback_file, 'a') as f:
            f.write(json.dumps(feedback) + '\n')

    async def capture_user_feedback(self, session_id, helpful: bool):
        """Record explicit user feedback."""
        feedback = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "helpful": helpful,
            "type": "user_feedback"
        }

        with open(self.feedback_file, 'a') as f:
            f.write(json.dumps(feedback) + '\n')

    def _categorize_response(self, response):
        """Categorize response quality."""
        if "I don't understand" in str(response):
            return "generic"
        elif "error" in str(response):
            return "error"
        else:
            return "specific"
```

## Phase 5: Comprehensive Testing
**Both Agents - Medium task**

### Handler Quality Tests
```python
# tests/intent/test_handler_quality.py
@pytest.mark.parametrize("handler_name,sample_input", HANDLER_TEST_CASES)
async def test_handler_response_quality(handler_name, sample_input):
    """Each handler returns quality response."""
    handler = getattr(handlers, handler_name)
    response = await handler(sample_input, "test_session")

    # No generic responses
    assert "I don't understand" not in response["response"]
    assert "undefined" not in response["response"]

    # Meaningful content
    assert len(response["response"]) > 20
    assert response["status"] != "error"
```

### Context Awareness Tests
```python
# tests/intent/test_context_aware.py
async def test_multi_turn_conversation():
    """Context carries across turns."""
    session_id = "test_conversation"

    # First turn
    response1 = await process_intent("What's my schedule?", session_id)

    # Follow-up uses context
    response2 = await process_intent("What about tomorrow?", session_id)

    # Should understand "tomorrow" in context of schedule
    assert "schedule" in response2["response"].lower()
    assert response2["context_aware"] == True
```

## Phase Z: Documentation & Validation
**Both Agents**

### Update Documentation
- Update Pattern-028 with context awareness
- Document handler quality standards
- Create feedback loop guide

### Final Validation
```bash
# Run quality audit
python scripts/audit_handler_responses.py
# All 219 handlers pass

# Test context system
pytest tests/intent/test_context_aware.py -v
# Multi-turn working

# Check monitoring
curl http://localhost:8001/metrics/intent/detailed
# Shows enhanced data

# Verify feedback capture
tail -n 10 data/intent_feedback.jsonl
# Feedback being collected
```

## Success Criteria

- [ ] All 219 handlers audited
- [ ] Generic responses eliminated
- [ ] Context awareness operational
- [ ] Enhanced monitoring live
- [ ] Feedback capture working
- [ ] Multi-turn conversations functional
- [ ] Documentation updated
- [ ] All tests passing

## Effort Indicators

- Phase -1: Discovery (simple)
- Phase 0: Audit (medium)
- Phase 1: Handler fixes (complex)
- Phase 2: Context system (medium)
- Phase 3: Monitoring (medium)
- Phase 4: Feedback (medium)
- Phase 5: Testing (medium)
- Phase Z: Documentation (simple)

## Critical Notes

- Focus on quality not performance (already fast)
- Each handler should be helpful even when uncertain
- Context should enhance not complicate
- Feedback prepares for future ML improvements

---

*Ready to complete the intent system with quality and context!*
