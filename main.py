#!/usr/bin/env python3
"""
Piper Morgan - Main Entry Point

This is the proper way to start Piper Morgan.
It initializes services via ServiceContainer and starts the web server.
"""

import asyncio
import logging
import sys

# Setup logging first
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def main():
    """Main entry point."""
    try:
        logger.info("Starting Piper Morgan...")

        # Initialize service container
        from services.container import ServiceContainer

        container = ServiceContainer()
        logger.info("Initializing services...")
        await container.initialize()
        logger.info(f"Services initialized: {container.list_services()}")

        # Start web server
        import uvicorn

        logger.info("Starting web server on http://127.0.0.1:8001")
        config = uvicorn.Config(
            "web.app:app",
            host="127.0.0.1",
            port=8001,
            reload=False,  # Disable reload (incompatible with initialized services)
            log_level="info",
        )
        server = uvicorn.Server(config)
        await server.serve()

    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
        container = ServiceContainer()
        container.shutdown()
    except Exception as e:
        logger.error(f"Startup failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    # Check for CLI commands (Issue #218 CORE-USERS-ONBOARD)
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "setup":
            # Run interactive setup wizard
            from scripts.setup_wizard import run_setup_wizard

            success = asyncio.run(run_setup_wizard())
            sys.exit(0 if success else 1)

        elif command == "status":
            # Run system health check
            from scripts.status_checker import run_status_check

            asyncio.run(run_status_check())
            sys.exit(0)

        else:
            print(f"Unknown command: {command}")
            print()
            print("Available commands:")
            print("  python main.py setup   - Interactive setup wizard")
            print("  python main.py status  - Check system health")
            print("  python main.py         - Start Piper Morgan")
            sys.exit(1)

    # Normal startup (no command specified)
    asyncio.run(main())
