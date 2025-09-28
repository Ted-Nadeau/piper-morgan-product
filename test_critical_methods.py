#!/usr/bin/env python3
"""Test critical method signatures"""

import re


def extract_method_signature(content: str, method_name: str) -> str:
    """Extract a single method signature from file content"""
    pattern = rf"(async\s+)?def\s+{re.escape(method_name)}\s*\([^)]*\)(?:\s*->\s*[^:]*)?:"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(0).replace("\n", " ").strip()
    return "NOT FOUND"


# Load both files
with open("services/integrations/github/github_agent.py", "r") as f:
    agent_content = f.read()

with open("services/integrations/github/github_integration_router.py", "r") as f:
    router_content = f.read()

# Critical methods that bypassing services use
critical_methods = [
    "get_issue_by_url",
    "get_open_issues",
    "get_recent_issues",
    "get_recent_activity",
    "list_repositories",
]

print("🔍 Critical Method Signature Status")
print("=" * 40)

for method in critical_methods:
    agent_sig = extract_method_signature(agent_content, method)
    router_sig = extract_method_signature(router_content, method)

    print(f"\n{method}:")
    print(f"  Agent:  {agent_sig}")
    print(f"  Router: {router_sig}")

    # Basic match check (remove spaces and async for comparison)
    agent_norm = re.sub(r"\s+", " ", agent_sig.replace("async ", ""))
    router_norm = re.sub(r"\s+", " ", router_sig.replace("async ", ""))

    if agent_norm == router_norm:
        print(f"  ✅ MATCH")
    else:
        print(f"  ❌ MISMATCH")

print(f"\n📊 Router completion status:")
print(
    f"Methods implemented: {len([m for m in critical_methods if 'def ' + m in router_content])}/5"
)
