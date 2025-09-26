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

try:
    from scripts.coverage_config import check_tiered_coverage, COVERAGE_TIERS
except ImportError:
    print("Error: Could not import coverage configuration")
    sys.exit(1)

def generate_coverage_report():
    """Generate detailed coverage report for local analysis"""
    print("🔍 Generating coverage report...")
    
    try:
        # Generate HTML and terminal reports
        result = subprocess.run([
            'python3', '-m', 'pytest', 'tests/',
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
