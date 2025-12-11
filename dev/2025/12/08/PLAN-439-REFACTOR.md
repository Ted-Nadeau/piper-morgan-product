# Plan: #439 ALPHA-SETUP-REFACTOR - Function Extraction

**Issue**: ALPHA-SETUP-REFACTOR: Function extraction for API key collection and wizard phases
**Status**: READY TO IMPLEMENT
**Estimated Time**: 3-4 hours
**Risk**: Low (refactoring, no behavior changes)

---

## Current State Analysis

### File Structure
- **File**: `scripts/setup_wizard.py` (1427 lines)
- **Functions**: 21 total
- **Main problem function**: `collect_and_validate_api_keys()` (406 lines, lines 682-1087)
- **Main orchestrator**: `run_setup_wizard()` (340 lines, lines 1088-1427)

### Duplication Patterns Identified

**API Key Collection - Same pattern repeated 4x**:
- OpenAI (lines 693-800): ~108 lines
- Anthropic (lines 801-893): ~93 lines
- Gemini (lines 894-1000): ~107 lines
- GitHub (lines 1001-1087): ~87 lines

**Pattern in each section**:
1. Check keychain for existing key (`retrieve_user_key`)
2. Check for global key migration (`_check_global_keychain_key`)
3. Check environment variable (`{PROVIDER}_API_KEY`)
4. Manual entry loop with validation
5. Store key with `store_user_key`

**Variation**: GitHub skips validation (`validate=False`) while others use `validate=True`

### Function Size Issues

**`run_setup_wizard()`** (340 lines) has these logical phases:
- Pre-flight checks (Python 3.12, venv, SSH) - ~60 lines
- Docker setup - ~120 lines
- System checks - ~80 lines
- User account creation - ~40 lines
- Final setup complete marking - ~40 lines

**`collect_and_validate_api_keys()`** (406 lines) should be split into:
- OpenAI section
- Anthropic section
- Gemini section
- GitHub section

---

## Refactoring Phases

### Phase 1: Extract API Key Helper (1.5 hours)

**Goal**: DRY out the repeated API key collection pattern

**New function**:
```python
async def _collect_single_api_key(
    user_id: str,
    service: UserAPIKeyService,
    provider: str,
    env_var_name: str,
    format_hint: str,
    validation_fn: Optional[Callable] = None,
    skip_validation: bool = False,
) -> Optional[str]:
    """
    Generic API key collection with keychain, env var, and manual entry.

    Args:
        user_id: User ID for keychain storage
        service: UserAPIKeyService instance
        provider: Provider name (openai, anthropic, gemini, github)
        env_var_name: Environment variable name (e.g., OPENAI_API_KEY)
        format_hint: Format hint for manual entry (e.g., sk-...)
        validation_fn: Custom validation function (optional)
        skip_validation: Skip validation during store (for GitHub)

    Returns:
        API key if successful, None if skipped
    """
    # 1. Check keychain
    # 2. Check env var
    # 3. Manual entry loop
    # 4. Store and validate
    # 5. Return key or None
```

**Acceptance Criteria for Phase 1**:
- [ ] `_collect_single_api_key()` created
- [ ] OpenAI section refactored to use helper
- [ ] Anthropic section refactored to use helper
- [ ] Gemini section refactored to use helper
- [ ] GitHub section refactored to use helper
- [ ] Tests still pass
- [ ] Manual test: `python main.py setup` (test one provider)

### Phase 2: Split Main Wizard Function (1.5 hours)

**Goal**: Break `run_setup_wizard()` into focused functions

**New functions**:
```python
async def _wizard_preflight_checks() -> bool:
    """Check Python 3.12, setup venv, SSH key"""
    # Pre-flight checks - ~60 lines

async def _wizard_docker_setup() -> bool:
    """Docker availability and service startup"""
    # Docker setup - ~120 lines

async def _wizard_system_checks() -> bool:
    """Database, Redis, ChromaDB, Temporal checks"""
    # System checks - ~80 lines

async def _wizard_user_account() -> str:
    """Create user account, return user_id"""
    # User creation - ~40 lines

async def _wizard_mark_complete(user_id: str) -> bool:
    """Mark setup as complete"""
    # Setup complete - ~40 lines
```

**Refactored `run_setup_wizard()`**:
```python
async def run_setup_wizard():
    """Main orchestrator - calls sub-functions in sequence"""
    if not await _wizard_preflight_checks():
        return
    if not await _wizard_docker_setup():
        return
    if not await _wizard_system_checks():
        return

    user_id = await _wizard_user_account()
    await collect_and_validate_api_keys(user_id)

    await _wizard_mark_complete(user_id)
```

**Acceptance Criteria for Phase 2**:
- [ ] All 5 new functions created
- [ ] `run_setup_wizard()` now <80 lines
- [ ] All new functions <50 lines
- [ ] Tests still pass
- [ ] Manual test: `python main.py setup` (full flow)

### Phase 3: Validation (1 hour)

**Acceptance Criteria**:
- [ ] No function >50 lines (except orchestrators)
- [ ] No duplicate code blocks >10 lines
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Manual wizard test successful
- [ ] No import errors
- [ ] Code follows existing patterns

---

## Implementation Order

1. **Extract API key helper first** (isolated change, easy to test)
2. **Refactor each API key section** (one at a time, test incrementally)
3. **Split wizard main function** (less risky, more isolated)
4. **Run full test suite** (validate no regressions)
5. **Manual end-to-end test** (smoke test)

---

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Break async/await structure | Low | High | Test each phase incrementally |
| Keychain integration issues | Low | Medium | Reuse existing patterns exactly |
| Import errors | Very Low | Medium | Verify imports after extraction |
| Behavioral change | Low | High | Manual test covers full flow |

---

## Testing Strategy

1. **Unit tests**: Extract helper, verify with one provider
2. **Integration tests**: Run full setup wizard (if env allows)
3. **Manual test**: `python main.py setup` - go through full flow
4. **Smoke test**: `pytest tests/ -m smoke`

---

## Success Criteria

- ✅ No functions >50 lines (except `run_setup_wizard()` orchestrator)
- ✅ All tests pass
- ✅ Manual wizard test successful
- ✅ No code duplication >10 lines
- ✅ All acceptance criteria from issue met
