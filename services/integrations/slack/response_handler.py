"""
Slack Response Handler
Spatial-to-Intent bridge maintaining metaphor purity for complete integration flow.

This handler processes spatial events through the complete Piper Morgan pipeline:
1. Receives spatial events with integer positions
2. Maps back to Slack context via adapter
3. Creates intents from spatial events
4. Processes through orchestration engine
5. Routes responses back to Slack with proper targeting
"""

import logging
from typing import Any, Dict, Optional

from services.domain.models import Intent, SpatialEvent
from services.integrations.slack.slack_client import SlackClient
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.intent_service.classifier import IntentClassifier
from services.orchestration.engine import OrchestrationEngine
from services.shared_types import IntentCategory

logger = logging.getLogger(__name__)


class SlackResponseHandler:
    """
    Handles complete flow from spatial events to Slack responses.

    Maintains spatial metaphor purity by using adapter for context mapping
    while enabling full integration with Piper Morgan's intent and orchestration systems.
    """

    def __init__(
        self,
        spatial_adapter: SlackSpatialAdapter,
        intent_classifier: IntentClassifier,
        orchestration_engine: OrchestrationEngine,
        slack_client: SlackClient,
    ):
        self.spatial_adapter = spatial_adapter
        self.intent_classifier = intent_classifier
        self.orchestration_engine = orchestration_engine
        self.slack_client = slack_client
        self.logger = logging.getLogger(__name__)

        self.logger.info("SlackResponseHandler initialized with complete integration pipeline")

    async def handle_spatial_event(self, spatial_event: SpatialEvent) -> Optional[Dict[str, Any]]:
        """
        Process spatial event through complete integration flow.

        Args:
            spatial_event: SpatialEvent with integer positioning from spatial adapter

        Returns:
            Response result if successful, None if no response needed
        """
        try:
            # Step 1: Get original Slack context from adapter using object position
            slack_context = await self._get_slack_context_from_spatial_event(spatial_event)
            if not slack_context:
                self.logger.warning(f"No Slack context found for spatial event {spatial_event.id}")
                return None

            # Step 2: Create intent from spatial event with preserved context
            intent = await self._create_intent_from_spatial_event(spatial_event, slack_context)
            if not intent:
                self.logger.debug(f"No intent created for spatial event {spatial_event.event_type}")
                return None

            # Step 3: Process through orchestration engine
            workflow_result = await self._process_through_orchestration(intent, slack_context)
            if not workflow_result:
                self.logger.debug(f"No workflow result for intent {intent.action}")
                return None

            # Step 4: Send response back to Slack with proper targeting
            response_result = await self._send_slack_response(workflow_result, slack_context)

            self.logger.info(
                f"✅ COMPLETE INTEGRATION SUCCESS: {spatial_event.event_type} -> "
                f"{intent.action} -> workflow -> response sent to {slack_context.get('channel_id')}"
            )

            return response_result

        except Exception as e:
            self.logger.error(f"Error handling spatial event {spatial_event.id}: {e}")
            return None

    async def _get_slack_context_from_spatial_event(
        self, spatial_event: SpatialEvent
    ) -> Optional[Dict[str, Any]]:
        """
        Get original Slack context from spatial event using adapter.

        Maps from spatial event's object_position back to Slack timestamp,
        then retrieves full context for response routing.
        """
        try:
            # Use object_position to find original Slack timestamp via adapter
            if spatial_event.object_position is None:
                self.logger.warning(f"Spatial event {spatial_event.id} has no object_position")
                return None

            # Get all position mappings to find the one matching our spatial event
            # Since we need reverse lookup by position, we'll search through adapter mappings
            slack_timestamp = None

            # Check adapter's position mappings to find matching timestamp
            async with self.spatial_adapter._lock:
                for timestamp, position in self.spatial_adapter._timestamp_to_position.items():
                    if position == spatial_event.object_position:
                        slack_timestamp = timestamp
                        break

            if not slack_timestamp:
                self.logger.warning(
                    f"No Slack timestamp found for position {spatial_event.object_position}"
                )
                return None

            # Get full response context from adapter
            response_context = await self.spatial_adapter.get_response_context(slack_timestamp)
            if not response_context:
                self.logger.warning(f"No response context found for timestamp {slack_timestamp}")
                return None

            # Enrich with spatial event details
            response_context.update(
                {
                    "spatial_event_type": spatial_event.event_type,
                    "spatial_position": spatial_event.object_position,
                    "territory_position": spatial_event.territory_position,
                    "room_position": spatial_event.room_position,
                    "path_position": spatial_event.path_position,
                    "actor_id": spatial_event.actor_id,
                    "significance_level": spatial_event.significance_level,
                    "original_timestamp": slack_timestamp,
                }
            )

            return response_context

        except Exception as e:
            self.logger.error(f"Error getting Slack context from spatial event: {e}")
            return None

    async def _create_intent_from_spatial_event(
        self, spatial_event: SpatialEvent, slack_context: Dict[str, Any]
    ) -> Optional[Intent]:
        """
        Create intent from spatial event with preserved Slack context.

        Uses enhanced IntentClassifier with spatial context to maintain
        the spatial intelligence throughout the intent classification process.
        """
        try:
            # Determine message content for classification
            message = self._extract_message_from_context(slack_context)
            if not message:
                # Generate synthetic message from spatial event
                message = f"Spatial event: {spatial_event.event_type}"

            # Prepare spatial context for enhanced classification
            spatial_context = {
                "room_id": slack_context.get("channel_id"),
                "territory_id": slack_context.get("workspace_id"),
                "path_id": slack_context.get("thread_ts"),
                "spatial_event_type": spatial_event.event_type,
                "attention_level": slack_context.get("attention_level", "medium"),
                "emotional_valence": slack_context.get("emotional_valence", "neutral"),
                "navigation_intent": slack_context.get("navigation_intent", "monitor"),
                "spatial_coordinates": {
                    "territory_position": spatial_event.territory_position,
                    "room_position": spatial_event.room_position,
                    "path_position": spatial_event.path_position,
                    "object_position": spatial_event.object_position,
                },
            }

            # Classify with spatial context using enhanced IntentClassifier
            intent = await self.intent_classifier.classify(
                message=message,
                context={"user_id": slack_context.get("user_id")},
                spatial_context=spatial_context,
            )

            # Enrich intent context with response targeting
            intent.context.update(
                {
                    "response_target": {
                        "channel_id": slack_context.get("channel_id"),
                        "thread_ts": slack_context.get("thread_ts"),
                        "workspace_id": slack_context.get("workspace_id"),
                    },
                    "spatial_context": spatial_context,
                    "original_spatial_event": spatial_event.id,
                }
            )

            self.logger.debug(
                f"Created intent {intent.action} from spatial event {spatial_event.event_type} "
                f"with confidence {intent.confidence}"
            )

            return intent

        except Exception as e:
            self.logger.error(f"Error creating intent from spatial event: {e}")
            return None

    async def _process_through_orchestration(
        self, intent: Intent, slack_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Process intent through orchestration engine.

        Routes intent through Piper Morgan's orchestration system while
        preserving spatial context for response generation.
        """
        try:
            # Skip only basic QUERY intents that don't need orchestration
            if intent.category == IntentCategory.QUERY:
                # For queries, generate direct response
                return {
                    "type": "query_response",
                    "content": await self._generate_query_response(intent, slack_context),
                    "intent": intent,
                }

            # Process CONVERSATION and LEARNING intents through orchestration
            # These are spatial monitoring intents that need workflow processing
            self.logger.debug(
                f"Processing {intent.category.value} intent '{intent.action}' through orchestration"
            )

            # Create workflow from intent via orchestration engine
            workflow = await self.orchestration_engine.create_workflow_from_intent(intent)
            if not workflow:
                self.logger.warning(f"No workflow created for intent {intent.action}")
                return None

            # Execute workflow
            execution_result = await self.orchestration_engine.execute_workflow(workflow.id)
            if not execution_result:
                self.logger.warning(f"Workflow execution failed for {workflow.id}")
                return None

            self.logger.info(
                f"✅ Successfully processed {intent.category.value} intent through orchestration: {workflow.id}"
            )

            return {
                "type": "workflow_result",
                "workflow_id": workflow.id,
                "result": execution_result,
                "intent": intent,
            }

        except Exception as e:
            self.logger.error(f"Error processing intent through orchestration: {e}")
            return None

    async def _send_slack_response(
        self, workflow_result: Dict[str, Any], slack_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Send response back to Slack with proper targeting.

        Uses preserved Slack context to route response to correct
        channel/thread with spatial awareness.
        """
        try:
            # Extract response content
            response_content = self._format_response_content(workflow_result)
            if not response_content:
                self.logger.debug("No response content to send")
                return None

            # Prepare Slack message parameters with proper targeting
            message_params = {
                "channel": slack_context.get("channel_id"),
                "text": response_content,
            }

            # Add thread targeting if in thread
            thread_ts = slack_context.get("thread_ts")
            if thread_ts:
                message_params["thread_ts"] = thread_ts

            # Send message via Slack client
            response = await self.slack_client.send_message(**message_params)

            self.logger.info(
                f"Sent Slack response to channel {slack_context.get('channel_id')} "
                f"{'in thread' if thread_ts else 'in channel'}"
            )

            return {
                "slack_response": response,
                "target_channel": slack_context.get("channel_id"),
                "thread_ts": thread_ts,
                "response_content": response_content,
            }

        except Exception as e:
            self.logger.error(f"Error sending Slack response: {e}")
            return None

    def _extract_message_from_context(self, slack_context: Dict[str, Any]) -> Optional[str]:
        """Extract original message content from Slack context"""
        # Try to get original message content from context
        content = slack_context.get("content")
        if content and isinstance(content, str):
            return content.strip()
        return None

    async def _generate_query_response(self, intent: Intent, slack_context: Dict[str, Any]) -> str:
        """Generate response content for query intents"""
        # Simple query response generation - could be enhanced with knowledge base
        action = intent.action

        if "status" in action.lower():
            return "📊 Current system status: All services operational"
        elif "help" in action.lower():
            return "🤖 I'm Piper Morgan, your AI Product Management Assistant. How can I help you today?"
        else:
            return f"🔍 I understand you want to {action}. Let me look into that for you."

    def _format_response_content(self, workflow_result: Dict[str, Any]) -> Optional[str]:
        """Format workflow result into response content"""
        result_type = workflow_result.get("type")

        if result_type == "query_response":
            return workflow_result.get("content")
        elif result_type == "workflow_result":
            result = workflow_result.get("result", {})
            if isinstance(result, dict):
                # Extract meaningful content from workflow result
                if "summary" in result:
                    return f"✅ {result['summary']}"
                elif "message" in result:
                    return result["message"]
                else:
                    return "✅ Task completed successfully"
            else:
                return str(result)

        return None

    async def get_handler_stats(self) -> Dict[str, Any]:
        """Get statistics about response handler performance"""
        return {
            "handler_type": "SlackResponseHandler",
            "adapter_stats": await self.spatial_adapter.get_mapping_stats(),
            "components": {
                "spatial_adapter": True,
                "intent_classifier": True,
                "orchestration_engine": True,
                "slack_client": True,
            },
        }
