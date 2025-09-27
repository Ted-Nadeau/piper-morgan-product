# Briefing Documentation Update Inventory
**Date**: September 22, 2025, 22:15
**Purpose**: Complete inventory of updates needed after CORE-GREAT-1 lessons

## Documents to Update

### 1. BRIEFING-PROJECT.md
- [ ] Add NAVIGATION.md reference
- [ ] Update session log format to v2
- [ ] Verify no hardcoded years

### 2. BRIEFING-METHODOLOGY.md
- [ ] Add GitHub checkbox discipline (PM validates)
- [ ] Add session log standard v2
- [ ] Add document location guidelines
- [ ] Add template flexibility principle
- [ ] Add verification requirements
- [ ] Add NAVIGATION.md reference

### 3. BRIEFING-CURRENT-STATE.md
- [ ] Update with GREAT-1 completion
- [ ] Add CORE-QUERY-1 issue
- [ ] Update percentage complete (30% → 35%?)
- [ ] Add "simpler than expected" pattern note

### 4. BRIEFING-ROLE-ARCHITECT.md
- [ ] Update session log command with v2 format
- [ ] Add NAVIGATION.md reference
- [ ] Add document location guidelines
- [ ] Emphasize GitHub checkbox discipline

### 5. BRIEFING-ROLE-LEAD-DEV.md
- [ ] Update session log command with v2 format
- [ ] Add NAVIGATION.md reference
- [ ] Emphasize PM validates checkboxes
- [ ] Add test scope specification
- [ ] Reference 00-START-HERE-LEAD-DEV.md more prominently

### 6. BRIEFING-ROLE-PROGRAMMER.md
- [ ] Update session log command with v2 format
- [ ] Add NAVIGATION.md reference
- [ ] Add verification requirements
- [ ] Fix any year hardcoding

### 7. CLAUDE.md (filesystem)
- [ ] Update session log command with v2 format
- [ ] Add NAVIGATION.md reference
- [ ] Fix any "2005" typos
- [ ] Add document location guidelines

### 8. .cursor/rules/*.mdc
- [ ] Update programmer-briefing.mdc with v2 log format
- [ ] Update verification-first.mdc with new standards
- [ ] Add NAVIGATION.md references

### 9. gameplan-template.md (now v8)
- [ ] Add GitHub checkbox discipline section
- [ ] Add test scope specification
- [ ] Add template flexibility clause
- [ ] Emphasize PM validation

### 10. agent-prompt-template.md
- [ ] Reduce prescriptive language
- [ ] Add flexibility statement
- [ ] Update session log format
- [ ] Add verification requirements

## Key Changes to Propagate

### Session Log Format v2
```
YYYY-MM-DD-HHMM-[role]-[product]-log.md

Roles: exec, arch, lead, prog
Products: opus, sonnet, code, cursor
```

### GitHub Checkbox Discipline
```markdown
## GitHub Progress Discipline (MANDATORY)
- Agents UPDATE progress descriptions
- PM VALIDATES by checking boxes
- Include "(PM will validate)" in criteria
```

### NAVIGATION.md Reference
```markdown
## Documentation Structure
For complete documentation navigation, see: docs/NAVIGATION.md
This file maps all documentation locations and purposes.
```

### Document Location Priority
```markdown
## Document Creation Guidelines
1. Artifacts (when reliable) - attached to project
2. Filesystem (when available) - /Users/xian/Development/piper-morgan/dev/
3. Sandbox (fallback) - verify all writes
```

### Template Flexibility
```markdown
## Template Adaptation
Templates provide structure but adapt to context:
- Skip irrelevant sections
- Evidence over format compliance
```

## Update Strategy

### Phase 1: Core Briefing Docs (Tonight)
1. Create updated versions of all 6 briefing docs
2. Place in filesystem at docs/briefing/
3. Upload to knowledge with BRIEFING- prefix

### Phase 2: Agent Instructions (Tonight)
1. Update CLAUDE.md
2. Update .cursor/rules files

### Phase 3: Templates (Tonight/Tomorrow)
1. Update gameplan-template to v9
2. Update agent-prompt-template

## Placement Locations

### Filesystem
```
/Users/xian/Development/piper-morgan/docs/briefing/
├── PROJECT.md
├── METHODOLOGY.md
├── CURRENT-STATE.md
└── roles/
    ├── ARCHITECT.md
    ├── LEAD-DEV.md
    └── PROGRAMMER.md
```

### Knowledge (with prefix)
- BRIEFING-PROJECT.md
- BRIEFING-METHODOLOGY.md
- BRIEFING-CURRENT-STATE.md
- BRIEFING-ROLE-ARCHITECT.md
- BRIEFING-ROLE-LEAD-DEV.md
- BRIEFING-ROLE-PROGRAMMER.md

## Success Criteria
- [ ] All docs have consistent session log format
- [ ] GitHub checkbox discipline is clear
- [ ] NAVIGATION.md is referenced everywhere
- [ ] Document locations are clear
- [ ] Templates have flexibility clauses
- [ ] No hardcoded years remain
- [ ] Verification requirements are explicit

---

*Ready to create updated versions of all documents*
