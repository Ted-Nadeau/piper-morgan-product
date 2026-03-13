# Gameplan: #626 Onboarding System Grammar Transform

## Overview
Transform onboarding from functional task-completion to warm relationship establishment.

**Key Insight**: Onboarding is Piper and user's FIRST MEETING. This is the moment to establish the relationship, not just collect project data.

## Phase 1: OnboardingGrammarContext

**File**: `services/onboarding/grammar_context.py`

```python
@dataclass
class OnboardingGrammarContext:
    """Rich context for grammar-conscious onboarding responses."""

    # Stage tracking
    stage: OnboardingStage = OnboardingStage.WELCOME

    # Relationship context
    is_first_meeting: bool = True

    # Progress context
    projects_captured: int = 0
    project_names: List[str] = field(default_factory=list)

    # User signals
    user_seems_hesitant: bool = False
    user_seems_eager: bool = False

    # Personality calibration (higher warmth for onboarding)
    warmth_level: float = 0.8  # Default warm for first meeting

    # Context availability
    context_available: bool = True
```

**Enum**:
```python
class OnboardingStage(str, Enum):
    WELCOME = "welcome"        # Initial greeting
    GATHERING = "gathering"    # Collecting projects
    CONFIRMING = "confirming"  # Confirming captured projects
    COMPLETE = "complete"      # Successfully onboarded
    DECLINED = "declined"      # User declined
```

**Tests**: ~20 tests
- Context creation from session state
- Stage detection
- User signal detection
- Formality derivation

---

## Phase 2: OnboardingNarrativeBridge

**File**: `services/onboarding/narrative_bridge.py`

```python
@dataclass
class OnboardingNarrativeBridge:
    """Transform onboarding context into warm, relationship-building phrases."""

    # Welcome messages (first meeting!)
    WELCOME_MESSAGES = {
        "warm": "Hi there! I'm Piper, and I'm excited to be your PM assistant...",
        "conversational": "Hello! I'm Piper, your PM assistant...",
        ...
    }

    # Place atmosphere
    PLACE_ATMOSPHERE = {
        "warm": "Welcome to your workspace - I'm here to help you stay organized...",
        ...
    }

    # Project acknowledgments (genuine interest)
    PROJECT_ACKNOWLEDGMENTS = {
        "first": "That sounds like a great project to be working on!",
        "additional": "Nice - I'd love to help you with that one too.",
        ...
    }

    # Completion celebrations
    COMPLETION_PHRASES = {
        "warm": "Wonderful! I'm looking forward to working together...",
        ...
    }
```

**Methods**:
- `get_welcome_message(ctx)` - First meeting greeting
- `get_place_atmosphere(ctx)` - Workspace welcome
- `acknowledge_project(ctx, project_name)` - Genuine interest
- `get_gathering_prompt(ctx)` - Ask about more projects
- `get_confirmation_prompt(ctx)` - Natural confirmation
- `celebrate_completion(ctx)` - Relationship established!
- `handle_decline(ctx)` - Warm, door-open goodbye
- `get_lost_session_message(ctx)` - Warm error recovery

**Tests**: ~30 tests
- Stage-appropriate messages
- Warmth calibration
- Project count awareness
- Contractor Test compliance

---

## Phase 3: Narrative Helpers

**File**: `services/onboarding/narrative_helpers.py`

```python
def get_welcome_message(
    warmth_level: float = 0.8,
    include_atmosphere: bool = True,
) -> str:
    """Get warm welcome for first meeting."""

def acknowledge_project(
    project_name: str,
    is_first_project: bool = True,
    warmth_level: float = 0.8,
) -> str:
    """Acknowledge project with genuine interest."""

def get_confirmation_prompt(
    project_names: List[str],
    warmth_level: float = 0.8,
) -> str:
    """Get natural confirmation prompt."""

def celebrate_completion(
    project_names: List[str],
    warmth_level: float = 0.8,
) -> str:
    """Celebrate successful onboarding."""

def handle_decline_warmly(
    had_projects: bool = False,
    warmth_level: float = 0.8,
) -> str:
    """Handle decline with warmth and open door."""
```

**Tests**: ~20 tests
- Helper function outputs
- Default behavior
- Contractor Test compliance

---

## Phase 4: Integration

**Update**: `services/onboarding/__init__.py`

Add exports:
- `OnboardingGrammarContext`
- `OnboardingStage`
- `OnboardingNarrativeBridge`
- All helper functions

**Verify**: All existing tests still pass + new grammar tests

---

## Completion Matrix

| Phase | Files | Tests | Status |
|-------|-------|-------|--------|
| 1 | grammar_context.py | ~20 | Pending |
| 2 | narrative_bridge.py | ~30 | Pending |
| 3 | narrative_helpers.py | ~20 | Pending |
| 4 | __init__.py update | verify | Pending |

**Total Expected**: ~70 new tests

---

## Key Phrases to Transform

| Current | Transformed |
|---------|-------------|
| "Hello! I'm Piper Morgan, your PM assistant. I notice we haven't set up..." | "Hi there! I'm Piper, and I'm excited to be your PM assistant. Since we're just meeting, I'd love to learn about what you're working on..." |
| "Got it - {project}." | "That sounds interesting! {project} - I'd love to help you with that." |
| "All set! I've added..." | "Wonderful! I'm looking forward to helping you with {projects}. We're going to work well together!" |
| "No problem!" | "No rush at all - I'll be here whenever you're ready. In the meantime, what can I help you with?" |

---

## Contractor Test Examples

**Welcome** (should sound like meeting a helpful colleague):
- ✅ "Hi there! I'm Piper, and I'm excited to be your PM assistant."
- ❌ "Onboarding initiated. Please provide project information."

**Project Acknowledgment** (genuine interest):
- ✅ "That sounds like a great project! I'd love to help you stay on track with it."
- ❌ "Project 'X' captured. Continue?"

**Completion** (relationship celebration):
- ✅ "Wonderful! I'm looking forward to working together on these projects."
- ❌ "Onboarding complete. 3 projects saved."
