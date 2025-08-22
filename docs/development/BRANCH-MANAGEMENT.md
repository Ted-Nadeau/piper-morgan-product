# Branch Management Guidelines

## 🌿 **Branch Strategy Overview**

Piper Morgan uses a **feature branch workflow** with **main branch protection** for major milestones and infrastructure changes.

## 📋 **Branch Types & Naming**

### **Main Branch** (`main`)

- **Purpose**: Production-ready code and major milestones
- **Protection**: Direct commits discouraged
- **Merge Policy**: Feature branches only after review/completion
- **Examples**:
  - Chief Architect Phase 1 ✅ (infrastructure milestone)
  - PM-034 Conversation API ✅ (major feature)
  - Bug fixes and hotfixes

### **Feature Branches** (`feature/*`)

- **Purpose**: Development of new features or major changes
- **Naming**: `feature/pm-XXX-description` or `feature/component-name`
- **Examples**:
  - `feature/pm-033d-core-coordination`
  - `feature/pm-033d-testing-ui`
  - `feature/smoke-test-infrastructure`

### **Development Branches** (`dev/*`)

- **Purpose**: Ongoing development work and experiments
- **Naming**: `dev/component-name` or `dev/experiment-name`
- **Examples**:
  - `dev/test-coverage-augmentation`
  - `dev/pattern-discovery`

### **Release Branches** (`release/*`)

- **Purpose**: Release preparation and stabilization
- **Naming**: `release/version-number`
- **Examples**:
  - `release/v1.0.0`
  - `release/v0.2.0`

## 🔄 **Branch Lifecycle**

### **1. Creation**

```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/pm-XXX-description

# Create development branch
git checkout -b dev/component-name
```

### **2. Development**

- **Commit frequently** with clear, descriptive messages
- **Keep up to date** with main: `git rebase main` or `git merge main`
- **Use conventional commits**: `feat:`, `fix:`, `docs:`, `refactor:`
- **Test before committing**: Automated pre-commit hooks run smoke tests (<5s)
- **Test before pushing**: Automated pre-push hooks run fast test suite (<30s)

### **3. Completion & Merge**

```bash
# Option A: Direct merge to main (for major milestones)
git checkout main
git merge feature/branch-name
git push origin main

# Option B: Create pull request (for review)
git push origin feature/branch-name
# Create PR on GitHub, then merge after review
```

## 🎯 **Merge Decision Matrix**

### **Direct Merge to Main** ✅

- **Major Infrastructure**: pytest.ini, testing frameworks
- **Critical Bug Fixes**: Security, production issues
- **Documentation**: Major docs, changelog updates
- **Examples**: Chief Architect Phase 1, pytest.ini, smoke test runner

### **Pull Request Required** 📋

- **New Features**: User-facing functionality
- **API Changes**: Breaking changes, new endpoints
- **Complex Refactoring**: Major code restructuring
- **Examples**: PM-034 features, new integrations

### **Development Branch Only** 🔬

- **Experiments**: Proof of concepts, research
- **Work in Progress**: Incomplete features
- **Testing**: New approaches, methodologies

## 🚀 **Current Branch Status** (August 19, 2025)

### **Active Branches**

```
main                              1ec12a1b ✅ Chief Architect Phase 1 Complete
feature/pm-033d-core-coordination ee620e65 [ahead 3] Core coordination work
feature/pm-033d-testing-ui        a2d3f2d9 ✅ PM-033d Phase 4 Complete
test-coverage-augmentation        1ec12a1b ✅ Merged to main
```

### **Branch Health**

- **main**: ✅ **CLEAN** - Up to date with latest infrastructure
- **feature/pm-033d-core-coordination**: ⚠️ **3 commits ahead** - Needs attention
- **feature/pm-033d-testing-ui**: ✅ **COMPLETE** - Ready for merge consideration

## 📝 **Commit Message Standards**

### **Conventional Commits**

```bash
feat: add new feature
fix: resolve bug
docs: update documentation
refactor: restructure code
test: add or update tests
chore: maintenance tasks
```

### **Examples from This Session**

```bash
feat: Chief Architect Phase 1 - Smoke Test Infrastructure Complete
docs: add comprehensive testing README and changelog
test: mark 14 database-independent tests with smoke markers
```

## 🔧 **Branch Maintenance**

### **Weekly Cleanup**

```bash
# Check for stale branches
git branch --merged main
git branch --no-merged main

# Clean up merged branches
git branch -d feature/completed-feature
git push origin --delete feature/completed-feature
```

### **Keeping Branches Current**

```bash
# Update feature branch with main
git checkout feature/your-branch
git rebase main
# or
git merge main
```

## ⚠️ **Common Pitfalls & Solutions**

### **Pitfall 1: Working on Wrong Branch**

```bash
# Check current branch
git branch

# If wrong, stash changes and switch
git stash
git checkout correct-branch
git stash pop
```

### **Pitfall 2: Outdated Feature Branch**

```bash
# Update with main
git checkout feature/your-branch
git rebase main
# Resolve conflicts if any
```

### **Pitfall 3: Forgetting to Push**

```bash
# Check status
git status

# Push if needed
git push origin feature/your-branch
```

## 🎯 **Immediate Actions Needed**

### **This Week**

1. **Review `feature/pm-033d-core-coordination`** - 3 commits ahead, needs attention
2. **Consider merging `feature/pm-033d-testing-ui`** - Phase 4 complete
3. **Clean up `test-coverage-augmentation`** - Now merged to main

### **Next Session**

1. **Establish branch review process** for feature merges
2. **Set up branch protection rules** on main
3. **Create branch templates** for consistent naming

## 📚 **Resources & References**

- **Conventional Commits**: https://www.conventionalcommits.org/
- **Git Flow**: https://nvie.com/posts/a-successful-git-branching-model/
- **GitHub Flow**: https://guides.github.com/introduction/flow/

---

## 🏁 **Quick Reference**

### **Daily Workflow**

```bash
git checkout main                    # Start from main
git pull origin main                # Get latest
git checkout -b feature/new-work    # Create feature branch
# ... work and commit ...
# (smoke tests run automatically on commit via pre-commit hook)
git checkout main                   # Switch back to main
git merge feature/new-work          # Merge when ready
# (fast tests run automatically on push via pre-push hook)
git push origin main                # Push to remote
git branch -d feature/new-work      # Clean up local
```

### **Manual Test Commands**

```bash
./scripts/run_tests.sh smoke     # <5s validation before commits
./scripts/run_tests.sh fast      # <30s validation before pushes
./scripts/run_tests.sh full      # Complete test suite for releases
./scripts/run_tests.sh coverage  # Coverage analysis for quality audits
```

### **Emergency Fixes**

```bash
git checkout main
git checkout -b hotfix/critical-fix
# ... fix and commit ...
git checkout main
git merge hotfix/critical-fix
git push origin main
git branch -d hotfix/critical-fix
```

---

_Last Updated: August 19, 2025 - Chief Architect Phase 1 Implementation Complete_
_Branch Management Guidelines Established_
