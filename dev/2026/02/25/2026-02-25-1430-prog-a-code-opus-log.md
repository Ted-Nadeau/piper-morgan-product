# Session Log: Programmer Agent A
**Date**: 2026-02-25
**Role**: Programmer Agent (prog-A)
**Issue**: #849 -- SEC-KEYCHAIN: Route-level keychain fixes (Categories B+C+D+E)
**Branch**: claude/m0-conversational-glue

## Timeline

### 14:30 -- Pre-flight verification
- Confirmed all target files exist at expected paths
- Confirmed line numbers match prompt exactly (B1:1650, B2:1736, B3:1686, C1:478, C2:516, C3:1261, D1:440, D2:1365, E1:529, E2:548)
- Baseline test run: 99 tests pass (slack/github/notion routes)
- Pre-existing failure: test_demo_plugin.py::test_plugin_has_router (API prefix mismatch, unrelated)

### 14:31 -- Category B: GitHub token store/retrieve/delete
- B1 (line 1650): store_api_key now passes username=current_user.sub
- B2 (line 1736): get_api_key now passes username=current_user.sub (function already had current_user)
- B3 (line 1686): delete_api_key now passes username=current_user.sub
- Added current_user param to save_github_token and disconnect_github function signatures

### 14:31 -- Category C: Connection test endpoints
- C1: _test_slack now accepts user_id param, uses "slack_bot" key (was "slack"), passes username=user_id
- C2: _test_github now accepts user_id param, uses "github_token" key (was "github"), passes username=user_id
- C3: get_notion_settings now uses username=current_user.sub for keychain retrieval
- Updated _test_integration caller to pass user_id to slack/github
- Updated check_integration_connection to accept current_user and thread user_id
- Updated check_all_connections to accept current_user and pass it through
- Added Depends and auth imports to integrations.py

### 14:32 -- Category D: Disconnection fixes
- D1: disconnect_slack now deletes "slack_bot" AND "slack_user" with username=current_user.sub (was "slack_bot_token" without username)
- D2: disconnect_notion now deletes "notion" with username=current_user.sub

### 14:32 -- Category E: Slack OAuth handler store fix
- E1: Bot token now stored via store_api_key("slack_bot", token, username=user_id) instead of f-string key
- E2: User token now stored via store_api_key("slack_user", token, username=user_id) instead of f-string key

### 14:33 -- Test updates for existing tests
- Updated test_settings_github.py: Added mock_user to save/disconnect tests, updated assertions
- Updated test_settings_notion.py: Added mock_user to get_settings/disconnect tests, updated assertions
- Updated test_settings_slack.py: Added mock_user to disconnect tests
- Updated test_integrations.py: Added mock_user to check_integration_connection and check_all_connections tests

### 14:37 -- New tests created
- Created test_keychain_scoping_849.py with 13 tests across 4 test classes
- All 13 new tests pass
- All 134 existing+new route tests pass

## Files Modified
1. web/api/routes/settings_integrations.py (B1, B2, B3, C3, D1, D2)
2. web/api/routes/integrations.py (C1, C2, + caller updates)
3. services/integrations/slack/oauth_handler.py (E1, E2)
4. tests/unit/web/api/routes/test_settings_github.py (updated existing tests)
5. tests/unit/web/api/routes/test_settings_notion.py (updated existing tests)
6. tests/unit/web/api/routes/test_settings_slack.py (updated existing tests)
7. tests/unit/web/api/routes/test_integrations.py (updated existing tests)
8. tests/unit/web/api/routes/test_keychain_scoping_849.py (NEW - 13 tests)
