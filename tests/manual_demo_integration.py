"""Test demo integration is functional"""

from services.plugins import get_plugin_registry, reset_plugin_registry

# Reset and load
reset_plugin_registry()

# Import triggers registration
from services.integrations.demo import DemoPlugin

# Get registry
registry = get_plugin_registry()

# Check demo plugin loaded
plugins = registry.list_plugins()
print(f"Loaded plugins: {plugins}")
assert "demo" in plugins, "Demo plugin should be registered"

# Get plugin
demo = registry.get_plugin("demo")
assert demo is not None, "Should be able to get demo plugin"

# Check metadata
metadata = demo.get_metadata()
print(f"\nDemo Plugin Metadata:")
print(f"  Name: {metadata.name}")
print(f"  Version: {metadata.version}")
print(f"  Description: {metadata.description}")
print(f"  Capabilities: {metadata.capabilities}")

# Check router
router = demo.get_router()
print(f"\nDemo Router:")
print(f"  Prefix: {router.prefix}")
print(f"  Routes: {len(router.routes)}")

# Check status
status = demo.get_status()
print(f"\nDemo Status:")
for key, value in status.items():
    print(f"  {key}: {value}")

print("\n✅ Demo integration test passed!")
