"""
Learning API Routes - Pattern Management and Analytics

CORE-LEARN-A (Issue #221)
Exposes learning system for pattern management, feedback, and analytics.

Features:
- Pattern retrieval and management
- Feedback submission and tracking
- Cross-feature knowledge sharing
- Learning analytics and statistics

Pattern-034: Error Handling Standards (REST-compliant)
Privacy: Metadata-only learning, no PII
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from services.learning.cross_feature_knowledge import CrossFeatureKnowledgeService
from services.learning.query_learning_loop import PatternType, QueryLearningLoop
from web.utils.error_responses import internal_error, not_found_error, validation_error

# Create router with prefix and tags for OpenAPI
router = APIRouter(prefix="/api/v1/learning", tags=["learning"])


# ============================================================================
# Service Initialization (Singleton Pattern)
# ============================================================================

_learning_loop: Optional[QueryLearningLoop] = None
_cross_feature_service: Optional[CrossFeatureKnowledgeService] = None


def get_learning_loop_instance() -> QueryLearningLoop:
    """Get or create singleton QueryLearningLoop instance."""
    global _learning_loop
    if _learning_loop is None:
        _learning_loop = QueryLearningLoop()
    return _learning_loop


def get_cross_feature_service_instance() -> Optional[CrossFeatureKnowledgeService]:
    """
    Get or create singleton CrossFeatureKnowledgeService instance.

    Note: Requires database session and knowledge graph infrastructure.
    Returns None if dependencies are not available (will be wired in Phase 2).
    """
    global _cross_feature_service
    # For now, return None - will be properly wired in orchestration integration
    # This requires database session and knowledge graph repository setup
    return None


# ============================================================================
# Request/Response Models
# ============================================================================


class PatternRequest(BaseModel):
    """Request body for learning a new pattern."""

    pattern_type: str = Field(..., description="Pattern type (query_pattern, response_pattern, workflow_pattern, integration_pattern, user_preference_pattern)")
    source_feature: str = Field(..., description="Feature that generated the pattern")
    pattern_data: Dict[str, Any] = Field(..., description="The actual pattern data")
    initial_confidence: float = Field(0.5, ge=0.0, le=1.0, description="Starting confidence level")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the pattern")


class FeedbackRequest(BaseModel):
    """Request body for submitting pattern feedback."""

    pattern_id: str = Field(..., description="Pattern identifier")
    success: bool = Field(..., description="Was pattern application successful?")
    feedback: Optional[str] = Field(None, description="Optional feedback text")
    context: Dict[str, Any] = Field(default_factory=dict, description="Feedback context")


class ApplyPatternRequest(BaseModel):
    """Request body for applying a pattern."""

    pattern_id: str = Field(..., description="Pattern identifier")
    context: Dict[str, Any] = Field(..., description="Application context")


class KnowledgeSharingRequest(BaseModel):
    """Request body for sharing knowledge across features."""

    source_feature: str = Field(..., description="Source feature name")
    target_feature: str = Field(..., description="Target feature name")
    knowledge_type: str = Field(..., description="Type of knowledge to share")
    content: Dict[str, Any] = Field(..., description="Knowledge content")


# ============================================================================
# Pattern Management Endpoints
# ============================================================================


@router.get("/patterns")
async def get_patterns(
    source_feature: Optional[str] = Query(None, description="Filter by source feature"),
    min_confidence: float = Query(0.5, ge=0.0, le=1.0, description="Minimum confidence"),
) -> Dict[str, Any]:
    """
    Get learned patterns with optional filtering.

    Query params:
    - source_feature: Filter by specific source feature
    - min_confidence: Minimum confidence threshold (0.0-1.0)

    Returns:
    - patterns: List of patterns matching criteria
    - count: Number of patterns returned
    """
    try:
        learning_loop = get_learning_loop_instance()

        if source_feature:
            # Get patterns for specific feature
            patterns_obj = await learning_loop.get_patterns_for_feature(
                source_feature=source_feature, min_confidence=min_confidence
            )
            # Convert LearnedPattern objects to dicts
            patterns = [
                {
                    "pattern_id": p.pattern_id,
                    "pattern_type": p.pattern_type.value,
                    "source_feature": p.source_feature,
                    "confidence": p.confidence,
                    "usage_count": p.usage_count,
                    "success_rate": p.success_rate,
                }
                for p in patterns_obj
            ]
        else:
            # Get all patterns from all features
            patterns = []

        return {"patterns": patterns, "count": len(patterns)}

    except Exception as e:
        return internal_error(
            message=f"Failed to retrieve patterns: {str(e)}",
            error_id="PATTERN_RETRIEVAL_ERROR",
        )


@router.post("/patterns")
async def learn_pattern(pattern: PatternRequest) -> Dict[str, Any]:
    """
    Learn a new pattern from query and context.

    Body:
    - pattern_type: Type of pattern (query_pattern, response_pattern, workflow_pattern, etc.)
    - source_feature: Feature that generated the pattern
    - pattern_data: The actual pattern data
    - initial_confidence: Starting confidence level (0.0-1.0)
    - metadata: Additional metadata about the pattern

    Returns:
    - status: Operation status
    - pattern_id: Generated pattern identifier
    """
    try:
        learning_loop = get_learning_loop_instance()

        # Convert string pattern_type to PatternType enum
        try:
            pattern_type_enum = PatternType(pattern.pattern_type)
        except ValueError:
            return validation_error(
                message=f"Invalid pattern_type: {pattern.pattern_type}. Must be one of: query_pattern, response_pattern, workflow_pattern, integration_pattern, user_preference_pattern",
                error_id="INVALID_PATTERN_TYPE",
            )

        pattern_id = await learning_loop.learn_pattern(
            pattern_type=pattern_type_enum,
            source_feature=pattern.source_feature,
            pattern_data=pattern.pattern_data,
            initial_confidence=pattern.initial_confidence,
            metadata=pattern.metadata,
        )

        return {
            "status": "pattern_learned",
            "pattern_id": pattern_id,
            "confidence": pattern.initial_confidence,
        }

    except ValueError as e:
        return validation_error(message=str(e), error_id="INVALID_PATTERN_DATA")
    except Exception as e:
        return internal_error(
            message=f"Failed to learn pattern: {str(e)}",
            error_id="PATTERN_LEARNING_ERROR",
        )


@router.post("/patterns/apply")
async def apply_pattern(request: ApplyPatternRequest) -> Dict[str, Any]:
    """
    Apply a learned pattern to new context.

    Body:
    - pattern_id: Pattern identifier
    - context: Contextual information for pattern application

    Returns:
    - status: Application status
    - result: Pattern application result
    - confidence: Application confidence score
    """
    try:
        learning_loop = get_learning_loop_instance()

        # apply_pattern returns Tuple[bool, Dict[str, Any], float]
        success, result_data, confidence = await learning_loop.apply_pattern(
            pattern_id=request.pattern_id, context=request.context
        )

        if not success:
            return not_found_error(
                message=f"Pattern not found or failed to apply: {request.pattern_id}",
                error_id="PATTERN_NOT_FOUND",
            )

        return {
            "status": "pattern_applied",
            "pattern_id": request.pattern_id,
            "result": result_data,
            "confidence": confidence,
        }

    except ValueError as e:
        return validation_error(message=str(e), error_id="INVALID_PATTERN_APPLICATION")
    except Exception as e:
        return internal_error(
            message=f"Failed to apply pattern: {str(e)}",
            error_id="PATTERN_APPLICATION_ERROR",
        )


# ============================================================================
# Feedback Endpoints
# ============================================================================


@router.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest) -> Dict[str, Any]:
    """
    Submit feedback on a pattern application.

    Body:
    - pattern_id: Pattern identifier
    - success: Was pattern application successful?
    - feedback: Optional feedback text
    - context: Additional context

    Returns:
    - status: Feedback recording status
    - pattern_id: Pattern identifier
    """
    try:
        learning_loop = get_learning_loop_instance()

        # Convert success bool to feedback_score float (-1.0 to 1.0)
        feedback_score = 1.0 if feedback.success else -1.0

        recorded = await learning_loop.provide_feedback(
            pattern_id=feedback.pattern_id,
            feedback_score=feedback_score,
            feedback_text=feedback.feedback,
            context=feedback.context,
        )

        if not recorded:
            return not_found_error(
                message=f"Pattern not found: {feedback.pattern_id}",
                error_id="PATTERN_NOT_FOUND",
            )

        return {
            "status": "feedback_recorded",
            "pattern_id": feedback.pattern_id,
            "success": feedback.success,
        }

    except ValueError as e:
        return validation_error(message=str(e), error_id="INVALID_FEEDBACK_DATA")
    except Exception as e:
        return internal_error(
            message=f"Failed to record feedback: {str(e)}",
            error_id="FEEDBACK_RECORDING_ERROR",
        )


# ============================================================================
# Analytics Endpoints
# ============================================================================


@router.get("/analytics")
async def get_analytics() -> Dict[str, Any]:
    """
    Get learning system analytics and statistics.

    Returns:
    - total_patterns: Total learned patterns
    - patterns_by_feature: Breakdown by feature
    - success_rate: Overall pattern success rate
    - avg_confidence: Average pattern confidence
    """
    try:
        learning_loop = get_learning_loop_instance()

        stats = await learning_loop.get_learning_stats()

        return {
            "total_patterns": stats.get("total_patterns", 0),
            "patterns_by_feature": stats.get("feature_distribution", {}),
            "pattern_type_distribution": stats.get("pattern_type_distribution", {}),
            "average_confidence": stats.get("average_confidence", 0.0),
            "total_feedback": stats.get("total_feedback", 0),
            "recent_patterns_24h": stats.get("recent_patterns_24h", 0),
            "recent_feedback_24h": stats.get("recent_feedback_24h", 0),
        }

    except Exception as e:
        return internal_error(
            message=f"Failed to retrieve analytics: {str(e)}",
            error_id="ANALYTICS_RETRIEVAL_ERROR",
        )


# ============================================================================
# Cross-Feature Knowledge Endpoints
# ============================================================================


@router.get("/knowledge/shared")
async def get_shared_knowledge(
    source_feature: Optional[str] = Query(None, description="Filter by source feature"),
    target_feature: Optional[str] = Query(None, description="Filter by target feature"),
) -> Dict[str, Any]:
    """
    Get cross-feature shared knowledge.

    Query params:
    - source_feature: Filter by source feature
    - target_feature: Filter by target feature

    Returns:
    - knowledge: List of shared knowledge items
    - count: Number of items

    Note: Requires orchestration integration (Phase 2)
    """
    cross_feature_service = get_cross_feature_service_instance()

    if cross_feature_service is None:
        return {
            "knowledge": [],
            "count": 0,
            "note": "Cross-feature knowledge service requires database integration (Phase 2)",
        }

    try:
        knowledge = await cross_feature_service.get_shared_knowledge(
            source_feature=source_feature, target_feature=target_feature
        )

        return {"knowledge": knowledge, "count": len(knowledge)}

    except Exception as e:
        return internal_error(
            message=f"Failed to retrieve shared knowledge: {str(e)}",
            error_id="KNOWLEDGE_RETRIEVAL_ERROR",
        )


@router.post("/knowledge/share")
async def share_knowledge(request: KnowledgeSharingRequest) -> Dict[str, Any]:
    """
    Share knowledge between features.

    Body:
    - source_feature: Source feature name
    - target_feature: Target feature name
    - knowledge_type: Type of knowledge
    - content: Knowledge content

    Returns:
    - status: Sharing status
    - knowledge_id: Generated knowledge identifier

    Note: Requires orchestration integration (Phase 2)
    """
    cross_feature_service = get_cross_feature_service_instance()

    if cross_feature_service is None:
        return validation_error(
            message="Cross-feature knowledge service requires database integration (Phase 2)",
            error_id="SERVICE_NOT_AVAILABLE",
        )

    try:
        result = await cross_feature_service.share_knowledge(
            source_feature=request.source_feature,
            target_feature=request.target_feature,
            knowledge_type=request.knowledge_type,
            content=request.content,
        )

        return {
            "status": "knowledge_shared",
            "knowledge_id": result.get("knowledge_id"),
            "confidence": result.get("confidence", 0.0),
        }

    except ValueError as e:
        return validation_error(message=str(e), error_code="INVALID_KNOWLEDGE_DATA")
    except Exception as e:
        return internal_error(
            message=f"Failed to share knowledge: {str(e)}",
            error_id="KNOWLEDGE_SHARING_ERROR",
        )


@router.get("/knowledge/stats")
async def get_knowledge_stats() -> Dict[str, Any]:
    """
    Get cross-feature knowledge sharing statistics.

    Returns:
    - total_shared: Total knowledge items shared
    - by_feature: Breakdown by feature
    - success_rate: Knowledge application success rate

    Note: Requires orchestration integration (Phase 2)
    """
    cross_feature_service = get_cross_feature_service_instance()

    if cross_feature_service is None:
        return {
            "total_shared": 0,
            "by_feature": {},
            "success_rate": 0.0,
            "avg_confidence": 0.0,
            "note": "Cross-feature knowledge service requires database integration (Phase 2)",
        }

    try:
        stats = await cross_feature_service.get_knowledge_sharing_stats()

        return {
            "total_shared": stats.get("total_shared", 0),
            "by_feature": stats.get("by_feature", {}),
            "success_rate": stats.get("success_rate", 0.0),
            "avg_confidence": stats.get("avg_confidence", 0.0),
        }

    except Exception as e:
        return internal_error(
            message=f"Failed to retrieve knowledge stats: {str(e)}",
            error_id="KNOWLEDGE_STATS_ERROR",
        )


# ============================================================================
# Health Check
# ============================================================================


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Learning system health check.

    Returns:
    - status: System status
    - services: Service availability
    """
    try:
        learning_loop = get_learning_loop_instance()
        cross_feature_service = get_cross_feature_service_instance()

        return {
            "status": "healthy",
            "services": {
                "learning_loop": "available" if learning_loop else "unavailable",
                "cross_feature_knowledge": (
                    "available" if cross_feature_service else "pending_phase_2"
                ),
            },
            "note": "Cross-feature knowledge requires database integration (Phase 2)",
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "services": {
                "learning_loop": "unavailable",
                "cross_feature_knowledge": "unavailable",
            },
        }
