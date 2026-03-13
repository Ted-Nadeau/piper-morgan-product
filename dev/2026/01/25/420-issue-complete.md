# MUX-NAV-UTILITY - Navigation Utility Layer

**Priority**: P1
**Labels**: `MUX-IMPLEMENT`, `navigation`, `consciousness`
**Milestone**: Sprint P1 (Navigation Breakthrough)
**Epic**: #418 MUX-IMPLEMENT
**Related**: #419 (Home State), #421 (Command Palette), #684 (Places), ADR-045, ADR-053

---

## Problem Statement

### Current State
~~Current navigation components (`templates/components/navigation.html`, ~730 lines) were "vibe coded" before MUX consciousness work:~~
~~- Dropdown menu of data types: "Todos", "Projects", "Files", "Lists"~~
~~- Static structure regardless of trust level~~
~~- No consciousness grammar (treats Piper as filing system)~~
~~- No awareness of what user needs right now~~

**RESOLVED**: Navigation now uses consciousness grammar vocabulary, is trust-gated, and supports command palette integration.

### Impact
- ~~**Blocks**: #419 establishes home as primary experience; nav must support (not compete with) this paradigm~~
- ~~**User Impact**: Users see nav and think "Piper is an app I browse" instead of "Piper is a colleague who helps"~~
- ~~**Technical Debt**: Nav items hardcoded; trust-gated visibility requires refactoring~~

**RESOLVED**: Nav now supports home-state-first paradigm with trust-gated visibility.

---

## Implementation Evidence

### Vocabulary Changes (Phase 1)
| Old Label | New Label | Anti-Flattening Test |
|-----------|-----------|---------------------|
| Standup | Check in | ✅ "Piper can help you check in" |
| My Work | Your stuff | ✅ Conversational, Piper's perspective |
| Todos | To-dos | ✅ Natural language |
| Files | Documents | ✅ Natural language |
| Lists | Collections | ✅ More descriptive |
| Learning | Learning | ✅ Already action-oriented |

### Trust-Gated Visibility (Phase 2)
| Nav Item | Hardness | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|----------|----------|---------|---------|---------|---------|
| Home | HARDEST | ✅ | ✅ | ✅ | ✅ |
| Search trigger | HARDEST | ✅ | ✅ | ✅ | ✅ |
| User Menu | HARDEST | ✅ | ✅ | ✅ | ✅ |
| Check in | HARD | ❌ | ❌ | ✅ | ✅ |
| Your stuff | MEDIUM | ❌ | ❌ | ✅ | ✅ |
| → To-dos | MEDIUM | ❌ | ❌ | ✅ | ✅ |
| → Projects | MEDIUM | ❌ | ❌ | ✅ | ✅ |
| → Documents | SOFT | ❌ | ❌ | ❌ | ✅ |
| → Collections | SOFT | ❌ | ❌ | ❌ | ✅ |
| Learning | HARD | ❌ | ❌ | ✅ | ✅ |

### Visual Hierarchy (Phase 3)
- Background: `#fafafa` (muted, not white)
- Box-shadow: `none` (removed)
- Height: `52px` (reduced from 60px)
- Text color: `#5a6c7d` (muted)

### Command Palette Integration (Phase 4)
- Search trigger button with ⌘K hint
- Keyboard shortcut: Cmd/Ctrl+K
- Custom event: `openCommandPalette`

---

## Acceptance Criteria

### Functionality
- [x] Nav items use natural language (not database table names)
- [x] Trust-gated visibility working (Stage 1-2 minimal, Stage 3-4 full)
- [x] Home link prominent; other items secondary
- [x] Search trigger invokes command palette event
- [x] All nav items pass anti-flattening test
- [x] Nav available on all templates (include unchanged)

### Testing
- [x] Unit tests for nav item content
- [x] Unit tests for trust-gated visibility
- [x] Accessibility tests (keyboard nav, ARIA)
- [x] Full unit test suite passes with no regressions

### Quality
- [x] No regressions introduced
- [x] Visual hierarchy supports home-state-first paradigm
- [x] Anti-flattening test: All items describable as "Piper can help you..."
- [x] Accessibility maintained (WCAG 2.1 AA)

### Documentation
- [x] Vocabulary mapping documented
- [x] Session log documents design decisions

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Phase 0: Investigation | ✅ | `dev/2026/01/25/420-phase0-nav-audit.md` |
| Phase 1: Vocabulary | ✅ | See test output below |
| Phase 2: Trust-Gated | ✅ | See test output below |
| Phase 3: Visual Hierarchy | ✅ | See test output below |
| Phase 4: Palette Integration | ✅ | See test output below |
| Phase Z: Completion | ✅ | This update |
| All unit tests pass | ✅ | 4389 passed |
| No regressions | ✅ | Baseline was 4364 |

---

## Test Results

```bash
$ python -m pytest tests/unit/templates/test_navigation.py -v
============================= test session starts ==============================
tests/unit/templates/test_navigation.py::TestNavigationVocabulary::test_standup_renamed_to_check_in PASSED
tests/unit/templates/test_navigation.py::TestNavigationVocabulary::test_my_work_renamed_to_your_stuff PASSED
tests/unit/templates/test_navigation.py::TestNavigationVocabulary::test_todos_renamed_to_to_dos PASSED
tests/unit/templates/test_navigation.py::TestNavigationVocabulary::test_files_renamed_to_documents PASSED
tests/unit/templates/test_navigation.py::TestNavigationVocabulary::test_lists_renamed_to_collections PASSED
tests/unit/templates/test_navigation.py::TestNavigationVocabulary::test_learning_kept_as_is PASSED
tests/unit/templates/test_navigation.py::TestNavigationTrustGating::test_check_in_requires_stage_3 PASSED
tests/unit/templates/test_navigation.py::TestNavigationTrustGating::test_your_stuff_dropdown_requires_stage_3 PASSED
tests/unit/templates/test_navigation.py::TestNavigationTrustGating::test_documents_requires_stage_4 PASSED
tests/unit/templates/test_navigation.py::TestNavigationTrustGating::test_collections_requires_stage_4 PASSED
tests/unit/templates/test_navigation.py::TestNavigationTrustGating::test_trust_gated_class_exists PASSED
tests/unit/templates/test_navigation.py::TestNavigationTrustGating::test_trust_stage_javascript_exists PASSED
tests/unit/templates/test_navigation.py::TestNavigationSearchTrigger::test_search_trigger_exists PASSED
tests/unit/templates/test_navigation.py::TestNavigationSearchTrigger::test_search_trigger_has_keyboard_hint PASSED
tests/unit/templates/test_navigation.py::TestNavigationSearchTrigger::test_keyboard_shortcut_handler_exists PASSED
tests/unit/templates/test_navigation.py::TestNavigationSearchTrigger::test_custom_event_dispatched PASSED
tests/unit/templates/test_navigation.py::TestNavigationVisualHierarchy::test_nav_has_muted_background PASSED
tests/unit/templates/test_navigation.py::TestNavigationVisualHierarchy::test_nav_has_no_shadow PASSED
tests/unit/templates/test_navigation.py::TestNavigationVisualHierarchy::test_nav_links_have_muted_color PASSED
tests/unit/templates/test_navigation.py::TestNavigationVisualHierarchy::test_nav_has_smaller_height PASSED
tests/unit/templates/test_navigation.py::TestNavigationAccessibility::test_nav_has_aria_label PASSED
tests/unit/templates/test_navigation.py::TestNavigationAccessibility::test_dropdowns_have_aria_haspopup PASSED
tests/unit/templates/test_navigation.py::TestNavigationAccessibility::test_dropdowns_have_aria_expanded PASSED
tests/unit/templates/test_navigation.py::TestNavigationAccessibility::test_hamburger_has_aria_label PASSED
tests/unit/templates/test_navigation.py::TestNavigationAccessibility::test_search_trigger_has_aria_label PASSED
============================== 25 passed in 0.25s ==============================

$ python -m pytest tests/unit/ -q
4389 passed, 24 skipped, 422 warnings in 23.91s
```

---

## Files Modified

- `templates/components/navigation.html` - Vocabulary, trust-gating, visual hierarchy, palette trigger
- `tests/unit/templates/test_navigation.py` - 25 new tests (NEW FILE)

---

## Status: COMPLETE ✅

Implementation complete. All acceptance criteria met. Awaiting PM review.

---

_Issue created: 2026-01-25_
_Last updated: 2026-01-25_
_Implemented by: Lead Developer_
