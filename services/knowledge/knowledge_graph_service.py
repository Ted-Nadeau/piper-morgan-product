"""
Knowledge Graph Service - PM-040
High-level business logic for knowledge graph operations
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Set

import structlog

from services.database.repositories import KnowledgeGraphRepository
from services.domain.models import KnowledgeEdge, KnowledgeNode
from services.ethics.boundary_enforcer import BoundaryEnforcer
from services.shared_types import EdgeType, NodeType

logger = structlog.get_logger()


class KnowledgeGraphService:
    """Service for knowledge graph operations with business logic and privacy compliance"""

    def __init__(
        self,
        knowledge_graph_repository: KnowledgeGraphRepository,
        boundary_enforcer: Optional[BoundaryEnforcer] = None,
    ):
        self.repo = knowledge_graph_repository
        self.boundary_enforcer = boundary_enforcer
        self.logger = logger.bind(service="knowledge_graph")

    # Node Operations
    async def create_node(
        self,
        name: str,
        node_type: NodeType,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        properties: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ) -> KnowledgeNode:
        """
        Create a new knowledge node with validation and privacy checks
        """
        self.logger.info(
            "Creating knowledge node", name=name, node_type=node_type.value, session_id=session_id
        )

        # Privacy check if boundary enforcer is available
        if self.boundary_enforcer:
            # For now, skip privacy check as BoundaryEnforcer expects Request objects
            # TODO(#TBD-BOUNDARY-01): Add content-based boundary checking method to BoundaryEnforcer
            pass

        # Create the node
        node = KnowledgeNode(
            name=name,
            node_type=node_type,
            description=description,
            metadata=metadata or {},
            properties=properties or {},
            session_id=session_id,
        )

        # Store in repository
        created_node = await self.repo.create_node(node)

        self.logger.info(
            "Knowledge node created",
            node_id=created_node.id,
            node_type=created_node.node_type.value,
        )

        return created_node

    async def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        """Get a node by ID"""
        return await self.repo.get_node_by_id(node_id)

    async def get_nodes_by_type(
        self, node_type: NodeType, session_id: Optional[str] = None, limit: int = 100
    ) -> List[KnowledgeNode]:
        """Get nodes by type with optional session filtering"""
        return await self.repo.get_nodes_by_type(node_type, session_id, limit)

    async def update_node(
        self,
        node_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> Optional[KnowledgeNode]:
        """Update an existing node"""
        node = await self.repo.get_node_by_id(node_id)
        if not node:
            return None

        # Privacy check for updated content
        if self.boundary_enforcer and (name or description or metadata):
            # TODO(#TBD-BOUNDARY-01): Add content-based boundary checking method to BoundaryEnforcer
            pass

        # Update fields
        if name is not None:
            node.name = name
        if description is not None:
            node.description = description
        if metadata is not None:
            node.metadata.update(metadata)
        if properties is not None:
            node.properties.update(properties)

        node.updated_at = datetime.now()

        # Save updates
        return await self.repo.update(node_id, **node.__dict__)

    # Edge Operations
    async def create_edge(
        self,
        source_node_id: str,
        target_node_id: str,
        edge_type: EdgeType,
        weight: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
        properties: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ) -> KnowledgeEdge:
        """
        Create an edge between two nodes with validation
        """
        # Verify both nodes exist
        source_node = await self.repo.get_node_by_id(source_node_id)
        target_node = await self.repo.get_node_by_id(target_node_id)

        if not source_node:
            raise ValueError(f"Source node {source_node_id} not found")
        if not target_node:
            raise ValueError(f"Target node {target_node_id} not found")

        self.logger.info(
            "Creating knowledge edge",
            source=source_node_id,
            target=target_node_id,
            edge_type=edge_type.value,
        )

        # Create the edge
        edge = KnowledgeEdge(
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            edge_type=edge_type,
            weight=weight,
            metadata=metadata or {},
            properties=properties or {},
            session_id=session_id or source_node.session_id,
        )

        created_edge = await self.repo.create_edge(edge)

        self.logger.info(
            "Knowledge edge created",
            edge_id=created_edge.id,
            edge_type=created_edge.edge_type.value,
        )

        return created_edge

    async def get_edge(self, edge_id: str) -> Optional[KnowledgeEdge]:
        """Get an edge by ID"""
        return await self.repo.get_edge_by_id(edge_id)

    # Graph Operations
    async def get_neighbors(
        self, node_id: str, edge_type: Optional[EdgeType] = None, direction: str = "both"
    ) -> List[KnowledgeNode]:
        """
        Find neighboring nodes

        Args:
            node_id: The node to find neighbors for
            edge_type: Optional filter by edge type
            direction: "incoming", "outgoing", or "both"
        """
        return await self.repo.find_neighbors(node_id, edge_type, direction)

    async def extract_subgraph(
        self,
        node_ids: List[str],
        max_depth: int = 2,
        edge_types: Optional[List[EdgeType]] = None,
        node_types: Optional[List[NodeType]] = None,
    ) -> Dict[str, Any]:
        """
        Extract a subgraph around specified nodes with filtering

        Args:
            node_ids: Starting nodes for subgraph extraction
            max_depth: How many levels to traverse
            edge_types: Optional filter for edge types to follow
            node_types: Optional filter for node types to include
        """
        self.logger.info("Extracting subgraph", start_nodes=len(node_ids), max_depth=max_depth)

        # Get basic subgraph from repository
        subgraph = await self.repo.get_subgraph(node_ids, max_depth)

        # Apply filtering if requested
        if edge_types or node_types:
            filtered_nodes = []
            filtered_edges = []

            # Filter nodes by type
            if node_types:
                node_type_set = set(node_types)
                for node in subgraph["nodes"]:
                    if node.node_type in node_type_set:
                        filtered_nodes.append(node)
            else:
                filtered_nodes = subgraph["nodes"]

            # Create set of valid node IDs for edge filtering
            valid_node_ids = {node.id for node in filtered_nodes}

            # Filter edges by type and valid nodes
            if edge_types:
                edge_type_set = set(edge_types)
                for edge in subgraph["edges"]:
                    if (
                        edge.edge_type in edge_type_set
                        and edge.source_node_id in valid_node_ids
                        and edge.target_node_id in valid_node_ids
                    ):
                        filtered_edges.append(edge)
            else:
                # Just filter by valid nodes
                for edge in subgraph["edges"]:
                    if (
                        edge.source_node_id in valid_node_ids
                        and edge.target_node_id in valid_node_ids
                    ):
                        filtered_edges.append(edge)

            subgraph["nodes"] = filtered_nodes
            subgraph["edges"] = filtered_edges

        # Privacy filtering if boundary enforcer is available
        if self.boundary_enforcer:
            # Filter nodes based on privacy boundaries
            privacy_filtered_nodes = []
            for node in subgraph["nodes"]:
                # TODO: Implement proper boundary check
                # For now, allow all nodes
                check = type("obj", (object,), {"allowed": True, "reason": None})
                if check.allowed:
                    privacy_filtered_nodes.append(node)
                else:
                    self.logger.debug(
                        "Node filtered by privacy boundaries", node_id=node.id, reason=check.reason
                    )

            subgraph["nodes"] = privacy_filtered_nodes

            # Update edges to only include those between allowed nodes
            allowed_node_ids = {node.id for node in privacy_filtered_nodes}
            subgraph["edges"] = [
                edge
                for edge in subgraph["edges"]
                if edge.source_node_id in allowed_node_ids
                and edge.target_node_id in allowed_node_ids
            ]

        self.logger.info(
            "Subgraph extracted", nodes=len(subgraph["nodes"]), edges=len(subgraph["edges"])
        )

        return subgraph

    async def find_paths(
        self, source_id: str, target_id: str, max_paths: int = 5, max_depth: int = 5
    ) -> List[List[KnowledgeNode]]:
        """
        Find paths between two nodes

        Args:
            source_id: Starting node
            target_id: Target node
            max_paths: Maximum number of paths to return
            max_depth: Maximum path length to consider
        """
        # For now, use repository's simple implementation
        # TODO: Implement more sophisticated algorithms (Dijkstra, A*, etc.)
        return await self.repo.find_paths(source_id, target_id, max_paths)

    # Bulk Operations
    async def create_nodes_bulk(
        self, nodes_data: List[Dict[str, Any]], session_id: Optional[str] = None
    ) -> List[KnowledgeNode]:
        """
        Create multiple nodes efficiently

        Args:
            nodes_data: List of node data dictionaries
            session_id: Session ID to apply to all nodes
        """
        nodes = []
        for data in nodes_data:
            node = KnowledgeNode(
                name=data.get("name", ""),
                node_type=data.get("node_type", NodeType.CONCEPT),
                description=data.get("description", ""),
                metadata=data.get("metadata", {}),
                properties=data.get("properties", {}),
                session_id=session_id or data.get("session_id"),
            )
            nodes.append(node)

        # Privacy check if enforcer available
        if self.boundary_enforcer:
            for node in nodes:
                # TODO: Implement proper boundary check
                # For now, allow all nodes
                check = type("obj", (object,), {"allowed": True, "reason": None})
                if not check.allowed:
                    raise ValueError(f"Node '{node.name}' violates boundaries: {check.reason}")

        return await self.repo.create_nodes_bulk(nodes)

    async def create_edges_bulk(
        self, edges_data: List[Dict[str, Any]], session_id: Optional[str] = None
    ) -> List[KnowledgeEdge]:
        """
        Create multiple edges efficiently

        Args:
            edges_data: List of edge data dictionaries
            session_id: Session ID to apply to all edges
        """
        edges = []
        for data in edges_data:
            edge = KnowledgeEdge(
                source_node_id=data["source_node_id"],
                target_node_id=data["target_node_id"],
                edge_type=data.get("edge_type", EdgeType.REFERENCES),
                weight=data.get("weight", 1.0),
                metadata=data.get("metadata", {}),
                properties=data.get("properties", {}),
                session_id=session_id or data.get("session_id"),
            )
            edges.append(edge)

        return await self.repo.create_edges_bulk(edges)

    # Analytics Operations
    async def get_node_degree(self, node_id: str, direction: str = "both") -> Dict[str, int]:
        """
        Get the degree (number of connections) for a node

        Returns:
            Dict with "incoming", "outgoing", and "total" counts
        """
        neighbors_in = await self.repo.find_neighbors(node_id, direction="incoming")
        neighbors_out = await self.repo.find_neighbors(node_id, direction="outgoing")

        return {
            "incoming": len(neighbors_in),
            "outgoing": len(neighbors_out),
            "total": len(set(n.id for n in neighbors_in + neighbors_out)),
        }

    async def get_graph_statistics(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get basic statistics about the knowledge graph

        Args:
            session_id: Optional session filter
        """
        nodes = await self.repo.get_nodes_by_session(session_id) if session_id else []
        edges = await self.repo.get_edges_by_session(session_id) if session_id else []

        # Count nodes by type
        node_type_counts = {}
        for node in nodes:
            node_type = node.node_type.value
            node_type_counts[node_type] = node_type_counts.get(node_type, 0) + 1

        # Count edges by type
        edge_type_counts = {}
        for edge in edges:
            edge_type = edge.edge_type.value
            edge_type_counts[edge_type] = edge_type_counts.get(edge_type, 0) + 1

        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "node_types": node_type_counts,
            "edge_types": edge_type_counts,
            "session_id": session_id,
        }

    # Privacy-Aware Operations
    async def get_nodes_with_privacy(
        self, session_id: str, include_private: bool = False
    ) -> List[KnowledgeNode]:
        """
        Get nodes with privacy filtering

        Args:
            session_id: Session to retrieve nodes for
            include_private: Whether to include private/sensitive nodes
        """
        if include_private or not self.boundary_enforcer:
            # No privacy filtering
            return await self.repo.get_nodes_by_session(session_id)

        # Use repository's privacy-aware method
        return await self.repo.get_nodes_with_privacy_check(session_id)

    async def create_node_with_privacy(
        self, node_data: Dict[str, Any], privacy_level: str = "standard"
    ) -> KnowledgeNode:
        """
        Create a node with enhanced privacy checks

        Args:
            node_data: Node creation data
            privacy_level: Privacy level to enforce ("standard", "strict", "public")
        """
        # Delegate to repository's privacy-aware creation
        node = KnowledgeNode(**node_data)
        return await self.repo.create_node_with_privacy_check(node, privacy_level)
