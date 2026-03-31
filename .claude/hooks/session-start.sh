#!/usr/bin/env bash
# session-start.sh — Enhanced SessionStart hook for Piper Morgan (#853)
#
# Performs four checks at agent session start:
#   1. Session log continuity (find today's log, warn if resuming)
#   2. Mailbox check (count unread messages)
#   3. Briefing freshness (warn if BRIEFING-CURRENT-STATE.md > 7 days old)
#   4. Role identity injection
#
# Token budget: Total stdout must stay under 500 characters.
# Safety: Must NEVER exit non-zero (exit 2 blocks agent start).

set -uo pipefail

# Project root — resolve relative to this script's location
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

output=""

# ─── 1. Session Log Continuity ────────────────────────────────────────────────
TODAY=$(date +%Y-%m-%d)
YEAR=$(date +%Y)
MONTH=$(date +%m)
DAY=$(date +%d)
LOG_DIR="$PROJECT_ROOT/dev/$YEAR/$MONTH/$DAY"

if [ -d "$LOG_DIR" ]; then
    # Look for today's lead session log
    EXISTING_LOG=$(find "$LOG_DIR" -name "*lead*opus*log*" -type f 2>/dev/null | head -1)
    if [ -n "$EXISTING_LOG" ]; then
        LOG_NAME=$(basename "$EXISTING_LOG")
        output+="SESSION LOG: $LOG_NAME exists — RESUME it, do not create new."$'\n'
    fi
fi

# ─── 2. Mailbox Check ────────────────────────────────────────────────────────
INBOX_DIR="$PROJECT_ROOT/mailboxes/lead/inbox"

if [ -d "$INBOX_DIR" ]; then
    # Count non-hidden, non-MANIFEST files
    UNREAD=$(find "$INBOX_DIR" -maxdepth 1 -type f ! -name '.*' ! -name 'MANIFEST.md' 2>/dev/null | wc -l | tr -d ' ')
    if [ "$UNREAD" -gt 0 ]; then
        FILES=$(find "$INBOX_DIR" -maxdepth 1 -type f ! -name '.*' ! -name 'MANIFEST.md' -exec basename {} \; 2>/dev/null | head -3 | tr '\n' ', ' | sed 's/,$//')
        output+="MAILBOX: $UNREAD unread — $FILES"$'\n'
    else
        output+="MAILBOX: empty"$'\n'
    fi
else
    output+="MAILBOX: empty"$'\n'
fi

# ─── 3. Briefing Freshness ───────────────────────────────────────────────────
BRIEFING="$PROJECT_ROOT/docs/briefing/BRIEFING-CURRENT-STATE.md"

if [ -f "$BRIEFING" ]; then
    # Get file age in days (macOS and Linux compatible)
    if stat -f %m "$BRIEFING" >/dev/null 2>&1; then
        # macOS
        MOD_EPOCH=$(stat -f %m "$BRIEFING")
    else
        # Linux
        MOD_EPOCH=$(stat -c %Y "$BRIEFING")
    fi
    NOW_EPOCH=$(date +%s)
    AGE_DAYS=$(( (NOW_EPOCH - MOD_EPOCH) / 86400 ))

    if [ "$AGE_DAYS" -gt 7 ]; then
        MOD_DATE=$(date -r "$MOD_EPOCH" +%Y-%m-%d 2>/dev/null || date -d "@$MOD_EPOCH" +%Y-%m-%d 2>/dev/null || echo "unknown")
        output+="BRIEFING: STALE ($AGE_DAYS days old, last updated $MOD_DATE)"$'\n'
    fi
fi

# ─── 4. Cross-Pollination Brief ──────────────────────────────────────────────
XPOLL_BRIEF="$PROJECT_ROOT/docs/briefs/cross-pollination/current.md"

if [ -f "$XPOLL_BRIEF" ]; then
    NOW_EPOCH=$(date +%s)
    if stat -f %m "$XPOLL_BRIEF" >/dev/null 2>&1; then
        BRIEF_EPOCH=$(stat -f %m "$XPOLL_BRIEF")
    else
        BRIEF_EPOCH=$(stat -c %Y "$XPOLL_BRIEF")
    fi
    BRIEF_AGE=$(( (NOW_EPOCH - BRIEF_EPOCH) / 86400 ))
    if [ "$BRIEF_AGE" -gt 2 ]; then
        output+="XPOLL BRIEF: STALE ($BRIEF_AGE days)"$'\n'
    else
        output+="XPOLL BRIEF: current.md available"$'\n'
    fi
else
    output+="XPOLL BRIEF: not found"$'\n'
fi

# ─── 5. Role Identity ────────────────────────────────────────────────────────
# Default role for this project
output+="ROLE: Lead Developer (see CLAUDE.md)"$'\n'

# ─── Output ───────────────────────────────────────────────────────────────────
if [ -n "$output" ]; then
    # Truncate to stay under 500 chars
    if [ ${#output} -gt 490 ]; then
        output="${output:0:480}... (truncated)"
    fi
    echo "$output"
fi

exit 0
