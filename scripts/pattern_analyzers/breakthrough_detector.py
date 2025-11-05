"""
Breakthrough Detection - Signal synthesis and breakthrough classification.

Combines signals from multiple analyzers to identify and classify breakthrough moments.

Breakthrough Types:
- Implementation Breakthrough: ADR creation + refactoring events
- Discovery Breakthrough: Parallel work + semantic emergence
- Coordination Breakthrough: High parallel work + velocity spike
- Architectural Breakthrough: ADR creation + architectural insight
"""

from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .base import BaseAnalyzer, BreakthroughEvent, BreakthroughSignal
from .semantic_analyzer import SemanticAnalyzer
from .structural_analyzer import StructuralAnalyzer
from .temporal_analyzer import TemporalAnalyzer


class BreakthroughType:
    """Enumeration of breakthrough types based on signal patterns"""

    IMPLEMENTATION = "implementation_breakthrough"
    DISCOVERY = "discovery_breakthrough"
    COORDINATION = "coordination_breakthrough"
    ARCHITECTURAL = "architectural_breakthrough"
    VELOCITY = "velocity_breakthrough"
    COMPLETION = "completion_breakthrough"


class BreakthroughDetector:
    """
    Synthesis engine that combines signals from multiple analyzers to detect breakthroughs.

    Uses signal convergence and pattern matching to identify different types of
    breakthrough moments with confidence scores.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root

        # Initialize all analyzers
        self.temporal_analyzer = TemporalAnalyzer(project_root)
        self.semantic_analyzer = SemanticAnalyzer(project_root)
        self.structural_analyzer = StructuralAnalyzer(project_root)

        # Breakthrough classification rules (signal patterns)
        self.breakthrough_patterns = {
            BreakthroughType.IMPLEMENTATION: {
                "required": {BreakthroughSignal.ADR_CREATION},
                "supporting": {
                    BreakthroughSignal.REFACTORING_EVENT,
                    BreakthroughSignal.VELOCITY_SPIKE,
                },
                "min_supporting": 1,
            },
            BreakthroughType.DISCOVERY: {
                "required": {BreakthroughSignal.SEMANTIC_EMERGENCE},
                "supporting": {
                    BreakthroughSignal.PARALLEL_WORK,
                    BreakthroughSignal.ARCHITECTURAL_INSIGHT,
                },
                "min_supporting": 1,
            },
            BreakthroughType.COORDINATION: {
                "required": {BreakthroughSignal.PARALLEL_WORK},
                "supporting": {
                    BreakthroughSignal.VELOCITY_SPIKE,
                    BreakthroughSignal.COMPLETION_SPIKE,
                },
                "min_supporting": 1,
            },
            BreakthroughType.ARCHITECTURAL: {
                "required": {BreakthroughSignal.ARCHITECTURAL_INSIGHT},
                "supporting": {
                    BreakthroughSignal.ADR_CREATION,
                    BreakthroughSignal.REFACTORING_EVENT,
                },
                "min_supporting": 1,
            },
            BreakthroughType.VELOCITY: {
                "required": {BreakthroughSignal.VELOCITY_SPIKE},
                "supporting": {
                    BreakthroughSignal.PARALLEL_WORK,
                    BreakthroughSignal.COMPLETION_SPIKE,
                },
                "min_supporting": 0,  # Can be standalone
            },
            BreakthroughType.COMPLETION: {
                "required": {BreakthroughSignal.COMPLETION_SPIKE},
                "supporting": {
                    BreakthroughSignal.VELOCITY_SPIKE,
                    BreakthroughSignal.REFACTORING_EVENT,
                },
                "min_supporting": 0,  # Can be standalone
            },
        }

    async def detect_breakthroughs(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Run all analyzers and synthesize breakthrough detection results.

        Returns:
            Dict with keys:
            - breakthroughs: List of detected breakthrough events
            - signals: All signals detected by all analyzers
            - analysis_metadata: Metadata from each analyzer
        """
        # Run all analyzers in parallel
        temporal_results = await self.temporal_analyzer.analyze(start_date, end_date)
        semantic_results = await self.semantic_analyzer.analyze(start_date, end_date)
        structural_results = await self.structural_analyzer.analyze(start_date, end_date)

        # Collect all signals
        all_signals = self._collect_all_signals()

        # Group signals by date for temporal clustering
        signals_by_date = self._group_signals_by_date(all_signals)

        # Detect breakthrough events from signal patterns
        breakthrough_events = self._classify_breakthroughs(signals_by_date)

        # Calculate confidence scores
        breakthrough_events = self._calculate_confidence_scores(breakthrough_events, all_signals)

        return {
            "breakthroughs": breakthrough_events,
            "signals": all_signals,
            "signals_by_date": signals_by_date,
            "analysis_metadata": {
                "temporal": {
                    "baseline_velocity": temporal_results.get("velocity_data", {}).get(
                        "baseline_velocity", 0
                    ),
                    "total_commits": temporal_results.get("velocity_data", {}).get(
                        "total_commits", 0
                    ),
                },
                "semantic": {
                    "total_concepts_emerged": len(semantic_results.get("term_emergence", [])),
                    "high_validation_concepts": len(
                        [
                            t
                            for t, s in semantic_results.get("validation_scores", {}).items()
                            if s >= 0.67
                        ]
                    ),
                },
                "structural": {
                    "total_adrs_created": structural_results.get("adr_activity", {}).get(
                        "total_adrs_created", 0
                    ),
                    "refactoring_events": len(structural_results.get("refactoring_events", [])),
                },
            },
            "analysis_period": {
                "start": temporal_results["analysis_period"]["start"],
                "end": temporal_results["analysis_period"]["end"],
            },
        }

    def _collect_all_signals(self) -> Dict[BreakthroughSignal, Any]:
        """Collect signals from all analyzers"""
        all_signals = {}

        # Temporal signals
        temporal_signals = self.temporal_analyzer.get_breakthrough_signals()
        all_signals.update(temporal_signals)

        # Semantic signals
        semantic_signals = self.semantic_analyzer.get_breakthrough_signals()
        all_signals.update(semantic_signals)

        # Structural signals
        structural_signals = self.structural_analyzer.get_breakthrough_signals()
        all_signals.update(structural_signals)

        return all_signals

    def _group_signals_by_date(
        self, all_signals: Dict[BreakthroughSignal, Any]
    ) -> Dict[str, List[Tuple[BreakthroughSignal, Any]]]:
        """Group signals by date for temporal clustering"""
        signals_by_date = defaultdict(list)

        for signal_type, evidence in all_signals.items():
            # Extract dates from evidence
            dates = self._extract_dates_from_evidence(signal_type, evidence)

            for date_str in dates:
                signals_by_date[date_str].append((signal_type, evidence))

        return dict(signals_by_date)

    def _extract_dates_from_evidence(
        self, signal_type: BreakthroughSignal, evidence: Any
    ) -> Set[str]:
        """Extract date strings from signal evidence"""
        dates = set()

        if isinstance(evidence, dict):
            # Check for common date fields
            if "dates" in evidence:
                dates.update(evidence["dates"])
            elif "date" in evidence:
                dates.add(evidence["date"])

            # Check nested structures
            if "events" in evidence and isinstance(evidence["events"], list):
                for event in evidence["events"]:
                    if isinstance(event, dict) and "date" in event:
                        # Extract just YYYY-MM-DD part
                        date_str = event["date"].split("T")[0]
                        dates.add(date_str)

            # Check ADR creation signal
            if "adrs" in evidence and isinstance(evidence["adrs"], list):
                for adr in evidence["adrs"]:
                    if isinstance(adr, dict) and "date" in adr:
                        date_str = adr["date"].split("T")[0]
                        dates.add(date_str)

        return dates

    def _classify_breakthroughs(
        self, signals_by_date: Dict[str, List[Tuple[BreakthroughSignal, Any]]]
    ) -> List[Dict[str, Any]]:
        """Classify breakthrough events based on signal patterns"""
        breakthrough_events = []

        for date_str, signals_list in signals_by_date.items():
            signal_types = {signal_type for signal_type, _ in signals_list}

            # Check each breakthrough pattern
            for breakthrough_type, pattern in self.breakthrough_patterns.items():
                required_signals = pattern["required"]
                supporting_signals = pattern["supporting"]
                min_supporting = pattern["min_supporting"]

                # Check if required signals are present
                if not required_signals.issubset(signal_types):
                    continue

                # Count supporting signals
                supporting_count = len(supporting_signals & signal_types)

                if supporting_count >= min_supporting:
                    # We have a breakthrough!
                    breakthrough_events.append(
                        {
                            "date": date_str,
                            "type": breakthrough_type,
                            "signals": list(signal_types),
                            "required_signals": list(required_signals),
                            "supporting_signals": list(supporting_signals & signal_types),
                            "signal_count": len(signal_types),
                            "supporting_count": supporting_count,
                        }
                    )

        return sorted(
            breakthrough_events, key=lambda x: (x["date"], x["signal_count"]), reverse=True
        )

    def _calculate_confidence_scores(
        self, breakthrough_events: List[Dict[str, Any]], all_signals: Dict[BreakthroughSignal, Any]
    ) -> List[Dict[str, Any]]:
        """Calculate confidence scores for breakthrough events"""
        for event in breakthrough_events:
            # Base confidence from signal count
            signal_count = event["signal_count"]
            base_confidence = min(1.0, signal_count / 4.0)  # Max at 4 signals

            # Bonus for supporting signals
            supporting_count = event["supporting_count"]
            supporting_bonus = supporting_count * 0.1

            # Bonus for cross-analyzer convergence
            signal_types = set(event["signals"])
            analyzers_involved = set()
            if any(
                s
                in {
                    BreakthroughSignal.VELOCITY_SPIKE,
                    BreakthroughSignal.PARALLEL_WORK,
                    BreakthroughSignal.COMPLETION_SPIKE,
                }
                for s in signal_types
            ):
                analyzers_involved.add("temporal")
            if any(
                s
                in {BreakthroughSignal.SEMANTIC_EMERGENCE, BreakthroughSignal.ARCHITECTURAL_INSIGHT}
                for s in signal_types
            ):
                analyzers_involved.add("semantic")
            if any(
                s in {BreakthroughSignal.ADR_CREATION, BreakthroughSignal.REFACTORING_EVENT}
                for s in signal_types
            ):
                analyzers_involved.add("structural")

            convergence_bonus = (len(analyzers_involved) - 1) * 0.15

            # Total confidence (capped at 1.0)
            confidence = min(1.0, base_confidence + supporting_bonus + convergence_bonus)

            event["confidence"] = round(confidence, 2)
            event["analyzers_involved"] = list(analyzers_involved)

        return breakthrough_events

    def generate_breakthrough_report(self, results: Dict[str, Any]) -> str:
        """Generate human-readable breakthrough detection report"""
        lines = []
        lines.append("=" * 80)
        lines.append("BREAKTHROUGH DETECTION REPORT")
        lines.append("=" * 80)

        period = results["analysis_period"]
        lines.append(f"\nAnalysis Period: {period['start']} to {period['end']}")

        # Summary stats
        breakthroughs = results["breakthroughs"]
        signals = results["signals"]

        lines.append(f"\n{'=' * 80}")
        lines.append("SUMMARY")
        lines.append("=" * 80)
        lines.append(f"Total Breakthroughs Detected: {len(breakthroughs)}")
        lines.append(f"Total Signals Detected: {len(signals)}")

        # List signal types
        lines.append("\nSignal Types Detected:")
        for signal_type in signals.keys():
            lines.append(f"  - {signal_type.value}")

        # Breakthrough events
        lines.append(f"\n{'=' * 80}")
        lines.append("BREAKTHROUGH EVENTS")
        lines.append("=" * 80)

        for i, event in enumerate(breakthroughs, 1):
            lines.append(f"\n{i}. {event['type'].upper()} ({event['date']})")
            lines.append(f"   Confidence: {event['confidence']:.0%}")
            lines.append(f"   Signals: {event['signal_count']} total")
            lines.append(f"   Analyzers: {', '.join(event['analyzers_involved'])}")

            lines.append("\n   Required Signals:")
            for sig in event["required_signals"]:
                lines.append(f"     ✓ {sig.value}")

            if event["supporting_signals"]:
                lines.append("\n   Supporting Signals:")
                for sig in event["supporting_signals"]:
                    lines.append(f"     + {sig.value}")

        # Metadata
        metadata = results["analysis_metadata"]
        lines.append(f"\n{'=' * 80}")
        lines.append("ANALYSIS METADATA")
        lines.append("=" * 80)

        lines.append("\nTemporal Analysis:")
        lines.append(
            f"  Baseline velocity: {metadata['temporal']['baseline_velocity']:.2f} commits/day"
        )
        lines.append(f"  Total commits: {metadata['temporal']['total_commits']}")

        lines.append("\nSemantic Analysis:")
        lines.append(f"  Concepts emerged: {metadata['semantic']['total_concepts_emerged']}")
        lines.append(
            f"  High-validation concepts: {metadata['semantic']['high_validation_concepts']}"
        )

        lines.append("\nStructural Analysis:")
        lines.append(f"  ADRs created: {metadata['structural']['total_adrs_created']}")
        lines.append(f"  Refactoring events: {metadata['structural']['refactoring_events']}")

        lines.append("\n" + "=" * 80)

        return "\n".join(lines)
