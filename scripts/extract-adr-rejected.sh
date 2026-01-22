#!/bin/bash
# extract-adr-rejected.sh
# Extract rejected alternatives from ADRs
# Medium feasibility strategy (28% precision but highest volume) from Phase 2 experiment
#
# Usage: ./scripts/extract-adr-rejected.sh
# Example: ./scripts/extract-adr-rejected.sh

set -e

ADR_DIR="docs/internal/architecture/current/adrs/"
OUTPUT_FILE="dev/active/emergent-adr-candidates.md"

echo "# Emergent Anti-Pattern Candidates: ADR Rejected Alternatives"
echo ""
echo "**Generated**: $(date +%Y-%m-%d)"
echo "**Directory**: $ADR_DIR"
echo ""
echo "---"
echo ""

echo "## Rejected Options (❌ marker)"
echo ""
echo '```'
grep -rn "❌" "$ADR_DIR" --include="*.md" 2>/dev/null || echo "No ❌ markers found"
echo '```'
echo ""

echo "## 'Rejected Because' Sections"
echo ""
echo '```'
grep -rn -A 3 "[Rr]ejected [Bb]ecause\|[Rr]ejected:\|NOT [Cc]hosen" "$ADR_DIR" --include="*.md" 2>/dev/null || echo "No rejection sections found"
echo '```'
echo ""

echo "## 'Considered but' Language"
echo ""
echo '```'
grep -rn "[Cc]onsidered but\|[Dd]iscarded\|[Rr]uled out" "$ADR_DIR" --include="*.md" 2>/dev/null || echo "No 'considered but' language found"
echo '```'
echo ""

echo "## 'Why Not' Sections"
echo ""
echo '```'
grep -rn -B 1 -A 3 "[Ww]hy [Nn]ot\|[Ww]hy we didn't" "$ADR_DIR" --include="*.md" 2>/dev/null || echo "No 'why not' sections found"
echo '```'
echo ""

echo "---"
echo ""
echo "## Cross-Reference Check"
echo ""
echo "**Already Indexed ADR Anti-Patterns**:"
echo "- A-01: Dual repository (ADR-005)"
echo "- A-02: get_session() (ADR-006)"
echo "- A-03, A-04: Config patterns (ADR-010)"
echo "- A-05: Stored procedures (ADR-043)"
echo "- A-06, A-09: Shared database (ADR-040)"
echo "- A-07, A-08: LLM/Keyword matching (ADR-039)"
echo "- A-10: Thread-local injection (ADR-051)"
echo "- A-11: Verification theater (ADR-028)"
echo ""
echo "**Skip these ADRs** - already covered."
echo ""

echo "---"
echo ""
echo "## Classification Template"
echo ""
echo "| Candidate | ADR | Classification | Notes |"
echo "|-----------|-----|----------------|-------|"
echo "| [description] | [adr-xxx] | TRUE EMERGENT / VARIATION / FALSE POSITIVE | [notes] |"
echo ""
echo "---"
echo ""
echo "*Run classification manually, then update anti-pattern-index.md with TRUE EMERGENT entries*"
