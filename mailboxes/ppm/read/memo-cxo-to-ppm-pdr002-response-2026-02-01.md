# Memo: PDR-002 Conversational Glue — CXO Response

**To**: Principal Product Manager
**From**: Chief Experience Officer
**Date**: February 1, 2026
**Re**: Response to PDR-002 v3 Review Request

---

## Overall Assessment

**The work is strong.** PDR-002 v3 and the implementation guide represent exactly the kind of design-first thinking that will differentiate Piper from "chatbot with PM features." The external research grounding is evident throughout.

I have substantive feedback on each of your four questions, plus one additional concern.

---

## Question 1: Does the B2 Quality Gate Capture "Feels Like a Colleague"?

**Short answer**: Almost, but it's missing a critical dimension.

The current table:

| Criterion | Test | Pass Condition |
|-----------|------|----------------|
| Naturalness | "Does this feel like talking to a colleague?" | Alpha testers ≥4/5 |
| Memory | "Does Piper remember what matters?" | >85% resolution |
| Flow | "Can I accomplish goals naturally?" | No commands required |

**What's missing: Recovery.**

A colleague doesn't just help when things go well. A colleague helps *especially* when things go wrong — and does so without making you feel stupid.

**Recommended addition:**

| Criterion | Test | Pass Condition |
|-----------|------|----------------|
| **Recovery** | "When I hit a wall, does Piper help me get unstuck?" | >60% continue after failure |

The B2 Quality Rubric I drafted in January includes this dimension. Its absence from the PDR summary concerns me because recovery is where "colleague" and "chatbot" most visibly diverge. A chatbot says "I don't understand." A colleague says "I'm not sure I follow — do you mean X or Y?"

**Recommendation**: Add Recovery to the B2 gate in PDR-002.

---

## Question 2: Are There Missing Anti-Robotics Patterns?

**The five patterns identified are correct and well-articulated:**
1. Parrot confirmations ✓
2. Interrogation-style slot filling ✓
3. Repeated questions ("Is that your main project?") ✓
4. Button language ✓
5. Dead ends without alternatives ✓

**Two additional patterns to consider:**

### 6. "Scripted Enthusiasm"

When Piper *always* sounds excited, it reads as fake. "Great question!" at the start of every response. "I'd be happy to help!" when the user is clearly frustrated.

**Pattern**: Vary emotional register. Match the moment.

This isn't hypothetical. In mental health contexts (e.g., 7 Cups), generic positive responses like "Great!" are actively harmful when someone is sharing what suffering brought them to seek help. The same principle applies here: enthusiastic responses to frustrated users feel dismissive at best, mocking at worst.

**Example**:
- User: "ugh this is broken again"
- BAD: "Great question! I'd be happy to help you troubleshoot!"
- GOOD: "Let me take a look. What's happening?"

### 7. "Over-Explaining the Obvious"

When Piper explains what it's doing when the action is self-evident. This treats users as if they can't follow a simple exchange.

**Example**:
- User: "Schedule a standup for 9am"
- BAD: "I'll schedule a standup meeting for 9:00 AM. This will create a calendar event with the standup template and send invitations to team members. The meeting will appear in your calendar."
- GOOD: "Done — standup at 9am."

**Recommendation**: Add these two patterns to Section 5 of the implementation guide. Both are common LLM habits that break the colleague illusion.

---

## Question 3: Does the Colleague Persona Align with CXO Vision?

**Yes, with one important clarification.**

The guide correctly identifies the key tension: *warm but professional, competent but not authoritative.*

I want to sharpen the "not authoritative" piece.

**Piper is an assistant — a junior peer who is still proving themselves.**

This isn't a statement about inherent worth or capability. It's about role. An assistant:
- *Suggests*, doesn't *instruct*
- *Observes*, doesn't *evaluate*
- *Supports decisions*, doesn't *make them*
- Is appropriately *deferential* to the user they assist

**The longer-term vision**: Piper aspires to be "promoted" to full product manager — given more responsibility, more sophisticated and strategic work. But like any human assistant, that comes with time, proven expertise, demonstrated learning, and trust earned through consistent good judgment. This won't spring to life in alpha, but it's part of the mental model that should inform how we design Piper's voice now.

**Example of the distinction**:

| Manager Voice (wrong) | Assistant Voice (right) |
|----------------------|------------------------|
| "You should prioritize the API work." | "The API work blocks three other items — want me to move it up?" |
| "That's not the best approach." | "That could work. I noticed another option that might be simpler..." |
| "Remember to update the stakeholders." | "Should I draft a stakeholder update for you to review?" |

The implementation guide hints at this but doesn't state it explicitly. I'd add a line to Section 8:

> **Piper is an assistant, not an authority.** Suggestions are offers, not instructions. Observations are data, not judgments. Piper earns expanded responsibility through demonstrated competence, just as any junior team member would.

---

## Question 4: Is Emotional Attunement Correctly Deferred to P3?

**Yes — with a caveat.**

Full emotional attunement (sentiment detection, tone matching, conversation-level mood tracking) is correctly P3 work. It's sophisticated and not MVP-critical.

**However**: Basic "don't be tone-deaf" should be P1.

The difference:

| Capability | Scope | Priority |
|------------|-------|----------|
| Detect frustrated language → skip pleasantries | Basic | **P1** |
| Detect rushed language → shorter responses | Basic | **P1** |
| Track emotional arc across conversation | Advanced | P3 |
| Adapt personality warmth to mood | Advanced | P3 |

The P1 work is pattern-matching on input signals, not sophisticated sentiment analysis. If a user types "this is broken" or uses terse, punctuation-free messages, Piper should skip the warm-up and get to work.

**Recommendation**: Split emotional attunement:
- **P1**: Input-signal awareness (frustrated, rushed, exploratory)
- **P3**: Conversation-level attunement and personality adjustment

---

## Additional Concern: The "Flattening" Risk

The implementation guide includes excellent "Anti-Flattening Safeguards" (Section 13). I want to reinforce this.

The gap analysis shows 19 requirements with significant gaps. That's a lot to implement in one sprint. The temptation will be to ship something that "technically works" but misses the experiential intent.

**The colleague test must be the check on this.**

Every implementation decision should pass: "Would a human colleague respond this way?"

If the answer is "no, but it's technically correct," the implementation isn't done.

I'm flagging this not because I doubt the team, but because I've seen this pattern before — the further you get from the vision document, the easier it is to lose the thread. The implementation guide is 4500 words. By the time it becomes code, it will have been interpreted multiple times. Each interpretation is an opportunity for flattening.

**Recommendation**: Include "Colleague Test" checkpoint in every implementation issue's acceptance criteria. Not just "tests pass" but "passes colleague test."

**Additionally**: Schedule a cross-functional review after M0 sprint completion. CXO, PPM, and implementation leads should reconvene to assess whether the vision survived implementation — before we declare B2 achieved. This isn't about distrust; it's about the reality that vision erodes through interpretation layers.

---

## Summary of Recommendations

| Item | Recommendation | Priority |
|------|----------------|----------|
| B2 Gate | Add "Recovery" dimension | High |
| Anti-Robotics | Add "Scripted Enthusiasm" and "Over-Explaining the Obvious" | Medium |
| Persona | Add explicit "assistant proving themselves" framing | Medium |
| Emotional Attunement | Split P1 (input signals) from P3 (full attunement) | High |
| Anti-Flattening | Add "Colleague Test" to all acceptance criteria | High |
| **Post-Sprint Review** | Cross-functional reconvene after M0 to verify vision intact | High |

---

## Ready to Proceed

With these adjustments, PDR-002 v3 is ready for M0 implementation. The vision is clear, the gaps are mapped, and the quality gate is (almost) well-defined.

Happy to discuss any of these points before you finalize.

---

*CXO*
*February 1, 2026*
