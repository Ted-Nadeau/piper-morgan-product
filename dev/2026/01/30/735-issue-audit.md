# Audit: Issue #735 against feature.md template

**Date**: 2026-01-30
**Issue**: #735 - Finish: Mount History sidebar component (#425)

---

## Current Issue Content

```markdown
## Problem

History button in global nav does nothing. The component exists but was never mounted.

## Root Cause

`HistorySidebar.mount()` is never called:

1. `templates/home.html:1012` includes `history_sidebar.html`
2. This creates `window.HistorySidebar` object with methods
3. Navigation button calls `window.HistorySidebar.toggle()`
4. **BUT** `mount()` is never called, so DOM element doesn't exist

## Fix Needed

Add to `home.html` DOMContentLoaded handler:
```javascript
// Mount history sidebar
if (window.HistorySidebar) {
  HistorySidebar.mount(document.body);
}
```

## Design Question

There are TWO sidebar features:
1. **Left conversation sidebar** - shows past conversations list - WORKS
2. **Right history sidebar** (#425) - feature-rich view with search, date grouping - NOT MOUNTED

PM noted: "the tab for opening and closing the chat history sidebar works just fine"

Need to evaluate whether both are needed or if left sidebar is sufficient.

## Verification

- [ ] History button in nav opens right-side sidebar
- [ ] Search functionality works
- [ ] Date grouping (today, yesterday, this week, older) works
- [ ] Click conversation to view/continue

## Related

- Original feature: #425 MUX-IMPLEMENT-MEMORY-SYNC
- Trust gate fix: #732
```

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Header** | | |
| Title format: [LABEL]-[SHORT-NAME] | ⚠️ | Title is descriptive but doesn't follow template format |
| Priority | ❌ | Missing |
| Labels | ⚠️ | Has `bug` label, but issue is really "finish implementation" |
| Milestone | ❌ | Missing |
| Epic | ❌ | Missing (should reference #425 MUX-IMPLEMENT-MEMORY-SYNC) |
| Related | ✅ | Present |
| **Problem Statement** | | |
| Current State | ✅ | "History button does nothing" |
| Impact - Blocks | ❌ | Missing |
| Impact - User Impact | ⚠️ | Implied but not explicit |
| Impact - Technical Debt | ❌ | Missing |
| Strategic Context | ❌ | Missing (why now? how fits into larger goals?) |
| **Goal** | | |
| Primary Objective | ⚠️ | "Fix Needed" section implies it but not clearly stated |
| Example User Experience | ❌ | Missing |
| Not In Scope | ❌ | Missing - especially important given TWO sidebars |
| **What Already Exists** | | |
| Infrastructure ✅ | ✅ | Root cause shows component exists |
| What's Missing ❌ | ✅ | `mount()` call missing |
| **Requirements** | | |
| Phase 0: Investigation | ❌ | Missing (should answer Design Question first) |
| Phase 1: Tasks | ⚠️ | "Fix Needed" has one task but no phases |
| Phase Z: Completion | ❌ | Missing |
| **Acceptance Criteria** | | |
| Functionality | ⚠️ | "Verification" section has 4 items but unchecked format is right |
| Testing | ❌ | No unit test requirements |
| Quality | ❌ | No regression requirements |
| Documentation | ❌ | Missing |
| **Completion Matrix** | ❌ | Missing entirely |
| **Testing Strategy** | | |
| Unit Tests | ❌ | Missing |
| Integration Tests | ❌ | Missing |
| Manual Testing Checklist | ⚠️ | Partial in "Verification" section |
| **Success Metrics** | | |
| Quantitative | ❌ | Missing |
| Qualitative | ❌ | Missing |
| **STOP Conditions** | ❌ | Missing |
| **Effort Estimate** | ❌ | Missing |
| **Dependencies** | ❌ | Missing |
| **Related Documentation** | ⚠️ | Partial in "Related" |
| **Evidence Section** | ❌ | Missing |
| **Completion Checklist** | ❌ | Missing |

---

## Summary

| Status | Count |
|--------|-------|
| ✅ Present | 6 |
| ⚠️ Partial | 8 |
| ❌ Missing | 22 |

**TOTAL**: 36 items, 6 fully present (17%)

---

## Critical Issues

### 1. Design Question UNRESOLVED ⚠️

The issue identifies TWO sidebar components:
1. **Left sidebar** (#565) - works, simpler
2. **Right sidebar** (#425) - more features, not mounted

**Question needs PM decision**:
- Mount the right sidebar as designed?
- OR deprecate it in favor of left sidebar?
- OR merge features into one?

**This blocks the entire gameplan.**

### 2. Missing Phases

No phased approach. Should be:
- Phase 0: PM decision on Design Question
- Phase 1: Implementation (if mounting)
- Phase 2: Testing
- Phase Z: Completion

### 3. Wrong Label

Issue has `bug` label but it's really "incomplete implementation" from #425. Should be `finish` or `enhancement`.

---

## Actions Required

Before proceeding to gameplan:

1. **PM Decision Required**: Resolve Design Question (two sidebars)
2. **Rewrite issue** using feature.md template
3. **Add proper phases** based on PM decision
4. **Add acceptance criteria** with testable items
5. **Add completion matrix**
6. **Fix label** from `bug` to appropriate type

---

## STOP: PM Decision Needed

**The audit reveals this issue cannot proceed without PM clarification on the Design Question.**

Two options:
- **Option A**: Mount HistorySidebar (right sidebar) as designed in #425
- **Option B**: Mark #425 as superseded by #565 (left sidebar), close #735 as "won't fix"
- **Option C**: Merge features from right sidebar into left sidebar (new scope)

Awaiting PM direction before rewriting issue.
