# Agent Prompt: Phase 2A - Coverage Reality Analysis

**Agent**: Code  
**Mission**: Analyze current orchestration module coverage reality to inform pragmatic enforcement strategy, following Chief Architect's gameplan Phase 2.

## Context from Chief Architect's Gameplan
- **Approach**: Pragmatic coverage enforcement - high standards for completed work, baseline tracking for overall
- **Philosophy**: Coverage for COMPLETED components should approach 100%, overall coverage is metric to improve
- **Strategy**: Tiered enforcement based on component completion status

## Phase 2A Analysis Tasks

### 1. Comprehensive Coverage Assessment
```bash
# Generate detailed orchestration module coverage analysis
echo "=== Orchestration Module Coverage Assessment ==="

# Generate comprehensive coverage report
PYTHONPATH=. python -m pytest tests/ --cov=services/orchestration --cov-report=term-missing --cov-report=html --cov-report=json -q

echo ""
echo "Coverage summary:"
PYTHONPATH=. python -m pytest tests/ --cov=services/orchestration --cov-report=term --tb=no -q | grep -E "(TOTAL|orchestration)"

# Save detailed coverage data for analysis
PYTHONPATH=. python -c "
import json
try:
    with open('htmlcov/coverage.json', 'r') as f:
        coverage_data = json.load(f)
    
    print('\\n=== DETAILED COVERAGE BREAKDOWN ===')
    orchestration_files = {}
    total_statements = 0
    total_missing = 0
    
    for filename, data in coverage_data['files'].items():
        if 'services/orchestration' in filename:
            statements = data['summary']['num_statements']
            missing = data['summary']['missing_lines']
            covered = statements - missing
            coverage_pct = (covered / statements * 100) if statements > 0 else 100
            
            orchestration_files[filename] = {
                'statements': statements,
                'missing': missing,
                'covered': covered,
                'coverage_pct': coverage_pct
            }
            total_statements += statements
            total_missing += missing
    
    # Sort by coverage percentage
    sorted_files = sorted(orchestration_files.items(), key=lambda x: x[1]['coverage_pct'], reverse=True)
    
    print(f'Total orchestration statements: {total_statements}')
    print(f'Total covered statements: {total_statements - total_missing}')
    print(f'Overall coverage: {((total_statements - total_missing) / total_statements * 100):.1f}%')
    print()
    
    print('File-by-file coverage:')
    for filename, stats in sorted_files:
        short_name = filename.replace('services/orchestration/', '')
        print(f'{stats[\"coverage_pct\"]:5.1f}% | {stats[\"covered\"]:3d}/{stats[\"statements\"]:3d} | {short_name}')

except Exception as e:
    print(f'Coverage analysis error: {e}')
    print('Running basic coverage analysis instead...')
"
```

### 2. Component Classification Analysis
```bash
# Classify orchestration files by completion status and importance
echo "=== Component Classification Analysis ==="

echo "Analyzing orchestration module structure:"
find services/orchestration -name "*.py" | grep -v __pycache__ | sort

echo ""
echo "=== QueryRouter-Specific Files (Completed Components) ==="
find services/orchestration -name "*.py" -exec grep -l "QueryRouter\|query_router" {} \; | sort
echo ""
echo "Coverage for QueryRouter-specific files:"
for file in $(find services/orchestration -name "*.py" -exec grep -l "QueryRouter\|query_router" {} \;); do
    echo "File: $file"
    PYTHONPATH=. python -m pytest tests/ --cov="$file" --cov-report=term --tb=no -q 2>/dev/null | grep -E "(TOTAL|$(basename $file))" || echo "No coverage data"
done

echo ""
echo "=== Core Orchestration Files (Active) ==="
# Check for recently modified files (likely active)
echo "Recently modified orchestration files (last 60 days):"
find services/orchestration -name "*.py" -mtime -60 | sort

echo ""
echo "=== Legacy/Unused Files Analysis ==="
# Check for files that might be legacy or unused
echo "Files with no imports or minimal usage:"
find services/orchestration -name "*.py" -exec sh -c '
    file="$1"
    # Count imports of this file
    basename=$(basename "$file" .py)
    imports=$(grep -r "from.*$basename\|import.*$basename" services/ tests/ --include="*.py" 2>/dev/null | wc -l)
    lines=$(wc -l < "$file" 2>/dev/null || echo 0)
    if [ "$imports" -lt 2 ] && [ "$lines" -gt 50 ]; then
        echo "$imports imports, $lines lines: $file (potential legacy)"
    fi
' sh {} \;
```

### 3. Test Coverage Quality Analysis
```bash
# Analyze test coverage quality and gaps
echo "=== Test Coverage Quality Analysis ==="

echo "Orchestration test files:"
find tests/ -name "*.py" -exec grep -l "orchestration\|QueryRouter" {} \; | sort

echo ""
echo "Test coverage by module:"
for module in engine workflow_factory queryrouter coordinator; do
    echo "--- $module ---"
    module_file="services/orchestration/${module}.py"
    if [ -f "$module_file" ]; then
        echo "Module exists: $module_file"
        
        # Check for dedicated test file
        test_file="tests/unit/test_${module}.py"
        integration_test="tests/integration/test_${module}.py"
        
        if [ -f "$test_file" ]; then
            echo "  Unit tests: $test_file exists"
            echo "  Test count: $(grep -c "def test_" "$test_file" 2>/dev/null || echo 0) tests"
        else
            echo "  Unit tests: MISSING $test_file"
        fi
        
        if [ -f "$integration_test" ]; then
            echo "  Integration tests: $integration_test exists"
        else
            echo "  Integration tests: MISSING $integration_test"
        fi
        
        # Check coverage for this specific module
        PYTHONPATH=. python -m pytest tests/ --cov="$module_file" --cov-report=term --tb=no -q 2>/dev/null | grep -E "(TOTAL|$module)" || echo "  Coverage: No data available"
    else
        echo "Module does not exist: $module_file"
    fi
    echo ""
done
```

### 4. Realistic Enforcement Strategy Analysis
```bash
# Determine realistic enforcement thresholds based on current state
echo "=== Realistic Enforcement Strategy Analysis ==="

# Calculate what enforcement levels are actually achievable
PYTHONPATH=. python3 -c "
import subprocess
import json

def get_coverage_for_pattern(pattern):
    try:
        result = subprocess.run([
            'python', '-m', 'pytest', 'tests/', 
            f'--cov={pattern}', '--cov-report=json', '--tb=no', '-q'
        ], capture_output=True, text=True, env={'PYTHONPATH': '.'})
        
        with open('coverage.json', 'r') as f:
            data = json.load(f)
        
        total_statements = sum(file_data['summary']['num_statements'] 
                              for file_data in data['files'].values())
        total_missing = sum(len(file_data['missing_lines']) 
                           for file_data in data['files'].values())
        
        if total_statements > 0:
            coverage_pct = ((total_statements - total_missing) / total_statements) * 100
            return coverage_pct, total_statements, total_missing
        return 0, 0, 0
    except Exception as e:
        print(f'Error calculating coverage for {pattern}: {e}')
        return 0, 0, 0

print('=== TIERED COVERAGE ANALYSIS ===')

# Overall orchestration coverage
overall_cov, overall_stmt, overall_miss = get_coverage_for_pattern('services/orchestration')
print(f'Overall orchestration module: {overall_cov:.1f}% ({overall_stmt - overall_miss}/{overall_stmt})')

# Core files coverage
core_patterns = [
    'services/orchestration/engine.py',
    'services/orchestration/workflow_factory.py'
]

print('\\nCore orchestration files:')
for pattern in core_patterns:
    try:
        cov, stmt, miss = get_coverage_for_pattern(pattern)
        print(f'  {pattern.split(\"/\")[-1]}: {cov:.1f}% ({stmt - miss}/{stmt})')
    except:
        print(f'  {pattern.split(\"/\")[-1]}: Coverage measurement failed')

print('\\n=== ENFORCEMENT RECOMMENDATIONS ===')
print(f'Current baseline: {overall_cov:.1f}% (do not regress below this)')
print(f'Achievable target: {min(overall_cov + 10, 80):.1f}% (10% improvement or 80% max)')
print(f'Completed components: 80%+ (high standard for finished work)')
print(f'Legacy components: Track but do not block on low coverage')
"
```

### 5. Test Infrastructure Assessment
```bash
# Assess current test infrastructure for coverage enforcement
echo "=== Test Infrastructure Assessment ==="

echo "Current pytest configuration:"
if [ -f "pyproject.toml" ]; then
    echo "pyproject.toml coverage config:"
    grep -A 10 -B 5 "tool.coverage\|tool.pytest" pyproject.toml | head -15
fi

echo ""
echo "Coverage tool availability:"
python -c "
try:
    import coverage
    print('✅ coverage.py available')
except ImportError:
    print('❌ coverage.py not available')

try:
    import pytest_cov
    print('✅ pytest-cov available')
except ImportError:
    print('❌ pytest-cov not available')
"

echo ""
echo "Current test execution capability:"
echo "Total tests: $(find tests/ -name "*.py" -exec grep -c "def test_" {} + | awk '{sum += $1} END {print sum}')"
echo "Orchestration tests: $(find tests/ -name "*.py" -exec grep -l "orchestration\|QueryRouter" {} \; | xargs grep -c "def test_" 2>/dev/null | awk '{sum += $1} END {print sum}')"

echo ""
echo "CI integration status:"
if grep -q "coverage\|--cov" .github/workflows/test.yml 2>/dev/null; then
    echo "✅ Coverage already in CI configuration"
    grep -A 5 -B 5 "coverage\|--cov" .github/workflows/test.yml
else
    echo "❌ No coverage enforcement in CI"
fi
```

## Evidence Collection Requirements

### Coverage Baseline Assessment
```
=== Orchestration Module Coverage Reality ===
Overall coverage: [X]% ([covered]/[total] statements)
File count: [X] Python files in orchestration module
Coverage distribution: [breakdown by file]

Component classification:
- QueryRouter files: [X]% coverage ([list of files])
- Core orchestration files: [X]% coverage ([list of files])
- Legacy/unused files: [X]% coverage ([list of files])

Coverage quality assessment: [COMPREHENSIVE/BASIC/POOR]
```

### Enforcement Readiness Assessment
```
=== Coverage Enforcement Readiness ===
Current baseline: [X]% (minimum to maintain)
Achievable target: [X]% (realistic improvement goal)
High-standard components: [list files that should have 80%+]

Test infrastructure:
- pytest-cov available: [YES/NO]
- CI integration: [EXISTS/MISSING]
- Test file organization: [GOOD/NEEDS_WORK]

Ready for enforcement: [YES/NO]
Blocking issues: [list or NONE]
```

### Strategic Recommendations
```
=== Coverage Strategy Recommendations ===
Tiered enforcement approach:
- Tier 1 (Completed work): [X]% threshold for [list of files]
- Tier 2 (Overall baseline): [X]% threshold for orchestration module  
- Tier 3 (Legacy code): [track but don't enforce]

Implementation priority:
1. [highest priority recommendation]
2. [second priority recommendation]
3. [third priority recommendation]

Time estimates:
- Configuration setup: [X] minutes
- Achieving targets: [X] hours/not feasible
```

## Success Criteria
- [ ] Comprehensive coverage assessment with file-by-file breakdown
- [ ] Component classification (completed/active/legacy) with coverage levels
- [ ] Realistic enforcement threshold recommendations based on current state
- [ ] Test infrastructure readiness assessment
- [ ] Clear strategy for tiered coverage enforcement
- [ ] Evidence-based recommendations for Phase 2B implementation

## Time Estimate
25-30 minutes for comprehensive coverage reality analysis

## Critical Focus
**Reality assessment**: Document actual current coverage, not aspirational goals
**Component differentiation**: Distinguish completed work from legacy code
**Realistic targets**: Base enforcement on achievable improvement, not arbitrary standards
**Infrastructure verification**: Ensure we can actually implement proposed enforcement

**Deliverable**: Complete coverage reality assessment ready for Phase 2B enforcement implementation
