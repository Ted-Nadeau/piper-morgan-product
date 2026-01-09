# Phase 1.3: Visual Design Audit - Design Tokens
**UX Investigation - Piper Morgan**
**Date**: November 13, 2025, 18:59 PT
**Investigator**: Claude Code (UXR)

---

## Executive Summary

This document extracts all visual design elements from Piper Morgan's touchpoints and proposes a unified design token system. The audit reveals **two completely separate visual systems** (light and dark themes) with no shared tokens or variables, indicating ad-hoc styling without design system governance.

**Critical Finding**: Moving forward with **light theme as default** and **dark theme as user option** (per PM guidance), a comprehensive token system is required to ensure consistency.

---

## Color Audit

### Current Light Theme (home.html, standup.html)

#### Primary Colors
```css
/* Blues (Primary Actions) */
--color-primary:        #3498db;  /* Main blue - buttons, links */
--color-primary-hover:  #2980b9;  /* Darker blue - hover states */

/* Greens (Success States) */
--color-success-bg:     #d4edda;  /* Light green background */
--color-success-border: #c3e6cb;  /* Green border */
--color-success-text:   #155724;  /* Dark green text */
--color-metric-green:   #27ae60;  /* Metric values (standup) */

/* Reds (Error States) */
--color-error-bg:       #f8d7da;  /* Light red background */
--color-error-border:   #f5c6cb;  /* Red border */
--color-error-text:     #721c24;  /* Dark red text */

/* Standup-specific error (different!) */
--color-error-standup-bg:   #ffebee;  /* Even lighter red */
--color-error-standup-text: #c62828;  /* Different red */

/* Info States (Upload only) */
--color-info-bg:        #d1ecf1;  /* Light blue background */
--color-info-border:    #bee5eb;  /* Blue border */
--color-info-text:      #0c5460;  /* Dark cyan text */
```

#### Neutral Colors
```css
/* Backgrounds */
--color-bg-page:        #f5f5f5;  /* Page background */
--color-bg-container:   #ffffff;  /* Container/card background */
--color-bg-section:     #f8f9fa;  /* Section backgrounds */
--color-bg-code:        #f8f9fa;  /* Code blocks */
--color-bg-input:       #fdfdfd;  /* Chat window background */

/* Text */
--color-text-primary:   #2c3e50;  /* Headings, primary text */
--color-text-secondary: #7f8c8d;  /* Muted text, placeholders */
--color-text-disabled:  #bdc3c7;  /* Disabled buttons */

/* Borders */
--color-border-light:   #ecf0f1;  /* Input borders, separators */
--color-border-medium:  #444;     /* (Not used in light theme) */
```

#### Progress/Upload Colors
```css
/* Upload Progress */
--color-progress-start: #27ae60;  /* Gradient start */
--color-progress-end:   #2ecc71;  /* Gradient end */
```

---

### Current Dark Theme (learning-dashboard.html, personality-preferences.html)

#### Primary Colors
```css
/* Blues (Primary Actions) - DIFFERENT from light theme! */
--color-primary-dark:       #007acc;  /* Main blue (VS Code blue) */
--color-primary-dark-hover: #005a9e;  /* Darker blue hover */

/* Greens (Success States) */
--color-success-dark-bg:    #1e4620;  /* Dark green background */
--color-success-dark-text:  #4ade80;  /* Bright green text */
--color-success-dark-border:#4ade80;  /* Bright green border */

/* Reds (Error States) */
--color-error-dark-bg:      #4a1e1e;  /* Dark red background */
--color-error-dark-text:    #f87171;  /* Bright red text */
--color-error-dark-alt-bg:  #2d1b1b;  /* Darker red (messages) */
--color-error-dark-alt-text:#ff6b6b;  /* Different bright red */

/* Yellows (Warning/Loading States) */
--color-warning-dark-bg:    #4a4a1e;  /* Dark yellow background */
--color-warning-dark-text:  #fbbf24;  /* Bright yellow text */
--color-warning-dark-border:#fbbf24;  /* Bright yellow border */
```

#### Neutral Colors
```css
/* Backgrounds */
--color-bg-dark-page:       #1a1a1a;  /* Page background (very dark) */
--color-bg-dark-card:       #2d2d2d;  /* Card background */
--color-bg-dark-card-alt:   #2a2a2a;  /* Alternate card background */
--color-bg-dark-section:    #333;     /* Section/metric backgrounds */
--color-bg-dark-hover:      #3a3a3a;  /* Hover states */
--color-bg-dark-input:      #333;     /* Input backgrounds */

/* Text */
--color-text-dark-primary:  #e0e0e0;  /* Primary text */
--color-text-dark-secondary:#888;     /* Secondary text */
--color-text-dark-tertiary: #666;     /* Tertiary text (footer) */
--color-text-dark-muted:    #bbb;     /* Muted text (labels) */

/* Borders */
--color-border-dark-light:  #444;     /* Light borders */
--color-border-dark-medium: #555;     /* Medium borders */
--color-border-dark-accent: #007acc;  /* Accent borders (left side) */
```

#### Button Variants (Dark Theme Only)
```css
/* Secondary Buttons */
--color-btn-secondary-bg:       #555;
--color-btn-secondary-bg-hover: #666;

/* Danger Buttons */
--color-btn-danger-bg:          #dc2626;
--color-btn-danger-bg-hover:    #b91c1c;

/* Success Buttons */
--color-btn-success-bg:         #16a34a;
--color-btn-success-bg-hover:   #15803d;
```

---

## Proposed Unified Color System

### Strategy: Light Default + Dark Mode Option

Based on PM guidance ("light as default, dark as option"), propose a unified token system that supports both themes:

```css
/* === SEMANTIC COLOR TOKENS === */

/* Primary (Actions, Links, Focus) */
--color-primary-50:   #e3f2fd;  /* Lightest */
--color-primary-100:  #bbdefb;
--color-primary-200:  #90caf9;
--color-primary-300:  #64b5f6;
--color-primary-400:  #42a5f5;
--color-primary-500:  #3498db;  /* Base (current light theme) */
--color-primary-600:  #2980b9;  /* Current hover */
--color-primary-700:  #1976d2;
--color-primary-800:  #1565c0;
--color-primary-900:  #0d47a1;  /* Darkest */

/* Success (Positive actions, confirmations) */
--color-success-50:   #e8f5e9;
--color-success-100:  #c8e6c9;
--color-success-200:  #a5d6a7;
--color-success-300:  #81c784;
--color-success-400:  #66bb6a;
--color-success-500:  #27ae60;  /* Base (current metric green) */
--color-success-600:  #2e7d32;
--color-success-700:  #1b5e20;
--color-success-800:  #155724;  /* Current text green */
--color-success-900:  #0d3d17;

/* Error (Errors, destructive actions) */
--color-error-50:     #ffebee;
--color-error-100:    #ffcdd2;
--color-error-200:    #ef9a9a;
--color-error-300:    #e57373;
--color-error-400:    #ef5350;
--color-error-500:    #f44336;
--color-error-600:    #e53935;
--color-error-700:    #c62828;  /* Current standup error */
--color-error-800:    #b71c1c;
--color-error-900:    #721c24;  /* Current error text */

/* Warning (Caution, loading states) */
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

/* Info (Informational states) */
--color-info-50:      #e1f5fe;
--color-info-100:     #b3e5fc;
--color-info-200:     #81d4fa;
--color-info-300:     #4fc3f7;
--color-info-400:     #29b6f6;
--color-info-500:     #03a9f4;
--color-info-600:     #039be5;
--color-info-700:     #0288d1;
--color-info-800:     #0c5460;  /* Current info text */
--color-info-900:     #01579b;

/* Neutral (Backgrounds, text, borders) */
--color-neutral-0:    #ffffff;  /* Pure white */
--color-neutral-50:   #fafafa;
--color-neutral-100:  #f5f5f5;  /* Current page bg */
--color-neutral-200:  #eeeeee;
--color-neutral-300:  #e0e0e0;
--color-neutral-400:  #bdbdbd;
--color-neutral-500:  #9e9e9e;
--color-neutral-600:  #757575;
--color-neutral-700:  #616161;
--color-neutral-800:  #424242;
--color-neutral-900:  #212121;
--color-neutral-950:  #1a1a1a;  /* Current dark bg */
--color-neutral-1000: #000000;  /* Pure black */
```

### Light Mode Token Mapping
```css
:root,
[data-theme="light"] {
  /* Backgrounds */
  --bg-page:       var(--color-neutral-100);  /* #f5f5f5 */
  --bg-container:  var(--color-neutral-0);    /* #ffffff */
  --bg-section:    var(--color-neutral-50);
  --bg-hover:      var(--color-neutral-100);

  /* Text */
  --text-primary:   var(--color-neutral-900);
  --text-secondary: var(--color-neutral-600);
  --text-disabled:  var(--color-neutral-400);

  /* Borders */
  --border-light:   var(--color-neutral-200);
  --border-medium:  var(--color-neutral-300);
  --border-dark:    var(--color-neutral-400);

  /* Semantic */
  --primary:        var(--color-primary-500);
  --primary-hover:  var(--color-primary-600);
  --success:        var(--color-success-500);
  --error:          var(--color-error-500);
  --warning:        var(--color-warning-500);
  --info:           var(--color-info-500);
}
```

### Dark Mode Token Mapping
```css
[data-theme="dark"] {
  /* Backgrounds */
  --bg-page:       var(--color-neutral-950);  /* #1a1a1a */
  --bg-container:  var(--color-neutral-900);  /* #2d2d2d */
  --bg-section:    var(--color-neutral-800);
  --bg-hover:      var(--color-neutral-700);

  /* Text */
  --text-primary:   var(--color-neutral-100);
  --text-secondary: var(--color-neutral-400);
  --text-disabled:  var(--color-neutral-600);

  /* Borders */
  --border-light:   var(--color-neutral-800);
  --border-medium:  var(--color-neutral-700);
  --border-dark:    var(--color-neutral-600);

  /* Semantic - adjust for dark mode visibility */
  --primary:        #007acc;  /* VS Code blue, better for dark */
  --primary-hover:  #005a9e;
  --success:        #4ade80;  /* Brighter green for visibility */
  --error:          #f87171;  /* Brighter red */
  --warning:        #fbbf24;  /* Brighter yellow */
  --info:           #4fc3f7;  /* Brighter cyan */
}
```

---

## Typography Audit

### Current Typography (Consistent Across All Touchpoints)

```css
/* Font Families */
--font-family-base: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-family-mono: "Monaco", "Menlo", monospace;

/* Font Sizes (Observed) */
/* Home.html */
H1: 2.5em        /* "Piper Morgan" heading */
P (subtitle): 1.2em
Body: 16px
Input: 16px
Button: 16px
Example: 0.9em (varies)
Code inline: 0.9em
Label: 0.85em

/* Standup.html */
H1: 2.5em        /* Same as home */
H2: varies
Metric value: 2em
Metric label: smaller
Button: 16px

/* Learning Dashboard (Dark) */
H1: 2.5em        /* Consistent */
Subtitle: 1.1em
Card title: 1.4em
Metric value: 2.5em   /* LARGER than light theme */
Metric label: 0.9em
Button: 0.95em         /* SMALLER than light theme */

/* Personality Preferences (Dark) */
H1: 2.5em
Preference title: 1.3em
Description: 0.95em
Button: 16px
Label: 0.9em
```

### Inconsistencies Found

| Element | Light Theme | Dark Theme | Issue |
|---------|-------------|------------|-------|
| Metric Value | `2em` | `2.5em` | Different sizes |
| Button Text | `16px` | `0.95em` (~15px) | Mixed units |
| Subtitle | `1.2em` | `1.1em` | Slightly different |

---

### Proposed Typography Scale

Based on **type scale** methodology (1.25 ratio - Major Third):

```css
/* === TYPOGRAPHY TOKENS === */

/* Font Families */
--font-family-sans:    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
--font-family-mono:    "SF Mono", Monaco, "Cascadia Code", Menlo, Consolas, monospace;
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
--line-height-tight:   1.25;  /* Headings */
--line-height-normal:  1.5;   /* Body text */
--line-height-relaxed: 1.75;  /* Long-form content */

/* Letter Spacing */
--letter-spacing-tight:   -0.025em;
--letter-spacing-normal:   0;
--letter-spacing-wide:     0.025em;
--letter-spacing-wider:    0.05em;
--letter-spacing-widest:   0.1em;
```

### Semantic Typography Tokens
```css
/* Headings */
--heading-1-size:       var(--font-size-3xl);  /* 48px */
--heading-1-weight:     var(--font-weight-bold);
--heading-1-line-height: var(--line-height-tight);

--heading-2-size:       var(--font-size-2xl);  /* 39px */
--heading-2-weight:     var(--font-weight-semibold);
--heading-2-line-height: var(--line-height-tight);

--heading-3-size:       var(--font-size-xl);   /* 31px */
--heading-3-weight:     var(--font-weight-semibold);

--heading-4-size:       var(--font-size-lg);   /* 25px */
--heading-4-weight:     var(--font-weight-medium);

/* Body */
--body-size:            var(--font-size-base); /* 16px */
--body-weight:          var(--font-weight-normal);
--body-line-height:     var(--line-height-normal);

--body-sm-size:         var(--font-size-sm);   /* 12.8px */
--body-sm-line-height:  var(--line-height-normal);

/* UI Elements */
--button-size:          var(--font-size-base); /* 16px */
--button-weight:        var(--font-weight-semibold);

--input-size:           var(--font-size-base);
--input-weight:         var(--font-weight-normal);

--label-size:           var(--font-size-sm);
--label-weight:         var(--font-weight-medium);
--label-spacing:        var(--letter-spacing-wider);

/* Metrics */
--metric-value-size:    var(--font-size-2xl);  /* 39px - unified! */
--metric-value-weight:  var(--font-weight-bold);
--metric-label-size:    var(--font-size-xs);
--metric-label-weight:  var(--font-weight-medium);
--metric-label-spacing: var(--letter-spacing-widest);
```

---

## Spacing Audit

### Current Spacing (Observed)

```css
/* Container Padding */
Home container:     30px
Standup container:  30px
Learning card:      25px
Personality card:   25px

/* Button Padding */
Light theme:        15px 30px   (vertical horizontal)
Dark theme:         12px 24px   (DIFFERENT!)

/* Section Padding */
Light theme:        20px
Dark theme:         15px

/* Margins */
Section margins:    20px 0
Card margins:       20px 0
Message margins:    15px
Metric margins:     20px
```

### Inconsistencies

| Element | Light | Dark | Issue |
|---------|-------|------|-------|
| Card padding | 30px | 25px | Inconsistent |
| Button padding | 15px/30px | 12px/24px | Different scale |
| Section padding | 20px | 15px | Inconsistent |

---

### Proposed Spacing Scale

Based on **8px grid system** (common industry standard):

```css
/* === SPACING TOKENS === */

/* Base unit: 8px */
--space-0:   0;
--space-1:   0.25rem;  /* 4px  - 0.5x */
--space-2:   0.5rem;   /* 8px  - 1x base */
--space-3:   0.75rem;  /* 12px - 1.5x */
--space-4:   1rem;     /* 16px - 2x */
--space-5:   1.25rem;  /* 20px - 2.5x */
--space-6:   1.5rem;   /* 24px - 3x */
--space-7:   1.75rem;  /* 28px - 3.5x */
--space-8:   2rem;     /* 32px - 4x */
--space-10:  2.5rem;   /* 40px - 5x */
--space-12:  3rem;     /* 48px - 6x */
--space-16:  4rem;     /* 64px - 8x */
--space-20:  5rem;     /* 80px - 10x */
--space-24:  6rem;     /* 96px - 12x */

/* Semantic Spacing */
--padding-btn-sm:     var(--space-2) var(--space-4);   /* 8px 16px */
--padding-btn:        var(--space-3) var(--space-6);   /* 12px 24px */
--padding-btn-lg:     var(--space-4) var(--space-8);   /* 16px 32px */

--padding-card-sm:    var(--space-4);  /* 16px */
--padding-card:       var(--space-6);  /* 24px */
--padding-card-lg:    var(--space-8);  /* 32px */

--padding-container:  var(--space-8);  /* 32px - unified */

--margin-section:     var(--space-5) 0;  /* 20px 0 */
--margin-element:     var(--space-4) 0;  /* 16px 0 */

--gap-sm:             var(--space-2);  /* 8px */
--gap-md:             var(--space-4);  /* 16px */
--gap-lg:             var(--space-6);  /* 24px */
```

---

## Border Radius Audit

### Current Border Radius

```css
/* Observed Values */
Cards:              10px (light), 12px (dark)
Buttons:            8px (both)
Inputs:             8px (both)
Sections:           8px
Messages:           18px (chat bubbles!)
Badges/Pills:       20px (rounded)
Toggle switch:      26px (fully rounded)
Metric cards:       8px
Progress bar:       10px
```

### Inconsistencies

- Cards vary: 10px vs 12px
- Chat bubbles use 18px (unique)
- Badges use 20px (unique)
- No systematic scale

---

### Proposed Border Radius Scale

```css
/* === BORDER RADIUS TOKENS === */

--radius-none:   0;
--radius-sm:     0.25rem;  /* 4px */
--radius-base:   0.5rem;   /* 8px - default for most UI */
--radius-md:     0.75rem;  /* 12px */
--radius-lg:     1rem;     /* 16px */
--radius-xl:     1.25rem;  /* 20px */
--radius-2xl:    1.5rem;   /* 24px */
--radius-full:   9999px;   /* Fully rounded */

/* Semantic Radius */
--radius-button:      var(--radius-base);   /* 8px */
--radius-input:       var(--radius-base);   /* 8px */
--radius-card:        var(--radius-md);     /* 12px - unified */
--radius-badge:       var(--radius-full);   /* Pill shape */
--radius-message:     var(--radius-lg);     /* 16px - softer bubbles */
--radius-modal:       var(--radius-lg);     /* 16px */
```

---

## Shadow Audit

### Current Shadows

```css
/* Home.html */
.container box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);

/* Standup.html */
.metric box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

/* Learning Dashboard */
.card box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);  /* DARKER! */

/* No shadows on other elements */
```

### Inconsistencies

- Different blur radii: 10px vs 3px vs 6px
- Different opacities: 0.1 vs 0.3
- Dark theme has heavier shadows
- No consistent elevation system

---

### Proposed Shadow Scale

Based on **Material Design elevation**:

```css
/* === SHADOW TOKENS === */

/* Light Theme Shadows */
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

/* Dark Theme Shadows (heavier for depth) */
[data-theme="dark"] {
  --shadow-xs:  0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow-sm:  0 1px 3px 0 rgba(0, 0, 0, 0.4),
                0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow-md:  0 4px 6px -1px rgba(0, 0, 0, 0.5),
                0 2px 4px -1px rgba(0, 0, 0, 0.4);
  --shadow-lg:  0 10px 15px -3px rgba(0, 0, 0, 0.6),
                0 4px 6px -2px rgba(0, 0, 0, 0.5);
  --shadow-xl:  0 20px 25px -5px rgba(0, 0, 0, 0.7),
                0 10px 10px -5px rgba(0, 0, 0, 0.6);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
}

/* Semantic Shadows */
--shadow-card:    var(--shadow-md);   /* Elevated cards */
--shadow-modal:   var(--shadow-2xl);  /* Modals, dropdowns */
--shadow-button:  var(--shadow-sm);   /* Subtle button depth */
--shadow-hover:   var(--shadow-lg);   /* Hover state elevation */
```

---

## Transition/Animation Audit

### Current Transitions

```css
/* Button (Dark Theme) */
transition: all 0.2s ease;
transform: translateY(-1px);  /* Hover */

/* Progress Bar */
transition: width 0.3s ease;

/* Toggle Switch */
transition: 0.3s;  /* Background + dot */

/* Pattern Bar Fill */
transition: width 0.5s ease;
```

### Current Animations

```css
/* Spinner */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
animation: spin 1s linear infinite;

/* Pulsing Dot */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
animation: pulse 2s infinite;
```

---

### Proposed Animation Tokens

```css
/* === ANIMATION TOKENS === */

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

/* Common Animations */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## Z-Index Scale

### Current Z-Index Usage

**Not systematically observed** - no layering conflicts found yet, but need scale for future:

```css
/* === Z-INDEX TOKENS === */

--z-base:        0;      /* Default layer */
--z-dropdown:    1000;   /* Dropdowns */
--z-sticky:      1020;   /* Sticky headers */
--z-fixed:       1030;   /* Fixed elements */
--z-modal-backdrop: 1040; /* Modal backdrops */
--z-modal:       1050;   /* Modals */
--z-popover:     1060;   /* Popovers */
--z-tooltip:     1070;   /* Tooltips */
--z-notification: 1080;  /* Toast notifications */
--z-max:         9999;   /* Always on top */
```

---

## Container Width Audit

### Current Max Widths

```css
Home:                800px
Standup:             1000px
Learning Dashboard:  1400px
Personality:         800px
```

### Proposed Container System

```css
/* === CONTAINER TOKENS === */

--container-xs:   480px;   /* Mobile forms */
--container-sm:   640px;   /* Small content */
--container-md:   768px;   /* Standard content */
--container-lg:   1024px;  /* Wide content */
--container-xl:   1280px;  /* Dashboard layouts */
--container-2xl:  1536px;  /* Extra wide */
--container-full: 100%;    /* Full width */

/* Semantic Containers */
--container-form:      var(--container-sm);  /* 640px */
--container-content:   var(--container-md);  /* 768px */
--container-dashboard: var(--container-xl);  /* 1280px */
```

---

## Complete Token System Summary

### File Structure Recommendation

```
styles/
├── tokens/
│   ├── colors.css          /* All color tokens */
│   ├── typography.css      /* Font tokens */
│   ├── spacing.css         /* Spacing/sizing tokens */
│   ├── borders.css         /* Radius tokens */
│   ├── shadows.css         /* Shadow tokens */
│   ├── animations.css      /* Transition/animation tokens */
│   └── z-index.css         /* Layering tokens */
├── themes/
│   ├── light.css           /* Light theme mappings */
│   └── dark.css            /* Dark theme mappings */
└── components/
    ├── buttons.css         /* Button component styles */
    ├── forms.css           /* Form component styles */
    ├── cards.css           /* Card component styles */
    └── ... (more components)
```

### Usage Example

```css
/* Button using design tokens */
.button {
  /* Typography */
  font-family: var(--font-family-sans);
  font-size: var(--button-size);
  font-weight: var(--button-weight);

  /* Spacing */
  padding: var(--padding-btn);

  /* Colors (automatically theme-aware) */
  background-color: var(--primary);
  color: var(--color-neutral-0);

  /* Borders */
  border: none;
  border-radius: var(--radius-button);

  /* Shadows */
  box-shadow: var(--shadow-button);

  /* Transitions */
  transition: var(--transition-colors), var(--transition-transform);

  /* Cursor */
  cursor: pointer;
}

.button:hover {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-hover);
}

.button:disabled {
  background-color: var(--color-neutral-400);
  color: var(--color-neutral-600);
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}
```

---

## Key Findings Summary

### 🚨 Critical Issues

1. **Two Separate Color Systems**: Light uses `#3498db`, dark uses `#007acc` with no shared tokens
2. **Inconsistent Metric Sizes**: 2em vs 2.5em for same component
3. **Mixed Units**: px, em, rem used inconsistently
4. **No Design Token System**: All values hard-coded in components

### ⚠️ High Priority Issues

1. **Card Padding Varies**: 30px vs 25px
2. **Button Padding Varies**: 15px/30px vs 12px/24px
3. **Border Radius Varies**: 10px vs 12px for same element type
4. **Shadow Inconsistency**: Different blur/opacity across touchpoints

### 📋 Medium Priority

1. **No Spacing Scale**: No 4px/8px grid evident
2. **No Typography Scale**: Sizes chosen ad-hoc
3. **No Z-Index System**: Not needed yet, but will be
4. **Container Widths Vary**: 800px/1000px/1400px without system

---

## Recommendations

### Immediate Actions (Phase 3 - Design System)

1. **Implement Unified Token System**
   - Create CSS custom properties for all tokens
   - Light theme as default
   - Dark theme as opt-in [data-theme="dark"]

2. **Refactor Existing Styles**
   - Replace all hard-coded values with tokens
   - Unify light theme variations (home.html + standup.html)
   - Ensure dark theme uses same token references

3. **Document Token Usage**
   - Create style guide showing all tokens
   - Provide usage examples for each component
   - Define when to use each semantic token

### Future Enhancements

1. **Theme Switcher UI**
   - Add toggle in settings/preferences
   - Persist user preference
   - Smooth transition animation

2. **Component Library**
   - Build reusable components using tokens
   - Ensure all components support both themes
   - Create Storybook or similar documentation

3. **Accessibility Audit**
   - Verify color contrast ratios (WCAG AA)
   - Test with screen readers
   - Ensure keyboard navigation works

---

**Document Version**: 1.0
**Last Updated**: 2025-11-13 19:30 PT
**Next**: Phase 1.4 - Technical Constraints Documentation
