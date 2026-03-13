# Agent Prompt: Capabilities Naming Analysis

**Date**: January 12, 2026
**Requested by**: PM (xian)
**Purpose**: Deep dive into Piper's capabilities, their current working titles, and recommendations for consistent naming
**Context**: Alpha tester feedback (Ted) noted that "features don't all have names" and suggested normalizing the capabilities list

---

## Background

Piper Morgan has accumulated many capabilities over development, but they lack consistent naming:
- Some have official names (e.g., "Morning Standup", "Interactive Standup Assistant")
- Some are described by what they do (e.g., "document analysis", "GitHub issue creation")
- Some are referenced by technical names (e.g., "spatial intelligence", "preference learning")

This inconsistency affects:
1. **User communication**: Release notes, onboarding, help text
2. **Marketing**: How we describe Piper externally
3. **Internal clarity**: How the team talks about features

---

## Your Task

### Phase 1: Discovery

1. **Inventory all capabilities** by examining:
   - `services/intent_service/canonical_handlers.py` - What intents are handled?
   - `services/integrations/*/` - What integrations exist?
   - `config/PIPER.md` - What capabilities are documented?
   - `docs/ALPHA_TESTING_GUIDE.md` - How are features described to testers?
   - `docs/releases/*.md` - How are features named in release notes?
   - Empty state copy in `templates/*.html` - How are capabilities referenced?

2. **For each capability, note**:
   - Current name(s) used (may have multiple)
   - Technical/internal name (code references)
   - Brief description of what it does
   - Which integration(s) it uses (if any)

### Phase 2: Analysis

1. **Identify naming patterns** currently in use:
   - Verb-first ("Generate standup", "Create issue")
   - Noun-first ("Standup generation", "Issue creation")
   - Feature names ("Morning Standup", "Spatial Intelligence")
   - Integration names ("GitHub integration", "Slack commands")

2. **Identify inconsistencies**:
   - Same capability with different names
   - Similar capabilities with very different naming styles
   - Overly technical names exposed to users
   - Vague or unclear names

### Phase 3: Recommendations

1. **Propose a naming convention** that:
   - Is user-friendly (product managers are primary audience)
   - Is consistent across similar capabilities
   - Works in multiple contexts (UI, docs, marketing)
   - Scales as we add more capabilities

2. **Suggest specific names** for each capability, with rationale

3. **Identify any capabilities that might benefit from**:
   - A proper product name (like "Morning Standup")
   - Grouping under a category
   - Renaming for clarity

---

## Deliverables

Create a report at `dev/2026/01/12/capabilities-naming-analysis-report.md` with:

1. **Capability Inventory Table**
   | Capability | Current Names | Technical Reference | Description | Integrations |
   |------------|---------------|---------------------|-------------|--------------|

2. **Pattern Analysis** - What naming patterns exist, which work, which don't

3. **Recommended Naming Convention** - Rules for naming capabilities consistently

4. **Proposed Names** - New/updated names for each capability with rationale

5. **Questions for PM** - Any decisions that need human input

---

## Stakeholder Review Path

After this analysis:
1. PM reviews and provides feedback
2. Share with Communications Chief for messaging alignment
3. Share with Principal Product Manager for product positioning
4. Share with Chief Experience Officer for UX consistency

---

## Success Criteria

- Complete inventory of all user-facing capabilities
- Clear naming convention that can guide future features
- Specific recommendations that can be implemented in v0.8.4 or later
- Alignment with Piper's voice (professional, friendly, PM-focused)

---

*This prompt created as part of v0.8.4 release preparation based on alpha tester feedback.*
