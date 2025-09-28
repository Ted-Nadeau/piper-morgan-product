#!/usr/bin/env python3
"""
Precise verification focusing only on GitHubIntegrationRouter class methods
"""

import re


def get_class_methods_only(content: str) -> dict:
    """Extract only methods that belong to GitHubIntegrationRouter class"""
    methods = {}
    lines = content.split("\n")

    # Find class start
    class_start = None
    for i, line in enumerate(lines):
        if "class GitHubIntegrationRouter:" in line:
            class_start = i
            break

    if class_start is None:
        return {}

    # Find class end (next class or module-level function)
    class_end = len(lines)
    for i in range(class_start + 1, len(lines)):
        line = lines[i].strip()
        if line.startswith("class ") or (
            line.startswith("def ") and not lines[i].startswith("    ")
        ):
            class_end = i
            break

    # Extract methods from class content
    class_content = "\n".join(lines[class_start:class_end])

    # Find method definitions within class
    for match in re.finditer(
        r"^\s+def\s+(\w+)\s*\([^)]*\)(?:\s*->\s*[^:]*)?:", class_content, re.MULTILINE
    ):
        method_name = match.group(1)
        if not method_name.startswith("_"):  # Skip private methods
            methods[method_name] = match.group(0).strip()

    return methods


def check_method_delegation(content: str, method_name: str) -> bool:
    """Check if a method follows the delegation pattern"""
    # Extract the method body
    pattern = rf"def {re.escape(method_name)}\([^)]*\)(?:\s*->\s*[^:]*)?:(.*?)(?=def|\Z)"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return False

    method_body = match.group(1)

    # Required delegation pattern elements
    required_patterns = [
        "_get_preferred_integration(",
        "if integration:",
        "if is_legacy:",
        "_warn_deprecation_if_needed(",
        "raise RuntimeError(",
    ]

    # All patterns must be present
    for pattern in required_patterns:
        if pattern not in method_body:
            return False

    return True


def main():
    print("🔍 PRECISE VERIFICATION: GitHubIntegrationRouter Class Methods Only")
    print("=" * 70)

    # Load router file
    with open("services/integrations/github/github_integration_router.py", "r") as f:
        router_content = f.read()

    # Get only class methods
    class_methods = get_class_methods_only(router_content)

    print(f"GitHubIntegrationRouter class methods found: {len(class_methods)}")
    print()

    # Check delegation pattern for each method
    compliant_methods = []
    non_compliant_methods = []

    for method_name in sorted(class_methods.keys()):
        if check_method_delegation(router_content, method_name):
            compliant_methods.append(method_name)
            print(f"✅ {method_name}")
        else:
            non_compliant_methods.append(method_name)
            print(f"❌ {method_name}")

    print()
    print("📊 DELEGATION PATTERN COMPLIANCE:")
    total_methods = len(class_methods)
    compliant_count = len(compliant_methods)
    compliance_percentage = (compliant_count / total_methods * 100) if total_methods > 0 else 0

    print(f"Compliant methods: {compliant_count}/{total_methods} ({compliance_percentage:.1f}%)")

    if non_compliant_methods:
        print(f"❌ Non-compliant methods: {non_compliant_methods}")

    print()
    print("📋 FINAL ASSESSMENT:")

    if compliance_percentage == 100:
        print("🎉 100% DELEGATION PATTERN COMPLIANCE ACHIEVED ✅")
        print("🚀 READY FOR PRODUCTION")
        return 0
    else:
        print(f"🚨 {100 - compliance_percentage:.1f}% INCOMPLETE - NOT PRODUCTION READY")
        print("⚠️  BLOCKED until 100% compliance achieved")
        return 1


if __name__ == "__main__":
    exit(main())
