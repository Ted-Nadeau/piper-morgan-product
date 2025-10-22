"""
System Health Checker for Piper Morgan

Checks health of database, API keys, and performance metrics.
Provides actionable recommendations for issues.

Issue #218 CORE-USERS-ONBOARD Phase 1B
"""

import asyncio
import sys
from datetime import datetime
from typing import Any, Dict

# Add parent directory to path for imports
sys.path.insert(0, ".")


class StatusChecker:
    """Check system health and provide diagnostics"""

    async def check_database(self) -> Dict[str, Any]:
        """Check database connectivity and health"""
        try:
            from sqlalchemy import text

            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                # Check basic connectivity
                await session.execute(text("SELECT 1"))

                # Count users
                user_count_result = await session.execute(text("SELECT COUNT(*) FROM users"))
                user_count = user_count_result.scalar_one()

                # Get database size (optional, might not work on all setups)
                try:
                    size_result = await session.execute(
                        text("SELECT pg_database_size(current_database())")
                    )
                    db_size_bytes = size_result.scalar_one()
                    db_size_mb = db_size_bytes / (1024 * 1024)
                    size_info = f"{db_size_mb:.1f} MB"
                except Exception:
                    size_info = "unknown"

            return {
                "status": "✓",
                "message": "PostgreSQL connected",
                "details": f"{user_count} users registered, database size: {size_info}",
            }
        except Exception as e:
            return {
                "status": "✗",
                "message": f"Database error: {str(e)[:100]}",
                "details": None,
            }

    async def check_api_keys(self) -> Dict[str, Any]:
        """Check API key validity for all providers"""
        try:
            from sqlalchemy import text

            from services.database.session_factory import AsyncSessionFactory
            from services.security.user_api_key_service import UserAPIKeyService

            async with AsyncSessionFactory.session_scope() as session:
                # Get first user (for alpha, might just be one)
                user_result = await session.execute(text("SELECT id, username FROM users LIMIT 1"))
                user = user_result.first()

                if not user:
                    return {
                        "status": "⚠",
                        "message": "No users found. Run setup wizard first.",
                        "details": {},
                    }

                user_id = user[0]
                service = UserAPIKeyService()

                # Check each provider
                results = {}
                for provider in ["openai", "anthropic", "github"]:
                    try:
                        # Retrieve key
                        key = await service.retrieve_user_key(session, user_id, provider)

                        if not key:
                            results[provider] = {"status": "○", "message": "Not configured"}
                            continue

                        # Validate (only for OpenAI/Anthropic, skip GitHub)
                        if provider in ["openai", "anthropic"]:
                            is_valid = await service.validate_user_key(session, user_id, provider)

                            if is_valid:
                                results[provider] = {"status": "✓", "message": "Valid"}
                            else:
                                results[provider] = {
                                    "status": "✗",
                                    "message": "Invalid or expired",
                                }
                        else:
                            # GitHub token (don't validate, expensive)
                            results[provider] = {
                                "status": "✓",
                                "message": "Configured (not validated)",
                            }

                    except Exception as e:
                        results[provider] = {
                            "status": "✗",
                            "message": f"Error: {str(e)[:50]}",
                        }

            return results

        except Exception as e:
            return {
                "status": "✗",
                "message": f"Error checking API keys: {e}",
                "details": {},
            }

    async def check_performance(self) -> Dict[str, Any]:
        """Check basic performance metrics"""
        try:
            from sqlalchemy import text

            from services.database.session_factory import AsyncSessionFactory

            start = datetime.now()

            # Quick database query
            async with AsyncSessionFactory.session_scope() as session:
                await session.execute(text("SELECT 1"))

            end = datetime.now()
            response_time_ms = (end - start).total_seconds() * 1000

            if response_time_ms < 100:
                status = "✓"
                details = "Good"
            elif response_time_ms < 500:
                status = "⚠"
                details = "Acceptable"
            else:
                status = "✗"
                details = "Slow"

            return {
                "status": status,
                "message": f"Response time: {response_time_ms:.1f}ms",
                "details": details,
            }
        except Exception as e:
            return {
                "status": "✗",
                "message": f"Performance check failed: {e}",
                "details": None,
            }


async def run_status_check():
    """Main status check entry point"""

    print("\n" + "=" * 50)
    print("Piper Morgan System Status")
    print("=" * 50)
    print()

    checker = StatusChecker()

    # Database
    print("Database:")
    db_status = await checker.check_database()
    print(f"  {db_status['status']} {db_status['message']}")
    if db_status["details"]:
        print(f"     {db_status['details']}")

    # API Keys
    print("\nAPI Keys:")
    key_status = await checker.check_api_keys()

    if isinstance(key_status, dict) and "status" in key_status:
        # Error case
        print(f"  {key_status['status']} {key_status['message']}")
    else:
        # Provider results
        for provider, status in key_status.items():
            print(f"  {status['status']} {provider}: {status['message']}")

    # Performance
    print("\nPerformance:")
    perf_status = await checker.check_performance()
    print(f"  {perf_status['status']} {perf_status['message']}")
    if perf_status["details"]:
        print(f"     {perf_status['details']}")

    # Recommendations
    print("\nRecommendations:")

    recommendations = []

    if db_status["status"] == "✗":
        recommendations.append("  • Fix database connectivity (see error above)")
        recommendations.append("  • Try: docker-compose up -d db")

    if isinstance(key_status, dict):
        if "status" in key_status:
            # Error case
            if key_status["status"] == "⚠":
                recommendations.append(
                    "  • Configure at least one API provider (run: python main.py setup)"
                )
        else:
            # Check if any valid keys
            valid_keys = [p for p, s in key_status.items() if s["status"] in ["✓", "○"]]
            if not valid_keys:
                recommendations.append(
                    "  • Configure at least one API provider (run: python main.py setup)"
                )

    if perf_status["status"] in ["⚠", "✗"]:
        recommendations.append("  • System performance is slow - check database load")
        recommendations.append("  • Try: docker-compose restart")

    if not recommendations:
        recommendations.append("  ✓ All systems operational!")

    for rec in recommendations:
        print(rec)

    print()


if __name__ == "__main__":
    # Allow running directly
    asyncio.run(run_status_check())
