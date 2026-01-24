# Trust computation service
# Issue #647: TRUST-LEVELS-1 - Core Infrastructure
# Issue #648: TRUST-LEVELS-2 - Integration
# Issue #649: TRUST-LEVELS-3 - Discussability
# ADR-053: Trust Computation Architecture

from services.trust.explanation_detector import (
    ExplanationDetectionResult,
    ExplanationDetector,
    ExplanationQueryType,
)
from services.trust.explanation_handler import ExplanationHandler, ExplanationHandlerResult
from services.trust.outcome_classifier import OutcomeClassification, OutcomeClassifier, OutcomeType
from services.trust.proactivity_gate import PROACTIVITY_CONFIGS, ProactivityConfig, ProactivityGate
from services.trust.signal_detector import SignalDetectionResult, SignalDetector, SignalType
from services.trust.trust_computation_service import STAGE_THRESHOLDS, TrustComputationService
from services.trust.trust_explainer import ExplanationContext, TrustExplainer
from services.trust.trust_integration import TrustIntegration

__all__ = [
    # Core service (#647)
    "TrustComputationService",
    "STAGE_THRESHOLDS",
    # Proactivity gating (#648)
    "ProactivityGate",
    "ProactivityConfig",
    "PROACTIVITY_CONFIGS",
    # Outcome classification (#648)
    "OutcomeClassifier",
    "OutcomeClassification",
    "OutcomeType",
    # Signal detection (#648)
    "SignalDetector",
    "SignalDetectionResult",
    "SignalType",
    # Integration (#648)
    "TrustIntegration",
    # Discussability (#649)
    "TrustExplainer",
    "ExplanationContext",
    "ExplanationDetector",
    "ExplanationDetectionResult",
    "ExplanationQueryType",
    "ExplanationHandler",
    "ExplanationHandlerResult",
]
