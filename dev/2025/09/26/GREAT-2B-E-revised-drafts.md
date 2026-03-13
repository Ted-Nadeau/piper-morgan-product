# Revised GREAT-2B through 2E Issue Drafts

Based on Phase -1 discoveries showing services are more complete than expected.

---

## CORE-GREAT-2B: Complete GitHub Spatial Migration (#193)

### Context
Investigation revealed GitHub has a sophisticated 4-week deprecation router with 75% complete spatial migration infrastructure. Not the dual pattern cleanup we expected.

### Acceptance Criteria
- [ ] Complete spatial migration using existing deprecation router
- [ ] Remove deprecated patterns after 4-week window
- [ ] Verify all GitHub calls use spatial intelligence
- [ ] Ensure OrchestrationEngine routes GitHub requests (if initialized)
- [ ] Tests passing for spatial GitHub operations

### Tasks
- [ ] Review existing deprecation router implementation
- [ ] Identify remaining 25% of non-spatial patterns
- [ ] Migrate remaining patterns to spatial
- [ ] Test GitHub operations end-to-end
- [ ] Remove deprecated code paths

### Lock Strategy
- Deprecation router prevents premature removal
- Tests verify spatial patterns work
- Old patterns physically removed after migration

### Success Validation
```bash
# No old patterns remain
grep -r "github_service" . --include="*.py" | grep -v spatial

# All GitHub operations use spatial
pytest tests/integrations/github/spatial/ -v
```

### Estimated Duration
1 day (simpler than expected due to existing infrastructure)

---

## CORE-GREAT-2C: Verify Slack & Notion Spatial Systems (#194)

### Context
Major discovery: Slack has COMPLETE spatial intelligence system (20+ files, operational since July 2025). Notion also complete. This is verification, not implementation.

### Acceptance Criteria
- [ ] Verify Slack spatial system fully operational
- [ ] Confirm all 20+ Slack spatial files work correctly
- [ ] Verify Notion spatial integration works
- [ ] Re-enable Slack webhook verification (TBD-SECURITY-02) if still disabled
- [ ] Document both systems for team knowledge

### Tasks
- [ ] Test Slack spatial operations end-to-end
- [ ] Verify workspace_navigator.py, spatial_mapper.py, attention_model.py work
- [ ] Test Notion spatial operations
- [ ] Check webhook verification status and enable if needed
- [ ] Create brief documentation of what exists

### Lock Strategy
- Tests confirm spatial systems operational
- Webhook verification enabled and tested
- Documentation prevents "rediscovery"

### Success Validation
```bash
# Slack spatial tests pass
pytest tests/integrations/slack/spatial/ -v

# Notion tests pass
pytest tests/integrations/notion/ -v

# Webhook verification enabled
grep "verify_signature" services/integrations/slack/webhook_router.py
```

### Estimated Duration
1 day (verification only, not implementation)

---

## CORE-GREAT-2D: Google Calendar Spatial Wrapper & Config Validation (#195)

### Context
Google Calendar is the ONLY service actually needing spatial wrapper creation. Also implement configuration validation.

### Acceptance Criteria
- [ ] Create spatial wrapper for Google Calendar
- [ ] Follow pattern from Slack/Notion spatial implementations
- [ ] Implement configuration validation at startup
- [ ] Add validation to CI pipeline
- [ ] Update Excellence Flywheel in agent configs

### Tasks
- [ ] Study Slack spatial pattern (20+ files as reference)
- [ ] Create Calendar spatial wrapper following pattern
- [ ] Implement config validation on startup
- [ ] Add config validation to CI
- [ ] Update agent configs with Excellence Flywheel
- [ ] Test Calendar operations with spatial intelligence

### Lock Strategy
- Config validation in CI
- Startup fails on invalid config
- Calendar spatial tests required

### Success Validation
```bash
# Calendar has spatial wrapper
ls -la services/integrations/calendar/spatial*.py

# Config validation works
python validate_config.py

# CI includes validation
grep "validate_config" .github/workflows/ci.yml
```

### Estimated Duration
1-2 days (main implementation work of GREAT-2)

---

## CORE-GREAT-2E: Documentation Fixes & Excellence Flywheel (#196)

### Context
62 broken links found but ~28 are session logs (not real documentation). Excellence Flywheel referenced 200+ times in docs but ZERO in agent configs.

### Acceptance Criteria
- [ ] Fix actual documentation broken links (exclude session logs)
- [ ] Add Excellence Flywheel methodology to ALL agent configs
- [ ] Add link checker to CI pipeline
- [ ] Update ADRs with current integration reality
- [ ] Document discovered spatial systems

### Tasks
- [ ] Identify real vs session log broken links
- [ ] Fix legitimate broken documentation links
- [ ] Add Excellence Flywheel to .claude/, .cursor/ configs
- [ ] Implement link checker in CI
- [ ] Update integration ADRs with spatial reality
- [ ] Brief documentation of Slack's 20+ file spatial system

### Optional (if time permits)
- [ ] Create integration pattern source of truth (if helpful)
- [ ] Document OrchestrationEngine initialization needs

### Lock Strategy
- Link checker runs in CI
- Excellence Flywheel embedded in configs
- ADRs reflect actual architecture

### Success Validation
```bash
# No broken documentation links
python check_links.py docs/

# Excellence Flywheel in configs
grep -r "Excellence.*Flywheel\|flywheel" .claude/ .cursor/

# Link checker in CI
grep "check_links" .github/workflows/ci.yml
```

### Estimated Duration
1 day

---

## Summary of Changes

### From Original Expectations
- **2B**: Complete migration instead of cleanup
- **2C**: Verification instead of implementation
- **2D**: Only real implementation work needed
- **2E**: Reduced scope, add Excellence Flywheel

### Total Duration
- Original estimate: 5 days
- Revised estimate: 4-5 days (but different work)
- Most work is verification and completion, not cleanup

### Key Investigation Still Needed
- [ ] OrchestrationEngine initialization status (lazy like QueryRouter?)
- [ ] Ethical boundary layer integration
- [ ] Why Slack spatial work wasn't visible/documented
