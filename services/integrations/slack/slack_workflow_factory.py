"""
Slack Workflow Factory - Create workflows from spatial events
Converts Slack spatial events into Piper Morgan workflows with spatial context.

Integrates spatial metaphor processing with existing workflow orchestration
to enable Slack events to trigger appropriate Piper workflows.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from services.domain.models import Intent, Task, Workflow, WorkflowResult
from services.intent_service.classifier import IntentClassifier
from services.intent_service.spatial_intent_classifier import SpatialIntentClassifier
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import IntentCategory, TaskStatus, TaskType, WorkflowStatus, WorkflowType

from .event_handler import EventProcessingResult
from .spatial_agent import NavigationDecision, NavigationIntent


@dataclass
class SpatialWorkflowContext:
    """Spatial context for workflow creation"""

    room_id: str
    territory_id: str
    spatial_event_type: str
    attention_level: str
    emotional_valence: str
    navigation_intent: str
    spatial_coordinates: Dict[str, Any] = field(default_factory=dict)
    user_context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SlackWorkflowMapping:
    """Mapping from spatial events to workflow types"""

    spatial_event_type: str
    attention_level: str
    navigation_intent: str
    workflow_type: WorkflowType
    priority: int
    confidence_threshold: float
    spatial_context_required: List[str] = field(default_factory=list)


class SlackWorkflowFactory:
    """Factory for creating workflows from Slack spatial events"""

    def __init__(
        self,
        workflow_factory: WorkflowFactory,
        intent_classifier: Optional[IntentClassifier] = None,
    ):
        self.workflow_factory = workflow_factory
        self.intent_classifier = intent_classifier or IntentClassifier()
        self.spatial_intent_classifier = SpatialIntentClassifier()
        self.logger = logging.getLogger(__name__)
        self.spatial_mappings = self._create_spatial_mappings()

    def _create_spatial_mappings(self) -> List[SlackWorkflowMapping]:
        """Create mappings from spatial events to workflow types"""
        return [
            # High attention events (mentions) -> immediate response workflows
            SlackWorkflowMapping(
                spatial_event_type="attention_attracted",
                attention_level="high",
                navigation_intent="respond",
                workflow_type=WorkflowType.CREATE_TASK,
                priority=1,
                confidence_threshold=0.8,
                spatial_context_required=["room_id", "user_context"],
            ),
            # Help requests -> task creation
            SlackWorkflowMapping(
                spatial_event_type="attention_attracted",
                attention_level="high",
                navigation_intent="respond",
                workflow_type=WorkflowType.CREATE_TASK,
                priority=1,
                confidence_threshold=0.7,
                spatial_context_required=["room_id", "user_context"],
            ),
            # Status updates -> report generation
            SlackWorkflowMapping(
                spatial_event_type="message_placed",
                attention_level="medium",
                navigation_intent="monitor",
                workflow_type=WorkflowType.GENERATE_REPORT,
                priority=3,
                confidence_threshold=0.6,
                spatial_context_required=["room_id"],
            ),
            # Alerts -> ticket creation
            SlackWorkflowMapping(
                spatial_event_type="attention_attracted",
                attention_level="high",
                navigation_intent="investigate",
                workflow_type=WorkflowType.CREATE_TICKET,
                priority=1,
                confidence_threshold=0.8,
                spatial_context_required=["room_id", "user_context"],
            ),
            # Emotional events -> feedback analysis
            SlackWorkflowMapping(
                spatial_event_type="emotional_marker_updated",
                attention_level="medium",
                navigation_intent="investigate",
                workflow_type=WorkflowType.ANALYZE_FEEDBACK,
                priority=2,
                confidence_threshold=0.7,
                spatial_context_required=["room_id", "emotional_valence"],
            ),
            # New room exploration -> pattern learning
            SlackWorkflowMapping(
                spatial_event_type="room_created",
                attention_level="low",
                navigation_intent="explore",
                workflow_type=WorkflowType.LEARN_PATTERN,
                priority=4,
                confidence_threshold=0.5,
                spatial_context_required=["room_id"],
            ),
            # Strategic discussions -> strategy planning
            SlackWorkflowMapping(
                spatial_event_type="message_placed",
                attention_level="medium",
                navigation_intent="monitor",
                workflow_type=WorkflowType.PLAN_STRATEGY,
                priority=2,
                confidence_threshold=0.6,
                spatial_context_required=["room_id", "user_context"],
            ),
            # Performance discussions -> metrics analysis
            SlackWorkflowMapping(
                spatial_event_type="message_placed",
                attention_level="medium",
                navigation_intent="monitor",
                workflow_type=WorkflowType.ANALYZE_METRICS,
                priority=3,
                confidence_threshold=0.6,
                spatial_context_required=["room_id"],
            ),
        ]

    async def create_workflow_from_spatial_event(
        self,
        event_result: EventProcessingResult,
        navigation_decision: NavigationDecision,
        spatial_context: SpatialWorkflowContext,
    ) -> Optional[Workflow]:
        """Create workflow from spatial event processing result"""
        try:
            # Find appropriate workflow mapping
            mapping = self._find_workflow_mapping(
                event_result, navigation_decision, spatial_context
            )

            if not mapping:
                self.logger.info(
                    f"No workflow mapping found for spatial event: {event_result.spatial_event.event_type if event_result.spatial_event else 'unknown'}"
                )
                return None

            # Create spatial context for enhanced classification
            if event_result.spatial_event:
                spatial_context_dict = (
                    self.spatial_intent_classifier.convert_spatial_context_to_dict(
                        self.spatial_intent_classifier.create_spatial_context_from_event(
                            event_result.spatial_event,
                            navigation_decision.intent.value,
                            spatial_context.user_context,
                        )
                    )
                )

                # Use enhanced IntentClassifier with spatial context
                message = f"Spatial event: {event_result.spatial_event.event_type}"
                intent = await self.intent_classifier.classify(
                    message=message,
                    context=spatial_context.user_context,
                    spatial_context=spatial_context_dict,
                )
            else:
                # Fallback to original method
                intent = self._create_intent_from_spatial_event(
                    event_result, navigation_decision, spatial_context, mapping
                )

            # Create workflow using existing factory
            workflow = await self.workflow_factory.create_from_intent(
                intent, project_context=self._create_project_context(spatial_context)
            )

            if workflow:
                # Enrich workflow with spatial context
                self._enrich_workflow_with_spatial_context(workflow, spatial_context)
                self.logger.info(
                    f"Created workflow {workflow.id} from spatial event {event_result.spatial_event.event_type if event_result.spatial_event else 'unknown'}"
                )

            return workflow

        except Exception as e:
            import traceback

            self.logger.error(f"Error creating workflow from spatial event: {e}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return None

    def _find_workflow_mapping(
        self,
        event_result: EventProcessingResult,
        navigation_decision: NavigationDecision,
        spatial_context: SpatialWorkflowContext,
    ) -> Optional[SlackWorkflowMapping]:
        """Find appropriate workflow mapping for spatial event"""
        best_mapping = None
        best_score = 0.0

        for mapping in self.spatial_mappings:
            score = self._calculate_mapping_score(
                mapping, event_result, navigation_decision, spatial_context
            )

            if score > best_score and score >= mapping.confidence_threshold:
                best_score = score
                best_mapping = mapping

        return best_mapping

    def _calculate_mapping_score(
        self,
        mapping: SlackWorkflowMapping,
        event_result: EventProcessingResult,
        navigation_decision: NavigationDecision,
        spatial_context: SpatialWorkflowContext,
    ) -> float:
        """Calculate how well a mapping matches the spatial event"""
        score = 0.0

        # Event type match
        if (
            event_result.spatial_event
            and event_result.spatial_event.event_type == mapping.spatial_event_type
        ):
            score += 0.4

        # Attention level match
        if event_result.attention_level.value == mapping.attention_level:
            score += 0.3

        # Navigation intent match
        if navigation_decision.intent.value == mapping.navigation_intent:
            score += 0.3

        # Priority bonus
        score += (5 - mapping.priority) * 0.1

        return min(score, 1.0)

    def _create_intent_from_spatial_event(
        self,
        event_result: EventProcessingResult,
        navigation_decision: NavigationDecision,
        spatial_context: SpatialWorkflowContext,
        mapping: SlackWorkflowMapping,
    ) -> Intent:
        """Create intent from spatial event for workflow creation"""
        # Determine action based on workflow type
        action = self._get_action_for_workflow_type(mapping.workflow_type)

        # Determine category based on workflow type
        category = self._get_category_for_workflow_type(mapping.workflow_type)

        # Create context with spatial information
        context = {
            "original_message": f"Spatial event: {event_result.spatial_event.event_type if event_result.spatial_event else 'unknown'}",
            "spatial_context": {
                "room_id": spatial_context.room_id,
                "territory_id": spatial_context.territory_id,
                "attention_level": spatial_context.attention_level,
                "emotional_valence": spatial_context.emotional_valence,
                "navigation_intent": spatial_context.navigation_intent,
                "spatial_coordinates": spatial_context.spatial_coordinates,
            },
            "user_context": spatial_context.user_context,
            "workflow_priority": mapping.priority,
            "spatial_event_type": (
                event_result.spatial_event.event_type if event_result.spatial_event else "unknown"
            ),
        }

        return Intent(
            category=category,
            action=action,
            context=context,
            confidence=navigation_decision.confidence,
        )

    def _get_action_for_workflow_type(self, workflow_type: WorkflowType) -> str:
        """Get action string for workflow type"""
        action_mapping = {
            WorkflowType.CREATE_TASK: "create_task",
            WorkflowType.CREATE_TICKET: "create_ticket",
            WorkflowType.GENERATE_REPORT: "generate_report",
            WorkflowType.ANALYZE_FEEDBACK: "analyze_feedback",
            WorkflowType.LEARN_PATTERN: "learn_pattern",
            WorkflowType.PLAN_STRATEGY: "plan_strategy",
            WorkflowType.ANALYZE_METRICS: "analyze_metrics",
            WorkflowType.CREATE_FEATURE: "create_feature",
            WorkflowType.REVIEW_ITEM: "review_item",
        }
        return action_mapping.get(workflow_type, "process_spatial_event")

    def _get_category_for_workflow_type(self, workflow_type: WorkflowType) -> IntentCategory:
        """Get intent category for workflow type"""
        category_mapping = {
            WorkflowType.CREATE_TASK: IntentCategory.EXECUTION,
            WorkflowType.CREATE_TICKET: IntentCategory.EXECUTION,
            WorkflowType.GENERATE_REPORT: IntentCategory.ANALYSIS,
            WorkflowType.ANALYZE_FEEDBACK: IntentCategory.ANALYSIS,
            WorkflowType.LEARN_PATTERN: IntentCategory.LEARNING,
            WorkflowType.PLAN_STRATEGY: IntentCategory.PLANNING,
            WorkflowType.ANALYZE_METRICS: IntentCategory.ANALYSIS,
            WorkflowType.CREATE_FEATURE: IntentCategory.EXECUTION,
            WorkflowType.REVIEW_ITEM: IntentCategory.REVIEW,
        }
        return category_mapping.get(workflow_type, IntentCategory.UNKNOWN)

    def _create_project_context(self, spatial_context: SpatialWorkflowContext) -> Dict[str, Any]:
        """Create project context from spatial context"""
        return {
            "spatial_room_id": spatial_context.room_id,
            "spatial_territory_id": spatial_context.territory_id,
            "spatial_attention_level": spatial_context.attention_level,
            "spatial_emotional_valence": spatial_context.emotional_valence,
            "spatial_navigation_intent": spatial_context.navigation_intent,
            "source": "slack_spatial_integration",
        }

    def _enrich_workflow_with_spatial_context(
        self, workflow: Workflow, spatial_context: SpatialWorkflowContext
    ):
        """Enrich workflow with spatial context information"""
        # Add spatial context to workflow context
        workflow.context.update(
            {
                "spatial_integration": {
                    "room_id": spatial_context.room_id,
                    "territory_id": spatial_context.territory_id,
                    "spatial_event_type": spatial_context.spatial_event_type,
                    "attention_level": spatial_context.attention_level,
                    "emotional_valence": spatial_context.emotional_valence,
                    "navigation_intent": spatial_context.navigation_intent,
                    "spatial_coordinates": spatial_context.spatial_coordinates,
                    "user_context": spatial_context.user_context,
                    "created_at": datetime.now().isoformat(),
                }
            }
        )

        # Add spatial information to tasks
        for task in workflow.tasks:
            if task.result is None:
                task.result = {}
            task.result["spatial_context"] = {
                "room_id": spatial_context.room_id,
                "territory_id": spatial_context.territory_id,
            }

    def get_workflow_mappings(self) -> List[SlackWorkflowMapping]:
        """Get all workflow mappings"""
        return self.spatial_mappings.copy()

    def add_workflow_mapping(self, mapping: SlackWorkflowMapping):
        """Add a new workflow mapping"""
        self.spatial_mappings.append(mapping)
        self.logger.info(
            f"Added workflow mapping: {mapping.spatial_event_type} -> {mapping.workflow_type.value}"
        )

    def get_spatial_workflow_stats(self) -> Dict[str, Any]:
        """Get statistics about spatial workflow mappings"""
        return {
            "total_mappings": len(self.spatial_mappings),
            "workflow_types": list(
                set(mapping.workflow_type.value for mapping in self.spatial_mappings)
            ),
            "spatial_event_types": list(
                set(mapping.spatial_event_type for mapping in self.spatial_mappings)
            ),
            "attention_levels": list(
                set(mapping.attention_level for mapping in self.spatial_mappings)
            ),
            "navigation_intents": list(
                set(mapping.navigation_intent for mapping in self.spatial_mappings)
            ),
            "priority_distribution": {
                priority: len([m for m in self.spatial_mappings if m.priority == priority])
                for priority in range(1, 6)
            },
        }
