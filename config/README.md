# Piper Morgan Configuration

This directory contains the configuration system for Piper Morgan AI Assistant.

## 📁 **File Structure**

```
config/
├── README.md                 # This documentation
├── PIPER.defaults.md         # Product defaults (versioned)
├── PIPER.user.md.example     # User template (versioned)
├── PIPER.user.md             # Your personal config (gitignored)
└── PIPER.md                  # Legacy config (to be removed)
```

## 🚀 **Quick Setup**

### First Time Setup
1. Copy the template to create your personal configuration:
   ```bash
   cp config/PIPER.user.md.example config/PIPER.user.md
   ```

2. Edit `config/PIPER.user.md` with your personal information:
   - Name, role, timezone
   - Current projects and priorities
   - Working hours and preferences
   - Communication style

3. Save the file - Piper Morgan will automatically use your configuration.

### Configuration Updates
- Edit `config/PIPER.user.md` anytime to update your context
- Changes take effect immediately (hot-reload)
- Your user config is private and never committed to git

## 🏗️ **Architecture**

### Configuration Priority
1. **User Configuration** (`PIPER.user.md`) - Your personal settings
2. **Product Defaults** (`PIPER.defaults.md`) - Fallback values
3. **System Defaults** - Hard-coded minimums

### Separation of Concerns
- **Product Configuration**: System behavior, templates, technical specs
- **User Configuration**: Personal context, projects, preferences
- **Privacy**: User configs are gitignored for clean multi-user deployments

## 📝 **Configuration Files**

### PIPER.defaults.md
- **Purpose**: Product defaults and system configuration
- **Maintenance**: Maintained by development team
- **Version Control**: Tracked in git, versioned with releases
- **Content**: System templates, performance specs, default patterns

### PIPER.user.md.example
- **Purpose**: Template for user configuration
- **Maintenance**: Updated when new configuration options are added
- **Version Control**: Tracked in git as documentation
- **Content**: Complete template with customization instructions

### PIPER.user.md
- **Purpose**: Your personal configuration
- **Maintenance**: Maintained by you
- **Version Control**: Gitignored (private)
- **Content**: Your name, projects, priorities, preferences

## 🔧 **Customization Guide**

### Essential Customizations
- [ ] **Name & Role**: Update identity information
- [ ] **Timezone**: Set your local timezone
- [ ] **Working Hours**: Define your schedule
- [ ] **Current Projects**: List active work with allocations
- [ ] **Priorities**: Rank your standing priorities

### Notion Integration Setup
- [ ] **ADR Database ID**: Configure database for Architecture Decision Records
- [ ] **Default Parent Page**: Set default parent for published content
- [ ] **Test Parent Page**: Set parent for testing scenarios
- [ ] **Validation Level**: Choose basic, enhanced, or full validation

### Advanced Customizations
- [ ] **Communication Style**: Define preferred interaction patterns
- [ ] **Calendar Patterns**: Set up recurring meetings and routines
- [ ] **Knowledge Sources**: Link to your documentation and resources
- [ ] **Success Metrics**: Define how you measure progress

## 🚚 **MVP Shipping Benefits**

### Clean Installations
- New users copy template and customize
- No personal data in repository
- Consistent onboarding experience

### Multi-User Support
- Each user maintains private configuration
- Product updates don't affect user settings
- Clean separation of concerns

### Privacy & Security
- User configurations never committed
- Personal information stays local
- Repository stays clean and professional

## 🔍 **Troubleshooting**

### Common Issues

**Piper Morgan not using my configuration**
- Check file location: `config/PIPER.user.md`
- Verify file format matches template
- Check for YAML formatting errors

**Configuration not updating**
- Save the file and try again (hot-reload enabled)
- Check file permissions
- Restart Piper Morgan if needed

**Personal information in git**
- Check `.gitignore` includes `config/PIPER.user.md`
- Remove from git: `git rm --cached config/PIPER.user.md`
- Recommit with proper gitignore

### Getting Help
- Review `PIPER.user.md.example` for complete template
- Check `PIPER.defaults.md` for system configuration
- Create GitHub issue for configuration problems

## 📊 **Configuration Validation**

### File Verification
```bash
# Check file structure
ls -la config/

# Verify gitignore working
git status | grep PIPER.user.md  # Should return nothing

# Validate Notion configuration
PYTHONPATH=. python -c "
from config.notion_user_config import NotionUserConfig
from pathlib import Path
config = NotionUserConfig.load_from_user_config(Path('config/PIPER.user.md'))
print('✅ Notion configuration loaded successfully')
print(f'ADR Database: {config.get_database_id(\"adrs\")[:8]}...')
print(f'Default Parent: {config.get_parent_id(\"default\")[:8]}...')
"
```

## 🔗 **Notion Integration Configuration**

### Setup Requirements
1. **Notion API Key**: Set `NOTION_API_KEY` environment variable
2. **Database IDs**: Get 32-character Notion database/page IDs
3. **Configuration File**: Add notion section to `config/PIPER.user.md`

### Configuration Template
Add this section to your `config/PIPER.user.md`:

```yaml
notion:
  # REQUIRED: Core Publishing Configuration
  publishing:
    default_parent: "your-default-parent-page-id"
    enabled: true

  # REQUIRED: ADR Database Configuration
  adrs:
    database_id: "your-adr-database-id"
    enabled: true
    auto_publish: true

  # OPTIONAL: Development & Testing
  development:
    test_parent: "your-test-parent-page-id"
    debug_parent: "your-debug-parent-page-id"
    mock_mode: false

  # OPTIONAL: Validation Settings
  validation:
    level: "basic"  # basic|enhanced|full
    connectivity_check: true
    cache_results: true
```

### ID Format Requirements
- **Notion IDs**: Must be 32-character hexadecimal strings
- **Pattern**: `25[a-f0-9]{30}` (starts with '25', followed by 30 hex chars)
- **Example**: `25e11704d8bf80deaac2f806390fe7da`
- **Get IDs**: Use Notion share links or API tools

### Error Handling
Configuration system provides actionable error messages:
- Missing required fields with resolution steps
- Invalid ID format with pattern examples
- File not found with setup instructions
- API connectivity issues with troubleshooting

### Troubleshooting Notion Configuration

**Configuration not found:**
```bash
# Copy template and configure
cp config/PIPER.user.md.example config/PIPER.user.md
# Edit the notion section with your IDs
```

**Invalid Notion ID format:**
- IDs must be exactly 32 characters
- Must start with '25'
- Only lowercase hex characters (0-9, a-f)
- Get from Notion page/database share URLs

**API connectivity issues:**
- Check NOTION_API_KEY environment variable
- Verify API key has access to specified databases/pages
- Test with simple API call first

### Best Practices
- Update configuration regularly as projects change
- Keep user config file clean and organized
- Use meaningful project names and clear priorities
- Include context that helps Piper understand your work

---

## 🎯 **Migration from Legacy**

If you have an existing `config/PIPER.md`:

1. **Backup** your current file:
   ```bash
   cp config/PIPER.md config/PIPER.md.backup
   ```

2. **Create new user config** from template:
   ```bash
   cp config/PIPER.user.md.example config/PIPER.user.md
   ```

3. **Migrate your personal content** from `PIPER.md.backup` to `PIPER.user.md`

4. **Test** that Piper Morgan works with new configuration

5. **Remove** legacy file once satisfied:
   ```bash
   rm config/PIPER.md config/PIPER.md.backup
   ```

---

**Status**: Configuration Separation Complete ✅
**MVP Ready**: Multi-user deployment supported
**Privacy**: User configurations properly isolated
