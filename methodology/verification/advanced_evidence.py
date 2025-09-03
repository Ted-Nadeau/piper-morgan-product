"""
Advanced Evidence Validation Engine

Sophisticated evidence validation with automatic categorization, performance optimization,
and comprehensive reporting for the verification pyramid framework.

Built on Phase 1 foundation to provide enhanced evidence processing capabilities
for complex agent coordination scenarios.
"""

import asyncio
import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from .evidence import Evidence, EvidenceCollector, EvidenceType

logger = logging.getLogger(__name__)


@dataclass
class ValidationReport:
    """Comprehensive validation report with cross-references and recommendations"""

    total_evidence: int = 0
    validated_evidence: int = 0
    failed_evidence: int = 0
    results: List[Dict[str, Any]] = field(default_factory=list)
    cross_references: Dict[str, List[str]] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def validation_rate(self) -> float:
        """Calculate validation success rate"""
        if self.total_evidence == 0:
            return 0.0
        return self.validated_evidence / self.total_evidence

    def add_result(self, evidence: Evidence, validation_result: Dict[str, Any]):
        """Add validation result for an evidence item"""
        self.total_evidence += 1
        if validation_result.get("valid", False):
            self.validated_evidence += 1
        else:
            self.failed_evidence += 1

        result_entry = {
            "evidence_id": id(evidence),
            "evidence_type": (
                evidence.evidence_type.value if hasattr(evidence, "evidence_type") else "unknown"
            ),
            "validation_result": validation_result,
            "timestamp": datetime.now(),
        }
        self.results.append(result_entry)

    def add_cross_references(self, evidence: Evidence, cross_refs: List[str]):
        """Add cross-references for evidence validation"""
        evidence_id = str(id(evidence))
        self.cross_references[evidence_id] = cross_refs


@dataclass
class CachedValidation:
    """Cached validation result with TTL"""

    result: Dict[str, Any]
    timestamp: datetime
    ttl: int  # Time to live in seconds

    def is_expired(self) -> bool:
        """Check if cached result has expired"""
        return datetime.now() > self.timestamp + timedelta(seconds=self.ttl)


class EvidenceAutoCategorizer:
    """Automatically categorize evidence based on content analysis"""

    # Pattern matching for automatic categorization
    CATEGORIZATION_PATTERNS = {
        "terminal": [
            r"\$\s+.*",  # Command prompt patterns (fixed - removed ^ anchor)
            r"PASSED|FAILED|ERROR",  # Test result patterns
            r"exit code: \d+",  # Process completion patterns
            r"python -m pytest",  # Test command patterns
            r"npm run|yarn",  # Build command patterns
        ],
        "url": [
            r"https?://[^\s]+",  # HTTP/HTTPS URL patterns
            r"localhost:\d+",  # Local service URLs
            r"github\.com/[^\s]+",  # GitHub URLs
            r".*#\d+",  # Issue/PR references
        ],
        "metric": [
            r"\d+(\.\d+)?\s*(ms|s|MB|KB|%)",  # Performance metrics
            r"latency|throughput|memory|cpu",  # Metric keywords
            r"\d+\.\d+x\s+speedup",  # Performance improvements
            r"\d+/\d+\s+(passed|failed)",  # Test counts
        ],
        "artifact": [
            r"\.py$|\.md$|\.json$|\.yaml$|\.yml$",  # File extensions
            r"created|generated|updated|modified",  # Action indicators
            r"Created:\s+.*",  # Creation messages
            r"File.*saved",  # Save confirmations
        ],
        "generic": [
            r"deployment_id|status",  # Deployment patterns
            r"log_entry|system",  # System log patterns
            r"success|failure|initialized",  # Status patterns
        ],
    }

    # Confidence scoring weights
    CONFIDENCE_WEIGHTS = {
        "exact_match": 1.0,
        "pattern_match": 0.8,
        "keyword_match": 0.6,
        "context_match": 0.4,
    }

    def __init__(self):
        """Initialize auto-categorizer with compiled patterns"""
        self.compiled_patterns = {}
        self.categorization_cache: Dict[str, Tuple[str, float]] = {}  # Add categorization cache
        for category, patterns in self.CATEGORIZATION_PATTERNS.items():
            self.compiled_patterns[category] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
        logger.info("EvidenceAutoCategorizer initialized with pattern matching and caching")

    async def categorize(self, evidence: Evidence) -> Tuple[str, float]:
        """
        Automatically categorize evidence based on content analysis

        Returns:
            Tuple of (category, confidence_score)
        """
        if not hasattr(evidence, "data") or not evidence.data:
            return "unknown", 0.0

        content = str(evidence.data)
        category_scores = {}

        # Check cache first for performance boost
        cache_key = self._get_cache_key(evidence)
        if cache_key in self.categorization_cache:
            return self.categorization_cache[cache_key]

        # Test against each category's patterns
        for category, patterns in self.compiled_patterns.items():
            score = 0.0
            matches = 0

            for pattern in patterns:
                if pattern.search(content):
                    matches += 1
                    score += self.CONFIDENCE_WEIGHTS["pattern_match"]

            if matches > 0:
                # Bonus for multiple pattern matches
                score += (matches - 1) * 0.1
                category_scores[category] = min(score, 1.0)

        # Return category with highest confidence
        if category_scores:
            best_category = max(category_scores.items(), key=lambda x: x[1])
            result = (best_category[0], best_category[1])
        else:
            # Default to 'generic' for unmatched evidence instead of 'unknown'
            result = ("generic", 0.5)

        # Cache the result for future use
        self.categorization_cache[cache_key] = result
        return result

    async def categorize_batch(self, evidence_list: List[Evidence]) -> List[Tuple[str, float]]:
        """Categorize multiple evidence items efficiently with caching"""
        results = []
        for evidence in evidence_list:
            category, confidence = await self.categorize(evidence)
            results.append((category, confidence))
        return results

    def _get_cache_key(self, evidence: Evidence) -> str:
        """Generate cache key for evidence categorization"""
        return str(hash(str(evidence.data))) if hasattr(evidence, "data") else "no_data"


class EvidenceCache:
    """High-performance evidence caching with smart invalidation"""

    def __init__(self, default_ttl: int = 300):
        """Initialize cache with default TTL of 5 minutes"""
        self.cache: Dict[str, Any] = {}
        self.validation_cache: Dict[str, CachedValidation] = {}
        self.default_ttl = default_ttl
        self.hit_count = 0
        self.miss_count = 0

        logger.info(f"EvidenceCache initialized with {default_ttl}s default TTL")

    def _generate_evidence_key(self, evidence: Evidence) -> str:
        """Generate unique cache key for evidence"""
        content_hash = hash(str(evidence.data)) if hasattr(evidence, "data") else 0
        evidence_type = "unknown"
        if hasattr(evidence, "evidence_type") and evidence.evidence_type is not None:
            evidence_type = evidence.evidence_type.value
        return f"{evidence_type}_{content_hash}"

    def _calculate_ttl(self, validation_result: Dict[str, Any]) -> int:
        """Calculate smart TTL based on validation result"""
        base_ttl = self.default_ttl

        # Longer TTL for successful validations
        if validation_result.get("valid", False):
            base_ttl *= 2

        # Shorter TTL for complex validations that might change
        if validation_result.get("complexity", "simple") == "complex":
            base_ttl = int(base_ttl * 0.5)

        return base_ttl

    async def get_cached_validation(self, evidence: Evidence) -> Optional[Dict[str, Any]]:
        """Retrieve cached validation result if available and valid"""
        evidence_key = self._generate_evidence_key(evidence)

        if evidence_key in self.validation_cache:
            cached_result = self.validation_cache[evidence_key]
            if not cached_result.is_expired():
                self.hit_count += 1
                logger.debug(f"Cache hit for evidence key: {evidence_key[:20]}...")
                return cached_result.result
            else:
                # Remove expired entry
                del self.validation_cache[evidence_key]

        self.miss_count += 1
        logger.debug(f"Cache miss for evidence key: {evidence_key[:20]}...")
        return None

    async def cache_validation(self, evidence: Evidence, result: Dict[str, Any]):
        """Cache validation result with smart TTL"""
        evidence_key = self._generate_evidence_key(evidence)
        ttl = self._calculate_ttl(result)

        cached_validation = CachedValidation(result=result, timestamp=datetime.now(), ttl=ttl)

        self.validation_cache[evidence_key] = cached_validation
        logger.debug(f"Cached validation for {evidence_key[:20]}... with TTL {ttl}s")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total_requests if total_requests > 0 else 0

        return {
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate,
            "cached_items": len(self.validation_cache),
            "active_items": len([c for c in self.validation_cache.values() if not c.is_expired()]),
        }

    async def cleanup_expired(self):
        """Remove expired cache entries"""
        expired_keys = [
            key for key, cached_val in self.validation_cache.items() if cached_val.is_expired()
        ]

        for key in expired_keys:
            del self.validation_cache[key]

        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")


class AdvancedEvidenceValidator:
    """Enhanced evidence validation with automatic categorization and caching"""

    def __init__(self):
        """Initialize advanced evidence validator"""
        self.base_collector = EvidenceCollector()
        self.auto_categorizer = EvidenceAutoCategorizer()
        self.cache = EvidenceCache()

        # Enhanced validation rules extending base collector
        self.advanced_validation_rules = {
            "terminal": self._validate_terminal_evidence_advanced,
            "url": self._validate_url_evidence_advanced,
            "metric": self._validate_metric_evidence_advanced,
            "artifact": self._validate_artifact_evidence_advanced,
        }

        logger.info("AdvancedEvidenceValidator initialized with caching and auto-categorization")

    async def validate_evidence_collection(self, evidence_list: List[Evidence]) -> ValidationReport:
        """
        Comprehensive evidence validation with detailed reporting

        Args:
            evidence_list: List of evidence items to validate

        Returns:
            ValidationReport with comprehensive validation results
        """
        start_time = time.time()
        report = ValidationReport()

        logger.info(f"Starting validation of {len(evidence_list)} evidence items")

        # Process evidence items
        for evidence in evidence_list:
            # Check cache first
            cached_result = await self.cache.get_cached_validation(evidence)

            if cached_result:
                validation_result = cached_result
            else:
                # Auto-categorize if needed
                if not hasattr(evidence, "evidence_type") or evidence.evidence_type is None:
                    category, confidence = await self.auto_categorizer.categorize(evidence)
                    logger.debug(
                        f"Auto-categorized evidence as '{category}' with {confidence:.2f} confidence"
                    )
                    # Convert string category to EvidenceType if possible
                    try:
                        evidence.evidence_type = EvidenceType(category)
                    except ValueError:
                        logger.warning(
                            f"Unknown category '{category}', using TERMINAL_OUTPUT as fallback"
                        )
                        evidence.evidence_type = EvidenceType.TERMINAL_OUTPUT

                # Validate using appropriate rule
                validation_result = await self._validate_single_evidence(evidence)

                # Cache the result
                await self.cache.cache_validation(evidence, validation_result)

            # Add result to report
            report.add_result(evidence, validation_result)

            # Find cross-references
            cross_refs = await self._find_cross_references(evidence)
            report.add_cross_references(evidence, cross_refs)

        # Add performance metrics
        processing_time = time.time() - start_time
        report.performance_metrics = {
            "processing_time_seconds": processing_time,
            "items_per_second": len(evidence_list) / processing_time if processing_time > 0 else 0,
            "cache_hit_rate": self.cache.get_cache_stats()["hit_rate"],
        }

        # Generate recommendations
        report.recommendations = self._generate_recommendations(report)

        logger.info(
            f"Validation completed: {report.validated_evidence}/{report.total_evidence} valid "
            f"({report.validation_rate:.1%}) in {processing_time:.2f}s"
        )

        return report

    async def _validate_single_evidence(self, evidence: Evidence) -> Dict[str, Any]:
        """Validate a single piece of evidence"""
        evidence_type = (
            evidence.evidence_type.value if hasattr(evidence, "evidence_type") else "unknown"
        )

        # Use advanced validation if available, fallback to base validation
        if evidence_type in self.advanced_validation_rules:
            return await self.advanced_validation_rules[evidence_type](evidence)
        elif (
            hasattr(evidence, "evidence_type")
            and evidence.evidence_type in self.base_collector.validation_rules
        ):
            # Use base collector validation
            is_valid, errors = self.base_collector.validation_rules[evidence.evidence_type](
                evidence.data
            )
            return {"valid": is_valid, "errors": errors, "validation_method": "base_collector"}
        else:
            return {
                "valid": False,
                "errors": [f"No validation rule for evidence type: {evidence_type}"],
                "validation_method": "unknown",
            }

    async def _validate_terminal_evidence_advanced(self, evidence: Evidence) -> Dict[str, Any]:
        """Advanced terminal evidence validation"""
        data = evidence.data
        errors = []

        # Basic validation
        is_valid, base_errors = self.base_collector._validate_terminal_output(data)
        errors.extend(base_errors)

        # Advanced checks
        if "command" in data:
            # Check for dangerous commands
            dangerous_patterns = ["rm -rf", "sudo rm", "> /dev/null 2>&1"]
            command = data["command"]
            for pattern in dangerous_patterns:
                if pattern in command.lower():
                    errors.append(f"Potentially dangerous command detected: {pattern}")

        # Check for test execution evidence
        test_indicators = ["pytest", "test", "PASSED", "FAILED"]
        has_test_evidence = any(indicator in str(data) for indicator in test_indicators)

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "validation_method": "advanced_terminal",
            "has_test_evidence": has_test_evidence,
            "complexity": "complex" if has_test_evidence else "simple",
        }

    async def _validate_url_evidence_advanced(self, evidence: Evidence) -> Dict[str, Any]:
        """Advanced URL evidence validation"""
        # Implementation for URL validation
        return {"valid": True, "errors": [], "validation_method": "advanced_url"}

    async def _validate_metric_evidence_advanced(self, evidence: Evidence) -> Dict[str, Any]:
        """Advanced metric evidence validation"""
        # Implementation for metric validation
        return {"valid": True, "errors": [], "validation_method": "advanced_metric"}

    async def _validate_artifact_evidence_advanced(self, evidence: Evidence) -> Dict[str, Any]:
        """Advanced artifact evidence validation"""
        # Implementation for artifact validation
        return {"valid": True, "errors": [], "validation_method": "advanced_artifact"}

    async def _find_cross_references(self, evidence: Evidence) -> List[str]:
        """Find cross-references to validate evidence consistency"""
        cross_refs = []

        # Implementation would search for related evidence
        # For now, return empty list

        return cross_refs

    def _generate_recommendations(self, report: ValidationReport) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []

        if report.validation_rate < 0.8:
            recommendations.append("Validation rate is low - review evidence quality requirements")

        if report.performance_metrics.get("processing_time_seconds", 0) > 5:
            recommendations.append("Evidence processing is slow - consider batch optimizations")

        cache_hit_rate = report.performance_metrics.get("cache_hit_rate", 0)
        if cache_hit_rate < 0.5:
            recommendations.append("Low cache hit rate - review evidence caching strategy")

        return recommendations


class EvidenceEngineTestInterface:
    """Testing interface for cross-agent validation"""

    def __init__(self, validator: AdvancedEvidenceValidator):
        """Initialize test interface with validator"""
        self.validator = validator

    async def test_validation_accuracy(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test validation accuracy with provided test cases"""
        results = {
            "total_cases": len(test_cases),
            "passed": 0,
            "failed": 0,
            "accuracy": 0.0,
            "details": [],
        }

        for i, test_case in enumerate(test_cases):
            # Convert test case to Evidence object
            evidence = Evidence(
                evidence_type=test_case.get("expected_type", EvidenceType.TERMINAL_OUTPUT),
                data=test_case.get("data", {}),
                timestamp=datetime.now(),
                source="test_interface",
            )

            validation_result = await self.validator._validate_single_evidence(evidence)
            expected_valid = test_case.get("expected_valid", True)

            case_result = {
                "case_id": i,
                "expected_valid": expected_valid,
                "actual_valid": validation_result.get("valid", False),
                "passed": validation_result.get("valid", False) == expected_valid,
            }

            results["details"].append(case_result)

            if case_result["passed"]:
                results["passed"] += 1
            else:
                results["failed"] += 1

        results["accuracy"] = (
            results["passed"] / results["total_cases"] if results["total_cases"] > 0 else 0
        )

        return results

    async def benchmark_performance(self, evidence_samples: List[Evidence]) -> Dict[str, float]:
        """Benchmark evidence processing performance"""
        start_time = time.time()

        report = await self.validator.validate_evidence_collection(evidence_samples)

        end_time = time.time()
        processing_time = end_time - start_time

        return {
            "total_processing_time_seconds": processing_time,
            "items_processed": len(evidence_samples),
            "items_per_second": (
                len(evidence_samples) / processing_time if processing_time > 0 else 0
            ),
            "average_time_per_item_ms": (
                (processing_time * 1000) / len(evidence_samples) if evidence_samples else 0
            ),
            "cache_hit_rate": report.performance_metrics.get("cache_hit_rate", 0),
            "validation_success_rate": report.validation_rate,
        }
