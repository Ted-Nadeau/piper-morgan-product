# Test-Driven Development Requirements - MANDATORY (Pragmatic Edition)

## Core Principle: Test Discipline with Strategic Flexibility

While TDD remains a core pillar, we recognize that different contexts require different approaches to achieve systematic excellence.

## TDD Zones - Know Your Context

### 🔴 RED ZONE - Strict TDD Required

**MUST write tests FIRST for:**
- Bug fixes (reproduce bug in test before fixing)
- Refactoring existing code
- Complex business logic
- Public API changes
- Payment/security features
- Any code that could break existing functionality

```bash
# Red Zone Process
1. Write failing test that captures requirement
2. Run test - MUST see it fail for right reason
3. Write minimal code to pass
4. Refactor if needed
5. All related tests must still pass
```

### 🟡 YELLOW ZONE - Architecture-First Allowed

**MAY develop architecture with tests for:**
- New integrations (no existing code to break)
- Infrastructure setup
- Greenfield features
- Spatial metaphor extensions
- Research spikes

```bash
# Yellow Zone Process
1. Verify no existing patterns to follow
2. Design architecture based on requirements
3. Implement WITH comprehensive tests
4. Ensure test coverage before completion
5. Document why Architecture-First was chosen
```

### 🟢 GREEN ZONE - Test-After Acceptable

**CAN write tests after implementation for:**
- Configuration files
- Simple scripts and tooling
- Documentation examples
- UI prototypes
- Proof of concepts

```bash
# Green Zone Process
1. Implement functionality
2. Add tests before merging
3. Mark as prototype if no tests
4. Upgrade to Yellow/Red zone if becoming permanent
```

## The Decision Framework

Before starting any work, ask:

1. **Could this break existing functionality?** → RED ZONE (Strict TDD)
2. **Is architecture the main unknown?** → YELLOW ZONE (Architecture-First)
3. **Is this a prototype or tool?** → GREEN ZONE (Test-After)
4. **Is this production-critical?** → RED ZONE (Strict TDD)

## Key Rules

### Always Document Your Zone Choice
```python
# PM-074: Using Architecture-First (Yellow Zone)
# Reason: New Slack integration, no existing code to break
# Comprehensive tests will be written alongside implementation
```

### Never Skip Tests Entirely
- Even Green Zone requires tests before production
- Prototypes without tests must be marked clearly
- Test debt must be tracked in GitHub issues

### Velocity Matters
When Architecture-First achieves 3-5x velocity with good test coverage, that's systematic excellence, not a methodology failure.

## Examples

### Red Zone Example - Bug Fix
```bash
# 1. Write test that reproduces bug
def test_workflow_should_complete_not_hang():
    # This currently times out
    result = await workflow.execute()
    assert result.status == "COMPLETED"  # Fails!

# 2. Fix the bug
# 3. Test now passes
```

### Yellow Zone Example - New Integration
```bash
# 1. Design spatial metaphor architecture
# 2. Implement Slack integration WITH tests
class TestSlackSpatialMapping:
    def test_channel_maps_to_room(self):
        # Written alongside implementation

# 3. Full test coverage before declaring complete
```

### Green Zone Example - Developer Tool
```bash
# 1. Create ngrok monitoring script
# 2. Add basic tests before team use
# 3. Document as "tool - basic tests only"
```

## Pragmatic TDD Checklist

- [ ] Identified which zone this work belongs in
- [ ] Documented zone choice and reasoning
- [ ] Following appropriate process for that zone
- [ ] Tests exist before marking work complete
- [ ] Test coverage appropriate for criticality

## Remember

The Excellence Flywheel spins through **systematic quality**, not dogmatic processes. When we achieve exceptional velocity WITH comprehensive tests, we codify that success rather than apologize for it.

**Default to Red Zone TDD**, but recognize when Yellow Zone Architecture-First or Green Zone rapid prototyping better serves our systematic excellence.

---

*Updated: July 27, 2025 - Added pragmatic zones based on Slack integration success*
