# Memo: Design Token Exceptions — CXO Response

**From**: Chief Experience Officer
**To**: Lead Developer
**Date**: January 30, 2026
**Re**: Response to #430 Theme Consistency — Permission/Role Colors

---

## Short Answer

**Option 1, scoped narrowly**: Add semantic tokens for role/action visualization, but keep it tight.

---

## Reasoning

The key question is: **do these colors carry meaning, or are they just aesthetic choices?**

They carry meaning:
- Indigo = "this person owns this"
- Violet = "share/collaborate action"

When colors are semantic (meaning-carrying), they belong in the token system. The hex value `#667eea` doesn't tell a future developer anything. `--color-role-owner` tells them exactly what it means.

---

## Recommended Token Structure

```css
/* Role Visualization */
--color-role-owner: #667eea;

/* Action Types */
--color-action-collaborate: #8b5cf6;
--color-action-collaborate-hover: #7c3aed;
```

This is 3 tokens, not a slippery slope. The frame is:
- **Role tokens**: For visualizing user relationship to a resource (owner, admin, viewer, etc.)
- **Action tokens**: For visualizing action categories (collaborate, destructive, etc.)

If/when we add more roles or action types, they get tokens in these categories. If we don't, we have 3 well-named tokens instead of 3 magic hex values.

---

## Why Not the Other Options

**Option 2 (feature-specific tokens)**: "Collaboration" as a feature is too broad. The share button isn't really "collaboration feature" — it's a specific action type. Feature-based tokens would lead to `--color-feature-settings`, `--color-feature-chat`, etc. That's the wrong abstraction.

**Option 3 (leave as exceptions)**: Workable but philosophically inconsistent. We tokenize other semantic colors (success, warning, error). Role/action colors are equally semantic.

---

## On Dark Mode

Agreed — defer. Dark mode needs systematic treatment:
- Define dark variants for existing tokens
- Decide on approach (CSS custom properties with media query override, separate stylesheet, or theme class)
- Apply consistently

Not a "fix the error page" task. That's treating the symptom.

---

## Priority

**Low**. The 3 hardcoded values work fine. This is a "when you're in the area" improvement, not urgent work.

If you're doing any permission/role UI work and touch those CSS files anyway, adding the tokens then would be natural. Otherwise, it can wait.

---

*CXO*
*January 30, 2026*
