# MCP Proof of Concept Plan

**Date**: July 17, 2025
**Timeline**: 2-3 days
**Objective**: Validate MCP value with minimal integration risk

## Executive Summary

Based on the technical analysis, MCP's stateful connections and federated architecture represent a significant shift from our current patterns. This POC will validate the core value proposition with minimal risk by implementing a simple file system MCP server integration.

## Selected Use Case: Enhanced File Search

**Why This Use Case:**
- **Low Risk**: File system access is local, no external dependencies
- **High Value**: Demonstrates MCP resource capabilities
- **Minimal Changes**: Extends existing file search without replacing core logic
- **Clear Success Metrics**: Improved search results are easily measurable

**Value Proposition:**
Current file search is limited to filename matching. MCP file server can provide:
- Content-based search across uploaded documents
- Metadata extraction (file type, size, creation date)
- Semantic search capabilities
- Structured file information

## POC Architecture

### Minimal Integration Strategy
```
Piper Morgan Core (unchanged)
         ↓
Enhanced File Search (new)
         ↓
MCP Client (minimal)
         ↓
MCP File Server (local)
         ↓
uploads/ directory
```

### Code Structure
```
services/mcp/
├── client.py          # Basic MCP client
├── handlers.py        # Message handlers
├── resources.py       # Resource access layer
└── file_server.py     # Local file server implementation
```

## Implementation Plan

### Day 1: Foundation
1. **Install MCP SDK**: `pip install "mcp[cli]"`
2. **Create basic client**: Connect to local file server
3. **Implement file server**: Expose uploads/ directory as MCP resources

### Day 2: Integration
1. **Create resource handlers**: Access files via MCP
2. **Extend file search**: Add MCP-based search option
3. **Add fallback logic**: Graceful degradation if MCP unavailable

### Day 3: Validation
1. **Performance testing**: Compare MCP vs direct file access
2. **Error handling**: Test connection failures and recovery
3. **User experience**: Validate improved search results

## Success Criteria

### Technical Success
- [ ] MCP client connects to local file server
- [ ] File resources accessible via MCP protocol
- [ ] Search results include MCP-sourced data
- [ ] Fallback to direct file access works
- [ ] Performance acceptable (<500ms additional latency)

### Functional Success
- [ ] Enhanced search finds files by content
- [ ] Metadata extraction provides useful information
- [ ] No degradation of existing functionality
- [ ] Clear error messages for MCP failures

## Risk Mitigation

### 1. Isolation Strategy
**Risk**: MCP code breaks existing functionality
**Mitigation**:
- Feature flag: `ENABLE_MCP_FILE_SEARCH=false` by default
- Separate service module with clear boundaries
- Existing file search remains primary path

### 2. Fallback Mechanisms
**Risk**: MCP server unavailable
**Mitigation**:
```python
async def search_files(query: str):
    if settings.ENABLE_MCP_FILE_SEARCH:
        try:
            return await mcp_file_search(query)
        except MCPConnectionError:
            logger.warning("MCP file server unavailable, using direct search")

    return await direct_file_search(query)
```

### 3. Performance Monitoring
**Risk**: Unacceptable latency
**Mitigation**:
- Instrument all MCP calls with timing
- Set timeout limits (5 seconds max)
- Monitor success/failure rates
- Circuit breaker pattern for repeated failures

### 4. Development Isolation
**Risk**: Breaking existing development workflow
**Mitigation**:
- Optional dependency: MCP SDK not required for basic development
- Docker container for MCP server (isolated from host)
- Clear documentation for enabling/disabling MCP features

## Skeleton Code Implementation

### services/mcp/client.py
```python
import asyncio
from typing import Optional, List
from mcp.client import MCPClient
from mcp.types import Resource, Tool

class PiperMCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.client: Optional[MCPClient] = None
        self.connected = False

    async def connect(self) -> bool:
        """Connect to MCP server with timeout."""
        try:
            self.client = MCPClient(self.server_url)
            await asyncio.wait_for(self.client.connect(), timeout=5.0)
            self.connected = True
            return True
        except Exception as e:
            logger.error(f"MCP connection failed: {e}")
            return False

    async def list_resources(self) -> List[Resource]:
        """List available resources."""
        if not self.connected:
            return []
        return await self.client.list_resources()

    async def get_resource(self, uri: str) -> Optional[dict]:
        """Get resource content."""
        if not self.connected:
            return None
        return await self.client.get_resource(uri)
```

### services/mcp/handlers.py
```python
from typing import List, Optional
from .client import PiperMCPClient
from ..shared_types import FileInfo

class MCPFileHandler:
    def __init__(self, client: PiperMCPClient):
        self.client = client

    async def search_files(self, query: str) -> List[FileInfo]:
        """Search files using MCP server."""
        try:
            resources = await self.client.list_resources()
            matching_files = []

            for resource in resources:
                if query.lower() in resource.name.lower():
                    content = await self.client.get_resource(resource.uri)
                    file_info = FileInfo(
                        name=resource.name,
                        path=resource.uri,
                        size=content.get('size', 0),
                        content_preview=content.get('content', '')[:200]
                    )
                    matching_files.append(file_info)

            return matching_files
        except Exception as e:
            logger.error(f"MCP file search failed: {e}")
            return []
```

### services/mcp/resources.py
```python
from typing import Optional, List
from .handlers import MCPFileHandler
from .client import PiperMCPClient

class MCPResourceManager:
    def __init__(self):
        self.client = PiperMCPClient("stdio://./scripts/mcp_file_server.py")
        self.handler = MCPFileHandler(self.client)
        self.initialized = False

    async def initialize(self):
        """Initialize MCP connection."""
        if not self.initialized:
            self.initialized = await self.client.connect()
        return self.initialized

    async def enhanced_file_search(self, query: str) -> List[FileInfo]:
        """Enhanced file search using MCP."""
        if not await self.initialize():
            return []
        return await self.handler.search_files(query)
```

## Integration Points

### File Search Enhancement
```python
# In services/queries/file_queries.py
async def search_files(query: str, use_mcp: bool = False) -> List[FileInfo]:
    """Search files with optional MCP enhancement."""

    # Standard file search
    results = await direct_file_search(query)

    # MCP enhancement (if enabled)
    if use_mcp and settings.ENABLE_MCP_FILE_SEARCH:
        mcp_manager = MCPResourceManager()
        mcp_results = await mcp_manager.enhanced_file_search(query)
        results.extend(mcp_results)

    return results
```

## Next Steps After POC

### If Successful
1. **Expand to GitHub MCP server**: Replace direct GitHub API calls
2. **Add external documentation**: Connect to external knowledge sources
3. **Implement advanced features**: Subscriptions, prompts, sampling

### If Unsuccessful
1. **Document lessons learned**: Performance, complexity, or reliability issues
2. **Revert to direct integrations**: Continue with existing patterns
3. **Reassess MCP adoption**: Consider future evaluation when protocol matures

## Success Metrics

- **Connection Success Rate**: >95% successful connections
- **Search Performance**: <500ms additional latency
- **Error Recovery**: Graceful fallback in <100ms
- **User Experience**: Improved search relevance (subjective evaluation)

---
*This POC plan provides a concrete, low-risk path to validate MCP value while maintaining system stability and developer productivity.*
