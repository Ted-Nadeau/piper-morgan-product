# Command Inventory: Piper Morgan

**Issue**: #551 ARCH-COMMANDS - Command Parity Across Interfaces
**Phase**: 1 (Deep Inventory)
**Created**: 2026-01-22
**Status**: Complete

---

## Executive Summary

| Interface | Command Count | Status |
|-----------|---------------|--------|
| CLI (argparse + Click) | 29 | Inventoried |
| Web Chat Patterns | 541+ patterns → ~20 intents | Inventoried |
| Slack Commands | 2 slash commands | Inventoried |
| URL Routes | 202 endpoints | Inventoried |

**Key Finding**: No unified command registry exists. Commands are scattered across 6 registration points with no single source of truth.

---

## Table of Contents

1. [CLI Commands](#cli-commands-inventory)
2. [Web Chat Patterns](#web-chat-patterns-inventory)
3. [Slack Commands](#slack-commands-inventory)
4. [URL Routes](#url-routes-inventory)
5. [Parity Matrix](#parity-matrix)
6. [Gap Classification](#gap-classification)
7. [Recommendations](#recommendations)

---

## CLI Commands Inventory

### Summary
- **main.py (argparse)**: 6 commands
- **cli/commands/ (Click)**: 8 modules with 23+ subcommands
- **Total**: ~29 CLI operations

### main.py (argparse) - Application Entry Point

| Command | Arguments | Options | Handler Location | Description |
|---------|-----------|---------|------------------|-------------|
| `setup` | - | - | `scripts/setup_wizard.py:run_setup_wizard` | Interactive setup wizard |
| `status` | - | - | `scripts/status_checker.py:run_status_check` | Check system health |
| `preferences` | - | - | `scripts/preferences_questionnaire.py:main` | Configure user preferences |
| `keys` | `add\|list\|validate` | `<provider>` | `services/config/llm_config_service.py` | Manage API keys |
| `rotate-key` | `<provider>` | - | `cli/commands/keys.py:rotate_key_interactive` | Key rotation workflow |
| `migrate-user` | - | - | (Not shown) | Migrate alpha user |
| **(default)** | - | `--verbose`, `--no-browser` | `main.py:main` | Start web server on 8001 |

### cli/commands/ (Click Modules)

#### standup.py
| Command | Options | Description |
|---------|---------|-------------|
| `standup` | `--format {cli,slack}`, `--slack`, `--github`, `--notion` | Morning standup generation |

#### issues.py
| Command | Subcommands | Description |
|---------|-------------|-------------|
| `issues` | `create`, `verify`, `sync`, `triage`, `status`, `patterns` | Issue management with PM numbers |

#### cal.py
| Command | Subcommands | Description |
|---------|-------------|-------------|
| `cal` | `today`, `temporal`, `health` | Calendar operations |

#### documents.py
| Command | Subcommands | Description |
|---------|-------------|-------------|
| `documents` | `decide`, `context`, `add`, `review`, `status` | Document management |

#### keys.py
| Command | Description |
|---------|-------------|
| `rotate-key` | Interactive key rotation |

#### personality.py
| Command | Subcommands | Description |
|---------|-------------|-------------|
| `personality` | `show`, `update` | Personality configuration |

#### publish.py
| Command | Options | Description |
|---------|---------|-------------|
| `publish` | `--to`, `--location`, `--database`, `--format` | Publish to Notion |

#### notion.py
| Command | Subcommands | Description |
|---------|-------------|-------------|
| `notion` | `status`, `search`, `pages`, `test`, `sync` | Notion integration |

### CLI Inconsistencies

| Issue | Location | Impact |
|-------|----------|--------|
| Framework mismatch | main.py (argparse) vs cli/commands/ (Click) | Medium |
| Duplicate functionality | `keys` in main.py and keys.py | Low |
| Entry point fragmentation | Multiple `main()` functions | Medium |
| Missing from __init__.py | Most command classes not exported | Low |

---

## Web Chat Patterns Inventory

### Summary
- **Pattern groups**: 17 total
- **Total regex patterns**: 541+
- **Canonical handlers**: 6
- **QUERY action handlers**: 14

### Pattern Groups

| # | Pattern Group | Category | Patterns | Handler |
|---|---------------|----------|----------|---------|
| 1 | GREETING_PATTERNS | CONVERSATION | 9 | _handle_conversation_query |
| 2 | FAREWELL_PATTERNS | CONVERSATION | 5 | _handle_conversation_query |
| 3 | THANKS_PATTERNS | CONVERSATION | 5 | _handle_conversation_query |
| 4 | IDENTITY_PATTERNS | IDENTITY | 18 | _handle_identity_query |
| 5 | TEMPORAL_PATTERNS | TEMPORAL | 66 | _handle_temporal_query |
| 6 | STATUS_PATTERNS | STATUS | 61 | _handle_status_query |
| 7 | CONTEXTUAL_QUERY_PATTERNS | QUERY | 7 | varies |
| 8 | CALENDAR_QUERY_PATTERNS | QUERY | 54 | _handle_meeting_time_query |
| 9 | GITHUB_QUERY_PATTERNS | QUERY | 26 | varies |
| 10 | PRODUCTIVITY_QUERY_PATTERNS | QUERY | 4 | _handle_productivity_query |
| 11 | TODO_QUERY_PATTERNS | QUERY | 8 | EXECUTION handler |
| 12 | DOCUMENT_QUERY_PATTERNS | QUERY | 9 | _handle_update_document_query |
| 13 | PRIORITY_PATTERNS | PRIORITY | 53 | _handle_priority_query |
| 14 | GUIDANCE_PATTERNS | GUIDANCE | 22 | _handle_guidance_query |
| 15 | FILE_REFERENCE_PATTERNS | (support) | 54 | detect_file_reference() |

### Canonical Handlers

| Handler | Category | Capabilities |
|---------|----------|--------------|
| _handle_identity_query | IDENTITY | Name, role, capabilities, help |
| _handle_temporal_query | TEMPORAL | Time, date, scheduling |
| _handle_status_query | STATUS | Project status, work progress |
| _handle_priority_query | PRIORITY | Top priorities, focus areas |
| _handle_guidance_query | GUIDANCE | Advice, recommendations, setup help |
| _handle_conversation_query | CONVERSATION | Greetings, farewells, thanks |

### QUERY Action Handlers (intent_service.py)

| Handler | Action | Purpose |
|---------|--------|---------|
| _handle_meeting_time_query | meeting_time | Calendar - time in meetings |
| _handle_week_calendar_query | week_calendar | Calendar - weekly view |
| _handle_recurring_meetings_query | recurring_meetings | Calendar - standing meetings |
| _handle_shipped_this_week | shipped_query | GitHub - shipped items |
| _handle_stale_prs | stale_prs_query | GitHub - PRs needing review |
| _handle_review_issue_query | review_issue_query | GitHub - issue analysis |
| _handle_close_issue_query | close_issue_query | GitHub - close issues |
| _handle_comment_issue_query | comment_issue_query | GitHub - issue comments |
| _handle_productivity_query | productivity_query | Metrics analysis |
| _handle_changes_query | changes_query | Change detection |
| _handle_attention_query | attention_query | Priority items |
| _handle_update_document_query | update_document_query | Notion mutations |
| _handle_standup_query | show_standup | Standup generation |
| _handle_projects_query | list_projects | Project listing |

### Pattern Architecture

```
User Message
    ↓
PreClassifier.pre_classify()
    ↓
Pattern Group Matching (priority order)
    ↓
Intent Generated (category + action)
    ↓
CanonicalHandlers.handle() OR QueryRouter
    ↓
Specific Handler Method
```

### Critical Pattern Ordering

1. CONTEXTUAL_QUERY before TEMPORAL (avoid collision)
2. CALENDAR_QUERY before TEMPORAL
3. GUIDANCE before STATUS

---

## Slack Commands Inventory

### Summary
- **Total slash commands**: 2
- **Registration**: Hardcoded in `_process_slash_command()`

### Direct Slash Commands

| Command | Handler | Response Type | Description |
|---------|---------|---------------|-------------|
| `/piper` | `_handle_piper_command()` | ephemeral | Help and capabilities |
| `/standup` | `_handle_standup_command()` | in_channel | Generate standup |

### /piper Subcommands

| Subcommand | Handler | Description |
|------------|---------|-------------|
| `help` | `_build_help_response()` | Show available commands |
| (empty) | `_build_help_response()` | Default to help |
| (unknown) | (warm response) | Direct to /piper help |

### /standup Response Format

Three-section structure:
- **Yesterday**: Completed items (max 3)
- **Today**: High-priority items (max 3)
- **Blockers**: Current blockers (max 2)

### Command Registration

| Aspect | Current State |
|--------|---------------|
| Registration method | Hardcoded |
| Command discovery | No |
| Help generation | Dynamic via CanonicalHandlers |

### Outstanding TODOs

- `_get_completed_since_yesterday()` - Needs TodoManagementService
- `_get_today_priorities()` - Needs TodoManagementService
- `_get_blockers()` - Needs blocker detection service

---

## URL Routes Inventory

### Summary
- **Total route modules**: 25
- **Total endpoints**: 202
- **Auth required**: 162
- **Optional auth**: 18
- **No auth**: 22

### Route Modules

| Module | Prefix | Endpoints | Purpose |
|--------|--------|-----------|---------|
| auth.py | /auth | 4 | Authentication |
| intent.py | /api/v1 | 2 | Intent processing |
| health.py | /api/v1/health | 3 | Health monitoring |
| todos.py | /api/v1/todos | 10 | Todo CRUD |
| lists.py | /api/v1/lists | 14 | List CRUD |
| projects.py | /api/v1/projects | 9 | Project CRUD |
| files.py | /api/v1/files | 5 | File management |
| conversations.py | /api/v1/conversations | 6 | Conversations |
| documents.py | /api/v1/documents | 6 | Document analysis |
| standup.py | /api/v1/standup | 4 | Standup generation |
| learning.py | /api/v1/learning | 25 | Pattern management |
| setup.py | /setup | 13 | Setup wizard |
| settings_integrations.py | /api/v1/settings/integrations | 33 | Integration settings |
| integrations.py | /api/v1/integrations | 3 | Integration health |
| admin.py | (no prefix) | 10 | Admin monitoring |
| api_keys.py | /api/v1/keys | 5 | API key management |
| preferences.py | /api/v1/preferences | 5 | User preferences |
| personality.py | /api/v1/personality | 3 | Personality profiles |
| feedback.py | /api/v1/feedback | 3 | Feedback collection |
| knowledge_graph.py | /api/v1/knowledge | 4 | Knowledge graph |
| ui.py | (no prefix) | 20 | HTML pages |
| conversation_context_demo.py | /conversation | 6 | Demo endpoints |
| loading_demo.py | /loading | 8 | Demo loading states |
| debug.py | (no prefix) | 1 | Debug utilities |

### Endpoints by Category

#### Authentication (4)
- POST /auth/login
- POST /auth/logout
- GET /auth/me
- POST /auth/change-password

#### Core Features (33)
- Todos: 10 endpoints (CRUD + sharing)
- Lists: 14 endpoints (CRUD + items + sharing)
- Projects: 9 endpoints (CRUD + sharing)

#### Integrations (52)
- Slack settings: 11 endpoints
- Calendar settings: 10 endpoints
- Notion settings: 6 endpoints
- GitHub settings: 6 endpoints
- Integration health: 3 endpoints

#### Standup (4)
- POST /api/v1/standup/generate
- GET /api/v1/standup/modes
- GET /api/v1/standup/formats
- GET /api/v1/standup/health

---

## Parity Matrix

### Core Commands

| Command | CLI | Web Chat | Slack | URL | Notes |
|---------|-----|----------|-------|-----|-------|
| standup | ✅ | ✅ | ✅ | ✅ | Full parity |
| calendar/today | ✅ | ✅ | ❌ | ❌ | Gap: Slack, URL |
| calendar/week | ✅ | ✅ | ❌ | ❌ | Gap: Slack, URL |
| todos/list | ❌ | ✅ | ❌ | ✅ | Gap: CLI, Slack |
| todos/create | ❌ | ❌ | ❌ | ✅ | Gap: CLI, Web, Slack |
| priorities | ❌ | ✅ | ❌ | ❌ | Gap: CLI, Slack, URL |
| status | ✅ | ✅ | ❌ | ❌ | Gap: Slack, URL |
| help | ❌ | ✅ | ✅ | ❌ | Gap: CLI, URL |
| issues/create | ✅ | ❌ | ❌ | ❌ | CLI only |
| documents | ✅ | ✅ | ❌ | ✅ | Gap: Slack |
| notion | ✅ | ❌ | ❌ | ✅ | Gap: Web, Slack |
| personality | ✅ | ❌ | ❌ | ✅ | Gap: Web, Slack |

### Legend
- ✅ Exists
- ❌ Gap
- ⚠️ Partial
- 🔄 Intentional difference

---

## Gap Classification

### Category A: True Gaps (Should Exist)

| Gap | Impact | Priority |
|-----|--------|----------|
| /calendar in Slack | High | P1 |
| /todo in Slack | High | P1 |
| /priorities in Slack | Medium | P2 |
| CLI help command | Low | P3 |

### Category B: Inconsistencies

| Inconsistency | Description | Resolution |
|---------------|-------------|------------|
| Framework mismatch | argparse vs Click | Standardize on Click |
| Entry points | Fragmented across modules | Unified `piper` command |
| Pattern ordering | Implicit, fragile | Document in Pattern Priority Matrix |

### Category C: Intentional Differences

| Difference | Reason |
|------------|--------|
| issues CLI-only | PM workflow, not user-facing |
| Admin endpoints URL-only | Security, no chat interface |
| OAuth callbacks URL-only | Technical requirement |

---

## Recommendations

### Phase 2: CommandRegistry Design

1. **Central Registry**: Single source of truth for all commands
2. **Interface Adapters**: CLI, Web, Slack, URL adapters query registry
3. **Dynamic Discovery**: `_get_slash_commands()` queries registry
4. **Metadata Schema**: Command name, description, interfaces, handler

### Phase 3: Implementation Priorities

1. **High Priority**: Close Slack gaps (/calendar, /todo)
2. **Medium Priority**: Unify CLI entry points
3. **Low Priority**: Document intentional differences

### Architecture Goals

- No hardcoded command lists
- Interface parity by default (gaps must be justified)
- Self-documenting command system
- Dynamic help generation from registry

---

## Appendix: Data Sources

- CLI: `main.py`, `cli/commands/*.py`
- Web Chat: `services/intent_service/pre_classifier.py`, `canonical_handlers.py`
- Slack: `services/integrations/slack/webhook_router.py`
- URL: `web/api/routes/*.py`

---

*Document generated: 2026-01-22*
*Phase 1 of Issue #551 ARCH-COMMANDS*
