# Settings Permissions Refactor Proposal
**Date**: December 1, 2025, 8:40 AM
**Issue**: 100+ specific bash commands cluttering settings.local.json
**Goal**: Simplify to wildcard patterns while maintaining safety

---

## Current State Analysis

**Problems**:
1. Lines 8-106: Individual bash commands accumulate over time
2. Many are one-off commands (timestamp-specific, curl with hardcoded IDs)
3. Hard to audit what's actually needed
4. File grows unbounded

**Safe Items** (Keep as-is):
- MCP server tools (serena, context7)
- Read/Write/Edit patterns for specific paths
- WebSearch, WebFetch with domain restrictions

---

## Proposed Refactor

### Option A: Conservative (Recommended)

Replace lines 8-106 with these categories:

```json
"allow": [
  // === Development Tools ===
  "Bash(git:*)",
  "Bash(gh:*)",
  "Bash(alembic:*)",
  "Bash(pytest:*)",
  "Bash(python:*)",
  "Bash(python3:*)",
  "Bash(python3.12:*)",
  "Bash(pip:*)",

  // === Build & Test Scripts ===
  "Bash(./scripts/*)",
  "Bash(.pre-commit-hooks/*)",
  "Bash(bd:*)",
  "Bash(./scripts/bd-safe:*)",

  // === Database ===
  "Bash(docker:*)",
  "Bash(psql:*)",

  // === System Utilities ===
  "Bash(ls:*)",
  "Bash(cat:*)",
  "Bash(echo:*)",
  "Bash(mkdir:*)",
  "Bash(cp:*)",
  "Bash(rm:*)",
  "Bash(chmod:*)",
  "Bash(ln:*)",
  "Bash(open:*)",
  "Bash(tee:*)",

  // === Process Management ===
  "Bash(pkill:*)",
  "Bash(pgrep:*)",
  "Bash(lsof:*)",
  "Bash(kill:*)",

  // === Shell Constructs ===
  "Bash(for:*)",
  "Bash(do:*)",
  "Bash(done:*)",
  "Bash(break:*)",
  "Bash(source:*)",

  // === Security ===
  "Bash(openssl:*)",

  // === Web Development ===
  "Bash(curl:*)",
  "Bash(brew:*)",

  // === Temporary Files ===
  "Bash(/tmp/*)",

  // === Python Environment ===
  "Bash(PYTHONPATH=*)",
  "Bash(export PYTHONPATH=*)",
  "Bash(export PATH=*)",

  // === Skip Pre-commit Hooks (for emergencies) ===
  "Bash(SKIP=*)",

  // === MCP Servers ===
  "mcp__serena__*",
  "mcp__context7__*",

  // === Web Tools ===
  "WebSearch",
  "WebFetch(domain:github.com)",
  "WebFetch(domain:steve-yegge.medium.com)",

  // === File Permissions ===
  "Read(/Users/xian/Development/**)",
  "Edit(src/**)",
  "Edit(**/*.py)",
  "Write(docs/**)",
  "Write(**/*.py)",
  "Read(/Users/xian/Downloads/**)",
  "Read(/tmp/**)",
  "Read(/private/tmp/**)",
  "Read(/Users/xian/Development/piper-morgan/.env*)",
  "Edit(/Users/xian/Development/piper-morgan/.env*)",
  "Write(/Users/xian/Development/piper-morgan/.env*)"
]
```

### Option B: Aggressive (More Permissive)

```json
"allow": [
  // === Development - Everything ===
  "Bash(*)",

  // === MCP Servers ===
  "mcp__serena__*",
  "mcp__context7__*",

  // === Web Tools ===
  "WebSearch",
  "WebFetch(*)",

  // === File Permissions ===
  "Read(/Users/xian/Development/**)",
  "Edit(/Users/xian/Development/**)",
  "Write(/Users/xian/Development/**)",
  "Read(/Users/xian/Downloads/**)",
  "Read(/tmp/**)",
  "Read(/private/tmp/**)"
]
```

### Option C: Hybrid (Balance Safety & Convenience)

Start with Option A, but add escape hatch:

```json
"defaultMode": "bypassPermissions"  // Already set!
```

**Note**: You already have `"defaultMode": "bypassPermissions"` on line 7, which means the `allow` list might not even be enforced strictly. This explains why you need to approve bash commands manually - the system is asking for confirmation despite bypass mode.

---

## Recommendation

**Choose Option A** because:
1. ✅ Maintains audit trail (know what commands are allowed)
2. ✅ Removes one-off clutter (timestamp-specific commands)
3. ✅ Easy to understand categories
4. ✅ Safer than full wildcard
5. ✅ Still allows necessary workflows

**Reduces**: 106 lines → ~60 lines (40% reduction)
**Maintains**: All necessary permissions
**Improves**: Readability and maintainability

---

## Implementation Steps

1. **Backup current settings**:
   ```bash
   cp .claude/settings.local.json .claude/settings.local.json.backup
   ```

2. **Apply Option A** (I can do this)

3. **Test workflows**:
   - Run pytest
   - Run git commands
   - Run bd commands
   - Test setup wizard
   - Test start/stop scripts

4. **If issues**: Revert from backup, add missing patterns

5. **Clean up backup** after 1 week of successful usage

---

## Questions for PM

1. **Which option do you prefer?** (A/B/C)
2. **Do you want to keep `defaultMode: "bypassPermissions"`?**
   - If yes: The `allow` list is just documentation
   - If no: Need to be more careful with wildcards
3. **Any specific commands you want individually listed?** (security-sensitive operations)

---

## Safe to Remove (One-off Commands)

These were added for specific one-time tasks and can be deleted:

- `Bash(TIMESTAMP=20251109_130557:*)` - Specific date
- `Bash(/tmp/backup_$TIMESTAMP_user_tables.sql)` - One-time backup
- `Bash(for line in 145 154 163 188 198 221 244 267 279 303)` - Specific line numbers
- `Bash(do curl -s -X POST 'http://localhost:8001/api/v1/learning/patterns/57ef5268-b496-4f8f-9586-dcb91dae54c1/feedback'...)` - Hardcoded UUID
- `Bash(/tmp/issue-400-body.txt)` - Specific temp file
- `Bash(/tmp/issue-407-body.txt)` - Specific temp file
- `Bash(Multi-step procedure for architecture review emails.)` - Not even a command?

---

## Next Steps

**After you decide on option**:
1. I'll apply the refactor
2. You reload Claude Code (end/rejoin chat)
3. We test with Pattern B implementation
4. Adjust if needed

Ready when you are!
