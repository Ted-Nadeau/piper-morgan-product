"""
API Key Strength Analysis Service

Analyzes API key strength including length, entropy, character diversity,
and pattern detection. Provides security scoring and recommendations.

Issue #252 CORE-KEYS-STRENGTH-VALIDATION
"""

import logging
import math
import re
from dataclasses import dataclass
from typing import Dict, Set

logger = logging.getLogger(__name__)


@dataclass
class KeyStrength:
    """Results of key strength analysis"""

    length_score: float
    entropy_score: float
    character_diversity_score: float
    pattern_score: float
    overall_score: float
    recommendations: list[str]
    security_level: str  # 'weak', 'medium', 'strong'


class KeyStrengthAnalyzer:
    """Analyzes API key strength and security characteristics"""

    def __init__(self):
        """Initialize key strength analyzer"""
        self.min_scores = {
            "length": 0.7,
            "entropy": 0.6,
            "diversity": 0.7,
            "pattern": 0.8,
            "overall": 0.7,
        }

    def analyze_key_strength(self, api_key: str, provider: str = None) -> KeyStrength:
        """
        Analyze API key strength across multiple dimensions

        Args:
            api_key: The API key to analyze
            provider: Optional provider for context-specific analysis

        Returns:
            KeyStrength object with detailed analysis
        """
        try:
            # Perform individual analyses
            length_score = self._check_length(api_key, provider)
            entropy_score = self._calculate_entropy(api_key)
            diversity_score = self._check_character_diversity(api_key)
            pattern_score = self._check_patterns(api_key)

            # Calculate overall score (weighted average)
            overall_score = self._calculate_overall_score(
                length_score, entropy_score, diversity_score, pattern_score
            )

            # Generate recommendations
            recommendations = self._generate_recommendations(
                length_score, entropy_score, diversity_score, pattern_score, provider
            )

            # Determine security level
            security_level = self._determine_security_level(overall_score)

            return KeyStrength(
                length_score=length_score,
                entropy_score=entropy_score,
                character_diversity_score=diversity_score,
                pattern_score=pattern_score,
                overall_score=overall_score,
                recommendations=recommendations,
                security_level=security_level,
            )

        except Exception as e:
            logger.error(f"Failed to analyze key strength: {e}")
            return KeyStrength(
                length_score=0.0,
                entropy_score=0.0,
                character_diversity_score=0.0,
                pattern_score=0.0,
                overall_score=0.0,
                recommendations=["Error analyzing key strength"],
                security_level="unknown",
            )

    def _check_length(self, key: str, provider: str = None) -> float:
        """Check if key meets minimum length requirements"""
        length = len(key)

        # Provider-specific length requirements
        min_lengths = {
            "openai": 51,  # sk-... format
            "anthropic": 108,  # sk-ant-... format
            "github": 40,  # ghp_... format
            "default": 32,  # General minimum
        }

        min_length = min_lengths.get(provider, min_lengths["default"])

        if length < min_length:
            return 0.0
        elif length < min_length * 1.2:  # 20% buffer
            return 0.7
        else:
            return 1.0

    def _calculate_entropy(self, key: str) -> float:
        """Calculate Shannon entropy of the key"""
        if not key:
            return 0.0

        # Count character frequencies
        char_counts = {}
        for char in key:
            char_counts[char] = char_counts.get(char, 0) + 1

        # Calculate Shannon entropy
        entropy = 0.0
        key_length = len(key)

        for count in char_counts.values():
            probability = count / key_length
            if probability > 0:
                entropy -= probability * math.log2(probability)

        # Normalize to 0-1 scale (max entropy for ASCII is ~6.64 bits)
        max_entropy = 6.64
        normalized_entropy = min(entropy / max_entropy, 1.0)

        return normalized_entropy

    def _check_character_diversity(self, key: str) -> float:
        """Check use of different character types"""
        if not key:
            return 0.0

        char_types = {
            "lowercase": bool(re.search(r"[a-z]", key)),
            "uppercase": bool(re.search(r"[A-Z]", key)),
            "digits": bool(re.search(r"[0-9]", key)),
            "symbols": bool(re.search(r"[^a-zA-Z0-9]", key)),
        }

        # Count unique character types
        unique_types = sum(char_types.values())

        # Score based on diversity (4 types = perfect score)
        diversity_score = unique_types / 4.0

        return diversity_score

    def _check_patterns(self, key: str) -> float:
        """Check for common weak patterns"""
        if not key:
            return 0.0

        pattern_penalties = 0.0

        # Check for repeating characters (more than 3 in a row)
        if re.search(r"(.)\1{3,}", key):
            pattern_penalties += 0.3

        # Check for sequential patterns (abc, 123, etc.)
        sequential_patterns = [
            r"abcdefg",
            r"1234567",
            r"qwerty",
            r"password",
            r"ABCDEFG",
            r"7654321",
            r"fedcba",
        ]

        for pattern in sequential_patterns:
            if pattern.lower() in key.lower():
                pattern_penalties += 0.4

        # Check for common substitutions (@ for a, 3 for e, etc.)
        common_substitutions = [r"p@ssw0rd", r"@dmin", r"t3st", r"k3y"]

        for pattern in common_substitutions:
            if re.search(pattern, key, re.IGNORECASE):
                pattern_penalties += 0.2

        # Check for keyboard patterns
        keyboard_patterns = [r"qwertyui", r"asdfghjk", r"zxcvbnm", r"12345678", r"87654321"]

        for pattern in keyboard_patterns:
            if pattern in key.lower():
                pattern_penalties += 0.3

        # Return score (1.0 - penalties, minimum 0.0)
        pattern_score = max(1.0 - pattern_penalties, 0.0)

        return pattern_score

    def _calculate_overall_score(
        self, length: float, entropy: float, diversity: float, pattern: float
    ) -> float:
        """Calculate weighted overall score"""
        # Weights for different aspects
        weights = {"length": 0.2, "entropy": 0.3, "diversity": 0.2, "pattern": 0.3}

        overall = (
            length * weights["length"]
            + entropy * weights["entropy"]
            + diversity * weights["diversity"]
            + pattern * weights["pattern"]
        )

        return round(overall, 3)

    def _generate_recommendations(
        self, length: float, entropy: float, diversity: float, pattern: float, provider: str = None
    ) -> list[str]:
        """Generate improvement recommendations"""
        recommendations = []

        if length < self.min_scores["length"]:
            min_length = 51 if provider == "openai" else 40 if provider == "github" else 32
            recommendations.append(f"Use a longer key (minimum {min_length} characters)")

        if entropy < self.min_scores["entropy"]:
            recommendations.append("Increase randomness - avoid predictable patterns")

        if diversity < self.min_scores["diversity"]:
            recommendations.append("Use a mix of uppercase, lowercase, numbers, and symbols")

        if pattern < self.min_scores["pattern"]:
            recommendations.append("Avoid common patterns, sequences, and dictionary words")

        if not recommendations:
            recommendations.append("Key strength is good")

        return recommendations

    def _determine_security_level(self, overall_score: float) -> str:
        """Determine security level based on overall score"""
        if overall_score >= 0.8:
            return "strong"
        elif overall_score >= 0.6:
            return "medium"
        else:
            return "weak"

    def is_key_acceptable(
        self, key_strength: KeyStrength, allow_medium: bool = True
    ) -> tuple[bool, str]:
        """
        Check if key strength is acceptable for storage

        Args:
            key_strength: Results from analyze_key_strength
            allow_medium: Whether to accept medium-strength keys

        Returns:
            Tuple of (acceptable, reason)
        """
        if key_strength.security_level == "strong":
            return True, "Key strength is strong"

        if key_strength.security_level == "medium" and allow_medium:
            return True, "Key strength is acceptable (medium)"

        if key_strength.security_level == "medium" and not allow_medium:
            return (
                False,
                f"Key strength too low ({key_strength.overall_score:.0%}). Requires strong key.",
            )

        # Weak key
        return (
            False,
            f"Key strength too low ({key_strength.overall_score:.0%}). {key_strength.recommendations[0] if key_strength.recommendations else 'Use a stronger key.'}",
        )
