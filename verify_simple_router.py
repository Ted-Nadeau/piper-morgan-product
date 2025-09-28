#!/usr/bin/env python3
"""
Simple verification of GitHubIntegrationRouter method completeness
"""

import re


def main():
    print("🔍 GitHubIntegrationRouter Method Completeness Check")
    print("=" * 55)

    # Expected methods from GitHubAgent
    expected_methods = [
        "create_issue",
        "create_issue_from_work_item",
        "create_pm_issue",
        "get_closed_issues",
        "get_development_context",
        "get_issue",
        "get_issue_by_url",
        "get_issues_by_priority",
        "get_open_issues",
        "get_recent_activity",
        "get_recent_issues",
        "list_repositories",
        "parse_github_url",
        "test_connection",
    ]

    # Read router file
    with open("services/integrations/github/github_integration_router.py", "r") as f:
        router_content = f.read()

    print(f"Expected methods: {len(expected_methods)}")
    print()

    # Check each method
    found_methods = []
    missing_methods = []

    for method in expected_methods:
        # Look for method definition
        pattern = rf"def {re.escape(method)}\("
        if re.search(pattern, router_content):
            found_methods.append(method)
            print(f"✅ {method}")
        else:
            missing_methods.append(method)
            print(f"❌ {method}")

    print()
    print(f"Found: {len(found_methods)}/{len(expected_methods)} methods")

    if missing_methods:
        print(f"❌ Missing: {missing_methods}")
        return 1
    else:
        print("✅ All methods implemented")

    # Quick delegation pattern check for a few key methods
    critical_methods = [
        "get_issue_by_url",
        "get_open_issues",
        "get_recent_issues",
        "get_recent_activity",
        "list_repositories",
    ]

    print()
    print("🔍 Delegation Pattern Check (Critical Methods):")

    for method in critical_methods:
        method_match = re.search(
            rf"def {re.escape(method)}\(.*?\n(.*?)\n.*?def", router_content, re.DOTALL
        )
        if method_match:
            method_body = method_match.group(1)
            if (
                "integration, is_legacy = self._get_preferred_integration(" in method_body
                and "raise RuntimeError(" in method_body
            ):
                print(f"✅ {method} - follows delegation pattern")
            else:
                print(f"❌ {method} - delegation pattern issue")
        else:
            print(f"❌ {method} - not found")

    print()
    completeness = len(found_methods) / len(expected_methods) * 100
    print(f"📊 Router Completeness: {completeness:.1f}%")

    if completeness >= 100:
        print("🎯 Assessment: COMPLETE ✅")
        return 0
    else:
        print("🚨 Assessment: INCOMPLETE ❌")
        return 1


if __name__ == "__main__":
    exit(main())
