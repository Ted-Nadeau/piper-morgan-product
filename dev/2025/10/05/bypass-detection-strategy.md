# Intent Bypass Detection Strategy

**Epic**: GREAT-4B - Intent Classification Universal Enforcement
**Phase**: Phase 0 - Bypass Detection Tests
**Date**: October 5, 2025
**Author**: Cursor Agent

---

## Purpose

Ensure 100% of user interactions go through intent classification.
Prevent regressions where new code bypasses intent layer.

---

## Test Types

### 1. Unit Tests (pytest)

**Location**: `tests/intent/`

- **`test_no_web_bypasses.py`** - Web route enforcement
  - Verifies `/api/v1/intent` endpoint exists
  - Ensures direct service endpoints return 404/403/405
  - Allows health/docs endpoints to bypass (explicitly permitted)
- **`test_no_cli_bypasses.py`** - CLI command enforcement
  - Checks all CLI commands reference intent system
  - Verifies imports of intent-related modules
  - Skips gracefully if CLI directory doesn't exist
- **`test_no_slack_bypasses.py`** - Slack handler enforcement
  - Ensures Slack event handlers use intent classification
  - Checks plugin references to intent system
  - Validates handler files contain intent references

### 2. Automated Scanner

**Location**: `scripts/scan_for_bypasses.py`

- **Static code analysis** for potential bypasses
- **Web route scanning**: Finds routes without intent references
- **CLI command scanning**: Identifies commands missing intent imports
- **Integration handler scanning**: Checks handler files for intent usage
- **Runs in CI** on every PR
- **Fails build** if bypasses detected

### 3. Integration Tests

- End-to-end flows verify intent usage
- User scenarios test full path
- Validates intent classification in real workflows

---

## Running Tests

### Local Testing

```bash
# Run all bypass detection tests
pytest tests/intent/test_no_*_bypasses.py -v

# Run automated scanner
python3 scripts/scan_for_bypasses.py

# Both should pass for GREAT-4B completion
```

### Expected Output

```bash
$ pytest tests/intent/test_no_web_bypasses.py -v
========================= test session starts =========================
tests/intent/test_no_web_bypasses.py::TestWebIntentEnforcement::test_intent_endpoint_exists PASSED
tests/intent/test_no_web_bypasses.py::TestWebIntentEnforcement::test_no_direct_github_access PASSED
tests/intent/test_no_web_bypasses.py::TestWebIntentEnforcement::test_no_direct_slack_access PASSED
tests/intent/test_no_web_bypasses.py::TestWebIntentEnforcement::test_no_direct_notion_access PASSED
tests/intent/test_no_web_bypasses.py::TestWebIntentEnforcement::test_no_direct_calendar_access PASSED
tests/intent/test_no_web_bypasses.py::TestWebIntentEnforcement::test_health_endpoint_allowed PASSED
tests/intent/test_no_web_bypasses.py::TestWebIntentEnforcement::test_docs_endpoint_allowed PASSED
========================= 7 passed in 0.45s =========================

$ python3 scripts/scan_for_bypasses.py
✅ NO BYPASSES DETECTED
```

---

## CI Integration

### GitHub Actions

Add to `.github/workflows/ci.yml`:

```yaml
- name: Scan for intent bypasses
  run: python3 scripts/scan_for_bypasses.py

- name: Run bypass detection tests
  run: pytest tests/intent/test_no_*_bypasses.py -v
```

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: scan-bypasses
      name: Scan for intent bypasses
      entry: python3 scripts/scan_for_bypasses.py
      language: system
      pass_filenames: false
```

---

## Bypass Categories

### Allowed Bypasses (Explicit Exceptions)

- **Health endpoints**: `/health`, `/metrics` - Infrastructure monitoring
- **Documentation**: `/docs`, `/openapi.json` - API documentation
- **Static assets**: CSS, JS, images - No business logic

### Prohibited Bypasses

- **Direct service calls**: `/api/github/*`, `/api/slack/*`, etc.
- **CLI commands**: All commands must use intent classification
- **Integration handlers**: Slack, webhooks must route through intent
- **API endpoints**: All business logic endpoints must use intent

---

## Detection Methods

### 1. Static Analysis

- **Regex pattern matching** for route definitions
- **Import analysis** for intent service usage
- **File content scanning** for intent references

### 2. Runtime Testing

- **HTTP request testing** to verify endpoint behavior
- **Mock testing** for CLI command validation
- **Integration testing** for handler verification

### 3. Code Structure Analysis

- **Directory scanning** for handler files
- **File naming conventions** to identify handlers
- **Content analysis** for intent system integration

---

## Maintenance

### Adding New Tests

1. **Identify new entry points** (routes, commands, handlers)
2. **Add detection logic** to appropriate test file
3. **Update scanner** if new patterns emerge
4. **Document exceptions** if bypass is intentional

### Updating Scanner

1. **Add new file patterns** to scan
2. **Update exemption lists** for allowed bypasses
3. **Enhance detection logic** for new bypass types
4. **Test scanner** against known bypasses

---

## Troubleshooting

### False Positives

- **Review exemption lists** in scanner
- **Check for indirect intent usage** (via handlers)
- **Verify intent reference patterns** are comprehensive

### False Negatives

- **Enhance detection patterns** in scanner
- **Add specific test cases** for missed bypasses
- **Review file naming conventions** for handlers

### Test Failures

- **Check infrastructure state** (directories exist, files present)
- **Verify test assumptions** about system structure
- **Update tests** if architecture changes

---

## Success Metrics

- **0 bypasses detected** by automated scanner
- **All tests passing** in bypass detection suite
- **CI pipeline green** with bypass checks enabled
- **No regressions** in future development

---

## Related Documentation

- **GREAT-4B Epic**: Complete universal enforcement plan
- **Pattern-028**: Intent Classification pattern
- **Pattern-032**: Intent Pattern Catalog
- **ADR-032**: Intent Classification Universal Entry

---

**Status**: ✅ Detection strategy documented and implemented
