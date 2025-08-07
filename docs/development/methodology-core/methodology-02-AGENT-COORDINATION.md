# Agent Coordination Patterns - MANDATORY

## Strategic Agent Deployment

### Claude Code Deployment
Best for:
- Multi-file systematic changes
- Test creation and infrastructure
- Architecture and design work
- Pattern discovery across codebase

```bash
# Code deployment template:
Please implement [task] following our systematic methodology.

VERIFY FIRST:
1. [specific verification commands]
2. [pattern discovery commands]

OBJECTIVE: [clear single goal]

SUCCESS CRITERIA: [measurable outcome]
```

### Cursor Deployment
Best for:
- Targeted single-file fixes
- UI testing and debugging
- Quick iterations with verification
- Documentation updates

```bash
# Cursor deployment template:
Please fix [specific issue] with TDD approach.

MANDATORY VERIFICATION:
1. [exact test to write]
2. [exact file to modify]

NO ASSUMPTIONS - verify everything.
```

## Coordination Protocol
1. Create GitHub issue FIRST
2. Assign to appropriate agent
3. Monitor progress via commits
4. Verify completion with evidence
5. Update tracking documents

## Proven Parallel Deployment Patterns (August 5, 2025 Validation)

### Claude Code Strengths (High Context)
- **Multi-file systematic implementations**: PM-034 LLM classifier (500+ lines)
- **GitHub Actions management**: CI/CD pipeline deployment
- **Domain model architecture**: Universal List refactoring (1,500+ lines)
- **Database schema design**: Strategic indexing and migration patterns
- **Integration planning**: PM-040 Knowledge Graph connection architecture

### Cursor Strengths (Implementation Focus)
- **API endpoint development**: PM-034 API layer (600+ lines)
- **Testing infrastructure**: Comprehensive test suites (800+ lines)
- **Documentation creation**: Complete API documentation (1,000+ lines)
- **Performance validation**: Empirical testing and benchmarking
- **User experience considerations**: Backward compatibility preservation

### Coordination Success Patterns
- **Strategic Task Decomposition**: Break complex features into parallel tracks
- **Interface Agreement**: Align on domain models before implementation
- **Progress Synchronization**: Regular coordination checkpoints
- **Integration Validation**: Combined testing of parallel work streams

### Example: PM-034 Parallel Success
**Claude Code Track**:
- LLMIntentClassifier service (500+ lines)
- Factory pattern with dependency injection
- Knowledge Graph integration hooks
- Performance benchmarking framework

**Cursor Track**:
- QueryRouter API integration (600+ lines)
- A/B testing framework implementation
- Comprehensive test coverage (30+ tests)
- API documentation (1,000+ lines)

**Result**: Complete feature in 1h 10min with perfect integration
