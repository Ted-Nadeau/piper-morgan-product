"""
Linear MCP Spatial Adapter

Linear-specific MCP spatial adapter implementation following the established
spatial adapter pattern for external system integration.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import aiohttp

from services.integrations.mcp.token_counter import TokenCounter
from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)

from .consumer_core import MCPConsumerCore

logger = logging.getLogger(__name__)


class LinearMCPSpatialAdapter(BaseSpatialAdapter):
    """
    Linear MCP spatial adapter implementation.

    Maps Linear issue IDs to spatial positions using MCP protocol
    for external service integration.
    """

    def __init__(self):
        super().__init__("linear_mcp")
        self.mcp_consumer = MCPConsumerCore()
        self._lock = asyncio.Lock()
        self._issue_to_position: Dict[str, int] = {}
        self._position_to_issue: Dict[int, str] = {}
        self._context_storage: Dict[str, Dict[str, Any]] = {}

        # Linear API configuration
        self._linear_token: Optional[str] = None
        self._linear_api_base = "https://api.linear.app/graphql"
        self._session: Optional[aiohttp.ClientSession] = None

        # Token counting for MCP operations (Issue #369)
        self.token_counter = TokenCounter()

        logger.info("LinearMCPSpatialAdapter initialized")

    async def configure_linear_api(
        self, token: Optional[str] = None, api_base: Optional[str] = None
    ):
        """Configure Linear API access"""
        if token:
            self._linear_token = token
        if api_base:
            self._linear_api_base = api_base

        # Initialize HTTP session
        if not self._session:
            self._session = aiohttp.ClientSession()

        logger.info("Linear API configured")

    async def _call_linear_api(
        self, query: str, variables: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """Make GraphQL API call to Linear"""
        if not self._session:
            await self.configure_linear_api()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._linear_token}" if self._linear_token else "",
        }

        payload = {"query": query, "variables": variables or {}}

        try:
            async with self._session.post(
                self._linear_api_base, json=payload, headers=headers, timeout=30
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data")
                else:
                    logger.warning(
                        f"Linear API returned {response.status}: {await response.text()}"
                    )
                    return None
        except Exception as e:
            logger.error(f"Linear API call failed: {e}")
            return None

    async def get_issue_by_id(self, issue_id: str) -> Optional[Dict[str, Any]]:
        """Get Linear issue by ID"""
        try:

            async def _operation():
                query = """
                query GetIssue($id: String!) {
                    issue(id: $id) {
                        id
                        number
                        title
                        description
                        priority
                        estimate
                        createdAt
                        updatedAt
                        dueDate
                        state {
                            id
                            name
                            type
                        }
                        assignee {
                            id
                            email
                            name
                        }
                        creator {
                            id
                            email
                            name
                        }
                        team {
                            id
                            name
                            key
                            organization {
                                id
                                name
                            }
                        }
                        project {
                            id
                            name
                        }
                        cycle {
                            id
                            name
                            startsAt
                            endsAt
                        }
                        labels {
                            nodes {
                                id
                                name
                                color
                            }
                        }
                        parent {
                            id
                            number
                            title
                        }
                        children {
                            nodes {
                                id
                                number
                                title
                            }
                        }
                        subscribers {
                            nodes {
                                id
                                email
                                name
                            }
                        }
                        commentCount
                        relations {
                            nodes {
                                id
                                type
                                relatedIssue {
                                    id
                                    number
                                    title
                                }
                            }
                        }
                    }
                }
                """
                result = await self._call_linear_api(query, {"id": issue_id})
                return result.get("issue") if result else None

            result = await self.token_counter.wrap_mcp_call(
                "linear_get_issue_by_id",
                _operation(),
                input_data=f"issue_id={issue_id}",
            )
            logger.info(f"Retrieved Linear issue by ID: {issue_id}")
            return result
        except Exception as e:
            logger.error(f"Error getting Linear issue by ID {issue_id}: {e}")
            return None

    async def get_issue_by_number(
        self, team_key: str, issue_number: int
    ) -> Optional[Dict[str, Any]]:
        """Get Linear issue by team key and issue number"""
        try:

            async def _operation():
                query = """
                query GetIssueByNumber($teamKey: String!, $number: Float!) {
                    team(key: $teamKey) {
                        issue(number: $number) {
                            id
                            number
                            title
                            description
                            priority
                            estimate
                            createdAt
                            updatedAt
                            dueDate
                            state {
                                id
                                name
                                type
                            }
                            assignee {
                                id
                                email
                                name
                            }
                            creator {
                                id
                                email
                                name
                            }
                            team {
                                id
                                name
                                key
                                organization {
                                    id
                                    name
                                }
                            }
                            project {
                                id
                                name
                            }
                            cycle {
                                id
                                name
                                startsAt
                                endsAt
                            }
                            labels {
                                nodes {
                                    id
                                    name
                                    color
                                }
                            }
                            parent {
                                id
                                number
                                title
                            }
                            children {
                                nodes {
                                    id
                                    number
                                    title
                                }
                            }
                            subscribers {
                                nodes {
                                    id
                                    email
                                    name
                                }
                            }
                            commentCount
                            relations {
                                nodes {
                                    id
                                    type
                                    relatedIssue {
                                        id
                                        number
                                        title
                                    }
                                }
                            }
                        }
                    }
                }
                """
                result = await self._call_linear_api(
                    query, {"teamKey": team_key, "number": issue_number}
                )
                if result and result.get("team"):
                    return result["team"].get("issue")
                return None

            result = await self.token_counter.wrap_mcp_call(
                "linear_get_issue_by_number",
                _operation(),
                input_data=f"team_key={team_key},issue_number={issue_number}",
            )
            logger.info(f"Retrieved Linear issue {team_key}-{issue_number}")
            return result
        except Exception as e:
            logger.error(f"Error getting Linear issue {team_key}-{issue_number}: {e}")
            return None

    async def search_issues(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search Linear issues by query"""
        try:

            async def _operation():
                search_query = """
                query SearchIssues($query: String!, $first: Int!) {
                    issues(
                        filter: {
                            or: [
                                { title: { containsIgnoreCase: $query } },
                                { description: { containsIgnoreCase: $query } }
                            ]
                        },
                        first: $first,
                        orderBy: updatedAt
                    ) {
                        nodes {
                            id
                            number
                            title
                            description
                            priority
                            estimate
                            createdAt
                            updatedAt
                            dueDate
                            state {
                                id
                                name
                                type
                            }
                            assignee {
                                id
                                email
                                name
                            }
                            creator {
                                id
                                email
                                name
                            }
                            team {
                                id
                                name
                                key
                                organization {
                                    id
                                    name
                                }
                            }
                            project {
                                id
                                name
                            }
                            cycle {
                                id
                                name
                                startsAt
                                endsAt
                            }
                            labels {
                                nodes {
                                    id
                                    name
                                    color
                                }
                            }
                            commentCount
                        }
                    }
                }
                """
                result = await self._call_linear_api(search_query, {"query": query, "first": limit})
                if result and result.get("issues"):
                    return result["issues"].get("nodes", [])
                return []

            result = await self.token_counter.wrap_mcp_call(
                "linear_search_issues",
                _operation(),
                input_data=f"query={query},limit={limit}",
            )
            logger.info(f"Searched Linear issues with query '{query}', found {len(result)} results")
            return result
        except Exception as e:
            logger.error(f"Error searching Linear issues with query '{query}': {e}")
            return []

    async def map_to_position(self, issue_id: str, context: Dict[str, Any]) -> SpatialPosition:
        """Map Linear issue ID to spatial position"""
        async with self._lock:
            # Check if we already have a mapping
            if issue_id in self._issue_to_position:
                position = self._issue_to_position[issue_id]
                return SpatialPosition(
                    position=position,
                    context={"external_id": issue_id, "external_system": "linear", **context},
                )

            # Create new mapping
            position = len(self._issue_to_position) + 1
            self._issue_to_position[issue_id] = position
            self._position_to_issue[position] = issue_id
            self._context_storage[issue_id] = context

            logger.info(f"Mapped Linear issue {issue_id} to position {position}")

            return SpatialPosition(
                position=position,
                context={"external_id": issue_id, "external_system": "linear", **context},
            )

    async def map_from_position(self, position: SpatialPosition) -> Optional[str]:
        """Map spatial position back to Linear issue ID"""
        return self._position_to_issue.get(position.position)

    async def store_mapping(self, issue_id: str, position: SpatialPosition) -> bool:
        """Store mapping between Linear issue ID and spatial position"""
        try:
            async with self._lock:
                self._issue_to_position[issue_id] = position.position
                self._position_to_issue[position.position] = issue_id
                self._context_storage[issue_id] = position.context
            return True
        except Exception as e:
            logger.error(f"Failed to store mapping for Linear issue {issue_id}: {e}")
            return False

    async def get_context(self, issue_id: str) -> Optional[SpatialContext]:
        """Get spatial context for Linear issue ID"""
        context_data = self._context_storage.get(issue_id)
        if not context_data:
            return None

        return SpatialContext(
            territory_id="linear",
            room_id=context_data.get("team_key", "unknown"),
            path_id=f"issues/{context_data.get('issue_number', issue_id)}",
            attention_level=context_data.get("attention_level", "medium"),
            emotional_valence=context_data.get("emotional_valence", "neutral"),
            navigation_intent=context_data.get("navigation_intent", "explore"),
            external_system="linear",
            external_id=issue_id,
            external_context=context_data,
        )

    async def initialize_connection_pool(self):
        """Initialize MCP connection pool for Linear integration"""
        try:
            await self.mcp_consumer.initialize()
            logger.info("Linear MCP connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Linear MCP connection pool: {e}")

    async def close(self):
        """Close the Linear adapter and cleanup resources"""
        if self._session:
            await self._session.close()

        await self.mcp_consumer.close()
        logger.info("Linear MCP adapter closed")

    def get_mapping_stats(self) -> Dict[str, Any]:
        """Get statistics about current mappings"""
        return {
            "system_name": self.system_name,
            "total_mappings": len(self._issue_to_position),
            "total_contexts": len(self._context_storage),
            "next_position": len(self._issue_to_position) + 1,
            "linear_api_base": self._linear_api_base,
            "has_session": self._session is not None,
        }
