# Phase 1.4: Technical Constraints
**UX Investigation - Piper Morgan**
**Date**: November 13, 2025, 19:32 PT
**Investigator**: Claude Code (UXR)

---

## Executive Summary

This document catalogs the technical constraints that impact UX decisions in Piper Morgan. Understanding these constraints is essential for creating realistic UX recommendations that can actually be implemented within the current tech stack.

**Key Finding**: The current architecture favors **simplicity and zero build complexity** over framework features. This is intentional and works well for alpha, but creates constraints around component reusability, state management, and reactive UI patterns.

---

## Frontend Technology Stack

### JavaScript Framework: None (Vanilla JS)

**Current State**:
- ✅ Pure JavaScript (ES6+)
- ✅ No React, Vue, Angular, or Svelte
- ✅ No TypeScript
- ✅ No build process (no webpack, vite, parcel)
- ✅ No transpilation required

**Capabilities**:
- Modern JS features (async/await, arrow functions, template literals)
- Fetch API for HTTP requests
- DOM manipulation via vanilla methods
- ES modules NOT used (all inline scripts)

**Constraints**:
- ❌ No component reusability without duplication
- ❌ No reactive data binding
- ❌ No state management library
- ❌ Manual DOM updates required
- ❌ Event listeners manually attached
- ❌ No virtual DOM for efficient updates
- ❌ No JSX or templating syntax
- ❌ Code duplication across touchpoints (e.g., bot-message-renderer.js duplicated)

**UX Implications**:
- Simple interactions easy to implement
- Complex interactions require significant code
- Maintaining consistency requires manual effort
- Adding features means copy-paste patterns
- State synchronization must be manual

**Why This Constraint Exists**:
- Reduces deployment complexity (no build step)
- Easier onboarding for contributors
- Faster iteration during alpha
- No framework lock-in

**Recommendation**:
- ✅ **Keep for alpha** - simplicity is valuable
- 🔄 **Consider post-alpha**: Lightweight framework (Preact, Alpine.js, or htmx) for component reusability without heavy build process

---

### CSS Framework: None (Inline Styles)

**Current State**:
- ✅ Inline `<style>` tags in HTML
- ✅ No CSS framework (Bootstrap, Tailwind, etc.)
- ✅ No CSS preprocessor (Sass, Less)
- ✅ No CSS modules or scoped styles
- ✅ Tailwind config exists but NOT used

**Capabilities**:
- Full CSS3 support
- Custom properties (CSS variables) supported but NOT used
- Flexbox and Grid layouts
- Media queries for responsiveness
- CSS animations and transitions

**Constraints**:
- ❌ No design token system (yet)
- ❌ Styles duplicated across files
- ❌ No CSS class reuse across touchpoints
- ❌ Hard to maintain consistency
- ❌ Global namespace (class name collisions possible)
- ❌ No utility classes for rapid development

**Current File Structure**:
```
templates/
├── home.html          (300+ lines of inline CSS)
└── standup.html       (100+ lines of inline CSS)

web/assets/
├── learning-dashboard.html      (400+ lines of inline CSS)
└── personality-preferences.html (200+ lines of inline CSS)
```

**UX Implications**:
- Changing a button style requires editing 4+ files
- Theme changes must be replicated manually
- New features require rewriting common styles
- Inconsistencies accumulate over time

**Why This Constraint Exists**:
- No build process needed
- Faster initial development
- Self-contained HTML files
- Easy to debug (styles visible in file)

**Recommendation**:
- 🔄 **Implement CSS custom properties** for design tokens (no build required!)
- 🔄 **Extract shared styles** to `/web/assets/styles.css` loaded by all pages
- 📋 **Future**: Consider Tailwind or similar for utility classes

---

### HTML Templating: Jinja2 (Backend) + String Literals (Frontend)

**Current State**:
- ✅ Jinja2 templates for initial page render (home.html, standup.html)
- ✅ JavaScript string literals for dynamic content
- ✅ Template literals for HTML generation

**Example Current Pattern**:
```javascript
// Client-side templating (learning dashboard)
results.innerHTML = `
  <div class="success">✅ Standup generated successfully!</div>
  <div class="metrics">
    <div class="metric">
      <div class="metric-value">${data.generation_time}</div>
      <div class="metric-label">Generation Time</div>
    </div>
  </div>
`;
```

**Capabilities**:
- Server-side rendering for initial page load
- Dynamic client-side content updates
- Markdown rendering via marked.js CDN

**Constraints**:
- ❌ No client-side templating engine
- ❌ XSS risk with improper escaping
- ❌ No template inheritance on client
- ❌ String concatenation for complex UIs
- ❌ Hard to maintain complex nested structures

**Security Observations**:
- ✅ User messages use `textContent` (XSS safe)
- ⚠️ Bot messages use `innerHTML` (relies on backend sanitization)
- ✅ Markdown rendered via library (not raw HTML)

**UX Implications**:
- Simple updates work well
- Complex UI structures become messy
- Error-prone for nested elements
- Hard to maintain consistent structure

**Recommendation**:
- ✅ **Current approach acceptable for alpha**
- 🔄 **Consider**: Lightweight templating (Handlebars, Mustache) or template tag functions
- 🔄 **Improve**: Create helper functions for common patterns

---

### State Management: None (Manual)

**Current State**:
- ✅ Global variables for state
- ✅ Closure-based state in functions
- ✅ No centralized state store

**Examples**:
```javascript
// Global state (home.html)
let sessionId = null;

// Module-level state (learning dashboard)
let autoRefreshTimer = null;
let privacySettingsChanged = false;
```

**Constraints**:
- ❌ No reactivity (state changes don't auto-update UI)
- ❌ No state persistence (except via cookies/localStorage manually)
- ❌ State scattered across files
- ❌ No time-travel debugging
- ❌ No state synchronization across tabs

**UX Implications**:
- User actions require manual UI updates
- State can get out of sync
- Hard to implement complex flows
- Refresh often needed to see updates

**Current Patterns Observed**:
- Session ID passed with requests
- Auto-refresh for live data (30s polling)
- Cookie-based authentication state
- LocalStorage NOT currently used

**Recommendation**:
- ✅ **Acceptable for current complexity**
- 🔄 **Add**: Simple state utilities (pub/sub pattern)
- 📋 **Future**: Consider lightweight state library (Zustand, Nano Stores)

---

## Backend Technology

### API: FastAPI (Python)

**Current State**:
- ✅ RESTful JSON APIs
- ✅ FastAPI framework
- ✅ Pydantic models for validation
- ✅ JWT authentication
- ✅ Cookie-based sessions

**API Design**:
```python
# Current pattern
@app.post("/api/v1/intent")
async def process_intent(request: IntentRequest) -> IntentResponse:
    # Returns JSON

# Pattern with polling
@app.get("/api/v1/workflows/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    # Client polls this endpoint
```

**Constraints**:
- ❌ No WebSocket support (polling instead)
- ❌ No Server-Sent Events (SSE)
- ❌ No GraphQL (REST only)
- ✅ CORS configured for local dev

**UX Implications**:
- Real-time updates require polling (2s intervals)
- Not ideal for high-frequency updates
- Simple request/response works well
- Loading states need manual handling

**Recommendation**:
- ✅ **Current approach works for alpha**
- 🔄 **Consider**: WebSockets for real-time features (chat, live updates)
- 📋 **Future**: SSE for one-way real-time updates (notifications)

---

## Mobile & Responsive Design

### Current Responsiveness

**Media Queries Found**:
```css
/* Learning Dashboard Only */
@media (max-width: 768px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .setting-item {
    flex-direction: column;
  }
}
```

**Observations**:
- ✅ Viewport meta tag present in all pages
- ⚠️ Only learning dashboard has media queries
- ❌ Home and standup have minimal responsive design
- ❌ No mobile-first approach
- ❌ No tablet-specific breakpoints

**Testing**:
- ❌ No mobile device testing evident
- ❌ No responsive design testing tools
- ❌ No touch gesture support

**Constraints**:
- Fixed widths in many places
- Assumes desktop/laptop screen size
- No consideration for small screens (<768px)
- No orientation handling

**UX Implications**:
- Poor mobile experience likely
- Text may be too small on phones
- Buttons may be too small for touch
- Horizontal scrolling possible
- Forms may be awkward on mobile

**Mobile Breakpoints Missing**:
```css
/* Not currently defined */
--breakpoint-mobile:  320px;  /* Small phones */
--breakpoint-phablet: 480px;  /* Large phones */
--breakpoint-tablet:  768px;  /* Tablets */
--breakpoint-desktop: 1024px; /* Desktop */
--breakpoint-wide:    1280px; /* Wide screens */
```

**Recommendation**:
- 🚨 **High Priority**: Add mobile breakpoints to design system
- 🔄 **Test**: Actual mobile devices or browser dev tools
- 🔄 **Implement**: Touch-friendly sizing (44px minimum tap targets)
- 📋 **Future**: Progressive Web App (PWA) capabilities

---

## Accessibility

### Current State

**Semantic HTML**:
- ✅ Some semantic elements used (`<header>`, `<section>`)
- ⚠️ Mostly `<div>` and `<span>`
- ❌ No `<nav>`, `<aside>`, `<article>` structure
- ❌ No landmark roles

**ARIA Attributes**:
```bash
# Searched for ARIA attributes
grep -r "aria-" templates/ web/assets/
# Result: NONE FOUND
```

- ❌ No `aria-label`
- ❌ No `aria-describedby`
- ❌ No `aria-live` regions
- ❌ No `role` attributes (beyond semantic HTML)

**Keyboard Navigation**:
- ✅ Forms are keyboard accessible (native behavior)
- ✅ Buttons are keyboard accessible
- ⚠️ Custom radio buttons (dark theme) - need testing
- ⚠️ Toggle switches - need testing
- ❌ No visible focus indicators customized
- ❌ No skip links
- ❌ No keyboard shortcuts documented (except learning dashboard internal)

**Screen Reader Support**:
- ❌ No testing evident
- ❌ No screen reader-specific text
- ❌ No visually-hidden helpers
- ❌ Images missing alt text in some places

**Color Contrast**:
- ⚠️ Not validated against WCAG AA/AAA
- ⚠️ Light theme likely passes (dark text on light bg)
- ⚠️ Dark theme needs validation (light text on dark bg)
- ❌ No contrast checking in design process

**Focus Management**:
- ❌ No focus trapping in modals (no modals yet)
- ❌ No focus restoration after actions
- ❌ No programmatic focus management

**Constraints**:
- No accessibility testing tools
- No a11y linting
- No axe-core or similar
- No WAVE browser extension usage evident

**UX Implications**:
- Screen reader users may struggle
- Keyboard-only users may get stuck
- Low vision users may struggle with contrast
- Compliance risk (WCAG 2.1 AA should be target)

**Recommendation**:
- 🚨 **High Priority**: Add ARIA labels to interactive elements
- 🚨 **High Priority**: Test keyboard navigation
- 🔄 **Add**: Focus indicators
- 🔄 **Test**: Color contrast ratios
- 📋 **Future**: Automated a11y testing (axe-core, pa11y)

---

## Performance

### Current Approach

**Bundle Size**: N/A (no bundling)
- Each page loads independently
- Inline CSS (not cached across pages)
- Inline JavaScript (not cached across pages)

**External Dependencies**:
```html
<!-- Only external dependency -->
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
```

**Caching**:
- ❌ No cache headers observed
- ❌ No service worker
- ❌ No PWA manifest
- ❌ Static assets not versioned

**Loading Performance**:
- ✅ Small page sizes (HTML + inline CSS/JS)
- ✅ No framework overhead
- ✅ Fast initial render
- ⚠️ No code splitting (not applicable)
- ⚠️ No lazy loading

**API Performance**:
- Polling interval: 2s for workflows, 30s for dashboard
- No request debouncing observed
- No optimistic updates (except chat)
- No request caching client-side

**Constraints**:
- No build-time optimizations
- No minification
- No tree-shaking (not applicable)
- No image optimization pipeline

**UX Implications**:
- Fast initial loads (good!)
- Repeated visits reload everything (not cached)
- API polling can be wasteful
- No offline support

**Performance Observations**:
- ✅ Likely fast for alpha with low traffic
- ⚠️ Polling could be inefficient at scale
- ⚠️ No performance monitoring

**Recommendation**:
- ✅ **Current approach fine for alpha**
- 🔄 **Add**: Cache headers for static assets
- 🔄 **Consider**: Service worker for offline support
- 📋 **Future**: Performance monitoring (Web Vitals)

---

## Build & Deployment

### Current Process

**Build Process**: None
- No webpack, vite, rollup, or parcel
- No minification
- No bundling
- No transpilation
- No CSS processing

**Deployment**:
- Docker containers for services
- Python ASGI server (uvicorn)
- Port 8001 for web app
- Static files served by FastAPI

**Development**:
- No hot module replacement (HMR)
- Manual browser refresh required
- No development proxy
- No source maps (not needed - no build)

**Constraints**:
- Can't use TypeScript without build
- Can't use modern CSS features without PostCSS
- Can't use JSX or similar
- Can't optimize images at build time
- Can't tree-shake dependencies

**Benefits of Current Approach**:
- ✅ Instant deployments (no build time)
- ✅ Easy to debug (no source maps needed)
- ✅ Fast iteration cycle
- ✅ Simple deployment pipeline

**UX Implications**:
- Changes go live immediately
- Easy to experiment
- But: harder to maintain large codebase
- But: harder to enforce consistency

**Recommendation**:
- ✅ **Keep simple deployment for alpha**
- 🔄 **Consider**: Minimal build process (just CSS token processing)
- 📋 **Future**: Full build pipeline when needed

---

## Browser Support

### Target Browsers (Inferred)

**Current Code Assumes**:
- Modern JavaScript (ES6+)
- Fetch API
- CSS Grid and Flexbox
- CSS Custom Properties (for proposed tokens)

**Likely Supported**:
- ✅ Chrome 90+ (2021)
- ✅ Firefox 88+ (2021)
- ✅ Safari 14+ (2020)
- ✅ Edge 90+ (2021)

**NOT Supported**:
- ❌ Internet Explorer (any version)
- ❌ Old Android browsers
- ⚠️ Safari < 14 (some features may not work)

**No Polyfills**:
- No babel-polyfill
- No core-js
- No fetch polyfill
- Assumes modern browser

**Constraints**:
- Can't support IE11
- Can't support very old mobile browsers
- Alpha testers assumed to have modern browsers

**UX Implications**:
- Need to communicate browser requirements
- Users on old browsers will get broken experience
- No graceful degradation strategy

**Recommendation**:
- ✅ **Document minimum browser requirements**
- 🔄 **Add**: Browser detection and friendly error
- 📋 **Future**: Polyfills if older browser support needed

---

## Database & Backend Services

### Required Services (Docker)

**Running Services**:
```yaml
# docker-compose.yml
- PostgreSQL (port 5433)
- Redis (port 6379)
- ChromaDB (port 8000)
- Temporal (port 7233)
```

**Constraints**:
- User must have Docker installed
- Services must be running for app to work
- Setup wizard handles this (CLI)
- Web app assumes services available

**UX Implications**:
- Can't be "just open in browser"
- Requires technical setup
- If services crash, app breaks
- No error recovery UX

**Recommendation**:
- ✅ **Acceptable for alpha** (technical users)
- 🔄 **Add**: Service health check UI
- 🔄 **Add**: Graceful degradation if service down
- 📋 **Future**: Hosted version (no local Docker needed)

---

## Authentication & Security

### Current Implementation

**Authentication**:
- ✅ JWT tokens
- ✅ Bcrypt password hashing (12 rounds)
- ✅ HTTP-only cookies
- ✅ CSRF protection (via cookies)

**Constraints**:
- CLI-based account creation only
- No password reset flow
- No email verification
- No 2FA/MFA
- No OAuth (Google, GitHub login)

**UX Implications**:
- Can't create account from web
- Can't reset forgotten password
- Must use CLI for user management
- Technical barrier for non-technical users

**Recommendation**:
- 🚨 **High Priority**: Add web login UI
- 🔄 **Add**: Web signup form
- 📋 **Future**: Password reset flow
- 📋 **Future**: Social login (OAuth)

---

## Internationalization (i18n)

### Current State

**Language**: English only
- ❌ No i18n library
- ❌ No translation files
- ❌ Strings hard-coded in HTML/JS
- ❌ No locale support
- ❌ No RTL (right-to-left) support

**Constraints**:
- English-only product
- Can't support other languages without major refactor
- Dates/times use browser defaults

**UX Implications**:
- Limited to English-speaking users
- Can't expand globally without i18n

**Recommendation**:
- ✅ **Fine for alpha** (English-speaking testers)
- 📋 **Future**: i18next or similar if needed

---

## Error Handling & Logging

### Current Error Handling

**Frontend**:
```javascript
try {
  const response = await fetch(...);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "An API error occurred");
  }

  // Handle success
} catch (error) {
  // Show error message
  showError(error.message);
}
```

**Observed Patterns**:
- ✅ Try-catch blocks used
- ✅ Error messages shown to user
- ⚠️ Error messages vary in format
- ❌ No error tracking (Sentry, etc.)
- ❌ No error logging to backend
- ❌ No error IDs for support

**UX Implications**:
- Users see errors but can't report them effectively
- No way to debug user-reported issues
- Errors disappear on refresh
- No error history

**Recommendation**:
- 🔄 **Add**: Error tracking (Sentry, LogRocket)
- 🔄 **Add**: Error IDs shown to users
- 🔄 **Improve**: Consistent error message format

---

## Testing Infrastructure

### Current Testing

**Backend**:
- ✅ pytest for backend tests
- ✅ Integration tests exist
- ✅ Auth tests exist

**Frontend**:
- ❌ No Jest, Vitest, or Jasmine
- ❌ No Playwright or Cypress
- ❌ No visual regression testing
- ❌ No accessibility testing (axe-core)
- ❌ Manual testing only

**Constraints**:
- Can't do automated UI testing
- Can't regression test frontend
- Can't test user flows automatically
- Can't test accessibility automatically

**UX Implications**:
- Regressions may slip through
- Accessibility issues not caught
- Time-consuming manual testing
- Hard to maintain quality at scale

**Recommendation**:
- 🔄 **Add**: Playwright for E2E tests
- 🔄 **Add**: Accessibility linting (axe-core)
- 📋 **Future**: Visual regression tests

---

## Summary: Technical Constraints Impact on UX

### Strengths of Current Approach

1. ✅ **Simplicity**: No build complexity, easy to understand
2. ✅ **Fast iteration**: Changes deploy immediately
3. ✅ **Debugging**: Easy to debug without source maps
4. ✅ **Small footprint**: No framework overhead

### Limitations for UX

1. ❌ **Component reusability**: Hard to maintain consistency
2. ❌ **State management**: Manual updates error-prone
3. ❌ **Mobile support**: Minimal responsive design
4. ❌ **Accessibility**: No tooling or testing
5. ❌ **Real-time**: Polling instead of WebSockets
6. ❌ **Offline**: No service worker or caching

### Recommended Technical Improvements

#### Immediate (Alpha)
1. 🚨 Add CSS custom properties for design tokens
2. 🚨 Add ARIA labels and keyboard navigation testing
3. 🔄 Add mobile responsive breakpoints
4. 🔄 Extract shared styles to external CSS file

#### Short-term (Post-Alpha)
1. 🔄 Add lightweight JavaScript utilities (state helpers, templating)
2. 🔄 Implement WebSockets for real-time updates
3. 🔄 Add error tracking (Sentry)
4. 🔄 Add E2E testing (Playwright)

#### Long-term (v2.0+)
1. 📋 Consider lightweight framework (Preact, Alpine.js, htmx)
2. 📋 Add build process for optimization
3. 📋 PWA support (offline, installable)
4. 📋 Automated accessibility testing

---

## Constraints Matrix

| Feature | Current State | UX Impact | Priority |
|---------|---------------|-----------|----------|
| Component reuse | ❌ Manual duplication | Medium | 🔄 Short-term |
| Design tokens | ❌ Hard-coded | High | 🚨 Immediate |
| Mobile responsive | ⚠️ Minimal | High | 🚨 Immediate |
| Accessibility | ❌ Not tested | High | 🚨 Immediate |
| Real-time updates | ⚠️ Polling | Low | 📋 Future |
| Offline support | ❌ None | Low | 📋 Future |
| Error tracking | ❌ None | Medium | 🔄 Short-term |
| Testing | ⚠️ Backend only | Medium | 🔄 Short-term |
| State management | ❌ Manual | Medium | 🔄 Short-term |
| Build process | ❌ None | Low | 📋 Future |

---

**Document Version**: 1.0
**Last Updated**: 2025-11-13 20:00 PT
**Next**: Phase 2 - User Journey Mapping
