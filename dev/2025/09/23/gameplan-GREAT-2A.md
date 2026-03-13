# Gameplan: CORE-GREAT-2A - Dual Pattern Discovery & Documentation

**Date**: September 23, 2025
**Issue**: #[TBD] (Part 1 of 3 for CORE-GREAT-2 epic #181)
**Architect**: Claude Opus 4.1
**Lead Developer**: [To be assigned]

---

## Strategic Context: Integration Cleanup Phase

### Where We Are
CORE-GREAT-1 complete - QueryRouter resurrected and locked. Now addressing technical debt from incomplete pattern migrations.

### This Epic's Structure
CORE-GREAT-2 decomposed into three sequential issues:
- **#[TBD] GREAT-2A**: Discovery & Documentation (THIS GAMEPLAN)
- **#[TBD] GREAT-2B**: Service Pattern Cleanup
- **#[TBD] GREAT-2C**: Documentation & Locks

**Critical**: Must understand ALL dual patterns before removing any (Inchworm Protocol).

---

## Infrastructure Verification Checkpoint

### My Understanding (Based on GREAT-1 findings)
```yaml
Expected Structure:
- Services: services/ directory with domain-driven design
- Old patterns: Direct service instantiation
- New patterns: Through OrchestrationEngine
- Config: config/PIPER.user.md (mixed with system config)
- Documentation: docs/ with various .md files
- ADRs: docs/internal/architecture/current/adrs/
```

### PM Verification Required
Before agents begin, please verify:
```bash
# Check service structure
ls -la services/
find services/ -name "*service*.py" | head -20

# Look for dual patterns (preliminary)
grep -r "GitHubService\|github_service" . --include="*.py" | head -10

# Verify ADR locations
ls -la docs/internal/architecture/current/adrs/ | grep -E "005|006|027|030"

# Check for pattern detection scripts
ls -la scripts/ | grep -i pattern
find . -name "*detect*pattern*.py" 2>/dev/null
```

**Expected**: Multiple patterns exist, ADRs describe intended state, no detection scripts yet.

---

## The Investigation Mission

**Goal**: Complete forensic analysis of all dual patterns before any cleanup.

**Why This Matters**:
- Can't safely remove what we don't fully understand
- ADRs may not reflect actual implementation (75% pattern)
- Need to know which code depends on which pattern

---

## Phase 0: GitHub & ADR Investigation

### Both Agents Together
1. **Verify Issue Exists**
   ```bash
   gh issue view [2A issue number]
   ```

2. **Review Critical ADRs**
   ```bash
   # Find and read the ADRs
   cat docs/internal/architecture/current/adrs/ADR-005-*.md
   cat docs/internal/architecture/current/adrs/ADR-006-*.md
   cat docs/internal/architecture/current/adrs/ADR-027-*.md
   cat docs/internal/architecture/current/adrs/ADR-030-*.md
   ```

3. **Document ADR Intent**
   Create summary of what SHOULD exist per ADRs

---

## Phase 1: Dual Pattern Discovery

### Deploy: Both Agents (Different Search Strategies)

#### Claude Code Instructions - Broad Pattern Search
```markdown
Investigate ALL service instantiation patterns:

1. Find every way GitHub service is called:
   - Direct instantiation: GitHubService()
   - Through orchestration: orchestration.github
   - Via import: from services.github import
   - CLI direct calls
   - Web endpoint calls

2. Repeat for Slack service

3. Repeat for Notion service

4. Create pattern frequency map:
   - Which pattern appears most?
   - Which files use which pattern?
   - Any patterns beyond dual (triple+)?

5. Search for configuration validation:
   - Where should it happen?
   - Where does it actually happen?
   - What's broken about it?

Deploy subagents if needed for parallel search.
Document EVERYTHING found, even if unclear.
```

#### Cursor Instructions - Targeted File Analysis
```markdown
Analyze specific service files for patterns:

1. In services/github_service.py:
   - How is it instantiated?
   - What patterns exist?
   - Which is "old" vs "new"?

2. In web/app.py:
   - How are services called?
   - Direct or through orchestration?

3. In cli/commands/:
   - How do CLI commands access services?
   - Do they bypass orchestration?

4. In services/orchestration/engine.py:
   - Which services are integrated?
   - Which are missing?

Document exact line numbers and patterns.
```

### Cross-Validation Point
Compare findings:
- Do both agents find same dual patterns?
- Any patterns one found that other missed?
- Agreement on old vs new classification?

---

## Phase 2: Documentation Link Analysis

### Deploy: Code for Broad Search, Cursor for Verification

#### Code Instructions - Find All Broken Links
```markdown
Search for all documentation links:
1. Find all .md files
2. Extract all links (http, relative paths, anchors)
3. Test each link
4. Report all 28 (or more?) broken ones
5. Categorize by type of break (404, moved, never existed)
```

#### Cursor Instructions - Verify Specific Breaks
```markdown
For each broken link Code finds:
1. Confirm it's actually broken
2. Try to find where it moved to
3. Check git history for when it broke
4. Document fix needed
```

---

## Phase 3: Pattern Usage Mapping

### Both Agents - Create Dependency Map

Goal: Understand what breaks if we remove old patterns

```markdown
For each dual pattern found:
1. List ALL files using old pattern
2. List ALL files using new pattern
3. Identify transition points (files using BOTH)
4. Flag high-risk removals
5. Estimate cleanup complexity
```

---

## Phase Z: Final Documentation & Handoff

### Evidence Compilation
- Complete dual pattern inventory
- ADR compliance assessment
- Broken link report with fixes
- Risk assessment for pattern removal
- Configuration validation gaps

### GitHub Update
```bash
gh issue edit [2A number] --body "
## Status: Complete - Awaiting PM Approval

### Patterns Discovered
- GitHub: [X old pattern files, Y new pattern files]
- Slack: [X old pattern files, Y new pattern files]
- Notion: [X old pattern files, Y new pattern files]

### Documentation Issues
- [28/X] broken links found and categorized
- Configuration validation gaps documented

### Risk Assessment
- High risk removals: [list]
- Safe removals: [list]
- Requires refactor: [list]

Ready for GREAT-2B pattern cleanup.
"
```

### Handoff to GREAT-2B
Document for cleanup phase:
- Exact patterns to remove
- Order of removal (safest first)
- Files requiring special attention
- Testing requirements

### PM Approval Request
```markdown
@xian - GREAT-2A Discovery complete:
- All dual patterns documented ✓
- ADR review complete ✓
- Broken links identified ✓
- Risk assessment done ✓

Ready to proceed to GREAT-2B cleanup.
```

---

## Success Criteria Checklist

- [ ] All GitHub dual patterns documented (PM will validate)
- [ ] All Slack dual patterns documented (PM will validate)
- [ ] All Notion dual patterns documented (PM will validate)
- [ ] Pattern usage map created (PM will validate)
- [ ] 28+ broken links found and categorized (PM will validate)
- [ ] Configuration validation gaps identified (PM will validate)
- [ ] ADR compliance assessed (PM will validate)
- [ ] Risk assessment complete (PM will validate)

---

## STOP Conditions

- If more than 2 patterns for any service (investigate why)
- If ADRs completely wrong about current state
- If pattern removal would break production
- If configuration validation more broken than expected
- If >50 broken links (bigger problem than thought)

---

## Evidence Requirements

- Pattern search results with line numbers
- File lists showing pattern usage
- Broken link report with categories
- ADR compliance notes
- Risk assessment document

---

## Remember

This is investigation only - NO CLEANUP YET. We need to understand the full scope before removing anything. The 75% pattern suggests ADRs might describe intent that was never completed.

---

*Discovery enables safe cleanup. Document everything.*
