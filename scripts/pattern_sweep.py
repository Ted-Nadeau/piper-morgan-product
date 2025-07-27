#!/usr/bin/env python3
"""
Pattern Sweep Process with TLDR Integration
Systematic pattern detection and learning acceleration system.
"""

import argparse
import asyncio
import json
import re
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from tldr_runner import TLDRRunner


@dataclass
class Pattern:
    """Represents a detected pattern in the codebase"""

    id: str
    category: str  # code, usage, performance, coordination
    type: str  # class, function, test, workflow, etc.
    description: str
    occurrences: int
    files: List[str]
    confidence: float  # 0.0 to 1.0
    first_seen: str
    last_seen: str
    examples: List[str]
    related_patterns: List[str] = None

    def __post_init__(self):
        if self.related_patterns is None:
            self.related_patterns = []


@dataclass
class PatternSweepResult:
    """Results from a pattern sweep run"""

    timestamp: str
    total_files_scanned: int
    patterns_detected: int
    new_patterns: int
    updated_patterns: int
    sweep_duration_ms: float
    pattern_categories: Dict[str, int]
    top_patterns: List[Pattern]


class PatternDetector:
    """Core pattern detection engine"""

    def __init__(self):
        self.code_patterns = {
            # Async patterns
            "async_session_factory": {
                "regex": r"async\s+with.*session_factory\(\)",
                "category": "code",
                "type": "async_pattern",
                "description": "AsyncSessionFactory usage pattern",
            },
            "async_context_manager": {
                "regex": r"async\s+with.*as\s+\w+:",
                "category": "code",
                "type": "async_pattern",
                "description": "Async context manager pattern",
            },
            # Repository patterns
            "repository_constructor": {
                "regex": r"(\w+)Repository\(\w*session\w*\)",
                "category": "code",
                "type": "repository_pattern",
                "description": "Repository pattern instantiation",
            },
            # Test patterns
            "pytest_mark_asyncio": {
                "regex": r"@pytest\.mark\.asyncio",
                "category": "code",
                "type": "test_pattern",
                "description": "Async test marker pattern",
            },
            "test_fixture_usage": {
                "regex": r"def\s+test_\w+\([^)]*(\w+_factory|\w+_session)[^)]*\):",
                "category": "code",
                "type": "test_pattern",
                "description": "Test fixture dependency pattern",
            },
            # Error handling patterns
            "graceful_degradation": {
                "regex": r"test_mode.*=.*True|\.test_mode\s*=\s*True",
                "category": "code",
                "type": "error_handling",
                "description": "Graceful degradation test mode pattern",
            },
            "try_except_log": {
                "regex": r"try:.*?except.*?logger\.(error|warning)",
                "category": "code",
                "type": "error_handling",
                "description": "Try-except with logging pattern",
            },
            # Domain patterns
            "domain_model_enum": {
                "regex": r"class\s+\w+\(.*Enum\):",
                "category": "code",
                "type": "domain_pattern",
                "description": "Domain model enum pattern",
            },
            "workflow_type": {
                "regex": r"WorkflowType\.\w+",
                "category": "code",
                "type": "domain_pattern",
                "description": "Workflow type usage pattern",
            },
        }

        self.session_patterns = {
            # Development velocity patterns
            "systematic_verification": {
                "regex": r"SYSTEMATIC VERIFICATION|Systematic Verification|systematic verification",
                "category": "usage",
                "type": "methodology",
                "description": "Systematic verification methodology usage",
            },
            "verification_first": {
                "regex": r"VERIFY FIRST|verification.*first|verify.*before",
                "category": "usage",
                "type": "methodology",
                "description": "Verification-first approach pattern",
            },
            # Success patterns
            "implementation_success": {
                "regex": r"SUCCESS:|✅.*SUCCESS|COMPLETE.*✅",
                "category": "usage",
                "type": "outcome",
                "description": "Successful implementation pattern",
            },
            "rapid_implementation": {
                "regex": r"(\d+)[\s-]*minute[s]?\s+(implementation|fix|debug)",
                "category": "performance",
                "type": "velocity",
                "description": "Rapid implementation timing pattern",
            },
            # Issue resolution patterns
            "root_cause_identified": {
                "regex": r"ROOT CAUSE|root cause|Root Cause",
                "category": "usage",
                "type": "debugging",
                "description": "Root cause identification pattern",
            },
            "pm_ticket_resolution": {
                "regex": r"PM-\d+.*COMPLETE|PM-\d+.*✅",
                "category": "coordination",
                "type": "workflow",
                "description": "PM ticket completion pattern",
            },
        }

    async def scan_file_for_patterns(self, file_path: Path) -> List[Tuple[str, Pattern]]:
        """Scan a single file for all patterns"""
        patterns_found = []

        try:
            content = file_path.read_text(encoding="utf-8")
            file_str = str(file_path)

            # Choose pattern set based on file type
            if file_path.suffix == ".py":
                pattern_set = self.code_patterns
            elif file_path.suffix == ".md":
                pattern_set = self.session_patterns
            else:
                return patterns_found

            for pattern_id, pattern_config in pattern_set.items():
                matches = re.findall(pattern_config["regex"], content, re.MULTILINE | re.DOTALL)

                if matches:
                    # Extract examples (first 3 matches)
                    examples = [str(match)[:100] for match in matches[:3]]

                    pattern = Pattern(
                        id=pattern_id,
                        category=pattern_config["category"],
                        type=pattern_config["type"],
                        description=pattern_config["description"],
                        occurrences=len(matches),
                        files=[file_str],
                        confidence=min(
                            1.0, len(matches) / 10.0
                        ),  # More matches = higher confidence
                        first_seen=datetime.now().isoformat(),
                        last_seen=datetime.now().isoformat(),
                        examples=examples,
                    )

                    patterns_found.append((pattern_id, pattern))

        except (UnicodeDecodeError, PermissionError):
            # Skip files that can't be read
            pass

        return patterns_found

    async def detect_patterns_in_directory(
        self, directory: Path, file_extensions: Set[str]
    ) -> Dict[str, Pattern]:
        """Detect patterns across all files in directory"""
        all_patterns = defaultdict(
            lambda: {"files": set(), "occurrences": 0, "examples": [], "first_pattern": None}
        )

        files_to_scan = []
        for ext in file_extensions:
            files_to_scan.extend(directory.rglob(f"*{ext}"))

        # Scan files concurrently in batches to avoid overwhelming the system
        batch_size = 50
        for i in range(0, len(files_to_scan), batch_size):
            batch = files_to_scan[i : i + batch_size]
            tasks = [self.scan_file_for_patterns(file_path) for file_path in batch]
            batch_results = await asyncio.gather(*tasks)

            for file_patterns in batch_results:
                for pattern_id, pattern in file_patterns:
                    pattern_data = all_patterns[pattern_id]
                    pattern_data["files"].update(pattern.files)
                    pattern_data["occurrences"] += pattern.occurrences
                    pattern_data["examples"].extend(pattern.examples)

                    if pattern_data["first_pattern"] is None:
                        pattern_data["first_pattern"] = pattern

        # Convert aggregated data back to Pattern objects
        final_patterns = {}
        for pattern_id, data in all_patterns.items():
            base_pattern = data["first_pattern"]
            final_pattern = Pattern(
                id=pattern_id,
                category=base_pattern.category,
                type=base_pattern.type,
                description=base_pattern.description,
                occurrences=data["occurrences"],
                files=sorted(list(data["files"])),
                confidence=min(1.0, data["occurrences"] / (len(data["files"]) * 5)),
                first_seen=base_pattern.first_seen,
                last_seen=base_pattern.last_seen,
                examples=data["examples"][:5],  # Keep top 5 examples
            )
            final_patterns[pattern_id] = final_pattern

        return final_patterns


class PatternSweepRunner:
    """Main Pattern Sweep orchestrator with TLDR integration"""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.tldr_runner = TLDRRunner()
        self.detector = PatternDetector()
        self.pattern_storage_path = self.project_root / "scripts" / "pattern_sweep_data.json"

    async def run_pattern_sweep(
        self,
        include_tests: bool = True,
        include_docs: bool = True,
        include_source: bool = True,
        save_results: bool = True,
        verbose: bool = False,
    ) -> PatternSweepResult:
        """Run comprehensive pattern sweep across codebase"""

        start_time = time.time()

        if verbose:
            print("🔍 Starting Pattern Sweep with TLDR Integration...")

        # Determine file extensions to scan
        extensions = set()
        if include_source:
            extensions.add(".py")
        if include_docs:
            extensions.update([".md", ".rst"])
        if include_tests:
            extensions.add(".py")  # Tests are Python files

        # Run pattern detection
        if verbose:
            print(f"📁 Scanning {self.project_root} for patterns...")

        detected_patterns = await self.detector.detect_patterns_in_directory(
            self.project_root, extensions
        )

        # Load existing patterns for comparison
        existing_patterns = self._load_existing_patterns()
        new_patterns = 0
        updated_patterns = 0

        for pattern_id, pattern in detected_patterns.items():
            if pattern_id not in existing_patterns:
                new_patterns += 1
            else:
                # Check if pattern has changed significantly
                old_pattern = existing_patterns[pattern_id]
                if pattern.occurrences != old_pattern.get("occurrences", 0) or len(
                    pattern.files
                ) != len(old_pattern.get("files", [])):
                    updated_patterns += 1

        # Calculate categories
        categories = Counter()
        for pattern in detected_patterns.values():
            categories[pattern.category] += 1

        # Get top patterns by confidence and occurrence
        top_patterns = sorted(
            detected_patterns.values(), key=lambda p: (p.confidence * p.occurrences), reverse=True
        )[:10]

        # Create results
        sweep_duration = (time.time() - start_time) * 1000  # Convert to ms
        total_files = sum(len(pattern.files) for pattern in detected_patterns.values())

        result = PatternSweepResult(
            timestamp=datetime.now().isoformat(),
            total_files_scanned=total_files,
            patterns_detected=len(detected_patterns),
            new_patterns=new_patterns,
            updated_patterns=updated_patterns,
            sweep_duration_ms=sweep_duration,
            pattern_categories=dict(categories),
            top_patterns=top_patterns,
        )

        if save_results:
            self._save_patterns(detected_patterns, result)

        if verbose:
            self._print_results(result)

        return result

    def _load_existing_patterns(self) -> Dict[str, Any]:
        """Load previously detected patterns"""
        if self.pattern_storage_path.exists():
            try:
                with open(self.pattern_storage_path, "r") as f:
                    data = json.load(f)
                    return data.get("patterns", {})
            except (json.JSONDecodeError, KeyError):
                pass
        return {}

    def _save_patterns(self, patterns: Dict[str, Pattern], result: PatternSweepResult):
        """Save patterns and results to storage"""
        patterns_data = {pattern_id: asdict(pattern) for pattern_id, pattern in patterns.items()}

        storage_data = {
            "last_sweep": asdict(result),
            "patterns": patterns_data,
            "sweep_history": self._load_sweep_history() + [asdict(result)],
        }

        with open(self.pattern_storage_path, "w") as f:
            json.dump(storage_data, f, indent=2)

    def _load_sweep_history(self) -> List[Dict]:
        """Load sweep history"""
        if self.pattern_storage_path.exists():
            try:
                with open(self.pattern_storage_path, "r") as f:
                    data = json.load(f)
                    return data.get("sweep_history", [])
            except (json.JSONDecodeError, KeyError):
                pass
        return []

    def _print_results(self, result: PatternSweepResult):
        """Print pattern sweep results"""
        print(f"\n🎯 Pattern Sweep Complete!")
        print(f"   📊 Files Scanned: {result.total_files_scanned}")
        print(f"   🔍 Patterns Detected: {result.patterns_detected}")
        print(f"   🆕 New Patterns: {result.new_patterns}")
        print(f"   📈 Updated Patterns: {result.updated_patterns}")
        print(f"   ⚡ Duration: {result.sweep_duration_ms:.1f}ms")

        print(f"\n📋 Pattern Categories:")
        for category, count in result.pattern_categories.items():
            print(f"   {category}: {count}")

        print(f"\n🏆 Top Patterns by Confidence:")
        for i, pattern in enumerate(result.top_patterns[:5], 1):
            print(
                f"   {i}. {pattern.description} ({pattern.occurrences} occurrences, {pattern.confidence:.2f} confidence)"
            )

    async def run_with_tldr_integration(
        self,
        pattern_sweep: bool = True,
        run_tests: bool = True,
        test_pattern: Optional[str] = None,
        verbose: bool = False,
    ):
        """Run pattern sweep integrated with TLDR testing"""

        if verbose:
            print("🚀 Starting TLDR + Pattern Sweep Integration...")

        results = {}

        # 1. Run pattern sweep first
        if pattern_sweep:
            if verbose:
                print("🔍 Phase 1: Pattern Detection...")
            pattern_result = await self.run_pattern_sweep(verbose=verbose)
            results["pattern_sweep"] = pattern_result

        # 2. Run TLDR tests to validate patterns
        if run_tests:
            if verbose:
                print("🧪 Phase 2: TLDR Validation...")

            # Get test files based on detected patterns
            test_files = self.tldr_runner.discover_tests(pattern=test_pattern)

            if test_files:
                test_start = time.time()
                test_results = await self.tldr_runner.run_multiple_tests(
                    test_files[:10], timeout=0.1, verbose=verbose  # Limit to 10 tests for speed
                )
                test_duration = (time.time() - test_start) * 1000

                results["tldr_tests"] = {
                    "test_files": len(test_files),
                    "duration_ms": test_duration,
                    "results": test_results,
                }

                if verbose:
                    success_count = sum(1 for result in test_results.values() if result[0] == 0)
                    print(f"   ✅ Tests Passed: {success_count}/{len(test_results)}")
                    print(f"   ⚡ Test Duration: {test_duration:.1f}ms")

        return results


async def main():
    parser = argparse.ArgumentParser(
        description="Pattern Sweep Process with TLDR Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./scripts/pattern_sweep.py --pattern-sweep-only
  ./scripts/pattern_sweep.py --with-pattern-detection --learn-usage-patterns
  ./scripts/pattern_sweep.py --tldr-integration --verbose
        """,
    )

    parser.add_argument(
        "--pattern-sweep-only", action="store_true", help="Run only pattern detection"
    )
    parser.add_argument(
        "--with-pattern-detection",
        action="store_true",
        help="Run pattern detection with TLDR tests",
    )
    parser.add_argument(
        "--learn-usage-patterns", action="store_true", help="Include session log pattern learning"
    )
    parser.add_argument(
        "--tldr-integration", action="store_true", help="Full TLDR + Pattern Sweep integration"
    )
    parser.add_argument("--test-pattern", type=str, help="Test file pattern to filter")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    runner = PatternSweepRunner()

    if args.pattern_sweep_only:
        result = await runner.run_pattern_sweep(
            include_docs=args.learn_usage_patterns, verbose=args.verbose
        )
    elif args.with_pattern_detection or args.tldr_integration:
        result = await runner.run_with_tldr_integration(
            pattern_sweep=True, run_tests=True, test_pattern=args.test_pattern, verbose=args.verbose
        )
    else:
        # Default: pattern sweep only
        result = await runner.run_pattern_sweep(verbose=True)

    return result


if __name__ == "__main__":
    asyncio.run(main())
