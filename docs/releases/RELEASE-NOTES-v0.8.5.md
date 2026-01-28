# Release Notes: v0.8.5

**Release Date**: January 27, 2026
**Release Type**: Feature Release (MUX-IMPLEMENT Complete)

---

## Overview

**MUX-IMPLEMENT is complete!** This release completes the Modeled User Experience (MUX) super epic, delivering a fully accessible, consistent UI with lifecycle state support across all MUX objects.

**Key achievements in this release:**
- **WCAG 2.1 AA Accessibility**: Full contrast compliance and ARIA landmarks across all components
- **Design Token System**: Centralized CSS tokens with accessibility verification
- **Lifecycle State Persistence**: Database support for lifecycle states on projects, work items, features, and todos
- **Navigation and Command Palette**: Fully accessible keyboard navigation with ARIA patterns

---

## New Features

### MUX-IMPLEMENT Epic Complete (#403)

#### P1: Navigation & Command Palette (#419)
- Complete navigation component with ARIA landmarks
- Command palette with combobox ARIA pattern
- Keyboard navigation support throughout
- `aria-controls`, `aria-expanded`, `aria-activedescendant` attributes

**Files**: `templates/components/navigation.html`, `templates/components/command_palette.html`

#### P2: Document Access (#420, #421, #422)
- Document query pre-classifier improvements
- Portfolio integration
- Document management UI

#### P3: Conversation Model (#423, #424, #425, #426, #427)
- Conversation state management
- Follow-up detection with context
- Channel personality adapter
- ADR-049 ProcessRegistry for guided processes

**Commits**: `bbb741cd`, `92ee6cc7`, `43eb3706`, `70adf068`

#### P4: Accessibility & Polish (#428, #429, #430)
- Full ARIA accessibility audit and fixes
- WCAG 2.1 AA contrast compliance
- Theme consistency with design tokens

---

## Accessibility Improvements

### ARIA Accessibility (#428)

8 components audited and enhanced:
- **Navigation**: `role="navigation"`, `role="menu"`, `role="menuitem"`, `aria-current="page"`
- **Command Palette**: `role="combobox"`, `role="listbox"`, `role="option"`, `aria-activedescendant`
- **Home Places**: `role="region"`, `aria-labelledby`, `aria-live="polite"`
- **SVG Icons**: `aria-hidden="true"` for decorative elements

### WCAG 2.1 AA Contrast (#429)

22 color combinations tested, 11 failing colors fixed:

| Token | Before | After |
|-------|--------|-------|
| `--color-primary` | 3.15:1 | 4.84:1 |
| `--color-accent-success` | 2.87:1 | 4.72:1 |
| `--color-accent-error` | 3.82:1 | 4.85:1 |
| `--color-accent-warning` | 2.19:1 | 4.92:1 |
| `--color-text-secondary` | 2.56:1 | 5.24:1 |
| `--color-text-disabled` | 2.56:1 | 4.61:1 |

9 new tokens added including `-decorative` variants for brand color preservation.

**Documentation**: `docs/accessibility/contrast-audit-2026-01.md`

### Design Tokens v1.1.0 (#430)

- Centralized color, spacing, and typography tokens
- High contrast mode support (`prefers-contrast: more`)
- Reduced motion support (`prefers-reduced-motion: reduce`)
- Systematic token naming with WCAG ratios documented

**File**: `web/static/css/tokens.css`

---

## Bug Fixes

### Issue #718: Lifecycle State Column Missing
**Problem**: Database tables missing lifecycle_state column reported in investigation.

**Resolution**: Already fixed - migration `70847a6596f3` adds lifecycle_state VARCHAR(50) to features, work_items, projects, and todo_items tables.

**Commit**: Migration verified applied in production database.

---

## Architecture

### ADR-049: Two-Tier Intent Architecture
ProcessRegistry pattern for guided processes established.

**Commit**: `70adf068`

### Feature Lifecycle Serialization (#705)
Feature.to_dict() now includes lifecycle_state when present.

**Commit**: `c29f3a34`

---

## Test Results

```
=============== 5253 passed, 24 skipped ================
```

- All unit tests passing
- Accessibility audit verified
- Contrast ratios verified with automated testing
- 1000+ new tests added during MUX-IMPLEMENT

---

## Database Migrations

### Migration: 70847a6596f3

Adds `lifecycle_state` VARCHAR(50) nullable column to:
- `features`
- `work_items`
- `projects`
- `todo_items`

```bash
python -m alembic upgrade head
```

---

## Upgrade Notes

### For Existing Users

```bash
git pull origin main
python -m alembic upgrade head  # Adds lifecycle_state columns
python main.py
```

### For New Alpha Testers

```bash
git clone --depth 1 -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
./scripts/alpha-setup.sh
```

Visit http://localhost:8001/setup to create your account.

---

## Related Issues

| Issue | Type | Description |
|-------|------|-------------|
| #403 | Epic | MUX-IMPLEMENT - Complete UI Polish |
| #419 | Feature | Navigation & Command Palette |
| #420-422 | Feature | Document Access |
| #423-427 | Feature | Conversation Model |
| #428 | Feature | ARIA Accessibility |
| #429 | Feature | WCAG Contrast Compliance |
| #430 | Feature | Theme Consistency |
| #705 | Feature | Feature lifecycle serialization |
| #718 | Bug | Lifecycle state column verification |

---

## What's Next

- **M1: MVP Foundation** - Core MVP features
- **M2: MVP Activation** - User activation flow
- **M3: MVP Skills** - Skill system development
- **Alpha tester feedback** on new accessibility features

---

**Full Changelog**: [v0.8.4.3...v0.8.5](https://github.com/mediajunkie/piper-morgan-product/compare/v0.8.4.3...v0.8.5)
