# Claude Code Agent Prompt: GREAT-3A Phase 1B - Config Pattern Audit

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase 1B work.

## Mission
**Quick Audit**: Verify config pattern consistency across all 4 integrations (GitHub, Slack, Notion, Calendar).

## Context from Phase 1
- **Slack**: ✅ Uses service injection pattern (`config_service.py` + router accepts param)
- **Notion**: ❌ Uses static pattern (`config/notion_config.py`) - needs alignment
- **GitHub**: ❓ Has `config_service.py` but Phase 1 said "router doesn't use it"
- **Calendar**: ❓ Phase 1 said "direct env access" - verify actual pattern

## Chief Architect Decision
**All 4 integrations MUST use consistent service injection pattern** for plugin architecture. This is why we're fixing it now in GREAT-3A.

## Your Tasks

### Task 1: GitHub Config Pattern Verification
**Question**: Does GitHub router use service injection pattern?

```bash
cd ~/Development/piper-morgan

# Check if config_service exists
ls -la services/integrations/github/config_service.py

# Check router __init__ signature
grep -A 20 "def __init__" services/integrations/github/github_integration_router.py | head -25

# Check if router accepts config_service parameter
grep "config_service" services/integrations/github/github_integration_router.py -B 2 -A 5

# Check how router uses config (if at all)
grep "self.config" services/integrations/github/github_integration_router.py -A 3
```

**Document**:
- Does GitHub have service injection pattern? (Yes/No)
- If No: What pattern does it use instead?
- If Yes: Is it fully implemented or partial?

### Task 2: Calendar Config Pattern Verification
**Question**: Does Calendar router use service injection pattern?

```bash
# Check for config_service in Calendar
ls -la services/integrations/calendar/ | grep config

# Check router __init__ signature
grep -A 20 "def __init__" services/integrations/calendar/calendar_integration_router.py | head -25

# Check if router accepts config_service
grep "config_service" services/integrations/calendar/calendar_integration_router.py -B 2 -A 5

# Check GoogleCalendarMCPAdapter pattern
grep -A 30 "def __init__" services/mcp/consumer/google_calendar_adapter.py | head -35
grep "config" services/mcp/consumer/google_calendar_adapter.py | head -20
```

**Document**:
- Does Calendar have service injection pattern? (Yes/No)
- Where does Calendar get config? (env direct, static class, service?)
- Does it match Slack pattern or need alignment?

### Task 3: Pattern Comparison Table

Create table:
```
Integration | Has config_service.py? | Location | Router Accepts Config? | Pattern Type | Needs Alignment?
----------- | ---------------------- | -------- | ---------------------- | ------------ | ----------------
Slack       | ✅ Yes                | services/integrations/slack/ | ✅ Yes (param) | Service injection | ❌ No (reference)
Notion      | ❌ No                 | config/ (static) | ❌ No | Static utility | ✅ YES
GitHub      | [your finding]        | [location] | [yes/no] | [type] | [yes/no]
Calendar    | [your finding]        | [location] | [yes/no] | [type] | [yes/no]
```

### Task 4: Specific Alignment Recommendations

For each integration that needs alignment, specify:
- What files to create
- What signatures to change
- Pattern to follow (use Slack as reference)

## Deliverable

Create: `dev/2025/10/02/phase-1b-code-pattern-audit.md`

Include:
1. **GitHub Pattern Analysis**: Current state + alignment needed?
2. **Calendar Pattern Analysis**: Current state + alignment needed?
3. **Pattern Comparison Table**: All 4 integrations side-by-side
4. **Alignment Recommendations**: Specific changes for GitHub/Calendar if needed

## Time Estimate
15-20 minutes for complete audit

## Success Criteria
- [ ] GitHub config pattern verified
- [ ] Calendar config pattern verified
- [ ] Comparison table created
- [ ] Specific alignment recommendations provided
- [ ] Clear list of what needs fixing

---

**Deploy at 2:15 PM**
**Coordinate with Cursor on Notion implementation**
