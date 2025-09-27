# CORE-GREAT-2 Decomposition into Manageable Issues (Updated)

## Recommended: 5 Issues for Integration Cleanup

Based on GREAT-1 lessons and accounting for all integrations including Google Calendar:

---

## CORE-GREAT-2A: ADR Review & Pattern Discovery
**Duration**: ~1 day
**Type**: Investigation & Documentation

### Scope
- Review ADR-005, 006, 027, 030 for current compliance
- Run pattern detection commands for ALL services (GitHub, Slack, Notion, Google Calendar)
- Document all dual implementations found
- Identify spatial intelligence wrapper patterns
- Note plugin architecture considerations
- Create inventory of what needs cleanup

### Acceptance Criteria
- [ ] All 4 ADRs reviewed with compliance notes (PM will validate)
- [ ] Dual pattern inventory for all 4 services (PM will validate)
- [ ] Service call patterns mapped (old vs new) (PM will validate)
- [ ] Spatial intelligence integration points documented (PM will validate)
- [ ] Broken documentation links identified (all 28+) (PM will validate)
- [ ] Excellence Flywheel gaps documented (PM will validate)
- [ ] Related TODOs documented (TBD-API-01, TBD-LLM-01, TBD-SECURITY-02) (PM will validate)

### Investigation Commands
```bash
# Find all service patterns
grep -r "GitHubService\|GithubService\|github_service" . --include="*.py"
grep -r "SlackService\|slack_service" . --include="*.py"
grep -r "NotionService\|notion_service" . --include="*.py"
grep -r "CalendarService\|GoogleCalendar\|calendar_service" . --include="*.py"

# Check spatial intelligence usage
grep -r "spatial\|dimension" services/integrations/ --include="*.py"
```

### Why Separate
Pure investigation work - no code changes. Sets foundation for cleanup. Must understand spatial intelligence wrapping before changing services.

---

## CORE-GREAT-2B: GitHub Service Unification
**Duration**: ~1 day
**Type**: Code Cleanup

### Scope
- Remove old GitHub service patterns
- Ensure all GitHub calls go through OrchestrationEngine
- Maintain spatial intelligence wrapper compatibility
- Update imports and references
- Address TBD-LLM-01 (GitHub issue generator LLM integration)
- Test GitHub functionality end-to-end

### Acceptance Criteria
- [ ] Old GitHub patterns removed (PM will validate)
- [ ] All GitHub calls use single pattern through OrchestrationEngine (PM will validate)
- [ ] Spatial intelligence wrapper still functional (PM will validate)
- [ ] TBD-LLM-01 resolved or documented for future (PM will validate)
- [ ] GitHub tests passing (PM will validate)
- [ ] No broken GitHub functionality (PM will validate)

### Lock Strategy
- Dual pattern detection test for GitHub
- All old import paths removed
- Integration tests verify single flow
- Spatial wrapper tests remain passing

---

## CORE-GREAT-2C: Slack & Notion Service Unification
**Duration**: ~1 day
**Type**: Code Cleanup

### Scope
- Remove old Slack service patterns
- Remove old Notion service patterns
- Address TBD-SECURITY-02 (Re-enable Slack webhook verification - HIGH PRIORITY)
- Ensure all calls go through OrchestrationEngine
- Maintain spatial intelligence wrapper compatibility
- Update imports and references

### Acceptance Criteria
- [ ] Old Slack patterns removed (PM will validate)
- [ ] Old Notion patterns removed (PM will validate)
- [ ] TBD-SECURITY-02 resolved (webhook verification enabled) (PM will validate)
- [ ] All service calls use single pattern (PM will validate)
- [ ] Spatial intelligence wrappers functional (PM will validate)
- [ ] Integration tests passing (PM will validate)

### Lock Strategy
- Dual pattern detection tests
- Old import paths removed
- Security verification enabled and tested
- Integration tests for both services

### Security Note
TBD-SECURITY-02 is HIGH priority - webhook verification must be re-enabled before production.

---

## CORE-GREAT-2D: Google Calendar & Configuration Validation
**Duration**: ~1 day
**Type**: Code Cleanup & Infrastructure

### Scope
- Remove old Google Calendar service patterns (if any exist)
- Unify Calendar calls through OrchestrationEngine
- Implement configuration validation at startup
- Add validation to CI pipeline
- Update Excellence Flywheel in agent configs
- Address TBD-API-01 if related to configuration

### Acceptance Criteria
- [ ] Google Calendar using single pattern (PM will validate)
- [ ] Config validation runs on startup (PM will validate)
- [ ] Invalid config prevents startup (PM will validate)
- [ ] CI includes config validation (PM will validate)
- [ ] Excellence Flywheel in all agent configs (PM will validate)
- [ ] All 4 services configuration validated (PM will validate)

### Lock Strategy
- Config validation in CI
- Startup fails on invalid config
- Excellence methodology embedded
- Calendar service tests passing

---

## CORE-GREAT-2E: Documentation Cleanup & Final Verification
**Duration**: ~1 day
**Type**: Documentation & Testing

### Scope
- Fix all 28+ broken documentation links
- Update affected ADRs with cleanup results
- Add link checker to CI
- Final pattern verification for all 4 services
- Document spatial intelligence integration patterns
- Note plugin architecture readiness
- Update pattern catalog

### Acceptance Criteria
- [ ] Zero broken documentation links (PM will validate)
- [ ] Link checker in CI pipeline (PM will validate)
- [ ] ADRs updated with current reality (PM will validate)
- [ ] Spatial intelligence patterns documented (PM will validate)
- [ ] Plugin architecture considerations noted (PM will validate)
- [ ] Pattern catalog updated (PM will validate)
- [ ] All success validation commands pass (PM will validate)

### Success Validation
```bash
# All services should use single pattern
grep -r "github_service\|slack_service\|notion_service\|calendar_service" . --include="*.py" | grep -v "orchestration"

# Config validation should work
python validate_config.py

# No broken links
python check_links.py

# No dual patterns
python detect_dual_patterns.py
```

### Lock Strategy
- Link checker runs in CI
- Documentation tests prevent future breaks
- ADRs reflect clean state
- Pattern detection for all 4 services

---

## Architectural Considerations

### Spatial Intelligence System
- Wraps raw service endpoints with dimensional context
- Must maintain compatibility during cleanup
- Document how it interacts with unified patterns

### Plugin Architecture (Future)
- Keep in mind for GREAT-3
- Don't create patterns that will conflict
- Note any preparation needed

### Security Priority
- TBD-SECURITY-02 (Slack webhook) is HIGH priority
- Must be addressed in 2C

---

## Why This Decomposition Works

### Service Distribution
- GitHub alone (2B) - Usually most complex
- Slack + Notion (2C) - Similar patterns, includes security fix
- Google Calendar + Config (2D) - Calendar simpler, pairs well with config
- Documentation (2E) - Final cleanup and verification

### Progressive Completion
- Know what we're dealing with (2A)
- Clean primary service (2B)
- Clean secondary services (2C)
- Clean tertiary service + infrastructure (2D)
- Document and lock everything (2E)

### Risk Mitigation
- Security issue (TBD-SECURITY-02) addressed mid-epic
- Spatial intelligence compatibility verified throughout
- Plugin architecture considerations documented

---

## Success Metrics
Each issue ~6-8 hours of focused work:
- Investigation
- Implementation
- Testing
- Lock creation
- Documentation
- Evidence collection

This matches our GREAT-1C daily progress sweet spot.
