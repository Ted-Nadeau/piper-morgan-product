# Issue #332: Application-Layer Stored Procedures Research Report

**Date**: November 22, 2025, 7:08 AM
**Task**: Document application-layer stored procedures pattern
**Phase**: Phase 1 (Research & Audit)
**Status**: ✅ COMPLETE

---

## Executive Summary

The Piper Morgan codebase implements a **"stored procedures" pattern at the application layer** using Python instead of SQL. This design allows workflows to be composed, executed, and modified without database-layer procedures.

**Key Finding**: No database stored procedures (CREATE PROCEDURE, PL/pgSQL) exist in the codebase. All orchestration happens in Python.

---

## Pattern Implementation

### 1. Orchestration Engine (`services/orchestration/engine.py`)

**Location**: lines 63-490
**Primary Method**: `execute_workflow()` (lines 246-311)

**Pattern Elements**:
- **Workflow Composition**: `create_workflow_from_intent()` method builds multi-step procedures from a single intent
- **Task Execution**: `execute_workflow()` executes tasks in dependency order with error handling
- **Task Types**: Explicit task types (ANALYZE_REQUEST, EXTRACT_REQUIREMENTS, IDENTIFY_DEPENDENCIES, GENERATE_DOCUMENTATION, EXECUTE_GITHUB_ACTION)
- **Status Tracking**: Workflow and task status enums track execution state

**Example Flow**:
```python
# OrchestrationEngine converts intent → workflow → execution
1. Intent comes in (e.g., "create github issue")
2. create_workflow_from_intent() builds task sequence
3. execute_workflow() runs each task in order
4. Tasks can depend on previous task results
5. Errors at critical points stop execution
```

**Key Methods**:
- `execute_workflow(workflow)` - Multi-step orchestrated execution
- `create_workflow_from_intent(intent)` - Intent → Workflow translation
- `_execute_task(task, workflow)` - Individual task execution
- `handle_query_intent(intent)` - Query-specific orchestration

---

### 2. Workflow Factory (`services/orchestration/workflow_factory.py`)

**Location**: lines 22-539
**Primary Method**: `create_from_intent()` (lines 137-434)

**Pattern Elements**:
- **Workflow Registry**: Maps intent strings to workflow types
- **Validation Registry**: Context requirements per workflow type
- **Workflow Templates**: Predefined workflows for common patterns

**Example Registry**:
```python
{
    "create_github_issue": WorkflowType.CREATE_TICKET,
    "analyze_data": WorkflowType.ANALYZE_FILE,
    "generate_report": WorkflowType.GENERATE_REPORT,
    "list_projects": WorkflowType.LIST_PROJECTS,
    # ... etc
}
```

**Validation Requirements** (per workflow type):
```python
WorkflowType.CREATE_TICKET: {
    "context_requirements": {
        "critical": ["original_message"],
        "important": ["project_id", "repository"],
        "optional": ["labels", "priority", "assignee"],
    },
    "performance_threshold_ms": 50,
    "pre_execution_checks": ["project_resolution", "repository_access"],
}
```

**Why This Matters**:
- Decouples workflow definition from execution
- Makes workflows discoverable and testable
- Allows context validation before execution begins

---

### 3. Intent Service (`services/intent/intent_service.py`)

**Location**: lines 65-5184
**Primary Method**: `process_intent()` (lines 105-438)

**Pattern Elements**:
- **Intent Classification**: Routes to specific handler based on intent type
- **Intent Handlers**: 25+ handler methods prefixed with `_handle_*_intent`
- **Multi-Step Processing**: Each handler can execute multiple sequential steps

**Intent Handler Examples**:
- `_handle_query_intent()` - Query processing (lines 473-492)
- `_handle_execution_intent()` - Command execution (lines 605-709)
- `_handle_create_issue()` - Issue creation (lines 711-781)
- `_handle_update_issue()` - Issue updates (lines 783-888)
- `_handle_analysis_intent()` - Data analysis (lines 890-942)
- `_handle_strategic_planning()` - Strategic planning (lines 3451-3577)
- `_handle_prioritization()` - Priority calculation (lines 3977-4066)
- `_handle_learn_pattern()` - Pattern learning (lines 4659-4754)

**Pattern in Action**:
```
1. process_intent() dispatches to appropriate handler
2. Handler executes multi-step procedure:
   - Validate input
   - Fetch required data
   - Process/transform
   - Return structured response
3. All without leaving Python application layer
```

---

### 4. Workflow Composition Pattern

**File**: `services/orchestration/workflows.py`
**Status**: File exists but appears empty in current structure

**Conceptual Pattern**:
```python
# Workflows are composed of tasks
Workflow = [
    Task(type=ANALYZE_REQUEST, ...),      # Step 1
    Task(type=EXTRACT_REQUIREMENTS, ...), # Step 2 (depends on Step 1)
    Task(type=IDENTIFY_DEPENDENCIES, ...), # Step 3
    Task(type=GENERATE_DOCUMENTATION, ...), # Step 4
    Task(type=EXECUTE_GITHUB_ACTION, ...), # Step 5
]

# Engine executes in order, with error handling
for task in workflow.tasks:
    result = execute_task(task, workflow)
    if task.critical and result.failed:
        stop_execution()
```

---

## Database Verification

**Search**: Checked all migration files for SQL stored procedures
**Result**: ✅ ZERO database-layer stored procedures found

No files contain:
- `CREATE PROCEDURE`
- `CREATE OR REPLACE FUNCTION`
- `PL/pgSQL` code blocks

**Implication**: All "procedures" are application-layer Python, not database layer.

---

## Pattern Characteristics

| Aspect | Implementation | Benefit |
|--------|----------------|---------|
| **Composition** | Factory pattern + registry | Discoverable, extensible workflows |
| **Execution** | Async task orchestration | Non-blocking, parallel-ready |
| **Error Handling** | Critical task detection | Fail-fast on important errors |
| **State Tracking** | Enum-based status | Clear execution visibility |
| **Context Validation** | Pre-execution checks | Fail early with clear messages |
| **Intent Routing** | Method dispatch pattern | Type-safe intent handling |
| **Multi-Step Logic** | Sequential task execution | Complex procedures as code |

---

## Why This Pattern?

### Trade-off: Application Layer vs Database Layer

**If using SQL stored procedures**:
- ✓ Reduced network round-trips
- ✗ Tightly coupled to PostgreSQL
- ✗ Harder to version control
- ✗ Requires database migration for changes
- ✗ Limited debugging capabilities

**Piper Morgan's choice (Application Layer)**:
- ✓ Database-agnostic
- ✓ Version-controlled with code
- ✓ Testable in isolation
- ✓ Python ecosystem debugging tools
- ✓ Deployable without database changes
- ✗ Slightly more network traffic
- ✗ Requires connection pooling for efficiency

---

## Code Metrics

| Component | Lines | Methods | Key Pattern |
|-----------|-------|---------|-------------|
| OrchestrationEngine | ~428 | 11 | Task orchestration + workflow execution |
| WorkflowFactory | ~518 | 9 | Workflow definition + validation registry |
| IntentService | ~5120 | 65+ | Intent routing + handler dispatch |
| **Total** | **~6066** | **85+** | Application-layer procedure composition |

---

## Related Architecture Decisions

**Relevant ADRs** (if they exist):
- Async execution patterns (workflow execution is async)
- Intent classification system (routes to handlers)
- Error handling strategy (critical task detection)
- Database-agnostic design (no stored procedures)

---

## Findings for ADR

### What to Document

1. **Definition**: Application-layer stored procedures (orchestrated Python workflows)
2. **Benefits**: Flexibility, version control, testability, database agnostic
3. **Trade-offs**: Network latency vs database procedures
4. **Implementation**: OrchestrationEngine, WorkflowFactory, IntentService pattern
5. **Code Examples**:
   - How workflows are created (`WorkflowFactory.create_from_intent()`)
   - How workflows are executed (`OrchestrationEngine.execute_workflow()`)
   - How intents are handled (`IntentService.process_intent()`)

### What NOT to Document

- Specific handler implementations (there are 65+ - document pattern, not each one)
- Database schema (no stored procedures, so not relevant)
- Individual intent types (document the dispatch pattern instead)

---

## Phase 1 Complete ✅

**Research Questions Answered**:
- ✅ What is the pattern? Application-layer procedure composition
- ✅ Where is it implemented? Orchestration, Factory, Intent Service
- ✅ Why this design? Database agnostic, version controlled, testable
- ✅ Are there database procedures? No - pure Python/async
- ✅ How is it different from SQL procedures? Different layer, different benefits

**Next Steps**:
1. Phase 2: Write ADR documenting the pattern and rationale
2. Phase 3: Add code examples showing pattern in action
3. Phase 4: Integrate ADR into documentation structure

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
