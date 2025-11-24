"""
Structural Analysis - Architectural evolution via Serena MCP and git.

Detects:
- ADR creation and evolution
- Class/interface creation and changes
- Major refactoring events (>20 files)
- Import graph evolution
- Architectural pattern adoption
"""

import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from git import Repo

from .base import BaseAnalyzer, BreakthroughSignal


class StructuralAnalyzer(BaseAnalyzer):
    """
    Analyzes structural/architectural patterns in codebase evolution.

    Uses git history to track file system changes and ADR documentation.
    Can be extended with Serena MCP for deep symbolic analysis.
    """

    def __init__(self, project_root: Path):
        super().__init__(project_root)
        self.repo = Repo(project_root)
        self.adr_dir = project_root / "docs" / "internal" / "architecture" / "current" / "adrs"

    async def analyze(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Run structural analysis for specified time period.

        Returns:
            Dict with keys:
            - adr_activity: ADR creation and updates
            - refactoring_events: Major code restructuring
            - class_evolution: New classes/interfaces
            - import_changes: Dependency graph evolution
            - architectural_patterns: Pattern adoption
        """
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=30)

        # Track ADR creation and updates
        adr_activity = self._analyze_adr_activity(start_date, end_date)

        # Detect major refactoring events
        refactoring_events = self._detect_refactoring_events(start_date, end_date)

        # Track class/interface creation
        class_evolution = self._analyze_class_evolution(start_date, end_date)

        # Analyze import graph changes
        import_changes = self._analyze_import_changes(start_date, end_date)

        # Detect architectural pattern adoption
        architectural_patterns = self._detect_architectural_patterns(start_date, end_date)

        self.results = {
            "adr_activity": adr_activity,
            "refactoring_events": refactoring_events,
            "class_evolution": class_evolution,
            "import_changes": import_changes,
            "architectural_patterns": architectural_patterns,
            "analysis_period": {
                "start": self._format_date(start_date),
                "end": self._format_date(end_date),
            },
        }

        return self.results

    def _analyze_adr_activity(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Track ADR creation and modification activity.

        Returns:
            Dict with ADR creation events and summary
        """
        adr_events = []
        adr_files = list(self.adr_dir.glob("adr-*.md")) if self.adr_dir.exists() else []

        for adr_file in adr_files:
            # Extract ADR number
            match = re.match(r"adr-(\d+)-(.+)\.md", adr_file.name)
            if not match:
                continue

            adr_num, adr_slug = match.groups()

            # Get file creation/modification dates from git
            try:
                # Use git log --follow to track file through renames/moves
                # --diff-filter=A finds the actual creation (Added) commit
                import subprocess

                result = subprocess.run(
                    [
                        "git",
                        "log",
                        "--follow",
                        "--diff-filter=A",
                        "--format=%ct %H",
                        "--",
                        str(adr_file.relative_to(self.project_root)),
                    ],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0 and result.stdout.strip():
                    # Parse timestamp and commit hash
                    timestamp_str, commit_hash = result.stdout.strip().split()
                    creation_date = datetime.fromtimestamp(int(timestamp_str))
                    creation_commit = self.repo.commit(commit_hash)

                    if start_date <= creation_date <= end_date:
                        # Parse ADR title from file
                        try:
                            content = adr_file.read_text(encoding="utf-8")
                            title_match = re.search(r"^#\s+ADR-\d+:\s*(.+)$", content, re.MULTILINE)
                            title = title_match.group(1) if title_match else adr_slug

                            adr_events.append(
                                {
                                    "adr_number": adr_num,
                                    "title": title,
                                    "file": adr_file.name,
                                    "created": self._format_date(creation_date),
                                    "commit": creation_commit.hexsha[:8],
                                    "author": creation_commit.author.name,
                                }
                            )
                        except (UnicodeDecodeError, AttributeError):
                            pass

            except Exception:
                continue

        return {
            "events": sorted(adr_events, key=lambda x: x["created"]),
            "total_adrs_created": len(adr_events),
            "adr_creation_rate": len(adr_events) / max(1, (end_date - start_date).days),
        }

    def _detect_refactoring_events(
        self, start_date: datetime, end_date: datetime, file_threshold: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Detect major refactoring events (commits affecting many files).

        Args:
            file_threshold: Minimum files changed to qualify as refactoring

        Returns:
            List of refactoring events
        """
        refactoring_events = []

        for commit in self.repo.iter_commits(since=start_date, until=end_date):
            files_changed = len(commit.stats.files)

            if files_changed >= file_threshold:
                commit_date = datetime.fromtimestamp(commit.committed_date)

                # Classify refactoring type
                refactor_type = "major_refactoring"
                if files_changed >= 50:
                    refactor_type = "architectural_overhaul"
                elif "refactor" in commit.message.lower():
                    refactor_type = "targeted_refactoring"

                refactoring_events.append(
                    {
                        "date": self._format_date(commit_date),
                        "commit": commit.hexsha[:8],
                        "message": commit.message.split("\n")[0][:100],
                        "files_changed": files_changed,
                        "lines_added": commit.stats.total["insertions"],
                        "lines_deleted": commit.stats.total["deletions"],
                        "type": refactor_type,
                        "author": commit.author.name,
                    }
                )

        return sorted(refactoring_events, key=lambda x: x["files_changed"], reverse=True)

    def _analyze_class_evolution(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Track creation of new classes/interfaces.

        Returns:
            Dict with class creation events and patterns
        """
        class_pattern = re.compile(r"^class\s+(\w+)\(?(.*?)\)?:", re.MULTILINE)
        new_classes = []

        # Get all Python file changes in the period
        for commit in self.repo.iter_commits(since=start_date, until=end_date):
            commit_date = datetime.fromtimestamp(commit.committed_date)

            # Look at Python files in the commit
            for file_path in commit.stats.files:
                if not file_path.endswith(".py"):
                    continue

                try:
                    # Get diff to find new classes
                    diffs = commit.diff(commit.parents[0] if commit.parents else None)

                    for diff in diffs:
                        if diff.a_path == file_path or diff.b_path == file_path:
                            if diff.new_file or (diff.diff and b"+class " in diff.diff):
                                # Parse classes from diff
                                diff_text = diff.diff.decode("utf-8") if diff.diff else ""
                                added_lines = [
                                    line[1:]
                                    for line in diff_text.split("\n")
                                    if line.startswith("+")
                                ]
                                added_text = "\n".join(added_lines)

                                classes = class_pattern.findall(added_text)
                                for class_name, base_classes in classes:
                                    new_classes.append(
                                        {
                                            "class_name": class_name,
                                            "base_classes": base_classes.strip(),
                                            "file": file_path,
                                            "date": self._format_date(commit_date),
                                            "commit": commit.hexsha[:8],
                                        }
                                    )

                except Exception:
                    continue

        # Identify patterns in class creation
        base_class_counts = Counter(c["base_classes"] for c in new_classes if c["base_classes"])

        return {
            "new_classes": new_classes[:20],  # Limit to 20 most recent
            "total_classes_created": len(new_classes),
            "common_base_classes": dict(base_class_counts.most_common(5)),
            "classes_per_day": len(new_classes) / max(1, (end_date - start_date).days),
        }

    def _analyze_import_changes(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Track changes in import patterns (coupling/decoupling).

        Returns:
            Dict with import evolution metrics
        """
        import_pattern = re.compile(r"^(?:from|import)\s+([\w.]+)", re.MULTILINE)
        import_timeline = defaultdict(list)

        # Sample commits to avoid excessive processing
        commit_count = 0
        sample_interval = 5  # Sample every 5th commit

        for commit in self.repo.iter_commits(since=start_date, until=end_date):
            commit_count += 1
            if commit_count % sample_interval != 0:
                continue

            commit_date = datetime.fromtimestamp(commit.committed_date)

            # Get imports from Python files
            for file_path in commit.stats.files:
                if file_path.endswith(".py"):
                    try:
                        file_content = (commit.tree / file_path).data_stream.read().decode("utf-8")
                        imports = import_pattern.findall(file_content)

                        for imp in imports:
                            # Track top-level module
                            top_level = imp.split(".")[0]
                            import_timeline[top_level].append(
                                {"date": self._format_date(commit_date), "file": file_path}
                            )

                    except Exception:
                        continue

        # Calculate import diversity
        unique_imports = len(import_timeline)
        total_import_uses = sum(len(uses) for uses in import_timeline.values())

        return {
            "unique_modules_imported": unique_imports,
            "total_import_uses": total_import_uses,
            "top_imported_modules": [
                {"module": mod, "usage_count": len(uses)}
                for mod, uses in sorted(
                    import_timeline.items(), key=lambda x: len(x[1]), reverse=True
                )[:10]
            ],
        }

    def _detect_architectural_patterns(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """
        Detect adoption of architectural patterns.

        Looks for pattern indicators in code and documentation.

        Returns:
            Dict with detected pattern adoptions
        """
        # Architectural pattern signatures
        pattern_signatures = {
            "repository_pattern": [r"Repository\(", r"class.*Repository:"],
            "factory_pattern": [r"Factory\(", r"class.*Factory:"],
            "adapter_pattern": [r"Adapter\(", r"class.*Adapter:"],
            "service_pattern": [r"Service\(", r"class.*Service:"],
            "middleware_pattern": [r"Middleware\(", r"class.*Middleware:"],
        }

        pattern_adoptions = defaultdict(list)

        # Search commits for pattern introductions
        for commit in self.repo.iter_commits(since=start_date, until=end_date):
            commit_date = datetime.fromtimestamp(commit.committed_date)

            for pattern_name, signatures in pattern_signatures.items():
                for file_path in commit.stats.files:
                    if file_path.endswith(".py"):
                        try:
                            file_content = (
                                (commit.tree / file_path).data_stream.read().decode("utf-8")
                            )

                            # Check if any signature matches
                            for signature in signatures:
                                if re.search(signature, file_content):
                                    pattern_adoptions[pattern_name].append(
                                        {
                                            "date": self._format_date(commit_date),
                                            "file": file_path,
                                            "commit": commit.hexsha[:8],
                                        }
                                    )
                                    break

                        except Exception:
                            continue

        return {
            "patterns_detected": list(pattern_adoptions.keys()),
            "pattern_usage": {pattern: len(uses) for pattern, uses in pattern_adoptions.items()},
        }

    def get_breakthrough_signals(self) -> Dict[BreakthroughSignal, Any]:
        """
        Extract breakthrough signals from structural analysis.

        Returns:
            Dict mapping signal types to evidence
        """
        if not self.results:
            return {}

        signals = {}

        # ADR creation signal
        adr_activity = self.results.get("adr_activity", {})
        adr_events = adr_activity.get("events", [])

        if adr_events:
            signals[BreakthroughSignal.ADR_CREATION] = {
                "count": len(adr_events),
                "adrs": [
                    {"number": e["adr_number"], "title": e["title"], "date": e["created"]}
                    for e in adr_events
                ],
            }

        # Refactoring event signal
        refactoring_events = self.results.get("refactoring_events", [])

        if refactoring_events:
            # Major refactoring = >30 files changed
            major_refactorings = [e for e in refactoring_events if e["files_changed"] >= 30]

            if major_refactorings:
                signals[BreakthroughSignal.REFACTORING_EVENT] = {
                    "count": len(major_refactorings),
                    "max_files_changed": max(e["files_changed"] for e in major_refactorings),
                    "events": [
                        {
                            "date": e["date"],
                            "files_changed": e["files_changed"],
                            "type": e["type"],
                        }
                        for e in major_refactorings[:3]
                    ],
                }

        return signals
