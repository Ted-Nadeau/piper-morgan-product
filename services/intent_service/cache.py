"""
Intent classification caching layer.

Reduces redundant classifications for repeated queries.
Implements in-memory cache with TTL-based expiration.

Created: October 5, 2025
Issue: #206 (CORE-GREAT-4B Phase 3)
"""

import hashlib
import logging
import time
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class IntentCache:
    """
    In-memory cache for intent classification results.

    Uses text hash as key to handle case variations and whitespace.
    Implements TTL-based expiration for cache entries.

    Performance Target:
    - Hit rate >60% for production workload
    - Latency reduction: ~1ms → <0.1ms for cache hits
    """

    def __init__(self, ttl: int = 3600):
        """
        Initialize cache.

        Args:
            ttl: Time-to-live in seconds (default 1 hour)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl
        self.hits = 0
        self.misses = 0
        logger.info(f"IntentCache initialized with TTL={ttl}s")

    def get(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Get cached intent result if exists and not expired.

        Args:
            text: User input text

        Returns:
            Cached intent dict or None if miss/expired
        """
        key = self._hash_text(text)

        if key in self.cache:
            entry = self.cache[key]

            # Check expiration
            if time.time() < entry["expires_at"]:
                self.hits += 1
                logger.debug(f"Cache HIT for: {text[:50]}...")
                return entry["intent"]
            else:
                # Expired - remove
                del self.cache[key]
                logger.debug(f"Cache EXPIRED for: {text[:50]}...")

        self.misses += 1
        logger.debug(f"Cache MISS for: {text[:50]}...")
        return None

    def set(self, text: str, intent: Dict[str, Any]) -> None:
        """
        Cache intent classification result.

        Args:
            text: User input text
            intent: Classification result to cache
        """
        key = self._hash_text(text)

        self.cache[key] = {
            "intent": intent,
            "expires_at": time.time() + self.ttl,
            "cached_at": time.time(),
        }

        logger.debug(f"Cache SET for: {text[:50]}...")

    def invalidate(self, text: str) -> bool:
        """
        Remove specific entry from cache.

        Args:
            text: User input text to invalidate

        Returns:
            True if entry was removed, False if not found
        """
        key = self._hash_text(text)
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache INVALIDATED for: {text[:50]}...")
            return True
        return False

    def clear(self) -> None:
        """Clear entire cache and reset metrics."""
        count = len(self.cache)
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info(f"Cache CLEARED ({count} entries removed)")

    def get_metrics(self) -> Dict[str, Any]:
        """
        Return cache performance metrics.

        Returns:
            Dict with hits, misses, hit_rate, size, ttl
        """
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0

        return {
            "hits": self.hits,
            "misses": self.misses,
            "total_requests": total,
            "hit_rate_percent": round(hit_rate, 2),
            "cache_size": len(self.cache),
            "ttl_seconds": self.ttl,
        }

    def _hash_text(self, text: str) -> str:
        """
        Create cache key from text.

        Normalizes text (lowercase, strip) before hashing to handle
        case variations and whitespace differences.

        Args:
            text: User input text

        Returns:
            MD5 hash of normalized text
        """
        normalized = text.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()
