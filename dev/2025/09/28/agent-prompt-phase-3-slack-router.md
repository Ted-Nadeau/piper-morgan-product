# Claude Code Prompt: Phase 3 - Slack Integration Router Implementation

## Mission: Implement SlackIntegrationRouter

**Context**: Phase 1 and 2 validated the router pattern for MCP adapters. Slack is fundamentally different - it uses direct spatial pattern (no MCP adapter) with SlackSpatialAdapter + SlackClient components. This requires a different delegation approach while maintaining the same router interface pattern.

**Objective**: Create SlackIntegrationRouter that delegates to Slack's spatial system or basic client, following the established pattern but adapting for Slack's unique architecture.

## Phase 0 Key Findings Reference

From your investigation:
- **Pattern**: Direct spatial (NOT MCP) - 6 spatial implementation files
- **Components**: SlackSpatialAdapter + SlackClient (not single adapter)
- **Spatial Files**: spatial_adapter.py, spatial_agent.py, spatial_intent_classifier.py, spatial_mapper.py, spatial_memory.py, spatial_types.py
- **Client**: SlackClient with 12+ async methods (send_message, get_channel_info, list_channels, etc.)
- **Integration**: Webhook-based with event-driven architecture

## Key Architectural Difference

**Calendar/Notion Pattern** (MCP):
```python
# Single adapter to delegate to
self.spatial_calendar = GoogleCalendarMCPAdapter()
```

**Slack Pattern** (Direct Spatial):
```python
# Multiple components to coordinate
self.spatial_adapter = SlackSpatialAdapter()
self.slack_client = SlackClient()
# Webhook router handles event integration
```

## Implementation Tasks

### Task 1: Analyze Slack Components

Before implementing, understand what to expose:

```bash
# Check SlackClient methods
grep "async def " services/integrations/slack/slack_client.py | grep -v "__" | head -20

# Check SlackSpatialAdapter interface
grep "def " services/integrations/slack/spatial_adapter.py | grep -v "__" | head -20

# Check webhook router usage
grep -A 5 "SlackSpatialAdapter\|SlackClient" services/integrations/slack/webhook_router.py | head -30
```

**Document**: Which methods should router expose? SlackClient methods? Spatial methods? Both?

### Task 2: Design Router Interface

Based on analysis, determine router approach:

**Option A - Expose Client Methods** (simpler):
Router primarily delegates to SlackClient, with spatial intelligence as internal detail

**Option B - Expose Spatial + Client** (comprehensive):
Router exposes both SlackClient methods and spatial adapter methods

**Recommendation**: Start with Option A (client methods) as this matches how services currently use Slack

### Task 3: Implement Router Class

```python
# services/integrations/slack/slack_integration_router.py
"""
SlackIntegrationRouter - Feature flag controlled access to Slack integrations

Provides unified interface for Slack operations with support for:
- Spatial intelligence (SlackSpatialAdapter + SlackClient)
- Legacy basic Slack operations (basic SlackClient only)
- Feature flag control via USE_SPATIAL_SLACK
"""

import os
import warnings
from typing import Optional, List, Dict, Any, Tuple

class SlackIntegrationRouter:
    """
    Router for Slack integration with spatial/legacy delegation.

    Unlike Calendar/Notion, Slack uses direct spatial pattern (not MCP).
    Coordinates SlackSpatialAdapter + SlackClient for spatial mode.
    """

    def __init__(self, config_service=None):
        """Initialize router with feature flag checking"""
        # Check feature flags
        self.use_spatial = os.getenv('USE_SPATIAL_SLACK', 'true').lower() == 'true'
        self.allow_legacy = os.getenv('ALLOW_LEGACY_SLACK', 'false').lower() == 'true'

        # Initialize spatial integration (adapter + client)
        self.spatial_slack = None
        self.slack_client_spatial = None

        if self.use_spatial:
            try:
                from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
                from services.integrations.slack.slack_client import SlackClient

                self.spatial_slack = SlackSpatialAdapter()
                self.slack_client_spatial = SlackClient(config_service)
            except ImportError as e:
                warnings.warn(f"Spatial Slack unavailable: {e}")

        # Initialize legacy integration (basic client only)
        self.slack_client_legacy = None

        if self.allow_legacy:
            try:
                from services.integrations.slack.slack_client import SlackClient
                self.slack_client_legacy = SlackClient(config_service)
            except ImportError as e:
                warnings.warn(f"Legacy Slack unavailable: {e}")

    def _get_preferred_integration(self, operation: str) -> Tuple[Optional[Any], bool]:
        """
        Get preferred integration based on feature flags.

        For Slack, returns the client (spatial or legacy) that should be used.
        Spatial mode uses spatial_slack for intelligence + slack_client_spatial for operations.
        """
        # Try spatial first if enabled
        if self.use_spatial and self.slack_client_spatial:
            # Note: spatial_slack provides intelligence, client does operations
            return self.slack_client_spatial, False

        # Fall back to legacy if allowed
        elif self.allow_legacy and self.slack_client_legacy:
            return self.slack_client_legacy, True

        # No integration available
        else:
            return None, False

    def _warn_deprecation_if_needed(self, operation: str, is_legacy: bool):
        """Warn about legacy usage for future migration"""
        if is_legacy:
            warnings.warn(
                f"Using legacy Slack for {operation}. "
                "Consider enabling USE_SPATIAL_SLACK=true for spatial intelligence.",
                DeprecationWarning,
                stacklevel=3
            )

    # Delegate SlackClient methods (primary interface)

    async def send_message(self, channel: str, text: str,
                          thread_ts: Optional[str] = None) -> Dict[str, Any]:
        """Send message to Slack channel"""
        client, is_legacy = self._get_preferred_integration("send_message")

        if client:
            self._warn_deprecation_if_needed("send_message", is_legacy)
            return await client.send_message(channel, text, thread_ts)
        else:
            raise RuntimeError("No Slack integration available")

    async def get_channel_info(self, channel: str) -> Dict[str, Any]:
        """Get channel information"""
        client, is_legacy = self._get_preferred_integration("get_channel_info")

        if client:
            self._warn_deprecation_if_needed("get_channel_info", is_legacy)
            return await client.get_channel_info(channel)
        else:
            raise RuntimeError("No Slack integration available")

    async def list_channels(self) -> List[Dict[str, Any]]:
        """List all channels"""
        client, is_legacy = self._get_preferred_integration("list_channels")

        if client:
            self._warn_deprecation_if_needed("list_channels", is_legacy)
            return await client.list_channels()
        else:
            raise RuntimeError("No Slack integration available")

    async def get_user_info(self, user: str) -> Dict[str, Any]:
        """Get user information"""
        client, is_legacy = self._get_preferred_integration("get_user_info")

        if client:
            self._warn_deprecation_if_needed("get_user_info", is_legacy)
            return await client.get_user_info(user)
        else:
            raise RuntimeError("No Slack integration available")

    async def list_users(self) -> List[Dict[str, Any]]:
        """List all users"""
        client, is_legacy = self._get_preferred_integration("list_users")

        if client:
            self._warn_deprecation_if_needed("list_users", is_legacy)
            return await client.list_users()
        else:
            raise RuntimeError("No Slack integration available")

    async def get_conversation_history(self, channel: str,
                                      limit: int = 100) -> List[Dict[str, Any]]:
        """Get conversation history"""
        client, is_legacy = self._get_preferred_integration("get_conversation_history")

        if client:
            self._warn_deprecation_if_needed("get_conversation_history", is_legacy)
            return await client.get_conversation_history(channel, limit)
        else:
            raise RuntimeError("No Slack integration available")

    async def get_thread_replies(self, channel: str,
                                 thread_ts: str) -> List[Dict[str, Any]]:
        """Get replies in a thread"""
        client, is_legacy = self._get_preferred_integration("get_thread_replies")

        if client:
            self._warn_deprecation_if_needed("get_thread_replies", is_legacy)
            return await client.get_thread_replies(channel, thread_ts)
        else:
            raise RuntimeError("No Slack integration available")

    async def add_reaction(self, channel: str, timestamp: str,
                          reaction: str) -> Dict[str, Any]:
        """Add reaction to message"""
        client, is_legacy = self._get_preferred_integration("add_reaction")

        if client:
            self._warn_deprecation_if_needed("add_reaction", is_legacy)
            return await client.add_reaction(channel, timestamp, reaction)
        else:
            raise RuntimeError("No Slack integration available")

    async def test_auth(self) -> Dict[str, Any]:
        """Test authentication"""
        client, is_legacy = self._get_preferred_integration("test_auth")

        if client:
            self._warn_deprecation_if_needed("test_auth", is_legacy)
            return await client.test_auth()
        else:
            raise RuntimeError("No Slack integration available")

    # Spatial intelligence access (if needed)
    def get_spatial_adapter(self) -> Optional[Any]:
        """Get spatial adapter for advanced spatial operations"""
        if self.use_spatial:
            return self.spatial_slack
        return None
```

### Task 4: Add Feature Flag Methods

```python
# In services/infrastructure/config/feature_flags.py

@staticmethod
def should_use_spatial_slack() -> bool:
    """Check if spatial Slack integration should be used"""
    return FeatureFlags._get_boolean_flag("USE_SPATIAL_SLACK", True)

@staticmethod
def is_legacy_slack_allowed() -> bool:
    """Check if legacy Slack integration is allowed"""
    return FeatureFlags._get_boolean_flag("ALLOW_LEGACY_SLACK", False)
```

### Task 5: Verify Router Implementation

```python
# Test router initialization
python -c "
import asyncio
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

async def test_router():
    router = SlackIntegrationRouter()
    print(f'✅ Router initialized')
    print(f'   Use spatial: {router.use_spatial}')
    print(f'   Spatial adapter: {router.spatial_slack is not None}')
    print(f'   Spatial client: {router.slack_client_spatial is not None}')

    # Test method availability
    methods = ['send_message', 'get_channel_info', 'list_channels',
               'get_user_info', 'list_users', 'get_conversation_history',
               'get_thread_replies', 'add_reaction', 'test_auth']

    print(f'\n   Methods available: {len(methods)}')
    for method in methods:
        has_method = hasattr(router, method) and callable(getattr(router, method))
        if not has_method:
            print(f'   ❌ Missing: {method}')

asyncio.run(test_router())
"
```

### Task 6: Test Feature Flag Control

```bash
# Test spatial mode
USE_SPATIAL_SLACK=true python -c "
import asyncio
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

async def test():
    router = SlackIntegrationRouter()
    client, is_legacy = router._get_preferred_integration('test')
    print(f'Spatial mode - Client: {type(client).__name__ if client else None}, Legacy: {is_legacy}')

asyncio.run(test())
"

# Test legacy mode
USE_SPATIAL_SLACK=false ALLOW_LEGACY_SLACK=true python -c "
import asyncio
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

async def test():
    router = SlackIntegrationRouter()
    client, is_legacy = router._get_preferred_integration('test')
    print(f'Legacy mode - Client: {type(client).__name__ if client else None}, Legacy: {is_legacy}')

asyncio.run(test())
"
```

## Evidence Requirements

```markdown
# Phase 3: Slack Router Implementation Report

## Architectural Difference Noted
Unlike Calendar/Notion MCP pattern, Slack uses:
- Direct SlackSpatialAdapter (not MCP adapter)
- SlackClient for operations
- Webhook router for event handling

## Router Implementation
**Location**: services/integrations/slack/slack_integration_router.py
**Size**: [line count]
**Methods**: [count] SlackClient methods delegated
**Pattern**: Adapted router pattern for non-MCP spatial architecture

## Methods Implemented: X/9 minimum
[List: send_message, get_channel_info, list_channels, get_user_info,
 list_users, get_conversation_history, get_thread_replies, add_reaction, test_auth]

## Testing Results
[Initialization, method availability, feature flags, spatial/legacy modes]

## Pattern Adaptation
- Same _get_preferred_integration logic
- Same _warn_deprecation_if_needed
- Same RuntimeError handling
- Different: Coordinates adapter + client instead of single MCP adapter

## Services Ready for Migration
[List from Phase 0: webhook_router.py uses SlackSpatialAdapter + SlackClient]

## Ready for Phase 4: [YES/NO]
```

## Update Requirements

1. **Update Session Log**: Add Phase 3 completion
2. **Update GitHub Issue #199**: Add Slack router completion
3. **Tag Cursor**: Request verification

## Critical Success Factors

- **Pattern Adaptation**: Follow established pattern while adapting for Slack's architecture
- **Spatial Intelligence**: Spatial adapter available through spatial mode
- **Client Methods**: All SlackClient methods accessible through router
- **Feature Flag Control**: Must actually switch between spatial and legacy

## STOP Conditions

- If SlackClient methods don't work through router
- If spatial adapter can't be accessed when needed
- If webhook integration pattern breaks

---

**Your Mission**: Implement SlackIntegrationRouter adapting the pattern for non-MCP spatial architecture while maintaining consistency with Calendar/Notion routers.

**Quality Standard**: Pattern consistency with necessary architectural adaptations clearly documented.
