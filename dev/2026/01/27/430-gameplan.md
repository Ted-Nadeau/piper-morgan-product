# Gameplan: #430 MUX-IMPLEMENT-THEME-CONSISTENCY

**Issue**: #430
**Date**: January 27, 2026
**Author**: Lead Developer (Claude Code Opus)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Chief Architect's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (verified)
- [x] CSS architecture: tokens.css exists (230 lines, comprehensive)
- [x] Spacing utilities: spacing.css exists (252 lines, 8px grid)
- [x] Testing framework: pytest (verified)
- [x] Template location: templates/ directory (verified)

**My understanding of the task**:
- I believe we need to: Migrate hardcoded CSS values in templates to use design token variables
- I think this involves: Search/replace of hex colors, px values, and inline styles with var(--token) references
- I assume the current state is: tokens.css complete but underutilized; templates have hardcoded values

### Part A.2: Work Characteristics Assessment

**Worktree Assessment**:

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work
- [ ] Exploratory/risky changes

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min) - this is larger
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work

**Assessment**: **SKIP WORKTREE** - Single agent doing sequential template migration. Files are independent but work is sequential (audit → migrate → verify). No parallel agents needed.

### Part B: PM Verification Required

**What exists in the filesystem?**
```
web/static/css/tokens.css      # 230 lines, comprehensive design tokens
web/static/css/spacing.css     # 252 lines, spacing utilities
templates/*.html               # 15+ page templates
templates/components/*.html    # 27 component templates
```

**Recent work in this area?**
- November 2025: UX audit documented gaps G13-G19
- January 27, 2026: Design system deep dive confirmed tokens.css is underutilized

**Actual task needed?**
- [x] Add to existing application (migrate templates to use existing tokens)

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding is correct, gameplan appropriate

---

## Phase 0: Initial Bookending - Audit Hardcoded Values

### Purpose
Inventory all hardcoded values that need migration before making changes.

### Required Actions

1. **GitHub Issue Verification**
```bash
gh issue view 430
```

2. **Audit hex colors in templates**
```bash
grep -rn "#[0-9a-fA-F]\{3,6\}" templates/ --include="*.html" | grep -v "var(--"
```

3. **Audit hardcoded px values**
```bash
grep -rn "[0-9]\+px" templates/ --include="*.html" | head -50
```

4. **Create migration inventory**
Document each file with hardcoded values and what tokens they should use.

5. **Update GitHub Issue**
```bash
gh issue comment 430 --body "## Status: Investigation Started
- Auditing hardcoded values in templates
- Creating migration inventory
- Will report findings before proceeding"
```

### Deliverables
- Migration inventory table (file → hardcoded values → target tokens)

### Progressive Bookend
```bash
gh issue comment 430 -b "✓ Phase 0 complete: Audit inventory created. [X] hardcoded colors, [Y] hardcoded px values identified."
```

### STOP Conditions
- If a hardcoded value has no corresponding token → document and ask PM

---

## Phase 0.5: Frontend-Backend Contract Verification

**Skip this phase** - No API changes, CSS-only work.

---

## Phase 0.6: Data Flow & Integration Verification

**Skip this phase** - No data flow changes, CSS-only work.

---

## Phase 1: Template Migration - Core Pages

### Objective
Migrate home.html, projects.html, project_detail.html, work_items.html to use tokens.

### Tasks

**1.1 home.html Migration**
- [ ] Replace hardcoded hex colors with var(--color-*)
- [ ] Replace hardcoded px spacing with var(--space-*) or utility classes
- [ ] Verify tokens.css is loaded first in head
- [ ] Visual verification - no appearance change

**1.2 projects.html Migration**
- [ ] Replace hardcoded hex colors with var(--color-*)
- [ ] Replace hardcoded px spacing
- [ ] Visual verification

**1.3 project_detail.html Migration**
- [ ] Replace hardcoded hex colors with var(--color-*)
- [ ] Replace hardcoded px spacing
- [ ] Visual verification

**1.4 work_items.html Migration**
- [ ] Replace hardcoded hex colors with var(--color-*)
- [ ] Replace hardcoded px spacing
- [ ] Visual verification

### Evidence Required
- Before/after grep showing reduced hardcoded values
- Visual confirmation (pages look identical)

### Progressive Bookend
```bash
gh issue comment 430 -b "✓ Phase 1 complete: Core pages migrated (home, projects, project_detail, work_items). Visual verification: no regressions."
```

---

## Phase 2: Template Migration - Secondary Pages

### Objective
Migrate todos.html, standup.html, and other page templates.

### Tasks

**2.1 todos.html Migration**
- [ ] Replace hardcoded values
- [ ] Visual verification

**2.2 standup.html Migration**
- [ ] Replace hardcoded values
- [ ] Visual verification

**2.3 Remaining templates**
- [ ] documents.html
- [ ] files.html
- [ ] lists.html
- [ ] insights.html
- [ ] learning-dashboard.html
- [ ] settings pages

### Evidence Required
- Grep output showing migration progress

### Progressive Bookend
```bash
gh issue comment 430 -b "✓ Phase 2 complete: Secondary pages migrated. [X] files updated."
```

---

## Phase 3: Component CSS Audit

### Objective
Ensure component CSS files use tokens consistently.

### Tasks

**3.1 chat.css audit**
- [ ] Identify hardcoded values
- [ ] Replace with tokens where appropriate
- [ ] Note any values that should remain hardcoded (calculated/special)

**3.2 error-page.css audit**
- [ ] Same process

**3.3 Other CSS files** (spot check)
- [ ] Verify newer files already use tokens
- [ ] Document any exceptions

### Evidence Required
- Summary of changes made
- List of intentional exceptions (if any)

---

## Phase 4: Token Mapping Documentation

### Objective
Create reference for which token to use when.

### Tasks

**4.1 Create token usage guide**
- [ ] Document color token semantics (when to use primary vs accent)
- [ ] Document spacing scale usage (padding vs margin conventions)
- [ ] Document typography scale

**4.2 Add to PR checklist** (optional, PM approval needed)
- [ ] "CSS changes use design tokens from tokens.css"

### Deliverables
- `docs/internal/design/token-usage-guide.md` or section in existing doc

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **Verification grep**
```bash
# Count remaining hardcoded colors (should be minimal)
grep -rn "#[0-9a-fA-F]\{3,6\}" templates/ --include="*.html" | grep -v "var(--" | wc -l
```

2. **Visual verification**
- [ ] Home page looks identical
- [ ] Projects workflow (list → detail) consistent
- [ ] Work items page consistent
- [ ] No visual regressions

3. **GitHub issue update**
```bash
gh issue edit 430 --add-label "ready-for-review"
gh issue comment 430 --body "Implementation complete. Evidence: [summary]"
```

4. **Session log completion**
- [ ] All phases documented
- [ ] Evidence captured

### Success Criteria
- [ ] <10 hardcoded hex colors remaining in templates (down from ~50+)
- [ ] All core pages use tokens.css variables
- [ ] No visual regressions
- [ ] Token usage guide created

### PM Approval Request
```markdown
@PM - Issue #430 complete and ready for review:
- All acceptance criteria met ✓
- Evidence provided (grep counts, visual verification) ✓
- Token usage guide created ✓
- No visual regressions confirmed ✓

Please review and close if satisfied.
```

---

## Verification Gates

- [ ] Phase 0: Audit inventory complete
- [ ] Phase 1: Core pages migrated, visual verification passed
- [ ] Phase 2: Secondary pages migrated
- [ ] Phase 3: CSS audit complete
- [ ] Phase 4: Token usage guide created
- [ ] Phase Z: Final grep shows <10 hardcoded colors

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent | Task | Evidence Required |
|-------|-------|------|-------------------|
| 0-Z | Lead Dev (single) | Full implementation | Grep counts, visual verification |

**Rationale for single agent**: Sequential file-by-file work, no parallelization benefit. Each file must be audited → migrated → verified before next.

---

## STOP Conditions

Stop immediately and escalate if:
- Token missing for common pattern (need to add to tokens.css)
- Migration causes visual regression
- Performance impact detected
- Pattern conflict with #429 contrast requirements

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Visual regression | Low | Test each file immediately after migration |
| Missing token | Low | tokens.css is comprehensive; document if found |
| Browser compatibility | Very Low | CSS variables widely supported |

---

## Effort Estimate

**Overall**: Medium (4-6 hours)

| Phase | Estimate |
|-------|----------|
| Phase 0 (Audit) | 30 min |
| Phase 1 (Core pages) | 2 hours |
| Phase 2 (Secondary pages) | 1.5 hours |
| Phase 3 (CSS audit) | 1 hour |
| Phase 4 (Documentation) | 30 min |
| Phase Z (Verification) | 30 min |

---

## Token Mapping Reference

Quick reference for migration (from tokens.css):

| Hardcoded Value | Token Variable |
|-----------------|----------------|
| #3498db | var(--color-primary) |
| #2980b9 | var(--color-primary-dark) |
| #27ae60 | var(--color-accent-success) |
| #e74c3c | var(--color-accent-error) |
| #f5f5f5 | var(--color-neutral-light-gray) |
| #2c3e50 | var(--color-text-primary) |
| #7f8c8d | var(--color-text-secondary) |
| #ffffff | var(--color-neutral-white) |
| 4px | var(--space-xs) |
| 8px | var(--space-sm) |
| 16px | var(--space-md) |
| 24px | var(--space-lg) |
| 32px | var(--space-xl) |
| 30px | var(--space-lg) [close enough] |

---

_Gameplan created: January 27, 2026, 6:25 PM_
_Audit completed: January 27, 2026, 6:35 PM - All gaps fixed_
_Ready for PM approval_
