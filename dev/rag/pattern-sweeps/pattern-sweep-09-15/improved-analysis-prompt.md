# Improved Pattern Analysis Prompt - Iteration for Objectivity

## Original Prompt Issues Identified

The original prompt inadvertently encouraged:
- Confirmation bias ("breakthrough moments", "energy patterns")
- Grandiose framing ("OMNIBUS synthesis", "critical path")
- Subjective interpretation ("lived experience", "human outcomes")
- Pattern overinterpretation ("dependency relationships", "knowledge architecture")

## Revised Prompt for Future Analyses

---

# Pattern Analysis Request - Objective Focus

Please conduct a pattern analysis with these specific constraints:

## METHODOLOGY: Evidence-Based Analysis Only

**Required Approach:**
1. Start with quantitative data from `pattern_sweep_data.json`
2. Note file counts, occurrence frequencies, and distribution
3. Identify what can be objectively measured vs. subjectively interpreted
4. Explicitly separate correlation from causation
5. State confidence levels and evidence quality for each finding

**Avoid:**
- Causal claims without controlled comparison
- Percentages without clear methodology
- Superlatives ("unprecedented", "revolutionary", "breakthrough")
- Emotional/energy language ("breakthrough moments", "energy flow")

## SPECIFIC QUESTIONS (Measurable)

Instead of "map concept dependencies", ask:
1. **What patterns appear in the code with frequency >100?**
2. **Which patterns increased/decreased between time periods?** (with specific counts)
3. **What patterns appear in test files vs. production files?**
4. **Which documented practices have corresponding code patterns?**

Instead of "track breakthrough moments", ask:
1. **What specific problems were documented and what solutions were implemented?**
2. **How many days elapsed between problem identification and solution?**
3. **What was the test success rate before/after specific changes?**

Instead of "identify knowledge architecture", ask:
1. **What documentation exists and what's its word count/structure?**
2. **How many session logs exist and what's their average length?**
3. **What patterns repeat across multiple documents?**

## DELIVERABLES (Verifiable)

Replace subjective deliverables with:

1. **Pattern Frequency Report**
   - Table of patterns with occurrence counts
   - Distribution across file types
   - No interpretation, just data

2. **Change Analysis**
   - Specific files changed between dates
   - Line counts added/removed
   - Test coverage changes (numerical)

3. **Documentation Inventory**
   - List of documents with word counts
   - Creation dates and last modified dates
   - Link/reference counting

4. **Correlation Analysis**
   - X occurred, then Y occurred (no causation claims)
   - Time gaps between related events
   - Frequency of co-occurrence

5. **Uncertainty Report**
   - What data is missing
   - What claims cannot be verified
   - Alternative explanations for patterns

## OUTPUT REQUIREMENTS

1. **Confidence Levels**: Every claim must have:
   - HIGH: Directly measurable in code/logs
   - MEDIUM: Documented but subjective
   - LOW: Inferred from incomplete data
   - SPECULATION: Interesting but unverifiable

2. **Evidence Standards**:
   - Quote specific lines from logs
   - Reference specific file paths
   - Provide exact counts/measurements
   - Note when data is incomplete

3. **Anti-Patterns to Avoid**:
   - "Mathematical precision" (unless p-values provided)
   - "X% accuracy" (unless validation methodology explained)
   - "Unprecedented/revolutionary" (unless comparative data provided)
   - "Causes/enables/leads to" (use "preceded by" or "correlated with")

## SUCCESS CRITERIA

The analysis succeeds if:
- An outsider could verify every claim by checking the cited evidence
- No claims require insider knowledge to evaluate
- Uncertainty and alternative explanations are explicit
- Data and interpretation are clearly separated

## CRITICAL REVIEW REQUIREMENT

After completing analysis, add section:
"**Devil's Advocate Review**: If I were skeptical of this analysis, what would I challenge? What evidence would convince a skeptic?"

---

## Additional Prompting Improvements

### 1. Replace Loaded Terms

| Original Term | Better Alternative |
|--------------|-------------------|
| "breakthrough moments" | "documented changes" |
| "energy patterns" | "activity frequency" |
| "critical path" | "sequence of events" |
| "knowledge architecture" | "documentation structure" |
| "lived experience" | "documented events" |
| "human outcomes" | "measurable results" |

### 2. Add Skepticism Triggers

Add to prompt:
- "What would a skeptical reviewer question?"
- "What alternative explanations exist?"
- "What evidence is missing?"
- "What cannot be determined from available data?"

### 3. Require Comparison Baseline

Add to prompt:
- "Compare with what baseline?"
- "What would be expected by chance?"
- "How does this compare to typical software projects?"
- "What industry benchmarks exist?"

### 4. Enforce Humility Statements

Require sections:
- "Limitations of this analysis"
- "What this analysis cannot determine"
- "Assumptions made"
- "Data quality issues"

## Example of Improved Analysis Output

Instead of:
> "The September 9-15 period represents a critical consolidation moment with mathematical precision in the spiral development pattern."

Write:
> "September 9-15 shows 6 documented problem-solution pairs (MEDIUM confidence: from session logs). The time gap between periods varies from 9-41 days, median 17 days (HIGH confidence: calculated from dates). No statistical significance can be determined from 5 data points."

Instead of:
> "94% pattern detection accuracy validated against lived experience"

Write:
> "Pattern detection identified 14 patterns. Manual review agreed with 13/14 patterns (LOW confidence: self-validation, no independent review). Accuracy percentage cannot be calculated without false negative analysis."

## The Meta-Learning for Prompt Design

**Good prompts should:**
1. Request specific, measurable things
2. Explicitly discourage overinterpretation
3. Require evidence quality ratings
4. Include skepticism as part of the process
5. Separate data from interpretation

**Prompts should avoid:**
1. Emotional/dramatic language that encourages narrative
2. Terms that imply causation without proof
3. Requests for subjective assessment without criteria
4. Superlatives and absolute claims
5. Validation against "experience" rather than data

This revised approach would produce analysis that's:
- More credible to skeptics
- More useful for decision-making
- Less prone to confirmation bias
- More honest about uncertainty
- Actually reproducible by others
