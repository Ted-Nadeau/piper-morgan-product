# Subagent Prompt: #428 ARIA Labels Implementation

## Your Identity
You are a Coding Agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Mission
Audit all UI components for ARIA compliance and fix gaps, ensuring WCAG 2.1 AA screen reader accessibility.

## Context
- **GitHub Issue**: #428 MUX-IMPLEMENT-ARIA: ARIA Labels
- **Current State**: Some components have ARIA (dialog, toast, empty-state), but navigation, command palette, and place windows need systematic review
- **Target State**: All interactive components have proper ARIA attributes for screen reader users
- **Dependencies**: #430 Theme Consistency (COMPLETE)
- **Infrastructure Verified**: Templates exist at templates/components/

---

## Phase 0: Component Audit

**Tasks**:
1. Read each component template and document current ARIA state
2. Create audit matrix showing what exists vs what's needed

**Files to audit**:
- `templates/components/navigation.html`
- `templates/components/command_palette.html`
- `templates/components/place_window.html`
- `templates/home.html` (Places section)
- `templates/components/toast.html`
- `templates/components/spinner.html`
- `templates/components/confirmation-dialog.html`
- `templates/components/empty-state.html`

**Expected Output**:
```markdown
| Component | Current ARIA | Needed | Status |
|-----------|--------------|--------|--------|
| navigation.html | [list] | [list] | ✅/❌ |
```

---

## Phase 1: Navigation ARIA

**Required additions** (from ARIA Authoring Practices):
- `role="navigation"` on `<nav>` with `aria-label="Main navigation"`
- `aria-current="page"` on active nav item
- `aria-expanded` on dropdown triggers
- `aria-haspopup="true"` on dropdown triggers

**Reference pattern**:
```html
<nav role="navigation" aria-label="Main navigation">
  <a href="/" aria-current="page">Home</a>
  <button aria-expanded="false" aria-haspopup="true">Your stuff</button>
</nav>
```

---

## Phase 2: Command Palette ARIA

**Required additions** (combobox pattern):
- `role="dialog"` with `aria-modal="true"` on container
- `aria-label="Command palette"` on dialog
- `role="combobox"` on search input
- `aria-controls` linking input to results
- `role="listbox"` on results container
- `role="option"` on each result item
- `aria-activedescendant` for keyboard navigation (if JS handles this)

**Reference pattern**:
```html
<div role="dialog" aria-modal="true" aria-label="Command palette">
  <input role="combobox" aria-expanded="true"
         aria-controls="results" aria-activedescendant="result-1">
  <ul id="results" role="listbox">
    <li id="result-1" role="option" aria-selected="true">...</li>
  </ul>
</div>
```

---

## Phase 3: Place Windows & Remaining

**Required additions**:
- Place windows: `role="region"` with `aria-label="[Place name]"`
- Decorative emoji: `aria-hidden="true"`
- Toast: Verify `role="alert"` and `aria-live="assertive"`
- Spinner: Verify `role="status"` and `aria-live="polite"`

---

## Acceptance Criteria
- [ ] All components audited with matrix
- [ ] navigation.html has proper ARIA (role, aria-current, aria-expanded)
- [ ] command_palette.html has dialog/combobox ARIA
- [ ] place_window.html has region ARIA and hidden decorative elements
- [ ] toast.html has alert role verified
- [ ] spinner.html has status role verified
- [ ] No visual regressions (ARIA changes are invisible)

---

## Evidence Requirements

For EVERY change:
- Show the before/after diff
- Confirm no visual regression (structure only changed)

**Handoff format**:
```
## Issue #428 Completion Report
**Status**: Complete/Partial/Blocked

**Audit Matrix**:
[table of all components with ARIA status]

**Files Modified**:
- templates/components/navigation.html (+X lines)
- templates/components/command_palette.html (+X lines)
- [etc.]

**Changes Made**:
- navigation.html: Added role="navigation", aria-label, aria-current
- [etc.]

**Verification**:
- No visual changes (ARIA is structural only)
- All components now have proper screen reader semantics

**Blockers** (if any):
- [description]
```

---

## STOP Conditions
STOP immediately if:
- Component cannot be made accessible without redesign
- ARIA pattern conflicts with existing JavaScript behavior
- Template structure prevents proper ARIA implementation

Report the blocker and wait for PM decision.

---

## Constraints
- Do NOT add JavaScript (ARIA attributes only)
- Do NOT change visual appearance
- Do NOT modify CSS
- Preserve all existing functionality
- Use standard ARIA patterns from W3C APG
