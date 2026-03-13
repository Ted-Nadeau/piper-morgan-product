# Gameplan: #633 CONSCIOUSNESS-TRANSFORM CLI Output

**Issue**: #633 CONSCIOUSNESS-TRANSFORM: CLI Output (Mechanical → Conscious)
**Created**: 2026-01-21
**Estimated Effort**: 3 hours
**Methodology**: TDD, Multi-Agent

---

## Phase 0: Infrastructure Verification

### Files Confirmed to Exist
```
main.py                      # Entry point with startup/shutdown messages
cli/commands/cal.py          # Calendar CLI
cli/commands/keys.py         # Key management CLI
cli/commands/standup.py      # Standup CLI
services/consciousness/      # Consciousness framework (ready)
```

### Consciousness Framework Ready
- `validate_mvc()` available
- Error consciousness patterns from #631 can be reused
- Loading consciousness patterns from #630 can inform startup messages

---

## Phase 1: Create CLI Consciousness Wrapper

**Agent**: Code Agent

**Deliverables**:
- `services/consciousness/cli_consciousness.py` (NEW)
- `tests/unit/services/consciousness/test_cli_consciousness.py` (NEW)

**Functions Required**:
1. `format_startup_message_conscious()` - "Starting up..."
2. `format_ready_message_conscious(url: str)` - "I'm up and running..."
3. `format_shutdown_message_conscious()` - "Shutting down..."
4. `format_cli_success_conscious(action: str, detail: str)` - Success confirmations
5. `format_cli_error_conscious(error: str)` - Error with invitation to retry

**TDD Approach**:
1. Write tests first (8+ tests)
2. Implement formatters
3. Validate MVC on each

**Acceptance Criteria**:
- [ ] 8+ tests passing
- [ ] All formatters have identity voice
- [ ] MVC validation passes

---

## Phase 2: Integration

**Agent**: Code Agent

**Deliverables**:
- Modified `main.py`
- Updated exports in `services/consciousness/__init__.py`

**Integration Points**:
1. `main.py:109` - Startup message
2. `main.py:137-143` - Ready message block
3. `main.py:165` - Shutdown message
4. `main.py:172` - Error message
5. `main.py:244-246` - Key storage success/failure

**Acceptance Criteria**:
- [ ] Import works: `python -c "from services.consciousness import ..."`
- [ ] CLI still starts: `python main.py --help`
- [ ] Server starts normally: `python main.py` (brief test)

---

## Phase 3: Validation

**Agent**: Validator

**Validation Steps**:
1. Run `python main.py --help` - verify no crashes
2. Run `python main.py` briefly - capture startup output
3. Score output against rubric
4. Document before/after

**Target Score**: 14+/20 (CLI is simpler than full responses)

**Acceptance Criteria**:
- [ ] CLI functions normally
- [ ] Rubric score ≥14/20
- [ ] Before/after documented

---

## STOP Conditions

1. CLI commands fail after changes
2. Server won't start
3. Key management breaks
4. Import errors

---

## Completion Matrix

| Criterion | Verification Method |
|-----------|-------------------|
| Wrapper created | `ls services/consciousness/cli_consciousness.py` |
| Tests pass | `pytest tests/unit/services/consciousness/test_cli_consciousness.py -v` |
| Integration works | `python main.py --help` succeeds |
| Score ≥14/20 | Manual rubric scoring |

---

*Gameplan Version: 1.0*
*Streamlined from template v9.3*
