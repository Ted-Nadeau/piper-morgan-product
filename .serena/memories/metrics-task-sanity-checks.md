# Metrics Task Sanity Checks

**Created**: January 3, 2026
**Context**: Subagent reported 1.17M LOC / 11K files while also reporting 145K / 502 for production - a 10x discrepancy that went unnoticed.

## Root Cause

The `.venv/` directory (note the dot) contains ~10K Python files from dependencies. The exclusion pattern used `./venv/*` but the actual directory is `.venv/`.

## Correct Exclusion Patterns for LOC Metrics

Always exclude these directories when counting "authored code":
```bash
.venv/          # Virtual environment (dot prefix)
venv/           # Virtual environment (no dot)
node_modules/   # Node.js dependencies
.git/           # Git internals
__pycache__/    # Python bytecode cache
.pytest_cache/  # Pytest cache
archive/        # Archived/deprecated code
trash/          # Deleted files
```

## Sanity Check Protocol for Metrics Tasks

Before reporting metrics, verify:

1. **Sum Check**: Do component sums match totals?
   - If production + test + other ≠ total, investigate

2. **Order of Magnitude Check**: Are any numbers suspiciously large?
   - Python codebase with >10K files → likely includes venv
   - >500K LOC in a single project → verify exclusions

3. **Ratio Check**: Are ratios reasonable?
   - Test:Production ratio typically 0.5-1.5x
   - Avg LOC/file typically 100-400 for well-organized code

4. **Cross-Validate**: Run targeted counts to verify
   ```bash
   # Direct count of core directories
   find ./services ./web ./cli ./scripts -name "*.py" | wc -l

   # Compare to "total" claim
   ```

## Accurate Piper Morgan Metrics (January 2026)

| Category | Files | LOC | Avg LOC/File |
|----------|-------|-----|--------------|
| Production (services/, web/, cli/, scripts/) | 502 | 145,571 | 290 |
| Tests (tests/) | 403 | 115,681 | 287 |
| Other (dev/, methodology/, etc.) | ~140 | ~25K | ~180 |
| **Total Authored** | ~1,045 | ~286K | ~274 |
| Dependencies (.venv/) | ~10K | ~3.9M | - |

## Lesson

When reporting metrics, always:
1. State what's included/excluded
2. Verify sums reconcile
3. Flag any 10x+ discrepancies for investigation
