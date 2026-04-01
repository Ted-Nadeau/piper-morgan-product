# Memo: Ted Nadeau GitHub Repository Permissions Investigation

**Date**: March 8, 2026
**Investigator**: Documentation Management Specialist
**Status**: Investigation only — no changes made

---

## Findings

### 1. Ted's Current Permission Level

**Ted Nadeau is not a collaborator on the repository.**

Only two accounts have access:
| Account | Role | Permissions |
|---------|------|-------------|
| `mediajunkie` (PM) | Admin | Full access |
| `piper-reviewer` | Write | Push, pull, triage (no admin/maintain) |

No pending invitations. No teams configured. Ted does not currently have push access.

### 2. Branch Protection on Main

**None.** Main is completely unprotected:
- No branch protection rules
- No rulesets (newer GitHub mechanism)
- `protected: false`

Anyone with write access can push directly to main without a PR.

### 3. Bypass Mechanisms

Not applicable — Ted isn't a collaborator. However, the `piper-reviewer` account has write access and could push directly to main with no protection to prevent it.

### 4. How Could Ted Have Pushed to Main?

If Ted pushed directly to main at some point, possible explanations:
- He was temporarily added as a collaborator and later removed
- He pushed via a fork (but the repo is public, and fork pushes to upstream require PR acceptance)
- He pushed using PM's credentials or a shared machine
- The push didn't actually happen (misremembered — the HOSR transcript from Mar 5 mentions Ted was on the wrong branch and having git confusion)

**Most likely**: Per the HOSR transcript, Ted had trouble with `git switch`/`git pull` and was on main instead of production. He may not have actually pushed — just been working on the wrong local branch.

---

## Options (If PM Wants to Add Ted as Collaborator)

### Option A: Add Ted with Write access, no branch protection
- Simplest. Same as current `piper-reviewer` setup.
- Risk: Anyone with write can push directly to main.

### Option B: Add Ted with Write access + enable branch protection on main
- Require PRs for all pushes to main
- Can exempt PM (`mediajunkie`) via "allow specified actors to bypass"
- Requires GitHub Free plan minimum (branch protection is available on free public repos)
- **Recommended if enforcing PR workflow**

### Option C: Add Ted with Triage access only (read + issue management)
- Ted can file issues, comment, manage labels — but cannot push code
- Would need to fork and submit PRs for any code contributions
- Most restrictive; appropriate if Ted's contributions are primarily advisory

### Option D: Don't add Ted — use fork-and-PR workflow
- Ted forks the repo, pushes to his fork, submits PRs
- PM reviews and merges
- No permissions change needed
- Natural for public repo collaboration

---

## Recommendation

The repo currently has **zero branch protection**, which means `piper-reviewer` (and any future collaborator with write access) can push directly to main. Regardless of Ted's situation, **enabling branch protection on main with PM bypass** (Option B) would be good hygiene. This is a separate decision from Ted's access level.

For Ted specifically, Option C (Triage) or Option D (fork-and-PR) seem most aligned with his current role as alpha tester and methodology advisor rather than active code contributor.

---

*Investigation only — no changes made to repository settings.*
