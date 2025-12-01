# Advisor Mailbox - Ted Nadeau

## Purpose
Enable async participation in Piper Morgan architectural discussions without requiring real-time presence in development sessions.

## Directory Structure
```
/advisors/ted-nadeau/
  manifest.json       # Message tracking and status
  README.md          # This file
  /inbox/            # Questions/requests from team
  /outbox/           # Your responses
  /context/          # Background documents
  /archive/          # Processed conversations
```

## Workflow

### Receiving Messages (Team → Ted)
1. Team places questions in `/inbox/` with context
2. Manifest updated with new message metadata
3. You check inbox at your convenience
4. Questions include relevant context documents

### Responding (Ted → Team)
1. Read message in `/inbox/`
2. Create response in `/outbox/` with same ID
3. Update manifest.json:
   - Mark inbox message as "read"
   - Add outbox entry
4. Team integrates response in next relevant session

### Message Format
```markdown
# Subject Line

**From**: [Sender]
**To**: [Recipient]
**Date**: [ISO timestamp]
**Priority**: [high/medium/low]
**Context**: [Which discussion/ADR/issue this relates to]

---

[Message body]

## Specific Questions
1. [Numbered questions for clarity]

## Response Needed By
[Optional deadline if time-sensitive]
```

## Manifest Structure
```json
{
  "messages": {
    "inbox": [
      {
        "id": "001",
        "subject": "Subject line",
        "from": "Sender",
        "date": "ISO timestamp",
        "status": "unread|read",
        "priority": "high|medium|low",
        "file": "inbox/001-filename.md"
      }
    ],
    "outbox": [...],
    "archive": [...]
  }
}
```

## Bootstrap Plan

This mailbox itself is the first project you can contribute to:

1. **Use it** - Participate through this interface
2. **Improve it** - Enhance based on your experience
3. **Build it** - Create the full implementation

Your improvements become the spec. Your experience shapes the feature.

## Getting Started

1. Read `/inbox/001-bootstrap-feedback.md`
2. Create `/outbox/001-bootstrap-response.md`
3. Update manifest.json
4. Suggest improvements to this workflow

## Integration Points

Your responses will be integrated into:
- Architecture Decision Records (ADRs)
- Development session planning
- Technical implementation guidance
- Strategic direction discussions

## Async Advantages

- Respond at your convenience
- Deep thinking time for complex questions
- Written record of all architectural input
- No timezone/scheduling constraints
- Progressive context building

## Future Enhancements (Your Domain)

As you build the full implementation, consider:
- Notification system (email? Slack?)
- Web interface for easier interaction
- Threading for complex discussions
- Priority/categorization improvements
- Integration with git workflows
- Multi-advisor scaling

---

*Welcome to async collaboration! Your first message awaits in the inbox.*
