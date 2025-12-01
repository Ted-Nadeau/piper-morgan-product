# Release Notes Policy
**Established**: November 30, 2025
**Owner**: Product Manager (xian)
**Enforcement**: Pre-push git hook + process discipline

---

## Policy Statement

**Release notes are MANDATORY when the Product Manager increments the version number in `pyproject.toml`.**

This policy ensures proper documentation of changes between official production releases for alpha testers, stakeholders, and the development team.

---

## When Release Notes Are Required

### ✅ REQUIRED

Release notes **MUST** be created when:
- PM increments version in `pyproject.toml` (e.g., 0.8.1.2 → 0.8.1.3)
- Changes are being deployed to `production` branch
- Preparing for alpha tester deployment

### ❌ NOT REQUIRED

Release notes are **NOT** required for:
- Development commits on `main` or feature branches
- Version remains unchanged
- Internal development work
- PR merges (unless PM increments version)

---

## Release Notes Format

### File Naming Convention

```
dev/YYYY/MM/DD/RELEASE-NOTES-vX.Y.Z.md
```

**Examples**:
- `dev/2025/11/30/RELEASE-NOTES-v0.8.1.3.md`
- `dev/2025/12/01/RELEASE-NOTES-v0.8.2.0.md`

### Required Sections

1. **Header** - Release date, branch, previous version
2. **Summary** - 2-3 sentence overview of changes
3. **What Changed** - Detailed breakdown of modifications
4. **For Alpha Testers** - Action items and testing guidance
5. **Files Changed** - Complete list with line counts
6. **Technical Details** - Deployment process, rollback instructions
7. **Known Issues** - Pre-existing or new issues
8. **Next Steps** - What alpha testers should do next
9. **Support** - How to get help
10. **Commits** - Full list with hashes and descriptions

### Template

Use the most recent release notes as a template. Example: [RELEASE-NOTES-v0.8.1.3.md](../../2025/11/30/RELEASE-NOTES-v0.8.1.3.md)

---

## Enforcement Mechanism

### Pre-Push Git Hook (Technical)

**Location**: `scripts/hooks/pre-push-release-notes-check.sh`

**Behavior**:
1. Detects pushes to `production` branch
2. Compares `pyproject.toml` version with remote
3. If version changed, requires release notes file
4. Validates file exists, is not empty, mentions version
5. **Blocks push** if release notes missing

**Installation**:
```bash
# One-time setup (already done for you)
ln -sf ../../scripts/hooks/pre-push-release-notes-check.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

**Bypass** (emergency only):
```bash
git push --no-verify
# WARNING: Only use if discussed with PM
```

### Process Discipline (Human)

**Deployment Checklist** (in CLAUDE.md):
1. Version bump in `pyproject.toml`
2. **Create release notes** ← MANDATORY
3. Safety tag
4. Merge to production
5. Push to origin (hook will enforce #2)

---

## Workflow Examples

### Example 1: Version Bump with Release Notes ✅

```bash
# 1. PM bumps version
vim pyproject.toml
# version = "0.8.1.3" → version = "0.8.1.4"

# 2. Create release notes
mkdir -p dev/2025/11/30
vim dev/2025/11/30/RELEASE-NOTES-v0.8.1.4.md
# ... write release notes following template ...

# 3. Commit both
git add pyproject.toml dev/2025/11/30/RELEASE-NOTES-v0.8.1.4.md
git commit -m "chore: Bump version to 0.8.1.4"

# 4. Push to production
git push origin production
# ✅ Hook validates release notes exist, push succeeds
```

### Example 2: Push Without Version Change ✅

```bash
# Some fixes, no version bump
git add services/some_fix.py
git commit -m "fix: Some bug"

# Push to production
git push origin production
# ✅ Hook sees version unchanged, allows push
```

### Example 3: Version Bump, Forgot Release Notes ❌

```bash
# 1. PM bumps version
vim pyproject.toml
# version = "0.8.1.3" → version = "0.8.1.4"

# 2. Commit (forgot release notes!)
git add pyproject.toml
git commit -m "chore: Bump version to 0.8.1.4"

# 3. Try to push
git push origin production
# ❌ Hook blocks push:
# "PUSH BLOCKED: Release notes missing"
# "Required file: dev/2025/11/30/RELEASE-NOTES-v0.8.1.4.md"

# 4. Fix by creating release notes
mkdir -p dev/2025/11/30
vim dev/2025/11/30/RELEASE-NOTES-v0.8.1.4.md

# 5. Commit and push again
git add dev/2025/11/30/RELEASE-NOTES-v0.8.1.4.md
git commit -m "docs: Add release notes for v0.8.1.4"
git push origin production
# ✅ Now succeeds
```

---

## Rationale

### Why This Policy Exists

1. **Alpha Tester Communication**: Testers need to know what changed and how to test it
2. **Audit Trail**: Document what went into each production release
3. **Rollback Guidance**: Each release documents how to revert if needed
4. **Professional Practice**: Industry standard for production software
5. **Historical Record**: Future reference for architectural decisions

### Why Enforced via Hook

1. **Prevents Accidents**: Easy to forget in rush to deploy
2. **Consistent Process**: Everyone follows same workflow
3. **Fails Fast**: Catch missing notes before push completes
4. **Automation**: Reduces cognitive load, increases reliability

### Why Only for Version Changes

1. **Proportional Response**: Not every commit needs release notes
2. **PM Control**: PM decides when to increment version (signals importance)
3. **Avoid Noise**: Too many release notes → alpha testers ignore them
4. **Focus**: Release notes document *releases*, not every commit

---

## Responsibilities

### Product Manager (xian)
- Decides when to increment version
- Reviews release notes for accuracy
- Approves deployment to production
- Can waive requirement (rare, documented)

### Lead Developer (Claude Code)
- Drafts release notes when version bumped
- Ensures all sections complete
- Verifies facts with git history
- Follows template format

### Alpha Testers
- Read release notes after pulling production
- Follow "For Alpha Testers" action items
- Report any discrepancies

---

## Exceptions

### Emergency Hotfixes

In rare cases, PM may approve push without release notes:

```bash
# PM explicitly approves bypass
git push --no-verify origin production

# MUST follow up with release notes within 24 hours
```

**Document exception**:
- Why bypass was necessary
- What was fixed
- Commit retroactive release notes

### Non-Production Branches

This policy **only applies to `production` branch**. Other branches:
- `main` - no release notes required
- Feature branches - no release notes required
- Development branches - no release notes required

---

## Troubleshooting

### Hook Not Running

```bash
# Verify hook is installed
ls -la .git/hooks/pre-push

# Should be symlink to scripts/hooks/pre-push-release-notes-check.sh

# If missing, reinstall:
ln -sf ../../scripts/hooks/pre-push-release-notes-check.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

### Hook Running But Not Blocking

```bash
# Check hook is executable
chmod +x .git/hooks/pre-push
chmod +x scripts/hooks/pre-push-release-notes-check.sh

# Test hook manually
bash scripts/hooks/pre-push-release-notes-check.sh
```

### Release Notes Rejected by Hook

**Error**: "Release notes file is empty"
- **Fix**: Add content to the file

**Error**: "Release notes don't mention version X.Y.Z"
- **Fix**: Ensure file contains version number in header or text

**Error**: "Could not read version from pyproject.toml"
- **Fix**: Verify pyproject.toml syntax is correct

---

## History

### Version 1.0 (November 30, 2025)
- Initial policy established
- Pre-push hook implemented
- Enforcement begins

### Trigger Event
v0.8.1.3 was deployed without release notes due to rushed deployment. This policy prevents recurrence.

---

## Related Documentation

- **Gameplan Template**: [knowledge/gameplan-template.md](../../knowledge/gameplan-template.md) - Phase Z includes release notes
- **CLAUDE.md**: Production deployment protocol includes release notes
- **Release Notes Examples**: [dev/2025/11/30/](../../2025/11/30/) - Recent examples

---

**Questions?** Contact PM (xian) or refer to [RELEASE-NOTES-v0.8.1.3.md](../../2025/11/30/RELEASE-NOTES-v0.8.1.3.md) as the canonical example.
