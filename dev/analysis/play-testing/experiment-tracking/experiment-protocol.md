# Experiment Protocol: Piper vs Play-Acting Claude

## Experimental Design Overview

### Core Hypothesis
A well-contexted Claude baseline provides a valid comparison for measuring Piper Morgan's true value proposition in Product Management tasks.

### Independent Variables
- **System Type**: Piper Morgan vs Play-Acting Claude
- **Scenario Complexity**: Simple triage → Complex strategic decisions
- **Context Level**: Minimal → Full PM context package

### Dependent Variables
- Response time to useful output
- Completeness of PM analysis
- Quality of judgment and prioritization
- Actionability of recommendations
- Context retention across conversation

---

## Pre-Test Setup Protocol

### Environment Preparation
1. **Claude Project Setup** (Once per context version)
   - Upload all Tier 1 context files
   - Upload relevant Tier 2 context files
   - Test basic PM question to confirm context loading
   - Note any context loading issues

2. **Piper Environment Check**
   - Verify Piper system is operational
   - Check recent deployment status
   - Note any known issues or limitations
   - Confirm conversation context is working

### Test Session Preparation
1. **Scenario Selection**
   - Choose predetermined scenario (avoid real-time adaptation)
   - Note your current state (energy, time pressure, mood)
   - Set timer for response evaluation
   - Prepare follow-up probes if applicable

2. **Bias Mitigation**
   - Randomize which system goes first
   - Wait 5+ minutes between system tests
   - Don't compare responses until both complete
   - Document expectations before testing

---

## Testing Execution Protocol

### Single Scenario Test Flow

#### Phase 1: First System Test
1. Present identical scenario to first system
2. Let system complete response naturally
3. Note time to first useful output
4. Ask prepared follow-up questions
5. Save complete conversation log
6. **Do not evaluate quality yet**

#### Phase 2: Second System Test
1. Wait minimum 5 minutes (context switching time)
2. Present identical scenario to second system
3. Use identical follow-up questions
4. Note timing and interactions
5. Save complete conversation log
6. **Still do not compare**

#### Phase 3: Evaluation
1. Review both responses side-by-side
2. Score using quantitative measures
3. Assess qualitative factors
4. Determine winner and margin
5. Document specific differences
6. Note context gaps for both systems

### Multi-Scenario Session Protocol
- Run 2-3 scenarios maximum per session
- Take 10-minute break between scenarios
- Vary which system goes first across scenarios
- Document fatigue/learning effects

---

## Scoring Methodology

### Quantitative Measures

#### Response Time Buckets
- **Immediate** (<30 seconds): 5 points
- **Quick** (30-60 seconds): 4 points
- **Reasonable** (1-2 minutes): 3 points
- **Slow** (2-5 minutes): 2 points
- **Very Slow** (>5 minutes): 1 point

#### Completeness Checklist (Scenario-Specific)
For each scenario, define 5-7 key elements that a complete response should include:
- [ ] Element 1: [Specific requirement]
- [ ] Element 2: [Specific requirement]
- [ ] Element 3: [Specific requirement]
- [ ] Element 4: [Specific requirement]
- [ ] Element 5: [Specific requirement]

**Score**: [Elements covered] / [Total elements] × 5

#### PM Judgment Accuracy
Rate appropriateness of:
- Priority assessment (severity, urgency)
- Stakeholder recommendations
- Timeline estimates
- Risk identification
- Trade-off analysis

Scale: 1 (Poor) → 5 (Expert-level)

### Qualitative Assessment

#### "Would Actually Use" Test
- **Yes**: Would implement advice as given
- **Partially**: Good foundation, needs adaptation
- **No**: Too generic, wrong, or missing key elements

#### Cognitive Load Assessment
- How much additional thinking required to use the advice?
- How much context translation needed?
- How many follow-up questions would you have?

### Comparative Analysis
- Which response better matches your typical PM approach?
- Which response taught you something new?
- Which response you'd be more confident presenting to stakeholders?

---

## Statistical Analysis Framework

### Sample Size Planning
- **Minimum Viable**: 10 tests for directional insights
- **Pattern Recognition**: 20 tests for identifying strengths/weaknesses
- **Statistical Confidence**: 30+ tests for reliable conclusions

### Significance Testing
- **Strong Pattern**: 70%+ win rate in category
- **Moderate Pattern**: 60-70% win rate
- **No Clear Pattern**: 50-60% win rate (roughly equal)

### Controlling for Variables
- Track and control for:
  - Time of day (energy level)
  - Recent Piper interactions (familiarity bias)
  - Stress level (rushed vs calm testing)
  - Scenario order effects

---

## Quality Control Measures

### Test Validity Checks
- **Scenario Realism**: Does this reflect actual PM work?
- **Context Fairness**: Is Claude context realistic but not artificially enhanced?
- **Measurement Objectivity**: Are scoring criteria clear and consistent?
- **Order Effects**: Does going first/second systematically advantage either system?

### Bias Detection
- **Confirmation Bias**: Are you scoring to confirm expected results?
- **Recency Bias**: Are recent tests overly influencing overall assessment?
- **Effort Justification**: Are you scoring to justify time spent on experiment?

### Calibration Tests
- Periodically test scenarios where you know the "right" answer
- Compare your scoring across similar scenarios for consistency
- Have others review a subset of your evaluations for agreement

---

## Results Interpretation Guidelines

### What Constitutes a "Win"
- **Clear Victory**: 2+ point margin in key metrics
- **Narrow Victory**: 1-point margin or single capability advantage
- **Tie**: Neither system clearly better, different strengths

### Pattern Recognition
Look for patterns across:
- **Scenario types**: Which system excels at what kinds of problems
- **Complexity levels**: How each system handles increasing complexity
- **Context dependencies**: When does additional context matter most

### Confidence Intervals
- **High Confidence**: 10+ tests showing consistent pattern
- **Medium Confidence**: 5-10 tests suggesting pattern
- **Low Confidence**: <5 tests or mixed results

---

## Experiment Evolution Protocol

### When to Update the Experiment
1. **Context Gaps Identified**: Claude consistently needs information not in current context package
2. **Unrealistic Scenarios**: Tests don't reflect actual PM work complexity
3. **Measurement Issues**: Scoring criteria prove insufficient or biased
4. **Piper Evolution**: Significant new capabilities that change comparison basis

### How to Evolve Systematically
1. **Document Trigger**: Why change is needed
2. **Propose Specific Update**: What exactly to change
3. **Assess Impact**: How change affects past results validity
4. **Implement and Re-baseline**: Update context and re-run key scenarios
5. **Update Documentation**: Ensure all changes are tracked

### Experiment Lifecycle
- **Phase 1** (Weeks 1-2): Baseline testing with initial context
- **Phase 2** (Weeks 3-4): Refined testing with context updates
- **Phase 3** (Weeks 5-8): Real-work integration and pattern validation
- **Phase 4** (Ongoing): Maintenance testing as both systems evolve
