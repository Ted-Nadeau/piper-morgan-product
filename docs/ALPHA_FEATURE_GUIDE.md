# Alpha Feature Guide (v0.8.5.1)

**Version**: 0.8.5.1
**Last Updated**: January 31, 2026

A guide to what Piper Morgan can do in the current alpha release.

---

## Quick Start

| Task | How |
|------|-----|
| Start Piper | `python main.py` → opens http://localhost:8001 |
| Check system health | `python main.py status` |
| Run setup wizard | `python main.py setup` or visit /setup in browser |
| Set preferences | `python main.py preferences` |

---

## Getting Set Up

### GUI Setup Wizard

The easiest way to get started. Visit http://localhost:8001/setup after starting Piper.

**What it does:**
- Checks system health (Docker, Python, ports, database)
- Configures API keys (OpenAI, Anthropic, Google Gemini, Notion)
- Creates your user account
- Connects integrations via OAuth (Slack, Google Calendar)

### CLI Alternative

For terminal lovers: `python main.py setup` walks through the same process.

### System Health Check

Run `python main.py status` anytime to verify:
- Database connection
- API key validity
- Integration health
- Performance metrics

---

## Core Features

### Chat with Piper

The main interface. Type naturally and Piper responds.

**What Piper understands well:**

| Category | Examples |
|----------|----------|
| Identity | "What's your name?" "What can you do?" "Are you working?" |
| Time | "What day is it?" "What did we do yesterday?" "What's on my agenda?" |
| Projects | "What projects am I working on?" "Status of [project]?" "Which should I focus on?" |
| Actions | "Create a GitHub issue about X" "Give me a status report" |

**For full chat capabilities**, see the [Canonical Query Test Matrix](internal/testing/canonical-query-test-matrix.md) — 19 of 25 query types work (76%).

### Interactive Standup

Create standup reports through conversation.

**How to use:**
1. Say "let's write a standup" or type `/standup`
2. Piper asks what you accomplished, what's next, any blockers
3. Review and refine iteratively until satisfied
4. Piper learns your preferences over time

### Portfolio Onboarding

For new users, Piper guides you through setting up your projects.

**How it works:**
1. Say "Hello!" as a new user
2. Piper offers to help set up your portfolio
3. Describe your projects conversationally
4. Projects are saved for future context

---

## Managing Your Work

### Lists, Todos, Projects

All three work similarly with full CRUD and sharing:

| Action | How |
|--------|-----|
| View | Click "Your Stuff" → Lists/Todos/Projects |
| Create | Click "+ Create" button |
| Edit | Click item → Edit |
| Delete | Click item → Delete (if you're owner/admin) |
| Share | Click item → Share → Enter email + role |

**Sharing roles:**
- **Viewer**: Can see but not modify
- **Editor**: Can modify but not delete or share
- **Admin**: Full access except transfer ownership

### Files

Upload and manage documents.

| Action | How |
|--------|-----|
| Upload | Files page → Upload (PDF, DOCX, TXT, MD, JSON up to 10MB) |
| Download | Click file → Download |
| Delete | Click file → Delete |

Files are user-isolated — you only see your own.

### Lifecycle Indicators

Projects and todos show lifecycle status badges:
- **Active**: Currently being worked on
- **Paused**: On hold
- **Completed**: Done
- **Archived**: No longer relevant

---

## Integrations

### Integration Health Dashboard

**Where**: Settings → Integrations

Check the health of all your connected services:
- Green = Healthy
- Yellow = Degraded
- Red = Failed
- Gray = Not configured

Click "Test All" for a comprehensive check, or test individual integrations.

### Slack

**Setup**: Settings → Integrations → Slack → Connect (OAuth)

**What works:**
- Send messages to channels
- Read channel history
- Receive notifications

### Google Calendar

**Setup**: Settings → Integrations → Calendar → Connect (OAuth)

**What works:**
- View your schedule ("What's on my calendar?")
- Create events
- Check availability

### GitHub

**Setup**: Settings → Integrations → GitHub → Enter PAT token

**What works:**
- Create issues ("Create a GitHub issue about X")
- Search issues
- View repository status
- Update issues

### Notion

**Setup**: Added during setup wizard (API key)

**What works:**
- Create pages
- Search content
- Document analysis ("Analyze this document")

---

## Personalization

### Preferences

Run `python main.py preferences` to set your preferences across 5 dimensions:

| Dimension | What it affects |
|-----------|-----------------|
| Communication | How Piper phrases responses |
| Work style | Task recommendations |
| Decision making | How much guidance vs. options |
| Learning | Explanation depth |
| Feedback | How Piper gives suggestions |

### Learning System

Piper learns from your interactions over time:
- Communication patterns
- Preferred workflows
- Common requests

This is experimental — feedback welcome on whether personalization feels accurate.

---

## Accessibility

Piper is designed to be accessible:

- **Keyboard navigation**: Tab through all UI elements
- **Screen readers**: ARIA landmarks throughout
- **High contrast**: Respects system preference
- **Reduced motion**: Respects system preference
- **Color contrast**: WCAG 2.1 AA compliant (4.5:1 minimum)

---

## Security

### What's Protected

| Data | Protection |
|------|------------|
| API keys | Encrypted in system keychain |
| Passwords | Bcrypt hashed (12 rounds) |
| Sessions | JWT tokens with expiration |
| Resources | Owner-based access control |

### What's Not Yet Protected

- Data at rest (database contents) — **use test data only**
- Full encryption at rest planned for beta

### Audit Logging

All sensitive operations are logged:
- Authentication events
- API key operations
- User actions

---

## Commands Reference

### CLI Commands

| Command | Purpose |
|---------|---------|
| `python main.py` | Start server |
| `python main.py --verbose` | Start with detailed logging |
| `python main.py --no-browser` | Start without opening browser |
| `python main.py setup` | Run setup wizard |
| `python main.py status` | Check system health |
| `python main.py preferences` | Set user preferences |
| `python main.py migrate-user` | Migrate user data |

### Chat Commands

| Command | Purpose |
|---------|---------|
| `/standup` | Start interactive standup |
| `/help` | Get help |

---

## Technical Details

For alpha testers who want to know what's under the hood:

- **Database**: PostgreSQL (via Docker on port 5433)
- **Test coverage**: 5,253 tests passing
- **API**: FastAPI on port 8001
- **Auth**: JWT tokens with bcrypt passwords

---

## See Also

- [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) — What's broken or incomplete
- [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — Setup instructions
- [ALPHA_QUICKSTART.md](ALPHA_QUICKSTART.md) — 2-5 minute setup
- [Canonical Query Test Matrix](internal/testing/canonical-query-test-matrix.md) — Full chat capabilities

---

_Last Updated: January 31, 2026_
