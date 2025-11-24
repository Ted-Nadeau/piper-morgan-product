"""
Demo endpoint for enhanced conversation context tracking.

Shows how to integrate the EnhancedContextTracker with FastAPI endpoints
for improved conversation continuity and context awareness.

Issue #248 CORE-UX-CONVERSATION-CONTEXT
"""

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from services.conversation.context_tracker import (
    enhanced_context_tracker,
    enrich_message_context,
    get_conversation_context_summary,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/conversation", tags=["conversation"])


class MessageRequest(BaseModel):
    """Request model for message context enrichment"""

    message: str
    conversation_id: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None


class MessageResponse(BaseModel):
    """Response model for enriched message"""

    original_message: str
    enriched_message: str
    confidence_score: float
    resolved_references_count: int
    active_entities_count: int
    conversation_flow_length: int
    processing_time_ms: float


@router.post("/enrich", response_model=MessageResponse)
async def enrich_message(request: MessageRequest):
    """Enrich a message with conversation context"""

    try:
        enrichment = await enrich_message_context(
            request.message, request.conversation_id, request.session_id, request.user_id
        )

        processing_time_ms = enrichment.enrichment_metadata.get("processing_time", 0.0) * 1000

        return MessageResponse(
            original_message=enrichment.original_message,
            enriched_message=enrichment.enriched_message,
            confidence_score=enrichment.confidence_score,
            resolved_references_count=len(enrichment.resolved_references),
            active_entities_count=len(enrichment.active_entities),
            conversation_flow_length=len(enrichment.conversation_state.conversation_flow),
            processing_time_ms=processing_time_ms,
        )

    except Exception as e:
        logger.error(f"Failed to enrich message: {e}")
        raise HTTPException(status_code=500, detail="Message enrichment failed")


@router.get("/summary/{conversation_id}")
async def get_conversation_summary(conversation_id: str):
    """Get summary of conversation context"""

    try:
        summary = await get_conversation_context_summary(conversation_id)
        return summary

    except Exception as e:
        logger.error(f"Failed to get conversation summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to get conversation summary")


@router.get("/stats")
async def get_context_tracking_stats():
    """Get performance statistics for context tracking"""

    try:
        stats = enhanced_context_tracker.get_performance_stats()
        return {
            "context_tracking_stats": stats,
            "status": "healthy" if stats["success_rate"] > 0.8 else "degraded",
        }

    except Exception as e:
        logger.error(f"Failed to get context tracking stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get stats")


@router.post("/demo/conversation")
async def demo_conversation():
    """Demo conversation showing context tracking improvements"""

    conversation_id = "demo-conversation"
    demo_messages = [
        "Hello! I'm working on issue #123 in the auth project.",
        "The bug is causing login failures for users.",
        "Can you help me debug it?",
        "I think the problem is in the authentication service.",
        "Let's check the logs for that service.",
    ]

    results = []

    for i, message in enumerate(demo_messages):
        try:
            enrichment = await enrich_message_context(message, conversation_id)

            results.append(
                {
                    "turn": i + 1,
                    "original": message,
                    "enriched": enrichment.enriched_message,
                    "confidence": enrichment.confidence_score,
                    "resolved_references": [
                        {
                            "original": ref.original_text,
                            "resolved": ref.resolved_entity,
                            "type": ref.entity_type,
                            "confidence": ref.confidence,
                        }
                        for ref in enrichment.resolved_references
                    ],
                    "active_entities": [
                        {
                            "id": entity.entity_id,
                            "type": entity.entity_type,
                            "mentions": entity.mention_count,
                            "aliases": list(entity.aliases),
                        }
                        for entity in enrichment.active_entities
                    ],
                    "conversation_flow": enrichment.conversation_state.conversation_flow[
                        -3:
                    ],  # Last 3
                }
            )

        except Exception as e:
            logger.error(f"Demo conversation failed at turn {i+1}: {e}")
            results.append({"turn": i + 1, "original": message, "error": str(e)})

    # Get final conversation summary
    try:
        final_summary = await get_conversation_context_summary(conversation_id)
    except Exception as e:
        final_summary = {"error": str(e)}

    return {
        "demo_conversation": results,
        "final_summary": final_summary,
        "improvements_demonstrated": [
            "Reference resolution (it, that, the bug)",
            "Entity tracking across turns (issue #123, auth project)",
            "Conversation flow classification",
            "Context persistence and retrieval",
            "Confidence scoring for enrichment quality",
        ],
    }


@router.get("/demo/entity-patterns")
async def demo_entity_patterns():
    """Show entity patterns used for extraction"""

    return {
        "entity_patterns": enhanced_context_tracker.entity_patterns,
        "examples": {
            "issue": [
                "issue #123 → extracts: 123",
                "the bug → extracts: reference to previously mentioned issue",
                "that ticket → extracts: reference to previously mentioned issue",
            ],
            "project": [
                "project auth → extracts: auth",
                "the project → extracts: reference to previously mentioned project",
                "repo myapp → extracts: myapp",
            ],
            "file": [
                "file auth.py → extracts: auth.py",
                "the script → extracts: reference to previously mentioned file",
                "config.json → extracts: config.json",
            ],
            "user": [
                "@john → extracts: john",
                "user alice → extracts: alice",
                "I, me, my → extracts: current user references",
            ],
        },
    }


@router.post("/demo/reference-resolution")
async def demo_reference_resolution():
    """Demo reference resolution capabilities"""

    conversation_id = "demo-references"

    # Setup conversation with entities
    setup_messages = [
        "I'm working on issue #456 in the payment service.",
        "The database connection is failing in config.py.",
        "User @alice reported this yesterday.",
    ]

    # Messages with references to resolve
    reference_messages = [
        "Can you check the issue?",  # Should resolve to issue #456
        "The bug is in that file.",  # Should resolve to config.py
        "She mentioned it was urgent.",  # Should resolve to @alice
        "Let's fix it in the service.",  # Should resolve to payment service
    ]

    # Setup phase
    for msg in setup_messages:
        await enrich_message_context(msg, conversation_id)

    # Resolution phase
    resolution_results = []
    for msg in reference_messages:
        enrichment = await enrich_message_context(msg, conversation_id)

        resolution_results.append(
            {
                "original": msg,
                "enriched": enrichment.enriched_message,
                "references_resolved": [
                    {
                        "original_text": ref.original_text,
                        "resolved_to": ref.resolved_entity,
                        "entity_type": ref.entity_type,
                        "confidence": ref.confidence,
                        "replacement": ref.replacement_text,
                    }
                    for ref in enrichment.resolved_references
                ],
                "confidence_score": enrichment.confidence_score,
            }
        )

    return {
        "setup_phase": setup_messages,
        "resolution_results": resolution_results,
        "explanation": "This demo shows how pronouns and references like 'the issue', 'that file', 'she', 'the service' are resolved to specific entities mentioned earlier in the conversation.",
    }
