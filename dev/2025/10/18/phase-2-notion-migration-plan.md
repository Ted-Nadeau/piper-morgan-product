# Phase 2 Planning: Notion MCP Migration (Server → Tool-Based)

**Date**: October 18, 2025, 7:00 AM
**Lead Developer**: Claude Sonnet 4.5
**Task**: CORE-MCP-MIGRATION #198 - Phase 2
**Estimated Duration**: 3-4 hours

---

## Phase 1 Success - Pattern Established ✅

**What We Learned from Calendar & GitHub**:

### Calendar Pattern (Tool-Based MCP)
- **Structure**: Direct MCP adapter (GoogleCalendarMCPAdapter)
- **Configuration**: YAML from PIPER.user.md
- **Integration**: Service injection via config service
- **Feature Flag**: USE_SPATIAL_CALENDAR
- **Result**: Clean, simple, 100% functional

### GitHub Pattern (Delegated MCP)
- **Structure**: MCP adapter primary + spatial fallback
- **Configuration**: Already had PIPER.user.md support
- **Integration**: Router delegates to MCP first
- **Feature Flag**: USE_MCP_GITHUB
- **Result**: ADR-038 compliant, production-ready

### Key Success Factors
1. ✅ Service injection pattern
2. ✅ Feature flags for control
3. ✅ Graceful fallback strategies
4. ✅ Comprehensive test coverage
5. ✅ Configuration from PIPER.user.md

---

## Phase 2 Objective

**Current State**: Notion uses server-based MCP (60% complete per Phase -1)
**Target State**: Notion uses tool-based MCP (like Calendar/GitHub)
**Migration**: Convert from server architecture to tool architecture

### Why This Migration?

**From ADR-037** (our decision from yesterday):
- Tool-based MCP is our canonical pattern
- Server-based adds unnecessary complexity
- Calendar and GitHub prove tool-based works
- Consistency across all integrations

---

## What We Know About Notion

**From Phase -1 Discovery**:
- Location: `services/mcp/` (server-based structure)
- Status: 60% complete (architectural incomplete)
- Implementation: Server-based MCP with protocol handlers
- Problem: More complex than needed

**Questions We Need Answered**:
1. What Notion operations are implemented?
2. What's the current server structure?
3. What configuration exists?
4. What tests exist?
5. What's actually working vs incomplete?

---

## Phase 2 Strategy

### Step 0: Investigation (Code - 30 minutes)

**Objective**: Understand current Notion implementation

**Tasks**:
1. Analyze existing Notion server structure
2. Identify implemented operations
3. Review configuration approach
4. Check test coverage
5. Determine what's working vs broken
6. Identify migration complexity

**Deliverable**: Notion investigation report with migration plan

---

### Step 1: Create Tool-Based Adapter (Code - 1.5 hours)

**Objective**: Build new NotionMCPAdapter following Calendar pattern

**Pattern to Follow**:
```python
class NotionMCPAdapter(BaseSpatialAdapter):
    """Tool-based MCP adapter for Notion following Calendar pattern"""

    def __init__(self, config_service: Optional[NotionConfigService] = None):
        super().__init__("notion_mcp")
        self.config_service = config_service or NotionConfigService()
        # Initialize MCP consumer core
        # Load configuration
        # Setup Notion client

    async def get_database(self, database_id: str) -> Dict[str, Any]:
        """Get Notion database"""
        # Implement operation

    async def query_database(self, database_id: str, **kwargs) -> List[Dict]:
        """Query Notion database"""
        # Implement operation

    # ... other Notion operations
```

**Tasks**:
1. Create `services/mcp/consumer/notion_adapter.py`
2. Implement NotionMCPAdapter class
3. Add key Notion operations (databases, pages, blocks)
4. Implement spatial context extraction
5. Add circuit breaker pattern
6. Follow Calendar's structure exactly

---

### Step 2: Configuration Service (Code - 30 minutes)

**Objective**: Ensure NotionConfigService reads from PIPER.user.md

**Pattern to Follow** (from Calendar):
```python
class NotionConfigService:
    def _load_from_user_config(self) -> Dict[str, Any]:
        """Load Notion config from PIPER.user.md"""
        # Parse YAML from markdown
        # Extract notion: section
        # Return config dict

    def _load_config(self) -> NotionConfig:
        """Load with priority: env > user config > defaults"""
        user_config = self._load_from_user_config()
        return NotionConfig(
            token=os.getenv("NOTION_TOKEN", user_config.get("token")),
            # ... other config
        )
```

**Tasks**:
1. Check if NotionConfigService exists
2. Add PIPER.user.md loading if missing
3. Implement priority order (env > user > defaults)
4. Add Notion section to PIPER.user.md

---

### Step 3: Integration Router (Code - 1 hour)

**Objective**: Create or update NotionIntegrationRouter

**Pattern to Follow** (from GitHub):
```python
class NotionIntegrationRouter:
    def __init__(self, config_service: Optional[NotionConfigService] = None):
        self.config_service = config_service or NotionConfigService()

        # MCP adapter (new tool-based)
        self.mcp_adapter: Optional[NotionMCPAdapter] = None
        if USE_MCP_NOTION:
            self.mcp_adapter = NotionMCPAdapter(self.config_service)

        # Legacy server fallback (if we keep it temporarily)
        self.legacy_server = None  # or initialize if needed

    async def get_database(self, database_id: str):
        """Delegate to MCP adapter with fallback"""
        if self.mcp_adapter:
            return await self.mcp_adapter.get_database(database_id)
        # fallback or error
```

**Tasks**:
1. Check if NotionIntegrationRouter exists
2. Wire NotionMCPAdapter as primary
3. Add USE_MCP_NOTION feature flag
4. Implement delegation pattern
5. Handle legacy server (deprecate or remove)

---

### Step 4: Migration & Testing (Code - 1 hour)

**Objective**: Migrate from server-based to tool-based

**Tasks**:
1. Create comprehensive test suite
   - NotionMCPAdapter tests (following Calendar pattern)
   - Integration router tests
   - Configuration tests
2. Test all Notion operations
3. Verify no regressions
4. Update documentation

**Test Pattern** (from Calendar):
```python
class TestNotionMCPAdapter:
    def test_initialization(self):
        """Test adapter initializes correctly"""

    @pytest.mark.asyncio
    async def test_get_database(self):
        """Test database retrieval"""

    # ... other operation tests

class TestNotionConfigLoading:
    def test_loads_from_piper_user_md(self):
        """Test config loads from PIPER.user.md"""

    def test_env_vars_override(self):
        """Test environment variables override"""
```

---

### Step 5: Deprecate Server-Based (Code - 30 minutes)

**Objective**: Remove or deprecate old server-based implementation

**Tasks**:
1. Mark server-based code as deprecated
2. Remove server imports from router
3. Update feature flags (USE_MCP_NOTION=true by default)
4. Clean up unused server code
5. Update documentation

**Strategy**:
- If server code is broken: Delete immediately
- If server code works: Feature flag migration, then delete
- Follow Issue #109 pattern if gradual deprecation needed

---

## Phase 2 Success Criteria

Notion migration is **100% complete** when:

- [ ] NotionMCPAdapter exists (tool-based, following Calendar pattern)
- [ ] NotionConfigService reads from PIPER.user.md
- [ ] NotionIntegrationRouter wires MCP adapter as primary
- [ ] USE_MCP_NOTION feature flag exists (defaults true)
- [ ] All Notion operations functional via MCP adapter
- [ ] Comprehensive test suite (15+ tests)
- [ ] All tests passing
- [ ] Server-based code deprecated or removed
- [ ] Documentation updated
- [ ] Notion section added to PIPER.user.md

---

## Time Estimates

**Total**: 3-4 hours (as Chief Architect estimated)

- **Step 0**: Investigation - 30 min
- **Step 1**: Tool-based adapter - 1.5 hours
- **Step 2**: Configuration - 30 min
- **Step 3**: Integration router - 1 hour
- **Step 4**: Testing - 1 hour
- **Step 5**: Deprecation - 30 min

**Buffer**: 30 min for unexpected issues

---

## Key Differences from Phase 1

**Phase 1** (Calendar/GitHub): Completion work
- Calendar: Added missing config loading
- GitHub: Wired existing MCP adapter

**Phase 2** (Notion): Migration work
- More complex: Converting architecture
- Need to extract working operations from server
- May need to rebuild some operations
- Deprecation required

**Risk Level**: Medium (migration always riskier than completion)

---

## Pattern Reusability

**From Calendar** (100% complete):
- Tool-based MCP adapter structure
- Configuration loading pattern
- Service injection approach
- Test suite structure

**From GitHub** (100% complete):
- Delegation pattern (if we keep server temporarily)
- Feature flag approach
- Router wiring
- Fallback strategies

**Apply Both**:
- Start with Calendar's clean tool-based pattern
- Add GitHub's delegation if needed for migration
- Aim for Calendar's simplicity as end state

---

## Risk Factors

**Low Risk**:
- Pattern is proven (Calendar & GitHub)
- Clear examples to follow
- Good test coverage expected

**Medium Risk**:
- Migration complexity (not just wiring)
- Current server implementation unclear
- May have working features we need to preserve
- Notion API may have quirks

**High Risk** (unlikely):
- Server-based was chosen for good reason we don't know
- Operations too complex for tool-based
- Major architectural blocker

**Mitigation**:
- Start with investigation (Step 0)
- Identify any architectural concerns early
- Escalate to Chief Architect if needed

---

## Questions for Investigation (Step 0)

1. **What Notion operations exist in server-based code?**
2. **Are they working or broken?**
3. **Why was server-based chosen originally?**
4. **What's the complexity of Notion API integration?**
5. **Do we have Notion test credentials?**
6. **Are there any Notion-specific challenges?**
7. **Can we test Notion operations easily?**

---

## Next Steps

**Immediate** (7:00 AM):
1. Create Step 0 investigation prompt for Code
2. Deploy Code to analyze Notion implementation
3. Wait for investigation report (~30 min)
4. Review findings and adjust plan
5. Proceed with migration steps

**Expected Completion**: ~11:00 AM (4 hours from now)

---

## Success Pattern

**Follow the Inchworm**:
- ✅ Phase -1: Discovery (yesterday)
- ✅ Phase 0.5: ADR (yesterday)
- ✅ Phase 1: Calendar & GitHub (yesterday)
- 🔄 Phase 2: Notion (today)
- 📋 Phase 3: Slack (later)
- 📋 Phase 4: Verification (later)

**Stay Disciplined**:
- One phase at a time
- Evidence before proceeding
- Test everything
- Document thoroughly

---

**Ready to begin Phase 2 with Notion investigation!** 🎯
