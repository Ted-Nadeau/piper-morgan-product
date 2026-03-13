# IAC26 Conference Proposal - DRAFT
**Deadline**: October 5, 2025 (11:59 PM PST)

---

## Session Title
**Ethics as Information Architecture: Why AI Safety Requires IA Thinking**

## Session Subtitle / Plain Language Title
Building AI systems where harmful behavior is architecturally impossible, not just against policy

## Detailed Description (for review/curation teams)

Information architects understand something crucial that many AI developers miss: structure determines possibility. The way you organize information doesn't just affect usability—it defines what actions are even possible within a system.

This talk demonstrates how ethical AI development is fundamentally an information architecture problem. When you treat ethics as interface-level features (warning messages, terms of service, content moderation after the fact), those protections are fragile and easily circumvented. When you architect ethical principles directly into the information flow—making certain harmful patterns structurally impossible—you create systems that can't be tricked into causing harm.

I'll share specific examples from building Piper Morgan, a product management AI assistant designed with ethics-first architecture:

**The Architecture Approach**:
- Every user request passes through boundary enforcement BEFORE any AI processing
- Critical decisions require human approval through non-bypassable gateways (like Asimov's laws implemented as code)
- The system learns from metadata relationships, not content, preserving privacy while enabling intelligence
- Professional boundaries are enforced at the structural level, not prompt level

**The Technical Proof**:
- Demonstrated 80.3% clustering accuracy using only relationship metadata (zero content analysis)
- Proved that privacy-preserving AI can achieve practical intelligence for knowledge work
- Created protection hierarchies that resolve principle conflicts systematically
- Built systems where "jailbreaking" ethical constraints is architecturally impossible

**The IA Insight**:
This is applied information architecture. The four ethical principles (Human Empowerment, System Integrity, Project Excellence, Professional Boundaries) become structural constraints on how information flows through the system. You're not moderating bad outcomes—you're architecting information spaces where those outcomes can't occur.

The talk addresses the conference theme directly: navigating the complexity of AI development requires the clarity that comes from proper information architecture. IA practitioners aren't being made obsolete by AI—their perspective is desperately needed to prevent AI systems from becoming harmful through architectural negligence.

Attendees will learn:
- How to architect ethical constraints as structural patterns, not policies
- Why metadata-only learning preserves privacy while enabling intelligence
- How protection hierarchies resolve competing principles systematically
- Practical implementation patterns for ethical information architecture
- Why IA thinking is essential for responsible AI development

This is IA applied at the architectural level—using information structure to create clarity, trust, and human-centered AI systems that serve people rather than exploit them.

## Short Description (for conference website - 1000 char max)

AI systems that treat ethics as an afterthought—adding content warnings or terms of service after building the core capabilities—create fragile protections easily circumvented by users or undermined by business pressures. This talk demonstrates why ethical AI development is fundamentally an information architecture problem.

Drawing from building Piper Morgan (a product management AI assistant with ethics-first architecture), I'll show how ethical principles become structural constraints on information flow. When boundary enforcement happens before AI processing, when human decision-making authority is architecturally preserved, when systems learn from relationship metadata rather than content—you create AI that can't be tricked into causing harm because the architecture itself prevents it.

This is applied IA at the systems level: using information structure to create clarity, trust, and human-centered AI. Information architects aren't being made obsolete by AI—their expertise in organizing information spaces is essential for building AI systems that serve human flourishing rather than optimizing for engagement metrics that harm users.

Attendees will learn practical patterns for architecting ethics into AI systems and why IA thinking is desperately needed in responsible AI development.

## Intended Experience Level
**Intermediate** - Assumes familiarity with information architecture principles and basic understanding of AI/ML systems. Does not require coding expertise but includes architectural implementation examples.

## What Will Attendees Gain? (3-5 specific takeaways)

1. **Structural Ethics Framework**: Understand how to implement ethical principles as architectural constraints rather than policy guidelines, making harmful behavior technically impossible rather than just prohibited

2. **Privacy-Preserving Intelligence Pattern**: Learn how metadata-only learning enables sophisticated AI assistance while maintaining complete content privacy (with empirical results: 80.3% clustering accuracy without content access)

3. **Protection Hierarchy Design**: Apply systematic approaches to resolving conflicts between competing principles (human agency vs. system capability, privacy vs. learning, speed vs. safety)

4. **Boundary Enforcement Architecture**: Implement pre-processing interception patterns that prevent harmful interactions before any AI processing occurs

5. **IA's Essential Role in AI**: Recognize why information architecture expertise is critical for responsible AI development and how to position IA practice as essential to AI safety

## Your Experience and Knowledge (800 char max)

I'm building Piper Morgan, a product management AI assistant with ethics-first architecture, where I've implemented the patterns discussed in this talk. As Director of Product at Kind and former 18F product manager, I've spent years navigating the tension between business metrics and human welfare in digital product development.

My background combines product management, UX design, and information architecture—the intersection where ethical principles meet practical implementation. I've written extensively about AI collaboration methodology and built systems that prove privacy-preserving intelligence is empirically achievable, not just theoretically interesting.

I'm also author of "Product Management for UX People" and have spoken at IA conferences for over a decade about human-centered design in increasingly complex information systems.

## Have You Presented This Material Elsewhere?

This specific talk is new, developed for IAC26. However, the underlying work has been documented in my "Building Piper Morgan" blog series (published since July 2024), including:

- "Why Ethical AI Can't Be an Afterthought" (September 2024) - establishing the philosophical foundation
- "Privacy-First Intelligence: How We Proved Metadata Learning Can Work" (September 2024) - demonstrating empirical results

The conference talk synthesizes this work specifically for the IA community, emphasizing how IA thinking solves problems that pure engineering or ethics-only approaches miss.

## Which Topic Area Does Your Talk Best Fit?

**Engaging with issues of ethics in IA and design**

(Secondary relevance: "Exploring forward-thinking concepts" - the metadata-only learning approach represents novel application of IA principles to AI safety)

## How Does Your Proposal Map to the Theme? (1000 char max)

"Navigating Complexity: Clarity and Understanding with Information Architecture"

AI systems represent unprecedented complexity—billions of parameters trained on incomprehensible amounts of data, making decisions that affect millions of users. The traditional response is either to throw up our hands ("it's a black box") or bolt on safeguards after the fact.

Information architecture offers a third path: create clarity through structure.

This talk demonstrates how IA principles—organizing information flow, creating hierarchies, defining relationships, architecting constraints—cut through AI complexity to create systems people can understand and trust. When ethical principles become architectural patterns, users gain clarity about what the system will and won't do. When protection hierarchies resolve principle conflicts systematically, developers gain understanding about how to navigate ethical trade-offs.

The complexity of AI development doesn't require abandoning human-centered design—it requires information architects who can structure these systems so that harmful patterns become impossible, privacy is preserved through architectural choice, and human agency remains supreme through systematic enforcement.

IA thinking doesn't just make AI more usable. It makes AI fundamentally safer.

## Social Media-Ready Description (200 char max, include #IAC26)

Information architects aren't being made obsolete by AI—we're desperately needed to prevent AI from harming people through architectural negligence. #IAC26 @xian

## Anything Else We Should Know?

This talk draws on active development work (Piper Morgan is operational with ethics-first architecture) and empirical results (metadata learning validated at 80.3% clustering accuracy). I'm prepared to share code examples and architectural diagrams as supplementary materials if the talk is accepted.

The work explicitly references inspiration from Asimov's laws of robotics—not as science fiction, but as an architectural pattern for building hierarchical protection systems in AI.

I'm also happy to adjust talk length if lightning talk format would be preferred, though the full format allows for deeper exploration of implementation patterns that IA practitioners can apply to their own AI projects.

---

## Speaker Information

**Name**: Christian Crumlish

**Tagline**: Director of Product at Kind, 18F alum, author of "Product Management for UX People," builder of Piper Morgan (AI product assistant)

**Email**: [YOUR EMAIL]

**Biography** (500-800 words):

Christian Crumlish is Director of Product at Kind and former product manager at 18F (the federal government's digital services agency). He brings over two decades of experience in UX design, product management, and information architecture to the challenge of building ethical AI systems.

At Kind, Christian leads product development for mental health and peer support platforms, where the intersection of technology and human welfare isn't theoretical—it's the core challenge of every product decision. This experience shapes his approach to AI development: technology should amplify human capability without replacing human judgment, strengthen systems without creating dependencies, and maintain professional boundaries even when business metrics might reward boundary violations.

Previously at 18F, Christian worked on federal digital services including healthcare.gov improvements and agency modernization efforts, learning how to navigate complex stakeholder interests while keeping user needs central. This public service perspective informs his conviction that AI systems should be built for human flourishing, not just engagement metrics.

Christian is author of "Product Management for UX People" and has been a regular speaker at IA Summit/IAC conferences for over a decade. His writing combines technical depth with accessible explanation—a skill honed through years of translating between engineers, designers, and business stakeholders.

Currently, Christian is building Piper Morgan, a product management AI assistant designed with ethics-first architecture. This project demonstrates that privacy-preserving AI isn't just theoretically possible but empirically validated—achieving 80.3% clustering accuracy using only metadata relationships, with zero content analysis required.

His "Building Piper Morgan" blog series documents this work in public, sharing both successes and methodology. The approach emphasizes systematic engineering over good intentions, architectural enforcement over policy guidelines, and information architecture principles as essential tools for AI safety.

Christian's work sits at the intersection of product management, information architecture, and ethical AI development—proving that human-centered design principles scale to AI systems when properly architected into the information structure itself.
