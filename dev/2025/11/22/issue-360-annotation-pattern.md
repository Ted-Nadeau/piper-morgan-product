# ARCH-ANNOTATION: Implement Ted's Annotation Pattern for Decision Tracking (#360)

**Priority**: P2 (Innovation opportunity, differentiator)
**Suggested by**: Ted Nadeau (architectural review)
**Effort**: 8-10 hours (initial implementation)

## Problem

Current system tracks WHAT changed but not WHY. No mechanism to capture human reasoning behind data changes, missing critical context for AI learning.

**Current state**:
- Audit logs show: "User X changed priority from P2 to P0 at timestamp Y"
- Missing context: "WHY did they change priority? What factors influenced decision?"

**Lost learning opportunities**:
- Why did PM reject certain suggestions?
- What context made a bug critical vs minor?
- Why was a feature deferred?
- What trade-offs were considered?

## Innovation Opportunity

Ted's annotation pattern could differentiate Piper from competitors:
- AI learns from human decision-making patterns
- Captures institutional knowledge
- Enables "decision replay" for onboarding
- Creates training data for better AI suggestions

## Solution

Implement annotation system to capture decision rationale:

```python
# Domain model for annotations
class Annotation(Base):
    """Captures the WHY behind data changes"""
    __tablename__ = 'annotations'

    id = Column(String, primary_key=True)
    entity_type = Column(String, nullable=False)  # 'issue', 'task', 'priority'
    entity_id = Column(String, nullable=False)
    field_name = Column(String)  # What changed
    old_value = Column(JSON)
    new_value = Column(JSON)

    # The innovation: WHY it changed
    reason = Column(Text)  # Human-provided reason
    factors = Column(JSON)  # Structured factors considered
    alternatives = Column(JSON)  # Other options considered
    confidence = Column(Float)  # How certain was decision

    # Learning metadata
    pattern_extracted = Column(Boolean, default=False)
    pattern_id = Column(String, ForeignKey('patterns.id'))

    # Audit
    created_by = Column(String, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
```

## Acceptance Criteria

### Core Implementation
- [ ] Create Annotation model and migration
- [ ] Create AnnotationRepository with CRUD
- [ ] Create AnnotationService with business logic
- [ ] Add annotation triggers to critical workflows
- [ ] Create API endpoints for annotations

### Integration Points
- [ ] Issue priority changes require annotation
- [ ] Task deferrals capture reasoning
- [ ] Feature cuts document trade-offs
- [ ] Bug severity changes explain context

### UI/UX (Minimal for MVP)
- [ ] Optional "Why?" field on changes
- [ ] Quick reasons dropdown (common patterns)
- [ ] Skip option with "No reason provided"
- [ ] Annotation history view

### Learning Pipeline
- [ ] Extract patterns from annotations
- [ ] Identify decision factors
- [ ] Build suggestion model
- [ ] Confidence scoring

## Example Usage

```python
# When changing priority
async def change_issue_priority(
    issue_id: str,
    new_priority: Priority,
    annotation: Optional[AnnotationRequest] = None
):
    old_issue = await repo.get(issue_id)

    # Update issue
    old_issue.priority = new_priority
    await repo.save(old_issue)

    # Capture reasoning if provided
    if annotation:
        await annotation_service.create(
            entity_type="issue",
            entity_id=issue_id,
            field_name="priority",
            old_value=old_issue.priority,
            new_value=new_priority,
            reason=annotation.reason,
            factors=annotation.factors
        )

    # AI learns from pattern
    if annotation and annotation.reason:
        await pattern_service.extract_from_annotation(annotation)
```

## Learning Examples

**Captured annotation**:
```json
{
  "entity_type": "issue",
  "entity_id": "PM-357",
  "field_name": "priority",
  "old_value": "P2",
  "new_value": "P0",
  "reason": "Security audit next week, RBAC must be done",
  "factors": ["security_audit", "external_deadline", "compliance"],
  "alternatives": ["defer_audit", "partial_implementation"],
  "confidence": 0.95
}
```

**Learned pattern**:
- When factors include "security_audit" → Increase priority
- When "external_deadline" present → P0 or P1 only
- When "compliance" mentioned → Cannot defer

## Phased Rollout

### Phase 1 (MVP - 8-10 hours)
- Basic annotation model
- API endpoints
- Critical workflow integration (priority changes)

### Phase 2 (Post-MVP)
- Pattern extraction
- Suggestion engine
- Confidence scoring

### Phase 3 (Future)
- Decision replay UI
- Onboarding from annotations
- Team pattern analysis

## Success Metrics

- Annotation capture rate >50% for critical changes
- Pattern extraction accuracy >80%
- AI suggestion relevance improves 30%
- User feedback: "AI understands our decision process"

## Competitive Advantage

**Without this**: AI remains reactive, suggesting based on data patterns only

**With this**: AI becomes proactive, understanding human reasoning and trade-offs

**Market differentiator**: "The only PM tool that learns WHY you make decisions"

---

*Note: This is Ted Nadeau's most innovative suggestion - could fundamentally change how AI assistants learn from humans*
