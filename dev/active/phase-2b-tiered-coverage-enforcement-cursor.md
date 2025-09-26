# Agent Prompt: Phase 2B - Tiered Coverage Enforcement Implementation

**Agent**: Cursor  
**Mission**: Implement tiered coverage enforcement based on Code's analysis, following Chief Architect's pragmatic approach for different component completion levels.

## Context from Phase 2A Analysis
- **Overall baseline**: 15% coverage (235/1608 statements) - prevent regression
- **Component classification**: 2 completed, 3 active, 5 legacy files 
- **Key gap**: engine.py (QueryRouter) at 35% vs 80% standard for completed work
- **Infrastructure**: pytest-cov ready, CI enforcement missing

## Phase 2B Implementation Tasks

### 1. Configure Tiered Coverage Enforcement
```bash
# Create tiered coverage configuration
echo "=== Creating Tiered Coverage Configuration ==="

# Create coverage configuration file
cat > scripts/coverage_config.py << 'EOF'
#!/usr/bin/env python3
"""
Tiered Coverage Configuration for GREAT-1C
Based on Phase 2A analysis - different standards for different completion levels

Philosophy: High standards for completed work, reasonable baselines for active work,
track but don't block legacy code.
"""

# Tiered coverage requirements based on component completion status
COVERAGE_TIERS = {
    # Tier 1: Completed components (high standard)
    "completed": {
        "threshold": 80,
        "files": [
            "services/orchestration/engine.py",  # QueryRouter integration - completed
        ],
        "description": "Completed QueryRouter work should meet high coverage standard"
    },
    
    # Tier 2: Active development (reasonable baseline)  
    "active": {
        "threshold": 25,
        "files": [
            "services/orchestration/workflow_factory.py",
            "services/orchestration/coordinator.py",
        ],
        "description": "Active development should maintain reasonable coverage"
    },
    
    # Tier 3: Legacy code (track only)
    "legacy": {
        "threshold": 0,
        "files": [
            # Files with 0% coverage from analysis - track but don't enforce
        ],
        "description": "Legacy code tracked but not enforced to avoid blocking development"
    },
    
    # Overall baseline (prevent regression)
    "overall": {
        "threshold": 15,
        "pattern": "services/orchestration",
        "description": "Overall orchestration module must not regress below current 15%"
    }
}

def check_tiered_coverage():
    """Check coverage against tiered requirements"""
    import subprocess
    import json
    import sys
    
    results = {
        "passed": True,
        "failures": [],
        "warnings": []
    }
    
    print("=== Tiered Coverage Enforcement ===")
    
    # Check overall baseline first
    try:
        result = subprocess.run([
            'python', '-m', 'pytest', 'tests/', 
            '--cov=services/orchestration', '--cov-report=json', '--tb=no', '-q'
        ], capture_output=True, text=True, env={'PYTHONPATH': '.'})
        
        with open('coverage.json', 'r') as f:
            coverage_data = json.load(f)
        
        # Calculate overall coverage
        total_statements = sum(data['summary']['num_statements'] 
                             for data in coverage_data['files'].values())
        total_missing = sum(len(data['missing_lines']) 
                           for data in coverage_data['files'].values())
        overall_coverage = ((total_statements - total_missing) / total_statements * 100) if total_statements > 0 else 0
        
        print(f"Overall orchestration coverage: {overall_coverage:.1f}%")
        
        if overall_coverage < COVERAGE_TIERS["overall"]["threshold"]:
            results["passed"] = False
            results["failures"].append(f"Overall coverage {overall_coverage:.1f}% below baseline {COVERAGE_TIERS['overall']['threshold']}%")
        else:
            print(f"✅ Overall baseline maintained ({overall_coverage:.1f}% >= {COVERAGE_TIERS['overall']['threshold']}%)")
        
        # Check tier-specific requirements
        for tier_name, tier_config in COVERAGE_TIERS.items():
            if tier_name == "overall":
                continue
                
            print(f"\n--- {tier_name.title()} Tier (>={tier_config['threshold']}%) ---")
            
            for file_path in tier_config["files"]:
                # Calculate coverage for specific file
                file_coverage = 0
                if file_path in coverage_data['files']:
                    file_data = coverage_data['files'][file_path]
                    statements = file_data['summary']['num_statements']
                    missing = len(file_data['missing_lines'])
                    file_coverage = ((statements - missing) / statements * 100) if statements > 0 else 100
                
                print(f"  {file_path.split('/')[-1]}: {file_coverage:.1f}%", end="")
                
                if file_coverage < tier_config["threshold"]:
                    if tier_name == "completed":
                        results["passed"] = False
                        results["failures"].append(f"Completed work {file_path} has {file_coverage:.1f}% < {tier_config['threshold']}%")
                        print(" ❌ BELOW STANDARD")
                    else:
                        results["warnings"].append(f"{tier_name.title()} work {file_path} has {file_coverage:.1f}% < {tier_config['threshold']}%")
                        print(" ⚠️  Below target")
                else:
                    print(" ✅")
        
    except Exception as e:
        results["passed"] = False
        results["failures"].append(f"Coverage analysis failed: {e}")
    
    # Report results
    print(f"\n=== Coverage Enforcement Results ===")
    if results["failures"]:
        print("❌ FAILURES (blocking):")
        for failure in results["failures"]:
            print(f"  - {failure}")
    
    if results["warnings"]:
        print("⚠️  WARNINGS (non-blocking):")
        for warning in results["warnings"]:
            print(f"  - {warning}")
    
    if results["passed"] and not results["warnings"]:
        print("✅ All coverage requirements met!")
    elif results["passed"]:
        print("✅ Critical coverage requirements met (warnings noted)")
    
    return results["passed"]

if __name__ == "__main__":
    success = check_tiered_coverage()
    sys.exit(0 if success else 1)
EOF

chmod +x scripts/coverage_config.py
echo "✅ Tiered coverage configuration created"
```

### 2. Add CI Integration for Coverage Enforcement
```bash
# Add tiered coverage enforcement to CI workflow
echo "=== Adding Tiered Coverage Enforcement to CI ==="

# Find CI configuration file
ci_file=".github/workflows/test.yml"

# Add coverage enforcement job after performance tests
cat >> "$ci_file" << 'EOF'

  tiered-coverage-enforcement:
    name: Tiered Coverage Enforcement
    runs-on: ubuntu-latest
    needs: [performance-regression-check]  # Run after performance tests
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt --break-system-packages
        
    - name: Run Tiered Coverage Analysis
      run: |
        echo "Running tiered coverage enforcement..."
        
        # Generate coverage data
        PYTHONPATH=. python -m pytest tests/ --cov=services/orchestration --cov-report=json --tb=no -q
        
        # Run tiered coverage check
        python scripts/coverage_config.py
        
    - name: Coverage Enforcement Summary
      if: failure()
      run: |
        echo "❌ Coverage enforcement failed!"
        echo ""
        echo "This build failed because completed components don't meet coverage standards:"
        echo "• Completed work (QueryRouter): Must have ≥80% coverage"
        echo "• Active development: Should have ≥25% coverage (warnings only)"
        echo "• Overall baseline: Must maintain ≥15% (prevent regression)"
        echo ""
        echo "To resolve:"
        echo "1. Check the coverage analysis output above"
        echo "2. Add tests for completed QueryRouter components"
        echo "3. Run 'python scripts/coverage_config.py' locally to verify"
        echo "4. Consider if component classification needs updating"
        
    - name: Upload Coverage Report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: coverage-report
        path: |
          coverage.json
          htmlcov/
EOF

echo "✅ Tiered coverage enforcement added to CI"
```

### 3. Create Local Coverage Validation Tool
```bash
# Create local script for developers to check coverage before pushing
echo "=== Creating Local Coverage Validation Tool ==="

cat > scripts/check_coverage_locally.py << 'EOF'
#!/usr/bin/env python3
"""
Local Coverage Validation Tool

Run this before pushing to check if your changes meet coverage requirements.
Usage: python scripts/check_coverage_locally.py
"""

import subprocess
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.coverage_config import check_tiered_coverage, COVERAGE_TIERS

def generate_coverage_report():
    """Generate detailed coverage report for local analysis"""
    print("🔍 Generating coverage report...")
    
    try:
        # Generate HTML and terminal reports
        result = subprocess.run([
            'python', '-m', 'pytest', 'tests/',
            '--cov=services/orchestration',
            '--cov-report=html',
            '--cov-report=term-missing',
            '--cov-report=json',
            '--tb=no', '-q'
        ], env={'PYTHONPATH': '.'})
        
        if result.returncode == 0:
            print("✅ Coverage report generated successfully")
            print("📊 Detailed report: htmlcov/index.html")
            return True
        else:
            print("❌ Coverage generation failed")
            return False
    except Exception as e:
        print(f"❌ Error generating coverage: {e}")
        return False

def show_improvement_suggestions():
    """Show specific suggestions for improving coverage"""
    print("\n🎯 Coverage Improvement Suggestions:")
    
    print("\nFor QueryRouter (engine.py) to reach 80%:")
    print("• Add tests for error handling scenarios")
    print("• Test initialization with different configurations")
    print("• Test integration with workflow factory")
    print("• Add edge case testing for query routing logic")
    
    print("\nFor active development files:")
    print("• Focus on core functionality testing first")
    print("• Add integration tests for component interactions")
    print("• Consider testing happy path before edge cases")
    
    print("\nGeneral testing approach:")
    print("• Run: python -m pytest tests/ --cov=services/orchestration/engine.py --cov-report=term-missing")
    print("• Focus on missing lines shown in report")
    print("• Start with easiest tests (initialization, basic methods)")

def main():
    """Main local coverage validation"""
    print("🔍 Local Coverage Validation")
    print("=" * 50)
    
    # Generate coverage data
    if not generate_coverage_report():
        print("Failed to generate coverage report")
        sys.exit(1)
    
    # Run tiered coverage check
    print("\n" + "=" * 50)
    success = check_tiered_coverage()
    
    if not success:
        print("\n" + "=" * 50)
        show_improvement_suggestions()
        print("\n⚠️  Coverage requirements not met - see suggestions above")
        print("🚫 Push will be blocked by CI until coverage improves")
    else:
        print("\n✅ All coverage requirements met!")
        print("🎉 Safe to push - coverage enforcement will pass")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
EOF

chmod +x scripts/check_coverage_locally.py
echo "✅ Local coverage validation tool created"
```

### 4. Update Project Documentation
```bash
# Update coverage documentation with tiered approach
echo "=== Updating Coverage Documentation ==="

cat > docs/testing/tiered-coverage-enforcement.md << 'EOF'
# Tiered Coverage Enforcement

## Philosophy

Coverage requirements should match component completion status:
- **Completed work**: High standards (80%+) to ensure quality
- **Active development**: Reasonable baselines (25%+) to encourage testing
- **Legacy code**: Track but don't block (0% acceptable)
- **Overall baseline**: Prevent regression from current state

## Current Tiers (Sept 25, 2025)

### Tier 1: Completed Components (≥80% required)
- `services/orchestration/engine.py` - QueryRouter integration (completed)
- **Status**: Currently 35%, needs improvement
- **Standard**: High coverage for production-ready code

### Tier 2: Active Development (≥25% target)
- `services/orchestration/workflow_factory.py`
- `services/orchestration/coordinator.py`
- **Standard**: Reasonable coverage to encourage testing

### Tier 3: Legacy Code (0% acceptable)
- Files identified as legacy or unused
- **Standard**: Track coverage but don't block development

### Overall Baseline (≥15% required)
- `services/orchestration/*` - Complete module
- **Standard**: Prevent regression from current 15% baseline

## Usage

### Local Testing
```bash
# Check coverage before pushing
python scripts/check_coverage_locally.py

# Quick coverage check
python scripts/coverage_config.py

# Focus on specific file
python -m pytest tests/ --cov=services/orchestration/engine.py --cov-report=term-missing
```

### CI Integration
- Tiered coverage runs after performance tests
- **Failures block**: Completed work below 80%, overall below 15%
- **Warnings only**: Active work below 25%

## Improving Coverage

### For QueryRouter (engine.py → 80%)
Priority areas to test:
1. Initialization with different configurations
2. Error handling scenarios
3. Integration with workflow factory
4. Query routing logic edge cases

### For Active Development
1. Focus on core functionality first
2. Add integration tests for interactions
3. Test happy paths before edge cases

## Updating Tiers

When components are completed:
1. Move from "active" to "completed" tier
2. Update `scripts/coverage_config.py`
3. Ensure coverage meets 80% standard
4. Update this documentation

## Rationale

This tiered approach:
- ✅ Maintains quality for completed work
- ✅ Encourages testing without blocking development
- ✅ Prevents coverage regression
- ✅ Recognizes different component maturity levels
- ✅ Provides clear improvement path
EOF

echo "✅ Tiered coverage documentation created"
```

### 5. Test and Verify Implementation
```bash
# Test the complete tiered coverage system
echo "=== Testing Tiered Coverage Implementation ==="

echo "Testing coverage configuration:"
python scripts/coverage_config.py

echo ""
echo "Testing local validation tool:"
python scripts/check_coverage_locally.py

echo ""
echo "Verifying CI configuration:"
if grep -q "tiered-coverage-enforcement" .github/workflows/test.yml; then
    echo "✅ CI job added successfully"
else
    echo "❌ CI job not found"
fi

echo ""
echo "System verification:"
echo "1. Configuration file: $([ -f scripts/coverage_config.py ] && echo '✅' || echo '❌') scripts/coverage_config.py"
echo "2. Local validation: $([ -f scripts/check_coverage_locally.py ] && echo '✅' || echo '❌') scripts/check_coverage_locally.py"
echo "3. Documentation: $([ -f docs/testing/tiered-coverage-enforcement.md ] && echo '✅' || echo '❌') docs/testing/tiered-coverage-enforcement.md"
echo "4. CI integration: $(grep -q 'tiered-coverage-enforcement' .github/workflows/test.yml && echo '✅' || echo '❌') CI job added"

echo ""
echo "Current status summary:"
echo "• Overall coverage baseline: 15% (must maintain)"
echo "• QueryRouter (completed): Needs improvement 35% → 80%"
echo "• Active development: 25% target (warnings only)"
echo "• Legacy code: Tracked but not enforced"
echo ""
echo "Next steps:"
echo "1. ✅ Tiered enforcement configured"
echo "2. 🔄 Improve QueryRouter coverage to meet completion standard"
echo "3. ✅ CI will enforce standards going forward"
```

## Evidence Collection Requirements

### Implementation Status
```
=== Tiered Coverage Implementation Results ===
Configuration system: [CREATED/FAILED]
CI integration: [ADDED/MISSING]
Local tools: [WORKING/BROKEN]
Documentation: [COMPLETE/INCOMPLETE]

Tier configuration:
- Completed (80%): [list files and current coverage]
- Active (25%): [list files and current coverage]
- Legacy (0%): [list files and current coverage]
- Overall (15%): [current percentage]

Testing results: [ALL_PASSED/SOME_FAILED]
```

### Enforcement Verification
```
=== Coverage Enforcement Verification ===
Local validation: [WORKING/BROKEN]
- Tiered thresholds: [PROPERLY_ENFORCED/ISSUES]
- Improvement suggestions: [PROVIDED/MISSING]

CI enforcement: [CONFIGURED/NEEDS_WORK]
- Job dependencies: [CORRECT/INCORRECT]
- Failure conditions: [APPROPRIATE/NEEDS_ADJUSTMENT]

Ready for production: [YES/NO]
Blocking issues: [list or NONE]
```

### Checkbox Assessment
```
=== "Required test coverage for orchestration module" Status ===
Can be checked: [YES/NO]
Enforcement mechanism: [WORKING/INCOMPLETE]
Realistic thresholds: [IMPLEMENTED/MISSING]

Evidence for checking:
- Tiered enforcement: [CONFIGURED/INCOMPLETE]
- CI integration: [WORKING/BROKEN]
- Completed work standard: [80% enforced/NOT_ENFORCED]
- Regression prevention: [15% baseline protected/NOT_PROTECTED]

Missing for completion: [list items or READY]
```

## Success Criteria
- [ ] Tiered coverage configuration implemented with realistic thresholds
- [ ] CI enforcement added with proper job dependencies
- [ ] Local validation tool created for developer use
- [ ] Documentation updated with tiered approach and usage instructions
- [ ] System tested and verified working end-to-end
- [ ] Evidence provided for checking "Required test coverage" checkbox

## Time Estimate
15-20 minutes for complete tiered enforcement implementation

## Critical Requirements
**Pragmatic thresholds**: 80% for completed work, 25% for active, 0% for legacy
**CI integration**: Blocks on completed work failures, warns on active work
**Developer tools**: Local validation and improvement suggestions
**Clear documentation**: Usage instructions and rationale for tiered approach

**Deliverable**: Working tiered coverage enforcement system that can legitimately check the coverage requirement checkbox
