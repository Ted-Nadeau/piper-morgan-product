# Agent Prompt: Phase 1A - GitHubIntegrationRouter Quality Implementation
*Following agent-prompt-template.md v7.0 with full methodology compliance*

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project under Lead Developer supervision. You follow systematic methodology and provide evidence for all claims.

## Essential Context: CORE-GREAT-2 Strategic Mission
**Strategic Goal**: Complete GitHub spatial intelligence migration to enable architectural consistency across all integrations. This work establishes patterns for CORE-QUERY-1 (other integration routers).

**Why This Matters**:
- Spatial intelligence provides 8-dimensional analysis vs basic API calls
- Router pattern enables feature flag control for gradual migration
- Bypassing routers defeats the entire spatial intelligence architecture
- Shortcuts or pattern violations undermine the strategic migration

**Epic Context**: CORE-GREAT-2B is part 2 of 5 in the spatial intelligence migration. Success here enables CORE-QUERY-1 work on Slack, Notion, and Calendar routers.

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Gameplan Assumptions FIRST
**Before implementing ANYTHING, verify infrastructure matches gameplan**:

```bash
# Verify GitHubIntegrationRouter exists and current state
ls -la services/integrations/github/github_integration_router.py
wc -l services/integrations/github/github_integration_router.py

# Verify GitHubAgent exists (source for method signatures)
ls -la services/integrations/github/github_agent.py
wc -l services/integrations/github/github_agent.py

# Check spatial implementation exists
ls -la services/integrations/spatial/github_spatial.py
wc -l services/integrations/spatial/github_spatial.py

# Verify current router implementation level
grep -c "def [a-z]" services/integrations/github/github_integration_router.py
grep -c "def [a-z]" services/integrations/github/github_agent.py
```

**If reality doesn't match gameplan assumptions, STOP immediately and report the mismatch.**

## Session Log Management
**Continue using existing session log**: `/home/claude/2025-09-27-1246-working-log.md`
**Do NOT create a new session log**

## MANDATORY REQUIREMENTS (Non-Negotiable)

### Requirement 1: EXACT Method Signatures
**COPY signatures directly from GitHubAgent - do NOT modify anything**

```bash
# For each method, get exact signature:
grep -A 2 "def method_name" services/integrations/github/github_agent.py

# Example process:
grep -A 2 "def get_issue_by_url" services/integrations/github/github_agent.py
# Copy signature EXACTLY including type hints and parameter names
```

### Requirement 2: MANDATORY Delegation Pattern
**EVERY method MUST follow this EXACT pattern**:

```python
def method_name(self, *args, **kwargs):
    """Docstring explaining what this method does and which services use it"""
    integration, is_legacy = self._get_preferred_integration("method_name")
    if integration:
        if is_legacy:
            self._warn_deprecation_if_needed("method_name")
        return integration.method_name(*args, **kwargs)
    else:
        raise RuntimeError(f"No GitHub integration available for method_name")
```

**All 4 components are MANDATORY**:
1. `_get_preferred_integration()` call
2. `_warn_deprecation_if_needed()` for legacy
3. `integration.method_name()` delegation
4. `RuntimeError` with specific method name

### Requirement 3: Quality Over Speed
**Take time to implement correctly. The previous 3-minute implementation failed quality requirements. Better to take appropriate time and get it right.**

## Critical Methods to Implement (Priority Order)

Based on Cursor verification findings, implement these methods with EXACT signatures:

### Phase 1A-1: Critical Methods (Used by Bypassing Services)
1. **get_issue_by_url** - Used by domain/github_domain_service.py, integrations/github/issue_analyzer.py
2. **get_open_issues** - Used by domain/github_domain_service.py, domain/pm_number_manager.py
3. **get_recent_issues** - Used by domain/github_domain_service.py
4. **get_recent_activity** - Used by domain/standup_orchestration_service.py
5. **list_repositories** - Used by domain/github_domain_service.py

### Phase 1A-2: Additional Methods
Find remaining 7 methods in GitHubAgent and implement using same pattern.

## Implementation Process

### Step 1: Get ALL GitHubAgent Method Signatures
```bash
# Get complete list of public methods
grep -n "def [a-z]" services/integrations/github/github_agent.py

# For each method, capture exact signature:
grep -A 3 "def get_issue_by_url" services/integrations/github/github_agent.py
grep -A 3 "def get_open_issues" services/integrations/github/github_agent.py
# Continue for all methods
```

### Step 2: Implement Critical Methods First
For each critical method:

```python
def get_issue_by_url(self, issue_url: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve GitHub issue by URL.
    Used by: domain/github_domain_service.py, integrations/github/issue_analyzer.py
    """
    integration, is_legacy = self._get_preferred_integration("get_issue_by_url")
    if integration:
        if is_legacy:
            self._warn_deprecation_if_needed("get_issue_by_url")
        return integration.get_issue_by_url(issue_url)
    else:
        raise RuntimeError("No GitHub integration available for get_issue_by_url")
```

### Step 3: Verify Each Method Before Moving to Next
After implementing each method:
- Signature matches GitHubAgent exactly ✓
- Has `_get_preferred_integration` call ✓
- Has deprecation warning for legacy ✓
- Has `RuntimeError` with method name ✓
- Delegates to `integration.method_name` ✓

## MANDATORY VERIFICATION SCRIPTS

### Pattern Verification Script
```python
# Run after each method implementation:
import inspect
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

router = GitHubIntegrationRouter()
methods = [m for m in dir(router) if not m.startswith('_') and callable(getattr(router, m))]

for method_name in methods:
    method = getattr(router, method_name)
    source = inspect.getsource(method)

    # Check ALL required pattern elements
    has_preferred = '_get_preferred_integration' in source
    has_warning = '_warn_deprecation_if_needed' in source
    has_error = 'RuntimeError' in source
    has_method_name = method_name in source

    if has_preferred and has_warning and has_error and has_method_name:
        print(f"✅ {method_name} - pattern complete")
    else:
        print(f"❌ {method_name} - pattern incomplete:")
        if not has_preferred: print("   Missing _get_preferred_integration")
        if not has_warning: print("   Missing deprecation warning")
        if not has_error: print("   Missing RuntimeError")
        if not has_method_name: print("   Missing method name in error")
```

### Signature Verification Script
```python
# Run after all methods implemented:
import inspect
from services.integrations.github.github_agent import GitHubAgent
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

agent = GitHubAgent()
router = GitHubIntegrationRouter()

agent_methods = [m for m in dir(agent) if not m.startswith('_') and callable(getattr(agent, m))]

for method_name in agent_methods:
    if hasattr(router, method_name):
        agent_sig = inspect.signature(getattr(agent, method_name))
        router_sig = inspect.signature(getattr(router, method_name))

        if agent_sig == router_sig:
            print(f"✅ {method_name} - signature matches")
        else:
            print(f"❌ {method_name} - signature mismatch:")
            print(f"   Agent:  {agent_sig}")
            print(f"   Router: {router_sig}")
    else:
        print(f"❌ {method_name} - missing from router")
```

## SUCCESS CRITERIA (All Must Pass)

**Router Completeness**:
- [ ] All 14 GitHubAgent methods implemented in router
- [ ] All signatures match GitHubAgent exactly (0 mismatches)
- [ ] All methods follow delegation pattern (100% compliance)

**Pattern Compliance**:
- [ ] Pattern verification script shows 100% compliance
- [ ] Signature verification script shows 100% matches
- [ ] All methods have proper docstrings with usage notes

**Quality Assurance**:
- [ ] No syntax errors or import failures
- [ ] Router initializes without errors
- [ ] All critical methods (5) implemented first

## Evidence Requirements

**For each implemented method, provide**:
- Exact signature copied from GitHubAgent
- Confirmation of pattern compliance
- Verification script output showing success

**For completion, provide**:
- Full pattern verification script output
- Full signature verification script output
- Count of methods: GitHubAgent vs GitHubIntegrationRouter

## Anti-Patterns to Avoid

❌ **Don't change parameter names or types from GitHubAgent**
❌ **Don't skip any of the 4 mandatory pattern components**
❌ **Don't implement methods without proper docstrings**
❌ **Don't claim completion without running verification scripts**

## Related Documentation Context

This work enables:
- **Immediate**: Phase 2 import replacement in 5 bypassing services
- **CORE-QUERY-1**: Router completion pattern for Slack, Notion, Calendar
- **Spatial Intelligence**: 8-dimensional analysis vs basic API calls
- **Feature Flag Control**: Gradual migration capabilities

## STOP Conditions

Stop immediately and escalate if:
- Infrastructure doesn't match verification commands
- GitHubAgent signatures are ambiguous or complex
- Spatial integration patterns are unclear
- Cannot provide evidence for pattern compliance

---

**Your mission: Complete GitHubIntegrationRouter with architectural integrity. Quality over speed. Evidence required for all claims.**
