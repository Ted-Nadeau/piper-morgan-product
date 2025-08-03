# Documentation Sync Process

## Overview

This document describes the automated documentation synchronization process that maintains a single source of truth for project documentation.

## 🎯 Single Source of Truth Strategy

### Canonical Source
- **`README.md` in root** is the canonical source of truth
- Contains the most up-to-date project information
- Actively maintained and updated

### Automated Sync
- **GitHub Action** automatically syncs root `README.md` → `docs/README.md`
- **CI validation** ensures docs stay in sync
- **Prevents drift** between documentation versions

## 🔄 Sync Process

### GitHub Action: `.github/workflows/sync-docs.yml`

**Triggers:**
- Push to `main` branch with changes to `README.md`
- Manual workflow dispatch

**Process:**
1. Copies `README.md` → `docs/README.md`
2. Commits changes if sync is needed
3. Validates sync was successful
4. Provides summary in GitHub Actions

### CI Validation: `.github/workflows/validate-docs-sync.yml`

**Triggers:**
- Pull requests affecting `README.md` or `docs/README.md`
- Push to `main` with changes to either file

**Validation:**
1. Ensures both files exist
2. Compares content for differences
3. Validates required docs structure
4. Fails CI if out of sync

## 📁 Documentation Structure

```
docs/
├── .nojekyll              # GitHub Pages configuration
├── index.html             # Landing page
├── README.md              # Auto-synced from root
├── architecture/          # Architecture documentation
├── development/           # Development guides
└── ...                    # Other documentation
```

## 🚀 How to Update Documentation

### For Most Updates
1. **Edit `README.md` in root** (canonical source)
2. **Push to main** - GitHub Action auto-syncs
3. **Verify** - CI validates sync

### For Emergency Fixes
1. **Edit `docs/README.md` directly** (if needed)
2. **Copy back to root** - `cp docs/README.md README.md`
3. **Commit both** - Ensures sync

### Manual Sync
```bash
# Sync from root to docs
cp README.md docs/README.md

# Validate sync
diff README.md docs/README.md

# Commit changes
git add docs/README.md
git commit -m "Manual sync README from root"
```

## 🔍 Validation Commands

### Check Sync Status
```bash
# Compare files
diff README.md docs/README.md

# Check if in sync
diff README.md docs/README.md > /dev/null && echo "✅ In sync" || echo "❌ Out of sync"
```

### Validate Structure
```bash
# Check required files
ls -la docs/.nojekyll docs/index.html docs/README.md

# Validate all exist
[ -f docs/.nojekyll ] && [ -f docs/index.html ] && [ -f docs/README.md ] && echo "✅ All files present"
```

## 🎯 Benefits

### ✅ Single Source of Truth
- Only one file to maintain (`README.md` in root)
- No manual sync required
- Consistent across all environments

### ✅ Automated Quality
- CI catches drift immediately
- GitHub Actions handle sync automatically
- Validation prevents broken docs

### ✅ Clear Process
- Well-documented sync process
- Easy to understand and follow
- Emergency procedures available

## 🚨 Troubleshooting

### Sync Failed
1. Check GitHub Actions for error details
2. Manually sync: `cp README.md docs/README.md`
3. Commit and push changes
4. Verify CI passes

### CI Validation Failed
1. Check diff output for differences
2. Sync files manually if needed
3. Ensure all required files exist
4. Re-run validation

### GitHub Pages Issues
1. Verify `.nojekyll` file exists
2. Check `index.html` is valid
3. Ensure `README.md` is accessible
4. Wait 5-10 minutes for Pages update

## 📋 Maintenance

### Regular Checks
- Monitor GitHub Actions for sync failures
- Review CI validation results
- Check GitHub Pages deployment status

### Updates
- Keep root `README.md` current
- Let automation handle the rest
- Document any process changes here

## 🔗 Related Documentation

- [GitHub Pages Configuration](./github-pages-setup.md)
- [Documentation Standards](./docs-standards.md)
- [CI/CD Pipeline](./cicd-pipeline.md)
