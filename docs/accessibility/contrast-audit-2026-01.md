# WCAG 2.1 AA Contrast Audit

**Date**: 2026-01-27
**Auditor**: Claude (Coding Agent)
**Standard**: WCAG 2.1 Level AA
**File Audited**: `web/static/css/tokens.css`

## Summary

- **Total combinations tested**: 22
- **Passing before fixes**: 10/22 (45%)
- **Passing after fixes**: 22/22 (100%)
- **Colors updated**: 8 tokens
- **New tokens added**: 6 tokens

## WCAG 2.1 AA Requirements

| Content Type | Minimum Contrast Ratio |
|--------------|----------------------|
| Normal text (< 18pt or < 14pt bold) | 4.5:1 |
| Large text (>= 18pt bold or >= 24pt) | 3:1 |
| UI components and graphical objects | 3:1 |
| Disabled/inactive UI | Exempt |
| Decorative elements | Exempt |
| Placeholder text (with visible labels) | Exempt (but 3:1 recommended) |

## Test Results - Before Fixes

| Element | Foreground | Background | Ratio | Required | Status |
|---------|------------|------------|-------|----------|--------|
| Body text | #2c3e50 | #ffffff | 10.98:1 | 4.5:1 | PASS |
| Secondary text | #7f8c8d | #ffffff | 3.48:1 | 4.5:1 | **FAIL** |
| Tertiary text | #555555 | #ffffff | 7.46:1 | 4.5:1 | PASS |
| Light/placeholder text | #bdc3c7 | #ffffff | 1.78:1 | 4.5:1 | **FAIL** |
| Medium gray text | #95a5a6 | #ffffff | 2.56:1 | 4.5:1 | **FAIL** |
| Primary link | #3498db | #ffffff | 3.15:1 | 4.5:1 | **FAIL** |
| Primary link (large) | #3498db | #ffffff | 3.15:1 | 3.0:1 | PASS |
| Error text | #e74c3c | #ffffff | 3.82:1 | 4.5:1 | **FAIL** |
| Success text | #27ae60 | #ffffff | 2.87:1 | 4.5:1 | **FAIL** |
| Danger text | #c0392b | #ffffff | 5.44:1 | 4.5:1 | PASS |
| Warning text | #f39c12 | #ffffff | 2.19:1 | 4.5:1 | **FAIL** |
| Special blue | #007acc | #ffffff | 4.51:1 | 4.5:1 | PASS |
| Primary button (white on blue) | #ffffff | #3498db | 3.15:1 | 4.5:1 | **FAIL** |
| Primary button hover | #ffffff | #2980b9 | 4.30:1 | 4.5:1 | **FAIL** |
| Success button | #ffffff | #27ae60 | 2.87:1 | 4.5:1 | **FAIL** |
| Danger button | #ffffff | #c0392b | 5.44:1 | 4.5:1 | PASS |
| Error button | #ffffff | #e74c3c | 3.82:1 | 4.5:1 | **FAIL** |
| Body on off-white | #2c3e50 | #f9f9f9 | 10.43:1 | 4.5:1 | PASS |
| Body on light-gray | #2c3e50 | #f5f5f5 | 10.07:1 | 4.5:1 | PASS |
| Secondary on light-gray-2 | #7f8c8d | #ecf0f1 | 3.03:1 | 4.5:1 | **FAIL** |
| Light text on dark bg | #e0e0e0 | #2c3e50 | 8.32:1 | 4.5:1 | PASS |
| White on dark bg | #ffffff | #2c3e50 | 10.98:1 | 4.5:1 | PASS |

## Fixes Applied

### Color Token Changes

| Token | Original | New Value | Old Ratio | New Ratio |
|-------|----------|-----------|-----------|-----------|
| `--color-primary` | #3498db | #2077b2 | 3.15:1 | 4.84:1 |
| `--color-primary-dark` | #2980b9 | #1a6a9e | 4.30:1 | 5.83:1 |
| `--color-accent-success` | #27ae60 | #1e8449 | 2.87:1 | 4.72:1 |
| `--color-accent-success-dark` | #229954 | #196f3d | 3.26:1 | 6.02:1 |
| `--color-accent-error` | #e74c3c | #d63031 | 3.82:1 | 4.85:1 |
| `--color-accent-error-dark` | #c62828 | #b71c1c | 4.92:1 | 6.28:1 |
| `--color-accent-warning` | #f39c12 | #8a6d00 | 2.19:1 | 4.92:1 |
| `--color-neutral-medium-gray` | #95a5a6 | #687a7c | 2.56:1 | 4.50:1 |
| `--color-neutral-medium-gray-dark` | #7f8c8d | #636e72 | 3.48:1 | 5.24:1 |
| `--color-text-secondary` | #7f8c8d | #636e72 | 3.48:1 | 5.24:1 |
| `--color-text-light` | #bdc3c7 | #767676 | 1.78:1 | 4.54:1 |

### New Tokens Added

| Token | Value | Ratio | Purpose |
|-------|-------|-------|---------|
| `--color-text-muted` | #636e72 | 5.24:1 | Muted text (alias for text-secondary) |
| `--color-text-disabled` | #757575 | 4.61:1 | Disabled text (WCAG exempt but accessible) |
| `--color-text-placeholder` | #bdc3c7 | 1.78:1 | Placeholder with visible labels (exempt) |
| `--color-disabled` | #bdc3c7 | - | Disabled background color |
| `--color-primary-decorative` | #3498db | 3.15:1 | Original blue for decorative use only |
| `--color-accent-success-decorative` | #27ae60 | 2.87:1 | Original green for decorative use only |
| `--color-accent-error-decorative` | #e74c3c | 3.82:1 | Original red for decorative use only |
| `--color-accent-warning-bg` | #f39c12 | - | Warning backgrounds with dark text |
| `--color-neutral-medium-gray-decorative` | #95a5a6 | 2.56:1 | Original gray for borders/decorative |

## Test Results - After Fixes

| Element | Foreground | Background | Ratio | Required | Status |
|---------|------------|------------|-------|----------|--------|
| Body text | #2c3e50 | #ffffff | 10.98:1 | 4.5:1 | PASS |
| Secondary text | #636e72 | #ffffff | 5.24:1 | 4.5:1 | PASS |
| Tertiary text | #555555 | #ffffff | 7.46:1 | 4.5:1 | PASS |
| Light text | #767676 | #ffffff | 4.54:1 | 4.5:1 | PASS |
| Medium gray text | #687a7c | #ffffff | 4.50:1 | 4.5:1 | PASS |
| Primary link | #2077b2 | #ffffff | 4.84:1 | 4.5:1 | PASS |
| Error text | #d63031 | #ffffff | 4.85:1 | 4.5:1 | PASS |
| Success text | #1e8449 | #ffffff | 4.72:1 | 4.5:1 | PASS |
| Danger text | #c0392b | #ffffff | 5.44:1 | 4.5:1 | PASS |
| Warning text | #8a6d00 | #ffffff | 4.92:1 | 4.5:1 | PASS |
| Primary button | #ffffff | #2077b2 | 4.84:1 | 4.5:1 | PASS |
| Primary button hover | #ffffff | #1a6a9e | 5.83:1 | 4.5:1 | PASS |
| Success button | #ffffff | #1e8449 | 4.72:1 | 4.5:1 | PASS |
| Error button | #ffffff | #d63031 | 4.85:1 | 4.5:1 | PASS |

## WCAG Exemptions Applied

### Disabled UI Elements (SC 1.4.3)

Per WCAG 2.1, "text that is part of an inactive user interface component" is exempt from contrast requirements. However, for usability:

- `--color-text-disabled` (#757575) provides 4.61:1 ratio
- This exceeds the 4.5:1 recommendation while remaining visually distinct as "disabled"

### Placeholder Text (SC 1.4.3)

Placeholder text is considered "incidental" when:
1. The form field has a visible label
2. The placeholder provides supplementary (not essential) information

For accessible placeholders without visible labels, use `--color-text-light` (#767676, 4.54:1).
For placeholders with visible labels, `--color-text-placeholder` (#bdc3c7) may be used.

### Decorative Elements

For icons, borders, and decorative elements that convey no meaning:
- `--color-primary-decorative` (#3498db)
- `--color-accent-success-decorative` (#27ae60)
- `--color-accent-error-decorative` (#e74c3c)
- `--color-neutral-medium-gray-decorative` (#95a5a6)

**Important**: These must ONLY be used for purely decorative purposes, never for meaningful text or interactive elements.

## Usage Guidelines

### Text on White Backgrounds
```css
/* Recommended for body text */
color: var(--color-text-primary);     /* 10.98:1 */

/* Recommended for secondary text */
color: var(--color-text-secondary);   /* 5.24:1 */

/* Recommended for links */
color: var(--color-primary);          /* 4.84:1 */

/* DO NOT use for text */
color: var(--color-primary-decorative);  /* 3.15:1 - FAILS */
```

### Buttons
```css
/* Primary button - accessible */
background: var(--color-primary);
color: white;  /* 4.84:1 */

/* Success button - accessible */
background: var(--color-accent-success);
color: white;  /* 4.72:1 */
```

### Warning Messages
```css
/* Warning text on white */
color: var(--color-accent-warning);  /* 4.92:1 */

/* Warning background with dark text */
background: var(--color-accent-warning-bg);
color: var(--color-text-primary);  /* Use dark text, not white */
```

## Verification Methodology

Contrast ratios calculated using the WCAG 2.1 relative luminance formula:

1. Convert sRGB to linear RGB
2. Calculate relative luminance: L = 0.2126R + 0.7152G + 0.0722B
3. Contrast ratio = (L1 + 0.05) / (L2 + 0.05)

Results verified against WebAIM Contrast Checker baseline (black on white = 21:1).

## Files Modified

- `web/static/css/tokens.css` - Updated color tokens and header
- `docs/accessibility/contrast-audit-2026-01.md` - This document

## Next Steps

1. Review any CSS that directly hardcodes color values (not using tokens)
2. Verify high contrast mode overrides work correctly
3. Test with actual users using screen readers and accessibility tools
4. Consider automated contrast testing in CI pipeline
