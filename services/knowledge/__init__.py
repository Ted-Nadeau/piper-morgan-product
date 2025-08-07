"""
Knowledge Services Module
Cross-project pattern recognition and knowledge graph services
"""

from .graph_query_service import GraphQueryService, get_graph_query_service
from .pattern_recognition_service import PatternRecognitionService, get_pattern_recognition_service

__all__ = [
    "PatternRecognitionService",
    "get_pattern_recognition_service",
    "GraphQueryService",
    "get_graph_query_service",
]
