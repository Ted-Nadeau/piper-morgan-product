# GAMEPLAN: CONV-LEARN-PREF #248 - Conversational Personality Preference Gathering

**Date**: November 22, 2025 (1:17 PM)
**Issue**: #248 (CONV-LEARN-PREF)
**Complexity**: Medium
**Estimated Effort**: 8-12 hours (1-1.5 day sprint)
**Lead Developer**: Claude Code
**Session ID**: [Current]

---

## 🚨 INFRASTRUCTURE VERIFICATION CHECKPOINT

### Infrastructure Confirmation Needed
Before coding, verify all dependencies exist:

```bash
# VERIFY: Personality system exists
✅ services/personality/personality_profile.py (confirmed)
✅ services/personality/enums (ConfidenceDisplayStyle, ActionLevel, TechnicalPreference)
✅ services/domain/user_preference_manager.py (confirmed)

# VERIFY: Learning system exists
? services/learning/pattern_learning.py (search needed)
? PatternType.USER_PREFERENCE_PATTERN (search needed)
? _apply_user_preference_pattern() (search needed)

# VERIFY: Conversation/intent system
✅ services/intent_service/ (exists)
? Intent handlers for personality-related intents
```

**Stop Condition**: If learning infrastructure not found as described in issue #248, STOP and escalate before proceeding.

---

## Context

**Issue Description**: Users should naturally express personality preferences in conversation rather than editing YAML files.

**Current State**:
- ✅ PersonalityProfile system (4 dimensions: warmth, confidence style, action, technical depth)
- ✅ UserPreferenceManager (stores preferences persistently)
- ✅ Learning infrastructure exists (but integration unclear)
- ❌ Conversational detection of preferences missing
- ❌ Natural language extraction not implemented
- ❌ Confirmation UI/flow not built

**Success Vision**: User says "Keep responses brief and technical" → System detects preference → Confirms → Updates profile

---

## DELIVERABLES (Completion Matrix)

| Component | Status | Evidence | Notes |
|-----------|--------|----------|-------|
| **Conversation Analyzer Service** | ⬜ Pending | test file | Detects preference hints |
| **Preference Hint Models** | ⬜ Pending | models.py | Data structures for detected preferences |
| **Natural Language Detection** | ⬜ Pending | test + impl | Regex/NLP for hint extraction |
| **Confirmation Flow** | ⬜ Pending | test + impl | User approval mechanism |
| **Preference Application Logic** | ⬜ Pending | impl | Apply confirmed prefs to profile |
| **Integration Tests** | ⬜ Pending | tests | Full cycle: detect → confirm → apply |
| **Documentation** | ⬜ Pending | doc.md | Usage examples, integration guide |
| **All Tests Passing** | ⬜ Pending | pytest output | 100% pass rate required |

---

## PHASE 0: INFRASTRUCTURE VERIFICATION (30 minutes)

### Checkpoint Tasks
1. Verify personality system structure:
   ```bash
   grep -r "PersonalityProfile\|ConfidenceDisplayStyle" services/ --include="*.py" | head -5
   ```

2. Verify learning infrastructure mentioned in issue:
   ```bash
   grep -r "USER_PREFERENCE_PATTERN\|_apply_user_preference_pattern" services/ --include="*.py"
   grep -r "learning.*pattern" services/ --include="*.py" | head -10
   ```

3. Verify intent service integration points:
   ```bash
   grep -r "IntentService\|handle_intent" services/intent_service/ --include="*.py" | head -10
   ```

4. Check existing personality tests for patterns:
   ```bash
   find tests -name "*personality*" -type f
   ```

### Phase 0 Decision Gate 🚦
- ✅ All infrastructure found? → Continue to Phase 1
- ❌ Learning system not as described? → STOP, escalate to PM with findings
- ⚠️ Partial infrastructure? → STOP, clarify requirements before proceeding

### GitHub Issue Update
```bash
gh issue edit 248 --body "
## Status: Phase 0 - Infrastructure Verification Starting (1:17 PM)
- [ ] Personality system structure verified
- [ ] Learning infrastructure located
- [ ] Intent service integration points identified
- [ ] Existing tests analyzed

Infrastructure Status: Pending verification
Started: $(date)
"
```

---

## PHASE 1: DESIGN & MODELS (1.5-2 hours)

### Phase 1.1: Preference Detection Models (30 min)

**Create**: `services/personality/preference_detection.py`

**Contents**:
```python
# Core data structures
@dataclass
class PreferenceHint:
    """A detected preference from conversation"""
    dimension: str  # "warmth" | "confidence" | "action" | "technical"
    detected_value: Union[float, str]  # 0.0-1.0 or enum value
    confidence_score: float  # 0.0-1.0 (how confident we are)
    source_text: str  # Original text that triggered detection
    reasoning: str  # Why we think this is a preference

@dataclass
class PreferenceConfirmation:
    """User's confirmation of a detected preference"""
    hint: PreferenceHint
    approved: bool
    user_feedback: Optional[str]  # If user rejected, their feedback

# Preference detection patterns
class PreferencePatterns:
    """Registry of patterns for detecting preferences"""
    PATTERNS = {
        "warmth_formal": [...],
        "warmth_friendly": [...],
        "confidence_show": [...],
        "confidence_hide": [...],
        # ... 20+ more patterns
    }
```

**Tests** (`tests/unit/services/personality/test_preference_detection.py`):
```python
def test_preference_hint_structure():
    """Verify PreferenceHint has required fields"""

def test_preference_hint_confidence_range():
    """Confidence score must be 0.0-1.0"""

def test_pattern_registry_coverage():
    """All 4 dimensions have detection patterns"""
```

---

### Phase 1.2: Conversation Analyzer Service (45 min)

**Create**: `services/personality/conversation_analyzer.py`

**Key Methods**:
```python
class ConversationAnalyzer:
    """Detects personality preferences from conversation"""

    async def detect_personality_preferences(
        self,
        conversation_text: str,
        user_id: str
    ) -> List[PreferenceHint]:
        """
        Analyze conversation for preference indicators.

        Returns:
            List of detected preferences with confidence scores
        """

    async def should_suggest_preference(
        self,
        hints: List[PreferenceHint],
        user_id: str
    ) -> Optional[PreferenceHint]:
        """
        Determine if preference should be suggested to user.

        Strategy:
        - High confidence (>0.8) always suggest
        - Medium (0.6-0.8) suggest if new/different from current
        - Low (<0.6) never suggest

        Never suggest multiple at once (non-intrusive)
        """

    async def apply_confirmation(
        self,
        hint: PreferenceHint,
        approval: bool,
        user_id: str
    ) -> Optional[PersonalityProfile]:
        """
        Apply confirmed preference to user's personality profile.

        If approved:
        - Update PersonalityProfile with new preference
        - Store in UserPreferenceManager
        - Log to learning system

        Returns updated profile or None if rejected
        """
```

**Detection Strategy**:
- Regex patterns for explicit signals ("I prefer", "keep it brief", etc.)
- Semantic indicators (formality level, emoji presence, etc.)
- Context clues (domain-specific language, technical jargon)

**Tests** (`tests/unit/services/personality/test_conversation_analyzer.py`):
```python
@pytest.mark.asyncio
async def test_detect_warmth_preference():
    """Detect 'be more friendly' → warmth_level increase"""

@pytest.mark.asyncio
async def test_detect_technical_preference():
    """Detect 'more technical detail' → technical_depth = DETAILED"""

@pytest.mark.asyncio
async def test_confidence_score_thresholds():
    """Only suggest high-confidence detections"""

@pytest.mark.asyncio
async def test_non_intrusive_single_suggestion():
    """Never suggest multiple preferences at once"""
```

---

### Phase 1.3: Integration Point Definition (30 min)

**Where preferences are suggested**: After user response in conversation

**Flow**:
```
1. User sends message
2. System generates response
3. (NEW) Conversation analyzer detects preferences in user's message
4. (NEW) If high confidence, store preference hint
5. System sends response
6. (NEW) After response, offer preference suggestion
7. (NEW) If user approves, apply and update profile
```

**Integration Points**:
- Hook into conversation response flow (likely in IntentService or web handlers)
- Add confirmation UI component (modal or inline)
- Call personality profile updater on approval

---

## PHASE 2: IMPLEMENTATION (4-5 hours)

### Phase 2.1: Detection Patterns Implementation (1.5 hours)

**File**: `services/personality/preference_patterns.py`

**Pattern Categories**:

```python
class WarmthPatterns:
    """Patterns for detecting warmth level preference"""
    INCREASE = [
        r"(?:be|feel|more|please)\s+(?:more\s+)?(?:friendly|warm|casual|personable)",
        r"(?:don't|don't be|less)\s+(?:so\s+)?(?:formal|stiff|corporate|robotic)",
        # ... 5+ patterns
    ]

    DECREASE = [
        r"(?:be|keep|stay)\s+(?:more\s+)?(?:professional|formal|business|corporate)",
        r"(?:less|don't be|tone down)\s+(?:the\s+)?(?:friendliness|warmth|casual)",
        # ... 5+ patterns
    ]

class ConfidencePatterns:
    """Patterns for detecting confidence display preference"""
    SHOW_SCORES = [
        r"(?:show|display|include|give)\s+(?:me\s+)?(?:confidence|certainty)\s+(?:scores|levels|percentages)",
        r"(?:how\s+)?(?:confident|sure)\s+(?:are\s+)?(?:you|is\s+that)",
        # ... patterns
    ]

    HIDE_SCORES = [
        r"(?:don't|stop)\s+(?:showing|displaying)\s+(?:confidence|certainty)",
        r"(?:just\s+)?(?:tell|give)\s+(?:me\s+)?(?:the\s+)?answer(?:\s+without\s+caveats)?",
        # ... patterns
    ]

class ActionPatterns:
    """Patterns for detecting action orientation"""
    HIGH_ACTION = [
        r"(?:give|show|include|with)\s+(?:me\s+)?(?:next\s+)?(?:steps|actions|todos)",
        r"what\s+(?:should|can|do\s+)?i\s+(?:do|try|do\s+next)",
        # ... patterns
    ]

    LOW_ACTION = [
        r"(?:just|only)\s+(?:explain|describe|tell)\s+(?:me|us)",
        r"don't\s+(?:tell\s+)?me\s+what\s+to\s+do",
        # ... patterns
    ]

class TechnicalPatterns:
    """Patterns for detecting technical depth preference"""
    DETAILED = [
        r"(?:more\s+)?(?:technical|detailed|in-depth|comprehensive)",
        r"(?:don't|no need to)\s+(?:simplify|dumb\s+down)",
        # ... patterns
    ]

    SIMPLIFIED = [
        r"(?:simplify|explain\s+like|in\s+plain|for\s+non-technical)",
        r"(?:less|minimize|reduce)\s+(?:jargon|technical\s+terms)",
        # ... patterns
    ]
```

**Scoring Function**:
```python
def detect_preference_from_patterns(text: str) -> List[PreferenceHint]:
    """
    Scan text for preference patterns.

    Returns PreferenceHint for each detected pattern with:
    - confidence_score based on match quality
    - source_text (the actual matched phrase)
    - reasoning (which pattern matched)
    """
```

**Tests**:
```python
def test_warmth_increase_pattern_matching():
    """'be more friendly' detected as warmth increase"""

def test_technical_depth_pattern_matching():
    """'more technical detail' detected as DETAILED"""

def test_confidence_score_accuracy():
    """Perfect match = 1.0, partial = 0.7-0.9, ambiguous = 0.5"""

def test_multiple_patterns_detection():
    """Multiple preferences detected in single message"""
```

---

### Phase 2.2: Confirmation Flow Implementation (1.5 hours)

**File**: `services/personality/preference_confirmer.py`

**Confirmation Strategy**:
```python
class PreferenceConfirmer:
    """Handles user confirmation of detected preferences"""

    async def generate_confirmation_message(
        self,
        hint: PreferenceHint,
        current_profile: PersonalityProfile
    ) -> str:
        """
        Generate user-friendly confirmation message.

        Example:
        "I noticed you prefer more technical explanations.
         Would you like me to use more technical detail in responses?"

        Include:
        - What was detected
        - What will change
        - Yes/No buttons or confirmation prompt
        """

    async def handle_user_response(
        self,
        confirmation_id: str,
        approved: bool,
        user_feedback: Optional[str]
    ) -> PreferenceConfirmation:
        """Process user's yes/no response"""
```

**UI Integration**:
```
[Response about your query...]

🎯 Preference Detected:
I noticed you prefer more technical explanations.
Would you like me to adjust your personality settings?

[Yes] [No] [Ask Later]
```

**Tests**:
```python
async def test_confirmation_message_generation():
    """Message is clear and actionable"""

async def test_user_approval_applies_preference():
    """Yes response updates PersonalityProfile"""

async def test_user_rejection_logs_feedback():
    """No response records why user rejected"""

async def test_preference_not_suggested_twice():
    """Same preference not suggested repeatedly"""
```

---

### Phase 2.3: Application Logic (1.5 hours)

**File**: Update `services/personality/personality_profile.py`

**New Methods**:
```python
class PersonalityProfile:
    async def apply_detected_preference(
        self,
        hint: PreferenceHint
    ) -> 'PersonalityProfile':
        """
        Apply detected preference to this profile.

        Dimension mapping:
        - "warmth" → update warmth_level
        - "confidence" → update confidence_style (enum)
        - "action" → update action_orientation (enum)
        - "technical" → update technical_depth (enum)

        Returns updated profile
        """

    def get_adjustment_preview(
        self,
        hint: PreferenceHint
    ) -> Dict[str, Any]:
        """
        Show user what will change before they approve.

        Returns:
        {
            "dimension": "warmth",
            "current_value": 0.5,
            "new_value": 0.7,
            "description": "Responses will be friendlier"
        }
        """
```

**Integration with UserPreferenceManager**:
```python
# After user approves preference
await preference_manager.set_preference(
    f"personality_{hint.dimension}",
    hint.detected_value,
    ttl_minutes=None  # Permanent preference
)

# Log to learning system
await learning_system.log_pattern(
    pattern_type=PatternType.USER_PREFERENCE_PATTERN,
    metadata={"hint": hint, "source": "conversational_detection"}
)
```

**Tests**:
```python
async def test_warmth_preference_application():
    """Warmth preference properly updates profile"""

async def test_confidence_style_enum_application():
    """Confidence style converted to correct enum"""

async def test_preference_persistence():
    """Preference saved to UserPreferenceManager"""

async def test_learning_system_logging():
    """Preference logged for learning system"""
```

---

### Phase 2.4: Intent Handler Hook (1 hour)

**Where to integrate**:
- After response generation in chat endpoint
- Before response returned to user

**Implementation**:
```python
# In web/api/routes/chat.py or similar
async def chat_endpoint(request):
    # Generate response (existing)
    response = await generate_response(request)

    # (NEW) Detect preferences in user's message
    preferences = await analyzer.detect_personality_preferences(
        request.message,
        user_id=current_user.id
    )

    # (NEW) Suggest if confident enough
    suggestion = await analyzer.should_suggest_preference(
        preferences,
        user_id=current_user.id
    )

    # (NEW) If suggestion, add to response
    if suggestion:
        response["preference_suggestion"] = {
            "id": generate_id(),
            "message": await confirmer.generate_confirmation_message(suggestion, profile),
            "hint": suggestion
        }

    return response
```

**Client-side handling** (frontend):
```javascript
// Listen for preference suggestions
if (response.preference_suggestion) {
    showConfirmationModal(response.preference_suggestion);

    // On user approval
    await POST `/api/preferences/confirm` {
        suggestion_id: response.preference_suggestion.id,
        approved: true/false
    }
}
```

---

## PHASE 3: TESTING & VALIDATION (2-3 hours)

### Phase 3.1: Unit Tests (1 hour)
- Pattern detection accuracy tests
- Preference hint scoring tests
- Profile application tests
- Preference manager integration tests

**Target**: 20+ unit tests, 100% pass rate

```bash
pytest tests/unit/services/personality/ -v
# Expected: All tests pass in <5 seconds
```

---

### Phase 3.2: Integration Tests (1 hour)

**Full cycle test**: Detection → Confirmation → Application

```python
@pytest.mark.asyncio
async def test_preference_gathering_full_cycle():
    """End-to-end: detect → confirm → apply"""
    # 1. Simulate user message with preference hint
    user_message = "Please be more technical in your explanations"

    # 2. Detect preference
    hints = await analyzer.detect_personality_preferences(user_message)
    assert len(hints) > 0
    assert hints[0].dimension == "technical"

    # 3. Get suggestion
    suggestion = await analyzer.should_suggest_preference(hints)
    assert suggestion is not None

    # 4. User approves
    confirmation = await confirmer.handle_user_response(
        suggestion.id,
        approved=True,
        user_feedback=None
    )
    assert confirmation.approved

    # 5. Apply to profile
    updated_profile = await profile.apply_detected_preference(suggestion.hint)
    assert updated_profile.technical_depth == TechnicalPreference.DETAILED

    # 6. Verify persistence
    stored_pref = await preference_manager.get_preference(
        f"personality_technical"
    )
    assert stored_pref == TechnicalPreference.DETAILED
```

**Test scenarios**:
- Simple detection (one clear preference)
- Multiple detections (several hints in one message)
- Low confidence rejection (not suggested)
- User rejection (feedback recorded)
- Duplicate suggestion prevention (not suggested twice)

---

### Phase 3.3: Manual Testing (30 min)

**Scenario 1: Natural Warmth Preference**
```
User: "Can you be more casual with me? I find the formal tone a bit stiff."
Expected:
  - Warmth preference detected
  - Suggestion offered
  - User approves
  - Profile updated to higher warmth
```

**Scenario 2: Technical Depth**
```
User: "I'd prefer more technical detail. I can handle complexity."
Expected:
  - Technical depth preference detected (DETAILED)
  - Suggestion offered
  - User approves
  - Profile updated
```

**Scenario 3: Multiple Preferences**
```
User: "Keep it brief and technical. Don't explain basics."
Expected:
  - Technical detected (DETAILED)
  - Action detected (LOW) - opposite of "don't explain"
  - Only suggest highest confidence one
  - Not intrusive
```

---

## PHASE 4: DOCUMENTATION (1 hour)

### Create: `docs/internal/development/personality/conversational-preference-gathering.md`

**Contents**:
1. Overview of feature
2. User workflow (how to use)
3. Technical architecture
4. Integration guide for developers
5. Testing procedures
6. Future enhancements

---

## 🛑 CRITICAL STOP CONDITIONS

**STOP immediately if**:

1. **Learning system not as described**
   - Issue mentions `PatternType.USER_PREFERENCE_PATTERN` and `_apply_user_preference_pattern()`
   - If not found after reasonable search, STOP
   - Escalate with: "Learning infrastructure doesn't match issue description"

2. **PersonalityProfile structure insufficient**
   - Must have 4 dimensions: warmth, confidence style, action, technical depth
   - Missing any dimension = STOP
   - Escalate with: "PersonalityProfile doesn't support all 4 dimensions"

3. **Tests start failing mid-implementation**
   - Don't skip failing tests
   - Stop immediately, investigate root cause
   - Don't add more code until tests pass

4. **Pattern detection producing >20% false positives**
   - If testing shows many wrong detections, algorithm needs redesign
   - Don't just lower confidence threshold
   - Stop and reconsider pattern approach

5. **Preference application breaks existing profile**
   - If updating a preference corrupts other dimensions, STOP
   - Verify profile update logic is atomic
   - Don't proceed until safe

6. **Pre-commit hooks failing**
   - If linting/formatting fails, fix immediately
   - Don't commit broken code
   - Use `./scripts/fix-newlines.sh` before each commit

---

## COMPLETION MATRIX

| Component | Target | Status | Evidence |
|-----------|--------|--------|----------|
| **Infrastructure Verification** | 100% | ⬜ | Bash output confirming files |
| **Preference Detection Models** | Complete | ⬜ | test file + models.py |
| **Conversation Analyzer Service** | Full implementation | ⬜ | service.py + tests |
| **Detection Patterns** | 20+ patterns | ⬜ | patterns.py |
| **Confirmation Flow** | Complete | ⬜ | confirmer.py + tests |
| **Profile Application** | All 4 dimensions | ⬜ | impl in personality_profile.py |
| **Intent Handler Integration** | Working | ⬜ | Integration in chat endpoint |
| **Unit Tests** | 20+, 100% pass | ⬜ | pytest output |
| **Integration Tests** | 5+, full cycle | ⬜ | pytest output |
| **Manual Testing** | 3+ scenarios pass | ⬜ | Documented in session log |
| **Documentation** | Complete guide | ⬜ | markdown file |
| **Pre-commit Hooks** | All passing | ⬜ | Git output |
| **All Tests Final** | 100% pass | ⬜ | pytest output |

**Definition of COMPLETE**:
- ✅ All completion matrix items have evidence
- ✅ All tests passing (unit + integration)
- ✅ Manual testing scenarios work
- ✅ No STOP conditions triggered
- ✅ Documentation complete
- ✅ Code committed and pushed

---

## GIT WORKFLOW

**Branch**: Working on main (per session instructions)

**Commits**:
1. After Phase 1 (models + patterns)
   ```
   feat(CONV-LEARN-PREF): Add preference detection models and patterns
   ```

2. After Phase 2.1-2.2 (services)
   ```
   feat(CONV-LEARN-PREF): Implement ConversationAnalyzer and ConfirmationFlow
   ```

3. After Phase 2.3-2.4 (integration)
   ```
   feat(CONV-LEARN-PREF): Integrate preference gathering into chat flow
   ```

4. After Phase 3 (tests)
   ```
   test(CONV-LEARN-PREF): Add comprehensive test suite
   ```

5. Final
   ```
   docs(CONV-LEARN-PREF): Add documentation and examples

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

---

## EFFORT ESTIMATE

| Phase | Task | Estimate | Actual |
|-------|------|----------|--------|
| 0 | Infrastructure Verification | 30 min | ⬜ |
| 1.1 | Models & Data Structures | 30 min | ⬜ |
| 1.2 | Analyzer Service Design | 45 min | ⬜ |
| 1.3 | Integration Points | 30 min | ⬜ |
| 2.1 | Detection Patterns | 1.5 h | ⬜ |
| 2.2 | Confirmation Flow | 1.5 h | ⬜ |
| 2.3 | Application Logic | 1.5 h | ⬜ |
| 2.4 | Intent Handler Hook | 1 h | ⬜ |
| 3.1 | Unit Tests | 1 h | ⬜ |
| 3.2 | Integration Tests | 1 h | ⬜ |
| 3.3 | Manual Testing | 30 min | ⬜ |
| 4 | Documentation | 1 h | ⬜ |
| **TOTAL** | | **10.5 h** | ⬜ |

**Buffer**: 1.5 hours (for debugging/refinement)
**Total with buffer**: ~12 hours

---

## DECISION GATES

🚦 **Phase 0 Gate** (Infrastructure Verification):
- If all systems found: Continue to Phase 1 ✅
- If missing learning system: Escalate to PM ❌
- Proceed: **YES / NO?**

🚦 **Phase 1 Gate** (Design Complete):
- Review models and patterns for completeness
- Confirm integration points are clear
- Proceed: **YES / NO?**

🚦 **Phase 2 Gate** (Implementation Halfway):
- After Phase 2.2 (services implemented)
- Verify tests are passing
- If tests failing: Debug before continuing
- Proceed: **YES / NO?**

🚦 **Phase 3 Gate** (Testing Complete):
- All unit tests passing
- All integration tests passing
- Manual scenarios working
- No STOP conditions triggered
- Ready for merge: **YES / NO?**

---

## NEXT ACTION

✅ **Ready to start Phase 0 Infrastructure Verification**

1. Execute verification commands
2. Document findings in this gameplan
3. Report infrastructure status
4. If clear to proceed: Start Phase 1 design

**Proceed with Phase 0?** 🚦

---

**Gameplan Status**: Ready for execution
**Last Updated**: 1:17 PM, November 22, 2025
**Lead Developer**: Claude Code
**PM**: xian
