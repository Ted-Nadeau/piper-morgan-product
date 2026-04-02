# deliver-mail

Assisted mail delivery workflow for the Piper Morgan mailbox system (v3).

## When to Use

- At session start when PM has downloaded memos from web agents
- When an agent has written memos that need routing to other inboxes
- When PM says "deliver mail", "check mail", or "run mail"
- Periodically to audit inbox staleness and delivery status

## Overview

This skill handles three phases:
1. **Ingest**: Route downloaded memos from `mailboxes/incoming/` to recipient inboxes
2. **Outbound**: Guide PM through delivering code-side memos to web agents
3. **Summary**: Log the run and report status

The PM operates the bridge between filesystem and claude.ai web. This skill handles everything else.

## Procedure

### Phase 1: Ingest (web-to-code routing)

**Step 1**: Read the last run timestamp from `mailboxes/DELIVERY-LOG.md` (the last `##` entry). If no entries exist, this is the first run.

**Step 2**: Ask PM:
```
Mail delivery starting. Last run: [timestamp or "first run"].
Have you downloaded any memos from web agents since then?
If so, please confirm they are in mailboxes/incoming/.
```

Wait for PM confirmation. If PM says no new downloads, skip to Phase 2.

**Step 3**: Scan `mailboxes/incoming/` for memo files (ignore `.gitkeep`).

**Step 4**: For each file in incoming:

1. **Parse routing from filename** using convention: `memo-YYYY-MM-DD-from-{slug}-to-{slug}[-cc-{slug}...].md`
   - Extract sender slug, primary recipient slug, CC slugs
   - If filename doesn't match convention, fall back to reading in-file To/CC/From headers

2. **Validate slugs** against `mailboxes/DIRECTORY.md`
   - If any slug is invalid, report to PM: "Invalid slug '{slug}' in {filename}. Valid slugs: [list]. Please correct the filename or tell me the intended recipient."
   - Do NOT route memos with invalid slugs. Wait for PM correction.

3. **Route the memo**:
   - Copy file to each recipient's `mailboxes/[slug]/inbox/`
   - Append a row to each recipient's `mailboxes/[slug]/inbox/MANIFEST.md`:
     ```
     | YYYY-MM-DD HH:MM | {from-slug} | {filename} | {first line of memo body after headers, truncated to 80 chars} |
     ```
   - Append to sender's `mailboxes/[from-slug]/sent.log`:
     ```
     YYYY-MM-DD HH:MM | {filename} → {recipient-slug}[, {cc-slug}...]
     ```
   - Move the original from `incoming/` to `mailboxes/[from-slug]/sent/`

4. **Report**: "Ingested {N} memos, routed to {M} inboxes."

### Phase 2: Outbound Audit (code-to-web delivery)

**Step 1**: Read `mailboxes/DIRECTORY.md` to identify web-environment roles.

**Step 2**: For each web-environment role (arch, cxo, ppm, comms, cio, host, cos, exec), check their `inbox/` for files that are NOT in their `inbox/MANIFEST.md` yet (undelivered) OR files that appear in the manifest but haven't been confirmed delivered to the web agent.

Actually, simplify: scan each web role's `inbox/` for any `.md` files other than `MANIFEST.md`. These are pending items. For each:

1. Read the memo file
2. Display to PM:
   ```
   📬 Pending delivery to [Role Name] ([slug]):
   Subject: [memo title]
   From: [sender]
   Preview: [first 3 lines of body]
   ```
3. If the memo body references repo file paths (anything matching a path pattern like `docs/`, `services/`, `config/`, etc.), list them:
   ```
   📎 This memo references:
   - docs/internal/architecture/current/adrs/adr-060-floor-first-routing.md
   - services/domain/models.py
   Please include these when delivering to the web agent.
   ```
4. Ask PM: `Deliver to [Role] now? (yes / skip / later)`
   - **yes**: Move file from `inbox/` to `read/`. Update the manifest entry if one exists, or add one marked as delivered.
   - **skip**: Leave in inbox. Note in delivery log as "skipped by PM".
   - **later**: Leave in inbox. Note in delivery log as "deferred".

**Step 3**: For code-environment roles (lead, docs), skip — they self-serve their inboxes.

**Step 4**: Report: "Delivered {X} memos to web agents. {Y} skipped. {Z} deferred."

### Phase 3: Summary + Log

**Step 1**: Check all inboxes for stale items (files older than 7 days, excluding MANIFEST.md).
- Report any stale items: "[Role] has {N} unread items, oldest from [date]"

**Step 2**: Append a timestamped entry to `mailboxes/DELIVERY-LOG.md`:

```markdown
## YYYY-MM-DD HH:MM

- **Ingested**: {N} memos from incoming/
- **Routed to inboxes**: {list of recipient slugs}
- **Web delivery**: {X} delivered, {Y} skipped, {Z} deferred
- **Stale inboxes**: {list or "none"}
- **Errors**: {any invalid slugs or issues, or "none"}
```

**Step 3**: Report summary to PM.

## Important Notes

- **Idempotency**: The skill checks manifests and sent logs to avoid duplicate deliveries. If a memo is already in a recipient's inbox and manifest, skip it.
- **Legacy memos**: Files without the naming convention are handled via in-file header parsing. Flag them to PM for awareness but still route them.
- **Mailboxes are gitignored**: All delivery operations are local. Nothing is committed to git.
- **The MANIFEST.md is the source of truth** for what has been delivered to an inbox. If it says delivered, it was delivered (filesystem-side). Web delivery confirmation is tracked separately in the delivery log.

## Error Handling

| Error | Action |
|-------|--------|
| Invalid slug in filename | Report to PM, do not route, wait for correction |
| No To/CC headers and non-standard filename | Report to PM, ask for routing instructions |
| File already exists in recipient inbox | Skip (idempotent), note in log |
| incoming/ is empty | Report "no new memos", proceed to Phase 2 |
| DELIVERY-LOG.md missing | Create it, treat as first run |
| MANIFEST.md missing for a role | Create it with header row |

## Quick Reference

```
mailboxes/
├── DIRECTORY.md          # Slug → role → environment mapping
├── DELIVERY-LOG.md       # Timestamped run history
├── incoming/             # Drop zone for downloaded memos
└── [role]/
    ├── inbox/
    │   ├── MANIFEST.md   # Delivery log for this inbox
    │   └── *.md          # Unread memos
    ├── read/             # Processed memos
    ├── sent/             # Copies of memos this role sent
    ├── sent.log          # Append-only outbound record
    └── context/          # Standing context (reserved, v2)
```
