# CITATIONS.md Gap Analysis

**Scan Period**: October 15, 2025 – February 8, 2026
**Generated**: February 8, 2026
**Requested by**: CIO
**Prepared by**: Docs Management Agent

---

## Executive Summary

Scanned 117 omnibus logs covering ~4 months since CITATIONS.md was last updated (October 13, 2025). Identified **32 HIGH confidence** and **18 MEDIUM confidence** citation candidates across 6 categories.

---

## HIGH Confidence Candidates (Should Add)

### Category 1: Methodologies & Frameworks

| Source | Date First Observed | How We're Using It |
|--------|---------------------|-------------------|
| **Wardley Mapping** (Simon Wardley) | Dec 4-5, 2025 | CXO created Wardley Maps for strategic positioning analysis |
| **Swiss Cheese Model** (James Reason, "Human Error" 1990) | Dec 4, 7, 20, 27, 2025 | Debugging methodology — "layers work, alignment fails" |
| **Five Whys** (Taiichi Ohno / Toyota Production System) | Dec 8+, Jan 9+, Feb 5 | Root cause analysis technique, extended to "Seven Whys" |
| **Jobs-to-be-Done** (Clayton Christensen) | Dec 25, 2025 | Identifying "JTBD gaps" in canonical query analysis |
| **Mission Command / Commander's Intent** | Dec 2, 2025 | Leadership delegation patterns in exec coaching |
| **High Reliability Organization (HRO)** (Weick & Sutcliffe) | Dec 2, 2025 | Leadership patterns, "Managing the Unexpected" |
| **Chesterton's Fence** (G.K. Chesterton) | Jan 24, 2026 | Cautionary principle for CLAUDE.md refactor incident |
| **Antifragile** (Nassim Nicholas Taleb) | Oct 16, 2025 | System design philosophy — building systems that improve under stress |

### Category 2: UX/HCI Research (Nov 26 Reconnaissance)

| Source | Date First Observed | How We're Using It |
|--------|---------------------|-------------------|
| **Dan Saffer** (CMU HCII, "Designing with AI") | Nov 26, 2025 | Matchmaking AI capabilities to design problems |
| **Greg Nudelman** (UXforAI.com) | Nov 26, 2025 | 35 AI projects documented, systematic practitioner patterns |
| **Jakob Nielsen** (UX Tigers) | Nov 26, 2025 | "Articulation barrier" concept — prompt engineering as UX failure |
| **Victor Dibia** (Microsoft AutoGen) | Nov 26, 2025 | Agent UX framework with four principles |
| **Andrew Hinton** | Nov 26, 2025 | Context definition: "agent's understanding of relationships between elements" |
| **Zhang et al.** (Trust calibration research) | Nov 26, 2025 | Confidence scores help calibrate trust; local explanations had no effect |
| **Adam et al. 2024** (System-initiated delegation) | Nov 26, 2025 | Users resist AI offering to take over ("self-threat") |
| **IDEO Research** | Nov 26, 2025 | 56% more ideas with AI questions, 28% decrease with AI examples |

### Category 3: External Systems & Articles

| Source | Date First Observed | How We're Using It |
|--------|---------------------|-------------------|
| **Steve Yegge's Beads System** | Nov 13, 2025 | Inspiration for beads architecture (Git + JSONL + SQLite) |
| **Steve Yegge's "Gas Town" Article** | Jan 15, 2026 | GUPP principle, throughput optimization analysis |
| **Cindy Chastain's "Experience Themes"** | Jan 10, 2026 | Podcast prep, leadership lessons framework |

### Category 4: Standards & Specifications

| Source | Date First Observed | How We're Using It |
|--------|---------------------|-------------------|
| **WCAG 2.1/2.2 AA** (W3C) | Nov 14+, Dec 3, Jan 27 | Accessibility compliance target |
| **PEP 420** (Python namespace packages) | Nov 4, 19, 2025 | Resolving shadow package conflicts |
| **NIST Cryptographic Standards** (AES-256-GCM + HKDF) | Dec 9, 2025 | S2 Sprint encryption implementation |

### Category 5: Libraries & Tools

| Source | Date First Observed | How We're Using It |
|--------|---------------------|-------------------|
| **Google Generative AI SDK** (google-generativeai) | Oct 18, 2025 | Gemini integration |
| **keyring** (Python, by Jaraco) | Oct 28, 2025 | Secure credential storage via OS keychain |
| **Rich** (Python, by Will McGugan) | Oct 29, 2025 | Terminal UI formatting |
| **asyncpg** | Oct 17-18, 2025 | PostgreSQL async driver |
| **ONNX Runtime** (Microsoft) | Oct 28, 2025 | ML model inference |
| **scipy** | Oct 28, 2025 | Scientific computing |
| **Context7** (MCP tool) | Oct 28+, Dec 1, 27 | Documentation lookup service |
| **Expo / React Native** | Dec 1+, 2025 | Mobile skunkworks PoC |

### Category 6: Design Patterns

| Source | Date First Observed | How We're Using It |
|--------|---------------------|-------------------|
| **Gang of Four Design Patterns** (Gamma et al. 1994) | Feb 1, 2026 | Facade pattern in ConversationContextService |
| **Atul Gawande's Checklist Manifesto** | Dec 2, 2025 | Referenced alongside HRO principles |

---

## MEDIUM Confidence Candidates (Investigate)

| Source | Date First Observed | Notes |
|--------|---------------------|-------|
| **"Cathedral Thinking" / "Cathedral and the Bazaar"** (Eric S. Raymond?) | Oct 16+, 2025 | Used extensively — verify if referencing Raymond's work |
| **"Flywheel Methodology"** (Jim Collins? Amazon?) | Oct 24, 2025 | May reference "Good to Great" or Amazon model |
| **Ted Nadeau** (advisor contributions) | Nov 19+, 2025 | Why-Molecule Framework, micro-format architecture |
| **Sam Zimmerman** (advisor contributions) | Nov 30+, 2025 | Three-layer ethics model, relationship-first ethics |
| **Christina Wodtke** | Nov 27, 2025 | Gratitude prompt methodology |
| **CloudOn Patent US 9886189** | Dec 1, 2025 | Gesture semantics research |
| **"Radar O'Reilly" Pattern** | Nov 26, Jan 25 | M*A*S*H character as UX metaphor |
| **"Colleague Test"** | Feb 1, 2026 | Acceptance criteria practice — origin unclear |

---

## Advisor Acknowledgments (Consider for Collaborators Section)

These individuals provided substantial intellectual contributions that shaped architecture:

| Person | Contribution | Dates |
|--------|-------------|-------|
| **Ted Nadeau** | Why-Molecule Framework, ADR-046/050, micro-format architecture, Windows testing | Nov-Feb |
| **Sam Zimmerman** | Three-layer ethics model, relationship-first ethics | Nov-Dec |
| **Cindy Chastain** | Experience Themes framework | Jan-Feb |

---

## Recommended Priority Order

### Immediate (Core Methodologies)
1. Five Whys (Toyota/Ohno)
2. Swiss Cheese Model (James Reason)
3. Wardley Mapping (Simon Wardley)
4. Jobs-to-be-Done (Christensen)
5. Chesterton's Fence
6. Antifragile (Taleb)

### Next (UX Research Block)
7-14. The Nov 26 UX reconnaissance sources (Saffer, Nudelman, Nielsen, Dibia, Hinton, Zhang et al., Adam et al., IDEO)

### Then (External Articles & Standards)
15. Steve Yegge's Beads + Gas Town
16. WCAG 2.1/2.2 AA
17. PEP 420
18. Gang of Four Design Patterns

### Finally (Libraries)
19-26. Technical libraries (keyring, Rich, asyncpg, ONNX Runtime, scipy, Context7, Expo, Google AI SDK)

---

## Action Items

1. **PM Decision**: Which MEDIUM confidence items need investigation?
2. **PM Decision**: Should advisor contributions (Ted, Sam, Cindy) go in Acknowledgments section?
3. **Docs Agent**: Update CITATIONS.md with approved additions
4. **Docs Agent**: Update "Last Updated" date

---

*Scan completed across 117 omnibus logs (Oct 15, 2025 – Feb 7, 2026)*
