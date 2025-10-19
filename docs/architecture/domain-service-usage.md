# Domain Service Usage by Layer

**Created**: October 19, 2025
**Issue**: #119 (CORE-STAND-FOUND)
**Related ADR**: ADR-029 (Domain Service Mediation Architecture)

## Overview

This document clarifies which layers should use domain services vs integration routers, based on the established architecture from ADR-029.

## Layer Pattern

```
Feature Layer (services/features/)
    ↓ uses
Domain Service Layer (services/domain/)
    ↓ uses internally
Integration Router Layer (services/integrations/)
    ↓ uses
External Systems (GitHub API, Slack API, etc.)
```

## Feature Layer (`services/features/`)

**SHOULD use**: Domain Services

✅ **Correct patterns**:
```python
from services.domain.github_domain_service import GitHubDomainService
from services.domain.slack_domain_service import SlackDomainService
from services.domain.notion_domain_service import NotionDomainService
from services.domain.calendar_domain_service import CalendarDomainService
```

❌ **Incorrect patterns** (bypasses domain layer):
```python
from services.integrations.github.github_integration_router import GitHubIntegrationRouter
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
```

**Examples**:
- `MorningStandupWorkflow` → Uses `GitHubDomainService` ✅
- `PersonalityManager` → Uses domain services ✅

## Orchestration Layer (`services/orchestration/`, `services/domain/*_orchestration_service.py`)

**SHOULD use**: Domain Services

✅ **Correct patterns**:
```python
# services/domain/standup_orchestration_service.py
from services.domain.github_domain_service import GitHubDomainService

workflow = MorningStandupWorkflow(
    github_domain_service=self._github_domain_service,  # ✅ Correct!
    ...
)
```

**Why**: Orchestration services mediate between features and domain services. They provide clean dependency injection and follow the same layer separation as features.

## Domain Service Layer (`services/domain/`)

**Uses**: Integration Routers internally
**Provides**: Clean abstractions for features

✅ **Correct patterns**:
```python
# services/domain/github_domain_service.py
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

class GitHubDomainService:
    def __init__(self):
        self._router = GitHubIntegrationRouter()  # ✅ Internal usage
```

**Why**: Domain services encapsulate integration complexity and provide business-focused interfaces.

## Integration Router Layer (`services/integrations/`)

**Uses**: External APIs
**Provides**: Routers and adapters with feature flag control

```python
# services/integrations/github/github_integration_router.py
class GitHubIntegrationRouter:
    def __init__(self):
        self._spatial = GitHubSpatialIntelligence()

    def get_recent_issues(self, ...):
        integration = self._get_integration()
        return integration.get_recent_issues(...)
```

## Architecture Enforcement

The codebase includes architecture enforcement tests (`tests/test_architecture_enforcement.py`) that verify:

1. **No direct GitHubAgent imports** - Services must use routers
2. **Domain services use routers** - Not legacy agents
3. **Orchestration/feature layers use domain services** - Not routers directly

### Enforcement Updates (October 19, 2025)

The architecture enforcement was corrected to align with ADR-029:

**Before** (too strict):
```python
required_router_services = [
    "services/domain/standup_orchestration_service.py",  # ❌ Incorrect!
    ...
]
```

**After** (correct):
```python
required_router_services = [
    # Orchestration services use domain services per ADR-029
    "services/domain/github_domain_service.py",  # ✅ Domain service
    "services/domain/pm_number_manager.py",      # ✅ Domain service
    ...
]
```

## Examples from Codebase

### ✅ Correct: Morning Standup (Feature Layer)

```python
# services/features/morning_standup.py
from services.domain.github_domain_service import GitHubDomainService

class MorningStandupWorkflow:
    def __init__(
        self,
        github_domain_service: GitHubDomainService,  # ✅ Domain service
        ...
    ):
        self.github_domain_service = github_domain_service
```

### ✅ Correct: Standup Orchestration (Orchestration Layer)

```python
# services/domain/standup_orchestration_service.py
from services.domain.github_domain_service import GitHubDomainService

class StandupOrchestrationService:
    def _initialize_dependencies(self):
        self._github_domain_service = GitHubDomainService()  # ✅ Domain service

    async def orchestrate_standup_workflow(self, user_id):
        workflow = MorningStandupWorkflow(
            github_domain_service=self._github_domain_service,  # ✅
            ...
        )
```

### ✅ Correct: GitHub Domain Service (Domain Layer)

```python
# services/domain/github_domain_service.py
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

class GitHubDomainService:
    def __init__(self):
        self._router = GitHubIntegrationRouter()  # ✅ Router for external access
```

## Testing Patterns

When testing services:

### Feature/Orchestration Layer Tests

```python
# tests/features/test_morning_standup.py
mock_github_domain_service = AsyncMock()  # ✅ Mock domain service
mock_github_domain_service.get_recent_issues.return_value = []

workflow = MorningStandupWorkflow(
    github_domain_service=mock_github_domain_service,  # ✅
    ...
)
```

### Domain Service Layer Tests

```python
# tests/domain/test_github_domain_service.py
@patch('services.integrations.github.github_integration_router.GitHubIntegrationRouter')
def test_github_domain_service(mock_router):
    mock_router_instance = Mock()
    mock_router.return_value = mock_router_instance

    service = GitHubDomainService()
    # Test domain service logic
```

## Summary

| Layer | Uses | Example |
|-------|------|---------|
| Feature | Domain Services | `MorningStandupWorkflow` → `GitHubDomainService` |
| Orchestration | Domain Services | `StandupOrchestrationService` → `GitHubDomainService` |
| Domain | Integration Routers | `GitHubDomainService` → `GitHubIntegrationRouter` |
| Integration | External APIs | `GitHubIntegrationRouter` → GitHub API |

## References

- **ADR-029**: Domain Service Mediation Architecture (September 12, 2025)
- **Issue #119**: CORE-STAND-FOUND - Morning Standup Foundation
- **Issue #193**: CORE-GREAT-2 - GitHub Architecture Enforcement
- `docs/architecture/github-integration-router.md` - Router pattern documentation
- `tests/test_architecture_enforcement.py` - Architecture enforcement tests
