# Gameplan: #662 MEM-ADR054-P2: Greeting Context Service

## Audit Findings

### Dependency Verified
- #657 MEM-ADR054-P1 ✅ Complete
- `ConversationalMemoryService` exists with `get_memory_window()` method
- `ConversationalMemoryEntry` has `timestamp`, `topic_summary`, `entities_mentioned`, `user_sentiment`

### Issue Spec Alignment
The spec closely matches ADR-054 Phase 2. Implementation can proceed as specified.

### Minor Adjustments
1. Add `PREVIOUS_TRIVIAL` detection logic (spec mentions it but doesn't define when to use it)
2. Consider edge case: negative sentiment + same day return (negative takes precedence per spec)

---

## Implementation Plan

### Phase 1: Greeting Condition Enum

```python
class GreetingCondition(Enum):
    SAME_DAY_RECENT = "same_day_recent"      # Back within ~8 hours
    NEXT_DAY_ACTIVE = "next_day_active"      # 8-36 hours, was working on something
    WEEK_GAP = "week_gap"                    # 36 hours - 1 week
    MONTH_GAP = "month_gap"                  # 1+ week (or 1+ month per name)
    PREVIOUS_TRIVIAL = "previous_trivial"    # Last session was brief/unimportant
    PREVIOUS_NEGATIVE = "previous_negative"  # Last session ended badly
    FIRST_SESSION = "first_session"          # Brand new user
```

### Phase 2: Greeting Context Dataclass

```python
@dataclass
class GreetingContext:
    condition: GreetingCondition
    last_session: Optional[ConversationalMemoryEntry]
    time_since_last: Optional[timedelta]
    suggested_greeting_approach: str
    can_reference_work: bool
    offer_fresh_start: bool
    topic_reference: Optional[str] = None
    entity_references: List[str] = field(default_factory=list)
```

### Phase 3: Greeting Context Service

```python
class GreetingContextService:
    WINDOW_HOURS = {
        "same_day": 8,
        "next_day": 36,
        "week": 168,      # 7 days
        "month": 720,     # 30 days
    }

    async def get_greeting_context(self, user_id: str) -> GreetingContext
    def _determine_condition(self, last_entry: Optional[ConversationalMemoryEntry]) -> GreetingCondition
    def _time_since(self, entry: Optional[ConversationalMemoryEntry]) -> Optional[timedelta]
    def _get_suggested_approach(self, condition: GreetingCondition) -> str
```

### Phase 4: Tests

1. Test `GreetingCondition` enum values
2. Test `GreetingContext` dataclass creation
3. Test condition detection:
   - `test_first_session_when_no_entries`
   - `test_same_day_recent_within_8_hours`
   - `test_next_day_active_8_to_36_hours`
   - `test_week_gap_36_hours_to_week`
   - `test_month_gap_over_week`
   - `test_negative_sentiment_overrides_time`
4. Test context flags:
   - `test_can_reference_work_for_recent`
   - `test_offer_fresh_start_for_gaps`
5. Integration test with mocked memory service

---

## Completion Matrix

| Criterion | Method | Evidence Required |
|-----------|--------|-------------------|
| GreetingCondition enum defined | Write | All PDR-002 conditions present |
| GreetingContext dataclass defined | Write | All fields present |
| GreetingContextService implemented | Write | Class exists with methods |
| get_greeting_context() works | Test | Returns appropriate context |
| Condition detection covers all scenarios | Test | Tests for each time range |
| Negative sentiment triggers clean slate | Test | test_negative_sentiment_overrides_time |
| First session detected | Test | test_first_session_when_no_entries |
| can_reference_work computed correctly | Test | test_can_reference_work_for_recent |
| offer_fresh_start computed correctly | Test | test_offer_fresh_start_for_gaps |
| Unit tests for all conditions | Test | All tests pass |
| Integration tests with memory service | Test | test_integration_with_memory_service |

---

## Suggested Greeting Approaches (from PDR-002)

| Condition | Approach |
|-----------|----------|
| SAME_DAY_RECENT | "Back already! We were working on [X]—continue?" |
| NEXT_DAY_ACTIVE | "Yesterday we discussed [X]. Continue, or different focus?" |
| WEEK_GAP | "It's been a bit! Want to pick up where we left off?" |
| MONTH_GAP | "Welcome back! Want me to catch you up, or start fresh?" |
| PREVIOUS_NEGATIVE | "What would you like to work on?" |
| FIRST_SESSION | Use FTUX flow |
| PREVIOUS_TRIVIAL | Generic friendly greeting |
