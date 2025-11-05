# Follow-Up: Document ActionMapper Scope (EXECUTION-only)

**Priority**: P3 - Documentation
**Labels**: `documentation`, `technical-debt`
**Parent Issue**: #284
**Estimated Effort**: 1 hour

## Problem

ActionMapper's ACTION_MAPPING dictionary contains 66 mappings, but only ~14 are actually used. The other ~52 mappings are for non-EXECUTION categories (ANALYSIS, SYNTHESIS, STRATEGY, QUERY, LEARNING) which have their own routing logic and never go through ActionMapper.

**This is confusing but not a bug** - those categories work correctly via their own handlers.

## Background

IntentService routes by category BEFORE ActionMapper:
```python
# services/intent/intent_service.py:235-260
if intent.category == "QUERY":
    return await self._handle_query_intent(...)       # Own routing
if intent.category == "EXECUTION":
    return await self._handle_execution_intent(...)   # ← ActionMapper used HERE
if intent.category == "ANALYSIS":
    return await self._handle_analysis_intent(...)    # Own routing
if intent.category == "SYNTHESIS":
    return await self._handle_synthesis_intent(...)   # Own routing
```

ActionMapper is only called in `_handle_execution_intent`, so mappings for other categories are never used.

## Proposed Solution

**Option A**: Remove unused mappings (cleaner)
- Remove ~52 non-EXECUTION mappings from ACTION_MAPPING
- Keep only EXECUTION-category actions (GitHub, todos, etc.)
- Update documentation to clarify EXECUTION-only scope

**Option B**: Keep mappings, document intent (current state)
- Add docstring explaining ACTION_MAPPING includes all categories
- Document that only EXECUTION mappings are actually used
- Explain why others are included (future-proofing? comprehensive reference?)

**Option C**: Create category-aware mapper
- Add category parameter to `map_action()`
- Route different categories to different mapping dictionaries
- More complex but supports all categories

## Recommendation

**Start with Option B** (1 hour effort):
1. Update ActionMapper docstring to clarify scope
2. Add comment explaining unused mappings
3. Document in ADR or pattern file
4. Full scope Option C and create issue for prioritization by PM and chief architect

## Files to Update

- `services/intent_service/action_mapper.py` - Add docstring clarification
- Consider ADR: "Why ActionMapper is EXECUTION-only"
- Consider pattern doc: "Intent Category Routing"

## Acceptance Criteria

- [ ] ActionMapper docstring clarifies EXECUTION-only scope
- [ ] Comment explains why non-EXECUTION mappings are present
- [ ] Developers understand which mappings are used vs unused
- [ ] Decision documented (keep vs remove unused mappings)

## Evidence

**Validation**: 34 passing analysis handler tests prove non-EXECUTION categories work without ActionMapper
**Investigation**: Session log `dev/2025/11/03/2025-11-03-0615-prog-code-log.md` (lines 453-642)
Monday, November 3, 2025 At 11:23 am
