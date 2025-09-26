# Agent Prompt: Documentation Phase - TODO Comments Methodology Cleanup

**Agent**: Code  
**Mission**: Scan production codebase for TODO comments and ensure methodology compliance - all TODOs must have issue numbers or be removed/fixed.

## Context
- **GREAT-1C Documentation Phase**: Remove or update misleading TODO comments
- **Methodology requirement**: All TODOs must reference GitHub issue numbers
- **Scope**: Production codebase only (exclude docs/, archives/, dev/ working files)

## TODO Cleanup Tasks

### 1. Comprehensive TODO Comment Scan
```bash
# Scan production codebase for TODO comments (exclude docs/archives/dev)
echo "=== TODO Comments Scan - Production Codebase Only ==="

echo "Scanning for TODO comments in production code:"
find . -type f -name "*.py" \
  -not -path "./docs/*" \
  -not -path "./archives/*" \
  -not -path "./dev/*" \
  -not -path "./.git/*" \
  -not -path "./htmlcov/*" \
  -not -path "./.pytest_cache/*" \
  -exec grep -Hn -i "TODO" {} \; | head -50

echo ""
echo "TODO count by directory:"
for dir in services tests config web database scripts; do
    if [ -d "$dir" ]; then
        count=$(find "$dir" -name "*.py" -exec grep -l -i "TODO" {} \; 2>/dev/null | wc -l)
        total_todos=$(find "$dir" -name "*.py" -exec grep -i "TODO" {} \; 2>/dev/null | wc -l)
        echo "  $dir: $total_todos TODOs in $count files"
    fi
done
```

### 2. TODO Methodology Compliance Analysis
```bash
# Analyze TODO comments for methodology compliance
echo "=== TODO Methodology Compliance Analysis ==="

echo "Checking TODO format compliance (must have issue numbers):"

# Create temporary file for analysis
find . -type f -name "*.py" \
  -not -path "./docs/*" \
  -not -path "./archives/*" \
  -not -path "./dev/*" \
  -not -path "./.git/*" \
  -exec grep -Hn -i "TODO" {} \; > /tmp/todo_analysis.txt

echo ""
echo "=== COMPLIANT TODOs (have issue numbers) ==="
grep -E "TODO.*#[0-9]+|TODO.*issue.*[0-9]+|TODO.*PM-[0-9]+" /tmp/todo_analysis.txt | head -10

echo ""
echo "=== NON-COMPLIANT TODOs (missing issue numbers) ==="
grep -v -E "TODO.*#[0-9]+|TODO.*issue.*[0-9]+|TODO.*PM-[0-9]+" /tmp/todo_analysis.txt | head -20

echo ""
echo "Compliance statistics:"
total_todos=$(wc -l < /tmp/todo_analysis.txt)
compliant_todos=$(grep -E "TODO.*#[0-9]+|TODO.*issue.*[0-9]+|TODO.*PM-[0-9]+" /tmp/todo_analysis.txt | wc -l)
non_compliant=$((total_todos - compliant_todos))

echo "  Total TODOs found: $total_todos"
echo "  Compliant (have issue numbers): $compliant_todos"
echo "  Non-compliant (missing issue numbers): $non_compliant"
echo "  Compliance rate: $(( compliant_todos * 100 / (total_todos + 1) ))%"
```

### 3. Categorize TODO Comments for Action
```bash
# Categorize TODOs by action required
echo "=== TODO Categorization for Action ==="

echo "Analyzing non-compliant TODOs for appropriate action:"

# Process each non-compliant TODO
grep -v -E "TODO.*#[0-9]+|TODO.*issue.*[0-9]+|TODO.*PM-[0-9]+" /tmp/todo_analysis.txt | while IFS= read -r todo_line; do
    file=$(echo "$todo_line" | cut -d: -f1)
    line_num=$(echo "$todo_line" | cut -d: -f2)
    todo_text=$(echo "$todo_line" | cut -d: -f3-)
    
    echo ""
    echo "File: $file:$line_num"
    echo "TODO: $todo_text"
    
    # Show context around the TODO
    echo "Context:"
    sed -n "$((line_num-2)),$((line_num+2))p" "$file" 2>/dev/null | cat -n
    
    # Suggest action based on content
    case "$todo_text" in
        *"fix"*|*"bug"*|*"error"*|*"broken"*)
            echo "  → SUGGESTED ACTION: Create GitHub issue and reference"
            ;;
        *"implement"*|*"add"*|*"create"*)
            echo "  → SUGGESTED ACTION: Create GitHub issue for feature"
            ;;
        *"remove"*|*"delete"*|*"clean"*|*"cleanup"*)
            echo "  → SUGGESTED ACTION: Either do now or create cleanup issue"
            ;;
        *"refactor"*|*"improve"*|*"optimize"*)
            echo "  → SUGGESTED ACTION: Create technical debt issue"
            ;;
        *"test"*|*"testing"*)
            echo "  → SUGGESTED ACTION: Create testing improvement issue"
            ;;
        *)
            echo "  → SUGGESTED ACTION: Review - may need issue or removal"
            ;;
    esac
    
    echo "  ---"
done | head -100  # Limit output for readability
```

### 4. Identify TODOs for Immediate Action
```bash
# Find TODOs that can be resolved immediately
echo "=== TODOs for Immediate Resolution ==="

echo "Checking for TODOs that may be outdated or easily fixable:"

# Look for TODOs that might be obsolete
echo ""
echo "Potentially obsolete TODOs (check if already implemented):"
grep -i -E "TODO.*implement.*QueryRouter|TODO.*fix.*LLM|TODO.*add.*orchestration" /tmp/todo_analysis.txt | head -10

echo ""
echo "Simple cleanup TODOs:"
grep -i -E "TODO.*remove|TODO.*delete|TODO.*cleanup|TODO.*unused" /tmp/todo_analysis.txt | head -10

echo ""
echo "Documentation TODOs:"
grep -i -E "TODO.*document|TODO.*comment|TODO.*doc" /tmp/todo_analysis.txt | head -10
```

### 5. Generate TODO Cleanup Plan
```bash
# Generate specific cleanup actions
echo "=== TODO Cleanup Action Plan ==="

cat > /tmp/todo_cleanup_plan.md << 'EOF'
# TODO Cleanup Action Plan

## Summary
- Total TODOs found: [FROM ANALYSIS]
- Non-compliant TODOs: [FROM ANALYSIS]
- Action required: Update with issue numbers or remove

## Immediate Actions

### Category 1: Remove Obsolete TODOs
TODOs that reference completed work:
- [ ] QueryRouter implementation TODOs (if already implemented)
- [ ] LLM integration TODOs (if already working)
- [ ] Orchestration TODOs (if already functional)

### Category 2: Create GitHub Issues
TODOs requiring new issues:
- [ ] Bug fixes and error handling improvements
- [ ] Feature implementations and enhancements  
- [ ] Refactoring and optimization work
- [ ] Testing improvements

### Category 3: Convert to Proper TODO Format
Update existing TODOs with issue references:
```
# Before
TODO: Fix this error handling

# After  
TODO(#123): Fix this error handling
```

### Category 4: Immediate Simple Fixes
TODOs that can be resolved now:
- [ ] Remove unused imports/code
- [ ] Add missing docstrings
- [ ] Simple cleanup tasks

## Implementation Priority
1. Remove obsolete TODOs (quick wins)
2. Create issues for legitimate TODOs
3. Update TODO format with issue references
4. Verify no new non-compliant TODOs introduced
EOF

echo "TODO cleanup plan generated at /tmp/todo_cleanup_plan.md"
echo ""
cat /tmp/todo_cleanup_plan.md
```

### 6. Execute High-Priority TODO Cleanup
```bash
# Execute immediate TODO cleanup where possible
echo "=== Executing High-Priority TODO Cleanup ==="

echo "Looking for QueryRouter-related TODOs that may now be obsolete:"

# Check if QueryRouter TODOs are obsolete
queryrouter_todos=$(grep -i -E "TODO.*QueryRouter|TODO.*query.*router" /tmp/todo_analysis.txt)
if [ -n "$queryrouter_todos" ]; then
    echo "Found QueryRouter TODOs:"
    echo "$queryrouter_todos"
    echo ""
    echo "Checking if QueryRouter is now working..."
    
    # Test if QueryRouter is implemented and working
    PYTHONPATH=. python3 -c "
from services.orchestration.engine import OrchestrationEngine
from database.session import get_async_session
import asyncio

async def check_queryrouter():
    try:
        async with get_async_session() as session:
            engine = OrchestrationEngine(session)
            if hasattr(engine, 'query_router') and engine.query_router:
                print('✅ QueryRouter is implemented and working')
                print('Many QueryRouter TODOs may now be obsolete')
                return True
            else:
                print('❌ QueryRouter not found or not working')
                return False
    except Exception as e:
        print(f'❌ QueryRouter test failed: {e}')
        return False

working = asyncio.run(check_queryrouter())
" 2>/dev/null

else
    echo "No QueryRouter-specific TODOs found"
fi

echo ""
echo "Looking for simple cleanup opportunities:"

# Find import cleanup TODOs
grep -i "TODO.*import" /tmp/todo_analysis.txt | head -5

# Find comment/documentation TODOs
grep -i "TODO.*comment\|TODO.*doc" /tmp/todo_analysis.txt | head -5
```

### 7. TODO Cleanup Verification
```bash
# Verify TODO cleanup and generate final report
echo "=== TODO Cleanup Verification ==="

echo "Final TODO compliance check:"

# Re-scan after any cleanup
find . -type f -name "*.py" \
  -not -path "./docs/*" \
  -not -path "./archives/*" \
  -not -path "./dev/*" \
  -not -path "./.git/*" \
  -exec grep -Hn -i "TODO" {} \; > /tmp/todo_final.txt

final_total=$(wc -l < /tmp/todo_final.txt)
final_compliant=$(grep -E "TODO.*#[0-9]+|TODO.*issue.*[0-9]+|TODO.*PM-[0-9]+" /tmp/todo_final.txt | wc -l)
final_non_compliant=$((final_total - final_compliant))

echo "Final TODO status:"
echo "  Total TODOs: $final_total"
echo "  Compliant: $final_compliant"
echo "  Non-compliant: $final_non_compliant"
echo "  Compliance rate: $(( final_compliant * 100 / (final_total + 1) ))%"

if [ $final_non_compliant -eq 0 ]; then
    echo "🎉 All TODOs now comply with methodology!"
else
    echo "⚠️  $final_non_compliant TODOs still need attention"
    echo ""
    echo "Remaining non-compliant TODOs:"
    grep -v -E "TODO.*#[0-9]+|TODO.*issue.*[0-9]+|TODO.*PM-[0-9]+" /tmp/todo_final.txt | head -10
fi
```

## Evidence Collection Requirements

### TODO Scan Results
```
=== TODO Methodology Compliance Results ===
Total TODOs found: [X] in production codebase
Compliant (with issue numbers): [X]
Non-compliant (missing issue numbers): [X]
Compliance rate: [X]%

Distribution by directory:
- services/: [X] TODOs
- tests/: [X] TODOs  
- config/: [X] TODOs
- web/: [X] TODOs
- database/: [X] TODOs
- scripts/: [X] TODOs
```

### Cleanup Actions Taken
```
=== TODO Cleanup Actions ===
Obsolete TODOs removed: [X]
TODOs updated with issue references: [X]
GitHub issues created: [X] 
Simple fixes completed: [X]

Categories addressed:
- QueryRouter TODOs: [OBSOLETE/UPDATED/STILL_RELEVANT]
- Bug fix TODOs: [ISSUE_CREATED/REMOVED/FIXED]
- Feature TODOs: [ISSUE_CREATED/REMOVED/IMPLEMENTED]
- Cleanup TODOs: [COMPLETED/ISSUE_CREATED]
```

### Final Compliance Status
```
=== Final TODO Compliance Status ===
Before cleanup: [X]% compliance
After cleanup: [X]% compliance
Improvement: [X] percentage points

Remaining work needed: [NONE/list specific issues]
Ready for Documentation Phase completion: [YES/NO]
```

## Success Criteria
- [ ] Complete scan of production codebase TODO comments
- [ ] Analysis of methodology compliance (issue number requirements)
- [ ] Categorization of TODOs by required action
- [ ] Removal of obsolete TODOs (especially QueryRouter-related)
- [ ] Creation of GitHub issues for legitimate TODOs
- [ ] Update of TODO format with proper issue references
- [ ] Verification of improved compliance rate
- [ ] Documentation Phase checkbox ready to check

## Time Estimate
30-40 minutes for comprehensive TODO cleanup

## Critical Requirements
**Scope limitation**: Production codebase only (exclude docs/, archives/, dev/)
**Methodology compliance**: All TODOs must have issue numbers or be removed
**Evidence-based cleanup**: Verify QueryRouter TODOs are obsolete before removal
**Systematic approach**: Categorize before action, verify after cleanup

**Deliverable**: Production codebase with methodology-compliant TODO comments, ready to check Documentation Phase checkbox
