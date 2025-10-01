# Agent Prompt: Phase 0A - Verify GitHubIntegrationRouter Completeness

## Mission: Critical Router Verification for CORE-GREAT-2B
**Objective**: Verify GitHubIntegrationRouter can handle ALL operations currently done by direct GitHubAgent imports

## Context from Lead Developer
**Discovery**: 5+ services bypass GitHubIntegrationRouter through direct GitHubAgent imports
**Risk**: About to refactor all bypassing services to use router instead
**Critical**: Must confirm router supports all operations before refactoring

## Bypassing Services Found:
- orchestration/engine.py
- domain/github_domain_service.py
- domain/pm_number_manager.py
- domain/standup_orchestration_service.py
- integrations/github/issue_analyzer.py

## Investigation Tasks

### Task 1: List All GitHubAgent Methods
```bash
# Get complete method list from GitHubAgent
grep -n "def " services/integrations/github/github_agent.py | grep -v "__"

# Focus on public methods (what services actually use)
grep -n "def [a-z]" services/integrations/github/github_agent.py
```

### Task 2: List All Router Methods
```bash
# Get complete method list from GitHubIntegrationRouter
grep -n "def " services/integrations/github/github_integration_router.py | grep -v "__"

# Look for routing methods or passthroughs
grep -n "def [a-z]" services/integrations/github/github_integration_router.py
```

### Task 3: Check What Bypassing Services Actually Use
```bash
# For each bypassing service, find what GitHub methods they call
for file in "orchestration/engine.py" "domain/github_domain_service.py" "domain/pm_number_manager.py" "domain/standup_orchestration_service.py" "integrations/github/issue_analyzer.py"; do
    echo "=== $file ==="
    grep -n "github\." "services/$file" | head -10
    echo
done
```

### Task 4: Create Method Comparison
```python
# Create comparison script: router_method_comparison.py
"""
Compare GitHubAgent methods vs GitHubIntegrationRouter methods
"""

import inspect
import sys
sys.path.append('.')

from services.integrations.github.github_agent import GitHubAgent
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

# Get public methods from each
agent_methods = [m for m in dir(GitHubAgent) if not m.startswith('_')]
router_methods = [m for m in dir(GitHubIntegrationRouter) if not m.startswith('_')]

print("GitHubAgent methods:")
for method in sorted(agent_methods):
    print(f"  - {method}")

print("\nGitHubIntegrationRouter methods:")
for method in sorted(router_methods):
    print(f"  - {method}")

print("\nMethods in Agent but NOT in Router:")
missing = set(agent_methods) - set(router_methods)
for method in sorted(missing):
    print(f"  ❌ {method}")

print("\nMethods in Router but NOT in Agent:")
extra = set(router_methods) - set(agent_methods)
for method in sorted(extra):
    print(f"  ➕ {method}")
```

## Expected Outcomes

### Scenario A: Router Complete ✅
- Router has all methods needed by bypassing services
- Can proceed with import replacement in Phase 1

### Scenario B: Router Missing Methods ❌
- Document specific missing methods
- Need to complete router before Phase 1
- Report to Lead Developer for scope adjustment

### Scenario C: Router Different Pattern 🤔
- Router may use different method names/patterns
- Need to understand mapping between agent and router
- May need bridge methods or different refactoring approach

## Reporting Format

```markdown
# Phase 0A Results: Router Completeness

## Method Comparison
- GitHubAgent methods: X total
- GitHubIntegrationRouter methods: Y total
- Missing from router: [list]
- Router-specific methods: [list]

## Usage Analysis
- orchestration/engine.py uses: [methods]
- domain/github_domain_service.py uses: [methods]
- [etc for each service]

## Completeness Assessment
[COMPLETE/INCOMPLETE/DIFFERENT_PATTERN]

## Recommendation
[Ready for Phase 1 / Need router completion / Need different approach]
```

## Success Criteria
- ✅ Complete method inventory for both GitHubAgent and GitHubIntegrationRouter
- ✅ Clear understanding of what each bypassing service uses
- ✅ Definitive answer on router completeness
- ✅ Ready/not ready assessment for Phase 1

---

**Deploy immediately to verify router can handle refactoring scope.**
