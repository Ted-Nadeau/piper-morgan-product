# Setup Prompt Queue System - Agent Instructions

## Context
You are setting up an async prompt queue system that allows AI agents to self-serve work without real-time coordination. The PM has downloaded the necessary files from a planning session and needs you to systematically establish this in the repository.

## Your Task
Set up the complete coordination queue structure in the repository, ensuring all paths are correct and the system is immediately operational.

## Step 1: Locate Downloaded Files
The PM has downloaded these files (likely in dev/active/):
- `manifest.json` - Central tracking file
- `README.md` - Instructions for agents
- `001-audit-models-object-model.md` - Pilot prompt 1
- `002-advisor-mailbox-ted.md` - Pilot prompt 2
- `003-composting-learning-pipeline.md` - Pilot prompt 3

Ask the PM: "Where did you save the downloaded coordination files?"

## Step 2: Create Directory Structure
```bash
# In repository root, create the structure
mkdir -p coordination/{available,claimed,complete,blocked}
```

## Step 3: Place Files Correctly
1. Copy `manifest.json` to `coordination/`
2. Copy `README.md` to `coordination/`
3. Copy all three `.md` prompt files to `coordination/available/`

## Step 4: Update All Paths in manifest.json
Open `coordination/manifest.json` and replace ALL occurrences of:
- `/mnt/user-data/outputs/coordination/` with `coordination/`

Specifically update the "file" field for each prompt:
- Change: `"file": "/mnt/user-data/outputs/coordination/available/001-audit-models-object-model.md"`
- To: `"file": "coordination/available/001-audit-models-object-model.md"`

## Step 5: Verify Path Consistency
Check that paths in manifest.json match actual file locations:
```bash
# For each file mentioned in manifest.json, verify it exists
ls coordination/available/001-audit-models-object-model.md
ls coordination/available/002-advisor-mailbox-ted.md
ls coordination/available/003-composting-learning-pipeline.md
```

## Step 6: Set Up Ted's Advisor Mailbox Structure
Since prompt 002 is about creating Ted's mailbox, also create:
```bash
mkdir -p advisors/ted-nadeau/{inbox,outbox,context,archive}
```

Copy any Ted-related files if the PM downloaded them:
- `advisors/ted-nadeau/manifest.json`
- `advisors/ted-nadeau/README.md`
- `advisors/ted-nadeau/inbox/001-bootstrap-feedback.md`
- `advisors/ted-nadeau/context/object-model-overview.md`

Update paths in Ted's manifest.json too (remove `/mnt/user-data/outputs/` prefix).

## Step 7: Create .gitignore Considerations
Add to `.gitignore` if needed:
```
# Coordination queue - keep claimed/complete but ignore local work files
coordination/claimed/*.tmp
coordination/blocked/*.tmp
```

## Step 8: Test the System
1. Verify manifest is valid JSON:
```bash
python -c "import json; json.load(open('coordination/manifest.json'))"
```

2. Verify all referenced files exist:
```bash
# This should show 3 files
ls coordination/available/*.md | wc -l
```

3. Ensure directories are ready:
```bash
# Should show 4 directories
ls -d coordination/*/
```

## Step 9: Commit Everything
```bash
git add coordination/
git add advisors/  # if you set up Ted's mailbox
git commit -m "feat: Add async prompt queue system for agent coordination

- Central manifest tracking in coordination/manifest.json
- 3 pilot prompts ready in available/
- README with complete agent instructions
- Directory structure for claim/complete/blocked workflow
- Ted's advisor mailbox structure prepared"
```

## Step 10: Create First Test Claim
To verify everything works, simulate claiming a prompt:
1. Copy `002-advisor-mailbox-ted.md` from `available/` to `claimed/`
2. Update manifest.json:
   - Change status from "available" to "claimed"
   - Add: `"claimed_by": "setup-test"`
   - Add: `"claimed_at": "[current-timestamp]"`
3. Then revert these changes (this was just a test)

## Success Verification
- [ ] coordination/ directory exists in repo root
- [ ] manifest.json has correct relative paths (no /mnt/)
- [ ] All 3 prompts are in coordination/available/
- [ ] README is in coordination/
- [ ] Empty directories exist for claimed/, complete/, blocked/
- [ ] Manifest loads as valid JSON
- [ ] Git commit successful

## Report Back
Tell the PM:
1. "Prompt queue system successfully established in /coordination/"
2. "3 pilot prompts ready for agents to claim"
3. "System tested and operational"
4. Share any issues encountered

## Notes
- This system allows any agent with repo access to claim and execute work
- Agents update the manifest when claiming/completing prompts
- The PM can check progress by reviewing manifest.json anytime
- No real-time coordination required!

---

*If you encounter any issues or need clarification, ask the PM before proceeding.*
