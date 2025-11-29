# Coordination Queue - Agent Instructions

## Overview
This is a self-service prompt queue for AI agents working on Piper Morgan. Instead of waiting for real-time coordination, agents can claim available work, execute it, and mark it complete.

## For Agents: How to Use This System

### 1. Check for Available Work
```bash
# Look at the manifest to see available prompts
cat /coordination/manifest.json | grep -A5 "available"

# Or check the available directory
ls /coordination/available/
```

### 2. Claim a Prompt
When you select a prompt to work on:
1. Read the full prompt file in `/available/`
2. Update manifest.json:
   - Change status from "available" to "claimed"
   - Add "claimed_by": "[your-session-id]"
   - Add "claimed_at": "[current-timestamp]"
3. Move the file from `/available/` to `/claimed/`

### 3. Execute the Work
- Follow the prompt specifications exactly
- Stay within defined scope
- Meet all acceptance criteria
- Create specified deliverables

### 4. Mark Complete
When work is verified complete:
1. Update manifest.json:
   - Change status from "claimed" to "complete"
   - Add "completed_at": "[timestamp]"
   - Add "verification": "passed"
2. Move prompt file to `/complete/`
3. Add completion notes to the prompt file

### 5. Handle Blocks
If you cannot complete due to external dependency:
1. Update status to "blocked"
2. Add "blocked_reason": "[explanation]"
3. Move file to `/blocked/`

## For Humans: Creating Prompts

### Prompt Structure
Each prompt must include:
- **Context**: Why this work matters
- **Scope**: What's in/out of scope
- **Acceptance Criteria**: Checklist of requirements
- **Deliverables**: What gets created
- **Resources**: Links to relevant docs
- **Verification**: How to confirm completion

### Adding New Prompts
1. Create new .md file in `/available/`
2. Add entry to manifest.json
3. Assign unique ID (increment from highest)
4. Set appropriate priority and impact scores

## Directory Structure
```
/coordination/
  manifest.json              # Source of truth for queue state
  README.md                  # This file
  /available/                # Prompts ready to claim
  /claimed/                  # Work in progress
  /complete/                 # Finished work
  /blocked/                  # Waiting on dependencies
```

## Manifest Schema
```json
{
  "id": "001",                       // Unique identifier
  "title": "Brief description",      // What the work is
  "file": "path/to/prompt.md",       // Full prompt details
  "status": "available",              // available|claimed|complete|blocked
  "priority": "P1",                   // P0 (urgent) to P3 (nice to have)
  "impact_score": 8,                  // 1-10 scale of importance
  "estimated_minutes": 60,            // Time estimate
  "max_claim_duration": 180,          // Timeout in minutes
  "dependencies": ["002"],            // IDs of prompts that must complete first
  "skills_required": ["python"],      // Required capabilities
  "claimed_by": "session-xyz",        // Who claimed it (when claimed)
  "claimed_at": "timestamp",          // When claimed
  "completed_at": "timestamp",        // When completed
  "verification": "passed"            // Verification status
}
```

## Timeout Policy
If a prompt is claimed but not completed within `max_claim_duration`:
- Status automatically reverts to "available"
- Agent should check if their claim is still valid before marking complete
- If you need more time, update the claim timestamp

## Priority Guidelines
- **P0**: Blocks other work, urgent production issue
- **P1**: High impact, should be done soon
- **P2**: Important but not urgent
- **P3**: Nice to have, can wait

## Questions?
If unclear about a prompt, don't guess:
1. Check resources section for context
2. Look for related completed prompts
3. Ask for clarification in session log
4. If still blocked, mark as blocked with clear reason

---

*System launched: November 29, 2025*
*Maintainer: PM (xian) with architectural oversight*
