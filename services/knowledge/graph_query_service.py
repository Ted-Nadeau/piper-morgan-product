"""
Graph Query Service - PM-040
Domain-specific language for complex graph traversals and aggregations
"""

import asyncio
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.repositories import KnowledgeGraphRepository
from services.domain.models import KnowledgeEdge, KnowledgeNode
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.knowledge.pattern_recognition_service import PatternRecognitionService
from services.shared_types import EdgeType, NodeType

logger = structlog.get_logger()


class QueryOperator(Enum):
    """Graph query operators for DSL"""

    AND = "and"
    OR = "or"
    NOT = "not"
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    IN = "in"
    NOT_IN = "not_in"


class AggregationType(Enum):
    """Aggregation operations for graph analysis"""

    COUNT = "count"
    SUM = "sum"
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    DISTINCT = "distinct"
    GROUP_BY = "group_by"


@dataclass
class QueryCondition:
    """Query condition for graph filtering"""

    field: str
    operator: QueryOperator
    value: Any
    metadata_field: Optional[str] = None


@dataclass
class GraphQuery:
    """Graph query definition with DSL"""

    query_id: str = field(
        default_factory=lambda: f"query_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    conditions: List[QueryCondition] = field(default_factory=list)
    aggregations: List[Dict[str, Any]] = field(default_factory=list)
    traversal_config: Dict[str, Any] = field(default_factory=dict)
    cache_ttl: int = 300  # 5 minutes default
    created_at: datetime = field(default_factory=datetime.now)


class GraphQueryService:
    """Sophisticated graph query service with DSL and caching"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.knowledge_repo = KnowledgeGraphRepository(session)
        self.knowledge_service = KnowledgeGraphService(self.knowledge_repo)
        self.pattern_service = PatternRecognitionService(session)

        # Caching
        self._query_cache: Dict[str, Tuple[Any, datetime]] = {}
        self._cache_cleanup_interval = 3600  # 1 hour

        # Performance tracking
        self._query_stats = {
            "total_queries": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "avg_query_time": 0.0,
        }

    async def execute_query(self, query: GraphQuery) -> Dict[str, Any]:
        """
        Execute a graph query using the DSL

        Args:
            query: GraphQuery object with conditions and aggregations

        Returns:
            Query results with metadata
        """
        start_time = datetime.now()

        try:
            # Check cache first
            cache_key = self._generate_cache_key(query)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                self._query_stats["cache_hits"] += 1
                return cached_result

            self._query_stats["cache_misses"] += 1

            # Execute query
            result = await self._execute_query_internal(query)

            # Cache result
            self._cache_result(cache_key, result, query.cache_ttl)

            # Update stats
            self._update_query_stats(start_time)

            logger.info(
                f"Graph query executed successfully",
                query_id=query.query_id,
                conditions_count=len(query.conditions),
                aggregations_count=len(query.aggregations),
                result_size=len(result.get("nodes", [])),
            )

            return result

        except Exception as e:
            logger.error(f"Graph query execution failed: {e}", query_id=query.query_id)
            raise

    async def find_nodes_by_pattern(
        self,
        pattern_conditions: List[Dict[str, Any]],
        node_types: Optional[List[NodeType]] = None,
        session_ids: Optional[List[str]] = None,
        limit: int = 100,
    ) -> List[KnowledgeNode]:
        """
        Find nodes matching pattern conditions

        Args:
            pattern_conditions: List of pattern conditions
            node_types: Optional node type filters
            session_ids: Optional session filters
            limit: Maximum number of results

        Returns:
            List of matching nodes
        """
        try:
            # Build query from pattern conditions
            query = GraphQuery()

            for condition in pattern_conditions:
                query.conditions.append(
                    QueryCondition(
                        field=condition.get("field", "metadata"),
                        operator=QueryOperator(condition.get("operator", "contains")),
                        value=condition.get("value"),
                        metadata_field=condition.get("metadata_field"),
                    )
                )

            # Add node type filter
            if node_types:
                query.traversal_config["node_types"] = [nt.value for nt in node_types]

            # Add session filter
            if session_ids:
                query.traversal_config["session_ids"] = session_ids

            # Execute query
            result = await self.execute_query(query)

            return result.get("nodes", [])[:limit]

        except Exception as e:
            logger.error(f"Pattern-based node search failed: {e}")
            return []

    async def aggregate_graph_data(
        self,
        aggregation_type: AggregationType,
        group_by: Optional[str] = None,
        filters: Optional[List[QueryCondition]] = None,
        session_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Perform aggregations on graph data

        Args:
            aggregation_type: Type of aggregation to perform
            group_by: Field to group by (optional)
            filters: Query conditions for filtering
            session_ids: Session IDs to include

        Returns:
            Aggregation results
        """
        try:
            # Build query
            query = GraphQuery()

            if filters:
                query.conditions.extend(filters)

            if session_ids:
                query.traversal_config["session_ids"] = session_ids

            # Add aggregation
            query.aggregations.append(
                {
                    "type": aggregation_type.value,
                    "field": group_by or "node_type",
                    "group_by": group_by,
                }
            )

            # Execute query
            result = await self.execute_query(query)

            return result.get("aggregations", {})

        except Exception as e:
            logger.error(f"Graph aggregation failed: {e}")
            return {}

    async def find_communities(
        self,
        min_community_size: int = 3,
        edge_types: Optional[List[EdgeType]] = None,
        session_ids: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find communities in the knowledge graph

        Args:
            min_community_size: Minimum size for a community
            edge_types: Edge types to consider
            session_ids: Session IDs to include

        Returns:
            List of communities with metadata
        """
        try:
            communities = []

            # Get all nodes
            all_nodes = []
            if session_ids:
                for session_id in session_ids:
                    nodes = await self.knowledge_repo.get_nodes_by_session(session_id)
                    all_nodes.extend(nodes)
            else:
                # Get nodes from all sessions (limited)
                all_nodes = await self.knowledge_repo.get_nodes_by_session("all", limit=1000)

            # Find connected components
            visited = set()

            for node in all_nodes:
                if node.id in visited:
                    continue

                # BFS to find connected component
                community = await self._find_connected_component(node, edge_types)

                if len(community) >= min_community_size:
                    communities.append(
                        {
                            "community_id": f"community_{len(communities)}",
                            "nodes": community,
                            "size": len(community),
                            "node_types": list(set(n.node_type.value for n in community)),
                            "metadata": self._analyze_community_metadata(community),
                        }
                    )

                visited.update(n.id for n in community)

            logger.info(f"Found {len(communities)} communities", min_size=min_community_size)
            return communities

        except Exception as e:
            logger.error(f"Community detection failed: {e}")
            return []

    async def find_influential_nodes(
        self, metric: str = "degree", top_k: int = 10, session_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Find most influential nodes based on various metrics

        Args:
            metric: Influence metric (degree, betweenness, closeness)
            top_k: Number of top nodes to return
            session_ids: Session IDs to include

        Returns:
            List of influential nodes with scores
        """
        try:
            influential_nodes = []

            # Get nodes to analyze
            all_nodes = []
            if session_ids:
                for session_id in session_ids:
                    nodes = await self.knowledge_repo.get_nodes_by_session(session_id)
                    all_nodes.extend(nodes)
            else:
                all_nodes = await self.knowledge_repo.get_nodes_by_session("all", limit=1000)

            # Calculate influence scores
            for node in all_nodes:
                score = await self._calculate_influence_score(node, metric)

                influential_nodes.append({"node": node, "score": score, "metric": metric})

            # Sort by score and return top k
            influential_nodes.sort(key=lambda x: x["score"], reverse=True)

            logger.info(f"Found {len(influential_nodes[:top_k])} influential nodes", metric=metric)
            return influential_nodes[:top_k]

        except Exception as e:
            logger.error(f"Influential node detection failed: {e}")
            return []

    async def analyze_graph_evolution(
        self, time_window_days: int = 30, session_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze how the graph has evolved over time

        Args:
            time_window_days: Time window for analysis
            session_ids: Session IDs to include

        Returns:
            Evolution analysis results
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=time_window_days)

            # Get nodes created in time window
            recent_nodes = []
            if session_ids:
                for session_id in session_ids:
                    nodes = await self.knowledge_repo.get_nodes_by_session(session_id)
                    recent_nodes.extend(
                        [n for n in nodes if n.created_at and n.created_at >= cutoff_date]
                    )
            else:
                all_nodes = await self.knowledge_repo.get_nodes_by_session("all", limit=1000)
                recent_nodes = [
                    n for n in all_nodes if n.created_at and n.created_at >= cutoff_date
                ]

            # Analyze evolution patterns
            evolution_data = {
                "time_window_days": time_window_days,
                "total_new_nodes": len(recent_nodes),
                "node_type_distribution": {},
                "growth_rate": len(recent_nodes) / time_window_days,
                "trends": await self._analyze_evolution_trends(recent_nodes),
                "communities": await self.find_communities(session_ids=session_ids),
                "influential_nodes": await self.find_influential_nodes(session_ids=session_ids),
            }

            # Calculate node type distribution
            for node in recent_nodes:
                node_type = node.node_type.value
                evolution_data["node_type_distribution"][node_type] = (
                    evolution_data["node_type_distribution"].get(node_type, 0) + 1
                )

            logger.info(
                f"Graph evolution analysis completed",
                time_window=time_window_days,
                new_nodes=len(recent_nodes),
            )

            return evolution_data

        except Exception as e:
            logger.error(f"Graph evolution analysis failed: {e}")
            return {}

    async def _execute_query_internal(self, query: GraphQuery) -> Dict[str, Any]:
        """Internal query execution logic"""
        try:
            # Apply filters to get base nodes
            base_nodes = await self._apply_filters(query.conditions, query.traversal_config)

            # Apply aggregations
            aggregations = {}
            if query.aggregations:
                aggregations = await self._apply_aggregations(base_nodes, query.aggregations)

            # Apply traversals
            traversals = {}
            if query.traversal_config:
                traversals = await self._apply_traversals(base_nodes, query.traversal_config)

            return {
                "query_id": query.query_id,
                "nodes": base_nodes,
                "aggregations": aggregations,
                "traversals": traversals,
                "metadata": {
                    "total_nodes": len(base_nodes),
                    "query_time": datetime.now().isoformat(),
                    "cache_key": self._generate_cache_key(query),
                },
            }

        except Exception as e:
            logger.error(f"Internal query execution failed: {e}")
            return {"error": str(e)}

    async def _apply_filters(
        self, conditions: List[QueryCondition], config: Dict[str, Any]
    ) -> List[KnowledgeNode]:
        """Apply filters to get base nodes"""
        try:
            # Get initial nodes based on config
            all_nodes = []

            if "session_ids" in config:
                for session_id in config["session_ids"]:
                    nodes = await self.knowledge_repo.get_nodes_by_session(session_id)
                    all_nodes.extend(nodes)
            else:
                all_nodes = await self.knowledge_repo.get_nodes_by_session("all", limit=1000)

            # Apply node type filter
            if "node_types" in config:
                filtered_nodes = []
                for node in all_nodes:
                    if node.node_type.value in config["node_types"]:
                        filtered_nodes.append(node)
                all_nodes = filtered_nodes

            # Apply conditions
            filtered_nodes = []
            for node in all_nodes:
                if self._node_matches_conditions(node, conditions):
                    filtered_nodes.append(node)

            return filtered_nodes

        except Exception as e:
            logger.error(f"Filter application failed: {e}")
            return []

    def _node_matches_conditions(
        self, node: KnowledgeNode, conditions: List[QueryCondition]
    ) -> bool:
        """Check if node matches all conditions"""
        for condition in conditions:
            if not self._node_matches_condition(node, condition):
                return False
        return True

    def _node_matches_condition(self, node: KnowledgeNode, condition: QueryCondition) -> bool:
        """Check if node matches a single condition"""
        try:
            if condition.field == "metadata":
                value = node.metadata.get(condition.metadata_field or "default", None)
            elif condition.field == "properties":
                value = node.properties.get(condition.metadata_field or "default", None)
            elif condition.field == "node_type":
                value = node.node_type.value
            elif condition.field == "name":
                value = node.name
            else:
                value = getattr(node, condition.field, None)

            return self._value_matches_condition(value, condition.operator, condition.value)

        except Exception as e:
            logger.error(f"Condition matching failed: {e}")
            return False

    def _value_matches_condition(
        self, value: Any, operator: QueryOperator, expected_value: Any
    ) -> bool:
        """Check if value matches condition"""
        try:
            if operator == QueryOperator.EQUALS:
                return value == expected_value
            elif operator == QueryOperator.NOT_EQUALS:
                return value != expected_value
            elif operator == QueryOperator.CONTAINS:
                return expected_value in str(value)
            elif operator == QueryOperator.NOT_CONTAINS:
                return expected_value not in str(value)
            elif operator == QueryOperator.IN:
                return value in expected_value
            elif operator == QueryOperator.NOT_IN:
                return value not in expected_value
            elif operator == QueryOperator.GREATER_THAN:
                return value > expected_value
            elif operator == QueryOperator.LESS_THAN:
                return value < expected_value
            else:
                return False

        except Exception:
            return False

    async def _apply_aggregations(
        self, nodes: List[KnowledgeNode], aggregations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Apply aggregations to nodes"""
        results = {}

        for agg in aggregations:
            agg_type = AggregationType(agg["type"])
            field = agg["field"]
            group_by = agg.get("group_by")

            if agg_type == AggregationType.COUNT:
                results[field] = len(nodes)
            elif agg_type == AggregationType.DISTINCT:
                values = set()
                for node in nodes:
                    if field == "node_type":
                        values.add(node.node_type.value)
                    elif field == "session_id":
                        values.add(node.session_id)
                    else:
                        values.add(getattr(node, field, None))
                results[field] = list(values)
            elif agg_type == AggregationType.GROUP_BY:
                groups = {}
                for node in nodes:
                    if group_by == "node_type":
                        key = node.node_type.value
                    elif group_by == "session_id":
                        key = node.session_id
                    else:
                        key = getattr(node, group_by, "unknown")

                    if key not in groups:
                        groups[key] = []
                    groups[key].append(node)

                results[f"group_by_{group_by}"] = {key: len(nodes) for key, nodes in groups.items()}

        return results

    async def _apply_traversals(
        self, nodes: List[KnowledgeNode], config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply graph traversals"""
        traversals = {}

        # Find paths between nodes
        if "find_paths" in config:
            source_id = config["find_paths"]["source_id"]
            target_id = config["find_paths"]["target_id"]
            paths = await self.knowledge_service.find_paths(source_id, target_id)
            traversals["paths"] = paths

        # Extract subgraphs
        if "extract_subgraph" in config:
            node_ids = config["extract_subgraph"]["node_ids"]
            subgraph = await self.knowledge_service.extract_subgraph(node_ids)
            traversals["subgraph"] = subgraph

        return traversals

    async def _find_connected_component(
        self, start_node: KnowledgeNode, edge_types: Optional[List[EdgeType]]
    ) -> List[KnowledgeNode]:
        """Find connected component using BFS"""
        component = []
        queue = [start_node]
        visited = {start_node.id}

        while queue:
            node = queue.pop(0)
            component.append(node)

            # Get neighbors
            neighbors = await self.knowledge_repo.find_neighbors(
                node.id, edge_type=edge_types[0] if edge_types else None
            )

            for neighbor in neighbors:
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    queue.append(neighbor)

        return component

    async def _calculate_influence_score(self, node: KnowledgeNode, metric: str) -> float:
        """Calculate influence score for a node"""
        try:
            if metric == "degree":
                # Calculate node degree
                neighbors = await self.knowledge_repo.find_neighbors(node.id)
                return len(neighbors)
            elif metric == "betweenness":
                # Simplified betweenness centrality
                return 1.0  # Placeholder
            elif metric == "closeness":
                # Simplified closeness centrality
                return 1.0  # Placeholder
            else:
                return 0.0

        except Exception as e:
            logger.error(f"Influence score calculation failed: {e}")
            return 0.0

    async def _analyze_evolution_trends(self, nodes: List[KnowledgeNode]) -> List[Dict[str, Any]]:
        """Analyze evolution trends"""
        trends = []

        # Analyze node type trends
        type_counts = {}
        for node in nodes:
            node_type = node.node_type.value
            type_counts[node_type] = type_counts.get(node_type, 0) + 1

        for node_type, count in type_counts.items():
            if count >= 3:  # Minimum threshold for trend
                trends.append(
                    {"type": "node_type_trend", "node_type": node_type, "frequency": count}
                )

        return trends

    def _analyze_community_metadata(self, community: List[KnowledgeNode]) -> Dict[str, Any]:
        """Analyze metadata for a community"""
        return {
            "size": len(community),
            "node_types": list(set(n.node_type.value for n in community)),
            "avg_degree": (
                sum(len(n.properties.get("degree", 0)) for n in community) / len(community)
                if community
                else 0
            ),
        }

    def _generate_cache_key(self, query: GraphQuery) -> str:
        """Generate cache key for query"""
        query_data = {
            "conditions": [(c.field, c.operator.value, c.value) for c in query.conditions],
            "aggregations": query.aggregations,
            "traversal_config": query.traversal_config,
        }
        query_str = json.dumps(query_data, sort_keys=True)
        return hashlib.md5(query_str.encode()).hexdigest()

    def _get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached result if available and not expired"""
        if cache_key in self._query_cache:
            result, timestamp = self._query_cache[cache_key]
            if datetime.now() - timestamp < timedelta(seconds=300):  # 5 minutes TTL
                return result
            else:
                del self._query_cache[cache_key]
        return None

    def _cache_result(self, cache_key: str, result: Dict[str, Any], ttl: int):
        """Cache query result"""
        self._query_cache[cache_key] = (result, datetime.now())

    def _update_query_stats(self, start_time: datetime):
        """Update query statistics"""
        self._query_stats["total_queries"] += 1
        query_time = (datetime.now() - start_time).total_seconds()

        # Update average query time
        total_queries = self._query_stats["total_queries"]
        current_avg = self._query_stats["avg_query_time"]
        self._query_stats["avg_query_time"] = (
            current_avg * (total_queries - 1) + query_time
        ) / total_queries

    def get_query_stats(self) -> Dict[str, Any]:
        """Get query service statistics"""
        return self._query_stats.copy()


# Singleton instance
_graph_query_service = None


def get_graph_query_service(session: AsyncSession) -> GraphQueryService:
    """Get graph query service instance"""
    global _graph_query_service
    if _graph_query_service is None:
        _graph_query_service = GraphQueryService(session)
    return _graph_query_service
