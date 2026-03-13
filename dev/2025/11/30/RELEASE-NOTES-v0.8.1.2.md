# Release Notes - v0.8.1.2

**Release Date**: November 30, 2025, 8:50 AM PT
**Branch**: production
**Previous Version**: v0.8.1.1

---

## Summary

Critical fix for alpha testers: Automatic environment variable loading and comprehensive setup documentation. This release solves the "lost environment variables after git pull" issue that was blocking alpha testing.

---

## What Changed

### 🔧 **Automatic .env Loading** (Critical Fix)

**Problem**: Environment variables appeared to "disappear" after pulling new code, requiring manual reconfiguration.

**Root Cause**: `main.py` wasn't calling `load_dotenv()`, so `.env` files existed but were never loaded.

**Fix**: Added automatic `.env` loading on startup:
```python
# main.py (lines 9-11)
from dotenv import load_dotenv
load_dotenv()  # Loads .env before any other imports
```

**Impact**:
- ✅ No more manual `export JWT_SECRET_KEY=...` needed
- ✅ Environment variables persist across git pull operations
- ✅ Consistent behavior for all alpha testers

---

### 📚 **Alpha Tester Documentation Improvements**

#### Updated `ALPHA_QUICKSTART.md`
- Changed from "5-Step" to "6-Step" setup
- **New Step 2**: "Configure environment variables (CRITICAL - 1 min)"
- Documents `JWT_SECRET_KEY` generation: `openssl rand -hex 32`
- Explains that `.env` is gitignored and survives git operations
- Added troubleshooting section: "Environment variables not loading after git pull?"

#### New Guide: `docs/setup/AFTER-GIT-PULL.md`
Comprehensive post-pull checklist for alpha testers:
1. Verify .env still exists (it always should - gitignored)
2. Check for new environment variables (diff .env.example)
3. Update Python dependencies if needed
4. Run system health check (`python main.py status`)
5. Check for database migrations
6. Test server startup

Includes:
- Version-specific migration notes (v0.8.1.1 → v0.8.1.2)
- Emergency rollback instructions
- Troubleshooting for common post-pull issues

---

### 🔨 **Script Fixes** (from earlier today)

**Fixed**: Symlink resolution in `start-piper.sh` and `stop-piper.sh`

**Problem**: Scripts failed when run via symlinks in repo root with `is_windows: command not found`

**Fix**: Added symlink resolution loop before calculating `SCRIPT_DIR`

**Impact**: Scripts now work correctly whether run as `./stop-piper.sh` or `./scripts/stop-piper.sh`

---

## For Alpha Testers

### 🎯 **Action Required on Alpha Laptop**

After pulling this release:

```bash
# 1. Pull production branch
git pull origin production

# 2. Create .env file (if you don't have one)
cp .env.example .env

# 3. Generate and set JWT_SECRET_KEY
openssl rand -hex 32  # Generates: ea31f4199ab466a3a221f412a016a529026b1b13959bcb9be2d7c1ae1c08c013
# Edit .env and add:
# JWT_SECRET_KEY=ea31f4199ab466a3a221f412a016a529026b1b13959bcb9be2d7c1ae1c08c013

# 4. Restart server
./scripts/stop-piper.sh
./scripts/start-piper.sh

# 5. Verify - should see NO JWT_SECRET_KEY warnings in terminal
```

### ✅ **What You Should See**

**Before (Broken)**:
```
{"event": "JWT_SECRET_KEY not set, using development fallback", "level": "warning"}
{"error":"authentication_required", "message":"Authentication required"}
```

**After (Fixed)**:
```
🚀 Starting Piper Morgan...
✅ Docker Desktop is running
✅ Virtual environment activated
✅ Backend is healthy
✅ Frontend is healthy
🎉 Piper Morgan is ready!
```

No JWT warnings, auth middleware working correctly.

---

## Files Changed

### Code Changes
1. `main.py` - Added `load_dotenv()` call
2. `scripts/start-piper.sh` - Symlink resolution fix
3. `scripts/stop-piper.sh` - Symlink resolution fix

### Documentation Changes
4. `docs/ALPHA_QUICKSTART.md` - Added environment setup step, troubleshooting
5. `docs/setup/AFTER-GIT-PULL.md` - New comprehensive post-pull guide
6. `pyproject.toml` - Version bump 0.8.1.1 → 0.8.1.2

### Session Documentation
7. `dev/active/2025-11-30-0705-lead-code-sonnet-log.md` - Investigation and fixes documented

**Total**: 7 files changed, 771 insertions(+), 8 deletions(-)

---

## Technical Details

### Deployment Process

**Phase 1**: Version bump (commit 468924a4)
```bash
version = "0.8.1.2"  # pyproject.toml
```

**Phase 2**: Safety tag created
```bash
git tag production-pre-env-fixes-2025-11-30
git push origin production-pre-env-fixes-2025-11-30
```

**Phase 3**: Fast-forward merge
```bash
git checkout production
git merge main --ff-only  # c0249905..468924a4
```

**Phase 4**: Production push
```bash
git push origin production
# ✅ Pre-push tests: 87 passed, 1 known failure (API quota)
```

**Rollback Path** (if needed):
```bash
git checkout production
git reset --hard production-pre-env-fixes-2025-11-30
git push origin production --force-with-lease
```

---

## Known Issues

None specific to this release.

**Pre-existing** (tracked in `.pytest-known-failures`):
- 1 test fails due to API quota limits (not a code issue)

---

## Next Steps for Alpha Testing

1. **Pull this release** on your alpha laptop
2. **Set JWT_SECRET_KEY** in .env (see "Action Required" above)
3. **Restart server** and verify no warnings
4. **Resume testing** - auth should work correctly now
5. **Report issues** if you encounter any problems

---

## Support

If you encounter issues after updating:

1. **Check `.env` exists**: `ls -la .env`
2. **Verify JWT key set**: `grep JWT_SECRET_KEY .env`
3. **Review post-pull guide**: `docs/setup/AFTER-GIT-PULL.md`
4. **Contact**: Report in #piper-alpha Slack channel or create GitHub issue

---

## Commits in This Release

- `468924a4` - chore: Bump version to 0.8.1.2 for production deployment
- `c2f58743` - fix: Add automatic .env loading and comprehensive alpha tester environment docs
- `dddd3b31` - fix: Handle symlinks correctly in stop/start-piper.sh scripts

**Full changelog**: [c0249905...468924a4](https://github.com/mediajunkie/piper-morgan-product/compare/c0249905...468924a4)

---

**Questions?** See `docs/setup/AFTER-GIT-PULL.md` or contact PM.
