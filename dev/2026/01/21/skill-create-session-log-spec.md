# Skill Specification: create-session-log

**Date**: January 21, 2026
**Phase**: 5a - Specification
**Status**: Draft

---

## Skill Overview

| Attribute | Value |
|-----------|-------|
| **Name** | create-session-log |
| **Trigger** | Session start, "start a session log", "create session log" |
| **Frequency** | Every session (highest frequency skill) |
| **Scope** | Cross-role (all agents) |
| **Complexity** | LOW (~60 lines) |

---

## Purpose

Create a properly named and structured session log file at the start of a work session, following project conventions for naming, location, and content structure.

**Key insight**: A single consolidated log per role per day is preferable to fragmented logs, even if efforts are separate. Check for existing same-day logs before creating new ones.

---

## Inputs

| Input | Required | Source | Example |
|-------|----------|--------|---------|
| Role | Yes | Briefing or PM assignment | "docs", "lead", "arch", "prog" |
| Tool | Yes | Environment | "code" (Claude Code), "cursor", "opus-direct" |
| Model | Yes | Environment | "opus", "sonnet", "haiku" |
| Date | Yes | System | 2026-01-21 |
| Time | Yes | System | 0750 (24-hour, no colon) |

---

## Outputs

1. **Session log file** at `dev/active/YYYY-MM-DD-HHMM-{role}-{tool}-{model}-log.md`
2. **Standard header** with role, model, date, start time
3. **Session Objectives** section (to be filled)
4. **Work Log** section started with first entry

---

## Dependencies

### Required Knowledge
- Role slug mappings (see below)
- Naming convention: `YYYY-MM-DD-HHMM-{role}-{tool}-{model}-log.md`
- Directory: `dev/active/`

### Role Slug Reference

| Role | Slug | Typical Model |
|------|------|---------------|
| Lead Developer | lead | opus |
| Chief Architect | arch | opus |
| Communications Director | comms | opus/sonnet |
| Documentation Manager | docs | haiku |
| Programmer (subagent) | prog | sonnet/haiku |
| Chief Innovation Officer | cio | opus |
| Chief Experience Officer | cxo | opus |
| Head of Sapient Resources | hosr | opus |
| Product & Project Manager | ppm | opus |
| Executive Summary Agent | exec | opus/sonnet |
| Spec Writer | spec | opus |

---

## Procedure

### Step 1: Check for Existing Same-Day Log

Before creating a new log, check if one already exists for this role today:

```bash
ls dev/active/*{YYYY-MM-DD}*{role}*log.md
```

If found: **Continue that log** instead of creating a new one. Add a new section:
```markdown
### [TIME] - Session Resumed
- [Context of resumption]
```

### Step 2: Determine File Name

Format: `{date}-{time}-{role}-{tool}-{model}-log.md`

Examples:
- `2026-01-21-0750-docs-code-haiku-log.md`
- `2026-01-21-1400-lead-code-opus-log.md`
- `2026-01-21-0900-arch-opus-log.md` (direct Opus, no "code")

### Step 3: Create File with Standard Header

```markdown
# Session Log: {date}-{time}-{role}-{tool}-{model}

**Role**: {Full Role Name}
**Model**: {Tool} ({Model})
**Date**: {Day of Week}, {Month} {Day}, {Year}
**Start Time**: {Time in 12-hour format}

## Session Objectives

1. [Primary objective from PM]
2. [Secondary objectives if any]

## Work Log

### {Time} - Session Start
- Created session log
- [Initial context or task]
```

### Step 4: Fill Initial Content

- Note objectives from PM's instructions
- Record any initial context or handoff information
- Begin work log with first entry

---

## Quality Criteria

1. **File created in correct location** (`dev/active/`)
2. **Naming convention followed exactly**
3. **Header complete** with all metadata
4. **Objectives section populated** (not left blank)
5. **Work log started** with first timestamped entry
6. **Single log per role per day** (unless PM explicitly requests separate)

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Correct Behavior |
|--------------|--------------|------------------|
| Creating fragmented logs | Hard to synthesize for omnibus | One log per role per day |
| Wrong role slug | Breaks discovery and synthesis | Use exact slugs from table |
| Missing time in filename | Ambiguous, breaks sorting | Include HHMM always |
| Blank objectives section | Log lacks purpose context | Fill from PM instructions |
| Forgetting to check existing | Duplicate logs for same day | Always check first |

---

## Examples

### Good: Resuming Existing Log

PM says "Good morning! Continue working on the anti-pattern index."

1. Check: `ls dev/active/*2026-01-21*docs*log.md`
2. Found: `2026-01-21-0750-docs-code-haiku-log.md`
3. **Resume that log** with new section:
   ```markdown
   ### 2:30 PM - Session Resumed
   - PM assigned continuation of anti-pattern index work
   ```

### Good: Creating New Log

PM says "Good morning! You are my docs agent. Create omnibus for yesterday."

1. Check: `ls dev/active/*2026-01-22*docs*log.md`
2. Not found → Create new
3. File: `dev/active/2026-01-22-0800-docs-code-haiku-log.md`

### Bad: Fragmented Logs

Same role, same day, multiple logs:
- `2026-01-21-0750-docs-code-haiku-log.md`
- `2026-01-21-1400-docs-code-haiku-log.md` ❌

Should be one consolidated log with resumed sections.

---

## Success Criteria

After skill execution:
- [ ] Correct file exists in `dev/active/`
- [ ] Filename matches convention exactly
- [ ] Header metadata is complete and accurate
- [ ] Objectives reflect PM's instructions
- [ ] Work log has first timestamped entry
- [ ] If same-day log existed, it was continued (not duplicated)

---

*Specification complete. Ready for SKILL.md draft.*
