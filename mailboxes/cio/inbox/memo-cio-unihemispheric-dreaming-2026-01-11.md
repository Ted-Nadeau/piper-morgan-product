# Memo: Unihemispheric Dreaming — A Scaling Consideration for Learning Architecture

**To**: Chief Architect, Principal Product Manager, Chief Experience Officer
**From**: Chief Innovation Officer
**Date**: January 11, 2026
**Re**: Potential design constraint for Piper's learning/dreaming system
**Status**: Request for Input (not urgent, no immediate action required)

---

## Context

Our current model for Piper's learning system uses a "dreaming" metaphor: during idle periods (e.g., when the user is asleep or away), Piper processes accumulated experience—composting raw interactions into durable learning. This mirrors human sleep's role in memory consolidation.

The trigger mechanism we've discussed is idle-time-based: after X hours without interaction, a background job initiates the dreaming cycle.

## The Scaling Problem

This model assumes predictable idle time. That assumption may not hold as Piper scales:

| Scenario | Problem |
|----------|---------|
| **Power user** | Frequent interactions, never long gaps |
| **Multi-user/team** | Different time zones, always someone active |
| **Dense scheduled jobs** | Background processing fills "idle" windows |

In these scenarios, dreaming gets indefinitely deferred. Learning doesn't happen. This is functionally equivalent to sleep deprivation—cognitive degradation over time.

## A Possible Frame: Unihemispheric Sleep

Dolphins (coincidentally, Piper's mascot) sleep with one brain hemisphere at a time—maintaining vigilance while still processing. Humans exhibit a milder version: the "first night in a hotel" phenomenon where part of the brain stays alert in unfamiliar environments.

This suggests an alternative architecture: **partial, rotating dreaming cycles** rather than all-or-nothing idle-time dreaming.

Conceptually:
- Piper's "mind" could have separable components that can sleep independently
- Some components dream while others remain responsive
- Cycles rotate, ensuring all components eventually process
- Vigilance is never fully sacrificed

## Questions This Raises

I'm not proposing a solution—I'm flagging a design constraint that should inform how we build the learning system. The questions I'd like your input on:

### For Chief Architect

1. **Separability**: What would it mean architecturally for learning to be partitioned? Domain-specific (Slack vs. Calendar)? User-specific? Temporal (recent vs. long-term)?
2. **Trigger mechanisms**: If not idle time, what signals dreaming cycles? Time rotation? Load thresholds? Quality degradation signals?
3. **Backlog timing**: Is this a constraint we should capture now for the learning system epic, or is it premature optimization?

### For Principal Product Manager

1. **Value proposition fit**: Does "Piper that learns continuously without downtime" matter to users? Or is "learns while you sleep" sufficient for v1?
2. **Scaling assumptions**: What usage patterns do we actually expect? Solo PM? Team-shared Piper? Enterprise multi-tenant?
3. **Competitive framing**: Do other AI assistants have visible learning cycles? Is "always learning" a differentiator or table stakes?

### For Chief Experience Officer

1. **User mental model**: Should users be aware of dreaming cycles? ("Piper is processing what we discussed") Or should it be invisible?
2. **Trust implications**: Does "partial sleep" affect the trust gradient? Does a "drowsy" Piper behave differently?
3. **MUX integration**: Does this concept affect the entity lifecycle or consciousness model? Is "dreaming state" a modeled UX element?

## Why I'm Raising This Now

We're close to completing B1, and MUX super-epic work is next. The learning system (Knowledge Graph, composting pipeline) is on the horizon. I want to ensure that when we design the dreaming mechanism, we don't paint ourselves into a corner that only works for solo users with predictable schedules.

This memo is exploratory. I'm not asking for immediate decisions—just your perspectives so I can synthesize a proposal that accounts for architectural, product, and experience considerations.

---

*Looking forward to your thoughts whenever time permits.*

— CIO
