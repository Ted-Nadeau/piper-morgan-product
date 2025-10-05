"""Map all web routes and their intent usage - GREAT-4B Phase 0"""

import re
from pathlib import Path


def map_web_routes():
    """Map all web routes and their intent usage."""

    routes = {"using_intent": [], "bypassing_intent": [], "unclear": []}

    # Find all route definitions in web directory
    web_files = list(Path("web").glob("**/*.py"))

    for file in web_files:
        content = file.read_text()

        # Find @app.* or @router.* decorators
        route_pattern = r'@(?:app|router)\.(get|post|put|delete|patch)\(["\']([^"\']+)'

        for match in re.finditer(route_pattern, content):
            method = match.group(1)
            path = match.group(2)

            # Check if route code uses intent
            # Look for "intent" in next 2000 chars after decorator
            route_start = match.end()
            next_lines = content[route_start : route_start + 2000]

            # Check for various intent-related patterns
            uses_intent = (
                "intent" in next_lines.lower()
                or "IntentClassifier" in next_lines
                or "classify" in next_lines
                or "canonical" in next_lines.lower()
            )

            route_info = {
                "file": str(file),
                "method": method.upper(),
                "path": path,
                "uses_intent": uses_intent,
            }

            if uses_intent:
                routes["using_intent"].append(route_info)
            else:
                routes["bypassing_intent"].append(route_info)

    return routes


if __name__ == "__main__":
    routes = map_web_routes()

    print("WEB ROUTES BASELINE")
    print("=" * 80)
    print(f"Using Intent: {len(routes['using_intent'])}")
    print(f"Bypassing:    {len(routes['bypassing_intent'])}")
    print(f"Total:        {len(routes['using_intent']) + len(routes['bypassing_intent'])}")

    if routes["using_intent"]:
        print("\nUSING INTENT:")
        for r in sorted(routes["using_intent"], key=lambda x: x["path"]):
            print(f"  {r['method']:6} {r['path']:50} ({r['file']})")

    if routes["bypassing_intent"]:
        print("\nBYPASSING ROUTES:")
        for r in sorted(routes["bypassing_intent"], key=lambda x: x["path"]):
            print(f"  {r['method']:6} {r['path']:50} ({r['file']})")

    # Calculate percentage
    total = len(routes["using_intent"]) + len(routes["bypassing_intent"])
    if total > 0:
        pct = (len(routes["using_intent"]) / total) * 100
        print(f"\nIntent Coverage: {pct:.1f}%")
