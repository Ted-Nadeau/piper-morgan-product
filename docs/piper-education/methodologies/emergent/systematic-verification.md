# Systematic Verification: "Check First, Implement Second"

## The Anti-Pattern We Discovered

During early Piper development, we repeatedly fell into a costly trap:

```python
# The Anti-Pattern in Action
def implement_feature():
    # Assume interface exists
    assumed_api = SomeAPI()  # Does this exist?

    # Guess method signatures
    result = assumed_api.process_data(data)  # What parameters?

    # Create new patterns
    my_custom_handler = MyHandler()  # Why not use existing?

    # Result: Hours of rework when assumptions proved wrong
```

**Real Examples of Failed Assumptions**:
- Assumed `GitHubIntegration` had `create_issue()` method (it was `create_github_issue()`)
- Created custom error handling when comprehensive framework existed
- Built duplicate configuration management before discovering ADR-010
- Implemented test patterns that conflicted with existing infrastructure

## The Correct Approach

### Verification-First Methodology

**Core Principle**: Never write code based on assumptions about existing infrastructure. Always verify first.

### The Verification Hierarchy

1. **Check if it exists** → 2. **Understand how it works** → 3. **Follow existing patterns** → 4. **Extend if needed**

### Practical Verification Commands

#### 1. Check Class/Function Existence

```bash
# Does this class exist?
rg "class GitHubIntegration" --type py

# What methods does it have?
rg "def.*github" services/integrations/github/ --type py

# What's the exact signature?
grep -A 5 "def create_github_issue" services/integrations/github/client.py
```

#### 2. Understand Existing Patterns

```bash
# How are errors handled in this codebase?
rg "class.*Error" --type py | head -20

# What's the configuration pattern?
find . -name "*config*.py" -type f | grep -v __pycache__

# How are tests structured?
ls -la tests/ | grep -E "(test_|_test\.py)"
```

#### 3. Verify Integration Points

```python
# Before implementing, verify the workflow
from services.orchestration.engine import OrchestrationEngine

# Check available task types
print([task for task in dir(TaskType) if not task.startswith('_')])

# Verify repository methods
from services.repositories.intent_repository import IntentRepository
print([m for m in dir(IntentRepository) if not m.startswith('_')])
```

#### 4. Database Schema Verification

```bash
# Check actual database models
grep -A 10 "class.*Base" services/database/models.py

# Verify enum definitions
grep -A 20 "class.*Enum" services/shared_types.py

# Understand relationships
rg "relationship\(" services/database/models.py
```

## Real-World Application: PM-012

### The Verification Process That Enabled Success

**Morning Audit (10:00 AM)**:
```bash
# 1. Verify GitHub integration exists
$ rg "class GitHub" --type py
services/integrations/github/client.py: class GitHubClient:

# 2. Check existing methods
$ rg "def.*issue" services/integrations/github/
create_github_issue(self, request: CreateGitHubIssueRequest)

# 3. Verify workflow integration
$ rg "GITHUB_CREATE_ISSUE" --type py
services/shared_types.py: GITHUB_CREATE_ISSUE = "github_create_issue"

# 4. Check for LLM integration
$ rg "generate.*content|llm.*issue" --type py
# No results - THIS IS THE 15% GAP!
```

**Result**: Precise identification that ONLY LLM integration was missing.

### Implementation Based on Verification

```python
# Because we verified first, implementation was surgical:

# 1. Extend existing enum (verified location)
# In services/shared_types.py
class TaskType(Enum):
    GENERATE_GITHUB_ISSUE_CONTENT = "generate_github_issue_content"  # NEW

# 2. Use existing patterns (verified from other agents)
# In services/agents/github_content_agent.py
class GitHubContentAgent(BaseAgent):  # Following verified pattern

# 3. Integrate with verified workflow
# In services/orchestration/workflows/github_workflow.py
# Extended existing workflow rather than creating new
```

## Verification Patterns by Category

### 1. Architecture Verification

```bash
# Understand layer boundaries
find . -type f -name "*.py" | grep -E "(domain|application|infrastructure)" | sort

# Check architectural decisions
ls -la docs/architecture/decisions/

# Verify design patterns in use
rg "Repository|Factory|Strategy|Observer" --type py
```

### 2. Configuration Verification

```bash
# Find configuration patterns
find . -name "*config*" -o -name "*settings*" | grep -v cache

# Check environment variables
grep -r "os.environ" . --include="*.py"

# Verify feature flags
rg "FeatureFlags|feature_flag" --type py
```

### 3. Testing Verification

```bash
# Understand test structure
tree tests/ -d -L 2

# Check test patterns
rg "class Test" tests/ | head -10

# Verify fixtures
rg "@pytest.fixture" tests/

# Find test utilities
ls -la tests/test_utils/
```

### 4. Error Handling Verification

```bash
# Find custom exceptions
rg "class.*Exception|class.*Error" --type py

# Check error handling patterns
rg "try:|except.*:" --type py -A 2 | head -20

# Verify logging patterns
rg "logger\." --type py | head -10
```

## Benefits Realized

### Time Savings

**Without Verification**:
- 2 hours implementing wrong interface
- 1 hour debugging integration issues
- 1 hour refactoring to match patterns
- Total: 4 hours wasted

**With Verification**:
- 15 minutes systematic verification
- 45 minutes correct implementation
- 0 minutes rework
- Total: 1 hour productive work

### Quality Improvements

- **Pattern Consistency**: 100% alignment with existing code
- **Integration Success**: First attempt always works
- **Maintenance**: Future developers find familiar patterns
- **Technical Debt**: Zero accumulation from assumptions

## The Verification Checklist

Before implementing ANY feature:

- [ ] **Existence Check**: Does this class/function/pattern already exist?
- [ ] **Interface Verification**: What's the exact method signature?
- [ ] **Pattern Analysis**: How does the codebase handle this type of work?
- [ ] **Integration Points**: Where does this fit in the architecture?
- [ ] **Configuration Check**: Are there existing settings/flags?
- [ ] **Test Patterns**: How should tests be structured?
- [ ] **Error Handling**: What exceptions should be raised/caught?
- [ ] **Documentation**: Are there ADRs or guides to follow?

## Common Verification Mistakes

### 1. Partial Verification
❌ Checking if class exists but not its methods
✅ Full interface verification including parameters and return types

### 2. Surface-Level Checks
❌ Finding one example and assuming it's the pattern
✅ Checking multiple examples to confirm consistent patterns

### 3. Ignoring Context
❌ Verifying technical details without business context
✅ Understanding both technical patterns and domain requirements

### 4. Verification Without Documentation
❌ Keeping verification knowledge in your head
✅ Documenting findings for future reference

## Institutional Impact

### Before Systematic Verification
- 40% of PR feedback about pattern misalignment
- 25% implementation time on rework
- Inconsistent codebase patterns
- Frustrated developers

### After Systematic Verification
- <5% PR feedback on patterns
- <2% rework time
- Consistent, maintainable codebase
- Confident, efficient development

## Tools for Efficient Verification

### Ripgrep Aliases
```bash
# Add to your shell profile
alias rgpy='rg --type py'
alias rgclass='rg "class.*" --type py'
alias rgdef='rg "def.*" --type py'
alias rgenum='rg "class.*Enum" --type py'
```

### Verification Scripts
```python
# Quick pattern checker
def verify_pattern(pattern_type):
    patterns = {
        'repository': 'rg "class.*Repository" --type py',
        'workflow': 'rg "class.*Workflow" --type py',
        'agent': 'rg "class.*Agent" --type py',
        'config': 'find . -name "*config*.py"'
    }
    os.system(patterns.get(pattern_type, ''))
```

## Conclusion

Systematic Verification transforms development from a guessing game into a precise science. The 15 minutes invested in verification saves hours of rework and creates compound benefits through pattern consistency.

Remember: **Every assumption is a future bug**. Every verification is an investment in velocity. The most powerful code is the code you don't have to write because you found it already exists.

When tempted to "just start coding," remember PM-012: 15 minutes of verification enabled a 3-hour complete implementation. That's the power of "Check First, Implement Second."
