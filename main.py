#!/usr/bin/env python3
"""
Piper Morgan - Main Entry Point

This is the proper way to start Piper Morgan.
It initializes services via ServiceContainer and starts the web server.
"""

import argparse
import asyncio
import logging
import os
import sys
import webbrowser

# Parse arguments early to set logging level
parser = argparse.ArgumentParser(description="Piper Morgan - AI Assistant")
parser.add_argument(
    "--verbose", "-v", action="store_true", help="Show detailed startup information"
)
parser.add_argument(
    "--no-browser", action="store_true", help="Don't auto-launch browser on startup"
)
parser.add_argument(
    "command",
    nargs="?",
    help="Command to run (setup, status, preferences, migrate-user, keys)",
)

# Parse known args to handle both flags and commands
args, unknown = parser.parse_known_args()

# Setup logging based on verbosity (Issue #254 CORE-UX-QUIET)
if args.verbose:
    # Verbose mode - show all details
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
else:
    # Quiet mode (default) - minimal output
    logging.basicConfig(level=logging.WARNING, format="%(message)s")

logger = logging.getLogger(__name__)


def should_open_browser() -> bool:
    """Check if browser should be opened (Issue #256 CORE-UX-BROWSER)"""
    # Don't open if explicitly disabled
    if args.no_browser:
        return False

    # Don't open if no display (CI/CD, SSH)
    if not os.environ.get("DISPLAY") and sys.platform != "darwin":
        return False

    # Don't open for commands (setup, status, etc.)
    if args.command:
        return False

    return True


async def open_browser_delayed():
    """Open browser after a short delay to let server start"""
    await asyncio.sleep(2)  # Wait for server to be ready
    try:
        webbrowser.open("http://localhost:8001")
        if args.verbose:
            logger.info("Browser opened to http://localhost:8001")
        else:
            print("   🌐 Browser opened")
    except Exception as e:
        if args.verbose:
            logger.warning(f"Failed to open browser: {e}")
        # In quiet mode, don't show browser errors (non-critical)


async def main():
    """Main entry point."""
    try:
        # Human-readable startup messages (Issue #254 CORE-UX-QUIET)
        if args.verbose:
            logger.info("Starting Piper Morgan...")
        else:
            print("🚀 Starting Piper Morgan...")

        # Initialize service container
        from services.container import ServiceContainer

        container = ServiceContainer()

        if args.verbose:
            logger.info("Initializing services...")
        else:
            print("   ⏳ Initializing services...")

        await container.initialize()

        if args.verbose:
            logger.info(f"Services initialized: {container.list_services()}")
        else:
            services = container.list_services()
            print(f"   ✓ Services initialized ({len(services)}/{len(services)})")

        # Start web server
        import uvicorn

        if args.verbose:
            logger.info("Starting web server on http://127.0.0.1:8001")
        else:
            # G50: Clear Server Startup Message with all necessary URLs
            print("\n" + "=" * 60)
            print("✅ Piper Morgan is running!")
            print("=" * 60)
            print("\n🌐 Web Interface:     http://localhost:8001")
            print("🔧 API Documentation: http://localhost:8001/docs")
            print("📊 Health Check:      http://localhost:8001/health")
            print("\nPress Ctrl+C to stop the server")
            print("=" * 60 + "\n")

        # Auto-launch browser if appropriate (Issue #256 CORE-UX-BROWSER)
        if should_open_browser():
            asyncio.create_task(open_browser_delayed())
            if not args.verbose:
                print("   ⏳ Opening browser...")

        config = uvicorn.Config(
            "web.app:app",
            host="127.0.0.1",
            port=8001,
            reload=False,  # Disable reload (incompatible with initialized services)
            log_level="warning" if not args.verbose else "info",  # Quiet uvicorn in quiet mode
        )
        server = uvicorn.Server(config)
        await server.serve()

    except KeyboardInterrupt:
        if args.verbose:
            logger.info("Shutting down gracefully...")
        else:
            print("\n👋 Shutting down gracefully...")
        container = ServiceContainer()
        container.shutdown()
    except Exception as e:
        if args.verbose:
            logger.error(f"Startup failed: {e}", exc_info=True)
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Check for CLI commands (Issue #218 CORE-USERS-ONBOARD)
    if args.command:
        command = args.command

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

        elif command == "preferences":
            # Run preference questionnaire (Issue #267 CORE-PREF-QUEST)
            from scripts.preferences_questionnaire import main as run_preferences

            success = asyncio.run(run_preferences())
            sys.exit(0 if success else 1)

        elif command == "keys":
            # Lightweight key management CLI (keychain-first)
            # Usage:
            #   python main.py keys add <provider>
            #   python main.py keys list
            #   python main.py keys validate [provider]
            from getpass import getpass

            from services.config.llm_config_service import LLMConfigService
            from services.infrastructure.keychain_service import KeychainService

            subargs = unknown  # remaining argv after first parse

            def print_keys_help():
                print("Usage:")
                print("  python main.py keys add <provider>")
                print("  python main.py keys list")
                print("  python main.py keys validate [provider]")
                print()
                print("Providers: openai, anthropic, gemini, perplexity")

            if not subargs:
                print_keys_help()
                sys.exit(1)

            action = subargs[0]
            keychain = KeychainService()
            llm_config = LLMConfigService()

            if action == "add":
                if len(subargs) < 2:
                    print("Error: provider required\n")
                    print_keys_help()
                    sys.exit(1)
                provider = subargs[1].lower()
                secret = getpass(f"Enter {provider} API key: ")
                if not secret:
                    print("No key entered. Aborting.")
                    sys.exit(1)
                # Store in OS keychain (global scope)
                try:
                    keychain.store_api_key(provider, secret)
                    print(f"✓ Stored {provider} key in OS keychain")
                except Exception as e:
                    print(f"❌ Failed to store key: {e}")
                    sys.exit(1)
                # Optional validation
                try:
                    valid = asyncio.run(llm_config.validate_api_key(provider, secret))
                    if valid:
                        print(f"✓ {provider} key validated successfully")
                    else:
                        print(
                            f"⚠ Validation failed for {provider}. Key saved; re-check provider/limits."
                        )
                except Exception as e:
                    print(f"⚠ Validation error: {e}")
                sys.exit(0)

            elif action == "list":
                configured = llm_config.get_configured_providers()
                if not configured:
                    print("No providers configured.")
                else:
                    print("Configured providers:")
                    for p in configured:
                        print(f"  - {p}")
                sys.exit(0)

            elif action == "validate":
                # Validate one or all configured providers
                if len(subargs) >= 2:
                    provider = subargs[1].lower()
                    try:
                        result = asyncio.run(llm_config.validate_provider(provider))
                        if result.is_valid:
                            print(f"✓ {provider}: valid")
                            sys.exit(0)
                        else:
                            print(f"❌ {provider}: {result.error_message}")
                            sys.exit(2)
                    except Exception as e:
                        print(f"❌ Validation error for {provider}: {e}")
                        sys.exit(2)
                else:
                    try:
                        results = asyncio.run(llm_config.validate_all_providers())
                        if not results:
                            print("No providers configured.")
                            sys.exit(1)
                        exit_code = 0
                        for provider, res in results.items():
                            if res.is_valid:
                                print(f"✓ {provider}: valid")
                            else:
                                print(f"❌ {provider}: {res.error_message}")
                                exit_code = 2
                        sys.exit(exit_code)
                    except Exception as e:
                        print(f"❌ Validation error: {e}")
                        sys.exit(2)
            else:
                print_keys_help()
                sys.exit(1)

        else:
            print(f"Unknown command: {command}")
            print()
            print("Available commands:")
            print("  python main.py setup        - Interactive setup wizard")
            print("  python main.py status       - Check system health")
            print("  python main.py preferences  - Configure user preferences")
            print("  python main.py keys         - Manage API keys (keychain)")
            print("  python main.py migrate-user - Migrate alpha user to production")
            print("  python main.py [--verbose]  - Start Piper Morgan")
            print()
            print("Options:")
            print("  --verbose, -v               - Show detailed startup information")
            print("  --no-browser                - Don't auto-launch browser")
            sys.exit(1)

    # Normal startup (no command specified)
    asyncio.run(main())
