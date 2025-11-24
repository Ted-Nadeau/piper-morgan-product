# Code Agent Prompt: UX Quick Wins Implementation
## Sprints 1-2 (Foundation & Navigation)

**Date**: November 15, 2025, 7:00 AM PT
**Assigned By**: Xian (PM)
**Agent Role**: Code Agent (Implementation)
**Context**: UX Audit findings - 5 high-priority Quick Wins approved for immediate implementation
**Timeline**: 2 weeks (Sprint 1: Week 1, Sprint 2: Week 2)

---

## Mission: Transform User Experience from 3/10 → 6/10

You are implementing **5 critical UX improvements** that will deliver an **80% reduction in user frustration**. These are the highest-priority gaps from a comprehensive 350+ page UX audit that identified 68 distinct issues.

**Why This Matters**: Users currently can't discover features, don't know if they're logged in, and must memorize URLs. These 5 fixes make Piper **usable** for external alpha users.

---

## Your Resources

### UX Audit Deliverables (Available in Repository)

**You have full access to**:
1. `docs/ux-audit/ux-audit-comprehensive-report.md` (30 pages) - Executive summary
2. `docs/ux-audit/ux-audit-phase1-touchpoint-inventory.md` (18 pages) - All touchpoints
3. `docs/ux-audit/ux-audit-phase1-interaction-patterns.md` (22 pages) - UI patterns
4. `docs/ux-audit/ux-audit-phase1-visual-design-tokens.md` (30 pages) - Color systems
5. `docs/ux-audit/ux-audit-phase4-gap-analysis.md` (50 pages) - All 68 gaps with details
6. `docs/ux-audit/ux-audit-roadmap-synthesis.md` (45 pages) - Integration with Sprint A8

**Key Document**: Start with `ux-audit-phase4-gap-analysis.md` - contains exact specifications for each gap.

### Code Navigation Tools (CRITICAL - USE THESE)

**Serena Symbolic Index** (`docs/NAVIGATION.md`):
- Maps all domain concepts to file locations
- Use `docs/NAVIGATION.md` to understand architecture before making changes
- Example: "Where is user authentication?" → Check Serena → `services/auth_service.py`

**Beads Context Management** (methodology):
- Progressive context loading (don't load everything at once)
- Start narrow (gap specification), expand as needed (related files)
- Use file scoring algorithm to prioritize what to read

**ALWAYS**: Consult `docs/NAVIGATION.md` before implementing any feature to understand existing patterns.

---

## Sprint 1 (Week 1): Foundation & Navigation

### Gap 1 (G1): Global Navigation Menu [PRIORITY 1]

**Score**: 700 (Impact: 10, Frequency: 10, Effort: 7)
**Effort**: 2-3 days
**Status**: CRITICAL - Blocks all other improvements

#### Problem Statement
No navigation menu exists anywhere in the application. Users:
- Can't discover features beyond what they stumble upon
- Must memorize or bookmark URLs manually
- Journey 1 (Onboarding): Can't find features → 😤 Frustrated
- Journey 2 (Daily PM): Must type `/standup` URL manually → 😤 Annoyed

#### Specification

**Create**: `/web/templates/components/navigation.html` (Jinja2 partial)

**Navigation Structure**:
```html
<nav class="global-nav" role="navigation" aria-label="Main navigation">
  <div class="nav-container">
    <!-- Logo/Brand -->
    <a href="/" class="nav-brand">
      <img src="/assets/pmlogo.png" alt="Piper Morgan" class="nav-logo">
      <span class="nav-title">Piper Morgan</span>
    </a>

    <!-- Main Navigation -->
    <ul class="nav-menu">
      <li><a href="/" class="nav-link">Home</a></li>
      <li><a href="/standup" class="nav-link">Standup</a></li>
      <li><a href="/files" class="nav-link">Files</a></li>
      <li><a href="/learning" class="nav-link">Learning</a></li>
      <li><a href="/settings" class="nav-link">Settings</a></li>
    </ul>

    <!-- User Menu (placeholder for G8) -->
    <div class="nav-user" id="user-menu-placeholder">
      <!-- G8 will add logged-in indicator here -->
    </div>
  </div>
</nav>
```

**Styling** (inline in `navigation.html` for now):
```css
<style>
.global-nav {
  background: #ffffff;
  border-bottom: 1px solid #ecf0f1;
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #2c3e50;
  font-weight: 600;
}

.nav-logo {
  height: 32px;
  width: auto;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 32px;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: #2c3e50;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background 0.2s;
}

.nav-link:hover {
  background: #f5f5f5;
}

.nav-link.active {
  background: #e3f2fd;
  color: #3498db;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-menu {
    gap: 16px;
  }
  .nav-link {
    padding: 8px;
    font-size: 14px;
  }
}
</style>
```

**Integration**:
1. Include in ALL page templates: `home.html`, `standup.html`, `learning-dashboard.html`, `personality-preferences.html`
2. Add at top of `<body>` tag: `{% include 'components/navigation.html' %}`
3. Add active state JavaScript to highlight current page

**Active State Logic** (add to each page):
```javascript
<script>
document.addEventListener('DOMContentLoaded', function() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link');

  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (currentPath === href || (currentPath === '/' && href === '/')) {
      link.classList.add('active');
    }
  });
});
</script>
```

**Accessibility Requirements**:
- `role="navigation"` on `<nav>`
- `aria-label="Main navigation"` for screen readers
- Keyboard navigable (Tab works through all links)
- Active state visible with 3:1 contrast ratio

#### Acceptance Criteria

- [ ] Navigation appears on all 4 existing pages (home, standup, learning, personality)
- [ ] Current page is highlighted in navigation
- [ ] Logo links to home page
- [ ] All links work correctly
- [ ] Keyboard navigation works (Tab through links, Enter activates)
- [ ] Responsive on mobile (>= 320px width)
- [ ] Screen reader announces "Main navigation" and all links

#### Testing

**Manual Tests**:
1. Load each page → Navigation appears at top
2. Click each link → Correct page loads + link highlighted
3. Click logo → Returns to home
4. Tab through navigation → Focus visible on each link
5. Press Enter on focused link → Page loads
6. Resize to mobile → Navigation remains usable
7. Test with screen reader → Announces correctly

**Files to Modify**:
- Create: `/web/templates/components/navigation.html`
- Modify: `/web/templates/home.html` (add include)
- Modify: `/web/templates/standup.html` (add include)
- Modify: `/web/templates/learning-dashboard.html` (add include)
- Modify: `/web/templates/personality-preferences.html` (add include)

---

### Gap 8 (G8): Logged-in User Indicator [PRIORITY 2]

**Score**: 630 (Impact: 9, Frequency: 10, Effort: 7)
**Effort**: 4 hours
**Status**: Quick win, builds on G1

#### Problem Statement
Users have no visual confirmation of authentication status. Journey affects:
- Can't see who is logged in (multi-user confusion)
- No obvious path to logout
- No access to account settings

#### Specification

**Modify**: `/web/templates/components/navigation.html` (created in G1)

**Replace** the `<div class="nav-user" id="user-menu-placeholder">` with:

```html
<div class="nav-user">
  <div class="user-menu" id="user-dropdown">
    <button class="user-button" aria-haspopup="true" aria-expanded="false">
      <span class="user-avatar">{{ user.username[0].upper() }}</span>
      <span class="user-name">{{ user.username }}</span>
      <svg class="user-chevron" width="16" height="16" viewBox="0 0 16 16">
        <path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="2" fill="none"/>
      </svg>
    </button>

    <div class="user-dropdown" hidden>
      <a href="/settings" class="dropdown-item">
        <svg width="16" height="16" viewBox="0 0 16 16">
          <path d="M8 10a2 2 0 100-4 2 2 0 000 4z"/>
          <path d="M14 8a6 6 0 11-12 0 6 6 0 0112 0z"/>
        </svg>
        Settings
      </a>
      <a href="/account" class="dropdown-item">
        <svg width="16" height="16" viewBox="0 0 16 16">
          <path d="M8 8a3 3 0 100-6 3 3 0 000 6zM3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3z"/>
        </svg>
        Account
      </a>
      <hr class="dropdown-divider">
      <a href="/logout" class="dropdown-item dropdown-item-danger">
        <svg width="16" height="16" viewBox="0 0 16 16">
          <path d="M10 3.5a.5.5 0 00-.5-.5h-8a.5.5 0 00-.5.5v9a.5.5 0 00.5.5h8a.5.5 0 00.5-.5v-2a.5.5 0 011 0v2A1.5 1.5 0 019.5 14h-8A1.5 1.5 0 010 12.5v-9A1.5 1.5 0 011.5 2h8A1.5 1.5 0 0111 3.5v2a.5.5 0 01-1 0v-2z"/>
          <path d="M15.854 8.354a.5.5 0 000-.708l-3-3a.5.5 0 00-.708.708L14.293 7.5H5.5a.5.5 0 000 1h8.793l-2.147 2.146a.5.5 0 00.708.708l3-3z"/>
        </svg>
        Logout
      </a>
    </div>
  </div>
</div>
```

**Styling** (add to navigation.html `<style>` block):
```css
.nav-user {
  position: relative;
}

.user-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f5f5f5;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.user-button:hover {
  background: #e8e8e8;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #3498db;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.user-name {
  font-size: 14px;
  color: #2c3e50;
  font-weight: 500;
}

.user-chevron {
  color: #7f8c8d;
  transition: transform 0.2s;
}

.user-button[aria-expanded="true"] .user-chevron {
  transform: rotate(180deg);
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 200px;
  background: white;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 8px 0;
  z-index: 1001;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  color: #2c3e50;
  text-decoration: none;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background: #f5f5f5;
}

.dropdown-item svg {
  color: #7f8c8d;
}

.dropdown-item-danger {
  color: #e74c3c;
}

.dropdown-item-danger svg {
  color: #e74c3c;
}

.dropdown-divider {
  margin: 8px 0;
  border: none;
  border-top: 1px solid #ecf0f1;
}
```

**Dropdown Interaction** (add to navigation.html):
```javascript
<script>
document.addEventListener('DOMContentLoaded', function() {
  const userButton = document.querySelector('.user-button');
  const userDropdown = document.querySelector('.user-dropdown');

  if (userButton && userDropdown) {
    userButton.addEventListener('click', function(e) {
      e.stopPropagation();
      const isExpanded = userButton.getAttribute('aria-expanded') === 'true';

      userButton.setAttribute('aria-expanded', !isExpanded);
      userDropdown.hidden = isExpanded;
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function() {
      userButton.setAttribute('aria-expanded', 'false');
      userDropdown.hidden = true;
    });

    // Keyboard support
    userButton.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        userButton.setAttribute('aria-expanded', 'false');
        userDropdown.hidden = true;
      }
    });
  }
});
</script>
```

**Backend Integration**:
- Ensure `user` object is passed to all templates
- Verify `user.username` is available in Jinja2 context
- Check: `services/auth_service.py` for user data

**Logout Endpoint**:
- Verify `/logout` route exists in `web/app.py`
- Should clear session and redirect to login
- If missing, create basic logout handler

#### Acceptance Criteria

- [ ] Username appears in top-right navigation on all pages
- [ ] Avatar shows first letter of username
- [ ] Clicking avatar opens dropdown menu
- [ ] Dropdown contains: Settings, Account, Logout links
- [ ] Clicking outside dropdown closes it
- [ ] Pressing Escape closes dropdown
- [ ] Logout link clears session and redirects to login
- [ ] Keyboard accessible (Tab to button, Enter opens, Arrow keys navigate)

#### Testing

**Manual Tests**:
1. Login → Username appears in navigation
2. Click username → Dropdown opens
3. Click Settings → Settings page loads
4. Click Logout → Logged out, redirected to login
5. Click outside dropdown → Closes
6. Press Escape → Closes
7. Tab to avatar, press Enter → Dropdown opens
8. Arrow down → Focuses first menu item

**Files to Modify**:
- Modify: `/web/templates/components/navigation.html` (add user menu)
- Verify: `/web/app.py` (ensure logout route exists)
- Verify: Template context includes `user` object

---

### Gap 50 (G50): Clear Server Startup Message [PRIORITY 3]

**Score**: 700 (Impact: 10, Frequency: 10, Effort: 7)
**Effort**: 1 hour
**Status**: Developer experience quick win

#### Problem Statement
When starting Piper, developers see minimal output and must:
- Guess which port the server is running on (8001? 8080?)
- Manually navigate to `localhost:8001` in browser
- Check config files to verify settings

Journey Impact: First-time setup confusion, wasted time

#### Specification

**Modify**: `/main.py` (or wherever Uvicorn server starts)

**Replace** the current startup logging with:

```python
import webbrowser
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def start_server():
    """Start the Piper Morgan server with clear messaging"""

    # Get configuration
    host = os.getenv("PIPER_HOST", "localhost")
    port = int(os.getenv("PIPER_PORT", "8001"))
    url = f"http://{host}:{port}"

    # Create startup message
    startup_message = Text()
    startup_message.append("✅ Piper Morgan is running!\n\n", style="bold green")
    startup_message.append(f"🌐 Web Interface: ", style="bold")
    startup_message.append(f"{url}\n", style="cyan underline")
    startup_message.append(f"🔧 API Documentation: ", style="bold")
    startup_message.append(f"{url}/docs\n", style="cyan underline")
    startup_message.append(f"📊 Health Check: ", style="bold")
    startup_message.append(f"{url}/health\n\n", style="cyan underline")
    startup_message.append("Press Ctrl+C to stop the server", style="dim")

    panel = Panel(
        startup_message,
        title="[bold]Piper Morgan Server[/bold]",
        border_style="green",
        padding=(1, 2)
    )

    console.print(panel)

    # Auto-open browser (optional, can be disabled via env var)
    auto_open = os.getenv("PIPER_AUTO_OPEN", "true").lower() == "true"
    if auto_open:
        console.print("🚀 Opening browser...", style="dim")
        webbrowser.open(url)

    # Start Uvicorn
    import uvicorn
    uvicorn.run(
        "web.app:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    start_server()
```

**Environment Variables** (document in `.env.example`):
```bash
# Server Configuration
PIPER_HOST=localhost
PIPER_PORT=8001
PIPER_AUTO_OPEN=true  # Set to 'false' to disable browser auto-open
```

**Fallback** (if `rich` not available):
```python
# Simple version without rich (if import fails)
def start_server_simple():
    host = os.getenv("PIPER_HOST", "localhost")
    port = int(os.getenv("PIPER_PORT", "8001"))
    url = f"http://{host}:{port}"

    print("=" * 60)
    print("✅ Piper Morgan is running!")
    print("")
    print(f"🌐 Web Interface:     {url}")
    print(f"🔧 API Documentation: {url}/docs")
    print(f"📊 Health Check:      {url}/health")
    print("")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print("")

    if os.getenv("PIPER_AUTO_OPEN", "true").lower() == "true":
        import webbrowser
        webbrowser.open(url)

    import uvicorn
    uvicorn.run("web.app:app", host=host, port=port, reload=True)
```

#### Acceptance Criteria

- [ ] Starting server prints clear, formatted message
- [ ] Message shows exact URL to access (http://localhost:8001)
- [ ] Shows links to: web interface, API docs, health check
- [ ] Browser auto-opens to web interface (can be disabled)
- [ ] Works with different port configurations
- [ ] Fallback works if `rich` not installed

#### Testing

**Manual Tests**:
1. Stop server if running
2. Run `python main.py` (or `piper start`)
3. Verify formatted message appears
4. Verify browser opens automatically
5. Verify URL in message is accessible
6. Set `PIPER_AUTO_OPEN=false` → Browser doesn't open
7. Set `PIPER_PORT=8080` → Message shows correct port

**Files to Modify**:
- Modify: `/main.py` (or entry point script)
- Update: `.env.example` (document env vars)
- Optional: Add `rich` to requirements if not present

---

## Sprint 2 (Week 2): Settings & Configuration

### Gap 2 (G2): Settings Index Page [PRIORITY 4]

**Score**: 576 (Impact: 8, Frequency: 9, Effort: 8)
**Effort**: 1 day
**Status**: Makes settings discoverable

#### Problem Statement
Settings scattered across multiple pages with no index. Journey 5 (Configuration):
- User doesn't know what's configurable
- Must guess URLs or navigate blindly
- No overview of available options

#### Specification

**Create**: `/web/templates/settings-index.html`

**Page Structure**:
```html
{% extends "base.html" %}

{% block title %}Settings - Piper Morgan{% endblock %}

{% block content %}
{% include 'components/navigation.html' %}

<div class="settings-container">
  <div class="settings-header">
    <h1>Settings</h1>
    <p class="settings-description">
      Configure Piper Morgan to match your workflow and preferences
    </p>
  </div>

  <div class="settings-grid">
    <!-- Personality Settings Card -->
    <a href="/settings/personality" class="settings-card">
      <div class="card-icon">🎭</div>
      <h3 class="card-title">Personality</h3>
      <p class="card-description">
        Customize how Piper communicates and responds to you
      </p>
      <div class="card-meta">
        <span class="meta-item">Communication style</span>
        <span class="meta-item">Response preferences</span>
      </div>
    </a>

    <!-- Learning Settings Card -->
    <a href="/settings/learning" class="settings-card">
      <div class="card-icon">🧠</div>
      <h3 class="card-title">Learning & Patterns</h3>
      <p class="card-description">
        Control how Piper learns from your behavior and suggests patterns
      </p>
      <div class="card-meta">
        <span class="meta-item">Pattern suggestions</span>
        <span class="meta-item">Learning preferences</span>
      </div>
    </a>

    <!-- Privacy Settings Card -->
    <a href="/settings/privacy" class="settings-card">
      <div class="card-icon">🔒</div>
      <h3 class="card-title">Privacy & Data</h3>
      <p class="card-description">
        Manage your data, conversation history, and privacy preferences
      </p>
      <div class="card-meta">
        <span class="meta-item">Data retention</span>
        <span class="meta-item">Export/delete data</span>
      </div>
    </a>

    <!-- Account Settings Card -->
    <a href="/settings/account" class="settings-card">
      <div class="card-icon">👤</div>
      <h3 class="card-title">Account</h3>
      <p class="card-description">
        Update your profile, password, and account preferences
      </p>
      <div class="card-meta">
        <span class="meta-item">Profile information</span>
        <span class="meta-item">Security settings</span>
      </div>
    </a>

    <!-- Integrations Card (Future) -->
    <a href="/settings/integrations" class="settings-card settings-card-disabled">
      <div class="card-icon">🔌</div>
      <h3 class="card-title">Integrations</h3>
      <p class="card-description">
        Connect Piper with GitHub, Notion, Slack, and other tools
      </p>
      <div class="card-badge">Coming Soon</div>
    </a>

    <!-- Advanced Settings Card -->
    <a href="/settings/advanced" class="settings-card">
      <div class="card-icon">⚙️</div>
      <h3 class="card-title">Advanced</h3>
      <p class="card-description">
        Developer options, experimental features, and system configuration
      </p>
      <div class="card-meta">
        <span class="meta-item">API access</span>
        <span class="meta-item">Debug mode</span>
      </div>
    </a>
  </div>
</div>
{% endblock %}
```

**Styling** (inline or in separate CSS):
```css
<style>
.settings-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 48px 24px;
}

.settings-header {
  margin-bottom: 48px;
}

.settings-header h1 {
  font-size: 32px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.settings-description {
  font-size: 16px;
  color: #7f8c8d;
  margin: 0;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.settings-card {
  background: white;
  border: 1px solid #ecf0f1;
  border-radius: 12px;
  padding: 24px;
  text-decoration: none;
  transition: all 0.2s;
  display: block;
  position: relative;
}

.settings-card:hover {
  border-color: #3498db;
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.15);
  transform: translateY(-2px);
}

.settings-card-disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.settings-card-disabled:hover {
  border-color: #ecf0f1;
  box-shadow: none;
  transform: none;
}

.card-icon {
  font-size: 32px;
  margin-bottom: 16px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.card-description {
  font-size: 14px;
  color: #7f8c8d;
  line-height: 1.5;
  margin: 0 0 16px 0;
}

.card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.meta-item {
  font-size: 12px;
  color: #95a5a6;
  padding: 4px 8px;
  background: #f5f5f5;
  border-radius: 4px;
}

.card-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 12px;
  font-weight: 600;
  color: #3498db;
  background: #e3f2fd;
  padding: 4px 12px;
  border-radius: 12px;
}

@media (max-width: 768px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}
</style>
```

**Backend Route** (add to `/web/app.py`):
```python
@app.get("/settings", response_class=HTMLResponse)
async def settings_index(request: Request):
    """Settings index page"""
    user = await get_current_user(request)
    return templates.TemplateResponse(
        "settings-index.html",
        {"request": request, "user": user}
    )
```

**Update Navigation** (if /settings link doesn't exist):
- Ensure navigation.html links to `/settings`
- Should be highlighted when on any `/settings/*` page

#### Acceptance Criteria

- [ ] `/settings` route renders settings index page
- [ ] 6 setting categories displayed as cards
- [ ] Cards show: icon, title, description, metadata
- [ ] Clicking card navigates to that settings page
- [ ] "Integrations" card shows "Coming Soon" badge
- [ ] Cards have hover effect (lift + blue border)
- [ ] Responsive grid (1 column on mobile, 2-3 on desktop)
- [ ] Navigation highlights "Settings" when on this page

#### Testing

**Manual Tests**:
1. Navigate to `/settings` → Index page loads
2. Click "Personality" card → Personality settings load
3. Click "Learning" card → Learning dashboard loads
4. Click "Privacy" card → Privacy settings load (or 404 if not created yet)
5. Hover over cards → Visual feedback
6. Resize to mobile → Single column grid
7. Check navigation → "Settings" is highlighted

**Files to Modify**:
- Create: `/web/templates/settings-index.html`
- Modify: `/web/app.py` (add `/settings` route)
- Verify: Navigation.html includes `/settings` link

---

### Gap 4 (G4): Breadcrumb Navigation [PRIORITY 5]

**Score**: 504 (Impact: 7, Frequency: 9, Effort: 8)
**Effort**: 1 day
**Status**: User orientation, especially important for settings

#### Problem Statement
Users don't know where they are in the app hierarchy. Journey 5 (Settings):
- On `/settings/personality` → No indication this is a sub-page of Settings
- Can't easily navigate back to settings index
- No sense of location in information architecture

#### Specification

**Create**: `/web/templates/components/breadcrumbs.html` (Jinja2 partial)

**Breadcrumb Component**:
```html
{#
  Breadcrumb component

  Usage in templates:
  {% set breadcrumbs = [
    {"label": "Settings", "url": "/settings"},
    {"label": "Personality", "url": None}
  ] %}
  {% include 'components/breadcrumbs.html' %}
#}

{% if breadcrumbs %}
<nav class="breadcrumbs" aria-label="Breadcrumb">
  <ol class="breadcrumb-list">
    <li class="breadcrumb-item">
      <a href="/" class="breadcrumb-link">
        <svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true">
          <path d="M8.707 1.5a1 1 0 00-1.414 0L.646 8.146a.5.5 0 00.708.708L2 8.207V13.5A1.5 1.5 0 003.5 15h9a1.5 1.5 0 001.5-1.5V8.207l.646.647a.5.5 0 00.708-.708L13 5.793V2.5a.5.5 0 00-.5-.5h-1a.5.5 0 00-.5.5v1.293L8.707 1.5z"/>
          <path d="M13 7.207l-5-5-5 5V13.5a.5.5 0 00.5.5h9a.5.5 0 00.5-.5V7.207z"/>
        </svg>
        <span class="sr-only">Home</span>
      </a>
    </li>

    {% for crumb in breadcrumbs %}
    <li class="breadcrumb-item">
      <span class="breadcrumb-separator" aria-hidden="true">/</span>
      {% if crumb.url %}
        <a href="{{ crumb.url }}" class="breadcrumb-link">
          {{ crumb.label }}
        </a>
      {% else %}
        <span class="breadcrumb-current" aria-current="page">
          {{ crumb.label }}
        </span>
      {% endif %}
    </li>
    {% endfor %}
  </ol>
</nav>
{% endif %}
```

**Styling**:
```css
<style>
.breadcrumbs {
  background: #f8f9fa;
  border-bottom: 1px solid #ecf0f1;
  padding: 12px 0;
}

.breadcrumb-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  list-style: none;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.breadcrumb-link {
  color: #7f8c8d;
  text-decoration: none;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: color 0.2s;
}

.breadcrumb-link:hover {
  color: #3498db;
}

.breadcrumb-link svg {
  width: 16px;
  height: 16px;
}

.breadcrumb-separator {
  color: #bdc3c7;
  font-size: 14px;
}

.breadcrumb-current {
  color: #2c3e50;
  font-size: 14px;
  font-weight: 500;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@media (max-width: 768px) {
  .breadcrumb-list {
    padding: 0 16px;
  }
  .breadcrumb-link,
  .breadcrumb-current {
    font-size: 13px;
  }
}
</style>
```

**Integration Examples**:

**In `personality-preferences.html`**:
```html
{% set breadcrumbs = [
  {"label": "Settings", "url": "/settings"},
  {"label": "Personality", "url": None}
] %}
{% include 'components/breadcrumbs.html' %}
```

**In `learning-dashboard.html`**:
```html
{% set breadcrumbs = [
  {"label": "Settings", "url": "/settings"},
  {"label": "Learning", "url": None}
] %}
{% include 'components/breadcrumbs.html' %}
```

**In `standup.html`**:
```html
{% set breadcrumbs = [
  {"label": "Standup", "url": None}
] %}
{% include 'components/breadcrumbs.html' %}
```

**Dynamic Breadcrumb Helper** (optional, in `web/utils.py`):
```python
def get_breadcrumbs(path: str) -> list:
    """
    Generate breadcrumbs from URL path

    Examples:
      /settings/personality → [{"label": "Settings", "url": "/settings"}, {"label": "Personality", "url": None}]
      /standup → [{"label": "Standup", "url": None}]
    """
    breadcrumbs = []

    # Path mappings
    labels = {
        "settings": "Settings",
        "personality": "Personality",
        "learning": "Learning",
        "standup": "Standup",
        "files": "Files",
        "account": "Account",
        "privacy": "Privacy",
        "advanced": "Advanced"
    }

    parts = [p for p in path.split("/") if p]

    for i, part in enumerate(parts):
        is_last = (i == len(parts) - 1)
        url = "/" + "/".join(parts[:i+1]) if not is_last else None
        label = labels.get(part, part.capitalize())

        breadcrumbs.append({
            "label": label,
            "url": url
        })

    return breadcrumbs
```

#### Acceptance Criteria

- [ ] Breadcrumbs appear below navigation on all settings pages
- [ ] Shows path from Home → Current page
- [ ] Home icon links to `/`
- [ ] Intermediate crumbs are clickable links
- [ ] Current page is not clickable (aria-current="page")
- [ ] Separator "/" between crumbs
- [ ] Screen reader announces "Breadcrumb" navigation
- [ ] Keyboard accessible (Tab through links)
- [ ] Responsive on mobile

#### Testing

**Manual Tests**:
1. Navigate to `/settings/personality` → See "Home / Settings / Personality"
2. Click "Settings" → Navigate to settings index
3. Click Home icon → Navigate to home page
4. Navigate to `/standup` → See "Home / Standup"
5. Tab through breadcrumbs → Focus visible
6. Test with screen reader → Announces "Breadcrumb navigation"

**Files to Modify**:
- Create: `/web/templates/components/breadcrumbs.html`
- Modify: `/web/templates/personality-preferences.html` (add breadcrumbs)
- Modify: `/web/templates/learning-dashboard.html` (add breadcrumbs)
- Modify: `/web/templates/standup.html` (add breadcrumbs)
- Optional: Create `/web/utils.py` (breadcrumb helper function)

---

## Cross-Sprint Considerations

### Accessibility Requirements (Apply to All)

**WCAG 2.2 AA Compliance** (documented in `CLAUDE.md`):
- Color contrast: 4.5:1 for normal text, 3:1 for large text
- Keyboard navigation: All interactive elements accessible via Tab
- Screen reader support: Proper ARIA labels and roles
- Focus indicators: 2px outline, 4.5:1 contrast
- Skip links: Allow keyboard users to skip navigation

**Test with**:
- Keyboard only (no mouse)
- Screen reader (NVDA, JAWS, or VoiceOver)
- Color contrast checker (WebAIM, axe DevTools)

### Design System Foundation (Prep for Sprints 3-4)

**Note**: Design system tokens are ready in Phase 3 deliverable
- `docs/ux-audit/ux-audit-phase3-design-system-implementation.md`
- Contains `tokens.css`, `light.css`, `dark.css` ready to use
- Don't implement yet, but be aware for future sprints

**Current work uses hard-coded values** (intentionally):
- Light theme colors: `#3498db`, `#2c3e50`, etc.
- Match existing home.html / standup.html styling
- Consistency within Quick Wins is goal
- Sprints 3-4 will migrate to token-based system

### Testing Strategy

**Manual Testing Checklist** (complete for all 5 gaps):
- [ ] Visual: Component appears correctly
- [ ] Functional: All interactions work
- [ ] Keyboard: Tab/Enter/Escape navigation
- [ ] Screen Reader: Proper announcements
- [ ] Mobile: Responsive behavior (320px - 1920px)
- [ ] Cross-browser: Chrome, Firefox, Safari
- [ ] Integration: Works with other components

**Evidence Required**:
- Screenshots of each component (desktop + mobile)
- Screen recording of keyboard navigation
- Console output showing no errors
- Accessibility audit results (browser DevTools)

---

## Development Workflow

### Step 1: Understand Architecture (Use Serena)

**Before making ANY changes**:
1. Read `docs/NAVIGATION.md` (Serena index)
2. Locate relevant services/routes
3. Understand existing patterns
4. Check for related code

**Example**:
```
Question: "Where should I add the settings index route?"
→ Check Serena → "web/app.py" contains FastAPI routes
→ Read web/app.py to understand pattern
→ Add new route following existing conventions
```

### Step 2: Progressive Context (Beads Approach)

**Don't load all files at once**:
1. Start with gap specification (this document)
2. Load target file (e.g., `web/app.py`)
3. Load dependencies only as needed (e.g., `services/auth_service.py`)
4. Load templates only when modifying them

**Use file scoring** to prioritize what to read:
- High score: Direct implementation files
- Medium score: Related utilities/services
- Low score: Distant dependencies

### Step 3: Implement Gap-by-Gap

**Work sequentially**:
- Sprint 1: G1 → G8 → G50 (in order)
- Sprint 2: G2 → G4 (in order)

**Why**: Later gaps build on earlier ones
- G8 (user menu) requires G1 (navigation) to exist
- G4 (breadcrumbs) works better with G2 (settings index)

### Step 4: Test Thoroughly

**After each gap**:
1. Manual testing (7-8 test scenarios per gap)
2. Accessibility check (keyboard + screen reader)
3. Visual verification (screenshot desktop + mobile)
4. Cross-browser check (Chrome, Firefox minimum)
5. Document any issues found

### Step 5: Document Progress

**Create**: `docs/ux-audit/quick-wins-progress.md`

**Track**:
```markdown
# Quick Wins Progress

## Sprint 1 (Week 1)

### G1: Global Navigation Menu
- Status: ✅ Complete
- Files Modified: 5
- Time: 2.5 days
- Issues: None
- Screenshots: [link]

### G8: Logged-in User Indicator
- Status: ✅ Complete
- Files Modified: 2
- Time: 4 hours
- Issues: Dropdown positioning on mobile (fixed)
- Screenshots: [link]

[etc.]
```

---

## Success Criteria (Overall)

### Sprint 1 Complete When:
- [ ] Navigation appears on all 4 pages
- [ ] User menu shows username and dropdown
- [ ] Server startup prints clear message with URL
- [ ] Browser auto-opens to Piper
- [ ] All components keyboard accessible
- [ ] All components work on mobile
- [ ] Zero console errors
- [ ] Documentation updated

### Sprint 2 Complete When:
- [ ] Settings index page exists at `/settings`
- [ ] 6 setting categories displayed as cards
- [ ] Breadcrumbs appear on all settings pages
- [ ] Breadcrumbs show correct hierarchy
- [ ] Navigation works with new pages
- [ ] All accessibility requirements met
- [ ] User testing shows 80% reduction in frustration

### Definition of Done (Per Gap):
- [ ] Code implemented and tested manually
- [ ] Accessibility validated (keyboard + screen reader)
- [ ] Responsive on mobile (320px - 1920px)
- [ ] Cross-browser tested (Chrome + Firefox minimum)
- [ ] Screenshots captured (desktop + mobile)
- [ ] Progress documented in `quick-wins-progress.md`
- [ ] No regression (existing features still work)
- [ ] Code reviewed (self-review minimum)

---

## Common Patterns to Follow

### File Organization
```
web/
├── templates/
│   ├── components/          # Reusable partials
│   │   ├── navigation.html
│   │   └── breadcrumbs.html
│   ├── home.html            # Main pages
│   ├── standup.html
│   └── settings-index.html
├── assets/                  # Static files
│   ├── pmlogo.png
│   └── (other assets)
└── app.py                   # FastAPI routes
```

### Jinja2 Template Pattern
```html
{% extends "base.html" %}

{% block title %}Page Title - Piper Morgan{% endblock %}

{% block content %}
{% include 'components/navigation.html' %}
{% include 'components/breadcrumbs.html' %}

<div class="page-container">
  <!-- Page content here -->
</div>
{% endblock %}
```

### FastAPI Route Pattern
```python
@app.get("/path", response_class=HTMLResponse)
async def route_name(request: Request):
    """Route description"""
    user = await get_current_user(request)

    # Additional data loading

    return templates.TemplateResponse(
        "template-name.html",
        {
            "request": request,
            "user": user,
            # Additional context
        }
    )
```

### CSS Styling Convention
```css
/* Component-specific styles in template */
<style>
.component-name {
  /* Base styles */
}

.component-name:hover {
  /* Hover states */
}

@media (max-width: 768px) {
  /* Mobile responsive */
}
</style>
```

---

## Questions & Escalation

### If You Get Stuck

**Ask Serena first** (`docs/NAVIGATION.md`):
- Can't find where to add code? → Check Serena
- Don't understand architecture? → Check Serena
- Need related files? → Check Serena

**Check existing patterns**:
- How do other routes work? → Look at `web/app.py`
- How are templates structured? → Look at existing templates
- What's the CSS pattern? → Look at existing styles

**Escalate to PM if**:
- Specification unclear or contradictory
- Missing dependencies (e.g., user object not in context)
- Architectural decision needed (e.g., should this be a service?)
- Blockers that prevent progress

### Don't Escalate For:
- Finding where to put code (use Serena)
- Understanding existing patterns (read code)
- Writing CSS (follow examples in spec)
- Testing manually (follow test scenarios in spec)

---

## Timeline & Reporting

### Week 1 (Sprint 1)
- Day 1-2: G1 (Navigation) - 2-3 days
- Day 3: G8 (User menu) - 4 hours
- Day 3: G50 (Startup message) - 1 hour
- Day 4: Testing, documentation, bug fixes

### Week 2 (Sprint 2)
- Day 1: G2 (Settings index) - 1 day
- Day 2: G4 (Breadcrumbs) - 1 day
- Day 3-4: Integration testing, bug fixes
- Day 4: Final documentation and handoff

### Daily Updates Expected:
- What did you complete?
- What are you working on?
- Any blockers or questions?
- Screenshots of progress

---

## Final Reminders

### Critical Success Factors

1. **Use Serena** (`docs/NAVIGATION.md`) before coding anything
2. **Follow specifications exactly** - don't improvise
3. **Test accessibility** - keyboard and screen reader
4. **Work sequentially** - don't skip ahead
5. **Document progress** - screenshots and notes
6. **Ask questions early** - don't guess if unclear

### What Good Looks Like

**After Sprint 1**:
- User lands on Piper → Sees clear navigation → Knows where they are
- User clicks Settings → Dropdown shows username → Can logout
- Developer starts server → Sees URL → Browser opens automatically

**After Sprint 2**:
- User clicks Settings → Sees 6 category cards → Picks one
- User on any settings page → Sees breadcrumbs → Can navigate back
- User feels oriented → Knows where features are → Can find things

**Overall Impact**: User experience transforms from 3/10 → 6/10

---

## Resources Summary

**You Have Access To**:
- ✅ All UX audit deliverables (docs/ux-audit/)
- ✅ Serena navigation index (docs/NAVIGATION.md)
- ✅ Full codebase (all services, templates, etc.)
- ✅ This comprehensive specification

**You Are Expected To**:
- Use Serena to navigate architecture
- Follow specifications precisely
- Test thoroughly (manual + accessibility)
- Document progress daily
- Ask questions when stuck
- Deliver production-quality code

**You Will Succeed By**:
- Reading docs before coding
- Following existing patterns
- Testing before marking complete
- Communicating progress clearly
- Maintaining focus on user impact

---

**Let's transform Piper's user experience together!** 🚀

**Start with G1 (Global Navigation Menu) - it's the foundation for everything else.**

Good luck! 💪
