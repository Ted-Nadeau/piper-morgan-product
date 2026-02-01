# Alpha Known Issues (v0.8.5.1)

**Version**: 0.8.5.1
**Last Updated**: January 31, 2026

This document helps alpha testers avoid wasting time on things we already know about.

---

## Known Issues

### Blocking

_None currently. All P0 issues resolved as of January 30, 2026._

### Annoying

| Issue | Description | Workaround |
|-------|-------------|------------|
| [#696](https://github.com/mediajunkie/piper-morgan-product/issues/696) | Settings uses hardcoded user ID | Settings changes work but may not attribute to correct user in audit logs |
| [#697](https://github.com/mediajunkie/piper-morgan-product/issues/697) | Intent service uses hardcoded user ID | Chat works but user context not fully preserved |

**Impact**: Both issues affect audit trail accuracy and multi-user attribution. Single-user alpha testing is unaffected functionally.

### Cosmetic

_None currently tracked._

---

## Partially Complete

These features exist but have rough edges. Expect some friction.

| Feature | Status | What Works | What Doesn't |
|---------|--------|------------|--------------|
| **Data Encryption** | Partial | API keys encrypted in keychain, passwords bcrypt-hashed | Data at rest not fully encrypted. Use test data only. |
| **GitHub OAuth** | Not started | PAT token auth works | OAuth connect flow planned for future release |
| **Advanced Privacy** | Basic only | Owner-based access, sharing works | Granular controls planned for beta |

---

## Needs Testing

These features are complete but need real-world validation from alpha testers:

| Feature | What to Test | How to Access |
|---------|--------------|---------------|
| **Portfolio Onboarding** | Does the conversational project setup make sense? | Say "Hello!" as a new user |
| **Interactive Standup** | Does iterative refinement feel natural? | Say "let's write a standup" |
| **Learning System** | Does Piper adapt to your communication style over time? | Use for a few days, note any personalization |
| **Lifecycle Indicators** | Do status badges appear correctly on projects/todos? | Check Projects and Todos views |
| **Accessibility** | Keyboard navigation, screen reader support | Tab through UI, test with VoiceOver |
| **Integration Health** | Does the dashboard accurately reflect your integration status? | Settings → Integrations → Test All |

---

## What Works

For detailed feature documentation, see [ALPHA_FEATURE_GUIDE.md](ALPHA_FEATURE_GUIDE.md).

**Summary by category:**

- **Setup**: GUI wizard, CLI wizard, system health checks
- **Authentication**: Login/logout, JWT tokens, password security
- **Integrations**: Slack (OAuth), Google Calendar (OAuth), GitHub (PAT), Notion (API key), Health Dashboard
- **Core UI**: Lists, Todos, Projects, Files — all with CRUD and sharing
- **Chat**: 19 of 25 canonical queries working (76%). See [Canonical Query Test Matrix](internal/testing/canonical-query-test-matrix.md) for details.
- **Accessibility**: WCAG 2.1 AA compliant, keyboard nav, high contrast mode
- **Quality**: 5,253 automated tests passing

---

## Planned for Beta

Brief overview. See [roadmap](internal/planning/roadmap/roadmap.md) for full details.

| Milestone | Focus |
|-----------|-------|
| M1: Foundation | Encryption at rest, auth context fixes, WebSocket infrastructure |
| M2: Activation | Wiring gaps, Notion activation, lifecycle UI completion |
| M3: Skills | Core skills library, multi-agent coordinator |
| M4: Documents | Unified document processing, file browser |
| M5: Polish | Registration flow, priority engine |

---

## How to Report Issues

### Before Reporting

1. Check this list — is it already known?
2. Gather context: `python main.py status > status.txt`

### What to Include

```
WHAT I TRIED: [specific action]
WHAT I EXPECTED: [expected result]
WHAT HAPPENED: [actual result]
ERROR MESSAGE: [if any]
```

### Where to Report

- **GitHub Issues**: [Create new issue](https://github.com/mediajunkie/piper-morgan-product/issues/new)
- **Email**: christian@[domain] for private issues
- **Weekly Check-in**: Discuss during scheduled calls

---

## Testing Focus

**Please focus on:**
- Setup experience — was the wizard intuitive?
- Daily workflows — what feels natural vs. clunky?
- Integration points — if you use GitHub/Slack/Notion/Calendar
- Performance — any lag or delays?
- Overall feel — delightful or frustrating?

**Please report:**
- Blockers (can't use at all)
- Frequent annoyances (happens repeatedly)
- Delightful surprises (what worked great!)
- Missing expectations (thought it would do X)

---

## See Also

- [ALPHA_FEATURE_GUIDE.md](ALPHA_FEATURE_GUIDE.md) — What's available and how to use it
- [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — Setup and usage instructions
- [ALPHA_QUICKSTART.md](ALPHA_QUICKSTART.md) — Quick 2-5 minute setup
- [Canonical Query Test Matrix](internal/testing/canonical-query-test-matrix.md) — Chat capabilities detail

---

_Last Updated: January 31, 2026_
