# ADR-049: Conversational State and Hierarchical Intent Architecture

**Status:** Accepted
**Date:** 2026-01-09
**Accepted:** 2026-01-26
**Issue:** [#490 FTUX-PORTFOLIO](https://github.com/mediajunkie/piper-morgan-product/issues/490)
**Implementation:** [#427 MUX-IMPLEMENT-CONVERSE-MODEL](https://github.com/mediajunkie/piper-morgan-product/issues/427)
**Author:** Lead Developer (Claude Code Opus)
**Approver:** PM (xian), PPM, Chief Architect

## Context

During implementation of portfolio onboarding (Issue #490), we discovered a fundamental architectural gap: Piper lacked "conversational state" - the ability to maintain control of a guided conversation once it begins.

### The Problem

When a user starts the onboarding flow:

1. **Turn 1 (Greeting)**: User says "Hello" → Piper correctly triggers onboarding prompt
2. **Turn 2 (Project Info)**: User says "My main project is called Piper Morgan" → **BUG**: Message gets re-classified as IDENTITY intent (because "Piper Morgan" matches identity patterns), returning the identity response instead of continuing onboarding

The root cause: Intent classification happens **every turn**, with no awareness that a guided process is in progress.

### Observed User Experience Issues

- User agrees to onboarding, immediately gets derailed by classification
- No continuity between conversational turns
- Pattern-045 "Green Tests, Red User" - unit tests passed while user experience was broken
- Manual testing caught every bug that automated tests missed

## Decision

**Adopt a two-tier intent architecture:**

### Tier 1: High-Level Conversational State (Process-Level Intent)

Represents the user's active engagement with a structured process:
- **Portfolio onboarding** - setting up projects
- **Standup assistant** - daily check-in
- **Feedback session** - detailed feedback collection
- **Planning session** - sprint/project planning

High-level state is:
- **Persistent** across multiple turns
- **Exclusive** - only one active process at a time
- **Checked first** before any turn-level classification
- **Maintained until** completion, explicit exit, or timeout

### Tier 2: Turn-Level Intent (Message-Level Classification)

Represents the micro-intent within a single message:
- User is clarifying ("I meant...")
- User is providing details ("The project is about...")
- User is asking a question ("What do you mean by...?")
- User is confirming ("Yes, that's correct")
- User is declining ("No thanks, maybe later")

Turn-level intent is:
- **Fluid** within the process context
- **Interpreted** by the active process handler
- **Secondary** to high-level state (process controls interpretation)

### Implementation Pattern

```python
async def process_intent(self, message: str, user_id: str, session_id: str):
    # TIER 1: Check for active conversational state FIRST
    if user_id:
        active_process = await self._check_active_process(user_id, session_id)
        if active_process:
            # Route directly to process handler - bypass classification
            return await active_process.handle_turn(message)

    # TIER 2: No active process - perform normal classification
    classified_intent = await self._classify_message(message)

    # Classification may START a new process (e.g., greeting → onboarding)
    return await self._route_to_handler(classified_intent)
```

### Process Priority Check Order

1. **Active onboarding session** (user is setting up portfolio)
2. **Active standup session** (user is doing daily check-in)
3. **Active planning session** (user is in planning mode)
4. **Pending clarification** (Piper asked a question)
5. **No active process** → perform classification

### State Transitions

```
[No Process] --(greeting + new user)--> [Onboarding Active]
[Onboarding Active] --(user confirms)--> [Onboarding Complete] --> [No Process]
[Onboarding Active] --(user declines)--> [Onboarding Declined] --> [No Process]
[Onboarding Active] --(timeout)--> [Onboarding Expired] --> [No Process]
```

## Rationale

### Why Process-Level Takes Priority

1. **User expectation**: When I agree to do something, I expect continuity
2. **UX principle**: Guided flows should feel guided, not interrupted
3. **Pattern precedent**: Standup assistant (Epic #242) already works this way
4. **Technical simplicity**: Single check at start vs. complex re-classification

### Why Not Just "Better Classification"?

We considered improving the intent classifier to detect "user is continuing onboarding" but rejected this because:

1. **Semantic ambiguity**: "My project is Piper Morgan" could legitimately be identity OR project info
2. **Fragile patterns**: Any pattern-based approach would have false positives
3. **Wrong abstraction**: The problem isn't classification accuracy, it's architectural flow
4. **LLM-dependent**: Would require expensive LLM calls for context-aware classification

### Singleton Manager Pattern

The `PortfolioOnboardingManager` uses a module-level singleton to persist session state across HTTP requests. This pattern:

- Avoids database round-trips for conversational state
- Works with FastAPI's async model
- Must be imported consistently (one canonical location: `conversation_handler._get_onboarding_components()`)

**Warning**: Creating new `PortfolioOnboardingManager()` instances loses state. Always use the singleton accessor.

## Consequences

### Positive

- **UX continuity**: Users complete guided flows without derailment
- **Predictable behavior**: Active process = process handles message
- **Testable**: E2E tests can verify full conversation flows
- **Extensible**: New guided processes follow the same pattern

### Negative

- **Process exclusivity**: Can't have two processes active simultaneously
- **Memory usage**: Session state lives in memory until completion/timeout
- **Restart sensitivity**: Server restart clears in-memory sessions
- **Singleton discipline**: Must use consistent accessor or state is lost

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Memory growth from abandoned sessions | `cleanup_expired()` runs on configurable interval (default 30 min) |
| Process "traps" user | Explicit decline patterns always work; timeout releases |
| Classification never runs during process | Deliberate - process handler interprets messages contextually |
| Testing complexity | E2E tests validate real user flows (Pattern-045 compliance) |

## Implementation Notes

### Generalized Architecture (January 2026)

The pattern has been generalized into the **ProcessRegistry** system:

**New Files**:
- `services/process/registry.py`: ProcessRegistry singleton, GuidedProcess protocol, ProcessType enum
- `services/process/adapters.py`: OnboardingProcessAdapter, StandupProcessAdapter
- `services/process/__init__.py`: Public API exports

**Modified Files**:
- `services/intent/intent_service.py`: Added unified `_check_active_guided_process()` using ProcessRegistry
- `services/container/initialization.py`: Registers default processes at startup

**Key Concepts**:
- **Guided Process**: Multi-turn conversation where Piper maintains control until completion/exit
- **ProcessRegistry**: Singleton tracking active processes per session, checks in priority order
- **GuidedProcess Protocol**: Interface for process handlers (process_type, check_active, handle_message)
- **ProcessType Enum**: ONBOARDING, STANDUP, PLANNING, FEEDBACK, CLARIFICATION

**Test Coverage**:
- `tests/unit/services/process/test_registry.py`: 18 tests for registry behavior
- `tests/unit/services/process/test_adapters.py`: 14 tests for adapters

### Original Files (MVP)

- `services/onboarding/portfolio_manager.py`: PortfolioOnboardingManager
- `services/standup/conversation_manager.py`: StandupConversationManager
- `services/conversation/conversation_handler.py`: Module-level singletons
- `tests/e2e/test_onboarding_http_e2e.py`: True E2E tests

### Pattern Compliance

This ADR aligns with:
- **Pattern-045** (Green Tests, Red User): E2E tests catch what unit tests miss
- **Pattern-046** (Beads Completion Discipline): Issue not closed until user experience verified
- **ADR-039** (Canonical Handler Pattern): Onboarding handler follows canonical pattern

### Future Vision

User-defined guided processes (analogous to Claude skills) could extend this architecture.

## Related Decisions

- **ADR-039**: Canonical Handler Pattern (onboarding handler structure)
- **ADR-048**: ServiceContainer Lifecycle (why not DI for manager)
- **ADR-050**: Conversation-as-Graph Model (related conversation architecture)
- **Pattern-045**: Green Tests, Red User (testing philosophy)

## Review History

| Date | Reviewer | Decision |
|------|----------|----------|
| 2026-01-09 | PM (xian) | Proposed |
| 2026-01-26 | PPM, Chief Architect | Approved for MVP implementation |
| 2026-01-26 | PM (xian) | Accepted - implemented in #427 |
