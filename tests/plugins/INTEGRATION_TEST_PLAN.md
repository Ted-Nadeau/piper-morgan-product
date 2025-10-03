# Plugin Integration Test Plan

## Phase 3C Testing Strategy

When each plugin wrapper is created, run:

### 1. Interface Compliance

```bash
pytest tests/plugins/test_plugin_interface.py -v
```

### 2. Plugin-Specific Tests

**SlackPlugin**:

- Router provides Slack routes
- Config service integration
- Spatial adapter present
- Webhook handling capability

**NotionPlugin**:

- Router provides Notion routes
- MCP adapter integration
- Config service present

**GitHubPlugin**:

- Router provides GitHub routes
- Config service integration
- Standard interface methods

**CalendarPlugin**:

- Router provides Calendar routes
- MCP adapter integration
- OAuth handling

### 3. Full System Integration

After all 4 plugins created:

```bash
# Start app and verify plugins loaded
uvicorn web.app:app --port 8001

# Check plugin registry endpoint (if created)
curl http://localhost:8001/api/v1/plugins

# Verify all routes mounted correctly
curl http://localhost:8001/docs
```

## Success Criteria

- [ ] All interface compliance tests pass
- [ ] All 4 plugins validate successfully
- [ ] Plugin registry shows 4 plugins
- [ ] All plugin routes accessible
- [ ] No runtime errors on startup
