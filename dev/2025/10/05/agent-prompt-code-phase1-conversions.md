# Prompt for Code Agent: GREAT-4B Phase 1 - High Priority Conversions

## Context from Phase 0

Baseline established:
- 16 high/medium priority bypasses
- 5 high priority: 4 CLI commands + 1 web route
- Slack is 100% compliant - use as conversion template
- Target: Convert high priority bypasses first

## Session Log

Continue: `dev/2025/10/05/2025-10-05-1540-prog-code-log.md`

## Mission

**Convert 5 high-priority bypasses** to use intent classification, following Slack's proven pattern.

---

## Phase 1: High Priority Conversions

### Step 1: Analyze Slack Pattern (Template)

```bash
# Study how Slack does intent universally
grep -A 20 "def.*handle.*event" services/integrations/slack/event_handler.py | head -50

# Find the pattern
grep -B 5 -A 10 "intent" services/integrations/slack/event_handler.py | head -30
```

**Document the pattern**: How does Slack intercept ALL events and route through intent?

### Step 2: Convert CLI Commands (4 high priority)

From baseline: cal, documents, issues, notion commands bypass intent.

**For EACH command:**

1. **Backup first**
```bash
cp cli/commands/[command].py cli/commands/[command].py.backup
```

2. **Add intent imports**
```python
from services.intent_service.canonical_handlers import CanonicalHandlers
# or
from services.intent_service import classifier
```

3. **Wrap execution in intent**
```python
async def execute(self, *args, **kwargs):
    # Convert command to natural language
    user_input = self._to_natural_language(*args, **kwargs)

    # Classify intent
    intent = await classifier.classify(user_input)

    # Route through canonical handlers
    handlers = CanonicalHandlers()
    result = await handlers.handle(intent, session_id="cli")

    return result
```

4. **Test the conversion**
```bash
python3 -m cli.commands.[command] --test
# Verify intent classification happens
```

5. **Run bypass detection**
```bash
pytest tests/intent/test_no_cli_bypasses.py -v -k "[command]"
# Should pass after conversion
```

**Commands to convert:**
- `cli/commands/cal.py`
- `cli/commands/documents.py`
- `cli/commands/issues.py`
- `cli/commands/notion.py`

### Step 3: Convert High Priority Web Route

From baseline: 1 high priority web route needs conversion.

**Check baseline report for which route**, then:

1. **Backup**
```bash
cp web/[file].py web/[file].py.backup
```

2. **Redirect to intent endpoint**
```python
# Before (direct service call):
@app.post("/api/github/create_issue")
async def create_issue(request: IssueRequest):
    result = await github_service.create_issue(...)
    return result

# After (through intent):
@app.post("/api/github/create_issue")
async def create_issue(request: IssueRequest):
    # Redirect to universal intent endpoint
    intent_request = {
        "text": f"Create GitHub issue: {request.title}"
    }
    return await process_intent(intent_request)
```

3. **Or remove route entirely** if `/api/v1/intent` handles it
```python
# Delete the route - force clients to use /api/v1/intent
```

4. **Test**
```bash
curl -X POST http://localhost:8001/api/github/create_issue -d '{"title":"test"}'
# Should return 404 or redirect properly
```

### Step 4: Verify with Detection Suite

```bash
# Run ALL bypass detection tests
pytest tests/intent/test_no_*_bypasses.py -v

# Run automated scanner
python3 scripts/scan_for_bypasses.py

# Both should show reduced bypass count
```

### Step 5: Update Baseline Report

```markdown
## Phase 1 Conversion Results

### Before
- High Priority Bypasses: 5
- CLI using intent: 12.5% (1/8)
- Web using intent: 18.2% (2/11)

### After
- High Priority Bypasses: 0 ✅
- CLI using intent: 62.5% (5/8)
- Web using intent: 27.3% (3/11)

### Remaining Work
- Medium Priority: 6 bypasses
- Low Priority: 5 (exclusions)
```

---

## Success Criteria

- [ ] Slack pattern documented
- [ ] 4 CLI commands converted
- [ ] 1 web route converted
- [ ] All conversions tested
- [ ] Bypass detection passes for converted items
- [ ] Baseline report updated
- [ ] Git commits for each conversion

---

## Evidence Format

```bash
$ pytest tests/intent/test_no_cli_bypasses.py::test_all_commands_import_intent -v
PASSED tests/intent/test_no_cli_bypasses.py::test_all_commands_import_intent

$ python3 scripts/scan_for_bypasses.py
⚠️  FOUND 11 POTENTIAL BYPASSES (reduced from 20)

$ git log --oneline -5
abc1234 Convert notion CLI command to use intent
def5678 Convert issues CLI command to use intent
...
```

---

*Estimated: 2-3 hours for 5 conversions*
