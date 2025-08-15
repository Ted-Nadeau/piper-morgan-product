"""
Multi-Agent Coordinator

Orchestrates multiple AI agents with intelligent task decomposition, parallel deployment,
and Excellence Flywheel methodology enforcement for PM-033d implementation.
"""

import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import structlog

from services.domain.models import Intent, Task, Workflow
from services.shared_types import IntentCategory, TaskStatus, WorkflowType

logger = structlog.get_logger()


class AgentType(Enum):
    """AI Agent types with specific strengths and capabilities"""

    CODE = "code"  # Infrastructure, backend, database, algorithms
    CURSOR = "cursor"  # Testing, UI, documentation, polish
    COORDINATOR = "coordinator"  # Orchestration and coordination only


class TaskComplexity(Enum):
    """Task complexity levels for decomposition strategy"""

    SIMPLE = "simple"  # Single agent, <30 minutes
    MODERATE = "moderate"  # Single agent, 30-120 minutes
    COMPLEX = "complex"  # Multi-agent, >120 minutes or cross-domain


class CoordinationStatus(Enum):
    """Multi-agent coordination status tracking"""

    PENDING = "pending"
    DECOMPOSING = "decomposing"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    MERGING = "merging"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentCapability:
    """Agent capability definition for intelligent assignment"""

    agent_type: AgentType
    strengths: List[str]
    domains: List[str]
    performance_rating: float  # 0.0-1.0
    current_load: int  # 0-100
    availability: bool


@dataclass
class SubTask:
    """Decomposed sub-task for agent assignment"""

    id: str
    title: str
    description: str
    estimated_duration_minutes: int
    complexity: TaskComplexity
    required_capabilities: List[str]
    dependencies: List[str]
    assigned_agent: Optional[AgentType] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class CoordinationResult:
    """Result from multi-agent coordination execution"""

    coordination_id: str
    status: CoordinationStatus
    subtasks: List[SubTask]
    total_duration_ms: int
    success_rate: float
    agent_performance: Dict[AgentType, Dict[str, Any]]
    error_details: Optional[str] = None
    merge_conflicts: List[str] = None


class TaskDecomposer:
    """Intelligent task decomposition with agent strength analysis"""

    def __init__(self):
        self.agent_capabilities = self._initialize_agent_capabilities()

    def _initialize_agent_capabilities(self) -> Dict[AgentType, AgentCapability]:
        """Initialize agent capability definitions based on PM-033d requirements"""
        return {
            AgentType.CODE: AgentCapability(
                agent_type=AgentType.CODE,
                strengths=[
                    "infrastructure",
                    "backend_services",
                    "database_operations",
                    "complex_algorithms",
                    "system_architecture",
                    "performance_optimization",
                    "async_programming",
                    "api_development",
                    "data_processing",
                ],
                domains=[
                    "orchestration",
                    "repositories",
                    "integrations",
                    "mcp_consumer",
                    "database",
                    "queries",
                    "domain_models",
                    "analysis",
                ],
                performance_rating=0.95,
                current_load=0,
                availability=True,
            ),
            AgentType.CURSOR: AgentCapability(
                agent_type=AgentType.CURSOR,
                strengths=[
                    "testing_frameworks",
                    "ui_components",
                    "documentation",
                    "code_polish",
                    "user_experience",
                    "frontend_integration",
                    "test_coverage",
                    "quality_assurance",
                    "refactoring",
                ],
                domains=[
                    "web",
                    "tests",
                    "docs",
                    "ui",
                    "validation",
                    "monitoring",
                    "user_guides",
                    "examples",
                    "integration_testing",
                ],
                performance_rating=0.90,
                current_load=0,
                availability=True,
            ),
        }

    async def decompose_task(self, intent: Intent, context: Dict[str, Any]) -> List[SubTask]:
        """
        Decompose complex task into agent-specific subtasks

        Args:
            intent: The high-level intent to decompose
            context: Additional context for decomposition

        Returns:
            List[SubTask]: Decomposed subtasks ready for agent assignment
        """
        start_time = time.time()
        logger.info("Starting task decomposition", intent_id=intent.id, category=intent.category)

        try:
            # Analyze task complexity
            complexity = self._analyze_complexity(intent, context)

            if complexity == TaskComplexity.SIMPLE:
                # Single subtask, assign to best agent
                return await self._create_simple_subtask(intent, context)

            elif complexity == TaskComplexity.MODERATE:
                # 2-3 subtasks, likely single agent
                return await self._create_moderate_subtasks(intent, context)

            else:  # COMPLEX
                # Multi-agent coordination required
                return await self._create_complex_subtasks(intent, context)

        except Exception as e:
            logger.error("Task decomposition failed", error=str(e), intent_id=intent.id)
            # Fallback: create single task for Code agent
            return [
                SubTask(
                    id=f"{intent.id}_fallback",
                    title=f"Fallback: {intent.description}",
                    description=f"Handle entire task as fallback: {intent.description}",
                    estimated_duration_minutes=60,
                    complexity=TaskComplexity.MODERATE,
                    required_capabilities=["general_programming"],
                    dependencies=[],
                    assigned_agent=AgentType.CODE,
                )
            ]

        finally:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.info("Task decomposition completed", duration_ms=duration_ms)

    def _analyze_complexity(self, intent: Intent, context: Dict[str, Any]) -> TaskComplexity:
        """Analyze task complexity for decomposition strategy"""

        # Check for multi-domain requirements
        domains = self._identify_required_domains(intent, context)
        if len(domains) > 2:
            return TaskComplexity.COMPLEX

        # Check for cross-agent capabilities
        required_caps = self._identify_required_capabilities(intent, context)
        code_caps = set(self.agent_capabilities[AgentType.CODE].strengths)
        cursor_caps = set(self.agent_capabilities[AgentType.CURSOR].strengths)

        if required_caps & code_caps and required_caps & cursor_caps:
            return TaskComplexity.COMPLEX

        # Estimate duration based on intent category and action/message
        estimated_minutes = self._estimate_duration(intent, context)
        if estimated_minutes > 120:
            return TaskComplexity.COMPLEX
        elif estimated_minutes > 30:
            return TaskComplexity.MODERATE
        else:
            return TaskComplexity.SIMPLE

    def _identify_required_domains(self, intent: Intent, context: Dict[str, Any]) -> List[str]:
        """Identify domains required for intent execution"""
        domains = []

        # Intent category mapping
        category_domains = {
            IntentCategory.EXECUTION: ["orchestration", "workflows"],
            IntentCategory.ANALYSIS: ["analysis", "queries"],
            IntentCategory.QUERY: ["queries", "repositories"],
            IntentCategory.STRATEGY: ["domain_models", "analysis"],
        }

        if intent.category in category_domains:
            domains.extend(category_domains[intent.category])

        # Action and message keyword analysis
        text_to_analyze = f"{intent.action} {intent.original_message}".lower()
        domain_keywords = {
            "database": ["database", "repository", "schema", "migration"],
            "ui": ["interface", "frontend", "web", "user"],
            "testing": ["test", "coverage", "validation", "verify"],
            "integration": ["integration", "api", "slack", "github"],
            "documentation": ["docs", "documentation", "guide", "readme"],
        }

        for domain, keywords in domain_keywords.items():
            if any(keyword in text_to_analyze for keyword in keywords):
                domains.append(domain)

        return list(set(domains))

    def _identify_required_capabilities(self, intent: Intent, context: Dict[str, Any]) -> set:
        """Identify capabilities required for intent execution"""
        capabilities = set()
        text_to_analyze = f"{intent.action} {intent.original_message}".lower()

        # Capability keyword mapping
        capability_keywords = {
            "infrastructure": ["infrastructure", "architecture", "system"],
            "backend_services": ["service", "api", "backend"],
            "database_operations": ["database", "schema", "migration", "query"],
            "testing_frameworks": ["test", "testing", "coverage", "validation"],
            "ui_components": ["ui", "interface", "frontend", "web"],
            "documentation": ["docs", "documentation", "guide", "readme"],
            "performance_optimization": ["performance", "optimization", "speed"],
        }

        for capability, keywords in capability_keywords.items():
            if any(keyword in text_to_analyze for keyword in keywords):
                capabilities.add(capability)

        return capabilities

    def _estimate_duration(self, intent: Intent, context: Dict[str, Any]) -> int:
        """Estimate task duration in minutes"""
        base_duration = 30  # Default 30 minutes

        # Category-based duration modifiers
        category_modifiers = {
            IntentCategory.EXECUTION: 1.5,
            IntentCategory.ANALYSIS: 1.0,
            IntentCategory.SYNTHESIS: 2.0,
            IntentCategory.STRATEGY: 1.8,
            IntentCategory.QUERY: 0.5,
        }

        duration = base_duration * category_modifiers.get(intent.category, 1.0)

        # Action and message complexity analysis
        text_to_analyze = f"{intent.action} {intent.original_message}".lower()
        complexity_indicators = [
            "implement",
            "create",
            "build",
            "develop",
            "integrate",
            "optimize",
            "refactor",
            "migrate",
            "enhance",
        ]

        complexity_count = sum(
            1 for indicator in complexity_indicators if indicator in text_to_analyze
        )

        # Each complexity indicator adds 20 minutes
        duration += complexity_count * 20

        return int(duration)

    async def _create_simple_subtask(
        self, intent: Intent, context: Dict[str, Any]
    ) -> List[SubTask]:
        """Create single subtask for simple complexity"""
        required_caps = self._identify_required_capabilities(intent, context)
        best_agent = self._select_best_agent(required_caps)

        return [
            SubTask(
                id=f"{intent.id}_simple",
                title=intent.action,
                description=f"Execute: {intent.action} - {intent.original_message}",
                estimated_duration_minutes=self._estimate_duration(intent, context),
                complexity=TaskComplexity.SIMPLE,
                required_capabilities=list(required_caps),
                dependencies=[],
                assigned_agent=best_agent,
            )
        ]

    async def _create_moderate_subtasks(
        self, intent: Intent, context: Dict[str, Any]
    ) -> List[SubTask]:
        """Create 2-3 subtasks for moderate complexity"""
        subtasks = []

        # Default moderate decomposition pattern
        text_to_analyze = f"{intent.action} {intent.original_message}".lower()
        if "implement" in text_to_analyze:
            # Implementation pattern: Core + Tests
            subtasks.extend(
                [
                    SubTask(
                        id=f"{intent.id}_core",
                        title=f"Core Implementation: {intent.action}",
                        description=f"Implement core functionality for: {intent.action} - {intent.original_message}",
                        estimated_duration_minutes=int(
                            self._estimate_duration(intent, context) * 0.7
                        ),
                        complexity=TaskComplexity.MODERATE,
                        required_capabilities=["infrastructure", "backend_services"],
                        dependencies=[],
                        assigned_agent=AgentType.CODE,
                    ),
                    SubTask(
                        id=f"{intent.id}_tests",
                        title=f"Testing: {intent.action}",
                        description=f"Create comprehensive tests for: {intent.action} - {intent.original_message}",
                        estimated_duration_minutes=int(
                            self._estimate_duration(intent, context) * 0.3
                        ),
                        complexity=TaskComplexity.SIMPLE,
                        required_capabilities=["testing_frameworks"],
                        dependencies=[f"{intent.id}_core"],
                        assigned_agent=AgentType.CURSOR,
                    ),
                ]
            )
        else:
            # General moderate task - single agent
            return await self._create_simple_subtask(intent, context)

        return subtasks

    async def _create_complex_subtasks(
        self, intent: Intent, context: Dict[str, Any]
    ) -> List[SubTask]:
        """Create multi-agent subtasks for complex coordination"""
        subtasks = []
        total_duration = self._estimate_duration(intent, context)

        # Complex coordination pattern: Architecture + Implementation + Integration + Tests
        subtasks.extend(
            [
                SubTask(
                    id=f"{intent.id}_architecture",
                    title=f"Architecture Design: {intent.action}",
                    description=f"Design architecture and interfaces for: {intent.action} - {intent.original_message}",
                    estimated_duration_minutes=int(total_duration * 0.25),
                    complexity=TaskComplexity.MODERATE,
                    required_capabilities=["infrastructure", "system_architecture"],
                    dependencies=[],
                    assigned_agent=AgentType.CODE,
                ),
                SubTask(
                    id=f"{intent.id}_core_implementation",
                    title=f"Core Implementation: {intent.action}",
                    description=f"Implement core business logic for: {intent.action} - {intent.original_message}",
                    estimated_duration_minutes=int(total_duration * 0.4),
                    complexity=TaskComplexity.MODERATE,
                    required_capabilities=["backend_services", "database_operations"],
                    dependencies=[f"{intent.id}_architecture"],
                    assigned_agent=AgentType.CODE,
                ),
                SubTask(
                    id=f"{intent.id}_integration",
                    title=f"Integration & Polish: {intent.action}",
                    description=f"Integration testing and code polish for: {intent.action} - {intent.original_message}",
                    estimated_duration_minutes=int(total_duration * 0.2),
                    complexity=TaskComplexity.SIMPLE,
                    required_capabilities=["testing_frameworks", "code_polish"],
                    dependencies=[f"{intent.id}_core_implementation"],
                    assigned_agent=AgentType.CURSOR,
                ),
                SubTask(
                    id=f"{intent.id}_validation",
                    title=f"Comprehensive Testing: {intent.action}",
                    description=f"Full test suite and validation for: {intent.action} - {intent.original_message}",
                    estimated_duration_minutes=int(total_duration * 0.15),
                    complexity=TaskComplexity.SIMPLE,
                    required_capabilities=["testing_frameworks", "quality_assurance"],
                    dependencies=[f"{intent.id}_integration"],
                    assigned_agent=AgentType.CURSOR,
                ),
            ]
        )

        return subtasks

    def _select_best_agent(self, required_capabilities: set) -> AgentType:
        """Select best agent based on capability match"""
        best_agent = AgentType.CODE  # Default
        best_score = 0.0

        for agent_type, capability in self.agent_capabilities.items():
            # Calculate capability match score
            agent_caps = set(capability.strengths)
            match_score = len(required_capabilities & agent_caps) / max(
                len(required_capabilities), 1
            )

            # Weight by performance rating and availability
            weighted_score = match_score * capability.performance_rating
            if capability.availability:
                weighted_score *= 1.2

            if weighted_score > best_score:
                best_score = weighted_score
                best_agent = agent_type

        return best_agent


class MultiAgentCoordinator:
    """
    Orchestrates multiple AI agents with task decomposition and coordination

    Implements PM-033d core coordination infrastructure with Excellence Flywheel
    methodology enforcement and <1000ms performance targets.
    """

    def __init__(self):
        self.task_decomposer = TaskDecomposer()
        self.coordination_sessions: Dict[str, CoordinationResult] = {}
        self._performance_metrics: List[Dict[str, Any]] = []

    async def coordinate_task(
        self, intent: Intent, context: Dict[str, Any] = None
    ) -> CoordinationResult:
        """
        Main coordination entry point - decompose and coordinate task execution

        Args:
            intent: High-level intent to coordinate
            context: Additional context for coordination

        Returns:
            CoordinationResult: Complete coordination execution results
        """
        start_time = time.time()
        coordination_id = f"coord_{intent.id}_{int(start_time * 1000)}"

        logger.info(
            "Starting multi-agent coordination",
            coordination_id=coordination_id,
            intent_id=intent.id,
        )

        try:
            # Phase 1: Task Decomposition (Excellence Flywheel: Verify First)
            subtasks = await self.task_decomposer.decompose_task(intent, context or {})

            # Phase 2: Agent Assignment Validation
            validated_assignments = await self._validate_agent_assignments(subtasks)

            # Phase 3: Coordination Protocol Setup
            coordination_protocol = await self._setup_coordination_protocol(validated_assignments)

            # Performance check: Must be <1000ms for coordination overhead
            coordination_overhead_ms = int((time.time() - start_time) * 1000)

            result = CoordinationResult(
                coordination_id=coordination_id,
                status=CoordinationStatus.ASSIGNED,
                subtasks=validated_assignments,
                total_duration_ms=coordination_overhead_ms,
                success_rate=1.0,
                agent_performance={
                    AgentType.CODE: {
                        "assigned_tasks": len(
                            [t for t in validated_assignments if t.assigned_agent == AgentType.CODE]
                        )
                    },
                    AgentType.CURSOR: {
                        "assigned_tasks": len(
                            [
                                t
                                for t in validated_assignments
                                if t.assigned_agent == AgentType.CURSOR
                            ]
                        )
                    },
                },
            )

            # Store coordination session
            self.coordination_sessions[coordination_id] = result

            # Performance target validation
            if coordination_overhead_ms < 1000:
                logger.info(
                    "Coordination performance target achieved",
                    duration_ms=coordination_overhead_ms,
                    target=1000,
                )
            else:
                logger.warning(
                    "Coordination performance target missed",
                    duration_ms=coordination_overhead_ms,
                    target=1000,
                )

            return result

        except Exception as e:
            error_result = CoordinationResult(
                coordination_id=coordination_id,
                status=CoordinationStatus.FAILED,
                subtasks=[],
                total_duration_ms=int((time.time() - start_time) * 1000),
                success_rate=0.0,
                agent_performance={},
                error_details=str(e),
            )

            logger.error(
                "Multi-agent coordination failed", coordination_id=coordination_id, error=str(e)
            )

            return error_result

    async def _validate_agent_assignments(self, subtasks: List[SubTask]) -> List[SubTask]:
        """Validate and optimize agent assignments for Excellence Flywheel compliance"""

        validated_tasks = []
        for subtask in subtasks:
            # Excellence Flywheel: Verify assignment logic
            if subtask.assigned_agent is None:
                # Auto-assign based on capabilities
                required_caps = set(subtask.required_capabilities)
                subtask.assigned_agent = self.task_decomposer._select_best_agent(required_caps)

            # Validate assignment makes sense
            agent_caps = self.task_decomposer.agent_capabilities[subtask.assigned_agent]
            capability_match = any(
                cap in agent_caps.strengths for cap in subtask.required_capabilities
            )

            if not capability_match:
                logger.warning(
                    "Suboptimal agent assignment detected",
                    subtask_id=subtask.id,
                    assigned_agent=subtask.assigned_agent.value,
                )
                # Reassign to better agent
                subtask.assigned_agent = self.task_decomposer._select_best_agent(
                    set(subtask.required_capabilities)
                )

            validated_tasks.append(subtask)

        return validated_tasks

    async def _setup_coordination_protocol(self, subtasks: List[SubTask]) -> Dict[str, Any]:
        """Setup communication protocols for agent coordination"""

        # Build dependency graph
        dependency_graph = {}
        for subtask in subtasks:
            dependency_graph[subtask.id] = {
                "dependencies": subtask.dependencies,
                "assigned_agent": subtask.assigned_agent,
                "estimated_duration": subtask.estimated_duration_minutes,
            }

        # Identify parallel execution opportunities
        parallel_groups = self._identify_parallel_groups(dependency_graph)

        # Setup communication channels (placeholder for future implementation)
        communication_protocol = {
            "coordination_method": "sequential_with_handoffs",
            "dependency_graph": dependency_graph,
            "parallel_groups": parallel_groups,
            "handoff_protocol": "github_branch_integration",
            "status_reporting": "real_time_coordination_updates",
        }

        return communication_protocol

    def _identify_parallel_groups(self, dependency_graph: Dict[str, Any]) -> List[List[str]]:
        """Identify tasks that can be executed in parallel"""

        parallel_groups = []
        processed_tasks = set()

        # Simple parallel identification: tasks with no dependencies can run together
        no_deps = [
            task_id
            for task_id, info in dependency_graph.items()
            if not info["dependencies"] and task_id not in processed_tasks
        ]

        if len(no_deps) > 1:
            parallel_groups.append(no_deps)
            processed_tasks.update(no_deps)

        # TODO: More sophisticated parallel analysis for dependent task chains

        return parallel_groups

    async def get_coordination_status(self, coordination_id: str) -> Optional[CoordinationResult]:
        """Get status of ongoing coordination session"""
        return self.coordination_sessions.get(coordination_id)

    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get coordination performance metrics for monitoring"""

        if not self.coordination_sessions:
            return {"total_coordinations": 0, "average_latency_ms": 0}

        sessions = list(self.coordination_sessions.values())
        total_sessions = len(sessions)
        average_latency = sum(s.total_duration_ms for s in sessions) / total_sessions
        success_rate = (
            sum(1 for s in sessions if s.status != CoordinationStatus.FAILED) / total_sessions
        )

        return {
            "total_coordinations": total_sessions,
            "average_latency_ms": int(average_latency),
            "success_rate": success_rate,
            "performance_target_met": average_latency < 1000,
            "agent_utilization": {
                "code_agent_tasks": sum(
                    s.agent_performance.get(AgentType.CODE, {}).get("assigned_tasks", 0)
                    for s in sessions
                ),
                "cursor_agent_tasks": sum(
                    s.agent_performance.get(AgentType.CURSOR, {}).get("assigned_tasks", 0)
                    for s in sessions
                ),
            },
        }
