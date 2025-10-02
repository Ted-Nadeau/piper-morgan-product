# GREAT-3A: Foundation & Refactoring

## Context
First sub-epic of GREAT-3. Addresses all prerequisites before plugin architecture implementation.

## Scope
1. **ADR Review & Investigation**
   - Review ADR-034 (Plugin Architecture)
   - Review ADR-013 (MCP + Spatial Intelligence)
   - Map current integration touchpoints
   - Determine actual plugin needs vs current router architecture

2. **Configuration Repair**
   - Use ConfigValidator output to identify issues
   - Fix refactoring artifacts from DDD work
   - Ensure all 4 services have valid configuration
   - Test through existing features (standup, etc.)

3. **main.py Refactoring** (1,107 → <500 lines)
   - Extract initialization into modules
   - Separate orchestration logic
   - Create clean service boundaries
   - Maintain all functionality

4. **web/app.py Refactoring** (1,001 → <500 lines)
   - Extract route groups
   - Separate business logic to services
   - Prepare for plugin endpoints
   - Keep only routing coordination

## Acceptance Criteria
- [ ] ADRs reviewed and understood
- [ ] Configuration issues identified and fixed
- [ ] main.py under 500 lines
- [ ] web/app.py under 500 lines
- [ ] All existing features still work
- [ ] No functionality lost in refactoring
- [ ] Clear module boundaries established

## Success Validation
```bash
# File sizes reduced
wc -l main.py web/app.py

# Configuration working
python validate_config.py --all-services

# Features still work
python main.py  # Starts successfully
curl http://localhost:8001/health  # Returns OK

# Tests passing
pytest tests/ -v
```

## Investigation Questions
- How much of router pattern already provides plugin-like interface?
- Which integration patterns should become the plugin standard?
- What configuration is actually broken vs just warnings?

## Time Estimate
Several hurons (thoroughness over speed)