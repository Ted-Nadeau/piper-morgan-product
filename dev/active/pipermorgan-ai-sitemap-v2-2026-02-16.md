# pipermorgan.ai — Information Architecture Sketch v2

**Version**: Draft v2
**Date**: February 16, 2026
**Author**: CXO
**Changes from v1**: Added Trust Signal section to homepage; clarified homepage section sequence and purposes

---

## Site Map

```
pipermorgan.ai
│
├── / (Homepage)
│   ├── Hero + Primary CTA
│   ├── Trust Signal ("your data stays yours")
│   ├── Differentiation ("work between the work")
│   ├── What Piper Does (capability highlights)
│   ├── Why Trust Us (building in public proof)
│   └── Secondary CTAs in footer area
│
├── /try (Primary CTA destination)
│   ├── Branching page: "How adventurous are you?"
│   │   ├── → /try/alpha ("I'm ready now")
│   │   │     └── Alpha signup process
│   │   │     └── Links to pmorgan.tech setup
│   │   │
│   │   └── → /try/beta ("Tell me when it's easier")
│   │         └── Beta waitlist form
│   │         └── Optional: role, tools, pain points, referral source
│   │
│   └── [Future: /try/start — direct product access when available]
│
├── /get-involved (Secondary CTA destination)
│   ├── Contributor overview
│   ├── → pmorgan.tech (setup guides, technical docs)
│   ├── → GitHub repository
│   └── [Future: community/Discord/forum links]
│
├── /journey (Tertiary — existing blog content)
│   ├── Blog index (building-in-public posts)
│   ├── Weekly Ships archive
│   └── Individual post pages
│
├── /methodology (Tertiary — how we work)
│   ├── Excellence Flywheel overview
│   ├── Systematic approach explanation
│   └── → Links to deeper methodology content
│
├── /playbook (Tertiary — when ready)
│   └── AI Leadership Playbook content
│   └── [Gated or ungated TBD]
│
├── /about
│   ├── Project story
│   ├── Your (xian's) background
│   └── Vision / where this is going
│
└── [Global elements]
    ├── Header nav: [Try Piper] [Get Involved] [Journey ▾] [About]
    ├── Footer: Newsletter signup, social links, pmorgan.tech link
    └── [Mobile: hamburger menu with same structure]
```

---

## Homepage Section Specification

This is the primary change in v2. Each section has a defined job, visitor mindset, and content guidance.

### Section 1: Hero

| Attribute | Value |
|-----------|-------|
| **Job** | Make the promise |
| **Visitor mindset** | "Tell me what this is" |
| **Length** | 2 lines max + CTA button |

**Content direction**:
- Headline: "THINK BIGGER"
- Subhead: "Piper holds the threads so you can focus on the decision."
- CTA: [Try Piper Morgan]

**Design notes**: Clean, confident, breathing room. No competing messages.

---

### Section 2: Trust Signal (NEW in v2)

| Attribute | Value |
|-----------|-------|
| **Job** | Address AI data anxiety immediately |
| **Visitor mindset** | "Can I trust this with my stuff?" |
| **Length** | 3-4 lines |

**Content direction**:
- Lead: "Your work. Your patterns. Yours."
- Body: What Piper learns about you isn't stored in public databanks or used to train someone else's model. It stays with you.

**Design notes**:
- Visually distinct from hero but connected (not a jarring break)
- Confident tone, not defensive
- Short — this reassures, it doesn't argue

**Why this placement**: The trust question arises *after* interest but *before* understanding. Placing it here prevents the anxiety from blocking engagement with the rest of the page.

**Connection to colleague framing**: A colleague doesn't report your conversations to a central authority. The data ownership philosophy is *why* Piper can be a colleague rather than a tool. This connection can be made explicit on /about or /methodology, but doesn't need to be stated in this section.

---

### Section 3: Differentiation

| Attribute | Value |
|-----------|-------|
| **Job** | Explain what makes Piper different |
| **Visitor mindset** | "How is this different from other tools?" |
| **Length** | Short paragraph (4-6 lines) |

**Content direction**:
- Core insight: "PM tools assume work is items in lists. But PM work is actually relationships between concerns at different scales."
- Texture: "Decisions ripple. Timelines interlock."
- Landing: "Piper is built for that reality."

**Design notes**: This is the intellectual hook for methodology-curious visitors. Keep it sharp.

---

### Section 4: What Piper Does

| Attribute | Value |
|-----------|-------|
| **Job** | Show specific capabilities |
| **Visitor mindset** | "What will it actually do for me?" |
| **Length** | 3-5 capability highlights |

**Content direction**: TBD by Comms. Possible angles:
- Morning standups that know your context
- Tracks what connects across tools
- Surfaces what matters when you need it
- Grows with you over time

**Design notes**: Can be visual (icons, cards) or prose. Should feel concrete after the abstract differentiation section.

---

### Section 5: Why Trust Us

| Attribute | Value |
|-----------|-------|
| **Job** | Provide credibility proof |
| **Visitor mindset** | "Why should I believe you?" |
| **Length** | Short section with links out |

**Content direction**:
- 160+ blog posts documenting the journey
- Open methodology, systematic approach
- Building in public since [date]
- Links to /journey, /methodology

**Design notes**: This is different from the Trust Signal (Section 2). Section 2 is about *data philosophy* ("your stuff stays yours"). Section 5 is about *credibility* ("we're doing this honestly"). Both belong; they address different concerns.

---

### Section 6: Footer CTAs

| Attribute | Value |
|-----------|-------|
| **Job** | Catch visitors ready to act |
| **Visitor mindset** | "I'm interested, what's next?" |

**Content direction**:
- Newsletter signup
- Get Involved link
- Social links
- pmorgan.tech link

---

## Trust Signal Reinforcement on Other Pages

The homepage establishes the data ownership claim. Other pages can reinforce without repeating:

| Page | Treatment |
|------|-----------|
| /try/alpha | "Your data stays local to your installation" |
| /try/beta | Standard privacy note ("We won't share your information") |
| /about | Expand into philosophy/values section |
| /methodology | Connect to "colleague" framing — why data ownership enables the relationship |

---

## Navigation Design

*Unchanged from v1*

### Primary Nav (Header)

| Item | Type | Destination |
|------|------|-------------|
| **Try Piper** | Button (emphasized) | /try |
| Get Involved | Link | /get-involved |
| Journey ▾ | Dropdown | /journey, /methodology, /playbook |
| About | Link | /about |

---

## Open Questions (Updated)

### Resolved Since v1

- **Trust Signal placement**: Confirmed — immediately after hero, before differentiation

### Still Open

1. **Journey dropdown naming**: Journey/Methodology/Playbook vs Blog/How It Works/Playbook
2. **Newsletter placement**: Footer only vs footer + /journey vs more aggressive
3. **/playbook timing**: Omit until ready (current recommendation)
4. **pmorgan.tech relationship**: Light /get-involved on pipermorgan.ai linking out (current recommendation)

---

## Next Steps

1. ✅ **CXO** — Sitemap v2 with trust signal section (this document)
2. → **Comms** — Draft copy for each homepage section
3. → **CXO** — Review copy for UX fit
4. → **Iterate** as needed
5. → **Designer** — Implementation gameplan

---

*IA sketch v2. Ready for Comms to draft homepage copy.*
