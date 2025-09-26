# Agent Prompt: Phase 4B - Implement Resilient JSON Parsing

**Agent**: Code  
**Mission**: Implement the Chief Architect's progressive fallback JSON parsing strategy to handle malformed LLM responses gracefully.

## Context from Chief Architect
- **Reality**: LLM providers will occasionally return malformed JSON under load, even with `response_format`
- **Strategy**: Progressive fallback parsing with multiple recovery strategies
- **Reliability targets**: 99%+ individual, 95%+ normal load, 80%+ extreme load acceptable
- **Max retries**: 2 retries for performance (<500ms requirement)

## Phase 4B Implementation Tasks

### 1. Backup Current Implementation
```python
# Create backup before implementing resilient parsing
import shutil
import datetime

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = f'services/intent_service/llm_classifier.py.phase4b_backup_{timestamp}'

shutil.copy('services/intent_service/llm_classifier.py', backup_file)
print(f"✅ Backup created: {backup_file}")
```

### 2. Implement Progressive Fallback Parsing Method
```python
# Add the resilient parsing method to LLMClassifier
resilient_parser = '''
def _parse_llm_response_resilient(self, response_text: str, attempt: int = 1) -> dict:
    """Parse LLM response with progressive fallback strategies
    
    Strategy progression:
    1. Direct JSON parse (works 95% of time)
    2. Fix common malformations (handles {category: "value"})
    3. Extract JSON from text response 
    4. Retry with stronger prompt (if attempt < 3)
    5. Regex extraction fallback
    6. Final unknown intent fallback
    """
    import re
    import json
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Strategy 1: Direct JSON parse (works 95% of time)
    try:
        parsed = json.loads(response_text)
        logger.debug(f"Parse strategy 1 success: Direct JSON parse")
        return parsed
    except json.JSONDecodeError as e:
        logger.debug(f"Parse strategy 1 failed: {e}")
        pass
    
    # Strategy 2: Fix common malformations (handles {category: "value"})
    try:
        # Replace unquoted keys with quoted keys
        # Handles: {category: "value"} -> {"category": "value"}
        fixed_text = re.sub(r'(\w+):', r'"\\1":', response_text)
        
        # Handle single quotes: {'category': 'value'} -> {"category": "value"}
        fixed_text = re.sub(r"'([^']*)'", r'"\\1"', fixed_text)
        
        parsed = json.loads(fixed_text)
        logger.debug(f"Parse strategy 2 success: Fixed malformed JSON")
        return parsed
    except json.JSONDecodeError as e:
        logger.debug(f"Parse strategy 2 failed: {e}")
        pass
    
    # Strategy 3: Extract JSON from text response
    try:
        # LLM might return "Here's the JSON: {...}" or similar
        json_match = re.search(r'\\{.*\\}', response_text, re.DOTALL)
        if json_match:
            json_text = json_match.group()
            parsed = json.loads(json_text)
            logger.debug(f"Parse strategy 3 success: Extracted JSON from text")
            return parsed
    except json.JSONDecodeError as e:
        logger.debug(f"Parse strategy 3 failed: {e}")
        pass
    
    # Strategy 4: Retry with stronger prompt (if attempt < 3)
    if attempt < 3:
        logger.warning(f"All parsing strategies failed, retrying with stronger prompt (attempt {attempt + 1})")
        return self._retry_with_strict_json_prompt(attempt + 1)
    
    # Strategy 5: Regex extraction fallback
    try:
        # Extract intent/category manually using common patterns
        intent_patterns = [
            r'"?(?:category|intent)"?\\s*:\\s*"?([^",\\}]+)"?',
            r'(CREATE_TASK|QUERY|UPDATE|EXECUTION|ANALYSIS)',
            r'(create_issue|list_projects|update_status|generate_report)'
        ]
        
        action_patterns = [
            r'"?(?:action)"?\\s*:\\s*"?([^",\\}]+)"?',
            r'(create_issue|list_projects|update_status|generate_report|create_milestone)'
        ]
        
        confidence_patterns = [
            r'"?(?:confidence)"?\\s*:\\s*([0-9.]+)',
            r'confidence[^0-9]*([0-9.]+)'
        ]
        
        # Try to extract category/intent
        category = None
        for pattern in intent_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                category = match.group(1).upper()
                break
        
        # Try to extract action
        action = None
        for pattern in action_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                action = match.group(1).lower()
                break
        
        # Try to extract confidence
        confidence = 0.7  # Default lower confidence for parsed responses
        for pattern in confidence_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                try:
                    confidence = float(match.group(1))
                    if confidence > 1.0:  # Handle percentage format
                        confidence = confidence / 100.0
                    break
                except ValueError:
                    pass
        
        if category and action:
            logger.warning(f"Parse strategy 5 success: Regex extraction - {category}/{action}")
            return {
                "category": category,
                "action": action,
                "confidence": confidence,
                "parse_method": "regex_fallback"
            }
            
    except Exception as e:
        logger.error(f"Parse strategy 5 failed: {e}")
        pass
    
    # Strategy 6: Final fallback - Unknown intent
    logger.error(f"All parsing strategies failed. Response text: {response_text[:200]}...")
    return {
        "category": "UNKNOWN",
        "action": "unknown",
        "confidence": 0.0,
        "parse_method": "failed",
        "original_response": response_text[:500]  # Keep sample for debugging
    }

def _retry_with_strict_json_prompt(self, attempt: int) -> dict:
    """Retry classification with stronger JSON formatting instructions"""
    
    # Create a more explicit JSON prompt
    strict_prompt = f"""
You are an intent classifier. Your task is to classify user messages into intents.

CRITICAL: You MUST respond with valid JSON only. No additional text or explanation.

The user message is: "{self.original_message if hasattr(self, 'original_message') else 'message'}"

Your response must be exactly this JSON format with no additional text:
{{"category": "EXECUTION", "action": "create_issue", "confidence": 0.95}}

Valid categories: EXECUTION, QUERY, ANALYSIS, UPDATE
Valid actions: create_issue, list_projects, update_status, generate_report, create_milestone

Respond only with valid JSON:
"""
    
    logger.warning(f"Retrying with strict JSON prompt (attempt {attempt})")
    
    try:
        # Make the retry call with stricter prompt
        response = asyncio.run(self.llm.complete(
            task_type="intent_classification",
            prompt=strict_prompt,
            response_format={"type": "json_object"},
            max_tokens=200,
            temperature=0.1  # Lower temperature for more consistent JSON
        ))
        
        # Parse the retry response
        return self._parse_llm_response_resilient(response, attempt)
        
    except Exception as e:
        logger.error(f"Retry attempt {attempt} failed: {e}")
        # Return to fallback parsing without further retries
        return self._parse_llm_response_resilient("", attempt + 10)  # Skip retry logic
'''

print("Resilient parsing method code prepared")
```

### 3. Add the Resilient Parser to LLM Classifier
```python
# Insert the resilient parsing method into the LLM classifier
print("=== Adding Resilient Parser to LLM Classifier ===")

with open('services/intent_service/llm_classifier.py', 'r') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []

# Find a good place to insert the method (after existing methods)
for i, line in enumerate(lines):
    new_lines.append(line)
    
    # Look for the end of an existing method to insert our new one
    if (line.strip().startswith('def _parse_llm_response') and 
        i + 1 < len(lines) and 
        not lines[i + 1].strip().startswith(' ')):
        
        # Insert the resilient parsing methods here
        resilient_methods = [
            '',
            '    def _parse_llm_response_resilient(self, response_text: str, attempt: int = 1) -> dict:',
            '        """Parse LLM response with progressive fallback strategies"""',
            '        import re',
            '        import json',
            '        import logging',
            '        import asyncio',
            '        ',
            '        logger = logging.getLogger(__name__)',
            '        ',
            '        # Strategy 1: Direct JSON parse (works 95% of time)',
            '        try:',
            '            parsed = json.loads(response_text)',
            '            logger.debug("Parse strategy 1 success: Direct JSON parse")',
            '            return parsed',
            '        except json.JSONDecodeError as e:',
            '            logger.debug(f"Parse strategy 1 failed: {e}")',
            '            pass',
            '        ',
            '        # Strategy 2: Fix common malformations',
            '        try:',
            '            # Replace unquoted keys with quoted keys',
            '            fixed_text = re.sub(r\'(\\w+):\', r\'"\\1":\', response_text)',
            '            # Handle single quotes',
            '            fixed_text = re.sub(r"\'([^\']*)\'"", r\'"\\1"\', fixed_text)',
            '            parsed = json.loads(fixed_text)',
            '            logger.debug("Parse strategy 2 success: Fixed malformed JSON")',
            '            return parsed',
            '        except json.JSONDecodeError:',
            '            pass',
            '        ',
            '        # Strategy 3: Extract JSON from text response',
            '        try:',
            '            json_match = re.search(r\'\\{.*\\}\', response_text, re.DOTALL)',
            '            if json_match:',
            '                json_text = json_match.group()',
            '                parsed = json.loads(json_text)',
            '                logger.debug("Parse strategy 3 success: Extracted JSON from text")',
            '                return parsed',
            '        except json.JSONDecodeError:',
            '            pass',
            '        ',
            '        # Strategy 4: Retry with stronger prompt (if attempt < 3)',
            '        if attempt < 3:',
            '            logger.warning(f"Retrying with stronger prompt (attempt {attempt + 1})")',
            '            return self._retry_with_strict_json_prompt(attempt + 1)',
            '        ',
            '        # Strategy 5: Regex extraction fallback',
            '        category = self._extract_category_regex(response_text)',
            '        action = self._extract_action_regex(response_text)',
            '        confidence = self._extract_confidence_regex(response_text)',
            '        ',
            '        if category and action:',
            '            logger.warning(f"Parse strategy 5 success: Regex extraction")',
            '            return {',
            '                "category": category,',
            '                "action": action,',
            '                "confidence": confidence,',
            '                "parse_method": "regex_fallback"',
            '            }',
            '        ',
            '        # Strategy 6: Final fallback',
            '        logger.error(f"All parsing strategies failed. Response: {response_text[:200]}...")',
            '        return {',
            '            "category": "UNKNOWN",',
            '            "action": "unknown",',
            '            "confidence": 0.0,',
            '            "parse_method": "failed"',
            '        }',
            '',
            '    def _extract_category_regex(self, text: str) -> str:',
            '        """Extract category using regex patterns"""',
            '        patterns = [',
            '            r\'"?(?:category|intent)"?\\s*:\\s*"?([^",\\}]+)"?\',',
            '            r\'(EXECUTION|QUERY|ANALYSIS|UPDATE)\',',
            '        ]',
            '        for pattern in patterns:',
            '            match = re.search(pattern, text, re.IGNORECASE)',
            '            if match:',
            '                return match.group(1).upper()',
            '        return "UNKNOWN"',
            '',
            '    def _extract_action_regex(self, text: str) -> str:',
            '        """Extract action using regex patterns"""',
            '        patterns = [',
            '            r\'"?(?:action)"?\\s*:\\s*"?([^",\\}]+)"?\',',
            '            r\'(create_issue|list_projects|update_status|generate_report)\',',
            '        ]',
            '        for pattern in patterns:',
            '            match = re.search(pattern, text, re.IGNORECASE)',
            '            if match:',
            '                return match.group(1).lower()',
            '        return "unknown"',
            '',
            '    def _extract_confidence_regex(self, text: str) -> float:',
            '        """Extract confidence using regex patterns"""',
            '        patterns = [',
            '            r\'"?(?:confidence)"?\\s*:\\s*([0-9.]+)\',',
            '            r\'confidence[^0-9]*([0-9.]+)\'',
            '        ]',
            '        for pattern in patterns:',
            '            match = re.search(pattern, text, re.IGNORECASE)',
            '            if match:',
            '                try:',
            '                    conf = float(match.group(1))',
            '                    return conf / 100.0 if conf > 1.0 else conf',
            '                except ValueError:',
            '                    pass',
            '        return 0.7  # Default confidence for fallback parsing',
            '',
            '    async def _retry_with_strict_json_prompt(self, attempt: int) -> dict:',
            '        """Retry with stronger JSON formatting instructions"""',
            '        strict_prompt = f"""You are an intent classifier.',
            'CRITICAL: Respond with valid JSON only. No additional text.',
            'User message: "{getattr(self, "current_message", "message")}"',
            'Response format: {{"category": "EXECUTION", "action": "create_issue", "confidence": 0.95}}',
            'Valid categories: EXECUTION, QUERY, ANALYSIS, UPDATE',
            'Respond only with valid JSON:"""',
            '        ',
            '        try:',
            '            response = await self.llm.complete(',
            '                task_type="intent_classification",',
            '                prompt=strict_prompt,',
            '                response_format={"type": "json_object"},',
            '                max_tokens=200,',
            '                temperature=0.1',
            '            )',
            '            return self._parse_llm_response_resilient(response, attempt)',
            '        except Exception as e:',
            '            logger.error(f"Retry attempt {attempt} failed: {e}")',
            '            return self._parse_llm_response_resilient("", attempt + 10)',
            ''
        ]
        
        new_lines.extend(resilient_methods)
        break

# Write the updated file with resilient parsing
with open('services/intent_service/llm_classifier.py', 'w') as f:
    f.write('\n'.join(new_lines))

print("✅ Resilient parsing methods added to LLM classifier")
```

### 4. Update Existing Parse Method to Use Resilient Parser
```python
# Modify the existing _parse_llm_response method to use resilient parsing
print("=== Updating Existing Parse Method ===")

with open('services/intent_service/llm_classifier.py', 'r') as f:
    content = f.read()

# Replace the existing _parse_llm_response call with resilient version
updated_content = content.replace(
    'self._parse_llm_response(',
    'self._parse_llm_response_resilient('
)

# Also store the current message for retry functionality
updated_content = updated_content.replace(
    'async def classify(self, message: str)',
    'async def classify(self, message: str)\n        self.current_message = message  # Store for retries'
)

with open('services/intent_service/llm_classifier.py', 'w') as f:
    f.write(updated_content)

print("✅ Updated existing parse method to use resilient parsing")
```

### 5. Test Resilient Parsing with Malformed JSON
```python
# Create test cases for resilient parsing
test_malformed_json = '''
import asyncio
from services.intent_service.llm_classifier import LLMClassifier

async def test_resilient_parsing():
    """Test resilient parsing with various malformed JSON scenarios"""
    
    classifier = LLMClassifier()
    
    # Test cases for different malformation types
    test_cases = [
        # Case 1: Valid JSON (should use strategy 1)
        '{"category": "EXECUTION", "action": "create_issue", "confidence": 0.95}',
        
        # Case 2: Unquoted keys (should use strategy 2)
        '{category: "EXECUTION", action: "create_issue", confidence: 0.95}',
        
        # Case 3: Single quotes (should use strategy 2)
        "{'category': 'EXECUTION', 'action': 'create_issue', 'confidence': 0.95}",
        
        # Case 4: JSON embedded in text (should use strategy 3)
        'Here is the classification: {"category": "EXECUTION", "action": "create_issue", "confidence": 0.95} Hope this helps!',
        
        # Case 5: Partial JSON requiring regex extraction (should use strategy 5)
        'The intent is EXECUTION and the action is create_issue with confidence 0.8',
        
        # Case 6: Complete garbage (should use strategy 6)
        'This is not JSON at all, just random text that cannot be parsed in any way',
    ]
    
    print("=== Testing Resilient JSON Parsing ===")
    
    for i, test_json in enumerate(test_cases, 1):
        print(f"\\nTest Case {i}: {test_json[:50]}...")
        
        try:
            # Test the resilient parser directly
            result = classifier._parse_llm_response_resilient(test_json)
            
            print(f"  Result: {result}")
            print(f"  Parse method: {result.get('parse_method', 'direct_json')}")
            print(f"  Confidence: {result.get('confidence', 'N/A')}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print("\\n=== Integration Test with Real Classification ===")
    
    # Test with actual classification call
    try:
        result = await classifier.classify("Create a GitHub issue about the bug")
        print(f"Real classification: {result}")
        print(f"Category: {result.category if hasattr(result, 'category') else 'N/A'}")
        print(f"Confidence: {result.confidence if hasattr(result, 'confidence') else 'N/A'}")
        
    except Exception as e:
        print(f"Real classification failed: {e}")

# Run resilient parsing tests
asyncio.run(test_resilient_parsing())
'''

# Save and run the resilient parsing test
with open('/tmp/test_resilient_parsing.py', 'w') as f:
    f.write(test_malformed_json)

print("Running resilient parsing tests...")
exec(open('/tmp/test_resilient_parsing.py').read())
```

### 6. Run Performance Tests to Verify <500ms Requirement
```bash
# Test that resilient parsing still meets performance requirements
echo "=== Testing Performance with Resilient Parsing ==="

# Run the original failing performance test
PYTHONPATH=. python -m pytest tests/regression/test_queryrouter_lock.py::test_performance_requirement_queryrouter_initialization_under_500ms -xvs

# Run load testing to see improvement in reliability
PYTHONPATH=. python -m pytest tests/performance/test_llm_classifier_benchmarks.py -xvs

echo ""
echo "Performance Analysis:"
echo "- Individual requests should still be <500ms"
echo "- Load testing should show improved reliability"
echo "- Some fallback parsing may add latency but should stay under threshold"
```

## Evidence Collection Requirements

### Resilient Parser Implementation
```
=== Resilient Parsing Implementation Status ===
Backup created: [filename with timestamp]
Methods added: [list of methods added to LLM classifier]
Existing integration: [SUCCESS/FAILED - updated existing parse calls]

Implementation completeness:
- Strategy 1 (Direct JSON): [IMPLEMENTED/MISSING]
- Strategy 2 (Fix malformations): [IMPLEMENTED/MISSING]  
- Strategy 3 (Extract from text): [IMPLEMENTED/MISSING]
- Strategy 4 (Retry with strong prompt): [IMPLEMENTED/MISSING]
- Strategy 5 (Regex extraction): [IMPLEMENTED/MISSING]
- Strategy 6 (Final fallback): [IMPLEMENTED/MISSING]
```

### Resilient Parsing Test Results
```
=== Resilient Parsing Test Results ===
Test Case Results:
1. Valid JSON: [parse_method used, result]
2. Unquoted keys: [parse_method used, result]  
3. Single quotes: [parse_method used, result]
4. Embedded JSON: [parse_method used, result]
5. Regex extraction: [parse_method used, result]
6. Complete garbage: [parse_method used, result]

Real Classification Test:
- Status: [SUCCESS/FAILED]
- Result: [actual classification result]
- Parse method: [which strategy was used]
```

### Performance Impact Assessment
```
=== Performance Impact of Resilient Parsing ===
QueryRouter Performance Test: [PASSED/FAILED - timing]
Load Testing Results: [improved reliability statistics]

Performance Analysis:
- Average response time: [Xms vs previous Xms]
- 95th percentile: [Xms vs 500ms requirement]
- Success rate under load: [X% vs previous X%]
- Fallback usage frequency: [X% using strategies 2-6]

Meets <500ms requirement: [YES/NO]
Meets reliability thresholds: [99% individual, 95% normal load, 80% extreme load]
```

## Success Criteria
- [ ] Resilient parsing method implemented with all 6 strategies
- [ ] Existing LLM classifier updated to use resilient parsing  
- [ ] Test cases verify each parsing strategy works correctly
- [ ] Performance tests still pass with <500ms requirement
- [ ] Load testing shows improved reliability (approaching target thresholds)

## Time Estimate
45-60 minutes for complete implementation and testing

## Critical Deliverable
**Production-ready JSON parsing** that gracefully handles LLM provider inconsistencies under load while maintaining performance requirements. This completes the Chief Architect's guidance for handling the reality of LLM provider behavior.

**Expected outcome**: Dramatically improved reliability under load scenarios while maintaining individual request performance.
