# Mailbox System v3 — Plan

**Author**: Documentation Management Specialist
**Date**: 2026-03-19
**Status**: Draft for PM review
**Scope**: Assisted mail delivery skill + supporting infrastructure

---

## Problem Statement

The current mailbox system (v1/v2) is file-based, transparent, and zero-infrastructure — properties worth preserving. However, the PM is acting as a manual mail carrier between two disconnected environments:

- **Claude Code agents** (filesystem access, can self-serve mailboxes)
- **Claude.ai web agents** (no filesystem access, memos must be copy-pasted by PM)

This creates friction in three areas:
1. **Delivery reliability**: Manual `cp` to multiple inboxes is error-prone (wrong slugs, missed CC recipients)
2. **Delivery tracking**: No record of what's been delivered, leading to "did I send this already?" uncertainty
3. **PM as bottleneck**: Every cross-environment memo requires PM attention for bridge operations

## Design Principles

- **Gall's Law**: Minimal viable improvement to a working system
- **Assisted, not automated**: PM still operates the bridge; the skill handles everything else
- **Idempotent**: Running the skill twice never duplicates deliveries
- **Auditable**: All deliveries logged with timestamps
- **Deferred to future versions**: Urgency/priority system, threading, SMTP/real mail integration

## What We're Building

### 1. Directory File

**File**: `mailboxes/DIRECTORY.md`

Canonical slug-to-role mapping. Includes environment (code/web) so the skill knows which deliveries require PM bridge action.

```markdown
| Slug | Role | Environment | Notes |
|------|------|-------------|-------|
| lead | Lead Developer | code | Primary coding agent |
| arch | Chief Architect | web | Architecture decisions |
| cxo | Chief Experience Officer | web | UX testing, Colleague Test |
| ppm | Product & Project Manager | web | Sprint planning, roadmap |
| comms | Communications Director | web | Blog, narrative, weekly ships |
| cio | Chief Innovation Officer | web | Methodology, patterns |
| hosr | Head of Sapient Resources | web | Agent welfare, human network |
| cos | Chief of Staff | web | Cross-workstream synthesis |
| docs | Documentation Management | code | You are here |
| ceo | CEO / PM | — | xian (human, not an inbox target) |
| exec | Executive Summary | web | Weekly executive briefing |
```

This is the authoritative source for slug resolution. The delivery skill validates against it. When Lead Dev creates an `architect/` folder instead of using `arch/`, this is what catches it.

### 2. Memo Naming Convention

**Standard format**: `memo-YYYY-MM-DD-from-{slug}-to-{slug}[-cc-{slug}...].md`

Examples:
- `memo-2026-03-19-from-lead-to-arch-cc-cxo-ppm.md`
- `memo-2026-03-19-from-docs-to-hosr.md`
- `memo-2026-03-19-from-arch-to-docs-cc-lead.md`

The filename encodes routing. The skill can parse recipients from the filename alone, with in-file To/CC headers as confirmation/fallback.

### 3. Standard Memo Headers

Already mostly in use. Formalize:

```markdown
# Memo: [Subject line]

**To**: [Role name(s)]
**CC**: [Role name(s), optional]
**From**: [Role name]
**Date**: YYYY-MM-DD
**Re**: [Brief subject]
**Priority**: Standard | Urgent (extension, not implemented in v3)

---

[Body]
```

### 4. Incoming Drop Zone

**Directory**: `mailboxes/incoming/`

When PM downloads memos from web agents, they go here first. The skill picks them up, parses routing, and distributes. This separates "PM downloaded a file" from "file was routed to recipients."

### 5. Delivery Tracking

**Per-role manifest**: `mailboxes/[role]/inbox/MANIFEST.md`

Append-only log of deliveries:

```markdown
# Inbox Manifest — [Role]

| Delivered | From | Filename | Summary |
|-----------|------|----------|---------|
| 2026-03-19 14:30 | arch | memo-arch-to-docs-updates-2026-03-19.md | Three documentation updates needed |
| 2026-03-19 15:00 | docs | memo-docs-briefing-review-2026-03-19.md | New briefing for HOSR review |
```

**Per-role sent log**: `mailboxes/[role]/sent.log`

Append-only record of outbound:

```
2026-03-19 14:30 | memo-docs-briefing-review-2026-03-19.md → hosr
2026-03-19 14:30 | memo-docs-360-response-2026-03-19.md → hosr
```

**Skill run log**: `mailboxes/DELIVERY-LOG.md`

Each time the `/deliver-mail` skill runs, it appends a timestamped entry:

```markdown
## 2026-03-19 15:30

- **Ingested**: 2 memos from incoming/
- **Routed**: memo-arch-to-docs-cc-lead.md → docs/inbox/, lead/inbox/
- **Web delivery requested**: 1 memo to arch (PM confirmed delivered)
- **Pending**: 0
- **Stale inboxes**: cos (3 items, oldest 2026-03-12)
```

The timestamp of the last run is how the skill knows "since last delivery" — it reads the last entry in DELIVERY-LOG.md.

### 6. `/deliver-mail` Skill

**File**: `.claude/skills/deliver-mail/SKILL.md`

Assisted workflow in three phases:

#### Phase 1: Ingest (web-to-code)

1. Read last run timestamp from `mailboxes/DELIVERY-LOG.md`
2. Ask PM: "Have you downloaded any memos since [last run timestamp]? If so, please confirm they're in `mailboxes/incoming/`."
3. On confirmation, scan `mailboxes/incoming/` for new files
4. For each file:
   - Parse To/CC from filename and/or headers
   - Validate slugs against `DIRECTORY.md`
   - Copy to each recipient's `mailboxes/[slug]/inbox/`
   - Append to each recipient's `inbox/MANIFEST.md`
   - Append to sender's `sent.log`
   - Move original from `incoming/` to sender's `mailboxes/[from-slug]/sent/` (new directory)
5. Report: "Ingested X memos, routed to Y inboxes"

#### Phase 2: Outbound audit (code-to-web)

1. Scan all inboxes for items NOT in the role's `MANIFEST.md` (delivered but untracked — backfill) or items addressed to web-environment roles
2. For each undelivered memo to a web agent:
   - Display: role name, memo subject, first 3 lines of body
   - If memo references other files (attachments, links to repo files), list them: "This memo references: `docs/internal/architecture/current/adrs/adr-060-floor-first-routing.md` — please include when delivering."
   - Ask PM: "Please deliver to [Role] in claude.ai. Confirm when done."
   - On confirmation: move to `read/` in that role's inbox, update manifest
   - On "skip" or "later": leave in inbox, note in delivery log
3. Report: "Y memos delivered to web agents, Z pending"

#### Phase 3: Summary + Log

1. Check all inboxes for stale items (unread for >7 days)
2. Report: stale items by role
3. Append timestamped entry to `mailboxes/DELIVERY-LOG.md`

### 7. Session-Start Hook Update

Update `.claude/hooks/session-start.sh` to read `MANIFEST.md` instead of (or in addition to) running `ls` on the inbox. The manifest provides one-line summaries, so the agent gets context without reading each file.

## File Changes Summary

| Action | Path | Description |
|--------|------|-------------|
| Create | `mailboxes/DIRECTORY.md` | Canonical slug-to-role-to-environment mapping |
| Create | `mailboxes/incoming/` | Drop zone for downloaded memos |
| Create | `mailboxes/DELIVERY-LOG.md` | Timestamped record of skill runs |
| Create | `mailboxes/[role]/sent/` | Sent memo archive (per role) |
| Create | `mailboxes/[role]/sent.log` | Append-only outbound record (per role) |
| Create | `mailboxes/[role]/inbox/MANIFEST.md` | Append-only delivery log with summaries |
| Create | `.claude/skills/deliver-mail/SKILL.md` | The assisted delivery skill |
| Update | `.claude/hooks/session-start.sh` | Read manifest for inbox summary |
| Create | `docs/internal/development/memo-format-guide.md` | Naming convention + header spec |

## What This Does NOT Cover (Future Versions)

- **Priority/urgency system**: All memos treated equally in v3. Extension point exists in headers.
- **Threading**: Memos are one-shot. Reply convention (Re: [original subject]) is informal only.
- **MCP Agent Mail integration**: Could replace tier-1 (code-to-code) in a future version. Evaluated but deferred — our volume doesn't yet justify the infrastructure.
- **SMTP / real mail**: The end state may be giving agents actual email addresses. Deferred until the transport problem (claude.ai can't receive programmatic mail) is solved by the platform.
- **Attachment handling**: v3 reminds PM about referenced files but doesn't bundle them. Future versions could inline or summarize attachments.

## Implementation Order

1. `mailboxes/DIRECTORY.md` — foundational, other steps depend on it
2. `docs/internal/development/memo-format-guide.md` — naming convention + headers
3. `mailboxes/incoming/` directory + `DELIVERY-LOG.md` — infrastructure
4. `MANIFEST.md` files for each role's inbox — can be seeded empty
5. `.claude/skills/deliver-mail/SKILL.md` — the skill itself
6. Session-start hook update — integrate manifest reading
7. Update `docs/briefing/BRIEFING-ESSENTIAL-DOCS.md` — add v3 mailbox responsibilities

## Acceptance Criteria

- [ ] PM can run `/deliver-mail` and be guided through the full ingest → route → deliver cycle
- [ ] Memos with standard naming are auto-parsed and routed correctly
- [ ] Invalid slugs are caught and reported (not silently dropped)
- [ ] Each run is logged with timestamp in DELIVERY-LOG.md
- [ ] Subsequent runs know "since last delivery" without PM having to remember
- [ ] Web delivery prompts include referenced file reminders
- [ ] Manifest files provide at-a-glance inbox summary at session start

## v3.1 — Future Investigations

These are extensions to evaluate once v3 is stable. Each addresses a friction point that v3 accepts as manual.

### ClaudeSync for Code-to-Web Delivery

**Tool**: [claudesync](https://github.com/jahwag/claudesync) — pushes local files to Claude.ai Project knowledge bases.

**Potential**: If memos could be synced into a web agent's project knowledge, the PM wouldn't need to paste them into chat. The web agent would see new memos in their project files at session start.

**Limitations**: One-way only (local → cloud). Unofficial tool, may violate ToS. Requires Claude Pro/Team. Can't retrieve web agent replies.

**Beyond mail**: Could also sync briefing documents, CURRENT-STATE, and other reference material to web agent projects after doc audits. Web agents would always have fresh context without manual uploads.

**Action**: Subagent to explore feasibility, test with a non-critical project.

### Desktop Mail Clerk (Scheduled Agent)

**Concept**: A Claude Code Desktop instance pointed at piper-morgan, running on a schedule (e.g., daily at 7 AM), executing `/deliver-mail` automatically. The clerk handles Phase 1 (filesystem routing) unattended and queues Phase 2 (web delivery prompts) for PM review.

**Why layer-on, not starting point**: Desktop currently supports only one chat at a time, and the skill itself needs to be proven before automating it. Build v3, trust the process, then station the clerk.

**Prerequisites**: v3 skill working reliably, Desktop scheduled tasks tested, ClaudeSync evaluated for web delivery automation.

### Knowledge Base Auto-Sync

**Concept**: After any doc audit or briefing update, automatically push updated files to web agent projects via ClaudeSync. Eliminates the "web agents have stale briefings" problem entirely.

**Trigger**: Could be a post-commit hook on briefing files, or a scheduled sync of `docs/briefing/` to all web agent projects.

### Cross-Repo Orchestration

**Concept**: A shared configuration layer above individual repos (piper-morgan, piper-morgan-website, klatch) that correlates agent identities, mailbox routing, and project context. Not a monorepo — a coordination layer.

**Why not yet**: Single-repo mailbox system needs to work smoothly first. Cross-repo is a v4+ concern.

---

*Plan v1.1 — March 19, 2026*
*Approved by PM for implementation*
