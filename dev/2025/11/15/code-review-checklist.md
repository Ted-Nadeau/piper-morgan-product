# UX Quick Wins Code Review Checklist

**For**: Pull Request on `claude/ux-quick-wins-navigation-settings-015W99syFQ7b9HrV2WoB9S48`
**Reviewer**: [Your Name]
**Date**: [Review Date]

---

## ✅ PATTERN CONSISTENCY CHECK

- [ ] **Navigation Component**
  - [ ] `{% include 'components/navigation.html' %}` used consistently across all pages
  - [ ] Component styling is inline (contained in component file)
  - [ ] JavaScript is scoped to component (no global namespace pollution)
  - [ ] Active link logic references `window.location.pathname`

- [ ] **Breadcrumbs Component**
  - [ ] `{% include 'components/breadcrumbs.html' %}` used in settings/learning/standup
  - [ ] Breadcrumbs array format: `[{"label": "...", "url": "..."}]`
  - [ ] Home link always first (icon-based)
  - [ ] Current page has `url: None` (non-clickable)

- [ ] **Route Handlers**
  - [ ] All route handlers return `templates.TemplateResponse(template_name, {"request": request})`
  - [ ] All routes include `request: Request` parameter
  - [ ] No deviation from existing route patterns

---

## ✅ CONTRACT VERIFICATION (Frontend ↔ Backend)

### User Context Contract

- [ ] Backend provides `request.state.user_claims` from JWT middleware
- [ ] Frontend receives `request.state.user_claims.user_email` and `.user_id`
- [ ] JavaScript extracts username from email: `email.split('@')[0]`
- [ ] `window.currentUser` object has: `username`, `email`, `user_id`

**Verify Template Context**:
```bash
grep -c "request.state.user_claims" templates/*.html
# Should be 4-5 matches (home, standup, personality, learning, settings)
```

### Logout Endpoint Contract

- [ ] Frontend calls: `POST /api/v1/auth/logout`
- [ ] Backend endpoint exists at: `/api/v1/auth/logout` (in auth router)
- [ ] Request includes: `credentials: 'include'` (for JWT auth)
- [ ] Response handling: `if (response.ok)` redirects to `/`

**Verify Endpoint Exists**:
```bash
grep -n "@router.post.*logout" web/api/routes/auth.py
# Should find the logout endpoint
```

### Settings Routes

- [ ] `/settings` route exists and returns `settings-index.html`
- [ ] `/personality-preferences` route exists and returns correct template
- [ ] `/learning` route exists and returns `learning-dashboard.html`

**TODO - Not Critical for Merge**:
```
❌ /account - NOT YET DEFINED (referenced in dropdown)
❌ /files - NOT YET DEFINED (referenced in nav)
❌ /settings/privacy - NOT YET DEFINED (referenced in settings index)
❌ /settings/advanced - NOT YET DEFINED (referenced in settings index)
```

- [ ] **DECISION REQUIRED**: Should missing routes be removed or created?

---

## ✅ ACCESSIBILITY (WCAG 2.2 AA) CHECK

### Navigation Component

- [ ] `<nav role="navigation" aria-label="Main navigation">`
- [ ] User button: `aria-haspopup="true"` and `aria-expanded="true/false"`
- [ ] Dropdown menu hidden by default with `hidden` attribute
- [ ] All links keyboard accessible (Tab key)
- [ ] Escape key closes dropdown
- [ ] Arrow keys navigate between items
- [ ] Enter key activates selected item

**Keyboard Navigation Test**:
```
1. Tab to navigation button
2. Press Enter → dropdown opens
3. Press ArrowDown → focus first item
4. Press ArrowUp → focus last item
5. Press Escape → dropdown closes
6. Press Tab away → dropdown closes
```

- [ ] Focus outline visible on all interactive elements
- [ ] Focus outline has sufficient contrast (2px, 4.5:1)

### Breadcrumbs Component

- [ ] `<nav role="navigation" aria-label="Breadcrumb">`
- [ ] Current page: `<span aria-current="page">...</span>`
- [ ] Previous pages: clickable `<a>` tags
- [ ] Separators: `aria-hidden="true"` (not announced to screen readers)
- [ ] Home icon: `aria-hidden="true"` + text alt in `<span class="sr-only">Home</span>`

### Color Contrast

- [ ] Primary color #3498db + dark text #2c3e50 = 4.5:1+ (WCAG AA)
- [ ] All text has sufficient contrast (test with WebAIM contrast checker)
- [ ] Hover/active states maintain contrast

**Tools to Test**:
- WebAIM Contrast Checker
- axe DevTools browser extension
- Chrome DevTools Lighthouse

---

## ✅ RESPONSIVE DESIGN CHECK

### Desktop (1200px+)

- [ ] Navigation spans full width with logo + menu + user dropdown
- [ ] Settings grid shows 2-3 columns
- [ ] Breadcrumbs span full width
- [ ] All elements aligned properly

### Tablet (768px)

- [ ] Settings grid collapses to single column
- [ ] Navigation font sizes reduce
- [ ] Mobile menu works if present

### Mobile (320-480px)

- [ ] Navigation text reduces or collapses
- [ ] No horizontal scrolling
- [ ] User dropdown accessible
- [ ] Settings cards full width
- [ ] Touch targets are 44x44px minimum

**Test Viewports**:
```
Chrome DevTools:
- 1920x1080 (desktop)
- 768x1024 (tablet)
- 375x667 (mobile)
- 320x568 (small mobile)
```

---

## ✅ CODE QUALITY CHECK

### HTML/Jinja2

- [ ] Valid Jinja2 syntax (`{% %}`, `{{ }}`)
- [ ] Proper HTML5 structure
- [ ] Semantic HTML (nav, button, link elements)
- [ ] No hardcoded URLs (uses relative paths like `/settings`)
- [ ] Template variables properly escaped

### CSS

- [ ] No CSS in global scope (all in component `<style>`)
- [ ] Mobile-first approach (base styles, then @media queries)
- [ ] No inline styles (except where necessary)
- [ ] Colors use hex format consistently
- [ ] Z-index hierarchy reasonable

### JavaScript

- [ ] No global variables (scoped to event handlers)
- [ ] Error handling present (try/catch in logout)
- [ ] Event listeners properly managed (added in DOMContentLoaded)
- [ ] No console errors (check browser dev tools)
- [ ] Proper async/await patterns (logout fetch)

---

## ✅ SECURITY CHECK

- [ ] Logout uses POST (not GET) ✓
- [ ] `credentials: 'include'` for JWT auth ✓
- [ ] No sensitive data in HTML comments
- [ ] No hardcoded API keys or tokens
- [ ] XSS protection: Template variables use `{{ }}` (auto-escaped in Jinja2)

---

## ✅ FUNCTIONAL TESTING

### Navigation Component

- [ ] [MANUAL TEST] Click logo → navigates to `/`
- [ ] [MANUAL TEST] Click each nav item → correct page loads
- [ ] [MANUAL TEST] Current page highlighted in blue
- [ ] [MANUAL TEST] Click avatar → dropdown opens
- [ ] [MANUAL TEST] Click away from dropdown → dropdown closes
- [ ] [MANUAL TEST] Click Logout → confirms logout (or redirects)
- [ ] [MANUAL TEST] Settings link highlights when on `/settings` or sub-pages

### Breadcrumbs Component

- [ ] [MANUAL TEST] Navigate to `/settings` → shows "Home / Settings"
- [ ] [MANUAL TEST] Navigate to `/personality-preferences` → shows "Home / Settings / Personality"
- [ ] [MANUAL TEST] Navigate to `/learning` → shows "Home / Settings / Learning"
- [ ] [MANUAL TEST] Navigate to `/standup` → shows "Home / Standup"
- [ ] [MANUAL TEST] Click Settings in breadcrumb → navigates to `/settings`
- [ ] [MANUAL TEST] Click Home in breadcrumb → navigates to `/`

### Settings Index Page

- [ ] [MANUAL TEST] `/settings` route accessible
- [ ] [MANUAL TEST] 6 setting cards visible (Personality, Learning, Privacy, Account, Integrations, Advanced)
- [ ] [MANUAL TEST] Each card shows icon, title, description, metadata
- [ ] [MANUAL TEST] Integrations card shows "Coming Soon" badge
- [ ] [MANUAL TEST] Clicking Personality card → navigates to `/personality-preferences`
- [ ] [MANUAL TEST] Clicking Learning card → navigates to `/learning`
- [ ] [MANUAL TEST] Other cards attempt navigation (will 404 if routes don't exist)

### User Indicator (G8)

- [ ] [MANUAL TEST] If logged in, username appears in avatar + dropdown
- [ ] [MANUAL TEST] Avatar shows first letter of username (uppercase)
- [ ] [MANUAL TEST] Logout button visible and clickable
- [ ] [MANUAL TEST] Clicking logout attempts to call `/api/v1/auth/logout`

### Server Startup Message (G50)

- [ ] [MANUAL TEST] Run `python main.py`
- [ ] [MANUAL TEST] Formatted startup message appears with:
  - [ ] Box borders (====)
  - [ ] ✅ Checkmark emoji
  - [ ] Web interface URL (http://localhost:8001)
  - [ ] API docs URL (/docs)
  - [ ] Health check URL (/health)
  - [ ] Instructions to press Ctrl+C
- [ ] [MANUAL TEST] Browser opens automatically (unless `--no-browser` flag used)

---

## ✅ VISUAL INSPECTION

### Desktop Screenshot

- [ ] Navigation visible at top of page
- [ ] Logo + brand name visible on left
- [ ] Main menu items visible (Home, Standup, Files, Learning, Settings)
- [ ] User dropdown visible on right
- [ ] Breadcrumbs visible below navigation (on relevant pages)
- [ ] Settings cards display in nice grid layout
- [ ] Colors match design spec (#3498db, #2c3e50, etc.)

### Mobile Screenshot

- [ ] Navigation responsive (fits in mobile viewport)
- [ ] User dropdown accessible on mobile
- [ ] Settings cards single column
- [ ] No horizontal scrolling
- [ ] Breadcrumbs readable on mobile

---

## ✅ DOCUMENTATION CHECK

- [ ] Session log updated with implementation details
- [ ] Acceptance criteria all checked in task spec
- [ ] Commit messages clear and descriptive
- [ ] Code comments explain non-obvious behavior
- [ ] No TODO comments without issue references

---

## ✅ INTEGRATION CHECK

### With Authentication System

- [ ] `request.state.user_claims` available (set by auth middleware)
- [ ] User email properly formatted for avatar
- [ ] Logout endpoint properly revokes token

### With Existing Pages

- [ ] Navigation appears on: home, standup, personality, learning
- [ ] Settings breadcrumbs appear on: settings, personality, learning
- [ ] No conflicts with existing CSS or JavaScript
- [ ] No regression in existing functionality

---

## DECISION POINTS

### CRITICAL: Missing Route Handlers

**Issue**: 5 routes referenced but not defined:
- `/account` (user dropdown)
- `/files` (main navigation)
- `/settings/privacy` (settings index)
- `/settings/advanced` (settings index)
- `/settings/integrations` (settings index, disabled with "Coming Soon")

**Options**:

1. ✅ **Recommended**: Create placeholder pages
   ```python
   @app.get("/account")
   async def account_page(request: Request):
       return templates.TemplateResponse("account.html", {"request": request})

   # Similar for other missing routes
   ```

2. **Alternative**: Remove/disable links
   - Remove from navigation (delete `/files` entry)
   - Remove from dropdown (delete `/account` link)
   - Disable settings cards (gray out + disable pointer)

**BLOCKER**: This MUST be resolved before merge

**Recommendation**: Create simple placeholder pages with "Coming Soon" message

---

## FINAL APPROVAL CHECKLIST

- [ ] All pattern consistency checks passed
- [ ] Contract verification successful
- [ ] Accessibility WCAG 2.2 AA verified
- [ ] Responsive design tested on 3+ viewport sizes
- [ ] Code quality acceptable
- [ ] Security checks passed
- [ ] All functional tests completed manually
- [ ] Visual inspection approved
- [ ] Documentation updated
- [ ] Integration issues resolved
- [ ] **Route handler decision made and implemented**

---

## SIGN-OFF

**Reviewer Name**: ________________
**Review Date**: ________________
**Status**: [ ] APPROVED [ ] APPROVED WITH CHANGES [ ] REQUEST CHANGES

**Comments**:
```
[Add reviewer comments here]
```

**Changes Required Before Merge**:
```
[ ] Create missing route handlers (/account, /files, /settings/*, etc.)
[ ] [Other items as needed]
```

---

## NOTES FOR REVIEWERS

### Testing Environment
- Browser: Chrome/Firefox/Safari (latest)
- OS: macOS/Linux/Windows
- Screen reader (optional): NVDA or JAWS for accessibility testing

### Common Issues to Watch For
- User context not available (auth middleware issue)
- Logout not working (endpoint not mounted)
- Breadcrumbs not showing (template not including component)
- Navigation overlap with other elements (z-index issue)

### Quick Verification Commands
```bash
# Check pattern consistency
grep -r "{% include 'components" templates/ --include="*.html"

# Check for missing routes
grep -r "href=\"/" templates/ --include="*.html" -o | sort -u

# Run tests (if applicable)
pytest tests/

# Check for console errors
# (Manual: open DevTools on each page)
```

---

**This checklist ensures comprehensive review coverage across pattern consistency, accessibility, functionality, and code quality.**
