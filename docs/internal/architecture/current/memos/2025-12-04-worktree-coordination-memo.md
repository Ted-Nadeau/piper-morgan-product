# Memo: Git Worktrees for Multi-Agent Coordination

**Date:** 2025-12-04
**From:** Special Assignments Agent (spec-code-opus)
**To:** Chief Architect, Lead Developer
**Re:** New git worktree infrastructure for agent isolation

---

## Summary

We've implemented a git worktree system that provides isolated working directories for agents working on coordination queue prompts. This eliminates context-switching overhead and prevents branch-related conflicts when multiple agents work in parallel.

## What's New

### Infrastructure

1. **`.trees/` directory** - Ignored by git, contains isolated worktrees
2. **Three shell scripts** in `scripts/`:
   - `worktree-setup.sh <prompt-id> <session-id>` - Creates isolated worktree
   - `worktree-teardown.sh <prompt-id>` - Cleans up (requires PM approval)
   - `worktree-status.sh` - Shows all active worktrees

3. **Schema extension** - `coordination/manifest.json` v1.1.0 adds:
   - `branch_name` - Git branch for the work
   - `worktree_path` - Path to isolated directory
   - `worktree_created_at` - Timestamp
   - `cleanup_approved` - PM must approve before teardown

### Workflow

```
1. Agent claims prompt:
   ./scripts/worktree-setup.sh 004 2025-12-04-0732-spec-code-opus

2. Agent works in isolated directory:
   cd .trees/004-073253/
   # All work happens here, isolated from other agents

3. Agent completes:
   - Commits and pushes to feature branch
   - Updates manifest status to "complete"

4. PM reviews and approves cleanup:
   - Sets cleanup_approved: true in manifest
   - Runs ./scripts/worktree-teardown.sh 004
```

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Naming | `.trees/<prompt-id>-<short-session>/` | Readable + unique |
| Cleanup | PM-controlled | Allows inspection before deletion |
| Enforcement | Advisory (warn, don't block) | Gauge adoption before strict |
| Implementation | Shell scripts first | Prove workflow before Python |

## Integration Points

### Existing Systems

| System | Integration | Status |
|--------|-------------|--------|
| Coordination Queue (`coordination/`) | Direct - manifest schema extended | Complete |
| MandatoryHandoffProtocol (`methodology/coordination/`) | Future - has `github_branch` field | Deferred to Phase 3-5 |
| EnforcementPatterns | Future - `worktree_isolation` rule | Deferred to Phase 3-5 |

### Future Work (GitHub #465)

Phase 3-5 will add Python integration:
- `WorktreeManager` class
- `worktree_isolation` enforcement rule
- Automatic PR creation on completion
- Integration with AgentCoordinator

## How to Use

### For Agents

When claiming coordination queue work:
```bash
# Instead of manual manifest updates, use:
./scripts/worktree-setup.sh <prompt-id> <your-session-id>

# Then work in the isolated directory
cd .trees/<prompt-id>-<session>/
```

### For PM

To check worktree status:
```bash
./scripts/worktree-status.sh
```

To approve cleanup after reviewing completed work:
1. Edit `coordination/manifest.json`
2. Set `cleanup_approved: true` for the prompt
3. Run `./scripts/worktree-teardown.sh <prompt-id>`

## Files Changed

- `.gitignore` - Added `.trees/` entry
- `.trees/README.md` - New documentation
- `scripts/worktree-setup.sh` - New script
- `scripts/worktree-teardown.sh` - New script
- `scripts/worktree-status.sh` - New script
- `coordination/manifest.json` - Schema v1.1.0
- `coordination/QUEUE-README.md` - Updated workflow docs

## GitHub Tracking

- Epic: #463 (FLY-COORD-TREES)
- Phase 0-2 (this work): #464
- Phase 3-5 (future): #465

## Questions?

See `coordination/QUEUE-README.md` for detailed workflow documentation or `.trees/README.md` for worktree-specific details.
