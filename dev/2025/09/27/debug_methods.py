#!/usr/bin/env python3
"""Debug method extraction"""

import re


def main():
    with open("services/integrations/github/github_integration_router.py", "r") as f:
        content = f.read()

    # Find all method definitions in the file
    all_methods = re.findall(r"(async\s+)?def\s+(\w+)\s*\([^)]*\)", content)

    print("🔍 ALL METHOD DEFINITIONS FOUND:")
    print("=" * 40)

    class_methods = []
    module_functions = []

    lines = content.split("\n")

    for i, line in enumerate(lines):
        if re.search(r"(async\s+)?def\s+\w+\s*\(", line):
            method_match = re.search(r"(async\s+)?def\s+(\w+)\s*\(", line)
            if method_match:
                method_name = method_match.group(2)

                # Check indentation to determine if it's a class method
                if line.startswith("    ") and not line.startswith("        "):
                    class_methods.append(method_name)
                    print(f"  CLASS: {method_name} (line {i+1})")
                elif not line.startswith(" "):
                    module_functions.append(method_name)
                    print(f"MODULE: {method_name} (line {i+1})")

    print()
    print(f"Class methods: {len(class_methods)}")
    print(f"Module functions: {len(module_functions)}")
    print()
    print("Class methods list:")
    for method in sorted(class_methods):
        print(f"  - {method}")


if __name__ == "__main__":
    main()
