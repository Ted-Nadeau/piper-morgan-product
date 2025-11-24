#!/usr/bin/env python3
r"""
Pre-commit hook to prevent Windows-illegal characters in filenames.

Windows forbids the following characters in filenames:
- : (colon)
- < (less than)
- > (greater than)
- " (double quote)
- / (forward slash - path separator)
- \ (backslash - path separator)
- | (pipe)
- ? (question mark)
- * (asterisk)

This hook checks all staged files and directories for these characters
and prevents the commit if any are found.
"""

import subprocess
import sys
from pathlib import Path

# Windows-illegal characters in filenames
ILLEGAL_CHARS = {
    ":": "colon",
    "<": "less-than",
    ">": "greater-than",
    '"': "double-quote",
    "|": "pipe",
    "?": "question-mark",
    "*": "asterisk",
}

# Forward slash and backslash are path separators, not illegal in individual filenames
# but we should be aware of them


def check_filename(filepath):
    """
    Check if a filename contains Windows-illegal characters.

    Args:
        filepath: Path to check

    Returns:
        Tuple of (is_valid, list_of_illegal_chars)
    """
    path = Path(filepath)

    # Check all parts of the path (directories and filename)
    for part in path.parts:
        for char, char_name in ILLEGAL_CHARS.items():
            if char in part:
                return False, [(char, char_name)]

    return True, []


def main():
    """
    Check all staged files for Windows-illegal characters.

    Returns:
        0 if all files are valid
        1 if any illegal characters found
    """
    # Get list of staged files from git
    try:
        result = subprocess.run(
            ["git", "diff-index", "--cached", "--diff-filter=ACM", "--name-only", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            # If there's no HEAD (initial commit), use git ls-files instead
            result = subprocess.run(
                ["git", "ls-files", "--cached", "--exclude-standard"],
                capture_output=True,
                text=True,
                check=True,
            )

        staged_files = result.stdout.strip().split("\n")
        staged_files = [f for f in staged_files if f]  # Remove empty strings

    except subprocess.CalledProcessError as e:
        print(f"Error getting staged files: {e}", file=sys.stderr)
        return 1

    if not staged_files:
        return 0

    # Check each staged file
    violations = []
    for filepath in staged_files:
        is_valid, illegal = check_filename(filepath)
        if not is_valid:
            violations.append((filepath, illegal))

    # Report violations
    if violations:
        print(
            "❌ Pre-commit hook: Windows-illegal characters found in filenames\n",
            file=sys.stderr,
        )

        for filepath, illegal_chars in violations:
            for char, char_name in illegal_chars:
                print(
                    f"   {filepath}",
                    file=sys.stderr,
                )
                print(
                    f"   └─ Contains illegal character: '{char}' ({char_name})",
                    file=sys.stderr,
                )
                print(
                    f"   └─ Suggested fix: Replace '{char}' with '-' (dash)",
                    file=sys.stderr,
                )
                print()

        print(
            'Windows filenames cannot contain: : < > " | ? *',
            file=sys.stderr,
        )
        print(
            "Use dashes (-) or underscores (_) instead.",
            file=sys.stderr,
        )
        print()
        print(
            "To bypass this check (not recommended): git commit --no-verify",
            file=sys.stderr,
        )

        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
