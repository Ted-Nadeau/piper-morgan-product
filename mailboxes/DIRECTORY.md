# Mailbox Directory

Canonical slug-to-role mapping. Used by `/deliver-mail` skill for routing validation.

| Slug | Role | Environment | Notes |
|------|------|-------------|-------|
| lead | Lead Developer | code | Primary coding agent, Claude Code |
| arch | Chief Architect | web | Architecture decisions, ADRs |
| cxo | Chief Experience Officer | web | UX testing, Colleague Test |
| ppm | Principal Product Manager | web | Sprint planning, roadmap |
| comms | Communications Chief | web | Blog, narrative, editorial calendar |
| cio | Chief Innovation Officer | web | Methodology, patterns |
| hosr | Head of Sapient Resources | web | Agent welfare, human network |
| exec | Chief of Staff | web | Executive office, cross-workstream synthesis, Weekly Ship drafts |
| docs | Documentation Management | code | Omnibus logs, mailbox ops, blog pipeline |
| pa | Piper Alpha | code | PM assistant, standup synthesis, meeting prep, document review |
| spec | Special Assignments | web | Specialist work, activated as needed |

## Notes

- **code** = Claude Code agent with filesystem access. Can self-serve mailboxes.
- **web** = Claude.ai web agent. Memos must be delivered by PM via copy-paste.
- **PM (xian)** is human, not a mailbox recipient. CC: PM means PM sees it in the session where mail is delivered.
- Slugs are lowercase, match directory names under `mailboxes/`.
- If a slug doesn't appear here, it's invalid. The `/deliver-mail` skill will reject it.

## Retired / Special Mailboxes

| Slug | Status | Notes |
|------|--------|-------|
| cos | retired | Was alias for Chief of Staff; use exec instead |
| dan-heck | external | Alpha tester inbox |
| ted-nadeau | external | Alpha tester inbox |

## PM / Founder

| Slug | Notes |
|------|-------|
| xian | Human PM/founder. Not a mailbox recipient. Also known as `ceo`. CC: xian means PM sees it during delivery. |
