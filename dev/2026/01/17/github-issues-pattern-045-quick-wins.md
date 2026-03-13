# Pattern-045 Quick Win Issues for Sprint A20

**Created**: January 17, 2026
**Created by**: PPM
**Source**: CXO Workstreams Review (Jan 16 memo)
**Purpose**: Address visible Pattern-045 (Discovery Problem) gaps without MUX architecture

---

## Issue 1: UX-AUTO-TITLE - Auto-Title Conversations

**Priority**: P2
**Labels**: `ux`, `quick-win`, `pattern-045`
**Milestone**: Sprint A20
**Epic**: None (standalone polish)
**Related**: Pattern-045, #565 (Conversation History Sidebar)

---

### Problem Statement

#### Current State
All conversations in the sidebar are titled "New conversation" regardless of content. Users cannot distinguish between conversations without clicking into each one.

#### Impact
- **Blocks**: Effective use of conversation history feature (#565)
- **User Impact**: History navigation nearly useless; must click each conversation to find content
- **Technical Debt**: None (new feature)

#### Strategic Context
Quick win that improves discoverability without MUX architecture. Makes existing #565 sidebar feature actually useful.

---

### Goal

**Primary Objective**: Automatically generate meaningful conversation titles based on first user message.

**Example User Experience**:
```
Before: "New conversation" | "New conversation" | "New conversation"
After: "Calendar for Monday" | "GitHub issue status" | "Project setup"
```

**Not In Scope**:
- ❌ User-editable titles (future enhancement)
- ❌ AI-generated summaries (MUX territory)
- ❌ Conversation categorization

---

### What Already Exists

#### Infrastructure ✅
- Conversation model with `title` field
- ConversationRepository with create/update methods
- First user message available at conversation start

#### What's Missing ❌
- Title generation logic
- Update call after first message

---

### Requirements

#### Acceptance Criteria
- [ ] Conversations receive auto-generated title after first user message
- [ ] Title is first 50 characters of user message (truncated with "...")
- [ ] Sidebar displays generated titles instead of "New conversation"
- [ ] Existing "New conversation" entries remain unchanged (no migration)

#### Implementation Approach
1. In `ConversationRepository.add_turn()` or equivalent, check if conversation title is default
2. If default and this is first user turn, update title to truncated message
3. Strip markdown/special characters from title

---

### Testing Strategy

**Scenario 1**: New conversation title generation
1. [ ] Start new conversation
2. [ ] Send message "What's on my calendar for Monday?"
3. [ ] Verify sidebar shows "What's on my calendar for Monday?" (or truncated)

**Scenario 2**: Long message truncation
1. [ ] Send message longer than 50 characters
2. [ ] Verify title truncates with "..."

---

### Effort Estimate

**Overall Size**: Small (1-2 hours)

---

## Issue 2: UX-SUPPRESS-NULLS - Suppress Null Field Display

**Priority**: P2
**Labels**: `ux`, `quick-win`, `pattern-045`
**Milestone**: Sprint A20
**Epic**: None (standalone polish)
**Related**: Pattern-045

---

### Problem Statement

#### Current State
UI displays null/empty fields with placeholder text like "No start date", "No end date", "No description". This exposes the data model rather than presenting user value.

#### Impact
- **Blocks**: Nothing directly
- **User Impact**: Cluttered UI; confusing messages; feels unpolished
- **Technical Debt**: Minor (template cleanup)

#### Strategic Context
Quick win that improves perceived quality. Addresses "exposing data model" anti-pattern identified in alpha screenshots.

---

### Goal

**Primary Objective**: Hide or gracefully handle null/empty fields instead of displaying "No X" placeholders.

**Example User Experience**:
```
Before:
  Start Date: No start date
  End Date: No end date
  Description: No description

After:
  [Fields simply not shown when empty]
  OR
  [Single line: "No dates set" if both missing]
```

**Not In Scope**:
- ❌ Adding default values
- ❌ Required field validation
- ❌ Data model changes

---

### What Already Exists

#### Infrastructure ✅
- Jinja2 templates with conditional rendering capability
- Existing `{% if field %}` patterns elsewhere

#### What's Missing ❌
- Consistent null-handling in affected templates

---

### Requirements

#### Acceptance Criteria
- [ ] Audit templates for "No X" placeholder patterns
- [ ] Replace with conditional display (hide when null)
- [ ] Verify all major views: projects, todos, lists, files, calendar
- [ ] No visual regression in populated fields

#### Implementation Approach
1. Search templates for "No " patterns
2. Wrap in `{% if field %}` conditionals
3. Test each affected view with null and populated data

---

### Testing Strategy

**Scenario 1**: Empty project view
1. [ ] Create project with minimal fields
2. [ ] Verify no "No X" placeholders visible
3. [ ] Verify populated fields still display

**Scenario 2**: Todo with no dates
1. [ ] Create todo without start/end dates
2. [ ] Verify date section hidden or gracefully handled

---

### Effort Estimate

**Overall Size**: Small (1-2 hours)

---

## Issue 3: UX-REMOVE-REDUNDANT-BADGES - Remove Redundant UI Badges

**Priority**: P3
**Labels**: `ux`, `quick-win`, `pattern-045`
**Milestone**: Sprint A20
**Epic**: None (standalone polish)
**Related**: Pattern-045

---

### Problem Statement

#### Current State
UI displays badges like "Owner" on items where the user can only see their own items anyway. This is redundant information that clutters the interface.

#### Impact
- **Blocks**: Nothing
- **User Impact**: Minor visual clutter; feels over-designed
- **Technical Debt**: None

#### Strategic Context
Quick win that reduces visual noise. Part of "clean empty states" and general UI polish.

---

### Goal

**Primary Objective**: Remove badges/labels that provide no additional information in single-user context.

**Example User Experience**:
```
Before:
  [Owner] My Project
  [Owner] Another Project

After:
  My Project
  Another Project
```

**Not In Scope**:
- ❌ Multi-user/sharing features
- ❌ Permission system changes
- ❌ Adding new badges

---

### What Already Exists

#### Infrastructure ✅
- Single-user context (user only sees own items)
- Badge rendering in templates

#### What's Missing ❌
- Audit of which badges are redundant
- Conditional display logic

---

### Requirements

#### Acceptance Criteria
- [ ] Audit all badge/label displays across templates
- [ ] Remove "Owner" badge from single-user views
- [ ] Preserve badges that convey meaningful info (status, priority, etc.)
- [ ] No functional regression

#### Implementation Approach
1. Search templates for badge patterns
2. Identify which are redundant in single-user context
3. Remove or conditionalize
4. Document which badges to restore when multi-user ships

---

### Testing Strategy

**Scenario 1**: Project list view
1. [ ] View projects list
2. [ ] Verify no "Owner" badges visible
3. [ ] Verify other meaningful badges (if any) still display

---

### Effort Estimate

**Overall Size**: Small (30 min - 1 hour)

---

## Summary

| Issue | Title | Priority | Effort |
|-------|-------|----------|--------|
| UX-AUTO-TITLE | Auto-Title Conversations | P2 | 1-2 hrs |
| UX-SUPPRESS-NULLS | Suppress Null Field Display | P2 | 1-2 hrs |
| UX-REMOVE-REDUNDANT-BADGES | Remove Redundant UI Badges | P3 | 30-60 min |

**Total Effort**: ~3-5 hours
**Impact**: Addresses 3 visible Pattern-045 gaps without MUX architecture

---

*Ready for Lead Developer to create in GitHub and add to A20*
