"""
PM-087 BoundaryEnforcer Service - Enhanced with Phase 3 Advanced Features
Core service for ethics boundary enforcement and decision making

Leverages existing ethics infrastructure:
- services/infrastructure/monitoring/ethics_metrics.py
- services/infrastructure/logging/config.py
- services/domain/models.py patterns

Phase 3 Enhancements:
- Adaptive boundary learning from metadata
- Audit transparency with security redactions
- Enhanced pattern detection algorithms
"""

import asyncio
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import Request

from services.domain.models import BoundaryViolation, EthicalDecision
from services.ethics.adaptive_boundaries import adaptive_boundaries
from services.ethics.audit_transparency import audit_transparency
from services.infrastructure.logging.config import get_ethics_logger
from services.infrastructure.monitoring.ethics_metrics import (
    EthicsDecisionType,
    EthicsMetrics,
    EthicsViolationType,
    ethics_metrics,
)


class BoundaryType:
    """Types of boundaries that can be enforced"""

    PROFESSIONAL = "professional"
    PERSONAL = "personal"
    DATA_PRIVACY = "data_privacy"
    HARASSMENT = "harassment"
    INAPPROPRIATE_CONTENT = "inappropriate_content"


class BoundaryDecision:
    """Result of a boundary enforcement decision"""

    def __init__(
        self,
        violation_detected: bool,
        boundary_type: str,
        explanation: str,
        audit_data: Dict[str, Any],
        session_id: Optional[str] = None,
    ):
        self.violation_detected = violation_detected
        self.boundary_type = boundary_type
        self.explanation = explanation
        self.audit_data = audit_data
        self.session_id = session_id
        self.timestamp = datetime.utcnow()


class BoundaryEnforcer:
    """Core service for ethics boundary enforcement"""

    def __init__(self):
        self.ethics_logger = get_ethics_logger(__name__)
        self.metrics = ethics_metrics

        # Boundary violation patterns
        self.harassment_patterns = [
            "harass",
            "harassment",
            "bully",
            "bullying",
            "intimidate",
            "threaten",
            "inappropriate",
            "unwanted",
            "uncomfortable",
            "offensive",
        ]

        self.professional_boundary_patterns = [
            "personal",
            "private",
            "relationship",
            "romantic",
            "dating",
            "family",
            "home",
            "personal life",
            "private life",
        ]

        self.inappropriate_content_patterns = [
            "explicit",
            "sexual",
            "violent",
            "hate speech",
            "discrimination",
            "racist",
            "sexist",
            "homophobic",
            "transphobic",
        ]

    async def enforce_boundaries(self, request: Request) -> BoundaryDecision:
        """Main boundary enforcement method - Enhanced with Phase 3 features"""
        start_time = time.time()

        # Extract content from request
        content = await self._extract_content_from_request(request)
        session_id = self._get_session_id_from_request(request)

        # Create interaction metadata for adaptive learning
        interaction_metadata = {
            "content_length": len(content),
            "session_id": session_id,
            "timestamp": datetime.utcnow(),
            "request_method": getattr(request, "method", "UNKNOWN"),
            "user_agent_hash": hash(str(request.headers.get("user-agent", ""))) % 10000,
            "time_of_day": datetime.utcnow().hour,
            "day_of_week": datetime.utcnow().weekday(),
        }

        # Perform enhanced boundary checks with adaptive patterns
        violation_detected = False
        boundary_type = None

        # Phase 3: Get adaptive learning enhancement
        adaptive_enhancement = await adaptive_boundaries.get_adaptive_patterns(
            boundary_type or "none"
        )
        explanation = ""
        confidence = 0.0

        # Check for harassment patterns (enhanced)
        harassment_result = await self._enhanced_harassment_check(content, adaptive_enhancement)
        if harassment_result["violation"]:
            violation_detected = True
            boundary_type = BoundaryType.HARASSMENT
            explanation = harassment_result["explanation"]
            confidence = harassment_result["confidence"]

        # Check professional boundaries (enhanced)
        elif await self._enhanced_professional_check(content, adaptive_enhancement):
            violation_detected = True
            boundary_type = BoundaryType.PROFESSIONAL
            explanation = "Content crosses professional boundaries"
            confidence = 0.8 + adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)

        # Check inappropriate content (enhanced)
        elif await self._enhanced_inappropriate_content_check(content, adaptive_enhancement):
            violation_detected = True
            boundary_type = BoundaryType.INAPPROPRIATE_CONTENT
            explanation = "Content contains inappropriate material"
            confidence = 0.75 + adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)

        # Record decision with enhanced data
        response_time_ms = (time.time() - start_time) * 1000
        decision_id = f"bd_{int(time.time() * 1000)}"

        decision = EthicalDecision(
            decision_id=decision_id,
            boundary_type=boundary_type or "none",
            violation_detected=violation_detected,
            explanation=explanation,
            audit_data={
                "content_length": len(content),
                "response_time_ms": response_time_ms,
                "session_id": session_id,
                "confidence": confidence,
                "adaptive_enhancement": adaptive_enhancement,
                "patterns_checked": len(
                    self.harassment_patterns
                    + self.professional_boundary_patterns
                    + self.inappropriate_content_patterns
                ),
            },
            timestamp=datetime.utcnow(),
        )

        await self.audit_decision(decision)

        # Phase 3: Learn from decision and log for transparency
        await adaptive_boundaries.learn_from_decision(decision)
        await audit_transparency.log_ethics_decision(decision)

        # Phase 3: Adaptive learning from interaction
        if (
            interaction_metadata.get("content_length", 0) > 20
        ):  # Learn from substantial interactions
            boundary_decision_obj = BoundaryDecision(
                violation_detected=violation_detected,
                boundary_type=boundary_type or "none",
                explanation=explanation,
                audit_data=decision.audit_data,
                session_id=session_id,
            )

            await adaptive_boundary_system.learn_from_interaction(
                boundary_decision_obj, interaction_metadata
            )

        # Log ethics decision with enhanced data
        self.ethics_logger.log_decision_point(
            "boundary_enforcement",
            {
                "decision_id": decision_id,
                "violation_detected": violation_detected,
                "boundary_type": boundary_type,
                "confidence": confidence,
                "response_time_ms": response_time_ms,
                "adaptive_enhancement": adaptive_enhancement.get("recommendation", "proceed"),
                "session_id": session_id,
            },
        )

        # Record enhanced metrics
        self.metrics.record_ethics_decision(
            EthicsDecisionType.BOUNDARY_ENFORCEMENT,
            "boundary_checked_enhanced",
            response_time_ms,
            session_id,
        )

        if violation_detected:
            # Record violation with enhanced data
            violation_type = self._map_boundary_type_to_violation_type(boundary_type)
            self.metrics.record_boundary_violation(
                violation_type,
                context=f"confidence:{confidence:.2f}|patterns:{adaptive_enhancement.get('learned_patterns_matched', 0)}",
                session_id=session_id,
            )

            # Log violation with enhanced details
            self.ethics_logger.log_boundary_violation(
                boundary_type,
                {
                    "decision_id": decision_id,
                    "confidence": confidence,
                    "adaptive_patterns_matched": adaptive_enhancement.get(
                        "learned_patterns_matched", 0
                    ),
                    "session_id": session_id,
                    "explanation": explanation,
                },
            )

        return BoundaryDecision(
            violation_detected=violation_detected,
            boundary_type=boundary_type or "none",
            explanation=explanation,
            audit_data={
                "decision_id": decision_id,
                "response_time_ms": response_time_ms,
                "confidence": confidence,
                "session_id": session_id,
                "content_length": len(content),
                "adaptive_enhancement": adaptive_enhancement,
            },
            session_id=session_id,
        )

    async def _enhanced_harassment_check(
        self, content: str, adaptive_enhancement: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enhanced harassment detection with confidence scoring"""
        content_lower = content.lower()
        base_confidence = 0.0
        matched_patterns = []

        # Check base patterns
        for pattern in self.harassment_patterns:
            if pattern in content_lower:
                matched_patterns.append(pattern)
                base_confidence += 0.3

        # Apply adaptive enhancement
        adaptive_adjustment = adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)
        final_confidence = min(1.0, base_confidence + adaptive_adjustment)

        # Apply temporal risk factor
        temporal_factor = adaptive_enhancement.get("temporal_risk_factor", 1.0)
        final_confidence *= temporal_factor

        violation_threshold = 0.5
        violation_detected = final_confidence > violation_threshold

        explanation = "Content contains potential harassment patterns"
        if matched_patterns:
            explanation += f" (matched: {len(matched_patterns)} patterns)"
        if adaptive_adjustment != 0:
            explanation += f" (adaptive confidence: {adaptive_adjustment:+.2f})"

        return {
            "violation": violation_detected,
            "confidence": final_confidence,
            "explanation": explanation,
            "matched_patterns": len(matched_patterns),
            "adaptive_adjustment": adaptive_adjustment,
        }

    async def _enhanced_professional_check(
        self, content: str, adaptive_enhancement: Dict[str, Any]
    ) -> bool:
        """Enhanced professional boundary check"""
        base_result = await self.validate_professional_boundaries(content)

        # Apply adaptive enhancement
        if adaptive_enhancement.get("recommendation") == "extra_caution":
            return True  # More strict when adaptive system suggests caution
        elif adaptive_enhancement.get("recommendation") == "proceed_with_confidence":
            return False  # More lenient when system is confident

        return base_result

    async def _enhanced_inappropriate_content_check(
        self, content: str, adaptive_enhancement: Dict[str, Any]
    ) -> bool:
        """Enhanced inappropriate content check"""
        base_result = await self.check_inappropriate_content(content)

        # Apply contextual risk factor
        contextual_factor = adaptive_enhancement.get("contextual_risk_factor", 1.0)
        if contextual_factor > 1.1 and base_result:
            return True  # Higher threshold met with risk factor

        return base_result

    async def validate_professional_boundaries(self, content: str) -> bool:
        """Check if content crosses professional boundaries"""
        content_lower = content.lower()

        for pattern in self.professional_boundary_patterns:
            if pattern in content_lower:
                return True

        return False

    async def check_harassment_patterns(self, content: str) -> bool:
        """Check for harassment patterns in content"""
        content_lower = content.lower()

        for pattern in self.harassment_patterns:
            if pattern in content_lower:
                return True

        return False

    async def check_inappropriate_content(self, content: str) -> bool:
        """Check for inappropriate content patterns"""
        content_lower = content.lower()

        for pattern in self.inappropriate_content_patterns:
            if pattern in content_lower:
                return True

        return False

    async def audit_decision(self, decision: EthicalDecision) -> None:
        """Audit an ethics decision"""
        try:
            # Record audit trail entry
            self.metrics.record_audit_trail_entry(success=True)

            # Log audit decision
            self.ethics_logger.log_behavior_pattern(
                "audit_decision",
                {
                    "decision_id": decision.decision_id,
                    "boundary_type": decision.boundary_type,
                    "violation_detected": decision.violation_detected,
                    "timestamp": decision.timestamp.isoformat(),
                },
            )

        except Exception as e:
            # Record audit failure
            self.metrics.record_audit_trail_entry(success=False)

            # Log error
            self.ethics_logger.log_boundary_violation(
                "audit_failure", {"error": str(e), "decision_id": decision.decision_id}
            )

    async def _extract_content_from_request(self, request: Request) -> str:
        """Extract content from request for boundary checking"""
        try:
            # Try to get content from request body
            body = await request.body()
            if body:
                return body.decode("utf-8")

            # Try to get from form data
            form_data = await request.form()
            if form_data:
                return str(form_data)

            # Try to get from query parameters
            query_params = dict(request.query_params)
            if query_params:
                return str(query_params)

            # Fallback to headers
            return str(dict(request.headers))

        except Exception as e:
            self.ethics_logger.log_boundary_violation("content_extraction_error", {"error": str(e)})
            return ""

    def _get_session_id_from_request(self, request: Request) -> Optional[str]:
        """Extract session ID from request"""
        # Try to get from headers
        session_id = request.headers.get("X-Session-ID")
        if session_id:
            return session_id

        # Try to get from request state (if middleware added it)
        if hasattr(request.state, "correlation"):
            return request.state.correlation.get("session_id")

        return None

    def _map_boundary_type_to_violation_type(self, boundary_type: str) -> EthicsViolationType:
        """Map boundary type to ethics violation type"""
        mapping = {
            BoundaryType.HARASSMENT: EthicsViolationType.HARASSMENT_ATTEMPT,
            BoundaryType.PROFESSIONAL: EthicsViolationType.PROFESSIONAL_BOUNDARY_VIOLATION,
            BoundaryType.PERSONAL: EthicsViolationType.PERSONAL_BOUNDARY_CROSS,
            BoundaryType.DATA_PRIVACY: EthicsViolationType.DATA_PRIVACY_VIOLATION,
            BoundaryType.INAPPROPRIATE_CONTENT: EthicsViolationType.INAPPROPRIATE_REQUEST,
        }

        return mapping.get(boundary_type, EthicsViolationType.PROFESSIONAL_BOUNDARY_VIOLATION)


# Singleton instance
boundary_enforcer = BoundaryEnforcer()
