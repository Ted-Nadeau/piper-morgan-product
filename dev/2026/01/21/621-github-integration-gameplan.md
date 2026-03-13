# Gameplan: GitHub Integration Grammar Transformation (#621)

**Issue**: #621 GRAMMAR-TRANSFORM: GitHub Integration (Partial → Conscious)
**Author**: Lead Developer (Claude Code / Opus)
**Date**: 2026-01-21
**Prerequisites**: #619, #620 complete (can reuse patterns)

---

## Strategic Insight

GitHub's 8-dimensional spatial intelligence is excellent - the analysis is deep and rich. The gap is purely in **presentation**: raw data structures need to become human narratives.

**Focus**: Narrative bridge layer, not data layer changes.

---

## Phase Overview

| Phase | Focus | Effort | Parallelizable |
|-------|-------|--------|----------------|
| 1 | GitHubResponseContext | 1h | No (foundation) |
| 2 | GitHub Narrative Bridge | 2h | After Phase 1 |
| 3 | Canonical Handler Integration | 2h | After Phase 2 |
| 4 | Testing | 1.5h | After Phase 3 |
| **Total** | | **6.5h** | |

---

## Phase 1: GitHubResponseContext

### Objective
Create a context dataclass for GitHub-specific grammar-conscious responses.

### Deliverables

**File**: `services/integrations/github/response_context.py`

```python
@dataclass
class GitHubResponseContext:
    """Rich context for grammar-conscious GitHub responses."""

    # Repository context
    repo_name: str
    repo_atmosphere: str  # "active", "quiet", "hot"

    # Item context
    item_type: str  # "issue", "pr", "commit"
    item_number: int
    item_title: str

    # Temporal context
    age_days: int
    activity_level: str  # "active", "recent", "stale"
    last_activity_hours: float

    # Priority context
    priority_level: str  # "critical", "high", "normal", "low"
    attention_score: float

    # Collaborative context
    author: str
    assignees: List[str]
    reviewers: List[str]
    comment_count: int

    # State context
    state: str  # "open", "closed", "merged"
    is_blocked: bool

    @classmethod
    def from_spatial_analysis(cls, issue_data: Dict, spatial: Dict) -> "GitHubResponseContext":
        """Build from GitHub issue data and spatial analysis."""
        ...
```

### Tests
- `tests/unit/services/integrations/github/test_response_context.py`
- Test from_spatial_analysis() factory
- Test atmosphere detection
- Test priority extraction

### Acceptance Criteria
- [ ] GitHubResponseContext dataclass created
- [ ] from_spatial_analysis() works
- [ ] All tests pass

---

## Phase 2: GitHub Narrative Bridge

### Objective
Create transformation functions that turn GitHub data into experiential narratives.

### Deliverables

**File**: `services/integrations/github/narrative_bridge.py`

```python
class GitHubNarrativeBridge:
    """Transform GitHub data into experiential narratives."""

    # Temporal narratives
    AGE_NARRATIVES = {
        "recent": "just created",
        "days": "has been open for {days} days",
        "weeks": "has been waiting for {weeks} weeks",
        "months": "has been around for {months} months",
    }

    ACTIVITY_NARRATIVES = {
        "active": "has lots of activity",
        "recent": "had some recent activity",
        "moderate": "has been pretty quiet",
        "stale": "has been quiet for a while",
    }

    PRIORITY_NARRATIVES = {
        "critical": "needs attention right away",
        "high": "is high priority",
        "normal": "",  # Don't mention normal priority
        "low": "is lower priority",
    }

    STATE_NARRATIVES = {
        "waiting_review": "waiting for someone to review",
        "blocked": "is stuck on something",
        "ready_merge": "is ready to merge",
        "needs_work": "needs some work",
    }

    def narrate_issue(self, ctx: GitHubResponseContext) -> str:
        """Create full narrative for an issue/PR."""
        ...

    def narrate_age(self, age_days: int) -> str:
        """Convert age to human-readable form."""
        if age_days == 0:
            return "just created"
        elif age_days == 1:
            return "created yesterday"
        elif age_days < 7:
            return f"open for {age_days} days"
        elif age_days < 30:
            weeks = age_days // 7
            return f"waiting for {weeks} {'week' if weeks == 1 else 'weeks'}"
        else:
            months = age_days // 30
            return f"around for {months} {'month' if months == 1 else 'months'}"

    def narrate_activity(self, activity_level: str) -> str:
        """Convert activity level to narrative."""
        return self.ACTIVITY_NARRATIVES.get(activity_level, "")

    def narrate_priority(self, priority_level: str) -> str:
        """Convert priority to narrative."""
        return self.PRIORITY_NARRATIVES.get(priority_level, "")

    def narrate_state(self, ctx: GitHubResponseContext) -> str:
        """Convert state to narrative based on full context."""
        if ctx.item_type == "pr":
            if not ctx.reviewers:
                return "waiting for someone to review"
            elif ctx.is_blocked:
                return "is stuck on something"
        return ""
```

### Tests
- Test each narrate_* function
- Test full narrate_issue() output
- Test edge cases (0 days, 1 day, etc.)
- Contractor Test: no technical jargon

### Acceptance Criteria
- [ ] GitHubNarrativeBridge class created
- [ ] All narrate_* functions implemented
- [ ] Tests verify human-readable output
- [ ] No raw data in narratives

---

## Phase 3: Canonical Handler Integration

### Objective
Update canonical handlers that present GitHub data to use the narrative bridge.

### Key Handlers to Update

**File**: `services/intent_service/canonical_handlers.py`

Search for GitHub-related handlers:
- Stale PR detection
- Issue listing
- PR review status
- Activity queries

### Example Transformation

**Before**:
```python
result = {
    "issues": [
        {"title": "Fix bug", "state": "open", "age_days": 14}
    ]
}
```

**After**:
```python
narrative_bridge = GitHubNarrativeBridge()
narratives = []
for issue in issues:
    ctx = GitHubResponseContext.from_issue(issue)
    narratives.append(narrative_bridge.narrate_issue(ctx))
# "Fix bug has been waiting for two weeks and is quiet lately"
```

### Acceptance Criteria
- [ ] Identified all GitHub-related canonical handlers
- [ ] Updated handlers to use narrative bridge
- [ ] Raw data no longer exposed in user-facing responses

---

## Phase 4: Testing

### Test Scenarios

1. **Issue Age Narration**
   - 0 days → "just created"
   - 1 day → "created yesterday"
   - 7 days → "waiting for a week"
   - 30 days → "around for a month"

2. **Activity Narration**
   - Active → "has lots of activity"
   - Stale → "been quiet for a while"

3. **PR State Narration**
   - No reviewers → "waiting for someone to review"
   - Blocked → "is stuck on something"

4. **Full Narrative**
   - Combines all elements naturally
   - Reads like a sentence, not a list

### Contractor Test
- No "activity_level", "age_days", etc. in output
- Professional language
- Not overly verbose

---

## Completion Matrix

| Phase | Component | Tests | Evidence |
|-------|-----------|-------|----------|
| 1 | GitHubResponseContext | ⬜ | Dataclass works |
| 2 | GitHubNarrativeBridge | ⬜ | Narratives human-readable |
| 3 | Canonical Handler Integration | ⬜ | No raw data in responses |
| 4 | Testing | ⬜ | All tests green |

---

## Files to Create/Modify

| File | Action | Phase |
|------|--------|-------|
| `services/integrations/github/response_context.py` | Create | 1 |
| `services/integrations/github/narrative_bridge.py` | Create | 2 |
| `services/intent_service/canonical_handlers.py` | Modify | 3 |
| `tests/unit/services/integrations/github/test_response_context.py` | Create | 1 |
| `tests/unit/services/integrations/github/test_narrative_bridge.py` | Create | 2 |

---

## Experience Test Validation

After implementation, verify these transformations:

| Input | Output (should be) |
|-------|-------------------|
| `{"age_days": 14, "activity_level": "stale"}` | "has been waiting for two weeks and is quiet lately" |
| `{"priority_level": "critical", "state": "open"}` | "needs attention right away" |
| `{"item_type": "pr", "reviewers": []}` | "waiting for someone to review" |
| `{"comment_count": 0}` | "no one's weighed in yet" |

---

*Ready for PM approval*
