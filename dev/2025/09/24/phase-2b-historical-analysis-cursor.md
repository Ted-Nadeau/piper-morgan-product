# Agent Prompt: Phase 2B - Historical Analysis and Pattern Identification

**Agent**: Cursor
**Mission**: Compare current vs PM-011 LLM classifier structure, identify what changed in prompt formatting, and pinpoint missing JSON instructions.

## Context from Phase 1
- **Root Cause**: Anthropic returning `{category: "value"}` instead of `{"category": "value"}`
- **Historical Working State**: PM-011 (commit 6861995b, June 24 2025) had proper JSON responses
- **Breaking Period**: July-August 2025 during infrastructure changes
- **PM Direction**: Fix Anthropic API interaction properly, identify what changed

## Phase 2B Investigation Tasks

### 1. Extract Working PM-011 LLM Classifier
```bash
# Get the working version from PM-011
git show 6861995b:services/intent_service/llm_classifier.py > /tmp/pm011_working_classifier.py

# Get current version for comparison
cp services/intent_service/llm_classifier.py /tmp/current_classifier.py

# Show file sizes and basic stats
echo "=== File Comparison Stats ==="
wc -l /tmp/pm011_working_classifier.py /tmp/current_classifier.py
echo ""
```

### 2. Detailed Diff Analysis - Focus on Prompts
```bash
# Show comprehensive diff between working and current versions
echo "=== PM-011 vs Current Diff Analysis ==="
diff -u /tmp/pm011_working_classifier.py /tmp/current_classifier.py

# Focus specifically on prompt-related changes
echo "=== Prompt-Related Changes ==="
diff -u /tmp/pm011_working_classifier.py /tmp/current_classifier.py | grep -A 5 -B 5 -i "prompt\|json\|system\|format\|response"

# Look for method signature changes
echo "=== Method Signature Changes ==="
diff -u /tmp/pm011_working_classifier.py /tmp/current_classifier.py | grep -A 3 -B 1 "def "
```

### 3. Extract JSON Instructions from Working Version
```bash
# Find JSON-related instructions in the working PM-011 version
echo "=== PM-011 JSON Instructions ==="
grep -n -A 5 -B 5 -i "json\|format\|response.*structure\|schema" /tmp/pm011_working_classifier.py

# Find system prompts or prompt templates
echo "=== PM-011 Prompt Templates ==="
grep -n -A 10 -B 2 -i "system.*prompt\|prompt.*template\|user.*message" /tmp/pm011_working_classifier.py

# Find string literals that might be prompts (multi-line strings)
echo "=== PM-011 Multi-line Strings (Potential Prompts) ==="
grep -n -A 10 '"""' /tmp/pm011_working_classifier.py
grep -n -A 10 "'''" /tmp/pm011_working_classifier.py

# Look for explicit JSON structure specifications
echo "=== PM-011 JSON Structure Specifications ==="
grep -n -A 5 -B 5 '{".*"}' /tmp/pm011_working_classifier.py
```

### 4. Trace What Changed in Prompt Construction
```bash
# Look at the evolution of prompt-related methods
echo "=== Prompt Method Evolution ==="

# Show git history of prompt-related changes
git log --oneline --since="2025-06-24" --until="2025-08-06" -p services/intent_service/llm_classifier.py | grep -A 10 -B 10 -i "prompt\|json\|format"

# Check if there were imports that changed (affecting JSON handling)
echo "=== Import Changes Analysis ==="
git log --oneline --since="2025-06-24" --until="2025-08-06" -p services/intent_service/llm_classifier.py | grep -A 3 -B 3 "import\|from.*import"

# Look for any TODO comments about JSON that might have been removed
echo "=== Removed TODO Comments ==="
git log --oneline --since="2025-06-24" -p services/intent_service/llm_classifier.py | grep -A 3 -B 3 "TODO.*json\|TODO.*JSON"
```

### 5. Analyze LLM Client Changes
```bash
# Compare LLM client between PM-011 and current
echo "=== LLM Client Comparison ==="
git show 6861995b:services/llm/clients.py > /tmp/pm011_client.py
diff -u /tmp/pm011_client.py services/llm/clients.py

# Look for changes in how API calls are made
echo "=== API Call Method Changes ==="
diff -u /tmp/pm011_client.py services/llm/clients.py | grep -A 5 -B 5 "complete\|chat\|messages"

# Check for prompt or system message handling changes
echo "=== Message Handling Changes ==="
diff -u /tmp/pm011_client.py services/llm/clients.py | grep -A 5 -B 5 -i "system\|user.*message\|prompt"
```

### 6. Identify Missing JSON Format Instructions
```bash
# Create a comprehensive comparison of JSON handling
echo "=== JSON Handling Comparison ==="

# Extract all JSON-related content from both versions
echo "PM-011 JSON Patterns:"
grep -n -i "json\|format.*response\|double.*quote\|property.*name" /tmp/pm011_working_classifier.py

echo ""
echo "Current JSON Patterns:"
grep -n -i "json\|format.*response\|double.*quote\|property.*name" services/intent_service/llm_classifier.py

# Look for explicit JSON schema or format specifications
echo ""
echo "=== Format Specification Comparison ==="
echo "PM-011 Format Specs:"
grep -n -A 10 -B 2 'category.*action.*confidence\|"category":\|response.*format' /tmp/pm011_working_classifier.py

echo ""
echo "Current Format Specs:"
grep -n -A 10 -B 2 'category.*action.*confidence\|"category":\|response.*format' services/intent_service/llm_classifier.py
```

## Evidence Collection Requirements

### File Comparison Analysis
```
=== PM-011 vs Current Structure ===
PM-011 File Size: [lines] lines
Current File Size: [lines] lines
Major Structural Changes: [list key differences]

Key Method Changes:
- Added methods: [list]
- Removed methods: [list]
- Modified methods: [list with brief description]

Import Changes:
- Added imports: [list]
- Removed imports: [list]
- Modified imports: [list]
```

### JSON Instruction Analysis
```
=== JSON Format Instruction Comparison ===

PM-011 (Working) JSON Instructions:
[paste exact JSON formatting instructions from working version]

Current (Broken) JSON Instructions:
[paste current JSON instructions if any, or "NONE FOUND"]

Specific Missing Instructions:
1. [specific instruction #1 that was removed]
2. [specific instruction #2 that was removed]
3. [etc.]
```

### Prompt Structure Changes
```
=== Prompt Construction Changes ===

PM-011 System Prompt:
[exact system prompt from working version]

Current System Prompt:
[current system prompt]

PM-011 User Message Format:
[how user messages were formatted in working version]

Current User Message Format:
[how user messages are currently formatted]

Key Differences Identified:
- [difference #1]
- [difference #2]
- [etc.]
```

### Root Cause Pattern
```
=== Breaking Change Pattern ===

What Was Removed/Changed:
[specific change that broke JSON formatting]

When It Changed:
- Commit Range: [approximate commit range]
- Likely Commit: [specific commit if identifiable]
- Context: [what was being changed when JSON broke]

How It Worked Before:
[description of working JSON instruction pattern]

Why It Broke:
[analysis of what the change removed or altered]
```

### Fix Recommendations
```
=== Recommended Fix Based on Historical Analysis ===

Missing JSON Instructions to Restore:
1. [specific instruction to add back]
2. [specific format requirement to restore]
3. [specific schema specification needed]

Location for Fix:
- File: services/intent_service/llm_classifier.py
- Method: [specific method name]
- Type of Change: [add system prompt / modify user message / etc.]

Working Example from PM-011:
[exact working prompt structure to restore]
```

## Success Criteria
- [ ] PM-011 vs current classifier fully compared
- [ ] Specific JSON instruction changes identified
- [ ] Missing format requirements documented
- [ ] Breaking change pattern analyzed
- [ ] Clear fix recommendations provided based on working version

## Time Estimate
20-25 minutes for complete historical analysis and pattern identification

## Critical Focus
- **Find exact JSON formatting differences** between working PM-011 and current broken version
- **Identify specific missing instructions** that caused Anthropic to return malformed JSON
- **Provide clear restoration path** based on historical working patterns
- **Evidence-based recommendations** for what needs to be added back to fix the issue

**The goal is to understand exactly what we lost between June (working) and now (broken) so Code can restore the proper JSON formatting instructions.**
