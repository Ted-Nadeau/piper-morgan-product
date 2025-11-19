import os
import sys


def test_module_caching():
    """Check if services module is already in sys.modules"""
    print(f"\n'services' in sys.modules: {'services' in sys.modules}")
    if "services" in sys.modules:
        print(f"  Module: {sys.modules['services']}")
        print(f"  Path: {getattr(sys.modules['services'], '__path__', 'NO __path__')}")

    # Try to access services
    try:
        import services

        print(f"✓ Imported services")
        print(f"  services.__path__: {services.__path__}")
    except Exception as e:
        print(f"✗ Failed to import services: {e}")
        raise

    # Check what's in it
    print(f"  Has 'integrations': {'integrations' in dir(services)}")

    # Try github
    try:
        import services.integrations.github.github_integration_router as router

        print(f"✓ Imported router module")
    except ImportError as e:
        print(f"✗ Failed: {e}")
        # List what's in services.integrations
        try:
            import services.integrations

            print(f"  services.integrations dir: {dir(services.integrations)}")
            print(f"  services.integrations.__path__: {services.integrations.__path__}")
        except:
            pass
        raise
