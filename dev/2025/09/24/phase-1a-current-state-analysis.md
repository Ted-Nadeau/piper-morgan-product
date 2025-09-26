# Agent Prompt: LLM Regression Phase 1A - Current State Analysis

**Mission**: Verify the LLM regression and capture exact error details to confirm root cause investigation path.

## Context from Lead Developer
- **API Keys confirmed present** in .env file (ANTHROPIC_API_KEY and OPENAI_API_KEY)
- **Historical context**: LLM JSON parsing worked in first month of project (July timeframe, during PM-011)
- **Current issue**: Performance test failing with `LowConfidenceIntentError` due to malformed JSON
- **Critical insight**: Keys exist but tests fail - suggests loading mechanism broken, not missing keys

## Investigation Tasks

### 1. Reproduce Current Error State
```bash
# Run the exact failing test
PYTHONPATH=. python -m pytest tests/regression/test_queryrouter_lock.py::test_performance_requirement_queryrouter_initialization_under_500ms -xvs

# Capture complete output including:
# - Full error message and stack trace
# - Any JSON parsing error details
# - Performance timing if available
# - Any API-related error messages
```

### 2. Verify API Key Loading Mechanism
```python
# Quick test script to check key loading
import os
from pathlib import Path

print("=== Environment API Key Check ===")
# Check if keys visible in Python environment
anthropic_key = os.environ.get('ANTHROPIC_API_KEY', 'NOT_FOUND')
openai_key = os.environ.get('OPENAI_API_KEY', 'NOT_FOUND')

print(f"ANTHROPIC_API_KEY: {'Present' if anthropic_key != 'NOT_FOUND' else 'Missing'}")
print(f"OPENAI_API_KEY: {'Present' if openai_key != 'NOT_FOUND' else 'Missing'}")

if anthropic_key != 'NOT_FOUND':
    print(f"ANTHROPIC_API_KEY length: {len(anthropic_key)} characters")
    print(f"ANTHROPIC_API_KEY prefix: {anthropic_key[:15]}...")

if openai_key != 'NOT_FOUND':
    print(f"OPENAI_API_KEY length: {len(openai_key)} characters") 
    print(f"OPENAI_API_KEY prefix: {openai_key[:15]}...")

# Check .env file accessibility from Python
env_file = Path('.env')
if env_file.exists():
    print(f"\n.env file exists and is readable: {env_file.stat().st_size} bytes")
else:
    print("\n.env file not found from Python working directory")
```

### 3. Test LLM Client Import and Initialization
```python
# Test the actual LLM integration imports
try:
    print("=== LLM Client Import Test ===")
    
    # Test intent classifier import (the failing component)
    from services.intent_service.llm_classifier import LLMClassifier
    print("✅ LLMClassifier import successful")
    
    # Test LLM client imports
    from services.llm.clients import llm_client
    print("✅ LLM client import successful")
    
    # Try to instantiate classifier
    classifier = LLMClassifier()
    print("✅ LLMClassifier instantiation successful")
    
    # Test basic method access (don't call yet)
    if hasattr(classifier, 'classify'):
        print("✅ classify method exists")
    
    if hasattr(classifier, '_parse_llm_response'):
        print("✅ _parse_llm_response method exists")
        
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Instantiation failed: {e}")
    print(f"Error type: {type(e).__name__}")
```

### 4. Check JSON Parsing Logic
```python
# Test the JSON parsing method that's failing
try:
    from services.intent_service.llm_classifier import LLMClassifier
    
    # Test with known good JSON response
    classifier = LLMClassifier()
    
    test_json = '{"category": "task_management", "action": "create_issue", "confidence": 0.95}'
    print(f"Testing JSON parsing with: {test_json}")
    
    # Find the actual parsing method (may be _parse_llm_response or similar)
    if hasattr(classifier, '_parse_llm_response'):
        try:
            result = classifier._parse_llm_response(test_json)
            print(f"✅ JSON parsing successful: {result}")
        except Exception as e:
            print(f"❌ JSON parsing failed: {e}")
    else:
        print("⚠️ _parse_llm_response method not found - check actual method name")
        
except Exception as e:
    print(f"❌ Failed to test JSON parsing: {e}")
```

## Evidence Collection Requirements

### Error Details Report
```
=== Current Error State ===
Test Command: [exact pytest command]
Exit Code: [0 or error code]

Full Error Output:
[paste complete terminal output]

Key Error Patterns Found:
- JSON parsing error: [yes/no - exact message]
- LowConfidenceIntentError: [yes/no - exact message] 
- API client error: [yes/no - exact message]
- Import/module error: [yes/no - exact message]

Performance Timing:
- Test duration: [seconds]
- Target requirement: <500ms
- Actual performance: [measured time if available]
```

### API Key Status Report  
```
=== API Key Loading Status ===
Environment Variable Check:
- ANTHROPIC_API_KEY: [Present/Missing + length if present]
- OPENAI_API_KEY: [Present/Missing + length if present]

.env File Status:
- File exists: [yes/no]
- File readable: [yes/no]
- File size: [bytes]

Python Environment Access:
- os.environ shows keys: [yes/no]
- Keys loaded correctly: [yes/no]
```

### LLM Integration Status Report
```
=== LLM Integration Status ===
Import Tests:
- LLMClassifier import: [success/failed]
- LLM client import: [success/failed]
- Instantiation: [success/failed + error if failed]

Method Availability:
- classify method: [exists/missing]
- JSON parsing method: [exists/missing - actual method name]

JSON Parsing Test:
- Test JSON: {"category": "task_management", "action": "create_issue", "confidence": 0.95}
- Parsing result: [success/failed + details]
```

## Success Criteria
- [ ] Exact error reproduced and captured
- [ ] API key loading mechanism status confirmed  
- [ ] LLM client integration status verified
- [ ] JSON parsing capability tested in isolation
- [ ] Clear evidence of root cause area (keys vs loading vs parsing vs client)

## Time Estimate
15-20 minutes for complete Phase 1A analysis

## Next Steps After Completion
Report findings to Lead Developer with evidence. Based on results, will determine if issue is:
- API key loading mechanism
- LLM client configuration  
- JSON parsing logic regression
- Environment/dependency issue

**Report all findings with exact output - no interpretation needed, just facts.**
