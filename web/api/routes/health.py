"""
Production Health Check Endpoints
Provides health monitoring for database and system components

Issue #229 CORE-USERS-PROD: Database Production Hardening
"""

import time
from datetime import datetime, timezone
from typing import Any, Dict

import structlog
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from services.database.session_factory import AsyncSessionFactory

logger = structlog.get_logger()

# Health check router
router = APIRouter(prefix="/api/v1/health", tags=["health"])


class HealthStatus:
    """Health status levels"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@router.get("")
async def basic_health():
    """
    Basic health check endpoint.

    Returns simple status to verify API is running.
    """
    return {
        "status": HealthStatus.HEALTHY,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "piper-morgan",
    }


@router.get("/database")
async def database_health():
    """
    Database health check endpoint.

    Tests PostgreSQL connectivity, measures response time,
    and reports connection pool stats.

    Issue #229 CORE-USERS-PROD
    """
    try:
        start_time = time.time()

        # Test database connection and query
        async with AsyncSessionFactory.session_scope() as session:
            # Basic connectivity test
            result = await session.execute(text("SELECT 1 as health_check"))
            health_value = result.scalar()

            # Check database stats
            stats_query = text(
                """
                SELECT
                    count(*) as total_connections,
                    (SELECT count(*) FROM pg_stat_activity WHERE state = 'active') as active_connections,
                    (SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public') as table_count,
                    (SELECT pg_database_size(current_database())) as database_size_bytes
            """
            )
            stats_result = await session.execute(stats_query)
            stats = stats_result.fetchone()

            response_time = (time.time() - start_time) * 1000  # Convert to ms

            if health_value == 1:
                return {
                    "status": HealthStatus.HEALTHY,
                    "response_time_ms": round(response_time, 2),
                    "database": {
                        "total_connections": stats.total_connections,
                        "active_connections": stats.active_connections,
                        "table_count": stats.table_count,
                        "database_size_mb": round(stats.database_size_bytes / (1024 * 1024), 2),
                    },
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Database query returned unexpected result",
                )

    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}",
        )


@router.get("/detailed")
async def detailed_health():
    """
    Detailed health check with all components.

    Combines database health with system info.

    Issue #229 CORE-USERS-PROD
    """
    try:
        # Get database health
        db_start = time.time()
        db_health = await database_health()
        db_health["check_duration_ms"] = round((time.time() - db_start) * 1000, 2)

        # System info
        import psutil

        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        system_health = {
            "status": HealthStatus.HEALTHY,
            "cpu_percent": round(psutil.cpu_percent(interval=0.1), 1),
            "memory_percent": round(memory.percent, 1),
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "disk_percent": round(disk.percent, 1),
            "disk_free_gb": round(disk.free / (1024**3), 2),
        }

        # Determine overall status
        overall_status = HealthStatus.HEALTHY
        if (
            system_health["cpu_percent"] > 90
            or system_health["memory_percent"] > 90
            or system_health["disk_percent"] > 90
        ):
            overall_status = HealthStatus.UNHEALTHY
        elif (
            system_health["cpu_percent"] > 75
            or system_health["memory_percent"] > 75
            or system_health["disk_percent"] > 80
        ):
            overall_status = HealthStatus.DEGRADED

        return {
            "overall_status": overall_status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "components": {"database": db_health, "system": system_health},
            "service": "piper-morgan",
            "environment": "production",
        }

    except HTTPException:
        # Re-raise HTTP exceptions from database_health
        raise
    except Exception as e:
        logger.error("Detailed health check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}",
        )
