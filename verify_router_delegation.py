#!/usr/bin/env python3
"""
Verification script for GitHubIntegrationRouter delegation pattern compliance
"""

import ast
import sys
from typing import List, Tuple


def extract_method_signatures(file_path: str) -> List[Tuple[str, str]]:
    """Extract method signatures from Python file"""
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    methods = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "GitHubIntegrationRouter":
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    # Skip private methods and __init__
                    if not item.name.startswith("_") and item.name != "__init__":
                        # Extract signature
                        args = []
                        for arg in item.args.args[1:]:  # Skip 'self'
                            args.append(arg.arg)
                        methods.append((item.name, ", ".join(args)))

    return sorted(methods)


def check_delegation_pattern(file_path: str) -> List[str]:
    """Check if methods follow delegation pattern"""
    with open(file_path, "r") as f:
        content = f.read()

    issues = []

    # Expected pattern components
    required_patterns = [
        "_get_preferred_integration(",
        "if integration:",
        "if is_legacy:",
        "_warn_deprecation_if_needed(",
        "return integration.",
        "raise RuntimeError(",
    ]

    # Find all method definitions
    lines = content.split("\n")
    current_method = None
    method_content = []
    in_method = False

    for i, line in enumerate(lines):
        if "def " in line and not line.strip().startswith("#") and "self," in line:
            # New method found
            if current_method and not current_method.startswith("_"):
                # Analyze previous method
                method_body = "\n".join(method_content)
                if current_method not in ["initialize", "get_integration_status"]:
                    # Check if it follows delegation pattern
                    missing_patterns = []
                    for pattern in required_patterns:
                        if pattern not in method_body:
                            missing_patterns.append(pattern)

                    if missing_patterns:
                        issues.append(
                            f"Method {current_method} missing patterns: {missing_patterns}"
                        )

            # Start new method
            current_method = line.split("def ")[1].split("(")[0].strip()
            method_content = [line]
            in_method = True
        elif in_method:
            method_content.append(line)
            # Check if method ends (next def or class end)
            if line.strip() and not line.startswith(" ") and not line.startswith("\t"):
                in_method = False

    # Check final method
    if current_method and not current_method.startswith("_"):
        method_body = "\n".join(method_content)
        if current_method not in ["initialize", "get_integration_status"]:
            missing_patterns = []
            for pattern in required_patterns:
                if pattern not in method_body:
                    missing_patterns.append(pattern)

            if missing_patterns:
                issues.append(f"Method {current_method} missing patterns: {missing_patterns}")

    return issues


def main():
    github_agent_file = "services/integrations/github/github_agent.py"
    router_file = "services/integrations/github/github_integration_router.py"

    print("🔍 GitHubIntegrationRouter Delegation Pattern Verification")
    print("=" * 60)

    # Get GitHubAgent methods
    try:
        agent_methods = extract_method_signatures(github_agent_file)
        print(f"✅ GitHubAgent methods found: {len(agent_methods)}")
        for name, args in agent_methods:
            print(f"   - {name}({args})")
    except Exception as e:
        print(f"❌ Failed to read GitHubAgent: {e}")
        return 1

    print()

    # Get GitHubIntegrationRouter methods
    try:
        router_methods = extract_method_signatures(router_file)
        print(f"✅ GitHubIntegrationRouter methods found: {len(router_methods)}")
        for name, args in router_methods:
            print(f"   - {name}({args})")
    except Exception as e:
        print(f"❌ Failed to read GitHubIntegrationRouter: {e}")
        return 1

    print()

    # Check completeness
    agent_method_names = {name for name, _ in agent_methods}
    router_method_names = {
        name for name, _ in router_methods if name not in ["initialize", "get_integration_status"]
    }

    missing_methods = agent_method_names - router_method_names
    extra_methods = router_method_names - agent_method_names

    if missing_methods:
        print(f"❌ Missing methods in router: {missing_methods}")
    else:
        print("✅ All GitHubAgent methods implemented in router")

    if extra_methods:
        print(f"ℹ️  Router-specific methods: {extra_methods}")

    print()

    # Check delegation pattern compliance
    delegation_issues = check_delegation_pattern(router_file)

    if delegation_issues:
        print("❌ Delegation pattern issues found:")
        for issue in delegation_issues:
            print(f"   - {issue}")
        return 1
    else:
        print("✅ All methods follow proper delegation pattern")

    print()

    # Summary
    completeness = len(router_method_names) / len(agent_method_names) * 100
    print(f"📊 Router Completeness: {completeness:.1f}%")

    if completeness >= 100 and not delegation_issues:
        print("🎯 Assessment: COMPLETE ✅")
        return 0
    else:
        print("🚨 Assessment: INCOMPLETE ❌")
        return 1


if __name__ == "__main__":
    sys.exit(main())
