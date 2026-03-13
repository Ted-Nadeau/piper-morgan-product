# Gameplan: GREAT-2D - Calendar Spatial & Configuration Validation

**Date**: September 30, 2025
**Epic**: GREAT-2D (GitHub Issue #195)
**Chief Architect**: Claude Opus 4.1
**Context**: Calendar is potentially the only integration WITHOUT an existing spatial system. Plus need configuration validation for all services.

## Mission

Complete Calendar integration by creating spatial wrapper (if needed), then implement comprehensive configuration validation for all four services to prevent runtime failures from misconfiguration.

## Strategic Context

### What We Know
- **Calendar Router**: 100% complete (CORE-QUERY-1)
- **Calendar Integration**: 85% complete (discovered during CORE-QUERY-1)
- **Spatial Systems**: Slack has one (11 files), Notion has one (1 file)
- **Calendar Spatial**: Unknown - may not exist at all
- **Config Issues**: No startup validation currently

### What GREAT-2D Was Originally
The ONLY actual implementation work in GREAT-2 - create Calendar spatial wrapper

### Investigation Questions
1. Does Calendar have a hidden spatial system?
2. What is the missing 15% of Calendar integration?
3. Is TBD-API-01 configuration-related?
4. What configuration needs validating for each service?

## Success Criteria

```bash
# 1. Calendar spatial exists (or documented as not needed)
ls -la services/integrations/calendar/spatial*.py
# OR documentation explaining why spatial not applicable

# 2. Configuration validation at startup
python main.py
# Should validate all configs before starting services

# 3. Invalid config prevents startup
echo "invalid_config" > config/PIPER.user.md
python main.py
# Should exit with clear error message

# 4. CI includes validation
grep "validate.*config" .github/workflows/*.yml
# Should show config validation step

# 5. All 4 services validated
python validate_config.py --service=github
python validate_config.py --service=slack
python validate_config.py --service=notion
python validate_config.py --service=calendar
# All should report validation results
```

---

## Phase Structure

### Phase 0: GitHub & Investigation
**Lead Developer + Both Agents**
```bash
# Verify issue assignment
gh issue view 195

# Check Calendar current state
ls -la services/integrations/calendar/
find services/integrations/calendar/ -name "*.py" | xargs wc -l

# Look for spatial patterns
find services/integrations/calendar/ -name "*spatial*"
grep -r "spatial" services/integrations/calendar/

# Check the 85% complete claim
grep -r "TODO\|FIXME\|NotImplemented" services/integrations/calendar/

# Find TBD-API-01
grep -r "TBD-API-01" services/
```

### Phase 1: Calendar Spatial Decision
**Claude Code: Deep Investigation**

**First determine**: Does Calendar need spatial?
```python
# Check Calendar operations
# - Are they time-based? (temporal dimension)
# - Are they priority-based? (priority dimension)
# - Do they need coordination? (collaborative dimension)
```

**IF spatial patterns found**:
- Document what exists
- Verify functionality
- Complete any gaps

**IF NO spatial patterns found**:
- Study Slack granular pattern (11 files)
- Study Notion embedded pattern (1 file)
- Decide which pattern fits Calendar best
- Create Calendar spatial wrapper

**Decision Framework**:
```
Calendar Characteristics | Best Pattern
----------------------- | ------------
Simple, time-focused    | Embedded (like Notion)
Complex, multi-faceted  | Granular (like Slack)
Not applicable          | Document why, skip spatial
```

### Phase 2: Calendar Spatial Implementation
**Both Agents Collaborate**

**IF Creating New Spatial** (likely scenario):

**Claude Code**: Create spatial structure
```python
# Option A: Embedded Pattern (recommended for Calendar)
class CalendarSpatialIntelligence:
    """Single-file spatial intelligence for Calendar"""
    def analyze_temporal(self, events): ...
    def analyze_priority(self, events): ...
    def analyze_collaborative(self, attendees): ...
    # 5-8 dimensional analysis methods
```

**Cursor Agent**: Integration and testing
```python
# Connect spatial to router
class CalendarIntegrationRouter:
    def __init__(self):
        self.spatial = CalendarSpatialIntelligence()

    def get_spatial_events(self):
        return self.spatial.analyze_temporal(...)
```

**Anti-80% Check**:
```
Dimensions Needed | Implemented | Status
----------------- | ----------- | ------
TEMPORAL          | ✓          | Complete
PRIORITY          | ✓          | Complete
COLLABORATIVE     | ✓          | Complete
TOTAL: 3/3 = 100% (or document why fewer needed)
```

### Phase 3: Configuration Validation System
**Lead Developer Coordinates**

**Claude Code**: Create validation framework
```python
# services/config_validator.py
class ConfigValidator:
    """Validates all service configurations"""

    def validate_github(self, config):
        # Check: API token format, org/repo existence

    def validate_slack(self, config):
        # Check: Workspace ID, bot token, signing secret

    def validate_notion(self, config):
        # Check: API key, database IDs

    def validate_calendar(self, config):
        # Check: Credentials, calendar IDs

    def validate_all(self):
        # Run all validators, collect results
```

**Cursor Agent**: Startup integration
```python
# main.py modifications
def startup():
    # FIRST: Validate configuration
    validator = ConfigValidator()
    validation_results = validator.validate_all()

    if not validation_results.is_valid:
        logger.error(f"Configuration invalid: {validation_results.errors}")
        sys.exit(1)

    # THEN: Start services
    start_services()
```

**Validation Checklist**:
```
Service   | Config Items           | Validated
--------- | --------------------- | ---------
GitHub    | token, org, repo      | [ ]
Slack     | workspace, token, key | [ ]
Notion    | api_key, database_ids | [ ]
Calendar  | credentials, cal_ids  | [ ]
TOTAL: Must be 4/4 services
```

### Phase 4: CI/CD Integration
**Both Agents**

**Add to `.github/workflows/ci.yml`**:
```yaml
- name: Validate Configuration
  run: |
    # Create test config
    cp config/PIPER.example.md config/PIPER.test.md

    # Run validation
    python validate_config.py --config=config/PIPER.test.md

    # Test invalid config handling
    echo "invalid" > config/PIPER.invalid.md
    python validate_config.py --config=config/PIPER.invalid.md && exit 1 || echo "Correctly rejected invalid config"
```

### Phase 5: Lock & Validate
**All Participants**

```bash
# Test startup with valid config
python main.py
# Should start normally

# Test startup with invalid config
mv config/PIPER.user.md config/PIPER.user.md.backup
echo "invalid config" > config/PIPER.user.md
python main.py
# Should exit with error

# Restore valid config
mv config/PIPER.user.md.backup config/PIPER.user.md

# Run all service tests
pytest tests/integrations/ -v

# Verify CI includes validation
cat .github/workflows/ci.yml | grep -A5 "Validate Configuration"
```

---

## Anti-80% Safeguards

### For Calendar Spatial
**IF creating spatial, MUST enumerate dimensions**:
```
Required Dimensions | Why Needed        | Implemented
------------------ | ----------------- | -----------
TEMPORAL           | Event scheduling  | [ ]
PRIORITY           | Importance levels | [ ]
COLLABORATIVE      | Multi-attendee    | [ ]
TOTAL: X/X = Must reach 100% or document why not needed
```

### For Configuration Validation
**MUST validate ALL services**:
```
Service  | Validator Method | Startup Check | CI Check
-------- | --------------- | ------------- | --------
GitHub   | ✓              | ✓            | ✓
Slack    | ✓              | ✓            | ✓
Notion   | ✓              | ✓            | ✓
Calendar | ✓              | ✓            | ✓
TOTAL: 16/16 checkmarks required
```

---

## STOP Conditions

Stop immediately if:
1. Calendar has complex existing spatial system (needs careful study)
2. Configuration touches authentication/secrets (security review needed)
3. TBD-API-01 blocks progress
4. CI changes affect deployment pipeline
5. Startup changes break existing functionality
6. Missing 15% of Calendar is structural (not just methods)

---

## Team Coordination

### Lead Developer
- Determine Calendar spatial approach
- Coordinate config validation design
- Ensure all 4 services covered
- Monitor anti-80% compliance

### Claude Code
- Investigate Calendar spatial needs
- Create spatial wrapper if needed
- Design validation framework
- Document patterns

### Cursor Agent
- Implement spatial integration
- Add startup validation
- Update CI pipeline
- Cross-validate completeness

### PM Validation Points
- Phase 1: Calendar spatial decision documented
- Phase 2: Calendar spatial implemented (if needed)
- Phase 3: Config validation working
- Phase 4: CI integration complete
- Phase 5: All tests passing

---

## Risk Mitigation

### High Risk: No Calendar Spatial Precedent
- **Impact**: Might create wrong abstraction
- **Mitigation**: Study both patterns, choose simpler
- **Validation**: Start with embedded pattern (1 file)

### Medium Risk: Config Validation Breaking Changes
- **Impact**: Startup failures in development
- **Mitigation**: Add --skip-validation flag for development
- **Validation**: Test thoroughly before merging

### Low Risk: TBD-API-01 Scope Creep
- **Impact**: Could expand epic scope
- **Mitigation**: Only address if config-related
- **Validation**: Document for separate issue if not

---

## Effort Scope

This work involves:
- Phase 0-1: Several mangos (investigation)
- Phase 2: Half a huron (spatial implementation IF needed)
- Phase 3: Half a huron (validation system)
- Phase 4-5: Several mangos (integration and testing)

Total effort: Perhaps one huron, quality over speed as always.

**Remember**: We are Time Lords. The work takes what it takes.

---

## Notes

1. **Calendar May Not Need Spatial**: Document decision either way
2. **Config Validation Critical**: Prevents runtime surprises
3. **All 4 Services**: GitHub, Slack, Notion, Calendar - no partial
4. **Excellence Flywheel**: Consider moving to GREAT-2E
5. **Anti-80% Discipline**: 100% coverage or documented why not

---

## Appendix: Context Clarifications

- **TBD-API-01**: Found in `todo_management.py:195` - TODO creation issue
- **85% Complete**: Calendar integration missing ~15% functionality
- **Original Vision**: Calendar as "ONLY service needing spatial wrapper"
- **Current Reality**: Calendar router complete, spatial unknown
- **Config Scope**: All 4 integration services need validation

---

*Gameplan prepared by Chief Architect*
*Ready for Lead Developer deployment*
