# Claude Smart Permissions System

**Date Implemented:** July 27, 2025
**Purpose:** Optimize development workflow while maintaining security through intelligent permission management

## Overview

The Smart Permissions System allows Claude Code to automatically execute safe, read-only operations while requiring explicit permission for potentially destructive or external operations.

## Permission Categories

### 🟢 Auto-Allow Operations (No Permission Required)

These operations are automatically allowed for smooth development flow:

#### Test Execution & Verification
- `pytest` - Run tests with any arguments
- `PYTHONPATH=. pytest` - Run tests with Python path
- `./scripts/tldr_runner.py` - TLDR continuous verification
- `timeout` - Time-limited command execution

#### Read-Only File Operations
- `ls` - List directory contents
- `find` - Search for files
- `grep` / `rg` - Search file contents
- `cat` / `head` / `tail` - Read file contents
- `wc` - Count lines/words
- `which` - Find executables
- `pwd` - Show current directory
- `tree` - Display directory structure

#### Safe Environment Queries
- `echo` - Display text
- `env | grep` - Check environment variables
- `python --version` - Check Python version
- `node --version` - Check Node version

#### Git Read Operations
- `git status` - Check repository status
- `git log` - View commit history
- `git diff` - View changes
- `git branch` - List branches
- `git remote -v` - View remotes

#### GitHub CLI Read Operations
- `gh repo view` - View repository info
- `gh run list/view` - View workflow runs
- `gh workflow list` - List workflows
- `gh issue list/view` - View issues

#### Docker Read Operations
- `docker ps` - List containers
- `docker images` - List images
- `docker-compose ps` - List compose services

### 🔴 Require Permission Operations

These operations require explicit user permission:

#### File Modifications
- `rm` - Remove files
- `mv` - Move/rename files
- `cp` - Copy files
- `chmod` - Change permissions
- `mkdir` - Create directories

#### Git Write Operations
- `git add` - Stage changes
- `git commit` - Create commits
- `git push` - Push to remote
- `git checkout` - Switch branches
- `git merge` - Merge branches
- `git reset` - Reset changes

#### GitHub CLI Write Operations
- `gh issue create` - Create issues
- `gh pr create` - Create pull requests
- `gh repo set-default` - Change default repo

#### Network & External Services
- `curl` - HTTP requests
- `wget` - Download files
- `WebFetch` - Fetch web content

#### Package Management
- `pip install` - Install Python packages
- `npm install` - Install Node packages
- `npm run` - Run npm scripts

#### Docker Operations
- `docker run` - Run containers
- `docker-compose up/down` - Manage services
- `docker build` - Build images

#### Database Operations
- `alembic` - Database migrations
- `python scripts/init_db.py` - Initialize database

#### Process Management
- `kill` / `pkill` - Terminate processes

#### Environment Modifications
- `source` - Execute shell scripts
- `export` - Set environment variables

### ❌ Explicitly Denied Operations

These operations are always denied for safety:
- `rm -rf` - Recursive force removal
- `sudo` / `su` - Superuser operations
- `> /dev/` - Device file operations
- `dd` - Disk operations
- `format` - Disk formatting

## Configuration

The smart permissions are configured in `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      // Auto-allowed safe operations
    ],
    "deny": [
      // Explicitly denied dangerous operations
    ]
  },
  "smart_permissions": {
    "mode": "restrictive",
    "auto_allow_categories": [...],
    "require_permission_categories": [...],
    "permission_request_template": "Permission requested for {command}: {reason}",
    "log_permission_requests": true
  }
}
```

## Usage Examples

### ✅ Auto-Allowed (No Permission Needed)
```bash
# Run tests
PYTHONPATH=. pytest services/integrations/slack/tests/ -v

# Search codebase
grep -r "pattern" services/ --include="*.py"

# Check git status
git status

# List files
ls -la services/integrations/slack/
```

### ⚠️ Requires Permission
```bash
# Remove file
rm old_file.py
# Claude will ask: "Permission requested for rm old_file.py: Remove outdated file"

# Commit changes
git commit -m "Add feature"
# Claude will ask: "Permission requested for git commit: Create commit for new feature"

# Install package
pip install new-package
# Claude will ask: "Permission requested for pip install: Add required dependency"
```

## Benefits

1. **Faster Development**: No interruptions for common read operations
2. **Safety**: Destructive operations require explicit approval
3. **Transparency**: Clear categorization of operations
4. **Auditability**: Permission requests can be logged
5. **Flexibility**: Easy to adjust categories as needed

## Maintenance

To modify permissions:
1. Edit `.claude/settings.local.json`
2. Move commands between `allow` and commented sections
3. Restart Claude Code session for changes to take effect

## Best Practices

1. **Start Restrictive**: Begin with minimal permissions and add as needed
2. **Review Regularly**: Periodically review permission requests to optimize
3. **Document Changes**: Update this document when modifying permissions
4. **Test Safely**: Use auto-allowed operations to verify before destructive changes
