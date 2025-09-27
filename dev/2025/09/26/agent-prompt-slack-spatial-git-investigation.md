# Claude Code Agent Prompt: Slack Spatial Intelligence Git Investigation

## Your Identity
You are Claude Code Agent, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Mission: Git Commit Analysis for Lost Slack Spatial Work
**Objective**: Investigate July 28-29, 2025 commits to determine if Slack spatial intelligence work was completed but subsequently lost or regressed.

## Context from Lead Developer
- PM recalls Slack spatial integration work done July 28-29 (with debugging on July 29)
- Current investigation shows **no** `slack_spatial.py` in `/services/integrations/spatial/`
- Slack integration successfully triggers Piper workflows from company Slack instance
- **Question**: Was spatial intelligence work completed but lost, or was PM's impression incorrect?

## Investigation Tasks

### 1. Git History Analysis
```bash
# Look for commits around July 28-29, 2025
git log --oneline --since="2025-07-27" --until="2025-07-30" --grep="slack"
git log --oneline --since="2025-07-27" --until="2025-07-30" --grep="spatial"
git log --oneline --since="2025-07-27" --until="2025-07-30" --all

# Check for file additions/deletions
git log --name-status --since="2025-07-27" --until="2025-07-30" | grep -i slack
git log --name-status --since="2025-07-27" --until="2025-07-30" | grep -i spatial
```

### 2. File History Investigation
```bash
# Check if slack_spatial.py ever existed
git log --follow --all -- "**/slack_spatial.py" 
git log --follow --all -- "services/integrations/spatial/slack_spatial.py"

# Look for any spatial + slack combinations
find . -name "*.py" -exec git log --follow {} \; | grep -A5 -B5 -i "slack.*spatial\|spatial.*slack"
```

### 3. Commit Content Analysis
For any July 28-29 commits found:
```bash
# Show full commit details
git show [commit-hash]

# Look for slack-related changes in spatial areas
git diff [commit-hash]~1 [commit-hash] -- services/integrations/spatial/
git diff [commit-hash]~1 [commit-hash] -- services/integrations/slack/
```

### 4. Stash and Merge Investigation
Given PM mentioned "Code flubbed a merge and undid some stashed work":
```bash
# Check recent stash activity
git stash list
git reflog --all | grep -i stash

# Look for merge commits that might have lost work
git log --merges --since="2025-07-20" --oneline
```

## Evidence Requirements

### For Each Finding, Provide:
1. **Commit hash and date**
2. **Commit message and author** 
3. **Files changed** (especially any spatial/slack related)
4. **Code snippets** showing spatial intelligence implementation
5. **Evidence of loss/regression** (if found)

### Expected Outcomes:
- **Scenario A**: Found evidence of Slack spatial work that was subsequently lost
- **Scenario B**: Found partial work that was incomplete 
- **Scenario C**: No evidence found (PM's impression was incorrect)
- **Scenario D**: Work exists but in different location/name

## Reporting Format

```markdown
# Slack Spatial Intelligence Git Investigation Results

## Executive Summary
[Was work found? Lost? Never completed?]

## Commit Analysis
### July 28, 2025
- [Commit details]

### July 29, 2025  
- [Commit details]

## File History Findings
[Evidence of slack_spatial.py or similar]

## Code Evidence
[Any actual spatial intelligence code found]

## Conclusion
[Assessment of what happened to the work]
```

## Success Criteria
- ✅ Complete git history searched for July 28-29
- ✅ Evidence provided for any claims
- ✅ Clear assessment of whether work was lost or never completed
- ✅ Specific file paths and commit hashes documented

## Critical Notes
- Focus on **evidence-based conclusions** only
- Document the investigation process clearly
- If work was lost, identify the specific point of loss
- Consider that work might be in unexpected locations

---

**Deploy immediately and report findings to Lead Developer for Chief Architect briefing.**
