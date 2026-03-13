# Phase 0: Navigation Item Audit

**Issue**: #420 MUX-NAV-UTILITY
**Date**: 2026-01-25

---

## Current Nav Items Inventory

| Current Label | Location | Anti-Flattening Test | Verdict |
|--------------|----------|---------------------|---------|
| Piper Morgan (brand) | nav-brand | ✅ Brand, appropriate | KEEP |
| Standup | nav-link | ⚠️ "Standup" is action-oriented but jargony | REVISE |
| **My Work** (dropdown) | nav-dropdown | ❌ Database-style, "filing cabinet" | REVISE |
| → Todos | dropdown-item | ❌ Database table name | REVISE |
| → Projects | dropdown-item | ⚠️ Generic but acceptable | REVISE |
| → Files | dropdown-item | ❌ Database table name | REVISE |
| → Lists | dropdown-item | ❌ Database table name | REVISE |
| Learning | nav-link | ✅ Action-oriented | KEEP |
| User Menu | nav-user | ✅ Standard pattern | KEEP |
| → Settings | dropdown-item | ✅ Standard | KEEP |
| → Account | dropdown-item | ✅ Standard | KEEP |
| → Logout | dropdown-item | ✅ Standard | KEEP |

---

## Anti-Flattening Test

**Test**: Can each item be described as "Piper can help you..."?

| Item | Test Phrase | Pass? |
|------|-------------|-------|
| Standup | "Piper can help you with your standup" | ⚠️ |
| My Work | "Piper can help you with my work" | ❌ Nonsense |
| Todos | "Piper can help you with todos" | ❌ |
| Projects | "Piper can help you with projects" | ⚠️ |
| Files | "Piper can help you with files" | ❌ |
| Lists | "Piper can help you with lists" | ❌ |
| Learning | "Piper can help you with learning" | ✅ |

---

## Vocabulary Mapping (Current → Proposed)

Based on consciousness grammar and naming-conventions-v1:

| Current | Proposed | Rationale |
|---------|----------|-----------|
| Standup | Check in | More natural, less jargon |
| My Work | Your stuff | Natural language, Piper's perspective |
| Todos | Things to do | Natural phrasing |
| Projects | What you're working on | Descriptive, conversational |
| Files | Your documents | Natural language |
| Lists | Your collections | More descriptive |
| Learning | Keep as-is | Already action-oriented |

**Alternative vocabulary** (more concise):

| Current | Alt Proposed | Rationale |
|---------|--------------|-----------|
| My Work | Your work | Simpler, still natural |
| Todos | To-dos | Slightly better |
| Projects | Projects | Could keep if others change |
| Files | Documents | Standard term |
| Lists | Lists | Could keep |

---

## Trust-Visibility Matrix

Based on HardnessLevel from #419:

| Nav Item | Hardness | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|----------|----------|---------|---------|---------|---------|
| Home (brand click) | HARDEST | ✅ | ✅ | ✅ | ✅ |
| Check in (Standup) | HARD | ❌ | ❌ | ✅ | ✅ |
| Your stuff dropdown | MEDIUM | ❌ | ❌ | ✅ | ✅ |
| → Things to do | MEDIUM | ❌ | ❌ | ✅ | ✅ |
| → Projects | MEDIUM | ❌ | ❌ | ✅ | ✅ |
| → Documents | SOFT | ❌ | ❌ | ❌ | ✅ |
| → Collections | SOFT | ❌ | ❌ | ❌ | ✅ |
| Learning | HARD | ❌ | ❌ | ✅ | ✅ |
| User Menu | HARDEST | ✅ | ✅ | ✅ | ✅ |
| Search trigger | HARDEST | ✅ | ✅ | ✅ | ✅ |

**Stage 1-2 minimal nav**: Home, Search, User Menu only
**Stage 3**: + Check in, Your stuff (To-dos, Projects), Learning
**Stage 4**: + Documents, Collections

---

## Design Decision: Vocabulary Choice

**Recommendation**: Use natural but concise labels

| Current | Final Proposed |
|---------|----------------|
| Standup | Check in |
| My Work | Your stuff |
| Todos | To-dos |
| Projects | Projects |
| Files | Documents |
| Lists | Collections |
| Learning | Learning |

**Rationale**:
- "Check in" is warmer than "Standup" (corporate jargon)
- "Your stuff" is conversational and Piper-perspective
- "To-dos" is natural language (hyphenated)
- "Projects" is universal enough to keep
- "Documents" is clearer than "Files"
- "Collections" is more descriptive than "Lists"

---

## Missing Element: Search Trigger

Current nav has NO search trigger for command palette (#421).

**Add**: Search icon with Cmd/Ctrl+K hint between brand and nav items.

---

## Phase 0 Deliverables

✅ Nav item audit table (above)
✅ Trust-visibility matrix (above)
✅ Vocabulary mapping (above)
✅ Blockers identified: None - #419 trust_stage available

---

## Next: Phase 1

Implement vocabulary changes in `templates/components/navigation.html`.
