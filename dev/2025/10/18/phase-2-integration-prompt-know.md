# Phase 2: IntentService Integration - CORE-KNOW #99

**Agent**: Claude Code (Programmer)
**Issue**: #99 - CORE-KNOW
**Phase**: 2 - IntentService Integration
**Date**: October 18, 2025, 3:45 PM
**Duration**: ~1-1.5 hours estimated (likely ~45 min actual)

---

## Mission

Connect the Knowledge Graph to conversation flow by integrating with IntentService. This follows the **exact same pattern** as Ethics #197 (completed today), which successfully provided universal coverage by integrating at the service layer.

## Context

**Phase 1 Complete** ✅:
- Database tables created (knowledge_nodes, knowledge_edges)
- 10 indexes for performance
- All verification tests passing (6/6)
- CRUD operations functional

**Pattern from Ethics #197**:
- Integrated at IntentService.process_intent()
- After ethics check, before intent classification
- Feature flag control (ENABLE_ETHICS_ENFORCEMENT)
- 100% test pass rate
- Production-ready in 30 minutes

**Your Job**: Apply the same pattern for Knowledge Graph.

---

## Implementation Strategy

### Step 1: Create Integration Layer (20-30 minutes)

**New File**: `services/knowledge/conversation_integration.py`

```python
"""
Knowledge Graph integration for conversation enhancement.

Provides context enrichment from the Knowledge Graph for conversation processing.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.knowledge.models import KnowledgeNode, KnowledgeEdge, NodeType

logger = logging.getLogger(__name__)


class ConversationKnowledgeGraphIntegration:
    """
    Integrate Knowledge Graph with conversation flow.

    Follows the proven pattern from Ethics integration (#197).
    """

    def __init__(self, kg_service: Optional[KnowledgeGraphService] = None):
        """
        Initialize conversation integration.

        Args:
            kg_service: Optional KnowledgeGraphService instance (for testing)
        """
        self.kg_service = kg_service or KnowledgeGraphService()
        self.enabled = True  # Will be controlled by feature flag

    async def enhance_conversation_context(
        self,
        message: str,
        session_id: str,
        base_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enhance conversation context with Knowledge Graph insights.

        Args:
            message: User's message text
            session_id: Conversation session identifier
            base_context: Optional base context to enhance

        Returns:
            Enhanced context dictionary with graph insights
        """
        if not self.enabled:
            logger.debug("Knowledge Graph enhancement disabled")
            return base_context or {}

        try:
            # Start with base context
            enhanced_context = base_context.copy() if base_context else {}

            # Query Knowledge Graph for relevant context
            graph_insights = await self._query_graph_context(message, session_id)

            # Merge graph insights into context
            enhanced_context['knowledge_graph'] = graph_insights

            # Add specific enrichments
            if graph_insights.get('projects'):
                enhanced_context['related_projects'] = graph_insights['projects']

            if graph_insights.get('patterns'):
                enhanced_context['recent_patterns'] = graph_insights['patterns']

            if graph_insights.get('entities'):
                enhanced_context['mentioned_entities'] = graph_insights['entities']

            logger.info(
                f"Enhanced context with {len(graph_insights.get('projects', []))} projects, "
                f"{len(graph_insights.get('patterns', []))} patterns"
            )

            return enhanced_context

        except Exception as e:
            # Graceful degradation - log error but continue
            logger.error(f"Knowledge Graph enhancement failed: {e}", exc_info=True)
            return base_context or {}

    async def _query_graph_context(
        self,
        message: str,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Query Knowledge Graph for relevant context.

        Args:
            message: User's message
            session_id: Session identifier

        Returns:
            Dictionary with graph insights
        """
        insights = {
            'projects': [],
            'patterns': [],
            'entities': [],
            'relationships': []
        }

        try:
            # Query for project-related nodes
            # Extract potential project mentions from message
            # This is a simple implementation - enhance with NER later
            project_keywords = self._extract_keywords(message, ['project', 'website', 'site'])

            if project_keywords:
                projects = await self._query_projects(project_keywords)
                insights['projects'] = projects

            # Query for recent patterns in this session
            patterns = await self._query_session_patterns(session_id)
            insights['patterns'] = patterns

            # Query for entities mentioned
            entities = await self._query_entities(message)
            insights['entities'] = entities

            return insights

        except Exception as e:
            logger.error(f"Graph query failed: {e}")
            return insights

    async def _query_projects(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Query for project nodes matching keywords."""
        try:
            # Search for project nodes
            projects = []
            for keyword in keywords:
                # Use KnowledgeGraphService to find nodes
                nodes = await self.kg_service.search_nodes(
                    node_type=NodeType.PROJECT,
                    search_term=keyword
                )

                for node in nodes[:3]:  # Limit to top 3
                    projects.append({
                        'id': str(node.id),
                        'name': node.name,
                        'description': node.description,
                        'metadata': node.metadata
                    })

            return projects

        except Exception as e:
            logger.error(f"Project query failed: {e}")
            return []

    async def _query_session_patterns(self, session_id: str) -> List[Dict[str, Any]]:
        """Query for patterns in this session."""
        try:
            # Find interaction nodes for this session
            nodes = await self.kg_service.get_nodes_by_session(session_id)

            # Extract patterns from recent interactions
            patterns = []
            for node in nodes[-5:]:  # Last 5 interactions
                patterns.append({
                    'timestamp': node.created_at.isoformat() if node.created_at else None,
                    'type': node.node_type.value if hasattr(node.node_type, 'value') else str(node.node_type),
                    'summary': node.description
                })

            return patterns

        except Exception as e:
            logger.error(f"Pattern query failed: {e}")
            return []

    async def _query_entities(self, message: str) -> List[Dict[str, Any]]:
        """Query for entities mentioned in message."""
        try:
            # Simple entity extraction (enhance later with NER)
            entities = []

            # Look for capitalized words that might be entities
            words = message.split()
            potential_entities = [w.strip('.,!?') for w in words if w[0].isupper()]

            for entity_name in potential_entities[:5]:  # Limit to 5
                # Search for matching nodes
                nodes = await self.kg_service.search_nodes(
                    search_term=entity_name
                )

                if nodes:
                    node = nodes[0]
                    entities.append({
                        'name': node.name,
                        'type': node.node_type.value if hasattr(node.node_type, 'value') else str(node.node_type),
                        'id': str(node.id)
                    })

            return entities

        except Exception as e:
            logger.error(f"Entity query failed: {e}")
            return []

    def _extract_keywords(self, text: str, topic_words: List[str]) -> List[str]:
        """Extract keywords related to topic words."""
        keywords = []
        text_lower = text.lower()

        for topic in topic_words:
            if topic in text_lower:
                # Simple extraction - find words near topic word
                words = text_lower.split()
                if topic in words:
                    idx = words.index(topic)
                    # Get context words around topic
                    start = max(0, idx - 2)
                    end = min(len(words), idx + 3)
                    context = words[start:end]
                    keywords.extend([w for w in context if len(w) > 3])

        return list(set(keywords))[:5]  # Limit to 5 unique keywords
```

### Step 2: Integrate with IntentService (15-20 minutes)

**File to modify**: `services/intent/intent_service.py`

**Add integration at the start of `process_intent()`**:

```python
# At top of file
from services.knowledge.conversation_integration import ConversationKnowledgeGraphIntegration
import os

class IntentService:
    def __init__(self):
        # ... existing initialization ...

        # Knowledge Graph integration (like Ethics)
        self.kg_integration = ConversationKnowledgeGraphIntegration()

    async def process_intent(
        self,
        message: str,
        session_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> IntentProcessingResult:
        """
        Process user intent with Knowledge Graph enhancement.

        Flow:
        1. Ethics check (existing - from #197)
        2. Knowledge Graph enhancement (NEW)
        3. Intent classification (existing)
        4. Response generation (existing)
        """

        # Ethics check (existing from #197)
        if hasattr(self, 'boundary_enforcer') and os.getenv('ENABLE_ETHICS_ENFORCEMENT', 'false').lower() == 'true':
            ethics_result = await self.boundary_enforcer.enforce_boundaries(
                message=message,
                session_id=session_id,
                context=context or {}
            )

            if ethics_result.blocked:
                return IntentProcessingResult(
                    blocked=True,
                    reason=ethics_result.reason,
                    metadata={'ethics': ethics_result}
                )

        # Knowledge Graph enhancement (NEW)
        enhanced_context = context or {}
        if os.getenv('ENABLE_KNOWLEDGE_GRAPH', 'false').lower() == 'true':
            try:
                enhanced_context = await self.kg_integration.enhance_conversation_context(
                    message=message,
                    session_id=session_id,
                    base_context=context
                )
                logger.info("Knowledge Graph context enhancement successful")
            except Exception as e:
                logger.error(f"Knowledge Graph enhancement failed: {e}", exc_info=True)
                # Graceful degradation - continue with base context
                enhanced_context = context or {}

        # Continue with existing intent processing using enhanced_context
        # ... rest of existing process_intent() code ...

        # Use enhanced_context instead of context for the rest of the method
```

### Step 3: Add Feature Flag Configuration (5 minutes)

**File**: `.env` or `config/settings.py`

```bash
# Knowledge Graph Feature Flag
ENABLE_KNOWLEDGE_GRAPH=false  # Start disabled for safety

# Knowledge Graph Configuration
KNOWLEDGE_GRAPH_TIMEOUT_MS=100  # Query timeout
KNOWLEDGE_GRAPH_CACHE_TTL=300   # Cache TTL in seconds
```

**Update environment variables documentation**:
- Add to `docs/internal/operations/environment-variables.md`
- Document ENABLE_KNOWLEDGE_GRAPH flag
- Document configuration options

### Step 4: Create Integration Tests (20-30 minutes)

**File**: `dev/2025/10/18/test-knowledge-graph-integration.py`

```python
"""
Test Knowledge Graph integration with IntentService.

Tests:
1. Context enhancement with graph insights
2. Graceful degradation when KG unavailable
3. Feature flag control
4. Performance within limits
"""

import asyncio
import os
from services.intent.intent_service import IntentService
from services.knowledge.conversation_integration import ConversationKnowledgeGraphIntegration


async def test_knowledge_graph_enhancement():
    """Test that KG enhances conversation context."""
    print("\n=== Test 1: Knowledge Graph Enhancement ===")

    # Enable feature flag
    os.environ['ENABLE_KNOWLEDGE_GRAPH'] = 'true'

    # Create service
    intent_service = IntentService()

    # Test message mentioning a project
    message = "What's the status of the website project?"
    session_id = "test-session-kg-001"

    # Process intent
    result = await intent_service.process_intent(
        message=message,
        session_id=session_id
    )

    # Check for graph enhancement
    if hasattr(result, 'context') and result.context:
        kg_data = result.context.get('knowledge_graph', {})
        print(f"✅ PASS: Knowledge Graph enhancement applied")
        print(f"   Projects: {len(kg_data.get('projects', []))}")
        print(f"   Patterns: {len(kg_data.get('patterns', []))}")
        print(f"   Entities: {len(kg_data.get('entities', []))}")
    else:
        print(f"❌ FAIL: No graph enhancement in context")

    return True


async def test_feature_flag_disabled():
    """Test that KG is bypassed when feature flag disabled."""
    print("\n=== Test 2: Feature Flag Disabled ===")

    # Disable feature flag
    os.environ['ENABLE_KNOWLEDGE_GRAPH'] = 'false'

    # Create service
    intent_service = IntentService()

    # Process intent
    message = "What's the status of the website project?"
    session_id = "test-session-kg-002"

    result = await intent_service.process_intent(
        message=message,
        session_id=session_id
    )

    # Should have no graph enhancement
    if hasattr(result, 'context') and result.context:
        kg_data = result.context.get('knowledge_graph')
        if kg_data is None:
            print(f"✅ PASS: Knowledge Graph disabled via feature flag")
        else:
            print(f"❌ FAIL: Knowledge Graph active despite disabled flag")
    else:
        print(f"✅ PASS: No context (KG disabled)")

    return True


async def test_graceful_degradation():
    """Test that system handles KG failures gracefully."""
    print("\n=== Test 3: Graceful Degradation ===")

    # Enable feature flag
    os.environ['ENABLE_KNOWLEDGE_GRAPH'] = 'true'

    # Test with non-existent session (should not crash)
    intent_service = IntentService()

    message = "Some random message"
    session_id = "nonexistent-session-999"

    try:
        result = await intent_service.process_intent(
            message=message,
            session_id=session_id
        )
        print(f"✅ PASS: System handled KG query gracefully")
    except Exception as e:
        print(f"❌ FAIL: System crashed on KG failure: {e}")
        return False

    return True


async def test_performance():
    """Test that KG enhancement meets performance targets."""
    print("\n=== Test 4: Performance Target (<100ms) ===")

    import time

    # Enable feature flag
    os.environ['ENABLE_KNOWLEDGE_GRAPH'] = 'true'

    intent_service = IntentService()

    message = "What's the status?"
    session_id = "test-session-kg-perf"

    # Measure time
    start = time.time()
    result = await intent_service.process_intent(
        message=message,
        session_id=session_id
    )
    elapsed_ms = (time.time() - start) * 1000

    if elapsed_ms < 100:
        print(f"✅ PASS: Performance within target ({elapsed_ms:.1f}ms < 100ms)")
    else:
        print(f"⚠️  WARNING: Performance slower than target ({elapsed_ms:.1f}ms > 100ms)")

    return True


async def main():
    """Run all integration tests."""
    print("=" * 60)
    print("Knowledge Graph Integration Tests")
    print("=" * 60)

    tests = [
        ("Enhancement", test_knowledge_graph_enhancement),
        ("Feature Flag", test_feature_flag_disabled),
        ("Graceful Degradation", test_graceful_degradation),
        ("Performance", test_performance),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"Passed: {passed}/{total} ({100*passed//total}%)")

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Success Criteria

Phase 2 is complete when:

- [ ] ConversationKnowledgeGraphIntegration class created
- [ ] IntentService integration complete
- [ ] Feature flag ENABLE_KNOWLEDGE_GRAPH working
- [ ] All integration tests passing (4/4)
- [ ] Context enhancement with graph insights functional
- [ ] Graceful degradation on KG failures
- [ ] Performance within 100ms target
- [ ] Documentation updated

---

## Deliverables

1. **services/knowledge/conversation_integration.py** (new)
2. **services/intent/intent_service.py** (modified)
3. **dev/2025/10/18/test-knowledge-graph-integration.py** (new)
4. **.env** or **config/settings.py** (feature flag added)
5. **docs/internal/operations/environment-variables.md** (updated)
6. **dev/2025/10/18/phase-2-integration-report.md** (completion report)

---

## Important Notes

### Pattern from Ethics #197

This follows the **exact same pattern** that worked for Ethics:
1. Integration layer (ConversationKnowledgeGraphIntegration)
2. IntentService integration point
3. Feature flag control
4. Graceful degradation
5. Comprehensive testing

### Graceful Degradation is Critical

If Knowledge Graph fails:
- Log error but continue
- Return base context (not enhanced)
- User sees no error
- System remains operational

### Performance Target

- Knowledge Graph queries must complete in <100ms
- Use simple queries initially
- Optimize later if needed
- Cache frequently accessed data

### Feature Flag Default

- Start with ENABLE_KNOWLEDGE_GRAPH=false
- Enable after testing confirms stability
- Can disable instantly if issues arise

---

## Time Estimate

- Step 1 (Integration layer): 20-30 minutes
- Step 2 (IntentService): 15-20 minutes
- Step 3 (Feature flag): 5 minutes
- Step 4 (Tests): 20-30 minutes
- **Total**: 1-1.5 hours

**Time Lords applies**: Take time needed for correctness, but this is very similar to Ethics #197 which took 30 minutes.

---

## Next Phase Preview

**Phase 3** (after this):
- Test with canonical queries
- Verify enhanced responses
- Performance validation
- Production readiness

**Phase 4** (Issue #230):
- Add boundary enforcement
- Depth limits, node limits, timeouts
- Prevent resource exhaustion

But first: Connect Knowledge Graph to conversation flow!

---

**Ready to integrate Knowledge Graph with IntentService!** 🧠

**This will activate Piper Morgan's memory and context awareness!**
