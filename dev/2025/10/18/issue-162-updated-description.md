# CORE-STAND-MODES-API #162: Expose Multi-Modal Generation via REST API

## Scope (Updated for Alpha)

Expose existing 4 generation modes via REST API endpoints, enabling programmatic access to standup generation.

**Deferred to MVP**: Advanced UI controls and interactive web interface (see MVP-STAND-MODES-UI)

## Current Implementation Status ✅

**DISCOVERY**: Implementation is 90%+ complete!

✅ **4 generation modes implemented** in MorningStandupWorkflow (610 lines):

- `generate_with_documents()` - Document-focused standup
- `generate_with_issues()` - Issue Intelligence integration
- `generate_with_calendar()` - Calendar-aware standup
- `generate_with_trifecta()` - All integrations combined

✅ **StandupOrchestrationService** (142 lines) - DDD-compliant domain service
✅ **Multi-format support** - CLI, Slack, Web formats
✅ **Performance excellence** - 0.1ms generation time (20,000x better than 2s target)

## Work Required

- REST API endpoint design and implementation
- OpenAPI documentation
- Authentication integration (existing patterns)
- Response format standardization
- Testing and validation

## API Design Specification

```
POST /api/standup/generate
Query Parameters:
  - mode: standard|with_documents|with_issues|with_calendar|trifecta
  - format: json|slack|cli|web
  - user_id: string (from auth)

Response:
{
  "success": true,
  "standup": {
    "content": "...",
    "format": "json",
    "metadata": {...},
    "performance_metrics": {...}
  }
}
```

## Success Criteria

- [ ] REST endpoints for all 4 generation modes functional
- [ ] Query parameters for mode and format selection working
- [ ] Proper HTTP status codes and error responses
- [ ] OpenAPI documentation complete
- [ ] Integration with existing auth patterns
- [ ] Performance maintained (<2s response, current 0.1ms generation)
- [ ] All existing functionality preserved

## Dependencies

- CORE-STAND #240 (Core verification) complete
- Existing auth infrastructure

## Estimate

1.5 days (reduced from original due to mature implementation)

## Related Issues

- **Continues in**: MVP-STAND-MODES-UI for advanced UI controls
- **Depends on**: CORE-STAND #240, CORE-STAND-FOUND #119
