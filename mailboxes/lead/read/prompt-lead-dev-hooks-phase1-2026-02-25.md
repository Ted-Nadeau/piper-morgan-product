# Assignment: Claude Hooks Phase 1 — Enhanced SessionStart

**To**: Lead Developer
**From**: CIO (via PM)
**Date**: February 25, 2026
**Priority**: Standard (non-blocking, high-value infrastructure)
**Estimated Effort**: 1-2 hours
**GitHub Issue**: TBD (create before starting)

---

## Context

We currently have a minimal echo-only SessionStart hook in `.claude/settings.json`. The CIO approved expanding it to address three recurring agent failure modes that cost us time on nearly every multi-session day:

1. **Post-compaction context loss** — Agents create new session logs instead of resuming existing ones after context compaction
2. **Unchecked mailboxes** — Agents skip inbox reads despite the `check-mailbox` skill existing
3. **Stale briefings** — No mechanism alerts agents when BRIEFING-CURRENT-STATE.md is outdated

These are all problems we've documented repeatedly in session logs and omnibus entries. Hooks solve them deterministically — unlike CLAUDE.md instructions, hooks *always* execute.

---

## Task

Replace the current echo-only SessionStart hook with a shell script that performs four checks and injects concise context into the agent's session.

### What the Script Should Do

**1. Session Log Continuity Check**
- Look for an existing session log matching today's date in the standard log locations (`dev/` tree)
- If found: inject the log path so the agent can resume it
- If this appears to be a post-compaction resume (check for signals like the session already being underway): warn explicitly that a log already exists and should be continued, not replaced

**2. Mailbox Check**
- Count unread messages in the agent's mailbox directory (the `mailboxes/` tree)
- If unread messages exist: inject the count and list filenames
- If no unread messages: inject "Mailbox: empty" (one line, minimal tokens)

**3. Briefing Freshness Check**
- Check the modification date of `docs/briefing/BRIEFING-CURRENT-STATE.md`
- If older than 7 days: inject a warning with the last-modified date
- If current: inject nothing (no noise for a non-problem)

**4. Role Identity Injection**
- If a role identifier is detectable from the session context (e.g., from the initial prompt or a `.claude/` config): inject a one-line role reminder
- If not detectable: skip silently (don't inject noise)

### Where It Lives

- **Script**: `.claude/hooks/session-start.sh`
- **Configuration**: Update the existing hook entry in `.claude/settings.json` to point to the new script
- **Both files committed to git** (project-level, shared)

---

## Constraints

**Token budget**: Total stdout output from the hook must not exceed **500 characters**. Hooks inject into Claude's context window — verbose output wastes tokens. If any check produces output longer than its share, truncate with "... (see file for details)" and write the full output to a temp file the agent can optionally read.

**Failure mode**: The script must **never fail with a non-zero exit code** unless something is genuinely dangerous. A missing mailbox directory, a missing briefing file, or inability to detect role should all result in silent skips, not errors. Exit code 2 blocks the triggering action — we don't want a broken hook preventing agents from starting.

**No dependencies**: The script should use standard bash utilities only (find, stat, ls, wc, date). No Python, no npm, no external tools. This must work on any machine with bash.

**Fallback documentation**: Add a brief section to CLAUDE.md (or the appropriate agent onboarding doc) noting what these hooks do and what agents should do manually if hooks don't fire (e.g., in non-Claude-Code environments). The hooks are a safety net, not a replacement for protocol awareness.

---

## Verification Checklist

Before marking complete:

- [ ] Script created at `.claude/hooks/session-start.sh` and is executable
- [ ] `.claude/settings.json` updated to reference new script
- [ ] Script handles all four checks (log continuity, mailbox, briefing freshness, role identity)
- [ ] Total stdout stays under 500 characters in all tested scenarios
- [ ] Script exits cleanly (exit 0) even when mailbox/briefing/log directories don't exist
- [ ] Tested manually: run the script from project root and verify output is concise and correct
- [ ] Tested edge case: run with no existing session log (should not warn about resuming)
- [ ] Tested edge case: run with a stale BRIEFING-CURRENT-STATE.md (should warn)
- [ ] Fallback behavior documented
- [ ] Committed with descriptive message
- [ ] GitHub issue updated with evidence

---

## What This Is NOT

- **Not a replacement for CLAUDE.md progressive loading** — hooks handle critical-path items agents skip; CLAUDE.md handles detailed protocols
- **Not Phase 2 or 3** — no PreToolUse guards, no Stop hooks, no prompt-type hooks. Just the SessionStart enhancement.
- **Not a Dex clone** — we're cherry-picking one proven pattern, not rebuilding our infrastructure

---

## Reference

- **Spec Agent evaluation memo**: `memo-spec-to-cio-claude-hooks-evaluation-2026-02-16.md` (attached or in CIO mailbox)
- **CIO approval**: Feb 20, 2026 weekly memo
- **Existing hook**: Current echo-only hook in `.claude/settings.json`
- **Claude Hooks docs**: https://docs.anthropic.com/en/docs/claude-code (Hooks section)

---

*Assignment approved by CIO. Questions → PM or CIO.*
