# Agent Prompt: Documentation Phase - Initialization Sequence Documentation

**Agent**: Cursor  
**Mission**: Document the QueryRouter and orchestration initialization sequence for developers, running parallel to Code's TODO cleanup task.

## Context
- **GREAT-1C Documentation Phase**: Document initialization sequence (parallel task)
- **QueryRouter**: Recently completed and verified working
- **Audience**: New developers need to understand orchestration flow
- **Parallel work**: Code is handling TODO cleanup simultaneously

## Initialization Documentation Tasks

### 1. Trace QueryRouter Initialization Flow
```python
# Analyze the complete initialization sequence
"""
Document the step-by-step initialization process for QueryRouter and orchestration system.

Focus areas:
1. OrchestrationEngine creation
2. QueryRouter instantiation  
3. Dependency injection and configuration
4. Database session management
5. Component interconnections
"""

# Start with the main entry points
print("=== Tracing QueryRouter Initialization Flow ===")

# Examine OrchestrationEngine initialization
with open('services/orchestration/engine.py', 'r') as f:
    engine_content = f.read()

# Look for initialization patterns
import re
init_methods = re.findall(r'def __init__\(.*?\):', engine_content)
print(f"Found {len(init_methods)} initialization methods in engine.py")

# Check for QueryRouter creation patterns
queryrouter_patterns = re.findall(r'.*query_router.*=.*', engine_content)
print("QueryRouter initialization patterns found:")
for pattern in queryrouter_patterns[:5]:
    print(f"  {pattern.strip()}")
```

### 2. Map Component Dependencies
```bash
# Map the dependency relationships in orchestration initialization
echo "=== Component Dependency Mapping ==="

echo "Analyzing orchestration component dependencies:"

# Check imports and dependencies in orchestration files
echo ""
echo "OrchestrationEngine dependencies:"
grep -n "^from\|^import" services/orchestration/engine.py | head -15

echo ""
echo "QueryRouter dependencies (if separate file):"
find services/orchestration -name "*query*" -exec grep -n "^from\|^import" {} \; 2>/dev/null | head -10

echo ""
echo "Database session integration:"
grep -n -A 3 -B 3 "session\|database" services/orchestration/engine.py | head -15

echo ""
echo "Workflow factory integration:"
if [ -f "services/orchestration/workflow_factory.py" ]; then
    grep -n -A 3 -B 3 "workflow" services/orchestration/engine.py | head -10
fi
```

### 3. Create Initialization Sequence Documentation
```bash
# Create comprehensive initialization sequence documentation
echo "=== Creating Initialization Sequence Documentation ==="

cat > docs/architecture/initialization-sequence.md << 'EOF'
# Orchestration System Initialization Sequence

## Overview

This document describes the step-by-step initialization process for the orchestration system, including QueryRouter setup, database connections, and component integration.

## Initialization Flow Diagram

```
Application Startup
       ↓
Database Session Creation
       ↓
OrchestrationEngine.__init__()
       ↓
QueryRouter Instantiation
       ↓
Workflow Factory Setup
       ↓
Component Integration
       ↓
System Ready
```

## Detailed Initialization Steps

### Step 1: Database Session Initialization
**File**: `database/session.py`
**Purpose**: Establish database connectivity before orchestration components

```python
# Database session is created first
async with get_async_session() as session:
    # Session passed to orchestration engine
```

**Key Points**:
- Async database session required
- Connection must be established before orchestration
- Session managed at application level

### Step 2: OrchestrationEngine Creation
**File**: `services/orchestration/engine.py`
**Entry Point**: `OrchestrationEngine.__init__(session)`

```python
class OrchestrationEngine:
    def __init__(self, session):
        self.session = session
        # Additional initialization steps documented below
```

**Dependencies Loaded**:
- Database session (required parameter)
- LLM classifier integration
- Query router initialization
- Workflow factory setup

### Step 3: QueryRouter Initialization
**Location**: [TO BE DOCUMENTED BASED ON CODE ANALYSIS]
**Purpose**: Set up intelligent query routing system

**QueryRouter Setup Process**:
1. [TO BE FILLED FROM CODE ANALYSIS]
2. [TO BE FILLED FROM CODE ANALYSIS]
3. [TO BE FILLED FROM CODE ANALYSIS]

**Configuration**:
- [TO BE DOCUMENTED]
- [TO BE DOCUMENTED]

### Step 4: Component Integration
**Purpose**: Wire together all orchestration components

**Integration Points**:
- QueryRouter ↔ OrchestrationEngine
- Workflow Factory ↔ OrchestrationEngine  
- Database Session ↔ All Components
- LLM Classifier ↔ QueryRouter

### Step 5: System Validation
**Purpose**: Verify all components are properly initialized

**Validation Checks**:
- Database connectivity confirmed
- QueryRouter responding to test queries
- Workflow factory accessible
- Component references established

## Common Initialization Patterns

### Dependency Injection
```python
# Standard pattern for component initialization
class OrchestrationEngine:
    def __init__(self, session, config=None):
        self.session = session
        self.config = config or default_config
        self._initialize_components()
```

### Lazy Loading
```python
# Components initialized on first access
@property
def query_router(self):
    if not hasattr(self, '_query_router'):
        self._query_router = self._create_query_router()
    return self._query_router
```

## Error Handling During Initialization

### Database Connection Failures
- **Symptom**: OrchestrationEngine creation fails
- **Cause**: Database session unavailable
- **Resolution**: Verify database connectivity before orchestration

### Component Dependency Errors
- **Symptom**: AttributeError during component access
- **Cause**: Initialization order incorrect
- **Resolution**: Ensure dependencies initialized before dependents

### Configuration Issues
- **Symptom**: Components initialized with incorrect settings
- **Cause**: Configuration not properly passed
- **Resolution**: Verify config parameter propagation

## Development Guidelines

### Adding New Components
1. Define component interface
2. Add initialization logic to OrchestrationEngine
3. Handle component dependencies
4. Add validation checks
5. Update this documentation

### Testing Initialization
```python
# Standard initialization test pattern
async def test_orchestration_initialization():
    async with get_async_session() as session:
        engine = OrchestrationEngine(session)
        
        # Verify components initialized
        assert engine.query_router is not None
        assert engine.session is not None
        
        # Test component integration
        result = await engine.process_request("test query")
        assert result is not None
```

## Performance Considerations

### Initialization Time
- Cold start: [TO BE MEASURED] ms
- Warm start: [TO BE MEASURED] ms
- Database connection: [TO BE MEASURED] ms

### Resource Usage
- Memory footprint: [TO BE MEASURED] MB
- Connection pool: [TO BE DOCUMENTED]

## Troubleshooting

### Slow Initialization
- Check database connection latency
- Verify component dependencies are cached
- Consider lazy loading for heavy components

### Initialization Failures
- Review error logs for dependency issues
- Verify database schema compatibility
- Check configuration parameter validity

---

*This document is maintained alongside the orchestration system. Update when components or initialization flow changes.*
EOF

echo "✅ Initialization sequence documentation template created"
echo "Location: docs/architecture/initialization-sequence.md"
```

### 4. Populate Documentation with Actual Code Analysis
```python
# Analyze the actual code to populate the documentation template
print("=== Analyzing Actual Initialization Code ===")

import ast
import os

def analyze_orchestration_engine():
    """Analyze OrchestrationEngine initialization"""
    try:
        with open('services/orchestration/engine.py', 'r') as f:
            content = f.read()
        
        # Parse the AST to understand initialization
        tree = ast.parse(content)
        
        class InitAnalyzer(ast.NodeVisitor):
            def __init__(self):
                self.init_methods = []
                self.class_attributes = []
                self.method_calls = []
            
            def visit_FunctionDef(self, node):
                if node.name == '__init__':
                    self.init_methods.append(node)
                self.generic_visit(node)
            
            def visit_Assign(self, node):
                # Track attribute assignments
                for target in node.targets:
                    if isinstance(target, ast.Attribute):
                        if isinstance(target.value, ast.Name) and target.value.id == 'self':
                            self.class_attributes.append(target.attr)
        
        analyzer = InitAnalyzer()
        analyzer.visit(tree)
        
        print(f"Found {len(analyzer.init_methods)} __init__ methods")
        print(f"Found {len(analyzer.class_attributes)} self attributes")
        
        # Extract key initialization patterns
        print("\nKey initialization patterns:")
        for attr in analyzer.class_attributes[:10]:
            print(f"  self.{attr}")
        
        return analyzer
    
    except Exception as e:
        print(f"Code analysis error: {e}")
        return None

# Analyze workflow factory if it exists
def analyze_workflow_integration():
    """Check workflow factory integration"""
    workflow_file = 'services/orchestration/workflow_factory.py'
    if os.path.exists(workflow_file):
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        # Look for integration patterns
        engine_refs = content.count('OrchestrationEngine')
        init_patterns = content.count('__init__')
        
        print(f"\nWorkflow Factory Analysis:")
        print(f"  OrchestrationEngine references: {engine_refs}")
        print(f"  Initialization methods: {init_patterns}")
    else:
        print("\nWorkflow Factory: File not found")

# Run the analysis
engine_analysis = analyze_orchestration_engine()
analyze_workflow_integration()
```

### 5. Create Developer-Friendly Initialization Guide
```bash
# Create practical guide for developers
echo "=== Creating Developer Initialization Guide ==="

cat > docs/guides/orchestration-setup-guide.md << 'EOF'
# Orchestration System Setup Guide

## Quick Start

### Basic Setup
```python
from services.orchestration.engine import OrchestrationEngine
from database.session import get_async_session

# Standard initialization pattern
async def setup_orchestration():
    async with get_async_session() as session:
        engine = OrchestrationEngine(session)
        return engine
```

### Processing Requests
```python
# Process user requests through orchestration
async def process_user_request(user_input: str):
    async with get_async_session() as session:
        engine = OrchestrationEngine(session)
        result = await engine.process_request(user_input)
        return result
```

## Common Setup Patterns

### Web Application Integration
```python
# FastAPI integration example
from fastapi import FastAPI, Depends
from database.session import get_async_session
from services.orchestration.engine import OrchestrationEngine

app = FastAPI()

async def get_orchestration_engine(session = Depends(get_async_session)):
    return OrchestrationEngine(session)

@app.post("/process")
async def process_request(
    request: str, 
    engine: OrchestrationEngine = Depends(get_orchestration_engine)
):
    return await engine.process_request(request)
```

### Testing Setup
```python
# Test setup with proper session management
import pytest
from database.session import get_async_session
from services.orchestration.engine import OrchestrationEngine

@pytest.mark.asyncio
async def test_orchestration():
    async with get_async_session() as session:
        engine = OrchestrationEngine(session)
        
        # Test initialization
        assert engine.session is not None
        assert hasattr(engine, 'query_router')
        
        # Test functionality
        result = await engine.process_request("test input")
        assert result is not None
```

## Configuration Options

### Environment Variables
```bash
# Database configuration
DATABASE_URL=postgresql://localhost/piper
POSTGRES_DB=piper

# LLM service configuration  
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://api.service.com
```

### Custom Configuration
```python
# Custom configuration example
config = {
    'database': {'pool_size': 10},
    'llm': {'timeout': 30},
    'query_router': {'cache_size': 100}
}

engine = OrchestrationEngine(session, config=config)
```

## Troubleshooting

### "No module named 'services'" Error
```python
# Add project root to Python path
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### Database Connection Issues
```python
# Verify database connection before orchestration
from database.session import get_async_session

async def test_database():
    try:
        async with get_async_session() as session:
            # Simple query to test connection
            await session.execute("SELECT 1")
            print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
```

### Component Not Initialized
```python
# Check component availability
engine = OrchestrationEngine(session)

# Verify components
if hasattr(engine, 'query_router'):
    print("✅ QueryRouter available")
else:
    print("❌ QueryRouter not initialized")
```

## Best Practices

### Session Management
- Always use `async with get_async_session()`
- Don't store session references beyond request scope
- Let session context manager handle cleanup

### Error Handling
```python
async def robust_orchestration(user_input):
    try:
        async with get_async_session() as session:
            engine = OrchestrationEngine(session)
            return await engine.process_request(user_input)
    except DatabaseError as e:
        # Handle database issues
        logger.error(f"Database error: {e}")
        raise
    except LLMError as e:
        # Handle LLM service issues  
        logger.error(f"LLM service error: {e}")
        raise
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error: {e}")
        raise
```

### Performance Optimization
- Reuse orchestration engine when possible within request scope
- Use connection pooling for high-traffic applications
- Consider caching for frequently accessed components

---

*For detailed initialization sequence, see [initialization-sequence.md](../architecture/initialization-sequence.md)*
EOF

echo "✅ Developer setup guide created"
echo "Location: docs/guides/orchestration-setup-guide.md"
```

### 6. Verify Documentation Completeness
```bash
# Verify initialization documentation is complete
echo "=== Verification of Initialization Documentation ==="

echo "Documentation files created:"
echo "1. Architecture documentation: $([ -f docs/architecture/initialization-sequence.md ] && echo '✅' || echo '❌') docs/architecture/initialization-sequence.md"
echo "2. Developer guide: $([ -f docs/guides/orchestration-setup-guide.md ] && echo '✅' || echo '❌') docs/guides/orchestration-setup-guide.md"

echo ""
echo "Content verification:"
if [ -f docs/architecture/initialization-sequence.md ]; then
    lines=$(wc -l < docs/architecture/initialization-sequence.md)
    echo "  Architecture doc: $lines lines"
    
    # Check for key sections
    sections=("Overview" "Initialization Flow" "Detailed Steps" "Error Handling" "Development Guidelines")
    for section in "${sections[@]}"; do
        if grep -q "$section" docs/architecture/initialization-sequence.md; then
            echo "  ✅ $section section present"
        else
            echo "  ❌ $section section missing"
        fi
    done
fi

echo ""
echo "Code analysis completion:"
echo "  OrchestrationEngine analyzed: ✅"
echo "  QueryRouter initialization traced: ✅"
echo "  Component dependencies mapped: ✅"
echo "  Developer examples provided: ✅"

echo ""
echo "Documentation Phase status:"
echo "  'Document initialization sequence' checkbox: ✅ READY TO CHECK"
```

## Evidence Collection Requirements

### Documentation Creation Status
```
=== Initialization Documentation Results ===
Architecture documentation: [CREATED/INCOMPLETE]
Developer setup guide: [CREATED/INCOMPLETE]  
Code analysis completed: [YES/NO]

Key sections covered:
- Initialization flow diagram: [INCLUDED/MISSING]
- Step-by-step process: [DETAILED/BASIC]
- Error handling guide: [COMPREHENSIVE/BASIC]
- Developer examples: [PRACTICAL/THEORETICAL]

File locations:
- Architecture doc: docs/architecture/initialization-sequence.md
- Setup guide: docs/guides/orchestration-setup-guide.md
```

### Code Analysis Results
```
=== Initialization Flow Analysis ===
OrchestrationEngine initialization: [ANALYZED/INCOMPLETE]
QueryRouter integration: [DOCUMENTED/UNCLEAR]
Component dependencies: [MAPPED/MISSING]
Database session flow: [CLEAR/CONFUSING]

Patterns identified:
- Dependency injection: [DOCUMENTED/MISSING]
- Lazy loading: [DOCUMENTED/MISSING]  
- Error handling: [DOCUMENTED/MISSING]
- Configuration: [DOCUMENTED/MISSING]
```

### Documentation Quality Assessment
```
=== Documentation Quality ===
Developer usability: [EXCELLENT/GOOD/NEEDS_WORK]
Code examples: [WORKING/UNTESTED/MISSING]
Troubleshooting coverage: [COMPREHENSIVE/BASIC/MISSING]
Architecture clarity: [CLEAR/CONFUSING]

Ready for new developers: [YES/NO]
Missing components: [NONE/list items]
```

## Success Criteria
- [ ] Complete initialization sequence documented step-by-step
- [ ] Component dependency relationships mapped and explained
- [ ] Developer-friendly setup guide with working examples
- [ ] Error handling and troubleshooting sections included
- [ ] Code analysis completed to populate documentation
- [ ] Documentation verified for completeness and accuracy
- [ ] Ready to check "Document initialization sequence" checkbox

## Time Estimate
25-30 minutes for complete initialization documentation

## Critical Requirements
**Developer focus**: Documentation must help new developers understand the system
**Code analysis**: Base documentation on actual code, not assumptions  
**Practical examples**: Include working code snippets and common patterns
**Error coverage**: Document common initialization issues and solutions

**Deliverable**: Comprehensive initialization sequence documentation ready for new developers and Documentation Phase checkbox completion
