# Piper Morgan Wiki — Structure Proposal

**Date**: March 9, 2026
**Prepared by**: Documentation Management Specialist
**Status**: Draft for PM review

---

## Design Principles

1. **Two entry points**: Testers/contributors come for practical help; observers come for the story and methodology. Both should find what they need from the home page.
2. **High transparency**: The multi-agent methodology, patterns, and development philosophy are part of the project's value — share them openly.
3. **Living document**: Wiki pages should be maintainable by agents during regular doc sweeps, not a one-time dump that goes stale.
4. **Complement, don't duplicate**: The wiki curates and contextualizes — it links to repo files for details rather than copying entire documents.
5. **Encouraging tone**: Lower the barrier. Make it clear that participation is welcome, imperfection is expected, and the project is genuinely collaborative.

---

## Proposed Page Structure

### Home
- What is Piper Morgan (2-3 sentences)
- Who's building it and why
- Two paths: "I want to try it" → Getting Started; "I want to understand it" → About the Project
- Current version and status badge
- Links to blog, website, repo

---

### Section 1: For Participants

#### Getting Started
- Prerequisites (Docker, Python 3.11+, API keys)
- Quick setup (clone, configure, run — adapted from ALPHA_QUICKSTART)
- First conversation walkthrough
- Common setup issues and fixes (drawn from Ted/Dominique experiences)

#### Known Issues & Workarounds
- Current known issues (adapted from ALPHA_KNOWN_ISSUES)
- Platform-specific notes (macOS, Windows, Linux)
- How to report a bug (GitHub issue template guidance)

#### How to Contribute
- Ways to help (testing, filing issues, sharing feedback, methodology discussion)
- Git workflow for contributors (fork → branch → PR, now that branch protection is on)
- Code conventions quick reference
- Where to find us (GitHub issues, any other channels)

#### Feature Guide
- What Piper can do today (adapted from ALPHA_FEATURE_GUIDE)
- Conversation examples
- Integration status (Google Calendar, Slack, GitHub)

#### Release History
- Version timeline with highlights
- Link to detailed release notes in repo

---

### Section 2: About the Project

#### Project Overview
- The problem Piper Morgan addresses (fragmented PM workflows, AI as colleague not tool)
- Design philosophy: "software that learns you, not the other way around"
- The north star: attunement, memory, judgment

#### Architecture Overview
- High-level system diagram
- Key components (intent service, domain model, integrations, MCP)
- Entity model: Products, Projects, Repositories
- How a conversation flows through the system

#### The Multi-Agent Methodology
- Why multi-agent (and what that means here — not autonomous swarms, but role-based collaboration)
- The virtual org: roles and responsibilities (Architect, Lead Dev, CXO, Comms, HOSR, Chief of Staff, PPM, CIO)
- How agents coordinate (mailboxes, session logs, omnibus synthesis)
- The PM as bottleneck (good and bad)

#### Development Patterns & Principles
- Selected patterns with explanations (curated ~10-15 most important):
  - Assembly Assumption (Pattern-062)
  - Green Tests, Red User (Pattern-045)
  - Verification First (Pattern-006)
  - Cascade Investigation (Pattern-060)
  - The 75% Pattern (Patterns 045-047)
  - Time Lord Doctrine
  - Cathedral Principle (Gall's Law application)
  - Others as appropriate
- Link to full pattern catalog in repo for the curious

#### The Weekly Ship
- What it is and why we publish weekly
- Index of published ships with links
- How ships are produced (workstream reviews → Chief of Staff synthesis → PM editing → publication)

#### Glossary
- Key terms defined (adapted from glossary v1.1)
- Living document — terms added as methodology evolves

---

### Section 3: Project History

#### Timeline
- Key milestones from inception to present
- Sprint history (M0 Conversational Glue, upcoming M1)
- The "periods" framework (if useful for context)

#### Blog Posts & Publications
- Index of published pieces with brief descriptions and links
- Organized chronologically or thematically

#### Talks & Presentations
- IA Conference 2026 (upcoming, April 17)
- Any other public appearances

---

### Sidebar Navigation (GitHub Wiki sidebar)

```
Home

── For Participants ──
Getting Started
Known Issues
How to Contribute
Feature Guide
Release History

── About the Project ──
Project Overview
Architecture Overview
Multi-Agent Methodology
Patterns & Principles
The Weekly Ship
Glossary

── History ──
Timeline
Blog Posts
Talks
```

---

## Content Sourcing Strategy

Most wiki content can be adapted from existing sources:

| Wiki Page | Primary Source |
|-----------|---------------|
| Getting Started | ALPHA_QUICKSTART.md, ALPHA_TESTING_GUIDE.md, Ted/Dominique setup logs |
| Known Issues | ALPHA_KNOWN_ISSUES.md |
| How to Contribute | New (but draws from CLAUDE.md conventions) |
| Feature Guide | ALPHA_FEATURE_GUIDE.md |
| Release History | docs/releases/ |
| Project Overview | PROJECT.md, blog posts |
| Architecture Overview | architecture.md, domain-models.md, PDRs |
| Multi-Agent Methodology | Briefings, methodology-core/, blog posts |
| Patterns & Principles | patterns/ catalog (curated selection) |
| The Weekly Ship | Blog post index, ship workstream drafts |
| Glossary | piper-morgan-glossary-v1.1.md |
| Timeline | Omnibus logs, release notes |
| Blog Posts | Published posts index |

---

## Implementation Approach

1. **PM enables wiki** on the GitHub repo settings
2. **I write initial content** for all pages (~15 pages, adapted from existing sources)
3. **PM reviews and edits** — especially tone, project overview, and methodology sections where PM voice matters most
4. **Ongoing maintenance**: wiki updates can be added to the weekly docs audit checklist

---

## Open Questions for PM

1. **Tone**: The blog posts have a distinctive first-person voice. Should the wiki use that same voice, or a more neutral third-person project voice?
2. **Blog post hosting**: Are published posts on LinkedIn, a personal blog, or both? Need correct links for the index.
3. **Screenshots/images**: Worth including setup screenshots or architecture diagrams? The alpha-onboarding images exist already.
4. **Ship index**: Do you want all ships listed, or just recent/notable ones?
5. **Sidebar**: GitHub wiki has a custom sidebar feature (_Sidebar.md). The proposed structure above would go there.

---

*Proposal ready for PM review.*
