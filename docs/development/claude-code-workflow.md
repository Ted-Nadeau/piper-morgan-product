# Claude Code Workflow Patterns

**Date:** 2025-07-23
**Author:** Claude Code
**Version:** 1.0

This document captures the workflow patterns, best practices, and coordination strategies learned through several weeks of development work on Piper Morgan, including recent major implementations (PM-038, PM-039, Foundation Sprint, PM-012).

---

## Table of Contents

1. [Typical Usage Patterns](#typical-usage-patterns)
2. [File Management](#file-management)
3. [Coordination Patterns](#coordination-patterns)
4. [Best Practices](#best-practices)
5. [Common Pitfalls](#common-pitfalls)
6. [Integration Points](#integration-points)

---

## Typical Usage Patterns

### When Claude Code is Most Effective

**1. Systematic Implementation Tasks**
- Multi-file architectural changes requiring coordination
- Configuration pattern migrations (e.g., ADR-010 implementation)
- Database schema updates with enum additions
- End-to-end feature implementation with testing

**Example from PM-012:**
```
Mission: Transform GitHub API from prototype to production utility
Scope: 8 files modified, 3 new components, database schema updates
Result: 85% → 100% production readiness in single session
```

**2. Research and Analysis Tasks**
- Codebase exploration for understanding existing patterns
- Architecture decision research and documentation
- Integration point analysis across multiple services
- Legacy code assessment and modernization planning

**3. Production Deployment Preparation**
- Configuration documentation creation
- User guide development
- Deployment checklist creation
- Error handling and user experience polish

### Optimal Session Structure

**Morning Sessions (10:00-12:00 PM):**
- High-complexity implementation work
- Architectural changes requiring focus
- Multi-component integration tasks

**Afternoon Sessions (2:00-4:00 PM):**
- Documentation completion
- Production readiness tasks
- Testing and validation work
- Cleanup and commit preparation

---

## File Management

### Multi-File Change Coordination

**Pattern: Dependency-First Implementation**
```
1. Domain models (services/domain/models.py)
2. Shared types and enums (services/shared_types.py)
3. Configuration services (following ADR-010)
4. Implementation components
5. Integration layer updates
6. Database schema migrations
7. Testing and validation
```

**Example from PM-012 GitHub Implementation:**
- Added `ProjectContext` to domain models first
- Extended `TaskType` enum in shared_types
- Created `GitHubConfigService` following ADR-010
- Implemented `ProductionGitHubClient` with config service
- Updated `OrchestrationEngine` integration
- Added database enum: `ALTER TYPE tasktype ADD VALUE 'GENERATE_GITHUB_ISSUE_CONTENT'`
- Comprehensive testing and validation

### Commit Strategy

**Single Cohesive Commits:**
- Group related changes into logical units
- Include all supporting files (models, configs, integrations)
- Ensure each commit represents a complete, working feature
- Use descriptive commit messages with context

**Template:**
```
PM-XXX: [Feature Description] - [Impact Summary]

- [Technical change 1]
- [Technical change 2]
- [Configuration/infrastructure changes]
- [Testing and validation completed]

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Coordination Patterns

### Working with Cursor

**Handoff Protocol:**
1. **Preparation Phase (Cursor):** Requirements analysis, architecture scouting, risk assessment
2. **Implementation Phase (Claude Code):** Systematic implementation, testing, integration
3. **Validation Phase (Both):** Code review, production readiness verification

**Information Transfer:**
- GitHub issues as single source of truth
- Preparation reports inform implementation approach
- Implementation findings feed back to architectural understanding
- Session logs maintain continuity across tool switches

**Example from PM-015 Group 3:**
```
Cursor Phase: ADR-010 analysis, FeatureFlags utility research
Claude Code Phase: Implementation using preparation work, 100% test success
Result: Minimized implementation time through preparation coordination
```

### Receiving Instructions

**Optimal Instruction Format:**
```
Mission: [Clear objective]
Priority Tasks: [Ordered list with success criteria]
Strategic Context: [Why this matters, how it fits bigger picture]
Constraints: [Budget, time, compatibility requirements]
Success Criteria: [Specific measurable outcomes]
```

**Multi-Agent Coordination:**
- Reference GitHub issues for complete context
- Build on previous agent work rather than duplicating
- Document how preparation work influenced implementation
- Update GitHub issues with findings and results

---

## Best Practices

### Technical Implementation

**1. Follow Established Patterns**
```python
# ADR-010 Configuration Pattern (Good)
def __init__(self, config_service: GitHubConfigService):
    self.config_service = config_service

# Direct environment access in application layer (Avoid)
def __init__(self):
    self.token = os.getenv("GITHUB_TOKEN")
```

**2. Domain-Driven Development**
- Start with domain models and shared types
- Business logic belongs in domain services
- Infrastructure concerns separated from domain logic
- Database schema generated from domain models

**3. Comprehensive Testing**
- Test imports and basic functionality first
- Create integration tests for complex workflows
- Validate end-to-end scenarios before committing
- Include fallback and error handling tests

### Process Management

**1. Todo List Discipline**
- Use TodoWrite tool for complex multi-step tasks
- Mark tasks complete immediately upon finishing
- Only one task "in_progress" at a time
- Add new tasks discovered during implementation

**2. Progressive Implementation**
- Start with simplest working version
- Add complexity incrementally
- Test each increment before proceeding
- Maintain working state throughout development

**3. Documentation Integration**
- Update documentation alongside code changes
- Create user guides for production features
- Document configuration requirements clearly
- Include examples and troubleshooting guidance

---

## Common Pitfalls

### Technical Pitfalls

**1. Configuration Management**
```python
# Antipattern: Mixed configuration approaches
class Service:
    def __init__(self):
        self.token = config_service.get_token()  # ConfigService
        self.timeout = os.getenv("TIMEOUT")      # Direct access - inconsistent!

# Correct: Consistent ADR-010 pattern
class Service:
    def __init__(self, config_service: ConfigService):
        self.config = config_service.get_service_config()
```

**2. Database Schema Synchronization**
- Always check if new enums exist in database before using
- Add missing enum values with `ALTER TYPE` statements
- Test enum additions before deploying application changes
- Consider migration order for production deployments

**3. Import and Dependency Issues**
- Read files before making assumptions about available classes
- Check existing imports and naming conventions
- Verify all dependencies exist before implementing features
- Test imports in isolation before integration

### Process Pitfalls

**1. Incomplete Context Analysis**
- Always read GitHub issues completely before starting
- Look for preparation work from other agents
- Check for related issues and dependencies
- Verify current status and recent updates

**2. Premature Optimization**
- Implement working solution first
- Add production features incrementally
- Test basic functionality before adding complexity
- Maintain backward compatibility during transitions

**3. Documentation Neglect**
- Update documentation alongside code changes
- Don't defer user guides until "later"
- Include configuration examples and setup instructions
- Test documentation accuracy before committing

---

## Integration Points

### Three-AI Orchestra Coordination

**Role Definitions:**
- **Cursor:** Analysis, scouting, architectural exploration, risk assessment
- **Claude Code:** Systematic implementation, integration, testing, production preparation
- **User:** Strategic direction, requirements clarification, quality validation

**Coordination Mechanisms:**
1. **GitHub Issues:** Authoritative source of requirements and progress
2. **Session Logs:** Continuity and context preservation
3. **Preparation Reports:** Analysis findings to inform implementation
4. **Handoff Prompts:** Structured context transfer between tools

### Workflow Integration Points

**With Project Management:**
- PM issue tracking and progress updates
- Roadmap impact assessment and reporting
- Stakeholder communication through clear documentation
- Success metrics tracking and validation

**With Development Process:**
- Git workflow integration with meaningful commits
- Testing integration with existing test suites
- Configuration management following established patterns
- Deployment preparation with production readiness checklists

**With Quality Assurance:**
- End-to-end testing and validation
- Error handling and edge case coverage
- Performance impact assessment
- User experience validation

---

## Recent Success Examples

### PM-012: GitHub API Design + High-Impact Implementation
**Context:** Transform prototype GitHub integration to production utility
**Approach:** Systematic three-priority implementation with ADR-010 patterns
**Result:** 85% → 100% production readiness, comprehensive testing suite
**Key Pattern:** LLM integration → Production client → Configuration migration

### Foundation Sprint: Python 3.11 + ADR-010 + Cleanup
**Context:** Establish consistent development foundation
**Approach:** Version standardization, configuration patterns, architectural debt reduction
**Result:** Consistent development environment, established patterns for future work
**Key Pattern:** Infrastructure first → Pattern establishment → Debt reduction

### PM-039: Intent Classification Coverage
**Context:** Complete intent classification system with comprehensive patterns
**Approach:** Action unification, fuzzy matching, comprehensive test coverage
**Result:** Production-ready intent system with robust pattern matching
**Key Pattern:** Domain analysis → Implementation → Comprehensive testing

---

## Continuous Improvement

This document represents current understanding based on several weeks of development work. It should be updated regularly as new patterns emerge and lessons are learned.

**Next Evolution Areas:**
- Integration with GitHub Actions for automated testing
- Enhanced coordination protocols for complex multi-session projects
- Performance optimization patterns for large-scale implementations
- Advanced testing strategies for AI-powered components

**Feedback Integration:**
- User experience insights from production deployments
- Performance lessons from real-world usage
- Coordination efficiency improvements from multi-agent work
- Quality enhancement strategies from production incidents

---

*This document is a living guide that evolves with our development practices and learned experiences.*
