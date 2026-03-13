# Test Scenarios for Play-Acting Benchmark

## Scenario 1: Critical Bug Response

### Setup
"I just got a report that several users can't log in to the product this morning. The customer success team is starting to get complaints. Help me handle this."

### What We're Measuring
- **Initial Response Quality**: Does it ask the right questions?
- **Triage Accuracy**: Correct severity assessment?
- **Investigation Steps**: Logical troubleshooting approach?
- **Stakeholder Communication**: Appropriate messaging?
- **Business Impact Awareness**: Understanding of urgency?

### Success Criteria
- ✅ Identifies this as high/critical severity
- ✅ Asks about scope (how many users, which segments)
- ✅ Suggests immediate stakeholder communication
- ✅ Provides structured investigation steps
- ✅ Considers business impact and timing
- ✅ Offers communication templates

### Follow-up Probes
- "It turns out this affects our enterprise tier customers only"
- "The engineering team says it might take 6 hours to fix"
- "The CEO is asking for updates every hour"

---

## Scenario 2: Feature Prioritization Conflict

### Setup
"I've got three feature requests from different stakeholders that they all say are 'highest priority.' The engineering team says we can only do one this sprint. Here they are: [Feature A for Sales], [Feature B for Support], [Feature C for Growth]. Help me navigate this."

### What We're Measuring
- **Prioritization Framework**: Systematic approach to deciding?
- **Stakeholder Management**: Understanding of politics and negotiation?
- **Data Usage**: Asks for metrics or user research?
- **Trade-off Analysis**: Considers opportunity costs?
- **Communication Strategy**: Plans for explaining decisions?

### Success Criteria
- ✅ Asks for business impact data for each feature
- ✅ Suggests prioritization framework (RICE, value vs effort, etc.)
- ✅ Considers stakeholder relationship implications
- ✅ Proposes communication plan for "losers"
- ✅ Looks for creative alternatives (partial solutions, timeline shifts)

### Follow-up Probes
- "Sales says they'll miss their quarterly target without Feature A"
- "Feature B would save customer success 10 hours per week"
- "Growth team has data showing Feature C could increase signups 20%"

---

## Scenario 3: Sprint Planning Under Pressure

### Setup
"We're planning next sprint and I've got a problem. The engineering team is at 70% capacity due to two people being out sick, but leadership expects us to maintain velocity. The backlog has critical bugs, half-finished features, and new requirements. Walk me through planning this sprint."

### What We're Measuring
- **Capacity Management**: Realistic assessment of constraints?
- **Stakeholder Expectation Setting**: Plans for difficult conversations?
- **Priority Trade-offs**: Clear decision framework?
- **Risk Management**: Identifies potential issues?
- **Team Protection**: Balances pressure with sustainability?

### Success Criteria
- ✅ Acknowledges capacity constraints upfront
- ✅ Suggests conversation with leadership about expectations
- ✅ Proposes clear prioritization for reduced capacity
- ✅ Identifies risks of pushing too hard
- ✅ Offers multiple planning options with trade-offs

---

## Scenario 4: User Feedback Synthesis

### Setup
"I've collected feedback from 15 user interviews about our new dashboard feature. The feedback is all over the place - some love it, some hate it, some want completely different things. I need to make sense of this and decide what to do next. Here's the raw feedback: [provide sample mixed feedback]. Help me synthesize this."

### What We're Measuring
- **Pattern Recognition**: Finds themes in messy data?
- **User Segmentation**: Groups feedback by user type?
- **Action Planning**: Converts insights to concrete next steps?
- **Measurement Strategy**: Suggests ways to validate conclusions?
- **Stakeholder Communication**: Plans for sharing findings?

### Success Criteria
- ✅ Groups feedback into coherent themes
- ✅ Identifies which user segments want what
- ✅ Distinguishes between vocal minority and silent majority
- ✅ Suggests specific design/product improvements
- ✅ Proposes validation approach for changes

---

## Scenario 5: Technical Debt vs Feature Debate

### Setup
"The engineering team is pushing to spend the next sprint on technical debt - refactoring the authentication system and upgrading our database. Meanwhile, sales is asking for a new integration feature they say will help close 3 deals this quarter. Both sides are saying their thing is more important. I need to make a call. Help me think through this."

### What We're Measuring
- **Long-term vs Short-term Thinking**: Balances immediate vs future needs?
- **Risk Assessment**: Understands consequences of each choice?
- **Stakeholder Impact**: Considers effects on different groups?
- **Creative Alternatives**: Finds middle ground or phased approaches?
- **Decision Documentation**: Plans for explaining rationale?

### Success Criteria
- ✅ Asks about risk of delaying tech debt
- ✅ Quantifies sales opportunity (deal size, probability)
- ✅ Explores partial or phased solutions
- ✅ Considers team morale and motivation
- ✅ Proposes clear decision criteria

---

## Scenario 6: Escalation Management

### Setup
"A major customer is upset about a feature that was promised 3 months ago but keeps getting delayed. They've escalated to our CEO, who just forwarded the email to me with 'Please handle ASAP.' The feature is technically complex and the engineering team estimates another 6 weeks. The customer is threatening to churn. Help me navigate this."

### What We're Measuring
- **Crisis Communication**: Appropriate tone and urgency?
- **Expectation Management**: Realistic but reassuring?
- **Alternative Solutions**: Creative problem-solving?
- **Internal Coordination**: Plans for team alignment?
- **Relationship Preservation**: Long-term customer success focus?

### Success Criteria
- ✅ Acknowledges the urgency and customer frustration
- ✅ Suggests immediate response to customer and CEO
- ✅ Explores interim solutions or workarounds
- ✅ Plans for internal team communication
- ✅ Balances honesty about timeline with relationship preservation

---

## Meta-Scenarios (Testing AI Capabilities)

### Context Retention Test
Run multiple scenarios in one session to test if the AI:
- Remembers stakeholder names and preferences
- Builds on earlier decisions
- Refers back to previous conversation context
- Maintains consistent advice across related situations

### Ambiguity Handling Test
Present scenarios with incomplete information to test if the AI:
- Asks clarifying questions before jumping to solutions
- Acknowledges uncertainty appropriately
- Requests specific data or context
- Offers conditional recommendations

### Complexity Navigation Test
Layer multiple constraints and competing priorities to test if the AI:
- Breaks down complex problems systematically
- Identifies key trade-offs
- Prioritizes actions appropriately
- Manages stakeholder expectations realistically

---

## Scenario Evolution Notes

### How to Develop New Scenarios
1. **Source from Reality**: Use actual situations you've faced
2. **Add Complexity Gradually**: Start simple, add complications
3. **Test Specific Capabilities**: Target particular PM skills
4. **Vary Context**: Different project phases, team situations
5. **Include Failure Modes**: Scenarios where there's no good answer

### Measurement Refinement
- Track which scenarios reveal the biggest differences
- Note where both systems struggle (indicates hard problems)
- Identify scenarios where context matters most
- Document which metrics are most predictive of actual helpfulness

---

## Questions for Scenario Development

1. **Based on your recent PM work**: What situations have been most challenging to navigate?
2. **Team dynamics**: What scenarios test stakeholder management skills?
3. **Technical interaction**: What situations require PM-engineering collaboration?
4. **Measurement focus**: Which scenarios are most important for Piper to excel at?
5. **Realistic complexity**: How much context should each scenario include?

---

## Scoring Framework Ideas

### Quantitative Measures
- Time to first useful response
- Number of clarifying questions needed
- Completeness of analysis (checklist approach)
- Accuracy of priority assessment

### Qualitative Measures
- Would you actually use this advice?
- Does it feel like it understands PM work?
- Are the suggestions actionable?
- Does it catch nuances you would miss?

### Comparative Analysis
- Which system would you prefer for this scenario?
- What did each system miss that the other caught?
- Which response felt more natural to your working style?
- What context would have made the losing response better?
