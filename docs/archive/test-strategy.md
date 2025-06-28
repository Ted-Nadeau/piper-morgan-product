# Piper Morgan 1.0 - Test Strategy Document

## Overview

This document defines the comprehensive testing strategy for Piper Morgan, ensuring quality, reliability, and maintainability through systematic testing practices. Our approach emphasizes test-first development, architectural validation, and AI-specific testing patterns.

## Testing Philosophy

### Core Principles

1. **Tests Define Behavior** - Tests are the source of truth for expected functionality
2. **Test-First Development** - Write tests before implementation to drive design
3. **Architecture Validation** - Tests catch architectural drift and pattern violations
4. **Continuous Feedback** - Fast test execution enables rapid iteration
5. **Living Documentation** - Tests document system behavior better than comments

### Testing Pyramid

```
         ╱╲
        ╱E2E╲        <- End-to-End (5%)
       ╱______╲         Real services, full workflows
      ╱        ╲
     ╱Integration╲   <- Integration (20%)
    ╱______________╲    Component interactions
   ╱                ╲
  ╱   Unit Tests     ╲ <- Unit (75%)
 ╱____________________╲   Isolated components
```

## Test Categories

### 1. Unit Tests (75% of tests)

**Purpose**: Test individual components in isolation

**Characteristics**:
- Fast execution (<100ms per test)
- No external dependencies
- Deterministic results
- High code coverage

**Example**:
```python
class TestProjectContext:
    @pytest.mark.asyncio
    async def test_explicit_project_id_takes_precedence(self):
        # Given: Mock repository
        mock_repo = Mock(spec=ProjectRepository)
        mock_repo.get_by_id.return_value = Project(id="123", name="Test")
        
        # When: Resolving with explicit ID
        context = ProjectContext(mock_repo, mock_llm)
        project, needs_confirm = await context.resolve_project(
            Intent(context={"project_id": "123"}),
            session_id="test"
        )
        
        # Then: Returns project without confirmation
        assert project.id == "123"
        assert needs_confirm is False
```

**What to Unit Test**:
- Domain model business logic
- Service orchestration logic
- Utility functions
- Error handling paths
- Edge cases

### 2. Integration Tests (20% of tests)

**Purpose**: Test component interactions and external integrations

**Characteristics**:
- Moderate execution time (100ms-5s)
- May use test databases
- Tests real API contracts
- Validates data flow

**Example**:
```python
class TestQueryIntegration:
    @pytest.mark.asyncio
    async def test_list_projects_through_api(self, test_client, test_db):
        # Given: Projects in database
        await create_test_projects(test_db)
        
        # When: API request
        response = await test_client.post("/api/v1/intent", json={
            "message": "list all projects"
        })
        
        # Then: Correct response format
        assert response.status_code == 200
        data = response.json()
        assert data["intent"]["category"] == "query"
        assert len(data["data"]["projects"]) == 3
```

**What to Integration Test**:
- API endpoint behavior
- Database operations
- External service integrations
- Message passing between services
- Transaction boundaries

### 3. End-to-End Tests (5% of tests)

**Purpose**: Validate complete user workflows

**Characteristics**:
- Slow execution (>5s)
- Uses real services
- Tests business scenarios
- Catches system-level issues

**Example**:
```python
class TestGitHubWorkflow:
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_create_issue_from_natural_language(self, live_system):
        # Given: Live system with GitHub integration
        
        # When: Natural language request
        response = await live_system.process_intent(
            "Create a bug ticket for the login crash on mobile"
        )
        
        # Then: Real GitHub issue created
        assert response.workflow_status == "completed"
        assert "github.com" in response.issue_url
        
        # Verify issue content
        issue = await verify_github_issue(response.issue_number)
        assert "mobile" in issue.labels
        assert "bug" in issue.labels
```

**What to E2E Test**:
- Critical user journeys
- Multi-system workflows
- Performance under load
- Error recovery scenarios

## AI-Specific Testing Patterns

### 1. Intent Classification Testing

**Challenge**: Non-deterministic AI responses

**Strategy**: Statistical validation
```python
class TestIntentClassification:
    @pytest.mark.parametrize("message,expected_category,expected_action", [
        ("Create a ticket for bug", IntentCategory.EXECUTION, "create_ticket"),
        ("List all projects", IntentCategory.QUERY, "list_projects"),
        ("Analyze last sprint", IntentCategory.ANALYSIS, "analyze_metrics"),
    ])
    async def test_classification_accuracy(self, classifier, message, expected_category, expected_action):
        # Run classification
        intent = await classifier.classify(message)
        
        # Assert with confidence threshold
        assert intent.category == expected_category
        assert intent.action == expected_action
        assert intent.confidence >= 0.8  # 80% confidence minimum
```

### 2. Prompt Testing

**Challenge**: Prompt changes affect behavior

**Strategy**: Regression test suite
```python
class TestPromptStability:
    @pytest.fixture
    def golden_dataset(self):
        """Known good input/output pairs"""
        return [
            ("Create GitHub issue", {"action": "create_github_issue", "confidence": 0.95}),
            # ... more examples
        ]
    
    async def test_prompt_regression(self, classifier, golden_dataset):
        for input_text, expected in golden_dataset:
            result = await classifier.classify(input_text)
            assert result.action == expected["action"]
            assert result.confidence >= expected["confidence"] - 0.1  # Allow 10% variance
```

### 3. Knowledge Base Testing

**Challenge**: Semantic search quality

**Strategy**: Relevance benchmarks
```python
class TestKnowledgeSearch:
    async def test_search_relevance(self, knowledge_base):
        # Given: Known documents
        await knowledge_base.ingest("pm_best_practices.md", content=PM_BEST_PRACTICES)
        
        # When: Searching
        results = await knowledge_base.search("agile sprint planning")
        
        # Then: Relevant results
        assert len(results) >= 3
        assert any("sprint" in r.content.lower() for r in results)
        assert results[0].relevance_score >= 0.7
```

## Test Data Management

### 1. Test Fixtures

```python
@pytest.fixture
async def test_project():
    """Standard test project"""
    return Project(
        id="test-123",
        name="Test Project",
        integrations=[
            ProjectIntegration(
                type=IntegrationType.GITHUB,
                config={"repository": "test/repo"}
            )
        ]
    )

@pytest.fixture
async def test_db(db_engine):
    """Isolated test database"""
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield db_engine
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

### 2. Test Data Builders

```python
class ProjectBuilder:
    def __init__(self):
        self._project = Project(name="Test Project")
    
    def with_github(self, repo="test/repo"):
        self._project.integrations.append(
            ProjectIntegration(
                type=IntegrationType.GITHUB,
                config={"repository": repo}
            )
        )
        return self
    
    def with_default(self):
        self._project.is_default = True
        return self
    
    def build(self):
        return self._project

# Usage
project = ProjectBuilder().with_github().with_default().build()
```

### 3. Mock Data Strategies

```python
class MockLLMClient:
    """Deterministic LLM for testing"""
    
    def __init__(self, responses=None):
        self.responses = responses or {}
        self.calls = []
    
    async def complete(self, prompt):
        self.calls.append(prompt)
        # Return predetermined response based on prompt content
        for keyword, response in self.responses.items():
            if keyword in prompt:
                return response
        return "default response"
```

## Performance Testing

### 1. Load Testing

```python
@pytest.mark.performance
async def test_concurrent_intent_processing():
    # Create load
    tasks = []
    for i in range(100):
        task = asyncio.create_task(
            api_client.post("/api/v1/intent", json={
                "message": f"Create ticket {i}"
            })
        )
        tasks.append(task)
    
    # Measure performance
    start = time.time()
    responses = await asyncio.gather(*tasks)
    duration = time.time() - start
    
    # Assert performance criteria
    assert duration < 10  # 100 requests in 10 seconds
    assert all(r.status_code == 200 for r in responses)
```

### 2. Memory Testing

```python
@pytest.mark.memory
async def test_knowledge_base_memory_usage():
    # Measure baseline
    import psutil
    process = psutil.Process()
    baseline_memory = process.memory_info().rss
    
    # Ingest large documents
    for i in range(100):
        await knowledge_base.ingest(f"doc_{i}.txt", content="x" * 10000)
    
    # Check memory growth
    final_memory = process.memory_info().rss
    memory_growth_mb = (final_memory - baseline_memory) / 1024 / 1024
    
    assert memory_growth_mb < 500  # Less than 500MB growth
```

## Test Environment Management

### 1. Environment Configuration

```yaml
# pytest.ini
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
markers = [
    "unit: Unit tests (fast)",
    "integration: Integration tests (slower)",
    "e2e: End-to-end tests (slowest)",
    "performance: Performance tests",
    "memory: Memory usage tests"
]
```

### 2. Test Execution Profiles

```bash
# Fast feedback (unit tests only)
pytest -m unit

# Pre-commit (unit + integration)
pytest -m "unit or integration"

# Full suite (CI/CD)
pytest

# Performance validation
pytest -m performance --benchmark
```

### 3. CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: |
          pytest --cov=services --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

## Test Quality Metrics

### 1. Coverage Goals

- **Overall**: >80% line coverage
- **Domain Models**: >95% coverage
- **Services**: >85% coverage
- **API Endpoints**: >90% coverage
- **Integration Points**: >75% coverage

### 2. Test Health Indicators

```python
# Good test characteristics
- Fast execution (<100ms for unit tests)
- Isolated (no shared state)
- Deterministic (same result every run)
- Clear failure messages
- Tests one thing

# Bad test smells
- Flaky tests (intermittent failures)
- Long setup/teardown
- Testing implementation details
- Overly complex assertions
- Hidden dependencies
```

### 3. Test Maintenance

**Regular Review**:
- Remove obsolete tests
- Update tests for API changes
- Refactor complex test code
- Improve test performance

**Test Refactoring Patterns**:
```python
# Before: Repetitive setup
def test_case_1():
    project = Project(name="Test", ...)
    # test logic

def test_case_2():
    project = Project(name="Test", ...)
    # test logic

# After: Shared fixture
@pytest.fixture
def test_project():
    return Project(name="Test", ...)

def test_case_1(test_project):
    # test logic

def test_case_2(test_project):
    # test logic
```

## AI Testing Best Practices

### 1. Confidence Thresholds

```python
# Set appropriate thresholds
CLASSIFICATION_CONFIDENCE_THRESHOLD = 0.8
SEARCH_RELEVANCE_THRESHOLD = 0.7
GENERATION_QUALITY_THRESHOLD = 0.75

# Test against thresholds
assert intent.confidence >= CLASSIFICATION_CONFIDENCE_THRESHOLD
```

### 2. Fallback Testing

```python
async def test_low_confidence_fallback():
    # Given: Ambiguous input
    intent = await classifier.classify("do the thing")
    
    # Then: Low confidence triggers fallback
    if intent.confidence < 0.5:
        assert intent.category == IntentCategory.UNKNOWN
        assert "clarification" in intent.suggested_actions
```

### 3. A/B Testing Framework

```python
class ABTestFramework:
    async def test_prompt_variant(self, variant_a, variant_b, test_cases):
        results_a = []
        results_b = []
        
        for test in test_cases:
            result_a = await self.run_with_prompt(variant_a, test.input)
            result_b = await self.run_with_prompt(variant_b, test.input)
            
            results_a.append(self.score_result(result_a, test.expected))
            results_b.append(self.score_result(result_b, test.expected))
        
        # Statistical comparison
        assert self.is_significant_improvement(results_b, results_a)
```

## Test Documentation

### 1. Test Naming Conventions

```python
# Pattern: test_<scenario>_<expected_outcome>
def test_explicit_project_id_returns_project_without_confirmation():
    """When explicit project_id provided, should return project without confirmation"""
    pass

def test_invalid_project_id_raises_not_found_error():
    """When project_id doesn't exist, should raise ProjectNotFoundError"""
    pass
```

### 2. Test Documentation

```python
class TestWorkflowExecution:
    """
    Test workflow execution engine.
    
    These tests validate that workflows:
    1. Execute tasks in correct order
    2. Handle failures gracefully
    3. Persist state correctly
    4. Emit proper events
    """
    
    async def test_successful_workflow_completion(self):
        """
        Test that a workflow with multiple tasks completes successfully.
        
        Scenario:
        - Create workflow with 3 tasks
        - Execute workflow
        - Verify all tasks completed
        - Verify final status
        """
```

## Troubleshooting Test Issues

### Common Problems and Solutions

1. **Async Test Failures**
   ```python
   # Problem: RuntimeError: This event loop is already running
   # Solution: Use pytest-asyncio
   @pytest.mark.asyncio
   async def test_async_function():
       result = await async_function()
   ```

2. **Database Connection Issues**
   ```python
   # Problem: Connection pool exhausted
   # Solution: Proper cleanup
   @pytest.fixture
   async def db_session():
       session = create_session()
       yield session
       await session.close()
   ```

3. **Flaky AI Tests**
   ```python
   # Problem: Intermittent failures due to AI variance
   # Solution: Statistical validation
   success_count = 0
   for _ in range(10):
       result = await ai_function()
       if result.meets_criteria():
           success_count += 1
   assert success_count >= 8  # 80% success rate
   ```

## Conclusion

This test strategy ensures Piper Morgan maintains high quality through comprehensive testing at all levels. By combining traditional testing practices with AI-specific patterns, we can build confidence in both deterministic and probabilistic components of the system.

Key takeaways:
1. Test-first development prevents architectural drift
2. Multiple test levels provide comprehensive coverage
3. AI components need statistical validation approaches
4. Good test hygiene enables confident refactoring
5. Performance testing prevents degradation

Regular review and updates of this strategy ensure it evolves with the system's needs.
---
*Last Updated: June 27, 2025*

## Revision Log
- **June 27, 2025**: Added systematic documentation dating and revision tracking
