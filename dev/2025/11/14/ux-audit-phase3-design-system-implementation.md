# Phase 3: Design System Foundations - Implementation Guide
**UX Investigation - Piper Morgan**
**Date**: November 14, 2025, 11:10 AM PT
**Investigator**: Claude Code (UXR)

---

## Executive Summary

This document provides an **actionable implementation guide** for Piper Morgan's design system, building on the comprehensive token audit from Phase 1.3. The design system will:

1. **Unify visual language** across light/dark themes
2. **Enable consistent theming** via CSS custom properties
3. **Accelerate development** with reusable components
4. **Support accessibility** with WCAG-compliant tokens
5. **Facilitate maintenance** by centralizing design decisions

**Critical Decision** (from PM): **Light theme as default, dark theme as user option**

**Implementation Strategy**: Incremental adoption using CSS custom properties (no build process required)

---

## Design System Philosophy

### Principles

1. **Progressive Enhancement**: Works without JavaScript, enhanced with it
2. **No Build Dependency**: CSS custom properties work in all modern browsers
3. **Accessible by Default**: WCAG AA color contrast minimum
4. **Mobile-First**: Responsive tokens and components
5. **Theme-Agnostic Components**: Components work in both light and dark themes

### Technical Constraints (from Phase 1.4)

- ✅ No build process (keep it simple)
- ✅ CSS custom properties supported (modern browsers only)
- ✅ Vanilla JavaScript (no React/Vue)
- ✅ Inline styles currently (will extract to external CSS)
- ❌ No TypeScript (can't type-check design tokens)
- ❌ No Sass/Less (can't use mixins/functions)

**Impact**: Design system must be implementable with pure CSS + vanilla JS

---

## Implementation Roadmap

### Phase 3.1: Foundation (Week 1) 🟢

**Goal**: Establish token system and basic infrastructure

**Deliverables**:
1. `/web/styles/tokens.css` - All design tokens
2. `/web/styles/themes/light.css` - Light theme mappings
3. `/web/styles/themes/dark.css` - Dark theme mappings
4. `/web/styles/reset.css` - CSS reset/normalize
5. Theme toggle JavaScript utility

**Effort**: ~2-3 days

---

### Phase 3.2: Core Components (Week 2-3) 🟡

**Goal**: Build reusable component library

**Deliverables**:
1. `/web/styles/components/buttons.css`
2. `/web/styles/components/forms.css`
3. `/web/styles/components/cards.css`
4. `/web/styles/components/typography.css`
5. `/web/styles/components/navigation.css`

**Effort**: ~5-7 days

---

### Phase 3.3: Page Migration (Week 4+) 🔴

**Goal**: Migrate existing pages to use design system

**Deliverables**:
1. Migrate `home.html` to use tokens
2. Migrate `standup.html` to use tokens
3. Migrate `learning-dashboard.html` to unified theme
4. Migrate `personality-preferences.html` to unified theme
5. Add navigation header to all pages

**Effort**: ~7-10 days

---

## Token System Implementation

### File Structure

```
web/
├── styles/
│   ├── tokens.css              # All design tokens (source of truth)
│   ├── themes/
│   │   ├── light.css           # Light theme mappings
│   │   └── dark.css            # Dark theme mappings
│   ├── base/
│   │   ├── reset.css           # CSS reset
│   │   ├── typography.css      # Base typography styles
│   │   └── layout.css          # Layout utilities
│   ├── components/
│   │   ├── buttons.css         # Button components
│   │   ├── forms.css           # Form components
│   │   ├── cards.css           # Card components
│   │   ├── navigation.css      # Navigation components
│   │   ├── messages.css        # Message/toast components
│   │   └── badges.css          # Badge/pill components
│   └── utils/
│       ├── spacing.css         # Spacing utilities
│       └── display.css         # Display/visibility utilities
├── assets/
│   └── (existing assets)
└── (existing files)
```

---

## Implementation Guide: tokens.css

### Complete Token Definitions

```css
/**
 * Piper Morgan Design Tokens
 *
 * These tokens are the source of truth for all design decisions.
 * Do not use hard-coded values in components - always reference tokens.
 *
 * Structure:
 * 1. Color Primitives (50-900 scales)
 * 2. Typography Tokens
 * 3. Spacing Tokens
 * 4. Border Tokens
 * 5. Shadow Tokens
 * 6. Animation Tokens
 * 7. Z-Index Tokens
 * 8. Container Tokens
 */

:root {
  /* ==========================================
     COLOR PRIMITIVES
     Base color scales (50-900)
     These are NOT used directly in components
     They are mapped to semantic tokens in theme files
     ========================================== */

  /* Primary (Blue) - Actions, links, focus states */
  --color-primary-50:   #e3f2fd;
  --color-primary-100:  #bbdefb;
  --color-primary-200:  #90caf9;
  --color-primary-300:  #64b5f6;
  --color-primary-400:  #42a5f5;
  --color-primary-500:  #3498db;  /* Base - current light theme */
  --color-primary-600:  #2980b9;  /* Hover */
  --color-primary-700:  #1976d2;
  --color-primary-800:  #1565c0;
  --color-primary-900:  #0d47a1;

  /* Success (Green) - Positive actions, confirmations */
  --color-success-50:   #e8f5e9;
  --color-success-100:  #c8e6c9;
  --color-success-200:  #a5d6a7;
  --color-success-300:  #81c784;
  --color-success-400:  #66bb6a;
  --color-success-500:  #27ae60;  /* Base */
  --color-success-600:  #2e7d32;
  --color-success-700:  #1b5e20;
  --color-success-800:  #155724;
  --color-success-900:  #0d3d17;

  /* Error (Red) - Errors, destructive actions */
  --color-error-50:     #ffebee;
  --color-error-100:    #ffcdd2;
  --color-error-200:    #ef9a9a;
  --color-error-300:    #e57373;
  --color-error-400:    #ef5350;
  --color-error-500:    #f44336;
  --color-error-600:    #e53935;
  --color-error-700:    #c62828;
  --color-error-800:    #b71c1c;
  --color-error-900:    #721c24;

  /* Warning (Yellow) - Caution, loading states */
  --color-warning-50:   #fff8e1;
  --color-warning-100:  #ffecb3;
  --color-warning-200:  #ffe082;
  --color-warning-300:  #ffd54f;
  --color-warning-400:  #ffca28;
  --color-warning-500:  #ffc107;
  --color-warning-600:  #ffb300;
  --color-warning-700:  #ffa000;
  --color-warning-800:  #ff8f00;
  --color-warning-900:  #ff6f00;

  /* Info (Cyan) - Informational states */
  --color-info-50:      #e1f5fe;
  --color-info-100:     #b3e5fc;
  --color-info-200:     #81d4fa;
  --color-info-300:     #4fc3f7;
  --color-info-400:     #29b6f6;
  --color-info-500:     #03a9f4;
  --color-info-600:     #039be5;
  --color-info-700:     #0288d1;
  --color-info-800:     #0c5460;
  --color-info-900:     #01579b;

  /* Neutral (Grays) - Backgrounds, text, borders */
  --color-neutral-0:    #ffffff;
  --color-neutral-50:   #fafafa;
  --color-neutral-100:  #f5f5f5;
  --color-neutral-200:  #eeeeee;
  --color-neutral-300:  #e0e0e0;
  --color-neutral-400:  #bdbdbd;
  --color-neutral-500:  #9e9e9e;
  --color-neutral-600:  #757575;
  --color-neutral-700:  #616161;
  --color-neutral-800:  #424242;
  --color-neutral-900:  #212121;
  --color-neutral-950:  #1a1a1a;
  --color-neutral-1000: #000000;

  /* ==========================================
     TYPOGRAPHY TOKENS
     Based on Major Third scale (1.25 ratio)
     ========================================== */

  /* Font Families */
  --font-family-sans:    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-family-mono:    "SF Mono", Monaco, "Cascadia Code", Menlo, Consolas, "Courier New", monospace;
  --font-family-display: var(--font-family-sans);

  /* Font Sizes (Major Third Scale: 1.25 ratio) */
  --font-size-xs:    0.64rem;   /* 10.24px */
  --font-size-sm:    0.8rem;    /* 12.8px */
  --font-size-base:  1rem;      /* 16px - body text */
  --font-size-md:    1.25rem;   /* 20px */
  --font-size-lg:    1.563rem;  /* 25px */
  --font-size-xl:    1.953rem;  /* 31.25px */
  --font-size-2xl:   2.441rem;  /* 39px */
  --font-size-3xl:   3.052rem;  /* 48.83px */

  /* Font Weights */
  --font-weight-normal:    400;
  --font-weight-medium:    500;
  --font-weight-semibold:  600;
  --font-weight-bold:      700;

  /* Line Heights */
  --line-height-tight:   1.25;
  --line-height-normal:  1.5;
  --line-height-relaxed: 1.75;

  /* Letter Spacing */
  --letter-spacing-tight:   -0.025em;
  --letter-spacing-normal:   0;
  --letter-spacing-wide:     0.025em;
  --letter-spacing-wider:    0.05em;
  --letter-spacing-widest:   0.1em;

  /* ==========================================
     SPACING TOKENS
     Based on 8px grid system
     ========================================== */

  --space-0:   0;
  --space-1:   0.25rem;  /* 4px */
  --space-2:   0.5rem;   /* 8px */
  --space-3:   0.75rem;  /* 12px */
  --space-4:   1rem;     /* 16px */
  --space-5:   1.25rem;  /* 20px */
  --space-6:   1.5rem;   /* 24px */
  --space-7:   1.75rem;  /* 28px */
  --space-8:   2rem;     /* 32px */
  --space-10:  2.5rem;   /* 40px */
  --space-12:  3rem;     /* 48px */
  --space-16:  4rem;     /* 64px */
  --space-20:  5rem;     /* 80px */
  --space-24:  6rem;     /* 96px */

  /* ==========================================
     BORDER TOKENS
     ========================================== */

  /* Border Radius */
  --radius-none:   0;
  --radius-sm:     0.25rem;  /* 4px */
  --radius-base:   0.5rem;   /* 8px */
  --radius-md:     0.75rem;  /* 12px */
  --radius-lg:     1rem;     /* 16px */
  --radius-xl:     1.25rem;  /* 20px */
  --radius-2xl:    1.5rem;   /* 24px */
  --radius-full:   9999px;

  /* Border Widths */
  --border-width-0:    0;
  --border-width-1:    1px;
  --border-width-2:    2px;
  --border-width-4:    4px;

  /* ==========================================
     SHADOW TOKENS
     Material Design-inspired elevation
     ========================================== */

  --shadow-xs:  0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-sm:  0 1px 3px 0 rgba(0, 0, 0, 0.1),
                0 1px 2px 0 rgba(0, 0, 0, 0.06);
  --shadow-md:  0 4px 6px -1px rgba(0, 0, 0, 0.1),
                0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg:  0 10px 15px -3px rgba(0, 0, 0, 0.1),
                0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl:  0 20px 25px -5px rgba(0, 0, 0, 0.1),
                0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);

  /* ==========================================
     ANIMATION TOKENS
     ========================================== */

  /* Durations */
  --duration-instant:  0ms;
  --duration-fast:     150ms;
  --duration-base:     200ms;
  --duration-moderate: 300ms;
  --duration-slow:     500ms;
  --duration-slower:   1000ms;

  /* Easing Functions */
  --ease-linear:       linear;
  --ease-in:           cubic-bezier(0.4, 0, 1, 1);
  --ease-out:          cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out:       cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce:       cubic-bezier(0.68, -0.55, 0.265, 1.55);

  /* Semantic Transitions */
  --transition-base:   all var(--duration-base) var(--ease-out);
  --transition-colors: background-color var(--duration-base) var(--ease-out),
                       color var(--duration-base) var(--ease-out),
                       border-color var(--duration-base) var(--ease-out);
  --transition-transform: transform var(--duration-base) var(--ease-out);
  --transition-opacity:   opacity var(--duration-moderate) var(--ease-in-out);

  /* ==========================================
     Z-INDEX TOKENS
     Layering system
     ========================================== */

  --z-base:            0;
  --z-dropdown:        1000;
  --z-sticky:          1020;
  --z-fixed:           1030;
  --z-modal-backdrop:  1040;
  --z-modal:           1050;
  --z-popover:         1060;
  --z-tooltip:         1070;
  --z-notification:    1080;
  --z-max:             9999;

  /* ==========================================
     CONTAINER TOKENS
     Max widths for layouts
     ========================================== */

  --container-xs:   480px;
  --container-sm:   640px;
  --container-md:   768px;
  --container-lg:   1024px;
  --container-xl:   1280px;
  --container-2xl:  1536px;
  --container-full: 100%;
}
```

---

## Implementation Guide: light.css

### Light Theme Mappings

```css
/**
 * Light Theme (Default)
 *
 * Maps primitive tokens to semantic usage.
 * Components reference these semantic tokens, not primitives.
 */

:root,
[data-theme="light"] {
  /* ==========================================
     SEMANTIC COLOR MAPPINGS - LIGHT THEME
     ========================================== */

  /* Backgrounds */
  --bg-page:       var(--color-neutral-100);  /* #f5f5f5 */
  --bg-container:  var(--color-neutral-0);    /* #ffffff */
  --bg-section:    var(--color-neutral-50);   /* #fafafa */
  --bg-hover:      var(--color-neutral-100);
  --bg-active:     var(--color-neutral-200);
  --bg-disabled:   var(--color-neutral-100);

  /* Text */
  --text-primary:   var(--color-neutral-900);  /* #212121 - headings */
  --text-secondary: var(--color-neutral-600);  /* #757575 - body text */
  --text-tertiary:  var(--color-neutral-500);  /* #9e9e9e - muted text */
  --text-disabled:  var(--color-neutral-400);  /* #bdbdbd */
  --text-on-primary: var(--color-neutral-0);   /* White text on primary bg */

  /* Borders */
  --border-light:   var(--color-neutral-200);  /* #eeeeee */
  --border-medium:  var(--color-neutral-300);  /* #e0e0e0 */
  --border-dark:    var(--color-neutral-400);  /* #bdbdbd */
  --border-focus:   var(--color-primary-500);  /* Focus indicator */

  /* Interactive States */
  --primary:        var(--color-primary-500);  /* #3498db */
  --primary-hover:  var(--color-primary-600);  /* #2980b9 */
  --primary-active: var(--color-primary-700);

  /* Semantic States */
  --success:        var(--color-success-500);
  --success-bg:     var(--color-success-50);
  --success-border: var(--color-success-200);
  --success-text:   var(--color-success-800);

  --error:          var(--color-error-500);
  --error-bg:       var(--color-error-50);
  --error-border:   var(--color-error-200);
  --error-text:     var(--color-error-900);

  --warning:        var(--color-warning-500);
  --warning-bg:     var(--color-warning-50);
  --warning-border: var(--color-warning-200);
  --warning-text:   var(--color-warning-900);

  --info:           var(--color-info-500);
  --info-bg:        var(--color-info-50);
  --info-border:    var(--color-info-200);
  --info-text:      var(--color-info-800);

  /* Component-Specific */
  --button-primary-bg:       var(--primary);
  --button-primary-hover-bg: var(--primary-hover);
  --button-primary-text:     var(--text-on-primary);

  --input-bg:        var(--bg-container);
  --input-border:    var(--border-medium);
  --input-focus-border: var(--border-focus);

  --card-bg:         var(--bg-container);
  --card-border:     var(--border-light);

  /* Shadows (light theme uses lighter shadows) */
  --shadow-card:    var(--shadow-md);
  --shadow-modal:   var(--shadow-2xl);
  --shadow-button:  var(--shadow-sm);
  --shadow-hover:   var(--shadow-lg);
}
```

---

## Implementation Guide: dark.css

### Dark Theme Mappings

```css
/**
 * Dark Theme (User Option)
 *
 * Same semantic tokens, different values.
 * Components automatically adapt via semantic references.
 */

[data-theme="dark"] {
  /* ==========================================
     SEMANTIC COLOR MAPPINGS - DARK THEME
     ========================================== */

  /* Backgrounds */
  --bg-page:       var(--color-neutral-950);  /* #1a1a1a */
  --bg-container:  var(--color-neutral-900);  /* #212121 */
  --bg-section:    var(--color-neutral-800);  /* #424242 */
  --bg-hover:      var(--color-neutral-700);
  --bg-active:     var(--color-neutral-600);
  --bg-disabled:   var(--color-neutral-800);

  /* Text */
  --text-primary:   var(--color-neutral-50);   /* #fafafa - headings */
  --text-secondary: var(--color-neutral-300);  /* #e0e0e0 - body */
  --text-tertiary:  var(--color-neutral-400);  /* #bdbdbd - muted */
  --text-disabled:  var(--color-neutral-600);  /* #757575 */
  --text-on-primary: var(--color-neutral-0);   /* White on primary */

  /* Borders */
  --border-light:   var(--color-neutral-800);
  --border-medium:  var(--color-neutral-700);
  --border-dark:    var(--color-neutral-600);
  --border-focus:   #007acc;  /* VS Code blue for dark mode */

  /* Interactive States - Adjusted for dark mode visibility */
  --primary:        #007acc;  /* VS Code blue */
  --primary-hover:  #005a9e;
  --primary-active: #004578;

  /* Semantic States - Brighter for dark background */
  --success:        #4ade80;  /* Bright green */
  --success-bg:     #1e4620;
  --success-border: #2d5a2d;
  --success-text:   #4ade80;

  --error:          #f87171;  /* Bright red */
  --error-bg:       #4a1e1e;
  --error-border:   #5a2d2d;
  --error-text:     #f87171;

  --warning:        #fbbf24;  /* Bright yellow */
  --warning-bg:     #4a4a1e;
  --warning-border: #5a5a2d;
  --warning-text:   #fbbf24;

  --info:           #4fc3f7;  /* Bright cyan */
  --info-bg:        #1e3a4a;
  --info-border:    #2d4a5a;
  --info-text:      #4fc3f7;

  /* Component-Specific */
  --button-primary-bg:       var(--primary);
  --button-primary-hover-bg: var(--primary-hover);
  --button-primary-text:     var(--text-on-primary);

  --input-bg:        var(--bg-section);
  --input-border:    var(--border-medium);
  --input-focus-border: var(--border-focus);

  --card-bg:         var(--bg-container);
  --card-border:     var(--border-light);

  /* Shadows (dark theme uses heavier shadows for depth) */
  --shadow-card:    0 4px 6px -1px rgba(0, 0, 0, 0.5),
                    0 2px 4px -1px rgba(0, 0, 0, 0.4);
  --shadow-modal:   0 25px 50px -12px rgba(0, 0, 0, 0.8);
  --shadow-button:  0 1px 3px 0 rgba(0, 0, 0, 0.4);
  --shadow-hover:   0 10px 15px -3px rgba(0, 0, 0, 0.6);
}
```

---

## Component Library: Buttons

### buttons.css

```css
/**
 * Button Components
 *
 * All buttons use semantic tokens from theme files.
 * They automatically adapt to light/dark themes.
 */

/* Base Button */
.btn {
  /* Typography */
  font-family: var(--font-family-sans);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-tight);

  /* Spacing */
  padding: var(--space-3) var(--space-6);  /* 12px 24px */

  /* Visual */
  border: var(--border-width-0);
  border-radius: var(--radius-base);  /* 8px */
  background-color: var(--button-primary-bg);
  color: var(--button-primary-text);
  box-shadow: var(--shadow-button);

  /* Interaction */
  cursor: pointer;
  transition: var(--transition-colors), var(--transition-transform);
  user-select: none;

  /* Layout */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}

.btn:hover:not(:disabled) {
  background-color: var(--button-primary-hover-bg);
  transform: translateY(-1px);
  box-shadow: var(--shadow-hover);
}

.btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: var(--shadow-button);
}

.btn:disabled {
  background-color: var(--bg-disabled);
  color: var(--text-disabled);
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.btn:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}

/* Button Sizes */
.btn-sm {
  font-size: var(--font-size-sm);
  padding: var(--space-2) var(--space-4);  /* 8px 16px */
}

.btn-lg {
  font-size: var(--font-size-md);
  padding: var(--space-4) var(--space-8);  /* 16px 32px */
}

/* Button Variants */
.btn-secondary {
  background-color: var(--bg-section);
  color: var(--text-primary);
  border: var(--border-width-1) solid var(--border-medium);
}

.btn-secondary:hover:not(:disabled) {
  background-color: var(--bg-hover);
  border-color: var(--border-dark);
}

.btn-danger {
  background-color: var(--error);
  color: var(--text-on-primary);
}

.btn-danger:hover:not(:disabled) {
  background-color: var(--color-error-600);
}

.btn-success {
  background-color: var(--success);
  color: var(--text-on-primary);
}

.btn-success:hover:not(:disabled) {
  background-color: var(--color-success-600);
}

/* Button with Icon */
.btn-icon {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
}

.btn-icon-only {
  padding: var(--space-3);
  aspect-ratio: 1;
}
```

---

## Usage Examples

### Example 1: Migrating home.html Button

**Before** (hard-coded):
```html
<style>
  .submit-btn {
    background: #3498db;
    color: white;
    padding: 15px 30px;
    border-radius: 8px;
    font-size: 16px;
  }
  .submit-btn:hover {
    background: #2980b9;
  }
</style>

<button class="submit-btn">Send</button>
```

**After** (using design system):
```html
<link rel="stylesheet" href="/web/styles/tokens.css">
<link rel="stylesheet" href="/web/styles/themes/light.css">
<link rel="stylesheet" href="/web/styles/components/buttons.css">

<button class="btn">Send</button>
```

**Benefits**:
- ✅ Automatically supports dark theme
- ✅ Consistent with all other buttons
- ✅ Accessible focus states
- ✅ Keyboard navigation built-in
- ✅ Less code to maintain

---

### Example 2: Theme Toggle Implementation

**JavaScript** (theme-toggle.js):
```javascript
/**
 * Theme Toggle Utility
 *
 * Persists user theme preference to localStorage.
 * Applies theme on page load.
 */

const STORAGE_KEY = 'piper-theme';
const THEME_ATTRIBUTE = 'data-theme';

class ThemeToggle {
  constructor() {
    this.currentTheme = this.loadTheme();
    this.applyTheme(this.currentTheme);
  }

  loadTheme() {
    // Check localStorage first
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) return stored;

    // Check system preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    return prefersDark ? 'dark' : 'light';
  }

  applyTheme(theme) {
    document.documentElement.setAttribute(THEME_ATTRIBUTE, theme);
    this.currentTheme = theme;
  }

  toggle() {
    const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
    this.applyTheme(newTheme);
    localStorage.setItem(STORAGE_KEY, newTheme);

    // Dispatch event for other components to react
    window.dispatchEvent(new CustomEvent('themechange', {
      detail: { theme: newTheme }
    }));
  }

  get theme() {
    return this.currentTheme;
  }
}

// Initialize on page load
const themeToggle = new ThemeToggle();

// Export for use in other scripts
window.piperTheme = themeToggle;
```

**HTML** (theme toggle button in navigation):
```html
<button
  id="theme-toggle"
  class="btn btn-secondary btn-icon-only"
  aria-label="Toggle theme"
  title="Toggle light/dark theme"
>
  <span id="theme-icon">🌙</span>
</button>

<script src="/web/scripts/theme-toggle.js"></script>
<script>
  const button = document.getElementById('theme-toggle');
  const icon = document.getElementById('theme-icon');

  // Update icon based on current theme
  function updateIcon() {
    icon.textContent = piperTheme.theme === 'light' ? '🌙' : '☀️';
  }

  button.addEventListener('click', () => {
    piperTheme.toggle();
    updateIcon();
  });

  // Listen for theme changes from other sources
  window.addEventListener('themechange', updateIcon);

  // Set initial icon
  updateIcon();
</script>
```

---

## Migration Strategy

### Step 1: Add Design System Files (Week 1, Day 1-2)

1. Create directory structure:
   ```bash
   mkdir -p web/styles/{tokens,themes,base,components,utils}
   mkdir -p web/scripts
   ```

2. Create token files (copy from this document):
   - `web/styles/tokens.css`
   - `web/styles/themes/light.css`
   - `web/styles/themes/dark.css`

3. Add theme toggle utility:
   - `web/scripts/theme-toggle.js`

---

### Step 2: Create Core Components (Week 1, Day 3-5)

Priority order:
1. `buttons.css` (highest usage)
2. `forms.css` (inputs, textareas, selects)
3. `cards.css` (containers, sections)
4. `typography.css` (headings, paragraphs, lists)
5. `navigation.css` (header, nav menu, breadcrumbs)

---

### Step 3: Migrate Pages One-by-One (Week 2-4)

**Recommended order**:
1. **home.html** (most visible, will set pattern)
2. **standup.html** (similar to home, easy win)
3. **personality-preferences.html** (complex, dark theme currently)
4. **learning-dashboard.html** (complex, dark theme currently)

**Migration Pattern** (for each page):
```html
<!-- OLD: Inline styles in <style> tag -->
<style>
  .container {
    max-width: 800px;
    background: #ffffff;
    padding: 30px;
    border-radius: 10px;
  }
</style>

<!-- NEW: Link to design system -->
<link rel="stylesheet" href="/web/styles/tokens.css">
<link rel="stylesheet" href="/web/styles/themes/light.css">
<link rel="stylesheet" href="/web/styles/base/reset.css">
<link rel="stylesheet" href="/web/styles/components/cards.css">
<link rel="stylesheet" href="/web/styles/components/buttons.css">
<script src="/web/scripts/theme-toggle.js"></script>

<!-- Page-specific styles (only if unique to this page) -->
<style>
  /* Keep only page-specific styles here */
  .unique-layout {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: var(--space-6);
  }
</style>
```

---

## Component Library (Continued)

### Forms Component

```css
/* forms.css */

.form-group {
  margin-bottom: var(--space-5);
}

.form-label {
  display: block;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
  letter-spacing: var(--letter-spacing-wider);
  text-transform: uppercase;
}

.form-input,
.form-textarea,
.form-select {
  /* Typography */
  font-family: var(--font-family-sans);
  font-size: var(--font-size-base);
  color: var(--text-primary);

  /* Visual */
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background-color: var(--input-bg);
  border: var(--border-width-1) solid var(--input-border);
  border-radius: var(--radius-base);

  /* Interaction */
  transition: var(--transition-colors);
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: var(--input-focus-border);
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-input:disabled,
.form-textarea:disabled,
.form-select:disabled {
  background-color: var(--bg-disabled);
  color: var(--text-disabled);
  cursor: not-allowed;
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: var(--text-tertiary);
}

/* Validation States */
.form-input.is-valid,
.form-textarea.is-valid {
  border-color: var(--success);
}

.form-input.is-invalid,
.form-textarea.is-invalid {
  border-color: var(--error);
}

.form-help-text {
  display: block;
  margin-top: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
}

.form-error-text {
  display: block;
  margin-top: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--error-text);
}
```

---

## Testing & Validation

### Accessibility Checklist

Before deploying design system:

- [ ] Color contrast meets WCAG AA (4.5:1 for text, 3:1 for UI)
- [ ] Focus indicators visible on all interactive elements
- [ ] Keyboard navigation works for all components
- [ ] Screen reader tested (VoiceOver/NVDA)
- [ ] ARIA labels on icon-only buttons
- [ ] Theme toggle announces state change

### Browser Testing

- [ ] Chrome 90+ (latest 2 versions)
- [ ] Firefox 88+ (latest 2 versions)
- [ ] Safari 14+ (latest 2 versions)
- [ ] Edge 90+ (latest 2 versions)

### Device Testing

- [ ] Desktop (1920x1080, 1366x768)
- [ ] Tablet (1024x768, 768x1024)
- [ ] Mobile (375x667, 414x896)

---

## Success Metrics

### Design System Adoption

- **Target**: 100% of pages using design system by Week 4
- **Measure**: Count of pages with `<link>` to tokens.css
- **Current Baseline**: 0% (all inline styles)

### Visual Consistency

- **Target**: Single color palette across all pages
- **Measure**: No hard-coded color values in HTML
- **Current Baseline**: 4 different color schemes

### Development Velocity

- **Target**: 50% faster to add new UI components
- **Measure**: Time to add button vs. current copy-paste
- **Current Baseline**: ~15 min to copy/paste/modify button

### Theme Coverage

- **Target**: 100% of UI elements support dark theme
- **Measure**: Manual testing of all touchpoints
- **Current Baseline**: 2/4 pages have dark theme

---

## Maintenance & Governance

### Design Token Updates

**Who can update tokens?**
- Design lead (you, PM)
- Frontend lead (with design approval)

**Process**:
1. Propose token change in issue/PR
2. Show visual diff (screenshots before/after)
3. Get design approval
4. Test in both themes
5. Merge and announce in changelog

### Adding New Components

**Template** (component-name.css):
```css
/**
 * Component Name
 *
 * Description: What this component does
 * Usage: How to use it
 * Variants: List available variants
 *
 * Example:
 * <div class="component-name component-variant">
 *   Content
 * </div>
 */

.component-name {
  /* Use semantic tokens only */
  /* Group properties logically */
  /* Comment complex decisions */
}
```

---

## Next Steps After Phase 3

Once design system is implemented:

1. **Add Navigation** (Phase 4 priority #1)
   - Header component with logo, nav links, theme toggle, user menu
   - Present on all pages
   - Mobile-responsive

2. **Notification System** (Phase 4 priority #2)
   - Toast/message component
   - Success/error/info/warning variants
   - Auto-dismiss with configurable duration

3. **Settings Index** (Phase 4 priority #3)
   - Central settings page
   - Links to all configuration areas
   - Breadcrumb navigation

4. **Mobile Optimization** (Phase 4 priority #4)
   - Responsive breakpoints
   - Touch-friendly hit targets (44px minimum)
   - Mobile navigation pattern

---

## Summary

### What We've Created

1. **Complete Token System**: 100+ design tokens covering colors, typography, spacing, borders, shadows, animations
2. **Theme Support**: Light (default) + Dark (user option) via CSS custom properties
3. **Component Library**: Buttons, forms, cards ready to implement
4. **Migration Strategy**: Incremental, page-by-page approach
5. **Governance**: Processes for maintaining design system

### Implementation Effort

- **Phase 3.1 (Foundation)**: 2-3 days
- **Phase 3.2 (Components)**: 5-7 days
- **Phase 3.3 (Migration)**: 7-10 days
- **Total**: ~3-4 weeks for complete design system

### Impact

- ✅ Unify fragmented visual language
- ✅ Enable dark theme across all pages
- ✅ Accelerate future development (50% faster)
- ✅ Improve accessibility (WCAG AA compliance)
- ✅ Reduce technical debt (no more inline styles)
- ✅ Support "wholeness of experience" (consistent across touchpoints)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-14 12:30 PM PT
**Next**: Phase 4 - Gap Analysis & Prioritization
