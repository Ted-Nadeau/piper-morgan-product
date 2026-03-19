"""
Workflow entry points for the workflow dispatcher.

ADR-059: Each function here is an entry point registered in the
workflow dispatcher. Adding a new workflow means:
1. Write an async entry point function here
2. Register it in register_default_workflows()

No switch statements. No modifying intent_service.py.
"""

from typing import Any, Dict, Optional

import structlog

from services.intent_service.workflow_dispatcher import WorkflowEntry, register_workflow

logger = structlog.get_logger(__name__)


async def start_meeting_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Start the meeting slot-filling workflow.

    Extracted from intent_service.py soft offer acceptance (line 454-489).
    Uses the slot_filling_adapter to gather meeting details.
    """
    from services.personality.formality import DEFAULT_WARMTH
    from services.slot_filling.slot_template import MEETING_TEMPLATE

    ctx = context or {}
    trigger_message = ctx.get("trigger_message", "")
    active_lens = ctx.get("active_lens")
    formality_baseline = ctx.get("formality_baseline", DEFAULT_WARMTH)
    slot_filling_adapter = ctx.get("slot_filling_adapter")

    if slot_filling_adapter is None:
        logger.error("meeting_workflow_missing_slot_filling_adapter")
        return None

    # Import here to avoid circular dependency
    from services.intent_service.soft_invocation import WorkflowOfferService

    workflow_offer_service = WorkflowOfferService()

    slot_response = await slot_filling_adapter.manager.start_filling(
        user_id=user_id,
        session_id=session_id,
        template=MEETING_TEMPLATE,
        initial_message=trigger_message,
        active_lens=active_lens,
        formality_baseline=formality_baseline,
    )

    acceptance_msg = workflow_offer_service.format_acceptance(
        "meeting", formality_baseline=formality_baseline
    )
    combined_msg = f"{acceptance_msg}\n\n{slot_response.message}"

    # Return the data the caller needs to build IntentProcessingResult
    return {
        "message": combined_msg,
        "intent_data": {
            "category": "soft_offer_accepted",
            "action": "meeting",
            "context": {
                "slot_filling_active": True,
                "filled_slots": slot_response.filled_slots,
                "template_name": slot_response.template_name,
                "active_lens": active_lens,
            },
        },
    }


def register_default_workflows() -> None:
    """
    Register all default workflow entry points.

    Called during application startup. To add a new workflow:
    1. Write an entry point function above
    2. Add a register_workflow() call here
    """
    register_workflow(
        "meeting",
        WorkflowEntry(
            entry_point=start_meeting_workflow,
            description="Meeting scheduling via slot-filling",
            requires_context=["trigger_message"],
        ),
    )

    logger.info(
        "default_workflows_registered",
        count=1,
        types=["meeting"],
    )
