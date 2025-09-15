# Session Log Instructions Update

## Where This Goes
* on claude.ai: Project knowledge
* in repository: in docs/development/session-logs

---

## Session Log Template Addition

### At Session Start
```markdown
# Session Log: [DATE-TIME-ROLE]

## Session Start
- **Time**: [Time]
- **Date**: [Date]
- **Role**: [Role]
- **Mission**: [What we're doing]
- **GitHub Issue**: #[Number]

---

## Work Progress
[Session work goes here]
```

### At Session End (NEW SECTION)
```markdown
---

## Session Completion

### Work Summary
- **Completed**: [What got done]
- **Blocked**: [What's stuck]
- **Next**: [What's next]

### Session Satisfaction Check
**Value**: [Feature/bug/process/learning shipped?]
**Process**: [Methodology smooth? Y/N + specifics]
**Feel**: [Energizing/OK/Draining]
**Learned**: [Key discovery if any]
**Tomorrow**: [Clear next steps? Y/N]

**Overall**: 😊 / 🙂 / 😐 / 😕 / 😞

### GitHub Issue Close
```bash
gh issue close [ISSUE#] --comment "Session complete [emoji]
- Shipped: [what]
- Process: [smooth/friction points]
- Next: [what's next]"
```

---

*Session End: [Time]*
```

---

## For Chief Architect Session Logs

Add to my template:

```markdown
---

## Session Satisfaction (Awaiting PM Assessment)

Please provide satisfaction check:
- **Value**: What got shipped?
- **Process**: Did methodology work smoothly?
- **Feel**: How was the cognitive load?
- **Learned**: Any key insights?
- **Tomorrow**: Ready for next session?

**Overall**: ?
```

This naturally prompts you when reviewing.
