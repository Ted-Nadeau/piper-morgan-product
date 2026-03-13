# Agent Prompt: ADR Analysis Plan - Systematic Investigation

**Agent**: Code
**Mission**: Create a comprehensive analysis plan to resolve ADR-032/ADR-036 confusion and verify QueryRouter implementation documentation status.

## Context from PM
- **ADR-032**: Original planning document
- **ADR-036**: Contains QueryRouter fix plan (needs updating to reflect completed work)
- **Issue**: Code wrote an ADR plan earlier, but numbering confusion exists
- **Cursor observation**: Plan may have incorrectly targeted ADR-032 instead of ADR-036
- **Goal**: Update ADR-036 to reflect completed QueryRouter implementation

## Phase 1: Historical Analysis and Plan Discovery

### 1A. Locate Code's Earlier ADR Plan
```bash
# Search for Code's earlier ADR planning work
echo "=== Searching for Code's Earlier ADR Plan ==="

# Check recent session logs and working files
echo "Searching session logs for ADR planning work:"
find . -name "*session*log*" -o -name "*ADR*" -o -name "*adr*" | head -20

# Search for ADR-related content in development files
echo ""
echo "Searching dev/ directory for ADR work:"
find dev/ -name "*ADR*" -o -name "*adr*" 2>/dev/null | head -10

# Search for mentions of ADR plans in recent files
echo ""
echo "Searching for ADR plan references:"
grep -r "ADR.*plan\|plan.*ADR" . --include="*.md" --include="*.txt" 2>/dev/null | head -10

# Look for specific mentions of QueryRouter ADR work
echo ""
echo "Searching for QueryRouter ADR references:"
grep -r "QueryRouter.*ADR\|ADR.*QueryRouter" . --include="*.md" 2>/dev/null | head -5
```

### 1B. Examine Current ADR Status
```bash
# Examine current state of both ADRs
echo "=== Current ADR Status Analysis ==="

echo "Checking for ADR files:"
find docs/ -name "*ADR*" -o -name "*032*" -o -name "*036*" 2>/dev/null

echo ""
echo "ADR-032 current status:"
if [ -f "docs/architecture/ADR-032.md" ]; then
    echo "✅ ADR-032 exists"
    echo "Last modified: $(stat -f "%Sm" docs/architecture/ADR-032.md 2>/dev/null || stat -c "%y" docs/architecture/ADR-032.md 2>/dev/null)"
    echo "Size: $(wc -l < docs/architecture/ADR-032.md) lines"
    echo ""
    echo "Content preview:"
    head -20 docs/architecture/ADR-032.md
else
    echo "❌ ADR-032 not found"
fi

echo ""
echo "ADR-036 current status:"
if [ -f "docs/architecture/ADR-036.md" ]; then
    echo "✅ ADR-036 exists"
    echo "Last modified: $(stat -f "%Sm" docs/architecture/ADR-036.md 2>/dev/null || stat -c "%y" docs/architecture/ADR-036.md 2>/dev/null)"
    echo "Size: $(wc -l < docs/architecture/ADR-036.md) lines"
    echo ""
    echo "Content preview:"
    head -20 docs/architecture/ADR-036.md
else
    echo "❌ ADR-036 not found"
fi
```

## Phase 2: ADR Content Analysis

### 2A. Analyze ADR-036 Current State
```bash
# Determine if ADR-036 reflects completed or planned work
echo "=== ADR-036 Content Analysis ==="

if [ -f "docs/architecture/ADR-036.md" ]; then
    echo "Analyzing ADR-036 language for completion status:"

    # Check for future tense (indicates planning, not completion)
    future_indicators=$(grep -i "will\|shall\|should\|need to\|plan to\|intend to" docs/architecture/ADR-036.md | wc -l)
    echo "Future tense indicators: $future_indicators"

    # Check for past tense (indicates completed work)
    past_indicators=$(grep -i "implemented\|completed\|fixed\|resolved\|done\|have " docs/architecture/ADR-036.md | wc -l)
    echo "Past tense indicators: $past_indicators"

    # Check for QueryRouter-specific content
    echo ""
    echo "QueryRouter references in ADR-036:"
    grep -n -i "queryrouter\|query router" docs/architecture/ADR-036.md | head -5

    # Check for status sections
    echo ""
    echo "Status or implementation sections:"
    grep -n -i -A 3 -B 1 "status\|implementation\|progress" docs/architecture/ADR-036.md

    # Language analysis
    if [ "$future_indicators" -gt "$past_indicators" ]; then
        echo ""
        echo "📋 ASSESSMENT: ADR-036 appears to describe PLANNED work (future tense dominant)"
        echo "Action needed: Update to reflect completed QueryRouter implementation"
    else
        echo ""
        echo "✅ ASSESSMENT: ADR-036 appears to describe COMPLETED work (past tense dominant)"
        echo "Verification needed: Ensure accuracy of completion claims"
    fi
fi
```

### 2B. Analyze ADR-032 for QueryRouter References
```bash
# Check if ADR-032 has been modified with QueryRouter content
echo "=== ADR-032 QueryRouter Analysis ==="

if [ -f "docs/architecture/ADR-032.md" ]; then
    echo "Checking ADR-032 for QueryRouter content:"

    queryrouter_refs=$(grep -i -n "queryrouter\|query router" docs/architecture/ADR-032.md | wc -l)
    echo "QueryRouter references: $queryrouter_refs"

    if [ "$queryrouter_refs" -gt 0 ]; then
        echo ""
        echo "QueryRouter content found in ADR-032:"
        grep -i -n -A 2 -B 2 "queryrouter\|query router" docs/architecture/ADR-032.md
        echo ""
        echo "🚨 WARNING: ADR-032 may have been incorrectly modified with QueryRouter content"
        echo "Original ADR-032 should be planning document, not QueryRouter implementation"
    else
        echo "✅ ADR-032 appears clean of QueryRouter implementation content"
    fi

    # Check modification dates relative to QueryRouter work
    echo ""
    echo "ADR-032 modification analysis:"
    echo "Last modified: $(stat -f "%Sm" docs/architecture/ADR-032.md 2>/dev/null || stat -c "%y" docs/architecture/ADR-032.md 2>/dev/null)"
    echo "Check if this coincides with recent QueryRouter work"
fi
```

## Phase 3: Plan Assessment Framework

### 3A. Create Decision Matrix
```bash
# Create systematic assessment framework
echo "=== ADR Plan Assessment Framework ==="

cat > /tmp/adr_assessment.md << 'EOF'
# ADR Analysis Results

## Historical Plan Discovery
- [ ] Code's earlier ADR plan found: YES/NO
- [ ] Plan location: [file path or MISSING]
- [ ] Plan targets: ADR-032 / ADR-036 / UNCLEAR
- [ ] Plan quality assessment: GOOD / BAD / NEEDS_REVIEW

## Current ADR Status
### ADR-032
- [ ] File exists: YES/NO
- [ ] Contains QueryRouter content: YES/NO (should be NO)
- [ ] Recently modified: YES/NO
- [ ] Assessment: ORIGINAL_STATE / INCORRECTLY_MODIFIED / NEEDS_VERIFICATION

### ADR-036
- [ ] File exists: YES/NO
- [ ] Language indicates: PLANNED_WORK / COMPLETED_WORK / MIXED
- [ ] QueryRouter content: COMPREHENSIVE / PARTIAL / MISSING
- [ ] Implementation accuracy: ACCURATE / OUTDATED / INCORRECT

## Decision Matrix Results
Based on findings above:

### If Code's Plan Found and Targets ADR-036:
- [ ] Plan quality: GOOD → Execute if not done, verify if done
- [ ] Plan quality: BAD → Create new plan and execute

### If Code's Plan Found and Targets ADR-032:
- [ ] Assessment: MISLABELED → Convert to ADR-036 plan
- [ ] Assessment: INCORRECT → Discard, create ADR-036 plan

### If No Plan Found:
- [ ] Action: Create new ADR-036 update plan

## Recommended Actions
1. [Primary action based on analysis]
2. [Secondary action if needed]
3. [Verification steps]

## Implementation Priority
- [ ] Immediate: [critical issues]
- [ ] Next: [standard updates]
- [ ] Future: [nice to have improvements]
EOF

echo "Assessment framework created at /tmp/adr_assessment.md"
```

## Phase 4: Analysis Execution Plan

### 4A. Systematic Investigation Steps
```bash
# Execute the systematic analysis
echo "=== Executing Systematic ADR Investigation ==="

echo "Step 1: Historical plan discovery"
# [Execute Phase 1 tasks]

echo ""
echo "Step 2: Current ADR content analysis"
# [Execute Phase 2 tasks]

echo ""
echo "Step 3: Decision matrix population"
# [Populate assessment framework based on findings]

echo ""
echo "Step 4: Recommendation generation"
# [Create specific action plan based on analysis]
```

### 4B. Verification and Validation
```bash
# Verify findings and create action plan
echo "=== Analysis Verification and Action Planning ==="

echo "Verification checklist:"
echo "- [ ] Historical plan status confirmed"
echo "- [ ] ADR-032 integrity verified"
echo "- [ ] ADR-036 current state assessed"
echo "- [ ] QueryRouter implementation accuracy checked"
echo "- [ ] Action plan created"

echo ""
echo "Ready for implementation planning based on findings"
```

## Success Criteria for Analysis Plan
- [ ] Code's earlier ADR plan located and evaluated (or confirmed missing)
- [ ] ADR-032 integrity verified (should not contain QueryRouter implementation)
- [ ] ADR-036 current state assessed (planning vs completion language)
- [ ] QueryRouter implementation accuracy in ADRs determined
- [ ] Clear decision matrix populated with findings
- [ ] Specific action recommendations provided
- [ ] Implementation plan ready for PM approval

## Output Requirements
1. **Historical Plan Status**: Found/Missing with location and assessment
2. **ADR-032 Status**: Original state or modifications detected
3. **ADR-036 Status**: Planning document or implementation record
4. **Decision Matrix**: Completed assessment framework
5. **Action Plan**: Specific steps for ADR resolution
6. **Implementation Priority**: Critical vs standard vs future tasks

**Deliverable**: Complete analysis with clear recommendations for systematic ADR resolution, ready for PM review and approval before execution.
