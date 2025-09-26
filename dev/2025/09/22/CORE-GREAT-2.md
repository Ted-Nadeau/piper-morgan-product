# CORE-GREAT-2: Integration Cleanup Epic

## Title
CORE-GREAT-2: Integration Cleanup - Single Flow & Configuration

## Labels
epic, refactor, cleanup, great-refactor

## Description

## Overview
Clean up dual patterns and establish single flow through OrchestrationEngine. Fix configuration validation and documentation.

## Background
- Multiple integration patterns coexist (old and new)
- Configuration validation is broken
- 28 documentation links are broken
- Excellence Flywheel methodology not consistently applied
- Dual implementation patterns create confusion

## Pre-Work: ADR Review
- [ ] Review ADR-005 (Eliminate Dual Repository Implementations) for completion
- [ ] Review ADR-006 (Standardize Async Session Management) for accuracy
- [ ] Review ADR-027 (Configuration Architecture) for validation requirements
- [ ] Review ADR-030 (Configuration Service Centralization) for implementation
- [ ] Run verification commands to find dual patterns
- [ ] Document any remaining dual implementations
- [ ] Update ADRs if cleanup reveals different reality
- [ ] Create new REFACTOR epics if additional cleanup needed

## Acceptance Criteria
- [ ] Only one way to call GitHub service
- [ ] Only one way to call Slack service
- [ ] Only one way to call Notion service
- [ ] Configuration validated automatically on startup
- [ ] Zero broken documentation links (currently 28)
- [ ] Excellence Flywheel methodology in all agent configs
- [ ] No dual implementation patterns remain

## Tasks
- [ ] Complete ADR pre-work review
- [ ] Find and document all dual implementation patterns
- [ ] Remove old GitHub service patterns
- [ ] Remove old Slack service patterns
- [ ] Remove old Notion service patterns
- [ ] Ensure all service calls go through OrchestrationEngine
- [ ] Implement configuration validation at startup
- [ ] Fix all 28 broken documentation links
- [ ] Update Excellence Flywheel documentation
- [ ] Update agent configuration files with methodology
- [ ] Remove deprecated import paths
- [ ] Add configuration validation to CI
- [ ] Add link checker to CI
- [ ] Update affected ADRs with cleanup results

## Lock Strategy
- Old import paths physically removed from codebase
- Config validation runs in CI pipeline
- Link checker runs in CI pipeline
- Methodology embedded in agent configs
- Dual pattern detection test added
- All related ADRs updated to reflect clean state

## Dependencies
- CORE-GREAT-1 must be 100% complete

## Estimated Duration
1 week

## Success Validation
```bash
# Should return only new pattern
grep -r "github_service" . --include="*.py"

# Should pass without errors
python validate_config.py

# Should find 0 broken links
python check_links.py

# Should show no dual implementations
python detect_dual_patterns.py
```

## Pattern Cleanup Checklist
- [ ] Repository patterns unified (ADR-005)
- [ ] Session management standardized (ADR-006)
- [ ] Configuration validation working (ADR-027)
- [ ] Service calls single-flow (new)
- [ ] Import paths cleaned (new)
- [ ] Documentation links fixed (new)

---

**Note**: This epic follows the Inchworm Protocol - must be 100% complete before moving to CORE-GREAT-3
