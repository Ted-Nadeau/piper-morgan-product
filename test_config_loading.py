"""Test config-based plugin loading"""

from services.plugins import get_plugin_registry, reset_plugin_registry

# Test 1: Default behavior (with config that has all plugins enabled)
print("Test 1: Config loading (all plugins enabled)")
reset_plugin_registry()
registry = get_plugin_registry()

results = registry.load_enabled_plugins()
print(f"Loaded {len(results)} plugin(s): {list(results.keys())}")
print(f"Success: {sum(1 for s in results.values() if s)}/{len(results)}")

assert len(results) == 4, f"Expected 4 plugins, got {len(results)}"
assert all(results.values()), f"Some plugins failed to load: {results}"
print("✅ Test 1 passed\n")

# Test 2: Check config reading
print("Test 2: Config reading")
reset_plugin_registry()
registry = get_plugin_registry()

enabled = registry.get_enabled_plugins()
print(f"Enabled plugins: {enabled}")
assert len(enabled) == 4, f"Expected 4 enabled plugins, got {len(enabled)}"
print("✅ Test 2 passed\n")

# Test 3: Verify loaded plugins are functional
print("Test 3: Plugin functionality")
reset_plugin_registry()
registry = get_plugin_registry()
registry.load_enabled_plugins()

loaded_plugins = registry.list_plugins()
print(f"Loaded {len(loaded_plugins)} plugin(s):")
for name in sorted(loaded_plugins):
    plugin = registry.get_plugin(name)
    metadata = plugin.get_metadata()
    print(f"  - {name}: v{metadata.version} - {metadata.capabilities}")

assert len(loaded_plugins) == 4, f"Expected 4 loaded plugins, got {len(loaded_plugins)}"
print("✅ Test 3 passed\n")

print("✅ All config integration tests passed!")
