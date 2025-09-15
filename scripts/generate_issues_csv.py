#!/usr/bin/env python3
"""
Generate CSV file of GitHub issues for project planning
Uses GitHubDomainService to fetch issues with proper pagination handling
"""

import asyncio
import csv

# Add project root to path for imports
import sys
from pathlib import Path
from typing import Any, Dict, List

import structlog

sys.path.append(str(Path(__file__).parent.parent))

from services.integrations.github.github_agent import GitHubAgent

logger = structlog.get_logger()


async def fetch_all_issues(github_agent: GitHubAgent) -> List[Dict[str, Any]]:
    """Fetch all issues from the repository using existing GitHub agent methods"""
    all_issues = []

    logger.info("Starting to fetch GitHub issues using existing methods...")

    try:
        # Use existing methods to get recent and closed issues
        # This avoids modifying core Piper code
        logger.info("Fetching recent issues...")
        recent_issues = await github_agent.get_recent_issues(limit=50)  # Get more recent issues
        all_issues.extend(recent_issues)

        logger.info("Fetching closed issues...")
        closed_issues = await github_agent.get_closed_issues(limit=50)  # Get recent closed issues
        all_issues.extend(closed_issues)

        # Remove duplicates based on issue number
        seen_numbers = set()
        unique_issues = []
        for issue in all_issues:
            if issue["number"] not in seen_numbers:
                unique_issues.append(issue)
                seen_numbers.add(issue["number"])

        logger.info(f"Fetched {len(unique_issues)} unique issues")
        return unique_issues

    except Exception as e:
        logger.error(f"Error fetching issues: {e}")
        return []


def process_issues_for_csv(issues: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Process GitHub issues into CSV format"""
    csv_data = []

    for issue in issues:
        # Skip pull requests (they appear as issues in GitHub API)
        if "pull_request" in issue:
            continue

        csv_row = {
            "issue_number": str(issue.get("number", "")),
            "issue_title": issue.get("title", "").replace("\n", " ").replace("\r", " "),
            "status": "Open" if issue.get("state") == "open" else "Closed",
        }
        csv_data.append(csv_row)

    logger.info(f"Processed {len(csv_data)} issues for CSV (excluding PRs)")
    return csv_data


def write_csv_file(csv_data: List[Dict[str, str]], output_path: Path):
    """Write issues data to CSV file"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["issue_number", "issue_title", "status"]

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

    logger.info(f"CSV file written to: {output_path}")
    logger.info(f"Total issues in CSV: {len(csv_data)}")


async def main():
    """Main function to generate issues CSV"""
    try:
        # Initialize GitHub agent directly (no modifications to core code)
        logger.info("Initializing GitHub agent...")
        github_agent = GitHubAgent()

        # Fetch all issues using existing methods
        issues = await fetch_all_issues(github_agent)

        if not issues:
            logger.error("No issues found or failed to fetch issues")
            return

        # Process for CSV
        csv_data = process_issues_for_csv(issues)

        if not csv_data:
            logger.error("No valid issues to write to CSV")
            return

        # Write CSV file
        output_path = Path(__file__).parent.parent / "docs" / "planning" / "issues.csv"
        write_csv_file(csv_data, output_path)

        logger.info("✅ Issues CSV generation completed successfully!")
        print(f"✅ Generated {output_path} with {len(csv_data)} issues")

    except Exception as e:
        logger.error(f"Failed to generate issues CSV: {e}")
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
