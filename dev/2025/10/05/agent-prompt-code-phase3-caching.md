# Prompt for Code Agent: GREAT-4B Phase 3 - Caching Implementation

## Context

Phases 0-2 complete:
- 100% NL input coverage validated
- IntentEnforcementMiddleware operational
- Bypass prevention tests created

**Your task**: Implement caching layer to optimize intent classification performance.

## Session Log

Continue: `dev/2025/10/05/2025-10-05-1540-prog-code-log.md`

## Mission

**Create IntentCache service** and integrate with classifier to achieve >60% cache hit rate for common queries, reducing repeated classification overhead.

---

## Phase 3: Caching Implementation

### Step 1: Create Cache Service

Create: `services/intent_service/cache.py`

```python
"""
Intent classification caching layer.
Reduces redundant classifications for repeated queries.
"""
import hashlib
import json
import time
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class IntentCache:
    """
    In-memory cache for intent classification results.

    Uses text hash as key to handle case variations and whitespace.
    Implements TTL-based expiration.
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
            if time.time() < entry['expires_at']:
                self.hits += 1
                logger.debug(f"Cache HIT for: {text[:50]}...")
                return entry['intent']
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
            'intent': intent,
            'expires_at': time.time() + self.ttl,
            'cached_at': time.time()
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
        """Clear entire cache."""
        count = len(self.cache)
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info(f"Cache CLEARED ({count} entries removed)")

    def get_metrics(self) -> Dict[str, Any]:
        """
        Return cache performance metrics.

        Returns:
            Dict with hits, misses, hit_rate, size
        """
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0

        return {
            'hits': self.hits,
            'misses': self.misses,
            'total_requests': total,
            'hit_rate_percent': round(hit_rate, 2),
            'cache_size': len(self.cache),
            'ttl_seconds': self.ttl
        }

    def _hash_text(self, text: str) -> str:
        """
        Create cache key from text.

        Normalizes text (lowercase, strip) before hashing.

        Args:
            text: User input text

        Returns:
            MD5 hash of normalized text
        """
        normalized = text.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()
```

### Step 2: Integrate with Classifier

Edit: `services/intent_service/classifier.py`

Find the `classify` method and wrap with cache:

```python
from .cache import IntentCache

class IntentClassifier:
    def __init__(self):
        # ... existing init code ...
        self.cache = IntentCache(ttl=3600)  # 1 hour TTL
        logger.info("IntentCache integrated with classifier")

    async def classify(self, text: str, use_cache: bool = True):
        """
        Classify user intent with caching.

        Args:
            text: User input text
            use_cache: Whether to use cache (default True)
        """
        # Check cache first (if enabled)
        if use_cache:
            cached_result = self.cache.get(text)
            if cached_result is not None:
                logger.info(f"Returning cached intent for: {text[:50]}...")
                return cached_result

        # Cache miss - perform classification
        logger.info(f"Classifying (no cache): {text[:50]}...")
        result = await self._classify_internal(text)

        # Cache the result (if caching enabled)
        if use_cache:
            self.cache.set(text, result)

        return result

    async def _classify_internal(self, text: str):
        """
        Internal classification logic (rename existing classify method).
        """
        # ... existing classification logic ...
        pass
```

**Note**: You'll need to rename the existing `classify` method to `_classify_internal` and create new `classify` method with cache wrapper.

### Step 3: Add Cache Monitoring Endpoint

Add to `web/app.py`:

```python
@app.get("/api/admin/intent-cache-metrics")
async def intent_cache_metrics():
    """Get intent cache performance metrics."""
    from services.intent_service import classifier

    if hasattr(classifier, 'cache'):
        metrics = classifier.cache.get_metrics()
        return {
            "cache_enabled": True,
            "metrics": metrics,
            "status": "operational"
        }
    else:
        return {
            "cache_enabled": False,
            "status": "not_configured"
        }

@app.post("/api/admin/intent-cache-clear")
async def clear_intent_cache():
    """Clear the intent cache (admin only)."""
    from services.intent_service import classifier

    if hasattr(classifier, 'cache'):
        classifier.cache.clear()
        return {"status": "cache_cleared"}
    else:
        return {"status": "cache_not_configured"}
```

### Step 4: Test Cache Behavior

Create test script: `dev/2025/10/05/test_cache_behavior.py`

```python
"""Test intent cache behavior."""
import asyncio
from services.intent_service import classifier

async def test_cache():
    """Test cache hits and misses."""

    test_queries = [
        "What day is it?",
        "What's my schedule?",
        "What day is it?",  # Duplicate - should hit cache
        "Create an issue about login bug",
        "What's my schedule?",  # Duplicate - should hit cache
        "What day is it?",  # Duplicate - should hit cache
    ]

    print("Testing cache behavior...\n")

    for i, query in enumerate(test_queries, 1):
        print(f"{i}. Query: {query}")
        result = await classifier.classify(query)
        print(f"   Intent: {result.get('intent', 'unknown')}")

        metrics = classifier.cache.get_metrics()
        print(f"   Cache: {metrics['hits']} hits, {metrics['misses']} misses, "
              f"{metrics['hit_rate_percent']}% hit rate\n")

    print("\nFinal Metrics:")
    final_metrics = classifier.cache.get_metrics()
    print(f"  Total Requests: {final_metrics['total_requests']}")
    print(f"  Cache Hits: {final_metrics['hits']}")
    print(f"  Cache Misses: {final_metrics['misses']}")
    print(f"  Hit Rate: {final_metrics['hit_rate_percent']}%")
    print(f"  Cache Size: {final_metrics['cache_size']} entries")

    # Verify hit rate
    if final_metrics['hit_rate_percent'] >= 50:
        print("\n✅ Cache performing well (>50% hit rate)")
    else:
        print(f"\n⚠️  Cache hit rate below 50%")

if __name__ == "__main__":
    asyncio.run(test_cache())
```

Run test:
```bash
python3 dev/2025/10/05/test_cache_behavior.py
```

Expected output showing cache hits for duplicates.

### Step 5: Production Testing

```bash
# Start server
python main.py

# Test cache metrics endpoint
curl http://localhost:8001/api/admin/intent-cache-metrics

# Expected:
# {
#   "cache_enabled": true,
#   "metrics": {
#     "hits": 0,
#     "misses": 0,
#     "hit_rate_percent": 0,
#     "cache_size": 0
#   }
# }

# Make some requests
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"text": "What day is it?"}'

# Make same request again (should hit cache)
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"text": "What day is it?"}'

# Check metrics again
curl http://localhost:8001/api/admin/intent-cache-metrics

# Should show 1 hit, 1 miss, 50% hit rate
```

### Step 6: Document Implementation

Create: `dev/2025/10/05/cache-implementation.md`

```markdown
# Intent Cache Implementation

## Purpose
Reduce redundant intent classifications for repeated queries.
Improve response time for common user inputs.

## Design

### Cache Strategy
- **Type**: In-memory hash table
- **Key**: MD5 hash of normalized text (lowercase, trimmed)
- **TTL**: 1 hour (3600 seconds)
- **Eviction**: Lazy expiration on access

### Integration Point
`IntentClassifier.classify()` method wraps cache:
1. Check cache for text hash
2. If hit and not expired → return cached result
3. If miss/expired → classify via internal method
4. Cache result for future requests

### Performance Target
- **Hit Rate**: >60% for production workload
- **Latency Reduction**: ~1ms → <0.1ms for cache hits

## Configuration

### TTL Adjustment
Edit `services/intent_service/classifier.py`:
```python
self.cache = IntentCache(ttl=7200)  # 2 hours
```

### Disable Caching
```python
result = await classifier.classify(text, use_cache=False)
```

## Monitoring

### Metrics Endpoint
`GET /api/admin/intent-cache-metrics`

Returns:
- hits: Number of cache hits
- misses: Number of cache misses
- hit_rate_percent: Percentage of requests served from cache
- cache_size: Number of entries currently cached

### Cache Management
`POST /api/admin/intent-cache-clear` - Clear cache manually

## Future Enhancements
- Redis backend for distributed caching
- Configurable TTL per intent category
- Pre-warming cache with common queries
- Cache size limits with LRU eviction
```

---

## Success Criteria

- [ ] IntentCache service created (cache.py)
- [ ] Integrated with classifier
- [ ] Metrics endpoint operational
- [ ] Test script validates cache behavior
- [ ] Hit rate >50% in tests (target >60% in production)
- [ ] Server starts without errors
- [ ] Documentation complete
- [ ] Git commit created

---

## Evidence Format

```bash
$ python3 dev/2025/10/05/test_cache_behavior.py
Testing cache behavior...

1. Query: What day is it?
   Intent: TEMPORAL
   Cache: 0 hits, 1 misses, 0.0% hit rate

2. Query: What's my schedule?
   Intent: TEMPORAL
   Cache: 0 hits, 2 misses, 0.0% hit rate

3. Query: What day is it?
   Intent: TEMPORAL
   Cache: 1 hits, 2 misses, 33.33% hit rate

...

Final Metrics:
  Total Requests: 6
  Cache Hits: 3
  Cache Misses: 3
  Hit Rate: 50.0%
  Cache Size: 3 entries

✅ Cache performing well (>50% hit rate)

$ curl http://localhost:8001/api/admin/intent-cache-metrics
{
  "cache_enabled": true,
  "metrics": {
    "hits": 15,
    "misses": 8,
    "hit_rate_percent": 65.22
  }
}
```

---

**Effort**: Medium (~45 minutes)
**Complexity**: Moderate (new service + integration)
