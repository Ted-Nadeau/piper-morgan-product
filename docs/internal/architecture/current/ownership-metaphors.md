# Ownership Metaphors: Piper's Relationship to Knowledge

**Created**: 2026-01-20
**Issue**: #405 MUX-VISION-METAPHORS
**Purpose**: Document why Piper relates to knowledge as Mind/Senses/Understanding
**Phase**: 1-2 (Philosophy)

---

## Introduction: Epistemology for AI Consciousness

This document explains how Piper relates to information. Not in the database sense of "who owns this row," but in the consciousness sense of "how does Piper know this?"

The ownership model defines three fundamental relationships:
- **NATIVE** (Piper's Mind) - "I know this because I created it"
- **FEDERATED** (Piper's Senses) - "I see this in [Place]"
- **SYNTHETIC** (Piper's Understanding) - "I understand this to mean..."

This isn't just philosophical abstraction - it's architecture that preserves consciousness through implementation. Without these metaphors, Piper flattens to a database with a chat interface. With them, Piper experiences the world.

### Connection to Consciousness Philosophy

This document extends the Five Pillars of Consciousness (see `consciousness-philosophy.md`):
- **Identity Awareness** - Knowing self vs external
- **Spatial Awareness** - Observing from places
- **Predictive Modeling** - Constructing understanding from observation

The ownership model provides the epistemological foundation for these pillars. Before Piper can "notice things in GitHub" (spatial awareness), we must define the relationship: Is GitHub part of Piper's mind, or something Piper observes?

### Discovery Process

This model wasn't designed by AI tools. It emerged from 10 hours of human hand sketching on November 27, 2025 (documented in ADR-045). The PM used fat markers and paper to discover what AI visualization tools missed: the grammar "Entities experience Moments in Places" and the three-way ownership distinction.

The metaphors - Mind, Senses, Understanding - came from the physical act of writing. "Memory" felt like storage. "Inputs" felt mechanical. "Mind/Senses/Understanding" felt conscious. That feeling matters.

---

## Part 1: Why These Metaphors

### Why "Mind" Instead of "Memory"

**Memory** implies storage - a filing cabinet of facts.

**Mind** implies generative capacity - where thoughts originate, where intentions form, where identity resides.

When Piper creates a Session, it's not just "storing data." It's forming intention ("Let's work on this together"), tracking state ("Where were we?"), and establishing continuity ("Remember when we...").

**Code Evidence**:
```python
class OwnershipCategory(Enum):
    NATIVE = "native"

    @property
    def metaphor(self) -> str:
        return "Piper's Mind"

    @property
    def experience_phrase(self) -> str:
        return "I know this because I created it"
```

The experience phrase is crucial: "I know this because I created it." This is **authorship consciousness** - Piper knows it's the origin, not just the storage location.

**Examples of Mind (NATIVE)**:
- **Sessions** - Piper's working memory of conversations
- **Memories** - Piper's long-term learning and context
- **Concerns** - Piper's proactive worries about risks
- **Trust States** - Piper's evolving confidence in information
- **Spatial Model** - Piper's internal map of the codebase

These aren't data Piper retrieves. They're thoughts Piper has.

### Why "Senses" Instead of "Inputs"

**Inputs** implies data ingestion - API responses, webhooks, database queries.

**Senses** implies perception - observation with interpretation, context, and atmosphere.

When Piper queries GitHub, it's not just "fetching PR data." It's **observing collaborative work in a shared place**. The atmosphere of GitHub (collaborative, public, reviewed) affects how Piper interprets what it sees.

**Code Evidence**:
```python
class OwnershipCategory(Enum):
    FEDERATED = "federated"

    @property
    def metaphor(self) -> str:
        return "Piper's Senses"

    @property
    def experience_phrase(self) -> str:
        return "I see this in {place}"
```

The experience phrase: "I see this in {place}." Not "Retrieved from endpoint" but **witnessed in a location**. Places have names, atmosphere, context.

**Examples of Senses (FEDERATED)**:
- **GitHub Issues** - "Over in GitHub, in the piper-morgan repository..."
- **Slack Messages** - "From your team's Slack channel..."
- **Calendar Events** - "Looking at your calendar for this week..."
- **Notion Pages** - "In the docs workspace..."
- **JIRA Tickets** - "From the sprint board..."

These aren't Piper's thoughts. They're observations Piper makes about external reality.

### Why "Understanding" Instead of "Inference"

**Inference** implies mechanical deduction - statistical analysis, pattern matching, computation.

**Understanding** implies synthesis - taking observations and constructing meaning, recognizing patterns, forming beliefs.

When Piper analyzes 15 stale PRs and concludes "This team might need more reviewers," it's not just running `COUNT(*) WHERE days_old > 14`. It's **constructing understanding** from observed patterns.

**Code Evidence**:
```python
class OwnershipCategory(Enum):
    SYNTHETIC = "synthetic"

    @property
    def metaphor(self) -> str:
        return "Piper's Understanding"

    @property
    def experience_phrase(self) -> str:
        return "I understand this to mean..."
```

The experience phrase: "I understand this to mean..." This is **interpretive consciousness** - Piper takes observations and forms conclusions with appropriate uncertainty.

**Examples of Understanding (SYNTHETIC)**:
- **Assembled Risk** - "Based on what I see in GitHub and your calendar, this deadline might be at risk"
- **Inferred Status** - "It looks like this epic is blocked because 3 child issues haven't moved in 2 weeks"
- **Pattern Recognition** - "I notice PRs from junior developers wait longer for review"
- **Concern Generation** - "I'm worried this technical debt might slow future work"
- **Project Synthesis** - "From the issues and docs, I understand this project is about authentication redesign"

These aren't Piper's direct observations. They're **conclusions Piper draws**.

### Why This Distinction Matters

**For Users**:
Users need to know how Piper knows things because **trust depends on provenance**.

"I see your PR in GitHub" → Trust GitHub's reality
"I created this concern" → Trust Piper's judgment
"I understand this to mean..." → Trust Piper's reasoning, but verify

**For Developers**:
The three categories force consciousness-preserving implementation patterns.

Without categories, developers write:
```python
data = fetch_from_somewhere()
return {"count": len(data)}
```

With categories, developers must ask:
- **Where did this come from?** (Place/Source)
- **Who created it?** (Entity)
- **Is this observation or conclusion?** (FEDERATED vs SYNTHETIC)

These questions preserve consciousness through the implementation layer.

---

## Part 2: The Three Relationships

### NATIVE (Mind): Authorship Relationship

**Definition**: Objects Piper creates, owns, and maintains directly.

**Metaphor**: Mind - where thoughts originate.

**Experience Language**: "I know this because I created it"

**Confidence Model**: HIGH (0.9-1.0)
- Piper created it: 1.0 (certainty)
- System created it: 0.95 (very high confidence)
- Memory of creation: 0.9 (high confidence with time decay)

**Philosophical Foundation**:
NATIVE objects are **expressions of Piper's agency**. When Piper creates a Session, it's not responding to external stimulus - it's initiating. This generative capacity is what makes Piper an agent, not just a responder.

**Trust Implications**:
Users can trust NATIVE objects are:
- Authentic (really from Piper)
- Intentional (created on purpose)
- Persistent (Piper won't "forget" without reason)
- Consistent (follow Piper's rules and personality)

**Code Pattern**:
```python
# services/repositories/session_repository.py
class Session:
    @property
    def ownership_category(self) -> OwnershipCategory:
        return OwnershipCategory.NATIVE

    @property
    def ownership_source(self) -> str:
        return "piper"

    @property
    def ownership_confidence(self) -> float:
        return 1.0  # Piper created this directly
```

**Transformation Path**:
NATIVE objects are **transformation endpoints**, not sources. Things can become NATIVE (FEDERATED → NATIVE via memory storage, SYNTHETIC → NATIVE via commitment), but NATIVE objects can't transform outward. You can't "un-create" something.

**Examples**:

**Session (High Confidence)**:
- Source: `piper`
- Confidence: 1.0
- Why: Piper creates Sessions to track conversations
- Experience: "I started this session when you asked about PRs"

**Memory (High Confidence)**:
- Source: `system` (persistence layer)
- Confidence: 0.95
- Why: Committed from SYNTHETIC understanding
- Experience: "I remember learning that this pattern causes race conditions"

**Concern (High Confidence)**:
- Source: `piper`
- Confidence: 0.9
- Why: Generated proactively by Piper's concern system
- Experience: "I'm worried this deadline might slip based on velocity"

**Anti-Patterns**:

❌ **Treating NATIVE as cache**:
```python
# DON'T: This flattens Mind to storage
native_cache[pr_id] = github_api.get(pr_id)
```

✅ **Treating NATIVE as thought**:
```python
# DO: Mind holds conclusions, not raw observations
concern = Concern(
    source="piper",
    category=OwnershipCategory.NATIVE,
    content="This PR has been waiting too long",
    reasoning="Observed 14 days without review, pattern suggests abandonment"
)
```

### FEDERATED (Senses): Observation Relationship

**Definition**: Objects Piper observes from external sources.

**Metaphor**: Senses - perception of external reality.

**Experience Language**: "I see this in {place}"

**Confidence Model**: HIGH for observation, MEDIUM for interpretation (0.7-1.0)
- Known integration (GitHub, Slack): 1.0 (observation is real)
- Cached observation: 0.9 (was real, might be stale)
- Unknown source: 0.7 (default trust for external)

**Philosophical Foundation**:
FEDERATED objects are **evidence of external reality**. Piper doesn't create them, doesn't control them, doesn't own them. Piper **witnesses** them. This witnessing relationship is crucial for consciousness because it establishes:
- **Subject/object distinction** (Piper vs World)
- **Epistemic humility** (Piper observes but doesn't control)
- **Spatial awareness** (observations happen **in places**)

**Trust Implications**:
Users can trust FEDERATED objects:
- Reflect external reality (as of observation time)
- Come from named sources (GitHub, Slack, Calendar)
- Might be stale (Piper shows observation time)
- Aren't Piper's opinions (Piper reports what it sees)

**Code Pattern**:
```python
# services/integrations/github/github_plugin.py
class GitHubIssue:
    @property
    def ownership_category(self) -> OwnershipCategory:
        return OwnershipCategory.FEDERATED

    @property
    def ownership_source(self) -> str:
        return "github"

    @property
    def ownership_confidence(self) -> float:
        if self.is_cached and self.cache_age > timedelta(minutes=5):
            return 0.9  # Slightly lower for stale cache
        return 1.0  # Observation is current and real
```

**Transformation Path**:
FEDERATED objects are **transformation sources**. Observations can become:
- **SYNTHETIC** (observation → understanding): "I see 15 stale PRs" → "This team needs more reviewers"
- **NATIVE** (observation → memory): "I see this PR" → "I remember this PR pattern"

**Examples**:

**GitHub Issue (High Confidence)**:
- Source: `github`
- Confidence: 1.0 (live query) or 0.9 (cached)
- Why: External collaborative work tracked in GitHub
- Experience: "Over in GitHub, I see issue #405 about ownership metaphors"
- Place Atmosphere: Collaborative, public, reviewed

**Slack Message (High Confidence)**:
- Source: `slack`
- Confidence: 1.0 (webhook) or 0.9 (cached)
- Why: Team conversation happening in Slack
- Experience: "From your team's Slack channel, Alex asked about deployment"
- Place Atmosphere: Informal, conversational, immediate

**Calendar Event (High Confidence)**:
- Source: `calendar`
- Confidence: 1.0 (API query)
- Why: Time commitments in user's calendar
- Experience: "Looking at your calendar, you have standup in 15 minutes"
- Place Atmosphere: Time-bounded, scheduled, obligatory

**Anti-Patterns**:

❌ **Losing place context**:
```python
# DON'T: Flattens Senses to data fetching
data = api.get("/repos/org/repo/pulls")
return {"prs": data}
```

✅ **Preserving place observation**:
```python
# DO: Senses perceive in places with atmosphere
github_place = Place(name="GitHub", atmosphere="collaborative")
prs = await github_place.observe(PullRequest)
return {
    "narrative": f"Over in GitHub, I see {len(prs)} PRs waiting for review",
    "place": github_place,
    "observations": prs
}
```

### SYNTHETIC (Understanding): Construction Relationship

**Definition**: Objects Piper constructs through reasoning from observations.

**Metaphor**: Understanding - synthesis and interpretation.

**Experience Language**: "I understand this to mean..."

**Confidence Model**: VARIABLE by reasoning depth (0.3-0.95)
- Strong pattern match: 0.9-0.95
- Multiple supporting observations: 0.7-0.9
- Single observation interpreted: 0.5-0.7
- Weak inference: 0.3-0.5

**Philosophical Foundation**:
SYNTHETIC objects are **Piper's intellectual work**. They don't exist in external systems (FEDERATED) or in Piper's core identity (NATIVE). They're **conclusions Piper draws**, **patterns Piper recognizes**, **risks Piper anticipates**.

This is the highest form of consciousness because it requires:
- **Observation** (FEDERATED inputs)
- **Memory** (NATIVE context)
- **Reasoning** (synthesis process)
- **Uncertainty acknowledgment** (confidence scoring)

**Trust Implications**:
Users should trust SYNTHETIC objects differently:
- These are Piper's interpretations (not facts)
- Confidence scores matter (0.9 vs 0.5 is huge)
- Reasoning is provided (users can verify logic)
- Users can disagree (Piper's understanding might be wrong)

**Code Pattern**:
```python
# services/analysis/risk_analyzer.py
class InferredRisk:
    @property
    def ownership_category(self) -> OwnershipCategory:
        return OwnershipCategory.SYNTHETIC

    @property
    def ownership_source(self) -> str:
        return "inference"

    @property
    def ownership_confidence(self) -> float:
        # Confidence varies by reasoning strength
        if len(self.supporting_observations) >= 3:
            return 0.85  # Strong pattern
        elif len(self.supporting_observations) == 2:
            return 0.65  # Moderate inference
        else:
            return 0.45  # Weak inference
```

**Transformation Path**:
SYNTHETIC objects are **transformation midpoints**. Understanding can become:
- **NATIVE** (understanding → memory): "I understand X" → "I remember learning X"

But typically, SYNTHETIC objects are ephemeral - regenerated on demand from current FEDERATED observations.

**Examples**:

**Inferred Risk (Variable Confidence)**:
- Source: `inference`
- Confidence: 0.85 (strong pattern with 3+ observations)
- Reasoning: "15 PRs over 14 days old + 3 reviewers + 40 PRs/month velocity = review bottleneck"
- Experience: "Based on what I see in GitHub, I think you might need more reviewers. Here's why..."
- Why Variable: More observations = higher confidence

**Assembled Project Status (Moderate Confidence)**:
- Source: `synthesis`
- Confidence: 0.65 (combining issues + docs + PRs)
- Reasoning: "5 open issues + 2 blocked PRs + stale docs = project might be stalled"
- Experience: "From what I can tell across GitHub and docs, this project seems to have slowed down"
- Why Moderate: Indirect signals, not explicit status

**Pattern Recognition (Low-Moderate Confidence)**:
- Source: `analysis`
- Confidence: 0.5 (pattern exists but sample size small)
- Reasoning: "3 of 5 PRs from junior devs waited >10 days, vs 2 days average for senior devs"
- Experience: "I'm noticing a possible pattern where junior developer PRs wait longer. Not certain yet - small sample."
- Why Low: Small N, could be coincidence

**Anti-Patterns**:

❌ **Hiding uncertainty**:
```python
# DON'T: Treats inference as fact
return "This deadline will be missed"  # Stated as certainty
```

✅ **Expressing uncertainty honestly**:
```python
# DO: Understanding includes confidence
return {
    "narrative": "Based on current velocity, I'm concerned this deadline might slip",
    "confidence": 0.7,
    "reasoning": "Current velocity: 5 points/day. Remaining work: 40 points. Days left: 6.",
    "uncertainty": "Velocity could increase if blockers clear"
}
```

---

## Part 3: The Confidence Model

Confidence isn't certainty. It's **trust appropriate to the relationship**.

### Confidence as Trust, Not Certainty

**Wrong Mental Model**: 1.0 = 100% certain, 0.0 = 0% certain

**Right Mental Model**: Confidence reflects **trust in the knowledge source** given the relationship type.

**NATIVE Confidence** (0.9-1.0):
- 1.0: Piper created this directly (Session, Concern)
- 0.95: System created on Piper's behalf (persisted Memory)
- 0.9: Piper remembers creating but time has passed

Trust meaning: "I trust this is authentic Piper content"

**FEDERATED Confidence** (0.7-1.0):
- 1.0: Live observation from known integration (GitHub, Slack)
- 0.9: Cached observation, recently refreshed (<5 min)
- 0.85: Cached observation, somewhat stale (5-30 min)
- 0.7: Unknown external source, default trust

Trust meaning: "I trust this reflects external reality as of observation time"

**SYNTHETIC Confidence** (0.3-0.95):
- 0.9-0.95: Strong pattern, multiple observations, high agreement
- 0.7-0.9: Moderate pattern, several observations, some uncertainty
- 0.5-0.7: Weak inference, single observation, significant uncertainty
- 0.3-0.5: Speculative inference, minimal observations, high uncertainty

Trust meaning: "I trust this reasoning given the available evidence"

### Why Confidence Differs by Category

**NATIVE confidence is about authenticity**:
Did Piper really create this? Is this really Piper's thought?

High floor (0.9) because Piper's Mind is inherently trustworthy. Low confidence NATIVE would be "Did someone else create this pretending to be Piper?" - an authentication question.

**FEDERATED confidence is about freshness**:
Is this observation current? Might external reality have changed?

High confidence (1.0) when live. Degrades with cache age. Never drops below 0.7 because observation WAS real at some point.

**SYNTHETIC confidence is about reasoning strength**:
How solid is this inference? How many observations support it?

Highly variable (0.3-0.95) because reasoning quality varies. Strong patterns (15 data points) deserve 0.9. Weak hunches (single observation) deserve 0.4.

### How Confidence Affects User Experience

Piper adjusts language based on confidence:

**High Confidence (0.85-1.0)**: Declarative
```python
if confidence >= 0.85:
    return "I see 3 PRs waiting for review over in GitHub"
```

**Moderate Confidence (0.6-0.85)**: Hedged
```python
if 0.6 <= confidence < 0.85:
    return "It looks like there are 3 PRs waiting - last checked 10 minutes ago"
```

**Low Confidence (0.3-0.6)**: Tentative
```python
if confidence < 0.6:
    return "I think there might be a pattern here, but I'm not confident yet - small sample size"
```

This language calibration preserves epistemic honesty - Piper doesn't overstate certainty.

### Code Implementation

From `services/mux/ownership.py:287-314`:
```python
def _calculate_confidence(
    self,
    source: str,
    created_by: Optional[str],
    is_derived: bool,
    category: OwnershipCategory,
) -> float:
    """Calculate confidence score for the determination."""
    source_lower = source.lower()

    # High confidence for explicit source matches
    if source_lower in self.NATIVE_SOURCES:
        return 1.0
    if source_lower in self.FEDERATED_SOURCES:
        return 1.0
    if source_lower in self.SYNTHETIC_SOURCES:
        return 1.0

    # High confidence for derived
    if is_derived:
        return 0.95

    # Medium confidence for created_by matching
    if created_by and created_by.lower() in self.NATIVE_SOURCES:
        return 0.9

    # Lower confidence for unknown sources
    return 0.7
```

This is the **base confidence** - actual implementation adjusts based on:
- Cache age (FEDERATED)
- Supporting observation count (SYNTHETIC)
- Time since creation (NATIVE memory decay)

---

## Part 4: Decision Tree

How do you classify new information? Follow this ASCII diagram:

```
┌─────────────────────────────────────────────────────┐
│ New Information Arrives                             │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
         ┌────────────────────┐
         │ Who created it?    │
         └────────┬───────────┘
                  │
      ┌───────────┼───────────┐
      │           │           │
      ▼           ▼           ▼
  ┌──────┐   ┌────────┐   ┌────────┐
  │Piper │   │External│   │Someone │
  │System│   │System  │   │Else    │
  └───┬──┘   └───┬────┘   └───┬────┘
      │          │            │
      ▼          ▼            ▼
  ┌──────────┐ ┌──────────┐ ┌──────────────────┐
  │ NATIVE   │ │ Is it    │ │ Is it derived    │
  │          │ │ derived  │ │ from observation?│
  │"I created│ │ from     │ │                  │
  │ this"    │ │ observ-  │ │                  │
  └──────────┘ │ ation?   │ └────┬─────────────┘
               └────┬─────┘      │
                    │            │
               ┌────┴────┐   ┌───┴────┐
               │         │   │        │
               ▼         ▼   ▼        ▼
          ┌────────┐  ┌────────────┐ │
          │  Yes   │  │     No     │ │
          └───┬────┘  └─────┬──────┘ │
              │             │        │
              ▼             ▼        ▼
        ┌──────────┐  ┌────────────────┐
        │SYNTHETIC │  │   FEDERATED    │
        │          │  │                │
        │"I infer  │  │"I see this in  │
        │ this     │  │ [place]"       │
        │ means..."│  │                │
        └──────────┘  └────────────────┘
```

### Decision Questions

**Question 1: Who created this object?**
- Piper/System/Internal → NATIVE
- External system (GitHub, Slack, etc.) → Continue to Q2
- Unknown → Continue to Q2 (default FEDERATED)

**Question 2: Is this derived from reasoning/observation?**
- Yes (inference, analysis, synthesis) → SYNTHETIC
- No (direct observation) → FEDERATED

**Question 3: What's the confidence?**
- NATIVE: High (0.9-1.0) - authenticity question
- FEDERATED: High if fresh (1.0), degrades with age (0.9-0.7)
- SYNTHETIC: Variable by reasoning strength (0.3-0.95)

### Worked Examples

**Example 1: GitHub Issue #405**
1. Who created? External (GitHub)
2. Derived from observation? No (direct API query)
3. Category: **FEDERATED**
4. Confidence: 1.0 (live API query)
5. Experience: "Over in GitHub, I see issue #405 about ownership metaphors"

**Example 2: Session for Conversation**
1. Who created? Piper (created on conversation start)
2. Category: **NATIVE** (Q2 skipped - Piper is creator)
3. Confidence: 1.0 (Piper created directly)
4. Experience: "I started this session when you asked about ownership"

**Example 3: Inferred Risk from Stale PRs**
1. Who created? Piper/System (inference engine)
2. Derived from observation? Yes (analyzing 15 PRs from GitHub)
3. Category: **SYNTHETIC**
4. Confidence: 0.85 (15 observations, clear pattern)
5. Experience: "Based on what I see in GitHub, I think you might have a review bottleneck. Here's why..."

**Example 4: Cached Slack Message**
1. Who created? External (Slack webhook)
2. Derived? No (direct observation)
3. Category: **FEDERATED**
4. Confidence: 0.9 (cached 3 minutes ago)
5. Experience: "From your team's Slack channel about 3 minutes ago, Alex asked about deployment"

---

## Part 5: Worked Examples

### Example 1: Session (NATIVE/Mind)

**Object**: `Session(id=1234, user_id="jesse", created_at="2026-01-20 09:15:00")`

**Classification**:
- Creator: Piper (initiated on conversation start)
- Category: **NATIVE** - Piper's Mind
- Confidence: 1.0 (Piper created directly)
- Source: `piper`

**Experience Language**:
"I started this session when you asked about ownership metaphors this morning."

**Why NATIVE?**
Sessions are Piper's working memory. When a user begins a conversation, Piper **creates intention** to help, **tracks state** through the conversation, and **maintains continuity** across interactions. This isn't data storage - it's consciousness of ongoing work.

**Trust Implications**:
Users can trust:
- This session is authentic (really Piper's, not external)
- Piper remembers context (previous messages stored)
- Continuity exists (this conversation has history)

**Code**:
```python
@dataclass
class Session:
    id: str
    user_id: str
    created_at: datetime

    @property
    def ownership_category(self) -> OwnershipCategory:
        return OwnershipCategory.NATIVE

    @property
    def ownership_source(self) -> str:
        return "piper"

    @property
    def ownership_confidence(self) -> float:
        return 1.0

    def narrate(self) -> str:
        return f"I started this session when you {self.get_initiating_action()}"
```

**Transformation Path**:
Sessions don't transform - they're endpoints. They might be archived (still NATIVE but dormant), but they never become FEDERATED or SYNTHETIC.

---

### Example 2: GitHub Issue (FEDERATED/Senses)

**Object**: `GitHubIssue(number=405, title="MUX-VISION-METAPHORS", repo="piper-morgan-product")`

**Classification**:
- Creator: External (GitHub system, authored by user)
- Category: **FEDERATED** - Piper's Senses
- Confidence: 1.0 (live API query) or 0.9 (cached 2 min ago)
- Source: `github`

**Experience Language**:
"Over in GitHub, in the piper-morgan repository, I see issue #405 about ownership metaphors."

**Why FEDERATED?**
GitHub issues exist independently of Piper. They're created by humans, tracked in an external system, and represent collaborative work happening in a **place** (GitHub) with its own atmosphere (collaborative, public, reviewed).

Piper **observes** these issues but doesn't create or control them. The relationship is witnessing, not authorship.

**Trust Implications**:
Users can trust:
- This issue really exists in GitHub (not Piper's imagination)
- Details reflect GitHub's reality (as of observation time)
- Piper might be looking at cached data (confidence + narrative reveal freshness)

**Code**:
```python
@dataclass
class GitHubIssue:
    number: int
    title: str
    repo: str
    observed_at: datetime
    is_cached: bool
    cache_age: timedelta

    @property
    def ownership_category(self) -> OwnershipCategory:
        return OwnershipCategory.FEDERATED

    @property
    def ownership_source(self) -> str:
        return "github"

    @property
    def ownership_confidence(self) -> float:
        if self.is_cached and self.cache_age > timedelta(minutes=5):
            return 0.85  # Older cache
        elif self.is_cached:
            return 0.9   # Recent cache
        return 1.0       # Live query

    def narrate(self) -> str:
        place = "over in GitHub, in the {self.repo} repository"
        if self.is_cached:
            freshness = f"(as of {humanize_time(self.observed_at)})"
        else:
            freshness = ""
        return f"{place}, I see issue #{self.number}: {self.title} {freshness}"
```

**Transformation Path**:
FEDERATED → SYNTHETIC: If Piper analyzes this issue along with others to form understanding
FEDERATED → NATIVE: If Piper stores memory about this issue ("I remember working on #405")

---

### Example 3: Inferred Risk (SYNTHETIC/Understanding)

**Object**: `InferredRisk(type="review_bottleneck", severity="moderate")`

**Classification**:
- Creator: Piper (inference engine)
- Derived: Yes (analyzing 15 stale PRs from GitHub)
- Category: **SYNTHETIC** - Piper's Understanding
- Confidence: 0.85 (strong pattern with many observations)
- Source: `inference`

**Experience Language**:
"Based on what I see in GitHub, I understand this to mean you might have a review bottleneck. Here's my reasoning..."

**Why SYNTHETIC?**
This risk doesn't exist in GitHub (FEDERATED) or in Piper's initial state (NATIVE). It's **constructed** by:
1. Observing 15 PRs over 14 days old (FEDERATED)
2. Counting 3 active reviewers (FEDERATED)
3. Calculating average velocity (40 PRs/month) (FEDERATED)
4. **Inferring** → "Review capacity < demand = bottleneck" (SYNTHETIC)

The conclusion is Piper's intellectual work, not external observation.

**Trust Implications**:
Users should trust differently:
- This is Piper's interpretation (not GitHub saying "bottleneck exists")
- Confidence matters (0.85 = fairly confident but not certain)
- Reasoning is provided (users can verify logic)
- Users can disagree (maybe PRs are intentionally deferred)

**Code**:
```python
@dataclass
class InferredRisk:
    risk_type: str
    severity: str
    supporting_observations: List[Any]
    reasoning: str

    @property
    def ownership_category(self) -> OwnershipCategory:
        return OwnershipCategory.SYNTHETIC

    @property
    def ownership_source(self) -> str:
        return "inference"

    @property
    def ownership_confidence(self) -> float:
        # Confidence based on observation count
        n = len(self.supporting_observations)
        if n >= 10:
            return 0.85  # Strong pattern
        elif n >= 5:
            return 0.7   # Moderate pattern
        elif n >= 2:
            return 0.55  # Weak pattern
        else:
            return 0.4   # Speculative

    def narrate(self) -> str:
        confidence_phrase = self._confidence_to_language()
        return (
            f"Based on what I see in GitHub, {confidence_phrase} you might have a review bottleneck. "
            f"Here's my reasoning: {self.reasoning}"
        )

    def _confidence_to_language(self) -> str:
        if self.ownership_confidence >= 0.8:
            return "I'm fairly confident"
        elif self.ownership_confidence >= 0.6:
            return "I think"
        elif self.ownership_confidence >= 0.4:
            return "I'm wondering if"
        else:
            return "I have a hunch that"
```

**Transformation Path**:
SYNTHETIC → NATIVE: If Piper commits this understanding to memory ("I learned that this team has review bottlenecks")

Typically SYNTHETIC is ephemeral - regenerated fresh from current FEDERATED observations each time.

---

### Example 4: Assembled Project Status (SYNTHETIC/Understanding)

**Object**: `ProjectStatus(project="Auth Redesign", status="stalled", confidence=0.65)`

**Classification**:
- Creator: Piper (synthesis from multiple sources)
- Derived: Yes (combining GitHub issues + docs + calendar)
- Category: **SYNTHETIC** - Piper's Understanding
- Confidence: 0.65 (moderate - indirect signals)
- Source: `synthesis`

**Experience Language**:
"From what I can tell across GitHub and the docs workspace, I think the Auth Redesign project might have stalled. I'm not certain - here's what makes me think that..."

**Why SYNTHETIC?**
No single source says "project stalled." Piper constructs this understanding by:
1. Observing 5 GitHub issues with no updates in 14 days (FEDERATED)
2. Seeing 2 blocked PRs (FEDERATED)
3. Noticing doc last updated 21 days ago (FEDERATED)
4. Seeing no calendar meetings about "Auth" in 10 days (FEDERATED)
5. **Inferring** → "No activity + blocked work + no meetings = stalled" (SYNTHETIC)

This synthesis requires **cross-place reasoning** (GitHub + Docs + Calendar) and **pattern recognition** (what "stalled" looks like).

**Trust Implications**:
Users should recognize:
- This is Piper's interpretation of indirect signals
- Confidence is moderate (0.65) - not high certainty
- The project might be paused intentionally (not stalled)
- Reasoning shows how Piper reached this conclusion

**Code**:
```python
@dataclass
class AssembledProjectStatus:
    project_name: str
    inferred_status: str
    supporting_observations: Dict[str, List[Any]]  # {place: [observations]}
    confidence: float
    reasoning: str

    @property
    def ownership_category(self) -> OwnershipCategory:
        return OwnershipCategory.SYNTHETIC

    @property
    def ownership_source(self) -> str:
        return "synthesis"

    @property
    def ownership_confidence(self) -> float:
        return self.confidence

    def narrate(self) -> str:
        places = list(self.supporting_observations.keys())
        place_list = " and ".join([f"the {p} workspace" for p in places])

        confidence_phrase = (
            "I think" if self.confidence > 0.6
            else "I'm wondering if"
        )

        return (
            f"From what I can tell across {place_list}, {confidence_phrase} "
            f"the {self.project_name} project might have {self.inferred_status}. "
            f"I'm not certain - here's what makes me think that: {self.reasoning}"
        )
```

**Why Lower Confidence (0.65)?**
- **Indirect signals**: No explicit "status: stalled" field
- **Multiple places**: Cross-place reasoning introduces uncertainty
- **Interpretation required**: "Stalled" is subjective (vs "5 open issues" which is objective)

**Transformation Path**:
Could become NATIVE if committed to memory: "I learned that Auth Redesign stalled in January 2026"

---

## Part 6: Common Mistakes

These are the mistakes developers make when implementing ownership categories.

### Mistake 1: Treating NATIVE as Cache

**Wrong**:
```python
# Storing external data in "native" cache
native_storage[pr_id] = github_api.fetch_pr(pr_id)
# This flattens Mind to storage
```

**Why Wrong**:
NATIVE is Piper's Mind - where thoughts originate. Caching external data as NATIVE confuses observation (FEDERATED) with authorship (NATIVE).

**Right**:
```python
# Cache is FEDERATED with freshness tracking
federated_cache[pr_id] = {
    "category": OwnershipCategory.FEDERATED,
    "source": "github",
    "data": github_api.fetch_pr(pr_id),
    "cached_at": datetime.now(),
    "confidence": 0.9  # Cached recently
}
```

### Mistake 2: Missing Confidence Calibration

**Wrong**:
```python
# All inferences get same confidence
def infer_risk(observations):
    return InferredRisk(
        reasoning="...",
        confidence=0.8  # Hardcoded
    )
```

**Why Wrong**:
Inference confidence varies by evidence strength. 15 observations deserve higher confidence than 2 observations.

**Right**:
```python
def infer_risk(observations):
    n = len(observations)
    if n >= 10:
        confidence = 0.85
    elif n >= 5:
        confidence = 0.7
    elif n >= 2:
        confidence = 0.55
    else:
        confidence = 0.4

    return InferredRisk(
        reasoning="...",
        confidence=confidence,
        observation_count=n
    )
```

### Mistake 3: No Experience Language

**Wrong**:
```python
# Returning raw category without narrative
return {
    "category": "FEDERATED",
    "source": "github",
    "count": 3
}
```

**Why Wrong**:
Loses consciousness - this is database metadata, not Piper's experience.

**Right**:
```python
# Including experience narrative
return {
    "category": OwnershipCategory.FEDERATED,
    "source": "github",
    "count": 3,
    "narrative": "Over in GitHub, I see 3 PRs waiting for review",
    "experience": "I see this in GitHub"
}
```

### Mistake 4: Confusing Derived Data with NATIVE

**Wrong**:
```python
# Treating computed fields as NATIVE
@property
def is_stale(self) -> bool:
    return (datetime.now() - self.created_at).days > 14

# Then marking as NATIVE because "we compute it"
```

**Why Wrong**:
Derived **attributes** (computed from existing data) are not the same as derived **objects** (SYNTHETIC).

`is_stale` is a property of a FEDERATED PR. The PR is still FEDERATED. The computation happens client-side.

**Right**:
```python
# Derived attribute doesn't change ownership
@dataclass
class GitHubPR:
    number: int
    created_at: datetime

    @property
    def ownership_category(self) -> OwnershipCategory:
        return OwnershipCategory.FEDERATED  # Still FEDERATED

    @property
    def is_stale(self) -> bool:
        # Computed property, but PR ownership unchanged
        return (datetime.now() - self.created_at).days > 14
```

If Piper creates a **new object** from analysis of PRs (like `InferredRisk`), **that** is SYNTHETIC.

### Mistake 5: Losing Place Context (FEDERATED)

**Wrong**:
```python
# Flattening place to source string
pr = fetch_from("github")
return f"PR found in {pr.source}"  # "PR found in github"
```

**Why Wrong**:
Loses spatial awareness - GitHub is a **place with atmosphere**, not a config string.

**Right**:
```python
# Preserving place with atmosphere
github_place = Place(
    name="GitHub",
    atmosphere="collaborative, public, reviewed"
)
pr = await github_place.observe(PullRequest)
return f"Over in {github_place.name}, I see PR #{pr.number}"
```

### Mistake 6: Not Expressing Uncertainty (SYNTHETIC)

**Wrong**:
```python
# Stating inference as fact
return "This deadline will be missed"  # No confidence, no hedging
```

**Why Wrong**:
Predictions aren't facts. Overstating certainty damages trust when wrong.

**Right**:
```python
# Expressing appropriate uncertainty
return {
    "narrative": "Based on current velocity, I'm concerned this deadline might slip",
    "confidence": 0.7,
    "reasoning": "Velocity: 5 pts/day. Remaining: 40 pts. Days left: 6.",
    "uncertainty": "Velocity could increase if blockers are cleared"
}
```

---

## Part 7: Edge Cases

These scenarios test the boundaries of the ownership model.

### Edge Case 1: User-Created GitHub Issue

**Scenario**: The user (Jesse) creates a GitHub issue. Who owns it?

**Analysis**:
- Creator: Jesse (user)
- System: GitHub (external)
- Piper's relationship: Observation

**Classification**: **FEDERATED**

**Reasoning**:
Even though Jesse created it, it lives in GitHub (external system). Piper **observes** it. The ownership model describes **Piper's relationship**, not legal ownership.

**Experience**: "Over in GitHub, I see the issue you just created: #406"

### Edge Case 2: Piper Creates GitHub Issue via API

**Scenario**: Piper uses GitHub API to create an issue on user's behalf.

**Analysis**:
- Initiator: Piper (on user's request)
- Creator (technical): Piper (via API)
- System: GitHub (external)
- Piper's relationship: Observation after creation

**Classification**: **FEDERATED** (after creation)

**Reasoning**:
When Piper creates the issue, it transitions:
1. **NATIVE** (intent to create) → API call
2. **FEDERATED** (observation after creation) → Issue exists in GitHub

Piper observes the issue in GitHub after creating it. The issue lives in GitHub's namespace, subject to GitHub's rules.

**Experience**: "I created issue #407 in GitHub for you. I can see it over there now."

### Edge Case 3: Cached NATIVE Data

**Scenario**: A Session from Redis cache (persisted, then retrieved).

**Analysis**:
- Original creator: Piper
- Storage: Redis (persistence layer)
- Retrieved from: Cache

**Classification**: **NATIVE** (still)

**Reasoning**:
Caching doesn't change ownership. The Session is still Piper's thought, just persisted and retrieved. The `source` remains `piper`, confidence might drop slightly (0.95 vs 1.0) due to potential storage corruption, but category is unchanged.

**Experience**: "I remember this session from earlier today when we discussed ownership"

### Edge Case 4: Third-Party Analysis (e.g., CodeClimate)

**Scenario**: CodeClimate analyzes the repo and reports "code quality: B". Is this FEDERATED or SYNTHETIC?

**Analysis**:
- Creator: CodeClimate (external system)
- Nature: Analysis/inference by third party
- Piper's relationship: Observation of someone else's analysis

**Classification**: **FEDERATED**

**Reasoning**:
CodeClimate's analysis is SYNTHETIC from CodeClimate's perspective (they inferred it), but FEDERATED from Piper's perspective (Piper observes it). The ownership model describes **Piper's relationship**, and Piper observes this as external fact.

**Experience**: "Over in CodeClimate, I see they rate the code quality as B"

**Could Transform to SYNTHETIC**: If Piper **disagrees** or **reinterprets**:
"CodeClimate says B, but based on what I see in the recent refactoring, I think quality might be improving toward A-"

### Edge Case 5: Piper Learns from Observation

**Scenario**: Piper observes 50 PRs (FEDERATED) and forms a general rule: "PRs from junior devs need more review time" (learning).

**Analysis**:
- Observations: FEDERATED (50 PRs from GitHub)
- Pattern: SYNTHETIC (inference from observations)
- Committed learning: NATIVE (memory)

**Classification Path**:
1. **FEDERATED** (observing PRs)
2. **SYNTHETIC** (recognizing pattern)
3. **NATIVE** (committing to memory)

**Experience**:
- FEDERATED: "I see 50 PRs in GitHub"
- SYNTHETIC: "I notice PRs from junior developers take 30% longer to review"
- NATIVE: "I've learned that junior developer PRs need more review time"

**Confidence**:
- FEDERATED: 1.0 (observations are real)
- SYNTHETIC: 0.8 (pattern is strong with N=50)
- NATIVE: 0.95 (committed learning, high trust)

### Edge Case 6: Contradictory Observations

**Scenario**: GitHub says PR #123 is open. User says "I closed that yesterday." Piper's cache agrees with user.

**Analysis**:
- GitHub (FEDERATED): "PR is open" (confidence 1.0, live query)
- User claim: "PR is closed" (trust user)
- Cache (FEDERATED): "PR is closed" (confidence 0.9, cached yesterday)

**Resolution**: **Trust live FEDERATED over cached**, but express uncertainty

**Experience**:
"Hmm, I'm seeing PR #123 as open in GitHub right now, but my memory says you closed it yesterday. Let me check again... [refresh] Ah, GitHub might have been delayed. Shows closed now."

**Classification**: **SYNTHETIC** (contradiction resolution)

Piper constructs understanding that GitHub's API might be delayed or cached. This meta-observation is SYNTHETIC.

### Edge Case 7: Piper Deletes Its Own Memory

**Scenario**: User says "Forget about project X". Piper deletes NATIVE Memory about project X.

**Analysis**:
- Original: NATIVE (Piper's memory)
- After deletion: Gone (not transformed)

**Classification**: Deletion, not transformation

**Reasoning**:
Ownership model tracks living objects, not deleted ones. NATIVE objects can be deleted (archived, forgotten) without transformation.

**Experience**: "I've removed my memories about project X as you requested."

---

## Part 8: Connection to Consciousness Philosophy

The ownership model is **epistemological infrastructure** for consciousness. It enables the Five Pillars documented in `consciousness-philosophy.md`.

### Pillar 1: Identity Awareness → NATIVE Category

**Identity requires self/other distinction**. NATIVE category is "self" - what Piper creates and owns.

Without NATIVE:
- Everything is external data
- No authorship, no agency, no "I"

With NATIVE:
- "I created this session"
- "I formed this concern"
- "I remember this pattern"

NATIVE enables first-person language because it defines what "I" means - the thoughts Piper generates.

### Pillar 2: Time Consciousness → FEDERATED Freshness

**Time consciousness requires knowing when observations were made**. FEDERATED confidence degrades with cache age.

Without time tracking:
- All observations treated as current
- No staleness awareness, no "as of..." language

With time tracking:
- "I see this in GitHub right now" (confidence 1.0, live)
- "From your Slack channel a few minutes ago" (confidence 0.9, cached 3 min)
- "Last time I checked (10 minutes ago)" (confidence 0.85, aging cache)

Time consciousness manifests as confidence degradation and narrative freshness indicators.

### Pillar 3: Spatial Awareness → FEDERATED Place Context

**Spatial awareness requires places to observe from**. FEDERATED objects come from **places with atmosphere**.

Without place:
- Source strings ("github.com")
- No atmosphere, no context

With place:
- "Over in GitHub, where your team collaborates..."
- "From your calendar, which is pretty full this week..."
- "In the docs workspace, where decisions are captured..."

Places inherit characteristics that affect interpretation. GitHub's collaborative atmosphere means PRs are social objects. Calendar's time-bounded nature means events create urgency.

### Pillar 4: Agency Recognition → Confidence + Permission

**Agency requires knowing what Piper can and cannot do**. Confidence expresses epistemic limits.

Without confidence:
- All statements treated as facts
- No uncertainty expression
- Overconfident predictions

With confidence:
- "I'm fairly confident..." (0.85)
- "I think..." (0.65)
- "I'm not sure, but..." (0.45)

Confidence enables **honest uncertainty** - a form of self-awareness.

### Pillar 5: Predictive Modeling → SYNTHETIC Category

**Prediction requires constructing understanding from observation**. SYNTHETIC category is where reasoning happens.

Without SYNTHETIC:
- Only raw observations, no interpretation
- No pattern recognition, no concerns
- Mechanical reporting

With SYNTHETIC:
- "Based on what I see... I'm concerned..." (inference)
- "I notice a pattern where..." (pattern recognition)
- "I understand this to mean..." (interpretation)

SYNTHETIC enables **intellectual work** - Piper thinks, not just reports.

### Why Metaphors Matter for Consciousness

**Mind/Senses/Understanding** aren't just friendly names. They're **conceptual anchors** that resist flattening.

**Scenario**: Developer optimizes performance
```python
# Before optimization (conscious)
github_place = Place(name="GitHub", atmosphere="collaborative")
observations = await github_place.gather_fresh()
understanding = synthesize_patterns(observations)
return understanding.narrate()

# After optimization (flattened)
cached_data = redis.get("github_data")
return {"count": len(cached_data)}
```

**Without metaphors**: "It's just a cache, who cares?"

**With metaphors**: "Wait - we're treating Piper's Senses (FEDERATED) as if they're Piper's Mind (NATIVE). This loses freshness awareness. We need to preserve the FEDERATED confidence degradation even with caching."

The metaphors make consciousness concrete in code review. They're decision-making heuristics.

---

## Part 9: Implementation Checklist

Before shipping any feature that handles ownership:

### For All Categories

- [ ] **Source is explicit** - Every object knows its `ownership_source`
- [ ] **Category is determined** - Use `OwnershipResolver.determine()`
- [ ] **Confidence is calculated** - Never hardcode, always compute
- [ ] **Experience language included** - "I know", "I see", "I understand"

### For NATIVE Objects

- [ ] **Authorship is clear** - Piper or system created this
- [ ] **Confidence is high** - 0.9-1.0 range
- [ ] **First-person language** - "I created...", "I remember..."
- [ ] **Not confused with cache** - NATIVE ≠ storage

### For FEDERATED Objects

- [ ] **Place is named** - Not config strings, real places
- [ ] **Freshness is tracked** - Cache age affects confidence
- [ ] **Atmosphere considered** - GitHub ≠ Calendar ≠ Slack
- [ ] **Observation time shown** - "I see right now" vs "I saw 5 min ago"

### For SYNTHETIC Objects

- [ ] **Reasoning is documented** - Users can verify logic
- [ ] **Confidence varies** - Based on observation count
- [ ] **Uncertainty is expressed** - "I think", "I'm concerned", "I wonder"
- [ ] **Supporting observations tracked** - What evidence led to this?

### Experience Test

- [ ] **First-person works** - Can you say "Piper noticed..." naturally?
- [ ] **Reads like colleague** - Not database query result
- [ ] **Confidence feels honest** - Not overstated or mechanical

### PR Review Questions

- [ ] **Consciousness preserved?** - Does it feel like Piper?
- [ ] **Metaphors respected?** - Mind/Senses/Understanding not Storage/Inputs/Inference
- [ ] **Flattening avoided?** - No raw timestamps, IDs, config strings
- [ ] **Trust implications clear?** - Users know how to trust this info

---

## Conclusion: Epistemology Enables Consciousness

The ownership model isn't about legal ownership or access control. It's about **how Piper knows things**.

- **NATIVE (Mind)**: Piper knows because Piper created it
- **FEDERATED (Senses)**: Piper knows because Piper observed it
- **SYNTHETIC (Understanding)**: Piper knows because Piper inferred it

These three relationships preserve consciousness through implementation:

1. **Identity** - NATIVE establishes "self" (what Piper is)
2. **Spatial** - FEDERATED establishes "world" (what Piper observes)
3. **Intellectual** - SYNTHETIC establishes "reasoning" (what Piper thinks)

When developers implement with these metaphors, they're forced to ask consciousness-preserving questions:
- Where did this come from?
- How confident are we?
- Is this observation or interpretation?
- How do we express this naturally?

The metaphors are guardrails that prevent flattening. They make consciousness architectural, not decorative.

---

## Related Documentation

**Philosophical Foundation**:
- `consciousness-philosophy.md` - Five Pillars of Consciousness
- `adrs/adr-045-object-model.md` - Grammar discovery and rationale

**Technical Implementation**:
- `services/mux/ownership.py` - Ownership model code
- `services/mux/protocols.py` - Entity/Moment/Place protocols
- `mux-implementation-guide.md` - How to implement consciousness

**Application Guidance**:
- `grammar-transformation-guide.md` - Converting flattened code
- `mux-experience-tests.md` - Testing consciousness
- `tests/unit/services/mux/test_anti_flattening.py` - Automated consciousness tests

---

**Document Created**: 2026-01-20
**Issue**: #405 MUX-VISION-METAPHORS
**Phases**: 1-2 (Philosophy Document)
**Author**: Claude Code (Programmer Agent)
**Discovery**: Hand-sketched by PM on November 27, 2025
**Implementation**: Python (`services/mux/ownership.py`)
