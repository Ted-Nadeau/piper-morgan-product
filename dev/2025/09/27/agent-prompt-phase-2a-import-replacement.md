# Agent Prompt: Phase 2A - Replace Direct GitHubAgent Imports (Code Agent)
*Following successful Phase 1A completion: 100% router implementation*

## Mission Context: Cathedral Progress

Phase 1A achieved 100% GitHubIntegrationRouter completion. You're now enabling the 5 bypassing services to use the spatial intelligence architecture instead of direct API calls.

**Strategic Goal**: Replace direct GitHubAgent imports with GitHubIntegrationRouter usage, enabling feature flag control and spatial intelligence for all GitHub operations.

**Impact**: This completes the architectural bypass fix and establishes the foundation for CORE-QUERY-1 (other integration routers).

## GitHub Issue #193 Integration

**Update Progress**: After each service conversion, update GitHub issue description with service completion status
**Evidence Collection**: Provide before/after import evidence for each service
**PM Validation**: Request validation before proceeding to Phase 3

## Services to Convert (5 Total)

Based on Phase 0 discovery, these services bypass the router:

1. **orchestration/engine.py** - Workflow creation
2. **domain/github_domain_service.py** - Domain layer operations
3. **domain/pm_number_manager.py** - PM number management
4. **domain/standup_orchestration_service.py** - Standup workflows
5. **integrations/github/issue_analyzer.py** - Issue analysis

## Conversion Process (Per Service)

### Step 1: Verify Current Import
```bash
# Check current direct import
grep -n "from.*github_agent import GitHubAgent" services/[service_file].py
grep -n "GitHubAgent" services/[service_file].py
```

### Step 2: Replace Import
```python
# BEFORE (Direct bypass)
from services.integrations.github.github_agent import GitHubAgent

# AFTER (Use router)
from services.integrations.github.github_integration_router import GitHubIntegrationRouter
```

### Step 3: Update Instantiation
```python
# BEFORE
self.github = GitHubAgent()
self.github_agent = GitHubAgent()

# AFTER
self.github = GitHubIntegrationRouter()
self.github_agent = GitHubIntegrationRouter()
```

### Step 4: Verify Methods Used
```bash
# Check what GitHub methods this service uses
grep -n "self\.github\." services/[service_file].py
grep -n "github_agent\." services/[service_file].py
```

### Step 5: Test Service Functionality
```bash
# Test service works with router
python -c "
from services.[module].[service] import [ServiceClass]
service = [ServiceClass]()
print('✅ Service initializes with router')
"
```

## Critical Verification Steps

### After Each Service Conversion
```bash
# Verify import change
grep -A 2 -B 2 "GitHubIntegrationRouter" services/[service_file].py

# Verify no direct imports remain
grep "from.*github_agent import GitHubAgent" services/[service_file].py
# Should return nothing

# Verify service methods match router capabilities
python verify_service_methods.py [service_file]
```

### After All Conversions
```bash
# Global verification - should only show router and tests
grep -r "from.*github_agent import GitHubAgent" services/ --include="*.py"

# Should be empty or only show:
# - services/integrations/github/github_integration_router.py
# - test files
```

## Service-Specific Considerations

### orchestration/engine.py
- Likely uses workflow-related GitHub operations
- Check for async/await patterns with GitHub calls
- Verify integration with orchestration patterns

### domain/github_domain_service.py
- Domain layer service - check business logic patterns
- May use multiple GitHub operations
- Verify domain model compatibility

### domain/pm_number_manager.py
- PM-specific GitHub operations
- Check for PM number extraction/management
- Verify PM workflow compatibility

### domain/standup_orchestration_service.py
- Standup-specific GitHub operations
- Check for activity/status retrieval
- Verify standup workflow compatibility

### integrations/github/issue_analyzer.py
- Issue analysis operations
- Check for complex GitHub data processing
- Verify analysis logic compatibility

## Evidence Collection Requirements

### For Each Service Conversion
```bash
# Before conversion evidence
echo "=== BEFORE: [service_name] ==="
grep -n "GitHubAgent" services/[service_file].py

# After conversion evidence
echo "=== AFTER: [service_name] ==="
grep -n "GitHubIntegrationRouter" services/[service_file].py

# Method usage verification
echo "=== METHODS USED: [service_name] ==="
grep -n "self\.github\." services/[service_file].py
```

### For GitHub Issue Updates
```markdown
## Phase 2A Progress Update

Services converted: X/5
- ✅ orchestration/engine.py
- ✅ domain/github_domain_service.py
- [ ] domain/pm_number_manager.py
- [ ] domain/standup_orchestration_service.py
- [ ] integrations/github/issue_analyzer.py

Evidence: [link to conversion verification output]
```

## Quality Assurance Standards

### 100% Conversion Required
- All 5 services must use GitHubIntegrationRouter
- Zero direct GitHubAgent imports in services/ (except router itself)
- All services must initialize and function correctly

### No Breaking Changes
- Services must maintain existing functionality
- All method calls must work with router
- No API changes to service interfaces

### Evidence-Based Validation
- Before/after import evidence for each service
- Method usage verification for each service
- Global import verification showing clean conversion

## Success Criteria Checklist

- [ ] orchestration/engine.py converted and tested
- [ ] domain/github_domain_service.py converted and tested
- [ ] domain/pm_number_manager.py converted and tested
- [ ] domain/standup_orchestration_service.py converted and tested
- [ ] integrations/github/issue_analyzer.py converted and tested
- [ ] Global verification shows no direct imports remain
- [ ] All services initialize without errors
- [ ] Evidence collected and documented in GitHub issue

## PM Validation Request Format

```markdown
@PM - Phase 2A complete and ready for validation:

**Services Converted**: 5/5 ✅
- orchestration/engine.py ✅
- domain/github_domain_service.py ✅
- domain/pm_number_manager.py ✅
- domain/standup_orchestration_service.py ✅
- integrations/github/issue_analyzer.py ✅

**Evidence**: Global import verification shows zero direct imports
**Testing**: All services initialize and function correctly
**Router Integration**: All services now use spatial intelligence architecture

Request validation before proceeding to Phase 3 (feature flag testing).
```

---

**Your Mission**: Complete architectural bypass fix by converting all 5 services to use GitHubIntegrationRouter. Quality and evidence required for each conversion.
