# Session Log Standard v2.0
**Last Updated**: September 23, 2025

## Purpose
Session logs maintain context, institutional memory, and enable effective handoffs between development sessions. They are critical for the Excellence Flywheel methodology.

## When to Create a Session Log
- Every development session (Chief Architect, Lead Developer, Agents)
- At the START of each session (not at the end)
- One log per session (do not create multiple unless asked to and even then verify the reason for starting a new one)

## Nomenclature

### Format
```
YYYY-MM-DD-HHMM-[role]-[product]-log.md
```

### Role Slugs (EXACTLY THESE)
- `exec` - Chief of Staff/Executive Assistant
- `arch` - Chief Architect
- `lead` - Lead Developer
- `prog` - Programmer (both Code and Cursor)

### Product/Model Slugs
- `opus` - Claude Opus (in Claude.ai)
- `sonnet` - Claude Sonnet (in Claude.ai)
- `code` - Claude Code
- `cursor` - Cursor Agent

### Examples
```
2025-09-22-0816-arch-opus-log.md
2025-09-22-1046-lead-sonnet-log.md
2025-09-22-1400-prog-code-log.md
2025-09-22-1400-prog-cursor-log.md
2025-09-22-0900-exec-opus-log.md
```

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

## Location Strategy

### Priority Order (Use First Available)

1. **Artifacts** (when reliable)
   - Pros: Attached to project, versioning, easy navigation
   - Cons: Intermittent bugs, naming issues
   - Backup: Download periodically with -HHMM timestamp

2. **Filesystem** (when available)
   - Pros: Secure, real-time, findable
   - Cons: Not available in standard Claude.ai
   - Path: `/Users/xian/Development/piper-morgan/dev/YYYY/MM/DD/`

3. **Sandbox** (fallback)
   - Pros: Usually available
   - Cons: Update failures, no project attachment
   - Backup: Download with -HHMM timestamps

### CRITICAL: Verify Every Write

```bash
# After ANY log update:
echo "Verifying log update..." && tail -5 [logfile]
# Or
cat [logfile] | grep -c "latest entry"
```

## Commands for Each Role

### Chief Architect (opus)
```bash
# Create directory and log
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-arch-opus-log.md
```

### Lead Developer (sonnet)
```bash
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-lead-sonnet-log.md
```

### Programmer - Code
```bash
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-prog-code-log.md
```

### Programmer - Cursor
```bash
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-prog-cursor-log.md
```

## Reliability Protocol

### Every Write Must:
1. Attempt the write
2. Verify it succeeded
3. Report any failure
4. Fall back to next option if failed

### Verification Example
```python
# Write
with open(logfile, 'a') as f:
    f.write(entry)

# Verify
with open(logfile, 'r') as f:
    content = f.read()
    if entry not in content:
        print("WARNING: Write failed")
```

## Backup Strategy

### Manual Snapshots
When downloading for backup, add timestamp:
```
Original: 2025-09-22-0816-arch-opus-log.md
Backup:   2025-09-22-0816-arch-opus-log-1430.md
                                         ^^^^
                                    backup time
```

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
Templates can be found in project knowledge or the `knowledge/` directory on the local filesystem:
- `session-log-template.md` - Standard sessions
- `session-log-template-chief-architect.md` - Chief Architect sessions
- `session-log-template-lead-developer.md` - Lead Developer sessions

## Related Documentation
- `methodology-00-EXCELLENCE-FLYWHEEL.md` - Core methodology
- `github-guide.md` - GitHub workflow requirements
- `gameplan-template-.md` - For creating gameplans
- `agent-prompt-template-v6.md` - For deploying agents

### End of Session
Always download/save final version to filesystem


---

*This standard prioritizes reliability over any specific location*
