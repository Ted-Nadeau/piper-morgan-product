"""
Base classes and data models for enhanced pattern analysis.
"""

import sys
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Add parent directory to path to import from pattern_sweep.py
sys.path.insert(0, str(Path(__file__).parent.parent))
from pattern_sweep import Pattern


class PatternLifecycle(Enum):
    """Pattern lifecycle stages based on usage trajectory"""

    EMERGING = "emerging"  # Rapid growth, new pattern
    ESTABLISHED = "established"  # Stable usage, proven pattern
    DECLINING = "declining"  # Decreasing usage, being replaced
    SUPERSEDED = "superseded"  # Explicitly replaced by newer pattern


class BreakthroughSignal(Enum):
    """Types of signals that indicate breakthrough moments"""

    VELOCITY_SPIKE = "velocity_spike"  # Sudden increase in commit/work rate
    PARALLEL_WORK = "parallel_work"  # Multiple agents working simultaneously
    ADR_CREATION = "adr_creation"  # Architectural decision documented
    SEMANTIC_EMERGENCE = "semantic_emergence"  # New concept/terminology appears
    REFACTORING_EVENT = "refactoring_event"  # Major code restructuring
    ARCHITECTURAL_INSIGHT = "architectural_insight"  # New understanding documented
    COMPLETION_SPIKE = "completion_spike"  # Multiple issues closed rapidly


@dataclass
class EnhancedPattern(Pattern):
    """
    Extended pattern with lifecycle, validation, and breakthrough tracking.

    Inherits from Pattern (from pattern_sweep.py) and adds:
    - Lifecycle stage tracking
    - Growth rate analysis
    - Multi-context validation
    - Breakthrough correlation
    - Architectural impact assessment
    """

    lifecycle_stage: PatternLifecycle = PatternLifecycle.EMERGING
    growth_rate: float = 0.0  # Occurrences change rate over time window
    validation_signals: List[str] = field(
        default_factory=list
    )  # ["in_adr", "in_omnibus", "in_code"]
    related_breakthroughs: List[str] = field(default_factory=list)  # ["nov_3_p1_polish"]
    architectural_impact: str = "unknown"  # "high", "medium", "low", "unknown"
    first_seen_commit: Optional[str] = None  # Git commit hash where first seen
    peak_usage_date: Optional[str] = None  # Date of highest usage

    def __post_init__(self):
        """Initialize default values for inherited fields"""
        super().__post_init__()
        if not self.validation_signals:
            self.validation_signals = []
        if not self.related_breakthroughs:
            self.related_breakthroughs = []

    @property
    def validation_score(self) -> float:
        """
        Calculate validation confidence based on cross-context appearances.

        Returns: 0.0 to 1.0 confidence score
        - 0.0: No validation (only in one context)
        - 0.5: Partial validation (in 2 contexts)
        - 1.0: Full validation (in ADR + omnibus + code)
        """
        if not self.validation_signals:
            return 0.0

        # Maximum score when pattern appears in all three key contexts
        max_contexts = 3  # ADR, omnibus logs, code
        return min(1.0, len(self.validation_signals) / max_contexts)

    @property
    def is_breakthrough_related(self) -> bool:
        """Check if this pattern is associated with any breakthrough moments"""
        return len(self.related_breakthroughs) > 0


@dataclass
class BreakthroughEvent:
    """
    Represents a detected breakthrough moment with supporting evidence.

    A breakthrough is identified by multiple converging signals:
    velocity spikes, semantic emergence, architectural changes, etc.
    """

    id: str  # Unique identifier (e.g., "nov_3_p1_polish")
    date: str  # ISO format date
    name: str  # Human-readable name
    description: str  # What happened
    signals: Dict[BreakthroughSignal, Any]  # Signal type -> evidence
    confidence: float  # 0.0 to 1.0 detection confidence
    related_patterns: List[str]  # Pattern IDs that emerged/changed
    related_adrs: List[str]  # ADR numbers created
    related_issues: List[str]  # Issue numbers closed
    agent_sessions: int  # Number of parallel agent sessions
    velocity_multiplier: float  # How much faster than normal
    semantic_concepts: List[str]  # New concepts/terms that emerged

    @property
    def signal_count(self) -> int:
        """Count of distinct breakthrough signals detected"""
        return len(self.signals)

    @property
    def is_high_confidence(self) -> bool:
        """Check if this is a high-confidence breakthrough (>0.8)"""
        return self.confidence >= 0.8

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "date": self.date,
            "name": self.name,
            "description": self.description,
            "signals": {signal.value: value for signal, value in self.signals.items()},
            "confidence": self.confidence,
            "related_patterns": self.related_patterns,
            "related_adrs": self.related_adrs,
            "related_issues": self.related_issues,
            "agent_sessions": self.agent_sessions,
            "velocity_multiplier": self.velocity_multiplier,
            "semantic_concepts": self.semantic_concepts,
            "signal_count": self.signal_count,
            "is_high_confidence": self.is_high_confidence,
        }


class BaseAnalyzer(ABC):
    """
    Abstract base class for all pattern analyzers.

    Each analyzer focuses on a specific layer of pattern detection:
    - TemporalAnalyzer: When/how fast patterns change (git, session logs)
    - SemanticAnalyzer: What concepts emerge/evolve (term tracking)
    - StructuralAnalyzer: How architecture evolves (Serena, ADRs)
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results: Dict[str, Any] = {}

    @abstractmethod
    async def analyze(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Run analysis for the specified time period.

        Args:
            start_date: Analysis window start (None = earliest available)
            end_date: Analysis window end (None = now)

        Returns:
            Dictionary of analysis results with analyzer-specific structure
        """
        pass

    @abstractmethod
    def get_breakthrough_signals(self) -> Dict[BreakthroughSignal, Any]:
        """
        Extract breakthrough signals from analysis results.

        Returns:
            Dictionary mapping signal types to evidence
        """
        pass

    def get_results(self) -> Dict[str, Any]:
        """Get the most recent analysis results"""
        return self.results

    def _format_date(self, dt: datetime) -> str:
        """Format datetime as ISO string"""
        return dt.isoformat()

    def _parse_date(self, date_str: str) -> datetime:
        """Parse ISO date string to datetime"""
        return datetime.fromisoformat(date_str)
