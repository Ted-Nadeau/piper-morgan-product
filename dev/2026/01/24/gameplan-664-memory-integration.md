# Gameplan: #664 MEM-ADR054-P4: Memory Integration

## Audit Findings

### Dependencies Complete
- #657 MEM-ADR054-P1 ✅ ConversationalMemoryService with `record_conversation_end()`
- #662 MEM-ADR054-P2 ✅ GreetingContextService with `get_greeting_context()`
- #663 MEM-ADR054-P3 ✅ UserHistoryService with `mark_private()`, `unmark_private()`

### Existing Infrastructure

**Session Management**:
- `SessionContextManager.end_session_with_persistence()` - saves context but doesn't record to memory

**Memory Recording**:
- `ConversationalMemoryService.record_conversation_end(summary, entities, outcome, sentiment)` - ready to use

**Privacy**:
- `UserHistoryService.mark_private(user_id, conversation_id)` ✅ already implemented
- `UserHistoryService.unmark_private(user_id, conversation_id)` ✅ already implemented
- Repository filters out private by default ✅

**Domain Models**:
- `ConversationTurn` has `entities`, `intent`, `user_message`, `assistant_response`

### Gaps to Fill

1. **Conversation Summarizer**: Rule-based extraction of topic, entities, sentiment
2. **Session Hooks**: Wire session end to memory recording
3. **Privacy Mode Service**: Start private session, manage state

---

## Implementation Plan

### Phase 1: Conversation Summarizer (Rule-Based)

```python
# services/memory/conversation_summarizer.py

@dataclass
class ConversationSummaryResult:
    """Result of summarizing a conversation."""
    topic: str              # "Discussed sprint planning", "Worked on bug #123"
    entities: List[str]     # ["#123", "@alice", "sprint-42"]
    outcome: Optional[str]  # "Completed", "In progress", "Blocked"
    sentiment: str          # "positive", "neutral", "negative"

class ConversationSummarizer:
    """Rule-based conversation summarizer."""

    def summarize(self, turns: List[ConversationTurn]) -> ConversationSummaryResult:
        """Extract summary from conversation turns."""
        # Topic: First meaningful user message or dominant intent
        # Entities: Collect from all turns
        # Outcome: Infer from last response or explicit signals
        # Sentiment: Simple heuristic (frustration words, thanks, etc.)
```

**Key heuristics**:
- Topic: Use first user message, truncated, or dominant intent category
- Entities: Union of all `turn.entities`
- Outcome: Check for completion signals ("done", "thanks", "completed")
- Sentiment: Word lists for positive/negative signals

### Phase 2: Session Hooks

```python
# services/memory/session_hooks.py

async def on_session_end(
    user_id: str,
    conversation_id: str,
    turns: List[ConversationTurn],
    memory_service: ConversationalMemoryService,
    summarizer: Optional[ConversationSummarizer] = None,
    is_private: bool = False,
) -> None:
    """Handle session end by recording to memory."""

    if is_private:
        return  # Don't record private sessions

    summarizer = summarizer or ConversationSummarizer()
    summary = summarizer.summarize(turns)

    await memory_service.record_conversation_end(
        user_id=user_id,
        conversation_id=conversation_id,
        summary=summary.topic,
        entities=summary.entities,
        outcome=summary.outcome,
        sentiment=summary.sentiment,
    )
```

### Phase 3: Privacy Mode Service

```python
# services/memory/privacy_mode.py

@dataclass
class PrivacyState:
    """Current privacy state for a session."""
    is_private: bool
    reason: Optional[str]  # Why private (user request, auto-detected sensitive)

class PrivacyModeService:
    """Manages privacy mode for conversations."""

    def __init__(self, history_service: UserHistoryService):
        self.history_service = history_service
        self._session_privacy: Dict[str, PrivacyState] = {}

    def start_private_session(
        self,
        conversation_id: str,
        reason: str = "user_request"
    ) -> PrivacyState:
        """Mark current session as private (won't be remembered)."""

    def end_private_session(self, conversation_id: str) -> None:
        """End private mode (future turns will be remembered)."""

    def is_private(self, conversation_id: str) -> bool:
        """Check if session is currently private."""

    async def retroactively_mark_private(
        self,
        user_id: str,
        conversation_id: str,
    ) -> bool:
        """Mark already-recorded conversation as private."""
        return await self.history_service.mark_private(user_id, conversation_id)
```

---

## Completion Matrix

| Criterion | Method | Evidence Required |
|-----------|--------|-------------------|
| ConversationSummarizer extracts topic | Test | Returns meaningful topic |
| Entity extraction aggregates across turns | Test | Union of all entities |
| Sentiment detection works | Test | Positive/neutral/negative |
| on_session_end calls memory service | Test | Memory service called |
| Private sessions not recorded | Test | Skip if is_private=True |
| start_private_session works | Test | State tracked |
| retroactively_mark_private works | Test | Calls history service |
| All unit tests pass | Test | pytest output |

---

## Files to Create

```
services/memory/conversation_summarizer.py   # Rule-based summarizer
services/memory/session_hooks.py             # Session end handling
services/memory/privacy_mode.py              # Privacy mode service
tests/unit/services/memory/test_conversation_summarizer.py
tests/unit/services/memory/test_session_hooks.py
tests/unit/services/memory/test_privacy_mode.py
```

---

## Spec Adjustments

1. **Summarization**: Rule-based per ADR-054 recommendation (not LLM)
2. **Sentiment**: Word-list heuristic per ADR-054 recommendation (not LLM)
3. **E2E tests**: Deferred - unit tests cover service layer
4. **Greeting integration**: Defer to caller - GreetingContextService is ready

---

## Order of Implementation

1. ConversationSummarizer (no dependencies, pure logic)
2. session_hooks (depends on summarizer)
3. PrivacyModeService (depends on UserHistoryService)
4. Update `services/memory/__init__.py` exports
5. Tests for all components
