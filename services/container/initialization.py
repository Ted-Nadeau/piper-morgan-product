"""Service initialization logic."""

import logging
from typing import Optional

from services.container.exceptions import ServiceInitializationError
from services.container.service_registry import ServiceRegistry

logger = logging.getLogger(__name__)


class ServiceInitializer:
    """Handles service initialization in correct order."""

    def __init__(self, registry: ServiceRegistry):
        self.registry = registry

    async def initialize_all(self) -> None:
        """
        Initialize all services in correct dependency order.

        Order:
        1. LLM service (no dependencies)
        2. OrchestrationEngine (depends on LLM)
        3. Intent service (depends on LLM and OrchestrationEngine)
        """
        logger.info("Starting service initialization sequence")

        # Initialize in dependency order
        await self._initialize_llm_service()
        self._initialize_orchestration_engine()
        self._initialize_intent_service()

        logger.info("Service initialization sequence complete")

    async def _initialize_llm_service(self) -> None:
        """Initialize LLM service."""
        try:
            logger.info("Initializing LLM service")

            # Import here to avoid circular imports
            from services.domain.llm_domain_service import LLMDomainService

            # Create LLM service
            llm_service = LLMDomainService()

            # Initialize (async validation)
            await llm_service.initialize()

            # Register
            self.registry.register(
                "llm", llm_service, metadata={"version": "1.0", "dependencies": []}
            )

            logger.info("LLM service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize LLM service: {e}", exc_info=True)
            raise ServiceInitializationError("llm", e)

    def _initialize_orchestration_engine(self) -> None:
        """Initialize OrchestrationEngine (depends on LLM)."""
        try:
            logger.info("Initializing OrchestrationEngine")

            # Import here to avoid circular imports
            from services.orchestration.engine import OrchestrationEngine

            # Get LLM service from registry
            llm_service = self.registry.get("llm")

            # Get LLM client from LLM service
            # LLMDomainService wraps LLMClient, so we need to get the client
            llm_client = llm_service._llm_client

            # Create OrchestrationEngine with LLM client
            orchestration_engine = OrchestrationEngine(llm_client=llm_client)

            # Register
            self.registry.register(
                "orchestration",
                orchestration_engine,
                metadata={"version": "1.0", "dependencies": ["llm"]},
            )

            logger.info("OrchestrationEngine initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize OrchestrationEngine: {e}", exc_info=True)
            raise ServiceInitializationError("orchestration", e)

    def _initialize_intent_service(self) -> None:
        """Initialize Intent service (depends on LLM and OrchestrationEngine)."""
        try:
            logger.info("Initializing Intent service")

            # Import here to avoid circular imports
            from services.intent.intent_service import IntentService

            # Get OrchestrationEngine from registry
            orchestration_engine = self.registry.get("orchestration")

            # Create Intent service with OrchestrationEngine
            intent_service = IntentService(orchestration_engine=orchestration_engine)

            # Register
            self.registry.register(
                "intent",
                intent_service,
                metadata={"version": "1.0", "dependencies": ["llm", "orchestration"]},
            )

            logger.info("Intent service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Intent service: {e}", exc_info=True)
            raise ServiceInitializationError("intent", e)
