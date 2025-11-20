"""Test plugin discovery mechanism"""

from services.plugins import get_plugin_registry, reset_plugin_registry

# Reset to clean state
reset_plugin_registry()

# Get registry
registry = get_plugin_registry()

# Test discovery
available = registry.discover_plugins()

print(f"Discovered {len(available)} plugin(s):")
for name, module_path in sorted(available.items()):
    print(f"  - {name}: {module_path}")

# Expected output:
# Discovered 4 plugin(s):
#   - calendar: services.integrations.calendar.calendar_plugin
#   - github: services.integrations.github.github_plugin
#   - notion: services.integrations.notion.notion_plugin
#   - slack: services.integrations.slack.slack_plugin

assert len(available) == 4, f"Expected 4 plugins, found {len(available)}"
assert "slack" in available, "Slack plugin not found"
assert "github" in available, "GitHub plugin not found"
assert "notion" in available, "Notion plugin not found"
assert "calendar" in available, "Calendar plugin not found"

print("\n✅ Discovery test passed!")
