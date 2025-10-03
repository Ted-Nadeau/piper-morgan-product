#!/usr/bin/env python3
"""
Config Pattern Compliance Report Generator

Runs compliance tests and generates a summary report showing
which integrations pass/fail each compliance check.
"""

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


@dataclass
class TestResult:
    """Individual test result"""

    name: str
    integration: str
    status: str  # PASSED, FAILED, SKIPPED
    message: str = ""


@dataclass
class IntegrationReport:
    """Compliance report for a single integration"""

    name: str
    file_exists: bool = False
    class_exists: bool = False
    methods_complete: bool = False
    router_integration: bool = False
    graceful_degradation: bool = False
    no_direct_env: bool = False
    overall_status: str = "UNKNOWN"
    test_results: List[TestResult] = field(default_factory=list)

    def calculate_status(self):
        """Calculate overall compliance status"""
        checks = [
            self.file_exists,
            self.class_exists,
            self.methods_complete,
            self.router_integration,
            self.graceful_degradation,
            self.no_direct_env,
        ]

        passed_checks = sum(checks)
        total_checks = len(checks)

        if passed_checks == total_checks:
            self.overall_status = "✅ PASS"
        elif passed_checks >= total_checks * 0.7:  # 70% threshold
            self.overall_status = "⚠️ PARTIAL"
        else:
            self.overall_status = "❌ FAIL"

        return self.overall_status


@dataclass
class ComplianceReport:
    """Overall compliance report"""

    timestamp: str
    integrations: Dict[str, IntegrationReport] = field(default_factory=dict)
    overall_compliance: float = 0.0

    def calculate_overall_compliance(self):
        """Calculate overall compliance percentage"""
        if not self.integrations:
            self.overall_compliance = 0.0
            return

        compliant_count = sum(
            1 for report in self.integrations.values() if report.overall_status == "✅ PASS"
        )

        self.overall_compliance = (compliant_count / len(self.integrations)) * 100
        return self.overall_compliance


def run_pytest_with_json() -> Dict[str, Any]:
    """Run pytest and capture results in text format"""
    test_dir = Path(__file__).parent

    # Run tests for each integration separately to avoid parsing issues
    all_tests = []
    integrations = ["slack", "notion", "github", "calendar"]

    for integration in integrations:
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(test_dir / "test_config_pattern_compliance.py"),
            "-k",
            integration,
            "-v",
            "--tb=short",
        ]

        try:
            # Set PYTHONPATH to ensure imports work
            env = os.environ.copy()
            env["PYTHONPATH"] = str(test_dir.parent.parent.parent)

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=test_dir.parent.parent.parent, env=env
            )

            # Parse text output and add to all_tests
            integration_data = parse_pytest_text_output(result.stdout)
            all_tests.extend(integration_data.get("tests", []))

        except Exception as e:
            print(f"Error running pytest for {integration}: {e}")

    return {"tests": all_tests}


def parse_pytest_text_output(output: str) -> Dict[str, Any]:
    """Parse pytest text output to extract test results"""
    lines = output.split("\n")
    tests = []

    for line in lines:
        # Look for test result lines like:
        # tests/integration/config_pattern_compliance/test_config_pattern_compliance.py::TestConfigPatternCompliance::test_config_service_file_exists[slack] PASSED [10%]
        if "::test_" in line and ("PASSED" in line or "FAILED" in line or "SKIPPED" in line):
            # Extract test name and status - handle format with percentage
            if "PASSED [" in line:
                test_name = line.split(" PASSED [")[0].strip()
                status = "passed"
            elif "FAILED [" in line:
                test_name = line.split(" FAILED [")[0].strip()
                status = "failed"
            elif "SKIPPED [" in line:
                test_name = line.split(" SKIPPED [")[0].strip()
                status = "skipped"
            else:
                continue

            tests.append({"nodeid": test_name, "outcome": status, "call": {"longrepr": ""}})

    return {"tests": tests}


def parse_test_results(pytest_data: Dict[str, Any]) -> Dict[str, IntegrationReport]:
    """Parse pytest results into integration reports"""
    integrations = {}

    # Initialize integration reports
    for integration in ["slack", "notion", "github", "calendar"]:
        integrations[integration] = IntegrationReport(name=integration)

    # Process test results
    tests = pytest_data.get("tests", [])

    for test in tests:
        test_name = test.get("nodeid", "")
        outcome = test.get("outcome", "unknown")
        longrepr = test.get("call", {}).get("longrepr", "")

        # Extract integration name from test
        integration = None
        for integ in ["slack", "notion", "github", "calendar"]:
            if f"[{integ}]" in test_name:
                integration = integ
                break

        if not integration:
            continue

        # Map test results to compliance checks
        report = integrations[integration]
        passed = outcome == "passed"

        # Initialize tracking lists if not exists
        if not hasattr(report, "_test_results"):
            report._test_results = {}

        # Store individual test results
        if "file_exists" in test_name:
            report.file_exists = passed
        elif "class_exists" in test_name:
            report.class_exists = passed
        elif "required_methods" in test_name:
            report._test_results["methods"] = passed
        elif "init_signature" in test_name:
            report._test_results["signature"] = passed
        elif "accepts_config_service" in test_name:
            report._test_results["accepts"] = passed
        elif "stores_config_service" in test_name:
            report._test_results["stores"] = passed
        elif "graceful_degradation" in test_name:
            report.graceful_degradation = passed
        elif "no_direct_env_access" in test_name:
            report.no_direct_env = passed

        # Store individual test result
        test_result = TestResult(
            name=test_name.split("::")[-1],
            integration=integration,
            status=outcome,
            message=str(longrepr) if longrepr else "",
        )
        report.test_results.append(test_result)

    # Calculate combined results and overall status for each integration
    for report in integrations.values():
        # Combine method tests (both required_methods and init_signature must pass)
        if hasattr(report, "_test_results"):
            results = report._test_results
            report.methods_complete = results.get("methods", False) and results.get(
                "signature", False
            )
            report.router_integration = results.get("accepts", False) and results.get(
                "stores", False
            )

        report.calculate_status()

    return integrations


def generate_text_report(report: ComplianceReport) -> str:
    """Generate human-readable text report"""
    output = []

    # Header
    output.append("CONFIG PATTERN COMPLIANCE REPORT")
    output.append("=" * 50)
    output.append(f"Generated: {report.timestamp}")
    output.append("")

    # Summary table
    output.append("Integration | File | Class | Methods | Router | Graceful | No-Env | Status")
    output.append("-" * 75)

    for name, integ_report in report.integrations.items():
        file_check = "✅" if integ_report.file_exists else "❌"
        class_check = "✅" if integ_report.class_exists else "❌"
        methods_check = "✅" if integ_report.methods_complete else "❌"
        router_check = "✅" if integ_report.router_integration else "❌"
        graceful_check = "✅" if integ_report.graceful_degradation else "❌"
        env_check = "✅" if integ_report.no_direct_env else "❌"

        output.append(
            f"{name:<11} | {file_check:<4} | {class_check:<5} | {methods_check:<7} | "
            f"{router_check:<6} | {graceful_check:<8} | {env_check:<6} | {integ_report.overall_status}"
        )

    output.append("")
    output.append(
        f"Overall Compliance: {report.overall_compliance:.1f}% "
        f"({sum(1 for r in report.integrations.values() if r.overall_status == '✅ PASS')} "
        f"of {len(report.integrations)} integrations)"
    )

    # Detailed recommendations
    output.append("")
    output.append("RECOMMENDATIONS:")
    output.append("-" * 20)

    for name, integ_report in report.integrations.items():
        if integ_report.overall_status != "✅ PASS":
            output.append(f"\n{name.upper()}:")

            if not integ_report.file_exists:
                output.append(f"  • Create services/integrations/{name}/config_service.py")
            if not integ_report.class_exists:
                output.append(f"  • Implement {name.title()}ConfigService class")
            if not integ_report.methods_complete:
                output.append(
                    f"  • Add required methods: get_config(), is_configured(), _load_config()"
                )
            if not integ_report.router_integration:
                output.append(f"  • Update router to accept config_service parameter")
            if not integ_report.graceful_degradation:
                output.append(f"  • Implement graceful degradation when config missing")
            if not integ_report.no_direct_env:
                output.append(f"  • Replace direct os.getenv() with config service usage")

    # Reference implementations
    output.append("")
    output.append("REFERENCE IMPLEMENTATIONS:")
    output.append("-" * 25)
    output.append("• Slack: Complete reference pattern")
    output.append("• Notion: Recently implemented (Phase 1B)")
    output.append("")
    output.append("For implementation details, see:")
    output.append("• services/integrations/slack/config_service.py")
    output.append("• services/integrations/notion/config_service.py")

    return "\n".join(output)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Generate config pattern compliance report")
    parser.add_argument(
        "--integrations",
        default="slack,notion,github,calendar",
        help="Comma-separated list of integrations to test",
    )
    parser.add_argument("--output", help="Output file path (default: print to stdout)")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    print("🧪 Running config pattern compliance tests...")

    # Run pytest and collect results
    pytest_data = run_pytest_with_json()

    # Parse results into report
    integration_reports = parse_test_results(pytest_data)

    # Filter requested integrations
    requested = args.integrations.split(",")
    filtered_reports = {
        name: report for name, report in integration_reports.items() if name in requested
    }

    # Create final report
    report = ComplianceReport(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), integrations=filtered_reports
    )
    report.calculate_overall_compliance()

    # Generate output
    if args.format == "json":
        import json

        output_text = json.dumps(report.__dict__, indent=2, default=str)
    else:
        output_text = generate_text_report(report)

    # Write output
    if args.output:
        with open(args.output, "w") as f:
            f.write(output_text)
        print(f"✅ Report written to: {args.output}")
    else:
        print("\n" + output_text)

    # Exit with appropriate code
    if report.overall_compliance == 100.0:
        print(f"\n🎉 All integrations compliant!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {report.overall_compliance:.1f}% compliance - work needed")
        sys.exit(1)


if __name__ == "__main__":
    main()
