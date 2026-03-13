# Gameplan: CORE-GREAT-2B - Complete GitHub Spatial Migration

**Date**: September 28, 2025
**Issue**: #193 (Part 2 of 5 for CORE-GREAT-2 epic #181)
**Architect**: Claude Opus 4.1
**Lead Developer**: [To be assigned]

---

## Strategic Context: GitHub Spatial Migration Completion

### Where We Are (from GREAT-2A Discovery)
GitHub has a sophisticated 4-week deprecation router with 75% complete spatial migration infrastructure. This is NOT the dual pattern cleanup we expected - it's completion work for an already advanced system.

### Architectural Clarification (Added Sept 28)
Three layers may co-exist - we're ONLY addressing spatial:
1. **Spatial Intelligence** ← WHAT WE'RE COMPLETING
2. **MCP Pattern** ← NOTE BUT DON'T REQUIRE
3. **Plugin Architecture** ← DON'T TOUCH (GREAT-3)

### Scope Boundaries
- **DO**: Complete spatial intelligence migration
- **CHECK**: If MCP adapters exist and work with spatial
- **DON'T**: Implement MCP if missing
- **DON'T**: Touch plugin architecture
- **DON'T**: Break anything that's partially done

### Evidence from Investigation
- Advanced deprecation router exists with feature flag switching
- Spatial/legacy pattern toggle already implemented
- 75% of GitHub operations already migrated
- 4-week deprecation window before old pattern removal

### This Issue's Focus
Complete the remaining 25% of spatial migration using the existing infrastructure. No rebuilding, no major refactoring - just finish what's already 75% done.

### Scope Boundaries (PM Clarification)
- **YES**: Complete spatial intelligence integration for remaining operations
- **CHECK**: Preserve any existing MCP patterns (don't add new ones)
- **NO**: Do not address plugin architecture (GREAT-3 scope)
- **NO**: Do not break anything pre-positioned for plugins

---

## Infrastructure Verification Checkpoint

### Expected Structure (PM to verify)
```yaml
GitHub Integration:
- services/integrations/github/
  - github_agent.py (legacy?)
  - github_domain_service.py
  - github_integration_router.py (deprecation router)
  - spatial/ (spatial implementations)

Spatial System:
- services/integrations/spatial/github/ (or similar)
```

### PM Verification Required
```bash
# Verify deprecation router exists
cat services/integrations/github/github_integration_router.py | head -30

# Check spatial implementations
ls -la services/integrations/spatial/github/
ls -la services/integrations/github/spatial/

# Find feature flags or toggles
grep -r "feature.*flag\|spatial.*toggle\|deprecation" services/integrations/github/
```

---

## Phase 0: Understand Current State (45 min)

### Deploy: Both Agents Together

#### 0A. Map the Deprecation Router
```bash
# Understand the router structure
cat services/integrations/github/github_integration_router.py

# Find the feature flag mechanism
grep -r "spatial_enabled\|use_spatial\|legacy_mode" services/integrations/github/

# Check deprecation timeline
grep -r "4.*week\|deprecat.*date\|removal.*date" services/integrations/github/
```

#### 0B. Check MCP Pattern Status (Note but Don't Implement)
```bash
# Check if GitHub has MCP adapter
ls -la services/integrations/github/*mcp*
grep -r "MCP\|ModelContext" services/integrations/github/

# Document what exists but DON'T implement if missing
# This is just awareness, not a requirement
```

#### 0C. Identify Remaining Legacy Patterns
```markdown
Find what's NOT yet migrated:

1. List all GitHub operations:
   - create_issue()
   - update_issue()
   - create_pr()
   - list_issues()
   - etc.

2. For each operation, check:
   - Is there a spatial version?
   - Is the router pointing to spatial?
   - Is the legacy version marked deprecated?

3. Document the gaps:
   - Operations without spatial versions
   - Operations still routing to legacy
   - Operations not in deprecation window
```

### Evidence Collection
- List of all GitHub operations
- Status of each (spatial/legacy/mixed)
- Deprecation timeline for each

---

## Phase 1: Complete Spatial Implementations (2 hours)

### Deploy: Code for Implementation, Cursor for Verification

#### Code Instructions - Complete Missing Spatial Operations
```markdown
For each operation still using legacy pattern:

1. Find the legacy implementation:
   ```python
   # Example: Legacy create_issue
   def create_issue(self, title, body, labels):
       # Direct API call
       return self.client.create_issue(...)
   ```

2. Create spatial version following existing pattern:
   ```python
   # Example: Spatial create_issue
   def create_issue_spatial(self, context):
       # Extract spatial dimensions
       spatial_context = self.extract_spatial_context(context)

       # Apply spatial intelligence
       enhanced_request = self.spatial_mapper.enhance(
           operation="create_issue",
           context=spatial_context,
           params=context.params
       )

       # Execute with spatial awareness
       return self.spatial_executor.execute(enhanced_request)
   ```

3. Follow the pattern from completed spatial operations
```

#### Cursor Instructions - Verify Spatial Patterns
```markdown
For each new spatial implementation:

1. Verify it follows existing spatial patterns
2. Check integration with spatial mapper
3. Ensure proper error handling
4. Validate spatial context extraction

Quality checks:
- Consistent with other spatial operations
- Proper deprecation notices on legacy version
- Router updated to use spatial version
```

### Cross-Validation
- Code implements, Cursor verifies pattern consistency
- Both confirm router configuration updated
- Both verify tests passing

---

## Phase 2: Update Deprecation Router (1 hour)

### Both Agents - Router Configuration

#### 2A. Update Router Mappings
```python
# Before
ROUTE_MAPPINGS = {
    "create_issue": {
        "spatial": False,  # Still using legacy
        "handler": self.legacy_create_issue
    },
    # ...
}

# After
ROUTE_MAPPINGS = {
    "create_issue": {
        "spatial": True,  # Now using spatial
        "handler": self.spatial_create_issue,
        "legacy_handler": self.legacy_create_issue,  # Keep for rollback
        "deprecation_date": "2025-10-26"  # 4 weeks
    },
    # ...
}
```

#### 2B. Test Feature Flag Toggle
```bash
# Test with spatial enabled
GITHUB_USE_SPATIAL=true pytest tests/integrations/github/

# Test with legacy (should still work during deprecation)
GITHUB_USE_SPATIAL=false pytest tests/integrations/github/

# Verify both paths work
```

---

## Phase 3: Testing & Validation (1 hour)

### Deploy: Cursor for Testing, Code for Fixes

#### 3A. Integration Tests
```bash
# Run all GitHub integration tests
pytest tests/integrations/github/ -v

# Run spatial-specific tests
pytest tests/integrations/github/test_spatial_*.py -v

# Run deprecation tests
pytest tests/integrations/github/test_deprecation_router.py -v
```

#### 3B. End-to-End Validation
```python
# Create test script: validate_github_spatial.py
"""
Test all GitHub operations through spatial layer
"""

def test_full_github_flow():
    # Create issue via spatial
    issue = github.create_issue_spatial(context)

    # Update via spatial
    updated = github.update_issue_spatial(issue.id, context)

    # List via spatial
    issues = github.list_issues_spatial(context)

    # Verify spatial enhancement worked
    assert issue.has_spatial_metadata
    assert updated.spatial_dimensions

print("All spatial operations validated")
```

---

## Phase 4: Documentation & Deprecation Notices (30 min)

### Both Agents - Documentation Updates

#### 4A. Update Migration Guide
Create/update `docs/migrations/github-spatial-migration.md`:
```markdown
# GitHub Spatial Migration Status

## Completed Operations (as of Sept 28, 2025)
- create_issue ✅
- update_issue ✅
- create_pr ✅
- [list all completed]

## Deprecation Timeline
- Legacy patterns deprecated: Sept 28, 2025
- Removal date: Oct 26, 2025 (4 weeks)
- Feature flag: GITHUB_USE_SPATIAL

## Migration Instructions
[How to switch to spatial]
```

#### 4B. Add Deprecation Warnings
```python
# In legacy methods
import warnings

def legacy_create_issue(self, ...):
    warnings.warn(
        "legacy_create_issue is deprecated. Use spatial version. "
        "Will be removed Oct 26, 2025",
        DeprecationWarning,
        stacklevel=2
    )
    # ... existing code
```

---

## Phase Z: Lock & Handoff

### Evidence Collection
1. List of all migrated operations
2. Test results showing spatial working
3. Deprecation timeline documented
4. Router configuration updated

### GitHub Issue Update
```markdown
## GREAT-2B Complete

### Spatial Migration Status
- Operations migrated: X/Y
- All spatial implementations working
- Deprecation router updated
- 4-week removal timeline set

### Evidence
- All tests passing: [link to CI]
- Spatial operations verified: [test output]
- Documentation updated: [link]

### Next Steps
- Monitor deprecation period
- Remove legacy after Oct 26, 2025
```

### Lock Strategy Implementation
```python
# Add to tests/regression/
def test_github_spatial_lock():
    """Ensure GitHub spatial migration not reversed"""
    router = GitHubIntegrationRouter()

    # Check all operations use spatial
    for operation in router.operations:
        assert router.is_spatial_enabled(operation), \
            f"{operation} must use spatial pattern"

    # Verify deprecation notices exist
    for legacy_method in router.get_legacy_methods():
        assert hasattr(legacy_method, '__deprecated__')
```

---

## Success Criteria

- [ ] All GitHub operations have spatial versions
- [ ] Deprecation router points to spatial by default
- [ ] Legacy patterns marked with deprecation warnings
- [ ] All tests passing with spatial enabled
- [ ] Documentation shows migration status
- [ ] 4-week deprecation timeline documented
- [ ] Lock tests prevent regression

---

## STOP Conditions

- If spatial pattern different than expected
- If deprecation router more complex than described
- If breaking changes would affect production
- If less than 75% actually complete

---

## Time Estimate

- Phase 0: 45 minutes (understand current state)
- Phase 1: 2 hours (complete implementations)
- Phase 2: 1 hour (update router)
- Phase 3: 1 hour (testing)
- Phase 4: 30 minutes (documentation)
- **Total: ~5.25 hours**

---

*Complete what's started. Use existing infrastructure. No rebuilding.*
