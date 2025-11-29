# Pilot Setup - Complete File Download Guide

## Files to Download (11 total)

### Coordination Queue Files (5 files)
1. **File**: `coordination-manifest.json`
   - **Currently at**: `/mnt/user-data/outputs/coordination/manifest.json`
   - **Save to your laptop as**: `downloads/coordination-manifest.json`

2. **File**: `coordination-README.md`
   - **Currently at**: `/mnt/user-data/outputs/coordination/README.md`
   - **Save to your laptop as**: `downloads/coordination-README.md`

3. **File**: `001-audit-models-object-model.md`
   - **Currently at**: `/mnt/user-data/outputs/coordination/available/001-audit-models-object-model.md`
   - **Save to your laptop as**: `downloads/001-audit-models-object-model.md`

4. **File**: `002-advisor-mailbox-ted.md`
   - **Currently at**: `/mnt/user-data/outputs/coordination/available/002-advisor-mailbox-ted.md`
   - **Save to your laptop as**: `downloads/002-advisor-mailbox-ted.md`

5. **File**: `003-composting-learning-pipeline.md`
   - **Currently at**: `/mnt/user-data/outputs/coordination/available/003-composting-learning-pipeline.md`
   - **Save to your laptop as**: `downloads/003-composting-learning-pipeline.md`

### Ted's Advisor Mailbox Files (4 files)
6. **File**: `ted-manifest.json`
   - **Currently at**: `/mnt/user-data/outputs/advisors/ted-nadeau/manifest.json`
   - **Save to your laptop as**: `downloads/ted-manifest.json`

7. **File**: `ted-README.md`
   - **Currently at**: `/mnt/user-data/outputs/advisors/ted-nadeau/README.md`
   - **Save to your laptop as**: `downloads/ted-README.md`

8. **File**: `001-bootstrap-feedback.md`
   - **Currently at**: `/mnt/user-data/outputs/advisors/ted-nadeau/inbox/001-bootstrap-feedback.md`
   - **Save to your laptop as**: `downloads/001-bootstrap-feedback.md`

9. **File**: `object-model-overview.md`
   - **Currently at**: `/mnt/user-data/outputs/advisors/ted-nadeau/context/object-model-overview.md`
   - **Save to your laptop as**: `downloads/object-model-overview.md`

### Agent Setup Instructions (2 files)
10. **File**: `setup-prompt-queue-instructions.md`
    - **Currently at**: `/mnt/user-data/outputs/setup-prompt-queue-instructions.md`
    - **Save to your laptop as**: `downloads/setup-prompt-queue-instructions.md`

11. **File**: `audit-models-object-model.md` (the completed audit example)
    - **Currently at**: `/mnt/user-data/outputs/audit-models-object-model.md`
    - **Save to your laptop as**: `downloads/audit-models-object-model.md`

---

## Final Folder Structure (what the agent will create)

```
your-repo/
├── coordination/
│   ├── manifest.json          (from coordination-manifest.json)
│   ├── README.md              (from coordination-README.md)
│   ├── available/
│   │   ├── 001-audit-models-object-model.md
│   │   ├── 002-advisor-mailbox-ted.md
│   │   └── 003-composting-learning-pipeline.md
│   ├── claimed/               (empty initially)
│   ├── complete/              (empty initially)
│   └── blocked/               (empty initially)
└── advisors/
    └── ted-nadeau/
        ├── manifest.json      (from ted-manifest.json)
        ├── README.md          (from ted-README.md)
        ├── inbox/
        │   └── 001-bootstrap-feedback.md
        ├── outbox/            (empty initially)
        ├── context/
        │   └── object-model-overview.md
        └── archive/           (empty initially)
```

---

## Your Action Plan

### Step 1: Download All Files
Download all 11 files listed above to a `downloads/` folder on your laptop. Use the suggested names to avoid conflicts (e.g., `coordination-README.md` and `ted-README.md` instead of two files named `README.md`).

### Step 2: Give This Prompt to Claude Code

```
I have downloaded 11 files for setting up a prompt queue system and advisor mailbox. They're in my downloads folder. Please:

1. Create the directory structure:
   - coordination/ with subdirs: available/, claimed/, complete/, blocked/
   - advisors/ted-nadeau/ with subdirs: inbox/, outbox/, context/, archive/

2. Place the files correctly:
   - coordination-manifest.json → coordination/manifest.json
   - coordination-README.md → coordination/README.md
   - 001-audit-models-object-model.md → coordination/available/
   - 002-advisor-mailbox-ted.md → coordination/available/
   - 003-composting-learning-pipeline.md → coordination/available/
   - ted-manifest.json → advisors/ted-nadeau/manifest.json
   - ted-README.md → advisors/ted-nadeau/README.md
   - 001-bootstrap-feedback.md → advisors/ted-nadeau/inbox/
   - object-model-overview.md → advisors/ted-nadeau/context/

3. Update all paths in both manifest.json files:
   - Remove any "/mnt/user-data/outputs/" prefixes
   - Make paths relative to repo root (e.g., "coordination/available/001...")

4. Verify the JSON files are valid and all referenced files exist.

5. Commit everything to git.

The downloaded files are in: [tell agent where you saved them]
```

### Step 3: Run Your First Pilot

Once the agent confirms setup is complete, start a new agent session and say:

```
Check coordination/manifest.json for available work.
Claim prompt 002 (advisor mailbox) and execute it following the README instructions.
```

---

## Success Checklist
- [ ] All 11 files downloaded
- [ ] Agent created folder structure
- [ ] Files placed in correct locations
- [ ] Paths updated in manifest files
- [ ] Git commit successful
- [ ] First pilot agent can see available work

---

*This guide ensures you get exactly the right files and the agent knows exactly where to put them.*
