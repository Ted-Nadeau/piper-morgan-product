# Release Notes - v0.8.1.3

**Release Date**: November 30, 2025, 3:44 PM PT
**Branch**: production
**Previous Version**: v0.8.1.2

---

## Summary

Critical restoration of login UI functionality combined with setup detection to prevent unconfigured startup. This release fixes a critical authentication blocker discovered during alpha testing and adds safeguards to guide first-time users through required setup.

---

## What Changed

### 🔐 **Login UI Restoration (Critical Fix)**

**Problem**: The login UI files (`templates/login.html`, `static/css/auth.css`, `static/js/auth.js`) were created in commit b1eaa78b on November 24, but were accidentally deleted during a production→main merge (commit 87848363) on November 27. Despite the original files existing in git history, they were removed from the working tree.

**Impact**: Alpha testers could not access the login page, blocking all authentication and testing workflows.

**Root Cause**: Merge conflict resolution during the production→main sync chose production's version (files deleted) over main's version (files present), causing the files to be lost despite being in git history.

**Fix**: Restored all three files from original commit b1eaa78b using `git checkout b1eaa78b -- [files]`:
- `templates/login.html` - Login page UI (72 lines)
- `static/css/auth.css` - Authentication styling (146 lines)
- `static/js/auth.js` - Client-side login form handling (69 lines)

**Deployed**: commit dced0d6a

---

### 🛡️ **Setup Detection (New Feature)**

**Purpose**: Prevents application startup if essential configuration is missing, guiding first-time users through required setup.

**What It Does**:
- Checks for user existence in database (needed for authentication)
- Verifies OpenAI API key is configured and active (required for AI features)
- Blocks startup if either check fails
- Shows clear welcome message explaining what's needed
- Offers interactive choice to run setup wizard immediately or quit

**Implementation**:
- New `is_setup_complete()` function in `scripts/setup_wizard.py`
- Startup check in `main.py` before server initialization
- Handles database errors gracefully (first run scenario)

**Benefits**:
- Prevents confusing errors when AI features aren't available
- Guides first-time users clearly rather than failing silently
- Allows deferred setup (users can run wizard later if preferred)
- Integrates seamlessly with existing setup wizard

**Files Changed**:
- `main.py` - Startup check logic (33 lines added)
- `scripts/setup_wizard.py` - Setup detection function (44 lines added)
- Session documentation (investigation and design notes)

**Related Issues**: #388 (Setup detection and startup check)

---

### 📚 **Version & Venv Documentation**

**New Guide**: `docs/dev-tips/version-bump-and-venv-fix.md`

Comprehensive documentation covering:
- Version bump process and best practices
- Virtual environment corruption diagnosis
- Recovery procedures for venv issues
- Integration with CI/CD deployment pipeline

**Purpose**: Provides alpha testers and developers with clear guidance on managing version changes and resolving environment-related issues.

---

## For Alpha Testers

### 🎯 **Action Required on Alpha Laptop**

After pulling this release:

```bash
# 1. Pull production branch
git pull origin production

# 2. You should see login UI files restored:
#    - templates/login.html
#    - static/css/auth.css
#    - static/js/auth.js

# 3. Restart server
./scripts/stop-piper.sh
./scripts/start-piper.sh

# 4. Verify - you should see:
#    ✅ Setup detection check pass
#    ✅ No file not found errors for login UI
#    ✅ Server starts successfully
```

### ✅ **What You Should See**

**Before (Broken)**:
```
404 Not Found: /templates/login.html
Error: Cannot load authentication UI
Login page unavailable
```

**After (Fixed)**:
```
🚀 Starting Piper Morgan...
✅ Docker Desktop is running
✅ Virtual environment activated
✅ Setup detection: system ready
✅ Backend is healthy
✅ Frontend is healthy
🎉 Piper Morgan is ready!
```

Login page loads successfully, authentication workflow works end-to-end.

### 📋 **First-Time Setup (If Required)**

If you see setup detection warning:

```bash
# Run interactive setup wizard
python main.py setup

# Or follow the interactive prompts offered by the startup check
```

The setup wizard will guide you through:
1. Creating admin user account
2. Configuring OpenAI API key
3. Validating database connectivity

---

## Files Changed

### Code Changes
1. `main.py` - Added startup setup detection check
2. `scripts/setup_wizard.py` - Added setup completion verification function
3. `static/css/auth.css` - Authentication styling (RESTORED)
4. `static/js/auth.js` - Login form handling (RESTORED)
5. `templates/login.html` - Login page UI (RESTORED)

### Documentation Changes
6. `docs/dev-tips/version-bump-and-venv-fix.md` - Version and venv management guide (NEW)
7. `pyproject.toml` - Version bump 0.8.1.2 → 0.8.1.3

### Session Documentation
8. Investigation reports and session logs documenting the authentication UI recovery process

**Total**: 7 files changed, 1,087 insertions(+), 1 deletion(-)

---

## Technical Details

### Deployment Process

**Phase 1**: Login UI restoration (commit dced0d6a)
```bash
# Restored from original commit b1eaa78b
git checkout b1eaa78b -- templates/login.html static/css/auth.css static/js/auth.js
```

**Phase 2**: Setup detection merge (commit d378c99a)
```bash
# Merged feat/setup-detection-388 to main
git merge feat/setup-detection-388 --no-ff
```

**Phase 3**: Documentation merge (commit a0fa63a3)
```bash
# Merged fix/version-and-venv-docs to main
git merge fix/version-and-venv-docs --no-ff
```

**Phase 4**: Version bump (commit d192f159)
```bash
version = "0.8.1.3"  # pyproject.toml
```

**Phase 5**: Production deployment (commit fae04751)
```bash
git checkout production
git merge main --ff-only  # 468924a4..d192f159
git push origin production
```

### Rollback Path (if needed)

```bash
# If critical issue discovered post-deployment:
git checkout production
git reset --hard 468924a4  # Revert to v0.8.1.2
git push origin production --force-with-lease

# Then notify PM immediately
```

---

## Known Issues

None specific to this release.

**Pre-existing** (tracked in `.pytest-known-failures`):
- 1 test fails due to API quota limits (not a code issue)

---

## Next Steps for Alpha Testing

1. **Pull this release** on your alpha laptop
2. **Verify login UI is restored** - should see no 404 errors
3. **Test authentication flow** - login page loads, credentials validate
4. **Complete setup if needed** - run setup wizard if prompted
5. **Resume full testing** - all authentication workflows should now work
6. **Report issues** if you encounter any problems with login or setup

---

## Support

If you encounter issues after updating:

1. **Login page not loading**: Verify files exist:
   ```bash
   ls -la templates/login.html static/css/auth.css static/js/auth.js
   ```

2. **Setup detection preventing startup**: Run setup wizard:
   ```bash
   python main.py setup
   ```

3. **Other issues**: Check `docs/dev-tips/version-bump-and-venv-fix.md` for troubleshooting

4. **Need help**: Report in #piper-alpha Slack channel or create GitHub issue

---

## Commits in This Release

- `dced0d6a` - fix: Restore login UI files deleted in production→main merge
- `d378c99a` - feat: Merge setup detection to prevent unconfigured startup
- `a0fa63a3` - docs: Merge version bump and venv management documentation
- `d192f159` - chore: Bump version to 0.8.1.3 for production deployment
- `fae04751` - chore: Deploy v0.8.1.3 to production - Login UI restored + setup detection + docs

**Full changelog**: [468924a4...fae04751](https://github.com/mediajunkie/piper-morgan-product/compare/468924a4...fae04751)

---

**Questions?** See `docs/dev-tips/version-bump-and-venv-fix.md` or contact PM.
