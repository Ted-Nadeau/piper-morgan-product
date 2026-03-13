# Integration Quick Reference

## At a Glance

All 4 integrations are fully functional and production-ready.

## Directory Structure

```
services/integrations/
├── github/                  # GitHub integration (MCP + Spatial)
│   ├── github_plugin.py
│   ├── github_integration_router.py
│   ├── config_service.py
│   ├── production_client.py
│   ├── content_generator.py
│   ├── issue_analyzer.py
│   └── test_pm0008.py
│
├── slack/                   # Slack integration (Direct Spatial)
│   ├── slack_plugin.py
│   ├── slack_integration_router.py
│   ├── slack_client.py
│   ├── spatial_adapter.py
│   ├── config_service.py
│   ├── event_handler.py
│   ├── webhook_router.py
│   ├── oauth_handler.py
│   ├── README.md
│   └── tests/ (10+ test files)
│
├── calendar/                # Google Calendar (Tool-based MCP)
│   ├── calendar_plugin.py
│   ├── calendar_integration_router.py
│   ├── config_service.py
│   └── __init__.py
│
├── notion/                  # Notion (Tool-based MCP)
│   ├── notion_plugin.py
│   ├── notion_integration_router.py
│   ├── config_service.py
│   ├── README.md
│   └── __init__.py
│
├── mcp/                     # MCP Adapters
│   ├── notion_adapter.py    # NotionMCPAdapter (22 methods)
│   └── gitbook_adapter.py
│
└── spatial_adapter.py       # Base spatial adapter
```

## Configuration

### GitHub
```bash
export GITHUB_TOKEN="ghp_xxxxx"
export GITHUB_DEFAULT_REPO="owner/repo"
```

### Slack
```bash
export SLACK_BOT_TOKEN="xoxb-xxxxx"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

### Calendar
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
export GOOGLE_CALENDAR_ID="primary"
```

### Notion
```bash
export NOTION_API_KEY="secret_xxxxx"
export NOTION_WORKSPACE_ID="workspace_id"
```

## Usage Examples

### GitHub
```python
from services.integrations.github.github_plugin import GitHubPlugin

plugin = GitHubPlugin()
await plugin.initialize()

router = plugin.integration_router
issues = await router.get_recent_issues()
```

### Slack
```python
from services.integrations.slack.slack_plugin import SlackPlugin

plugin = SlackPlugin()
await plugin.initialize()

router = plugin.integration_router
await router.send_message("general", "Hello!")
channels = await router.list_channels()
```

### Calendar
```python
from services.integrations.calendar.calendar_plugin import CalendarPlugin

plugin = CalendarPlugin()
await plugin.initialize()

router = plugin.integration_router
events = await router.get_todays_events()
```

### Notion
```python
from services.integrations.notion.notion_plugin import NotionPlugin

plugin = NotionPlugin()
await plugin.initialize()

router = plugin.integration_router
await router.connect()
databases = await router.list_databases()
```

## Testing

### GitHub Tests
```bash
pytest tests/ -k github -v
pytest services/integrations/github/test_pm0008.py -v
pytest tests/integration/test_github_integration_e2e.py -v
```

### Slack Tests
```bash
pytest tests/integration/test_slack_config_loading.py -v          # 36 tests
pytest tests/services/integrations/slack/test_slack_config.py -v  # 16 tests
pytest tests/ -k slack -v
```

### Calendar Tests
```bash
pytest tests/integration/test_calendar_config_loading.py -v
pytest tests/integration/test_calendar_integration.py -v
```

### Notion Tests
```bash
pytest tests/integration/test_notion_config_loading.py -v         # 19 tests
pytest tests/services/integrations/mcp/test_notion_adapter.py -v
pytest tests/features/test_notion_integration.py -v
```

## Architecture Comparison

| Aspect | GitHub | Slack | Calendar | Notion |
|--------|--------|-------|----------|--------|
| **Plugin Wrapper** | ✅ GitHubPlugin | ✅ SlackPlugin | ✅ CalendarPlugin | ✅ NotionPlugin |
| **Router** | ✅ GitHubIntegrationRouter | ✅ SlackIntegrationRouter | ✅ CalendarIntegrationRouter | ✅ NotionIntegrationRouter |
| **MCP Adapter** | ✅ GitHubMCPSpatialAdapter | ❌ N/A | ✅ GoogleCalendarMCPAdapter | ✅ NotionMCPAdapter |
| **Spatial Adapter** | ✅ Fallback | ✅ Primary | ✅ Included | ✅ Included |
| **Direct Spatial** | Fallback | Primary | N/A | N/A |
| **Feature Flags** | ✅ USE_MCP_GITHUB | ✅ USE_SPATIAL_SLACK | ✅ USE_SPATIAL_CALENDAR | ✅ USE_SPATIAL_NOTION |
| **Config Service** | ✅ GitHubConfigService | ✅ SlackConfigService | ✅ CalendarConfigService | ✅ NotionConfigService |
| **Operations Count** | 20+ | 22 | 4+ | 22 |
| **Test Count** | 4+ | 46+ | 8+ | 23+ |

## Key Methods by Integration

### GitHub Router
- `get_recent_issues()`
- `get_issue(issue_number)`
- `create_issue()`
- `update_issue()`
- `search_issues()`
- `get_repository_info()`
- `get_workflow_status()`

### Slack Router
- `send_message(channel, text)`
- `get_channel_info(channel)`
- `list_channels()`
- `get_user_info(user)`
- `list_users()`
- `test_auth()`
- `map_to_position()` (spatial)
- `get_spatial_adapter()` (spatial)

### Calendar Router
- `connect()`
- `test_connection()`
- `get_todays_events()`
- `get_events(start_date, end_date)`
- `create_event()`
- `update_event()`

### Notion Router
- `connect()`
- `test_connection()`
- `list_databases()`
- `get_database(database_id)`
- `query_database()`
- `get_page(page_id)`
- `create_page()`
- `update_page()`
- `search_notion()`
- `list_users()`

## Feature Flags

All integrations support runtime feature flags:

### Spatial Flags
- `USE_SPATIAL_GITHUB=true` (default) - Use MCP adapter
- `USE_SPATIAL_SLACK=true` (default) - Use direct spatial
- `USE_SPATIAL_CALENDAR=true` (default) - Use MCP adapter
- `USE_SPATIAL_NOTION=true` (default) - Use MCP adapter

### Legacy Flags
- `ALLOW_LEGACY_GITHUB=false` (default) - Disable legacy fallback
- `ALLOW_LEGACY_SLACK=false` (default) - Disable legacy fallback
- `ALLOW_LEGACY_CALENDAR=false` (default) - Disable legacy fallback
- `ALLOW_LEGACY_NOTION=false` (default) - Disable legacy fallback

## Configuration Priority

All integrations use 3-layer priority:

```
Environment Variables (HIGHEST)
         ↓
PIPER.user.md (MIDDLE)
         ↓
Hardcoded Defaults (LOWEST)
```

## Documentation

- **Full Report**: `dev/2025/10/26/integration-archaeology-investigation.md`
- **GitHub README**: `services/integrations/github/` (config_service.py docstrings)
- **Slack README**: `services/integrations/slack/README.md`
- **Calendar README**: `services/integrations/calendar/` (config_service.py docstrings)
- **Notion README**: `services/integrations/notion/README.md`
- **ADR-037**: Tool-based MCP Standardization (Calendar/Notion)
- **ADR-039**: Direct Spatial Architecture (Slack)
- **CORE-MCP-MIGRATION #198**: GitHub MCP migration documentation

## Orchestration

The `OrchestrationEngine` coordinates multiple integrations:

```python
from services.orchestration.engine import OrchestrationEngine

engine = OrchestrationEngine()
workflow = engine.create_workflow()
result = await engine.execute_workflow(workflow)
```

Workflows can combine multiple integrations for complex tasks.

---

**Last Updated**: October 26, 2025
**Investigation Status**: COMPLETE ✅
**All Integrations**: VERIFIED FUNCTIONAL
