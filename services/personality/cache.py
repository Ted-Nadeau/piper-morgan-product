"""
Profile caching implementation for <100ms performance
Thread-safe LRU cache with TTL and performance monitoring
"""

import logging
import threading
import time
from collections import OrderedDict
from typing import Optional

from .exceptions import CacheError
from .personality_profile import PersonalityProfile

logger = logging.getLogger(__name__)


class ProfileCache:
    """Thread-safe LRU cache for PersonalityProfile entities"""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 1800):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds  # 30 minutes default
        self.cache = OrderedDict()
        self.timestamps = {}
        self.lock = threading.RLock()

        # Performance tracking
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def get(self, user_id: str) -> Optional[PersonalityProfile]:
        """Get profile from cache with TTL check"""
        with self.lock:
            try:
                if user_id not in self.cache:
                    self.misses += 1
                    return None

                # Check TTL
                if self._is_expired(user_id):
                    self._remove(user_id)
                    self.misses += 1
                    return None

                # Move to end (most recently used)
                profile = self.cache[user_id]
                self.cache.move_to_end(user_id)
                self.hits += 1

                return profile

            except Exception as e:
                logger.error(f"Cache get error for user {user_id}: {e}")
                self.misses += 1
                return None

    def put(self, user_id: str, profile: PersonalityProfile):
        """Store profile in cache with eviction if needed"""
        with self.lock:
            try:
                # Remove if already exists
                if user_id in self.cache:
                    del self.cache[user_id]
                    del self.timestamps[user_id]

                # Add new entry
                self.cache[user_id] = profile
                self.timestamps[user_id] = time.time()

                # Move to end (most recently used)
                self.cache.move_to_end(user_id)

                # Evict oldest if over capacity
                while len(self.cache) > self.max_size:
                    oldest_user = next(iter(self.cache))
                    self._remove(oldest_user)
                    self.evictions += 1

            except Exception as e:
                logger.error(f"Cache put error for user {user_id}: {e}")
                raise CacheError(f"Failed to cache profile: {e}")

    def invalidate(self, user_id: str):
        """Remove specific user from cache"""
        with self.lock:
            if user_id in self.cache:
                self._remove(user_id)

    def clear(self):
        """Clear entire cache"""
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()

    def _is_expired(self, user_id: str) -> bool:
        """Check if cache entry has expired"""
        if user_id not in self.timestamps:
            return True

        age = time.time() - self.timestamps[user_id]
        return age > self.ttl_seconds

    def _remove(self, user_id: str):
        """Remove user from cache and timestamps"""
        if user_id in self.cache:
            del self.cache[user_id]
        if user_id in self.timestamps:
            del self.timestamps[user_id]

    def get_stats(self) -> dict:
        """Get cache performance statistics"""
        with self.lock:
            total_requests = self.hits + self.misses
            hit_rate = self.hits / total_requests if total_requests > 0 else 0.0

            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": hit_rate,
                "evictions": self.evictions,
                "ttl_seconds": self.ttl_seconds,
            }

    def cleanup_expired(self):
        """Remove expired entries (can be called periodically)"""
        with self.lock:
            expired_users = []
            for user_id in list(self.cache.keys()):
                if self._is_expired(user_id):
                    expired_users.append(user_id)

            for user_id in expired_users:
                self._remove(user_id)

            if expired_users:
                logger.info(f"Cleaned up {len(expired_users)} expired cache entries")
