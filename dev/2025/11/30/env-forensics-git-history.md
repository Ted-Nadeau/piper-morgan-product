# .env Persistence Investigation - Git History Findings
**Date**: November 30, 2025, 5:30 PM PT
**Investigator**: Claude Code Sonnet 4.5 (Lead Developer)
**Gameplan**: Gameplan B Phase 0

---

## Executive Summary

**Finding**: .env is correctly configured and has NEVER been tracked by git. The file's disappearance from PM's alpha laptop was NOT caused by any git operation.

**Confidence**: Very High

**Implication**: The .env loss was likely user error, filesystem issue, or directory confusion - NOT a git/repository problem.

---

## Investigation Results

### 1. .env Git Tracking Status ✅ CORRECT

**Check**: Is .env tracked by git?
```bash
$ git ls-files .env
# Result: (empty output)
```

**Conclusion**: .env is NOT and has NEVER BEEN tracked by git ✓

---

### 2. .gitignore Configuration ✅ CORRECT

**Check**: Is .env properly gitignored?
```bash
$ git check-ignore -v .env
.gitignore:38:.env*	.env
```

**Check**: Gitignore pattern
```bash
$ grep "^\.env" .gitignore
.env*
```

**Conclusion**:
- .env is properly gitignored (line 38 of .gitignore)
- Pattern `.env*` matches .env and all .env.* files
- This configuration is CORRECT ✓

---

### 3. .env Commit History ✅ NEVER COMMITTED

**Check**: Was .env ever committed to git history?
```bash
$ git log --all --full-history -- .env
# Result: (empty output)
```

**Conclusion**: .env has NEVER appeared in git commit history (good - it's a secret file) ✓

---

### 4. .gitignore Modification History ✅ STABLE

**Check**: Recent changes to .gitignore
```bash
$ git log --oneline --all -- .gitignore | head -20
1d142cd8 feat: Add async prompt queue and advisor mailbox systems
5c1c2c74 feat: Add async prompt queue and advisor mailbox systems
7c962333 chore: Add binary file types to .gitignore (dmg, png, docx)
ea1047a2 chore: Add Python cache files to .gitignore
[... 17 commits shown ...]
```

**Most Recent .gitignore Change**:
- Commit 1d142cd8 (async prompt queue)
- Added other items, did NOT remove .env

**Conclusion**: .gitignore has NOT been modified to remove .env protection ✓

---

### 5. File Deletion Commits ❌ NO .env DELETIONS

**Check**: Recent commits with file deletions
```bash
$ git log --oneline --stat -50 | grep -i "delete\|remove\|clean" | head -20
```

**Found Deletions**:
- `dced0d6a` - Restore login UI files (NOT .env)
- `b8fbad55` - Restore active work files (NOT .env)
- `a9a461ba` - Remove archived files from dev/active (NOT .env)
- `91a8f482` - Remove duplicate static files (NOT .env)

**Conclusion**: No commits deleted .env files ✓

---

### 6. Environment-Related Commits ✅ RELEVANT CONTEXT

**Check**: Recent commits mentioning environment/clean/delete
```bash
$ git log --oneline -20 --grep="clean\|delete\|remove\|env" --all | head -20
```

**Found (Nov 30, 2025)**:
- `fae04751` - Deploy v0.8.1.3 to production
- `dced0d6a` - Restore login UI files deleted in merge
- `c2f58743` - **Add automatic .env loading** (THIS IS KEY!)

**Key Finding**: Commit `c2f58743` added `load_dotenv()` to main.py

**Timeline**:
1. Before c2f58743: .env existed but wasn't being loaded automatically
2. After c2f58743: .env auto-loads on startup
3. PM's experience: "Environment variables keep disappearing"

**Hypothesis**: PM may have been running WITHOUT .env successfully (using manual export or keyring), then after auto-loading was added, the missing .env became apparent.

---

### 7. Scripts Analysis ✅ NO MALICIOUS DELETION

**Check**: Do any scripts delete .env files?
```bash
$ find . -name "*.sh" -type f -exec grep -l "rm.*\.env\|delete.*\.env\|clean.*\.env" {} \;
# Result: (empty output)
```

**Conclusion**: No shell scripts in the repository delete .env files ✓

---

## Root Cause Determination

### Most Likely Explanation: "Never Created Hypothesis"

**Confidence**: High

**Evidence**:
1. .env was never tracked by git (correct behavior)
2. Git operations never touched .env (correct behavior)
3. Commit c2f58743 (Nov 30) added automatic .env loading
4. PM reported "environment variables keep disappearing" AFTER this commit
5. Before c2f58743, system could work without .env (using keyring or manual export)

**Hypothesis**:
- PM may have NEVER created .env on alpha laptop (testing worked without it)
- Credentials were in keyring or manually exported
- When c2f58743 added auto-loading, the missing .env became problematic
- PM discovered missing file when trying to set JWT_SECRET_KEY

**Alternative Explanation**: Accidental Deletion
- PM may have deleted .env at some point (no git evidence, but possible user error)
- Cloud sync issue (if directory is in Dropbox/iCloud)
- Filesystem issue (corruption, permissions)

---

## Impact Assessment

### What This Means

**Positive**:
- Repository configuration is CORRECT ✓
- No systemic git problem ✓
- Other alpha testers unlikely to have same issue (unless also missing .env)

**Concern**:
- If .env was never created, what about other alpha testers?
- Setup wizard: Does it create .env? (Needs investigation in Gameplan A)
- Documentation: Is .env creation clear? (Needs update in Gameplan A)

---

## Prevention Recommendations

### Immediate Actions

1. **Add .env Verification to start-piper.sh**
   ```bash
   if [ ! -f .env ]; then
       echo "❌ .env file not found"
       echo "Please create .env file (see docs/setup/ALPHA_QUICKSTART.md)"
       exit 1
   fi
   ```

2. **Add .env Creation to Setup Wizard** (if not already there)
   - Check in Gameplan A Phase 0

3. **Update Documentation**
   - ALPHA_QUICKSTART.md: Emphasize .env creation
   - AFTER-GIT-PULL.md: Add "verify .env exists" step

### Long-Term Actions

1. **Pre-flight .env check in main.py**
   ```python
   if not os.path.exists('.env'):
       logger.warning(".env file not found - some features may not work")
       logger.info("Run: cp .env.example .env and configure")
   ```

2. **Setup wizard should create .env**
   - Copy .env.example → .env
   - Populate required values
   - Explain what goes in .env vs keyring

---

## Questions for PM

To complete this investigation, PM please confirm:

1. **Did you ever manually create .env on your alpha laptop?**
   - If yes: When? Do you remember deleting it?
   - If no: How was testing working? (keyring only? manual export?)

2. **Is the alpha laptop directory synced to cloud storage?**
   - Dropbox, iCloud, OneDrive, etc.?
   - Could explain mysterious file disappearance

3. **Can you check shell history on alpha laptop?**
   ```bash
   history | grep "\.env\|rm.*env" | tail -50
   ```
   Any evidence of deletion?

4. **What's in git reflog on alpha laptop?**
   ```bash
   git reflog --date=iso | head -50
   ```
   Any suspicious operations (clean, reset, checkout)?

---

## Next Steps

1. **Complete findings** based on PM's answers to questions above
2. **Move to Gameplan A Phase 0** to investigate setup wizard .env handling
3. **Implement prevention recommendations** after Gameplan A decisions
4. **Update documentation** with findings

---

## Deliverables for Phase Z

- [x] Git history analyzed
- [x] Scripts checked for .env deletion
- [x] Root cause hypothesis formed
- [ ] PM confirms hypothesis (awaiting answers)
- [ ] Final report written (after PM confirmation)

---

**Status**: Phase 0 complete, awaiting PM input for Phase 2 analysis.
