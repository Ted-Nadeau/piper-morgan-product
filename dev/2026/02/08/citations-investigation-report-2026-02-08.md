# Citations Investigation Report

**Date**: February 8, 2026
**Requested by**: PM + CIO
**Prepared by**: Docs Management Agent

---

## Investigation Summary

Deep investigation of MEDIUM confidence items from initial gap analysis, plus verification of metaphor origins.

---

## Part 1: Metaphor Origins

### "Cathedral Thinking" / "Cathedral Builder"

**Finding**: Two distinct traditions exist, and yours appears to be the *second* (purpose/long-term), not the first (Raymond's open source model).

| Tradition | Source | Meaning | Your Usage |
|-----------|--------|---------|------------|
| **Raymond's Cathedral** | Eric S. Raymond, "The Cathedral and the Bazaar" (1997) | *Negative* — closed, top-down, slow development vs. the open "bazaar" | NOT this |
| **Christopher Wren Parable** | Bruce Barton, "What Can a Man Believe?" (1927) | *Positive* — long-term purpose, "I'm building a cathedral" mindset | **This is yours** |

**The Wren Story**: After the Great Fire of 1666, Christopher Wren asks three bricklayers what they're doing. First says "laying bricks," second says "earning wages," third says "building a cathedral." The story is likely **apocryphal** — no documentary evidence from Wren's era, first appears in 1927.

**Recommendation**: If citing, acknowledge as "commonly attributed to Christopher Wren" or "the 'cathedral builder' parable" rather than claiming it as a verified historical event. The concept of "cathedral thinking" (long-term projects for future generations) is now widely used independently of both Raymond and Wren.

Sources:
- [Three Bricklayers origin investigation](https://djchuang.com/origin-story-parable-of-the-three-bricklayers/)
- [Sacred Structures analysis](https://sacredstructures.org/mission/the-story-of-three-bricklayers-a-parable-about-the-power-of-purpose/)

---

### Saint-Exupéry "Endless Immensity of the Sea" Quote

**Finding**: This is a **folk paraphrase**, not an actual Saint-Exupéry quote.

| Version | Source | Status |
|---------|--------|--------|
| "If you want to build a ship, don't drum up people to collect wood... but rather teach them to long for the endless immensity of the sea" | Popular attribution | **Not verified** |
| Original passage in *Citadelle* (1948) | Saint-Exupéry | Different wording, looser connection |

The modern quote first appeared in a 1995 diet book (!), then circulated anonymously before being attributed to Saint-Exupéry around 2007. Quote Investigator calls it "one of the rare cases where a paraphrase has more impact than the original."

**Recommendation**: Cite as "commonly attributed to Saint-Exupéry" or "inspired by *Citadelle*" — this is an honest folk-wisdom attribution, not a direct quote.

Source: [Quote Investigator analysis](https://quoteinvestigator.com/2015/08/25/sea/)

---

## Part 2: Flywheel Origins

### Jim Collins' Flywheel (2001)

The flywheel concept originates from **Jim Collins, "Good to Great" (October 2001)**. The metaphor: a 5,000-pound flywheel that takes enormous effort to start moving but builds momentum with each push.

**Key insight**: "Good to great comes about by a cumulative process—step by step, action by action, decision by decision, turn by turn of the flywheel."

### Amazon Flywheel / Virtuous Cycle

Jeff Bezos famously sketched the Amazon flywheel **on a napkin in 2001** after studying Collins' work. Amazon hired Collins to teach the executive team "the flywheel effect."

### Product-Led Growth Flywheel

The term has proliferated into product management, growth loops, and PLG frameworks. Appcues, Amplitude, ProductLed, and others have created their own "flywheel" frameworks.

### Your "Excellence Flywheel"

**Assessment**: Homegrown. The *metaphor* draws from Collins' widespread terminology, but your specific definition (Systematic Verification First → Test-Driven Development → Multi-Agent Coordination → GitHub-First Tracking) is bespoke. The flywheel metaphor is now nearly a commodity term — what makes yours distinct is the specific components and how they reinforce each other.

**Recommendation**: No external citation needed for "Excellence Flywheel" — it's your original application. Could optionally acknowledge Collins as the origin of the flywheel metaphor in business contexts.

Sources:
- [Jim Collins - The Flywheel Effect](https://www.jimcollins.com/concepts/the-flywheel.html)
- [Amazon Flywheel origin](https://feedvisor.com/resources/amazon-trends/amazon-flywheel-explained/)

---

## Part 3: Internal Coinages (No Citation Needed)

These appear in the omnibus logs but have no external origin — they're your original terms:

| Term | Status | Notes |
|------|--------|-------|
| **"Radar O'Reilly Pattern"** | Original | M*A*S*H character reference for anticipatory assistance. The broader concept is "anticipatory design" in UX, but this specific naming is yours. |
| **"Colleague Test"** | Original | Acceptance criteria practice. No external framework found. |
| **"75% Pattern"** | Original | Anti-pattern for abandoned implementations |
| **"Inchworm Protocol"** | Original | Development methodology for incremental progress |
| **"Two Parallel Realities"** | Original | Architectural observation |

---

## Part 4: Advisor Contributions

### Ted Nadeau

**Status**: Personal advisor + alpha tester with substantial technical contributions.

**Contributions documented**:
- Why-Molecule Framework (Intent Specification DSL)
- ADR-046, ADR-050 contributions
- Micro-format architecture proposal (11 format types)
- Windows testing + 14 extracted issues

**Recommendation**: Add to Acknowledgments section as advisor. The Why-Molecule Framework appears to be collaborative/internal work, not previously published.

---

### Sam Zimmerman

**Status**: Ethics advisor with architectural contributions.

**Contributions documented**:
- Three-layer ethics model: Inviolate boundaries / Adaptation mechanism / Ethical style
- "Relationship-first ethics" framing

**Recommendation**: Add to Acknowledgments section as advisor. No published external work found for this specific framework.

---

### Cindy Chastain

**Status**: Advisor + podcast collaborator with **published external work**.

**Published Work Found**:
- **"Experience Themes: An Element of Story Applied to Design"**
  - Published: [Boxes and Arrows](https://boxesandarrows.com/experience-themes/) (2009)
  - Presented: IA Summit 2009, UX Savannah 2010
  - Framework: Using narrative themes from user research to guide UX design

**Quote**: "An Experience Theme is basically an over-arching statement or phrase that encapsulates the value and focus of the experience we intend to deliver to users."

**Recommendation**: Add to CITATIONS.md as external published work. Also add to Acknowledgments as advisor.

---

### Christina Wodtke

**Status**: Referenced for gratitude prompt methodology.

**Published Work Found**:
- **"Radical Focus: Achieving Your Most Important Goals with Objectives and Key Results"** (2016, 2nd ed. 2021)
- One of the four people who shaped OKRs (alongside Doerr, Grove, Drucker)
- Friday celebrations as "antidote to Monday's grim business"

**Note**: The specific "gratitude prompt" methodology ("Knowing what you know about me, what should I be grateful for today?") was referenced in the Nov 27 omnibus but I couldn't find this as a published Wodtke technique. May be from personal communication or a different source.

**Recommendation**: If using OKR/celebration concepts, cite "Radical Focus." The gratitude prompt may be original or from personal advice.

Sources:
- [Radical Focus on Amazon](https://www.amazon.com/Radical-Focus-Achieving-Important-Objectives/dp/0996006087)
- [Christina Wodtke's website](https://cwodtke.com/)

---

## Part 5: Steve Yegge's Work (Verified)

### Beads

**Full Citation**:
- **Steve Yegge** - "Introducing Beads: A coding agent memory system" (Medium, December 2025)
- GitHub: https://github.com/steveyegge/beads
- Architecture: Git-backed JSONL + SQLite cache for agent memory

**Key concept**: Solves the "50 First Dates" problem — agents wake up with no memory of yesterday's work.

### Gas Town

**Full Citation**:
- **Steve Yegge** - "Welcome to Gas Town" (Medium, January 2026)
- GitHub: https://github.com/steveyegge/gastown
- Multi-agent orchestration framework for AI coding

**Key concept**: GUPP (Gas Town Universal Propulsion Principle) — "If there is work on your hook, YOU MUST RUN IT."

**Note**: Your omnibus logs show analysis and comparison to Piper's mailbox system, but you deliberately chose NOT to adopt the throughput-first philosophy wholesale.

---

## Summary: Actions by Category

### Add to CITATIONS.md

| Source | Category | Priority |
|--------|----------|----------|
| Cindy Chastain, "Experience Themes" (Boxes and Arrows, 2009) | UX Framework | HIGH |
| Steve Yegge, "Beads" (2025) | Agent Architecture | HIGH |
| Steve Yegge, "Gas Town" (2026) | Agent Orchestration | HIGH |
| Christina Wodtke, "Radical Focus" (2016) | Methodology | MEDIUM |
| Jim Collins, "Good to Great" / Flywheel (2001) | Optional | LOW (metaphor only) |

### Add to Acknowledgments Section

| Person | Role | Contribution |
|--------|------|--------------|
| Ted Nadeau | Advisor + Alpha Tester | Why-Molecule Framework, ADRs, micro-formats, Windows testing |
| Sam Zimmerman | Ethics Advisor | Three-layer ethics model, relationship-first ethics |
| Cindy Chastain | Advisor + Collaborator | Experience Themes framework (also cite published work) |

### Document as Original Work

| Term | Status |
|------|--------|
| "Cathedral Thinking" (your usage) | Original application of folk parable |
| "Excellence Flywheel" | Original framework using common metaphor |
| "Radar O'Reilly Pattern" | Original coinage |
| "Colleague Test" | Original practice |

### Optional Footnotes

| Item | Note |
|------|------|
| Christopher Wren / Three Bricklayers | "Commonly attributed" — apocryphal |
| Saint-Exupéry sea quote | "Commonly attributed" — folk paraphrase |

---

*Investigation completed February 8, 2026*
