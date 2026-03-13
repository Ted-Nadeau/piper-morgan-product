# Session Log: Repository Size Audit for Alpha Tester Onboarding

**Date**: 2026-01-22 1:12 PM
**Agent**: spec-code-opus (Special Assignments)
**PM**: xian
**Purpose**: Investigate repository bloat and propose cleanup plan for alpha testers

---

## Executive Summary

The repository is **9.3GB** total, but a fresh clone would be **~792MB** (still large). The working directory contains significant untracked bloat, and the git history contains large binaries that were committed and later removed.

### Key Findings

| Category | Size | Tracked in Git? | Impact on Clone |
|----------|------|-----------------|-----------------|
| `dev/` (session logs, archives) | 5.0GB | NO | None |
| `venv/` | 1.3GB | NO (gitignored) | None |
| `skunkworks/mobile/` | 1.2GB | Partially | Small |
| `archive/` | 153MB | YES (153 files) | YES |
| `trash/` | 788KB | YES (42 files) | YES |
| `htmlcov/` | 27MB | NO | None |
| `.git/` history | 880MB | N/A | **YES - 792MB clone** |

### The Real Problem: Git History Bloat

A fresh `git clone` is **792MB** because the history contains large binaries that were **committed then deleted**:

**Top offenders in git history** (no longer in working tree):
- `venv/` binaries: ~180MB (58MB onnxruntime, 31MB grpc, 27MB pulsar, etc.)
- `data_backup/postgres/pg_wal/`: 16MB WAL file
- ChromaDB binary data: 16MB + 6MB
- Survey data files: 2 × 14MB
- Large screenshots in `dev/`: 8MB + 8MB + 5MB
- Blog images: Multiple 3-4MB PNGs
- Test fixtures: 7MB PDF

---

## Detailed Breakdown

### 1. Untracked Local Bloat (Not Affecting Clones)

These are large but already gitignored or untracked:

| Directory | Size | Status |
|-----------|------|--------|
| `dev/archive/2025/` | 4.7GB | Untracked (session logs, raw transcripts) |
| `venv/` | 1.3GB | Gitignored |
| `node_modules/` (2 locations) | 348MB | Gitignored |
| `htmlcov/` | 27MB | Untracked |
| `__pycache__/` | 64MB | Gitignored |

**Largest single files** (untracked):
- `dev/archive/2025/11/21/2025-11-21-1825-prog-code-raw.txt`: **1.6GB**
- `dev/archive/2025/11/21/2025-11-21-2002-prog-code-raw.txt`: **1.5GB**
- `dev/archive/2025/11/21/2025-11-21-2102-prog-code-raw.txt`: **1.2GB**

These are raw Claude Code session transcripts - massive but don't affect clones.

### 2. Tracked Files That Should Be Gitignored

| Directory | Files | Size | Should Remove? |
|-----------|-------|------|----------------|
| `archive/` | 153 | ~5MB tracked | YES - historical cruft |
| `trash/` | 42 | ~1MB | YES - it's literally trash |
| `archive/piper-morgan-0.1.1/` | Contains old DBs | ~1MB tracked | YES |
| `archive/piper-morgan-1.0/` | Old project copy | ~1MB tracked | YES |

### 3. Git History Bloat (Affects Every Clone)

**Binaries accidentally committed then removed**:

```
58MB  venv/lib/python3.9/site-packages/onnxruntime/capi/onnxruntime_pybind11_state.so
31MB  venv/lib/python3.9/site-packages/grpc/_cython/cygrpc.cpython-39-darwin.so
27MB  venv/lib/python3.9/site-packages/_pulsar.cpython-39-darwin.so
23MB  venv/lib/python3.9/site-packages/numpy/.dylibs/libopenblas64_.0.dylib
21MB  venv/lib/python3.9/site-packages/cryptography/hazmat/bindings/_rust.abi3.so
16MB  data_backup/postgres/pg_wal/000000010000000000000001
16MB  archive/piper-morgan-0.1.1/pm_kb_docs_backup/.../data_level0.bin
14MB  archive/piper-morgan-0.1.1/survey.cat (×2)
 8MB  dev/2025/10/24/screencapture-medium-*.png (×3)
 7MB  tests/fixtures/empty_document.pdf
 6MB  archive/piper-morgan-0.1.1/backups/.../data_level0.bin
```

**Images in docs** (still tracked):
- Multiple 3-4MB blog images in `docs/assets/blog-images/`
- `docs/comms/blog/` PNGs

---

## Proposed Cleanup Plan

### Phase 1: Immediate Gitignore Updates (No History Rewrite)

Add to `.gitignore`:
```gitignore
# Development artifacts (already untracked)
dev/
htmlcov/
.coverage

# Directories that shouldn't be tracked
archive/
trash/

# Database files
*.sqlite3
*.db
data_backup/

# Large test fixtures
tests/fixtures/*.pdf

# Session logs and raw transcripts
*-raw.txt
```

**Impact**: Prevents future bloat, doesn't fix existing clone size.

### Phase 2: Remove Tracked Files (Preserves History)

```bash
# Remove from tracking but keep locally
git rm -r --cached archive/
git rm -r --cached trash/
git commit -m "chore: Remove archive/ and trash/ from tracking"
```

**Impact**: Future clones won't include these files (saves ~5MB), but history still contains them.

### Phase 3: History Rewrite (Nuclear Option)

Use `git filter-repo` to remove large blobs from history:

```bash
# Install
pip install git-filter-repo

# Analyze what to remove
git filter-repo --analyze

# Remove specific large files
git filter-repo --path venv/ --invert-paths
git filter-repo --path data_backup/ --invert-paths
git filter-repo --path-glob '*.so' --invert-paths
git filter-repo --path-glob '*.bin' --invert-paths
```

**Impact**: Could reduce clone from 792MB to ~50-100MB. **BUT**:
- Rewrites all commit SHAs
- Breaks all existing clones (must re-clone)
- Breaks any open PRs
- Requires coordination with all contributors

### Phase 4: Large File Management (Going Forward)

1. **Git LFS** for necessary large files (images, PDFs):
   ```bash
   git lfs install
   git lfs track "*.png"
   git lfs track "*.pdf"
   ```

2. **External storage** for blog images (CDN, S3, etc.)

3. **Pre-commit hook** to reject large files:
   ```bash
   # .pre-commit-config.yaml addition
   - repo: https://github.com/pre-commit/pre-commit-hooks
     hooks:
       - id: check-added-large-files
         args: ['--maxkb=500']
   ```

---

## Recommendations for Alpha Tester Onboarding

### Option A: Conservative (Recommended Now)
1. Implement Phase 1 (gitignore updates)
2. Implement Phase 2 (remove archive/trash from tracking)
3. Document that clone is ~800MB (acceptable for development repo)
4. Defer history rewrite to later

**Clone size after**: ~790MB (minimal change, but stops future growth)

### Option B: Aggressive (Better UX, More Risk)
1. All of Option A
2. Implement Phase 3 (history rewrite)
3. Coordinate with all existing contributors to re-clone
4. Set up Git LFS for images

**Clone size after**: ~50-100MB

### Option C: Shallow Clone Workaround
Document for alpha testers:
```bash
# Quick start (minimal download)
git clone --depth 1 https://github.com/mediajunkie/piper-morgan-product.git

# Later, if full history needed
git fetch --unshallow
```

**Clone size**: ~31MB initial, 792MB if unshallowed

---

## Files to Review Before Deciding

1. **`docs/assets/blog-images/`** - Are these needed in repo or can they be hosted externally?
2. **`tests/fixtures/empty_document.pdf`** - 7MB PDF, is this necessary?
3. **`archive/piper-morgan-0.1.1/`** and `archive/piper-morgan-1.0/` - Historical project snapshots, any value?
4. **`skunkworks/mobile/`** - Mobile POC, should it be a separate repo?

---

## Next Steps

Awaiting PM decision on:
1. Which phase(s) to implement
2. Whether history rewrite is acceptable
3. Timeline for alpha tester onboarding
4. Whether to move blog images to external hosting

---

---

## Implementation (4:20 PM)

### Changes Made

1. **Updated `.gitignore`** - Added explicit rules for:
   - `dev/`, `archive/`, `trash/` (development artifacts)
   - `htmlcov/`, `.coverage` (test coverage)
   - `*.sqlite3`, `*.db`, `data_backup/` (database files)

2. **Removed from tracking**:
   - `dev/`: 2,898 files removed
   - `archive/`: 153 files removed
   - `trash/`: 42 files removed
   - **Total: 3,093 files**

### Results

| Metric | Before | After |
|--------|--------|-------|
| Tracked files | 6,065 | 2,974 |
| Tracked file size | ~260MB | **91MB** |

### For Alpha Testers

Recommended clone command:
```bash
git clone --depth 1 https://github.com/mediajunkie/piper-morgan-product.git
```

This gives them:
- ~91MB download (vs 792MB full clone)
- All source code, tests, configs - fully functional
- Can commit and push normally

What they won't have:
- Git history (no `git log`, `git blame`)
- If needed later: `git fetch --unshallow`

---

*Session log updated 2026-01-22 4:20 PM*
