#!/usr/bin/env python3
"""
Pre-commit hook to prevent hallucinated GitHub URLs from being committed.

Blocks commits containing 'Codewarrior1988' to prevent the spread of
this hallucinated GitHub username that has repeatedly infected the codebase.
"""

import re
import sys
from pathlib import Path


def check_file(filepath: Path) -> list[str]:
    """Check a single file for hallucinated URLs."""
    errors = []

    # Skip the hook file itself
    if filepath.name == "check-hallucinated-urls.py":
        return errors

    try:
        content = filepath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        # Skip binary files or files that can't be read
        return errors

    # Check for the hallucinated username
    if "Codewarrior1988" in content:
        lines = content.split("\n")
        for line_num, line in enumerate(lines, 1):
            if "Codewarrior1988" in line:
                # Allow if it's in a CORRECTED note, warning text, or documenting the bug
                if (
                    "[CORRECTED" in line
                    or "NEVER use" in line
                    or "is NOT" in line
                    or "hallucinated" in line.lower()
                    or "fabricated" in line.lower()
                ):
                    continue
                errors.append(
                    f"{filepath}:{line_num}: Contains hallucinated GitHub URL 'Codewarrior1988'. "
                    f"Use 'mediajunkie/piper-morgan-product' instead."
                )

    return errors


def main():
    """Check all staged files."""
    import subprocess

    # Get list of staged files
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Error: Could not get list of staged files", file=sys.stderr)
        return 1

    staged_files = [f for f in result.stdout.strip().split("\n") if f]

    if not staged_files:
        return 0

    all_errors = []
    for filename in staged_files:
        filepath = Path(filename)
        if filepath.exists():
            errors = check_file(filepath)
            all_errors.extend(errors)

    if all_errors:
        print("❌ Hallucinated GitHub URL detected!", file=sys.stderr)
        print("", file=sys.stderr)
        for error in all_errors:
            print(f"  {error}", file=sys.stderr)
        print("", file=sys.stderr)
        print("The correct GitHub repository is:", file=sys.stderr)
        print("  https://github.com/mediajunkie/piper-morgan-product", file=sys.stderr)
        print("", file=sys.stderr)
        print("'Codewarrior1988' is a hallucinated URL that keeps spreading.", file=sys.stderr)
        print("Please fix these occurrences before committing.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
