"""
Slack Pipeline Observability Monitor

Comprehensive correlation tracking and monitoring infrastructure for Slack integration.
Eliminates silent failures through complete request tracing and context preservation.

This module provides bulletproof observability for the entire Slack pipeline,
ensuring no request can fail silently without proper error reporting and tracking.
"""

import asyncio
import contextvars
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

# Context variables for request tracking across async boundaries
correlation_id: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id")
slack_event_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "slack_event_id", default=None
)
processing_stage: contextvars.ContextVar[str] = contextvars.ContextVar(
    "processing_stage", default="unknown"
)

# Global registry of active pipelines for debugging
ACTIVE_PIPELINES: Dict[str, "SlackPipelineMetrics"] = {}

logger = logging.getLogger(__name__)


class ProcessingStage(Enum):
    """Pipeline processing stages for comprehensive tracking"""

    WEBHOOK_RECEIVED = "webhook_received"
    CONTEXT_EXTRACTED = "context_extracted"
    SPATIAL_MAPPED = "spatial_mapped"
    INTENT_CLASSIFIED = "intent_classified"
    WORKFLOW_CREATED = "workflow_created"
    WORKFLOW_EXECUTED = "workflow_executed"
    RESPONSE_GENERATED = "response_generated"
    SLACK_API_CALLED = "slack_api_called"
    RESPONSE_SENT = "response_sent"
    PIPELINE_COMPLETED = "pipeline_completed"
    PIPELINE_FAILED = "pipeline_failed"


@dataclass
class StageMetrics:
    """Metrics for a single pipeline stage"""

    stage: ProcessingStage
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_ms: Optional[float] = None
    success: Optional[bool] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def complete_success(self, metadata: Optional[Dict[str, Any]] = None):
        """Mark stage as successfully completed"""
        self.completed_at = datetime.now(timezone.utc)
        self.duration_ms = (self.completed_at - self.started_at).total_seconds() * 1000
        self.success = True
        if metadata:
            self.metadata.update(metadata)

    def complete_failure(self, error: str, metadata: Optional[Dict[str, Any]] = None):
        """Mark stage as failed with error details"""
        self.completed_at = datetime.now(timezone.utc)
        self.duration_ms = (self.completed_at - self.started_at).total_seconds() * 1000
        self.success = False
        self.error = error
        if metadata:
            self.metadata.update(metadata)


@dataclass
class SlackPipelineMetrics:
    """Comprehensive metrics tracking for a single Slack pipeline execution"""

    correlation_id: str
    slack_event_id: Optional[str]
    started_at: datetime
    webhook_data: Dict[str, Any] = field(default_factory=dict)
    stages: Dict[ProcessingStage, StageMetrics] = field(default_factory=dict)
    completed_at: Optional[datetime] = None
    total_duration_ms: Optional[float] = None
    final_status: Optional[str] = None
    error_details: Optional[str] = None

    # Additional properties for test interface compatibility
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    processing_stages: List[Any] = field(default_factory=list)

    def start_pipeline(self):
        """Start pipeline timing"""
        self.start_time = datetime.now(timezone.utc)
        logger.info(f"Pipeline {self.correlation_id} started")

    def end_pipeline(self):
        """End pipeline timing"""
        self.end_time = datetime.now(timezone.utc)
        if self.start_time:
            duration = (self.end_time - self.start_time).total_seconds()
            logger.info(f"Pipeline {self.correlation_id} ended after {duration:.2f}s")

    def record_stage(self, stage_name: str, stage_data: Dict[str, Any]):
        """Record a processing stage with data"""
        stage_record = {
            "name": stage_name,
            "data": stage_data,
            "correlation_id": self.correlation_id,
            "timestamp": datetime.now(timezone.utc),
        }
        self.processing_stages.append(stage_record)
        logger.debug(f"Recorded stage {stage_name} for pipeline {self.correlation_id}")

    def start_stage(
        self, stage: ProcessingStage, metadata: Optional[Dict[str, Any]] = None
    ) -> StageMetrics:
        """Start tracking a new pipeline stage"""
        stage_metrics = StageMetrics(
            stage=stage, started_at=datetime.now(timezone.utc), metadata=metadata or {}
        )
        self.stages[stage] = stage_metrics

        # Update context variable for logging
        processing_stage.set(stage.value)

        logger.info(
            f"SLACK_PIPELINE [{self.correlation_id}] Stage {stage.value} started",
            extra={
                "correlation_id": self.correlation_id,
                "slack_event_id": self.slack_event_id,
                "stage": stage.value,
                "metadata": metadata,
            },
        )

        return stage_metrics

    def complete_stage(
        self,
        stage: ProcessingStage,
        success: bool = True,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Complete a pipeline stage with success/failure status"""
        if stage not in self.stages:
            logger.warning(f"Attempting to complete stage {stage.value} that was never started")
            return

        stage_metrics = self.stages[stage]
        if success:
            stage_metrics.complete_success(metadata)
            logger.info(
                f"SLACK_PIPELINE [{self.correlation_id}] Stage {stage.value} completed successfully in {stage_metrics.duration_ms:.2f}ms",
                extra={
                    "correlation_id": self.correlation_id,
                    "slack_event_id": self.slack_event_id,
                    "stage": stage.value,
                    "duration_ms": stage_metrics.duration_ms,
                    "success": True,
                    "metadata": metadata,
                },
            )
        else:
            stage_metrics.complete_failure(error or "Unknown error", metadata)
            logger.error(
                f"SLACK_PIPELINE [{self.correlation_id}] Stage {stage.value} FAILED after {stage_metrics.duration_ms:.2f}ms: {error}",
                extra={
                    "correlation_id": self.correlation_id,
                    "slack_event_id": self.slack_event_id,
                    "stage": stage.value,
                    "duration_ms": stage_metrics.duration_ms,
                    "success": False,
                    "error": error,
                    "metadata": metadata,
                },
            )

    def complete_pipeline(self, success: bool = True, error_details: Optional[str] = None):
        """Complete the entire pipeline with final status"""
        self.completed_at = datetime.now(timezone.utc)
        self.total_duration_ms = (self.completed_at - self.started_at).total_seconds() * 1000
        self.final_status = "success" if success else "failed"
        self.error_details = error_details

        if success:
            logger.info(
                f"SLACK_PIPELINE [{self.correlation_id}] COMPLETED SUCCESSFULLY in {self.total_duration_ms:.2f}ms",
                extra={
                    "correlation_id": self.correlation_id,
                    "slack_event_id": self.slack_event_id,
                    "total_duration_ms": self.total_duration_ms,
                    "stages_completed": len([s for s in self.stages.values() if s.success]),
                    "final_status": "success",
                },
            )
        else:
            logger.error(
                f"SLACK_PIPELINE [{self.correlation_id}] FAILED after {self.total_duration_ms:.2f}ms: {error_details}",
                extra={
                    "correlation_id": self.correlation_id,
                    "slack_event_id": self.slack_event_id,
                    "total_duration_ms": self.total_duration_ms,
                    "error_details": error_details,
                    "final_status": "failed",
                },
            )

        # Remove from active pipelines registry
        ACTIVE_PIPELINES.pop(self.correlation_id, None)

    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive pipeline summary for debugging"""
        return {
            "correlation_id": self.correlation_id,
            "slack_event_id": self.slack_event_id,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "total_duration_ms": self.total_duration_ms,
            "final_status": self.final_status,
            "error_details": self.error_details,
            "stages": {
                stage.value: {
                    "started_at": metrics.started_at.isoformat(),
                    "completed_at": (
                        metrics.completed_at.isoformat() if metrics.completed_at else None
                    ),
                    "duration_ms": metrics.duration_ms,
                    "success": metrics.success,
                    "error": metrics.error,
                    "metadata": metrics.metadata,
                }
                for stage, metrics in self.stages.items()
            },
        }


class SlackPipelineMonitor:
    """Singleton monitor for managing Slack pipeline observability"""

    _instance: Optional["SlackPipelineMonitor"] = None

    def __new__(cls) -> "SlackPipelineMonitor":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            logger.info("SlackPipelineMonitor initialized")

    def start_pipeline(
        self, webhook_data: Dict[str, Any], event_id: Optional[str] = None
    ) -> SlackPipelineMetrics:
        """Start tracking a new Slack pipeline execution"""
        # Generate correlation ID
        corr_id = str(uuid.uuid4())

        # Set context variables
        correlation_id.set(corr_id)
        slack_event_id.set(event_id)
        processing_stage.set(ProcessingStage.WEBHOOK_RECEIVED.value)

        # Create pipeline metrics
        pipeline_metrics = SlackPipelineMetrics(
            correlation_id=corr_id,
            slack_event_id=event_id,
            started_at=datetime.now(timezone.utc),
            webhook_data=webhook_data,
        )

        # Register in active pipelines
        ACTIVE_PIPELINES[corr_id] = pipeline_metrics

        logger.info(
            f"SLACK_PIPELINE [{corr_id}] STARTED",
            extra={
                "correlation_id": corr_id,
                "slack_event_id": event_id,
                "webhook_event_type": webhook_data.get("type", "unknown"),
                "active_pipelines_count": len(ACTIVE_PIPELINES),
            },
        )

        return pipeline_metrics

    def get_active_pipelines(self) -> Dict[str, SlackPipelineMetrics]:
        """Get all currently active pipelines for debugging"""
        return ACTIVE_PIPELINES.copy()

    def get_pipeline_summary(self, correlation_id: str) -> Optional[Dict[str, Any]]:
        """Get summary for a specific pipeline"""
        pipeline = ACTIVE_PIPELINES.get(correlation_id)
        return pipeline.get_summary() if pipeline else None

    def cleanup_stale_pipelines(self, max_age_minutes: int = 30):
        """Clean up pipelines that have been running too long (likely stuck)"""
        cutoff_time = datetime.now(timezone.utc).timestamp() - (max_age_minutes * 60)
        stale_pipelines = []

        for correlation_id, pipeline in ACTIVE_PIPELINES.items():
            if pipeline.started_at.timestamp() < cutoff_time:
                stale_pipelines.append(correlation_id)

        for correlation_id in stale_pipelines:
            pipeline = ACTIVE_PIPELINES.pop(correlation_id, None)
            if pipeline:
                logger.warning(
                    f"SLACK_PIPELINE [{correlation_id}] cleaned up as stale (running > {max_age_minutes}min)",
                    extra={"correlation_id": correlation_id, "max_age_minutes": max_age_minutes},
                )


# Context management utilities
def get_current_correlation_id() -> Optional[str]:
    """Get the current correlation ID from context"""
    try:
        return correlation_id.get()
    except LookupError:
        return None


def get_current_slack_event_id() -> Optional[str]:
    """Get the current Slack event ID from context"""
    try:
        return slack_event_id.get()
    except LookupError:
        return None


def get_current_processing_stage() -> str:
    """Get the current processing stage from context"""
    try:
        return processing_stage.get()
    except LookupError:
        return "unknown"


def preserve_context():
    """Get current context for preservation across async boundaries"""
    return {
        "correlation_id": get_current_correlation_id(),
        "slack_event_id": get_current_slack_event_id(),
        "processing_stage": get_current_processing_stage(),
    }


def restore_context(context: Dict[str, Any]):
    """Restore context in a new async context"""
    if context.get("correlation_id"):
        correlation_id.set(context["correlation_id"])
    if context.get("slack_event_id"):
        slack_event_id.set(context["slack_event_id"])
    if context.get("processing_stage"):
        processing_stage.set(context["processing_stage"])


# Decorator for automatic context preservation
def preserve_slack_context(func):
    """Decorator to automatically preserve Slack context across async calls"""

    async def wrapper(*args, **kwargs):
        context = preserve_context()
        result = await func(*args, **kwargs)
        restore_context(context)
        return result

    return wrapper
