# PM-033a: MCP Consumer Core Architecture

**Date**: 2025-08-10
**Status**: READY FOR IMPLEMENTATION
**Target Sprint**: Monday Development Sprint (August 11, 2025)

## Architecture Overview

The MCP Consumer Core provides foundational Model Context Protocol client capabilities, enabling Piper Morgan to consume external MCP services and tools while laying groundwork for future server mode operations.

## System Components

### 1. Core MCP Client Layer

```python
services/mcp/
├── client.py              # Existing MCP client (11,377 lines)
├── resources.py           # Resource management (16,155 lines)
├── exceptions.py          # Error handling (648 lines)
└── consumer/              # NEW: Consumer core components
    ├── __init__.py
    ├── protocol_client.py # Protocol-compliant client
    ├── tool_federation.py # External tool integration
    ├── resource_discovery.py # Service discovery
    └── auth_integration.py # JWT authentication bridge
```

### 2. Integration Points

#### 2.1 JWT Authentication (ADR-011)
```python
# services/mcp/consumer/auth_integration.py
class MCPAuthenticationBridge:
    """Bridge JWT authentication to MCP protocol"""

    def __init__(self, jwt_service: JWTService):
        self.jwt_service = jwt_service

    async def get_mcp_token(self, user_context: UserContext) -> str:
        """Generate MCP-compatible token from JWT claims"""
        jwt_token = await self.jwt_service.create_access_token(
            subject=user_context.user_id,
            audience=["mcp-protocol"],
            additional_claims={
                "protocol_version": "1.0",
                "permissions": user_context.mcp_permissions
            }
        )
        return jwt_token
```

#### 2.2 Workflow Integration
```python
# services/orchestration/mcp_workflow_adapter.py
class MCPWorkflowAdapter:
    """Adapt MCP tool calls to workflow system"""

    async def create_mcp_workflow(
        self,
        tool_call: MCPToolCall,
        context: WorkflowContext
    ) -> Workflow:
        """Convert MCP tool call to workflow"""
        intent = self._mcp_to_intent(tool_call)
        workflow = await self.factory.create_from_intent(intent)
        return workflow
```

#### 2.3 Query Router Enhancement
```python
# services/queries/mcp_query_extension.py
class MCPQueryExtension:
    """Extend query router with MCP resource queries"""

    async def query_mcp_resources(
        self,
        query: str,
        mcp_servers: List[str]
    ) -> QueryResult:
        """Query external MCP resources"""
        results = []
        for server in mcp_servers:
            client = MCPProtocolClient(server)
            resources = await client.search(query)
            results.extend(resources)
        return self._format_results(results)
```

### 3. Protocol Implementation

#### 3.1 MCP Protocol Client
```python
# services/mcp/consumer/protocol_client.py
class MCPProtocolClient:
    """Standards-compliant MCP client implementation"""

    def __init__(self, config: MCPConfiguration):
        self.config = config
        self.auth_bridge = MCPAuthenticationBridge()
        self.connection_pool = MCPConnectionPool()

    async def connect(self, server_url: str) -> MCPConnection:
        """Establish MCP protocol connection"""
        token = await self.auth_bridge.get_mcp_token()
        connection = await self.connection_pool.get_connection(
            server_url,
            auth_token=token,
            protocol_version=self.config.protocol_version
        )
        return connection

    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> MCPToolResult:
        """Execute tool via MCP protocol"""
        request = MCPToolRequest(
            tool=tool_name,
            parameters=parameters,
            context=self._build_context()
        )
        response = await self.connection.send(request)
        return MCPToolResult.from_response(response)
```

#### 3.2 Tool Federation Service
```python
# services/mcp/consumer/tool_federation.py
class MCPToolFederation:
    """Federate external MCP tools"""

    def __init__(self):
        self.discovered_tools = {}
        self.tool_cache = {}

    async def discover_tools(
        self,
        servers: List[str]
    ) -> Dict[str, MCPTool]:
        """Discover available tools from MCP servers"""
        for server in servers:
            client = MCPProtocolClient(server)
            tools = await client.list_tools()
            self.discovered_tools[server] = tools
        return self.discovered_tools

    async def federate_tool_call(
        self,
        tool_id: str,
        parameters: Dict
    ) -> Any:
        """Federate tool call to appropriate server"""
        server, tool = self._resolve_tool(tool_id)
        client = MCPProtocolClient(server)
        result = await client.execute_tool(tool, parameters)
        return result
```

### 4. Configuration Management

#### 4.1 MCP Configuration Service Enhancement
```python
# services/infrastructure/config/mcp_configuration.py (existing)
class MCPConfigurationService:
    """Enhanced with consumer mode settings"""

    def get_consumer_config(self) -> MCPConsumerConfig:
        """Get MCP consumer configuration"""
        return MCPConsumerConfig(
            enabled=self.get_bool("MCP_CLIENT_ENABLED"),
            timeout=self.get_int("MCP_CLIENT_TIMEOUT"),
            max_retries=self.get_int("MCP_CLIENT_MAX_RETRIES"),
            pool_size=self.get_int("MCP_CLIENT_POOL_SIZE"),
            protocol_version=self.get_str("MCP_PROTOCOL_VERSION"),
            discovery_servers=self.get_list("MCP_DISCOVERY_SERVERS"),
            tool_servers=self.get_list("MCP_TOOL_SERVERS"),
            auth_method=self.get_str("MCP_TOOL_AUTH_METHOD")
        )
```

### 5. Testing Infrastructure

#### 5.1 Reality Testing for MCP
```python
# tests/integration/test_mcp_consumer_reality.py
class TestMCPConsumerReality:
    """Reality testing for MCP consumer - no mocking"""

    @pytest.mark.asyncio
    async def test_real_mcp_connection(self):
        """Test actual MCP protocol connection"""
        client = MCPProtocolClient(test_config)
        connection = await client.connect("https://test.mcp.server")
        assert connection.is_connected

    @pytest.mark.asyncio
    async def test_real_tool_execution(self):
        """Test actual tool execution via MCP"""
        client = MCPProtocolClient(test_config)
        result = await client.execute_tool(
            "search",
            {"query": "test"}
        )
        assert result.success
```

## Implementation Roadmap

### Phase 1: Core Infrastructure (Day 1)
- [ ] Set up MCP consumer package structure
- [ ] Implement MCPProtocolClient with JWT integration
- [ ] Create authentication bridge
- [ ] Establish connection pooling

### Phase 2: Tool Federation (Day 2)
- [ ] Implement tool discovery service
- [ ] Create tool federation router
- [ ] Add caching layer for tool responses
- [ ] Integrate with workflow factory

### Phase 3: Integration (Day 3)
- [ ] Connect to query router
- [ ] Enhance workflow orchestration
- [ ] Add MCP resource queries
- [ ] Implement error handling

### Phase 4: Testing & Validation (Day 4)
- [ ] Reality testing suite
- [ ] Performance benchmarking
- [ ] Security audit
- [ ] Documentation completion

## Performance Targets

- **Connection Establishment**: <100ms
- **Tool Discovery**: <500ms for 10 servers
- **Tool Execution**: <1s average latency
- **Cache Hit Rate**: >80% for repeated queries
- **Connection Pool Efficiency**: >90% connection reuse

## Security Considerations

### Authentication Flow
1. User authenticates → JWT issued
2. JWT claims → MCP token generation
3. MCP token → Protocol authentication
4. Secure connection established

### Data Protection
- TLS 1.3 for all MCP connections
- Token rotation every 15 minutes
- Audit logging for all tool executions
- PII filtering before external calls

## Success Metrics

### Technical Metrics
- [ ] 5+ external MCP tools integrated
- [ ] <1s average tool execution time
- [ ] 99.9% connection reliability
- [ ] Zero authentication failures

### Business Metrics
- [ ] 30% workflow automation improvement
- [ ] User feedback on tool federation value
- [ ] Foundation for PM-033b/c/d phases
- [ ] Protocol compliance certification ready

## Dependencies

### Existing Infrastructure
- ✅ MCP client base (11,377 lines)
- ✅ Resource management (16,155 lines)
- ✅ JWT authentication (ADR-011)
- ✅ Workflow factory (fixed bug)

### External Requirements
- MCP protocol specification v1.0
- Test MCP server for development
- Tool registry access
- Performance monitoring

## Risk Mitigation

### Technical Risks
- **Protocol Changes**: Version compatibility layer
- **Connection Failures**: Retry with exponential backoff
- **Tool Incompatibility**: Validation before federation

### Operational Risks
- **Rate Limiting**: Implement client-side throttling
- **Caching Strategy**: TTL configuration per tool
- **Monitoring**: Comprehensive metrics collection

---

**Ready for Implementation**: All architectural components defined with clear integration points and implementation roadmap for aggressive Monday development sprint.
