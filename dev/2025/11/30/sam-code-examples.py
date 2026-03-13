# Code Examples: Sequential Task Orchestration Patterns

# 1. Basic Orchestration Pattern
"""
Core pattern showing how we wrap unreliable AI functions with deterministic control flow
"""

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TaskResult:
    success: bool
    data: Optional[Dict[str, Any]]
    confidence: float
    attempts: int
    error: Optional[str]


class OrchestrationEngine:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.checkpoints = []

    async def execute_with_retry(self, agent, task, context):
        """
        Wrapper pattern for unreliable agent functions
        """
        for attempt in range(self.max_retries):
            try:
                # Add conversational framing (empirically improves performance)
                prompt = self._build_conversational_prompt(task, context, attempt)

                # Execute AI agent (unreliable function)
                result = await agent.execute(prompt)

                # Deterministic validation
                if self._validate_structure(result):
                    return TaskResult(
                        success=True,
                        data=result,
                        confidence=result.get("confidence", 0.5),
                        attempts=attempt + 1,
                        error=None,
                    )

                # Failed validation, enhance context for retry
                context["previous_attempt"] = result
                context["failure_reason"] = self._get_validation_errors(result)

            except Exception as e:
                if attempt == self.max_retries - 1:
                    return TaskResult(
                        success=False, data=None, confidence=0.0, attempts=attempt + 1, error=str(e)
                    )

                # Degradation strategy
                await asyncio.sleep(2**attempt)  # Exponential backoff

        return TaskResult(
            success=False,
            data=None,
            confidence=0.0,
            attempts=self.max_retries,
            error="Max retries exceeded",
        )

    def _build_conversational_prompt(self, task, context, attempt):
        """
        Empirical finding: conversational tone improves agent performance
        """
        if attempt == 0:
            return f"Let's work on this together: {task.description}"
        else:
            # Non-blaming retry message
            return f"I see what you were going for. Let's refine this approach: {task.description}. Consider: {context.get('failure_reason', 'being more explicit')}"


# 2. Sequential Task Decomposition
"""
Shows how complex requests decompose into sequential subtasks
"""


class TaskDecomposer:
    def __init__(self):
        self.task_patterns = {
            "research_and_present": ["research", "analyze", "structure", "generate", "validate"],
            "code_review": [
                "parse",
                "analyze_patterns",
                "identify_issues",
                "suggest_fixes",
                "validate_fixes",
            ],
            "document_creation": ["outline", "draft_sections", "integrate", "edit", "format"],
        }

    async def decompose_and_execute(self, request: str, engine: OrchestrationEngine):
        """
        Main orchestration loop - deterministic control with AI execution
        """
        # Deterministic: Identify task pattern
        pattern = self._identify_pattern(request)
        subtasks = self.task_patterns.get(pattern, ["generic_process"])

        results = []
        context = {"original_request": request}

        for subtask_type in subtasks:
            # Deterministic: Select appropriate agent
            agent = self._select_agent(subtask_type)

            # Deterministic: Prepare task with accumulated context
            task = self._prepare_task(subtask_type, context)

            # AI Execution: Run with retry wrapper
            result = await engine.execute_with_retry(agent, task, context)

            # Deterministic: Checkpoint for rollback capability
            engine.checkpoints.append(
                {"subtask": subtask_type, "result": result, "context": context.copy()}
            )

            if not result.success:
                # Degradation strategy
                if self._can_skip(subtask_type):
                    continue
                else:
                    return self._handle_critical_failure(subtask_type, result)

            # Update context for next task
            context.update(result.data)
            results.append(result)

        return self._integrate_results(results)


# 3. Spatial Dimension Implementation (Simplified)
"""
How spatial dimensions translate to code for agent organization
"""


class SpatialOrchestrator:
    def __init__(self):
        self.dimensions = {
            "proximity": self._calculate_semantic_distance,
            "authority": self._check_permission_level,
            "temporal": self._enforce_sequence_constraints,
            "functional": self._match_capabilities,
            "trust": self._assess_confidence,
            "context": self._gather_relevant_context,
            "ethical": self._validate_boundaries,
            "uncertainty": self._quantify_unknowns,
        }

    def route_to_agent(self, task, available_agents):
        """
        Use spatial dimensions to select optimal agent
        """
        scores = {}

        for agent in available_agents:
            score = 0.0
            for dimension, evaluator in self.dimensions.items():
                # Each dimension contributes to routing decision
                dimensional_score = evaluator(task, agent)
                score += dimensional_score * self._get_dimension_weight(dimension, task)

            scores[agent] = score

        # Deterministic selection based on spatial evaluation
        return max(scores, key=scores.get)

    def _calculate_semantic_distance(self, task, agent):
        """
        Example: Proximity dimension using embeddings
        """
        # In practice: Uses embedding similarity
        task_embedding = self._get_embedding(task.description)
        agent_capability_embedding = self._get_embedding(agent.capability_description)
        return 1.0 - cosine_distance(task_embedding, agent_capability_embedding)


# 4. Error Recovery Patterns
"""
Common failure modes and recovery strategies
"""


class RecoveryStrategies:
    @staticmethod
    async def handle_schema_violation(task, result, engine):
        """
        Pattern: When AI returns malformed data, retry with example
        """
        enhanced_context = {
            "expected_schema": task.output_schema,
            "example_output": task.example_output,
            "actual_output": result,
            "specific_errors": validate_against_schema(result, task.output_schema),
        }

        # Retry with explicit structure guidance
        return await engine.execute_with_retry(
            agent=task.agent, task=task.with_context(enhanced_context), context=enhanced_context
        )

    @staticmethod
    async def handle_timeout(task, engine):
        """
        Pattern: Decompose into smaller chunks
        """
        if task.can_decompose:
            subtasks = task.decompose()
            results = []
            for subtask in subtasks:
                result = await engine.execute_with_retry(
                    agent=task.agent, task=subtask, context={"parent_task": task.id}
                )
                results.append(result)
            return merge_results(results)
        else:
            # Fallback to simpler approach
            return await engine.execute_with_retry(
                agent=get_simpler_agent(task.agent),
                task=task.simplify(),
                context={"degraded": True},
            )


# 5. Multi-Agent Validation Pattern
"""
Using multiple agents to validate critical outputs
"""


class MultiAgentValidator:
    def __init__(self, confidence_threshold: float = 0.8):
        self.confidence_threshold = confidence_threshold

    async def validate_with_consensus(self, primary_result, task, engine):
        """
        Pattern: Run multiple agents in parallel for validation
        """
        validation_agents = self._select_validators(task.type)

        validation_tasks = []
        for agent in validation_agents:
            validation_task = asyncio.create_task(
                engine.execute_with_retry(
                    agent=agent,
                    task=create_validation_task(primary_result, task),
                    context={"mode": "validation"},
                )
            )
            validation_tasks.append(validation_task)

        validations = await asyncio.gather(*validation_tasks)

        # Deterministic consensus logic
        consensus = self._calculate_consensus(validations)

        if consensus.confidence < self.confidence_threshold:
            # Human-in-the-loop escalation
            return await self._escalate_to_human(primary_result, validations)

        return consensus


# Usage Example
"""
How these patterns compose in practice
"""


async def main():
    engine = OrchestrationEngine(max_retries=3)
    decomposer = TaskDecomposer()
    spatial = SpatialOrchestrator()

    # Complex request
    request = "Research recent developments in AI safety and create a presentation for executives"

    # Orchestrate with patterns
    result = await decomposer.decompose_and_execute(request, engine)

    # Validate critical output
    if result.requires_validation:
        validator = MultiAgentValidator()
        validated_result = await validator.validate_with_consensus(result, request, engine)

    return validated_result


# Note: This is simplified from actual implementation
# Full code at: github.com/[your-username]/piper-morgan
