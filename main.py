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
    asyncio.run(main())
