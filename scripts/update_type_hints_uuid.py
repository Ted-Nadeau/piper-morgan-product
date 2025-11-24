#!/usr/bin/env python3
"""
Automation script to update user_id type hints from str to UUID.

Issue #262 - UUID Migration
Updates 152 occurrences across ~40 files in services/

Usage:
    python scripts/update_type_hints_uuid.py [--dry-run]
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple


def update_file(filepath: Path, dry_run: bool = False) -> Tuple[bool, int]:
    """
    Update user_id type hints from str to UUID in a single file.

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
        or "from typing import UUID" in content
        or "import uuid" in content
    )

    # Patterns to update
    patterns = [
        # user_id: str -> user_id: UUID
        (r"\buser_id: str\b", "user_id: UUID"),
        # user_id: Optional[str] -> user_id: Optional[UUID]
        (r"\buser_id: Optional\[str\]", "user_id: Optional[UUID]"),
        # owner_id: str -> owner_id: UUID (but NOT for todo_items - see special handling)
        # (r'\bowner_id: str\b', 'owner_id: UUID'),
    ]

    # Special handling: DO NOT convert owner_id in todo-related files
    # (todo_items.owner_id is NOT a user reference)
    is_todo_file = "todo" in filepath.name.lower()

    # Apply patterns
    for pattern, replacement in patterns:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            changes_made += len(matches)

    # Add UUID import if needed and changes were made
    if changes_made > 0 and not has_uuid_import:
        # Find where to add the import
        # Look for existing typing imports
        typing_import_match = re.search(r"^from typing import (.+?)$", content, re.MULTILINE)

        if typing_import_match:
            # Add UUID to existing typing import
            imports = typing_import_match.group(1)
            if "UUID" not in imports:
                # Add UUID to the import list
                new_imports = (
                    imports.rstrip() + ", UUID" if not imports.endswith(",") else imports + " UUID"
                )
                content = content.replace(
                    f"from typing import {imports}", f"from typing import {new_imports}"
                )
        else:
            # No typing import exists, add both typing and uuid imports
            # Find first import statement
            import_match = re.search(r"^(import |from )", content, re.MULTILINE)
            if import_match:
                # Insert before first import
                insert_pos = import_match.start()
                content = content[:insert_pos] + "from uuid import UUID\n" + content[insert_pos:]
            else:
                # No imports at all, add at top after docstring/comments
                lines = content.split("\n")
                insert_line = 0
                for i, line in enumerate(lines):
                    if (
                        line.strip()
                        and not line.strip().startswith("#")
                        and not line.strip().startswith('"""')
                    ):
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

    # Find all Python files in services/
    services_dir = Path(__file__).parent.parent / "services"
    python_files = list(services_dir.rglob("*.py"))

    print(f"📁 Scanning {len(python_files)} Python files in services/\n")

    modified_files: List[Path] = []
    total_changes = 0
    skipped_files = []

    for filepath in python_files:
        # Skip __pycache__ and other non-source files
        if "__pycache__" in str(filepath):
            continue

        # Skip database/models.py (already updated in Phase 2)
        if "database/models.py" in str(filepath):
            print(
                f"⏭️  Skipping {filepath.relative_to(services_dir.parent)} (already updated in Phase 2)"
            )
            skipped_files.append(filepath)
            continue

        # Check if file needs updating
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if "user_id: str" in content or "user_id: Optional[str]" in content:
            modified, count = update_file(filepath, dry_run)

            if modified:
                modified_files.append(filepath)
                total_changes += count
                rel_path = filepath.relative_to(services_dir.parent)
                print(f"✅ {'Would update' if dry_run else 'Updated'} {rel_path} ({count} changes)")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"{'DRY RUN ' if dry_run else ''}SUMMARY:")
    print(f"  Files {'that would be ' if dry_run else ''}modified: {len(modified_files)}")
    print(f"  Total changes: {total_changes}")
    print(f"  Files skipped: {len(skipped_files)}")
    print(f"{'=' * 60}\n")

    if dry_run:
        print("💡 Run without --dry-run to apply changes")
        print("   python scripts/update_type_hints_uuid.py")
    else:
        print("✅ Type hint updates complete!")
        print("\n📝 Next steps:")
        print("   1. Verify changes: git diff services/")
        print("   2. Run tests: pytest tests/")
        print("   3. Proceed to Phase 4 (test updates)")

    return 0 if not dry_run or len(modified_files) > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
