# Condensed Update Guide for Briefing Documents
**Created**: September 22, 2025, 22:21
**Purpose**: Quick reference for updating all briefing docs

## 1. Critical Updates to Apply to ALL Briefing Docs

### Add at the top of each doc (after title):
```markdown
## Documentation Navigation
For complete documentation structure, see: **docs/NAVIGATION.md**
```

### Replace ALL session log commands with:
```markdown
## Session Log
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-[role]-[product]-log.md

Roles: exec, arch, lead, prog
Products: opus, sonnet, code, cursor
```

### Add GitHub Checkbox section (if missing):
```markdown
## GitHub Progress Discipline (MANDATORY)
- Agents UPDATE progress descriptions
- PM VALIDATES by checking boxes
- Include "(PM will validate)" in criteria
- Evidence required before PM checks
```

### Add Template Flexibility (to role docs):
```markdown
## Template Adaptation
Templates provide structure but adapt to context:
- Skip irrelevant sections
- Evidence over format compliance
```

## 2. Document-Specific Updates

### CURRENT-STATE.md
- Update status: CORE-GREAT-1 COMPLETE
- Add CORE-QUERY-1 to known issues
- Update percentage (30% → 35%)
- Note "simpler than expected" pattern

### LEAD-DEV.md
- Emphasize 00-START-HERE-LEAD-DEV.md
- Add test scope specification requirement
- Stress PM validates checkboxes

### ARCHITECT.md
- Add document location guidelines
- Emphasize infrastructure verification WITH PM

### PROGRAMMER.md
- Fix any "2005" year bugs
- Add verification requirements

## 3. Files to Update

### In docs/briefing/ (filesystem):
- [ ] PROJECT.md
- [ ] METHODOLOGY.md (use BRIEFING-METHODOLOGY-updated.md)
- [ ] CURRENT-STATE.md
- [ ] roles/ARCHITECT.md
- [ ] roles/LEAD-DEV.md
- [ ] roles/PROGRAMMER.md

### In knowledge (with BRIEFING- prefix):
- [ ] BRIEFING-PROJECT.md
- [ ] BRIEFING-METHODOLOGY.md
- [ ] BRIEFING-CURRENT-STATE.md
- [ ] BRIEFING-ROLE-ARCHITECT.md
- [ ] BRIEFING-ROLE-LEAD-DEV.md
- [ ] BRIEFING-ROLE-PROGRAMMER.md

### Other locations:
- [ ] /CLAUDE.md (root)
- [ ] /.cursor/rules/programmer-briefing.mdc
- [ ] /.cursor/rules/verification-first.mdc

## 4. Quick Verification Checklist

After updates, verify:
- [ ] No "2005" anywhere
- [ ] Session logs: YYYY-MM-DD-HHMM-[role]-[product]-log.md
- [ ] NAVIGATION.md referenced
- [ ] "(PM will validate)" in acceptance criteria
- [ ] Document locations clear (Artifacts → Filesystem → Sandbox)

---

*Use BRIEFING-METHODOLOGY-updated.md as the template for consistency*
