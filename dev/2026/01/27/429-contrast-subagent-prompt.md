# Subagent Prompt: #429 Contrast Testing

## Your Identity
You are a Coding Agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Mission
Verify and document contrast ratios for all color combinations in tokens.css, fixing any that fail WCAG 2.1 AA requirements.

## Context
- **GitHub Issue**: #429 MUX-IMPLEMENT-CONTRAST-TESTS: Contrast Testing
- **Current State**: tokens.css claims WCAG 2.2 AA compliance but no systematic verification exists. Known issue: disabled text #95a5a6 = 3.2:1 (fails 4.5:1 requirement)
- **Target State**: All color combinations verified and documented, failures fixed
- **Dependencies**: #430 Theme Consistency (COMPLETE - tokens now used consistently)
- **Infrastructure Verified**: tokens.css at web/static/css/tokens.css

---

## WCAG 2.1 AA Requirements

| Element Type | Required Ratio |
|--------------|----------------|
| Normal text (< 18pt / 24px) | 4.5:1 |
| Large text (≥ 18pt bold or ≥ 24px) | 3:1 |
| UI components & graphical objects | 3:1 |
| Focus indicators | 3:1 against adjacent |

---

## Phase 0: Inventory Color Combinations

**Task**: Extract all foreground/background color pairs from tokens.css

Read `web/static/css/tokens.css` and identify:
1. All text colors (--color-text-*, --color-neutral-*)
2. All background colors (--color-background-*, --color-neutral-*)
3. Button text/background combinations
4. Accent colors used for text (error, success, warning)

Create test matrix template.

---

## Phase 1: Calculate Contrast Ratios

**Use this formula** (or WebAIM reference):
- Convert hex to RGB
- Calculate relative luminance: L = 0.2126*R + 0.7152*G + 0.0722*B
- Contrast ratio = (L1 + 0.05) / (L2 + 0.05) where L1 > L2

**Required tests**:

| Element | FG Token | BG Token | Hex FG | Hex BG | Ratio | Pass? |
|---------|----------|----------|--------|--------|-------|-------|
| Body text | --color-text-primary | --color-background-primary | #2c3e50 | #ffffff | ? | ? |
| Secondary text | --color-text-secondary | --color-background-primary | #7f8c8d | #ffffff | ? | ? |
| Muted text | --color-text-muted | --color-background-primary | #95a5a6 | #ffffff | ? | ? |
| Disabled text | --color-text-disabled | white | #95a5a6 | #ffffff | 3.2:1 | ❌ KNOWN |
| Primary button | white | --color-primary | #ffffff | #3498db | ? | ? |
| Danger button | white | --color-accent-danger | #ffffff | #e74c3c | ? | ? |
| Success text | --color-accent-success | white | #27ae60 | #ffffff | ? | ? |
| Error text | --color-accent-error | white | #e74c3c | #ffffff | ? | ? |
| Links | --color-primary | --color-background-primary | #3498db | #ffffff | ? | ? |

**Place atmosphere tests** (test against lightest gradient stop):
- Issue tracking: text on #e8f4fc
- Communication: text on #dcfce7
- Temporal: text on #f3e8ff
- Documentation: text on #f3f4f6

---

## Phase 2: Fix Failures

**Known failure to fix**:
- `--color-text-disabled` / `--color-neutral-medium-gray` (#95a5a6) = 3.2:1
- Need: 4.5:1 minimum for text
- Solution: Darken to approximately #6b7b7d or similar (calculate exact value)

**For any new failures found**:
1. Calculate required color adjustment
2. Verify adjustment maintains visual coherence
3. Update tokens.css with new value
4. Re-test to confirm fix

---

## Phase 3: Documentation

**Create contrast audit report** at `docs/accessibility/contrast-audit-2026-01.md`:

```markdown
# Contrast Audit Report - January 2026

## Summary
- Total combinations tested: X
- Passing: X
- Fixed: X
- Remaining issues: 0

## Results Table
[full table with all ratios]

## Fixes Applied
- --color-text-disabled: #95a5a6 → #XXXXXX (3.2:1 → X.X:1)

## Verification
- All text combinations ≥ 4.5:1
- All UI components ≥ 3:1
```

**Update tokens.css header** with verification date.

---

## Acceptance Criteria
- [ ] All token color combinations inventoried
- [ ] All combinations tested with documented ratios
- [ ] All normal text ≥ 4.5:1
- [ ] All large text ≥ 3:1
- [ ] All UI components ≥ 3:1
- [ ] Disabled text fixed (currently 3.2:1)
- [ ] Contrast audit report created
- [ ] tokens.css header updated with verification date

---

## Evidence Requirements

**Handoff format**:
```
## Issue #429 Completion Report
**Status**: Complete/Partial/Blocked

**Contrast Audit Results**:
| Element | FG | BG | Ratio | Pass |
|---------|----|----|-------|------|
[full table]

**Fixes Applied**:
- [token]: [old value] → [new value] ([old ratio] → [new ratio])

**Files Modified**:
- web/static/css/tokens.css (+X/-Y lines) - if fixes needed
- docs/accessibility/contrast-audit-2026-01.md (new file)

**Verification**:
- X/X combinations passing WCAG AA
- No visual regressions

**Blockers** (if any):
- [description]
```

---

## STOP Conditions
STOP immediately if:
- Brand color cannot meet contrast requirements (need design decision)
- Fix would significantly change visual appearance
- Place atmosphere colors fail and require redesign

Report the blocker and wait for PM decision.

---

## Constraints
- Do NOT change brand identity colors without approval
- Do NOT modify anything except tokens.css (if fixes needed)
- Maintain visual coherence - adjustments should be subtle
- Document all calculations

---

## Reference: Contrast Calculation

For hex color #RRGGBB:
1. Convert to RGB (0-255)
2. Convert to sRGB: c = c/255
3. Linearize: c = c <= 0.03928 ? c/12.92 : ((c+0.055)/1.055)^2.4
4. Luminance L = 0.2126*R + 0.7152*G + 0.0722*B
5. Ratio = (max(L1,L2) + 0.05) / (min(L1,L2) + 0.05)

Or use: https://webaim.org/resources/contrastchecker/
