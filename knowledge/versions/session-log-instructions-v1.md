# Session Log Instructions

## Purpose
Session logs maintain context, institutional memory, and enable effective handoffs between development sessions. They are critical for the Excellence Flywheel methodology.

## When to Create a Session Log
- Every development session (Chief Architect, Lead Developer, Agents)
- At the START of each session (not at the end)
- One log per session (do not create multiple unless asked to and even then verify the reason for starting a new one)

## File Naming Convention
```
docs/development/session-logs/YYYY-MM-DD-HHMM-[role]-log.md
```

Examples:
- `2025-09-16-1430-chief-of-staff-opus-log.md`
-  `2025-09-16-1430-chief-architect-opus-log.md`
- `2025-09-16-1430-lead-developer-sonnet-log.md`
- `2025-09-16-1430-comms-director-sonnet-log.md`
- `2025-09-16-1430-claude-code-log.md`
- `2025-09-16-1430-cursor-agent-log.md`

**CRITICAL**: Use `.md` extension, never `.txt` (`txt/markdown` format, not `txt/txt`)

## Which Template to Use

### Standard Sessions
Use `session-log-template.md` for:
- Agent sessions (Claude Code, Cursor)
- General development work
- Other roles not specified below

### Chief Architect Sessions
Use `session-log-template-chief-architect.md` for:
- Chief Architect strategic sessions
- Sessions requiring PM assessment
- Architecture and planning work

### Lead Developer Sessions
Use `session-log-template-lead-developer.md` for:
- Lead Developer coordinating agents
- Multi-agent deployment tracking
- Cross-validation management

## Session Satisfaction Metrics

At the end of EVERY session, complete the satisfaction check:

- **Value**: What got shipped? (feature/bug/process/learning)
- **Process**: Did methodology work smoothly? (Y/N + specifics)
- **Feel**: How was the cognitive load? (Energizing/OK/Draining)
- **Learned**: Any key discoveries?
- **Tomorrow**: Are next steps clear? (Y/N)
- **Overall**: Choose emoji (😊 / 🙂 / 😐 / 😕 / 😞)

## GitHub Integration

When closing an issue at session end:
```bash
gh issue close [ISSUE#] --comment "Session complete [emoji]
- Shipped: [what]
- Process: [smooth/friction points]
- Next: [what's next]"
```

## Handoff Protocol

### What to Include for Next Session
- Context from current work
- Progress made
- Blockers encountered
- Next steps
- Key decisions made
- Artifacts created

### Archive System
- All logs stored chronologically in `docs/development/session-logs/`
- Archive older logs periodically to `archive/` subdirectory
- Cross-reference related sessions

## Common Pitfalls to Avoid
- Creating logs in .txt format (must be .md)
- Forgetting satisfaction assessment
- Not updating GitHub issues
- Missing handoff information
- Creating multiple logs per session
- Not creating log at session start

## Templates Location
Templates are in `knowledge/` directory:
- `session-log-template.md` - Standard sessions
- `session-log-template-chief-architect.md` - Chief Architect sessions
- `session-log-template-lead-developer.md` - Lead Developer sessions

## Related Documentation
- `methodology-00-EXCELLENCE-FLYWHEEL.md` - Core methodology
- `github-guide.md` - GitHub workflow requirements
- `gameplan-template-v7.md` - For creating gameplans
- `agent-prompt-template-v6.md` - For deploying agents

---

*Last Updated: September 16, 2025*
*Version: 2.0 - Extracted templates to avoid nested backticks issue*
