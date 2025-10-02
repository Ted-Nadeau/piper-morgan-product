# Gameplan: GREAT-3A - Foundation & Refactoring (REVISED)

**Date**: October 2, 2025  
**Epic**: GREAT-3A (GitHub Issue #[TBD])  
**Chief Architect**: Claude Opus 4.1  
**Revision**: Based on Phase -1 infrastructure verification findings

## Critical Update

**main.py refactoring REMOVED from scope** - File is only 141 lines (not 1,107 as documented). Already optimal size.

## Mission (Revised)

Complete foundational work for plugin architecture: fix configuration issues, refactor web/app.py, and investigate plugin needs versus current router architecture.

## Phase Structure (Revised)

### Phase 0: Investigation & ADR Review
**Both Agents - Thorough Understanding**

```bash
# Check current file sizes (VERIFIED)
wc -l main.py web/app.py
# main.py: 141 lines ✅ (no refactoring needed)
# web/app.py: 1,052 lines (needs refactoring)

# Run ConfigValidator to see issues
python validate_config.py --all-services --verbose

# Review router architecture (CORRECTED PATH)
find services/integrations/ -name "*router.py" | xargs wc -l

# Check ADRs
ls -la docs/internal/architecture/current/adrs/adr-034*
ls -la docs/internal/architecture/current/adrs/adr-013*
```

**Key Questions to Answer**:
1. What configuration is actually broken vs warnings?
2. How much does router pattern already provide plugin interface?
3. Which routes in app.py belong together?
4. Do we already have plugin-like architecture in routers?

### Phase 1: Configuration Repair
**Claude Code: Investigation**
- Run ConfigValidator and document all issues
- Trace each configuration error to root cause
- Identify which are refactoring artifacts vs missing config
- Test through working features (standup, chat, etc.)

**Cursor Agent: Remediation**
- Fix configuration issues systematically
- Update config files where needed
- Ensure all 4 services validate clean
- Document any config that needs environment setup

**Validation**:
```bash
# All services should validate
for service in github slack notion calendar; do
    python validate_config.py --service=$service
done

# Features should work
python main.py  # Should start without errors
curl http://localhost:8001/health  # Should return OK
```

### Phase 2: [REMOVED - main.py already optimal]
~~main.py refactoring removed - file is 141 lines, already well under 500 line target~~

### Phase 3: web/app.py Refactoring
**Target**: 1,052 lines → <500 lines

**Suggested Route Groups**:
```python
# web/app.py (main app only) ~200 lines
# web/routes/health.py ~50 lines
# web/routes/chat.py ~200 lines
# web/routes/standup.py ~150 lines
# web/routes/api.py ~200 lines
# web/routes/static.py ~100 lines
# web/routes/admin.py ~100 lines
```

**Process**:
1. Map all current routes
2. Group by functionality
3. Extract route groups incrementally
4. Move business logic to services
5. Keep only routing in web/

**Anti-80% Check**:
```
Route Group  | Extracted | Tested | Working
------------ | --------- | ------ | -------
health       | [ ]       | [ ]    | [ ]
chat         | [ ]       | [ ]    | [ ]
standup      | [ ]       | [ ]    | [ ]
api          | [ ]       | [ ]    | [ ]
static       | [ ]       | [ ]    | [ ]
admin        | [ ]       | [ ]    | [ ]
TOTAL: 0/18 = 0% (Must reach 100%)
```

**Validation After Each**:
```bash
# Server starts
python web/app.py

# UI loads
curl http://localhost:8081/

# API endpoints work
curl http://localhost:8081/api/health
```

### Phase 4: Plugin Architecture Mapping
**Both Agents - Investigation**

**Document Findings**:
1. How routers already provide plugin-like interface
2. What additional abstraction is needed
3. Which spatial pattern should be standard
4. What the plugin contract should include

**Review Actual Router Structure** (in services/integrations/):
- calendar/calendar_integration_router.py
- github/github_integration_router.py
- notion/notion_integration_router.py
- slack/slack_integration_router.py

**Create Comparison**:
```
Current Router Interface | Plugin Interface Needs | Gap
----------------------- | --------------------- | ---
init()                  | init()                | None
route methods           | execute()             | Abstraction needed
feature flags           | enable/disable        | Formalize
spatial access          | spatial pattern       | Standardize
```

### Phase 5: Validation & Documentation
**All Work - Final Verification**

```bash
# File sizes achieved
wc -l main.py web/app.py
# main.py: 141 lines ✅ (already optimal)
# web/app.py: <500 lines (target)

# Configuration clean
python validate_config.py --all-services

# All tests passing
pytest tests/ -v

# Server operational
python main.py &
python web/app.py &
curl http://localhost:8001/health
curl http://localhost:8081/
```

**Document**:
- Configuration fixes applied
- Route organization structure
- Plugin architecture findings
- Why main.py didn't need refactoring

---

## Time Estimate (Revised)

- Phase 0: Half a mango (investigation)
- Phase 1: One mango (config repair)
- ~~Phase 2: Two mangos (main.py refactor)~~ REMOVED
- Phase 3: Two mangos (app.py refactor)
- Phase 4: Half a mango (mapping)
- Phase 5: Half a mango (validation)

**Total: 4-5 mangos** (reduced from 6-7 mangos)

---

## Success Criteria (Revised)

### Must Achieve
- [ ] All configuration issues resolved
- [x] main.py under 500 lines (already 141 lines)
- [ ] web/app.py under 500 lines
- [ ] All functionality preserved
- [ ] Tests passing
- [ ] Clear module boundaries
- [ ] Plugin needs documented

---

## Notes

1. **Phase -1 Success**: Infrastructure verification prevented wasted effort
2. **main.py Status**: Already microservice-oriented, no refactoring needed
3. **Focus Shift**: Primary effort now on web/app.py refactoring
4. **Path Correction**: Routers in services/integrations/ not integration_routers/

---

*Gameplan revised based on infrastructure verification*  
*Ready for Phase 0 deployment*