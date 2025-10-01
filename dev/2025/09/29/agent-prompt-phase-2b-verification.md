# Agent Prompt: Phase 2B - Verify Import Replacement Quality (Cursor Agent)
*Cross-verification of Code agent's Phase 2A import replacement work*

## Mission: Verify Architectural Bypass Fix

Code agent has converted 5 bypassing services to use GitHubIntegrationRouter instead of direct GitHubAgent imports. Your role is to verify the quality and completeness of these conversions before proceeding to Phase 3.

**Critical Standard**: 100% conversion completeness - no partial success accepted for foundational infrastructure.

## Verification Framework

### 1. Conversion Completeness Verification
```bash
# Global import scan - should find ZERO direct imports in services
echo "=== GLOBAL IMPORT VERIFICATION ==="
grep -r "from.*github_agent import GitHubAgent" services/ --include="*.py"

# Expected result: Empty OR only these allowed locations:
# - services/integrations/github/github_integration_router.py (imports for delegation)
# - test files (tests can import directly)

# If ANY services show up, conversion is INCOMPLETE
```

### 2. Service-by-Service Verification
For each of the 5 services, verify proper conversion:

```bash
# Verify each service individually
services=(
    "services/orchestration/engine.py"
    "services/domain/github_domain_service.py"
    "services/domain/pm_number_manager.py"
    "services/domain/standup_orchestration_service.py"
    "services/integrations/github/issue_analyzer.py"
)

for service in "${services[@]}"; do
    echo "=== Verifying $service ==="

    # Check for proper router import
    grep -n "GitHubIntegrationRouter" "$service"

    # Check no direct agent imports remain
    grep -n "GitHubAgent" "$service"

    # Check instantiation patterns
    grep -n "\.GitHubIntegrationRouter()" "$service"

    echo "---"
done
```

### 3. Functional Verification
```python
# Test each service can initialize with router
def test_service_initialization():
    """Verify all converted services can initialize without errors"""

    try:
        # Test orchestration engine
        from services.orchestration.engine import OrchestrationEngine
        engine = OrchestrationEngine()
        print("✅ OrchestrationEngine initializes with router")
    except Exception as e:
        print(f"❌ OrchestrationEngine failed: {e}")

    try:
        # Test GitHub domain service
        from services.domain.github_domain_service import GitHubDomainService
        service = GitHubDomainService()
        print("✅ GitHubDomainService initializes with router")
    except Exception as e:
        print(f"❌ GitHubDomainService failed: {e}")

    try:
        # Test PM number manager
        from services.domain.pm_number_manager import PMNumberManager
        manager = PMNumberManager()
        print("✅ PMNumberManager initializes with router")
    except Exception as e:
        print(f"❌ PMNumberManager failed: {e}")

    try:
        # Test standup orchestration
        from services.domain.standup_orchestration_service import StandupOrchestrationService
        standup = StandupOrchestrationService()
        print("✅ StandupOrchestrationService initializes with router")
    except Exception as e:
        print(f"❌ StandupOrchestrationService failed: {e}")

    try:
        # Test issue analyzer
        from services.integrations.github.issue_analyzer import IssueAnalyzer
        analyzer = IssueAnalyzer()
        print("✅ IssueAnalyzer initializes with router")
    except Exception as e:
        print(f"❌ IssueAnalyzer failed: {e}")

test_service_initialization()
```

### 4. Method Compatibility Verification
```python
# Verify services use methods that exist in router
def verify_method_compatibility():
    """Check that services only use methods available in router"""

    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    router = GitHubIntegrationRouter()
    available_methods = [m for m in dir(router) if not m.startswith('_') and callable(getattr(router, m))]

    print(f"Router provides {len(available_methods)} methods:")
    for method in sorted(available_methods):
        print(f"  - {method}")

    # Check each service's method usage
    services_to_check = [
        "services/orchestration/engine.py",
        "services/domain/github_domain_service.py",
        "services/domain/pm_number_manager.py",
        "services/domain/standup_orchestration_service.py",
        "services/integrations/github/issue_analyzer.py"
    ]

    for service_file in services_to_check:
        print(f"\n=== Method usage in {service_file} ===")
        with open(service_file, 'r') as f:
            content = f.read()

        # Find GitHub method calls
        import re
        method_calls = re.findall(r'(?:self\.github|github_agent)\.(\w+)', content)

        for method_call in set(method_calls):
            if method_call in available_methods:
                print(f"  ✅ {method_call} - available in router")
            else:
                print(f"  ❌ {method_call} - NOT available in router")

verify_method_compatibility()
```

## Quality Assurance Checklist

### Conversion Completeness
- [ ] All 5 services import GitHubIntegrationRouter
- [ ] Zero services import GitHubAgent directly
- [ ] All services instantiate router correctly
- [ ] Global import scan shows clean conversion

### Functional Completeness
- [ ] All 5 services initialize without errors
- [ ] All method calls use router-available methods
- [ ] No breaking changes to service interfaces
- [ ] Services maintain existing functionality

### Quality Standards
- [ ] 100% conversion rate (not 80%, not 90%, not 95%)
- [ ] Evidence-based verification with output
- [ ] All tests demonstrate working functionality

## Common Issues to Check For

### Incomplete Conversion
- Service imports both GitHubAgent AND GitHubIntegrationRouter
- Service has mixed instantiation patterns
- Service uses direct imports in some methods but router in others

### Method Compatibility Issues
- Service calls methods not available in router
- Service expects different method signatures
- Service uses async patterns incompatible with router

### Instantiation Problems
- Service instantiates with wrong parameters
- Service expects different initialization pattern
- Service fails to initialize with router

## Reporting Format

### Phase 2B Verification Results
```markdown
## Phase 2B Results: Import Replacement Verification

### Conversion Completeness
- Global import scan: [CLEAN/VIOLATIONS_FOUND]
- Services converted: X/5
- Router imports verified: [YES/NO]

### Service-by-Service Results
- orchestration/engine.py: [✅ CONVERTED / ❌ ISSUES]
- domain/github_domain_service.py: [✅ CONVERTED / ❌ ISSUES]
- domain/pm_number_manager.py: [✅ CONVERTED / ❌ ISSUES]
- domain/standup_orchestration_service.py: [✅ CONVERTED / ❌ ISSUES]
- integrations/github/issue_analyzer.py: [✅ CONVERTED / ❌ ISSUES]

### Functional Verification
- Service initialization: X/5 passing
- Method compatibility: [COMPATIBLE/ISSUES_FOUND]
- Breaking changes: [NONE/IDENTIFIED]

### Quality Assessment
[READY_FOR_PHASE_3 / NEEDS_FIXES]

### Issues Requiring Resolution
[List any problems found that must be fixed]
```

## Success Criteria (All Must Pass)

- [ ] Global import scan shows zero direct GitHubAgent imports in services
- [ ] All 5 services use GitHubIntegrationRouter
- [ ] All 5 services initialize without errors
- [ ] All method calls are router-compatible
- [ ] No breaking changes introduced
- [ ] Evidence provided for all verification steps

## Critical Standards Reminder

**100% Standard**: Partial conversion is not acceptable for foundational infrastructure. If any service still uses direct imports, the conversion is incomplete and Phase 3 cannot proceed.

**Evidence Required**: All claims must be backed by verification output. No "looks good" without test results.

**Quality Gate**: This verification determines readiness for Phase 3 feature flag testing. Only proceed if all criteria pass.

---

**Your Mission**: Verify the architectural bypass fix is complete and ready for feature flag testing. Maintain 100% quality standards for foundational infrastructure.
