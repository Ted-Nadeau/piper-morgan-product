# LLM Configuration Architecture

**Component**: LLM Configuration & Provider Management
**Status**: Production
**Version**: 2.0 (Post-Refactoring)

---

## Overview

The LLM configuration system provides secure, multi-provider API key management following Domain-Driven Design principles.

---

## Architecture Layers

### Domain Layer

```
services/domain/llm_domain_service.py
```

- **Purpose**: Mediates ALL LLM access
- **Pattern**: Domain Service (ADR-029, Pattern-008)
- **Responsibilities**:
  - Provider selection
  - Request routing
  - Error handling
  - Logging

### Infrastructure Layer

```
services/config/llm_config_service.py
services/infrastructure/keychain_service.py
services/llm/provider_selector.py
```

- **Purpose**: External system integration
- **Responsibilities**:
  - API key storage/retrieval
  - Provider configuration
  - Key validation

---

## Component Details

### LLMDomainService

**Location**: `services/domain/llm_domain_service.py`

**Interface**:

```python
class LLMDomainService:
    async def initialize() -> None
    async def complete(prompt: str, provider: str = None) -> str
    def get_available_providers() -> List[str]
    def get_default_provider() -> str
```

**Usage**:

```python
from services.service_registry import ServiceRegistry

llm = ServiceRegistry.get_llm()
response = await llm.complete("Hello", provider="openai")
```

---

### KeychainService

**Location**: `services/infrastructure/keychain_service.py`

**Interface**:

```python
class KeychainService:
    def store_api_key(provider: str, key: str) -> None
    def get_api_key(provider: str) -> Optional[str]
    def delete_api_key(provider: str) -> bool
    def check_migration_status(providers: List[str]) -> Dict
```

**Storage**:

- Service: `piper-morgan`
- Key format: `{provider}_api_key`
- Backend: macOS Keychain (encrypted)

---

### LLMConfigService

**Location**: `services/config/llm_config_service.py`

**Responsibilities**:

- Key retrieval (keychain-first, env fallback)
- Provider validation
- Configuration loading
- Migration support

**Fallback Chain**:

```
1. macOS Keychain (encrypted) ✅
2. Environment variables (migration support)
3. None (graceful degradation)
```

---

### ProviderSelector

**Location**: `services/llm/provider_selector.py`

**Purpose**: Intelligent provider selection based on:

- Task type (coding, research, general)
- Provider availability
- Cost considerations
- Exclusion rules

---

## Initialization Flow

```
main.py
  ↓
initialize_domain_services()
  ↓
LLMDomainService.initialize()
  ↓
├─ LLMConfigService.validate_all_providers()
├─ ProviderSelector initialization
└─ Client initialization
  ↓
ServiceRegistry.register("llm", service)
```

---

## Access Pattern

**All consumers** use ServiceRegistry:

```python
# Application Layer (web, CLI, Slack)
from services.service_registry import ServiceRegistry

llm = ServiceRegistry.get_llm()
response = await llm.complete(prompt)
```

**Never access directly**:

- ❌ `from services.llm.clients import llm_client`
- ❌ `from services.config.llm_config_service import LLMConfigService`

---

## Provider Configuration

**File**: `config/PIPER.user.md`

```yaml
llm:
  default_provider: openai
  excluded_providers:
    - anthropic # Don't use during development

  environment: development # or production
```

---

## Security Model

### Key Storage

- **Production**: macOS Keychain (encrypted, OS-managed)
- **Migration**: Environment variables (temporary)
- **Never**: Plaintext files

### Access Control

- Keys loaded once at startup
- Never logged or exposed
- Encrypted at rest
- OS-level protection

### Key Rotation

1. Generate new key at provider
2. Store in keychain: `python scripts/migrate_keys_to_keychain.py`
3. Verify: `python scripts/test_llm_keys.py`
4. Revoke old key at provider

---

## Testing

### Unit Tests

- `tests/config/test_llm_config_service.py` (35 tests)
- `tests/domain/test_llm_domain_service.py` (15 tests)
- `tests/llm/test_provider_selector.py` (8 tests)

### Integration Tests

- Real API validation
- End-to-end provider selection
- ServiceRegistry integration

---

## Migration Path

From environment variables to keychain:

```bash
# 1. Check status
python scripts/migrate_keys_to_keychain.py --dry-run

# 2. Migrate
python scripts/migrate_keys_to_keychain.py

# 3. Verify
python scripts/test_llm_keys.py

# 4. Clean up .env
# Remove API keys from .env file
```

---

## Related ADRs

- **ADR-029**: Domain Service Mediation Architecture
- **Pattern-008**: DDD Service Layer Pattern
- **ADR-010**: Configuration Management (Hybrid Access)

---

## Future Enhancements

- [ ] Additional providers (Cohere, Together AI)
- [ ] Cost tracking per provider
- [ ] Usage analytics
- [ ] Automatic key rotation
- [ ] Multi-user support

---

_Architecture documented: October 9, 2025_
