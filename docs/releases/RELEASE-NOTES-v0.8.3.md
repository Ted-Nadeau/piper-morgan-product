# Release Notes - v0.8.3

**Release Date**: January 2, 2026
**Branch**: production
**Previous Version**: v0.8.2

---

## Summary

This release introduces the **Integration Health Dashboard** and **OAuth connection management** from the Settings page. Alpha testers can now connect Slack and Google Calendar directly from the web UI, monitor integration health status, and manage their connections without touching environment variables. Notion setup is now part of the GUI setup wizard.

---

## What Changed

### 🔌 **Integration Health Dashboard (#530)**

**What It Does**: New dashboard showing real-time health status of all integrations with one-click testing.

**Access**: Settings → Integrations (http://localhost:8001/settings/integrations)

**Features**:
- Real-time health status for Slack, Calendar, GitHub, Notion
- One-click "Test" button for each integration
- "Test All" button for comprehensive health check
- Visual status indicators (healthy, degraded, failed, not configured)
- Error messages with fix suggestions

**Why This Matters**:
- No more guessing if integrations are working
- Quick diagnosis when something breaks
- Professional integration management UI
- Reduces support burden for alpha testers

**Files Changed**:
- `web/api/routes/integrations.py` - Health check endpoints
- `templates/integrations.html` - Dashboard UI
- `scripts/status_checker.py` - CLI integration checks

---

### 🔗 **Settings OAuth Connection Management (#528, #529)**

**What It Does**: Connect and disconnect Slack and Google Calendar directly from the Settings page.

**Access**: Settings → Integrations → Click "Connect" button

**New Features**:
- **Slack Connect**: One-click OAuth flow to connect your Slack workspace
- **Calendar Connect**: One-click OAuth flow to connect Google Calendar
- **Disconnect**: Revoke integration access with confirmation dialog
- **Status Display**: See connected account details (workspace name, email)

**Technical Details**:
- OAuth 2.0 web server flow with PKCE
- State tokens for CSRF protection (15-minute expiry)
- Refresh tokens stored in secure keychain
- Session-independent OAuth (works even if logged out)

**Why This Matters**:
- No more editing environment variables for integrations
- Connect integrations without restarting the server
- Disconnect and reconnect anytime
- Visual confirmation of connection status

**Files Changed**:
- `web/api/routes/settings_integrations.py` - NEW: OAuth endpoints
- `services/integrations/calendar/oauth_handler.py` - NEW: Calendar OAuth
- `services/auth/auth_middleware.py` - Auth-exempt OAuth paths

---

### 📝 **Notion Setup in Wizard (#527)**

**What It Does**: Configure Notion API key during initial setup with automatic validation.

**Where**: Setup wizard Step 2 (API Keys)

**Features**:
- Notion API key input field in setup wizard
- Real-time validation using Notion SDK
- Workspace name display on successful connection
- Secure storage in system keychain

**Why This Matters**:
- Complete integration setup during initial onboarding
- No separate Notion configuration step needed
- Validation ensures key works before saving

**Files Changed**:
- `scripts/setup_wizard.py` - Notion validation logic
- `web/api/routes/setup.py` - Notion validation endpoint
- `templates/setup.html` - Notion card in UI
- `web/static/js/setup.js` - Notion handling

---

### 🐛 **Bug Fixes**

1. **Calendar OAuth State Fix (#529)**
   - Problem: "State not found" errors on Calendar OAuth callback
   - Cause: Each HTTP request created new handler with empty state dict
   - Fix: Module-level singleton pattern for state persistence
   - Result: Calendar OAuth works reliably

2. **Toast Visibility Fix (#530)**
   - Problem: Toast notifications invisible on integrations page
   - Cause: Missing `tokens.css` include (z-index variable undefined)
   - Fix: Added CSS include, increased duration to 7 seconds
   - Result: Toasts visible and readable

3. **Breadcrumb Overlap Fix (#530)**
   - Problem: Breadcrumbs overlapping with navigation
   - Fix: CSS layout adjustments
   - Result: Clean navigation header

4. **Auth Bypass Test Fix (#502)**
   - Problem: Test failing due to missing auth fixtures
   - Fix: Added proper auth context to test
   - Result: All tests passing

---

## For Alpha Testers

### 🎯 **What to Test Now**

**New Features** (focus testing here):
- 🔍 **Integration Dashboard**: Visit Settings → Integrations
- 🔍 **Slack Connect**: Click "Connect" on Slack card
- 🔍 **Calendar Connect**: Click "Connect" on Calendar card
- 🔍 **Notion in Setup**: Re-run setup wizard to test Notion

**Working Features** (stable):
- ✅ Setup wizard (now with Notion)
- ✅ Login/authentication
- ✅ Chat interface
- ✅ Lists, Todos, Projects CRUD
- ✅ File upload/download

### ✅ **What You Should See After Pulling**

```bash
# 1. Pull production branch
git checkout production
git pull origin production

# 2. Verify version
grep version pyproject.toml
# Should show: version = "0.8.3"

# 3. Restart server
python main.py

# 4. Visit Integration Dashboard
# Navigate to: http://localhost:8001/settings/integrations
# You should see cards for Slack, Calendar, GitHub, Notion
# Each card has Test/Connect/Disconnect buttons
```

### 🆕 **Try the New Integration Features**

1. **Test Integration Health**
   - Go to Settings → Integrations
   - Click "Test All" button
   - Observe status updates for each integration

2. **Connect Slack** (if you have a Slack workspace)
   - Click "Connect" on Slack card
   - Authorize in Slack OAuth popup
   - Return to see "Connected" status with workspace name

3. **Connect Calendar** (if you have Google Calendar)
   - Click "Connect" on Calendar card
   - Authorize in Google OAuth popup
   - Return to see "Connected" status with email

4. **Disconnect an Integration**
   - Click "Disconnect" on a connected integration
   - Confirm in dialog
   - Status changes back to "Not Configured"

---

## Files Changed

### Major Changes
1. `web/api/routes/settings_integrations.py` - NEW: OAuth connect/disconnect endpoints
2. `services/integrations/calendar/oauth_handler.py` - NEW: Calendar OAuth handler
3. `templates/integrations.html` - Integration health dashboard UI
4. `web/api/routes/integrations.py` - Health check endpoints

### Bug Fixes
5. `services/auth/auth_middleware.py` - Auth-exempt OAuth paths
6. `web/static/js/toast.js` - 7s duration for readability
7. `templates/integrations.html` - Toast CSS fix

### Setup Wizard
8. `scripts/setup_wizard.py` - Notion validation
9. `web/api/routes/setup.py` - Notion endpoint
10. `templates/setup.html` - Notion card
11. `web/static/js/setup.js` - Notion handling

### Tests
12. `tests/unit/web/api/routes/test_integrations.py` - NEW
13. `tests/unit/web/api/routes/test_setup_calendar.py` - NEW
14. `tests/unit/web/api/routes/test_setup_notion.py` - NEW
15. `tests/unit/web/api/routes/test_setup_slack.py` - NEW
16. `tests/integration/test_integrations_dashboard.py` - NEW

### Configuration
17. `pyproject.toml` - Version bump 0.8.2 → 0.8.3

---

## Technical Details

### Deployment Process

**Timeline**: December 28, 2025 - January 2, 2026

**Phase 1: Feature Development (Dec 28-31)**
- Integration health dashboard (#530)
- Notion setup wizard (#527)
- Calendar OAuth (#529)
- Slack OAuth (#528)

**Phase 2: Bug Fixes (Jan 1)**
- Toast visibility fix
- Calendar state persistence fix
- Auth middleware updates

**Phase 3: Release (Jan 2)**
- Version bump to 0.8.3
- Release notes
- Alpha documentation updates
- Production deployment

### Rollback Path (if needed)

```bash
# If critical issue discovered post-deployment:
git checkout production
git reset --hard v0.8.2
git push origin production --force-with-lease

# Then notify PM immediately
```

**Previous stable version**: v0.8.2

---

## Known Issues

**Pre-existing issues** (carried forward from v0.8.2):
- Encryption at rest not yet implemented (S2 security phase pending)
- 1 test occasionally fails due to API quota limits

**New issues**: None reported during development.

---

## Next Steps for Alpha Testing

1. **Pull this release** on your alpha laptop
2. **Visit Integration Dashboard** to see health status
3. **Try connecting integrations** (Slack, Calendar)
4. **Report any OAuth issues** - these are the newest features
5. **Test workflows** as usual (lists, todos, files)

---

## Support

If you encounter issues after updating:

1. **OAuth not working**: Check browser console for errors, ensure popup blockers are disabled
2. **Toast not visible**: Hard refresh (Cmd+Shift+R) to reload CSS
3. **Integration stuck**: Try Disconnect → Connect again
4. **Version mismatch**: Verify with `grep version pyproject.toml`
5. **Need help**: Report in #piper-alpha Slack channel or create GitHub issue

---

## Commits in This Release

**Integration Dashboard (#530)**:
- `1f741f57` - feat(#530): Integration health check dashboard
- `1ef9e5a2` - fix(#530): Fix breadcrumb overlap with navigation
- `d4917fc9` - fix(#530): Include toast component for notifications
- `12c46378` - fix(#530): Toast visibility on integrations page
- `eff39a61` - feat(#530): Integrations dashboard enhancements

**OAuth Connections (#528, #529)**:
- `3ff2fecd` - fix(#529): Calendar OAuth state persistence via module-level singleton
- `12f3c9dd` - feat(#528): Settings integrations OAuth endpoints

**Notion Setup (#527)**:
- `a240143a` - feat(#527): Add Notion API key validation to setup wizard

**Tests**:
- `5c4cae6d` - test(#527-530): Add tests for setup and integrations
- `8a99631a` - fix(#502): Add auth fixtures to test_bypass_prevention.py

**Documentation**:
- `7b13c7da` - docs: Add session logs and omnibus logs (Dec 24 - Jan 1)
- Multiple session logs and omnibus logs

**Full changelog**: [v0.8.2...v0.8.3](https://github.com/mediajunkie/piper-morgan-product/compare/v0.8.2...v0.8.3)

---

**Questions?** Contact PM (xian) or refer to this release notes document.
