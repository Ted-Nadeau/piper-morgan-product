# Environment Variable & Keyring Architecture Investigation
**Date**: 2025-11-30
**Scope**: Comprehensive mapping of env vars and keyring usage
**Status**: Complete

---

## Section 1: Environment Variables - Current Usage Map

### 1.1 API Keys (Secrets)

These are sensitive credentials that should ideally be in keyring, not .env:

| Variable | Provider | Usage | Default | Notes |
|----------|----------|-------|---------|-------|
| `OPENAI_API_KEY` | OpenAI | LLM config service | None (required) | Referenced in 40+ places |
| `ANTHROPIC_API_KEY` | Anthropic | LLM config service | None (optional) | Used for Claude models |
| `GEMINI_API_KEY` | Google Gemini | LLM config service | None (optional) | Used for Gemini models |
| `PERPLEXITY_API_KEY` | Perplexity | LLM config service | None (optional) | Used for Perplexity models |
| `GITHUB_TOKEN` | GitHub | GitHub integration | None (optional) | Can also use `GH_TOKEN` as fallback |
| `GH_TOKEN` | GitHub | GitHub integration | None (optional) | Fallback for `GITHUB_TOKEN` |
| `SLACK_BOT_TOKEN` | Slack | Slack integration | None (optional) | Format: `xoxb-*` |
| `SLACK_APP_TOKEN` | Slack | Slack integration | None (optional) | Format: `xapp-*` |
| `SLACK_SIGNING_SECRET` | Slack | Slack integration | None (optional) | Request verification |
| `NOTION_API_KEY` | Notion | Notion integration | None (optional) | Bearer token for API calls |

**Key Finding**: All API keys are directly read via `os.getenv()` throughout the codebase. This is **anti-pattern #1** - they should be retrieved from keyring, not environment.

### 1.2 Database Configuration (Infrastructure)

| Variable | Component | Usage | Default | Notes |
|----------|-----------|-------|---------|-------|
| `POSTGRES_USER` | PostgreSQL | Connection string | `"piper"` | Database user |
| `POSTGRES_PASSWORD` | PostgreSQL | Connection string | `"dev_changeme_in_production"` | ⚠️ Default password in code |
| `POSTGRES_HOST` | PostgreSQL | Connection string | `"localhost"` | Database host |
| `POSTGRES_PORT` | PostgreSQL | Connection string | `"5433"` | Non-standard port (not 5432) |
| `POSTGRES_DB` | PostgreSQL | Connection string | `"piper_morgan"` | Database name |
| `POSTGRES_SSL_MODE` | PostgreSQL | Connection SSL | `"prefer"` | SSL preference |
| `POSTGRES_SSL_ROOT_CERT` | PostgreSQL | SSL cert path | None | Optional SSL root CA |
| `POSTGRES_SSL_CERT` | PostgreSQL | SSL cert path | None | Optional client cert |
| `POSTGRES_SSL_KEY` | PostgreSQL | SSL cert path | None | Optional client key |

**Location**: `services/database/connection.py` - heavily concentrated

### 1.3 Application Configuration (Non-Secret)

| Variable | Component | Usage | Default | Notes |
|----------|-----------|-------|---------|-------|
| `ENVIRONMENT` | Core | Env detection | `"development"` | One of: development, staging, production |
| `PIPER_ENVIRONMENT` | Core | Env detection (LLM) | `"development"` | ⚠️ Duplicate of `ENVIRONMENT` |
| `APP_DEBUG` | Database | Debug logging | `"false"` | Enable SQL echo |
| `BACKEND_PORT` | Server | Port binding | `8001` | HTTP backend port |
| `WEB_PORT` | Server | Port binding | `8080`/`8081` | Frontend port (env-dependent) |
| `BACKEND_HOST` | Server | Host binding | `"0.0.0.0"`/`"127.0.0.1"` | Binding address (env-dependent) |
| `WEB_HOST` | Server | Host binding | `"0.0.0.0"`/`"127.0.0.1"` | Binding address (env-dependent) |

### 1.4 Integration Configuration (Non-Secret)

| Variable | Integration | Usage | Default | Notes |
|-----------|-------------|-------|---------|-------|
| `NOTION_WORKSPACE_ID` | Notion | Workspace ID | None | User's workspace ID |
| `NOTION_ENVIRONMENT` | Notion | Environment | `"development"` | API environment selection |
| `NOTION_API_BASE_URL` | Notion | Base URL | None | Custom API endpoint |
| `NOTION_TIMEOUT_SECONDS` | Notion | Timeout | `30` (from config) | Request timeout |
| `NOTION_RATE_LIMIT_RPM` | Notion | Rate limiting | `60` (from config) | Requests per minute |
| `GOOGLE_CALENDAR_ID` | Calendar | Calendar ID | `"primary"` | Google Calendar identifier |
| `GOOGLE_TOKEN_FILE` | Calendar | Token path | `"token.json"` | OAuth token file |
| `GOOGLE_CLIENT_SECRETS_FILE` | Calendar | Secrets path | `"credentials.json"` | OAuth credentials file |
| `GOOGLE_CALENDAR_SCOPES` | Calendar | OAuth scopes | Standard scopes | Comma-separated scopes |
| `GOOGLE_CALENDAR_TIMEOUT` | Calendar | Timeout | `30` | Request timeout |
| `SLACK_ENVIRONMENT` | Slack | Environment | `"development"` | API environment |
| `SLACK_TIMEOUT_SECONDS` | Slack | Timeout | `30` | Request timeout |
| `SLACK_MAX_RETRIES` | Slack | Retries | `3` | Max retry attempts |
| `SLACK_RATE_LIMIT_RPM` | Slack | Rate limiting | `60` | Requests per minute |
| `SLACK_BURST_LIMIT` | Slack | Burst limit | `10` | Max burst size |
| `SLACK_DEFAULT_CHANNEL` | Slack | Channel | None | Default message channel |
| `SLACK_CLIENT_ID` | Slack | OAuth | None | OAuth client ID |
| `SLACK_CLIENT_SECRET` | Slack | OAuth | None | OAuth client secret |
| `SLACK_REDIRECT_URI` | Slack | OAuth | None | OAuth callback URI |
| `SLACK_WEBHOOK_URL` | Slack | Webhook | None | Incoming webhook URL |
| `SLACK_API_BASE_URL` | Slack | Base URL | None | Custom API endpoint |
| `GITHUB_API_TIMEOUT` | GitHub | Timeout | `30` | Request timeout |
| `GITHUB_API_PER_PAGE` | GitHub | Pagination | `30` | Results per page |
| `GITHUB_ENABLE_METRICS` | GitHub | Metrics | `"true"` | Enable metrics collection |
| `GITHUB_USE_PRODUCTION_CLIENT` | GitHub | Client mode | `"true"` | Use production client |
| `GITHUB_ENABLE_CONTENT_GENERATION` | GitHub | Content gen | `"true"` | Enable auto-generation |
| `GITHUB_ALLOWED_REPOS` | GitHub | Access control | Empty | Comma-separated repo list |
| `DEMO_API_KEY` | Demo | API key | `""` | Demo integration key |
| `DEMO_API_ENDPOINT` | Demo | Endpoint | `"https://api.example.com"` | Demo API endpoint |
| `DEMO_ENABLED` | Demo | Feature flag | `"true"` | Enable demo mode |

### 1.5 Feature Flags (Behavior Control)

| Variable | Feature | Usage | Default | Notes |
|----------|---------|-------|---------|-------|
| `REQUIRE_AUTH` | Auth | Standup routes | `"true"` | Require authentication |
| `ENABLE_MCP_FILE_SEARCH` | MCP | File searching | `"false"` | Enable MCP file search |
| `ENABLE_ETHICS_ENFORCEMENT` | Ethics | Intent processing | `"false"` | Enable ethics checks |
| `ENABLE_KNOWLEDGE_GRAPH` | Knowledge graph | Intent processing | `"false"` | Enable knowledge graph |
| `USE_SPATIAL_GITHUB` | Spatial | GitHub router | `false` | Use spatial GitHub impl |
| `ALLOW_LEGACY_GITHUB` | Legacy | GitHub router | `false` | Allow legacy GitHub |
| `USE_SPATIAL_CALENDAR` | Spatial | Calendar router | `false` | Use spatial calendar |
| `ALLOW_LEGACY_CALENDAR` | Legacy | Calendar router | `false` | Allow legacy calendar |
| `USE_MCP_GITHUB` | MCP | GitHub integration | `true` | Use MCP GitHub |
| `USE_MCP_POOL` | MCP | Connection pooling | `false` | Use MCP connection pool |
| `MCP_MAX_CONNECTIONS` | MCP | Pool config | `10` | Max pool connections |
| `MCP_CONNECTION_TIMEOUT` | MCP | Pool config | `30.0` | Connection timeout |
| `MCP_SERVER_URL` | MCP | Server config | `"stdio://./scripts/mcp_file_server.py"` | MCP server URL |
| `PIPER_EXCLUDED_PROVIDERS` | LLM | Config | `""` | Comma-separated excluded LLMs |
| `PIPER_DEFAULT_PROVIDER` | LLM | Config | `"openai"` | Default LLM provider |
| `JWT_SECRET_KEY` | Auth | JWT signing | None (required) | Secret for token signing |
| `REDIS_URL` | Cache | Redis | `"redis://localhost:6379"` | Redis connection URL |

---

## Section 2: Keyring Storage - Current Implementation

### 2.1 Keyring Service Architecture

**File**: `services/infrastructure/keychain_service.py`

```python
SERVICE_NAME = "piper-morgan"
```

The keychain service provides:
- **Storage method**: `keyring.set_password(service_name, key_name, api_key)`
- **Retrieval method**: `keyring.get_password(service_name, key_name)`
- **Deletion method**: `keyring.delete_password(service_name, key_name)`

### 2.2 Keyring Key Naming Convention

Keys stored in keyring follow this pattern:

```
{provider}_api_key          # Single user: "openai_api_key"
{username}_{provider}_api_key  # Multi-user: "user123_openai_api_key"
```

### 2.3 Supported Providers in Keyring

According to `list_stored_keys()`:

1. `openai`
2. `anthropic`
3. `gemini`
4. `perplexity`

**Gap Finding**: GitHub, Slack, Notion tokens are NOT handled by keyring service! Only LLM providers are supported.

### 2.4 Usage Locations

**Current keyring usage is MINIMAL**:

- `services/infrastructure/keychain_service.py:96` - `keyring.set_password()`
- `services/infrastructure/keychain_service.py:119` - `keyring.get_password()`

**That's it**. Only 2 actual uses of keyring in production code!

### 2.5 User API Key Storage (Database Alternative)

**File**: `services/security/user_api_key_service.py`

The system has a **separate** database-based approach via `UserAPIKey` model:
- Stores API keys in `user_api_keys` table
- Encrypted at rest in database
- Per-user, per-provider tracking
- Methods: `store_user_key()`, `retrieve_user_key()`, `validate_api_key()`

**Gap Finding**: Two competing storage mechanisms:
1. Keyring (OS-level, global scope)
2. Database `UserAPIKey` table (application-level, per-user)

---

## Section 3: Setup Wizard Flow & Environment Handling

### 3.1 Setup Wizard Entry Point

**File**: `scripts/setup_wizard.py`

```python
# Main entry: async def run_setup_wizard()
# Called from main.py when setup is incomplete
```

### 3.2 Environment Variable Reading in Setup Wizard

The setup wizard checks environment variables for **three keys only**:

**Line 666**: `openai_key = os.environ.get("OPENAI_API_KEY")`
```python
# Check if OPENAI_API_KEY is already in environment
# If found, validate it
# If not, prompt user to enter manually via getpass()
```

**Line 754**: `anthropic_key = os.environ.get("ANTHROPIC_API_KEY")`
```python
# Same pattern: check env → validate → or prompt
```

**Line 827**: `github_token = os.environ.get("GITHUB_TOKEN")`
```python
# Same pattern: check env → store (no validation) → or prompt
```

### 3.3 Setup Wizard Storage Strategy

The wizard stores keys in **database** via `UserAPIKeyService`:

```python
# Lines 674-680: Store OpenAI key
await service.store_user_key(
    user_id=user_id,
    provider="openai",
    api_key=openai_key,
    session=session,
    validate=True,  # Validate during storage
)
```

**Key points**:
- Keys are stored in `user_api_keys` table, NOT keyring
- Each key is associated with a specific user
- Keys are validated during storage
- No fallback to keyring during setup

### 3.4 Load Dotenv Timing

**File**: `main.py:9-12`

```python
from dotenv import load_dotenv
load_dotenv()  # Loads BEFORE any other imports
```

This is called **at module import time**, making `.env` available globally.

**Observation**: This means `.env` is loaded once at startup, not per-request.

### 3.5 Setup Completion Check

**Function**: `is_setup_complete()` (lines 1119-1160)

Checks:
1. At least one user exists in `users` table
2. At least one active OpenAI key exists in `user_api_keys` table

If either fails, triggers setup wizard on startup.

---

## Section 4: Architecture Gaps & Issues Discovered

### Gap 1: No Unified Secret Storage Strategy

**Problem**: The codebase has THREE approaches to storing secrets:

1. **Environment variables** (.env file)
   - Used everywhere for API keys
   - Loaded at startup via `load_dotenv()`
   - No encryption at rest
   - Hard to rotate

2. **OS Keyring** (barely used)
   - Created in `services/infrastructure/keychain_service.py`
   - Only supports 4 LLM providers
   - Never actually called in normal flow
   - Not integrated into main API key retrieval

3. **Database** (UserAPIKey table)
   - Only used during setup wizard
   - Per-user, per-provider
   - Encrypted at application level
   - Not used for actual API calls

**Current pattern in code**:
```python
# This is how LLM config actually retrieves keys (line 206 of llm_config_service.py)
key = os.getenv(env_var)  # Reads from environment, NOT keyring or database!
```

### Gap 2: Inconsistent Configuration Reading

**Problem**: Integration config services read from BOTH environment and user config:

```python
# From slack/config_service.py:184-185 (pattern replicated across all integrations)
bot_token=os.getenv("SLACK_BOT_TOKEN", auth_config.get("bot_token", "")),
app_token=os.getenv("SLACK_APP_TOKEN", auth_config.get("app_token", "")),
```

**Reading order**:
1. Check environment variable
2. Fall back to user config dictionary
3. Use default if both missing

This creates ambiguity: which takes precedence? What if both are set to different values?

### Gap 3: Database Credentials in Code Defaults

**Critical Finding**: Default database password is in source code!

**File**: `services/database/connection.py:68`

```python
password = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
```

The string `"dev_changeme_in_production"` is hardcoded as the default. This:
- Creates security liability (password in git history)
- Encourages insecure development practices
- Makes it hard to force password changes

### Gap 4: Setup Wizard Doesn't Create .env File

**Finding**: Setup wizard reads from environment variables but doesn't:
- Create `.env` file
- Document what to put in `.env`
- Validate environment is properly set up

Users must manually create `.env` or set environment variables.

### Gap 5: Feature Flags Mix Boolean and String Values

**Problem**: Inconsistent boolean handling:

```python
# Some use string comparison
os.getenv("REQUIRE_AUTH", "true").lower() == "true"

# Some use is_true() checks
os.getenv("ENABLE_MCP_FILE_SEARCH", "false").lower() == "true"

# Some use direct string
os.getenv("SLACK_ENVIRONMENT", "development")
```

No centralized boolean parsing. Easy to make mistakes.

### Gap 6: Missing Environment Variables Documentation

**Finding**: `.env.example` file exists but is not readable/maintainable:
- Not integrated into setup wizard
- Not validated against
- Not automatically updated when new variables added
- Manual process to keep in sync

### Gap 7: Keyring Backend Assumption

**File**: `services/infrastructure/keychain_service.py:67`

```python
backend = keyring.get_keyring()
logger.info(...backend=backend.__class__.__name__...)
```

The code assumes `keyring` will work, but:
- macOS Keychain requires specific setup
- Linux users might not have keyring service
- Windows has `pywin32` dependency
- Test environments might not have keyring backend

No fallback if keyring fails during initialization.

### Gap 8: Keychain Service Not Integrated

**Critical**: Even though `KeychainService` exists, it's never used for actual API key retrieval:

```python
# From llm_config_service.py - how keys are ACTUALLY retrieved
key = os.getenv(env_var)  # Direct os.getenv, NOT keyring!

# The keychain service exists but is only used in main.py 'keys' command
keychain.store_api_key(provider, secret)  # Manual CLI command only
```

---

## Section 5: Questions for PM (xian)

### Q1: What's the intended secret storage strategy?

**Current state**: Three competing mechanisms. Which should be canonical?

**Options**:
1. **Keyring-first** (OS-level security)
   - Store all secrets in OS keyring
   - Fall back to env during migration
   - Remove hardcoded defaults

2. **Database-first** (application-level control)
   - Store in `user_api_keys` table
   - Encrypt at rest
   - Per-user scoping
   - Requires authenticated access

3. **Environment + Keyring hybrid**
   - .env for config only (non-secrets)
   - Keyring for all API keys
   - Setup wizard helps migrate

### Q2: Should setup wizard create .env file?

**Current**: No. Users must manually set environment variables or create .env.

**Question**: Should setup wizard:
1. Create `.env` with all documented variables?
2. Only require critical variables?
3. Validate existing .env against schema?

### Q3: How should multi-user scenarios work?

**Current state**:
- KeychainService supports username parameter: `"user123_openai_api_key"`
- UserAPIKey table has `user_id` foreign key
- But setup wizard only stores single user's keys

**Question**: Should setup wizard support:
1. Multiple users with separate API keys?
2. Shared global keys for integrations?
3. Both (team workspace + personal overrides)?

### Q4: Should feature flags be environment-only?

**Current**: Feature flags scattered across multiple env vars with inconsistent naming/format.

**Suggested improvements**:
1. Centralized feature flag service
2. Consistent boolean parsing
3. Runtime modification (without restart)?
4. Experiment framework integration?

### Q5: What's the migration path from .env to keyring?

**Current**: Keychain service has `check_migration_status()` method but it's never called.

**Questions**:
1. Should migration happen automatically in setup?
2. Should there be a separate migration command?
3. How to handle secrets that are stored in both places?
4. How long to support .env fallback?

### Q6: Should database credentials be in keyring?

**Current**: PostgreSQL password defaults to hardcoded string.

**Options**:
1. Always require POSTGRES_PASSWORD env var
2. Store in keyring (system-wide, not per-user)
3. Prompt during setup
4. Use connection file (~/.pgpass)

### Q7: How to handle test environments?

**Current**: Tests patch `os.environ` directly.

**Questions**:
1. Should tests use real keyring?
2. Should tests use in-memory keyring?
3. Should tests skip keyring entirely (mock)?
4. How to manage test secrets securely?

---

## Section 6: Recommendations Summary

### High Priority
1. **Integrate KeychainService into actual API key retrieval**
   - Update `llm_config_service.py` to use keyring instead of os.getenv()
   - Update integration config services similarly
   - Provide environment variable fallback for migration period

2. **Standardize secret storage**
   - Choose canonical location (keyring vs database)
   - Document the decision with ADR
   - Update setup wizard accordingly

3. **Remove hardcoded database password**
   - Require explicit POSTGRES_PASSWORD environment variable
   - Or prompt during setup
   - Or use OS-level keyring

### Medium Priority
4. **Improve setup wizard secret handling**
   - Create/validate .env file
   - Check for existing environment variables
   - Offer to migrate from env to keyring
   - Better error messages for missing secrets

5. **Centralize feature flag parsing**
   - Create FeatureFlagService with consistent boolean conversion
   - Validate flag names at startup
   - Support runtime updates (optional)

6. **Document environment variables**
   - Update .env.example to be canonical source of truth
   - Add descriptions and valid values
   - Version it with schema validation

### Low Priority
7. **Add migration command**
   - `python main.py migrate-secrets` to move .env → keyring
   - Verify both sources have same values
   - Report conflicts

8. **Enhance keyring service**
   - Add support for Slack, GitHub, Notion tokens
   - Add backup/restore functionality
   - Add audit logging

---

## Appendix: File Locations Reference

**Main Files Mentioned**:
- `/Users/xian/Development/piper-morgan/main.py` - Entry point, load_dotenv() call
- `/Users/xian/Development/piper-morgan/scripts/setup_wizard.py` - Setup flow, env var collection
- `/Users/xian/Development/piper-morgan/services/infrastructure/keychain_service.py` - Keyring wrapper
- `/Users/xian/Development/piper-morgan/services/config/llm_config_service.py` - LLM provider config
- `/Users/xian/Development/piper-morgan/services/database/connection.py` - DB credentials
- `/Users/xian/Development/piper-morgan/services/integrations/*/config_service.py` - Integration configs

**Environment Variables By Category**:
- **API Keys**: 10 variables (OpenAI, Anthropic, Gemini, Perplexity, GitHub, Slack, Notion)
- **Database**: 8 variables (PostgreSQL connection details)
- **Server**: 5 variables (port, host, environment)
- **Integrations**: 25+ variables (Notion, Calendar, Slack, GitHub, Demo)
- **Feature Flags**: 13 variables (MCP, ethics, spatial, etc.)
- **LLM Config**: 4 variables (environment, defaults, exclusions)

**Total Unique Environment Variables: ~65 across all files**

---

**Investigation completed**: All major uses of os.getenv/os.environ identified, keyring usage mapped, setup wizard flow documented, gaps documented with questions for PM review.
