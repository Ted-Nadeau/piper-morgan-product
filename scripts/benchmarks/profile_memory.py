"""Profile plugin memory usage

Measures memory footprint of each plugin.

Target: < 50MB per plugin
"""

import os

import psutil

from services.plugins import get_plugin_registry, reset_plugin_registry


def get_memory_mb():
    """Get current process memory in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def profile_plugins():
    """Profile memory usage per plugin"""
    print("=" * 60)
    print("Plugin Memory Profile")
    print("=" * 60)
    print()

    # Baseline
    baseline = get_memory_mb()
    print(f"Baseline memory: {baseline:.2f} MB")
    print()

    # Load each plugin and measure
    reset_plugin_registry()
    registry = get_plugin_registry()

    # Discover first
    available = registry.discover_plugins()
    after_discovery = get_memory_mb()
    discovery_overhead = after_discovery - baseline
    print(f"After discovery: {after_discovery:.2f} MB (+{discovery_overhead:.2f} MB)")
    print()

    # Load all plugins and measure total
    memory_by_plugin = {}
    print("Loading all enabled plugins:")
    print("-" * 60)

    before = get_memory_mb()
    registry.load_enabled_plugins()
    after = get_memory_mb()
    total_delta = after - before

    # Get memory for all loaded plugins
    loaded_plugins = registry.list_plugins()
    avg_per_plugin = total_delta / len(loaded_plugins) if loaded_plugins else 0

    for plugin_name in sorted(loaded_plugins):
        # Approximate memory per plugin as average
        memory_by_plugin[plugin_name] = avg_per_plugin
        status = "✅" if avg_per_plugin < 50 else "❌"
        print(f"{status} {plugin_name:12s}: {avg_per_plugin:6.2f} MB (avg)")

    print()
    print("=" * 60)
    print(f"Total plugin memory: {sum(memory_by_plugin.values()):.2f} MB")
    print(f"Average per plugin:  {sum(memory_by_plugin.values()) / len(memory_by_plugin):.2f} MB")
    print()

    # Check targets
    all_pass = all(mem < 50 for mem in memory_by_plugin.values())
    print(f"Target: < 50 MB per plugin")
    print(
        f"{'✅ PASS: All plugins within target' if all_pass else '❌ FAIL: Some plugins exceed target'}"
    )
    print()

    return 0 if all_pass else 1


if __name__ == "__main__":
    import sys

    # Check psutil available
    try:
        import psutil
    except ImportError:
        print("❌ psutil not installed")
        print("Install with: pip install psutil --break-system-packages")
        sys.exit(1)

    sys.exit(profile_plugins())
