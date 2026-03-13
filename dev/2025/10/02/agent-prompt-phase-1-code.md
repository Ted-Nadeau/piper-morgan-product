# Claude Code Agent Prompt: GREAT-3A Phase 1 - Config Artifact Investigation

## 🎯 CRITICAL CONTEXT FROM PHASE 0

**What We Learned**:
- ConfigValidator is production-ready (the tool works)
- ConfigValidator OUTPUT reveals code-level issues (refactoring artifacts)
- These are NOT missing environment variables
- These are dependency gaps from DDD refactoring work

**From GREAT-2D** (yesterday's work):
> "Configuration gaps likely result from DDD refactoring work rather than missing environmental setup. Original integrations were successfully built with proper API keys and OAuth contracts."

**Your Mission**: Find WHERE in the code these refactoring artifacts exist.

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase 1 work.

## Mission
**Phase 1 Investigation**: Trace ConfigValidator "missing" results to actual code-level dependency gaps.

## Context
- **GitHub Issue**: GREAT-3A (number TBD)
- **Current State**: ConfigValidator shows Slack/Notion "missing" but system works (standup runs)
- **Target State**: Identify specific code expecting config that doesn't arrive properly
- **Chief Architect Guidance**: "Use ConfigValidator output as diagnostic tool to trace actual code issues"

## Your Specific Investigation Tasks

### Task 1: Run ConfigValidator and Capture Output
**Objective**: Get the actual diagnostic data

```bash
cd ~/Development/piper-morgan

# Run validator with full output
python -m services.infrastructure.config.config_validator --all-services --verbose > /tmp/config_output.txt 2>&1
cat /tmp/config_output.txt

# Also check the validator implementation
cat services/infrastructure/config/config_validator.py | head -200

# Check what it's actually validating
grep -A 10 "_validate_slack" services/infrastructure/config/config_validator.py
grep -A 10 "_validate_notion" services/infrastructure/config/config_validator.py
```

**Document**:
- Exact error messages
- What the validator is checking for
- What it reports as "missing"

### Task 2: Trace Slack Integration Config Flow
**Objective**: Follow config from startup to actual service usage

```bash
# Find where Slack integration initializes
grep -r "SlackIntegrationRouter" services/ --include="*.py" -A 5

# Check how Slack services get config
find services/integrations/slack/ -name "*.py" -exec grep -l "config" {} \;

# Look for config initialization
grep -r "SLACK_BOT_TOKEN\|SLACK_APP_TOKEN" services/ --include="*.py"

# Check if there's a config_service for Slack
ls -la services/integrations/slack/config_service.py
cat services/integrations/slack/config_service.py | head -100

# Find initialization sequence
grep -A 20 "def __init__" services/integrations/slack/slack_integration_router.py
```

**Questions to Answer**:
- How does SlackIntegrationRouter get its config?
- Where does it expect config to come from?
- Is there a config_service.py that's supposed to provide it?
- Was the connection broken during refactoring?

### Task 3: Trace Notion Integration Config Flow
**Objective**: Same as Slack but for Notion

```bash
# Find where Notion integration initializes
grep -r "NotionIntegrationRouter" services/ --include="*.py" -A 5

# Check how Notion gets config
find services/integrations/notion/ -name "*.py" -exec grep -l "config" {} \;

# Look for API key usage
grep -r "NOTION_API_KEY" services/ --include="*.py"

# Check router initialization
grep -A 20 "def __init__" services/integrations/notion/notion_integration_router.py
```

**Questions to Answer**:
- How does NotionIntegrationRouter get its config?
- Is there a missing config_service?
- What changed during DDD refactoring?

### Task 4: Check Working Integrations (GitHub, Calendar)
**Objective**: Understand what "working" looks like

```bash
# GitHub config flow (this one validates ✅)
ls -la services/integrations/github/config_service.py
cat services/integrations/github/config_service.py | head -100
grep -A 20 "def __init__" services/integrations/github/github_integration_router.py

# Calendar config flow (this one validates ✅)
grep -A 20 "def __init__" services/integrations/calendar/calendar_integration_router.py
```

**Questions to Answer**:
- What do GitHub and Calendar do differently?
- Do they have config_service.py files that Slack/Notion lack?
- Is there a pattern we can replicate?

### Task 5: Check Startup Integration Sequence
**Objective**: See where config actually gets passed to services

```bash
# Check web/app.py startup
grep -A 30 "@asynccontextmanager" web/app.py
grep -A 30 "def lifespan" web/app.py

# Check main.py startup (if relevant)
grep -A 30 "def main" main.py

# Look for service initialization patterns
grep -r "IntegrationRouter()" services/ --include="*.py" -A 3
```

**Questions to Answer**:
- How do routers get instantiated at startup?
- Where should config be injected?
- Is the initialization sequence broken?

### Task 6: Identify Specific Gaps
**Objective**: Create concrete list of what's broken

Create a comparison table:
```
Integration | Has config_service? | Router gets config? | Validator status | Gap identified
----------- | ------------------- | ------------------- | ---------------- | --------------
GitHub      | [yes/no]           | [yes/no]           | ✅ valid         | [description]
Slack       | [yes/no]           | [yes/no]           | ❌ missing       | [description]
Notion      | [yes/no]           | [yes/no]           | ❌ missing       | [description]
Calendar    | [yes/no]           | [yes/no]           | ✅ valid         | [description]
```

## Evidence Requirements

### For EVERY Claim You Make:
- **"Config is missing at line X"** → Show the code expecting config
- **"Router doesn't receive config"** → Show __init__ signature and calls
- **"config_service.py missing"** → Show ls -la output
- **"Initialization broken"** → Show startup sequence with gap
- **"DDD refactoring changed Y"** → Show before/after if possible (git blame)

### Git Investigation
If you find patterns:
```bash
# Check when config patterns changed
git log --all --oneline --grep="config" -- services/integrations/slack/
git log --all --oneline --grep="DDD\|refactor" -- services/integrations/

# Check specific file history
git log --follow services/integrations/slack/slack_integration_router.py
```

## Deliverable

Create comprehensive findings document:
**`dev/2025/10/02/phase-1-code-config-artifact-findings.md`**

Include:
1. **ConfigValidator Output**: Full output with error messages
2. **Slack Config Flow Analysis**: How it should work vs how it is
3. **Notion Config Flow Analysis**: Same as Slack
4. **Working Integration Comparison**: What GitHub/Calendar do right
5. **Startup Sequence Analysis**: Where config injection happens (or doesn't)
6. **Specific Gaps Identified**: Concrete list with line numbers
7. **Recommended Fixes**: What needs to be changed/added

## STOP Conditions

Stop immediately if:
- ConfigValidator output doesn't match expectations
- No obvious gaps found (report that as finding)
- Services actually getting config properly (means issue is elsewhere)
- Security concerns discovered

## Time Estimate
Half a mango (~30-45 minutes for thorough investigation)

## Success Criteria
- [ ] ConfigValidator output documented with full context
- [ ] Slack config flow traced from startup to usage
- [ ] Notion config flow traced from startup to usage
- [ ] Working integrations (GitHub/Calendar) analyzed for comparison
- [ ] Startup sequence understood
- [ ] Specific gaps identified with line numbers
- [ ] Concrete fix recommendations provided
- [ ] Findings document created with comprehensive evidence

---

**Deploy this prompt to Claude Code at 1:45 PM**
**Coordinate with Cursor agent on integration repair planning**
