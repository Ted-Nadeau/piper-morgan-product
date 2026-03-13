# Gameplan: #658 WORKSPACE-DETECTION

## Audit Findings

### Issue Spec Deviation from Codebase Reality

The issue spec assumes infrastructure that doesn't exist:

| Spec Assumes | Reality |
|--------------|---------|
| `Place` type with `.workspace_id` | `PlaceType` enum (no attributes) |
| `Place.matches()` method | No such type exists |
| `Place.to_context()` method | No such type exists |
| `detect_context_switch(current_place: Place, ...)` | Must work with dicts |

### Existing Infrastructure

**PlaceType enum** (`services/shared_types.py:236-255`):
```python
class PlaceType(str, Enum):
    SLACK_DM = "slack_dm"
    SLACK_CHANNEL = "slack_channel"
    WEB_CHAT = "web_chat"
    CLI = "cli"
    API = "api"
    UNKNOWN = "unknown"
```

**PlaceDetector** (`services/intent_service/place_detector.py`):
- Input: `spatial_context: Dict[str, Any]` with keys like:
  - `room_id`, `channel`, `is_dm`, `source`
  - `workspace_id`, `thread_ts`, `team_id`, `slack_user_id`
- Output: `PlaceType` enum

**workspace_id usage**: Found in 20 files, extracted from spatial context dicts.

---

## Gameplan (Adapted to Reality)

### Phase 1: Domain Models

Create `services/mux/workspace_detection.py`:

```python
@dataclass
class WorkspaceContext:
    """Represents a user's working context."""
    workspace_id: str           # Extracted from spatial_context
    workspace_type: str         # Derived from PlaceType
    friendly_name: str          # Generated from workspace_type + id
    last_active: datetime
    place_type: PlaceType       # Actual place enum
    metadata: Dict[str, Any]    # Original spatial_context subset

    @classmethod
    def from_spatial_context(
        cls,
        spatial_context: Dict[str, Any],
        place_type: PlaceType,
        timestamp: Optional[datetime] = None
    ) -> "WorkspaceContext":
        """Build WorkspaceContext from spatial_context dict."""
        workspace_id = cls._extract_workspace_id(spatial_context, place_type)
        workspace_type = cls._derive_workspace_type(place_type)
        friendly_name = cls._generate_friendly_name(workspace_type, spatial_context)
        return cls(
            workspace_id=workspace_id,
            workspace_type=workspace_type,
            friendly_name=friendly_name,
            last_active=timestamp or datetime.now(timezone.utc),
            place_type=place_type,
            metadata=spatial_context
        )

    @staticmethod
    def _extract_workspace_id(ctx: Dict[str, Any], place_type: PlaceType) -> str:
        """Extract workspace identifier based on place type."""
        if place_type in (PlaceType.SLACK_DM, PlaceType.SLACK_CHANNEL):
            return ctx.get("workspace_id") or ctx.get("team_id") or "unknown-slack"
        elif place_type == PlaceType.WEB_CHAT:
            return ctx.get("session_id") or "web-chat"
        elif place_type == PlaceType.CLI:
            return "cli"
        elif place_type == PlaceType.API:
            return ctx.get("client_id") or "api"
        return "unknown"

    @staticmethod
    def _derive_workspace_type(place_type: PlaceType) -> str:
        """Map PlaceType to workspace type string."""
        mapping = {
            PlaceType.SLACK_DM: "slack",
            PlaceType.SLACK_CHANNEL: "slack",
            PlaceType.WEB_CHAT: "web",
            PlaceType.CLI: "cli",
            PlaceType.API: "api",
            PlaceType.UNKNOWN: "unknown"
        }
        return mapping.get(place_type, "unknown")

    @staticmethod
    def _generate_friendly_name(workspace_type: str, ctx: Dict[str, Any]) -> str:
        """Generate human-readable workspace name."""
        if workspace_type == "slack":
            channel = ctx.get("channel") or ctx.get("room_id")
            if channel:
                return f"#{channel}"
            return "Slack"
        elif workspace_type == "web":
            return "web chat"
        elif workspace_type == "cli":
            return "terminal"
        elif workspace_type == "api":
            return "API"
        return "unknown context"

    def matches(self, other: "WorkspaceContext") -> bool:
        """Check if this context matches another (same workspace)."""
        return self.workspace_id == other.workspace_id
```

```python
@dataclass
class ContextSwitch:
    """Detected change in user's working context."""
    from_context: WorkspaceContext
    to_context: WorkspaceContext
    switch_type: str            # "explicit" | "implicit" | "return"
    time_away: Optional[timedelta] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
```

### Phase 2: Detection Logic

```python
def detect_context_switch(
    current_context: WorkspaceContext,
    previous_context: Optional[WorkspaceContext],
    session_history: List[WorkspaceContext]
) -> Optional[ContextSwitch]:
    """Detect if user has switched contexts."""
    if not previous_context:
        return None

    # Same workspace - no switch
    if current_context.matches(previous_context):
        return None

    # Check for return to earlier context
    for earlier in reversed(session_history[:-1]):
        if current_context.matches(earlier):
            return ContextSwitch(
                from_context=previous_context,
                to_context=current_context,
                switch_type="return",
                time_away=current_context.last_active - earlier.last_active
            )

    # Explicit switch to new context
    return ContextSwitch(
        from_context=previous_context,
        to_context=current_context,
        switch_type="explicit"
    )
```

### Phase 3: PlaceDetector Integration

The existing `PlaceDetector` remains unchanged. Integration happens at call sites:

```python
# Usage pattern
place_detector = PlaceDetector()
place_type = place_detector.detect(spatial_context)
workspace_context = WorkspaceContext.from_spatial_context(
    spatial_context=spatial_context,
    place_type=place_type
)
```

### Phase 4: Tests

Create `tests/unit/services/mux/test_workspace_detection.py`:

1. `TestWorkspaceContext`:
   - `test_from_spatial_context_slack_dm`
   - `test_from_spatial_context_slack_channel`
   - `test_from_spatial_context_web_chat`
   - `test_from_spatial_context_cli`
   - `test_matches_same_workspace`
   - `test_matches_different_workspace`
   - `test_friendly_name_generation`

2. `TestContextSwitch`:
   - `test_creates_with_all_fields`
   - `test_default_timestamp`

3. `TestDetectContextSwitch`:
   - `test_no_switch_when_no_previous`
   - `test_no_switch_same_workspace`
   - `test_explicit_switch_different_workspace`
   - `test_return_switch_to_earlier_context`
   - `test_time_away_calculation`

---

## Completion Matrix

| Criterion | Method | Evidence Required |
|-----------|--------|-------------------|
| `WorkspaceContext` dataclass defined | Write | File exists, imports work |
| `ContextSwitch` dataclass defined | Write | File exists, imports work |
| `detect_context_switch()` implemented | Write | Function callable |
| Detects "explicit" switches | Test | `test_explicit_switch_different_workspace` passes |
| Detects "return" switches | Test | `test_return_switch_to_earlier_context` passes |
| Integrates with PlaceDetector | Test | Integration test with real PlaceDetector |
| Unit tests for all scenarios | Test | All tests pass |
| time_away calculation verified | Test | `test_time_away_calculation` passes |

---

## Execution Order

1. Create `services/mux/workspace_detection.py` with domain models
2. Add detection logic
3. Ensure `services/mux/__init__.py` exports new types
4. Create test file
5. Run tests: `pytest tests/unit/services/mux/test_workspace_detection.py -v`
6. Verify all acceptance criteria

---

## Key Decisions (Adapted from Spec)

1. **WorkspaceContext.from_spatial_context()** - Factory method bridges existing dict-based infrastructure to new typed domain model
2. **matches() method on WorkspaceContext** - Not on nonexistent Place type
3. **detect_context_switch takes WorkspaceContext** - Not Place
4. **No changes to PlaceDetector** - Integration is at call sites
