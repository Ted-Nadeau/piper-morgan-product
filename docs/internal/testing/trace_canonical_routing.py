"""Trace canonical intent routing - Investigation for Chief Architect"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()
sys.path.insert(0, str(project_root))

from services.intent.intent_service import IntentService
from services.llm.clients import llm_client
from services.orchestration.engine import OrchestrationEngine


async def trace_priority_intent():
    """Trace how PRIORITY intent flows through the system"""

    print("=" * 80)
    print("CANONICAL ROUTING TRACE - PRIORITY Intent")
    print("=" * 80)

    # Initialize service
    orchestration_engine = OrchestrationEngine(llm_client=llm_client)
    service = IntentService(orchestration_engine=orchestration_engine)

    text = "What is my top priority today?"

    print(f"\nInput: '{text}'")
    print(f"\nChecking canonical_handlers.can_handle()...")

    # Call process_intent and capture result
    result = await service.process_intent(text, session_id="trace-test")

    print(f"\n{'=' * 80}")
    print("RESULT ANALYSIS")
    print("=" * 80)
    print(f"Result type: {type(result).__name__}")
    print(f"Success: {result.success}")
    print(f"Message: {result.message[:200] if result.message else 'None'}...")

    if hasattr(result, "error"):
        print(f"Error: {result.error}")
    if hasattr(result, "workflow_id"):
        print(f"Workflow ID: {result.workflow_id}")

    print(f"\n{'=' * 80}")
    print("ANALYSIS")
    print("=" * 80)

    if "No workflow type found" in str(result):
        print("⚠️  'No workflow type found' message detected")
        print("   This suggests intent reached WorkflowFactory")
        print("   Canonical handlers may not have caught it")
    else:
        print("✅ No workflow errors - canonical handler likely processed it")

    return result


async def trace_temporal_intent():
    """Trace how TEMPORAL intent flows through the system"""

    print("\n" + "=" * 80)
    print("CANONICAL ROUTING TRACE - TEMPORAL Intent")
    print("=" * 80)

    orchestration_engine = OrchestrationEngine(llm_client=llm_client)
    service = IntentService(orchestration_engine=orchestration_engine)

    text = "What's on my calendar today?"

    print(f"\nInput: '{text}'")

    result = await service.process_intent(text, session_id="trace-test")

    print(f"\nResult success: {result.success}")
    print(f"Message preview: {result.message[:100] if result.message else 'None'}...")

    return result


async def main():
    """Run all traces"""

    # Trace PRIORITY
    priority_result = await trace_priority_intent()

    # Trace TEMPORAL
    temporal_result = await trace_temporal_intent()

    print("\n" + "=" * 80)
    print("INVESTIGATION SUMMARY")
    print("=" * 80)
    print(f"PRIORITY result success: {priority_result.success}")
    print(f"TEMPORAL result success: {temporal_result.success}")

    if priority_result.success and temporal_result.success:
        print("\n✅ Both intents succeeded")
        print("   Canonical handlers are likely working correctly")
        print("   'No workflow type found' errors may be debug logs only")
    else:
        print("\n❌ One or more intents failed")
        print("   Investigation needed into canonical handler wiring")


if __name__ == "__main__":
    asyncio.run(main())
