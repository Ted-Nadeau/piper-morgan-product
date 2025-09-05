# CLI Usage Guide - PM Number Management

## Overview

The `piper issues` command provides comprehensive PM number management with automatic conflict detection and GitHub integration.

## Commands

### `piper issues create` - Create New Issue

Creates a new GitHub issue with an auto-assigned PM number.

**Syntax:**
```bash
python -c "from cli.commands.issues import issues; issues(['create', '--title', 'TITLE', '--body', 'DESCRIPTION', '--labels', 'LABELS', '--dry-run'])"
```

**Options:**
- `--title TEXT` (required): Issue title (max 200 characters)
- `--body TEXT`: Issue description (optional)
- `--labels TEXT`: Comma-separated labels (max 10 labels)
- `--dry-run`: Show what would be created without actually creating

**Examples:**
```bash
# Create a new issue
python -c "from cli.commands.issues import issues; issues(['create', '--title', 'Implement new feature', '--body', 'Add user authentication', '--labels', 'feature,enhancement'])"

# Dry run to preview
python -c "from cli.commands.issues import issues; issues(['create', '--title', 'Test issue', '--dry-run'])"
```

**Features:**
- Auto-assigns next available PM number (PM-140+)
- Prevents duplicate PM numbers across all systems
- Validates input (title length, label count)
- Integrates with GitHub API
- Updates CSV tracking automatically

### `piper issues verify` - Check System Consistency

Verifies PM number consistency across GitHub, CSV, and backlog systems.

**Syntax:**
```bash
python -c "from cli.commands.issues import issues; issues(['verify'])"
```

**Output:**
- Total PM numbers found
- GitHub issues checked
- CSV entries verified
- Inconsistencies detected
- Suggested actions for resolution

**Example Output:**
```
🔍 Verifying PM number consistency...
❌ PM number inconsistencies found!
  Issues found: 103
  - Duplicate PM number in CSV: PM-056
  - PM number PM-006 exists in CSV but not found in GitHub issues
  - PM number PM-124 in CSV missing GitHub issue number

💡 Suggested actions:
  - Run 'issues sync' to synchronize systems
  - Check GitHub issues for missing PM numbers
  - Verify CSV file format and completeness
```

### `piper issues sync` - Synchronize Systems

Synchronizes PM numbers across all tracking systems.

**Syntax:**
```bash
python -c "from cli.commands.issues import issues; issues(['sync', '--dry-run'])"
```

**Options:**
- `--dry-run`: Show what would be synced without making changes

**Features:**
- Syncs GitHub issues ↔ CSV file
- Syncs CSV file ↔ Backlog.md
- Resolves numbering conflicts
- Updates missing PM numbers
- Fixes duplicate PM numbers

## Error Handling

### Input Validation Errors

**Empty Title:**
```
❌ Error: Issue title cannot be empty
💡 Please provide a meaningful title for the issue
```

**Title Too Long:**
```
❌ Error: Issue title too long (max 200 characters)
💡 Current length: 250 characters
```

**Too Many Labels:**
```
❌ Error: Too many labels (max 10)
💡 Current count: 15 labels
```

### System Integration Errors

**GitHub Authentication:**
```
❌ Error: GitHub authentication failed
💡 Please run: gh auth login
```

**PM Number Conflicts:**
```
❌ Error: PM number PM-140 validation failed
   ⚠️  PM number already exists in CSV
   💡 Try using: PM-141
```

## Common Workflows

### 1. Create New Issue
```bash
# Step 1: Verify current system state
python -c "from cli.commands.issues import issues; issues(['verify'])"

# Step 2: Create issue with dry-run first
python -c "from cli.commands.issues import issues; issues(['create', '--title', 'My New Feature', '--dry-run'])"

# Step 3: Create actual issue
python -c "from cli.commands.issues import issues; issues(['create', '--title', 'My New Feature', '--body', 'Implementation details', '--labels', 'feature,enhancement'])"
```

### 2. Resolve System Inconsistencies
```bash
# Step 1: Check for issues
python -c "from cli.commands.issues import issues; issues(['verify'])"

# Step 2: Sync systems
python -c "from cli.commands.issues import issues; issues(['sync'])"

# Step 3: Verify resolution
python -c "from cli.commands.issues import issues; issues(['verify'])"
```

### 3. Bulk Issue Management
```bash
# Check system status
python -c "from cli.commands.issues import issues; issues(['verify'])"

# Sync all systems
python -c "from cli.commands.issues import issues; issues(['sync'])"

# Create multiple issues
python -c "from cli.commands.issues import issues; issues(['create', '--title', 'Issue 1', '--labels', 'bug'])"
python -c "from cli.commands.issues import issues; issues(['create', '--title', 'Issue 2', '--labels', 'feature'])"
```

## Troubleshooting

### Common Issues

**1. Module Import Errors**
- Ensure you're in the project root directory
- Activate virtual environment: `source venv/bin/activate`
- Check Python path: `PYTHONPATH=. python -c "..."`

**2. GitHub Authentication Issues**
- Check authentication: `gh auth status`
- Re-authenticate if needed: `gh auth login`
- Verify repository access: `gh repo view mediajunkie/piper-morgan-product`

**3. CSV File Issues**
- Check file permissions: `ls -la docs/planning/pm-issues-status.csv`
- Verify file format: `head -5 docs/planning/pm-issues-status.csv`
- Ensure file is writable: `chmod 644 docs/planning/pm-issues-status.csv`

**4. PM Number Conflicts**
- Run verification: `python -c "from cli.commands.issues import issues; issues(['verify'])"`
- Check for duplicates in CSV
- Use sync command to resolve conflicts

### Performance Notes

- Issue creation: < 2 seconds
- Verification: < 5 seconds (depends on GitHub API rate limits)
- Synchronization: < 10 seconds (depends on data volume)

### Best Practices

1. **Always use dry-run first** for new issues
2. **Verify system state** before making changes
3. **Sync regularly** to maintain consistency
4. **Use descriptive titles** (50-100 characters)
5. **Limit labels** to 3-5 most relevant ones
6. **Check authentication** before bulk operations

## Integration with Code Agent Services

The CLI integrates with:
- **PMNumberManager**: PM number generation and validation
- **GitHubAgent**: GitHub API integration
- **CSV Tracking**: Automatic updates to pm-issues-status.csv
- **Backlog Integration**: Cross-reference with backlog.md

All services are automatically initialized and configured through the CLI interface.