# Branch Discipline & Git Workflow

**Established**: 2025-11-27, 4:34 PM
**Status**: Active Policy

---

## Core Principles

1. **NO direct pushes to `production` without PM approval**
2. **Push to `production` only at end of sessions** when code is stable
3. **Version increments** happen at stable updates (next: 0.8.2 with release notes)
4. **ALL agents work in feature branches** (including Claude Code)
5. **Pull requests required** for all changes
6. **Merge to `main` first**, then push `main` → `production` on PM approval

---

## Workflow Steps

### Development Flow

```
feature-branch → PR → main → (PM approval) → production
```

### Step-by-Step

1. **Create feature branch**:
   ```bash
   git checkout -b fix/issue-XXX-description
   # or
   git checkout -b feat/issue-XXX-description
   ```

2. **Work in feature branch**:
   - Make commits with clear messages
   - Run `./scripts/fix-newlines.sh` before committing
   - Push to origin regularly

3. **Create Pull Request**:
   ```bash
   git push -u origin fix/issue-XXX-description
   gh pr create --title "fix(#XXX): Description" --body "..."
   ```

4. **After PR approval**:
   - Merge PR to `main`
   - Delete feature branch

5. **Push to production** (PM approval required):
   ```bash
   git checkout main
   git pull origin main
   git checkout production
   git merge main
   git push origin production
   ```

---

## Branch Naming

**Format**: `type/issue-number-brief-description`

**Types**:
- `fix/` - Bug fixes
- `feat/` - New features
- `docs/` - Documentation only
- `refactor/` - Code refactoring
- `test/` - Test additions/fixes

**Examples**:
- `fix/393-cookie-auth-mismatch`
- `feat/394-error-recovery-guidance`
- `docs/385-infra-refactor-completion`

---

## Version Management

**Current**: 0.8.1
**Next**: 0.8.2 (at next stable update)

**When to increment**:
- Stable feature complete
- Bug fixes deployed
- Ready for alpha testing
- PM approves release

**Release notes required** for each version increment.

---

## What Changed (2025-11-27)

**Previous workflow**:
- Direct commits to `production` branch
- No PR process
- Ad-hoc version increments

**New workflow**:
- Feature branches mandatory
- PR review required
- `main` as integration branch
- `production` as stable release branch
- PM approval gate before production push

---

## Critical Rules for Agents

❌ **NEVER**:
- Push directly to `production`
- Skip PR process
- Merge without approval
- Work on `main` or `production` directly

✅ **ALWAYS**:
- Create feature branch for work
- Use proper branch naming
- Create PR for review
- Wait for PM approval before production push
- Document in commit messages

---

## Emergency Hotfixes

If critical bug requires immediate production fix:

1. Create hotfix branch from `production`
2. Make minimal fix
3. Get PM approval
4. Merge to both `production` AND `main`
5. Document in release notes

---

**Related**:
- Git workflow: CLAUDE.md (to be updated)
- Version history: docs/CHANGELOG.md
- Release process: docs/RELEASE_PROCESS.md (if exists)
