# B1 FTUX Implicit Grammar Mapping

**Investigation Phase**: P0 - Investigation & Pattern Discovery
**Parent Issue**: #612 (MUX-399-P0)
**Date**: 2026-01-19
**Investigator**: Claude Code (Lead Developer role)

---

## Executive Summary

The B1 FTUX specs implicitly use Entity/Moment/Place/Situation thinking throughout, though without that vocabulary. The grammar is embedded in how they describe:
- **Entities**: Piper as colleague, User as person with context, Integrations as capabilities
- **Moments**: Task completion, first use, return visits, pauses
- **Places**: Views, channels, entry points, contexts
- **Situations**: Empty states, dead ends, onboarding, progressive disclosure

**Key insight**: The specs already think grammatically—they just need the vocabulary upgrade.

---

## Methodology

For each spec, I extracted:
1. **Entity concepts**: How does the spec treat actors and objects?
2. **Moment concepts**: What temporal/experiential events does it describe?
3. **Place concepts**: What contexts, views, or environments does it address?
4. **Situation concepts**: What circumstances trigger specific behaviors?

---

## Spec-by-Spec Analysis

### 1. Empty State Voice Guide (`empty-state-voice-guide-v1.md`)

**Source**: `docs/internal/design/specs/empty-state-voice-guide-v1.md`

#### Entity Concepts

| Implicit Entity | Quoted Evidence | Grammar Mapping |
|----------------|-----------------|-----------------|
| **Piper as Colleague** | "Would a helpful colleague say this?" (line 332) | Entity with relationship |
| **User as Person** | "first-time test", "return-user test" (lines 336-343) | Entity with history |
| **Integrations as Capabilities** | "Once you add your GitHub token... I can help you triage issues" (lines 117-119) | Federated Entities |

**Key Quote**:
> "Piper knows what it can do. State it simply." (line 42)

This implies Piper has **self-awareness** of capabilities—an Entity trait.

#### Moment Concepts

| Implicit Moment | Quoted Evidence | Grammar Mapping |
|----------------|-----------------|-----------------|
| **First Use** | "Imagine a user seeing this view for the first time" (line 336) | Emergent moment |
| **Completion** | "All caught up! Your todo list is clear." (lines 73-75) | Achieved moment |
| **Return** | "Does the empty state congratulate appropriately, or treat them like a newbie again?" (lines 343-344) | Recurring moment |
| **Teaching** | "Empty states are teaching moments" (line 13) | Transformative moment |

**Key Quote**:
> "Empty states are **teaching moments**. They orient users to what's possible without being a tutorial." (line 13)

The term "teaching moment" is exactly Moment thinking—a significant occurrence in time.

#### Place Concepts

| Implicit Place | Quoted Evidence | Grammar Mapping |
|----------------|-----------------|-----------------|
| **Views** | "Todos View", "Standup View", "Calendar View" (lines 58, 79, 124) | Places with atmosphere |
| **Empty States** | "oriented, not empty" (line 7) | Place quality |
| **Workspace** | "No documents in your knowledge base yet" (line 150) | Contextual place |

**Key Quote**:
> "Empty states should be **oriented, not empty**" (PDR-001, referenced line 7)

"Oriented" implies the Place has direction, atmosphere—not just absence.

#### Situation Concepts

| Implicit Situation | Quoted Evidence | Grammar Mapping |
|-------------------|-----------------|-----------------|
| **Missing Integration** | "GitHub isn't connected yet" template (lines 114-119) | Incomplete situation |
| **No Data** | "No todos yet" vs "All caught up" (lines 62, 69) | Different situations for same Place |
| **Error vs Empty** | "Empty state: Nothing exists yet (neutral) / Error state: Something went wrong" (lines 310-311) | Situation types |

---

### 2. Contextual Hint UX Spec (`contextual-hint-ux-spec-v1.md`)

**Source**: `docs/internal/design/specs/contextual-hint-ux-spec-v1.md`

#### Entity Concepts

| Implicit Entity | Quoted Evidence | Grammar Mapping |
|----------------|-----------------|-----------------|
| **Piper as Actor** | "I can also post this to Slack" (line 41) | Entity with capabilities |
| **User with State** | "session state", "user preferences" (lines 239-257) | Entity with memory |
| **Hints as Objects** | "hint_count", "shown_hints" tracking (lines 243-247) | Synthetic entities |

**Key Quote**:
> "I can also..." (line 207) - First person voice indicates Entity self-reference.

#### Moment Concepts

| Implicit Moment | Quoted Evidence | Grammar Mapping |
|----------------|-----------------|-----------------|
| **Post-Task** | "User completes a task successfully" (line 32) | Completion moment |
| **Context-Aware** | "Piper detects context that suggests a capability" (line 47) | Recognition moment |
| **Natural Pause** | "Only show at natural pause points" (line 125) | Interstitial moment |
| **Dismissal** | "Hint fades out, counts as 'ignored'" (line 143) | Ending moment |

**Key Quote**:
> "Surface capabilities at **moments when they're relevant**—after successful task completion, during natural pauses" (lines 12-13)

The word "moments" is used explicitly here.

#### Place Concepts

| Implicit Place | Quoted Evidence | Grammar Mapping |
|----------------|-----------------|-----------------|
| **Response Space** | "Below the response content, Above the input field" (lines 84-86) | UI Place |
| **Peripheral** | "noticeable but not block workflow" (line 22) | Atmospheric quality |

#### Situation Concepts

| Implicit Situation | Quoted Evidence | Grammar Mapping |
|-------------------|-----------------|-----------------|
| **Hint Eligibility** | `should_show_hint()` function (lines 262-273) | Computational situation |
| **Throttling** | "Maximum 2 suggestions per 5 interactions" (line 123) | Temporal situation |
| **Suppression** | "After 2nd ignored hint" (line 158) | User-driven situation |

**Key Pattern** (lines 262-273):
```python
def should_show_hint(session, user, hint_id):
    if not user.hints_enabled:
        return False
    if session.ignored_count >= 2:
        return False
    ...
```

This is **Situation evaluation** in code form—checking multiple factors to determine appropriate behavior.

---

### 3. Multi-Entry FTUX Exploration (`multi-entry-ftux-exploration-v1.md`)

**Source**: `docs/internal/design/specs/multi-entry-ftux-exploration-v1.md`

#### Entity Concepts

| Implicit Entity | Quoted Evidence | Grammar Mapping |
|----------------|-----------------|-----------------|
| **User with Identity** | "Account (email) / Identity" (line 337) | Core Entity |
| **Piper as Responder** | "Piper recognizes user, assesses context" (line 373) | Entity with perception |
| **Team as Collective** | "Team integration inheritance" (line 423) | Collective Entity |
| **Integrations** | "GitHub: connected / Slack: team has it / Calendar: not connected" (lines 293-297) | Federated Entities |

**Key Quote**:
> "Each entry point has different: User intent (why they're here), Available context (what Piper knows), Appropriate first interaction (what Piper should say/do)" (lines 62-64)

This is pure **Situation** thinking—same Entity, different context, different appropriate response.

#### Moment Concepts

| Implicit Moment | Quoted Evidence | Grammar Mapping |
|----------------|-----------------|-----------------|
| **Cold Start** | "User signed up, opened web app for first time" (line 71) | Emergent moment |
| **First @mention** | "User @mentions Piper without prior web setup" (line 113) | Introduction moment |
| **Token Expiry** | "your GitHub token expired" (line 275) | Lifecycle moment |
| **Progressive Setup** | "Setup happens as needed, not all upfront" (line 28) | Gradual moments |

**Key Quote**:
> "Value is demonstrated before configuration is demanded" (line 434)

This is temporal/experiential—a sequence of Moments where value precedes setup.

#### Place Concepts

| Implicit Place | Quoted Evidence | Grammar Mapping |
|----------------|-----------------|-----------------|
| **Entry Points** | "Web App (Direct)", "Slack @piper", "CLI `piper`", "Calendar Integration" (lines 43-47) | Entry Places |
| **Channels** | "User in #engineering: @piper..." (line 121) | Slack Place |
| **DMs** | "I'll send you a DM to set that up privately" (lines 138-139) | Private Place |

**Entry Point Map** (lines 37-57):
```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ Web (cold)  │   │ Slack       │   │ CLI         │
│             │   │ @mention    │   │             │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                         ▼
              ┌─────────────────┐
              │  Same Piper     │
              │  Same Context   │
              │  Same User      │
              └─────────────────┘
```

This diagram shows multiple **Places** converging to the same **Entity** (Piper) and **Entity** (User).

#### Situation Concepts

| Implicit Situation | Quoted Evidence | Grammar Mapping |
|-------------------|-----------------|-----------------|
| **Setup State** | "Setup complete vs setup incomplete → granular state" (line 290) | Progressive situation |
| **Capability Availability** | "computed from this state: Standup: Partial, Calendar: Unavailable" (lines 305-309) | Derived situation |
| **Contextual Prompts** | "Prompt Opportunity" table (lines 320-325) | Triggered situations |

**Key Quote**:
> "Rather than wizard steps, setup happens through **contextual prompts**" (line 318)

"Contextual prompts" = responding to **Situation**, not linear sequence.

---

## Grammar Mapping Table

| Spec | Entity Examples | Moment Examples | Place Examples | Situation Examples |
|------|-----------------|-----------------|----------------|-------------------|
| **Empty State Voice** | "Piper knows what it can do" (self-aware), User (first-time vs returning) | "teaching moments", completion ("All caught up!") | Views (Todos, Standup, Calendar), Empty states as oriented | Missing integration, No data vs All done |
| **Contextual Hints** | "I can also..." (first person), User session state | Post-task, Natural pause, Dismissal | Response space, Peripheral placement | Hint eligibility, Throttling, Suppression |
| **Multi-Entry FTUX** | User identity, Piper as responder, Team collective | Cold start, First @mention, Token expiry | Entry points (Web, Slack, CLI), Channels, DMs | Setup state, Capability availability, Contextual prompts |

---

## Cross-Cutting Observations

### 1. Piper is Already Treated as an Entity

All three specs use first-person language for Piper:
- "I can help you triage issues" (Empty State)
- "I can also post this to Slack" (Hints)
- "I'd need GitHub access" (Multi-Entry)

Piper is not described as a system but as a colleague with self-knowledge.

### 2. Moments are Described as Opportunities

The specs consistently frame temporal events as **opportunities for appropriate response**:
- Teaching moments
- Natural pause points
- Prompt opportunities

This aligns with the grammar's view that Moments are experienced, not just timestamps.

### 3. Places Have Atmosphere

Empty states are "oriented, not empty"—Places aren't just locations but have qualities:
- Clear (calendar)
- Populated vs empty
- Private (DM) vs public (channel)

### 4. Situations Drive Behavior

The specs describe behavior as situation-dependent, not rule-based:
- Same Place (Todos View) has different responses for "no todos" vs "all done"
- Same Entity (User) gets different treatment for first-time vs returning
- Same capability gets different hints based on session state

---

## Vocabulary Mapping Recommendations

| Current Spec Term | Proposed Grammar Term | Rationale |
|-------------------|----------------------|-----------|
| "View" | Place | A view is a Place in the UI |
| "Entry point" | Entry Place | A starting Place |
| "Session state" | Situation snapshot | State at a Moment |
| "Task completion" | Achieved Moment | A Moment type |
| "Teaching moment" | Transformative Moment | Already uses "moment" |
| "Integration" | Federated Entity | An Entity that connects to external system |
| "User preferences" | Entity configuration | Persistent Entity attributes |
| "Context detection" | Situation recognition | Perceiving current Situation |

---

## Implications for P1

### 1. Spec Language Update

P1 could include updating spec terminology to use the grammar vocabulary. This would:
- Make specs consistent with implementation
- Reinforce the grammar as shared language
- Help new team members understand the conceptual model

### 2. Situation as First-Class Concept

The specs implicitly model Situations but don't name them. Making Situation explicit would:
- Clarify when different behaviors apply
- Enable better computational modeling
- Connect to the Lens infrastructure (which perceives Situations)

### 3. Entity Registry

The specs mention multiple Entity types (User, Piper, Team, Integrations). A formal Entity registry could:
- Track what Entities exist
- Define their ownership model (Native/Federated/Synthetic)
- Enable grammar-compliant feature design

---

## Evidence Summary

| Claim | Spec | Line Numbers |
|-------|------|--------------|
| Piper as colleague with self-awareness | Empty State Voice | 42, 332 |
| "Teaching moments" language | Empty State Voice | 13 |
| First-person "I can" usage | Empty State Voice | 24, 31, 38 |
| "moments when relevant" language | Contextual Hints | 12-13 |
| Situation evaluation code | Contextual Hints | 262-273 |
| Entry point convergence diagram | Multi-Entry FTUX | 362-389 |
| Setup state as granular | Multi-Entry FTUX | 290-303 |
| Contextual prompts table | Multi-Entry FTUX | 320-325 |

---

*Analysis complete: 2026-01-19*
*P0 Deliverable 3 of 4*
