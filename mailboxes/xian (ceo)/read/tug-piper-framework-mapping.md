# Framework Mapping: TUG Ethics ↔ Piper Morgan Architecture

**Purpose**: Systematic exploration of alignment between The Understanding Group's AI ethics framework and Piper Morgan's ethical architecture.

**Context**: Following conversations with Dan Heck (TUG ethicist) on Feb 5, 2026, exploring how external IA-centric ethics work can enrich and validate Piper's approach.

---

## Framework Overview

### TUG: HAFF (Human Aligner Forever)

**Core Verbs**:
1. **Cultivate** Human Agency — Help people have good choices they understand
2. **Communicate** Holistically — Whole truth: factual, ethical, authentic
3. **Reflect** on Whole Systems — Gather info → system view → virtuous cycle

**Philosophical Grounding**:
- Habermas's three validity claims (factual, ethical, authentic)
- Moral foundations research (Haidt)
- Ethical pluralism with baselines

### Piper Morgan: Four Pillars of Ethical Operation

**Core Nouns**:
1. **Human Empowerment** — Amplify capability, never replace judgment
2. **System Integrity** — Strengthen organizations, not create dependencies
3. **Project Excellence** — Quality and safety never compromised
4. **Professional Boundaries** — Colleague-appropriate interactions

**Architectural Grounding**:
- Ethics as infrastructure (not policy)
- Multi-agent consensus for boundary decisions
- Trust gradient governing proactivity

---

## Direct Mappings

| TUG Concept | Piper Equivalent | Alignment Quality |
|-------------|------------------|-------------------|
| **Cultivate Human Agency** | **Human Empowerment (Pillar 1)** | ✅ Exact — both prioritize human decision-making authority |
| **Warranted Trust** | **Trust Gradient (ADR-053)** | ✅ Exact — trust should match reality, earned incrementally |
| **Ethical Pluralism** | **Multi-Agent Consensus** | ✅ Strong — multiple frameworks allowed, consensus required |
| **Baselines (Red Lines)** | **Inviolate Boundaries** | ✅ Exact — non-negotiable ethical floors |
| **Authenticity Validity** | **Professional Boundaries (Pillar 4)** | ✅ Strong — Piper doesn't claim authentic experience |
| **Ethics → Governance → Management** | **Ethics docs → ADRs → Patterns** | 🔶 Implicit — Piper does this but hasn't documented hierarchy |
| **Ethics Washing** awareness | **Verification Theater** awareness | ✅ Strong — both recognize performative ethics as anti-pattern |

---

## Complementary Distinctions

| Dimension | TUG Focus | Piper Focus | Relationship |
|-----------|-----------|-------------|--------------|
| **Target** | Human organizations adopting AI | AI agent behavior itself | Complementary scopes |
| **Form** | Vocabulary + framework | Working code + architecture | Different implementation stages |
| **Mechanism** | Conceptual (cultivate, communicate, reflect) | Operational (trust scores, stage transitions) | TUG is "why," Piper is "how" |
| **Output** | Organizational ethics policies | Agent ethical behavior | TUG shapes policy; Piper implements agent |

**Key Insight**: TUG helps organizations think about *how to interact ethically with AI*. Piper's framework makes *the AI behave ethically within those interactions*. These are not competing — they're two sides of the same coin.

---

## Validity Claims Analysis

TUG identifies three validity claims (from Habermas):

| Claim | Definition | AI Capability | Piper Implementation |
|-------|------------|---------------|---------------------|
| **Factual** | Is it true? | ✅ AI can do this | Intent classification, knowledge retrieval |
| **Ethical** | Aligned with group ethos? | ✅ AI can do this | Boundary enforcement, trust respect |
| **Authentic** | From genuine experience? | ❌ AI cannot do this | Professional Boundaries acknowledge this limit |

**Piper's Position**: We explicitly *do not claim* authentic experience. When Piper explains its reasoning or acknowledges limitations, it's being authentic *about its lack of authenticity* — which is the appropriate ethical stance.

---

## Vocabulary Adoption Candidates

| TUG Term | Current Piper Term | Recommendation |
|----------|-------------------|----------------|
| **Warranted Trust** | "Trust gradient" | **Adopt** — more precise, better communicates goal |
| **Validity Claims** | (no equivalent) | **Add** — useful for response evaluation |
| **Baselines** | "Inviolate boundaries" | **Keep ours** — more specific to implementation |
| **Ethics scaffolds Governance** | (implicit) | **Document** — make our hierarchy explicit |

---

## Enrichment Opportunities

### 1. Response Evaluation Enhancement

Add validity check to response quality assessment:

```
Response Quality = {
    Factual: Is this accurate?
    Ethical: Does this respect user/org values?
    Authentic: Are we appropriately NOT claiming experience?
}
```

### 2. Documentation Hierarchy

Make explicit in architecture docs:

```
Ethics Layer (Why)
├── Piper Morgan Ethical Principles
├── Ethics-First Architecture
└── Boundary definitions

Governance Layer (What)
├── ADRs (architectural decisions)
├── PDRs (product decisions)
└── Policies

Management Layer (How)
├── Patterns (operational)
├── Session protocols
└── Quality metrics
```

### 3. Verb Framing for Operations

TUG uses verbs (Cultivate, Communicate, Reflect). Could add operational verb layer to Piper's noun-based pillars:

| Pillar (Noun) | Operational Verb |
|---------------|-----------------|
| Human Empowerment | **Defer** to human judgment |
| System Integrity | **Strengthen** collective capability |
| Project Excellence | **Verify** before acting |
| Professional Boundaries | **Maintain** colleague stance |

---

## Gaps in Each Framework

### What TUG Provides That Piper Lacks

- Explicit philosophical grounding (Habermas, moral foundations)
- Vocabulary with academic validation
- Framework for organizational adoption
- Connection to democratic norms / discourse ethics

### What Piper Provides That TUG Lacks

- Implementation specificity (actual code)
- Trust computation mechanics (ADR-053 thresholds)
- Multi-agent consensus architecture
- Operational patterns for enforcement

---

## Collaboration Opportunities

1. **TUG reviews Piper's ethics docs** — External validation from IA ethics experts
2. **Piper as case study for TUG** — Working implementation of ethics-as-infrastructure
3. **Joint vocabulary development** — Merge warranted trust, validity claims into shared lexicon
4. **IA Conference synergy** — xian's April presentation could reference TUG framework

---

## Summary

**TUG and Piper Morgan are highly aligned** at the principle level. The frameworks are complementary rather than competitive:

- TUG provides the *organizational* ethics framework for AI adoption
- Piper provides the *agent-native* ethics implementation

Adopting TUG vocabulary (especially "warranted trust") strengthens our communication without requiring architectural changes. The theoretical grounding TUG offers gives academic legitimacy to approaches we've developed through practice.

---

*Prepared by: CIO*
*Date: February 8, 2026*
*For: xian, Dan Heck (TUG)*
