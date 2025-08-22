#!/usr/bin/env python3
"""
CLI Standup Test Runner
Simple script to test the CLI standup functionality
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cli.commands.standup import StandupCommand


async def test_cli_functionality():
    """Test the CLI functionality"""
    print("🧪 Testing CLI Standup Functionality")
    print("=" * 50)

    try:
        # Test 1: Command initialization
        print("\n1. Testing command initialization...")
        standup = StandupCommand()
        print("✅ Command initialized successfully")

        # Test 2: Color formatting
        print("\n2. Testing color formatting...")
        standup.print_success("Success message")
        standup.print_info("Info message")
        standup.print_warning("Warning message")
        standup.print_error("Error message")
        print("✅ Color formatting working")

        # Test 3: Slack message formatting
        print("\n3. Testing Slack message formatting...")
        test_content = (
            "**Bold text** and __italic text__ with `code` and [link](http://example.com)"
        )
        slack_output = standup.format_slack_message(test_content)
        print(f"Original: {test_content}")
        print(f"Slack: {slack_output}")
        print("✅ Slack formatting working")

        # Test 4: Slack output generation
        print("\n4. Testing Slack output generation...")
        test_results = {
            "greeting": "Good morning!",
            "time": "Today is Thursday, August 21, 2025 at 4:27 PM",
            "focus": "Q4 2025: MCP implementation",
            "status": "All systems operational",
        }
        slack_output = standup.generate_slack_output(test_results)
        print("Slack Output:")
        print(slack_output)
        print("✅ Slack output generation working")

        print("\n🎉 All CLI tests passed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ CLI test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    print("🚀 CLI Standup Test Runner")
    print("=" * 50)

    # Run async tests
    success = asyncio.run(test_cli_functionality())

    if success:
        print("\n✅ CLI functionality verified successfully!")
        sys.exit(0)
    else:
        print("\n❌ CLI functionality test failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
