#!/usr/bin/env python3
"""
Parse smoke test candidates and mark them with @pytest.mark.smoke
Phase 2b: Smoke Test Marking & Validation
"""

import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple


def parse_candidates(candidates_file: str) -> Dict[str, List[Tuple[str, str]]]:
    """
    Parse candidates file and group by test file.

    Returns: {
        "test/file.py": [
            ("TestClass", "test_method"),
            ("test_function", None),
            ...
        ]
    }
    """
    candidates = defaultdict(list)

    with open(candidates_file, "r") as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Parse pytest node ID format: path/to/test.py::Class::method or path/to/test.py::method
            if "::" not in line:
                continue

            parts = line.split("::")
            test_file = parts[0]

            if len(parts) == 3:
                # Format: file::Class::method
                test_class = parts[1]
                test_method = parts[2]
            elif len(parts) == 2:
                # Format: file::method
                test_class = None
                test_method = parts[1]
            else:
                print(f"Warning: Unexpected format: {line}")
                continue

            candidates[test_file].append((test_class, test_method))

    return dict(candidates)


def read_test_file(file_path: Path) -> str:
    """Read test file content."""
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        return None
    except Exception as e:
        print(f"ERROR reading {file_path}: {e}")
        return None


def find_test_function(content: str, class_name: str, method_name: str) -> Tuple[int, str]:
    """
    Find a test function/method in the file content.
    Returns: (line_number, indentation_level) or (None, None) if not found
    """
    lines = content.split("\n")

    if class_name:
        # Find method within class
        in_class = False
        class_indent = None

        for i, line in enumerate(lines):
            # Check if this is the class definition
            if f"class {class_name}" in line:
                in_class = True
                class_indent = len(line) - len(line.lstrip())
                continue

            if in_class:
                # If we hit another class or function at same/lower indent, class is done
                if line.strip() and not line.strip().startswith("#"):
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= class_indent and (
                        line.lstrip().startswith("class ")
                        or line.lstrip().startswith("def ")
                        and not line.lstrip().startswith("def _")
                    ):
                        if not line.lstrip().startswith(f"def {method_name}"):
                            in_class = False
                            continue

                # Look for the method definition
                if f"def {method_name}(" in line:
                    indent = len(line) - len(line.lstrip())
                    return (i, indent)
    else:
        # Find function (not in a class)
        for i, line in enumerate(lines):
            if f"def {method_name}(" in line:
                # Verify it's not indented (not a method)
                if line.startswith("def "):
                    indent = len(line) - len(line.lstrip())
                    return (i, indent)

    return (None, None)


def has_smoke_marker(lines: List[str], start_idx: int) -> bool:
    """Check if function already has @pytest.mark.smoke marker."""
    # Check previous few lines for decorators
    check_range = min(5, start_idx)
    for i in range(start_idx - check_range, start_idx):
        if i >= 0 and "@pytest.mark.smoke" in lines[i]:
            return True
    return False


def mark_tests_in_file(file_path: Path, tests: List[Tuple[str, str]]) -> int:
    """
    Mark specified tests in a file with @pytest.mark.smoke decorator.
    Returns: count of tests marked
    """
    content = read_test_file(file_path)
    if content is None:
        return 0

    lines = content.split("\n")
    marked_count = 0

    # Sort by line number descending so we insert from bottom to top (preserves line numbers)
    test_locations = []

    for class_name, method_name in tests:
        line_idx, indent = find_test_function(content, class_name, method_name)
        if line_idx is not None:
            test_locations.append((line_idx, indent, class_name, method_name))
        else:
            print(
                f"  WARNING: Could not find {class_name or 'module'}::{method_name} in {file_path.name}"
            )

    # Sort by line number descending
    test_locations.sort(reverse=True)

    for line_idx, indent, class_name, method_name in test_locations:
        # Check if already marked
        if has_smoke_marker(lines, line_idx):
            print(f"  SKIP: {class_name or 'module'}::{method_name} - already marked")
            continue

        # Insert decorator before the function
        decorator = " " * indent + "@pytest.mark.smoke"
        lines.insert(line_idx, decorator)
        marked_count += 1

    # Write back if changes made
    if marked_count > 0:
        new_content = "\n".join(lines)
        try:
            with open(file_path, "w") as f:
                f.write(new_content)
        except Exception as e:
            print(f"  ERROR writing {file_path}: {e}")
            return 0

    return marked_count


def main():
    # Verify we're in the right directory
    candidates_file = Path(
        "/Users/xian/Development/piper-morgan/dev/2025/12/09/smoke-test-candidates.txt"
    )
    repo_root = Path("/Users/xian/Development/piper-morgan")

    if not candidates_file.exists():
        print(f"ERROR: Candidates file not found: {candidates_file}")
        sys.exit(1)

    if not repo_root.exists():
        print(f"ERROR: Repository root not found: {repo_root}")
        sys.exit(1)

    print("=" * 80)
    print("Phase 2b: Smoke Test Marking")
    print("=" * 80)

    # Parse candidates
    print("\n1. Parsing candidates file...")
    candidates = parse_candidates(str(candidates_file))
    print(
        f"   Found {len(candidates)} test files with {sum(len(tests) for tests in candidates.values())} candidate tests"
    )

    # Mark tests
    print("\n2. Marking tests...")
    total_marked = 0
    files_modified = 0

    for test_file, tests in sorted(candidates.items()):
        file_path = repo_root / test_file
        if not file_path.exists():
            print(f"  SKIP: {test_file} - file not found")
            continue

        marked = mark_tests_in_file(file_path, tests)
        if marked > 0:
            files_modified += 1
            total_marked += marked
            print(f"  ✓ {test_file}: marked {marked} tests")

    print(f"\n{'=' * 80}")
    print(f"Marking Complete:")
    print(f"  Files modified: {files_modified}")
    print(f"  Tests marked: {total_marked}")
    print(f"{'=' * 80}")

    return 0 if total_marked > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
