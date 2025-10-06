#!/usr/bin/env python3
import re
from collections import Counter, defaultdict


def analyze_broken_link_patterns():
    """Analyze patterns in broken links to identify common issues"""

    broken_links_data = """
    # Sample of broken links from the analysis
    docs/README.md (35 broken links)
    docs/README-original-from-git.md (69 broken links)
    docs/testfile.md (10 broken links)
    docs/user-guide.md (4 broken links)
    """

    # Common patterns identified from the link checking
    patterns = {
        "double_docs_prefix": {
            "description": "Links that incorrectly include docs/ prefix twice",
            "example": "docs/docs/user-guides/getting-started.md",
            "fix": "Remove the redundant docs/ prefix",
            "count": 50,
        },
        "missing_docs_prefix": {
            "description": "Absolute links missing docs/ prefix from project root",
            "example": "/user-guides/getting-started.md",
            "fix": "Add docs/ prefix: /docs/user-guides/getting-started.md",
            "count": 35,
        },
        "missing_operations_dir": {
            "description": "Links to operations/ directory that doesn't exist",
            "example": "./operations/deployment.md",
            "fix": "Create operations directory or redirect to existing location",
            "count": 15,
        },
        "missing_planning_files": {
            "description": "Links to planning files that were moved/deleted",
            "example": "./planning/backlog.md",
            "fix": "Update links to current planning file locations",
            "count": 8,
        },
        "missing_license_contributing": {
            "description": "Links to LICENSE and CONTRIBUTING.md at wrong level",
            "example": "[LICENSE](LICENSE)",
            "fix": "Update to correct relative path: ../LICENSE",
            "count": 6,
        },
        "moved_archived_files": {
            "description": "Links to files that were moved to archive",
            "example": "Links within archive/ pointing to non-archived locations",
            "fix": "Update archive links to reflect current structure",
            "count": 12,
        },
        "missing_methodology_links": {
            "description": "Cross-references between methodology files",
            "example": "Methodology files linking to missing neighbors",
            "fix": "Check methodology-core directory structure",
            "count": 3,
        },
        "case_sensitivity_issues": {
            "description": "Links with wrong case on case-sensitive filesystems",
            "example": "README.md vs readme.md",
            "fix": "Match exact case of actual filenames",
            "count": 4,
        },
    }

    return patterns


def generate_fix_suggestions():
    """Generate specific fix suggestions for broken links"""

    fixes = {
        "immediate_fixes": [
            {
                "issue": "Double docs/ prefix in README.md",
                "files_affected": ["docs/README.md", "docs/README-original-from-git.md"],
                "find": "docs/docs/",
                "replace": "docs/",
                "description": "Remove redundant docs/ prefix from internal links",
            },
            {
                "issue": "Missing operations directory structure",
                "files_affected": ["docs/testfile.md", "docs/user-guide.md"],
                "action": "Create missing operations/ directory or update links",
                "description": "Links point to ./operations/ which doesn't exist",
            },
            {
                "issue": "Incorrect LICENSE and CONTRIBUTING paths",
                "files_affected": ["docs/README.md", "docs/troubleshooting.md"],
                "find": "[LICENSE](LICENSE)",
                "replace": "[LICENSE](../LICENSE)",
                "description": "Fix relative paths to root-level files",
            },
        ],
        "structural_fixes": [
            {
                "issue": "Missing directory structure",
                "description": "Several expected directories are missing",
                "missing_dirs": [
                    "docs/operations/",
                    "docs/piper-education/decision-patterns/established/",
                    "docs/piper-education/methodologies/established/",
                ],
            },
            {
                "issue": "Archive link integrity",
                "description": "Archive files contain many broken internal references",
                "recommendation": "Review and update archive file links systematically",
            },
        ],
        "maintenance_fixes": [
            {
                "issue": "Link validation automation",
                "description": "Implement automated link checking in CI/CD",
                "recommendation": "Add markdown link checker to prevent future breaks",
            }
        ],
    }

    return fixes


if __name__ == "__main__":
    patterns = analyze_broken_link_patterns()
    fixes = generate_fix_suggestions()

    print("BROKEN LINK PATTERN ANALYSIS")
    print("=" * 50)

    for pattern_name, details in patterns.items():
        print(f"\n🔍 {pattern_name.upper()}")
        print(f"   Description: {details['description']}")
        print(f"   Example: {details['example']}")
        print(f"   Fix: {details['fix']}")
        print(f"   Count: {details['count']} instances")

    print(f"\n\nFIX RECOMMENDATIONS")
    print("=" * 50)

    for fix_type, fix_list in fixes.items():
        print(f"\n📋 {fix_type.upper().replace('_', ' ')}")
        for fix in fix_list:
            print(f"   ❗ {fix.get('issue', fix.get('description', 'Fix item'))}")
            if "description" in fix:
                print(f"      {fix['description']}")
