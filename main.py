#!/usr/bin/env python3
"""
Piper Morgan Main Application

Configuration validation integrated at startup to prevent runtime failures
from misconfiguration. Use --skip-validation for development bypass.
"""

import argparse
import logging
import sys
from typing import Optional

# Import the ConfigValidator
try:
    from services.config_validator import ConfigValidator
except ImportError:
    print("❌ ERROR: ConfigValidator not found. Run Phase 1 Code agent first.")
    sys.exit(1)

logger = logging.getLogger(__name__)


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Piper Morgan - Intelligent PM Assistant")
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip configuration validation (development mode)",
    )
    parser.add_argument(
        "--config",
        default="config/PIPER.user.md",
        help="Path to configuration file (default: config/PIPER.user.md)",
    )
    return parser.parse_args()


def validate_configuration(config_path: str, skip_validation: bool = False) -> bool:
    """
    Validate configuration before starting services.

    Args:
        config_path: Path to configuration file
        skip_validation: If True, skip validation (development mode)

    Returns:
        True if validation passed or was skipped, False if critical failures
    """
    if skip_validation:
        print("⚠️  DEVELOPMENT MODE: Configuration validation skipped")
        print("   Use this mode only for development. Production requires validation.")
        return True

    print("🔍 Validating configuration...")

    try:
        # Create validator instance
        validator = ConfigValidator(config_path)

        # Run validation for all services
        validation_results = validator.validate_all_services()

        # Generate and display report
        report = validator.format_validation_report(validation_results)
        print(report)

        # Check if startup should be allowed
        startup_allowed = validator.is_startup_allowed(validation_results)

        if startup_allowed:
            print("✅ Configuration validation PASSED - Starting services...")
            return True
        else:
            print("❌ Configuration validation FAILED - Cannot start services")
            print("💡 Fix the configuration issues above and try again")
            print("🛠️  Or use --skip-validation for development mode")
            return False

    except Exception as e:
        print(f"❌ Configuration validation ERROR: {e}")
        print("💡 Check your configuration file format and try again")
        print("🛠️  Or use --skip-validation for development mode")
        return False


def start_services():
    """Start all application services"""
    print("🚀 Starting Piper Morgan services...")

    # Import and start services here
    # This will be where the actual application services start
    try:
        # Placeholder for service startup
        print("   📡 Starting web server...")
        print("   🔗 Starting integration routers...")
        print("   🧠 Starting spatial intelligence systems...")
        print("   ✅ All services started successfully")

        # Keep application running
        print("🎯 Piper Morgan is ready!")
        print("   Press Ctrl+C to stop")

        # In real implementation, this would start the actual services
        # For now, just wait for interrupt
        import time

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down Piper Morgan...")
        print("   Stopping services...")
        print("   ✅ Shutdown complete")
    except Exception as e:
        print(f"❌ Service startup failed: {e}")
        sys.exit(1)


def main():
    """Main application entry point"""
    setup_logging()
    args = parse_arguments()

    print("🤖 Piper Morgan - Intelligent PM Assistant")
    print("=" * 50)

    # Validate configuration first
    if not validate_configuration(args.config, args.skip_validation):
        print("🚫 Application startup aborted due to configuration issues")
        sys.exit(1)

    # Start services if validation passed
    start_services()


if __name__ == "__main__":
    main()
