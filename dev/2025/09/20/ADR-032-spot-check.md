# ADR-032 Spot Check: Intent Classification Universal Entry

## Quick Assessment

**ADR Title**: Intent Classification Universal Entry
**Status in ADR**: Unknown (need to check)
**Actual Status**: Likely incomplete based on pattern
**Critical for**: CORE-GREAT-1 and CORE-GREAT-4

---

## What ADR-032 Claims

Based on its title and number, ADR-032 should establish:
1. Intent classification as the universal entry point for all user interactions
2. No bypasses allowed - every interaction goes through intent
3. Consistent experience across all interfaces (Web, CLI, API, Slack)

---

## Evidence to Check (Commands for Lead Developer)

### 1. Check if Intent is Actually Universal

```bash
# Find all API endpoints that don't go through intent
grep -r "@app\.(get\|post\|put\|delete)" web/ --include="*.py" | grep -v intent

# Check if CLI commands use intent
grep -r "def execute" cli/commands/ --include="*.py" -A 5 | grep -v intent

# Find direct service calls bypassing intent
grep -r "github_service\|slack_service\|notion_service" web/ cli/ --include="*.py" | grep -v intent
```

### 2. Check Current Intent Usage

```bash
# Count how many places actually use intent classification
grep -r "intent.*classif\|classify.*intent" . --include="*.py" | wc -l

# Find the intent classifier implementation
find . -name "*intent*.py" -type f | xargs ls -la

# Check if OrchestrationEngine uses intent
grep -r "intent" services/orchestration/ --include="*.py"
```

### 3. Check for Bypass Routes

```bash
# Look for direct endpoint handlers
grep -r "def.*handle\|def.*process" web/ --include="*.py" | grep -v intent

# Check for TODO comments about intent
grep -r "TODO.*intent\|FIXME.*intent" . --include="*.py"

# Find workarounds mentioning intent
grep -r "workaround\|bypass\|skip.*intent" . --include="*.py" -i
```

---

## Red Flags to Watch For

### Pattern 1: Dual Routes
If you find both:
- `/api/intent/process` endpoint
- `/api/github/create_issue` endpoint

This means intent is optional, not universal.

### Pattern 2: Mixed Patterns in Same File
```python
# Red flag example
@app.post("/api/intent")  # Intent route
async def process_intent()...

@app.post("/api/github/create")  # Direct route (bypass!)
async def create_issue()...
```

### Pattern 3: Conditional Intent
```python
# Red flag example
if use_intent:  # Intent should not be optional!
    result = intent_classifier.classify(message)
else:
    result = direct_handler(message)
```

---

## Expected Findings

Based on the pattern of 75% complete work:

1. **Intent classifier exists and works** ✅
   - Likely in `services/intent_service/`
   - Probably handles basic classification

2. **Some endpoints use intent** 🟡
   - Chat interface might use it
   - Some CLI commands might use it

3. **But bypasses exist** ❌
   - Direct API endpoints still accessible
   - Some CLI commands skip intent
   - Slack might have direct handlers
   - Admin/debug routes bypass intent

4. **Not enforced universally** ❌
   - No CI check for intent coverage
   - No tests validating universal usage
   - No monitoring of bypass attempts

---

## Impact on CORE-GREAT Epics

### CORE-GREAT-1 (Orchestration Core)
- Need to ensure QueryRouter connects to intent
- OrchestrationEngine must require intent classification
- Cannot have direct routes to orchestration

### CORE-GREAT-4 (Intent Universalization)
- This is where we complete what ADR-032 intended
- Remove all bypasses found in this spot check
- Add enforcement mechanisms

---

## Verification Script for Lead Developer

Create a file `check_intent_universal.py`:

```python
#!/usr/bin/env python3
"""Check if intent classification is truly universal"""

import os
import re
from pathlib import Path

def find_bypasses():
    """Find all routes that bypass intent classification"""

    bypasses = []

    # Check web endpoints
    web_files = Path("web").rglob("*.py")
    for file in web_files:
        content = file.read_text()
        # Find routes that don't mention intent
        routes = re.findall(r'@app\.(get|post|put|delete)\("([^"]+)"\)', content)
        for method, route in routes:
            if 'intent' not in route.lower() and 'intent' not in content[max(0, content.find(route)-200):content.find(route)+200]:
                bypasses.append(f"Web bypass: {method.upper()} {route} in {file}")

    # Check CLI commands
    cli_files = Path("cli/commands").rglob("*.py")
    for file in cli_files:
        content = file.read_text()
        if 'def execute' in content and 'intent' not in content:
            bypasses.append(f"CLI bypass: {file}")

    # Check for direct service calls
    all_files = Path(".").rglob("*.py")
    for file in all_files:
        if 'test' in str(file):
            continue
        content = file.read_text()
        if re.search(r'(github|slack|notion)_service\.\w+\(', content):
            if 'intent' not in content:
                bypasses.append(f"Direct service call: {file}")

    return bypasses

if __name__ == "__main__":
    print("Checking for intent classification bypasses...")
    bypasses = find_bypasses()

    if bypasses:
        print(f"\n❌ Found {len(bypasses)} potential bypasses:\n")
        for bypass in bypasses:
            print(f"  - {bypass}")
        print(f"\nADR-032 is NOT fully implemented!")
    else:
        print("\n✅ No bypasses found - ADR-032 might be complete!")

    print(f"\nRecommendation: Run manual verification commands to confirm.")
```

---

## Summary

**ADR-032 Status**: Almost certainly incomplete

**Evidence Pattern**:
- Title suggests universal intent requirement
- System has bypasses (based on CORE-GREAT-4 being needed)
- Likely 50-75% implemented (pattern matches other incomplete work)

**Action Items**:
1. Run verification commands to confirm
2. Document actual state in CORE-GREAT-1 pre-work
3. Complete implementation in CORE-GREAT-4
4. Update ADR-032 with reality after CORE-GREAT-4

**The pattern continues**: Good decision, partial implementation, workarounds added, never completed.

---

*Spot check complete - Ready for Lead Developer audit tomorrow* 🐛
