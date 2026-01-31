# Memo: Design Token Exceptions - Role & Collaboration Colors

**From**: Lead Developer
**To**: CXO
**Date**: 2026-01-27
**Re**: #430 Theme Consistency - Remaining hardcoded colors for your review

---

## Context

We've completed the design token migration (#430), converting ~95% of hardcoded CSS values to use the token system in `tokens.css`. This improves maintainability and enables future theming.

During the final review, we identified 3 hardcoded color values that don't map to existing tokens. PM and I agreed to accept these for now and seek your guidance on the longer-term approach.

## The Exception: Permission/Role Colors

**Location**: `web/static/css/permissions.css`

| Element | Color | Hex |
|---------|-------|-----|
| Owner badge | Indigo | `#667eea` |
| Share button | Violet | `#8b5cf6` |
| Share button hover | Darker violet | `#7c3aed` |

These colors distinguish:
- **Owner** status (who owns a resource)
- **Share/collaboration** actions (inviting others)

## Question for You

Should we:

1. **Add role-specific tokens** (e.g., `--color-role-owner`, `--color-role-admin`)?
   - Pro: Consistent role visualization across UI
   - Con: Expands token scope beyond core UI into domain semantics

2. **Add feature-specific tokens** (e.g., `--color-feature-collaboration`)?
   - Pro: Groups collaboration UI elements
   - Con: Opens door to many feature-specific tokens

3. **Leave as hardcoded exceptions**?
   - Pro: Simple, 3 values is manageable
   - Con: Manual maintenance, inconsistent with token philosophy

4. **Something else**?
   - Your design perspective welcome

## Also Deferred: Dark Mode

The `error-page.css` file has ~10 hardcoded colors in its `@media (prefers-color-scheme: dark)` block. We deferred this because dark mode needs a proper token system (dark mode variants of existing tokens). This is separate work.

## No Action Required Immediately

This is informational. We've accepted the current state and can revisit when you have capacity. The 3 permission colors work fine as-is.

---

*Response welcome whenever convenient. No urgency.*
