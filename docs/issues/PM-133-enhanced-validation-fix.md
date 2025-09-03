# PM-133: Fix NotionMCPAdapter.get_current_user() for Enhanced Configuration Validation

**Labels**: enhancement, technical-debt, notion
**Parent**: PM-132
**Priority**: Medium
**Milestone**: Technical-Debt-Sprint
**Status**: Open

## Problem

Enhanced validation level in Notion configuration loader fails due to missing API method in NotionMCPAdapter.

## Context

From PM-132 implementation, enhanced validation attempts to test API connectivity by calling:

```python
user_info = await adapter.get_current_user()
```

However, the `get_current_user()` method does not exist in the current NotionMCPAdapter implementation, causing an AttributeError and preventing enhanced/full validation from working.

## Impact

- Enhanced validation level non-functional
- Full validation level non-functional
- Users cannot test API connectivity through configuration validation
- Feature completeness compromised

## Technical Details

- **Error**: `'NotionMCPAdapter' object has no attribute 'get_current_user'`
- **Location**: `config/notion_user_config.py` in `validate_async()` method
- **Current Status**: Basic validation works, enhanced/full validation broken
- **Dependency**: Requires NotionMCPAdapter interface enhancement

## Acceptance Criteria

- [ ] Add `get_current_user()` method to NotionMCPAdapter interface
- [ ] Enhanced validation level successfully tests API connectivity
- [ ] Full validation level successfully tests API connectivity and permissions
- [ ] All validation tiers (basic/enhanced/full) functional
- [ ] Integration tests verify enhanced validation working
- [ ] No regression in existing adapter functionality

## Implementation Requirements

1. **Method Signature**: `async def get_current_user(self) -> Optional[Dict[str, Any]]`
2. **Return Value**: User information dictionary or None if not authenticated
3. **Error Handling**: Graceful handling of API failures
4. **Testing**: Unit tests for new method
5. **Integration**: Enhanced validation tests passing

## Definition of Done

- [ ] `get_current_user()` method implemented with proper async/await pattern
- [ ] Enhanced validation tests pass consistently
- [ ] Full validation tests pass consistently
- [ ] No regression in existing adapter functionality
- [ ] Documentation updated
- [ ] Integration tests verify complete validation workflow

## Effort Estimate

- **Development**: 2-3 hours
- **Testing**: 1-2 hours
- **Documentation**: 0.5 hours
- **Total**: 3.5-5.5 hours

## Dependencies

- PM-132 (parent issue) - Configuration loader implementation
- NotionMCPAdapter interface enhancement
- Enhanced validation test suite

## Related Issues

- PM-132: Implement Notion configuration loader (parent)
- PM-134: Comprehensive integration testing (sibling)
- PM-135: Performance benchmarking framework (sibling)

## Notes

- This is a blocking issue for enhanced/full validation functionality
- Basic validation remains functional as workaround
- Priority medium due to feature completeness impact
