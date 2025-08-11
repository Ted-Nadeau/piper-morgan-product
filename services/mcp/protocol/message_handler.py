"""
MCP Message Handler - JSON-RPC 2.0 Protocol Implementation

Handles Model Context Protocol message serialization/deserialization
following JSON-RPC 2.0 specification over stateful connections.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

logger = logging.getLogger(__name__)


class MCPMessage:
    """Base MCP message structure following JSON-RPC 2.0"""

    def __init__(self, jsonrpc: str = "2.0", id: Optional[Union[str, int]] = None):
        self.jsonrpc = jsonrpc
        self.id = id if id is not None else str(uuid4())


class MCPRequest(MCPMessage):
    """MCP request message"""

    def __init__(self, method: str, params: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(**kwargs)
        self.method = method
        self.params = params or {}


class MCPResponse(MCPMessage):
    """MCP response message"""

    def __init__(
        self, result: Optional[Any] = None, error: Optional[Dict[str, Any]] = None, **kwargs
    ):
        super().__init__(**kwargs)
        if result is not None and error is not None:
            raise ValueError("Response cannot have both result and error")
        self.result = result
        self.error = error


class MCPNotification(MCPMessage):
    """MCP notification message (no response expected)"""

    def __init__(self, method: str, params: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(**kwargs)
        self.method = method
        self.params = params or {}
        self.id = None  # Notifications don't have IDs


class MCPMessageHandler:
    """Handles MCP protocol message serialization and deserialization"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._request_counter = 0

    def create_initialize_request(self, client_info: Dict[str, str]) -> MCPRequest:
        """Create MCP initialize request"""
        return MCPRequest(
            method="initialize",
            params={
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "authentication": {"methods": ["jwt", "oauth2"]},
                    "resources": {"subscribable": True},
                    "tools": {"callable": True},
                },
                "clientInfo": client_info,
            },
        )

    def create_list_resources_request(self, uri: Optional[str] = None) -> MCPRequest:
        """Create list resources request"""
        params = {}
        if uri:
            params["uri"] = uri

        return MCPRequest(method="resources/list", params=params)

    def create_get_resource_request(self, uri: str) -> MCPRequest:
        """Create get resource request"""
        return MCPRequest(method="resources/read", params={"uri": uri})

    def create_list_tools_request(self) -> MCPRequest:
        """Create list tools request"""
        return MCPRequest(method="tools/list", params={})

    def create_call_tool_request(self, name: str, arguments: Dict[str, Any]) -> MCPRequest:
        """Create call tool request"""
        return MCPRequest(method="tools/call", params={"name": name, "arguments": arguments})

    def create_list_prompts_request(self) -> MCPRequest:
        """Create list prompts request"""
        return MCPRequest(method="prompts/list", params={})

    def create_subscribe_request(self, uri: str) -> MCPRequest:
        """Create resource subscription request"""
        return MCPRequest(method="resources/subscribe", params={"uri": uri})

    def create_unsubscribe_request(self, uri: str) -> MCPRequest:
        """Create resource unsubscription request"""
        return MCPRequest(method="resources/unsubscribe", params={"uri": uri})

    def serialize_message(self, message: MCPMessage) -> str:
        """Serialize MCP message to JSON string"""
        try:
            # Convert class to dict, handling None values
            message_dict = {}

            # Handle different message types
            if isinstance(message, MCPRequest):
                message_dict = {
                    "jsonrpc": message.jsonrpc,
                    "id": message.id,
                    "method": message.method,
                    "params": message.params,
                }
            elif isinstance(message, MCPResponse):
                message_dict = {"jsonrpc": message.jsonrpc, "id": message.id}
                if message.result is not None:
                    message_dict["result"] = message.result
                if message.error is not None:
                    message_dict["error"] = message.error
            elif isinstance(message, MCPNotification):
                message_dict = {
                    "jsonrpc": message.jsonrpc,
                    "method": message.method,
                    "params": message.params,
                }

            # Remove None values for cleaner JSON
            cleaned_dict = {k: v for k, v in message_dict.items() if v is not None}

            return json.dumps(cleaned_dict, separators=(",", ":"))
        except Exception as e:
            self.logger.error(f"Failed to serialize MCP message: {e}")
            raise

    def deserialize_message(self, json_str: str) -> Union[MCPRequest, MCPResponse, MCPNotification]:
        """Deserialize JSON string to MCP message"""
        try:
            data = json.loads(json_str)

            # Determine message type based on content
            if "method" in data:
                if "id" in data:
                    return MCPRequest(**data)
                else:
                    return MCPNotification(**data)
            elif "result" in data or "error" in data:
                return MCPResponse(**data)
            else:
                raise ValueError("Invalid MCP message format")

        except Exception as e:
            self.logger.error(f"Failed to deserialize MCP message: {e}")
            raise

    def create_error_response(
        self,
        request_id: Union[str, int],
        error_code: int,
        error_message: str,
        error_data: Optional[Any] = None,
    ) -> MCPResponse:
        """Create error response for failed request"""
        error = {"code": error_code, "message": error_message}

        if error_data is not None:
            error["data"] = error_data

        return MCPResponse(id=request_id, error=error)

    def create_success_response(self, request_id: Union[str, int], result: Any) -> MCPResponse:
        """Create success response for successful request"""
        return MCPResponse(id=request_id, result=result)

    def validate_message(self, message: Union[MCPRequest, MCPResponse, MCPNotification]) -> bool:
        """Validate MCP message structure"""
        try:
            if isinstance(message, MCPRequest):
                return bool(message.method and message.jsonrpc == "2.0")
            elif isinstance(message, MCPResponse):
                return message.jsonrpc == "2.0" and (
                    message.result is not None or message.error is not None
                )
            elif isinstance(message, MCPNotification):
                return bool(message.method and message.jsonrpc == "2.0" and message.id is None)
            return False
        except Exception:
            return False

    def get_next_request_id(self) -> str:
        """Get next unique request ID"""
        self._request_counter += 1
        return f"req_{self._request_counter}_{uuid4().hex[:8]}"
