# Research Agent Prompt: Codebase Component Inventory for Wardley Map Validation

**Purpose**: Inventory the Piper Morgan codebase to identify technical components for Wardley map validation
**Prepared by**: CXO
**Date**: December 4, 2025

---

## Context

I'm working with the CXO to build a Wardley map of Piper Morgan's strategic positioning. We have a draft map but want to ensure we haven't missed significant technical components.

## Your Task

Inventory the codebase to identify distinct technical components, then help us categorize them by evolution stage.

## What to Look For

1. **Infrastructure components**: Databases, queues, caching layers, monitoring, logging
2. **Integration points**: External APIs consumed (GitHub, Slack, Notion, Calendar, LLM providers)
3. **Core services**: Major service classes, their responsibilities, and dependencies
4. **Custom implementations**: Things we built that could have been bought/borrowed
5. **Frameworks/libraries**: What we depend on vs. what we built ourselves

## For Each Component, Note

- Name and location in codebase
- What it does (one sentence)
- Whether it's: custom-built, configured-from-library, or pure-consumption-of-external-service
- Any dependencies on other components

## Output Format

```markdown
## Component: [Name]
- **Location**: [path/to/code]
- **Purpose**: [one sentence]
- **Type**: Custom / Configured / Consumed
- **Dependencies**: [list]
- **Suggested Wardley position**: Genesis / Custom / Product / Commodity
- **Notes**: [anything notable]
```

## Current Draft Map (for Reference)

Our current draft map has these components:

| Evolution Stage | Components |
|-----------------|------------|
| **Genesis** | Trust Architecture, Dreaming/Memory, Ethical Consensus, 8D Spatial Intelligence, Learning System, Colleague Relationship |
| **Custom** | Recognition Interface, Canonical Queries, Object Model, Contextual Awareness |
| **Product** | Intent Classification, MCP Federation, Plugin Architecture |
| **Commodity** | GitHub API, Slack API, LLM APIs, PostgreSQL, Calendar Integration |

We want to:
1. Validate these placements
2. Identify anything missing
3. Find components that might be mis-categorized

## Where to Start

1. `services/` directory — core business logic
2. `infrastructure/` or equivalent — technical plumbing
3. Integration modules — external API connections
4. `models/` or `domain/` — data structures and domain logic

## Deliverable

A structured inventory we can use to refine our Wardley map. Focus on technical accuracy; the CXO will handle strategic interpretation.

---

*Prompt prepared for research agent session*
