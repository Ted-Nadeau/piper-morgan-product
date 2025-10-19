# Gameplan: CORE-KNOW - Knowledge Graph Activation

**Sprint**: A3 (continuation)
**Issues**: #99 (CORE-KNOW) and #230 (CORE-KNOW-BOUNDARY)
**Duration**: 3-4 hours estimated
**Context**: Knowledge Graph exists (PM-040 complete), needs activation

---

## Strategic Approach

Like Ethics, the Knowledge Graph is likely 75-95% built but not connected. We'll follow the proven pattern:
1. Discover what exists
2. Connect to conversation flow
3. Add boundaries for safety
4. Test and activate

## Issue Sequencing

**Do #99 FIRST** (Connect Knowledge Graph) - Get it working
**Then #230** (Boundaries) - Make it safe

This follows our pattern: functionality first, safety second (but both required before production).

---

## Issue #99: CORE-KNOW - Connect Knowledge Graph

### Phase -1: Discovery (30 minutes)

**What we're looking for**:
```python
# Using Serena to investigate current state
mcp__serena__find_symbol(
    name_regex="KnowledgeGraph.*",
    scope="services"
)

# Check for existing integrations
mcp__serena__search_project(
    query="knowledge graph conversation context",
    file_pattern="*.py"
)

# Look for TODO markers
mcp__serena__search_project(
    query="TODO knowledge",
    file_pattern="services/**/*.py"
)
```

**Expected findings** (based on pattern):
- KnowledgeGraphService exists and works
- PostgreSQL backend operational
- Graph queries functional
- Just not connected to conversation flow

### Phase 1: Integration Architecture (30 minutes)

**Decision Point**: Where does KG integration belong?

**Option A: ConversationHandler** (if it exists)
```python
class ConversationHandler:
    def __init__(self):
        self.kg_service = KnowledgeGraphService()

    async def enhance_context(self, message, base_context):
        graph_context = await self.kg_service.query_context(message)
        return merge_contexts(base_context, graph_context)
```

**Option B: IntentService** (universal entry point)
```python
class IntentService:
    async def process_intent(self, message, session_id):
        # After ethics, before classification
        graph_context = await self.kg_service.get_relevant_context(message)
        enhanced_intent = self.enhance_with_graph(intent, graph_context)
```

**Option C: OrchestrationEngine** (workflow level)
```python
class OrchestrationEngine:
    async def execute(self, intent, context):
        # Enhance context with knowledge graph
        kg_context = await self.kg_service.query_for_intent(intent)
        context.update(kg_context)
```

**Recommendation**: Will decide based on Phase -1 findings, but likely Option B (IntentService) for consistency with Ethics placement.

### Phase 2: Implementation (1-2 hours)

**Step 2.1: Create Integration Layer**
```python
# services/knowledge/conversation_integration.py
class ConversationKnowledgeGraphIntegration:
    def __init__(self, kg_service: KnowledgeGraphService):
        self.kg_service = kg_service
        self.cache = {}  # Simple caching

    async def get_conversation_context(self, query: str, user_context: Dict):
        """Get relevant KG context for conversation"""
        # Query for project relationships
        projects = await self.kg_service.find_related_projects(query)

        # Get recent patterns
        patterns = await self.kg_service.get_recent_patterns()

        # Build enhanced context
        return {
            "projects": projects,
            "patterns": patterns,
            "insights": await self.generate_insights(projects, patterns)
        }
```

**Step 2.2: Wire to Conversation Flow**
- Add KG integration to chosen layer (likely IntentService)
- Pass graph context through to response generation
- Ensure feature flag control: `ENABLE_KNOWLEDGE_GRAPH`

**Step 2.3: Performance Optimization**
- Add caching for frequently accessed nodes
- Implement timeout (100ms target)
- Graceful degradation if KG slow/unavailable

### Phase 3: Testing & Activation (1 hour)

**Test Cases**:
```python
async def test_knowledge_graph_enhancement():
    """Test that KG enhances conversation context"""

    # Test canonical query WITHOUT KG
    response_without = await process_without_kg("What's the status of the website project?")
    assert "need more information" in response_without.lower()

    # Test WITH KG
    response_with = await process_with_kg("What's the status of the website project?")
    assert "SITE-001" in response_with  # Should identify specific project
    assert "3 of 5 phases" in response_with  # Should have real status
```

**Performance Tests**:
- Verify <100ms additional latency
- Test cache effectiveness
- Validate graceful degradation

**Feature Flag Activation**:
```python
# .env
ENABLE_KNOWLEDGE_GRAPH=true
KNOWLEDGE_GRAPH_TIMEOUT_MS=100
KNOWLEDGE_GRAPH_CACHE_TTL=300
```

---

## Issue #230: CORE-KNOW-BOUNDARY - Add Safety Rails

### Phase 4: Boundary Implementation (1 hour)

**Step 4.1: Define Boundaries**
```python
class GraphBoundaries:
    MAX_DEPTH = 5          # Traversal depth limit
    MAX_NODES = 1000       # Node visit limit
    MAX_TIME_MS = 5000     # Query timeout
    MAX_MEMORY_MB = 100    # Memory limit
```

**Step 4.2: Create Enforcer**
```python
class BoundaryEnforcer:
    def __init__(self, boundaries: GraphBoundaries):
        self.boundaries = boundaries
        self.visited_count = 0
        self.start_time = None

    async def check_depth(self, current_depth: int) -> bool:
        return current_depth < self.boundaries.MAX_DEPTH

    async def check_node_count(self) -> bool:
        self.visited_count += 1
        return self.visited_count < self.boundaries.MAX_NODES

    async def check_timeout(self) -> bool:
        elapsed = (time.time() - self.start_time) * 1000
        return elapsed < self.boundaries.MAX_TIME_MS
```

**Step 4.3: Integrate with KG Operations**
- Wrap all graph traversals with boundary checks
- Return partial results when limits hit
- Log boundary violations for monitoring

### Phase 5: Boundary Testing (30 minutes)

**Test boundary enforcement**:
- Create deep graph, verify depth limit
- Create wide graph, verify node limit
- Create slow operation, verify timeout
- Verify partial results returned correctly

---

## Success Criteria

### Issue #99 Complete When:
- [ ] Knowledge Graph connected to conversation flow
- [ ] Canonical queries show enhanced context
- [ ] Performance within 100ms target
- [ ] Feature flag control working
- [ ] Tests passing (enhancement + performance)

### Issue #230 Complete When:
- [ ] All boundaries enforced
- [ ] Partial results on limit
- [ ] No resource exhaustion possible
- [ ] Boundary tests passing
- [ ] Configuration working

---

## Time Estimate

**Issue #99** (CORE-KNOW):
- Phase -1: Discovery (30 min)
- Phase 1: Architecture (30 min)
- Phase 2: Implementation (1-2 hours)
- Phase 3: Testing (1 hour)
- **Subtotal**: 3-4 hours

**Issue #230** (CORE-KNOW-BOUNDARY):
- Phase 4: Boundaries (1 hour)
- Phase 5: Testing (30 min)
- **Subtotal**: 1.5 hours

**Total**: 4.5-5.5 hours

Given current velocity (70% under estimates), likely 2-3 hours actual.

---

## Risk Assessment

### Low Risk
- Knowledge Graph already exists (PM-040)
- Pattern established (Ethics same approach)
- Clear integration points
- Simple boundary logic

### Medium Risk
- PostgreSQL performance under load
- Complex graph queries timing out
- Cache invalidation complexity

### Mitigation
- Start with simple queries
- Conservative boundaries initially
- Monitor performance closely
- Feature flag for instant disable

---

## Next Steps

1. **Start Phase -1** (Discovery) immediately
2. **Report findings** to determine architecture
3. **Implement connection** (Phase 2)
4. **Add boundaries** (Phase 4)
5. **Activate with monitoring**

---

**This should complete Sprint A3 today!**

Given the efficiency on #198 (3.5h) and #197 (2.3h), we have runway to complete both #99 and #230 today, finishing Sprint A3 at 100%.

---

*Ready to activate Piper Morgan's memory!*
