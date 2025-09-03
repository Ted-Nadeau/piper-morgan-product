# Migration from Hardcoded Values to Configuration

**Date**: August 30, 2025
**Context**: Moving from system-level hardcoded Notion values to user-level configuration
**Target**: Complete migration to PIPER.user.md configuration structure

## Overview

This migration guide provides step-by-step instructions for moving from hardcoded Notion workspace values to a flexible, user-specific configuration system. The new system supports multi-user adoption and eliminates the need for code changes when workspace details change.

## Migration Benefits

- **Multi-user Support**: Each user can have their own Notion workspace configuration
- **Flexibility**: Easy to switch between different Notion workspaces
- **Maintainability**: No code changes required for workspace updates
- **Validation**: Built-in configuration validation prevents common errors
- **Documentation**: Clear error messages with actionable resolution steps

## Step-by-Step Migration Process

### 1. Create User Configuration File

```bash
# Copy the example configuration
cp config/PIPER.user.md.example config/PIPER.user.md

# Edit the file to add your Notion configuration
nano config/PIPER.user.md
```

### 2. Extract Hardcoded Values (from Phase 1 audit)

Based on the audit findings, here are the specific hardcoded values and their new configuration paths:

| Source File               | Line | Hardcoded Value                    | Configuration Path                 | Risk Level |
| ------------------------- | ---- | ---------------------------------- | ---------------------------------- | ---------- |
| `fields.py`               | 12   | `25e11704d8bf80deaac2f806390fe7da` | `notion.adrs.database_id`          | HIGH       |
| `adr.py`                  | 12   | `25e11704d8bf80deaac2f806390fe7da` | `notion.adrs.database_id`          | HIGH       |
| `test_publish_command.py` | 18   | `25d11704d8bf81dfb37acbdc143e6a80` | `notion.development.test_parent`   | MEDIUM     |
| `test_publish_gaps.py`    | 21   | `25d11704d8bf8135a3c9c732704c88a4` | `notion.development.test_parent`   | MEDIUM     |
| `tests/debug_parent.py`   | 19   | `25d11704d8bf80c8a71ddbe7aba51f55` | `notion.publishing.default_parent` | MEDIUM     |

### 3. Configuration Structure

Add the following configuration to your `config/PIPER.user.md`:

```yaml
notion:
  # REQUIRED: Core Publishing (based on audit findings)
  publishing:
    default_parent: "25d11704d8bf80c8a71ddbe7aba51f55" # From debug_parent.py:19
    enabled: true

  # REQUIRED: ADR Database (HIGH risk from audit)
  adrs:
    database_id: "25e11704d8bf80deaac2f806390fe7da" # From fields.py:12, adr.py:12
    enabled: true
    auto_publish: true

  # OPTIONAL: Workspace Configuration
  workspace:
    id: null # API discovery fallback
    name: "" # Human-readable reference

  # OPTIONAL: Development & Testing
  development:
    test_parent: "25d11704d8bf81dfb37acbdc143e6a80" # From test_publish_command.py:18
    debug_parent: "25d11704d8bf80c8a71ddbe7aba51f55" # From debug_parent.py:19
    mock_mode: false

  # OPTIONAL: Validation Settings (tiered approach)
  validation:
    level: "basic" # basic|enhanced|full
    connectivity_check: true
    cache_results: true
```

### 4. Validation Process

After creating your configuration, validate it using the new CLI commands:

```bash
# Test basic configuration format
piper notion test-config

# Validate configuration with different levels
piper notion validate --level basic      # Format + basic connectivity
piper notion validate --level enhanced   # Resource accessibility
piper notion validate --level full       # Comprehensive permissions
```

### 5. Verification Steps

Verify your configuration works correctly:

```bash
# Test ADR publishing with new configuration
piper publish docs/architecture/adr/adr-026-notion-client-migration.md --to notion --database

# Test page publishing with new configuration
piper publish README.md --to notion --location

# List your Notion pages to verify connectivity
piper notion pages

# Search for content to verify access
piper notion search --query "test"
```

## Configuration Field Details

### Required Fields

#### `notion.adrs.database_id`

- **Purpose**: Database for storing ADR (Architectural Decision Record) items
- **Format**: 32-character hexadecimal string
- **Example**: `25e11704d8bf80deaac2f806390fe7da`
- **Validation**: Must be valid Notion database ID with write access

#### `notion.publishing.default_parent`

- **Purpose**: Default parent page for new content when no specific location is provided
- **Format**: 32-character hexadecimal string
- **Example**: `25d11704d8bf80c8a71ddbe7aba51f55`
- **Validation**: Must be valid Notion page ID with write access

### Optional Fields

#### `notion.workspace.id`

- **Purpose**: Notion workspace identifier for API operations
- **Format**: 32-character hexadecimal string or null
- **Default**: null (auto-discovered from API)
- **Note**: Usually not required unless you need to specify a specific workspace

#### `notion.workspace.name`

- **Purpose**: Human-readable workspace name for reference
- **Format**: String
- **Default**: "" (empty string)
- **Note**: Purely informational, not used by the API

#### `notion.development.test_parent`

- **Purpose**: Parent page for test content during development
- **Format**: 32-character hexadecimal string
- **Default**: null
- **Note**: Useful for isolating test content from production

#### `notion.development.debug_parent`

- **Purpose**: Parent page for debug content and troubleshooting
- **Format**: 32-character hexadecimal string
- **Default**: null
- **Note**: Useful for debugging and development workflows

#### `notion.development.mock_mode`

- **Purpose**: Enable mock mode for testing without real API calls
- **Format**: Boolean
- **Default**: false
- **Note**: Useful for unit testing and development

#### `notion.validation.level`

- **Purpose**: Validation intensity level
- **Format**: "basic" | "enhanced" | "full"
- **Default**: "basic"
- **Note**: Higher levels perform more comprehensive checks

#### `notion.validation.connectivity_check`

- **Purpose**: Whether to test API connectivity during validation
- **Format**: Boolean
- **Default**: true
- **Note**: Disable for offline development

#### `notion.validation.cache_results`

- **Purpose**: Cache validation results for performance
- **Format**: Boolean
- **Default**: true
- **Note**: Useful for repeated validation calls

## Troubleshooting

### Common Issues

#### Configuration Not Found

```
Error: Configuration file not found
Resolution: Ensure config/PIPER.user.md exists and is readable
```

#### Invalid Notion ID Format

```
Error: Invalid database_id format: must be 32 hexadecimal characters
Resolution: Check that your Notion ID is exactly 32 characters long and contains only 0-9 and a-f
```

#### Access Denied

```
Error: Database not accessible: permission denied
Resolution:
1. Verify your NOTION_API_KEY has access to the specified database
2. Check that the database ID is correct
3. Ensure your integration has been added to the database
```

#### Connection Failed

```
Error: Failed to connect to Notion API
Resolution:
1. Check your internet connection
2. Verify NOTION_API_KEY is set correctly
3. Check if Notion API is experiencing issues
```

### Getting Help

If you encounter issues during migration:

1. **Check the logs**: Look for detailed error messages
2. **Validate configuration**: Run `piper notion validate --level basic`
3. **Test connectivity**: Run `piper notion status`
4. **Review documentation**: Check the user guide for configuration details
5. **Create issue**: Report bugs or request help through GitHub issues

## Post-Migration Cleanup

After successful migration:

1. **Remove hardcoded values**: Delete or comment out hardcoded Notion IDs in source files
2. **Update tests**: Ensure all tests use configuration values instead of hardcoded values
3. **Document changes**: Update any relevant documentation to reflect the new configuration approach
4. **Team communication**: Inform team members about the new configuration system

## Future Enhancements

The new configuration system supports future enhancements:

- **Environment-specific configs**: Different configurations for development, staging, and production
- **Team sharing**: Shared configuration templates for common setups
- **Automated validation**: CI/CD integration for configuration validation
- **Configuration management**: Tools for managing multiple configuration profiles

## Summary

This migration transforms the Notion integration from a rigid, single-workspace system to a flexible, multi-user configuration system. The benefits include:

- ✅ **Elimination of hardcoded values**
- ✅ **Support for multiple users and workspaces**
- ✅ **Built-in validation and error handling**
- ✅ **Clear migration path with specific value mappings**
- ✅ **Comprehensive testing and verification**

Follow the step-by-step process above to complete your migration. If you encounter any issues, refer to the troubleshooting section or create a GitHub issue for assistance.
