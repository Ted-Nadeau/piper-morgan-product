# Issue Generation & Sync Workflow

## Overview

This document describes the automated workflow for generating GitHub issues from the Piper Morgan backlog and keeping them in sync.

## Current State

- **Next Available Issue Number**: PM-035 (Test Infrastructure Isolation Fix)
- **Total Issues in Backlog**: 19 PM-XXX tickets
- **Script Location**: `scripts/generate_github_issues.py`

## Workflow Steps

### Step 1: Find Next Available Issue Number

```bash
# Search backlog for highest PM number
grep -o "PM-[0-9]\+" docs/planning/backlog.md | sort -V | uniq | tail -5
```

**Current Result**: PM-034 is the highest, so PM-035 is next available.

### Step 2: Create New Issues in Backlog

When creating new issues:

1. Use the next available PM number
2. Follow the standard format:

   ```markdown
   ### PM-XXX: Issue Title

   **Story**: As a [role], I want [capability] so [benefit]
   **Description**: Brief description of the work
   **Estimate**: X points | **Status**: Ready | **Dependencies**: None

   **Implementation Details**:

   - Detail 1
   - Detail 2

   **Success Criteria**:

   - [ ] Criterion 1
   - [ ] Criterion 2
   ```

### Step 3: Generate GitHub Issues

Use the automated script to create GitHub issues from backlog:

```bash
# Check what issues exist in GitHub
python scripts/generate_github_issues.py --check-existing

# Generate commands for missing issues (dry run)
python scripts/generate_github_issues.py --dry-run

# Generate and execute commands (requires gh auth login)
python scripts/generate_github_issues.py
```

## Script Features

### `scripts/generate_github_issues.py`

**Capabilities**:

- Parses `docs/planning/backlog.md` for PM-XXX tickets
- Checks existing GitHub issues via GitHub CLI
- Generates `gh issue create` commands for missing issues
- Handles authentication gracefully
- Supports dry-run mode for preview

**Usage**:

```bash
# Check existing issues only
python scripts/generate_github_issues.py --check-existing

# Preview commands without executing
python scripts/generate_github_issues.py --dry-run

# Generate and execute commands
python scripts/generate_github_issues.py

# Use custom backlog file
python scripts/generate_github_issues.py --backlog path/to/backlog.md
```

**Requirements**:

- Python 3.6+
- GitHub CLI (`gh`) for checking existing issues
- GitHub authentication (`gh auth login`) for creating issues

## Issue Format Mapping

The script maps backlog format to GitHub issues:

| Backlog Field                 | GitHub Field | Notes                |
| ----------------------------- | ------------ | -------------------- |
| `### PM-XXX: Title`           | `--title`    | Prefixed with PM-XXX |
| `**Story**: ...`              | Body         | First line           |
| `**Description**: ...`        | Body         | Second line          |
| `**Status**: ...`             | Body         | Included in body     |
| `**Estimate**: ...`           | Body         | Included in body     |
| `**Dependencies**: ...`       | Body         | Included in body     |
| `**Implementation Details**:` | Body         | Bullet points        |
| N/A                           | `--label`    | Always "enhancement" |

## Recent Additions

### PM-035: Test Infrastructure Isolation Fix

**Created**: July 16, 2025
**Status**: Ready
**Priority**: High (blocks reliable development)

**Key Points**:

- Fixes ~31 phantom test failures
- Improves test suite reliability from 85.5% to 95%+
- Focuses on infrastructure, not business logic
- Enables confident development workflow

## Maintenance

### Regular Tasks

1. **Weekly**: Run `--check-existing` to see sync status
2. **Before Sprints**: Generate missing issues
3. **After Backlog Updates**: Re-run generation

### Troubleshooting

**GitHub CLI Not Found**:

```bash
# Install GitHub CLI
brew install gh  # macOS
# or visit https://cli.github.com/
```

**Authentication Issues**:

```bash
# Login to GitHub
gh auth login
```

**Script Errors**:

- Check Python version (3.6+ required)
- Verify backlog.md format matches expected pattern
- Review error messages for specific issues

## Future Enhancements

### Planned Improvements

1. **Bidirectional Sync**: Update backlog from GitHub issue changes
2. **Status Tracking**: Automatically update issue status based on GitHub
3. **Label Mapping**: Map backlog priorities to GitHub labels
4. **Milestone Integration**: Link issues to GitHub milestones
5. **Template Support**: Support different issue templates

### Integration Opportunities

- **CI/CD Pipeline**: Auto-generate issues on backlog changes
- **Slack Notifications**: Alert team of new issues
- **Project Boards**: Auto-add issues to GitHub project boards
- **Release Notes**: Generate release notes from completed issues

## Success Metrics

- **Sync Accuracy**: 100% of backlog issues exist in GitHub
- **Update Frequency**: Issues created within 24 hours of backlog changes
- **Team Adoption**: Consistent use of PM-XXX numbering
- **Maintenance Overhead**: <30 minutes per week for sync tasks

---

_Last Updated: July 16, 2025_
