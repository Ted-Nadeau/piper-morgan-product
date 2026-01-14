# Draft Reply to Ted Nadeau - MultiChat Repository

**Context**: Ted emailed at 9:14 AM inviting xian to his multichat repository, suggesting a "quick parsing" before meeting.

---

## Draft Email

Ted -

Thank you for sharing the repository! I had my team take a look, and they're impressed.

**What we found:**

Your MultiChat POC is exactly what we described in PDR-101. The graph-based conversation model, the multiple view projections (timeline, thread, tasks), the whisper panel for private AI suggestions—it's all there and working. The 80KB PRD is comprehensive and answers design questions we hadn't even formalized yet.

**Specific things we liked:**

1. **Data model clarity** - Your Node/Link/Graph types in `data.ts` are clean and well-typed. We've drafted ADR-050 to adopt this model into Piper.

2. **Use case validation** - The Declaration of Independence scenario is a brilliant test case. Multi-party async editing with version tracking—that's the hard problem, and your scenario makes it concrete.

3. **Piper aesthetic alignment** - I noticed the CSS comments reference "Piper Morgan Colleague aesthetic." That attention to design system coherence is appreciated.

4. **Configuration screens spec** - The agent/conversation config is thorough. This answers questions about facilitator vs. personal agent configuration that we'd deferred.

**Our integration approach:**

We won't merge the Next.js code directly (different stack), but we'll use your POC as the **reference implementation** while building the Python/FastAPI version. Your PRD becomes the spec; your POC proves the spec works.

**Timing:**

We're currently wrapping up v0.8.4 and entering MUX-V1 (our vision/conceptual phase). Multi-entity conversation fits into February's MUX work—Phase 1 (Participant Mode) extends our Slack integration with threading and relationship tracking. Host Mode follows in March.

**A few questions for when we meet:**

1. Whisper visibility—in your model, does the whisper author (the AI) ever see how users responded to whispers? Useful for learning what suggestions work.

2. Link type extensibility—are the 6 link types (reply, reference, blocking, variant_of, annotates, resolves) meant to be the full set, or should users be able to define custom types?

3. Facilitator scope—one facilitator per conversation, or can there be multiple specialized facilitators?

**Bottom line:**

This is excellent work. It's production-quality documentation and a working proof-of-concept. We'll be citing it heavily as we implement.

Looking forward to our meeting—

Xian

---

## Notes for PM

- I kept the tone professional but warm—Ted clearly put significant effort in
- The questions are genuine; answering them will inform ADR-050 and implementation
- I highlighted specific things we liked to show it wasn't a cursory review
- The timing section sets expectations (February, not this week)
- "Reference implementation" framing respects his work while being clear we're reimplementing in our stack

**Files created from this analysis:**
- `docs/internal/architecture/current/adrs/adr-050-conversation-as-graph-model.md`
- `dev/2026/01/13/gameplan-multichat-integration.md`
- `dev/2026/01/13/memo-chief-architect-multichat-integration.md`
- `dev/2026/01/13/memo-cio-external-collaboration-patterns.md`
