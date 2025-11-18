#!/usr/bin/env python3
"""
Validate Markdown files for Jekyll compatibility.

Checks for common issues that break GitHub Pages Jekyll builds:
1. Misplaced --- separators (Jekyll interprets as YAML front matter delimiters)
2. Invalid YAML front matter if present
3. Malformed front matter blocks

Exit codes:
0 - All files valid
1 - Validation errors found
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def check_yaml_separators(filepath: Path, content: str) -> List[str]:
    """Check for problematic --- separators that break Jekyll."""
    errors = []
    lines = content.split("\n")

    # Check if file starts with front matter
    has_front_matter = False
    front_matter_end = -1

    if lines and lines[0].strip() == "---":
        # Look for closing ---
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                has_front_matter = True
                front_matter_end = i
                break

    # Check for --- after front matter (these break Jekyll)
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if has_front_matter:
                # Allow front matter delimiters
                if i == 0 or i == front_matter_end:
                    continue

            # After front matter or in files without front matter,
            # --- is interpreted as a separator and breaks Jekyll
            if i > front_matter_end:
                errors.append(
                    f"Line {i+1}: Jekyll-incompatible '---' separator found. "
                    f"Use blank lines or other formatting instead."
                )

    return errors


def check_yaml_front_matter(filepath: Path, content: str) -> List[str]:
    """Validate YAML front matter if present."""
    errors = []
    lines = content.split("\n")

    if not lines or lines[0].strip() != "---":
        return []  # No front matter, that's fine

    # Find closing ---
    closing_line = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            closing_line = i
            break

    if closing_line == -1:
        errors.append("YAML front matter not properly closed (missing closing '---')")
        return errors

    # Extract YAML content
    yaml_content = "\n".join(lines[1:closing_line])

    # Basic YAML validation (key: value format)
    for i, line in enumerate(lines[1:closing_line], 1):
        line = line.strip()
        if not line:
            continue  # Empty lines are OK
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*\s*:", line):
            errors.append(
                f"Line {i+1}: Invalid YAML format in front matter. "
                f"Expected 'key: value' format."
            )

    return errors


def validate_file(filepath: Path) -> Tuple[bool, List[str]]:
    """Validate a single Markdown file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return False, [f"Error reading file: {e}"]

    errors = []
    errors.extend(check_yaml_separators(filepath, content))
    errors.extend(check_yaml_front_matter(filepath, content))

    return len(errors) == 0, errors


def main():
    """Validate all Markdown files in docs/ directory."""
    docs_dir = Path(__file__).parent.parent / "docs"

    if not docs_dir.exists():
        print(f"❌ docs/ directory not found", file=sys.stderr)
        return 1

    # Find all .md files
    md_files = list(docs_dir.rglob("*.md"))

    if not md_files:
        print("✅ No Markdown files found to validate")
        return 0

    print(f"🔍 Validating {len(md_files)} Markdown files for Jekyll compatibility...")

    all_valid = True
    files_with_errors = []

    for filepath in md_files:
        valid, errors = validate_file(filepath)

        if not valid:
            all_valid = False
            files_with_errors.append((filepath, errors))

    if all_valid:
        print(f"✅ All {len(md_files)} files are Jekyll-compatible")
        return 0
    else:
        print(f"\n❌ Found issues in {len(files_with_errors)} file(s):\n")

        for filepath, errors in files_with_errors:
            rel_path = filepath.relative_to(docs_dir.parent)
            print(f"  {rel_path}:")
            for error in errors:
                print(f"    • {error}")
            print()

        return 1


if __name__ == "__main__":
    sys.exit(main())
