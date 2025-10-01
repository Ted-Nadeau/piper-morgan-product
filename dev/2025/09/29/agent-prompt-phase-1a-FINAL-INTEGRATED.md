# Agent Prompt: Phase 1A - GitHubIntegrationRouter Implementation (Final)
*Incorporating methodology analysis, GitHub tracking integration, and cathedral context*

## Your Mission: Building the Cathedral

You are completing **GitHubIntegrationRouter** to enable spatial intelligence architecture across all GitHub operations. This is not just implementing methods - you're building the foundation that enables 8-dimensional analysis vs basic API calls, with feature flag control for gradual adoption.

**The Cathedral**: Your work establishes the pattern for CORE-QUERY-1 (Slack, Notion, Calendar routers) and enables the entire spatial intelligence migration. When you lack proper resources or encounter unclear requirements, escalate rather than compromise quality.

## Strategic Context: CORE-GREAT-2B

**Current Reality**: GitHub integration infrastructure exists but services bypass it because router is only 14% complete (2 of 14 methods). Services must use direct imports because router lacks needed operations.

**Your Goal**: Complete all 14 GitHubAgent methods in router with proper spatial/legacy delegation, enabling 5 bypassing services to use architectural patterns.

**Why This Matters**: Enables spatial intelligence (8-dimensional analysis) vs basic API calls, establishes feature flag control, and provides the pattern for all integration routers.

## Infrastructure Verification (MANDATORY FIRST)

Verify reality matches expectations before implementing:

```bash
# Verify current router state
wc -l services/integrations/github/github_integration_router.py
grep -c "def [a-z]" services/integrations/github/github_integration_router.py

# Verify GitHubAgent source
wc -l services/integrations/github/github_agent.py
grep -c "def [a-z]" services/integrations/github/github_agent.py

# Verify spatial implementation exists
ls -la services/integrations/spatial/github_spatial.py
```

If reality doesn't match, STOP and report the mismatch with evidence.

## GitHub Issue #193 Integration

**Progressive Tracking**: Update GitHub issue #193 throughout your work:
- After implementing each method: Update method count in issue description
- After verification: Add evidence output to issue comments
- On any blocker: Report immediately with context
- Before requesting PM validation: Provide all required evidence

**Evidence Collection**: Each phase completion requires specific verification output as detailed in issue #193.

## Implementation Requirements (Non-Negotiable)

### 1. Exact Method Signatures
Copy signatures directly from GitHubAgent - no modifications:

```bash
# For each method, get exact signature:
grep -A 2 "def method_name" services/integrations/github/github_agent.py
```

### 2. Mandatory Delegation Pattern
Every method MUST follow this exact pattern:

```python
def method_name(self, *args, **kwargs):
    """Docstring explaining purpose and which services use it"""
    integration, is_legacy = self._get_preferred_integration("method_name")
    if integration:
        if is_legacy:
            self._warn_deprecation_if_needed("method_name")
        return integration.method_name(*args, **kwargs)
    else:
        raise RuntimeError(f"No GitHub integration available for method_name")
```

All 4 components are mandatory:
- `_get_preferred_integration()` call
- `_warn_deprecation_if_needed()` for legacy
- `integration.method_name()` delegation
- `RuntimeError` with specific method name

### 3. Quality Over Speed
Take the time needed to implement correctly. Previous implementation failed quality requirements. Architectural integrity is more important than completion speed.

## Critical Methods (Priority Order)

**Phase 1A-1: Critical Methods (Used by Bypassing Services)**
1. `get_issue_by_url` - Used by domain/github_domain_service.py, integrations/github/issue_analyzer.py
2. `get_open_issues` - Used by domain/github_domain_service.py, domain/pm_number_manager.py
3. `get_recent_issues` - Used by domain/github_domain_service.py
4. `get_recent_activity` - Used by domain/standup_orchestration_service.py
5. `list_repositories` - Used by domain/github_domain_service.py

**Phase 1A-2: Remaining Methods**
Find the other 7 GitHubAgent methods and implement with same pattern.

## Implementation Process

### Step 1: Method Discovery
```bash
# Get all GitHubAgent public methods
grep -n "def [a-z]" services/integrations/github/github_agent.py > agent_methods.txt

# For each method, capture exact signature
grep -A 3 "def get_issue_by_url" services/integrations/github/github_agent.py
# Continue for all methods
```

### Step 2: Implement with Verification
For each method:
1. Copy exact signature from GitHubAgent
2. Implement delegation pattern
3. Add descriptive docstring with service usage
4. Verify pattern compliance before next method

### Step 3: Progressive Verification
After every 2-3 methods, run verification scripts:

```python
# Pattern compliance check
import inspect
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

def verify_pattern_compliance():
    router = GitHubIntegrationRouter()
    methods = [m for m in dir(router) if not m.startswith('_') and callable(getattr(router, m))]

    for method_name in methods:
        method = getattr(router, method_name)
        source = inspect.getsource(method)

        has_preferred = '_get_preferred_integration' in source
        has_warning = '_warn_deprecation_if_needed' in source
        has_error = 'RuntimeError' in source
        has_method_name = method_name in source

        if has_preferred and has_warning and has_error and has_method_name:
            print(f"✅ {method_name} - pattern complete")
        else:
            print(f"❌ {method_name} - pattern incomplete")
            if not has_preferred: print("   Missing _get_preferred_integration")
            if not has_warning: print("   Missing deprecation warning")
            if not has_error: print("   Missing RuntimeError")
            if not has_method_name: print("   Missing method name in error")

verify_pattern_compliance()
```

## Required Evidence Collection

### For GitHub Issue #193 Comments
After implementation completion, provide:

```bash
# Router completeness verification
python -c "
from services.integrations.github.github_agent import GitHubAgent
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

agent_methods = len([m for m in dir(GitHubAgent) if not m.startswith('_') and callable(getattr(GitHubAgent, m))])
router_methods = len([m for m in dir(GitHubIntegrationRouter) if not m.startswith('_') and callable(getattr(GitHubIntegrationRouter, m))])

print(f'GitHubAgent methods: {agent_methods}')
print(f'Router methods: {router_methods}')
print(f'Completeness: {router_methods}/{agent_methods} = {100*router_methods/agent_methods:.1f}%')
"

# Pattern compliance verification
python verify_pattern_compliance.py

# Signature compatibility verification
python -c "
import inspect
from services.integrations.github.github_agent import GitHubAgent
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

agent = GitHubAgent()
router = GitHubIntegrationRouter()
agent_methods = [m for m in dir(agent) if not m.startswith('_') and callable(getattr(agent, m))]

mismatches = 0
for method_name in agent_methods:
    if hasattr(router, method_name):
        agent_sig = inspect.signature(getattr(agent, method_name))
        router_sig = inspect.signature(getattr(router, method_name))
        if agent_sig != router_sig:
            print(f'❌ {method_name} signature mismatch')
            mismatches += 1
        else:
            print(f'✅ {method_name} signature matches')

print(f'Total signature mismatches: {mismatches}')
"
```

## Success Criteria (Must ALL Pass)

- [ ] All 14 GitHubAgent methods implemented in router
- [ ] All signatures match GitHubAgent exactly (0 mismatches)
- [ ] All methods follow delegation pattern (100% compliance)
- [ ] Pattern verification script shows 100% compliance
- [ ] Router initializes without errors
- [ ] Evidence provided in GitHub issue #193

## PM Validation Request

After completing implementation and collecting evidence:

```markdown
@PM - Phase 1A complete and ready for validation:

**Router Completeness**: [X]/14 methods implemented ✅
**Pattern Compliance**: [verification script output] ✅
**Signature Compatibility**: [verification script output] ✅
**Evidence**: [link to verification outputs in issue comments] ✅

Request validation before proceeding to Phase 2 (import replacement).
```

## Quality Standards

**Architectural Necessity**: Pattern compliance is not optional - it's required for spatial intelligence migration success.

**Evidence Required**: No claims without verification output.

**Escalation Protocol**: If you encounter unclear requirements, missing context, or implementation challenges, escalate immediately rather than compromise quality.

**Session Log**: Continue using existing log `/home/claude/2025-09-27-1246-working-log.md`

---

**Your Mission**: Complete GitHubIntegrationRouter with architectural integrity. You're enabling spatial intelligence migration across all integrations. Quality over speed. Evidence required for all claims.
