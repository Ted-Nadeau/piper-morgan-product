#!/usr/bin/env python3
"""
Piper Morgan Completion Validator v1.0
Validates that GitHub issue acceptance criteria are complete.

Usage:
    python scripts/validate-completion.py <issue-number>
    python scripts/validate-completion.py 300

Returns:
    Exit 0 if all criteria met
    Exit 1 if criteria incomplete
"""

import sys
import subprocess
import re
from typing import Tuple, List


def fetch_issue(issue_number: int) -> str:
    """Fetch issue body from GitHub using gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "issue", "view", str(issue_number), "--json", "body", "--jq", ".body"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching issue #{issue_number}: {e.stderr}", file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError:
        print("❌ GitHub CLI (gh) not found. Install from: https://cli.github.com", file=sys.stderr)
        sys.exit(2)


def find_acceptance_criteria_section(body: str) -> str:
    """Extract the Acceptance Criteria section from issue body."""
    # Look for "## Acceptance Criteria" heading (with various case/formatting)
    pattern = r'##\s+Acceptance\s+Criteria.*?(?=\n##|\Z)'
    match = re.search(pattern, body, re.IGNORECASE | re.DOTALL)
    
    if not match:
        # Try alternate heading formats
        pattern = r'###\s+Acceptance\s+Criteria.*?(?=\n###|\n##|\Z)'
        match = re.search(pattern, body, re.IGNORECASE | re.DOTALL)
    
    if not match:
        return ""
    
    return match.group(0)


def parse_checkboxes(text: str) -> Tuple[List[str], List[str]]:
    """
    Parse markdown checkboxes into checked and unchecked lists.
    
    Returns:
        (checked_items, unchecked_items)
    """
    # Patterns for checked and unchecked boxes
    checked_pattern = r'[-*]\s+\[x\]\s+(.+?)(?=\n|$)'
    unchecked_pattern = r'[-*]\s+\[ \]\s+(.+?)(?=\n|$)'
    
    checked = re.findall(checked_pattern, text, re.IGNORECASE | re.MULTILINE)
    unchecked = re.findall(unchecked_pattern, text, re.IGNORECASE | re.MULTILINE)
    
    return checked, unchecked


def validate_acceptance_criteria(issue_number: int) -> bool:
    """
    Validate that all acceptance criteria checkboxes are checked.
    
    Returns:
        True if all criteria met, False otherwise
    """
    print(f"🔍 Validating issue #{issue_number}...")
    
    # Fetch issue
    body = fetch_issue(issue_number)
    
    if not body:
        print("❌ Issue body is empty", file=sys.stderr)
        return False
    
    # Find acceptance criteria section
    criteria_section = find_acceptance_criteria_section(body)
    
    if not criteria_section:
        print("⚠️  No 'Acceptance Criteria' section found in issue", file=sys.stderr)
        print("   (This might be okay if issue doesn't use acceptance criteria)")
        return True  # Pass if no criteria section (not all issues have one)
    
    # Parse checkboxes
    checked, unchecked = parse_checkboxes(criteria_section)
    
    total = len(checked) + len(unchecked)
    
    if total == 0:
        print("⚠️  No checkboxes found in Acceptance Criteria section")
        return True  # Pass if no checkboxes (criteria might be prose)
    
    # Report results
    print(f"\n📋 Acceptance Criteria Status:")
    print(f"   ✅ Checked: {len(checked)}")
    print(f"   ⬜ Unchecked: {len(unchecked)}")
    print(f"   📊 Total: {total}")
    
    if unchecked:
        print(f"\n❌ INCOMPLETE: {len(unchecked)} criteria remaining:\n")
        for i, item in enumerate(unchecked, 1):
            # Truncate long items
            display = item[:80] + "..." if len(item) > 80 else item
            print(f"   {i}. {display}")
        print()
        return False
    
    print(f"\n✅ SUCCESS: All {total} acceptance criteria met!")
    return True


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate-completion.py <issue-number>", file=sys.stderr)
        print("Example: python scripts/validate-completion.py 300", file=sys.stderr)
        sys.exit(1)
    
    try:
        issue_number = int(sys.argv[1])
    except ValueError:
        print(f"❌ Invalid issue number: {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)
    
    # Run validation
    passed = validate_acceptance_criteria(issue_number)
    
    # Exit with appropriate code
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
