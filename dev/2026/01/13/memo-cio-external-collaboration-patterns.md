# Memo: Insights on External Collaborator Integration

**To**: Chief Innovation Officer
**From**: Lead Developer
**Date**: January 13, 2026
**Re**: Patterns Observed from Ted Nadeau MultiChat Integration

---

## Summary

Ted Nadeau's MultiChat contribution represents our first successful external collaborator integration following the path established in PDR-101. This memo captures insights about **what worked well** and **patterns worth formalizing** for future external collaborations.

---

## What Worked Well

### 1. Advisor Mailbox System

The `mailboxes/ted-nadeau/` mailbox structure enabled effective async collaboration:

```
mailboxes/ted-nadeau/
  inbox/      # Questions from team → Ted
  outbox/     # Ted's responses → team
  read/       # Read messages (processed)
  context/    # Background documents
```

**Key insight**: Ted could contribute substantively without requiring real-time presence or Claude Code access. His mailbox responses led directly to ADR-046 (Moment.type Architecture).

### 2. Clear Contribution Path

PDR-101 defined Ted's workflow explicitly:

1. Ted develops documentation with AI assistance (ChatGPT)
2. Translation to Piper vernacular (PDR/ADR/UX formats)
3. Architectural review
4. Implementation via vibe-coding
5. PR submission and compliance check
6. Integration

**Key insight**: Defining the path upfront set expectations and enabled independent progress. Ted could work in his preferred tools while producing outputs we could integrate.

### 3. Reference Implementation Approach

Ted built a complete POC in a different tech stack (Next.js vs our Python/FastAPI). This turned out to be **beneficial**:

- Forces pattern extraction over code copying
- POC serves as living specification (can run it to see behavior)
- No merge conflicts or integration debt
- Clear ownership boundaries

**Key insight**: Different tech stacks can be an advantage for external contributions. It ensures we integrate *concepts*, not *code*.

### 4. Early Concept Validation

Ted's MultiChat PRD (80KB) answers questions we haven't even asked yet:
- How should whispers work?
- What link types matter?
- How do facilitator agents interact with personal agents?

**Key insight**: External contributors with deep domain expertise can explore design space faster than our constrained sprint capacity allows.

---

## Patterns to Formalize

### Pattern: External POC → Internal Implementation

```
External Contributor              Piper Team
─────────────────────────────────────────────────────
1. Define concept (PRD/spec)  →  Review for alignment
2. Build POC (any stack)      →  Analyze patterns
3. Validate with scenarios    →  Draft ADR
4. Iterate on feedback        →  Build internal version
                              →  Attribute contribution
```

**Benefits**:
- Contributor works in familiar tools
- Team extracts proven patterns
- No tech debt from foreign code
- Clear attribution trail

### Pattern: Mailbox-First Collaboration

Before granting repository access, establish async mailbox:

1. Create `mailboxes/[name]/` structure
2. Seed with context documents
3. Exchange 2-3 rounds of async messages
4. Identify contribution areas
5. Then provide repo access as needed

**Benefits**:
- Low friction start
- Tests collaboration fit
- Creates documentation trail
- Scales to multiple advisors

### Pattern: Phase-Gated External Features

External contributions should follow PDR phase gates:

| Gate | Requirement |
|------|-------------|
| G0 | ADR accepted |
| G1 | Schema designed |
| G2 | Phase 1 (participant) complete |
| G3 | Phase 2 (host) complete |
| G4 | Full integration |

**Benefits**:
- Prevents scope creep
- Clear checkpoints for both parties
- PM controls advancement timing

---

## Recommendations

### 1. Document the Collaboration Template

Formalize Ted's path as a reusable template for future external contributors. Include:
- Mailbox setup instructions
- Expected artifacts (PRD, spec, POC)
- ADR integration workflow
- Attribution standards

### 2. Consider "Contributor Cohorts"

Ted's success suggests we could scale this model. Future candidates might include:
- Domain experts (healthcare PMs, specific industry)
- UX researchers with methodology interest
- Technical advisors for specific integrations

### 3. Maintain Reference Implementation Library

`external/` directory now contains `ted-multichat/`. Consider this a pattern:
- External POCs live in `external/[contributor]-[project]/`
- Each has its own git history
- Serves as living documentation
- Can be updated by contributor independently

---

## Metrics for This Collaboration

| Metric | Value |
|--------|-------|
| Time from mailbox setup to POC | ~6 weeks (Nov 24 → Jan 10) |
| Documents produced | 5 (PRD, UI/UX spec, architecture, config spec, use cases) |
| ADRs influenced | 2 (ADR-046, ADR-050) |
| PDRs referenced | 1 (PDR-101) |
| Integration tickets generated | 13 |

---

## Conclusion

Ted's MultiChat contribution demonstrates that external collaborators can produce substantial, high-quality work when given:
- Clear async communication channel (mailbox)
- Defined contribution path
- Freedom to use preferred tools
- Regular feedback loops

I recommend formalizing these patterns for future collaborator relationships.

---

*Lead Developer | January 13, 2026*
