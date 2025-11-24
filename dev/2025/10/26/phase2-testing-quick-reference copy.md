# Phase 2 Testing - Quick Reference Card

**Generated From**: Code's archaeological investigation
**Date**: Sunday, October 26, 2025
**Purpose**: One-page command reference for E2E testing

---

## Essential Commands

### System Operations

**Start System**:
```bash
python main.py
# Starts web server on localhost:8001
# Location: main.py line 25
```

**Check Health**:
```bash
python main.py status
# Verifies services, database, external connections
# Location: main.py lines 178-209
```

**Database Status**:
```bash
psql -h localhost -p 5433 -U postgres -d piper_morgan
# PostgreSQL on port 5433 (NOT 5432)
```

**Service Status**:
```bash
# Check web server
curl http://localhost:8001/health

# Check database
psql -h localhost -p 5433 -U postgres -c "SELECT 1"
```

---

## User Management

### Test Users

**Create Alpha User** (alex-alpha):
```bash
# Via setup wizard (interactive)
python main.py setup

# Via Python/ORM
from services.database.models import AlphaUser
user = AlphaUser(username="alex-alpha", email="alex@test.com")

# Via migrations (automatic from personality_profiles)
# Already created during database setup
```

**Power User** (pat-power):
```bash
# Same methods as alex-alpha
# Create with advanced preferences
```

**Edge Case User** (eve-edge):
```bash
# Same methods, for destructive testing
```

### User Context

**Set User**:
```bash
# Via JWT token in HTTP headers
# Authentication: Bearer <jwt_token>

# JWT contains user_id claim
# Middleware: services/auth/auth_middleware.py
```

**Switch User**:
```bash
# Generate new JWT for different user
# Or use different auth token
```

---

## Core Features (MUST WORK)

### Onboarding

**Setup Wizard**:
```bash
python main.py setup
# Location: main.py lines 53-104
# Status: ✅ READY (Issue #218)
```

**First Run**:
```bash
python main.py
# Starts web server on localhost:8001
```

### API Keys

**Add Key**:
```bash
# Interactive via setup wizard
python main.py setup
# Then follow prompts for API keys

# Service: services/security/api_key_validator.py
# Status: ✅ READY (Issue #268)
```

**List Keys**:
```bash
# Query database
psql -h localhost -p 5433 -U postgres -d piper_morgan
# SELECT * FROM user_api_keys WHERE user_id='your_user_id';
```

**Validate Key**:
```bash
# Automatic during setup
# Uses KeyValidator, KeyStrengthAnalyzer, KeyLeakDetector
```

### Chat

**Basic Chat**:
```bash
# Via web interface
# Open: http://localhost:8001
# Location: Web server in main.py
```

**Chat with Context**:
```bash
# Same as basic chat
# Context managed by OrchestrationEngine
```

---

## Sprint A8 Features (IF EXISTS)

### Preferences (#267, #269)

**Run Questionnaire**:
```bash
python main.py preferences
# Location: main.py lines 106-145
# Service: services/personality/personality_profile.py
# Status: ✅ READY - 650 lines of test code
```

**View Preferences**:
```bash
# Query database
psql -h localhost -p 5433 -U postgres -d piper_morgan
# SELECT preferences FROM alpha_users WHERE username='your_user';
```

**Test Preference Effect**:
```bash
# Via web interface
# Set preferences first, then chat
# Response tone should match preference settings
```

### Cost Tracking (#271)

**View Costs**:
```bash
# Query database (no CLI command found)
psql -h localhost -p 5433 -U postgres -d piper_morgan
# SELECT * FROM api_usage_logs ORDER BY timestamp DESC LIMIT 10;
# Location: services/analytics/api_usage_tracker.py
# Status: ✅ READY - 269 lines test code, 15 tests
```

**Cost by Date**:
```bash
# SQL query
# SELECT SUM(estimated_cost) FROM api_usage_logs WHERE DATE(timestamp) = CURRENT_DATE;
```

### Knowledge Graph (#278)

**Test Graph Reasoning**:
```bash
# From Chief Architect - via web interface
# Message 1: "I prefer morning meetings because I have more energy"
# Message 2: "When should we schedule the architecture review?"
# EXPECT: Second response suggests morning

# Location: services/knowledge/knowledge_graph_service.py
# Status: ✅ READY - 40/40 tests pass
```

**Graph Status**:
```bash
# Query database for graph nodes/edges
psql -h localhost -p 5433 -U postgres -d piper_morgan
# SELECT * FROM knowledge_nodes LIMIT 10;
# SELECT * FROM knowledge_edges LIMIT 10;
```

### Key Validation (#268)

**Test Invalid Key**:
```bash
# During setup wizard
# Enter: "invalid-key-12345"
# EXPECT: Format validation rejection with clear error
```

**Test Valid Key**:
```bash
# During setup wizard
# Enter valid format: sk-proj-... or sk-ant-...
# EXPECT: Validation passes, strength checked, stored
```

---

## Integrations (IF EXISTS)

### GitHub

**Status Check**:
```bash
# Requires: export GITHUB_TOKEN=<your_token>
# Location: services/integrations/github/
# Operations: 20+ (issues, repos, workflows, content)
# Status: ✅ READY - MCP + Spatial Router
```

**Test Query**:
```bash
# Via web interface
# Message: "Show me my GitHub issues"
# EXPECT: Issues listed
```

### Calendar

**Status Check**:
```bash
# Requires: export GOOGLE_APPLICATION_CREDENTIALS=<path>
# Location: services/integrations/calendar/
# Operations: 4+ (connect, events, create, update)
# Status: ✅ READY - Tool-based MCP Router
```

**Test Query**:
```bash
# Via web interface
# Message: "Check my calendar for tomorrow"
# EXPECT: Events listed
```

### Slack

**Status Check**:
```bash
# Requires: export SLACK_BOT_TOKEN=<your_token>
# Location: services/integrations/slack/
# Operations: 22 (9 API + 13 spatial intelligence)
# Status: ✅ READY - Direct Spatial Router
```

**Test Query**:
```bash
# Via web interface
# Message: "Post to Slack: test message"
# EXPECT: Message posted
```

### Notion

**Status Check**:
```bash
# Requires: export NOTION_API_KEY=<your_key>
# Location: services/integrations/notion/
# Operations: 22 (databases, pages, search, workspace)
# Status: ✅ READY - Tool-based MCP Router
```

**Test Query**:
```bash
# Via web interface
# Message: "Create Notion page: Test Page"
# EXPECT: Page created
```

---

## Testing Infrastructure

### Run Tests

**All Tests**:
```bash
pytest tests/ -xvs
```

**Specific Suite**:
```bash
pytest tests/integration/ -xvs
```

**With Coverage**:
```bash
pytest tests/ --cov=services --cov-report=html
```

### Integration Tests

**Preferences → Behavior**:
```bash
[ACTUAL COMMAND - from Code's report if exists]
```

**Cost → Database**:
```bash
[ACTUAL COMMAND - from Code's report if exists]
```

**Graph → Retrieval**:
```bash
[ACTUAL COMMAND - from Code's report if exists]
```

---

## Evidence Collection

### Screenshots
```bash
# macOS
Command+Shift+4

# Save to:
~/Desktop/piper-phase2-evidence/
```

### Terminal Output
```bash
# Capture command output
command 2>&1 | tee evidence-[test-name].log
```

### Timing
```bash
# Time a command
time python main.py [command]
```

---

## Troubleshooting

### System Won't Start
```bash
# Check logs
[ACTUAL COMMAND - from Code's report]

# Restart services
[ACTUAL COMMAND - from Code's report]

# Clear cache
[ACTUAL COMMAND - from Code's report]
```

### Database Issues
```bash
# Check connection
[ACTUAL COMMAND - from Code's report]

# Reset test data
[ACTUAL COMMAND - from Code's report]

# Run migrations
alembic upgrade head
```

### Integration Failures
```bash
# Check credentials
[ACTUAL COMMAND - from Code's report]

# Test connection
[ACTUAL COMMAND - from Code's report]

# View logs
[ACTUAL COMMAND - from Code's report]
```

---

## File Locations (from Code's Report)

**Main Entry**: main.py (lines 25-266)
**Setup Wizard**: main.py lines 53-104
**Status Check**: main.py lines 178-209
**Preferences**: main.py lines 106-145

**Key Validator**: services/security/api_key_validator.py
**Preferences**: services/personality/personality_profile.py
**Cost Tracker**: services/analytics/api_usage_tracker.py
**Knowledge Graph**: services/knowledge/knowledge_graph_service.py (779 lines)
**Learning Loop**: services/learning/query_learning_loop.py (909 lines)
**User Preferences**: services/domain/user_preference_manager.py (829 lines)

**Integrations**:
- GitHub: services/integrations/github/
- Slack: services/integrations/slack/
- Calendar: services/integrations/calendar/
- Notion: services/integrations/notion/

**Database Models**: services/database/models.py
- User: lines 53-106
- AlphaUser: lines 108-179

**Tests**:
- Integration: tests/integration/ (79 files)
- Fixtures: tests/conftest.py (447+ fixtures)

---

## Environment Variables

**Required**:
```bash
# For integrations
export GITHUB_TOKEN=<your_github_token>
export SLACK_BOT_TOKEN=<your_slack_token>
export GOOGLE_APPLICATION_CREDENTIALS=<path_to_credentials.json>
export NOTION_API_KEY=<your_notion_key>

# Database (default)
export DATABASE_URL=postgresql://postgres@localhost:5433/piper_morgan
```

**Optional**:
```bash
# LLM providers
export ANTHROPIC_API_KEY=<your_key>
export OPENAI_API_KEY=<your_key>
export GROQ_API_KEY=<your_key>
export GOOGLE_API_KEY=<your_key>
```

**Test Mode**:
```bash
# For testing without external services
export PIPER_ENV=test
export DATABASE_URL=postgresql://postgres@localhost:5433/piper_morgan_test
```

---

## Priority Tags Quick Reference

- **[MUST WORK]** - Alpha blocker if broken
- **[IF EXISTS]** - Try and document reality
- **[FUTURE]** - Skip, note absence

---

## Success Checklist

**Before Starting**:
- [ ] System running on port 8001
- [ ] Database connected
- [ ] Environment variables set
- [ ] Test users created (if needed)

**During Testing**:
- [ ] Capture all terminal output
- [ ] Screenshot each step
- [ ] Note timing for operations
- [ ] Document confusion points

**After Testing**:
- [ ] Bugs documented with evidence
- [ ] Test results summarized
- [ ] Known issues listed
- [ ] Go/no-go recommendation

---

*Quick Reference v1.0*
*Update with Code's actual findings*
*Print for testing session*
