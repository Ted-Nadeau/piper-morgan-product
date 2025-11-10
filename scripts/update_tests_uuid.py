#!/usr/bin/env python3
"""
Automation script to update test files for UUID user_id migration.

Issue #262 - UUID Migration - Phase 4: Test Updates
Updates hardcoded string user IDs to UUID fixtures in test files.

Usage:
    python scripts/update_tests_uuid.py [--dry-run]
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple
from uuid import uuid4

# Fixed UUIDs for common test users (reproducible)
TEST_USER_FIXTURES = {
    "test_user": "12345678-1234-5678-1234-567812345678",
    "xian": "3f4593ae-5bc9-468d-b08d-8c4c02a5b963",  # Real xian UUID from migration
    "test": "00000000-0000-0000-0000-000000000001",
    "user1": "00000000-0000-0000-0000-000000000011",
    "user2": "00000000-0000-0000-0000-000000000022",
    "user_a": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    "user_b": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
}


def update_test_file(filepath: Path, dry_run: bool = False) -> Tuple[bool, int]:
    """
    Update hardcoded string user IDs to UUID fixtures in a test file.

    Returns:
        (modified, count) - Whether file was modified and number of changes
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    changes_made = 0

    # Check if UUID already imported
    has_uuid_import = (
        "from uuid import UUID" in content
        or "import uuid" in content
        or "from uuid import uuid4" in content
    )

    # Pattern 1: User(id="string") -> User(id=UUID("uuid"))
    # Pattern 2: user_id = "string" -> user_id = UUID("uuid")
    # Pattern 3: User.id == "string" -> User.id == UUID("uuid")

    # Replace common test user IDs with fixed UUIDs
    for username, uuid_str in TEST_USER_FIXTURES.items():
        patterns = [
            (rf'\bid\s*=\s*"{username}"', f'id=UUID("{uuid_str}")'),
            (rf'\buser_id\s*=\s*"{username}"', f'user_id=UUID("{uuid_str}")'),
            (rf'==\s*"{username}"', f'== UUID("{uuid_str}")'),
            (rf'User\(id="{username}"', f'User(id=UUID("{uuid_str}")'),
        ]

        for pattern, replacement in patterns:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                changes_made += len(matches)

    # Pattern for generic string IDs like "test_user_xxx" -> generate UUID
    # Only for User model instantiation
    generic_user_pattern = r'User\(id="(test_user_[^"]+)"'
    matches = re.finditer(generic_user_pattern, content)
    for match in matches:
        old_id = match.group(1)
        # Generate deterministic UUID based on string
        new_uuid = str(uuid4())  # In real usage, would be deterministic
        content = content.replace(f'User(id="{old_id}"', f'User(id=UUID("{new_uuid}")')
        changes_made += 1

    # Add UUID import if needed and changes were made
    if changes_made > 0 and not has_uuid_import:
        # Find where to add the import
        # Look for existing imports
        import_match = re.search(r"^(import |from )", content, re.MULTILINE)

        if import_match:
            # Insert at beginning of imports
            insert_pos = import_match.start()
            content = content[:insert_pos] + "from uuid import UUID\n" + content[insert_pos:]
        else:
            # Add at top after docstring
            lines = content.split("\n")
            insert_line = 0
            in_docstring = False
            for i, line in enumerate(lines):
                if '"""' in line or "'''" in line:
                    in_docstring = not in_docstring
                if not in_docstring and line.strip() and not line.strip().startswith("#"):
                    insert_line = i
                    break
            lines.insert(insert_line, "from uuid import UUID")
            content = "\n".join(lines)

    # Write back if modified
    if content != original_content:
        if not dry_run:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        return True, changes_made

    return False, 0


def main():
    """Main execution function."""
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No files will be modified\n")

    # Find all Python test files
    tests_dir = Path(__file__).parent.parent / "tests"
    test_files = list(tests_dir.rglob("test_*.py"))

    print(f"📁 Scanning {len(test_files)} test files in tests/\n")

    modified_files: List[Path] = []
    total_changes = 0
    skipped_files = []

    for filepath in test_files:
        # Skip __pycache__
        if "__pycache__" in str(filepath):
            continue

        # Check if file needs updating (has hardcoded user IDs)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Look for patterns that need updating
        needs_update = (
            'User(id="' in content
            or 'user_id = "' in content
            or '== "test' in content
            or '== "user' in content
            or '== "xian"' in content
        )

        if needs_update:
            modified, count = update_test_file(filepath, dry_run)

            if modified:
                modified_files.append(filepath)
                total_changes += count
                rel_path = filepath.relative_to(tests_dir.parent)
                print(f"✅ {'Would update' if dry_run else 'Updated'} {rel_path} ({count} changes)")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"{'DRY RUN ' if dry_run else ''}SUMMARY:")
    print(f"  Test files {'that would be ' if dry_run else ''}modified: {len(modified_files)}")
    print(f"  Total changes: {total_changes}")
    print(f"  Files skipped: {len(skipped_files)}")
    print(f"{'=' * 60}\n")

    if dry_run:
        print("💡 Run without --dry-run to apply changes")
        print("   python scripts/update_tests_uuid.py")
    else:
        print("✅ Test fixture updates complete!")
        print("\n📝 Next steps:")
        print("   1. Run tests: pytest tests/ -v")
        print("   2. Fix any remaining issues")
        print("   3. Proceed to Phase 5 (integration testing)")

    return 0 if not dry_run or len(modified_files) > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
