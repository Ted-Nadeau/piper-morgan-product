# Agent Prompt: Phase 1A - Complete GitHubIntegrationRouter Implementation

## Mission: Implement All Missing GitHubAgent Methods in Router
**Objective**: Complete GitHubIntegrationRouter with all 14 GitHubAgent methods using proper delegation pattern

## Context from Phase 0 Discovery
**Current Status**: Router only has 2 of 14 methods (14.3% complete)
**Critical Missing**: 5 methods used by bypassing services + 7 additional methods
**Pattern Established**: Router has working delegation examples to follow

## Implementation Strategy

### Phase 1A: Critical Methods First (High Priority)
Implement these 5 methods used by bypassing services:

```python
# In services/integrations/github/github_integration_router.py

def get_issue_by_url(self, issue_url: str):
    """
    Used by: domain/github_domain_service.py, integrations/github/issue_analyzer.py
    Retrieve GitHub issue by URL
    """
    integration, is_legacy = self._get_preferred_integration("get_issue_by_url")
    if integration:
        if is_legacy:
            self._warn_deprecation_if_needed("get_issue_by_url")
        return integration.get_issue_by_url(issue_url)
    else:
        raise RuntimeError("No GitHub integration available for get_issue_by_url")

def get_open_issues(self, repo: str = None):
    """
    Used by: domain/github_domain_service.py, domain/pm_number_manager.py
    Get open issues for repository
    """
    integration, is_legacy = self._get_preferred_integration("get_open_issues")
    if integration:
        if is_legacy:
            self._warn_deprecation_if_needed("get_open_issues")
        return integration.get_open_issues(repo)
    else:
        raise RuntimeError("No GitHub integration available for get_open_issues")

def get_recent_issues(self, days: int = 7):
    """
    Used by: domain/github_domain_service.py
    Get recent issues within specified days
    """
    integration, is_legacy = self._get_preferred_integration("get_recent_issues")
    if integration:
        if is_legacy:
            self._warn_deprecation_if_needed("get_recent_issues")
        return integration.get_recent_issues(days)
    else:
        raise RuntimeError("No GitHub integration available for get_recent_issues")

def get_recent_activity(self, days: int = 7):
    """
    Used by: domain/standup_orchestration_service.py
    Get recent GitHub activity for standup reporting
    """
    integration, is_legacy = self._get_preferred_integration("get_recent_activity")
    if integration:
        if is_legacy:
            self._warn_deprecation_if_needed("get_recent_activity")
        return integration.get_recent_activity(days)
    else:
        raise RuntimeError("No GitHub integration available for get_recent_activity")

def list_repositories(self):
    """
    Used by: domain/github_domain_service.py
    List available repositories
    """
    integration, is_legacy = self._get_preferred_integration("list_repositories")
    if integration:
        if is_legacy:
            self._warn_deprecation_if_needed("list_repositories")
        return integration.list_repositories()
    else:
        raise RuntimeError("No GitHub integration available for list_repositories")
```

### Phase 1B: Complete Remaining Methods
Find the other 7 missing methods and implement using same pattern:

```bash
# Get complete list of GitHubAgent methods
grep -n "def [a-z]" services/integrations/github/github_agent.py

# Check what's already in router
grep -n "def [a-z]" services/integrations/github/github_integration_router.py

# Implement all missing methods following the pattern above
```

### Phase 1C: Follow Established Pattern
Study existing router methods to ensure consistency:

```python
# Example pattern from existing methods:
def existing_method(self, param):
    """Follow this exact pattern for all new methods"""
    integration, is_legacy = self._get_preferred_integration("method_name")
    if integration:
        if is_legacy:
            self._warn_deprecation_if_needed("method_name")
        return integration.method_name(param)
    else:
        raise RuntimeError(f"No GitHub integration available for method_name")
```

## Implementation Guidelines

### Method Signature Consistency
- Copy exact signatures from GitHubAgent
- Preserve parameter names, types, defaults
- Maintain return type expectations

### Documentation
- Add docstring explaining purpose
- Note which services use the method
- Follow existing router docstring format

### Error Handling
- Use same RuntimeError pattern as existing methods
- Include method name in error message
- Let integration-level errors bubble up

### Deprecation Warnings
- Include `_warn_deprecation_if_needed()` call for legacy usage
- Use exact method name as warning context

## Verification Steps

### After Each Method Implementation
```python
# Test method exists and is callable
router = GitHubIntegrationRouter()
assert hasattr(router, 'new_method_name')
assert callable(getattr(router, 'new_method_name'))
```

### After All Methods Complete
```python
# Verify completeness
from services.integrations.github.github_agent import GitHubAgent
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

agent_methods = [m for m in dir(GitHubAgent) if not m.startswith('_') and callable(getattr(GitHubAgent, m))]
router_methods = [m for m in dir(GitHubIntegrationRouter) if not m.startswith('_') and callable(getattr(GitHubIntegrationRouter, m))]

missing = set(agent_methods) - set(router_methods)
assert not missing, f"Router still missing methods: {missing}"

print(f"✅ Router completeness: {len(router_methods)}/{len(agent_methods)} methods")
```

## Expected Challenges

### Method Signature Variations
- Some methods may have complex parameter types
- Copy signatures exactly from GitHubAgent
- Maintain type hints if present

### Integration Differences
- Spatial and legacy integrations may have different method signatures
- Follow existing router patterns for handling differences
- Add adapter logic if needed

### Testing Dependencies
- Some methods may require GitHub API access
- Focus on implementation completeness
- Cursor agent will handle functional testing

## Success Criteria
- [ ] All 5 critical methods implemented
- [ ] All remaining 7 methods implemented
- [ ] Method signatures match GitHubAgent exactly
- [ ] Delegation pattern consistent across all methods
- [ ] Router completeness test passes
- [ ] No import errors or syntax issues

## Completion Checklist
```bash
# Verify implementation complete
python -c "
from services.integrations.github.github_agent import GitHubAgent
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

agent_methods = set(m for m in dir(GitHubAgent) if not m.startswith('_'))
router_methods = set(m for m in dir(GitHubIntegrationRouter) if not m.startswith('_'))

missing = agent_methods - router_methods
if missing:
    print(f'❌ Missing: {missing}')
else:
    print('✅ Router implementation complete')
"
```

---

**Deploy for 3-hour implementation session. Focus on completeness and pattern consistency.**
