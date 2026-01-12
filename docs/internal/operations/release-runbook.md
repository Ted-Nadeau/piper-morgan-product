# Release Runbook

**Version**: 1.1
**Last Updated**: January 12, 2026

This runbook documents the complete process for releasing a new version of Piper Morgan to production.

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

### 1. Alpha Documentation (docs/ALPHA*)

Review and update as needed:

- [ ] `docs/ALPHA_TESTING_GUIDE.md` - Version number, new features section
- [ ] `docs/ALPHA_KNOWN_ISSUES.md` - Version number, update "What Works" section
- [ ] `docs/ALPHA_QUICKSTART.md` - Version number, highlights section
- [ ] `docs/ALPHA_AGREEMENT_v2.md` - Version number in header

### 2. Alpha Templates (docs/alpha/templates/)

Review and update if setup process changed:

- [ ] `alpha-tester-email-template.md` - Version number, prerequisites, setup highlights
- [ ] `alpha-tester-checkin-template.md` - Any new feedback areas
- [ ] `alpha-tester-profile-template.md` - Any new tracking fields

### 3. README Files

- [ ] `docs/README.md` - Release notes link points to new version
- [ ] `README.md` (root) - Verify still accurate (usually no changes needed)

### 4. Navigation

- [ ] `docs/NAVIGATION.md` - Add any new documentation sections created

### 5. Testing Documentation

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

### 6. Cleanup Working Files

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
| 1.1 | 2026-01-12 | Added Testing Documentation section (test count, canonical query matrix), Cleanup Working Files section |
| 1.0 | 2026-01-07 | Initial runbook based on v0.8.3.1 release |

---

**See Also**:
- [Versioning Strategy](../../versioning.md)
- [CI/CD Smoke Test Runbook](ci-cd-smoke-test-runbook.md)
