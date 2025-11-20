"""
ResponsePersonalityEnhancer - Aggregate Root

Orchestrates personality enhancement with <100ms performance constraint.
Integrates profile loading, transformations, and error handling.
"""

import asyncio
import logging
import time
from typing import Any, Dict, Optional
from uuid import UUID

from .cache import ProfileCache
from .exceptions import (
    PerformanceTimeoutError,
    PersonalityEnhancementError,
    ProfileLoadError,
    TransformationError,
)
from .personality_profile import (
    EnhancedResponse,
    Enhancement,
    PersonalityProfile,
    ResponseContext,
    ResponseType,
)
from .repository import PersonalityProfileRepository
from .transformations import TransformationService

logger = logging.getLogger(__name__)


class ResponsePersonalityEnhancer:
    """
    Aggregate root for personality enhancement

    Orchestrates the complete enhancement pipeline:
    1. Load PersonalityProfile (database + PIPER.user.md overrides)
    2. Apply context adaptation
    3. Transform content (warmth → confidence → actions)
    4. Monitor performance (<100ms constraint)
    """

    def __init__(
        self,
        profile_repository: PersonalityProfileRepository,
        transformation_service: Optional[TransformationService] = None,
        profile_cache: Optional[ProfileCache] = None,
        performance_timeout_ms: int = 70,
    ):  # Reduced to 70ms target
        self.profile_repository = profile_repository
        self.transformation_service = transformation_service or TransformationService()
        self.profile_cache = profile_cache or ProfileCache()
        self.performance_timeout_ms = performance_timeout_ms
        self.circuit_breaker = CircuitBreaker()

        # Metrics tracking
        self.enhancement_count = 0
        self.total_enhancement_time_ms = 0.0
        self.cache_hits = 0
        self.cache_misses = 0

    async def enhance_response(
        self, content: str, context: ResponseContext, user_id: str
    ) -> EnhancedResponse:
        """Core domain operation - enhance response with personality"""
        start_time = time.time()
        enhancements_applied = []

        try:
            # Check circuit breaker
            if self.circuit_breaker.is_open():
                logger.warning("Circuit breaker open, skipping enhancement")
                return self._create_fallback_response(
                    content, context, user_id, "Circuit breaker open"
                )

            # Performance timeout protection
            try:
                result = await asyncio.wait_for(
                    self._process_enhancement(
                        content, context, user_id, enhancements_applied, start_time
                    ),
                    timeout=self.performance_timeout_ms / 1000,
                )
                return result
            except asyncio.TimeoutError:
                raise asyncio.TimeoutError()  # Re-raise for outer handling

        except asyncio.TimeoutError:
            processing_time_ms = (time.time() - start_time) * 1000
            logger.warning(f"Enhancement timeout after {processing_time_ms:.1f}ms")
            self.circuit_breaker.record_failure()
            self._update_metrics(processing_time_ms, False)
            return self._create_fallback_response(
                content, context, user_id, f"Enhancement timeout ({processing_time_ms:.1f}ms)"
            )

        except (ProfileLoadError, TransformationError) as e:
            processing_time_ms = (time.time() - start_time) * 1000
            logger.error(f"Enhancement error: {e}")
            self.circuit_breaker.record_failure()
            self._update_metrics(processing_time_ms, False)
            return self._create_fallback_response(content, context, user_id, str(e))

        except Exception as e:
            processing_time_ms = (time.time() - start_time) * 1000
            logger.error(f"Unexpected enhancement error: {e}")
            self.circuit_breaker.record_failure()
            self._update_metrics(processing_time_ms, False)
            return self._create_fallback_response(
                content, context, user_id, f"Unexpected error: {e}"
            )

    async def _process_enhancement(
        self,
        content: str,
        context: ResponseContext,
        user_id: str,
        enhancements_applied: list,
        start_time: float,
    ) -> EnhancedResponse:
        """Core enhancement processing logic"""
        # 1. Load personality profile
        profile = await self._get_profile(user_id)
        if not profile:
            return self._create_fallback_response(content, context, user_id, "Profile not found")

        # 2. Adapt profile for context
        adapted_profile = profile.adjust_for_context(context)

        # 3. Apply transformations in order
        enhanced_content = await self._apply_transformations(
            content, adapted_profile, context, enhancements_applied
        )

        # 4. Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000

        # 5. Update metrics
        self._update_metrics(processing_time_ms, True)

        # 6. Create successful response
        return EnhancedResponse(
            original_content=content,
            enhanced_content=enhanced_content,
            personality_profile_used=adapted_profile,
            confidence_displayed=context.intent_confidence,
            enhancements_applied=enhancements_applied,
            processing_time_ms=processing_time_ms,
            context=context,
            success=True,
        )

    async def _get_profile(self, user_id: str) -> Optional[PersonalityProfile]:
        """Load PersonalityProfile with caching and PIPER.user.md overrides"""
        try:
            # Check cache first
            cached_profile = self.profile_cache.get(user_id)
            if cached_profile:
                self.cache_hits += 1
                return cached_profile

            self.cache_misses += 1

            # Load from repository (includes PIPER.user.md overrides)
            profile = await self.profile_repository.get_by_user_id(user_id)

            if not profile:
                # Create default profile
                profile = PersonalityProfile.get_default(user_id)
                await self.profile_repository.save(profile)

            # Cache the profile
            self.profile_cache.put(user_id, profile)

            return profile

        except Exception as e:
            logger.error(f"Error loading profile for user {user_id}: {e}")
            raise ProfileLoadError(f"Failed to load profile: {e}")

    async def _apply_transformations(
        self,
        content: str,
        profile: PersonalityProfile,
        context: ResponseContext,
        enhancements_applied: list,
    ) -> str:
        """Apply personality transformations in order: warmth → confidence → actions"""
        try:
            enhanced_content = content

            # 1. Add warmth
            if profile.warmth_level > 0.0:
                enhanced_content = self.transformation_service.add_warmth(
                    enhanced_content, profile.warmth_level, context
                )
                enhancements_applied.append(Enhancement.WARMTH_ADDED)

            # 2. Inject confidence
            if context.intent_confidence is not None:
                enhanced_content = self.transformation_service.inject_confidence(
                    enhanced_content, context.intent_confidence, profile.confidence_style, context
                )
                enhancements_applied.append(Enhancement.CONFIDENCE_INJECTED)

            # 3. Extract actions
            enhanced_content = self.transformation_service.extract_actions(
                enhanced_content, profile.action_orientation, context
            )
            enhancements_applied.append(Enhancement.ACTION_EXTRACTED)

            return enhanced_content

        except Exception as e:
            logger.error(f"Transformation error: {e}")
            raise TransformationError(f"Failed to apply transformations: {e}")

    def _create_fallback_response(
        self, content: str, context: ResponseContext, user_id: str, error_message: str
    ) -> EnhancedResponse:
        """Create fallback response when enhancement fails"""
        return EnhancedResponse(
            original_content=content,
            enhanced_content=content,  # Return original content
            personality_profile_used=PersonalityProfile.get_default(user_id),
            confidence_displayed=context.intent_confidence,
            enhancements_applied=[],
            processing_time_ms=0.0,
            context=context,
            success=False,
            error_message=error_message,
        )

    def _update_metrics(self, processing_time_ms: float, success: bool):
        """Update performance metrics"""
        self.enhancement_count += 1
        self.total_enhancement_time_ms += processing_time_ms

        if success:
            self.circuit_breaker.record_success()

        # Log performance warnings
        if processing_time_ms > 50:  # Warning threshold (70% of 70ms target)
            logger.warning(f"Enhancement took {processing_time_ms:.1f}ms (approaching 70ms limit)")

    def get_metrics(self) -> Dict[str, Any]:
        """Get enhancement metrics for monitoring"""
        avg_time = (
            self.total_enhancement_time_ms / self.enhancement_count
            if self.enhancement_count > 0
            else 0.0
        )

        cache_total = self.cache_hits + self.cache_misses
        cache_hit_rate = self.cache_hits / cache_total if cache_total > 0 else 0.0

        return {
            "enhancement_count": self.enhancement_count,
            "average_enhancement_time_ms": avg_time,
            "cache_hit_rate": cache_hit_rate,
            "circuit_breaker_state": self.circuit_breaker.get_state(),
            "performance_budget_ms": self.performance_timeout_ms,
        }


class CircuitBreaker:
    """Circuit breaker for performance protection"""

    def __init__(
        self, failure_threshold: int = 5, timeout_seconds: int = 10
    ):  # More aggressive circuit breaker
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def is_open(self) -> bool:
        """Check if circuit breaker is open"""
        if self.state == "OPEN":
            # Check if timeout has passed for half-open state
            if time.time() - self.last_failure_time > self.timeout_seconds:
                self.state = "HALF_OPEN"
                return False
            return True
        return False

    def record_success(self):
        """Record successful enhancement"""
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
        # Always reset failure count on success to prevent accumulation
        self.failure_count = 0

    def record_failure(self):
        """Record failed enhancement"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def get_state(self) -> str:
        """Get current circuit breaker state"""
        return self.state
