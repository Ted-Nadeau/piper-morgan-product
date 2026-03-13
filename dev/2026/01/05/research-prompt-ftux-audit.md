# Research Assignment: FTUX Gap Analysis

**Requested by**: Principal Product Manager (via HOSR)
**Agent Role**: Researcher / Special Assignments (requires codebase access)
**Output Format**: Gap analysis report (Markdown)
**Estimated Scope**: Medium (2-3 hours equivalent)

---

## Objective

Compare Piper Morgan's **current first-time user experience implementation** against the **vision defined in PDR-001** and related CXO specifications. Identify gaps, assess severity, and recommend prioritization.

---

## Source Documents to Review

### Vision Documents (What We Want)
1. `PDR-001-ftux-as-first-recognition-v2.md` - Core FTUX philosophy
2. `multi-entry-ftux-exploration-v1.md` - Multi-entry point design
3. `cross-session-greeting-ux-spec-v1.md` - Return user experience
4. `empty-state-voice-guide-v1.md` - Empty state voice/tone
5. `contextual-hint-ux-spec-v1.md` - Capability discovery hints

### Implementation Reality (What We Have)
1. Current codebase: `web/` directory, particularly templates and routes
2. Current user flow: Walk through actual FTUX as a new user would experience it
3. Any existing FTUX-related issues in GitHub

---

## Analysis Framework

For each PDR-001 principle, assess:

| Principle | PDR-001 Requirement | Current State | Gap Severity | Notes |
|-----------|---------------------|---------------|--------------|-------|
| [Principle name] | [What PDR says] | [What actually happens] | Critical/Significant/Minor/Aligned | [Context] |

### Severity Definitions

- **Critical**: Principle is violated or absent; blocks B2 release
- **Significant**: Partial implementation; degrades experience noticeably
- **Minor**: Small deviation; polish item
- **Aligned**: Current state matches vision

---

## Specific Questions to Answer

1. **Entry Points**: Does current implementation support multiple entry points (web, Slack, CLI), or is it web-wizard only?

2. **Value Before Setup**: Can a new user experience Piper's value before completing full integration setup?

3. **Progressive Disclosure**: Is setup front-loaded (wizard) or progressive (as-needed)?

4. **Empty States**: Do current empty states follow the voice guide, or are they generic system messages?

5. **Cross-Session Greeting**: Does Piper recognize returning users with context-aware greetings?

6. **Integration Prompts**: When Piper needs an integration, does it follow the conversational pattern or show error messages?

7. **Capability Hints**: Are contextual hints implemented per the spec?

---

## Deliverable

### Gap Analysis Report Structure

```
# FTUX Gap Analysis Report

**Date**:
**Analyst**: [Agent identifier]
**Requested by**: PPM via HOSR

## Executive Summary
[2-3 sentences: Overall assessment, critical gaps count, readiness assessment]

## Methodology
[How analysis was conducted]

## Gap Analysis by Principle
[Table format per framework above]

## Critical Gaps (Blocking B2)
[List with details]

## Significant Gaps (Should Address)
[List with details]

## Minor Gaps (Polish)
[List with details]

## Aligned Areas (Celebrate)
[What's working well]

## Recommendations
[Prioritized list of actions]

## Open Questions
[Things that couldn't be determined, need human input]
```

---

## Constraints

- Do NOT implement fixes—this is analysis only
- Do NOT create GitHub issues—report findings for PPM/Lead Dev to triage
- Flag any areas where you cannot determine current state (need human walkthrough)
- Time-box to avoid rabbit holes; note areas needing deeper investigation

---

## Handoff

Deliver report to HOSR for review. HOSR will share with PPM.

---

*Research prompt created by HOSR | January 5, 2026*
