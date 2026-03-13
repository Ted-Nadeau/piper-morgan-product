# Prompt for Code Agent: GREAT-4B Phase 0 - Baseline Intent Mapping

## Your Identity
You are Claude Code, starting Phase 0 work on GREAT-4B after completing GREAT-4A validation.

## Context from Phase -1

Infrastructure discovery confirms:
- `/api/v1/intent` endpoint exists and operational
- Slack has 375 intent references (heavy usage)
- CLI standup command uses intent
- Infrastructure ~95% built, need to verify no bypasses

**Your task: Map which entry points DON'T use intent yet.**

## Session Log Management

Create session log at: `dev/2025/10/05/2025-10-05-1540-prog-code-log.md`

## Mission

**Create comprehensive baseline map** showing which routes/commands use intent vs bypass, establishing 100% enforcement target.

---

## Phase 0: Baseline Mapping

### Step 1: Map Web Routes

Create script: `dev/2025/10/05/map_web_routes.py`

```python
import re
from pathlib import Path

def map_web_routes():
    """Map all web routes and their intent usage."""

    routes = {
        'using_intent': [],
        'bypassing_intent': [],
        'unclear': []
    }

    # Find all route definitions
    web_files = Path('web').glob('**/*.py')

    for file in web_files:
        content = file.read_text()

        # Find @app.* or @router.* decorators
        route_pattern = r'@(?:app|router)\.(get|post|put|delete|patch)\(["\']([^"\']+)'

        for match in re.finditer(route_pattern, content):
            method = match.group(1)
            path = match.group(2)

            # Check if route code uses intent
            # Look for "intent" in next 50 lines after decorator
            route_start = match.end()
            next_lines = content[route_start:route_start+2000]

            uses_intent = 'intent' in next_lines.lower()

            route_info = {
                'file': str(file),
                'method': method.upper(),
                'path': path,
                'uses_intent': uses_intent
            }

            if uses_intent:
                routes['using_intent'].append(route_info)
            else:
                routes['bypassing_intent'].append(route_info)

    return routes

if __name__ == "__main__":
    routes = map_web_routes()

    print("WEB ROUTES BASELINE")
    print("=" * 80)
    print(f"Using Intent: {len(routes['using_intent'])}")
    print(f"Bypassing:    {len(routes['bypassing_intent'])}")
    print(f"Total:        {len(routes['using_intent']) + len(routes['bypassing_intent'])}")

    if routes['bypassing_intent']:
        print("\nBYPASSING ROUTES:")
        for r in routes['bypassing_intent']:
            print(f"  {r['method']:6} {r['path']:40} ({r['file']})")
```

**Run and capture output.**

### Step 2: Map CLI Commands

Create script: `dev/2025/10/05/map_cli_commands.py`

```python
from pathlib import Path
import ast

def map_cli_commands():
    """Map all CLI commands and their intent usage."""

    commands = {
        'using_intent': [],
        'bypassing_intent': []
    }

    cli_dir = Path('cli/commands')
    if not cli_dir.exists():
        print("CLI commands directory not found")
        return commands

    for file in cli_dir.glob('*.py'):
        if file.name == '__init__.py':
            continue

        content = file.read_text()

        # Check for intent/Intent imports or usage
        uses_intent = (
            'intent' in content.lower() or
            'CanonicalHandlers' in content or
            'IntentService' in content
        )

        command_info = {
            'file': file.name,
            'uses_intent': uses_intent
        }

        if uses_intent:
            commands['using_intent'].append(command_info)
        else:
            commands['bypassing_intent'].append(command_info)

    return commands

if __name__ == "__main__":
    commands = map_cli_commands()

    print("\nCLI COMMANDS BASELINE")
    print("=" * 80)
    print(f"Using Intent: {len(commands['using_intent'])}")
    print(f"Bypassing:    {len(commands['bypassing_intent'])}")
    print(f"Total:        {len(commands['using_intent']) + len(commands['bypassing_intent'])}")

    if commands['bypassing_intent']:
        print("\nBYPASSING COMMANDS:")
        for c in commands['bypassing_intent']:
            print(f"  {c['file']}")
```

**Run and capture output.**

### Step 3: Verify Slack Integration

```bash
# Check if Slack uses intent universally
grep -r "def.*event\|@slack" services/integrations/slack/ --include="*.py" | wc -l

# Check how many mention intent
grep -r "intent" services/integrations/slack/ --include="*.py" | wc -l

# Calculate ratio
```

### Step 4: Create Baseline Report

Create: `dev/2025/10/05/intent-baseline-report.md`

```markdown
# Intent Classification Baseline - GREAT-4B Phase 0

**Date**: October 5, 2025
**Measured By**: Code Agent

## Current State

### Web Routes
- **Total Routes**: X
- **Using Intent**: Y (Z%)
- **Bypassing Intent**: N (M%)

**Bypassing Routes** (need conversion):
1. [METHOD] /path/to/route (file.py)
2. ...

### CLI Commands
- **Total Commands**: X
- **Using Intent**: Y (Z%)
- **Bypassing Intent**: N (M%)

**Bypassing Commands** (need conversion):
1. command_name.py
2. ...

### Slack Integration
- **Total Handlers**: 103
- **Intent References**: 375
- **Estimated Coverage**: ~100% (based on high reference count)

### Overall Metrics
- **Total Entry Points**: 123
- **Using Intent**: ~X (Y%)
- **Bypassing Intent**: ~N (M%)
- **Target**: 100%

## Bypass Analysis

For each bypass, document:
- **Route/Command**: Name
- **Reason**: Why it bypasses (if discoverable from code comments)
- **Effort**: Small/Medium/Large to convert
- **Priority**: High/Medium/Low

## Recommendations

Based on baseline:
1. Convert N web routes to use intent
2. Convert M CLI commands to use intent
3. Verify Slack coverage is truly 100%
4. Create bypass detection tests
```

---

## Success Criteria

- [ ] Web routes mapped (show counts)
- [ ] CLI commands mapped (show counts)
- [ ] Slack coverage verified
- [ ] Baseline report created with evidence
- [ ] Bypass list identified
- [ ] GitHub #206 updated with baseline

---

## Deliverables

1. **Scripts**: `map_web_routes.py`, `map_cli_commands.py`
2. **Baseline Report**: `intent-baseline-report.md`
3. **Evidence**: Terminal outputs from both scripts
4. **GitHub Update**: Issue with baseline metrics

---

## Evidence Format

```bash
$ python3 dev/2025/10/05/map_web_routes.py
WEB ROUTES BASELINE
================================================================================
Using Intent: 8
Bypassing:    3
Total:        11

BYPASSING ROUTES:
  POST   /api/github/create_issue                  (web/routes/github.py)
  GET    /api/health                               (web/app.py)
  GET    /docs                                     (web/app.py)

$ python3 dev/2025/10/05/map_cli_commands.py
CLI COMMANDS BASELINE
================================================================================
Using Intent: 1
Bypassing:    8
Total:        9

BYPASSING COMMANDS:
  create.py
  query.py
  ...
```

---

**Remember**: This is baseline measurement only - NO code changes yet. Just mapping what exists vs what needs conversion.

---

*Template Version: 9.0*
*Task: Baseline Mapping for GREAT-4B Phase 0*
*Estimated Effort: Small (30-45 minutes)*
