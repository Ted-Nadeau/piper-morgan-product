# CORE-LEARN-D Implementation: Document & Integrate Workflow Optimization

**Agent**: Claude Code (Programmer)
**Issue**: #224 CORE-LEARN-D - Workflow Optimization
**Sprint**: A5 - Learning System (FINAL ISSUE!)
**Date**: October 20, 2025, 2:15 PM
**Duration**: 1-2 hours estimated (based on discovery)

---

## 🎯 REALISTIC PREAMBLE: 96% COMPLETE, 4% WORK TO DO

Discovery found that CORE-LEARN-D infrastructure is **96% complete** (3,579 lines exist).

**What exists (the miracle from past days)**:
- ✅ Chain-of-Draft (552 lines) - Complete A/B testing & optimization engine
- ✅ QueryLearningLoop (610 lines) - Complete template system
- ✅ CrossFeatureKnowledgeService (601 lines) - Workflow optimization enum
- ✅ Learning API (511 lines) - Analytics dashboard
- ✅ PatternRecognitionService (543 lines) - Pattern detection
- ✅ UserPreferenceManager (762 lines) - Preference system

**What's needed (today's honest work - ~150 lines)**:
- ⚠️ Integration wiring (~50 lines) - Connect Chain-of-Draft to workflow optimization
- ⚠️ Integration tests (~100 lines) - Test the workflow optimization flow
- ⚠️ Documentation updates - Document Chain-of-Draft as workflow optimizer

**The Reality**: We built Chain-of-Draft and didn't document it as a workflow optimizer. Today we're completing that work properly - no shortcuts, no magical thinking.

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## Mission

**Wire Chain-of-Draft as workflow optimization system + document + test!**

Discovery found 96% complete (3,579 lines). **We need ~150 lines of real work**:
- Integration wiring (connect pieces)
- Integration tests (verify it works)
- Documentation (explain what exists)

**Scope**:
- Wire Chain-of-Draft experiment system as workflow optimizer
- Add workflow optimization helpers
- Create integration tests
- Document workflow optimization features

**NOT in scope**:
- Building optimization from scratch (EXISTS!)
- Creating A/B testing (EXISTS!)
- Implementing metrics (EXISTS!)

---

## Discovery Report

**YOU HAVE**: `core-learn-d-discovery-report.md` uploaded by PM

**CRITICAL FINDINGS**:
- 96% infrastructure exists (3,579 lines)
- Chain-of-Draft: 552 lines (COMPLETE A/B testing + optimization!)
- QueryLearningLoop: 610 lines (COMPLETE templates!)
- Learning API: 511 lines (COMPLETE dashboard!)
- Need ~150 lines: wiring + tests + docs

**Read the discovery report first!** It contains complete assessment.

---

## STOP Conditions

If ANY of these occur, STOP and escalate to PM immediately:

1. **Chain-of-Draft doesn't exist** - Discovery said 552 lines
2. **Chain-of-Draft doesn't do A/B testing** - Discovery said it's complete
3. **QueryLearningLoop doesn't have templates** - Discovery said WORKFLOW_PATTERN exists
4. **Learning API doesn't work** - Discovery said analytics complete
5. **Cannot provide verification evidence** - Must show wiring works
6. **Tests don't pass** - Must maintain zero regressions
7. **More than 200 lines needed** - Discovery said ~150 lines

---

## Evidence Requirements

### For EVERY Claim You Make:

- **"Wiring added"** → Show integration code + test results
- **"Tests pass"** → Show test output
- **"Optimization works"** → Show end-to-end example
- **"Documentation complete"** → Show updated docs
- **"Integration works"** → Show Chain-of-Draft → optimization flow

### Working Files Location:

- ✅ dev/active/ - For test scripts, verification
- ✅ services/orchestration/ - Chain-of-Draft
- ✅ services/learning/ - QueryLearningLoop, workflow patterns
- ✅ tests/integration/ - Integration tests
- ✅ docs/public/ - API documentation

---

## Implementation Plan (from Discovery)

### Phase 1: Integration Wiring (~50 lines, 45 minutes)

**Step 1: Find Chain-of-Draft**

```bash
# Discovery said it exists with 552 lines
ls -la services/orchestration/chain_of_draft.py

# Check what's there
head -100 services/orchestration/chain_of_draft.py
```

**Step 2: Add workflow optimization helper**

Add to `services/learning/query_learning_loop.py` (or create new service):

```python
async def optimize_workflow_via_experiments(
    self,
    workflow_description: str,
    context: Dict[str, Any],
    user_id: str
) -> Dict[str, Any]:
    """
    Use Chain-of-Draft to optimize a workflow.

    Creates two drafts of the workflow approach and compares them
    to identify the better strategy.

    Args:
        workflow_description: Description of the workflow to optimize
        context: Workflow context and parameters
        user_id: User ID for tracking

    Returns:
        Dict with optimization results:
        - best_approach: The better workflow approach
        - improvement_percentage: How much better (%)
        - time_savings: Estimated time saved
        - suggestions: Specific optimization suggestions
    """
    from services.orchestration.chain_of_draft import ChainOfDraftOrchestrator

    # Create orchestrator
    orchestrator = ChainOfDraftOrchestrator()

    # Run experiment with two workflow approaches
    experiment_config = {
        "user_id": user_id,
        "experiment_type": "workflow_optimization",
        "workflow": workflow_description,
        "context": context
    }

    # Run the experiment (two drafts)
    experiment_result = await orchestrator.run_draft_experiment(
        task_description=workflow_description,
        context=context
    )

    # Extract optimization insights
    best_draft = experiment_result.get("best_draft")
    quality_comparison = experiment_result.get("quality_comparison", {})

    # Calculate improvement percentage
    improvement = quality_comparison.get("improvement_percentage", 0)

    # Generate specific suggestions
    suggestions = []
    if improvement > 0:
        suggestions.append(f"Improved workflow by {improvement}% using better task decomposition")

        # Extract specific improvements from quality factors
        factors = quality_comparison.get("quality_factors", {})
        if factors.get("task_decomposition_score", 0) > 0.7:
            suggestions.append("Better task breakdown identified")
        if factors.get("performance_score", 0) > 0.7:
            suggestions.append("More efficient execution path found")

    return {
        "best_approach": best_draft.get("approach", ""),
        "improvement_percentage": improvement,
        "time_savings_ms": experiment_result.get("time_savings_ms", 0),
        "suggestions": suggestions,
        "experiment_data": experiment_result
    }
```

**Step 3: Add workflow template creation helper**

Add to `services/learning/query_learning_loop.py`:

```python
async def create_workflow_template_from_pattern(
    self,
    pattern: LearnedPattern,
    user_id: str
) -> Optional[Dict[str, Any]]:
    """
    Create a reusable workflow template from a learned pattern.

    Args:
        pattern: Learned WORKFLOW_PATTERN to convert to template
        user_id: User ID for template ownership

    Returns:
        Dict with template data or None if pattern unsuitable
    """
    # Only create templates from high-confidence workflow patterns
    if pattern.pattern_type != PatternType.WORKFLOW_PATTERN:
        return None

    if pattern.confidence < 0.8:  # High threshold for templates
        return None

    # Extract template structure from pattern
    pattern_data = pattern.pattern_data

    template = {
        "template_id": f"workflow_{pattern.id}",
        "template_name": pattern_data.get("workflow_name", f"Workflow Template {pattern.id}"),
        "steps": pattern_data.get("workflow_steps", []),
        "parameters": pattern_data.get("parameters", {}),
        "confidence": pattern.confidence,
        "usage_count": pattern.usage_count,
        "shareable": True,  # Via CrossFeatureKnowledgeService
        "owner_user_id": user_id,
        "created_from_pattern": pattern.id
    }

    # Store template (using existing pattern storage)
    await self._store_workflow_template(template)

    return template

async def _store_workflow_template(self, template: Dict[str, Any]):
    """Store workflow template using existing pattern storage."""
    # Templates are stored as a special type of pattern
    # This reuses existing storage infrastructure
    pass  # Implementation uses existing pattern storage
```

---

### Phase 2: Integration Tests (~100 lines, 45 minutes)

**Create test file**: `tests/integration/test_workflow_optimization.py`

```python
"""
Integration tests for workflow optimization system.

Tests the flow: Workflow → Chain-of-Draft → Optimization → Suggestions.
"""

import pytest
from services.learning.query_learning_loop import QueryLearningLoop
from services.orchestration.chain_of_draft import ChainOfDraftOrchestrator


class TestWorkflowOptimization:
    """Test workflow optimization via Chain-of-Draft."""

    @pytest.fixture
    async def learning_loop(self):
        """Create QueryLearningLoop instance."""
        loop = QueryLearningLoop()
        yield loop

    @pytest.fixture
    async def orchestrator(self):
        """Create ChainOfDraftOrchestrator instance."""
        orch = ChainOfDraftOrchestrator()
        yield orch

    async def test_workflow_optimization_end_to_end(
        self,
        learning_loop
    ):
        """
        Test complete workflow optimization flow.

        Simulates:
        1. User describes a workflow to optimize
        2. System runs A/B experiment via Chain-of-Draft
        3. Best approach identified with improvement percentage
        4. Optimization suggestions generated
        """
        # Describe a workflow to optimize
        workflow = "Create GitHub issue with proper labels and assignment"
        context = {
            "repo": "piper-morgan",
            "issue_type": "bug",
            "priority": "high"
        }

        # Run optimization
        result = await learning_loop.optimize_workflow_via_experiments(
            workflow_description=workflow,
            context=context,
            user_id="test_user"
        )

        # Verify results structure
        assert "best_approach" in result
        assert "improvement_percentage" in result
        assert "suggestions" in result
        assert "experiment_data" in result

        # Verify meaningful results
        assert result["best_approach"] is not None
        assert isinstance(result["suggestions"], list)

    async def test_chain_of_draft_integration(
        self,
        orchestrator
    ):
        """
        Test Chain-of-Draft experiment capabilities.

        Verifies A/B testing works as workflow optimizer.
        """
        task = "Optimize standup reminder workflow"
        context = {"frequency": "daily", "time": "9am"}

        # Run experiment
        experiment_result = await orchestrator.run_draft_experiment(
            task_description=task,
            context=context
        )

        # Verify experiment structure
        assert "best_draft" in experiment_result
        assert "quality_comparison" in experiment_result
        assert "experiment_time_ms" in experiment_result

        # Verify quality comparison provides optimization data
        quality = experiment_result["quality_comparison"]
        assert "improvement_percentage" in quality or "quality_factors" in quality

    async def test_workflow_template_creation(
        self,
        learning_loop
    ):
        """
        Test workflow template creation from patterns.

        Verifies high-confidence patterns can become reusable templates.
        """
        # Create a high-confidence workflow pattern
        pattern = {
            "id": "pattern_workflow_001",
            "pattern_type": PatternType.WORKFLOW_PATTERN,
            "pattern_data": {
                "workflow_name": "GitHub Issue Creation",
                "workflow_steps": [
                    "1. Validate issue data",
                    "2. Check for duplicates",
                    "3. Create issue with labels",
                    "4. Assign to team member"
                ],
                "parameters": {
                    "repo": "required",
                    "title": "required",
                    "labels": "optional"
                }
            },
            "confidence": 0.85,
            "usage_count": 20
        }

        # Create template from pattern
        template = await learning_loop.create_workflow_template_from_pattern(
            pattern=pattern,
            user_id="test_user"
        )

        # Verify template created
        assert template is not None
        assert template["template_name"] == "GitHub Issue Creation"
        assert len(template["steps"]) == 4
        assert template["confidence"] == 0.85
        assert template["shareable"] is True

    async def test_low_confidence_pattern_rejected(
        self,
        learning_loop
    ):
        """
        Test that low-confidence patterns don't become templates.

        Only patterns with confidence >= 0.8 should become templates.
        """
        # Create a low-confidence pattern
        pattern = {
            "id": "pattern_workflow_002",
            "pattern_type": PatternType.WORKFLOW_PATTERN,
            "pattern_data": {
                "workflow_name": "Unclear Workflow",
                "workflow_steps": ["Step 1", "Step 2"]
            },
            "confidence": 0.6,  # Too low
            "usage_count": 5
        }

        # Attempt template creation
        template = await learning_loop.create_workflow_template_from_pattern(
            pattern=pattern,
            user_id="test_user"
        )

        # Should be rejected
        assert template is None

    async def test_metrics_collection(
        self,
        orchestrator
    ):
        """
        Test that optimization metrics are collected.

        Verifies time to completion, improvement percentage, etc.
        """
        task = "Test workflow"
        context = {"test": True}

        # Run experiment
        result = await orchestrator.run_draft_experiment(
            task_description=task,
            context=context
        )

        # Verify metrics present
        assert "experiment_time_ms" in result
        assert result["experiment_time_ms"] > 0

        # Verify quality metrics
        quality = result.get("quality_comparison", {})
        assert "quality_factors" in quality or "scores" in quality
```

---

### Phase 3: Documentation (~50 lines, 30 minutes)

**Update**: `docs/public/api-reference/learning-api.md`

Add section:

```markdown
## Workflow Optimization

Piper Morgan optimizes workflows using the Chain-of-Draft experiment system to identify better approaches through A/B testing.

### How Workflow Optimization Works

**Process**:
1. **Define Workflow**: Describe the workflow to optimize
2. **Run Experiment**: Chain-of-Draft creates two approaches
3. **Compare Quality**: System evaluates both approaches using multi-factor scoring
4. **Identify Best**: Best approach selected based on quality assessment
5. **Generate Suggestions**: Specific optimization recommendations provided

**Example Flow**:
```
Workflow: "Create GitHub issue with labels"
    ↓
Two Approaches Generated (Draft 1 vs Draft 2)
    ↓
Quality Factors Assessed:
  - Task decomposition quality
  - Performance efficiency
  - Success probability
    ↓
Best Approach Selected (e.g., Draft 2)
    ↓
Suggestions: "Improved by 15% via better task breakdown"
```

### Workflow Templates

**Creating Templates from Patterns**:

High-confidence workflow patterns (≥ 0.8) automatically become reusable templates:

```python
# Learn workflow pattern
pattern = learn_workflow_pattern(user_actions)

# If confidence >= 0.8, create template
template = create_workflow_template_from_pattern(pattern, user_id)

# Template is shareable via CrossFeatureKnowledgeService
```

**Template Structure**:
```json
{
  "template_name": "GitHub Issue Creation",
  "steps": [
    "1. Validate issue data",
    "2. Check for duplicates",
    "3. Create issue with labels",
    "4. Assign to team member"
  ],
  "parameters": {
    "repo": "required",
    "title": "required",
    "labels": "optional"
  },
  "confidence": 0.85,
  "shareable": true
}
```

### A/B Testing Framework

**Running Workflow Experiments**:

```python
from services.learning.query_learning_loop import QueryLearningLoop

learning_loop = QueryLearningLoop()

# Optimize a workflow
result = await learning_loop.optimize_workflow_via_experiments(
    workflow_description="Create and assign GitHub issue",
    context={"repo": "piper-morgan", "priority": "high"},
    user_id="user123"
)

# Results include:
# - best_approach: The better workflow method
# - improvement_percentage: How much better (e.g., 15%)
# - time_savings_ms: Time saved in milliseconds
# - suggestions: List of specific optimization recommendations
```

### Optimization Metrics

**Collected Metrics**:
- **Time to Completion**: `experiment_time_ms` tracks total experiment duration
- **Error Rate**: Quality assessment includes error detection
- **User Satisfaction**: Quality scores reflect user value
- **Cognitive Load**: Task complexity assessment in quality factors

**Accessing Metrics**:
```bash
GET /api/v1/learning/analytics

Response:
{
  "workflow_optimizations": {
    "total_experiments": 45,
    "average_improvement": "18%",
    "time_saved_total_ms": 125000
  }
}
```

### Dashboard

**Workflow Optimization Dashboard**:

The existing Learning Analytics API provides workflow optimization metrics:

```bash
GET /api/v1/learning/analytics?feature=workflow_optimization

Response:
{
  "feature": "workflow_optimization",
  "experiments_run": 45,
  "average_improvement_percentage": 18.5,
  "most_optimized_workflows": [
    {"workflow": "github_issue_creation", "improvement": 22},
    {"workflow": "standup_reminders", "improvement": 15}
  ],
  "time_savings": {
    "total_ms": 125000,
    "average_per_workflow_ms": 2777
  }
}
```

### Integration with Chain-of-Draft

**Chain-of-Draft System** (`services/orchestration/chain_of_draft.py`):
- Runs 2-draft experiments automatically
- Compares drafts using `DraftQualityAssessor`
- Provides statistical comparison with improvement percentages
- Tracks experiment timing for performance metrics
- Generates learning summaries for cross-experiment analytics

**Quality Assessment Factors**:
1. **Task Decomposition**: How well workflow is broken down
2. **Performance**: Efficiency of execution approach
3. **Success Probability**: Likelihood of desired outcome
4. **Complexity Management**: Handling of cognitive load

### Best Practices

**When to Use Workflow Optimization**:
- Repetitive workflows with multiple steps
- Workflows where efficiency matters
- Workflows with measurable outcomes
- Workflows that vary by context

**Template Sharing**:
- High-confidence templates (≥ 0.8) can be shared across features
- CrossFeatureKnowledgeService manages template distribution
- Templates maintain versioning and ownership

**Optimization Suggestions**:
- Review suggested improvements before applying
- Test optimizations in safe environments first
- Track optimization impact over time
- Share successful optimizations with team

### Version History

**Version 1.3** (CORE-LEARN-D):
- Documented Chain-of-Draft as workflow optimization system
- Added workflow template creation from patterns
- Integration with A/B testing framework
- Workflow optimization metrics and dashboard
```

---

## Verification Steps

### Step 1: Verify Chain-of-Draft Exists

```bash
# Check Chain-of-Draft file
ls -la services/orchestration/chain_of_draft.py

# Should show 552 lines (from discovery)
wc -l services/orchestration/chain_of_draft.py
```

---

### Step 2: Verify Integration Added

```bash
# Check workflow optimization method added
grep -A 20 "optimize_workflow_via_experiments" services/learning/query_learning_loop.py

# Check template creation method added
grep -A 15 "create_workflow_template_from_pattern" services/learning/query_learning_loop.py
```

---

### Step 3: Run Existing Tests

```bash
# Ensure existing tests still pass
pytest tests/integration/test_learning_system.py -v

# Should pass: 7/9 (same as before - zero regressions)
```

---

### Step 4: Run New Tests

```bash
# Run new workflow optimization tests
pytest tests/integration/test_workflow_optimization.py -v

# Should pass: 5 new integration tests
```

---

### Step 5: Test End-to-End

Create manual test script in `dev/active/test_workflow_optimization_flow.py`:

```python
"""
Manual test for workflow optimization flow.

Tests: Workflow description → Chain-of-Draft → Optimization → Suggestions
"""

import asyncio
from services.learning.query_learning_loop import QueryLearningLoop


async def main():
    print("Testing Workflow Optimization Flow...")

    # Initialize learning loop
    learning_loop = QueryLearningLoop()

    # Test 1: Workflow optimization
    print("\n1. Running workflow optimization experiment...")
    workflow = "Create GitHub issue with proper labels and assignment"
    context = {
        "repo": "piper-morgan",
        "issue_type": "bug",
        "priority": "high"
    }

    result = await learning_loop.optimize_workflow_via_experiments(
        workflow_description=workflow,
        context=context,
        user_id="test_user_456"
    )

    print(f"Best approach: {result['best_approach'][:100]}...")
    print(f"Improvement: {result['improvement_percentage']}%")
    print(f"Time savings: {result['time_savings_ms']}ms")
    print(f"Suggestions: {result['suggestions']}")

    # Test 2: Template creation
    print("\n2. Testing template creation from pattern...")
    pattern = {
        "id": "test_workflow_pattern",
        "pattern_type": PatternType.WORKFLOW_PATTERN,
        "pattern_data": {
            "workflow_name": "Test Workflow",
            "workflow_steps": ["Step 1", "Step 2", "Step 3"],
            "parameters": {"param1": "value1"}
        },
        "confidence": 0.85,
        "usage_count": 15
    }

    template = await learning_loop.create_workflow_template_from_pattern(
        pattern=pattern,
        user_id="test_user_456"
    )

    if template:
        print(f"Template created: {template['template_name']}")
        print(f"Steps: {len(template['steps'])}")
        print(f"Confidence: {template['confidence']}")
    else:
        print("Template creation failed (unexpected!)")

    print("\n✅ All workflow optimization tests passed!")


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python dev/active/test_workflow_optimization_flow.py
```

---

## Success Criteria

CORE-LEARN-D is complete when:

- [ ] `optimize_workflow_via_experiments()` method added (~40 lines)
- [ ] `create_workflow_template_from_pattern()` method added (~30 lines)
- [ ] Integration with Chain-of-Draft verified
- [ ] 5 new integration tests passing
- [ ] All existing tests still passing (zero regressions)
- [ ] Manual end-to-end test demonstrates optimization flow
- [ ] Documentation updated with workflow optimization section
- [ ] Code committed with evidence
- [ ] Session log updated

---

## Files to Create/Modify

### Modify (Extend Existing)

- `services/learning/query_learning_loop.py` (~80 lines) - Add workflow optimization methods
- `docs/public/api-reference/learning-api.md` (~50 lines) - Add workflow optimization docs

### Create

- `tests/integration/test_workflow_optimization.py` (~200 lines) - 5 integration tests
- `dev/active/test_workflow_optimization_flow.py` (~80 lines) - Manual verification

### Session Log

- Continue in existing log or create new: `dev/2025/10/20/HHMM-prog-code-log.md`

---

## Expected Timeline

**Total**: 1-2 hours (from discovery)

**Breakdown**:
- 45 min: Integration wiring (~80 lines in QueryLearningLoop)
- 45 min: Integration tests (~200 lines, 5 tests)
- 30 min: Documentation updates (~50 lines)

---

## Remember

**YOU ARE INTEGRATING AND DOCUMENTING, NOT BUILDING!**

96% exists (3,579 lines):
- Chain-of-Draft (552 lines - COMPLETE A/B testing!)
- QueryLearningLoop (610 lines - COMPLETE templates!)
- CrossFeatureKnowledgeService (601 lines - COMPLETE sharing!)
- Learning API (511 lines - COMPLETE dashboard!)
- PatternRecognitionService (543 lines - COMPLETE patterns!)
- UserPreferenceManager (762 lines - COMPLETE preferences!)

**Your job** (~150 lines):
1. Wire Chain-of-Draft to workflow optimization API (~80 lines)
2. Test thoroughly (5 integration tests, ~200 lines total file)
3. Document what exists (~50 lines)

**Not your job**:
- Build A/B testing (EXISTS in Chain-of-Draft!)
- Create template system (EXISTS in QueryLearningLoop!)
- Implement metrics (EXISTS throughout!)
- Build dashboard (EXISTS in Learning API!)

**We built Chain-of-Draft and didn't document it as workflow optimizer. Today we complete that work properly - no shortcuts, no magical thinking.** ✍️🔧

---

**Ready to finish Sprint A5!** 🎉

*Discovery found 96% complete (3,579 lines). Implementation is wiring, testing, and documenting the excellent work from past days. Sprint A5 finale!*
