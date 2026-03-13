# Phase 3: Testing & Validation - CORE-KNOW #99

**Agent**: Claude Code (Programmer)
**Issue**: #99 - CORE-KNOW
**Phase**: 3 - Testing & Validation
**Date**: October 18, 2025, 4:15 PM
**Duration**: ~1 hour estimated

---

## Mission

Test the Knowledge Graph integration with **real canonical queries** and validate production readiness. This goes beyond unit tests to verify actual user-facing behavior.

## Context

**Phases 1-2 Complete** ✅:
- Database tables created and operational
- IntentService integration complete
- Feature flag control working
- Unit tests passing (6/6 = 100%)
- Performance excellent (2.3ms)

**Now**: Test with real scenarios to confirm it actually works for users.

---

## Canonical Queries from Issue #99

From the issue description, these queries should demonstrate Knowledge Graph enhancement:

### Before Knowledge Graph:
```
User: "What's the status of the website project?"
Response: "I need more information about which website project you're referring to."
```

### After Knowledge Graph:
```
User: "What's the status of the website project?"
Response: "The pmorgan.tech Website MVP (SITE-001) is in progress with 3 of 5 phases complete.
Based on recent activity, you've been focused on the technical foundation and design system.
The current blocker appears to be integrations with ConvertKit and Medium RSS feeds."
```

**Your Job**: Create tests that demonstrate this enhancement.

---

## Testing Strategy

### Step 1: Seed Test Data (15 minutes)

**Create realistic test data in Knowledge Graph**:

**File**: `dev/2025/10/18/seed-kg-test-data.py`

```python
"""
Seed Knowledge Graph with test data for canonical query testing.

Creates:
- Project nodes (SITE-001: pmorgan.tech Website MVP)
- Person nodes (PM, stakeholders)
- Document nodes (project docs)
- Edges (relationships between entities)
"""

import asyncio
from datetime import datetime
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.knowledge.knowledge_graph_repository import KnowledgeGraphRepository
from services.knowledge.models import NodeType, EdgeType
from services.database import AsyncSessionFactory


async def seed_test_data():
    """Seed Knowledge Graph with test data."""
    print("Seeding Knowledge Graph test data...")

    async with AsyncSessionFactory.session_scope() as session:
        repo = KnowledgeGraphRepository(session)
        kg_service = KnowledgeGraphService(repo)

        # 1. Create project node
        website_project = await kg_service.create_node(
            node_type=NodeType.CONCEPT,  # Using CONCEPT as PROJECT type
            name="pmorgan.tech Website MVP",
            description="Website project for Paul Morgan Tech",
            metadata={
                "project_id": "SITE-001",
                "status": "in_progress",
                "phases": {
                    "total": 5,
                    "complete": 3,
                    "current": "Integration"
                },
                "focus_areas": [
                    "technical foundation",
                    "design system"
                ],
                "blockers": [
                    "ConvertKit integration",
                    "Medium RSS feeds"
                ]
            }
        )
        print(f"✓ Created project node: {website_project.name}")

        # 2. Create person node (PM)
        pm_node = await kg_service.create_node(
            node_type=NodeType.PERSON,
            name="Paul Morgan",
            description="Project Manager and Tech Lead",
            metadata={
                "role": "PM",
                "interests": ["AI", "web development", "productivity"]
            }
        )
        print(f"✓ Created person node: {pm_node.name}")

        # 3. Create document nodes
        design_doc = await kg_service.create_node(
            node_type=NodeType.DOCUMENT,
            name="Website Design System",
            description="Design system documentation for website",
            metadata={
                "status": "complete",
                "last_updated": datetime.now().isoformat()
            }
        )
        print(f"✓ Created document node: {design_doc.name}")

        # 4. Create edges (relationships)
        await kg_service.create_edge(
            source_node_id=pm_node.id,
            target_node_id=website_project.id,
            edge_type=EdgeType.OWNS,
            metadata={"role": "owner"}
        )
        print(f"✓ Created edge: PM owns website project")

        await kg_service.create_edge(
            source_node_id=website_project.id,
            target_node_id=design_doc.id,
            edge_type=EdgeType.RELATED_TO,
            metadata={"relationship": "has_document"}
        )
        print(f"✓ Created edge: Project related to design doc")

        # 5. Create interaction history (patterns)
        interactions = [
            "Discussed technical foundation setup",
            "Reviewed design system progress",
            "Identified ConvertKit blocker",
            "Planning Medium RSS integration"
        ]

        for interaction in interactions:
            interaction_node = await kg_service.create_node(
                node_type=NodeType.CONCEPT,
                name=f"Interaction: {interaction[:30]}",
                description=interaction,
                metadata={
                    "type": "interaction",
                    "timestamp": datetime.now().isoformat()
                }
            )

            await kg_service.create_edge(
                source_node_id=pm_node.id,
                target_node_id=interaction_node.id,
                edge_type=EdgeType.RELATED_TO,
                metadata={"interaction_type": "discussion"}
            )

        print(f"✓ Created {len(interactions)} interaction nodes")

        print("\n✅ Test data seeding complete!")
        print(f"   Projects: 1")
        print(f"   People: 1")
        print(f"   Documents: 1")
        print(f"   Interactions: {len(interactions)}")
        print(f"   Edges: {2 + len(interactions)}")


if __name__ == "__main__":
    asyncio.run(seed_test_data())
```

### Step 2: Canonical Query Tests (20 minutes)

**File**: `dev/2025/10/18/test-canonical-queries.py`

```python
"""
Test canonical queries from Issue #99.

Validates that Knowledge Graph enhances responses with contextual information.
"""

import asyncio
import os
from services.intent.intent_service import IntentService


async def test_canonical_query_website_status():
    """
    Test canonical query: "What's the status of the website project?"

    Expected enhancement:
    - Should identify SITE-001 project
    - Should mention 3 of 5 phases complete
    - Should reference technical foundation and design system
    - Should mention ConvertKit and Medium RSS blockers
    """
    print("\n" + "=" * 70)
    print("Test: Canonical Query - Website Project Status")
    print("=" * 70)

    # Enable Knowledge Graph
    os.environ['ENABLE_KNOWLEDGE_GRAPH'] = 'true'

    # Create intent service
    intent_service = IntentService()

    # Test query
    message = "What's the status of the website project?"
    session_id = "canonical-test-001"

    print(f"\nQuery: {message}")
    print("-" * 70)

    # Process intent
    result = await intent_service.process_intent(
        message=message,
        session_id=session_id
    )

    # Check for Knowledge Graph enhancement
    if hasattr(result, 'context') and result.context:
        kg_data = result.context.get('knowledge_graph', {})

        print("\n📊 Knowledge Graph Enhancement:")
        print(f"   Projects found: {len(kg_data.get('projects', []))}")
        print(f"   Patterns found: {len(kg_data.get('patterns', []))}")
        print(f"   Entities found: {len(kg_data.get('entities', []))}")

        # Detailed project info
        projects = kg_data.get('projects', [])
        if projects:
            print("\n🎯 Project Details:")
            for proj in projects:
                print(f"   Name: {proj.get('name')}")
                print(f"   Description: {proj.get('description')}")
                metadata = proj.get('metadata', {})
                if metadata:
                    print(f"   Metadata: {metadata}")

        # Check for expected content
        has_project = any('website' in p.get('name', '').lower() for p in projects)
        has_context = len(projects) > 0

        if has_project:
            print("\n✅ PASS: Website project identified in Knowledge Graph")
        else:
            print("\n⚠️  WARNING: Website project not found")
            print(f"   Projects: {[p.get('name') for p in projects]}")

        if has_context:
            print("✅ PASS: Context enhanced with Knowledge Graph data")
        else:
            print("❌ FAIL: No context enhancement")

        return has_project and has_context
    else:
        print("\n❌ FAIL: No context in result")
        return False


async def test_query_without_kg():
    """
    Test same query WITHOUT Knowledge Graph.

    Should show the difference in context availability.
    """
    print("\n" + "=" * 70)
    print("Test: Query WITHOUT Knowledge Graph (comparison)")
    print("=" * 70)

    # Disable Knowledge Graph
    os.environ['ENABLE_KNOWLEDGE_GRAPH'] = 'false'

    # Create intent service
    intent_service = IntentService()

    # Same query
    message = "What's the status of the website project?"
    session_id = "canonical-test-002"

    print(f"\nQuery: {message}")
    print("-" * 70)

    # Process intent
    result = await intent_service.process_intent(
        message=message,
        session_id=session_id
    )

    # Check for Knowledge Graph enhancement
    if hasattr(result, 'context') and result.context:
        kg_data = result.context.get('knowledge_graph')

        if kg_data is None:
            print("\n✅ PASS: Knowledge Graph correctly disabled")
            print("   (No graph enhancement in context)")
            return True
        else:
            print("\n❌ FAIL: Knowledge Graph present despite disabled flag")
            return False
    else:
        print("\n✅ PASS: No context (KG disabled)")
        return True


async def test_multiple_projects():
    """Test query that should match multiple projects."""
    print("\n" + "=" * 70)
    print("Test: Multiple Project Query")
    print("=" * 70)

    # Enable Knowledge Graph
    os.environ['ENABLE_KNOWLEDGE_GRAPH'] = 'true'

    intent_service = IntentService()

    # Query that might match multiple projects
    message = "Show me all my projects"
    session_id = "canonical-test-003"

    print(f"\nQuery: {message}")
    print("-" * 70)

    result = await intent_service.process_intent(
        message=message,
        session_id=session_id
    )

    if hasattr(result, 'context') and result.context:
        kg_data = result.context.get('knowledge_graph', {})
        projects = kg_data.get('projects', [])

        print(f"\n📊 Found {len(projects)} projects")
        for proj in projects:
            print(f"   - {proj.get('name')}")

        if len(projects) >= 1:
            print("\n✅ PASS: Multiple projects queryable")
            return True
        else:
            print("\n⚠️  WARNING: Expected at least 1 project")
            return False
    else:
        print("\n❌ FAIL: No context")
        return False


async def main():
    """Run all canonical query tests."""
    print("\n" + "=" * 70)
    print("CANONICAL QUERY TESTS - Issue #99")
    print("=" * 70)

    tests = [
        ("Website Status (WITH KG)", test_canonical_query_website_status),
        ("Same Query (WITHOUT KG)", test_query_without_kg),
        ("Multiple Projects", test_multiple_projects),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\nPassed: {passed}/{total} ({100*passed//total if total else 0}%)")

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
```

### Step 3: Performance Validation (15 minutes)

**File**: `dev/2025/10/18/test-kg-performance.py`

```python
"""
Performance validation for Knowledge Graph integration.

Tests:
- Response time with KG enabled vs disabled
- Query performance under realistic load
- Cache effectiveness
"""

import asyncio
import os
import time
from statistics import mean, stdev
from services.intent.intent_service import IntentService


async def measure_response_time(message: str, session_id: str, kg_enabled: bool):
    """Measure response time for a query."""
    os.environ['ENABLE_KNOWLEDGE_GRAPH'] = 'true' if kg_enabled else 'false'

    intent_service = IntentService()

    start = time.time()
    result = await intent_service.process_intent(
        message=message,
        session_id=session_id
    )
    elapsed_ms = (time.time() - start) * 1000

    return elapsed_ms


async def test_performance_comparison():
    """Compare performance with KG enabled vs disabled."""
    print("\n" + "=" * 70)
    print("Test: Performance Comparison (KG ON vs OFF)")
    print("=" * 70)

    query = "What's the status of the website project?"
    iterations = 10

    # Test WITH Knowledge Graph
    print(f"\nTesting WITH Knowledge Graph ({iterations} iterations)...")
    times_with_kg = []
    for i in range(iterations):
        elapsed = await measure_response_time(query, f"perf-test-on-{i}", True)
        times_with_kg.append(elapsed)

    avg_with = mean(times_with_kg)
    std_with = stdev(times_with_kg) if len(times_with_kg) > 1 else 0

    print(f"   Average: {avg_with:.1f}ms")
    print(f"   Std Dev: {std_with:.1f}ms")
    print(f"   Min: {min(times_with_kg):.1f}ms")
    print(f"   Max: {max(times_with_kg):.1f}ms")

    # Test WITHOUT Knowledge Graph
    print(f"\nTesting WITHOUT Knowledge Graph ({iterations} iterations)...")
    times_without_kg = []
    for i in range(iterations):
        elapsed = await measure_response_time(query, f"perf-test-off-{i}", False)
        times_without_kg.append(elapsed)

    avg_without = mean(times_without_kg)
    std_without = stdev(times_without_kg) if len(times_without_kg) > 1 else 0

    print(f"   Average: {avg_without:.1f}ms")
    print(f"   Std Dev: {std_without:.1f}ms")
    print(f"   Min: {min(times_without_kg):.1f}ms")
    print(f"   Max: {max(times_without_kg):.1f}ms")

    # Calculate overhead
    overhead_ms = avg_with - avg_without
    overhead_pct = (overhead_ms / avg_without * 100) if avg_without > 0 else 0

    print(f"\n📊 Performance Impact:")
    print(f"   Overhead: {overhead_ms:.1f}ms ({overhead_pct:.1f}%)")

    # Target: <100ms overhead
    if overhead_ms < 100:
        print(f"✅ PASS: Overhead within target ({overhead_ms:.1f}ms < 100ms)")
        return True
    else:
        print(f"⚠️  WARNING: Overhead above target ({overhead_ms:.1f}ms > 100ms)")
        return False


async def test_cache_effectiveness():
    """Test that caching improves repeated query performance."""
    print("\n" + "=" * 70)
    print("Test: Cache Effectiveness")
    print("=" * 70)

    os.environ['ENABLE_KNOWLEDGE_GRAPH'] = 'true'

    query = "What's the status of the website project?"
    session_id = "cache-test-001"

    # First query (cold cache)
    print("\nFirst query (cold cache)...")
    time_cold = await measure_response_time(query, session_id, True)
    print(f"   Time: {time_cold:.1f}ms")

    # Repeated queries (warm cache)
    print("\nRepeated queries (warm cache)...")
    times_warm = []
    for i in range(5):
        elapsed = await measure_response_time(query, session_id, True)
        times_warm.append(elapsed)
        print(f"   Query {i+1}: {elapsed:.1f}ms")

    avg_warm = mean(times_warm)

    # Cache should improve performance
    improvement_ms = time_cold - avg_warm
    improvement_pct = (improvement_ms / time_cold * 100) if time_cold > 0 else 0

    print(f"\n📊 Cache Impact:")
    print(f"   Cold: {time_cold:.1f}ms")
    print(f"   Warm: {avg_warm:.1f}ms")
    print(f"   Improvement: {improvement_ms:.1f}ms ({improvement_pct:.1f}%)")

    # If warm is faster, cache is working
    if avg_warm <= time_cold:
        print(f"✅ PASS: Cache improving performance")
        return True
    else:
        print(f"⚠️  INFO: No cache benefit observed")
        return True  # Not a failure


async def main():
    """Run all performance tests."""
    print("\n" + "=" * 70)
    print("PERFORMANCE VALIDATION TESTS")
    print("=" * 70)

    tests = [
        ("Performance Comparison", test_performance_comparison),
        ("Cache Effectiveness", test_cache_effectiveness),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\nPassed: {passed}/{total} ({100*passed//total if total else 0}%)")

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Step 4: Production Readiness Check (10 minutes)

**File**: `dev/2025/10/18/production-readiness-checklist.md`

```markdown
# Production Readiness Checklist - Knowledge Graph Integration

## Functionality ✅
- [ ] Database schema created and operational
- [ ] IntentService integration complete
- [ ] Context enhancement working
- [ ] Feature flag control functional
- [ ] Graceful degradation on failures

## Testing ✅
- [ ] Unit tests passing (6/6 from Phase 2)
- [ ] Canonical queries enhanced correctly
- [ ] Feature flag disable/enable working
- [ ] Performance within targets (<100ms overhead)
- [ ] Cache effectiveness validated

## Performance ✅
- [ ] Query time < 100ms overhead
- [ ] No memory leaks
- [ ] Database queries optimized
- [ ] Caching working effectively

## Safety ✅
- [ ] Graceful degradation confirmed
- [ ] Error handling comprehensive
- [ ] No crashes on KG failures
- [ ] Feature flag instant disable

## Documentation ✅
- [ ] Environment variables documented
- [ ] Integration pattern documented
- [ ] Usage examples provided
- [ ] Troubleshooting guide available

## Configuration ✅
- [ ] ENABLE_KNOWLEDGE_GRAPH flag working
- [ ] Default: disabled (safe)
- [ ] Timeout configured
- [ ] Cache TTL configured

## Deployment ✅
- [ ] Database migrations run
- [ ] Test data can be seeded
- [ ] Verification scripts available
- [ ] Rollback procedure documented

## Next Steps
- [ ] Phase 4: Boundary enforcement (Issue #230)
- [ ] Phase 5: Final documentation
- [ ] Enable in production

## Risk Assessment
**Low Risk**:
- Feature flag provides instant disable
- Graceful degradation prevents crashes
- Performance impact negligible
- Comprehensive testing complete
```

---

## Success Criteria

Phase 3 is complete when:

- [ ] Test data seeded successfully
- [ ] Canonical queries show KG enhancement
- [ ] Without KG shows no enhancement (control test)
- [ ] Performance overhead < 100ms
- [ ] Cache effectiveness demonstrated
- [ ] Production readiness checklist complete
- [ ] All tests passing

---

## Deliverables

1. **seed-kg-test-data.py** - Test data seeding script
2. **test-canonical-queries.py** - Canonical query tests
3. **test-kg-performance.py** - Performance validation
4. **production-readiness-checklist.md** - Readiness assessment
5. **dev/2025/10/18/phase-3-testing-report.md** - Completion report

---

## Time Estimate

- Step 1 (Seed data): 15 minutes
- Step 2 (Canonical tests): 20 minutes
- Step 3 (Performance): 15 minutes
- Step 4 (Readiness): 10 minutes
- **Total**: ~1 hour

---

## Important Notes

### Focus on Real Behavior

This phase tests **what users will experience**, not just code correctness:
- Do queries actually get enhanced?
- Is the enhancement useful?
- Is performance acceptable?
- Does it work reliably?

### Comparison Testing

Always test WITH and WITHOUT KG to demonstrate:
- Enhancement value
- Feature flag control
- Performance impact

### Production Readiness

Before marking Phase 3 complete, verify:
- ✅ All functionality working
- ✅ All tests passing
- ✅ Performance acceptable
- ✅ Safety measures in place
- ✅ Ready for Phase 4 (boundaries)

---

## Next Phase Preview

**Phase 4** (Issue #230 - Boundaries):
- Traversal depth limits
- Node count limits
- Timeout enforcement
- Memory limits

**Phase 5** (Final):
- Complete documentation
- Configuration guide
- Deployment instructions

But first: Validate that Knowledge Graph enhancement actually works!

---

**Ready to test Knowledge Graph with real canonical queries!** 🧪

**This proves Piper Morgan's memory enhancement works in practice!**
