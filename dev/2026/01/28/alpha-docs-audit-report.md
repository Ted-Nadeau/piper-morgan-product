# Alpha Documentation Audit Report

**Date**: January 28, 2026
**Auditor**: Documentation Management Specialist
**Scope**: All alpha-facing documentation, email templates, release notes for v0.8.5
**Purpose**: Pre-send proofreading, currency, accuracy audit + qualitative editorial review

---

## Documents Reviewed (9 total)

| Document | Location | Lines | Last Updated |
|----------|----------|-------|-------------|
| ALPHA_QUICKSTART.md | docs/ | 407 | Jan 17, 2026 |
| ALPHA_TESTING_GUIDE.md | docs/ | 820 | Jan 19, 2026 |
| ALPHA_KNOWN_ISSUES.md | docs/ | 577 | Jan 8, 2026 |
| ALPHA_AGREEMENT_v2.md | docs/ | 154 | Dec 11, 2025 |
| Email template (canonical) | docs/operations/alpha-onboarding/ | 192 | Jan 27, 2026 |
| Email template (older copy) | docs/alpha/templates/ | 115 | Jan 27, 2026 |
| Release notes v0.8.5 | docs/releases/ | 192 | Jan 27, 2026 |
| Tester check-in template | docs/alpha/templates/ | 82 | Jan 5, 2026 |
| Tester profile template | docs/alpha/templates/ | 88 | Jan 5, 2026 |

---

## Part 1: Currency & Accuracy Issues

### CRITICAL (Blocks sending to testers)

**C1. ALPHA_QUICKSTART.md - Version mismatch throughout**
- Header says "Version: 0.8.5" but body still references **0.8.3** in 7+ places:
  - Line 209: "Testing Focus for 0.8.3"
  - Line 341: "What's Working in 0.8.3"
  - Lines 379, 398, 400: "602+ automated smoke tests" (now 5253)
  - Line 392: Links to `VERSION_NUMBERING.md` saying "what 0.8.3 means"
  - Line 398: "This is alpha software (0.8.3)"
  - Line 406: "Last Updated: January 17, 2026" (11 days stale)
- **Fix**: Update all 0.8.3 references to 0.8.5, update test count, update date

**C2. ALPHA_QUICKSTART.md - Screenshots are from 0.8.2 era**
- 5 screenshots in `docs/assets/images/alpha-onboarding/` dated Jan 18
- All show the setup wizard which has likely changed with MUX accessibility improvements
- Token system v1.1.0 means colors have changed
- **Fix**: PM needs to capture fresh screenshots from v0.8.5

**C3. ALPHA_KNOWN_ISSUES.md - Severely stale**
- Last Updated: January 8, 2026 (20 days old)
- Still says "Software Version: 0.8.4" in footer
- Test count says "2100+ tests" — actual is 5253
- Entire "Planned for Beta" section is empty placeholders: "[PM: Please populate based on roadmap]"
- "What to Ignore: UI polish (we know it's rough)" — but MUX-IMPLEMENT just fixed UI polish
- "All P0/P1 issues resolved as of November 23, 2025" — no mention of Jan 18-27 work
- **Fix**: Major refresh needed — update version, test counts, remove stale "what to ignore" guidance, populate beta section or remove it

**C4. Duplicate email templates**
- `docs/operations/alpha-onboarding/email-template.md` (v2.3, canonical, well-maintained)
- `docs/alpha/templates/alpha-tester-email-template.md` (older copy, has typo "Templatea" line 12)
- Both were updated to v0.8.5 by Lead Dev on Jan 27, but the older copy has:
  - Typo: "Email Templatea" (line 12)
  - Mentions "v0.8.3.1" in setup highlights section (line 61)
  - Different disk space claim: "2GB" vs "1GB" in canonical
  - Different time estimate: "45-60 minutes" vs "30-45 minutes"
- **Fix**: Delete the older copy or redirect to canonical. Having two creates confusion.

### IMPORTANT (Should fix before sending)

**I1. ALPHA_TESTING_GUIDE.md - Stale version references**
- Line 818: "Last updated: January 19, 2026" (9 days stale)
- Line 444: "Note for 0.8.4 Testers" — should reference 0.8.5
- Line 642: "Python 3.9+" — should be "Python 3.11+" (matches prerequisites)
- Line 81: Links to "ALPHA_AGREEMENT.md" but file is actually `ALPHA_AGREEMENT_v2.md`
- Line 127: Step 4 says "New in 0.8.2+" — remove "New" (it's been 4 releases)

**I2. ALPHA_TESTING_GUIDE.md - Missing 0.8.5 testing focus**
- "Priority Testing Areas" (line 446) still focuses on standup assistant and integration dashboard
- Missing: Lifecycle indicators, accessibility features, work items view, project detail view
- Missing: Any mention of MUX improvements, token system, ARIA

**I3. Release notes v0.8.5 - Minor upgrade path issue**
- Line 150: "git pull origin main" — should be "git pull origin production" for alpha testers
  (Testers clone from `production` branch, not `main`)

**I4. ALPHA_AGREEMENT_v2.md - Python version**
- Section 12: "Python 3.9+" — should be "Python 3.11+" to match all other docs

**I5. Older email template - "hosted version planned for 2026"**
- Line 80 of `alpha/templates/` version says "planned for 2026"
- We're IN 2026 now. The canonical version says "early 2026" which is also now past.
- **Fix**: Change to "later this year" or "later in 2026" or remove the claim

### MINOR (Nice to fix)

**M1. ALPHA_QUICKSTART.md - "Google Gemini (new in 0.8.2)"**
- Line 136: Gemini is no longer "new" — remove "(new in 0.8.2)"

**M2. ALPHA_KNOWN_ISSUES.md - Stale dates throughout**
- "Last Verified: December 24, 2025" for canonical query status
- "Nov 22-23, 2025" section headers still present
- These make the doc feel abandoned

**M3. ALPHA_TESTING_GUIDE.md - SSH clone instructions**
- Line 268: `git clone --depth 1 https://github.com/mediajunkie/piper-morgan-product.git`
- Missing `-b production` branch flag (quickstart has it, testing guide doesn't)

**M4. Screenshot images - Quickstart uses `<img>` tags, Testing Guide uses `![]()`**
- Lines 119-151 of Quickstart: `<img src="./assets/images/...">`
- Lines 384-427 of Testing Guide: `![](assets/images/...)`
- Path format differs: `./assets/` vs `assets/`
- Not broken, but inconsistent

---

## Part 2: Qualitative Editorial Review

### The Navigation Problem (Your Observation)

You identified the core structural issue: the Testing Guide serves three audiences with one document.

**Current structure** (820 lines):
1. Chapter 1: Setup (lines 25-436) — 411 lines, 50% of doc
2. Chapter 2: Testing (lines 438-617) — 179 lines, 22% of doc
3. Chapter 3: Troubleshooting (lines 619-820) — 201 lines, 25% of doc

**The problem**: A returning tester who just wants to test the new 0.8.5 features must scroll through 436 lines of setup (which they've already done) to find 179 lines of testing content. The doc has a "Quick Navigation" table at the top (line 9-17) with anchor links and a "Already have an account? Jump to Chapter 2" callout, which is good but insufficient for a doc this long.

**Recommended approach**: Improve in-document navigation rather than splitting into separate docs. Splitting would create maintenance burden (version numbers to update in 3 files instead of 1). Instead:

1. **Promote the Quick Nav** — Make it more prominent, add direct links to subsections
2. **Add a "Returning Tester" callout box** at the very top:
   ```
   ## Returning Tester? Start Here
   - **What's new in 0.8.5**: [anchor to What's New section]
   - **Testing scenarios**: [anchor to Chapter 2]
   - **Updated: Jan 28, 2026**
   ```
3. **Add a "What to Test in 0.8.5" section** at the start of Chapter 2 (currently missing — the doc still says "Focus on Integration Dashboard and OAuth")
4. **Consider collapsible sections** if these docs will be served as HTML (GitHub renders `<details>` tags)

### The "What's New" Stack Problem

Both Quickstart and Testing Guide accumulate "What's New" sections for each version. The Testing Guide now has 7 "What's New" sections (v0.8.3 through v0.8.5). This creates an archaeology experience — you're reading release notes in reverse chronological order for software you haven't used yet.

**Recommendation**:
- Keep only the current version's "What's New" prominently displayed
- Move older versions to a collapsible "Previous Release Notes" section or just link to the release notes files
- A new tester doesn't need to know what changed in 0.8.3.2 → 0.8.4

### ALPHA_KNOWN_ISSUES.md - Document Identity Crisis

This document tries to be three things:
1. Known bugs/issues list
2. Feature completeness matrix
3. Testing guide for what to focus on

The result is a 577-line document that's part changelog, part status board, part testing guide. The "What Works" section (lines 9-276) is 267 lines of things that are *fine* — which is useful for reference but buries the actual known issues.

**Recommendation**:
- Lead with the **known issues** (that's what the title promises)
- Move the completeness matrix to a separate section or the release notes
- The "What to Focus On" / "What to Ignore" guidance overlaps with Testing Guide Chapter 2

### Email Template Quality

The canonical email template (`docs/operations/alpha-onboarding/email-template.md`) is well-structured:
- Clear prerequisites
- Honest disclaimers
- Good "What Makes This Easy" framing
- Professional but approachable tone

One editorial note: the "P.S. You'll be tester #[2/3/4]" — given that you now have 6 testers, update the range or remove the specific number reference.

### Check-in and Profile Templates

Both are clean and well-designed. No issues found. The rotating question bank in the check-in template is a good approach for reducing survey fatigue.

---

## Part 3: Screenshots Audit

**5 screenshots exist** in `docs/assets/images/alpha-onboarding/`:
| File | Size | Date | Status |
|------|------|------|--------|
| setup-wizard-welcome.png | 597KB | Jan 18 | Needs refresh |
| setup-wizard-health-check.png | 182KB | Jan 18 | Needs refresh |
| setup-wizard-api-keys.png | 190KB | Jan 18 | Needs refresh |
| setup-wizard-user-creation.png | 103KB | Jan 18 | Needs refresh |
| setup-wizard-success.png | 78KB | Jan 18 | Needs refresh |

**Why refresh needed**: v0.8.5 includes MUX token system changes (color contrast fixes for 11 tokens), ARIA improvements, and potential layout changes from the design token migration. The setup wizard may visually differ from these screenshots.

**Screenshots NOT captured (should exist)**:
- Main chat interface (post-login)
- Lifecycle indicators on projects/todos
- Integration Settings dashboard
- Navigation with ARIA landmarks
- Any of the new views (Work Items, Project Detail)

**Recommendation**: Capture fresh screenshots for at minimum the existing 5 wizard steps. Consider adding 2-3 showing the actual app experience (chat, projects with lifecycle indicators, navigation).

---

## Part 4: Action Items Summary

### PM Actions Required (Cannot be done by agent)

| # | Action | Priority | Effort |
|---|--------|----------|--------|
| 1 | Capture 5 fresh setup wizard screenshots on v0.8.5 | HIGH | 10 min |
| 2 | Consider capturing 2-3 app experience screenshots | MEDIUM | 10 min |
| 3 | Decide: delete duplicate email template or designate canonical | HIGH | 2 min |
| 4 | Review "Planned for Beta" in KNOWN_ISSUES — populate or remove | MEDIUM | 15 min |
| 5 | Update tester number range in email template (currently says #2/3/4, have 6) | LOW | 1 min |
| 6 | Decide: "hosted version" claim — update timeframe or remove | LOW | 1 min |

### Agent Actions (I can do these with your approval)

| # | Action | Priority | Effort |
|---|--------|----------|--------|
| A1 | Fix all 0.8.3 → 0.8.5 references in QUICKSTART | HIGH | Quick |
| A2 | Update test counts (602 → 5253) across docs | HIGH | Quick |
| A3 | Update "Last Updated" dates across all docs | HIGH | Quick |
| A4 | Fix Python version 3.9 → 3.11 in Agreement and Testing Guide | HIGH | Quick |
| A5 | Fix "ALPHA_AGREEMENT.md" → "ALPHA_AGREEMENT_v2.md" link | MEDIUM | Quick |
| A6 | Fix Release Notes upgrade path (main → production) | MEDIUM | Quick |
| A7 | Add "Returning Tester" nav callout to Testing Guide top | MEDIUM | Moderate |
| A8 | Add "What to Test in 0.8.5" section to Testing Guide Ch. 2 | MEDIUM | Moderate |
| A9 | Remove "(new in 0.8.2)" labels from features in Quickstart | LOW | Quick |
| A10 | Fix typo "Templatea" in older email template (if keeping it) | LOW | Quick |
| A11 | Add `-b production` to Testing Guide clone command | MEDIUM | Quick |
| A12 | Refresh KNOWN_ISSUES version, test counts, stale dates | HIGH | Moderate |
| A13 | Consolidate "What's New" sections in Testing Guide | MEDIUM | Moderate |

---

## Summary Assessment

**Overall fitness for sending to testers**: Not yet ship-shape. The QUICKSTART and KNOWN_ISSUES documents have significant staleness issues that would undermine credibility with testers (mentioning 0.8.3, claiming 602 tests when there are 5253, empty "TBD" sections).

**Brightest spot**: The canonical email template and release notes are current and well-written.

**Biggest gap**: Screenshots need refresh, and KNOWN_ISSUES needs a major update.

**Recommended sequence**:
1. I fix the agent-actionable items (A1-A13)
2. You capture fresh screenshots
3. Quick review pass before sending

---

*Audit prepared by Documentation Management Specialist*
*January 28, 2026, 9:30 AM*
