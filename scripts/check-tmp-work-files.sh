#!/bin/bash
# Pre-commit hook: Detect work files in /tmp that should be in dev/active/
# Prevents loss of reports, verification, analysis documents

TMP_PATTERNS=(
    "*report*.md"
    "*verification*.md"
    "*analysis*.md"
    "*evidence*.md"
    "*findings*.md"
    "*summary*.md"
    "*issue*.md"
    "*sprint*.md"
)

FOUND_FILES=()

for pattern in "${TMP_PATTERNS[@]}"; do
    while IFS= read -r file; do
        if [[ ! -z "$file" && -f "$file" ]]; then
            FOUND_FILES+=("$file")
        fi
    done < <(find /tmp -maxdepth 1 -type f -name "$pattern" 2>/dev/null)
done

if [ ${#FOUND_FILES[@]} -gt 0 ]; then
    cat >&2 << 'WARN'

╔════════════════════════════════════════════════════════════════════════════╗
║ 🚨 WORK FILES DETECTED IN /tmp (EPHEMERAL STORAGE - WILL BE LOST!)        ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║ These work products are in temporary storage and will be garbage collected:║
║                                                                            ║
WARN

    for file in "${FOUND_FILES[@]}"; do
        printf "║   %-76s ║\n" "$(basename "$file") ($(stat -f%z "$file" 2>/dev/null | awk '{if ($1>1048576) printf "%.1fM", $1/1048576; else if ($1>1024) printf "%.1fK", $1/1024; else printf "%dB", $1}'))" >&2
    done

    cat >&2 << 'WARN'
║                                                                            ║
║ 🔧 REQUIRED ACTIONS (prevents commit):                                    ║
║   1. cp /tmp/filename.md dev/active/  (save your work)                   ║
║   2. git add dev/active/filename.md                                       ║
║   3. Run 'git commit' again                                               ║
║                                                                            ║
║ ℹ️  PREVENTION:                                                            ║
║   Always output work to dev/active/ not /tmp                              ║
║   dev/active/ is committed to Git and preserved                           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

WARN
    exit 1
fi

exit 0
