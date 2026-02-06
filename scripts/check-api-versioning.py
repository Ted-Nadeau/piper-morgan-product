#!/usr/bin/env python3
"""
Pre-commit hook to enforce API versioning convention.

All API endpoints must use the /api/v1/ prefix. This prevents:
- Silent 404 errors from inconsistent paths
- API version drift
- Frontend/backend path mismatches

Run manually: python3 scripts/check-api-versioning.py
"""

import re
import sys
from pathlib import Path

# Patterns that indicate wrong API paths (missing v1)
# Note: /api/admin/ is allowed as admin endpoints are versioned separately
WRONG_PATTERNS = [
    # JavaScript fetch calls - allow /api/v1/ and /api/admin/
    (r'fetch\(["\']\/api\/(?!v1\/|admin\/)', "fetch() call missing /api/v1/ prefix"),
    # Python route decorators - allow /api/v1/ and /api/admin/
    (
        r'@(?:app|router)\.(get|post|put|delete|patch)\(["\']\/api\/(?!v1|admin)',
        "Route decorator missing /api/v1/ prefix",
    ),
    # Router prefix definitions - allow /api/v1/ and /api/admin/
    (r'APIRouter\(prefix=["\']\/api\/(?!v1|admin)', "APIRouter prefix missing /api/v1/"),
]

# Files/directories to scan
SCAN_PATHS = [
    "web/",
    "templates/",
    "services/",
]

# Files to exclude (historical/backup)
EXCLUDE_PATTERNS = [
    ".backup",
    "backup-",
    "/docs/",  # Documentation may reference old paths
    "__pycache__",
]

# Line patterns to skip (comments, docstrings)
SKIP_LINE_PATTERNS = [
    r"^\s*#",  # Python comments
    r"^\s*//",  # JavaScript comments
    r"^\s*\*",  # Block comment lines
    r'^\s*"""',  # Docstring start/end
    r"^\s*'''",  # Single-quote docstring
]


def should_exclude(path: str) -> bool:
    """Check if path should be excluded from scanning."""
    return any(excl in path for excl in EXCLUDE_PATTERNS)


def is_comment_or_docstring(line: str) -> bool:
    """Check if a line is a comment or part of a docstring."""
    for skip_pattern in SKIP_LINE_PATTERNS:
        if re.match(skip_pattern, line):
            return True
    return False


def is_in_docstring(content: str, position: int) -> bool:
    """Check if position is inside a multi-line docstring."""
    # Count triple quotes before position
    before = content[:position]
    triple_double = before.count('"""')
    triple_single = before.count("'''")

    # If odd number of triple quotes, we're inside a docstring
    return (triple_double % 2 == 1) or (triple_single % 2 == 1)


def scan_file(filepath: Path) -> list:
    """Scan a single file for API versioning violations."""
    violations = []

    try:
        content = filepath.read_text()
    except UnicodeDecodeError:
        return []  # Skip binary files

    lines = content.split("\n")

    for pattern, description in WRONG_PATTERNS:
        matches = re.finditer(pattern, content)
        for match in matches:
            # Find line number
            line_num = content[: match.start()].count("\n") + 1

            # Skip if the line is a comment or docstring
            if line_num <= len(lines):
                line_content = lines[line_num - 1]
                if is_comment_or_docstring(line_content):
                    continue

            # Skip if inside a multi-line docstring
            if is_in_docstring(content, match.start()):
                continue

            violations.append(
                {
                    "file": str(filepath),
                    "line": line_num,
                    "description": description,
                    "match": match.group()[:60],  # Truncate for readability
                }
            )

    return violations


def main():
    """Main entry point."""
    all_violations = []

    for scan_path in SCAN_PATHS:
        path = Path(scan_path)
        if not path.exists():
            continue

        # Scan Python and HTML/JS files
        for ext in ["*.py", "*.html", "*.js"]:
            for filepath in path.rglob(ext):
                if should_exclude(str(filepath)):
                    continue
                violations = scan_file(filepath)
                all_violations.extend(violations)

    if all_violations:
        print(f"❌ FOUND {len(all_violations)} API VERSIONING VIOLATION(S):")
        print()
        for v in all_violations:
            print(f"  {v['file']}:{v['line']}")
            print(f"    Issue: {v['description']}")
            print(f"    Match: {v['match']}...")
            print()
        print("All API endpoints must use /api/v1/ prefix.")
        print("See CLAUDE.md 'API Conventions' section for details.")
        sys.exit(1)
    else:
        print("✅ API VERSIONING: All endpoints use /api/v1/ prefix")
        sys.exit(0)


if __name__ == "__main__":
    main()
