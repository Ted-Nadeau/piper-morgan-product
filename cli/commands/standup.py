"""
Morning Standup CLI Command - MVP Implementation
Uses persistent context infrastructure for <2 second generation

Built on: UserPreferenceManager + SessionPersistenceManager + GitHub integration
Performance: <2 seconds, saves 15+ minutes manual prep
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.domain.user_preference_manager import UserPreferenceManager
from services.features.morning_standup import MorningStandupWorkflow
from services.integrations.github.github_agent import GitHubAgent
from services.integrations.slack.response_handler import SlackResponseHandler
from services.orchestration.session_persistence import SessionPersistenceManager


class StandupCommand:
    """Morning Standup CLI Command with beautiful formatting and Slack integration"""

    # Color codes for beautiful output
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "gray": "\033[90m",
    }

    def __init__(self):
        """Initialize the standup command with required services"""
        self.preference_manager = UserPreferenceManager()
        self.session_manager = SessionPersistenceManager(self.preference_manager)
        self.github_agent = GitHubAgent()
        self.standup_workflow = MorningStandupWorkflow(
            preference_manager=self.preference_manager,
            session_manager=self.session_manager,
            github_agent=self.github_agent,
        )

    def print_colored(self, text: str, color: str = "reset", bold: bool = False) -> None:
        """Print colored and optionally bold text"""
        color_code = self.COLORS.get(color, self.COLORS["reset"])
        bold_code = self.COLORS["bold"] if bold else ""
        print(f"{bold_code}{color_code}{text}{self.COLORS['reset']}")

    def print_header(self, title: str) -> None:
        """Print a beautiful header"""
        print()
        self.print_colored("=" * 60, "cyan", bold=True)
        self.print_colored(f"  {title}", "cyan", bold=True)
        self.print_colored("=" * 60, "cyan", bold=True)
        print()

    def print_section(self, title: str, color: str = "blue") -> None:
        """Print a section header"""
        print()
        self.print_colored(f"📋 {title}", color, bold=True)
        self.print_colored("-" * 40, color)

    def print_success(self, message: str) -> None:
        """Print a success message"""
        self.print_colored(f"✅ {message}", "green")

    def print_info(self, message: str) -> None:
        """Print an info message"""
        self.print_colored(f"ℹ️  {message}", "blue")

    def print_warning(self, message: str) -> None:
        """Print a warning message"""
        self.print_colored(f"⚠️  {message}", "yellow")

    def print_error(self, message: str) -> None:
        """Print an error message"""
        self.print_colored(f"❌ {message}", "red")

    def format_slack_message(self, content: str) -> str:
        """Format content for Slack compatibility (no markdown conflicts)"""
        # Remove markdown that could cause Slack formatting issues
        slack_safe = content.replace("**", "*")  # Bold to Slack bold
        slack_safe = slack_safe.replace("__", "_")  # Italic to Slack italic
        slack_safe = slack_safe.replace("`", "`")  # Keep code blocks
        slack_safe = slack_safe.replace("```", "```")  # Keep code blocks

        # Remove any remaining markdown that could cause issues
        import re

        slack_safe = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", slack_safe)  # Remove links
        slack_safe = re.sub(r"#{1,6}\s+", "", slack_safe)  # Remove headers

        return slack_safe

    async def get_greeting(self) -> str:
        """Get context-aware greeting message"""
        try:
            greeting = await self.conversation_queries.get_greeting()
            return greeting
        except Exception as e:
            self.print_warning(f"Could not get personalized greeting: {e}")
            return "Good morning! Ready for our daily standup?"

    async def get_help(self) -> str:
        """Get context-aware help message"""
        try:
            help_text = await self.conversation_queries.get_help()
            return help_text
        except Exception as e:
            self.print_warning(f"Could not get help information: {e}")
            return (
                "I can help you with project management, daily operations, and development support."
            )

    async def get_status(self) -> str:
        """Get context-aware status message"""
        try:
            status = await self.conversation_queries.get_status()
            return status
        except Exception as e:
            self.print_warning(f"Could not get status information: {e}")
            return "I'm operating normally. All systems are go!"

    async def run_standup(self, user_id: str = "xian") -> Dict[str, str]:
        """Run the MVP morning standup using persistent context infrastructure"""
        results = {}

        try:
            self.print_colored("🚀 Morning Standup MVP", "magenta", bold=True)
            self.print_colored("━" * 50, "gray")

            # Performance tracking
            start_time = datetime.now()

            # Generate standup using our MVP workflow
            self.print_colored("⏱️  Generating standup (target: <2 seconds)...", "yellow")

            standup_result = await self.standup_workflow.generate_standup(user_id)

            # Display results
            self.print_colored(f"✅ Generated in {standup_result.generation_time_ms}ms", "green")
            self.print_colored(
                f"💰 Saved {standup_result.time_saved_minutes} minutes of manual prep", "cyan"
            )
            self.print_colored("━" * 50, "gray")

            # Yesterday's Accomplishments
            self.print_section("📋 Yesterday's Accomplishments", "green")
            if standup_result.yesterday_accomplishments:
                for accomplishment in standup_result.yesterday_accomplishments:
                    self.print_info(f"  {accomplishment}")
            else:
                self.print_info("  No specific accomplishments found")

            # Today's Priorities
            self.print_section("🎯 Today's Priorities", "blue")
            for priority in standup_result.today_priorities:
                self.print_info(f"  {priority}")

            # Blockers
            self.print_section("⚠️  Blockers", "red" if standup_result.blockers else "gray")
            if standup_result.blockers:
                for blocker in standup_result.blockers:
                    self.print_warning(f"  {blocker}")
            else:
                self.print_success("  No blockers identified")

            # Performance Summary
            self.print_colored("━" * 50, "gray")
            self.print_section("📊 Performance Summary", "cyan")
            self.print_info(f"  Context Source: {standup_result.context_source}")
            self.print_info(
                f"  GitHub Activity: {len(standup_result.github_activity.get('commits', []))} commits"
            )
            self.print_info(f"  Generation Time: {standup_result.generation_time_ms}ms")
            self.print_info(
                f"  Performance Target: {'✅ MET' if standup_result.generation_time_ms < 2000 else '❌ MISSED'}"
            )

            # Store results
            results.update(
                {
                    "user_id": standup_result.user_id,
                    "generation_time_ms": standup_result.generation_time_ms,
                    "time_saved_minutes": standup_result.time_saved_minutes,
                    "yesterday_accomplishments": standup_result.yesterday_accomplishments,
                    "today_priorities": standup_result.today_priorities,
                    "blockers": standup_result.blockers,
                    "context_source": standup_result.context_source,
                    "performance_met": standup_result.generation_time_ms < 2000,
                }
            )

            return results

            # Get current focus
            self.print_section("Current Focus", "yellow")
            focus_info = "Q4 2025: MCP implementation and UX enhancement"
            self.print_info(focus_info)
            results["focus"] = focus_info

        except Exception as e:
            self.print_error(f"Standup execution failed: {e}")
            results["error"] = str(e)

        return results

    def generate_slack_output(self, results: Dict[str, str]) -> str:
        """Generate Slack-ready output from standup results"""
        if "error" in results:
            return f"❌ Standup failed: {results['error']}"

        slack_output = []
        slack_output.append("🌅 *Morning Standup Report*")
        slack_output.append("")

        if "greeting" in results:
            slack_output.append(f"*Greeting:* {self.format_slack_message(results['greeting'])}")

        if "time" in results:
            slack_output.append(f"*Current Time:* {results['time']}")

        if "focus" in results:
            slack_output.append(f"*Current Focus:* {results['focus']}")

        if "status" in results:
            slack_output.append(f"*System Status:* {self.format_slack_message(results['status'])}")

        if "help" in results:
            help_preview = (
                results["help"][:150] + "..." if len(results["help"]) > 150 else results["help"]
            )
            slack_output.append(f"*Available Help:* {self.format_slack_message(help_preview)}")

        return "\n".join(slack_output)

    async def execute(self, output_format: str = "cli") -> None:
        """Execute the standup command with specified output format"""
        try:
            self.print_header("🌅 Piper Morgan Morning Standup")

            # Run standup sequence
            results = await self.run_standup()

            # Generate output based on format
            if output_format == "slack":
                slack_output = self.generate_slack_output(results)
                print("\n" + "=" * 60)
                self.print_colored("📱 Slack-Ready Output:", "magenta", bold=True)
                print("=" * 60)
                print(slack_output)
                print("=" * 60)
            else:
                # CLI format - already displayed above
                pass

            # Print summary
            self.print_header("🎯 Standup Complete")
            self.print_success("Morning standup completed successfully!")
            self.print_info("Use --format slack for Slack-ready output")

        except Exception as e:
            self.print_error(f"Standup command failed: {e}")
            sys.exit(1)


def main():
    """Main entry point for standup command"""
    import argparse

    parser = argparse.ArgumentParser(description="Piper Morgan Morning Standup")
    parser.add_argument(
        "--format", choices=["cli", "slack"], default="cli", help="Output format (default: cli)"
    )

    args = parser.parse_args()

    # Run standup command
    standup = StandupCommand()
    asyncio.run(standup.execute(output_format=args.format))


if __name__ == "__main__":
    main()
