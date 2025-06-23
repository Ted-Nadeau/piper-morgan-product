"""
Serializers for converting domain models to API representations.
This keeps serialization logic out of the pure domain models,
adhering to the Single Responsibility Principle.
"""
from typing import Dict, Any
from services.domain.models import Intent

def intent_to_dict(intent: Intent) -> Dict[str, Any]:
    """
    Converts an Intent domain model to a dictionary suitable for API responses.
    """
    if not intent:
        return {}
    return {
        "id": intent.id,
        "category": intent.category.value,
        "action": intent.action,
        "context": intent.context,
        "confidence": intent.confidence,
        "created_at": intent.created_at.isoformat()
    } 