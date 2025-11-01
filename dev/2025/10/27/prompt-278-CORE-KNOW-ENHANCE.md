# Claude Code Prompt: CORE-KNOW-ENHANCE - Optimize Knowledge Graph for Relationship-Based Reasoning

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

**Context from Sprint A8 Haiku Testing**:
- ✅ Issue #274: Sonnet in ~10 min (PM forgot model flag)
- ✅ Issue #268: Haiku in 19 min - simple integration
- ✅ Issue #269: Haiku in 6 min - medium complexity (architectural discovery!)
- ✅ Issue #271: Haiku in 15 min - high complexity (Phase -1 caught errors!)

This is your FOURTH real Haiku test. After crushing 3 issues including "high complexity," we're testing if Haiku can handle **ARCHITECTURAL work** - the ultimate challenge.

**Complexity Level**: ARCHITECTURAL - This is design + implementation work on a core system. If Haiku completes this well, it can handle ~90% of our work!

---

## Essential Context
Read these briefing documents first in docs/briefing/:
- BRIEFING-PROJECT.md - What Piper Morgan is
- BRIEFING-CURRENT-STATE.md - Current sprint (A8 Alpha Preparation)
- BRIEFING-ESSENTIAL-AGENT.md - Your role requirements
- BRIEFING-METHODOLOGY.md - Inchworm Protocol

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

**DO NOT**:
- ❌ Read old context files to self-direct
- ❌ Assume you should continue
- ❌ Start working on next task without authorization

**This is critical**. After compaction, get your bearings first.

---

## HAIKU 4.5 TEST PROTOCOL

**Model**: Use Haiku 4.5 for this task
```bash
claude --model haiku
```

**Why Continue with Haiku**: After exceptional performance on 3 issues (including Phase -1 architectural discovery in #271), we're testing if Haiku can handle architectural design work.

**What We've Learned**:
- Issue #268: Beat estimate (19 min on simple)
- Issue #269: Crushed estimate by 80%+ (6 min on medium, discovered system divergence!)
- Issue #271: Beat estimate by 67%+ (15 min on high, perfect Phase -1 execution)
- Haiku discovering architectural issues independently
- Quality consistently matches Sonnet

**This Task Is Different**:
- Not just integration - architectural enhancement
- Requires understanding graph theory concepts
- Design decisions about edge types and traversal
- Performance optimization considerations
- This is the real test of Haiku's limits!

**⚠️ STOP CONDITIONS** (watch carefully, this is harder):
- ⚠️ 2 failures on same subtask
- ⚠️ Breaks existing functionality
- ⚠️ Genuinely stuck (confusion about graph design)
- ⚠️ Architectural uncertainty (unsure about approach)
- ⚠️ Performance concerns unresolved

**If STOP triggered**: Report to PM. This is ARCHITECTURAL work - if Haiku hits limits here, that's valuable data! Escalating to Sonnet is completely expected for design work.

---

## SERENA MCP USAGE (MANDATORY)

This task involves understanding existing knowledge graph system:

```bash
# Find knowledge graph implementation
find_symbol "KnowledgeGraphService"
find_symbol "KnowledgeGraph"

# Find existing edge types
grep -r "EdgeType" services/ --include="*.py"

# Find graph traversal methods
find_referencing_symbols "KnowledgeGraphService"

# Find intent classification integration
find_symbol "IntentClassifier"
```

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

**BEFORE planning implementation**, verify what exists:

### Step 1: Find Knowledge Graph System
```bash
# Locate the knowledge graph implementation
find_symbol "KnowledgeGraphService"
find_symbol "KnowledgeGraph"

# Check directory structure
ls -la services/knowledge/ 2>/dev/null || ls -la services/ | grep -i knowledge

# Find actual files
find . -name "*knowledge*" -name "*.py" | grep -v __pycache__
```

### Step 2: Understand Current Implementation
```bash
# Read current edge types
grep -r "class.*EdgeType" services/ --include="*.py"

# Find existing traversal methods
grep -r "def.*traverse\|def.*expand\|def.*query" services/knowledge* --include="*.py"

# Check current schema
grep -r "CREATE TABLE.*knowledge\|CREATE TABLE.*graph" alembic/versions/ --include="*.py"
```

### Step 3: Find Related Systems
```bash
# Intent classification integration point
find_symbol "IntentClassifier"
find_referencing_symbols "IntentClassifier"

# Check if graph is already integrated anywhere
grep -r "knowledge.*graph\|graph.*service" services/ --include="*.py"
```

### Step 4: Check Documentation
```bash
# Look for existing ADRs or docs
ls -la docs/adr/*knowledge* 2>/dev/null
grep -r "knowledge graph" docs/ --include="*.md"

# Check domain models
grep -i "knowledge" docs/domain-models.md 2>/dev/null
```

---

## 📋 REPORT YOUR FINDINGS (Before Planning)

After infrastructure verification, provide:

```
PHASE -1 DISCOVERY REPORT: CORE-KNOW-ENHANCE

1. KNOWLEDGE GRAPH ARCHITECTURE:
   - Primary class: [name and location]
   - Current edge types: [count and examples]
   - Traversal capabilities: [what exists]
   - Database schema: [structure]
   - Integration points: [where it's used]

2. CURRENT STATE ASSESSMENT:
   - Completion level: [% complete per issue description]
   - What's working: [list]
   - What's missing: [list from issue spec]
   - Integration status: [connected to intent classification?]

3. IMPLEMENTATION STRATEGY:
   - Edge type enhancement approach: [plan]
   - Graph-first retrieval design: [approach]
   - Intent classification integration: [plan]
   - Performance considerations: [concerns]

4. CONFIDENCE LEVEL:
   - Architecture understanding: [High/Medium/Low]
   - Design decisions clear: [Yes/No/Partially]
   - Ready to proceed: [Yes/No - explain]

5. DESIGN QUESTIONS:
   - [Any architectural uncertainties]
   - [Performance trade-off concerns]
   - [Integration approach questions]
```

**Decision Point**:
- HIGH confidence → Proceed with implementation
- MEDIUM/LOW confidence → Report uncertainties, ask for guidance

---

## 🎯 Task Overview (After Verification)

**Goal**: Transform knowledge graph from fact storage to relationship-based reasoning engine

**Three Main Enhancements**:
1. **Enrich Edge Types** - Add causal & temporal relationships (~1 hour)
2. **Graph-First Retrieval** - Query graph before expensive LLM calls (~1 hour)
3. **Intent Classification Integration** - Wire graph into routing (~30 min)

**Estimated Total**: 2-3 hours (but we've learned estimates may be high for Haiku!)

---

## Enhancement 1: Enrich Edge Types

### Current State (Verify)
```python
# Find what currently exists
grep -r "class.*EdgeType" services/knowledge* --include="*.py"
```

### Expected Enhancement
Add causal and temporal edge types with confidence weighting:

```python
class CausalEdgeTypes(Enum):
    BECAUSE = "because"      # X BECAUSE Y
    ENABLES = "enables"      # X ENABLES Y
    REQUIRES = "requires"    # X REQUIRES Y
    PREVENTS = "prevents"    # X PREVENTS Y
    LEADS_TO = "leads_to"   # X LEADS_TO Y

class TemporalEdgeTypes(Enum):
    BEFORE = "before"
    DURING = "during"
    AFTER = "after"
    TRIGGERS = "triggers"

class WeightedEdge:
    edge_type: str
    confidence: float = 1.0  # 0.0 to 1.0
    usage_count: int = 0     # Strengthen with use
    last_accessed: datetime = None  # For decay
```

### Implementation Tasks
- [ ] Add new edge type enums
- [ ] Update database schema for confidence weights
- [ ] Migration for existing edges
- [ ] Update edge creation methods
- [ ] Add confidence decay logic (optional)

---

## Enhancement 2: Graph-First Retrieval

### Concept
Query → Graph → Context → LLM (not Query → LLM directly)

### Implementation Pattern
```python
class GraphFirstRetrieval:
    async def get_context(
        self,
        user_query: str,
        user_id: str
    ) -> dict:
        """Use graph for context before LLM"""

        # Step 1: Semantic search (use Haiku - 90% cheaper!)
        relevant_nodes = await self.graph.semantic_search(
            query=user_query,
            user_id=user_id,
            model='claude-3-haiku',  # Cost optimization!
            max_nodes=10
        )

        # Step 2: 2-hop graph expansion
        context_graph = await self.graph.expand(
            nodes=relevant_nodes,
            max_hops=2,
            edge_types=['BECAUSE', 'ENABLES', 'REQUIRES']
        )

        # Step 3: Extract reasoning chains
        reasoning_paths = self.extract_reasoning_chains(
            context_graph
        )

        # Step 4: Now use expensive model with focused context
        return {
            'nodes': context_graph.nodes,
            'relationships': context_graph.edges,
            'reasoning': reasoning_paths,
            'tokens_saved': self.calculate_savings()
        }
```

### Implementation Tasks
- [ ] Add semantic_search method (if not exists)
- [ ] Implement graph expansion (2-hop traversal)
- [ ] Extract reasoning chains from paths
- [ ] Calculate cost savings
- [ ] Performance optimization (<300ms target)

---

## Enhancement 3: Intent Classification Integration

### Integration Point
```python
class KnowledgeAwareIntentClassifier:
    def __init__(self, knowledge_graph: KnowledgeGraphService):
        self.graph = knowledge_graph

    async def classify_with_context(
        self,
        user_input: str,
        user_id: str
    ):
        """Enhance intent classification with graph context"""

        # Get graph context FIRST
        graph_context = await self.graph.get_relevant_context(
            user_input,
            user_id
        )

        # Use context to improve classification
        intent_hints = self.extract_hints(graph_context)

        # Classify with hints
        intent = await self.classify(
            user_input,
            context_hints=intent_hints
        )

        return intent, graph_context
```

### Implementation Tasks
- [ ] Find IntentClassifier location
- [ ] Add knowledge graph parameter
- [ ] Implement context extraction
- [ ] Extract intent hints from graph
- [ ] Wire into classification flow

---

## Testing Strategy

### Test Relationship Reasoning
```python
async def test_relationship_based_reasoning():
    """Verify graph provides reasoning chains"""

    # Create relationship chain
    await graph.add_relationship(
        'user', 'prefers_mornings',
        'BECAUSE', 'highest_energy',
        confidence=0.9
    )
    await graph.add_relationship(
        'highest_energy', 'ENABLES',
        'complex_problem_solving',
        confidence=0.85
    )

    # Query should return chain
    result = await graph.query(
        "When should I tackle hard problems?"
    )

    assert 'morning' in result
    assert 'highest_energy' in result.reasoning
    assert len(result.reasoning_chain) >= 2
    assert result.confidence >= 0.7  # Combined confidence
```

### Test Cost Reduction
```python
async def test_graph_first_cost_savings():
    """Verify graph-first reduces LLM costs"""

    # Without graph (baseline)
    baseline_cost = await measure_cost(
        query_with_llm_only("What's my schedule?")
    )

    # With graph-first
    graph_cost = await measure_cost(
        query_with_graph_first("What's my schedule?")
    )

    # Should save 50%+ tokens
    assert graph_cost < baseline_cost * 0.5
```

### Test Intent Enhancement
```python
async def test_intent_classification_with_graph():
    """Verify graph improves intent classification"""

    # Add graph context
    await graph.add_fact(
        'user', 'has_pattern', 'daily_standup'
    )

    # Classify with graph
    intent = await classifier.classify_with_context(
        "time for our sync",
        user_id
    )

    assert intent.name == 'standup'
    assert intent.confidence > 0.8
    assert 'daily_standup' in intent.graph_context
```

---

## Acceptance Criteria

### Functional Requirements
- [ ] 15+ edge types (causal + temporal)
- [ ] Confidence weights on edges
- [ ] Graph-first retrieval pattern implemented
- [ ] Connected to intent classification
- [ ] 2-hop graph traversal working
- [ ] Reasoning chain extraction
- [ ] Cost reduction demonstrated (>50%)

### Performance Requirements
- [ ] Graph traversal: <50ms for 2-hop expansion
- [ ] Semantic search: <200ms (using Haiku)
- [ ] Total context gathering: <300ms
- [ ] Token reduction: >60% on retrieval queries

### Testing Requirements
- [ ] Relationship reasoning tests
- [ ] Cost savings validation
- [ ] Intent classification enhancement tests
- [ ] Performance benchmarks
- [ ] Existing functionality preserved

### Quality Requirements
- [ ] Feature flag for gradual rollout
- [ ] Fallback to direct LLM if graph fails
- [ ] Error handling for graph failures
- [ ] Monitoring for latency
- [ ] Documentation of new patterns

---

## Success Metrics

**Cost Reduction**:
- Retrieval queries: >50% token reduction
- Simple questions: >60% cost savings
- Complex reasoning: Maintained quality with 40%+ savings

**Quality**:
- Context relevance: Improved (measure via feedback)
- Response quality: Maintained or improved
- Reasoning chains: Visible in responses

**Performance**:
- Graph operations: <300ms total
- No degradation in user experience
- Alpha tester feedback positive

---

## Risk Mitigation

**Preserve Existing Functionality**:
- Keep fact-based queries working
- Don't break current integrations
- Add feature flags
- Monitor latency closely

**Performance Safeguards**:
- Timeout on graph operations (500ms max)
- Fallback to direct LLM
- Cache hot paths
- Async operations where possible

**Quality Safeguards**:
- A/B test graph-first vs direct LLM
- Monitor accuracy metrics
- Easy rollback mechanism
- Gradual rollout to alpha testers

---

## Architectural Considerations

### Graph Design
- **Confidence decay**: Should old edges lose confidence?
- **Usage reinforcement**: Strengthen frequently used paths?
- **Pruning strategy**: Remove low-confidence edges?

### Performance
- **Caching**: Cache hot paths? Which ones?
- **Indexing**: Database indexes for traversal?
- **Parallelization**: Concurrent graph operations?

### Integration
- **Existing code**: How much to refactor?
- **Breaking changes**: Can we avoid them?
- **Feature flags**: How granular?

**Report these decisions** in your implementation plan!

---

## 🛑 STOP CONDITIONS - Watch Carefully

This is ARCHITECTURAL work - different from previous integration tasks:

**Trigger STOP if**:
- Unsure about graph theory concepts (2-hop traversal, reasoning chains)
- Unclear about performance trade-offs
- Architectural design decisions feel uncertain
- Breaking existing functionality
- 2 failures on same design decision
- Genuinely confused about approach

**Remember**: Escalating to Sonnet for architectural work is EXPECTED and GOOD! This is the hardest test yet.

---

## Expected Workflow

### Phase -1: Discovery & Verification (30-45 min)
1. Find knowledge graph system
2. Understand current edge types
3. Map integration points
4. Report findings and confidence level

### Phase 1: Edge Type Enhancement (30-60 min)
1. Add causal/temporal enums
2. Update database schema
3. Migration for existing data
4. Test edge creation

### Phase 2: Graph-First Retrieval (30-60 min)
1. Implement semantic search (if needed)
2. Add graph expansion (2-hop)
3. Extract reasoning chains
4. Measure cost savings

### Phase 3: Intent Integration (20-40 min)
1. Find IntentClassifier
2. Add graph parameter
3. Extract hints from graph
4. Wire into flow

### Phase 4: Testing & Validation (30-45 min)
1. Relationship reasoning tests
2. Cost reduction tests
3. Intent enhancement tests
4. Performance benchmarks

**Total Estimate**: 2-3 hours (but Haiku may surprise us!)

---

## Deliverables

**Code Changes**:
- Enhanced edge types with confidence
- Graph-first retrieval implementation
- Intent classification integration
- Database migrations
- Comprehensive tests

**Documentation**:
- Architecture decisions explained
- Performance benchmarks
- Usage examples
- Feature flag documentation

**Evidence**:
- All tests passing
- Cost reduction demonstrated
- Performance targets met
- Git commits with clear messages

---

## Final Notes

**This Is The Ultimate Test**:
- Not just integration - architectural design
- Requires understanding graph concepts
- Performance optimization needed
- Design decisions throughout

**Haiku's Track Record**:
- Beat every estimate so far
- Discovered architectural issues (#269 divergence)
- Perfect Phase -1 execution (#271)
- Quality consistently excellent

**Can Haiku Handle Architecture?**: Let's find out! 🚀

**If you hit limits**: That's valuable data! Report where you got stuck. Architectural work may be Sonnet territory, and that's perfectly fine.

---

*Prompt Version: 1.0*
*Issue: #278 CORE-KNOW-ENHANCE*
*Complexity: ARCHITECTURAL*
*Created: October 26, 2025, 6:50 PM PT*
