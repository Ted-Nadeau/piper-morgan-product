# Agent Prompt: Fix CI Pipeline - Add pytest

## Mission
Fix CI failures by adding missing pytest dependencies to requirements.txt. 2-minute surgical fix.

## Context from Diagnosis
**Root Cause**: pytest not in requirements.txt
**Error**: `/opt/hostedtoolcache/Python/3.11.13/x64/bin/python: No module named pytest`
**Impact**: CI pipeline failing, blocking Verification Phase

## Fix Tasks

### 1. Check Current requirements.txt
```bash
cd /Users/xian/Development/piper-morgan

# Show current state
grep -i pytest requirements.txt || echo "pytest not found"
```

### 2. Add pytest Dependencies
Add these lines to requirements.txt:
```
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

Place them in the testing/development dependencies section if one exists, otherwise add near the top.

### 3. Verify Addition
```bash
# Confirm addition
grep pytest requirements.txt

# Quick validation (optional, don't need to run full install)
cat requirements.txt | grep -A 2 -B 2 pytest
```

### 4. Git Commit
```bash
# Stage the change
git add requirements.txt

# Commit with clear message
git commit -m "[#187] Add pytest dependencies to fix CI pipeline

- Added pytest>=7.4.0
- Added pytest-asyncio>=0.21.0
- Fixes CI failures due to missing test framework"

# Show commit
git log -1 --oneline
```

## Evidence Requirements

```
Before:
[paste grep result showing pytest missing]

After:
[paste requirements.txt lines showing pytest added]

Commit:
[paste git commit hash and message]
```

## Success Criteria
- ✅ pytest>=7.4.0 added to requirements.txt
- ✅ pytest-asyncio>=0.21.0 added to requirements.txt
- ✅ Changes committed with clear message
- ✅ Ready for CI to pass on next run

## Time Box
2 minutes - this is a simple addition

Report completion with commit hash.
