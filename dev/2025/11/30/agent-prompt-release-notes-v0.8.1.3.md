# Agent Prompt: Draft Release Notes for v0.8.1.3
**Created**: November 30, 2025, 5:35 PM PT
**For**: Haiku Documentation Agent
**Gameplan**: Gameplan C Phase 1
**Model**: Haiku (cost-effective, structured writing)

---

## Context

You are a documentation agent tasked with drafting release notes for Piper Morgan v0.8.1.3, which was deployed to production today (November 30, 2025) without release notes. You need to create comprehensive, accurate release notes following the established format.

### What You Know

**Previous Release**:
- v0.8.1.2 deployed earlier today
- Release notes exist: `/dev/2025/11/30/RELEASE-NOTES-v0.8.1.2.md`
- Use this as your format template

**v0.8.1.3 Context** (from today's session):
- **Critical Fix**: Login UI files were accidentally deleted in a previous merge (commit 87848363), then restored today
- **Setup Detection**: Merged branch `feat/setup-detection-388` - prevents unconfigured startup
- **Venv Docs**: Merged branch `fix/version-and-venv-docs` - version bump and venv management guide

**Deployment Timeline** (November 30, 2025):
- ~3:38 PM PT: Login UI deletion discovered
- ~3:40 PM PT: Files restored from commit b1eaa78b (commit dced0d6a)
- ~3:42 PM PT: Branches merged (setup detection, venv docs)
- ~3:45 PM PT: Production deployment (commit fae04751)

**Key Commits**:
- `dced0d6a` - fix: Restore login UI files deleted in production→main merge
- `a0fa63a3` - docs: Merge version bump and venv management documentation
- `d192f159` - chore: Bump version to 0.8.1.3
- `fae04751` - chore: Deploy v0.8.1.3 to production

**Files Changed**:
- Login UI restored: `templates/login.html`, `static/css/auth.css`, `static/js/auth.js`
- Setup detection: `main.py`, `scripts/setup_wizard.py`
- Venv docs: `docs/dev-tips/version-bump-and-venv-fix.md`
- Version: `pyproject.toml`

---

## Your Task

Create `/dev/2025/11/30/RELEASE-NOTES-v0.8.1.3.md` following the v0.8.1.2 format.

### Required Sections

Use these exact sections (from v0.8.1.2 template):

1. **Header**
   ```markdown
   # Release Notes - v0.8.1.3

   **Release Date**: November 30, 2025, [TIME] PT
   **Branch**: production
   **Previous Version**: v0.8.1.2
   ```

2. **Summary**
   - Brief overview (2-3 sentences)
   - Critical fix: Login UI restoration
   - Alpha tester improvements: Setup detection, venv docs

3. **What Changed**
   - Section for each major change
   - Explain WHAT and WHY
   - Include backstory about login UI deletion/restoration

4. **For Alpha Testers**
   - Action required: `git pull origin production`
   - What's now available
   - How to use new features

5. **Files Changed**
   - Complete list with line counts (use git show --stat)

6. **Technical Details**
   - Deployment process
   - Rollback path

7. **Known Issues**
   - Any pre-existing issues (check `.pytest-known-failures`)

8. **Next Steps for Alpha Testing**
   - What alpha testers should do next

9. **Support**
   - How to get help

10. **Commits in This Release**
    - Full list with hashes and descriptions

### Tools You Can Use

**Git commands to gather information**:
```bash
# Get commit details
git show dced0d6a --stat
git show a0fa63a3 --stat
git show d192f159 --stat
git show fae04751 --stat

# Get commit messages
git log --oneline dced0d6a^..fae04751

# Full commit range
git log production --since="2025-11-30 14:30" --until="2025-11-30 16:00" --pretty=format:"- %h - %s"
```

**Read template**:
```bash
cat /dev/2025/11/30/RELEASE-NOTES-v0.8.1.2.md
```

---

## Quality Criteria

Your release notes must meet these standards:

- [ ] Accurate commit references (verify hashes)
- [ ] Clear action items for alpha testers
- [ ] Explains WHY changes were made (not just WHAT)
- [ ] Includes rollback instructions
- [ ] Matches v0.8.1.2 format and tone
- [ ] Professional, clear language
- [ ] No errors or omissions
- [ ] Login UI backstory explained (deletion in merge, restoration today)

---

## Constraints

**DO**:
- Read RELEASE-NOTES-v0.8.1.2.md completely first
- Use git commands to verify all facts
- Follow the template format exactly
- Explain login UI deletion/restoration timeline
- Include specific commit hashes
- Provide clear alpha tester instructions

**DON'T**:
- Make up information (verify everything with git)
- Skip sections from the template
- Use vague language ("some changes", "various improvements")
- Forget to include rollback path
- Omit explanation of WHY login UI was restored

---

## Deliverables

1. **File**: `/dev/2025/11/30/RELEASE-NOTES-v0.8.1.3.md`
2. **Format**: Markdown, following v0.8.1.2 template
3. **Length**: Similar to v0.8.1.2 (comprehensive but concise)
4. **Accuracy**: All facts verified against git history

---

## Success Criteria

Release notes are complete when:
- [ ] All 10 sections present
- [ ] All commit hashes verified
- [ ] Login UI story clearly explained
- [ ] Alpha tester actions clear
- [ ] Format matches v0.8.1.2
- [ ] No factual errors
- [ ] Professional tone throughout

---

## Example Structure (Login UI Section)

Here's how to explain the login UI restoration:

```markdown
### Login UI Restoration (Critical Fix)

**Problem**: The login UI files (templates/login.html, static/css/auth.css, static/js/auth.js) were accidentally deleted during a production→main merge on November 27, 2025 (commit 87848363). Despite the original creation commit (b1eaa78b from November 24) existing in git history, the files were removed from the working tree.

**Impact**: Alpha testers could not access the login page, blocking authentication testing.

**Fix**: Restored all three files from original commit b1eaa78b using `git checkout b1eaa78b -- [files]`

**Files Restored**:
- `templates/login.html` - Login page UI (146 lines)
- `static/css/auth.css` - Authentication styling (146 lines)
- `static/js/auth.js` - Client-side login logic (69 lines)

**Deployed**: commit dced0d6a
```

---

## Timeline

**Estimated Time**: 30-45 minutes
**Due**: As soon as possible (production already deployed)

---

## Questions for Lead Developer

If you encounter any issues:
- Can't find a commit → report which one
- Unclear what went into release → ask for clarification
- Format question → show example and ask
- Factual contradiction → report evidence of both sides

---

## Start Here

1. Read `/dev/2025/11/30/RELEASE-NOTES-v0.8.1.2.md` completely
2. Run git commands to gather commit information
3. Draft each section following the template
4. Verify all facts against git history
5. Write the file
6. Report completion

**Begin when ready. Good luck!**
