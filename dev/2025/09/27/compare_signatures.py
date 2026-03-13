#!/usr/bin/env python3
"""
Compare method signatures between GitHubAgent and GitHubIntegrationRouter
"""

import ast
import re
from typing import Dict, List, Tuple


def extract_method_signatures_from_file(file_path: str, class_name: str) -> Dict[str, str]:
    """Extract method signatures from a Python file"""
    with open(file_path, "r") as f:
        content = f.read()

    # Find method signatures using regex
    signatures = {}

    # Pattern to match method definitions
    method_pattern = r"(async\s+)?def\s+(\w+)\s*\((.*?)\)\s*->\s*([^:]+):"

    # Split into lines and find methods within the class
    lines = content.split("\n")
    in_class = False
    current_method = None
    method_lines = []

    for line in lines:
        # Check if we're entering the target class
        if f"class {class_name}" in line:
            in_class = True
            continue

        # Check if we're leaving the class (new class or end of file)
        if in_class and line.startswith("class ") and class_name not in line:
            in_class = False
            continue

        # If we're in the class, look for method definitions
        if in_class and ("def " in line and not line.strip().startswith("#")):
            # Save previous method if exists
            if current_method and method_lines:
                full_signature = "\n".join(method_lines).strip()
                # Clean up the signature
                clean_sig = re.sub(r"\s+", " ", full_signature.replace("\n", " "))
                signatures[current_method] = clean_sig

            # Start new method
            if "def " in line:
                method_match = re.search(r"def\s+(\w+)\s*\(", line)
                if method_match:
                    current_method = method_match.group(1)
                    method_lines = [line.strip()]
        elif in_class and current_method and (line.strip().startswith(")") or "def " not in line):
            # Continue collecting method signature lines
            if (
                line.strip()
                and not line.strip().startswith('"""')
                and not line.strip().startswith("try:")
            ):
                method_lines.append(line.strip())
                # Stop if we hit the end of signature
                if ")" in line and "->" in line and ":" in line:
                    full_signature = "\n".join(method_lines).strip()
                    clean_sig = re.sub(r"\s+", " ", full_signature.replace("\n", " "))
                    signatures[current_method] = clean_sig
                    current_method = None
                    method_lines = []

    # Handle the last method
    if current_method and method_lines:
        full_signature = "\n".join(method_lines).strip()
        clean_sig = re.sub(r"\s+", " ", full_signature.replace("\n", " "))
        signatures[current_method] = clean_sig

    return signatures


def normalize_signature(sig: str) -> str:
    """Normalize signature for comparison"""
    # Remove extra whitespace
    normalized = re.sub(r"\s+", " ", sig.strip())
    # Remove async prefix for comparison
    normalized = re.sub(r"^async\s+", "", normalized)
    return normalized


def compare_signatures():
    """Compare signatures between GitHubAgent and GitHubIntegrationRouter"""

    agent_file = "services/integrations/github/github_agent.py"
    router_file = "services/integrations/github/github_integration_router.py"

    print("🔍 Method Signature Comparison")
    print("=" * 50)

    # Extract signatures
    try:
        agent_sigs = extract_method_signatures_from_file(agent_file, "GitHubAgent")
        router_sigs = extract_method_signatures_from_file(router_file, "GitHubIntegrationRouter")
    except Exception as e:
        print(f"❌ Error reading files: {e}")
        return

    print(f"GitHubAgent methods: {len(agent_sigs)}")
    print(f"GitHubIntegrationRouter methods: {len(router_sigs)}")
    print()

    # Find common methods and compare
    common_methods = set(agent_sigs.keys()) & set(router_sigs.keys())
    mismatches = []
    matches = []

    for method in sorted(common_methods):
        agent_sig = normalize_signature(agent_sigs[method])
        router_sig = normalize_signature(router_sigs[method])

        if agent_sig != router_sig:
            mismatches.append(method)
            print(f"❌ {method}")
            print(f"   Agent:  {agent_sig}")
            print(f"   Router: {router_sig}")
            print()
        else:
            matches.append(method)
            print(f"✅ {method}")

    print()
    print(f"✅ Matching signatures: {len(matches)}")
    print(f"❌ Mismatched signatures: {len(mismatches)}")

    if mismatches:
        print(f"\n🚨 Signature mismatches found in: {mismatches}")
        return 1
    else:
        print("🎯 All signatures match!")
        return 0


if __name__ == "__main__":
    exit(compare_signatures())
