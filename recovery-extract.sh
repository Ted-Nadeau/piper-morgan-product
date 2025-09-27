#!/bin/bash

# Recovery script for stash commit 48a7a36d51f67b0e6c9ad0b6cfe6d07f168664a8
STASH_COMMIT="48a7a36d51f67b0e6c9ad0b6cfe6d07f168664a8"
RECOVERY_DIR="recovery-workspace"

echo "🔄 Extracting all lost files from stash commit $STASH_COMMIT"
echo "📁 Recovery directory: $RECOVERY_DIR"

# Create recovery directory structure
mkdir -p "$RECOVERY_DIR"/{dev,docs,knowledge,scripts,tests}

# Extract key methodology files
echo "📋 Extracting methodology files..."
git show "$STASH_COMMIT:dev/2025/09/21/AGENTS.md" > "$RECOVERY_DIR/AGENTS.md" 2>/dev/null
git show "$STASH_COMMIT:dev/2025/09/21/CLAUDE.md" > "$RECOVERY_DIR/CLAUDE-sept21.md" 2>/dev/null
git show "$STASH_COMMIT:dev/2025/09/21/MINIMAL-PROJECT-INSTRUCTIONS.md" > "$RECOVERY_DIR/MINIMAL-PROJECT-INSTRUCTIONS.md" 2>/dev/null

# Extract all Sept 22-24 session logs and work
echo "📝 Extracting session logs Sept 22..."
mkdir -p "$RECOVERY_DIR/dev/2025/09/22"
git show "$STASH_COMMIT:dev/2025/09/22/CORE-GREAT-1A-issue.md" > "$RECOVERY_DIR/dev/2025/09/22/CORE-GREAT-1A-issue.md" 2>/dev/null
git show "$STASH_COMMIT:dev/2025/09/22/CORE-GREAT-1B-issue.md" > "$RECOVERY_DIR/dev/2025/09/22/CORE-GREAT-1B-issue.md" 2>/dev/null
git show "$STASH_COMMIT:dev/2025/09/22/CORE-GREAT-1C-issue.md" > "$RECOVERY_DIR/dev/2025/09/22/CORE-GREAT-1C-issue.md" 2>/dev/null
git show "$STASH_COMMIT:dev/2025/09/22/gameplan-GREAT-1A.md" > "$RECOVERY_DIR/dev/2025/09/22/gameplan-GREAT-1A.md" 2>/dev/null
git show "$STASH_COMMIT:dev/2025/09/22/methodology-improvements-comprehensive.md" > "$RECOVERY_DIR/dev/2025/09/22/methodology-improvements-comprehensive.md" 2>/dev/null

echo "📝 Extracting session logs Sept 23..."
mkdir -p "$RECOVERY_DIR/dev/2025/09/23"
git show "$STASH_COMMIT:dev/2025/09/23/GREAT-1C-COMPLETION-issue.md" > "$RECOVERY_DIR/dev/2025/09/23/GREAT-1C-COMPLETION-issue.md" 2>/dev/null
git show "$STASH_COMMIT:dev/2025/09/23/chief-architect-eod-report-sept23.md" > "$RECOVERY_DIR/dev/2025/09/23/chief-architect-eod-report-sept23.md" 2>/dev/null
git show "$STASH_COMMIT:dev/2025/09/23/gameplan-GREAT-1C-evidence.md" > "$RECOVERY_DIR/dev/2025/09/23/gameplan-GREAT-1C-evidence.md" 2>/dev/null

echo "📝 Extracting session logs Sept 24..."
mkdir -p "$RECOVERY_DIR/dev/2025/09/24"
git show "$STASH_COMMIT:dev/2025/09/24/gameplan-llm-regression-fix.md" > "$RECOVERY_DIR/dev/2025/09/24/gameplan-llm-regression-fix.md" 2>/dev/null

echo "📚 Extracting knowledge base files..."
mkdir -p "$RECOVERY_DIR/knowledge/versions"
git show "$STASH_COMMIT:knowledge/CLAUDE.md" > "$RECOVERY_DIR/knowledge/CLAUDE.md" 2>/dev/null
git show "$STASH_COMMIT:knowledge/agent-prompt-template.md" > "$RECOVERY_DIR/knowledge/agent-prompt-template.md" 2>/dev/null
git show "$STASH_COMMIT:knowledge/gameplan-template.md" > "$RECOVERY_DIR/knowledge/gameplan-template.md" 2>/dev/null

echo "🧪 Extracting test infrastructure..."
mkdir -p "$RECOVERY_DIR/tests/mocks" "$RECOVERY_DIR/tests/utils"
git show "$STASH_COMMIT:tests/mocks/__init__.py" > "$RECOVERY_DIR/tests/mocks/__init__.py" 2>/dev/null
git show "$STASH_COMMIT:tests/mocks/mock_agents.py" > "$RECOVERY_DIR/tests/mocks/mock_agents.py" 2>/dev/null
git show "$STASH_COMMIT:tests/utils/__init__.py" > "$RECOVERY_DIR/tests/utils/__init__.py" 2>/dev/null
git show "$STASH_COMMIT:tests/utils/performance_monitor.py" > "$RECOVERY_DIR/tests/utils/performance_monitor.py" 2>/dev/null

echo "📊 Extracting scripts..."
git show "$STASH_COMMIT:scripts/check_coverage_locally.py" > "$RECOVERY_DIR/scripts/check_coverage_locally.py" 2>/dev/null
git show "$STASH_COMMIT:scripts/run_performance_tests.py" > "$RECOVERY_DIR/scripts/run_performance_tests.py" 2>/dev/null

echo "📋 Extracting omnibus logs..."
mkdir -p "$RECOVERY_DIR/docs/omnibus-logs"
git show "$STASH_COMMIT:docs/omnibus-logs/2025-09-19-omnibus-log.md" > "$RECOVERY_DIR/docs/omnibus-logs/2025-09-19-omnibus-log.md" 2>/dev/null
git show "$STASH_COMMIT:docs/omnibus-logs/2025-09-20-omnibus-log.md" > "$RECOVERY_DIR/docs/omnibus-logs/2025-09-20-omnibus-log.md" 2>/dev/null
git show "$STASH_COMMIT:docs/omnibus-logs/2025-09-21-omnibus-log.md" > "$RECOVERY_DIR/docs/omnibus-logs/2025-09-21-omnibus-log.md" 2>/dev/null
git show "$STASH_COMMIT:docs/omnibus-logs/2025-09-22-omnibus-log.md" > "$RECOVERY_DIR/docs/omnibus-logs/2025-09-22-omnibus-log.md" 2>/dev/null
git show "$STASH_COMMIT:docs/omnibus-logs/2025-09-23-omnibus-log.md" > "$RECOVERY_DIR/docs/omnibus-logs/2025-09-23-omnibus-log.md" 2>/dev/null
git show "$STASH_COMMIT:docs/omnibus-logs/2025-09-24-omnibus-log.md" > "$RECOVERY_DIR/docs/omnibus-logs/2025-09-24-omnibus-log.md" 2>/dev/null

echo "✅ Recovery extraction complete!"
echo ""
echo "📁 All recovered files are in: $RECOVERY_DIR/"
echo "🔍 Key methodology files:"
echo "  - AGENTS.md"
echo "  - CLAUDE-sept21.md"
echo "  - MINIMAL-PROJECT-INSTRUCTIONS.md"
echo ""
echo "📊 Count of recovered files:"
find "$RECOVERY_DIR" -type f -name "*.md" | wc -l | tr -d ' ' | sed 's/$/ markdown files/'
find "$RECOVERY_DIR" -type f -name "*.py" | wc -l | tr -d ' ' | sed 's/$/ python files/'
echo ""
echo "You can now review and selectively restore what you need!"