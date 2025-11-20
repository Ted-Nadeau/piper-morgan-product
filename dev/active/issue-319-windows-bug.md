# BUG-319: Windows Git Clone Fails - Illegal Character in Filename
**Priority**: P0 (Blocks Windows developers)
**Labels**: `bug`, `windows`, `quick-win`, `good-first-issue`
**Effort**: 2-3 hours
**Discovered by**: Ted Nadeau (architectural review)

---

## Problem

Repository cannot be cloned on Windows due to colon (`:`) in filename:
```
error: invalid path 'archive/piper-morgan-0.1.1/docs/claude docs 5:30/conversational_refactor.md'
```

Colons are illegal in Windows filenames (MS-DOS heritage).

## Impact

- Windows developers cannot clone repository
- Blocks Windows-based testing
- Prevents Windows contributors
- Violates cross-platform support goal

## Root Cause

Early development file created on macOS/Linux with timestamp in filename.

## Solution

1. **Immediate**: Rename problematic file(s)
2. **Prevention**: Add pre-commit hook to detect Windows-incompatible filenames
3. **Validation**: Test clone on Windows VM

## Acceptance Criteria

- [ ] Identify all files with Windows-illegal characters (`:`, `*`, `?`, `"`, `<`, `>`, `|`)
- [ ] Rename files to remove illegal characters
- [ ] Add `.githooks/pre-commit` script checking for Windows compatibility
- [ ] Document Windows compatibility in CONTRIBUTING.md
- [ ] Successfully clone repository on Windows 10/11
- [ ] Successfully clone repository in Git Bash
- [ ] No regression on macOS/Linux

## Implementation Steps

```bash
# 1. Find problematic files
find . -name "*:*" -o -name "*\**" -o -name "*?*"

# 2. Rename (example)
git mv "archive/piper-morgan-0.1.1/docs/claude docs 5:30/conversational_refactor.md" \
      "archive/piper-morgan-0.1.1/docs/claude-docs-0530/conversational_refactor.md"

# 3. Create pre-commit hook
#!/bin/bash
# .githooks/pre-commit
# Check for Windows-incompatible filenames
git diff --cached --name-only | while read file; do
  if echo "$file" | grep -E '[:<>"|?*]'; then
    echo "ERROR: Filename contains Windows-illegal character: $file"
    exit 1
  fi
done
```

## Testing

1. Clone on Windows 10 (native)
2. Clone on Windows 11 (native)
3. Clone in WSL
4. Clone in Git Bash
5. Verify pre-commit hook prevents bad filenames

---

*Quick win: 2-3 hours to unblock all Windows developers*
