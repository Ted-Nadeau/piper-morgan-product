# GitHub Development Guide

## Core Principle
All work happens in GitHub. No exceptions. If it's not in GitHub, it doesn't exist.

## Issue Workflow

### Before Starting Work
```bash
# 1. Verify issue exists
gh issue list --search "[TRACK]-[EPIC]"

# 2. Check issue is assigned
gh issue view [issue name]

# 3. If not assigned, assign it
gh issue edit [issue name] --add-assignee @me
```

### During Work
- Update issue description with progress (use comments only for describing new information)
- Seek permission to check boxes as tasks complete
- Provide evidence (test output, file changes)
- Link related PRs if any

### Evidence Requirements
Every claim needs proof:
```bash
# Show test results
pytest tests/test_feature.py -v

# Show file changes
git diff services/feature.py

# Show pattern discovery
grep -r "pattern" services/
```

## Creating Issues

### Manual Creation
```bash
# Create with title and body
gh issue create \
  --title "[TRACk]-[EPIC]: Feature Title" \
  --body "Description here" \
  --label "enhancement"
```

## Pull Request Standards

### PR Description Template
```markdown
## Summary
Brief description of changes

## Related Issue
Closes #PM-XXX

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Evidence
```
[Paste test output here]
```
```

## Common Workflows

### Fix Implementation
```bash
# 1. Start from issue
gh issue view [issue name]

# 2. Create branch
git checkout -b fix/issue-description

# 3. Make changes with TDD
# Write tests first, then implementation

# 4. Commit with reference
git commit -m "fix([issue]): Description of fix"

# 5. Create PR
gh pr create --fill
```

### Feature Development
```bash
# 1. Verify feature issue exists
gh issue view [issue name]

# 2. Create feature branch
git checkout -b feature/issue-name

# 3. Implement with evidence
# Keep terminal output for PR

# 4. Update issue with progress
gh issue comment PM-XXX --body "Implementation complete, tests passing"

# 5. Create PR with evidence
gh pr create --title "feat(issue name): Feature name" \
  --body "[Include test output and evidence]"
```

## Issue Management

### Status Updates
```bash
# Add labels
gh issue edit [issue name] --add-label "in-progress"

# Add comment with evidence
gh issue comment [issue name] --body "Tests passing: [paste output]"

# Close with comment
gh issue close [issue name] --comment "Completed in PR #123"
```

### Searching Issues
```bash
# Find by status
gh issue list --label "in-progress"

# Find by assignee
gh issue list --assignee @me

# Search by text
gh issue list --search "workflow"
```

## Best Practices

### DO ✅
- Create issue BEFORE starting work
- Update issue description as you progress
- Include evidence in comments
- Link PRs to issues
- Use consistent PM-XXX numbering

### DON'T ❌
- Work without an issue
- Close issues without evidence
- Create duplicate issues
- Skip testing requirements
- Forget to update status

## Integration with CSV Tracking

Keep `pmissuesstatus.csv` synchronized:
```bash
# After creating issue
echo "[issue name],Issue#,Title,Open" >> pmissuesstatus.csv

# After closing issue
# Update status to "Closed" in CSV
```

## Troubleshooting

### Authentication Issues
```bash
# Login to GitHub
gh auth login

# Check auth status
gh auth status
```

### Issue Not Found
```bash
# Verify you're in right repo
gh repo view

# List all issues
gh issue list --limit 100
```

### Automation Script Errors
```bash
# Check Python version (needs 3.6+)
python --version

# Verify backlog format
grep "PM-" docs/planning/backlog.md

# Run in dry-run mode first
python scripts/generate_github_issues.py --dry-run
```


---

*Last Updated: September 23, 2025*
*Version: 3.0 - Updated doc locations and removed PM-XXX references*
