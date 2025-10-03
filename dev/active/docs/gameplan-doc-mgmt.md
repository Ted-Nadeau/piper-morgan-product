# Gameplan: Documentation Management Tasks - October 3, 2025

**For**: Claude Code Doc-Mgmt Agent
**Context**: Post GREAT-3A completion, preparing briefing optimization and documentation updates

## Mission

Create optimized briefing documents for all roles, update navigation/index files, and prepare documentation infrastructure for reduced token usage while maintaining our methodology.

## Background Context

### What Was Completed Yesterday (GREAT-3A)
- Plugin architecture foundation created
- Config services standardized across all integrations
- web/app.py refactored from 1,052 to 467 lines
- 4 operational plugins (Slack, GitHub, Notion, Calendar)

### Current Problem
Lead Developer reported 21% token usage just for briefing (39K tokens). We need role-specific "essential" briefings that are 2.5K tokens each, with progressive loading for details.

## Phase 0: Investigation

**Check current briefing structure**:
```bash
# See what briefing docs exist
ls -la knowledge/BRIEFING-*.md
wc -w knowledge/BRIEFING-*.md

# Check project instructions
head -50 .claude/claude.md

# Check agent instructions
head -50 .cursorules
```

## Phase 1: Create Essential Briefings

### 1.1 Create Template Briefing

First, the PM will create `BRIEFING-ESSENTIAL-LEAD-DEV.md` as a template. Once that exists, use it as the pattern for others.

**If template doesn't exist yet**, create it with this structure:

```markdown
# BRIEFING-ESSENTIAL-[ROLE]
<!-- Target: 2.5K tokens max -->

## Current State
- Position: 1.1.3.2 (GREAT-3B active)
- Completed: GREAT-1, GREAT-2, GREAT-3A
- Active: GREAT-3B Plugin Infrastructure

## Your Role
[Role-specific 2-3 sentences]

## Key Patterns
- Router Architecture (complete)
- Spatial Intelligence (3 patterns)
- Config Services (standardized)
- Plugin System (operational)

## Current Focus
[Current epic goals]

## Progressive Loading
Say "Loading [topic] details" for:
- Full methodology → BRIEFING-METHODOLOGY
- Templates → gameplan-template, agent-prompt-template
- Architecture → ADR-038, ADR-034

## References
- Current state: BRIEFING-CURRENT-STATE
- Full role guide: BRIEFING-ROLE-[ROLE]
- Issues: GitHub #197-200
```

### 1.2 Create Other Role Briefings

Based on template, create:
- `BRIEFING-ESSENTIAL-ARCHITECT.md`
- `BRIEFING-ESSENTIAL-CHIEF-STAFF.md`
- `BRIEFING-ESSENTIAL-COMMS.md`
- `BRIEFING-ESSENTIAL-AGENT.md` (for coding agents, even shorter ~2K tokens)

**Customize each for the role's specific needs**:
- Architect: Focus on patterns, ADRs, system design
- Chief of Staff: Focus on progress, blockers, team coordination
- Comms: Focus on achievements, narrative, weekly ship
- Agent: Focus on current task, patterns, evidence requirements

## Phase 2: Update Project Instructions

### 2.1 Update .claude/claude.md

Add at the TOP of project instructions:
```markdown
## Role-Based Briefing (Start Here)

1. Identify your role for this conversation
2. Read the appropriate essential briefing:
   - Lead Developer → BRIEFING-ESSENTIAL-LEAD-DEV
   - Chief Architect → BRIEFING-ESSENTIAL-ARCHITECT
   - Chief of Staff → BRIEFING-ESSENTIAL-CHIEF-STAFF
   - Communications → BRIEFING-ESSENTIAL-COMMS

3. Load additional context only as needed using progressive loading

This reduces token usage by 60% while maintaining full capability.
```

### 2.2 Update .cursorules

Add similar instructions for agents:
```markdown
## Agent Briefing

Read BRIEFING-ESSENTIAL-AGENT.md first (2K tokens).
Load templates and patterns only when needed for specific tasks.
```

## Phase 3: Update Navigation Files

### 3.1 Update docs/NAVIGATION.md

Add new section:
```markdown
## 🚀 Quick Start by Role

### Essential Briefings (Start Here)
- [Lead Developer](../BRIEFING-ESSENTIAL-LEAD-DEV.md) - 2.5K tokens
- [Chief Architect](../BRIEFING-ESSENTIAL-ARCHITECT.md) - 2.5K tokens
- [Chief of Staff](../BRIEFING-ESSENTIAL-CHIEF-STAFF.md) - 2.5K tokens
- [Communications](../BRIEFING-ESSENTIAL-COMMS.md) - 2.5K tokens
- [Coding Agent](../BRIEFING-ESSENTIAL-AGENT.md) - 2K tokens

### Progressive Loading
Each essential briefing includes triggers for loading detailed documentation as needed.
```

### 3.2 Update docs/INDEX.md

Add table showing document hierarchy:
```markdown
## Document Hierarchy

| Level | Purpose | Token Size | When to Load |
|-------|---------|------------|--------------|
| Essential | Role-specific start | 2-2.5K | Always first |
| Current State | Live status | 3K | As needed |
| Full Briefing | Complete context | 10-15K | For deep work |
| Templates | Work artifacts | Variable | Task-specific |
```

## Phase 4: Update GitHub Action

### 4.1 Modify .github/workflows/weekly-doc-sweep.yml

Add step to update essential briefings:
```yaml
- name: Update Essential Briefings
  run: |
    # Extract current position from roadmap
    POSITION=$(grep "Current Position" docs/roadmap.md | cut -d: -f2)

    # Update all essential briefings
    for file in BRIEFING-ESSENTIAL-*.md; do
      sed -i "s/Position: .*/Position: $POSITION/" "$file"
    done

    # Commit if changed
    if [[ `git status --porcelain` ]]; then
      git add BRIEFING-ESSENTIAL-*.md
      git commit -m "chore: Update essential briefings position"
    fi
```

## Phase 5: Update docs/README.md

### 5.1 Check current state
```bash
cat docs/README.md
```

### 5.2 Update these sections

**Roadmap Status**:
- GREAT-1 ✅ Complete
- GREAT-2 ✅ Complete (all 6 sub-epics)
- GREAT-3 🚧 In Progress (3A complete, 3B active)
- Estimated 25% of Great Refactor complete

**Architecture Updates**:
- Router architecture operational
- Three spatial patterns documented
- Plugin system foundation complete
- Config validation infrastructure active

**Current Capabilities** (~80% functional):
- ✅ All integrations working via routers
- ✅ Plugin architecture operational
- ✅ Config validation active
- ✅ Spatial intelligence patterns
- 🚧 Dynamic plugin loading (3B)
- ❌ Learning system
- ❌ Complex workflows

## Phase 6: Validation

```bash
# Check all files created
ls -la BRIEFING-ESSENTIAL-*.md

# Verify token counts
for file in BRIEFING-ESSENTIAL-*.md; do
  echo "$file: $(wc -w < "$file") words"
done

# Verify links work
grep -h "](.*)" BRIEFING-ESSENTIAL-*.md | sort -u

# Check GitHub Action syntax
yamllint .github/workflows/weekly-doc-sweep.yml
```

## Success Criteria

- [ ] 5 essential briefing files created (under 2.5K tokens each)
- [ ] Project instructions updated in .claude/claude.md
- [ ] Agent instructions updated in .cursorules
- [ ] NAVIGATION.md includes quick start section
- [ ] INDEX.md shows document hierarchy
- [ ] GitHub Action updates essential briefings
- [ ] README.md reflects current reality

## Time Estimate
~2 hours total

---

*Execute systematically, validate each phase before proceeding*
