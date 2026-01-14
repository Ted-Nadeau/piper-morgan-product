# Agent Mailbox System

**Purpose**: Enable async communication between agents (internal roles) and external advisors without requiring the PM to be a human message bus.

---

## Directory Structure

```
mailboxes/
├── README.md                    # This file
├── arch/                        # Chief Architect
│   ├── inbox/                   # Unread messages
│   ├── read/                    # Read messages (moved from inbox)
│   └── context/                 # Background documents
├── cio/                         # Chief Innovation Officer
│   ├── inbox/
│   ├── read/
│   └── context/
├── ceo/                         # PM (xian)
│   ├── inbox/
│   ├── read/
│   └── context/
└── ted-nadeau/                  # External advisor
    ├── inbox/
    ├── read/
    ├── context/
    └── outbox/                  # External advisors respond here
```

---

## Role Slugs

| Role | Slug | Type |
|------|------|------|
| CEO/PM (xian) | `ceo` | Internal |
| Chief Architect | `arch` | Internal |
| Chief Innovation Officer | `cio` | Internal |
| Lead Developer | `lead` | Internal |
| Chief of Communications | `comms` | Internal |
| Principal Product Manager | `ppm` | Internal |
| Chief Experience Officer | `cxo` | Internal |
| Head of Sapient Resources | `hosr` | Internal |
| Chief of Staff / Exec Assistant | `exec` | Internal |
| Special Assignment Agent | `spec` | Internal |
| Ted Nadeau | `ted-nadeau` | External Advisor |

---

## Message Format

```markdown
# [Subject Line]

**From**: [sender-slug]
**To**: [recipient-slug]
**Date**: [YYYY-MM-DD HH:MM]
**In-Reply-To**: [original-message-filename, if reply]
**Response-Requested**: [yes/no]
**Priority**: [high/medium/low]

---

[Message body]

## Questions (if any)
1. [Numbered questions for clarity]

---
*Filed by: [agent-role] | Session: [session-id if applicable]*
```

### File Naming Convention

```
[NNNN]-[YYYY-MM-DD]-[from-slug]-[brief-subject].md

Examples:
0001-2026-01-13-lead-multichat-integration.md
0002-2026-01-13-ceo-slack-oauth-question.md
```

---

## Workflow

### Sending a Message

1. Create message file in recipient's `inbox/` folder
2. Use message format above
3. Set `Response-Requested: yes` if you need a reply

### Reading Messages (Agent Session Start)

Add to CLAUDE.md or session briefing:
```
## Session Start: Check Mailbox

Before starting work, check your inbox:
1. `ls mailboxes/[your-slug]/inbox/`
2. Read any new messages
3. Move read messages to `read/` folder
4. Address urgent items first
```

### Responding

1. If responding to internal agent: Create new message in their `inbox/`
2. If responding as external advisor: Create response in your `outbox/`
3. Set `In-Reply-To:` header to original filename

### Tracking Status

- **In `inbox/`** = Unread
- **In `read/`** = Read, no response needed
- **Has `In-Reply-To`** = Response to previous message
- **`Response-Requested: yes`** = Awaiting reply

---

## Internal vs External Advisors

### Internal Roles (Agents)
- Have direct file access
- Deliver messages by creating files in recipient's `inbox/`
- Read their own `inbox/` at session start

### External Advisors
- May or may not have file access
- Have additional `outbox/` folder for responses
- PM relays messages if advisor lacks file access

---

## Migration from advisors/

The previous `advisors/` structure is superseded by this system:
- `advisors/ted-nadeau/` → `mailboxes/ted-nadeau/`
- Same folder structure preserved
- Added internal role mailboxes

---

## CLAUDE.md Integration

Add to agent briefings:

```markdown
## Mailbox Check (Session Start)

Check your inbox before starting work:
\`\`\`bash
ls mailboxes/[your-role-slug]/inbox/
\`\`\`

If messages exist:
1. Read each message
2. Move to `read/` folder after reading
3. Create response if `Response-Requested: yes`
4. Note any action items for your session
```

---

*Established: January 13, 2026*
*Version: 1.0*
