# Methodology Improvements from CORE-GREAT-1 Session
**Date**: September 22, 2025  
**Sources**: PM observations, Lead Dev session analysis, Chief Architect review

## Critical Fixes Required

### 1. Session Log Standard (See session-log-standard-v2.md)
- Format: `YYYY-MM-DD-HHMM-[role]-[product]-log.md`
- Verification required after every write
- Location priority: Artifacts → Filesystem → Sandbox

### 2. Navigation Awareness
**Issue**: Assistants unaware of docs/NAVIGATION.md
**Fix**: Add to all briefing docs:
```markdown
## Documentation Navigation
See docs/NAVIGATION.md for complete documentation structure
```

### 3. GitHub Checkbox Discipline
**Issue**: Not emphasized as mandatory, agents self-marking
**Fix**: 
```markdown
## GitHub Progress Discipline (MANDATORY)

### PM Validates Checkboxes
- Agents UPDATE progress descriptions
- PM VALIDATES by checking boxes
- Include "(PM will validate)" in criteria
- Evidence required before PM checks

### Format
- [ ] Task description (PM will validate)
- [ ] Task with evidence: [link] (PM will validate)
```

### 4. Test Scope Specification
**Lead Dev Innovation**: Always specify test types
```markdown
## Test Requirements (Specify Scope)
- [ ] Unit tests: [what components]
- [ ] Integration tests: [what flows]  
- [ ] Performance tests: [what metrics]
- [ ] Regression tests: [what prevention]
```

### 5. Template Flexibility
**Issue**: Templates too prescriptive
**Fix**: Add adaptation clause:
```markdown
## Template Adaptation
This template provides structure but adapt to context:
- Skip irrelevant sections
- Combine phases if appropriate
- Add detail where needed
- Evidence over format compliance
```

## Process Improvements from Lead Dev

### Streamlined Prompts
- Test scope specificity built in
- PM validation notation
- Focused scope boundaries per agent
- Evidence requirements prominent

### Phase Boundaries
- Clear completion criteria before moving on
- No scope creep mid-phase
- Escalation for discoveries outside scope

### Evidence-First Culture
- No claims without proof
- Cross-validation between agents
- PM verification of evidence

## Documentation Updates Needed

### In All Briefing Docs
- Add NAVIGATION.md reference
- Fix any "2005" hardcoded years
- Add session log standard v2

### In METHODOLOGY.md
- Add GitHub checkbox discipline
- Add document location guidelines
- Add verification requirements
- Add template flexibility principle

### In gameplan-template-v8.md
- Add test scope specification
- Add PM validation notation
- Add template adaptation clause
- Emphasize GitHub discipline section

### In agent-prompt-template.md
- Reduce prescriptive language
- Add flexibility statement
- Include verification requirements
- Reference session log standard v2

## Key Lessons from Today

### What Worked
1. **Multi-agent resilience** - Survived Claude.ai outage
2. **Scope discipline** - QUERY issues properly separated
3. **Evidence culture** - Everything proven
4. **Phase Z** - Clear completion protocol

### What Needs Improvement
1. **Resource location clarity** - 20% of session on bad paths
2. **Checkbox discipline** - PM validates, not agents
3. **Session log reliability** - Must verify writes
4. **Template flexibility** - Guide not gospel

## Action Items

### Immediate (Tonight)
1. [ ] Update session log commands in all docs
2. [ ] Add NAVIGATION.md references
3. [ ] Fix any hardcoded "2005" years
4. [ ] Add GitHub checkbox discipline sections

### Tomorrow
1. [ ] Update templates with flexibility clauses
2. [ ] Add test scope specifications
3. [ ] Create verification checklist
4. [ ] Update METHODOLOGY.md comprehensively

### This Week
1. [ ] Audit all docs for consistency
2. [ ] Create prompt template modules
3. [ ] Document "simpler than expected" pattern
4. [ ] Standardize evidence formats

## The "Simpler Than Expected" Pattern

Today's discovery: QueryRouter's issue was session management, not complex dependencies.

**Pattern**: We often assume complexity where simplicity exists
**Mitigation**: Start with simple checks before complex investigation
**Document**: Add to troubleshooting guides

---

*These improvements strengthen the methodology based on real-world execution*