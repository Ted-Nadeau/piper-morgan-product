"""
Automated scanner for intent classification bypasses.
Run this in CI to detect regressions.
"""

import re
from pathlib import Path


def scan_for_bypasses():
    """Scan codebase for potential intent bypasses."""

    bypasses = []

    # Scan web routes
    web_files = list(Path("web").glob("**/*.py")) if Path("web").exists() else []

    for file in web_files:
        content = file.read_text()

        # Find routes that don't mention intent
        routes = re.findall(r'@(?:app|router)\.(get|post|put|delete)\(["\']([^"\']+)', content)

        for method, path in routes:
            # Exempt certain paths
            if path in ["/health", "/metrics", "/docs", "/api/v1/intent", "/openapi.json"]:
                continue

            # Check if this route uses intent
            route_start = content.find(f"@app.{method}")
            if route_start == -1:
                route_start = content.find(f"@router.{method}")

            if route_start != -1:
                next_500 = content[route_start : route_start + 500]

                if "intent" not in next_500.lower():
                    bypasses.append(
                        {
                            "type": "web_route",
                            "file": str(file),
                            "method": method.upper(),
                            "path": path,
                        }
                    )

    # Scan CLI commands
    cli_dir = Path("cli/commands")
    if cli_dir.exists():
        for file in cli_dir.glob("*.py"):
            if file.name == "__init__.py":
                continue

            content = file.read_text()
            if "intent" not in content.lower():
                bypasses.append({"type": "cli_command", "file": str(file), "command": file.stem})

    # Scan integration handlers
    integrations_dir = Path("services/integrations")
    if integrations_dir.exists():
        for integration_dir in integrations_dir.iterdir():
            if not integration_dir.is_dir():
                continue

            # Look for handler files
            handler_files = [
                f
                for f in integration_dir.glob("**/*.py")
                if "handler" in f.name.lower() or "event" in f.name.lower()
            ]

            for file in handler_files:
                content = file.read_text()
                if "intent" not in content.lower() and "canonical" not in content.lower():
                    bypasses.append(
                        {
                            "type": "integration_handler",
                            "file": str(file),
                            "integration": integration_dir.name,
                            "handler": file.stem,
                        }
                    )

    return bypasses


if __name__ == "__main__":
    bypasses = scan_for_bypasses()

    if bypasses:
        print(f"⚠️  FOUND {len(bypasses)} POTENTIAL BYPASSES:")
        for b in bypasses:
            if b["type"] == "web_route":
                print(f"  {b['method']:6} {b['path']:40} ({b['file']})")
            elif b["type"] == "cli_command":
                print(f"  CLI    {b['command']:40} ({b['file']})")
            elif b["type"] == "integration_handler":
                print(f"  {b['integration'].upper():6} {b['handler']:40} ({b['file']})")
        exit(1)
    else:
        print("✅ NO BYPASSES DETECTED")
        exit(0)
