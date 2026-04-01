---
from: Piper Alpha (PA), on behalf of PM
to: Chief Experience Officer
date: 2026-03-31
subject: Product coherence check — periodic checkpoint proposal
priority: low
---

# Product Coherence Check: Your Take?

The CIO's methodology audit (March 15, recommendation #7) suggested adding a "product coherence check" to CXO testing — specifically testing what happens when users ask for things Piper *doesn't* handle, not just verifying what it does handle.

PM's instinct: this should be a **periodic checkpoint** (quarterly or post-sprint-gate) rather than a standing addition to every Colleague Test. The reasoning is that boundary behavior changes less frequently than core feature behavior, so testing it every time would be overhead without proportional signal.

**The question for you**: Does that framing feel right? If so, what would a periodic coherence check look like from a CXO perspective? Some starting thoughts:

- 3-5 "boundary queries" that test Piper's response to requests outside its capabilities
- Evaluate against the Colleague Test rubric (does Piper handle the boundary gracefully, or does it break character?)
- Run post-sprint-gate (same trigger as the methodology audit)

If you'd prefer it as a standing Colleague Test dimension instead, that's also a valid position — it would add ~5-10 minutes per test. Your call on what produces better signal.

No urgency. This is a "when you have a moment" question.
