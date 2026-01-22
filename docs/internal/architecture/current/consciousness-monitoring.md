# Consciousness Monitoring Approach

**Created**: January 21, 2026
**Issue**: #407 MUX-VISION-STANDUP-EXTRACT (Phase Z)
**Purpose**: Ongoing quality assurance for consciousness patterns

---

## Monitoring Goals

1. **Prevent Regression** - Catch consciousness degradation early
2. **Measure Progress** - Track rollout across features
3. **Identify Gaps** - Find features that slipped through
4. **User Feedback** - Connect consciousness to user experience

---

## Automated Monitoring

### 1. MVC Spot Checks (CI Pipeline)

Add to test suite - sample outputs from each feature:

```python
# tests/unit/consciousness/test_mvc_spot_checks.py

@pytest.mark.smoke
def test_standup_mvc_compliance():
    """Spot check standup output for MVC elements."""
    output = generate_sample_standup()
    result = validate_mvc(output)
    assert result.checks["identity"], "Standup missing identity voice"
    # Full responses need all 4
    assert result.passes, f"Standup MVC fail: {result.missing}"

@pytest.mark.smoke
def test_loading_identity():
    """Loading messages need identity only."""
    from services.consciousness.loading_consciousness import get_conscious_loading_message
    msg = get_conscious_loading_message("workflow_execution", "starting")
    assert has_identity(msg), "Loading message missing identity"

@pytest.mark.smoke
def test_error_recovery_path():
    """Error messages need recovery invitation."""
    from services.ui_messages.user_friendly_errors import get_conversational_error_message
    msg = get_conversational_error_message(Exception("test error"))
    assert has_invitation(msg), "Error missing recovery invitation"
```

### 2. Regression Detection

Track consciousness scores over time:

```python
# services/consciousness/metrics.py

FEATURE_SCORES = {
    "todos": {"before": 2, "after": 18, "date": "2026-01-21"},
    "conversations": {"before": 9, "after": 18, "date": "2026-01-21"},
    "loading_states": {"before": 3, "after": 14, "date": "2026-01-21"},
    "error_messages": {"before": 6, "after": 16, "date": "2026-01-21"},
    # Add as features transform...
}

def get_consciousness_coverage():
    """Return % of features at Conscious level (≥13)."""
    conscious = sum(1 for f in FEATURE_SCORES.values() if f["after"] >= 13)
    return conscious / len(FEATURE_SCORES) * 100
```

### 3. Output Sampling

Periodically sample real outputs and score:

```bash
# scripts/consciousness-audit.sh
# Run weekly to spot-check real outputs

python -c "
from services.consciousness.validation import validate_mvc
# Sample recent outputs from logs/database
# Score and report any regressions
"
```

---

## Manual Monitoring

### Weekly Review (5 min)

1. Pick 1 transformed feature at random
2. Trigger 3 different outputs
3. Quick score against rubric
4. Note any concerns in `#consciousness-quality` (future Slack channel)

### Sprint Review Checkpoint

Add to sprint review:
- [ ] Any consciousness regressions reported?
- [ ] New features added without consciousness?
- [ ] User feedback mentioning Piper's "voice"?

### User Feedback Signals

Watch for these in user feedback:
- **Positive**: "Piper feels helpful", "like talking to a colleague"
- **Negative**: "robotic", "cold", "confusing responses"
- **Neutral**: No mention of interaction quality

---

## Metrics Dashboard (Future)

When we have analytics:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Features ≥13/20 | 100% | Score tracking |
| MVC Pass Rate | 95%+ | CI spot checks |
| User "colleague" feeling | 70%+ | Survey/feedback |
| Voice consistency | High | Manual review |

---

## Rollout Progress Tracker

### Wave 1: High-Frequency ✅
- [x] #622 Todos (2→18)
- [x] #625 Conversations (9→18)
- [x] #630 Loading States (3→14)
- [x] #631 Error Messages (6→16)

### Wave 2: Core Workflow
- [ ] #619 Intent Classification
- [ ] #632 Morning Standup
- [ ] #633 CLI Output

### Wave 3: Supporting
- [ ] #623 Feedback System
- [ ] #624 Calendar Integration
- [ ] #634 Search Results
- [ ] #635 Files/Projects
- [ ] #636 Learning Patterns

### Wave 4: Integration
- [ ] #620 Slack Integration
- [ ] #621 GitHub Integration
- [ ] #626 Onboarding System
- [ ] #627 Personality System
- [ ] #637 Settings/Auth
- [ ] #638 HTML Templates

### Long Tail
- [ ] #628 Edge cases

**Current Coverage**: 4/21 features (19%)
**Target**: 21/21 (100%)

---

## Escalation

If consciousness quality drops:

1. **Single feature regression** → Fix in next sprint
2. **Multiple regressions** → Stop and audit
3. **User complaints about voice** → Priority fix
4. **New feature shipped without consciousness** → Block until added

---

*Part of Consciousness Framework Documentation*
*Review monthly and update metrics*
