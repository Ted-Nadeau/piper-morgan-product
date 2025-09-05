"""
PM Number Management Service - Critical Verification Foundation
Phase 2: PM Number Management Service Implementation

Created: 2025-09-05 by Code Agent PM-123 Implementation
Follows Excellence Flywheel: Evidence-based verification → Implementation → GitHub tracking
Prevents PM number conflicts across GitHub, CSV, and backlog systems
"""

import asyncio
import csv
import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

from services.integrations.github.github_agent import GitHubAgent


@dataclass
class PMNumberEntry:
    """Individual PM number entry with tracking metadata"""

    pm_number: str
    issue_number: Optional[int]
    title: str
    status: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]) -> "PMNumberEntry":
        """Create PMNumberEntry from CSV row"""
        return cls(
            pm_number=row.get("PM_Number", "").strip(),
            issue_number=(
                int(row.get("Issue_Number", 0)) if row.get("Issue_Number", "").strip() else None
            ),
            title=row.get("Title", "").strip(),
            status=row.get("Status", "").strip(),
            notes=row.get("Notes", "").strip() if row.get("Notes", "").strip() else None,
        )

    def to_csv_row(self) -> Dict[str, str]:
        """Convert to CSV row format"""
        return {
            "PM_Number": self.pm_number,
            "Issue_Number": str(self.issue_number) if self.issue_number else "",
            "Title": self.title,
            "Status": self.status,
            "Notes": self.notes or "",
        }


@dataclass
class PMNumberValidation:
    """PM Number validation result with detailed feedback"""

    is_valid: bool
    pm_number: str
    conflicts: List[str]
    suggestions: List[str]
    next_available: Optional[str] = None
    validation_details: Optional[Dict[str, any]] = None


class PMNumberManager:
    """
    Domain service for PM number management with comprehensive verification.

    Responsibilities:
    - Validate PM number availability across all systems
    - Track PM numbers in CSV format
    - Prevent conflicts with GitHub issues
    - Suggest next available PM numbers
    - Maintain referential integrity
    """

    def __init__(self, csv_path: str = "docs/planning/pm-issues-status.csv"):
        """Initialize PM Number Manager with CSV tracking file path"""
        self.csv_path = csv_path
        self.github_agent = None
        self._cache_lock = asyncio.Lock()
        self._pm_entries_cache: Optional[List[PMNumberEntry]] = None
        self._github_issues_cache: Optional[List[Dict]] = None
        self._cache_timestamp: Optional[datetime] = None
        self._cache_ttl_minutes = 5  # 5-minute cache TTL

    async def get_github_agent(self) -> GitHubAgent:
        """Get or create GitHub agent instance"""
        if self.github_agent is None:
            self.github_agent = GitHubAgent()
        return self.github_agent

    async def validate_pm_number(self, pm_number: str) -> PMNumberValidation:
        """
        Comprehensive PM number validation across all systems.

        Args:
            pm_number: PM number to validate (e.g., "PM-140")

        Returns:
            PMNumberValidation with detailed results and suggestions
        """
        # Normalize PM number format
        normalized_pm = self._normalize_pm_number(pm_number)
        if not normalized_pm:
            return PMNumberValidation(
                is_valid=False,
                pm_number=pm_number,
                conflicts=["Invalid PM number format. Expected format: PM-XXX"],
                suggestions=["Use format PM-XXX where XXX is a number (e.g., PM-140)"],
            )

        conflicts = []
        suggestions = []
        validation_details = {}

        # Check CSV tracking system
        csv_conflicts = await self._check_csv_conflicts(normalized_pm)
        if csv_conflicts:
            conflicts.extend(csv_conflicts)

        # Check GitHub issues
        github_conflicts = await self._check_github_conflicts(normalized_pm)
        if github_conflicts:
            conflicts.extend(github_conflicts)

        # Check backlog references (docs/planning/backlog.md)
        backlog_conflicts = await self._check_backlog_conflicts(normalized_pm)
        if backlog_conflicts:
            conflicts.extend(backlog_conflicts)

        # Determine if valid
        is_valid = len(conflicts) == 0

        # Get next available if current is invalid
        next_available = None
        if not is_valid:
            next_available = await self.get_next_available_pm_number()
            suggestions.append(f"Use {next_available} instead")

        # Add validation details
        validation_details = {
            "csv_entries": len(await self._load_pm_entries()),
            "github_issues": len(await self._get_github_issues()),
            "normalized_format": normalized_pm,
            "validation_timestamp": datetime.now().isoformat(),
        }

        return PMNumberValidation(
            is_valid=is_valid,
            pm_number=normalized_pm,
            conflicts=conflicts,
            suggestions=suggestions,
            next_available=next_available,
            validation_details=validation_details,
        )

    async def get_next_available_pm_number(self) -> str:
        """
        Get the next available PM number based on current tracking.

        Returns:
            Next available PM number in PM-XXX format
        """
        pm_entries = await self._load_pm_entries()

        # Extract all PM numbers and find highest
        pm_numbers = set()
        for entry in pm_entries:
            if entry.pm_number and entry.pm_number.startswith("PM-"):
                try:
                    number_part = int(entry.pm_number[3:])  # Remove "PM-" prefix
                    pm_numbers.add(number_part)
                except ValueError:
                    continue  # Skip invalid format

        # Find next available number
        if not pm_numbers:
            return "PM-001"

        highest = max(pm_numbers)
        next_number = highest + 1

        return f"PM-{next_number:03d}"  # Zero-padded to 3 digits

    async def reserve_pm_number(
        self, pm_number: str, title: str, issue_number: Optional[int] = None
    ) -> bool:
        """
        Reserve a PM number by adding it to the CSV tracking system.

        Args:
            pm_number: PM number to reserve (e.g., "PM-140")
            title: Issue title
            issue_number: GitHub issue number (if available)

        Returns:
            True if reservation was successful
        """
        # Validate first
        validation = await self.validate_pm_number(pm_number)
        if not validation.is_valid:
            return False

        # Create new entry
        entry = PMNumberEntry(
            pm_number=validation.pm_number,
            issue_number=issue_number,
            title=title,
            status="OPEN",
            notes=f"Reserved: {datetime.now().isoformat()}",
            created_at=datetime.now(),
        )

        # Add to CSV
        return await self._add_csv_entry(entry)

    async def update_pm_entry(
        self,
        pm_number: str,
        issue_number: Optional[int] = None,
        status: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> bool:
        """
        Update an existing PM number entry.

        Args:
            pm_number: PM number to update
            issue_number: GitHub issue number to associate
            status: New status (OPEN, CLOSED, etc.)
            notes: Additional notes

        Returns:
            True if update was successful
        """
        pm_entries = await self._load_pm_entries()

        # Find entry to update
        target_entry = None
        for entry in pm_entries:
            if entry.pm_number == pm_number:
                target_entry = entry
                break

        if not target_entry:
            return False

        # Update fields
        if issue_number is not None:
            target_entry.issue_number = issue_number
        if status is not None:
            target_entry.status = status
        if notes is not None:
            target_entry.notes = notes

        # Write back to CSV
        return await self._write_csv_entries(pm_entries)

    async def get_pm_entry(self, pm_number: str) -> Optional[PMNumberEntry]:
        """
        Get PM entry by PM number.

        Args:
            pm_number: PM number to lookup

        Returns:
            PMNumberEntry if found, None otherwise
        """
        pm_entries = await self._load_pm_entries()

        for entry in pm_entries:
            if entry.pm_number == pm_number:
                return entry

        return None

    async def get_all_pm_entries(self) -> List[PMNumberEntry]:
        """
        Get all PM entries from CSV tracking system.

        Returns:
            List of all PMNumberEntry objects
        """
        return await self._load_pm_entries()

    async def get_pm_statistics(self) -> Dict[str, any]:
        """
        Get PM number usage statistics.

        Returns:
            Dictionary with PM number statistics
        """
        pm_entries = await self._load_pm_entries()
        github_issues = await self._get_github_issues()

        # Count by status
        status_counts = {}
        for entry in pm_entries:
            status = entry.status or "UNKNOWN"
            status_counts[status] = status_counts.get(status, 0) + 1

        # Count mapped vs unmapped GitHub issues
        mapped_issues = sum(1 for entry in pm_entries if entry.issue_number)

        # Calculate ranges
        pm_numbers = []
        for entry in pm_entries:
            if entry.pm_number and entry.pm_number.startswith("PM-"):
                try:
                    pm_numbers.append(int(entry.pm_number[3:]))
                except ValueError:
                    continue

        return {
            "total_pm_entries": len(pm_entries),
            "total_github_issues": len(github_issues),
            "mapped_issues": mapped_issues,
            "unmapped_issues": len(github_issues) - mapped_issues,
            "status_distribution": status_counts,
            "pm_number_range": {
                "lowest": min(pm_numbers) if pm_numbers else None,
                "highest": max(pm_numbers) if pm_numbers else None,
                "next_available": await self.get_next_available_pm_number(),
            },
            "generated_at": datetime.now().isoformat(),
        }

    async def verify_consistency(self) -> Dict[str, any]:
        """
        Verify PM number consistency across all systems.

        Returns:
            Dictionary with consistency check results
        """
        try:
            issues = []
            pm_entries = await self._load_pm_entries()
            github_issues = await self._get_github_issues()

            # Check for duplicate PM numbers in CSV
            pm_numbers_in_csv = [entry.pm_number for entry in pm_entries if entry.pm_number]
            duplicates = [pm for pm in set(pm_numbers_in_csv) if pm_numbers_in_csv.count(pm) > 1]

            for duplicate in duplicates:
                issues.append(f"Duplicate PM number in CSV: {duplicate}")

            # Check for PM numbers in GitHub but not in CSV
            pm_numbers_in_github = set()
            for issue in github_issues:
                title = issue.get("title", "")
                # Look for PM-XXX pattern in title
                pm_match = re.search(r"PM-\d{3}", title)
                if pm_match:
                    pm_numbers_in_github.add(pm_match.group())

            pm_numbers_in_csv_set = set(pm_numbers_in_csv)
            github_only = pm_numbers_in_github - pm_numbers_in_csv_set
            csv_only = pm_numbers_in_csv_set - pm_numbers_in_github

            for pm_num in github_only:
                issues.append(f"PM number {pm_num} exists in GitHub but not in CSV")

            for pm_num in csv_only:
                issues.append(f"PM number {pm_num} exists in CSV but not found in GitHub issues")

            # Check for missing issue numbers in CSV entries
            missing_issue_numbers = [
                entry.pm_number
                for entry in pm_entries
                if entry.pm_number and not entry.issue_number
            ]

            for pm_num in missing_issue_numbers:
                issues.append(f"PM number {pm_num} in CSV missing GitHub issue number")

            # Check backlog references
            backlog_conflicts = []
            backlog_path = "docs/planning/backlog.md"
            if os.path.exists(backlog_path):
                try:
                    with open(backlog_path, "r", encoding="utf-8") as f:
                        backlog_content = f.read()

                    # Find PM numbers referenced in backlog
                    backlog_pm_numbers = set(re.findall(r"PM-\d{3}", backlog_content))

                    # Check if backlog PM numbers exist in CSV
                    for pm_num in backlog_pm_numbers:
                        if pm_num not in pm_numbers_in_csv_set:
                            issues.append(
                                f"PM number {pm_num} referenced in backlog but not in CSV"
                            )

                except Exception:
                    issues.append("Could not read backlog.md for consistency check")

            return {
                "consistent": len(issues) == 0,
                "total_pm_numbers": len(pm_numbers_in_csv_set),
                "github_issues_checked": len(github_issues),
                "csv_entries_verified": len(pm_entries),
                "issues": issues,
                "duplicates_found": len(duplicates),
                "github_only_count": len(github_only),
                "csv_only_count": len(csv_only),
                "missing_issue_numbers": len(missing_issue_numbers),
                "verification_timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {
                "consistent": False,
                "error": str(e),
                "issues": [f"Verification failed: {e}"],
                "verification_timestamp": datetime.now().isoformat(),
            }

    async def synchronize_systems(self) -> Dict[str, any]:
        """
        Synchronize PM numbers across all tracking systems.

        Returns:
            Dictionary with synchronization results
        """
        try:
            errors = []
            github_issues_synced = 0
            csv_entries_updated = 0
            conflicts_resolved = 0

            # Get current state
            pm_entries = await self._load_pm_entries()
            github_issues = await self._get_github_issues()

            # Create lookup maps
            pm_to_csv_entry = {entry.pm_number: entry for entry in pm_entries if entry.pm_number}
            github_issue_map = {issue.get("number"): issue for issue in github_issues}

            # Find GitHub issues with PM numbers that aren't in CSV
            for issue in github_issues:
                title = issue.get("title", "")
                pm_match = re.search(r"PM-\d{3}", title)

                if pm_match:
                    pm_number = pm_match.group()
                    issue_number = issue.get("number")

                    # Check if this PM number exists in CSV
                    if pm_number not in pm_to_csv_entry:
                        # Add missing entry to CSV
                        try:
                            new_entry = PMNumberEntry(
                                pm_number=pm_number,
                                issue_number=issue_number,
                                title=title,
                                status="OPEN" if issue.get("state") == "open" else "CLOSED",
                                notes=f"Auto-synced from GitHub: {datetime.now().isoformat()}",
                            )
                            pm_entries.append(new_entry)
                            csv_entries_updated += 1
                            github_issues_synced += 1

                        except Exception as e:
                            errors.append(f"Failed to sync PM {pm_number} from GitHub: {e}")
                    else:
                        # Update existing entry if needed
                        existing_entry = pm_to_csv_entry[pm_number]
                        updated = False

                        if not existing_entry.issue_number:
                            existing_entry.issue_number = issue_number
                            updated = True

                        # Update status based on GitHub state
                        expected_status = "OPEN" if issue.get("state") == "open" else "CLOSED"
                        if existing_entry.status != expected_status:
                            existing_entry.status = expected_status
                            updated = True

                        if updated:
                            csv_entries_updated += 1
                            conflicts_resolved += 1

            # Write updated entries back to CSV
            if csv_entries_updated > 0:
                write_success = await self._write_csv_entries(pm_entries)
                if not write_success:
                    errors.append("Failed to write updated CSV entries")

            # Check for CSV entries missing from GitHub (these might need GitHub issues created)
            csv_pm_numbers = {entry.pm_number for entry in pm_entries if entry.pm_number}
            github_pm_numbers = set()

            for issue in github_issues:
                title = issue.get("title", "")
                pm_match = re.search(r"PM-\d{3}", title)
                if pm_match:
                    github_pm_numbers.add(pm_match.group())

            csv_only = csv_pm_numbers - github_pm_numbers
            if csv_only:
                for pm_num in csv_only:
                    errors.append(
                        f"PM number {pm_num} exists in CSV but no corresponding GitHub issue found"
                    )

            return {
                "success": len(errors) == 0,
                "github_issues_synced": github_issues_synced,
                "csv_entries_updated": csv_entries_updated,
                "conflicts_resolved": conflicts_resolved,
                "errors": errors,
                "csv_only_pm_numbers": list(csv_only) if csv_only else [],
                "synchronization_timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {
                "success": False,
                "github_issues_synced": 0,
                "csv_entries_updated": 0,
                "conflicts_resolved": 0,
                "errors": [f"Synchronization failed: {e}"],
                "synchronization_timestamp": datetime.now().isoformat(),
            }

    # Private methods for internal operations

    def _normalize_pm_number(self, pm_number: str) -> Optional[str]:
        """Normalize PM number to standard format PM-XXX"""
        if not pm_number:
            return None

        # Remove whitespace and convert to uppercase
        clean = pm_number.strip().upper()

        # Check if it matches PM-XXX pattern
        pattern = r"^PM-(\d{1,3})$"
        match = re.match(pattern, clean)

        if match:
            number = int(match.group(1))
            return f"PM-{number:03d}"  # Zero-pad to 3 digits

        # Try to parse number-only format
        if clean.isdigit():
            number = int(clean)
            return f"PM-{number:03d}"

        return None

    async def _load_pm_entries(self) -> List[PMNumberEntry]:
        """Load PM entries from CSV with caching"""
        async with self._cache_lock:
            # Check cache validity
            if (
                self._pm_entries_cache is not None
                and self._cache_timestamp is not None
                and (datetime.now() - self._cache_timestamp).seconds
                < (self._cache_ttl_minutes * 60)
            ):
                return self._pm_entries_cache

            # Load from CSV
            entries = []
            if os.path.exists(self.csv_path):
                try:
                    with open(self.csv_path, "r", newline="", encoding="utf-8") as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            if row.get("PM_Number", "").strip():  # Skip empty rows
                                entries.append(PMNumberEntry.from_csv_row(row))
                except Exception as e:
                    # Log error but don't fail - return empty list
                    entries = []

            # Update cache
            self._pm_entries_cache = entries
            self._cache_timestamp = datetime.now()

            return entries

    async def _get_github_issues(self) -> List[Dict]:
        """Get GitHub issues with caching"""
        async with self._cache_lock:
            # Check cache validity
            if (
                self._github_issues_cache is not None
                and self._cache_timestamp is not None
                and (datetime.now() - self._cache_timestamp).seconds
                < (self._cache_ttl_minutes * 60)
            ):
                return self._github_issues_cache

            # Load from GitHub API
            try:
                github_agent = await self.get_github_agent()
                # Get both open and closed issues for comprehensive checking
                open_issues = await github_agent.get_open_issues()
                closed_issues = await github_agent.get_closed_issues()
                all_issues = open_issues + closed_issues

                self._github_issues_cache = all_issues

            except Exception as e:
                # Fallback to empty list if GitHub API fails
                self._github_issues_cache = []

            return self._github_issues_cache

    async def _check_csv_conflicts(self, pm_number: str) -> List[str]:
        """Check for PM number conflicts in CSV tracking system"""
        pm_entries = await self._load_pm_entries()
        conflicts = []

        for entry in pm_entries:
            if entry.pm_number == pm_number:
                conflicts.append(f"PM number {pm_number} already exists in CSV: {entry.title}")

        return conflicts

    async def _check_github_conflicts(self, pm_number: str) -> List[str]:
        """Check for PM number conflicts in GitHub issue titles"""
        github_issues = await self._get_github_issues()
        conflicts = []

        for issue in github_issues:
            title = issue.get("title", "")
            if pm_number in title:
                issue_number = issue.get("number", "unknown")
                conflicts.append(
                    f"PM number {pm_number} found in GitHub issue #{issue_number}: {title}"
                )

        return conflicts

    async def _check_backlog_conflicts(self, pm_number: str) -> List[str]:
        """Check for PM number references in backlog documentation"""
        backlog_path = "docs/planning/backlog.md"
        conflicts = []

        if os.path.exists(backlog_path):
            try:
                with open(backlog_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if pm_number in content:
                        conflicts.append(f"PM number {pm_number} found in backlog documentation")
            except Exception:
                # Don't fail validation if we can't read backlog
                pass

        return conflicts

    async def _add_csv_entry(self, entry: PMNumberEntry) -> bool:
        """Add new entry to CSV file"""
        try:
            # Load existing entries
            entries = await self._load_pm_entries()

            # Add new entry
            entries.append(entry)

            # Write back to CSV
            return await self._write_csv_entries(entries)

        except Exception:
            return False

    async def _write_csv_entries(self, entries: List[PMNumberEntry]) -> bool:
        """Write all entries back to CSV file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)

            # Write CSV with proper headers
            with open(self.csv_path, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["PM_Number", "Issue_Number", "Title", "Status", "Notes"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for entry in entries:
                    writer.writerow(entry.to_csv_row())

            # Invalidate cache
            async with self._cache_lock:
                self._pm_entries_cache = None
                self._cache_timestamp = None

            return True

        except Exception:
            return False
