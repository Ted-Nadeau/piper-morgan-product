"""
Interactive Debugging Commands for Slack Pipeline

Command-line interface for debugging Slack integration pipeline issues.
Provides interactive debugging session with real-time monitoring capabilities.

This module enables rapid troubleshooting through interactive commands
for pipeline inspection, event replay, and health monitoring.
"""

import asyncio
import json
import sys
from typing import Optional

from services.debugging.slack_inspector import PipelineDebugger, SlackPipelineInspector


async def debug_slack_pipeline():
    """
    Interactive debugging session for Slack pipeline.

    Provides a command-line interface for pipeline inspection, trace analysis,
    event replay, and health monitoring. Essential for troubleshooting
    silent failures and performance issues.
    """
    debugger = PipelineDebugger()
    await debugger.start_debug_session()


def quick_health_check():
    """Quick health check without interactive session"""
    inspector = SlackPipelineInspector()
    health = inspector.get_pipeline_health()

    print(f"🏥 Slack Pipeline Health: {health['health_status'].upper()}")
    print(f"📊 Active Pipelines: {health['active_pipelines']}")
    print(f"🔄 Recent Success Rate: {health['recent_success_rate']:.1%}")
    print(f"⚡ Avg Processing Time: {health['avg_processing_time_ms']:.1f}ms")

    if health["stuck_pipelines"] > 0:
        print(f"⚠️  {health['stuck_pipelines']} stuck pipelines detected!")
        for stuck in health["stuck_pipeline_details"]:
            print(f"   - {stuck['correlation_id']} (running {stuck['duration_minutes']:.1f} min)")

    return health["health_status"] == "healthy"


def quick_trace(correlation_id: str) -> bool:
    """Quick trace of a specific pipeline"""
    inspector = SlackPipelineInspector()
    return inspector.print_pipeline_trace(correlation_id)


def show_active_pipelines():
    """Show summary of active pipelines"""
    inspector = SlackPipelineInspector()
    inspector.print_active_pipelines_summary()


def show_recent_failures(minutes: int = 60):
    """Show recent pipeline failures"""
    inspector = SlackPipelineInspector()
    inspector.print_failure_analysis(minutes)


async def replay_event_from_json(event_json: str, mock_calls: bool = True) -> bool:
    """Replay an event from JSON string"""
    try:
        event_data = json.loads(event_json)
        inspector = SlackPipelineInspector()
        result = await inspector.replay_event(event_data, mock_api_calls=mock_calls)
        return result is not None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Replay failed: {e}")
        return False


def show_pipeline_stats(minutes: int = 60):
    """Show pipeline statistics"""
    inspector = SlackPipelineInspector()
    stats = inspector.calculate_success_rate(minutes)

    print(f"\n📈 Pipeline Statistics ({minutes} minutes):")
    print(f"  Total Pipelines: {stats['total_pipelines']}")
    print(f"  Successful: {stats['successful_pipelines']}")
    print(f"  Failed: {stats['failed_pipelines']}")
    print(f"  Success Rate: {stats['success_rate']:.1%}")
    print(f"  Avg Duration: {stats['avg_duration_ms']:.1f}ms")

    return stats


async def main():
    """
    Main entry point for debugging commands.

    Usage:
        python -m services.debugging.commands                    # Interactive session
        python -m services.debugging.commands health             # Quick health check
        python -m services.debugging.commands trace <id>         # Quick trace
        python -m services.debugging.commands active             # Show active pipelines
        python -m services.debugging.commands failures [min]     # Show failures
        python -m services.debugging.commands stats [min]        # Show statistics
        python -m services.debugging.commands replay <json>      # Replay event
    """

    if len(sys.argv) == 1:
        # No arguments - start interactive session
        await debug_slack_pipeline()
        return

    command = sys.argv[1].lower()

    if command == "health":
        healthy = quick_health_check()
        sys.exit(0 if healthy else 1)

    elif command == "trace":
        if len(sys.argv) < 3:
            print("❌ Usage: python -m services.debugging.commands trace <correlation_id>")
            sys.exit(1)

        correlation_id = sys.argv[2]
        found = quick_trace(correlation_id)
        sys.exit(0 if found else 1)

    elif command == "active":
        show_active_pipelines()
        sys.exit(0)

    elif command == "failures":
        minutes = 60
        if len(sys.argv) > 2:
            try:
                minutes = int(sys.argv[2])
            except ValueError:
                print(f"❌ Invalid minutes value: {sys.argv[2]}")
                sys.exit(1)

        show_recent_failures(minutes)
        sys.exit(0)

    elif command == "stats":
        minutes = 60
        if len(sys.argv) > 2:
            try:
                minutes = int(sys.argv[2])
            except ValueError:
                print(f"❌ Invalid minutes value: {sys.argv[2]}")
                sys.exit(1)

        show_pipeline_stats(minutes)
        sys.exit(0)

    elif command == "replay":
        if len(sys.argv) < 3:
            print("❌ Usage: python -m services.debugging.commands replay '<event_json>'")
            sys.exit(1)

        event_json = " ".join(sys.argv[2:])  # Handle JSON with spaces
        success = await replay_event_from_json(event_json, mock_calls=True)
        sys.exit(0 if success else 1)

    elif command == "help":
        print("🔧 Slack Pipeline Debugging Commands")
        print("=" * 50)
        print("Interactive mode:")
        print("  python -m services.debugging.commands")
        print("")
        print("Quick commands:")
        print("  health                    - Quick health check")
        print("  trace <correlation_id>    - Show pipeline trace")
        print("  active                    - Show active pipelines")
        print("  failures [minutes]        - Show recent failures (default: 60)")
        print("  stats [minutes]           - Show statistics (default: 60)")
        print("  replay '<event_json>'     - Replay event for debugging")
        print("  help                      - Show this help")
        print("")
        print("Examples:")
        print("  python -m services.debugging.commands health")
        print("  python -m services.debugging.commands trace abc123-def456")
        print("  python -m services.debugging.commands failures 120")
        print(
            '  python -m services.debugging.commands replay \'{"type":"app_mention","text":"test"}\''
        )

        sys.exit(0)

    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'help' to see available commands")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
