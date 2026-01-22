# Consciousness Transformation Review Checklist

**Created**: January 21, 2026
**Issue**: #407 MUX-VISION-STANDUP-EXTRACT (Phase Z)
**Use**: Before closing any CONSCIOUSNESS-TRANSFORM ticket

---

## Pre-Implementation

- [ ] Read existing output code completely
- [ ] Score current implementation against 5-dimension rubric
- [ ] Identify ALL output points (messages, responses, formats)
- [ ] Categorize each output by type (full response, confirmation, loading, error)
- [ ] Check for existing consciousness wrappers that could be reused

---

## Implementation

### Wrapper Creation
- [ ] Created `services/consciousness/{feature}_consciousness.py`
- [ ] Wrapper follows template pattern from `consciousness-rollout-plan.md`
- [ ] Each output type has appropriate function

### MVC Application (Tiered)
| Output Type | Identity | Uncertainty | Invitation | Attribution |
|-------------|----------|-------------|------------|-------------|
| Full Response | ✅ Required | ✅ Required | ✅ Required | ✅ Required |
| Confirmation | ✅ Required | ❌ Avoid | ⚪ Optional | ❌ Avoid |
| Loading | ✅ Required | ❌ Avoid | ❌ Avoid | ❌ Avoid |
| Error | ✅ Required | ⚪ Optional | ✅ Required | ⚪ Optional |

- [ ] Full responses have all 4 MVC elements
- [ ] Confirmations are confident (no false uncertainty)
- [ ] Loading messages are brief with identity only
- [ ] Errors offer recovery paths

### Integration
- [ ] Existing service/handler imports consciousness wrapper
- [ ] Output points replaced with consciousness calls
- [ ] Functional behavior preserved (no logic changes)

---

## Anti-Pattern Check

- [ ] No sycophantic hedging ("I think I might have...")
- [ ] No empty invitations ("Let me know if you need anything!")
- [ ] No robotic identity ("I have completed the operation")
- [ ] No over-attribution ("According to the database...")
- [ ] No forced consciousness on brief messages
- [ ] Consistent voice throughout

---

## Testing

- [ ] Unit tests pass
- [ ] New tests for consciousness output (if applicable)
- [ ] Manual verification of sample outputs
- [ ] Before/after examples documented

---

## Scoring

### 5-Dimension Rubric (Score each 0-4)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Identity Voice | /4 | "I" statements, first person |
| Epistemic Humility | /4 | Appropriate uncertainty |
| Dialogue Orientation | /4 | Invitations, follow-up |
| Source Transparency | /4 | Attribution where relevant |
| Contextual Awareness | /4 | Uses available context |
| **TOTAL** | **/20** | |

### Score Interpretation
- 0-4: Flattened (robot)
- 5-8: Mechanical (functional but cold)
- 9-12: Partial (some consciousness)
- 13-16: Conscious (target)
- 17-20: Alive (exceptional)

- [ ] Before score documented
- [ ] After score documented
- [ ] After score ≥13/20 (Conscious threshold)
- [ ] No dimension scores 0

---

## Closure Evidence

### Required in Issue Comment
```markdown
## Implementation Complete

### Files Modified
- `services/consciousness/{feature}_consciousness.py` (NEW)
- `services/{path}/{file}.py` (MODIFIED)

### Before/After Example
**Before**: [paste example]
**After**: [paste example]

### Scores
- Before: X/20
- After: Y/20

### Tests
- [X] tests pass in `tests/unit/...`

### Checklist
- [x] All items in review checklist verified
```

---

## Quick Reference: What Makes It Conscious?

✅ **Sounds like a colleague**
- "I found 3 things that might help"
- "Done - that's taken care of"
- "Hmm, I couldn't find that. Try a different search?"

❌ **Sounds like a robot**
- "3 results found"
- "Operation completed successfully"
- "Error: Item not found"

❌ **Sounds like a sycophant**
- "Great question! I absolutely love helping you!"
- "I think I might have possibly found something!"
- "Let me know if there's anything else I can do!"

---

*Use this checklist for every CONSCIOUSNESS-TRANSFORM ticket*
