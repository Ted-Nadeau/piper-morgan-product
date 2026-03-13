# Session Log Instruction Plumbing - SOLUTION

## The Problem
Session log instructions aren't connected through the documentation chain. We have standards but no clear invocation path.

## The Solution: Add Explicit Links at Each Level

### 1. BRIEFING DOCS → Link to Session Log Standard

Add this to EACH role briefing doc:

```markdown
## Session Management

### Creating Your Session Log
Follow the session log standard for consistent naming and location.
See: **session-log-standard.md** in knowledge for complete instructions.

Format: `YYYY-MM-DD-HHMM-[role]-[product]-log.md`

Your role slug: `[arch|lead|prog]`
Your product slug: `[opus|sonnet|code|cursor]`

Example for this role:
```bash
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-[role]-[product]-log.md
```

### Verification Required
After EVERY write to your log:
```bash
tail -5 [your-log-file]  # Verify write succeeded
```
```

### 2. GAMEPLAN TEMPLATE → Reference for Lead Dev

In gameplan-template.md, add:

```markdown
## Session Requirements for Lead Developer

### Your Session Log
Create per session-log-standard.md:
- Format: `YYYY-MM-DD-HHMM-lead-sonnet-log.md`
- Verify all writes succeed
- Location priority: Artifacts → Filesystem → Sandbox

### Agent Session Logs
Ensure agents create logs per session-log-standard.md:
- Code: `prog-code-log.md`
- Cursor: `prog-cursor-log.md`
```

### 3. AGENT PROMPT TEMPLATE → Explicit Instructions

In agent-prompt-template.md, add:

```markdown
## Session Log Requirements

Create your session log following session-log-standard.md:

```bash
# For Code:
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-prog-code-log.md

# For Cursor:
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-prog-cursor-log.md
```

Verify EVERY write succeeds.
```

---

## Verification Requirements Language

Add this EXACT text where needed:

### For METHODOLOGY.md (after Document Creation Guidelines):

```markdown
## Verification Requirements

### Every Document Write Must Be Verified
```bash
# After ANY write operation:
# 1. Attempt the write
# 2. Verify it succeeded:
tail -10 [filename]  # or
grep "expected content" [filename]
# 3. Report any failure immediately
# 4. Fall back to next location option if failed
```

**This is MANDATORY** - Silent failures have caused lost work.
```

### For Role Docs (in Communication Style or Reporting sections):

```markdown
### Verification Discipline
- Verify EVERY file write succeeds
- Report failures immediately
- No silent failures allowed
- Check: `tail -5 [file]` after writes
```

---

## Template Flexibility Language

### For gameplan-template.md (at the top after version):

```markdown
## Template Adaptation Philosophy
This template provides proven structure, but adapt to your context:
- Skip sections that don't apply
- Combine phases when it makes sense
- Add detail where needed
- Evidence matters more than format

The goal is effective work, not template compliance.
```

### For agent-prompt-template.md (after Purpose):

```markdown
## Using This Template
This template has worked well, but:
- Adapt sections to your specific task
- Skip irrelevant parts
- Focus on evidence over format
- The goal is completion, not compliance

Critical sections (don't skip):
- Infrastructure verification
- Session log creation
- Evidence requirements
- GitHub discipline
```

---

## Complete Threading Map

```
1. Project Instructions (Claude.ai)
   ↓ Points to briefing docs

2. BRIEFING-ROLE-* docs
   ↓ Links to session-log-standard.md
   ↓ Provides role-specific examples

3. Gameplan (from Architect)
   ↓ References session requirements
   ↓ Links to session-log-standard.md

4. Agent Prompt (from Lead Dev)
   ↓ Contains explicit session log commands
   ↓ Includes verification requirements

5. Session Log Standard (central reference)
   ← All docs point here for details
```

---

## The Missing Links to Add

1. **In BRIEFING-PROJECT.md**: Add reference to session-log-standard.md
2. **In each BRIEFING-ROLE doc**: Add Session Management section with link
3. **In gameplan-template.md**: Add Session Requirements section
4. **In agent-prompt-template.md**: Add explicit session log commands
5. **In CLAUDE.md & .cursor/**: Add link to session-log-standard.md

This creates a complete chain where everyone knows where to find the session log instructions!
