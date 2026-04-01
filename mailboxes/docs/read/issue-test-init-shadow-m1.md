# Issue: TEST-INIT-SHADOW — Audit Remaining `__init__.py` Shadowing Risk

## Summary

M0's #868 discovered that shadowed `__init__.py` files in test directories caused 90+ test failures. The immediate issue was fixed, but 21 test directories remain at risk. Audit and remediate to prevent recurrence.

## Context

- **Discovered in M0**: #868 found `__init__.py` files in test directories shadowing production modules
- **Root cause**: Python's import system finds test directory `__init__.py` before production modules
- **M0 fix**: Removed the immediate offending files (commit `6a94f336`)
- **Latent risk**: Lead Developer noted 21 remaining `__init__.py` files in test directories that could cause future shadowing
- **Why now**: Catching this in M1 prevents future debugging sessions like #868

## Acceptance Criteria

- [ ] Audit all test directories for `__init__.py` files
- [ ] Identify which files are necessary vs. vestigial
- [ ] Remove unnecessary `__init__.py` files from test directories
- [ ] Document any `__init__.py` files that must remain (with rationale)
- [ ] Add CI check to prevent new `__init__.py` files in test directories (optional but recommended)
- [ ] All tests still pass after changes

## Technical Notes

From Architect memo (March 10, 2026):
> "#868 revealed shadowed `__init__.py` causing 90+ test failures. 21 directories still at risk."

Pattern to audit:
```bash
find tests/ -name "__init__.py" -type f
```

For each file found:
1. Is it required for pytest collection? (Usually no)
2. Does it shadow a production module? (Check parent directory name)
3. Can it be safely removed?

## Effort Estimate

- **Estimate**: 1-2 hours
- **Risk**: Low — removing files, with test verification

## Sprint

M1 — Testing track

## Labels

`testing`, `tech-debt`, `m1-sprint`, `infrastructure`

---

*Issue drafted by PPM, March 11, 2026*
*Source: Chief Architect memo, M0 #868 findings*
