# Preference Detection - Development Guide

**For Contributors**: How to develop and extend the preference detection system

---

## Architecture

```
services/personality/
├─ preference_detection.py
│  ├─ PreferenceDimension enum (WARMTH, CONFIDENCE, ACTION, TECHNICAL)
│  ├─ DetectionMethod enum (LANGUAGE_PATTERNS, BEHAVIORAL_SIGNALS, etc.)
│  ├─ ConfidenceLevel enum (VERY_HIGH, HIGH, MEDIUM, LOW)
│  ├─ PreferenceHint dataclass (detected preferences)
│  ├─ PreferenceConfirmation dataclass (user confirmations)
│  └─ PreferenceDetectionResult dataclass (detection output)
│
├─ conversation_analyzer.py
│  ├─ ConversationAnalyzer class
│  │  ├─ Language pattern word sets (WARM_WORDS, TECHNICAL_WORDS, etc.)
│  │  ├─ _detect_warmth_preference()
│  │  ├─ _detect_confidence_preference()
│  │  ├─ _detect_action_preference()
│  │  ├─ _detect_technical_preference()
│  │  └─ analyze_message() - main detection orchestration
│  │
│  └─ Explanation generation for each detection method
│
└─ personality_profile.py
   ├─ PersonalityProfile dataclass
   ├─ Enums: ConfidenceDisplayStyle, ActionLevel, TechnicalPreference
   └─ load_with_preferences() - load from DB

services/intent_service/
├─ preference_handler.py
│  ├─ PreferenceDetectionHandler class
│  │  ├─ _store_hints_in_session() - session storage (30-min TTL)
│  │  ├─ _retrieve_hint_from_session() - session retrieval
│  │  ├─ confirm_preference() - user confirmation
│  │  ├─ apply_auto_preferences() - silent application
│  │  ├─ suggest_preferences() - generate suggestions
│  │  └─ _log_preference_to_learning() - learning integration
│  │
│  └─ Global _SESSION_HINTS dict for temporary storage
│
└─ intent_hooks.py
   ├─ IntentProcessingHooks class
   ├─ on_intent_classified() - post-classification hook
   └─ _run_preference_detection() - preference detection orchestration

web/api/routes/
└─ preferences.py
   ├─ POST /preferences/hints/{id}/accept
   ├─ POST /preferences/hints/{id}/dismiss
   ├─ GET /preferences/profile
   ├─ GET /preferences/stats
   └─ GET /preferences/health
```

---

## Key Data Structures

### PreferenceHint

```python
@dataclass
class PreferenceHint:
    id: str  # Unique hint ID
    user_id: str  # User this hint is for
    dimension: PreferenceDimension  # Which dimension (WARMTH, etc.)
    detected_value: Any  # What value was detected
    current_value: Any  # Current setting (from profile)
    confidence_score: float  # 0.0-1.0
    detection_method: DetectionMethod  # How it was detected
    source_text: str  # User message that triggered detection
    evidence: Dict[str, Any] = field(default_factory=dict)  # Supporting data
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None  # For session hints

    def confidence_level(self) -> ConfidenceLevel:
        """Map confidence score to level"""
        if self.confidence_score >= 0.9:
            return ConfidenceLevel.VERY_HIGH
        elif self.confidence_score >= 0.7:
            return ConfidenceLevel.HIGH
        elif self.confidence_score >= 0.4:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    def is_ready_for_suggestion(self) -> bool:
        """Can be shown to user as suggestion?"""
        return self.confidence_score >= 0.4

    def is_ready_for_auto_apply(self) -> bool:
        """Can be applied silently without user confirmation?"""
        return (
            self.confidence_score >= 0.9 and
            self.detection_method == DetectionMethod.EXPLICIT_FEEDBACK
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for storage/API"""
        return {
            "id": self.id,
            "dimension": self.dimension.value,
            "detected_value": str(self.detected_value),
            "current_value": str(self.current_value),
            "confidence_score": self.confidence_score,
            "detection_method": self.detection_method.value,
            "source_text": self.source_text,
            # ... additional fields
        }
```

### PreferenceDetectionResult

```python
@dataclass
class PreferenceDetectionResult:
    hints: List[PreferenceHint] = field(default_factory=list)
    suggested_hints: List[PreferenceHint] = field(default_factory=list)
    auto_apply_hints: List[PreferenceHint] = field(default_factory=list)
    analysis_summary: str = ""
    confidence_summary: Dict[PreferenceDimension, float] = field(default_factory=dict)
    detected_at: datetime = field(default_factory=datetime.utcnow)

    def has_suggestions(self) -> bool:
        return len(self.suggested_hints) > 0

    def has_auto_applies(self) -> bool:
        return len(self.auto_apply_hints) > 0
```

---

## Development Workflow

### Adding a New Detection Method

**Example**: Add detection based on response length preference

1. **Add to DetectionMethod enum**:
   ```python
   class DetectionMethod(Enum):
       # ... existing methods ...
       RESPONSE_LENGTH_PATTERN = "response_length_pattern"
   ```

2. **Create detection function in ConversationAnalyzer**:
   ```python
   def _detect_response_length_preference(self, user_id, message, current_profile):
       """Detect if user wants shorter/longer responses"""
       if "longer" in message.lower():
           return PreferenceHint(
               id=self._next_hint_id(),
               user_id=user_id,
               dimension=PreferenceDimension.ACTION,  # Or create new dimension
               detected_value="HIGH",
               current_value=current_profile.action_orientation,
               detection_method=DetectionMethod.RESPONSE_LENGTH_PATTERN,
               confidence_score=0.7,
               source_text=message,
               evidence={"keyword": "longer"}
           )
       return None
   ```

3. **Integrate into analyze_message()**:
   ```python
   async def analyze_message(self, user_id, message, current_profile):
       result = PreferenceDetectionResult()

       # ... existing detections ...

       # Add new detection
       length_hint = self._detect_response_length_preference(user_id, message, current_profile)
       if length_hint:
           result.hints.append(length_hint)
           if length_hint.is_ready_for_suggestion():
               result.suggested_hints.append(length_hint)

       return result
   ```

4. **Add explanation**:
   ```python
   def _generate_explanation(self, hint: PreferenceHint) -> str:
       if hint.detection_method == DetectionMethod.RESPONSE_LENGTH_PATTERN:
           return f"Detected preference for {hint.detected_value.lower()} action orientation"
       # ... other methods ...
   ```

5. **Test it**:
   ```python
   @pytest.mark.asyncio
   async def test_detect_response_length_preference():
       analyzer = ConversationAnalyzer()
       profile = create_mock_profile()

       message = "I'd like longer, more detailed responses"
       result = analyzer.analyze_message("user123", message, profile)

       assert any(h.detection_method == DetectionMethod.RESPONSE_LENGTH_PATTERN for h in result.hints)
   ```

### Adding a New Personality Dimension

**Currently supported**: 4 dimensions (warmth, confidence, action, technical)

To add a new dimension:

1. **Add to PreferenceDimension enum**:
   ```python
   class PreferenceDimension(Enum):
       WARMTH = "warmth_level"
       CONFIDENCE = "confidence_style"
       ACTION = "action_orientation"
       TECHNICAL = "technical_depth"
       YOUR_DIMENSION = "your_dimension"  # ← Add here
   ```

2. **Add to PersonalityProfile**:
   ```python
   @dataclass
   class PersonalityProfile:
       warmth_level: float = 0.5
       confidence_style: ConfidenceDisplayStyle = CONTEXTUAL
       action_orientation: ActionLevel = MEDIUM
       technical_depth: TechnicalPreference = BALANCED
       your_dimension: YourType = DEFAULT_VALUE  # ← Add here
   ```

3. **Create detection method**:
   ```python
   def _detect_your_dimension_preference(self, user_id, message, current_profile):
       # Your detection logic
       # Return PreferenceHint with dimension=PreferenceDimension.YOUR_DIMENSION
   ```

4. **Update database schema** (if persistent storage needed)

### Improving Confidence Scoring

Confidence scoring currently uses word ratios:
```python
warm_score = len(words & self.WARM_WORDS) / (len(words) + 1)
confidence = min(0.7, warm_score * 2)
```

To improve:

1. **Add context weighting**:
   ```python
   def _calculate_warmth_confidence(self, message, warm_words, professional_words):
       word_ratio = len(warm_words & words) / (len(words) + 1)

       # Weight by position (words at end more significant)
       positional_weight = sum(
           (len(words) - i) / len(words)  # Recent words weighted more
           for i, word in enumerate(words)
           if word in warm_words
       ) / len(words)

       # Weight by sentence structure
       exclamation_weight = message.count('!') * 0.1

       combined = (word_ratio * 0.5 + positional_weight * 0.3 + exclamation_weight * 0.2)
       return min(0.7, combined * 2)
   ```

2. **Use NLP for better understanding**:
   ```python
   from transformers import pipeline

   # Use sentiment analysis
   sentiment_pipe = pipeline("sentiment-analysis")
   sentiment = sentiment_pipe(message)

   # Combine with word matching
   combined_confidence = (word_match_score + sentiment_confidence) / 2
   ```

3. **Test improvements**:
   ```python
   def test_improved_confidence_scoring():
       analyzer = ConversationAnalyzer()

       # Test messages with varying confidence signals
       test_cases = [
           ("I really love your approach!", 0.8),  # High confidence
           ("Maybe your approach is okay", 0.3),   # Low confidence
           # ... more cases
       ]

       for message, expected_confidence in test_cases:
           result = analyzer._calculate_warmth_confidence(message, ...)
           assert abs(result - expected_confidence) < 0.1
   ```

---

## Testing Guidelines

### Unit Tests (in `tests/unit/services/personality/`)

Test individual components in isolation:

```python
def test_preference_hint_confidence_levels():
    """Test confidence level classification"""
    # High confidence
    hint = PreferenceHint(confidence_score=0.95, ...)
    assert hint.confidence_level() == ConfidenceLevel.VERY_HIGH

    # Medium confidence
    hint = PreferenceHint(confidence_score=0.5, ...)
    assert hint.confidence_level() == ConfidenceLevel.MEDIUM
```

### Integration Tests (in `tests/integration/services/personality/`)

Test complete flows:

```python
@pytest.mark.asyncio
async def test_complete_preference_flow():
    """Test detect → confirm → store → apply"""
    # Detect preference
    result = analyzer.analyze_message(user_id, message, profile)
    assert len(result.suggested_hints) > 0

    # Confirm preference
    confirmation = await handler.confirm_preference(
        user_id=user_id,
        session_id=session_id,
        hint_id=result.suggested_hints[0].id,
        accepted=True
    )
    assert confirmation["success"]
```

### Performance Tests

```python
@pytest.mark.benchmark
def test_analyze_message_performance(benchmark):
    """Ensure preference detection stays fast"""
    analyzer = ConversationAnalyzer()
    profile = create_mock_profile()

    result = benchmark(
        analyzer.analyze_message,
        "user_id",
        "Long message with many preference signals...",
        profile
    )

    # Should complete in <50ms
    assert result is not None
```

---

## Code Style

### Naming Conventions

- `_detect_*_preference()`: Private detection methods
- `on_*()`: Hook methods
- `is_ready_for_*()`: Boolean check methods
- `*_hints`: Variables holding lists of hints
- `*_result`: Variables holding detection results

### Documentation

Always document detection methods:

```python
def _detect_warmth_preference(self, user_id: str, message: str, current_profile: Any) -> Optional[PreferenceHint]:
    """
    Detect warmth/friendliness preference from message.

    Analyzes user message for signals of preference toward warmth (0.8+) or
    professionalism (0.3-). Uses word matching against WARM_WORDS and
    PROFESSIONAL_WORDS sets.

    Args:
        user_id: User ID
        message: User's message text
        current_profile: Current PersonalityProfile

    Returns:
        PreferenceHint if preference detected, None otherwise

    Examples:
        >>> analyzer = ConversationAnalyzer()
        >>> hint = analyzer._detect_warmth_preference("user1", "I love your friendly tone!", profile)
        >>> hint.detected_value
        0.8
    """
    # ... implementation ...
```

---

## Debugging Tips

### Enable Detailed Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log detection details
logger = logging.getLogger('services.personality.conversation_analyzer')
logger.debug(f"Detecting preferences in: {message}")
logger.debug(f"Warm words found: {warm_words}")
logger.debug(f"Warm score: {warm_score}")
```

### Inspect Hint Objects

```python
result = analyzer.analyze_message(user_id, message, profile)

for hint in result.hints:
    print(f"Dimension: {hint.dimension.value}")
    print(f"Confidence: {hint.confidence_score}")
    print(f"Level: {hint.confidence_level().value}")
    print(f"Ready for suggestion: {hint.is_ready_for_suggestion()}")
    print(f"Ready for auto-apply: {hint.is_ready_for_auto_apply()}")
    print(f"Evidence: {hint.evidence}")
```

### Use the Health Endpoint

```bash
curl http://localhost:8001/api/v1/preferences/health
```

Shows status of all components and latencies.

---

## Performance Optimization

### Lazy Loading

```python
# ✗ Bad: Load profile for every message
async def analyze_every_message(message):
    profile = await PersonalityProfile.load_with_preferences(user_id)
    return analyzer.analyze_message(user_id, message, profile)

# ✓ Good: Load once, reuse
profile = await PersonalityProfile.load_with_preferences(user_id)
for message in messages:
    result = analyzer.analyze_message(user_id, message, profile)
```

### Word Set Optimization

```python
# ✗ Slow: Recreate sets on every call
def analyze(message):
    warm_words = {"love", "appreciate", ...}  # Recreated each time
    return word_matching(message, warm_words)

# ✓ Fast: Define as class variable
class ConversationAnalyzer:
    WARM_WORDS = {"love", "appreciate", ...}  # Defined once

    def analyze(self, message):
        return word_matching(message, self.WARM_WORDS)
```

### Batch Processing

```python
# For multiple messages at once
messages = [msg1, msg2, msg3]
profile = await load_profile_once()

results = [
    analyzer.analyze_message(user_id, msg, profile)
    for msg in messages
]
```

---

## Common Pitfalls

### ❌ Not checking for None profile

```python
# Wrong: Crashes if profile is None
value = current_profile.warmth_level  # AttributeError if None

# Right: Check first
if current_profile:
    value = current_profile.warmth_level
else:
    value = DEFAULT_VALUE
```

### ❌ Modifying shared word sets

```python
# Wrong: Affects all instances
WARM_WORDS.add("new_word")

# Right: Create copy if needed
warm_words = WARM_WORDS.copy()
warm_words.add("new_word")
```

### ❌ Not handling hint expiration

```python
# Wrong: Uses expired hints
hint = session_hints.get(hint_id)  # Might be expired

# Right: Check TTL
if hint['stored_at'] + TTL > now:
    use_hint(hint)
else:
    return error("Hint expired")
```

### ❌ Creating analyzer per request

```python
# Wrong: Creates new instance every time
async def process_intent(message):
    analyzer = ConversationAnalyzer()  # ← Inefficient
    return analyzer.analyze_message(...)

# Right: Create once, reuse
analyzer = ConversationAnalyzer()  # Create at startup

async def process_intent(message):
    return analyzer.analyze_message(...)  # Reuse
```

---

## Release Checklist

Before releasing changes:

- [ ] All unit tests passing (27/27)
- [ ] All integration tests passing (10/10)
- [ ] No new console errors or warnings
- [ ] Documentation updated
- [ ] Performance benchmarks acceptable (<100ms per detection)
- [ ] Code follows naming conventions
- [ ] Backward compatibility maintained
- [ ] Database migrations handled (if schema changes)
- [ ] Logging added for new features
- [ ] Error handling for edge cases

---

## Resources

- **Main Documentation**: `docs/features/preference-detection.md`
- **API Reference**: `docs/api/preference-detection-api.md`
- **Integration Guide**: `docs/integration/preference-detection-integration.md`
- **Issue**: #248 (CONV-LEARN-PREF)
- **Tests**: `tests/unit/` and `tests/integration/`

---

**Last Updated**: November 22, 2025
**Status**: Production Ready ✅
**Maintained By**: Claude Code
