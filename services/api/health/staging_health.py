"""
Comprehensive Health Check System for Staging Environment
Provides detailed health monitoring for all PM-038 components
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import aiohttp
import psutil
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from services.database.connection import get_db_session
from services.infrastructure.config.mcp_configuration import get_config
from services.mcp.resources import MCPResourceManager

logger = logging.getLogger(__name__)

# Health check router for staging
staging_health_router = APIRouter(prefix="/health", tags=["health"])


class HealthStatus:
    """Health status levels"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class StagingHealthChecker:
    """Comprehensive health checker for staging environment"""

    def __init__(self):
        self.last_check_time = None
        self.cached_results = {}
        self.cache_ttl = 30  # 30 seconds

    async def get_comprehensive_health(self) -> Dict[str, Any]:
        """Get comprehensive health status for all components"""
        current_time = time.time()

        # Use cached results if recent
        if (
            self.last_check_time
            and current_time - self.last_check_time < self.cache_ttl
            and self.cached_results
        ):
            return self.cached_results

        health_checks = {
            "database": self._check_database_health(),
            "redis": self._check_redis_health(),
            "chromadb": self._check_chromadb_health(),
            "mcp_integration": self._check_mcp_health(),
            "system_resources": self._check_system_resources(),
            "api_endpoints": self._check_api_endpoints(),
            "external_services": self._check_external_services(),
        }

        # Execute all health checks concurrently
        results = {}
        for component, check_coro in health_checks.items():
            try:
                results[component] = await check_coro
            except Exception as e:
                logger.error(f"Health check failed for {component}: {e}")
                results[component] = {
                    "status": HealthStatus.UNHEALTHY,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }

        # Calculate overall health
        overall_status = self._calculate_overall_status(results)

        final_result = {
            "overall_status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "environment": "staging",
            "version": "PM-038-staging",
            "components": results,
            "summary": self._generate_health_summary(results),
        }

        # Cache results
        self.cached_results = final_result
        self.last_check_time = current_time

        return final_result

    async def _check_database_health(self) -> Dict[str, Any]:
        """Check PostgreSQL database health"""
        try:
            start_time = time.time()

            # Test database connection and query
            async with get_db_session() as session:
                # Basic connectivity test
                result = await session.execute(text("SELECT 1 as health_check"))
                health_value = result.scalar()

                # Check database stats
                stats_query = text(
                    """
                    SELECT
                        count(*) as total_connections,
                        (SELECT count(*) FROM pg_stat_activity WHERE state = 'active') as active_connections,
                        (SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public') as table_count
                """
                )
                stats_result = await session.execute(stats_query)
                stats = stats_result.fetchone()

                response_time = (time.time() - start_time) * 1000  # Convert to ms

                if health_value == 1:
                    return {
                        "status": HealthStatus.HEALTHY,
                        "response_time_ms": round(response_time, 2),
                        "total_connections": stats.total_connections,
                        "active_connections": stats.active_connections,
                        "table_count": stats.table_count,
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                else:
                    return {
                        "status": HealthStatus.UNHEALTHY,
                        "error": "Database query returned unexpected result",
                        "timestamp": datetime.utcnow().isoformat(),
                    }

        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": f"Database connection failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def _check_redis_health(self) -> Dict[str, Any]:
        """Check Redis cache health"""
        try:
            import redis.asyncio as redis

            config = get_config()
            redis_url = f"redis://:{config.redis_password}@{config.redis_host}:{config.redis_port}"

            start_time = time.time()
            redis_client = redis.from_url(redis_url)

            # Test basic operations
            await redis_client.ping()
            await redis_client.set("health_check", "ok", ex=60)
            result = await redis_client.get("health_check")

            # Get Redis info
            info = await redis_client.info()
            response_time = (time.time() - start_time) * 1000

            await redis_client.close()

            if result == b"ok":
                return {
                    "status": HealthStatus.HEALTHY,
                    "response_time_ms": round(response_time, 2),
                    "connected_clients": info.get("connected_clients", 0),
                    "used_memory_human": info.get("used_memory_human", "unknown"),
                    "redis_version": info.get("redis_version", "unknown"),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            else:
                return {
                    "status": HealthStatus.UNHEALTHY,
                    "error": "Redis operations failed",
                    "timestamp": datetime.utcnow().isoformat(),
                }

        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": f"Redis connection failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def _check_chromadb_health(self) -> Dict[str, Any]:
        """Check ChromaDB vector database health"""
        try:
            config = get_config()
            chroma_url = f"http://{config.chroma_host}:{config.chroma_port}"

            start_time = time.time()

            async with aiohttp.ClientSession() as session:
                # Check heartbeat endpoint
                async with session.get(f"{chroma_url}/api/v1/heartbeat") as response:
                    if response.status == 200:
                        heartbeat_data = await response.json()
                        response_time = (time.time() - start_time) * 1000

                        # Get collection stats if available
                        try:
                            async with session.get(
                                f"{chroma_url}/api/v1/collections"
                            ) as collections_response:
                                if collections_response.status == 200:
                                    collections = await collections_response.json()
                                    collection_count = len(collections)
                                else:
                                    collection_count = "unknown"
                        except Exception:
                            collection_count = "unknown"

                        return {
                            "status": HealthStatus.HEALTHY,
                            "response_time_ms": round(response_time, 2),
                            "heartbeat": heartbeat_data,
                            "collection_count": collection_count,
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    else:
                        return {
                            "status": HealthStatus.UNHEALTHY,
                            "error": f"ChromaDB heartbeat failed with status {response.status}",
                            "timestamp": datetime.utcnow().isoformat(),
                        }

        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": f"ChromaDB connection failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def _check_mcp_health(self) -> Dict[str, Any]:
        """Check MCP integration health with PM-038 enhancements"""
        try:
            start_time = time.time()

            # Initialize MCP resource manager
            manager = MCPResourceManager()
            success = await manager.initialize(enabled=True)

            if not success:
                return {
                    "status": HealthStatus.UNHEALTHY,
                    "error": "MCP initialization failed",
                    "timestamp": datetime.utcnow().isoformat(),
                }

            # Test MCP operations
            test_results = {}

            # Test 1: List resources
            resources = await manager.list_available_resources()
            test_results["resource_count"] = len(resources)

            # Test 2: Enhanced file search (PM-038 feature)
            search_start = time.time()
            search_results = await manager.enhanced_file_search("test health check")
            search_time = (time.time() - search_start) * 1000
            test_results["search_response_time_ms"] = round(search_time, 2)
            test_results["search_results_count"] = len(search_results)

            # Test 3: Connection stats (pool performance)
            connection_stats = await manager.get_connection_stats()
            test_results["connection_stats"] = connection_stats

            # Test 4: Performance validation (should be under 500ms target)
            performance_ok = search_time < 500
            test_results["performance_target_met"] = performance_ok

            await manager.cleanup()

            total_time = (time.time() - start_time) * 1000

            # Determine status based on performance and functionality
            if performance_ok and test_results["resource_count"] > 0:
                status = HealthStatus.HEALTHY
            elif test_results["resource_count"] > 0:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.UNHEALTHY

            return {
                "status": status,
                "total_response_time_ms": round(total_time, 2),
                "tests": test_results,
                "pm038_features": {
                    "connection_pooling": connection_stats.get("using_pool", False),
                    "content_search": len(search_results) > 0,
                    "performance_target": "< 500ms",
                    "actual_performance": f"{search_time:.1f}ms",
                },
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": f"MCP health check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def _check_system_resources(self) -> Dict[str, Any]:
        """Check system resource utilization"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            # Disk usage
            disk = psutil.disk_usage("/")
            disk_percent = disk.percent

            # Determine status based on thresholds
            if cpu_percent > 90 or memory_percent > 90 or disk_percent > 90:
                status = HealthStatus.UNHEALTHY
            elif cpu_percent > 75 or memory_percent > 75 or disk_percent > 80:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.HEALTHY

            return {
                "status": status,
                "cpu_percent": round(cpu_percent, 1),
                "memory_percent": round(memory_percent, 1),
                "disk_percent": round(disk_percent, 1),
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            return {
                "status": HealthStatus.UNKNOWN,
                "error": f"System resource check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def _check_api_endpoints(self) -> Dict[str, Any]:
        """Check critical API endpoints"""
        try:
            endpoints_to_check = [
                "/api/v1/intent",
                "/api/v1/files/search",
                "/health/liveness",
                "/health/readiness",
            ]

            start_time = time.time()
            endpoint_results = {}

            async with aiohttp.ClientSession() as session:
                for endpoint in endpoints_to_check:
                    try:
                        url = f"http://localhost:8001{endpoint}"
                        endpoint_start = time.time()

                        # Use appropriate method for each endpoint
                        if endpoint == "/api/v1/intent":
                            # POST endpoint - test with minimal payload
                            payload = {"message": "health check", "session_id": "health"}
                            async with session.post(url, json=payload) as response:
                                endpoint_time = (time.time() - endpoint_start) * 1000
                                endpoint_results[endpoint] = {
                                    "status_code": response.status,
                                    "response_time_ms": round(endpoint_time, 2),
                                    "healthy": 200 <= response.status < 400,
                                }
                        else:
                            # GET endpoints
                            async with session.get(url) as response:
                                endpoint_time = (time.time() - endpoint_start) * 1000
                                endpoint_results[endpoint] = {
                                    "status_code": response.status,
                                    "response_time_ms": round(endpoint_time, 2),
                                    "healthy": 200 <= response.status < 400,
                                }

                    except Exception as e:
                        endpoint_results[endpoint] = {
                            "status_code": 0,
                            "response_time_ms": 0,
                            "healthy": False,
                            "error": str(e),
                        }

            total_time = (time.time() - start_time) * 1000
            healthy_endpoints = sum(
                1 for result in endpoint_results.values() if result.get("healthy", False)
            )
            total_endpoints = len(endpoints_to_check)

            # Determine overall status
            if healthy_endpoints == total_endpoints:
                status = HealthStatus.HEALTHY
            elif healthy_endpoints > 0:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.UNHEALTHY

            return {
                "status": status,
                "total_response_time_ms": round(total_time, 2),
                "healthy_endpoints": f"{healthy_endpoints}/{total_endpoints}",
                "endpoints": endpoint_results,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": f"API endpoint check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def _check_external_services(self) -> Dict[str, Any]:
        """Check external service dependencies"""
        try:
            services = {
                "anthropic": "https://api.anthropic.com/v1/messages",
                "openai": "https://api.openai.com/v1/models",
                "github": "https://api.github.com/rate_limit",
            }

            service_results = {}

            async with aiohttp.ClientSession() as session:
                for service_name, url in services.items():
                    try:
                        start_time = time.time()
                        async with session.get(
                            url, timeout=aiohttp.ClientTimeout(total=10)
                        ) as response:
                            response_time = (time.time() - start_time) * 1000
                            service_results[service_name] = {
                                "status_code": response.status,
                                "response_time_ms": round(response_time, 2),
                                "reachable": True,
                            }
                    except Exception as e:
                        service_results[service_name] = {
                            "status_code": 0,
                            "response_time_ms": 0,
                            "reachable": False,
                            "error": str(e),
                        }

            # Determine status
            reachable_services = sum(
                1 for result in service_results.values() if result.get("reachable", False)
            )
            total_services = len(services)

            if reachable_services == total_services:
                status = HealthStatus.HEALTHY
            elif reachable_services > 0:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.UNHEALTHY

            return {
                "status": status,
                "reachable_services": f"{reachable_services}/{total_services}",
                "services": service_results,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY,
                "error": f"External service check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
            }

    def _calculate_overall_status(self, component_results: Dict[str, Any]) -> str:
        """Calculate overall health status from component results"""
        statuses = [
            result.get("status", HealthStatus.UNKNOWN) for result in component_results.values()
        ]

        if all(status == HealthStatus.HEALTHY for status in statuses):
            return HealthStatus.HEALTHY
        elif any(status == HealthStatus.UNHEALTHY for status in statuses):
            return HealthStatus.UNHEALTHY
        elif any(status == HealthStatus.DEGRADED for status in statuses):
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.UNKNOWN

    def _generate_health_summary(self, component_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of health check results"""
        total_components = len(component_results)
        healthy_components = sum(
            1
            for result in component_results.values()
            if result.get("status") == HealthStatus.HEALTHY
        )
        degraded_components = sum(
            1
            for result in component_results.values()
            if result.get("status") == HealthStatus.DEGRADED
        )
        unhealthy_components = sum(
            1
            for result in component_results.values()
            if result.get("status") == HealthStatus.UNHEALTHY
        )

        return {
            "total_components": total_components,
            "healthy_components": healthy_components,
            "degraded_components": degraded_components,
            "unhealthy_components": unhealthy_components,
            "health_percentage": (
                round((healthy_components / total_components) * 100, 1)
                if total_components > 0
                else 0
            ),
        }


# Initialize health checker
health_checker = StagingHealthChecker()


@staging_health_router.get("/")
async def basic_health():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": "staging",
    }


@staging_health_router.get("/liveness")
async def liveness_probe():
    """Kubernetes-style liveness probe"""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}


@staging_health_router.get("/readiness")
async def readiness_probe():
    """Kubernetes-style readiness probe"""
    try:
        # Quick database connectivity check
        async with get_db_session() as session:
            await session.execute(text("SELECT 1"))

        return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Not ready: {str(e)}"
        )


@staging_health_router.get("/comprehensive")
async def comprehensive_health():
    """Comprehensive health check for all components"""
    try:
        health_result = await health_checker.get_comprehensive_health()

        # Return appropriate HTTP status based on overall health
        if health_result["overall_status"] == HealthStatus.HEALTHY:
            return health_result
        elif health_result["overall_status"] == HealthStatus.DEGRADED:
            # Still return 200 but indicate degraded performance
            return health_result
        else:
            # Return 503 for unhealthy status
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=health_result
            )

    except Exception as e:
        logger.error(f"Comprehensive health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}",
        )


@staging_health_router.get("/mcp")
async def mcp_health():
    """Dedicated MCP health check (PM-038 feature)"""
    try:
        mcp_result = await health_checker._check_mcp_health()

        if mcp_result["status"] == HealthStatus.HEALTHY:
            return mcp_result
        elif mcp_result["status"] == HealthStatus.DEGRADED:
            return mcp_result
        else:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=mcp_result)

    except Exception as e:
        logger.error(f"MCP health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"MCP health check failed: {str(e)}",
        )


@staging_health_router.get("/metrics")
async def health_metrics():
    """Prometheus-compatible health metrics"""
    try:
        health_result = await health_checker.get_comprehensive_health()

        # Convert to Prometheus format
        metrics = []

        # Overall health metric
        overall_healthy = 1 if health_result["overall_status"] == HealthStatus.HEALTHY else 0
        metrics.append(f'piper_health_overall{{environment="staging"}} {overall_healthy}')

        # Component health metrics
        for component, result in health_result["components"].items():
            component_healthy = 1 if result.get("status") == HealthStatus.HEALTHY else 0
            metrics.append(
                f'piper_health_component{{component="{component}",environment="staging"}} {component_healthy}'
            )

            # Response time metrics if available
            if "response_time_ms" in result:
                response_time = result["response_time_ms"]
                metrics.append(
                    f'piper_health_response_time_ms{{component="{component}",environment="staging"}} {response_time}'
                )

        # System resource metrics
        if "system_resources" in health_result["components"]:
            sys_res = health_result["components"]["system_resources"]
            if "cpu_percent" in sys_res:
                metrics.append(
                    f'piper_system_cpu_percent{{environment="staging"}} {sys_res["cpu_percent"]}'
                )
            if "memory_percent" in sys_res:
                metrics.append(
                    f'piper_system_memory_percent{{environment="staging"}} {sys_res["memory_percent"]}'
                )
            if "disk_percent" in sys_res:
                metrics.append(
                    f'piper_system_disk_percent{{environment="staging"}} {sys_res["disk_percent"]}'
                )

        return "\n".join(metrics) + "\n"

    except Exception as e:
        logger.error(f"Health metrics generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Metrics generation failed: {str(e)}",
        )
