# Principal Product Manager Brief: Roadmap Realignment
**Date**: December 27, 2025
**From**: Chief Architect
**Re**: MUX Dependencies and Canonical Query Prioritization

## Executive Summary

Pattern Sweep 2.0 revealed that Pattern-045 (Green Tests, Red User) applies directly to our canonical queries - 19 work technically but users cannot discover them. This validates the conversational glue approach as essential infrastructure before expanding features.

## Key Findings

1. **Setup/Config is Alpha Blocker**: Users need explicit setup before any conversational features
2. **Discovery Crisis Confirmed**: 433 pattern usages show features exist but aren't discoverable
3. **MUX Timing**: 38 issues across 4+ sprints - January start realistic after setup work
4. **Completion Risk**: Pattern-046 (Beads) shows multi-sprint epics have high 75% abandonment risk

## Proposed Dependency Stack

1. **Immediate (Alpha)**: Setup/Config web wizard with CLI parity
2. **Next (Beta)**: Conversational glue for discovery
3. **Then (v0.9)**: MUX consciousness architecture
4. **Future (v1.0)**: Proactive contextual assistance

## Questions for Your Expertise

1. **Canonical Query Prioritization**: Of our 63 queries, which 10-15 would constitute "minimum viable PM assistant" for alpha validation? Should we focus on daily workflow (standup, todos) or strategic work (analysis, planning)?

2. **Discovery vs Features Trade-off**: Should we pause new feature development entirely until conversational discovery works? Or maintain parallel tracks?

3. **User Validation Triggers**: What specific user behaviors or feedback would signal we've solved the discovery problem sufficiently to proceed with MUX?

4. **Alpha Success Metrics**: Given Pattern-045, should we measure feature usage or feature discovery as primary alpha KPI?

5. **Portfolio Approach**: You've seen many product evolutions - does our three-level progression (explicit→conversational→proactive) align with successful assistant products you've observed?

## Your Input Needed On

- Risk assessment of 38-issue MUX epic
- Prioritization framework for canonical queries
- User research methodology for discovery validation
- Success criteria for moving from alpha to beta

## Attachments
- Canonical Queries v2 (63 queries categorized)
- Pattern-045 documentation
- Conversational Glue Design Brief
