"""
Pattern Recognition Service - Cross-project pattern detection using metadata
Privacy-first design - analyzes patterns in metadata, never raw content
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.repositories import KnowledgeGraphRepository
from services.domain.models import KnowledgeEdge, KnowledgeNode
from services.shared_types import EdgeType, NodeType

logger = structlog.get_logger()


class PatternRecognitionService:
    """Cross-project pattern recognition using metadata analysis"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.knowledge_repo = KnowledgeGraphRepository(session)

        # Pattern detection configuration
        self.similarity_threshold = 0.7
        self.trend_detection_window = 30  # days
        self.anomaly_detection_threshold = 2.0  # standard deviations

    async def find_similar_nodes(
        self, node: KnowledgeNode, node_type: Optional[NodeType] = None, min_similarity: float = 0.7
    ) -> List[Tuple[KnowledgeNode, float]]:
        """
        Find nodes similar to the given node based on metadata analysis

        Args:
            node: Reference node to find similarities for
            node_type: Optional filter by node type
            min_similarity: Minimum similarity score threshold

        Returns:
            List of (node, similarity_score) tuples
        """
        try:
            # Get all nodes of the same type (if specified) or all nodes
            if node_type:
                candidate_nodes = await self.knowledge_repo.get_nodes_by_type(node_type)
            else:
                candidate_nodes = await self.knowledge_repo.get_nodes_by_session("all")

            similar_nodes = []

            for candidate in candidate_nodes:
                if candidate.id == node.id:
                    continue  # Skip self

                similarity_score = self._calculate_metadata_similarity(
                    node.metadata, candidate.metadata
                )

                if similarity_score >= min_similarity:
                    similar_nodes.append((candidate, similarity_score))

            # Sort by similarity score (highest first)
            similar_nodes.sort(key=lambda x: x[1], reverse=True)

            logger.info(
                f"Found {len(similar_nodes)} similar nodes for {node.name}",
                node_id=node.id,
                node_type=node.node_type.value,
                similarity_threshold=min_similarity,
            )

            return similar_nodes

        except Exception as e:
            logger.error(f"Error finding similar nodes: {e}")
            return []

    async def detect_cross_project_patterns(
        self, project_ids: List[str], pattern_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Detect patterns across multiple projects using metadata analysis

        Args:
            project_ids: List of project IDs to analyze
            pattern_types: Optional list of pattern types to focus on

        Returns:
            Dictionary with detected patterns and statistics
        """
        try:
            patterns = {
                "node_patterns": [],
                "edge_patterns": [],
                "trend_patterns": [],
                "anomaly_patterns": [],
                "statistics": {},
            }

            # Collect nodes from all projects
            all_nodes = []
            for project_id in project_ids:
                project_nodes = await self.knowledge_repo.get_nodes_by_session(project_id)
                all_nodes.extend(project_nodes)

            # Analyze node patterns by type
            node_patterns = self._analyze_node_patterns(all_nodes)
            patterns["node_patterns"] = node_patterns

            # Analyze edge patterns
            edge_patterns = await self._analyze_edge_patterns(project_ids)
            patterns["edge_patterns"] = edge_patterns

            # Detect trends
            trend_patterns = await self._detect_trends(all_nodes)
            patterns["trend_patterns"] = trend_patterns

            # Detect anomalies
            anomaly_patterns = await self._detect_anomalies(all_nodes)
            patterns["anomaly_patterns"] = anomaly_patterns

            # Calculate statistics
            patterns["statistics"] = {
                "total_nodes": len(all_nodes),
                "total_patterns": len(node_patterns)
                + len(edge_patterns)
                + len(trend_patterns)
                + len(anomaly_patterns),
                "projects_analyzed": len(project_ids),
                "pattern_types_detected": len(set(p["type"] for p in node_patterns)),
            }

            logger.info(
                f"Cross-project pattern detection completed",
                projects_analyzed=len(project_ids),
                total_patterns=patterns["statistics"]["total_patterns"],
            )

            return patterns

        except Exception as e:
            logger.error(f"Error in cross-project pattern detection: {e}")
            return {"error": str(e)}

    async def calculate_similarity_score(self, node1: KnowledgeNode, node2: KnowledgeNode) -> float:
        """
        Calculate similarity score between two nodes based on metadata

        Args:
            node1: First node for comparison
            node2: Second node for comparison

        Returns:
            Similarity score between 0.0 and 1.0
        """
        try:
            # Calculate metadata similarity
            metadata_similarity = self._calculate_metadata_similarity(
                node1.metadata, node2.metadata
            )

            # Calculate properties similarity
            properties_similarity = self._calculate_properties_similarity(
                node1.properties, node2.properties
            )

            # Calculate type similarity (bonus for same type)
            type_similarity = 1.0 if node1.node_type == node2.node_type else 0.5

            # Weighted combination
            final_similarity = (
                metadata_similarity * 0.5 + properties_similarity * 0.3 + type_similarity * 0.2
            )

            return min(final_similarity, 1.0)

        except Exception as e:
            logger.error(f"Error calculating similarity score: {e}")
            return 0.0

    async def identify_trends(
        self, nodes: List[KnowledgeNode], time_window_days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Identify trends in node creation and metadata patterns

        Args:
            nodes: List of nodes to analyze
            time_window_days: Time window for trend analysis

        Returns:
            List of detected trends
        """
        try:
            trends = []
            cutoff_date = datetime.now() - timedelta(days=time_window_days)

            # Filter nodes by time window
            recent_nodes = [
                node for node in nodes if node.created_at and node.created_at >= cutoff_date
            ]

            # Analyze node type trends
            type_counts = {}
            for node in recent_nodes:
                node_type = node.node_type.value
                type_counts[node_type] = type_counts.get(node_type, 0) + 1

            # Identify trending node types
            for node_type, count in type_counts.items():
                if count >= 3:  # Minimum threshold for trend
                    trends.append(
                        {
                            "type": "node_type_trend",
                            "node_type": node_type,
                            "frequency": count,
                            "trend_strength": min(count / 10.0, 1.0),  # Normalize
                            "time_window_days": time_window_days,
                        }
                    )

            # Analyze metadata pattern trends
            metadata_trends = self._analyze_metadata_trends(recent_nodes)
            trends.extend(metadata_trends)

            logger.info(
                f"Identified {len(trends)} trends in {len(recent_nodes)} recent nodes",
                time_window_days=time_window_days,
            )

            return trends

        except Exception as e:
            logger.error(f"Error identifying trends: {e}")
            return []

    async def detect_anomalies(self, nodes: List[KnowledgeNode]) -> List[Dict[str, Any]]:
        """
        Detect anomalies in node patterns and metadata

        Args:
            nodes: List of nodes to analyze

        Returns:
            List of detected anomalies
        """
        try:
            anomalies = []

            # Analyze node type distribution
            type_distribution = self._calculate_type_distribution(nodes)
            anomalies.extend(self._detect_type_anomalies(type_distribution))

            # Analyze metadata anomalies
            metadata_anomalies = self._detect_metadata_anomalies(nodes)
            anomalies.extend(metadata_anomalies)

            # Analyze temporal anomalies
            temporal_anomalies = self._detect_temporal_anomalies(nodes)
            anomalies.extend(temporal_anomalies)

            logger.info(f"Detected {len(anomalies)} anomalies in {len(nodes)} nodes")

            return anomalies

        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return []

    def _calculate_metadata_similarity(
        self, metadata1: Dict[str, Any], metadata2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between two metadata dictionaries"""
        if not metadata1 or not metadata2:
            return 0.0

        # Get all unique keys
        all_keys = set(metadata1.keys()) | set(metadata2.keys())
        if not all_keys:
            return 0.0

        # Calculate Jaccard similarity for key overlap
        common_keys = set(metadata1.keys()) & set(metadata2.keys())
        key_similarity = len(common_keys) / len(all_keys)

        # Calculate value similarity for common keys
        value_similarities = []
        for key in common_keys:
            val1 = metadata1[key]
            val2 = metadata2[key]

            if isinstance(val1, (str, int, float)) and isinstance(val2, (str, int, float)):
                # Simple value comparison
                if val1 == val2:
                    value_similarities.append(1.0)
                else:
                    value_similarities.append(0.0)
            elif isinstance(val1, dict) and isinstance(val2, dict):
                # Recursive dictionary comparison
                value_similarities.append(self._calculate_metadata_similarity(val1, val2))
            else:
                # Type mismatch
                value_similarities.append(0.0)

        # Combine key and value similarities
        if value_similarities:
            avg_value_similarity = sum(value_similarities) / len(value_similarities)
            return (key_similarity + avg_value_similarity) / 2
        else:
            return key_similarity

    def _calculate_properties_similarity(
        self, properties1: Dict[str, Any], properties2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between two properties dictionaries"""
        return self._calculate_metadata_similarity(properties1, properties2)

    def _analyze_node_patterns(self, nodes: List[KnowledgeNode]) -> List[Dict[str, Any]]:
        """Analyze patterns in node metadata and properties"""
        patterns = []

        # Group nodes by type
        nodes_by_type = {}
        for node in nodes:
            node_type = node.node_type.value
            if node_type not in nodes_by_type:
                nodes_by_type[node_type] = []
            nodes_by_type[node_type].append(node)

        # Analyze patterns for each node type
        for node_type, type_nodes in nodes_by_type.items():
            if len(type_nodes) >= 2:  # Need at least 2 nodes for pattern
                # Analyze metadata patterns
                metadata_patterns = self._analyze_metadata_patterns(type_nodes)
                for pattern in metadata_patterns:
                    pattern["node_type"] = node_type
                    patterns.append(pattern)

        return patterns

    async def _analyze_edge_patterns(self, project_ids: List[str]) -> List[Dict[str, Any]]:
        """Analyze patterns in edge relationships"""
        patterns = []

        for project_id in project_ids:
            edges = await self.knowledge_repo.get_edges_by_session(project_id)

            # Analyze edge type distribution
            edge_type_counts = {}
            for edge in edges:
                edge_type = edge.edge_type.value
                edge_type_counts[edge_type] = edge_type_counts.get(edge_type, 0) + 1

            # Identify common edge patterns
            for edge_type, count in edge_type_counts.items():
                if count >= 3:  # Minimum threshold for pattern
                    patterns.append(
                        {
                            "type": "edge_type_pattern",
                            "edge_type": edge_type,
                            "frequency": count,
                            "project_id": project_id,
                        }
                    )

        return patterns

    async def _detect_trends(self, nodes: List[KnowledgeNode]) -> List[Dict[str, Any]]:
        """Detect trends in node creation and metadata"""
        return await self.identify_trends(nodes)

    async def _detect_anomalies(self, nodes: List[KnowledgeNode]) -> List[Dict[str, Any]]:
        """Detect anomalies in node patterns"""
        return await self.detect_anomalies(nodes)

    def _analyze_metadata_patterns(self, nodes: List[KnowledgeNode]) -> List[Dict[str, Any]]:
        """Analyze metadata patterns across nodes"""
        patterns = []

        # Collect all metadata keys
        all_metadata_keys = set()
        for node in nodes:
            all_metadata_keys.update(node.metadata.keys())

        # Analyze frequency of metadata keys
        for key in all_metadata_keys:
            key_frequency = sum(1 for node in nodes if key in node.metadata)
            if key_frequency >= len(nodes) * 0.3:  # At least 30% of nodes have this key
                patterns.append(
                    {
                        "type": "metadata_key_pattern",
                        "key": key,
                        "frequency": key_frequency,
                        "frequency_ratio": key_frequency / len(nodes),
                    }
                )

        return patterns

    def _analyze_metadata_trends(self, nodes: List[KnowledgeNode]) -> List[Dict[str, Any]]:
        """Analyze trends in metadata patterns"""
        trends = []

        # Analyze metadata key trends
        metadata_key_counts = {}
        for node in nodes:
            for key in node.metadata.keys():
                metadata_key_counts[key] = metadata_key_counts.get(key, 0) + 1

        # Identify trending metadata keys
        for key, count in metadata_key_counts.items():
            if count >= 3:  # Minimum threshold for trend
                trends.append(
                    {
                        "type": "metadata_key_trend",
                        "key": key,
                        "frequency": count,
                        "trend_strength": min(count / len(nodes), 1.0),
                    }
                )

        return trends

    def _calculate_type_distribution(self, nodes: List[KnowledgeNode]) -> Dict[str, int]:
        """Calculate distribution of node types"""
        distribution = {}
        for node in nodes:
            node_type = node.node_type.value
            distribution[node_type] = distribution.get(node_type, 0) + 1
        return distribution

    def _detect_type_anomalies(self, type_distribution: Dict[str, int]) -> List[Dict[str, Any]]:
        """Detect anomalies in node type distribution"""
        anomalies = []

        if not type_distribution:
            return anomalies

        total_nodes = sum(type_distribution.values())
        avg_nodes_per_type = total_nodes / len(type_distribution)

        for node_type, count in type_distribution.items():
            # Detect unusually high or low counts
            if count > avg_nodes_per_type * 2:  # More than 2x average
                anomalies.append(
                    {
                        "type": "type_distribution_anomaly",
                        "node_type": node_type,
                        "count": count,
                        "expected_range": f"0-{avg_nodes_per_type * 1.5:.1f}",
                        "anomaly_type": "high_frequency",
                    }
                )
            elif count < avg_nodes_per_type * 0.3:  # Less than 30% of average
                anomalies.append(
                    {
                        "type": "type_distribution_anomaly",
                        "node_type": node_type,
                        "count": count,
                        "expected_range": f"{avg_nodes_per_type * 0.5:.1f}-{total_nodes}",
                        "anomaly_type": "low_frequency",
                    }
                )

        return anomalies

    def _detect_metadata_anomalies(self, nodes: List[KnowledgeNode]) -> List[Dict[str, Any]]:
        """Detect anomalies in metadata patterns"""
        anomalies = []

        # Analyze metadata key frequency
        key_frequency = {}
        for node in nodes:
            for key in node.metadata.keys():
                key_frequency[key] = key_frequency.get(key, 0) + 1

        # Detect unusual metadata keys
        avg_key_frequency = sum(key_frequency.values()) / len(key_frequency) if key_frequency else 0

        for key, frequency in key_frequency.items():
            if frequency > avg_key_frequency * 2:  # Unusually frequent
                anomalies.append(
                    {
                        "type": "metadata_key_anomaly",
                        "key": key,
                        "frequency": frequency,
                        "expected_frequency": f"0-{avg_key_frequency * 1.5:.1f}",
                        "anomaly_type": "high_frequency",
                    }
                )

        return anomalies

    def _detect_temporal_anomalies(self, nodes: List[KnowledgeNode]) -> List[Dict[str, Any]]:
        """Detect temporal anomalies in node creation"""
        anomalies = []

        # Group nodes by creation date (day)
        nodes_by_date = {}
        for node in nodes:
            if node.created_at:
                date_key = node.created_at.date()
                if date_key not in nodes_by_date:
                    nodes_by_date[date_key] = []
                nodes_by_date[date_key].append(node)

        if len(nodes_by_date) < 2:
            return anomalies

        # Calculate average nodes per day
        total_nodes = sum(len(nodes) for nodes in nodes_by_date.values())
        avg_nodes_per_day = total_nodes / len(nodes_by_date)

        # Detect days with unusual activity
        for date, day_nodes in nodes_by_date.items():
            if len(day_nodes) > avg_nodes_per_day * 2:  # Unusually high activity
                anomalies.append(
                    {
                        "type": "temporal_anomaly",
                        "date": str(date),
                        "node_count": len(day_nodes),
                        "expected_range": f"0-{avg_nodes_per_day * 1.5:.1f}",
                        "anomaly_type": "high_activity",
                    }
                )

        return anomalies


# Singleton instance
_pattern_recognition_service = None


def get_pattern_recognition_service(session: AsyncSession) -> PatternRecognitionService:
    """Get pattern recognition service instance"""
    global _pattern_recognition_service
    if _pattern_recognition_service is None:
        _pattern_recognition_service = PatternRecognitionService(session)
    return _pattern_recognition_service
