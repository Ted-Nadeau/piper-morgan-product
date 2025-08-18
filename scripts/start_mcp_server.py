#!/usr/bin/env python3
"""
Piper Morgan MCP Server Startup Script

Starts the dual-mode MCP server on localhost:8765 exposing:
- SpatialIntentClassifier as MCP resource
- QueryRouter federated search as MCP tool

Usage:
    python scripts/start_mcp_server.py [--port 8765] [--host localhost]
"""

import argparse
import asyncio
import logging
import signal
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.mcp.server.server_core import PiperMCPServer

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Start Piper Morgan MCP Server")
    parser.add_argument("--port", "-p", type=int, default=8765, help="Server port (default: 8765)")
    parser.add_argument(
        "--host", type=str, default="localhost", help="Server host (default: localhost)"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser.parse_args()


async def main():
    """Main startup function"""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print("🚀 Starting Piper Morgan MCP Server")
    print(f"   Host: {args.host}")
    print(f"   Port: {args.port}")
    print(f"   Mode: Dual (Consumer + Server)")
    print("=" * 50)

    # Initialize server
    server = PiperMCPServer(port=args.port, host=args.host)

    # Set up signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        print(f"\n📴 Received signal {signum}, shutting down gracefully...")
        asyncio.create_task(server.stop_server())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Display startup status
        health = await server.health_check()
        print(f"🏥 Initial health: {health['status']}")

        # Start server (this will run indefinitely)
        print("✅ MCP Server ready for connections")
        print("📋 Available services:")
        print("   - Resource: piper://intent/spatial_classifier (Spatial Intent Classifier)")
        print("   - Tool: federated_search (Multi-dimensional query routing)")
        print()
        print("🔌 Connect using MCP client to localhost:8765")
        print("📧 Server logs will appear below:")
        print("-" * 50)

        await server.start_server()

    except KeyboardInterrupt:
        print("\n📴 Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Server error: {e}")
        print(f"❌ Server failed: {e}")
    finally:
        await server.stop_server()
        print("📴 Server stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n📴 Startup cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        sys.exit(1)
