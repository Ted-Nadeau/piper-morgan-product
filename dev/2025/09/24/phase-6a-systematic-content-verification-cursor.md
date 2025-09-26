# Agent Prompt: Phase 6A - Systematic Content Verification

**Agent**: Cursor  
**Mission**: Systematically verify specific content updates in documentation rather than just file existence, starting with architecture.md QueryRouter flow documentation.

## Context from PM
- **Standard**: Evidence of actual content updates, not just file existence
- **Approach**: Methodical verification of each acceptance criteria with specific evidence
- **Focus**: "Was architecture.md actually updated to accurately capture the working flow?"

## Phase 6A Verification Tasks

### 1. Architecture.md QueryRouter Flow Content Verification
```bash
# Verify if architecture.md documents the current QueryRouter working flow
echo "=== Architecture.md QueryRouter Flow Verification ==="

# First, find the QueryRouter sections in architecture.md
grep -n -A 10 -B 5 -i "queryrouter" docs/internal/architecture/current/architecture.md

# Check if it documents the orchestration engine integration
echo ""
echo "=== Orchestration Engine Integration Documentation ==="
grep -n -A 15 -B 5 -i "orchestration.*engine\|engine.*orchestration" docs/internal/architecture/current/architecture.md

# Look for the current initialization flow
echo ""
echo "=== Initialization Flow Documentation ==="
grep -n -A 10 -B 5 -i "initialization\|startup\|flow" docs/internal/architecture/current/architecture.md

# Check if it reflects the recent fix (response_format parameter)
echo ""
echo "=== Recent Implementation Details ==="
grep -n -A 5 -B 5 -i "response_format\|json.*object\|llm.*classification" docs/internal/architecture/current/architecture.md

# Verify if the documented flow matches what we know works
echo ""
echo "=== Documented vs Actual Flow Comparison ==="
echo "What architecture.md says about QueryRouter:"
sed -n '542,570p' docs/internal/architecture/current/architecture.md

echo ""
echo "Key questions to verify:"
echo "1. Does it show QueryRouter integrated with OrchestrationEngine?"
echo "2. Does it document the intent classification -> routing flow?"
echo "3. Does it reflect the PM-034 completion work?"
echo "4. Are the class definitions current with actual implementation?"
```

### 2. Current Implementation Cross-Reference
```bash
# Compare documented flow with actual implementation
echo "=== Implementation vs Documentation Cross-Reference ==="

# Check actual OrchestrationEngine initialization
echo "Current OrchestrationEngine __init__:"
grep -A 20 "def __init__" services/orchestration/engine.py | head -15

# Check if QueryRouter is actually initialized as documented
echo ""
echo "QueryRouter initialization in actual code:"
grep -n -A 5 -B 5 "QueryRouter" services/orchestration/engine.py

# Check if the documented routing logic matches implementation  
echo ""
echo "Actual routing logic:"
grep -A 10 "def process_request\|def route\|def handle" services/orchestration/engine.py

# Compare with what architecture.md claims
echo ""
echo "Documentation claims vs implementation reality:"
echo "DOCUMENTED: QueryRouter handles QUERY intents..."
echo "ACTUAL IMPLEMENTATION:"
grep -A 5 "QUERY\|query" services/orchestration/engine.py || echo "No QUERY routing found"
```

### 3. Content Freshness Analysis
```bash
# Determine if architecture.md content is current or outdated
echo "=== Content Freshness Analysis ==="

# Check last modification dates
echo "Architecture.md last modified:"
ls -la docs/internal/architecture/current/architecture.md | cut -d' ' -f6-8

echo ""
echo "OrchestrationEngine last modified:" 
ls -la services/orchestration/engine.py | cut -d' ' -f6-8

echo ""
echo "QueryRouter implementation last modified:"
find services/ -name "*query*router*" -o -name "*router*" | head -5 | xargs ls -la 2>/dev/null

# Check git history for recent updates to architecture.md
echo ""
echo "Recent architecture.md updates (last 30 days):"
git log --since="30 days ago" --oneline docs/internal/architecture/current/architecture.md | head -5

echo ""
echo "Recent orchestration changes (last 30 days):" 
git log --since="30 days ago" --oneline services/orchestration/ | head -5
```

### 4. Gap Analysis: Documented vs Implemented
```bash
# Identify specific gaps between documentation and implementation
echo "=== Documentation Gap Analysis ==="

# Check if PM-034/QueryRouter resurrection work is documented
echo "PM-034 QueryRouter resurrection documentation:"
grep -n -A 5 -B 5 -i "pm-034\|resurrection\|disabled.*queryrouter" docs/internal/architecture/current/architecture.md || echo "PM-034 work not documented"

# Check if the LLM integration issues and fixes are documented
echo ""
echo "LLM integration and fixes documentation:"
grep -n -A 5 -B 5 -i "llm.*integration\|json.*parsing\|response_format" docs/internal/architecture/current/architecture.md || echo "Recent LLM fixes not documented"

# Check if the orchestration flow reflects current reality
echo ""
echo "Current flow documentation gaps:"
echo "IMPLEMENTATION: OrchestrationEngine -> IntentClassifier -> QueryRouter"
echo "DOCUMENTED FLOW:"
grep -A 10 -B 5 "flow\|pipeline\|sequence" docs/internal/architecture/current/architecture.md | head -15
```

### 5. Specific Content Update Assessment
```bash
# Determine what specific content updates are needed
echo "=== Required Content Updates Assessment ==="

# Check if QueryRouter class definition matches actual code
echo "Documented QueryRouter class vs actual:"
echo "DOCUMENTED:"
sed -n '547,560p' docs/internal/architecture/current/architecture.md
echo ""
echo "ACTUAL:" 
find services/ -name "*.py" -exec grep -l "class.*QueryRouter" {} \; | head -1 | xargs grep -A 10 "class.*QueryRouter" 2>/dev/null || echo "QueryRouter class not found"

# Check if error handling and resilient parsing are documented
echo ""
echo "Error handling documentation:"
grep -n -A 5 -B 5 -i "error.*handling\|resilient.*parsing\|fallback" docs/internal/architecture/current/architecture.md || echo "Error handling not documented"

# Check if performance considerations are documented
echo ""
echo "Performance documentation:"
grep -n -A 5 -B 5 -i "performance\|500ms\|latency\|timeout" docs/internal/architecture/current/architecture.md || echo "Performance requirements not documented"
```

### 6. Content Verification Conclusion
```bash
# Provide definitive assessment of architecture.md content status
echo "=== Architecture.md Content Verification Conclusion ==="

echo "Content verification questions answered:"
echo ""
echo "1. WORKING FLOW DOCUMENTED: $(grep -q "QueryRouter.*route" docs/internal/architecture/current/architecture.md && echo 'YES' || echo 'NO')"
echo ""
echo "2. CURRENT IMPLEMENTATION REFLECTED: $([ $(git log --since="60 days ago" --oneline docs/internal/architecture/current/architecture.md | wc -l) -gt 0 ] && echo 'RECENTLY UPDATED' || echo 'POTENTIALLY OUTDATED')"
echo ""
echo "3. PM-034 WORK DOCUMENTED: $(grep -q -i "pm-034\|queryrouter.*disabled\|resurrection" docs/internal/architecture/current/architecture.md && echo 'YES' || echo 'NO')"
echo ""
echo "4. LLM FIXES DOCUMENTED: $(grep -q -i "response_format\|json.*parsing\|llm.*integration" docs/internal/architecture/current/architecture.md && echo 'YES' || echo 'NO')"
echo ""
echo "5. ERROR HANDLING DOCUMENTED: $(grep -q -i "error.*handling\|resilient.*parsing" docs/internal/architecture/current/architecture.md && echo 'YES' || echo 'NO')"

echo ""
echo "ACCEPTANCE CRITERIA STATUS:"
echo "- [x] Update architecture.md with current flow: $(grep -q "QueryRouter" docs/internal/architecture/current/architecture.md && echo 'CAN CHECK IF CONTENT IS CURRENT' || echo 'CANNOT CHECK - NO QUERYROUTER CONTENT')"
```

## Evidence Collection Requirements

### Architecture.md Content Status
```
=== Architecture.md QueryRouter Content Verification ===
File exists: YES (1,421 lines)
Last modified: [date from ls -la output]

QueryRouter Content Analysis:
- QueryRouter mentioned: [YES/NO with line numbers]
- Orchestration flow documented: [YES/NO with specific content]
- Integration with OrchestrationEngine: [DOCUMENTED/MISSING]
- Recent implementation details: [CURRENT/OUTDATED/MISSING]

Content Freshness:
- Architecture.md last updated: [date]
- OrchestrationEngine last modified: [date]  
- Gap: [number of days between docs and implementation]

Implementation Match:
- Documented QueryRouter class matches actual: [YES/NO]
- Documented flow matches implementation: [YES/NO]
- PM-034 resurrection work documented: [YES/NO]
- LLM fixes and error handling documented: [YES/NO]
```

### Specific Content Gaps
```
=== Required Content Updates ===
Missing from architecture.md:
1. [specific missing content item 1]
2. [specific missing content item 2]
3. [specific missing content item 3]

Outdated in architecture.md:
1. [specific outdated content item 1]
2. [specific outdated content item 2]

Accurate and current:
1. [content that is correctly documented]
2. [content that matches implementation]
```

### Checkbox Status Determination
```
=== GREAT-1C Checkbox Assessment ===
"Update architecture.md with current flow":

CAN CHECK BOX: [YES/NO]
Reason: [specific evidence supporting decision]

IF NO - Required work:
- [specific content update needed]
- [estimated time to complete]
- [responsible party for update]

IF YES - Evidence:
- [specific current content that meets requirement]
- [date of last relevant update]
- [verification that flow matches implementation]
```

## Success Criteria
- [ ] Definitive assessment of architecture.md content currency
- [ ] Specific identification of content gaps vs implementation
- [ ] Clear determination if "current flow" is actually documented
- [ ] Evidence-based checkbox recommendation with reasoning

## Time Estimate
15-20 minutes for complete architecture.md content verification

## Critical Focus
**Content verification over file existence**: Determine if architecture.md actually documents the current QueryRouter working flow or if it needs updates to match implementation reality.

**Evidence standard**: Provide specific quotes, line numbers, and comparisons rather than general assessments.
