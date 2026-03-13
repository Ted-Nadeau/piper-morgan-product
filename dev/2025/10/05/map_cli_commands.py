"""Map all CLI commands and their intent usage - GREAT-4B Phase 0"""

from pathlib import Path


def map_cli_commands():
    """Map all CLI commands and their intent usage."""

    commands = {"using_intent": [], "bypassing_intent": []}

    # Check if CLI commands directory exists
    cli_dir = Path("cli/commands")
    if not cli_dir.exists():
        print(f"CLI commands directory not found at {cli_dir}")
        # Try alternative location
        cli_dir = Path("cli")
        if not cli_dir.exists():
            print("No CLI directory found")
            return commands

    # Find all Python files in CLI directory
    cli_files = list(cli_dir.glob("**/*.py"))

    for file in cli_files:
        if file.name == "__init__.py":
            continue

        content = file.read_text()

        # Check for intent/Intent imports or usage
        uses_intent = (
            "intent" in content.lower()
            or "CanonicalHandlers" in content
            or "IntentService" in content
            or "IntentClassifier" in content
            or "classify" in content
        )

        command_info = {
            "file": str(file),
            "name": file.stem,
            "uses_intent": uses_intent,
        }

        if uses_intent:
            commands["using_intent"].append(command_info)
        else:
            commands["bypassing_intent"].append(command_info)

    return commands


if __name__ == "__main__":
    commands = map_cli_commands()

    print("\nCLI COMMANDS BASELINE")
    print("=" * 80)
    print(f"Using Intent: {len(commands['using_intent'])}")
    print(f"Bypassing:    {len(commands['bypassing_intent'])}")
    print(f"Total:        {len(commands['using_intent']) + len(commands['bypassing_intent'])}")

    if commands["using_intent"]:
        print("\nUSING INTENT:")
        for c in sorted(commands["using_intent"], key=lambda x: x["name"]):
            print(f"  {c['name']:30} ({c['file']})")

    if commands["bypassing_intent"]:
        print("\nBYPASSING COMMANDS:")
        for c in sorted(commands["bypassing_intent"], key=lambda x: x["name"]):
            print(f"  {c['name']:30} ({c['file']})")

    # Calculate percentage
    total = len(commands["using_intent"]) + len(commands["bypassing_intent"])
    if total > 0:
        pct = (len(commands["using_intent"]) / total) * 100
        print(f"\nIntent Coverage: {pct:.1f}%")
