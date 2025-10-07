# Intent Categories Reference

**Version**: 1.0
**Last Updated**: October 6, 2025
**Coverage**: 13/13 categories (100%)

## Overview

Piper Morgan's intent classification system recognizes 13 distinct intent categories, each routing to specialized handlers optimized for that category's needs.

## Category Architecture

### Fast Path (Canonical Handlers)
**Performance**: ~1ms average response time
**Method**: Pre-classifier pattern recognition
**Use case**: Simple, deterministic queries

### Workflow Path (Orchestration)
**Performance**: 2000-3000ms average response time
**Method**: Full LLM classification + workflow execution
**Use case**: Complex, multi-step operations

---

## Categories (Alphabetical)

### 1. ANALYSIS
**Path**: Workflow
**Purpose**: Data analysis and insights generation
**Performance**: 2000-3000ms

**Example Queries**:
- "Analyze commits from last week"
- "What patterns exist in our code?"
- "Generate a report on test coverage"

**Handler**: `_handle_analysis_intent`
**Actions**: `analyze_commits`, `generate_report`, `analyze_data`
**Tests**: 9 tests (direct + interfaces + contracts)

---

### 2. CONVERSATION
**Path**: Workflow
**Purpose**: Conversational responses and general chat
**Performance**: 2000-3000ms

**Example Queries**:
- "Hey, how's it going?"
- "Tell me a joke"
- "What do you think about X?"

**Handler**: `_handle_conversation_intent`
**Tests**: 9 tests

---

### 3. EXECUTION
**Path**: Workflow
**Purpose**: Action execution and state changes
**Performance**: 2000-3000ms

**Example Queries**:
- "Create GitHub issue for bug fix"
- "Update ticket status to in progress"
- "Deploy to staging"

**Handler**: `_handle_execution_intent`
**Actions**: `create_issue`, `update_issue`
**Tests**: 9 tests

---

### 4. GUIDANCE
**Path**: Fast (Canonical)
**Purpose**: Recommendations and advice
**Performance**: ~1ms

**Example Queries**:
- "How should I approach this problem?"
- "What's the best way to structure this?"
- "Give me advice on X"

**Handler**: Canonical handler in `services/intent_service/canonical_handlers.py`
**Tests**: 9 tests

---

### 5. IDENTITY
**Path**: Fast (Canonical)
**Purpose**: Bot identity and capabilities
**Performance**: ~1ms

**Example Queries**:
- "Who are you?"
- "What can you do?"
- "Tell me about yourself"

**Handler**: Canonical handler
**Tests**: 9 tests

---

### 6. LEARNING
**Path**: Workflow
**Purpose**: Pattern recognition and learning
**Performance**: 2000-3000ms

**Example Queries**:
- "What patterns exist in our workflow?"
- "Learn from these examples"
- "Identify common issues"

**Handler**: `_handle_learning_intent`
**Actions**: `learn_pattern`
**Tests**: 9 tests

---

### 7. PRIORITY
**Path**: Fast (Canonical)
**Purpose**: Priority assessment and focus
**Performance**: ~1ms

**Example Queries**:
- "What's most important right now?"
- "What should I focus on?"
- "Show me top priorities"

**Handler**: Canonical handler
**Tests**: 9 tests

---

### 8. QUERY
**Path**: Workflow
**Purpose**: General information queries
**Performance**: 2000-3000ms

**Example Queries**:
- "What's the weather?"
- "Look up X"
- "Search for Y"

**Handler**: `_handle_query_intent`
**Tests**: 9 tests

---

### 9. STATUS
**Path**: Fast (Canonical)
**Purpose**: Current state and progress
**Performance**: ~1ms

**Example Queries**:
- "Show my standup status"
- "What am I working on?"
- "Current progress?"

**Handler**: Canonical handler
**Tests**: 9 tests

---

### 10. STRATEGY
**Path**: Workflow
**Purpose**: Strategic planning and prioritization
**Performance**: 2000-3000ms

**Example Queries**:
- "Plan next sprint"
- "Create a roadmap"
- "Prioritize backlog"

**Handler**: `_handle_strategy_intent`
**Actions**: `strategic_planning`, `prioritization`
**Tests**: 9 tests

---

### 11. SYNTHESIS
**Path**: Workflow
**Purpose**: Content generation and summarization
**Performance**: 2000-3000ms

**Example Queries**:
- "Generate a summary"
- "Create documentation"
- "Synthesize these notes"

**Handler**: `_handle_synthesis_intent`
**Actions**: `generate_content`, `summarize`
**Tests**: 9 tests

---

### 12. TEMPORAL
**Path**: Fast (Canonical)
**Purpose**: Time and schedule queries
**Performance**: ~1ms

**Example Queries**:
- "What's on my calendar?"
- "When is my next meeting?"
- "What day is it?"

**Handler**: Canonical handler
**Tests**: 9 tests

---

### 13. UNKNOWN
**Path**: Workflow
**Purpose**: Fallback for unclassifiable input
**Performance**: 2000-3000ms

**Example Queries**:
- "Blarghhh"
- "asdfasdf"
- [Gibberish or unclear input]

**Handler**: `_handle_unknown_intent`
**Response**: Helpful fallback, asks for clarification
**Tests**: 9 tests

---

## Category Selection Guide

### When to Use Each Category

**Need instant response?** → Use Fast Path categories (IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE)

**Need complex operation?** → Use Workflow Path categories (EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING)

**Uncertain classification?** → System will route to UNKNOWN and provide helpful fallback

### Classification Confidence

The classifier assigns confidence scores:
- **High confidence** (>0.9): Direct routing
- **Medium confidence** (0.7-0.9): Validated routing
- **Low confidence** (<0.7): May route to UNKNOWN

## Performance Summary

| Category | Path | Avg Time | Cache Hit Rate |
|----------|------|----------|----------------|
| IDENTITY | Fast | ~1ms | 84.6% |
| TEMPORAL | Fast | ~1ms | 84.6% |
| STATUS | Fast | ~1ms | 84.6% |
| PRIORITY | Fast | ~1ms | 84.6% |
| GUIDANCE | Fast | ~1ms | 84.6% |
| EXECUTION | Workflow | 2000-3000ms | 84.6% |
| ANALYSIS | Workflow | 2000-3000ms | 84.6% |
| SYNTHESIS | Workflow | 2000-3000ms | 84.6% |
| STRATEGY | Workflow | 2000-3000ms | 84.6% |
| LEARNING | Workflow | 2000-3000ms | 84.6% |
| QUERY | Workflow | 2000-3000ms | 84.6% |
| CONVERSATION | Workflow | 2000-3000ms | 84.6% |
| UNKNOWN | Workflow | 2000-3000ms | 84.6% |

**Cache speedup**: 7.6x for all categories
**Sustained throughput**: 602,907 req/sec
**Validated**: October 6, 2025 (GREAT-4E)

## Test Coverage

Each category has 9 tests:
- 1 direct interface test
- 3 interface tests (Web, Slack, CLI)
- 5 contract tests (performance, accuracy, error, multi-user, bypass)

**Total test coverage**: 126 tests (13 categories × 9 tests + coverage reports)
**Status**: All passing ✅

## Related Documentation

- [ADR-032: Intent Classification Universal Entry](../internal/architecture/current/adrs/adr-032-intent-classification-universal-entry.md)
- [Pattern-032: Intent Pattern Catalog](../internal/architecture/current/patterns/pattern-032-intent-pattern-catalog.md)
- [Intent Classification Guide](../guides/intent-classification-guide.md)
- [Migration Guide](../guides/intent-migration.md)

---

**Document Status**: ✅ Production Ready
**Last Validated**: October 6, 2025 (GREAT-4E)
**Coverage**: 13/13 categories (100%)
