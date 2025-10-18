# Environment Variables Reference

**Last Updated**: October 18, 2025

This document lists all environment variables used by Piper Morgan for configuration and feature flags.

---

## Ethics & Safety

### `ENABLE_ETHICS_ENFORCEMENT`

**Purpose**: Enable/disable ethics boundary enforcement

**Type**: Boolean (string "true" or "false")

**Default**: `false` (disabled for gradual rollout)

**Added**: October 18, 2025 (Issue #197)

**Usage**:
```bash
# Enable ethics enforcement
export ENABLE_ETHICS_ENFORCEMENT=true

# Disable ethics enforcement (default)
export ENABLE_ETHICS_ENFORCEMENT=false
```

**Behavior**:
- **`true`**: All requests through IntentService are checked for ethics violations
  - Harassment content blocked (HTTP 422)
  - Professional boundary violations blocked (HTTP 422)
  - Inappropriate content blocked (HTTP 422)
  - Complete audit trail logged
- **`false`**: Ethics checks skipped, all requests processed normally

**Coverage**: 95-100% (all entry points: web API, Slack, CLI, direct calls)

**Documentation**: `docs/internal/architecture/current/ethics-architecture.md`

**Testing**:
```bash
# Test with ethics enabled
ENABLE_ETHICS_ENFORCEMENT=true python dev/2025/10/18/test-ethics-integration.py

# Test with ethics disabled
ENABLE_ETHICS_ENFORCEMENT=false python dev/2025/10/18/test-ethics-integration.py
```

---

## Integration Configuration

### Slack

#### `SLACK_BOT_TOKEN`
**Purpose**: Slack bot OAuth token
**Type**: String (starts with `xoxb-`)
**Required**: Yes (for Slack integration)
**Example**: `xoxb-YOUR-BOT-TOKEN-HERE`

#### `SLACK_APP_TOKEN`
**Purpose**: Slack app-level token
**Type**: String (starts with `xapp-`)
**Required**: Yes (for Socket Mode)
**Example**: `xapp-YOUR-APP-TOKEN-HERE`

#### `SLACK_SIGNING_SECRET`
**Purpose**: Slack request verification secret
**Type**: String
**Required**: Yes (for webhook verification)
**Example**: `YOUR-SIGNING-SECRET-HERE`

### GitHub

#### `GITHUB_TOKEN`
**Purpose**: GitHub personal access token
**Type**: String (starts with `ghp_` or `github_pat_`)
**Required**: Yes (for GitHub integration)
**Permissions**: repo, read:org, workflow
**Example**: `ghp_YOUR_GITHUB_TOKEN_HERE`

### Notion

#### `NOTION_API_KEY`
**Purpose**: Notion integration token
**Type**: String (starts with `secret_`)
**Required**: Yes (for Notion integration)
**Example**: `secret_YOUR_NOTION_API_KEY_HERE`

#### `NOTION_WORKSPACE_ID`
**Purpose**: Notion workspace/page ID
**Type**: String (UUID format)
**Required**: Optional
**Example**: `12345678-1234-1234-1234-123456789012`

#### `NOTION_TIMEOUT_SECONDS`
**Purpose**: Notion API request timeout
**Type**: Integer
**Default**: `30`
**Example**: `60`

### Google Calendar

#### `GOOGLE_CALENDAR_ID`
**Purpose**: Google Calendar ID
**Type**: String (email format)
**Required**: Yes (for Calendar integration)
**Example**: `your-calendar@group.calendar.google.com`

#### `GOOGLE_CALENDAR_TIMEOUT`
**Purpose**: Google Calendar API timeout
**Type**: Integer (seconds)
**Default**: `30`
**Example**: `60`

---

## Development & Testing

### `PYTHONPATH`

**Purpose**: Python module search path
**Type**: String (colon-separated paths)
**Required**: Yes (for running tests/scripts)
**Example**: `PYTHONPATH=/Users/xian/Development/piper-morgan`

**Usage**:
```bash
# Run tests
PYTHONPATH=/Users/xian/Development/piper-morgan pytest tests/

# Run scripts
PYTHONPATH=/Users/xian/Development/piper-morgan python scripts/some_script.py
```

---

## Feature Flags

### Spatial Intelligence

#### `USE_SPATIAL_SLACK`
**Purpose**: Enable Slack spatial intelligence adapter
**Type**: Boolean
**Default**: `true`
**Added**: Recent (Slack spatial integration)

#### `USE_SPATIAL_CALENDAR`
**Purpose**: Enable Calendar spatial intelligence
**Type**: Boolean
**Default**: `true`

#### `USE_SPATIAL_NOTION`
**Purpose**: Enable Notion spatial intelligence
**Type**: Boolean
**Default**: `true`

### MCP (Model Context Protocol)

#### `ENABLE_MCP_FILE_SEARCH`
**Purpose**: Enable MCP file search functionality
**Type**: Boolean
**Default**: `false`
**Status**: Experimental

---

## Server Configuration

### `PORT`
**Purpose**: Web server port
**Type**: Integer
**Default**: `8001`
**Example**: `8001`

**Usage**:
```bash
# Start server on custom port
PORT=8080 python -m uvicorn web.app:app --port 8080
```

### `HOST`
**Purpose**: Web server host
**Type**: String
**Default**: `127.0.0.1`
**Example**: `0.0.0.0` (all interfaces)

---

## Database Configuration

### `DATABASE_URL`
**Purpose**: PostgreSQL connection string
**Type**: String (URL format)
**Default**: `postgresql://piper:piper@localhost:5433/piper_morgan`
**Example**: `postgresql://user:pass@host:port/database`

**Note**: Piper Morgan uses port 5433 (not standard 5432)

---

## LLM Provider Configuration

### OpenAI

#### `OPENAI_API_KEY`
**Purpose**: OpenAI API key
**Type**: String (starts with `sk-`)
**Required**: Yes (for OpenAI provider)
**Storage**: Keychain (secure)
**Example**: `sk-YOUR_OPENAI_API_KEY_HERE`

### Anthropic (Claude)

#### `ANTHROPIC_API_KEY`
**Purpose**: Anthropic API key
**Type**: String (starts with `sk-ant-`)
**Required**: Yes (for Anthropic provider)
**Storage**: Keychain (secure)
**Example**: `sk-ant-YOUR_ANTHROPIC_API_KEY_HERE`

### Google (Gemini)

#### `GEMINI_API_KEY`
**Purpose**: Google Gemini API key
**Type**: String
**Required**: Yes (for Gemini provider)
**Storage**: Keychain (secure)

### Perplexity

#### `PERPLEXITY_API_KEY`
**Purpose**: Perplexity API key
**Type**: String (starts with `pplx-`)
**Required**: Yes (for Perplexity provider)
**Storage**: Keychain (secure)
**Example**: `pplx-YOUR_PERPLEXITY_API_KEY_HERE`

---

## Logging & Monitoring

### `LOG_LEVEL`
**Purpose**: Application log level
**Type**: String (DEBUG, INFO, WARNING, ERROR, CRITICAL)
**Default**: `INFO`
**Example**: `DEBUG`

**Usage**:
```bash
# Enable debug logging
LOG_LEVEL=DEBUG python -m uvicorn web.app:app
```

---

## Quick Reference

### Common Development Setup

```bash
# Minimal development setup
export PYTHONPATH=/Users/xian/Development/piper-morgan
export ENABLE_ETHICS_ENFORCEMENT=false  # Start disabled

# With integrations
export GITHUB_TOKEN="ghp_..."
export GOOGLE_CALENDAR_ID="calendar@group.calendar.google.com"
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_APP_TOKEN="xapp-..."
export SLACK_SIGNING_SECRET="..."
export NOTION_API_KEY="secret_..."

# Start server
python -m uvicorn web.app:app --port 8001 --reload
```

### Production Setup

```bash
# Production environment variables
export ENABLE_ETHICS_ENFORCEMENT=true  # Enable ethics
export LOG_LEVEL=INFO
export PORT=8001
export DATABASE_URL="postgresql://piper:${DB_PASSWORD}@db:5433/piper_morgan"

# Integration tokens (from secure storage)
export GITHUB_TOKEN="${GITHUB_TOKEN}"
export SLACK_BOT_TOKEN="${SLACK_BOT_TOKEN}"
# ... etc

# Start server
python -m uvicorn web.app:app --port 8001 --workers 4
```

### Testing Setup

```bash
# Test with ethics enabled
export ENABLE_ETHICS_ENFORCEMENT=true
export PYTHONPATH=/Users/xian/Development/piper-morgan
pytest tests/ethics/ -v

# Test specific integration
export SLACK_BOT_TOKEN="test_token"
export SLACK_DEFAULT_CHANNEL="testing"
pytest tests/integrations/test_slack.py -v
```

---

## Security Notes

### Sensitive Variables

The following variables contain sensitive data and should **NEVER** be committed to version control:

- `SLACK_BOT_TOKEN`
- `SLACK_APP_TOKEN`
- `SLACK_SIGNING_SECRET`
- `GITHUB_TOKEN`
- `NOTION_API_KEY`
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`
- `PERPLEXITY_API_KEY`
- `DATABASE_URL` (if contains password)

**Storage**: Use `.env` files (gitignored) or secure secret management systems

**Keychain**: LLM provider keys are stored in system keychain for additional security

---

## Troubleshooting

### Variable Not Taking Effect

**Problem**: Changed environment variable but application still uses old value

**Solution**:
```bash
# Verify variable is set
echo $ENABLE_ETHICS_ENFORCEMENT

# Restart application
kill <pid>
python -m uvicorn web.app:app --port 8001
```

### Integration Configuration Missing

**Problem**: Integration shows as "missing" or "invalid"

**Solution**:
1. Check variable is set: `echo $SLACK_BOT_TOKEN`
2. Verify format: Slack tokens start with `xoxb-`
3. Check server logs for configuration errors
4. Restart application after setting variables

---

## See Also

- **Ethics Architecture**: `docs/internal/architecture/current/ethics-architecture.md`
- **Configuration Management**: `docs/piper-education/frameworks/emergent/configuration-management-framework.md`
- **Feature Flags**: `services/infrastructure/config/feature_flags.py`
- **Integration Setup**: `config/PIPER.user.md`

---

**Maintained by**: DevOps / Infrastructure Team
**Created**: October 18, 2025
**Last Review**: October 18, 2025
