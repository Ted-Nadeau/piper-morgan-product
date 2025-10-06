"""Find all hardcoded user context in handlers - GREAT-4C Phase 0."""

import re
from pathlib import Path


def audit_hardcoded_context():
    """Find hardcoded user references."""

    patterns = [
        r'"VA"',
        r"'VA'",
        r'"Kind Systems"',
        r"'Kind Systems'",
        r'if.*"VA".*in',
        r'config.*"VA"',
        r'"VA Q4"',
        r"'VA Q4'",
        r'"VA\/Kind"',
        r"'VA\/Kind'",
    ]

    handlers_file = Path("services/intent_service/canonical_handlers.py")

    if not handlers_file.exists():
        print(f"ERROR: {handlers_file} not found")
        return []

    content = handlers_file.read_text()

    findings = []
    for i, line in enumerate(content.split("\n"), 1):
        for pattern in patterns:
            if re.search(pattern, line):
                findings.append({"line": i, "content": line.strip(), "pattern": pattern})

    return findings


if __name__ == "__main__":
    findings = audit_hardcoded_context()

    print("=" * 80)
    print("HARDCODED CONTEXT AUDIT - GREAT-4C Phase 0")
    print("=" * 80)
    print(f"\nFound {len(findings)} hardcoded references:\n")

    for f in findings:
        print(f"  Line {f['line']:3}: {f['content']}")
        print(f"           Pattern: {f['pattern']}")
        print()

    if len(findings) == 0:
        print("✅ No hardcoded context found - handlers are multi-user ready!")
    else:
        print(f"⚠️  Found {len(findings)} hardcoded references that need fixing")

    print("\n" + "=" * 80)
