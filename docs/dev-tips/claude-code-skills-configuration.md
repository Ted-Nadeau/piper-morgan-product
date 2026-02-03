# Claude Code Skills Configuration

**Created**: February 1, 2026
**Updated**: February 1, 2026
**Purpose**: Enable proper skill discovery and invocation via the Skill tool

---

## The #1 Issue: Launch Location

**Claude Code discovers skills relative to where you launch it.**

Skills in `.claude/skills/` are **project-level** - they only appear when you launch Claude from that project directory.

**Symptom**:
```
/skills
Skills
No skills found
```

**Fix**: Launch Claude Code from the project root:
```bash
cd /Users/xian/Development/piper-morgan
claude
```

Or use the `piper` alias (already configured in ~/.zshrc):
```bash
piper  # Does cd + starts server
```

---

## Skill Locations

| Location | Path | Scope |
|----------|------|-------|
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project only |

Our skills are project-level, so they require launching from the project directory.

---

## Context Budget (Secondary Issue)

If you have many comprehensive skills, they may exceed the default 15,000 character budget. Check with `/context` for warnings about excluded skills.

**Fix** (already in ~/.zshrc):
```bash
export SLASH_COMMAND_TOOL_CHAR_BUDGET=50000
```

---

## Verification

From the project directory:
```bash
claude
/skills  # Should show 5 skills
```

Or invoke directly:
```
/audit-cascade
/check-mailbox
```

---

## See Also

- `.claude/skills/SKILLS.md` - Skill index and usage guide
- [Official docs](https://code.claude.com/docs/en/skills) - Claude Code skills documentation
