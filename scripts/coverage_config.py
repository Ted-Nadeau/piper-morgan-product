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
        "description": "Completed QueryRouter work should meet high coverage standard",
    },
    # Tier 2: Active development (reasonable baseline)
    "active": {
        "threshold": 25,
        "files": [
            "services/orchestration/workflow_factory.py",
            "services/orchestration/coordinator.py",
        ],
        "description": "Active development should maintain reasonable coverage",
    },
    # Tier 3: Legacy code (track only)
    "legacy": {
        "threshold": 0,
        "files": [
            # Files with 0% coverage from analysis - track but don't enforce
        ],
        "description": "Legacy code tracked but not enforced to avoid blocking development",
    },
    # Overall baseline (prevent regression)
    "overall": {
        "threshold": 15,
        "pattern": "services/orchestration",
        "description": "Overall orchestration module must not regress below current 15%",
    },
}


def check_tiered_coverage():
    """Check coverage against tiered requirements"""
    import json
    import os
    import subprocess
    import sys

    results = {"passed": True, "failures": [], "warnings": []}

    print("=== Tiered Coverage Enforcement ===")

    # Check overall baseline first
    try:
        result = subprocess.run(
            [
                "python3",
                "-m",
                "pytest",
                "tests/",
                "--cov=services/orchestration",
                "--cov-report=json",
                "--tb=no",
                "-q",
            ],
            capture_output=True,
            text=True,
            env={"PYTHONPATH": "."},
        )

        if not os.path.exists("coverage.json"):
            results["passed"] = False
            results["failures"].append("Coverage report not generated")
            return results["passed"]

        with open("coverage.json", "r") as f:
            coverage_data = json.load(f)

        # Calculate overall coverage
        total_statements = sum(
            data["summary"]["num_statements"] for data in coverage_data["files"].values()
        )
        total_missing = sum(len(data["missing_lines"]) for data in coverage_data["files"].values())
        overall_coverage = (
            ((total_statements - total_missing) / total_statements * 100)
            if total_statements > 0
            else 0
        )

        print(f"Overall orchestration coverage: {overall_coverage:.1f}%")

        if overall_coverage < COVERAGE_TIERS["overall"]["threshold"]:
            results["passed"] = False
            results["failures"].append(
                f"Overall coverage {overall_coverage:.1f}% below baseline {COVERAGE_TIERS['overall']['threshold']}%"
            )
        else:
            print(
                f"✅ Overall baseline maintained ({overall_coverage:.1f}% >= {COVERAGE_TIERS['overall']['threshold']}%)"
            )

        # Check tier-specific requirements
        for tier_name, tier_config in COVERAGE_TIERS.items():
            if tier_name == "overall":
                continue

            print(f"\n--- {tier_name.title()} Tier (>={tier_config['threshold']}%) ---")

            for file_path in tier_config["files"]:
                # Calculate coverage for specific file
                file_coverage = 0
                if file_path in coverage_data["files"]:
                    file_data = coverage_data["files"][file_path]
                    statements = file_data["summary"]["num_statements"]
                    missing = len(file_data["missing_lines"])
                    file_coverage = (
                        ((statements - missing) / statements * 100) if statements > 0 else 100
                    )

                print(f"  {file_path.split('/')[-1]}: {file_coverage:.1f}%", end="")

                if file_coverage < tier_config["threshold"]:
                    if tier_name == "completed":
                        results["passed"] = False
                        results["failures"].append(
                            f"Completed work {file_path} has {file_coverage:.1f}% < {tier_config['threshold']}%"
                        )
                        print(" ❌ BELOW STANDARD")
                    else:
                        results["warnings"].append(
                            f"{tier_name.title()} work {file_path} has {file_coverage:.1f}% < {tier_config['threshold']}%"
                        )
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
    import sys

    success = check_tiered_coverage()
    sys.exit(0 if success else 1)
