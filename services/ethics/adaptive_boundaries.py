"""
PM-087 Adaptive Boundaries System
Pattern learning from metadata only for enhanced boundary enforcement

Leverages existing infrastructure:
- services/infrastructure/monitoring/ethics_metrics.py
- services/infrastructure/logging/config.py
- services/domain/models.py patterns
"""

import asyncio
import hashlib
import json
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set

from services.domain.models import BoundaryViolation, EthicalDecision
from services.infrastructure.logging.config import get_ethics_logger
from services.infrastructure.monitoring.ethics_metrics import EthicsDecisionType, ethics_metrics


class PatternMetadata:
    """Metadata-only pattern information for learning"""

    def __init__(
        self, pattern_hash: str, frequency: int, first_seen: datetime, last_seen: datetime
    ):
        self.pattern_hash = pattern_hash
        self.frequency = frequency
        self.first_seen = first_seen
        self.last_seen = last_seen
        self.confidence_score = 0.0
        self.boundary_type = ""
        self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "pattern_hash": self.pattern_hash,
            "frequency": self.frequency,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "confidence_score": self.confidence_score,
            "boundary_type": self.boundary_type,
            "metadata": self.metadata,
        }


class AdaptiveBoundaries:
    """Adaptive boundary enforcement with pattern learning"""

    def __init__(self):
        self.ethics_logger = get_ethics_logger(__name__)
        self.metrics = ethics_metrics

        # Pattern learning storage (metadata only)
        self.learned_patterns: Dict[str, PatternMetadata] = {}
        self.pattern_frequency: Dict[str, int] = defaultdict(int)
        self.boundary_patterns: Dict[str, Set[str]] = defaultdict(set)

        # Learning configuration
        self.min_frequency_threshold = 3
        self.confidence_threshold = 0.7
        self.max_patterns_per_type = 50
        self.pattern_retention_days = 30

        # Performance tracking
        self.learning_operations_total = 0
        self.learning_errors = 0

    async def learn_from_decision(self, decision: EthicalDecision) -> None:
        """Learn from an ethics decision (metadata only)"""
        try:
            self.learning_operations_total += 1

            # Extract metadata patterns (no actual content)
            metadata_patterns = self._extract_metadata_patterns(decision)

            # Learn from each pattern
            for pattern_hash, pattern_data in metadata_patterns.items():
                await self._learn_pattern(pattern_hash, pattern_data, decision)

            # Record learning operation
            self.metrics.record_pattern_learning_operation(
                metadata_pattern="decision_learning", success=True
            )

            # Log learning activity
            self.ethics_logger.log_behavior_pattern(
                "pattern_learning",
                {
                    "patterns_processed": len(metadata_patterns),
                    "decision_id": decision.decision_id,
                    "boundary_type": decision.boundary_type,
                    "violation_detected": decision.violation_detected,
                },
            )

        except Exception as e:
            self.learning_errors += 1
            self.metrics.record_pattern_learning_operation(
                metadata_pattern="decision_learning", success=False
            )

            # Log error
            self.ethics_logger.log_boundary_violation(
                "learning_error", {"error": str(e), "decision_id": decision.decision_id}
            )

    async def learn_from_violation(self, violation: BoundaryViolation) -> None:
        """Learn from a boundary violation (metadata only)"""
        try:
            self.learning_operations_total += 1

            # Extract metadata patterns (no actual content)
            metadata_patterns = self._extract_violation_metadata_patterns(violation)

            # Learn from each pattern
            for pattern_hash, pattern_data in metadata_patterns.items():
                await self._learn_pattern(pattern_hash, pattern_data, violation)

            # Record learning operation
            self.metrics.record_pattern_learning_operation(
                metadata_pattern="violation_learning", success=True
            )

            # Log learning activity
            self.ethics_logger.log_behavior_pattern(
                "violation_learning",
                {
                    "patterns_processed": len(metadata_patterns),
                    "violation_id": violation.violation_id,
                    "violation_type": violation.violation_type,
                    "severity": violation.severity,
                },
            )

        except Exception as e:
            self.learning_errors += 1
            self.metrics.record_pattern_learning_operation(
                metadata_pattern="violation_learning", success=False
            )

            # Log error
            self.ethics_logger.log_boundary_violation(
                "learning_error", {"error": str(e), "violation_id": violation.violation_id}
            )

    async def get_adaptive_patterns(self, boundary_type: str) -> List[str]:
        """Get learned patterns for a boundary type"""
        patterns = []

        for pattern_hash, metadata in self.learned_patterns.items():
            if (
                metadata.boundary_type == boundary_type
                and metadata.confidence_score >= self.confidence_threshold
                and metadata.frequency >= self.min_frequency_threshold
            ):
                patterns.append(pattern_hash)

        return patterns

    async def update_confidence_scores(self) -> None:
        """Update confidence scores based on recent activity"""
        current_time = datetime.utcnow()

        for pattern_hash, metadata in self.learned_patterns.items():
            # Calculate confidence based on frequency and recency
            frequency_factor = min(metadata.frequency / 10.0, 1.0)
            recency_factor = 1.0 - min((current_time - metadata.last_seen).days / 30.0, 1.0)

            # Weighted confidence score
            metadata.confidence_score = (frequency_factor * 0.7) + (recency_factor * 0.3)

    async def cleanup_old_patterns(self) -> None:
        """Remove old patterns that are no longer relevant"""
        cutoff_date = datetime.utcnow() - timedelta(days=self.pattern_retention_days)

        patterns_to_remove = []
        for pattern_hash, metadata in self.learned_patterns.items():
            if (
                metadata.last_seen < cutoff_date
                and metadata.frequency < self.min_frequency_threshold
            ):
                patterns_to_remove.append(pattern_hash)

        for pattern_hash in patterns_to_remove:
            del self.learned_patterns[pattern_hash]

        # Log cleanup
        if patterns_to_remove:
            self.ethics_logger.log_behavior_pattern(
                "pattern_cleanup",
                {
                    "patterns_removed": len(patterns_to_remove),
                    "total_patterns": len(self.learned_patterns),
                },
            )

    def _extract_metadata_patterns(self, decision: EthicalDecision) -> Dict[str, Dict[str, Any]]:
        """Extract metadata patterns from decision (no content)"""
        patterns = {}

        # Create pattern hash from metadata
        metadata_str = json.dumps(
            {
                "boundary_type": decision.boundary_type,
                "violation_detected": decision.violation_detected,
                "content_length": decision.audit_data.get("content_length", 0),
                "session_id_hash": (
                    hashlib.md5(decision.session_id.encode()).hexdigest()
                    if decision.session_id
                    else ""
                ),
                "timestamp_hour": decision.timestamp.hour,
                "timestamp_weekday": decision.timestamp.weekday(),
            },
            sort_keys=True,
        )

        pattern_hash = hashlib.sha256(metadata_str.encode()).hexdigest()

        patterns[pattern_hash] = {
            "boundary_type": decision.boundary_type,
            "violation_detected": decision.violation_detected,
            "metadata": decision.audit_data,
            "timestamp": decision.timestamp,
        }

        return patterns

    def _extract_violation_metadata_patterns(
        self, violation: BoundaryViolation
    ) -> Dict[str, Dict[str, Any]]:
        """Extract metadata patterns from violation (no content)"""
        patterns = {}

        # Create pattern hash from metadata
        metadata_str = json.dumps(
            {
                "violation_type": violation.violation_type,
                "severity": violation.severity,
                "context_length": len(violation.context),
                "session_id_hash": (
                    hashlib.md5(violation.session_id.encode()).hexdigest()
                    if violation.session_id
                    else ""
                ),
                "timestamp_hour": violation.timestamp.hour,
                "timestamp_weekday": violation.timestamp.weekday(),
            },
            sort_keys=True,
        )

        pattern_hash = hashlib.sha256(metadata_str.encode()).hexdigest()

        patterns[pattern_hash] = {
            "violation_type": violation.violation_type,
            "severity": violation.severity,
            "metadata": violation.audit_data,
            "timestamp": violation.timestamp,
        }

        return patterns

    async def _learn_pattern(
        self, pattern_hash: str, pattern_data: Dict[str, Any], source: Any
    ) -> None:
        """Learn a new pattern or update existing pattern"""
        current_time = datetime.utcnow()

        if pattern_hash in self.learned_patterns:
            # Update existing pattern
            metadata = self.learned_patterns[pattern_hash]
            metadata.frequency += 1
            metadata.last_seen = current_time

            # Update metadata
            if isinstance(source, EthicalDecision):
                metadata.boundary_type = source.boundary_type
            elif isinstance(source, BoundaryViolation):
                metadata.boundary_type = source.violation_type

            # Update confidence
            await self._update_pattern_confidence(metadata)

        else:
            # Create new pattern
            metadata = PatternMetadata(
                pattern_hash=pattern_hash,
                frequency=1,
                first_seen=current_time,
                last_seen=current_time,
            )

            # Set boundary type
            if isinstance(source, EthicalDecision):
                metadata.boundary_type = source.boundary_type
            elif isinstance(source, BoundaryViolation):
                metadata.boundary_type = source.violation_type

            # Set initial confidence
            metadata.confidence_score = 0.1

            # Store pattern
            self.learned_patterns[pattern_hash] = metadata

            # Limit patterns per type
            await self._enforce_pattern_limits(metadata.boundary_type)

    async def _update_pattern_confidence(self, metadata: PatternMetadata) -> None:
        """Update pattern confidence based on frequency and recency"""
        # Simple confidence calculation
        frequency_factor = min(metadata.frequency / 10.0, 1.0)
        recency_factor = 1.0 - min((datetime.utcnow() - metadata.last_seen).days / 30.0, 1.0)

        metadata.confidence_score = (frequency_factor * 0.7) + (recency_factor * 0.3)

    async def _enforce_pattern_limits(self, boundary_type: str) -> None:
        """Enforce maximum patterns per boundary type"""
        type_patterns = [
            p for p in self.learned_patterns.values() if p.boundary_type == boundary_type
        ]

        if len(type_patterns) > self.max_patterns_per_type:
            # Remove lowest confidence patterns
            type_patterns.sort(key=lambda p: p.confidence_score)
            patterns_to_remove = type_patterns[: -self.max_patterns_per_type]

            for pattern in patterns_to_remove:
                del self.learned_patterns[pattern.pattern_hash]

    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning system statistics"""
        return {
            "total_patterns": len(self.learned_patterns),
            "learning_operations": self.learning_operations_total,
            "learning_errors": self.learning_errors,
            "patterns_by_type": {
                boundary_type: len(
                    [p for p in self.learned_patterns.values() if p.boundary_type == boundary_type]
                )
                for boundary_type in set(p.boundary_type for p in self.learned_patterns.values())
            },
            "high_confidence_patterns": len(
                [
                    p
                    for p in self.learned_patterns.values()
                    if p.confidence_score >= self.confidence_threshold
                ]
            ),
            "active_patterns": len(
                [
                    p
                    for p in self.learned_patterns.values()
                    if p.frequency >= self.min_frequency_threshold
                ]
            ),
        }


# Singleton instance
adaptive_boundaries = AdaptiveBoundaries()
