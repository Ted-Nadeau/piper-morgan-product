# DESIGN-TOKENS: Extract CSS Variables for Consistency
**Priority**: P2
**Labels**: `ux`, `design-system`, `technical-debt`
**Effort**: 3 days
**Sprint**: A11 (Pre-Beta)

---

## Problem Statement

Two separate color systems (light vs dark themes) with hard-coded values throughout. No CSS variables. Theme inconsistency confuses users. Technical debt makes changes expensive.

## Goal

Extract design tokens as CSS variables to enable consistent theming. Fix theme inconsistency. NOT full design system - just token extraction.

## Scope

**In Scope**:
- Create `/web/styles/tokens.css` with CSS variables
- Extract all colors to variables
- Extract spacing values (8px grid)
- Extract typography sizes
- Apply light theme everywhere (remove dark theme for now)
- Update all CSS to use variables

**Out of Scope**:
- Component library
- Dark theme toggle (defer to Beta)
- Full design system migration
- Documentation site
- Figma/design tools

## Acceptance Criteria

- [ ] All colors defined as CSS variables
- [ ] All spacing uses 8px grid variables
- [ ] All typography sizes as variables
- [ ] Zero hard-coded colors in CSS
- [ ] Consistent light theme on all pages
- [ ] One source of truth for design values

## Implementation Notes

```css
/* Example tokens.css */
:root {
  /* Colors */
  --color-primary: #3498db;
  --color-primary-hover: #2980b9;
  --color-success: #27ae60;
  --color-error: #e74c3c;

  /* Spacing (8px grid) */
  --space-1: 8px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;

  /* Typography */
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --font-size-lg: 20px;
}
```

## Success Metrics

- Theme consistency across all pages
- Future theme changes require editing 1 file (not 20)
- Foundation for dark theme later
- Reduced CSS file sizes

## Dependencies

- Complete after Tranche 3 (don't conflict)
- Before any Beta theming work

---

*This is Phase 1 of design system. Full component library is post-MVP.*
