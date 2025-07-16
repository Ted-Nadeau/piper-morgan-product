#!/usr/bin/env python3
"""
GitHub Issue Generator for Piper Morgan Backlog

This script parses docs/planning/backlog.md and generates GitHub issue creation commands
for all PM-XXX tickets that don't already exist in GitHub.

Usage:
    python scripts/generate_github_issues.py
    python scripts/generate_github_issues.py --dry-run
    python scripts/generate_github_issues.py --check-existing
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


class BacklogParser:
    def __init__(self, backlog_path: str = "docs/planning/backlog.md"):
        self.backlog_path = Path(backlog_path)
        self.issues = []

    def parse_backlog(self) -> List[Dict]:
        """Parse backlog.md and extract all PM-XXX issues"""
        if not self.backlog_path.exists():
            print(f"Error: {self.backlog_path} not found")
            return []

        content = self.backlog_path.read_text()

        # Find all PM-XXX sections
        pattern = (
            r"### (PM-\d+): ([^\n]+)\n\n\*\*Story\*\*: ([^\n]+)\n\*\*Description?\*\*: ([^\n]+)"
        )
        matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)

        issues = []
        for match in matches:
            issue_id = match.group(1)
            title = match.group(2).strip()
            story = match.group(3).strip()
            description = match.group(4).strip()

            # Extract additional details
            details = self._extract_issue_details(content, match.start())

            issues.append(
                {
                    "id": issue_id,
                    "title": title,
                    "story": story,
                    "description": description,
                    "details": details,
                    "status": self._extract_status(content, match.start()),
                    "estimate": self._extract_estimate(content, match.start()),
                    "dependencies": self._extract_dependencies(content, match.start()),
                }
            )

        return issues

    def _extract_issue_details(self, content: str, start_pos: int) -> str:
        """Extract implementation details and success criteria"""
        # Look for Implementation Details section
        pattern = r"\*\*Implementation Details\*\*:\n\n((?:- [^\n]+\n)+)"
        match = re.search(pattern, content[start_pos : start_pos + 2000])
        if match:
            return match.group(1).strip()
        return ""

    def _extract_status(self, content: str, start_pos: int) -> str:
        """Extract issue status"""
        pattern = r"\*\*Status\*\*: ([^\n|]+)"
        match = re.search(pattern, content[start_pos : start_pos + 500])
        if match:
            return match.group(1).strip()
        return "Ready"

    def _extract_estimate(self, content: str, start_pos: int) -> str:
        """Extract story points estimate"""
        pattern = r"\*\*Estimate\*\*: ([^\n]+)"
        match = re.search(pattern, content[start_pos : start_pos + 500])
        if match:
            return match.group(1).strip()
        return "TBD"

    def _extract_dependencies(self, content: str, start_pos: int) -> str:
        """Extract dependencies"""
        pattern = r"\*\*Dependencies\*\*: ([^\n]+)"
        match = re.search(pattern, content[start_pos : start_pos + 500])
        if match:
            return match.group(1).strip()
        return "None"


class GitHubIssueGenerator:
    def __init__(self, repo: str = "piper-morgan"):
        self.repo = repo
        self.existing_issues = set()

    def check_existing_issues(self) -> bool:
        """Check which PM-XXX issues already exist in GitHub"""
        try:
            # Use gh CLI to list issues with PM-XXX in title
            result = subprocess.run(
                ["gh", "issue", "list", "--repo", self.repo, "--search", "PM-"],
                capture_output=True,
                text=True,
                check=True,
            )

            # Parse output to extract PM-XXX numbers
            for line in result.stdout.split("\n"):
                if "PM-" in line:
                    # Extract PM-XXX from the line
                    match = re.search(r"PM-\d+", line)
                    if match:
                        self.existing_issues.add(match.group(0))

            print(
                f"Found {len(self.existing_issues)} existing PM issues: {sorted(self.existing_issues)}"
            )
            return True

        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not check existing issues: {e}")
            print("Proceeding without checking existing issues (assume none exist)")
            print("To check existing issues, run: gh auth login")
            return True  # Continue anyway
        except FileNotFoundError:
            print("Warning: GitHub CLI (gh) not found. Install from https://cli.github.com/")
            print("Proceeding without checking existing issues (assume none exist)")
            return True  # Continue anyway

    def generate_issue_command(self, issue: Dict) -> str:
        """Generate gh issue create command for a single issue"""
        if issue["id"] in self.existing_issues:
            return f"# {issue['id']} already exists in GitHub"

        # Build issue body
        body_parts = [
            f"**Story**: {issue['story']}",
            f"**Description**: {issue['description']}",
            f"**Status**: {issue['status']}",
            f"**Estimate**: {issue['estimate']}",
            f"**Dependencies**: {issue['dependencies']}",
        ]

        if issue["details"]:
            body_parts.append(f"\n**Implementation Details**:\n{issue['details']}")

        body = "\n\n".join(body_parts)

        # Escape quotes for shell command
        title_escaped = issue["title"].replace('"', '\\"')
        body_escaped = body.replace('"', '\\"').replace("\n", "\\n")

        return f'gh issue create --repo {self.repo} --title "{issue["id"]}: {title_escaped}" --body "{body_escaped}" --label "enhancement"'

    def generate_all_commands(self, issues: List[Dict], dry_run: bool = False) -> None:
        """Generate commands for all missing issues"""
        missing_issues = [issue for issue in issues if issue["id"] not in self.existing_issues]

        if not missing_issues:
            print("All PM issues already exist in GitHub!")
            return

        print(f"Generating commands for {len(missing_issues)} missing issues:")
        print()

        for issue in missing_issues:
            command = self.generate_issue_command(issue)
            print(f"# {issue['id']}: {issue['title']}")
            print(command)
            print()

        if dry_run:
            print("DRY RUN: No commands executed")
        else:
            print("To execute these commands, run:")
            print("python scripts/generate_github_issues.py")


def main():
    parser = argparse.ArgumentParser(description="Generate GitHub issues from backlog")
    parser.add_argument("--dry-run", action="store_true", help="Show commands without executing")
    parser.add_argument("--check-existing", action="store_true", help="Only check existing issues")
    parser.add_argument(
        "--backlog", default="docs/planning/backlog.md", help="Path to backlog file"
    )

    args = parser.parse_args()

    # Parse backlog
    parser = BacklogParser(args.backlog)
    issues = parser.parse_backlog()

    if not issues:
        print("No issues found in backlog")
        return

    print(f"Found {len(issues)} issues in backlog")

    # Check existing GitHub issues
    generator = GitHubIssueGenerator()
    if not generator.check_existing_issues():
        return

    if args.check_existing:
        return

    # Generate commands
    generator.generate_all_commands(issues, args.dry_run)


if __name__ == "__main__":
    main()
