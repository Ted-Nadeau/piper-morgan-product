---
name: cleanup-dev-active
description: Triage and archive stale files from dev/active/. Use during session
  wrap-up, weekly audits, or when dev/active/ exceeds ~15 files. Prevents working
  directory from becoming a graveyard of superseded drafts.
scope: cross-role
version: 1.0
created: 2026-03-30
---

# cleanup-dev-active

Triage files in `dev/active/` — archive completed/superseded work, keep only what's genuinely in progress.

## When to Use

- During session wrap-up when you notice dev/active/ is cluttered
- During weekly docs audit (#937-series)
- When dev/active/ exceeds ~15 files
- PM asks to "clean up dev/active" or "sort the working directory"

## Principle

`dev/active/` is a workbench, not a filing cabinet. Files land here during active work and should move out when the work is done. The accumulation pattern is: agent creates file → work completes → file stays because nobody moves it.

## Procedure

### Step 1: Inventory

```bash
# List files with last-modified dates
for f in dev/active/*; do
  if [ -f "$f" ]; then
    modified=$(git log -1 --format='%ai' -- "$f" 2>/dev/null | cut -d' ' -f1)
    echo "$modified | $(basename "$f")"
  elif [ -d "$f" ]; then
    echo "DIR      | $(basename "$f")/"
  fi
done | sort
```

### Step 2: Categorize Each File

For each file, determine its disposition:

| Category | Signal | Action |
|----------|--------|--------|
| **Active work** | Referenced in current sprint, upcoming deadline, or PM agenda | **Keep** in dev/active/ |
| **Completed deliverable** | Work is done, filed as issue, merged, or published | **Archive** to `dev/YYYY/MM/DD/` (use the file's last-modified date) |
| **Superseded draft** | Newer version exists elsewhere (docs/briefing/, docs/public/, etc.) | **Archive** to dated directory |
| **Duplicate** | Multiple versions with `(1)`, `(2)` suffixes | **Delete** duplicates, keep the latest or the one in its canonical location |
| **Reference data** | CSVs, indexes, reports that aren't actively being updated | **Move** to `docs/internal/` or archive |
| **Agent workspace** | Subdirectory for a specific agent (e.g., `pa/`) | **Keep** if agent is active |
| **Unknown** | Can't determine purpose | **Ask PM** before moving |

### Step 3: Execute Moves

```bash
# Archive completed/superseded files
mkdir -p dev/YYYY/MM/DD
git mv dev/active/completed-file.md dev/YYYY/MM/DD/

# Delete true duplicates (files with (1), (2) suffixes where canonical exists)
git rm "dev/active/file (1).md"

# Move reference data to permanent home
git mv dev/active/reference-data.csv docs/internal/appropriate-location/
```

### Step 4: Verify

```bash
# Count remaining files
ls dev/active/ | wc -l  # Target: <15

# Confirm no broken references
grep -r "dev/active/archived-file" docs/ .claude/  # Should be empty
```

### Step 5: Report

Add to session log:
```
### dev/active/ cleanup
- Before: N files
- Archived: X files to dev/YYYY/MM/DD/
- Deleted: Y duplicates
- Kept: Z active files
- After: Z files
```

## What to Keep (Safe List)

These types of files belong in dev/active/:
- Files for work with an upcoming deadline (conference talks, scheduled publishes)
- `publish-package/` — active publishing workflow artifacts
- Agent workspace directories (e.g., `pa/`) for active agents
- Specs or plans PM is actively reviewing

## What to Archive (Common Accumulations)

These commonly pile up and should be moved:
- Superseded briefing drafts (v0.1 when v0.2 is in docs/briefing/)
- Onboarding prompts after agent launch is complete
- Proposals after issues are filed
- Session logs that belong in dev/YYYY/MM/DD/ (rare — create-session-log usually puts them in the right place)
- Completed tracker spreadsheets

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Delete files without checking | May be PM's in-progress work | Archive to dated directory |
| Move files PM dropped here recently | PM uses dev/active/ as a dropbox | Ask before moving files < 3 days old |
| Clean up during active sprint work | Context switching wastes time | Do it at session boundaries |
| Move agent workspace directories | Other agents depend on the path | Only move if agent is decommissioned |

## Frequency

- **Light triage**: Every session wrap-up (move obviously completed files)
- **Full cleanup**: Weekly audit or when file count > 15
- **PM-initiated**: When PM says "clean up" or "sort dev/active"
