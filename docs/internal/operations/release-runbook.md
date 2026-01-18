# Release Runbook

**Version**: 1.3
**Last Updated**: January 15, 2026

This runbook documents the complete process for releasing a new version of Piper Morgan to production.

---

## How to Invoke a Release

**For Claude Code agents**: When the PM says "release" or "cut a release", you MUST:

1. Read this entire runbook first
2. Follow every step sequentially
3. Check off each item before proceeding
4. Do NOT skip documentation updates

**Prompt pattern for PM to use**:
> "Cut a release for v0.8.X.Y. Follow the release runbook at docs/internal/operations/release-runbook.md step by step."

---

## Pre-Release Checklist

### 1. Code Verification

- [ ] All planned issues for this release are closed
- [ ] All feature branches merged to main
- [ ] No open blockers or P0 issues

### 2. Test Suite

```bash
# Run full test suite
python -m pytest tests/ -v

# Expected: All tests pass (skipped tests for LLM/integration are acceptable)
# Record: X passed, Y skipped
```

- [ ] Unit tests passing
- [ ] Integration tests passing (if applicable)
- [ ] No new test failures introduced

### 3. Review Recent Commits

```bash
# Review commits since last release
git log --oneline v0.8.3..HEAD  # Replace with previous version tag
```

- [ ] All commits reviewed
- [ ] No accidentally merged debug code
- [ ] Commit messages are clear and descriptive

---

## Version Bump

### 1. Update pyproject.toml

```bash
# Edit pyproject.toml
# Change: version = "X.Y.Z" → version = "X.Y.Z+1"
```

- [ ] Version number updated in pyproject.toml

### 2. Create Release Notes

Create `docs/releases/RELEASE-NOTES-vX.Y.Z.md` with:

- Summary of changes
- New features (link to issues)
- Bug fixes (link to issues)
- Breaking changes (if any)
- Database migrations (if any)
- Configuration changes (if any)

- [ ] Release notes created

---

## Documentation Updates

**CRITICAL**: These steps are NOT optional. Skipping documentation updates means the release is incomplete.

### 1. Release Notes (MANDATORY)

- [ ] `docs/releases/RELEASE-NOTES-vX.Y.Z.md` - Create release notes file
- [ ] `docs/releases/README.md` - Update release index:
  - Update "Current Version" section
  - Add new row to Release History table
  - Update "Last updated" date
- [ ] `docs/README.md` - Update release notes link to new version
- [ ] `docs/versioning.md` - Update:
  - "Current Version" at top
  - Add row to Version History table
  - Update "Last updated" date at bottom

### 2. Alpha Documentation (MANDATORY - update version numbers)

These files have version numbers in their headers that MUST be updated:

- [ ] `docs/ALPHA_TESTING_GUIDE.md` - Update **Version** and **Last Updated** in header
- [ ] `docs/ALPHA_KNOWN_ISSUES.md` - Update **Version**, **Last Updated**, and title `(vX.Y.Z)`
- [ ] `docs/ALPHA_QUICKSTART.md` - Update **Version** and "What's New" section
- [ ] `docs/ALPHA_AGREEMENT_v2.md` - Update version in 3 places (header, line 15, line 153)

### 3. Alpha Templates (MANDATORY - update version numbers)

These templates reference version numbers that MUST be updated:

- [ ] `docs/alpha/templates/alpha-tester-email-template.md` - Update **Version** and **Last Updated**
- [ ] `docs/operations/alpha-onboarding/email-template.md` - Update version in multiple places (header, body text, footer)

### 4. Briefing Documentation (MANDATORY - update version)

- [ ] `docs/briefing/BRIEFING-CURRENT-STATE.md` - Update:
  - **Version** in STATUS BANNER
  - **Last Updated** date
  - Add row to Version History table
  - Update Release Notes link at bottom

### 5. Root README and Navigation

- [ ] `README.md` (root) - Verify still accurate (usually no changes needed)
- [ ] `docs/NAVIGATION.md` - Add any new documentation sections created

### 6. Testing Documentation

Update test statistics and coverage metrics:

```bash
# Get current test count
python -m pytest tests/ --collect-only -q 2>/dev/null | tail -3
# Record: X tests collected
```

- [ ] `docs/ALPHA_KNOWN_ISSUES.md` - Update test count (e.g., "2100+ tests")
- [ ] `docs/internal/testing/canonical-query-test-matrix-v2.md` - Review and update if new queries implemented:
  - Update "Last Tested" date
  - Update coverage percentages if changed
  - Mark any newly passing queries

### 7. Cleanup Working Files

- [ ] Remove any draft release notes from `dev/YYYY/MM/DD/` (canonical location is `docs/releases/`)
- [ ] Verify no stray working documents should be archived

---

## Git Operations

### 1. Commit Version Changes

```bash
# Run newline fixer first
./scripts/fix-newlines.sh

# Stage and commit
git add .
git commit -m "release: v0.8.3.1

- Bump version to 0.8.3.1
- Add release notes
- Update alpha documentation"
```

### 2. Create Git Tag

```bash
git tag -a v0.8.3.1 -m "Release v0.8.3.1"
```

### 3. Push to Remote

```bash
git push origin main
git push origin v0.8.3.1
```

- [ ] Code pushed to main
- [ ] Tag pushed to remote

---

## GitHub Release

### 1. Create Release

```bash
# Using GitHub CLI
gh release create v0.8.3.1 \
  --title "v0.8.3.1" \
  --notes-file docs/releases/RELEASE-NOTES-v0.8.3.1.md
```

Or via GitHub web UI:
1. Go to Releases → Draft a new release
2. Choose tag: v0.8.3.1
3. Title: v0.8.3.1
4. Copy content from release notes file
5. Publish release

- [ ] GitHub release published

---

## Post-Release Verification

### 1. Verify Release

- [ ] GitHub release shows correct tag
- [ ] Release notes display correctly
- [ ] Links in release notes work

### 2. Verify Application

```bash
# Fresh clone test (optional)
git clone https://github.com/mediajunkie/piper-morgan-product.git test-clone
cd test-clone
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py --version  # Should show new version
```

### 3. Notify Stakeholders

- [ ] Update session log with release completion
- [ ] Notify PM of release completion
- [ ] Update any tracking systems (if applicable)

---

## Rollback Procedure

If issues are discovered post-release:

```bash
# Delete the release on GitHub (if needed)
gh release delete v0.8.3.1 --yes

# Delete the tag
git tag -d v0.8.3.1
git push origin :refs/tags/v0.8.3.1

# Revert commits if needed
git revert HEAD
git push origin main

# Create hotfix version (e.g., 0.8.3.2)
```

---

## Artifact Checklist

After release, verify these artifacts exist:

| Artifact | Location | Status |
|----------|----------|--------|
| Release notes | `docs/releases/RELEASE-NOTES-vX.Y.Z.md` | |
| Git tag | `vX.Y.Z` | |
| GitHub release | Releases page | |
| Updated ALPHA docs | `docs/ALPHA_*.md` | |
| Session log entry | `dev/active/YYYY-MM-DD-*-log.md` | |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.3 | 2026-01-15 | Complete file inventory: marked Alpha docs and templates as MANDATORY, added specific file locations |
| 1.2 | 2026-01-15 | Added "How to Invoke" section, expanded mandatory release notes section (docs/releases/README.md, versioning.md) |
| 1.1 | 2026-01-12 | Added Testing Documentation section (test count, canonical query matrix), Cleanup Working Files section |
| 1.0 | 2026-01-07 | Initial runbook based on v0.8.3.1 release |

---

**See Also**:
- [Versioning Strategy](../../versioning.md)
- [CI/CD Smoke Test Runbook](ci-cd-smoke-test-runbook.md)
