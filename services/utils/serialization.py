from dataclasses import asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict

def serialize_dataclass(obj) -> Dict[str, Any]:
    """Serialize dataclass handling datetime and enum fields"""
    def convert_value(value):
        if isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, Enum):
            return value.value
        elif isinstance(value, (list, tuple)):
            return [convert_value(v) for v in value]
        elif isinstance(value, dict):
            return {k: convert_value(v) for k, v in value.items()}
        return value
    
    data = asdict(obj)
    return {k: convert_value(v) for k, v in data.items()} 