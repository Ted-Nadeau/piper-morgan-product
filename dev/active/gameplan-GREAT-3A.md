# Gameplan: GREAT-3A - Foundation & Refactoring

**Date**: October 2, 2025  
**Epic**: GREAT-3A (GitHub Issue #[TBD])  
**Chief Architect**: Claude Opus 4.1  
**Context**: First sub-epic of GREAT-3, addressing prerequisites before plugin architecture

## Mission

Complete all foundational work needed for clean plugin architecture: fix configuration issues, refactor monolithic files, and investigate actual plugin needs versus current router architecture.

## Strategic Context

### Current State
- **Router infrastructure**: Complete for all 4 integrations (GitHub, Slack, Notion, Calendar)
- **Spatial patterns**: Three documented patterns working (Granular, Embedded, Delegated MCP)
- **Monoliths**: main.py (1,107 lines), web/app.py (1,001 lines)
- **Configuration**: Refactoring artifacts detected by ConfigValidator

### What Success Enables
Clean boundaries and modular architecture will make plugin extraction natural and straightforward.

## Phase Structure

### Phase 0: Investigation & ADR Review
**Both Agents - Thorough Understanding**

```bash
# Check current file sizes
wc -l main.py web/app.py

# Run ConfigValidator to see issues
python validate_config.py --all-services --verbose

# Review router architecture
find services/integration_routers/ -name "*.py" | xargs wc -l

# Check ADRs
ls -la docs/internal/architecture/current/adrs/adr-034*
ls -la docs/internal/architecture/current/adrs/adr-013*
```

**Key Questions to Answer**:
1. What configuration is actually broken vs warnings?
2. How much does router pattern already provide plugin interface?
3. What are the natural module boundaries in main.py?
4. Which routes in app.py belong together?
5. Do we already have plugin-like architecture in routers?

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

### Phase 2: main.py Refactoring
**Target**: 1,107 lines → <500 lines

**Lead Developer Coordinates Division**

**Suggested Module Extraction**:
```python
# main.py (orchestration only) ~200 lines
# modules/initialization.py (startup, config) ~200 lines  
# modules/service_registry.py (service management) ~150 lines
# modules/api_handlers.py (route handlers) ~300 lines
# modules/middleware.py (auth, cors, etc.) ~150 lines
```

**Both Agents Collaborate**:
- Identify logical boundaries
- Extract modules incrementally
- Maintain all functionality
- Run tests after each extraction

**Anti-80% Check**:
```
Module Target    | Extracted | Tested | Working
---------------- | --------- | ------ | -------
initialization   | [ ]       | [ ]    | [ ]
service_registry | [ ]       | [ ]    | [ ]
api_handlers     | [ ]       | [ ]    | [ ]
middleware       | [ ]       | [ ]    | [ ]
TOTAL: 0/12 = 0% (Must reach 100%)
```

### Phase 3: web/app.py Refactoring
**Target**: 1,001 lines → <500 lines

**Suggested Route Groups**:
```python
# web/app.py (main app only) ~200 lines
# web/routes/health.py ~50 lines
# web/routes/chat.py ~200 lines
# web/routes/standup.py ~150 lines
# web/routes/api.py ~200 lines
# web/routes/static.py ~100 lines
```

**Process**:
1. Map all current routes
2. Group by functionality
3. Extract route groups
4. Move business logic to services
5. Keep only routing in web/

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
wc -l main.py web/app.py  # Both <500 lines

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
- Module structure and responsibilities
- Configuration fixes applied
- Route organization
- Plugin architecture findings

---

## STOP Conditions

Stop immediately if:
1. Refactoring breaks core functionality
2. Configuration fixes affect security
3. Test coverage drops below baseline
4. Circular dependencies emerge
5. Performance degrades significantly

---

## Team Coordination

### Lead Developer
- Coordinate module boundaries
- Ensure consistent refactoring approach
- Monitor functionality preservation
- Guide plugin architecture mapping

### Claude Code
- Deep investigation and analysis
- Module extraction strategy
- Configuration root cause analysis
- Architecture pattern documentation

### Cursor Agent
- Systematic refactoring execution
- Route group extraction
- Configuration remediation
- Cross-validation of extractions

---

## Time Estimate

- Phase 0: Half a mango (investigation)
- Phase 1: One mango (config repair)
- Phase 2: Two mangos (main.py refactor)
- Phase 3: Two mangos (app.py refactor)
- Phase 4: Half a mango (mapping)
- Phase 5: Half a mango (validation)

Total: Six to seven mangos (thoroughness over speed)

---

## Success Criteria

### Must Achieve
- [ ] All configuration issues resolved
- [ ] main.py under 500 lines
- [ ] web/app.py under 500 lines
- [ ] All functionality preserved
- [ ] Tests passing
- [ ] Clear module boundaries
- [ ] Plugin needs documented

### Nice to Have
- [ ] Performance improved
- [ ] Test coverage increased
- [ ] Additional tech debt addressed

---

## Notes

1. **Time Lord Approach**: Each phase takes what it takes
2. **Inchworm Discipline**: Complete each extraction before next
3. **Anti-80% Vigilance**: 100% functionality preserved
4. **Foundation First**: This work enables everything in 3B-3D

---

*Gameplan prepared by Chief Architect*  
*Ready for new Lead Developer with Sonnet 4.5*