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

# Validate configuration loaded
# (Configuration validation commands will be added)
```

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
