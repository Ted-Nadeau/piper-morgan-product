# Test-Driven Development Requirements - MANDATORY

## Every Change Requires TDD

### For Code Changes
```bash
# 1. Find relevant tests
find . -name "*test*.py" | grep -i [feature]

# 2. Write failing test
# 3. Run test - MUST see failure
pytest path/to/test.py::test_name -xvs

# 4. Implement minimal fix
# 5. Run test - MUST see success
# 6. Run related tests - MUST all pass
```

### For Documentation Changes
```bash
# 1. Test current state
python -m http.server 8000 --directory docs/
# Navigate to localhost:8000 and verify

# 2. Make change
# 3. Test new state
# 4. Verify change appears correctly
```

### For Bug Fixes
1. Write test that reproduces bug
2. Verify test fails for RIGHT reason
3. Fix bug with minimal change
4. Verify test passes
5. Verify no regressions

## TDD Violations That Break Excellence
- ❌ Writing code before test
- ❌ Not seeing test fail first
- ❌ Implementing more than needed
- ❌ Not verifying the fix works
- ❌ Skipping tests "just this once"
