#!/usr/bin/env python3
"""
Enhanced Pattern Sweep - Breakthrough Detection System

Multi-layer Pattern Intelligence System that detects:
- Methodology evolution breakthroughs
- Architectural insight moments
- Team coordination patterns
- Concept emergence and growth

Usage:
    # Analyze last 30 days
    python pattern_sweep_enhanced.py

    # Analyze specific date range
    python pattern_sweep_enhanced.py --start 2025-11-01 --end 2025-11-03

    # Generate JSON output
    python pattern_sweep_enhanced.py --format json --output results.json

    # Run individual analyzer
    python pattern_sweep_enhanced.py --analyzer temporal

    # Show detailed report
    python pattern_sweep_enhanced.py --verbose
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from pattern_analyzers.breakthrough_detector import BreakthroughDetector
from pattern_analyzers.semantic_analyzer import SemanticAnalyzer
from pattern_analyzers.structural_analyzer import StructuralAnalyzer
from pattern_analyzers.temporal_analyzer import TemporalAnalyzer


class PatternSweepEnhanced:
    """
    Enhanced Pattern Sweep orchestrator with CLI interface.

    Coordinates multiple analyzers to detect breakthrough moments
    and methodology evolution patterns.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.detector = BreakthroughDetector(project_root)

    async def run_full_analysis(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        verbose: bool = False,
    ) -> dict:
        """Run complete breakthrough detection analysis"""
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=30)

        print(f"🔍 Running Enhanced Pattern Sweep...")
        print(f"📅 Period: {start_date.date()} to {end_date.date()}")
        print()

        # Run breakthrough detection
        results = await self.detector.detect_breakthroughs(start_date, end_date)

        # Print summary
        self._print_summary(results, verbose)

        return results

    async def run_single_analyzer(
        self,
        analyzer_name: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> dict:
        """Run a single analyzer"""
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=30)

        print(f"🔍 Running {analyzer_name.title()} Analyzer...")
        print(f"📅 Period: {start_date.date()} to {end_date.date()}")
        print()

        analyzer_map = {
            "temporal": TemporalAnalyzer,
            "semantic": SemanticAnalyzer,
            "structural": StructuralAnalyzer,
        }

        if analyzer_name not in analyzer_map:
            raise ValueError(f"Unknown analyzer: {analyzer_name}")

        analyzer = analyzer_map[analyzer_name](self.project_root)
        results = await analyzer.analyze(start_date, end_date)
        signals = analyzer.get_breakthrough_signals()

        print(f"✓ Analysis complete")
        print(f"  Signals detected: {len(signals)}")
        for signal_type, evidence in signals.items():
            print(f"    - {signal_type.value}")

        return {"results": results, "signals": signals}

    def _print_summary(self, results: dict, verbose: bool = False):
        """Print analysis summary"""
        breakthroughs = results.get("breakthroughs", [])
        signals = results.get("signals", {})
        metadata = results.get("analysis_metadata", {})

        print("=" * 80)
        print("BREAKTHROUGH DETECTION SUMMARY")
        print("=" * 80)
        print()

        print(f"✓ Breakthroughs Detected: {len(breakthroughs)}")
        print(f"✓ Signals Detected: {len(signals)}")
        print()

        if breakthroughs:
            print("📊 Breakthrough Events:")
            for i, bt in enumerate(breakthroughs[:5], 1):  # Show top 5
                print(
                    f"  {i}. {bt['type'].upper()} ({bt['date']}) - {bt['confidence']:.0%} confidence"
                )
                if verbose:
                    print(f"     Signals: {', '.join(s.value for s in bt['signals'])}")
                    print(f"     Analyzers: {', '.join(bt['analyzers_involved'])}")

            if len(breakthroughs) > 5:
                print(f"  ... and {len(breakthroughs) - 5} more")
            print()

        # Print metadata summary
        print("📈 Analysis Metrics:")
        print(
            f"  Commit velocity: {metadata.get('temporal', {}).get('baseline_velocity', 0):.2f}/day"
        )
        print(
            f"  Concepts emerged: {metadata.get('semantic', {}).get('total_concepts_emerged', 0)}"
        )
        print(f"  ADRs created: {metadata.get('structural', {}).get('total_adrs_created', 0)}")
        print(
            f"  Refactoring events: {metadata.get('structural', {}).get('refactoring_events', 0)}"
        )
        print()

        if verbose:
            print("=" * 80)
            report = self.detector.generate_breakthrough_report(results)
            print(report)

    def save_results(self, results: dict, output_path: Path, format: str = "json"):
        """Save results to file"""
        if format == "json":
            # Convert signal enums to strings for JSON serialization
            serializable_results = self._make_json_serializable(results)

            with open(output_path, "w") as f:
                json.dump(serializable_results, f, indent=2)

            print(f"✓ Results saved to {output_path}")
        elif format == "text":
            report = self.detector.generate_breakthrough_report(results)
            with open(output_path, "w") as f:
                f.write(report)

            print(f"✓ Report saved to {output_path}")
        else:
            raise ValueError(f"Unknown format: {format}")

    def _make_json_serializable(self, obj, seen=None):
        """Convert objects to JSON-serializable format"""
        if seen is None:
            seen = set()

        # Check for circular references
        obj_id = id(obj)
        if obj_id in seen:
            return "<circular reference>"

        # Handle different types
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif hasattr(obj, "value"):  # Enum
            return obj.value
        elif isinstance(obj, dict):
            seen.add(obj_id)
            result = {}
            for k, v in obj.items():
                # Convert enum keys to their values
                key = k.value if hasattr(k, "value") else k
                result[key] = self._make_json_serializable(v, seen)
            seen.remove(obj_id)
            return result
        elif isinstance(obj, (list, tuple)):
            seen.add(obj_id)
            result = [self._make_json_serializable(item, seen) for item in obj]
            seen.remove(obj_id)
            return result
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            # Skip complex objects (like Repo)
            return str(type(obj).__name__)


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Enhanced Pattern Sweep - Breakthrough Detection System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze last 30 days
  %(prog)s

  # Analyze specific date range
  %(prog)s --start 2025-11-01 --end 2025-11-03

  # Run single analyzer
  %(prog)s --analyzer temporal

  # Generate detailed report
  %(prog)s --verbose --format text --output report.txt

  # Export JSON results
  %(prog)s --format json --output results.json
        """,
    )

    parser.add_argument("--start", type=str, help="Start date (YYYY-MM-DD). Default: 30 days ago")
    parser.add_argument("--end", type=str, help="End date (YYYY-MM-DD). Default: today")
    parser.add_argument(
        "--analyzer",
        type=str,
        choices=["temporal", "semantic", "structural"],
        help="Run single analyzer only",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")

    args = parser.parse_args()

    # Parse dates
    start_date = None
    end_date = None

    if args.start:
        try:
            start_date = datetime.strptime(args.start, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid start date format: {args.start}")
            print("Expected format: YYYY-MM-DD")
            sys.exit(1)

    if args.end:
        try:
            end_date = datetime.strptime(args.end, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid end date format: {args.end}")
            print("Expected format: YYYY-MM-DD")
            sys.exit(1)

    # Initialize orchestrator
    project_root = Path(__file__).parent.parent
    orchestrator = PatternSweepEnhanced(project_root)

    # Run analysis
    try:
        if args.analyzer:
            results = await orchestrator.run_single_analyzer(args.analyzer, start_date, end_date)
        else:
            results = await orchestrator.run_full_analysis(
                start_date, end_date, verbose=args.verbose
            )

        # Save results if output specified
        if args.output:
            output_path = Path(args.output)
            orchestrator.save_results(results, output_path, format=args.format)

    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
