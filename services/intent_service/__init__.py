"""
Intent Service
Understands and classifies user intentions
"""

from .classifier import IntentClassifier
from .honest_failure import HonestFailureHandler, create_graceful_error_response
from .intent_types import IntentClassificationContext, IntentUnderstanding
from .personality_bridge import PersonalityBridge
from .place_detector import PlaceDetector
from .warmth_calibration import WarmthCalibrator, WarmthLevel

# Create a global instance of the IntentClassifier in this package
# This makes it accessible as 'services.intent_service.classifier'
classifier = IntentClassifier()

from .prompts import INTENT_CLASSIFICATION_PROMPT

__all__ = [
    "classifier",
    "IntentClassifier",
    "INTENT_CLASSIFICATION_PROMPT",
    "PlaceDetector",
    "PersonalityBridge",
    "WarmthCalibrator",
    "WarmthLevel",
    "HonestFailureHandler",
    "create_graceful_error_response",
    "IntentClassificationContext",
    "IntentUnderstanding",
]
