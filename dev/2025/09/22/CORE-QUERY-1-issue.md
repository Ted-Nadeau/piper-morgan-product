# CORE-QUERY-1: Query Processing Investigation & Fix

## Context
During CORE-GREAT-1B validation, we discovered application-layer QUERY processing issues. While the orchestration infrastructure works correctly (QueryRouter is enabled and integrated), the actual query processing has failures at the application layer.

## Discovered Symptoms
- Web interface returns "INTENT_CLASSIFICATION_FAILED" for search queries
- Some responses contain invalid JSON formatting
- Server shows API key warnings during startup
- Query intent gets to QueryRouter but processing fails

## Architectural Context
**This is NOT an infrastructure issue**. The pipeline works:
1. Intent classifier receives query ✅
2. OrchestrationEngine routes to QueryRouter ✅  
3. QueryRouter receives the query ✅
4. Query processing fails ❌ (application layer)

## Acceptance Criteria

### Investigation Phase
- [ ] Identify why intent classification fails for queries
- [ ] Determine source of invalid JSON formatting
- [ ] Investigate API key configuration issues
- [ ] Check if query handlers are properly implemented
- [ ] Review any disabled query processing code (75% pattern check)

### Fix Phase
- [ ] Fix intent classification for query types
- [ ] Correct JSON formatting issues
- [ ] Resolve API key configuration
- [ ] Ensure query handlers execute properly
- [ ] Validate end-to-end query processing

### Validation Phase
- [ ] "Search for X" queries work through chat
- [ ] Responses are properly formatted JSON
- [ ] No API warnings at startup
- [ ] Query results return meaningful data
- [ ] Performance meets targets

## Evidence Required
- Terminal output showing query classification working
- Valid JSON responses from query endpoints
- Clean server startup (no API warnings)
- End-to-end query test results
- Before/after comparison of query processing

## Technical Notes
From GREAT-1B investigation:
- QueryRouter itself initializes correctly
- The handle_query_intent bridge method works
- Failure appears to be in actual query execution
- May involve search service configuration

## STOP Conditions
- If fixing requires major architectural changes
- If external API dependencies are missing
- If query system was never fully implemented
- If performance cannot meet requirements

## Definition of Done
- Query processing works end-to-end
- Intent classification succeeds for queries
- JSON responses are valid
- No API configuration warnings
- Tests demonstrate working queries
- Documentation updated

## Related
- Discovered during: CORE-GREAT-1B (#186)
- Blocks: Full end-to-end testing of chat features
- May relate to: Search service implementation