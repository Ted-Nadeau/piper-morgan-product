#!/usr/bin/env python3
"""
Final verification of GitHubIntegrationRouter implementation
"""

import re


def extract_methods_from_class(content: str, class_name: str) -> set:
    """Extract method names from a class"""
    methods = set()
    lines = content.split("\n")
    in_class = False

    for line in lines:
        if f"class {class_name}" in line:
            in_class = True
            continue
        if in_class and line.startswith("class ") and class_name not in line:
            break
        if in_class and line.startswith("def ") and class_name not in line:
            break  # Function outside class
        if in_class and "def " in line and not line.strip().startswith("#"):
            match = re.search(r"def\s+(\w+)\s*\(", line)
            if match and not match.group(1).startswith("_"):
                methods.add(match.group(1))

    return methods


def check_delegation_pattern(content: str, method_name: str) -> bool:
    """Check if a method follows delegation pattern"""
    # Find the method
    pattern = rf"def {re.escape(method_name)}\([^)]*\).*?(?=def|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return False

    method_body = match.group(0)

    # Router-specific methods don't need delegation
    if method_name in ["get_integration_status", "initialize"]:
        return True

    # Check for delegation pattern components
    required = [
        "_get_preferred_integration(",
        "if integration:",
        "if is_legacy:",
        "_warn_deprecation_if_needed(",
        "raise RuntimeError(",
    ]

    return all(pattern in method_body for pattern in required)


def main():
    print("🔍 FINAL VERIFICATION: GitHubIntegrationRouter Implementation")
    print("=" * 65)

    # Load files
    with open("services/integrations/github/github_agent.py", "r") as f:
        agent_content = f.read()

    with open("services/integrations/github/github_integration_router.py", "r") as f:
        router_content = f.read()

    # Extract methods
    agent_methods = extract_methods_from_class(agent_content, "GitHubAgent")
    router_methods = extract_methods_from_class(router_content, "GitHubIntegrationRouter")

    # Remove __init__ from comparison since they're different by design
    agent_methods.discard("__init__")

    print(f"GitHubAgent methods: {len(agent_methods)}")
    print(f"GitHubIntegrationRouter methods: {len(router_methods)}")
    print()

    # Check completeness
    missing_methods = agent_methods - router_methods
    router_specific = router_methods - agent_methods

    print("📊 COMPLETENESS ASSESSMENT:")
    if missing_methods:
        print(f"❌ Missing methods: {missing_methods}")
    else:
        print("✅ All GitHubAgent methods implemented")

    if router_specific:
        print(f"ℹ️  Router-specific methods: {router_specific}")

    print()

    # Check critical methods
    critical_methods = [
        "get_issue_by_url",
        "get_open_issues",
        "get_recent_issues",
        "get_recent_activity",
        "list_repositories",
    ]

    print("🎯 CRITICAL METHODS STATUS:")
    critical_present = 0
    for method in critical_methods:
        if method in router_methods:
            print(f"✅ {method}")
            critical_present += 1
        else:
            print(f"❌ {method}")

    print(f"Critical methods: {critical_present}/5")
    print()

    # Check delegation patterns
    print("🔄 DELEGATION PATTERN COMPLIANCE:")
    delegation_compliant = 0
    total_checked = 0

    for method in sorted(router_methods):
        if method != "__init__":  # Skip __init__
            total_checked += 1
            if check_delegation_pattern(router_content, method):
                print(f"✅ {method}")
                delegation_compliant += 1
            else:
                print(f"❌ {method}")

    print(
        f"Delegation pattern: {delegation_compliant}/{total_checked} ({delegation_compliant/total_checked*100:.1f}%)"
    )
    print()

    # Final assessment
    completeness = len(router_methods & agent_methods) / len(agent_methods) * 100

    print("📋 FINAL ASSESSMENT:")
    print(f"📊 Router Completeness: {completeness:.1f}%")
    print(
        f"🎯 Critical Methods: {critical_present}/5 ({'✅ COMPLETE' if critical_present == 5 else '❌ INCOMPLETE'})"
    )
    print(
        f"🔄 Delegation Pattern: {delegation_compliant}/{total_checked} ({'✅ EXCELLENT' if delegation_compliant/total_checked >= 0.9 else '❌ NEEDS WORK'})"
    )

    if (
        completeness >= 100
        and critical_present == 5
        and delegation_compliant / total_checked >= 0.9
    ):
        print("🎉 Assessment: READY FOR PRODUCTION ✅")
        return 0
    else:
        print("🚨 Assessment: NEEDS MORE WORK ❌")
        return 1


if __name__ == "__main__":
    exit(main())
