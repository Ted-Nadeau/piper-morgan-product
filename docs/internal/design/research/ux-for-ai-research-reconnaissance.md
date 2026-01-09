# UX for AI: Research Reconnaissance Report

The emerging field of "UX for AI" is characterized by rapid practitioner experimentation, fragmented pattern documentation, and academic research struggling to keep pace with deployed products. This reconnaissance identifies **three distinct knowledge clusters**—practitioner-led pattern work, academic HCI research, and corporate design systems—that rarely cite each other despite addressing identical challenges. The most productive Phase 2 research will bridge these communities.

---

## Key thinkers and practitioners to investigate further

**Tier 1: Essential Voices (high output, hands-on work)**

**Dan Saffer** (CMU HCII) teaches "Designing with AI" at Carnegie Mellon and offers a Maven course with Kerry Bodine titled "How to Select AI Projects That Are Actually Worth Doing." His approach emphasizes *matchmaking* between AI capabilities and design problems rather than cataloguing UI patterns. No public pattern library exists, but his workshops at CanUX and UXLx contain methodological frameworks for AI project selection. His podcast appearance on VAEXPERIENCE's "Design for AI" episode offers the most accessible entry point.

**Greg Nudelman** (UXforAI.com) has documented **35 AI projects** and published the most systematic practitioner-oriented pattern work. His 2025 Wiley book *UX for AI: A Framework for Designing AI-Driven Products* and newsletter represent the closest thing to an applied pattern language. Key concepts include the **Value Matrix** (prediction impact vs. accuracy trade-offs), **Iceberg UX** (visible interface as fraction of AI experience), and seven LLM design patterns including re-stating, talk-back, and guardrails.

**Jakob Nielsen** (UX Tigers Substack) has written extensively on prompt engineering as UX failure, documenting six design patterns for aided prompting: style galleries, prompt rewrite, targeted prompt rewrite, related prompts, prompt builders, and parametrization. His frame of the "articulation barrier" provides useful vocabulary for the prompt-vs-natural-expression problem.

**Victor Dibia** (Microsoft, AutoGen maintainer) published the most rigorous agent UX framework with four principles: capability discovery, observability/provenance, interruptibility, and cost-aware delegation. His work bridges technical architecture and interaction design.

**Tier 2: Company Design Teams**

- **Microsoft Copilot team**: Jon Friedman (CVP M365 Design), Matt Blank. Most extensively documented corporate AI design system with "three altitudes" framework (immersive, assistive, embedded) and HAX Toolkit.
- **Google Gemini**: Jenny Blackburn (VP UX for Gemini), Peter Hershey (contextual screen awareness patents). Less publicly documented than Microsoft.
- **Anthropic Claude**: Meaghan Choi (Claude Code designer). Design philosophy emphasizes "chatbot to work platform" transformation; Geist agency developed visual identity.
- **Perplexity**: Henry Modisett, quoted at Config 2024 on design-engineering convergence.

**Tier 3: Academic Researchers**

- **Saleema Amershi, Q. Vera Liao, Jina Suh** (Microsoft Research) - foundational HAI guidelines
- **Michael Bernstein** (Stanford HCI) - social computing and human-AI collaboration
- **Yunfeng Zhang** (IBM Research) - trust calibration research
- **Kenneth Holstein** (CMU CoALA Lab) - human-AI decision-making
- **Leigh Clark, Benjamin Cowan** (conversational UI research community)

---

## Important sources to investigate further

**Pattern Libraries (ranked by comprehensiveness)**

| Resource | URL | Assessment |
|----------|-----|------------|
| **Shape of AI** | shapeof.ai | Most comprehensive dedicated AI UX pattern library; active Slack community |
| **Google PAIR Guidebook** | pair.withgoogle.com/guidebook | Research-backed, principles-first approach |
| **Microsoft HAX Toolkit** | microsoft.com/haxtoolkit | 18 validated guidelines; production examples |
| **IBM Carbon for AI** | carbondesignsystem.com/guidelines/carbon-for-ai | Enterprise-grade components with AI tokens and labels |
| **PatternFly AI** | patternfly.org/patternfly-ai | Red Hat's conversation design patterns |

**Foundational Academic Papers**

- **Amershi et al. (2019)** "Guidelines for Human-AI Interaction" (CHI) - 18 guidelines that became field standard
- **Clark et al. (2019)** "What Makes a Good Conversation?" (CHI) - documents gap between conversational aspiration and reality
- **Moore & Arar (2019)** "Conversational UX Design: Natural Conversation Framework" - IBM's practitioner-oriented framework
- **Zhang et al. (2020)** "Effect of Confidence and Explanation on Trust Calibration" (FAT*) - key trust calibration research

**2024-2025 Academic Work**

- "The Role of Large Language Models in UI/UX Design" (Ahmed et al., 2025) - systematic review of 38 studies
- "Understanding the LLM-ification of CHI" (2025) - meta-analysis of 153 LLM papers at CHI
- "Human-AI Collaboration is Not Very Collaborative Yet" (Johns Hopkins, Frontiers 2024) - taxonomy critique

**Conference Recordings to Prioritize**

- Config 2024: Perplexity talk (Henry Modisett), UI3 redesign session
- Google I/O 2024: "Create helpful products with responsible AI design"
- Microsoft Build 2024: Sarah Bird's "Responsible AI by Design"
- IxDA 2024: Dan Saffer's "AI By Design" (Pittsburgh chapter)
- Designing with AI 2024 (Rosenfeld Media): Full virtual conference archive

**Deep-Read Practitioner Articles**

- Anthropic's "Improving frontend design through Skills" - addresses distributional convergence
- IDEO's 2024 AI Research Study - quantitative findings on AI-assisted ideation (**56% more ideas** with AI-generated questions, but **28% decrease** with AI-generated example ideas)
- Smashing Magazine's "Psychology of Trust in AI" (September 2025)
- Eugene Yan's "Patterns for Building LLM-based Systems & Products" - defensive UX and guardrails

---

## Thematic clusters emerging in the field

### Cluster 1: Trust, calibration, and appropriate reliance
**Maturity: HIGH** - Strong academic research + emerging design patterns

Core tension: Avoiding both algorithm aversion AND automation complacency. Key finding from Zhang et al.: confidence scores help calibrate trust but don't automatically improve decision outcomes. Local explanations (feature importance) had **no effect** on trust calibration.

Active design explorations include uncertainty language ("I'm not sure" vs. hedging), confidence percentages vs. categorical displays, progressive disclosure of reasoning, and "I don't know" as designed feature. Google's Gemini "thinking" display and Claude's extended thinking represent different approaches to the same problem.

**Gap**: Limited research on how confidence displays affect different user populations or evolve over time.

### Cluster 2: Conversation vs. artifact / generative vs. consumptive interfaces
**Maturity: HIGH** - Major products shipping different solutions

Claude Artifacts (split-window, auto-generated for substantial outputs) vs. OpenAI Canvas (collaborative editing with selective highlighting) represent two competing paradigms. Ink & Switch's research on dynamic documents (Potluck, Embark) offers alternative framings. Google's November 2025 "Generative UI" announcement (Dynamic View creating fully custom interactive interfaces per prompt) may reshape this landscape.

**Gap**: Limited pattern documentation for when to auto-generate artifacts vs. stay in chat; version control UX for AI-generated content.

### Cluster 3: Agency, control, and "who's driving"
**Maturity: MEDIUM** - Emerging academic research, limited product patterns

Key finding from Adam et al. (2024): When AI offers to take over (IS-invoked delegation) vs. user asking, users feel "self-threat" and resist more. Less perceived post-delegation control = more resistance. Victor Dibia's four principles (capability discovery, observability, interruptibility, cost-aware delegation) provide practitioner framework.

**Gap**: Few shipped examples of dynamic mode-switching UI; limited research on building user "delegation skills" over time.

### Cluster 4: Memory, personalization, and continuity
**Maturity: MEDIUM-HIGH** - Active technical research, UX patterns emerging

Technical approaches include vector databases (Pinecone, Chroma), memory blocks (Letta/MemGPT with structured, editable blocks), and active vs. subconscious memory formation. ChatGPT's implementation combines saved memories (user-editable) + background profile building from chat history.

**Gap**: Memory "bloat" problem (how to forget/decay outdated info); user control and transparency for what AI "remembers"; relevance retrieval timing.

### Cluster 5: Prompt articulation and input design
**Maturity: HIGH** - Active practitioner discourse

Nielsen's "articulation barrier" frame is useful: people struggle to express intent in writing, creating "low-articulation users." Current solutions span magic prompts (AI writes prompts to feed itself), hybrid interfaces (text + GUI elements), voice mode (conversation alleviates articulation barrier), and structured templates.

**Gap**: Longitudinal studies on whether users learn good prompting or just rely on scaffolding; when hiding complexity vs. building user capability is appropriate.

### Cluster 6: Agent and autonomous system UX
**Maturity: HIGH but NASCENT** - Rapidly emerging, significant industry attention

OpenAI's Operator (January 2025), Microsoft's Copilot agents, and AutoGen represent deployed agent systems. Emerging patterns include supervisor/worker models, risk classifiers (automatic approval for low-risk, explicit for high-risk), mission-control interfaces, and temporal navigation (replay AI decision chains).

**Gap**: "Agent Experience (AX)" as emerging discipline lacks established methodology; few longitudinal studies of trust development with agents.

### Cluster 7: Non-determinism as design constraint
**Maturity: MEDIUM** - Strong technical understanding, limited UX pattern development

Root causes are well-documented (sampling parameters, floating-point rounding, batch size variations, MoE routing, hardware variations). Thinking Machines Lab (September 2025) achieved perfect reproducibility with "batch-invariant" kernels at ~60% speed cost.

**Gap**: Is determinism even desirable? Limited UX research on setting user expectations about variability; when to expose vs. hide non-determinism.

### Cluster 8: Multi-modal integration
**Maturity: LOW-MEDIUM** - Technical challenges documented, UX patterns still emerging

Core challenges include seamless transitions between modalities, context retention across modality switches, discoverability of voice/gesture commands, and error recovery. Shipped examples (Google Nest Hub, BMW iDrive) provide limited pattern guidance for LLM-native multi-modal.

**Gap**: Most underexplored area relative to market importance; limited research on conflicting inputs from multiple modalities.

---

## Apparent gaps and underexplored areas

**Methodological gaps**

- **Longitudinal studies**: Nearly all research uses single-session evaluations; practitioners need understanding of trust evolution, skill development, and preference formation over weeks/months
- **Ecological validity**: Lab studies dominate; gap in research on real-world deployment contexts with actual stakes
- **Cross-platform consistency**: Almost no research on designing consistent AI experiences across devices/contexts
- **Accessibility**: Limited work on making LLM interfaces accessible to users with disabilities

**Conceptual gaps**

- **Human-AI handoff patterns**: Sparse documentation for escalation from AI to human agents
- **Collaborative editing patterns**: Limited patterns for true AI + human co-authoring workflows
- **Failure recovery**: What happens when AI fails mid-task beyond simple error messages?
- **AI personality design**: Beyond voice/tone, how to design consistent AI "character" over time
- **Privacy/data transparency**: How to show what user data AI accesses and retains

**Community gaps**

- **Practitioner-academic disconnect**: Academic HCI and practitioner design work rarely cite each other
- **Design system integration**: Few resources for integrating conversational patterns into existing design systems
- **Cost-benefit frameworks**: Researchers rarely address when NOT to use LLM interfaces
- **Cultural considerations**: Cross-cultural study (CHI 2024) shows US vs. Chinese users have very different interaction expectations; limited pattern adaptation

**Emerging areas with limited coverage**

- Agentic workflow visualization (how to show multi-step autonomous actions transparently)
- Cross-context memory and identity (AI that "knows you" across different applications)
- AI-to-AI interfaces (when agents communicate with each other, what do humans see?)
- Temporal navigation in AI systems (replaying, branching, versioning AI conversations)

---

## Recommended research questions for Phase 2

**Questions about user mental models and behavior**

1. How do users' mental models of LLM capabilities evolve with extended use, and what design interventions accelerate accurate calibration?
2. When do users prefer conversation vs. direct manipulation for AI-generated content, and what contextual factors predict preference?
3. How do different confidence display mechanisms (numeric, categorical, visual) affect user reliance across task types and user expertise levels?

**Questions about design patterns and frameworks**

4. What taxonomies effectively organize the space of AI interface patterns, and which categorical schemes have predictive power for design decisions?
5. How should artifact-generating AI interfaces handle versioning, branching, and undo differently than traditional productivity tools?
6. What patterns enable users to develop "AI delegation skills" vs. creating learned helplessness?

**Questions about organizational and systemic factors**

7. How do cross-functional teams (designers, engineers, ML researchers) currently collaborate on AI UX, and what processes produce better outcomes?
8. What evaluation methods do practitioners actually use for AI interfaces, and how do these correlate with user satisfaction and task success?
9. How are companies making build-vs-buy decisions for AI interface components, and what drives customization?

**Questions about emerging frontiers**

10. What UX patterns are emerging for agent systems that take autonomous actions, and how do these differ from conversational AI patterns?
11. How do multi-modal AI interfaces handle transitions between modalities, and what failure modes emerge?
12. What privacy and transparency patterns give users meaningful control without creating friction?

---

## Suggested structure for Phase 2 research

### Phase 2A: Deep-dive interviews (4-6 weeks)

**Priority 1 interviews (essential)**
- Greg Nudelman - Most comprehensive practitioner pattern work
- Dan Saffer - CMU methodology and AI project selection framework
- Shape of AI creator (Emily Campbell) - Pattern library development process
- Victor Dibia - Agent UX framework

**Priority 2 interviews (high value)**
- Microsoft Copilot design team member (Jon Friedman, Matt Blank, or Laura Bergstrom)
- Google Gemini UX (Jenny Blackburn or Peter Hershey)
- Anthropic designer (Meaghan Choi)
- Academic researcher bridging practitioner work (Q. Vera Liao, Kenneth Holstein)

**Interview protocol focus**
- Current pattern gaps they observe
- Decision-making frameworks for AI interaction mode selection
- Failed experiments and why they failed
- Predictions for next 18 months

### Phase 2B: Pattern analysis and synthesis (3-4 weeks)

**Comparative analysis**
- Map patterns across Shape of AI, PAIR, HAX Toolkit, and Carbon for AI
- Identify convergent vs. divergent pattern recommendations
- Document terminology variations for same concepts
- Build unified taxonomy proposal

**Gap analysis**
- Cross-reference pattern libraries against the 9 thematic challenges from user query
- Identify which challenges have robust patterns vs. sparse coverage
- Map academic research to pattern gaps

### Phase 2C: Case study deep-dives (2-3 weeks)

**Product-level analysis**
- Claude Artifacts: Evolution from launch to current state, design decisions, user reception
- ChatGPT memory: Implementation timeline, user feedback, privacy considerations
- Microsoft Copilot: Three-altitude framework in practice, enterprise deployment lessons
- Perplexity: Search-native AI UX, citation patterns, trust design

**Failure analysis**
- Document AI UX failures that received public criticism
- Analyze root causes through UX lens
- Extract defensive design patterns

### Phase 2D: Synthesis and framework development (2-3 weeks)

**Deliverables**
- Unified pattern taxonomy covering all 9 thematic areas
- Decision framework: When to use which AI interaction mode
- Gap map: Underexplored areas prioritized by market importance
- Research agenda: Questions requiring further investigation
- Resource guide: Curated sources organized by thematic cluster

**Recommended output formats**
- Annotated bibliography (academic + practitioner sources)
- Pattern cards or pattern language document
- Interview synthesis report
- Decision flowchart for AI UX pattern selection

---

## Key sources quick reference

| Category | Top 3 Sources |
|----------|---------------|
| Pattern Libraries | Shape of AI, Google PAIR Guidebook, Microsoft HAX Toolkit |
| Practitioner Writing | Greg Nudelman (UXforAI.com), Jakob Nielsen (Substack), Anthropic Design Blog |
| Academic Foundation | Amershi et al. 2019 (HAI Guidelines), Clark et al. 2019 (Conversation Challenges), Zhang et al. 2020 (Trust Calibration) |
| Conference Archives | Config 2024, Designing with AI 2024, CHI 2024/2025 |
| Corporate Documentation | Microsoft Copilot UX Guidance, IBM Carbon for AI, Apple HIG AI sections |

This reconnaissance reveals a field in rapid flux where practitioners are building faster than researchers can study and pattern libraries are emerging without shared vocabulary. The highest-value Phase 2 work will synthesize across these fragmented communities to create actionable frameworks for the specific tensions identified: conversation vs. artifact, who's driving, memory/continuity, and trust calibration.
