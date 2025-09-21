# Template Updates for Methodology Clarity

## Key Changes Summary

### 1. Agent Naming Convention
- **Claude Code** (not "Agent A" or "Code Agent")
- **Cursor Agent** (not "Agent B" or just "Cursor")
- Remove all generic A/B references

### 2. Session Log Fixes
Change from:
```
"Create a session log at..."
```

To:
```
"If you have not already started a session log for this session, create one at docs/development/session-logs/YYYY-MM-DD-HHMM-[agent-name]-log.md. If you already have a session log running, continue using it."
```

### 3. Cross-Validation Timing
Change from:
```
"Cross-validate every 30 minutes"
```

To:
```
"Cross-validate at logical junctures as specified in the gameplan (e.g., after completing major phases, when switching between investigation and implementation, or when encountering unexpected infrastructure)"
```

### 4. Checkbox Update Clarification (KEEP STRICT)
Keep the current requirement but clarify:
```
"CRITICAL: Update checkboxes in the issue DESCRIPTION using `gh issue edit`, never just add comments. Unchecked boxes incorrectly signal incomplete work. Each completed task must have its checkbox marked in the description itself."
```

---

## Updated gameplan-template.md Sections

### Multi-Agent Deployment Strategy Section

Replace the current Agent Division Template with:

```markdown
### Agent Division
**Claude Code** - Investigation & Broad Work
- Discovery tasks using /agent subagents
- Pattern finding across codebase
- Architecture mapping
- GitHub bookending responsibility

**Cursor Agent** - Implementation & Testing
- Specific file modifications
- Test creation and execution
- UI/UX adjustments
- Cross-validation of Claude Code's work

### Coordination Points
- Share findings via GitHub issue at logical junctures
- Cross-validate after major phase completions
- Create handoff document if sequential work needed
```

---

## Updated agent-prompt-template.md Sections

### Opening Section

Replace:
```
# [AGENT NAME] Prompt: [TASK DESCRIPTION]

## Your Identity
You are [Claude Code / Cursor], a specialized development agent...
```

With:
```
# Prompt for Claude Code: [TASK DESCRIPTION]
OR
# Prompt for Cursor Agent: [TASK DESCRIPTION]

## Your Identity
You are Claude Code, a specialized development agent...
OR
You are Cursor Agent, a specialized development agent...
```

### Session Log Section (NEW - Add This)

Add after "Your Identity":
```
## Session Log Management

If you have not already started a session log for this session:
- Create one at: docs/development/session-logs/YYYY-MM-DD-HHMM-[your-name]-log.md
- Format: Use markdown (.md extension, not .txt)
- Update throughout work with evidence and progress

If you already have a session log running:
- Continue using the existing log
- Do NOT create a new one
- Add timestamped entries for new work
```

### Cross-Validation Section

Replace timing requirements with:
```
## Cross-Validation Protocol

Coordinate with [other agent] at these logical junctures:
- After completing investigation phase
- Before major implementation changes
- When infrastructure doesn't match expectations
- At natural phase transitions defined in gameplan
- When ready for final verification

Lead Developer will specify exact coordination points based on the gameplan.
```

---

## Files for Knowledge Folder

Recommended files to copy to `/knowledge/`:
1. **gameplan-template.md** (with updates)
2. **agent-prompt-template.md** (with updates)
3. **GENESIS-DOCUMENTS-PACKAGE.md** (strategic context)
4. **PATTERNS-AND-INSIGHTS.md** (architectural learnings)
5. **methodology-00-EXCELLENCE-FLYWHEEL.md** (core methodology)
6. **cross-validation-protocol.md** (coordination patterns)

Create a `knowledge/README.md`:
```markdown
# Knowledge Folder

This folder contains templates and strategic documents that live in Claude's project knowledge but need filesystem access for Lead Developer and others.

## Templates (Update These When Methodology Evolves)
- gameplan-template.md - Chief Architect's planning template
- agent-prompt-template.md - Lead Developer's agent deployment template

## Strategic Documents (Reference Only)
- GENESIS-DOCUMENTS-PACKAGE.md - Origin story and vision
- PATTERNS-AND-INSIGHTS.md - Architectural patterns discovered
- methodology-00-EXCELLENCE-FLYWHEEL.md - Core methodology

## NOT Included
- Daily session logs (too detailed)
- Temporary work products
- Issue-specific gameplans

This is a bridge between Claude's project knowledge and the filesystem.
```

---

## Nested Code Block Issue

You're right about the triple backtick nesting being problematic. In templates, use:
- Single backticks for inline code: `command`
- Indentation for code blocks instead of triple backticks when inside a template
- Or use a different delimiter like `---` for template boundaries

This avoids the markdown parser confusion that might be causing the .txt file issue.
