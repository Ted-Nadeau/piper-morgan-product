"""
Pattern Discovery - Archaeological Search for Existing Implementations

Prevents rebuilding functionality that already exists (addresses the 60-80% case).
Provides systematic search and analysis of existing patterns in the codebase
before implementing new functionality.

Core principle: Check what exists before building new.
"""

import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


@dataclass
class PatternMatch:
    """A discovered pattern match with context"""

    file_path: str
    line_number: int
    match_text: str
    context_before: List[str]
    context_after: List[str]
    pattern_type: str
    confidence_score: float


@dataclass
class PatternDiscoveryResult:
    """Result of pattern discovery search"""

    search_terms: List[str]
    matches: List[PatternMatch]
    search_paths: List[str]
    total_files_searched: int
    patterns_found: int
    recommendations: List[str]
    search_duration_ms: float


class PatternDiscovery:
    """
    Archaeological pattern discovery to prevent rebuilding existing functionality

    Searches codebase systematically to find existing implementations
    that can be extended or reused instead of rebuilt from scratch.
    """

    def __init__(self, project_root: str = "."):
        """Initialize pattern discovery with project root path"""
        self.project_root = Path(project_root)
        self.search_patterns = {
            "class_definitions": r"class\s+(\w+)",
            "function_definitions": r"def\s+(\w+)\s*\(",
            "async_functions": r"async\s+def\s+(\w+)\s*\(",
            "imports": r"(?:from\s+\w+\s+)?import\s+([\w\s,]+)",
            "decorators": r"@(\w+)",
            "api_endpoints": r'@app\.(?:get|post|put|delete|patch)\s*\([\'"]([^\'"]+)[\'"]',
            "database_models": r"class\s+(\w+).*(?:Model|Base)",
            "test_functions": r"def\s+(test_\w+)\s*\(",
            "constants": r"^[A-Z_]+\s*=",
            "configuration": r"config\.|Config\.|SETTINGS\.",
        }

        # File extensions to search
        self.searchable_extensions = {
            ".py",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".md",
            ".yaml",
            ".yml",
            ".json",
        }

        # Directories to exclude from search
        self.excluded_dirs = {
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            "node_modules",
            ".pytest_cache",
            "build",
            "dist",
            ".next",
            ".cache",
        }

        logger.info(f"PatternDiscovery initialized with project root: {self.project_root}")

    def discover_patterns(
        self,
        search_terms: List[str],
        pattern_types: Optional[List[str]] = None,
        search_paths: Optional[List[str]] = None,
    ) -> PatternDiscoveryResult:
        """
        Discover existing patterns matching search terms

        Args:
            search_terms: Terms to search for in the codebase
            pattern_types: Specific pattern types to search for (default: all)
            search_paths: Specific paths to search (default: entire project)

        Returns:
            PatternDiscoveryResult with discovered matches and recommendations
        """
        import time

        start_time = time.time()

        logger.info(f"Starting pattern discovery for terms: {search_terms}")

        if pattern_types is None:
            pattern_types = list(self.search_patterns.keys())

        if search_paths is None:
            search_paths = [str(self.project_root)]

        all_matches = []
        total_files_searched = 0

        # Search each specified path
        for search_path in search_paths:
            path_obj = Path(search_path)
            if not path_obj.exists():
                logger.warning(f"Search path does not exist: {search_path}")
                continue

            # Search files in path
            if path_obj.is_file():
                matches = self._search_file(path_obj, search_terms, pattern_types)
                all_matches.extend(matches)
                total_files_searched += 1
            else:
                # Search directory recursively
                for file_path in self._get_searchable_files(path_obj):
                    matches = self._search_file(file_path, search_terms, pattern_types)
                    all_matches.extend(matches)
                    total_files_searched += 1

        # Generate recommendations based on findings
        recommendations = self._generate_recommendations(all_matches, search_terms)

        search_duration = (time.time() - start_time) * 1000

        result = PatternDiscoveryResult(
            search_terms=search_terms,
            matches=all_matches,
            search_paths=search_paths,
            total_files_searched=total_files_searched,
            patterns_found=len(all_matches),
            recommendations=recommendations,
            search_duration_ms=search_duration,
        )

        logger.info(
            f"Pattern discovery completed: {len(all_matches)} matches in {total_files_searched} files ({search_duration:.2f}ms)"
        )
        return result

    def _get_searchable_files(self, directory: Path) -> List[Path]:
        """Get list of searchable files in directory, excluding ignored paths"""
        searchable_files = []

        try:
            for item in directory.rglob("*"):
                # Skip directories
                if item.is_dir():
                    continue

                # Skip excluded directories
                if any(excluded in item.parts for excluded in self.excluded_dirs):
                    continue

                # Check file extension
                if item.suffix.lower() in self.searchable_extensions:
                    searchable_files.append(item)

        except PermissionError as e:
            logger.warning(f"Permission denied accessing {directory}: {e}")

        return searchable_files

    def _search_file(
        self, file_path: Path, search_terms: List[str], pattern_types: List[str]
    ) -> List[PatternMatch]:
        """Search a single file for patterns matching search terms"""
        matches = []

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            # Search each line
            for line_num, line in enumerate(lines, 1):
                line = line.rstrip()

                # Check for direct term matches
                for term in search_terms:
                    if term.lower() in line.lower():
                        match = PatternMatch(
                            file_path=str(file_path),
                            line_number=line_num,
                            match_text=line.strip(),
                            context_before=self._get_context_lines(lines, line_num - 1, -3),
                            context_after=self._get_context_lines(lines, line_num - 1, 3),
                            pattern_type="term_match",
                            confidence_score=0.7,
                        )
                        matches.append(match)

                # Check for pattern matches
                for pattern_name in pattern_types:
                    if pattern_name in self.search_patterns:
                        pattern = self.search_patterns[pattern_name]
                        if re.search(pattern, line, re.IGNORECASE):
                            # Check if any search terms are in the match context
                            context_text = " ".join(
                                [line]
                                + self._get_context_lines(lines, line_num - 1, -2)
                                + self._get_context_lines(lines, line_num - 1, 2)
                            )

                            term_relevance = sum(
                                1 for term in search_terms if term.lower() in context_text.lower()
                            )

                            if term_relevance > 0:
                                confidence = min(0.9, 0.5 + (term_relevance * 0.2))

                                match = PatternMatch(
                                    file_path=str(file_path),
                                    line_number=line_num,
                                    match_text=line.strip(),
                                    context_before=self._get_context_lines(lines, line_num - 1, -2),
                                    context_after=self._get_context_lines(lines, line_num - 1, 2),
                                    pattern_type=pattern_name,
                                    confidence_score=confidence,
                                )
                                matches.append(match)

        except Exception as e:
            logger.warning(f"Error searching file {file_path}: {e}")

        return matches

    def _get_context_lines(
        self, lines: List[str], center_line: int, context_range: int
    ) -> List[str]:
        """Get context lines around a center line"""
        if context_range < 0:
            # Before context
            start = max(0, center_line + context_range)
            end = center_line
        else:
            # After context
            start = center_line + 1
            end = min(len(lines), center_line + context_range + 1)

        return [line.rstrip() for line in lines[start:end]]

    def _generate_recommendations(
        self, matches: List[PatternMatch], search_terms: List[str]
    ) -> List[str]:
        """Generate recommendations based on discovered patterns"""
        recommendations = []

        if not matches:
            recommendations.append(f"No existing patterns found for {search_terms}")
            recommendations.append(
                "Proceed with new implementation, but consider creating reusable patterns"
            )
            return recommendations

        # Group matches by file and pattern type
        files_with_matches = set(match.file_path for match in matches)
        pattern_types_found = set(match.pattern_type for match in matches)

        recommendations.append(
            f"Found {len(matches)} pattern matches in {len(files_with_matches)} files"
        )

        # High confidence matches
        high_confidence_matches = [m for m in matches if m.confidence_score > 0.8]
        if high_confidence_matches:
            recommendations.append(
                f"Found {len(high_confidence_matches)} high-confidence matches - strongly consider reuse/extension"
            )

        # Specific recommendations by pattern type
        if "class_definitions" in pattern_types_found:
            recommendations.append(
                "Existing classes found - consider inheritance or composition instead of new class"
            )

        if (
            "function_definitions" in pattern_types_found
            or "async_functions" in pattern_types_found
        ):
            recommendations.append(
                "Existing functions found - consider refactoring/extending instead of duplicating"
            )

        if "api_endpoints" in pattern_types_found:
            recommendations.append(
                "Existing API endpoints found - ensure new endpoints follow established patterns"
            )

        if "database_models" in pattern_types_found:
            recommendations.append(
                "Existing database models found - consider model relationships and schema consistency"
            )

        if "test_functions" in pattern_types_found:
            recommendations.append(
                "Existing tests found - follow established test patterns and coverage approaches"
            )

        # File-specific recommendations
        if len(files_with_matches) < 3:
            recommendations.append(
                "Patterns concentrated in few files - consider if functionality should be consolidated"
            )
        else:
            recommendations.append(
                "Patterns distributed across files - ensure consistent interfaces and patterns"
            )

        return recommendations
