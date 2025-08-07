"""
Redis Connection Factory - Following AsyncSessionFactory Pattern
Provides Redis client management with connection pooling and health monitoring
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import redis.asyncio as redis
import structlog

from services.health.integration_health_monitor import health_monitor

logger = structlog.get_logger()


class RedisFactory:
    """Redis client factory following AsyncSessionFactory pattern"""

    _redis_pool: Optional[redis.ConnectionPool] = None

    @classmethod
    async def initialize(cls) -> None:
        """Initialize Redis connection pool"""
        if cls._redis_pool is None:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
            cls._redis_pool = redis.ConnectionPool.from_url(
                redis_url,
                max_connections=20,
                retry_on_timeout=True,
                decode_responses=False,  # Keep bytes for JSON serialization
            )

            logger.info("Redis connection pool initialized", redis_url=redis_url)

    @classmethod
    async def create_client(cls) -> redis.Redis:
        """Create Redis client from pool"""
        await cls.initialize()
        client = redis.Redis(connection_pool=cls._redis_pool)

        # Test connection
        try:
            await client.ping()
            health_monitor.record_success("redis_connection", 5.0, {"status": "connected"})
        except Exception as e:
            health_monitor.record_failure("redis_connection", str(e))
            logger.error(f"Redis connection test failed: {e}")

        return client

    @classmethod
    @asynccontextmanager
    async def redis_scope(cls) -> AsyncGenerator[redis.Redis, None]:
        """Redis client context manager following AsyncSessionFactory pattern"""
        client = await cls.create_client()
        try:
            yield client
        finally:
            await client.close()

    @classmethod
    async def close_pool(cls) -> None:
        """Close Redis connection pool"""
        if cls._redis_pool:
            await cls._redis_pool.disconnect()
            cls._redis_pool = None
            logger.info("Redis connection pool closed")
