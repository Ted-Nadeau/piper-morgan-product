# Anti-Pattern Coverage Gap Analysis

**Date**: January 21, 2026
**Purpose**: Identify patterns without documented anti-patterns to guide future scanning efforts.

---

## Summary

| Metric | Count |
|--------|-------|
| Total Patterns | 58 (001-058, excluding 032) |
| Patterns with Anti-Patterns | 9 |
| Coverage | 15.5% |
| Gap | 49 patterns |

---

## Patterns WITH Anti-Pattern Coverage

These patterns are linked in the anti-pattern index reverse index:

| Pattern | Anti-Patterns | Category |
|---------|---------------|----------|
| [Pattern-035](../docs/internal/architecture/current/patterns/pattern-035-mcp-adapter-methods.md) | I-03, I-04, I-05 | Integration |
| [Pattern-045](../docs/internal/architecture/current/patterns/pattern-045-green-tests-red-user.md) | T-01, T-02, T-03 | Testing |
| [Pattern-046](../docs/internal/architecture/current/patterns/pattern-046-beads-completion-discipline.md) | P-01, P-02 | Process |
| [Pattern-047](../docs/internal/architecture/current/patterns/pattern-047-time-lord-alert.md) | P-03, P-04 | Process |
| [Pattern-049](../docs/internal/architecture/current/patterns/pattern-049-audit-cascade.md) | T-04 | Testing |
| [Pattern-051](../docs/internal/architecture/current/patterns/pattern-051-parallel-place-gathering.md) | G-09 | Grammar |
| [Pattern-052](../docs/internal/architecture/current/patterns/pattern-052-personality-bridge.md) | G-01, G-07 | Grammar |
| [Pattern-053](../docs/internal/architecture/current/patterns/pattern-053-warmth-calibration.md) | G-02 | Grammar |
| [Pattern-054](../docs/internal/architecture/current/patterns/pattern-054-honest-failure.md) | G-05, G-10, I-01, I-02 | Grammar/Integration |

---

## Patterns WITHOUT Anti-Pattern Coverage (Gap)

### Priority 1: Core Architecture (11 patterns)

These foundational patterns likely have implicit anti-patterns worth documenting:

| Pattern | Name | Likely Anti-Patterns |
|---------|------|---------------------|
| 001 | Repository | Direct DB access, mixed query/command |
| 002 | Service | God service, business logic in routes |
| 003 | Factory | Constructor sprawl, hardcoded dependencies |
| 004 | CQRS-lite | Query mutation, command side effects |
| 005 | Transaction Management | Nested transactions, uncommitted reads |
| 007 | Async Error Handling | Swallowed exceptions, unhandled rejections |
| 008 | DDD Service Layer | Anemic domain, service bypass |
| 014 | Error Handling API Contract | Generic errors, missing status codes |
| 015 | Internal Task Handler | Task state leakage, untracked tasks |
| 017 | Background Task Error Handling | Silent failures, zombie tasks |
| 034 | Error Handling Standards | Inconsistent codes, missing context |

### Priority 2: Data & Query (5 patterns)

| Pattern | Name | Likely Anti-Patterns |
|---------|------|---------------------|
| 013 | Session Management | Session leaks, connection exhaustion |
| 016 | Repository Context Enrichment | Over-enrichment, context pollution |
| 023 | Query Layer Patterns | N+1 queries, unbounded results |
| 025 | Canonical Query Extension | Extension overload, unclear ownership |
| 026 | Cross-Feature Learning | Feature coupling, circular learning |

### Priority 3: AI & Intelligence (7 patterns)

| Pattern | Name | Likely Anti-Patterns |
|---------|------|---------------------|
| 012 | LLM Adapter | Prompt injection, hallucination trust |
| 019 | LLM Placeholder Instruction | Placeholder leak, instruction drift |
| 020 | Spatial Metaphor Integration | Metaphor mismatch, context loss |
| 022 | MCP+Spatial Intelligence | Tool sprawl, capability overlap |
| 028 | Intent Classification | Misclassification cascade, intent drift |
| 029 | Multi-Agent Coordination | Agent deadlock, coordination overhead |
| 055-058 | Grammar/Ownership patterns | *(Recently added, need first scan)* |

### Priority 4: Integration & Platform (7 patterns)

| Pattern | Name | Likely Anti-Patterns |
|---------|------|---------------------|
| 018 | Configuration Access | Config sprawl, env coupling |
| 027 | CLI Integration | Argument explosion, inconsistent flags |
| 030 | Plugin Interface | Interface bloat, version coupling |
| 031 | Plugin Wrapper | Wrapper overhead, abstraction leak |
| 033 | Notion Publishing | Sync drift, orphaned pages |
| 040 | Integration Swappability Guide | Leaky abstraction, provider coupling |

### Priority 5: Development & Process (14 patterns)

| Pattern | Name | Likely Anti-Patterns |
|---------|------|---------------------|
| 006 | Verification-First | Verification theater, check skipping |
| 009 | GitHub Issue Tracking | Issue sprawl, orphaned issues |
| 010 | Cross-Validation Protocol | Validation fatigue, false confidence |
| 011 | Context Resolution | Context explosion, implicit coupling |
| 021 | Development Session Management | Session drift, incomplete handoffs |
| 024 | Methodology Patterns | Process ossification, cargo culting |
| 036 | Signal Convergence | Signal noise, false convergence |
| 037 | Cross-Context Validation | Validation blind spots |
| 038 | Temporal Clustering | Spurious clusters, time bias |
| 039 | Feature Prioritization Scorecard | Score gaming, criteria drift |
| 041 | Systematic Fix Planning | Phase creep, scope explosion |
| 042 | Investigation-Only Protocol | Investigation paralysis |
| 043 | Defense-in-Depth Prevention | Security theater, layer overhead |
| 044 | MCP Skill Testing | Test brittleness, mock divergence |

### Priority 6: Infrastructure (1 pattern)

| Pattern | Name | Likely Anti-Patterns |
|---------|------|---------------------|
| 048 | Periodic Background Job | Job pile-up, missed schedules |

### Recently Added (4 patterns - need first scan)

| Pattern | Name | Status |
|---------|------|--------|
| 055 | Multi-Intent Decomposition | Not yet scanned |
| 056 | Consciousness Attribute Layering | Not yet scanned |
| 057 | Grammar-Driven Classification | Not yet scanned |
| 058 | Ownership Graph Navigation | Not yet scanned |

---

## Recommendations

### For Next Pattern Sweep (Feb 3, 2026)

**Focus Areas**:
1. **Core Architecture (P1)** - Highest impact, foundational patterns
2. **AI & Intelligence (P3)** - Growing importance, LLM-specific risks
3. **Recently Added (055-058)** - First-time scan needed

**Expected Yield**: 15-25 new anti-patterns based on Phase 2 experiment precision rates.

### For Ongoing Documentation

When writing or updating patterns, add "Anti-Patterns" section with:
- Common misuses
- What NOT to do
- Links to existing anti-patterns if applicable

### Coverage Target

**Goal**: 50% coverage (29 patterns) by end of Q1 2026
**Current**: 15.5% (9 patterns)
**Gap to close**: 20 patterns

---

## Cross-Reference: ADRs Without Anti-Pattern Coverage

ADRs scanned in pilot: 8
ADRs with anti-patterns documented: 7 (005, 006, 010, 028, 039, 040, 043, 051)
Total ADRs: 56

**ADR Coverage**: 12.5%

---

*Analysis complete. Ready for integration into anti-pattern index.*
