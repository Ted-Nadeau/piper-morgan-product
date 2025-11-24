# test_api_key_validator.py Refactoring Plan
**Bead**: piper-morgan-36m
**Date**: 2025-11-19
**Status**: In Progress

## Problem Summary

368 lines of non-functional test code testing an API design that was never implemented.

### Old API (Tests Expect)
- Module-level convenience functions: `validate_api_key()`, `get_supported_providers()`, `get_provider_format_info()`
- ValidationResult as enum with constants: `INVALID_FORMAT`, `UNKNOWN_PROVIDER`, `SECURITY_RISK`, `RATE_LIMITED`
- ValidationReport with: `is_valid`, `errors`, `checks_performed`, `metadata`, `key_hash`, `validation_time`
- Features: Rate limiting, live API validation, security pattern matching

### Actual API (Current Implementation)
- Class-based: `APIKeyValidator().validate_api_key(provider, api_key, strict_mode=False)`
- ValidationResult as dataclass: `valid: bool, message: str, provider: str, warnings: List[str]`
- ValidationReport with: `overall_valid`, `format_valid`, `strength_acceptable`, `leak_safe`, `security_level`, `recommendations`, `warnings`, `api_key_preview`
- Features: Format validation, strength checking, leak detection

## Test Analysis (27 tests total)

### ❌ Delete (14 tests, ~187 lines)

**TestConvenienceFunctions** (3 tests)
- `test_validate_api_key_convenience` - function doesn't exist
- `test_get_supported_providers` - function doesn't exist
- `test_get_provider_format_info` - function doesn't exist

**TestValidationError** (1 test)
- `test_validation_error_creation` - class doesn't exist

**Rate Limiting Tests** (3 tests)
- `test_rate_limiting` - feature doesn't exist
- `test_skip_rate_limit` - feature doesn't exist
- `test_clear_rate_limits` - method doesn't exist

**Live API Validation Tests** (3 tests)
- `test_skip_api_check` - feature doesn't exist
- `test_api_validation_failure` - feature doesn't exist
- `test_api_validation_network_error` - feature doesn't exist

**Helper Method Tests** (4 tests)
- `test_format_patterns_loaded` - attribute doesn't exist
- `test_security_patterns_loaded` - attribute doesn't exist
- `test_key_hashing` - method doesn't exist
- `test_prefix_checking` - method doesn't exist
- `test_validation_stats` - method doesn't exist

### ✅ Refactor (8 tests, keep scenarios but rewrite assertions)

**Format Validation Tests** (4 tests)
- `test_validate_openai_key_valid_format` → Check `format_valid == True`
- `test_validate_openai_key_invalid_format` → Check `format_valid == False` and `warnings`
- `test_validate_anthropic_key_valid_format` → Check `format_valid == True`
- `test_validate_unknown_provider` → Check `provider` field behavior

**Security Tests** (2 tests)
- `test_security_validation_test_key` → Map to `leak_safe == False` or strength check
- `test_security_validation_leaked_key` → Map to `leak_safe == False`

**Integration Tests** (2 tests)
- `test_github_token_validation` → Test GitHub format validation
- `test_slack_token_validation` → Test Slack format validation

**Report Tests** (1 test)
- `test_validation_report_creation` → Update to use actual fields

### ➕ Add New Tests (for actual features)

**Strength Validation**
- Test `strength_acceptable` for weak keys
- Test `strength_result` contains strength analysis

**Security Level**
- Test `security_level` values: 'high', 'medium', 'low', 'critical'

**Strict Mode**
- Test `strict_mode=True` parameter

**Recommendations & Warnings**
- Test `recommendations` list populated correctly
- Test `warnings` list populated correctly

## Implementation Strategy

1. Create new test file with refactored tests
2. Keep old file as `test_api_key_validator.py.old` for reference
3. Run tests incrementally to verify each scenario
4. Delete old file once all tests passing
5. Update bead piper-morgan-36m with results

## Expected Outcome

- **Before**: 27 tests, all failing, 368 lines
- **After**: ~15 tests, all passing, ~200 lines
- **Reduction**: 44% fewer tests, 45% less code, 100% functional
