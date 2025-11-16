# Combined Track A, B & C Cross-Check Verification Prompt for Cursor Agent

## Task
Perform automated code quality, accessibility, and integration verification for **all three tracks** (Track A, B, and C) implementation (G24, G42, G41, G57, G58, G59, G60, G48, G49, G26).

## Context
- Branch: `claude/ux-tranche3-feedback-accessibility-polish-015W99syFQ7b9HrV2WoB9S48`
- This is UX-TRANCHE3, a structured multi-track feature implementation
- Previous implementation: Polish Sprint (Tranche 2) with Toast, Loading, Form Validation
- All code should meet WCAG 2.2 Level AA accessibility standards

---

## Files to Verify

### TRACK A: Advanced Feedback Patterns

#### G24: Confirmation Dialogs
- [ ] `web/templates/components/confirmation-dialog.html` (48 lines)
- [ ] `web/static/css/dialog.css` (185 lines)
- [ ] `web/static/js/dialog.js` (182 lines)
- [ ] Integration in `templates/home.html`

#### G42: Skeleton Loading
- [ ] `web/templates/components/skeleton.html` (35 lines)
- [ ] `web/static/css/skeleton.css` (197 lines)

#### G41: Enhanced Error States
- [ ] `templates/404.html` (43 lines)
- [ ] `templates/500.html` (41 lines)
- [ ] `templates/network-error.html` (51 lines)
- [ ] `web/static/css/error-page.css` (344 lines)

---

### TRACK B: Accessibility Infrastructure

#### G57: Skip Links
- [ ] `web/templates/components/skip-link.html` (6 lines)
- [ ] `web/static/css/skip-link.css` (73 lines)
- [ ] Integration in all major pages

#### G58: Focus Management System
- [ ] `web/static/js/focus-manager.js` (269 lines)
- [ ] Integration in interactive pages

#### G59: Landmark Regions
- [ ] `docs/accessibility/landmark-regions.md` (284 lines)

#### G60: Color Contrast Audit
- [ ] `docs/accessibility/color-contrast-audit.md` (386 lines)

---

### TRACK C: Micro-Interactions & Polish

#### G48: Page Transitions
- [ ] `web/templates/components/page-transition.html` (12 lines)
- [ ] `web/static/css/page-transitions.css` (180 lines)
- [ ] `web/static/js/page-transitions.js` (195 lines)
- [ ] Integration in all major pages

#### G49: Hover & Focus States
- [ ] `web/static/css/hover-focus-states.css` (445 lines)

#### G26: Spacing System
- [ ] `web/static/css/spacing.css` (365 lines)
- [ ] `docs/design/spacing-system.md` (320 lines)

---

### Documentation & Validation
- [ ] `docs/track-a-validation.md` - Track A validation report
- [ ] `docs/track-b-validation.md` - Track B validation report
- [ ] `docs/track-c-validation.md` - Track C validation report

---

## Verification Checklist

### 1. File Structure & Creation (All Three Tracks)
```bash
# Verify all files exist
find web/templates/components web/static/css web/static/js templates docs/accessibility docs/design -type f | sort
```
- [ ] All 27 files from Track A, B, and C exist
- [ ] No empty or truncated files
- [ ] All files have proper newlines at EOF

---

### 2. Code Syntax Validation

#### JavaScript
```bash
# Check syntax for all three tracks
node -c web/static/js/dialog.js
node -c web/static/js/focus-manager.js
node -c web/static/js/page-transitions.js
```
- [ ] dialog.js has valid syntax
- [ ] focus-manager.js has valid syntax
- [ ] page-transitions.js has valid syntax
- [ ] No stray console.log statements (except intentional ones)
- [ ] No syntax errors in CSS files

#### HTML/Components
- [ ] All HTML components are well-formed
- [ ] No unclosed tags
- [ ] Proper attribute quoting

---

### 3. TRACK A: HTML/Component Validation

**confirmation-dialog.html**:
- [ ] Has `role="alertdialog"` with ARIA attributes
- [ ] `aria-modal="true"`, `aria-labelledby`, `aria-describedby` present
- [ ] `aria-hidden="true"` on initialization
- [ ] Close button with `onclick="Dialog.cancel()"`
- [ ] Two action buttons: Cancel and confirmation button

**skeleton.html**:
- [ ] Has 5 distinct skeleton variants
- [ ] All elements have `aria-busy="true"` and `aria-label`
- [ ] Proper class names for CSS targeting

**404.html, 500.html, network-error.html**:
- [ ] Proper DOCTYPE and HTML structure
- [ ] Include `/static/css/error-page.css` and `/static/css/base.css`
- [ ] Have `<main>` element with proper role
- [ ] Heading hierarchy correct (h1 for title, h2 for sections)
- [ ] Navigation buttons are semantic `<a>` or `<button>`
- [ ] network-error.html has online/offline event listener

---

### 4. TRACK B: HTML/Component Validation

**skip-link.html**:
- [ ] Single `<a>` tag with `href="#main-content"`
- [ ] Proper semantic structure
- [ ] Text: "Skip to main content"

---

### 5. TRACK A: JavaScript Validation (dialog.js)

**Public API**:
- [ ] `Dialog.show(config)` exists with proper signature
- [ ] `Dialog.confirm()` exists
- [ ] `Dialog.cancel()` exists
- [ ] `Dialog.close()` exists
- [ ] Helper functions: `confirmDelete()`, `confirmReset()`, `confirmClear()`

**Configuration Object**:
- [ ] Accepts: `title`, `message`, `confirmText`, `cancelText`, `onConfirm`, `onCancel`
- [ ] Sets aria attributes dynamically
- [ ] Updates button text

**Focus Management**:
- [ ] Saves focused element: `Dialog.focusedElementBeforeOpen`
- [ ] Restores focus after close
- [ ] Places focus on confirm button when dialog opens
- [ ] `_handleTabKey()` implements focus trap

**Keyboard Handling**:
- [ ] `_handleKeydown()` listens for Escape key
- [ ] Escape calls `Dialog.cancel()`
- [ ] Tab key handled by `_handleTabKey()`
- [ ] Event handlers added on show, removed on close

**Callbacks**:
- [ ] `confirmCallback` and `cancelCallback` stored and executed
- [ ] Callbacks cleared after execution (no memory leaks)

---

### 6. TRACK B: JavaScript Validation (focus-manager.js)

**Public API - All methods present**:
- [ ] `FocusManager.trap(element, autoFocusFirst)`
- [ ] `FocusManager.release(element)`
- [ ] `FocusManager.moveTo(target)`
- [ ] `FocusManager.getFocusableElements(container)`
- [ ] `FocusManager.isFocusable(element)`
- [ ] `FocusManager.getCurrentFocus()`
- [ ] `FocusManager.moveToNext(container)`
- [ ] `FocusManager.moveToPrevious(container)`
- [ ] `FocusManager.announce(text, priority)`

**Focus Stack**:
- [ ] `focusStack` array exists
- [ ] Each context has: element, previouslyFocused, keydownListener
- [ ] Supports nested modals

**Focus Trap**:
- [ ] `_handleTrapKeydown()` implements Tab cycling
- [ ] Tab/Shift+Tab cycles through focusable elements
- [ ] First element → focus moves to last (wrap around)
- [ ] Last element → focus moves to first (wrap around)

**Focusable Elements**:
- [ ] `getFocusableElements()` returns array of interactive elements
- [ ] Includes: a, button, input, select, textarea, [tabindex], audio, video
- [ ] Skips: disabled elements, hidden elements
- [ ] Uses getComputedStyle to check visibility

**Screen Reader Support**:
- [ ] `announce()` creates sr-only div with role="status"
- [ ] Uses aria-live="polite" or "assertive"
- [ ] Sets aria-atomic="true"
- [ ] Removes announcement after 1 second

**Utility Styles**:
- [ ] Creates .sr-only style if not present
- [ ] sr-only class properly hides visually but shows to screen readers

---

### 7. TRACK A: CSS Validation

**dialog.css**:
- [ ] `.confirmation-dialog` has `position: fixed`, `z-index: 2999`
- [ ] `.confirmation-dialog.active` shows dialog
- [ ] Modal backdrop: `rgba(0, 0, 0, 0.7)`
- [ ] Animation: `slideUp` keyframe exists
- [ ] `.btn-danger` exists with red color
- [ ] All buttons have hover and focus states
- [ ] Focus outline: 2px visible
- [ ] Mobile breakpoints: 768px and 480px
- [ ] `@media (prefers-reduced-motion: reduce)` disables animations

**skeleton.css**:
- [ ] Shimmer animation: `@keyframes shimmer`
- [ ] Animation duration: 1.5s infinite
- [ ] Gradient colors: #e0e0e0 to #f0f0f0
- [ ] Mobile breakpoints with reduced sizes
- [ ] Dark mode support
- [ ] `prefers-reduced-motion` uses static color instead

**error-page.css**:
- [ ] `.error-container` has `min-height: 100vh`
- [ ] `.error-content` has centered layout
- [ ] Icon animation: bounce keyframe
- [ ] All buttons have proper colors and hovers
- [ ] Help section has left border
- [ ] Mobile breakpoints: 768px, 480px
- [ ] `prefers-reduced-motion` removes animations
- [ ] Dark mode colors readable

---

### 8. TRACK B: CSS Validation

**skip-link.css**:
- [ ] `.skip-link` has `position: absolute`
- [ ] Positioned off-screen: `top: -40px`
- [ ] Shows on focus: `top: 0`
- [ ] Background color: `#3498db` (blue)
- [ ] Text color: white
- [ ] Focus outline: `3px solid #fff`
- [ ] `:focus-visible` for keyboard-only focus
- [ ] Mobile adjustments at 768px
- [ ] `prefers-reduced-motion` removes transition

---

### 9. TRACK C: CSS Validation

**page-transitions.css**:
- [ ] `.page-transition-overlay` has `position: fixed`, `z-index: 9999`
- [ ] `.page-transition-overlay.active` shows overlay
- [ ] Fade animations: `@keyframes fadeIn`, `fadeOut`
- [ ] Slide animations: `@keyframes slideUp`, `slideDown`
- [ ] Spinner animation: `@keyframes spin`
- [ ] `prefers-reduced-motion` disables animations
- [ ] High contrast mode support

**hover-focus-states.css**:
- [ ] Buttons have `transition: all 0.2s ease`
- [ ] Hover states: `translateY(-2px)` and `box-shadow`
- [ ] Focus states: 2px outline on all elements
- [ ] Links: underline + color change
- [ ] Form inputs: border-color + glow
- [ ] Cards: `translateY(-4px)` on hover
- [ ] Dark mode adjustments
- [ ] `prefers-reduced-motion` removes animations
- [ ] High contrast mode enhancements

**spacing.css**:
- [ ] CSS variables defined: `--space-xs` through `--space-5xl`
- [ ] Padding utilities: `.p-*`, `.px-*`, `.py-*`, `.pt-*`, `.pb-*`, `.pl-*`, `.pr-*`
- [ ] Margin utilities: `.m-*`, `.mx-*`, `.my-*`, `.mt-*`, `.mb-*`, `.ml-*`, `.mr-*`
- [ ] Gap utilities: `.gap-*`, `.row-gap-*`, `.col-gap-*`
- [ ] Common patterns: `.card-padding`, `.form-field-spacing`, etc.
- [ ] Mobile breakpoints at 768px (reduced spacing)
- [ ] Touch target minimum 48px

---

### 9.5. TRACK C: Integration Verification

**All pages (home.html, personality-preferences.html, standup.html, learning-dashboard.html)**:
- [ ] `page-transitions.css` linked in `<head>`
- [ ] `hover-focus-states.css` linked in `<head>`
- [ ] `spacing.css` linked in `<head>`
- [ ] `page-transition.html` component included in `<body>` (if needed)
- [ ] `page-transitions.js` loaded on appropriate pages

---

### 9. TRACK A: Integration Verification

**templates/home.html**:
- [ ] `dialog.css` linked in `<head>`
- [ ] `confirmation-dialog.html` included in `<body>`
- [ ] `dialog.js` loaded before `</body>`
- [ ] Proper script load order

---

### 10. TRACK B: Integration Verification

**All pages (home.html, personality-preferences.html, standup.html, learning-dashboard.html)**:
- [ ] `skip-link.css` linked in `<head>`
- [ ] `skip-link.html` included as first element in `<body>`
- [ ] Appears before navigation component

**Interactive pages (home.html, personality-preferences.html, standup.html)**:
- [ ] `focus-manager.js` loaded before other interactive scripts
- [ ] Proper script load order

---

### 11. Accessibility Compliance (WCAG 2.2 AA)

#### Color Contrast - TRACK A & B & C
- [ ] Dialog title: 7.8:1 (AAA)
- [ ] Dialog message: 5.2:1+ (AA)
- [ ] Danger button: 7.8:1 (AAA)
- [ ] Error title: 10.5:1+ (AAA)
- [ ] All buttons: 4.5:1+ (AA)

#### Color Contrast - TRACK B
- [ ] Skip link background: `#3498db` on white = 5.1:1 (AA)
- [ ] Skip link text: white on #3498db = 5.1:1 (AA)
- [ ] Focus outline: 3px white on blue = high contrast

#### Keyboard Navigation
- [ ] Tab navigates through elements
- [ ] Shift+Tab navigates backward
- [ ] Escape closes modals
- [ ] Enter confirms actions
- [ ] Focus visible on all interactive elements (2px+ outline)
- [ ] Focus trap in modals (can't escape with Tab)
- [ ] Skip link is first element in tab order

#### Screen Reader Support
- [ ] ARIA roles: alertdialog on modals
- [ ] aria-modal, aria-labelledby, aria-describedby on dialogs
- [ ] aria-hidden toggles visibility
- [ ] aria-busy on skeleton loaders
- [ ] All buttons have descriptive labels
- [ ] Links have clear text (not "Click here")

#### Focus Management
- [ ] Focus visible: 2px outline or similar
- [ ] Focus trap: Tab doesn't escape modal
- [ ] Focus restoration: Returns to opener after close
- [ ] First interactive element focused on dialog open
- [ ] Skip link focused when Tab pressed immediately

#### Motion & Animation
- [ ] `prefers-reduced-motion: reduce` disables animations
- [ ] Animations not essential (content accessible without)
- [ ] Animation duration reasonable (< 0.5s)

---

### 12. Pattern Consistency (vs Tranche 2)

Compare with existing patterns:
- [ ] Dialog.show() follows similar pattern to Toast.show()
- [ ] CSS organization matches existing files
- [ ] JavaScript uses same namespace pattern
- [ ] Component templates use same Jinja2 pattern
- [ ] Same comment header format in CSS

---

### 13. Common Issues Checklist

- [ ] No hardcoded IDs that could conflict
- [ ] No global scope pollution (functions in namespaces)
- [ ] No memory leaks (event listeners removed on close)
- [ ] No inline styles in HTML (all in CSS files)
- [ ] No deprecated HTML attributes
- [ ] Proper escaping of user input (XSS prevention)
- [ ] Error pages don't require authentication
- [ ] Skip link actually jumps to content (functional)

---

### 14. Documentation Quality

- [ ] `docs/track-a-validation.md` is comprehensive
- [ ] `docs/track-b-validation.md` is comprehensive
- [ ] Both documents well-organized and readable
- [ ] Examples and templates provided
- [ ] Accessibility deep dive sections present
- [ ] Testing checklists included

---

### 15. File Statistics

Run these to verify counts:
```bash
# Track A files
wc -l web/templates/components/confirmation-dialog.html \
    web/static/css/dialog.css \
    web/static/js/dialog.js \
    web/templates/components/skeleton.html \
    web/static/css/skeleton.css \
    templates/404.html \
    templates/500.html \
    templates/network-error.html \
    web/static/css/error-page.css

# Track B files
wc -l web/templates/components/skip-link.html \
    web/static/css/skip-link.css \
    web/static/js/focus-manager.js \
    docs/accessibility/landmark-regions.md \
    docs/accessibility/color-contrast-audit.md

# Track C files
wc -l web/templates/components/page-transition.html \
    web/static/css/page-transitions.css \
    web/static/js/page-transitions.js \
    web/static/css/hover-focus-states.css \
    web/static/css/spacing.css \
    docs/design/spacing-system.md

# All validation docs
wc -l docs/track-a-validation.md \
    docs/track-b-validation.md \
    docs/track-c-validation.md
```

**Expected totals**:
- Track A: ~1,200 lines
- Track B: ~900 lines
- Track C: ~1,500 lines
- Validation docs: ~880 lines

---

## Output Format

Please provide a report in this format:

```
# Combined Track A, B & C Verification Report

## Status Summary
### TRACK A
- G24 Confirmation Dialogs: ✅ PASS / ⚠️ ISSUES / ❌ FAIL
- G42 Skeleton Loading: ✅ PASS / ⚠️ ISSUES / ❌ FAIL
- G41 Enhanced Error States: ✅ PASS / ⚠️ ISSUES / ❌ FAIL

### TRACK B
- G57 Skip Links: ✅ PASS / ⚠️ ISSUES / ❌ FAIL
- G58 Focus Manager: ✅ PASS / ⚠️ ISSUES / ❌ FAIL
- G59 Landmark Regions: ✅ PASS / ⚠️ ISSUES / ❌ FAIL
- G60 Color Contrast Audit: ✅ PASS / ⚠️ ISSUES / ❌ FAIL

### TRACK C
- G48 Page Transitions: ✅ PASS / ⚠️ ISSUES / ❌ FAIL
- G49 Hover & Focus States: ✅ PASS / ⚠️ ISSUES / ❌ FAIL
- G26 Spacing System: ✅ PASS / ⚠️ ISSUES / ❌ FAIL

## File Verification
- All files exist: ✅
- All files have content: ✅
- All syntax valid: ✅

## Accessibility Compliance
- WCAG 2.2 AA: ✅ PASS / ⚠️ NEEDS REVIEW
- Color Contrast: ✅ PASS / ⚠️ NEEDS ATTENTION
- Keyboard Navigation: ✅ PASS / ⚠️ ISSUES
- Screen Reader Support: ✅ PASS / ⚠️ ISSUES

## Issues Found
1. [Issue description and file location]
2. [Next issue]

## Recommendations
1. [Recommendation if any]

## Overall Assessment
Ready for manual testing / Needs fixes before manual testing

## Critical vs Non-Critical

### Critical Issues (Block Manual Testing)
- [List any blocking issues]

### Non-Critical Issues (Can test manually, fix later)
- [List any minor issues]
```

---

## Critical Issues (Block Manual Testing)
- Any file missing or empty
- JavaScript syntax errors
- WCAG 2.2 AA violations (color contrast, keyboard nav, ARIA)
- Integration missing in templates
- Components not working due to missing dependencies

## Non-Critical Issues (Can test manually, fix later)
- Minor CSS refinements
- Animation timing adjustments
- Help text wording
- Mobile responsive tweaks
- Documentation formatting

---

## Quick Test Commands

```bash
# Verify all Track A, B & C files exist
find web/templates/components web/static/css web/static/js templates docs/accessibility docs/design \
  -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.md" | wc -l

# Check JavaScript syntax (all three tracks)
node -c web/static/js/dialog.js && \
node -c web/static/js/focus-manager.js && \
node -c web/static/js/page-transitions.js

# Count total lines (all tracks)
find web/templates/components web/static/css web/static/js templates docs/accessibility docs/design \
  -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.md" \) -exec wc -l {} + | tail -1

# Verify all integration points (Track A, B, C)
grep -r "dialog.css\|dialog.js\|confirmation-dialog\|skip-link.css\|skip-link\|focus-manager.js\|page-transitions.css\|page-transitions.js\|hover-focus-states.css\|spacing.css" templates/
```

---

Please run this verification on all three tracks (A, B, and C), then report your findings.
