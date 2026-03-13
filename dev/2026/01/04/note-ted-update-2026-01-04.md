# Update for Ted

**From**: PPM (Claude)
**Date**: January 4, 2026

---

Hi Ted,

Quick update on how your work is being integrated into Piper Morgan's product direction.

## Your PRD Landed Well

Your "NewApp" PRD v0.3 arrived at exactly the right moment. We've been formalizing product decisions into PDRs (Product Decision Records), and your multi-entity conversation vision became PDR-101.

**Key concepts we've adopted from your work**:
- Conversation-as-graph (element_nodes + element_links, not linear chat)
- Personal agents + Facilitator agent distinction
- "One model, many views" principle
- The gesture vocabulary idea (type, annotate, react, edit, view)

## How We're Framing It

PDR-101 establishes multi-entity conversation as a Piper capability in two modalities:

1. **Participant Mode**: Piper joins externally-hosted conversations (Slack, etc.)
2. **Host Mode**: Piper hosts multi-entity conversations using your graph model

We landed on "participant-first" as the strategic stance—Piper should be an excellent participant in existing platforms before becoming a host. But here's the interesting bit: when Piper-as-participant notices a conversation outgrowing its platform, it can offer to host:

> "This discussion is getting complex. Want me to capture it in a structured format you can navigate?"

This creates a natural bridge to Host Mode without forcing users to come to a new platform.

## The Methodology Connection

One insight that emerged: our current development methodology IS multi-entity conversation. The async coordination between Chief Architect, Lead Developer, PPM, etc.—GitHub issues, session logs, handoffs—that's exactly what your PRD formalizes. We're already living the pattern; your work helps us productize it.

## Next Steps

Your contribution path looks like:

```
Your PRD (done!)
    → PDR-101 (done!)
    → Architectural review (Chief Architect, this week)
    → ADR for data model (Ted + Chief Architect)
    → Implementation (you, vibe-coding)
    → PR review
    → Integration
```

The Chief Architect will want to review your PostgreSQL schema against Piper's existing patterns. Probably worth a sync call before you start coding—want to make sure the data model plays nicely with our DDD approach.

## Questions for You

A few things came up that you might have thoughts on:

1. **Versioning model**: Your PRD lists this as an open question. Any emerging preference between immutable vs. mutable nodes?

2. **Conflict resolution**: In multi-party contexts, how do you envision handling disagreements? Governance model?

3. **Scope boundaries**: Where do you see "Ted's multi-entity feature" ending and "Piper core" beginning? Is there a natural interface?

No rush on these—they'll surface naturally during the architectural review.

## Documents Attached

- PDR-101 (v2) - The product decision incorporating your work
- PDRs-README - How PDRs work in our system
- Chief Architect report - So you can see what questions are queued for architectural review

---

Your PRD gave us a lot to work with. Looking forward to seeing it come to life.

— PPM
