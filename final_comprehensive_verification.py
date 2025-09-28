#!/usr/bin/env python3
"""
Final comprehensive verification of all public methods in GitHubIntegrationRouter
"""

import re


def get_public_class_methods(content: str) -> list:
    """Get all public methods from GitHubIntegrationRouter class"""
    methods = []
    lines = content.split("\n")

    for i, line in enumerate(lines):
        if re.search(r"(async\s+)?def\s+(\w+)\s*\(", line):
            method_match = re.search(r"(async\s+)?def\s+(\w+)\s*\(", line)
            if method_match:
                method_name = method_match.group(2)

                # Check if it's a class method (indented) and public (not starting with _)
                if (
                    line.startswith("    ")
                    and not line.startswith("        ")
                    and not method_name.startswith("_")
                    and method_name != "__init__"
                ):
                    methods.append(method_name)

    return sorted(methods)


def check_delegation_pattern_comprehensive(content: str, method_name: str) -> dict:
    """Comprehensive check of delegation pattern with detailed results"""
    # Extract method body
    pattern = rf"(async\s+)?def {re.escape(method_name)}\([^)]*\)(?:\s*->\s*[^:]*)?:(.*?)(?=\n\s*(?:async\s+)?def|\Z)"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return {"found": False, "missing": ["method not found"]}

    method_body = match.group(2)

    # Check for required patterns
    checks = {
        "_get_preferred_integration(": "_get_preferred_integration(" in method_body,
        "if integration:": "if integration:" in method_body,
        "if is_legacy:": "if is_legacy:" in method_body,
        "_warn_deprecation_if_needed(": "_warn_deprecation_if_needed(" in method_body,
        "raise RuntimeError(": "raise RuntimeError(" in method_body,
    }

    missing = [pattern for pattern, found in checks.items() if not found]

    return {
        "found": True,
        "compliant": len(missing) == 0,
        "missing": missing,
        "method_body_excerpt": method_body[:200] + "..." if len(method_body) > 200 else method_body,
    }


def main():
    print("🔍 FINAL COMPREHENSIVE VERIFICATION")
    print("GitHubIntegrationRouter: 100% Delegation Pattern Compliance Check")
    print("=" * 70)

    # Load router file
    with open("services/integrations/github/github_integration_router.py", "r") as f:
        content = f.read()

    # Get all public methods
    public_methods = get_public_class_methods(content)

    print(f"Public methods to verify: {len(public_methods)}")
    print()

    # Check each method
    compliant_methods = []
    non_compliant_methods = []

    for method_name in public_methods:
        result = check_delegation_pattern_comprehensive(content, method_name)

        if result["found"] and result["compliant"]:
            compliant_methods.append(method_name)
            print(f"✅ {method_name}")
        else:
            non_compliant_methods.append(method_name)
            print(f"❌ {method_name}")
            if result["missing"]:
                print(f"   Missing: {', '.join(result['missing'])}")

    print()
    print("📊 FINAL COMPLIANCE ASSESSMENT:")
    total = len(public_methods)
    compliant = len(compliant_methods)
    percentage = (compliant / total * 100) if total > 0 else 0

    print(f"Compliant methods: {compliant}/{total} ({percentage:.1f}%)")

    if non_compliant_methods:
        print(f"❌ Non-compliant: {non_compliant_methods}")

    print()
    print("📋 PRODUCTION READINESS:")

    if percentage == 100.0:
        print("🎉 100% DELEGATION PATTERN COMPLIANCE ACHIEVED")
        print("✅ ALL METHODS FOLLOW EXACT DELEGATION PATTERN")
        print("✅ PROPER ERROR HANDLING FOR MISSING INTEGRATIONS")
        print("✅ DEPRECATION WARNINGS FOR LEGACY USAGE")
        print("🚀 PRODUCTION READY - PHASE 2 CAN PROCEED")
        return 0
    else:
        print(f"🚨 {100-percentage:.1f}% INCOMPLETE")
        print("❌ NOT PRODUCTION READY")
        print("⚠️  PHASE 2 BLOCKED UNTIL 100% COMPLIANCE")
        return 1


if __name__ == "__main__":
    exit(main())
