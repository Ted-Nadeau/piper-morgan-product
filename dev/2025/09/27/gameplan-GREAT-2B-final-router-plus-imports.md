# Final Gameplan: CORE-GREAT-2B - Complete GitHub Router & Fix Imports

**Date**: September 28, 2025 (Final revision 2:20 PM)
**Issue**: #193
**Architect**: Claude Opus 4.1
**Lead Developer**: Claude Sonnet 4

---

## Mission: Complete GitHub Router Infrastructure & Fix Architectural Bypass

### Discovery Summary
1. **First finding**: Services bypass router via direct imports
2. **Second finding**: Router only 14% complete (2 of 14 methods)
3. **Strategic decision**: Complete router FIRST, then fix imports

This becomes the pattern for CORE-QUERY-1 (other routers).

---

## Phase 1: Complete GitHubIntegrationRouter (3 hours)

### Deploy: Code for Implementation, Cursor for Testing

#### 1A. Implement Missing Critical Methods

Based on service usage analysis, implement these 5 critical methods first:

```python
# In services/integrations/github/github_integration_router.py

def get_issue_by_url(self, issue_url: str):
    """Used by github_domain_service, issue_analyzer"""
    if self._use_spatial():
        return self.spatial_backend.get_issue_by_url(issue_url)
    else:
        return self.legacy_agent.get_issue_by_url(issue_url)

def get_open_issues(self, repo: str = None):
    """Used by github_domain_service, pm_number_manager"""
    if self._use_spatial():
        return self.spatial_backend.get_open_issues(repo)
    else:
        return self.legacy_agent.get_open_issues(repo)

def get_recent_issues(self, days: int = 7):
    """Used by github_domain_service"""
    if self._use_spatial():
        return self.spatial_backend.get_recent_issues(days)
    else:
        return self.legacy_agent.get_recent_issues(days)

def get_recent_activity(self, days: int = 7):
    """Used by standup_orchestration_service"""
    if self._use_spatial():
        return self.spatial_backend.get_recent_activity(days)
    else:
        return self.legacy_agent.get_recent_activity(days)

def list_repositories(self):
    """Used by github_domain_service"""
    if self._use_spatial():
        return self.spatial_backend.list_repositories()
    else:
        return self.legacy_agent.list_repositories()
```

#### 1B. Implement Remaining Methods

Complete the other 7 methods following the same pattern:
- Check feature flag
- Delegate to spatial or legacy
- Maintain consistent return types

#### 1C. Verify Router Completeness

```python
# Create test: tests/test_router_completeness.py
def test_github_router_has_all_agent_methods():
    """Ensure router implements all GitHubAgent methods"""
    agent_methods = [m for m in dir(GitHubAgent) if not m.startswith('_')]
    router_methods = [m for m in dir(GitHubIntegrationRouter) if not m.startswith('_')]

    missing = set(agent_methods) - set(router_methods)
    assert not missing, f"Router missing methods: {missing}"
```

---

## Phase 2: Replace Direct Imports (2 hours)

### Deploy: Both Agents - Systematic Import Replacement

#### 2A. Fix All Bypassing Services

Replace imports in these files:
```python
# orchestration/engine.py
- from services.integrations.github.github_agent import GitHubAgent
+ from services.integrations.github.github_integration_router import GitHubIntegrationRouter

# domain/github_domain_service.py
- from services.integrations.github.github_agent import GitHubAgent
+ from services.integrations.github.github_integration_router import GitHubIntegrationRouter

# domain/pm_number_manager.py
- from services.integrations.github.github_agent import GitHubAgent
+ from services.integrations.github.github_integration_router import GitHubIntegrationRouter

# domain/standup_orchestration_service.py
- from services.integrations.github.github_agent import GitHubAgent
+ from services.integrations.github.github_integration_router import GitHubIntegrationRouter

# integrations/github/issue_analyzer.py
- from services.integrations.github.github_agent import GitHubAgent
+ from services.integrations.github.github_integration_router import GitHubIntegrationRouter
```

#### 2B. Update Instantiation

In each service, also update the instantiation:
```python
# Before
self.github = GitHubAgent()

# After
self.github = GitHubIntegrationRouter()
```

#### 2C. Verify No Direct Imports Remain

```bash
# Should return ONLY test files or the router itself
grep -r "from.*github_agent import GitHubAgent" . --include="*.py" | grep -v test | grep -v router

# Should be empty or only show allowed locations
```

---

## Phase 3: Test Feature Flag Control (1 hour)

### Deploy: Cursor for Testing, Code for Fixes

#### 3A. Test Each Service with Spatial

```bash
# Force spatial mode
export USE_SPATIAL_GITHUB=true
export ALLOW_LEGACY_GITHUB=false

# Test each previously-bypassing service
pytest tests/domain/test_github_domain_service.py -v
pytest tests/domain/test_pm_number_manager.py -v
pytest tests/domain/test_standup_orchestration.py -v
pytest tests/integrations/test_issue_analyzer.py -v
pytest tests/orchestration/test_engine.py -v
```

#### 3B. Test Each Service with Legacy

```bash
# Force legacy mode
export USE_SPATIAL_GITHUB=false
export ALLOW_LEGACY_GITHUB=true

# Run same tests, verify legacy path works
pytest tests/domain/test_github_domain_service.py -v
# ... etc
```

#### 3C. Verify Router Controls Behavior

```python
# Create test to verify feature flag control
def test_feature_flag_controls_github_behavior():
    """Verify feature flags actually control spatial/legacy routing"""

    # Test with spatial enabled
    os.environ['USE_SPATIAL_GITHUB'] = 'true'
    router = GitHubIntegrationRouter()
    # Add assertion that spatial backend is used

    # Test with legacy enabled
    os.environ['USE_SPATIAL_GITHUB'] = 'false'
    router = GitHubIntegrationRouter()
    # Add assertion that legacy backend is used
```

---

## Phase 4: Architectural Lock (30 min)

### Both Agents - Ensure Pattern Compliance

#### 4A. Create Architecture Test

```python
# tests/architecture/test_no_direct_github_imports.py
def test_no_direct_github_agent_imports():
    """Ensure no service bypasses the router"""

    import subprocess
    result = subprocess.run(
        ["grep", "-r", "from.*github_agent import GitHubAgent", "services/",
         "--include=*.py"],
        capture_output=True,
        text=True
    )

    violations = []
    for line in result.stdout.split('\n'):
        if line and 'test' not in line and 'router' not in line:
            violations.append(line)

    assert not violations, f"Direct GitHubAgent imports found:\n{violations}"
```

#### 4B. Add to CI/CD

```yaml
# .github/workflows/ci.yml
- name: Check GitHub Router Compliance
  run: |
    pytest tests/architecture/test_no_direct_github_imports.py -v
    pytest tests/test_router_completeness.py -v
```

---

## Phase 5: Documentation (30 min)

### Both Agents - Document the Pattern

#### 5A. Create Router Completion Guide

```markdown
# docs/architecture/router-completion-pattern.md

## Router Completion Pattern (from GREAT-2B)

### Problem
Services bypass incomplete routers via direct imports.

### Solution
1. Complete router with all agent methods
2. Each method delegates to spatial/legacy based on feature flags
3. Replace all direct imports with router imports
4. Test feature flag control

### Pattern for Other Routers (CORE-QUERY-1)
Apply same pattern to:
- Slack Router
- Notion Router
- Calendar Router
```

#### 5B. Update GitHub Issue

```markdown
## GREAT-2B Complete

### Router Completion
- Implemented all 14 GitHubAgent methods in router
- Proper spatial/legacy delegation
- Feature flag control verified

### Import Fixes
- Replaced all 5 direct imports with router
- No bypassing services remain

### Evidence
- Router completeness test: ✓
- No direct imports test: ✓
- Feature flag control: ✓
- All tests passing: ✓

This establishes pattern for CORE-QUERY-1.
```

---

## Success Criteria

- [ ] GitHubIntegrationRouter has all 14 methods
- [ ] All methods delegate to spatial/legacy properly
- [ ] Zero direct GitHubAgent imports remain
- [ ] Feature flags control behavior
- [ ] All tests pass with both modes
- [ ] Architecture test prevents regression
- [ ] Documentation shows pattern for other routers

---

## Time Estimate

- Phase 1: 3 hours (router completion)
- Phase 2: 2 hours (import replacement)
- Phase 3: 1 hour (testing)
- Phase 4: 30 minutes (architectural lock)
- Phase 5: 30 minutes (documentation)
- **Total: ~7 hours**

Longer than original estimate but includes the critical router completion work.

---

## What This Enables

1. **Immediate**: GitHub services use proper architecture
2. **CORE-QUERY-1**: Clear pattern for other routers
3. **GREAT-2C-E**: Simpler after all routers complete

---

*Complete the router. Fix the imports. Lock the pattern. This is the way.*
