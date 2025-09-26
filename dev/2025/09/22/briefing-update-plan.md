# Briefing Documentation Update Plan
**Date**: September 22, 2025, 21:45 PT  
**Objective**: Update all briefing docs with methodology improvements from GREAT-1 experience

## 1. Complete Inventory of Necessary Updates

### Session Log Updates (ALL DOCS)
- [ ] Replace ANY session log commands with v2 format
- [ ] Add verification requirement after writes
- [ ] Use role-product nomenclature (arch-opus, lead-sonnet, etc.)
- [ ] Fix any "2005" hardcoded years (use `$(date +%Y)`)

### Navigation Addition (ALL DOCS)
- [ ] Add reference to docs/NAVIGATION.md near top
- [ ] Format: "For documentation structure, see docs/NAVIGATION.md"

### GitHub Discipline (RELEVANT DOCS)
- [ ] Add PM validation principle for checkboxes
- [ ] Clarify agents update, PM validates
- [ ] Add "(PM will validate)" notation

### Test Scope Specification
- [ ] Add to gameplan-template-v8.md
- [ ] Add to ARCHITECT.md guidance
- [ ] Include in agent-prompt-template.md

### Template Flexibility
- [ ] Add adaptation clause to all templates
- [ ] Emphasize evidence over format compliance

## 2. Documents Requiring Updates

### Core Briefing Docs (6 files)
1. **PROJECT.md** - Minor (navigation only)
2. **METHODOLOGY.md** - Major (multiple additions)
3. **CURRENT-STATE.md** - Minor (update with GREAT-1 complete)
4. **ARCHITECT.md** - Moderate (session logs, GitHub discipline)
5. **LEAD-DEV.md** - Moderate (session logs, GitHub discipline)
6. **PROGRAMMER.md** - Moderate (session logs, verification)

### Templates (3 files)
7. **gameplan-template-v8.md** - Moderate (test scope, flexibility)
8. **agent-prompt-template.md** - Major (flexibility, GitHub discipline)
9. **session-log-standard-v2.md** - NEW (created tonight)

### Instructions (3 files)
10. **CLAUDE.md** - Major (session logs, navigation)
11. **MINIMAL-PROJECT-INSTRUCTIONS.md** - Minor (navigation reference)
12. **.cursor/rules/*.mdc** - Moderate (session logs, navigation)

## 3. Implementation Instructions

### For METHODOLOGY.md - Add These Sections

```markdown
## Documentation Navigation
For complete documentation structure, see docs/NAVIGATION.md

## Session Logs
Follow session-log-standard-v2.md for nomenclature and reliability.
Format: YYYY-MM-DD-HHMM-[role]-[product]-log.md
Verify EVERY write succeeds.

## GitHub Progress Discipline (MANDATORY)

### Checkbox Protocol
- **Agents**: Update progress descriptions with evidence
- **PM**: Validates completion by checking boxes
- **Format**: Include "(PM will validate)" in criteria
- **Evidence**: Required before PM checks any box

Example:
- [ ] QueryRouter initialized (PM will validate)
  - Evidence: [terminal output link]
```

### For ARCHITECT.md - Replace Session Log Section

```markdown
## Session Management

Start your session log using v2 nomenclature:
```bash
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-arch-opus-log.md
# Verify it worked:
tail -1 dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-arch-opus-log.md
```

For documentation structure, see docs/NAVIGATION.md
```

### For LEAD-DEV.md - Replace Session Log Section

```markdown
## Session Management

Start your session log using v2 nomenclature:
```bash
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-lead-sonnet-log.md
# Verify it worked:
tail -1 dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-lead-sonnet-log.md
```

First, check docs/NAVIGATION.md for documentation structure.
Always read 00-START-HERE-LEAD-DEV.md first.
```

### For PROGRAMMER.md - Replace Session Log Section

```markdown
## Session Discipline

Create session log with proper nomenclature:
```bash
# For Code:
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-prog-code-log.md

# For Cursor:
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-prog-cursor-log.md

# ALWAYS verify:
tail -1 [your-log-file]
```
```

### For CLAUDE.md - Major Updates

```markdown
## 🚨 MANDATORY FIRST READ

1. Check docs/NAVIGATION.md for documentation structure
2. These docs will be in: /Users/xian/Development/piper-morgan/docs/briefing/
3. In knowledge, search for:
   - BRIEFING-CURRENT-STATE
   - BRIEFING-ROLE-PROGRAMMER
   - BRIEFING-METHODOLOGY
   - BRIEFING-PROJECT

## SESSION DISCIPLINE
```bash
# Create session log with v2 nomenclature:
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-prog-code-log.md

# ALWAYS verify the write succeeded:
tail -1 dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-prog-code-log.md
```
```

### For gameplan-template-v8.md - Add Test Scope

```markdown
## Acceptance Criteria with Test Scope

### Feature Requirements
- [ ] Core functionality implemented (PM will validate)
- [ ] Integration points connected (PM will validate)
- [ ] Performance targets met (PM will validate)

### Test Requirements (SPECIFY SCOPE)
- [ ] Unit tests: [specify components to test]
- [ ] Integration tests: [specify flows to verify]
- [ ] Performance tests: [specify metrics < Xms]
- [ ] Regression tests: [specify what to prevent]

## Template Adaptation

This template provides structure but adapt to context:
- Skip irrelevant phases
- Combine if appropriate
- Add detail where helpful
- Evidence matters more than format
```

### For agent-prompt-template.md - Add Flexibility

```markdown
## Template Usage Note

This template is a guide, not a strict script:
- Adapt sections to your specific task
- Skip irrelevant parts
- Add detail where needed
- Focus on evidence and outcomes over format compliance

## GitHub Discipline (CRITICAL)

Agents update progress, PM validates:
- Use issue description (not comments)
- Provide evidence links
- PM checks boxes after validation
- Include "(PM will validate)" notation
```

## 4. File Placement Plan

### Filesystem Locations
```
/Users/xian/Development/piper-morgan/
├── docs/
│   └── briefing/
│       ├── PROJECT.md (updated)
│       ├── METHODOLOGY.md (updated)
│       ├── CURRENT-STATE.md (updated)
│       └── roles/
│           ├── ARCHITECT.md (updated)
│           ├── LEAD-DEV.md (updated)
│           └── PROGRAMMER.md (updated)
├── knowledge/
│   ├── gameplan-template.md (v8 updated)
│   ├── agent-prompt-template.md (updated)
│   └── session-log-standard-v2.md (NEW)
├── CLAUDE.md (updated)
└── .cursor/
    └── rules/
        ├── verification-first.mdc (updated)
        └── programmer-briefing.mdc (updated)
```

### Knowledge Additions (with BRIEFING- prefix)
- BRIEFING-PROJECT.md
- BRIEFING-METHODOLOGY.md
- BRIEFING-CURRENT-STATE.md
- BRIEFING-ROLE-ARCHITECT.md
- BRIEFING-ROLE-LEAD-DEV.md
- BRIEFING-ROLE-PROGRAMMER.md

## 5. Execution Checklist

### Tonight (Before Sleep)
1. [ ] Update all 6 core briefing docs
2. [ ] Update CLAUDE.md
3. [ ] Update templates
4. [ ] Place in filesystem
5. [ ] Add to knowledge with BRIEFING- prefix

### Verification
1. [ ] Search all files for "2005" - should find NONE
2. [ ] Verify all session log commands use $(date +%Y)
3. [ ] Confirm NAVIGATION.md referenced
4. [ ] Check GitHub discipline sections added
5. [ ] Verify template flexibility clauses included

---

*This plan ensures consistent, reliable briefing for all future sessions*