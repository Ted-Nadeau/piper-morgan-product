"""
Task result for orchestration
Domain Task model is in services.domain.models
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TaskResult:
    """Result from executing a task"""

    success: bool
    output_data: Dict[str, Any] = None
    error: Optional[str] = None
