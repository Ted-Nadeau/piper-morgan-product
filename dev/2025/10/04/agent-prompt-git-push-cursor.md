# Cursor Agent Prompt: GREAT-3C Git Push

## Mission
**Git Push**: Push committed GREAT-3C work to origin/main.

## Context

**Code Agent** will commit all GREAT-3C work.

**Your Task**: Push the commit to remote after Code completes.

## Your Steps

### Step 1: Verify Commit Exists

```bash
cd ~/Development/piper-morgan

# Check latest commit
git log -1 --oneline

# Should see GREAT-3C commit from Code agent
```

### Step 2: Push to Remote

```bash
# Push to origin/main
git push origin main
```

### Step 3: Verify Push

```bash
# Check remote status
git status

# Should say "Your branch is up to date with 'origin/main'"
```

### Step 4: Document Push

Record:
- Push timestamp
- Commit hash pushed
- Any warnings or messages

## Deliverable

Create: `dev/2025/10/04/git-push-cursor.md`

Include:
1. **Commit Pushed**: Hash and message summary
2. **Push Status**: Success/warnings
3. **Remote Verification**: Branch status
4. **Timestamp**: When pushed

## Success Criteria
- [ ] Commit verified
- [ ] Push successful
- [ ] Remote updated
- [ ] Status clean

---

**Deploy AFTER Code agent completes commit**
**Wait for PM's signal to deploy**
