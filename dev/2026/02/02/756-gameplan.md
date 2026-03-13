# Gameplan: #756 - Fix test_identical_filenames_different_times

**Issue**: #756
**Date**: 2026-02-02
**Type**: Test Fix (Test expectation doesn't match design)

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Task**: Update test to expect `AmbiguousFileReferenceError` when files have identical names, matching the actual FileResolver design.

**Infrastructure**:
- Test file: `tests/unit/services/test_file_resolver_edge_cases.py`
- Code under test: `services/file_context/file_resolver.py`
- The FileResolver intentionally raises AmbiguousFileReferenceError when scores are within 0.2
- Similar pattern already exists in `test_special_characters_in_filename`

**Worktree Assessment**: SKIP WORKTREE - Single test file fix, < 15 min

### Part B: PM Verification

- [ ] PM confirms this is a test bug (not code bug)
- [ ] PM confirms Option A (fix test) over Option B (add tiebreaker)

### Part C: Decision

- [ ] PROCEED with gameplan
- [ ] REVISE based on PM feedback

---

## Phase 0: Investigation (Complete)

See `dev/2026/02/02/756-issue-audit.md` for full analysis.

**Key Finding**: FileResolver's AmbiguousFileReferenceError is correct by design. Test expectation was wrong.

---

## Phase 0.5-0.8: N/A

- 0.5: N/A - No frontend
- 0.6: N/A - Single-layer test fix
- 0.7: N/A - Not conversational
- 0.8: N/A - No new state

---

## Phase 1: Fix the Test

### Current Test (Broken)

```python
async def test_identical_filenames_different_times(self, async_transaction):
    """Test handling multiple files with same name"""
    # ... creates 3 files named "report.pdf" ...
    file_id, confidence = await resolver.resolve_file_reference(intent, owner_id)
    assert file_id == files[0].id  # Most recent - WRONG EXPECTATION
```

### Fixed Test

```python
async def test_identical_filenames_different_times(self, async_transaction):
    """Test handling multiple files with same name - should raise ambiguity"""
    # ... creates 3 files named "report.pdf" ...

    # Identical filenames with similar scores should raise ambiguity
    with pytest.raises(AmbiguousFileReferenceError) as exc_info:
        await resolver.resolve_file_reference(intent, owner_id)

    # Verify the most recent file is first in candidates
    assert len(exc_info.value.files) == 3
    assert exc_info.value.files[0].id == files[0].id  # Most recent is first candidate
```

---

## Phase Z: Verification

### Acceptance Criteria

- [ ] Test updated to expect AmbiguousFileReferenceError
- [ ] Test verifies most recent file is first candidate
- [ ] Test passes in isolation: `pytest tests/unit/services/test_file_resolver_edge_cases.py::TestFileResolverEdgeCases::test_identical_filenames_different_times -xvs`
- [ ] Test passes in batch: `pytest tests/unit/services/test_file_resolver_edge_cases.py -xvs`

### STOP Conditions

- If FileResolver doesn't put most recent file first in candidates → investigate scoring
- If other tests in same file break → evaluate impact

### Evidence Required

- [ ] Test output showing pass
- [ ] Grep showing no other tests depend on "most recent wins" assumption

---

## Files to Modify

| File | Changes |
|------|---------|
| `tests/unit/services/test_file_resolver_edge_cases.py` | Update test_identical_filenames_different_times |

---

## Multi-Agent Deployment

**Single agent** - Simple test fix, one file, < 15 min

---

## Estimated Scope

- Phase 1: 10 min (fix test)
- Phase Z: 5 min (verify)

**Total**: ~15 min
