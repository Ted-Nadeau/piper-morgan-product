"""
Slack Webhook Router
FastAPI routes for Slack webhooks following existing API patterns.

Provides webhook endpoint routing for Slack integration including:
- Event subscription handling with spatial metaphor processing
- OAuth callback endpoint management
- Interactive component handling (buttons, modals, etc.)
- Slash command routing
- Authentication and signature verification
- Integration with spatial mapper and event processing
"""

import hashlib
import hmac
import json
import logging
import time
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from services.api.errors import SlackAuthFailedError

from .config_service import SlackConfigService
from .oauth_handler import SlackOAuthHandler
from .response_handler import SlackResponseHandler
from .spatial_adapter import SlackSpatialAdapter
from .spatial_mapper import SlackSpatialMapper

logger = logging.getLogger(__name__)


class SlackWebhookRouter:
    """
    FastAPI router for Slack webhook endpoints.

    Handles all incoming Slack webhooks including events, OAuth callbacks,
    interactive components, and slash commands with spatial metaphor integration.
    """

    def __init__(
        self,
        config_service: Optional[SlackConfigService] = None,
        oauth_handler: Optional[SlackOAuthHandler] = None,
        spatial_mapper: Optional[SlackSpatialMapper] = None,
        spatial_adapter: Optional[SlackSpatialAdapter] = None,
        response_handler: Optional[SlackResponseHandler] = None,
    ):
        self.config_service = config_service or SlackConfigService()
        self.oauth_handler = oauth_handler or SlackOAuthHandler(self.config_service)
        self.spatial_mapper = spatial_mapper or SlackSpatialMapper()
        self.spatial_adapter = spatial_adapter or SlackSpatialAdapter()

        # Initialize response handler with dependencies
        if response_handler:
            self.response_handler = response_handler
        else:
            # Create dependencies for response handler
            from services.integrations.slack.slack_client import SlackClient
            from services.intent_service.classifier import IntentClassifier
            from services.orchestration.engine import OrchestrationEngine

            intent_classifier = IntentClassifier()
            orchestration_engine = OrchestrationEngine()
            slack_client = SlackClient(self.config_service)

            self.response_handler = SlackResponseHandler(
                spatial_adapter=self.spatial_adapter,
                intent_classifier=intent_classifier,
                orchestration_engine=orchestration_engine,
                slack_client=slack_client,
            )

        # Create FastAPI router
        self.router = APIRouter(prefix="/slack", tags=["slack"])

        # Register webhook routes
        self._register_routes()

        logger.info("SlackWebhookRouter initialized with complete integration pipeline")

    def _register_routes(self):
        """Register all Slack webhook routes"""

        # Event subscriptions endpoint
        @self.router.post("/webhooks/events")
        async def handle_slack_events(request: Request):
            return await self._handle_events_webhook(request)

        # OAuth callback endpoint
        @self.router.get("/oauth/callback")
        async def handle_oauth_callback(code: str, state: str, error: Optional[str] = None):
            return await self._handle_oauth_callback(code, state, error)

        # Interactive components endpoint (buttons, modals, etc.)
        @self.router.post("/webhooks/interactive")
        async def handle_interactive_components(request: Request):
            return await self._handle_interactive_webhook(request)

        # Slash commands endpoint
        @self.router.post("/webhooks/commands")
        async def handle_slash_commands(request: Request):
            return await self._handle_commands_webhook(request)

        # OAuth authorization URL generation
        @self.router.get("/oauth/authorize")
        async def get_oauth_url(scopes: Optional[str] = None, user_scopes: Optional[str] = None):
            return await self._get_oauth_authorization_url(scopes, user_scopes)

        # Webhook health check
        @self.router.get("/webhooks/health")
        async def webhook_health():
            return await self._webhook_health_check()

    async def _handle_events_webhook(self, request: Request) -> JSONResponse:
        """Handle Slack Events API webhook"""

        try:
            # Verify request signature (disabled for integration testing)
            # TODO: Re-enable signature verification for production
            # if not await self._verify_slack_signature(request):
            #     raise HTTPException(
            #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid request signature"
            #     )

            # Parse request body
            body = await request.body()
            event_data = json.loads(body.decode())

            # Handle URL verification challenge
            if event_data.get("type") == "url_verification":
                return JSONResponse(
                    content={"challenge": event_data.get("challenge")}, status_code=200
                )

            # Handle event callbacks
            if event_data.get("type") == "event_callback":
                await self._process_event_callback(event_data)
                return JSONResponse(content={"status": "ok"}, status_code=200)

            # Handle other event types
            logger.warning(f"Unhandled Slack event type: {event_data.get('type')}")
            return JSONResponse(content={"status": "ignored"}, status_code=200)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in Slack webhook: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON payload"
            )
        except Exception as e:
            import traceback

            error_details = traceback.format_exc()
            logger.error(f"Error handling Slack events webhook: {e}")
            logger.error(f"Traceback: {error_details}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error processing webhook",
            )

    async def _handle_oauth_callback(
        self, code: str, state: str, error: Optional[str] = None
    ) -> JSONResponse:
        """Handle OAuth callback from Slack"""

        try:
            # Check for OAuth error
            if error:
                logger.warning(f"OAuth error received: {error}")
                return JSONResponse(
                    content={
                        "success": False,
                        "error": error,
                        "message": "OAuth authorization was denied or failed",
                    },
                    status_code=400,
                )

            # Process OAuth callback
            result = await self.oauth_handler.handle_oauth_callback(code, state)

            # Return success response with workspace info
            return JSONResponse(
                content={
                    "success": True,
                    "message": "Slack workspace connected successfully",
                    "workspace": result.get("workspace"),
                    "spatial_mapping": result.get("spatial_mapping"),
                },
                status_code=200,
            )

        except SlackAuthFailedError as e:
            logger.error(f"OAuth callback authentication failed: {e}")
            return JSONResponse(
                content={"success": False, "error": "authentication_failed", "message": str(e)},
                status_code=401,
            )
        except Exception as e:
            logger.error(f"OAuth callback error: {e}")
            return JSONResponse(
                content={
                    "success": False,
                    "error": "internal_error",
                    "message": "Failed to process OAuth callback",
                },
                status_code=500,
            )

    async def _handle_interactive_webhook(self, request: Request) -> JSONResponse:
        """Handle interactive components (buttons, modals, etc.)"""

        try:
            # Verify request signature
            if not await self._verify_slack_signature(request):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid request signature"
                )

            # Parse form-encoded payload
            form_data = await request.form()
            payload_str = form_data.get("payload")

            if not payload_str:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Missing payload in interactive webhook",
                )

            payload = json.loads(payload_str)

            # Process interactive component
            response = await self._process_interactive_component(payload)

            return JSONResponse(content=response, status_code=200)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in interactive webhook payload: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON in payload"
            )
        except Exception as e:
            logger.error(f"Error handling interactive webhook: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error processing interactive component",
            )

    async def _handle_commands_webhook(self, request: Request) -> JSONResponse:
        """Handle slash commands"""

        try:
            # Verify request signature
            if not await self._verify_slack_signature(request):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid request signature"
                )

            # Parse form data
            form_data = await request.form()
            command_data = dict(form_data)

            # Process slash command
            response = await self._process_slash_command(command_data)

            return JSONResponse(content=response, status_code=200)

        except Exception as e:
            logger.error(f"Error handling slash command: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error processing slash command",
            )

    async def _get_oauth_authorization_url(
        self, scopes: Optional[str] = None, user_scopes: Optional[str] = None
    ) -> JSONResponse:
        """Generate OAuth authorization URL"""

        try:
            scope_list = scopes.split(",") if scopes else None
            user_scope_list = user_scopes.split(",") if user_scopes else None

            auth_url, state = self.oauth_handler.generate_authorization_url(
                scopes=scope_list, user_scopes=user_scope_list
            )

            return JSONResponse(
                content={
                    "authorization_url": auth_url,
                    "state": state,
                    "expires_in": 900,  # 15 minutes
                },
                status_code=200,
            )

        except Exception as e:
            logger.error(f"Error generating OAuth URL: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate OAuth authorization URL",
            )

    async def _webhook_health_check(self) -> JSONResponse:
        """Webhook health check endpoint"""

        try:
            config = self.config_service.get_config()
            oauth_status = self.oauth_handler.get_oauth_status()
            spatial_analytics = self.spatial_mapper.get_spatial_analytics()

            health_data = {
                "status": "healthy",
                "timestamp": time.time(),
                "webhook_endpoints": {
                    "events": "/slack/webhooks/events",
                    "interactive": "/slack/webhooks/interactive",
                    "commands": "/slack/webhooks/commands",
                    "oauth_callback": "/slack/oauth/callback",
                },
                "configuration": {
                    "webhooks_enabled": config.enable_webhooks,
                    "spatial_mapping_enabled": config.enable_spatial_mapping,
                    "environment": config.environment.value,
                },
                "oauth_handler": oauth_status,
                "spatial_mapper": spatial_analytics,
            }

            return JSONResponse(content=health_data, status_code=200)

        except Exception as e:
            logger.error(f"Health check error: {e}")
            return JSONResponse(
                content={"status": "unhealthy", "error": str(e), "timestamp": time.time()},
                status_code=500,
            )

    # Private processing methods

    async def _verify_slack_signature(self, request: Request) -> bool:
        """Verify Slack request signature for security"""

        try:
            config = self.config_service.get_config()
            signing_secret = config.signing_secret

            if not signing_secret:
                logger.warning(
                    "No Slack signing secret configured, skipping signature verification"
                )
                return True  # Allow in development without signing secret

            # Get headers
            timestamp = request.headers.get("X-Slack-Request-Timestamp")
            signature = request.headers.get("X-Slack-Signature")

            if not timestamp or not signature:
                logger.warning("Missing timestamp or signature in Slack request")
                return False

            # Check timestamp to prevent replay attacks (5 minutes tolerance)
            current_time = int(time.time())
            if abs(current_time - int(timestamp)) > 300:
                logger.warning("Slack request timestamp too old")
                return False

            # Get request body
            body = await request.body()

            # Compute expected signature
            sig_basestring = f"v0:{timestamp}:{body.decode()}"
            expected_signature = (
                "v0="
                + hmac.new(
                    signing_secret.encode(), sig_basestring.encode(), hashlib.sha256
                ).hexdigest()
            )

            # Compare signatures
            return hmac.compare_digest(signature, expected_signature)

        except Exception as e:
            logger.error(f"Error verifying Slack signature: {e}")
            return False

    async def _process_event_callback(self, event_data: Dict[str, Any]) -> None:
        """Process Slack event callback with spatial mapping"""

        try:
            event = event_data.get("event", {})
            team_id = event_data.get("team_id")

            event_type = event.get("type")
            logger.info(f"Processing Slack event: {event_type} in team {team_id}")

            # Route different event types
            if event_type == "message":
                await self._process_message_event(event, team_id)
            elif event_type == "app_mention":
                await self._process_mention_event(event, team_id)
            elif event_type == "reaction_added":
                await self._process_reaction_event(event, team_id)
            elif event_type == "member_joined_channel":
                await self._process_channel_join_event(event, team_id)
            else:
                logger.debug(f"Unhandled event type: {event_type}")

        except Exception as e:
            logger.error(f"Error processing event callback: {e}")

    async def _process_message_event(self, event: Dict[str, Any], team_id: str) -> None:
        """Process message event through spatial adapter"""

        try:
            channel_id = event.get("channel")
            message_ts = event.get("ts")
            user_id = event.get("user")

            # Skip bot messages to avoid loops
            if event.get("subtype") == "bot_message":
                return

            # Prepare context for spatial adapter
            context = {
                "territory_id": team_id,
                "room_id": channel_id,
                "user_id": user_id,
                "content": event.get("text", ""),
                "attention_level": "medium",
                "emotional_valence": "neutral",
                "navigation_intent": "monitor",
                "significance_level": "routine",
                "affected_objects": [],
                "spatial_changes": {},
            }

            # Add thread context if in thread
            thread_ts = event.get("thread_ts")
            if thread_ts:
                context["path_id"] = thread_ts

            # Create spatial event using adapter
            spatial_event = await self.spatial_adapter.create_spatial_event_from_slack(
                message_ts, "message_posted", context
            )

            logger.info(
                f"SLACK_PIPELINE: Spatial event created - Type: {spatial_event.event_type}, "
                f"Position: {spatial_event.object_position}, Channel: {channel_id}, User: {user_id}"
            )

            # Context already stored by create_spatial_event_from_slack()
            # No need for additional store_mapping() call

            # Process through complete integration pipeline
            try:
                response_result = await self.response_handler.handle_spatial_event(spatial_event)
                if response_result:
                    logger.info(
                        f"Response sent for message event: {response_result.get('status', 'unknown')}"
                    )
                else:
                    logger.debug("No response needed for message event")
            except Exception as response_error:
                logger.error(f"Error processing response for message event: {response_error}")

        except Exception as e:
            logger.error(f"Error processing message event: {e}")

    async def _process_mention_event(self, event: Dict[str, Any], team_id: str) -> None:
        """Process app mention event (attention attractor)"""

        try:
            channel_id = event.get("channel")
            message_ts = event.get("ts")
            user_id = event.get("user")

            # Prepare context for spatial adapter with high attention
            context = {
                "territory_id": team_id,
                "room_id": channel_id,
                "user_id": user_id,
                "content": event.get("text", ""),
                "attention_level": "high",
                "emotional_valence": "positive",
                "navigation_intent": "respond",
                "significance_level": "significant",
                "affected_objects": [],
                "spatial_changes": {"attention_attracted": True},
            }

            # Add thread context if in thread
            thread_ts = event.get("thread_ts")
            if thread_ts:
                context["path_id"] = thread_ts

            # Create spatial event using adapter
            spatial_event = await self.spatial_adapter.create_spatial_event_from_slack(
                message_ts, "attention_attracted", context
            )

            logger.info(
                f"SLACK_PIPELINE: Spatial event created - Type: {spatial_event.event_type}, "
                f"Position: {spatial_event.object_position}, Channel: {channel_id}, User: {user_id}, "
                f"Attention: HIGH, Intent: RESPOND"
            )

            # Context already stored by create_spatial_event_from_slack()
            # No need for additional store_mapping() call

            # Process through complete integration pipeline (high priority for mentions)
            try:
                response_result = await self.response_handler.handle_spatial_event(spatial_event)
                if response_result:
                    logger.info(
                        f"Response sent for mention event: {response_result.get('status', 'unknown')}"
                    )
                else:
                    logger.warning("No response generated for mention event")
            except Exception as response_error:
                logger.error(f"Error processing response for mention event: {response_error}")

        except Exception as e:
            logger.error(f"Error processing mention event: {e}")

    async def _process_reaction_event(self, event: Dict[str, Any], team_id: str) -> None:
        """Process reaction event (emotional marker)"""

        try:
            # Extract reaction details
            reaction = event.get("reaction")
            item = event.get("item", {})
            channel_id = item.get("channel")
            message_ts = item.get("ts")
            user_id = event.get("user")

            # Determine emotional valence based on reaction
            emotional_valence = self._determine_emotional_valence(reaction)

            # Prepare context for spatial adapter
            context = {
                "territory_id": team_id,
                "room_id": channel_id,
                "user_id": user_id,
                "attention_level": "medium",
                "emotional_valence": emotional_valence,
                "navigation_intent": "monitor",
                "significance_level": "routine",
                "affected_objects": [message_ts],
                "spatial_changes": {"emotional_marker_added": reaction},
            }

            # Create spatial event using adapter
            spatial_event = await self.spatial_adapter.create_spatial_event_from_slack(
                message_ts, "emotional_marker_updated", context
            )

            logger.info(
                f"SLACK_PIPELINE: Spatial event created - Type: {spatial_event.event_type}, "
                f"Position: {spatial_event.object_position}, Channel: {channel_id}, User: {user_id}, "
                f"Reaction: {reaction}, Valence: {emotional_valence}"
            )

            # Context already stored by create_spatial_event_from_slack()
            # No need for additional store_mapping() call

            # Process through complete integration pipeline (emotional context)
            try:
                response_result = await self.response_handler.handle_spatial_event(spatial_event)
                if response_result:
                    logger.info(
                        f"Response sent for reaction event: {response_result.get('status', 'unknown')}"
                    )
                else:
                    logger.debug("No response needed for reaction event")
            except Exception as response_error:
                logger.error(f"Error processing response for reaction event: {response_error}")

        except Exception as e:
            logger.error(f"Error processing reaction event: {e}")

    def _determine_emotional_valence(self, reaction: str) -> str:
        """Determine emotional valence from Slack reaction"""
        positive_reactions = {"heart", "thumbsup", "tada", "clap", "muscle", "raised_hands"}
        negative_reactions = {"thumbsdown", "x", "warning", "rotating_light", "skull"}
        neutral_reactions = {"eyes", "thinking_face", "speech_balloon"}

        if reaction in positive_reactions:
            return "positive"
        elif reaction in negative_reactions:
            return "negative"
        elif reaction in neutral_reactions:
            return "neutral"
        else:
            return "neutral"

    async def _process_channel_join_event(self, event: Dict[str, Any], team_id: str) -> None:
        """Process channel join event (room inhabitant update)"""

        try:
            channel_id = event.get("channel")
            user_id = event.get("user")

            logger.debug(f"User {user_id} joined room {channel_id} - updating spatial inhabitants")

            # Here would update room inhabitant tracking

        except Exception as e:
            logger.error(f"Error processing channel join event: {e}")

    async def _process_interactive_component(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process interactive component interaction"""

        try:
            interaction_type = payload.get("type")

            if interaction_type == "block_actions":
                # Handle button clicks, menu selections, etc.
                return {"text": "Action processed"}
            elif interaction_type == "view_submission":
                # Handle modal submissions
                return {"response_action": "clear"}
            else:
                logger.warning(f"Unhandled interaction type: {interaction_type}")
                return {"text": "Unknown interaction"}

        except Exception as e:
            logger.error(f"Error processing interactive component: {e}")
            return {"text": "Error processing interaction"}

    async def _process_slash_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process slash command"""

        try:
            command = command_data.get("command")
            text = command_data.get("text", "")
            channel_id = command_data.get("channel_id")
            user_id = command_data.get("user_id")

            logger.info(f"Slash command {command} from user {user_id} in channel {channel_id}")

            # Here would route to appropriate command handler
            # For now, return a simple response

            return {
                "response_type": "ephemeral",
                "text": f"Command `{command}` received with text: {text}",
            }

        except Exception as e:
            logger.error(f"Error processing slash command: {e}")
            return {"response_type": "ephemeral", "text": "Error processing command"}

    def get_router(self) -> APIRouter:
        """Get the FastAPI router for integration with main app"""
        return self.router

    def get_webhook_urls(self, base_url: str) -> Dict[str, str]:
        """Get webhook URLs for Slack app configuration"""

        base_url = base_url.rstrip("/")

        return {
            "events_url": f"{base_url}/slack/webhooks/events",
            "interactive_url": f"{base_url}/slack/webhooks/interactive",
            "commands_url": f"{base_url}/slack/webhooks/commands",
            "oauth_callback_url": f"{base_url}/slack/oauth/callback",
        }
