# Spec Session Log: Capabilities Naming Analysis

**Date**: 2026-01-12 11:58 AM
**Role**: Lead Developer (Special Assignment)
**Task**: Analyze Piper's capabilities and recommend consistent naming convention
**Context**: Alpha tester feedback - "features don't all have names"

## Objective

Inventory all capabilities, analyze naming patterns, and recommend a consistent naming convention that works for users, docs, and marketing.

## Investigation Plan

### Phase 1: Discovery
1. Examine canonical handlers for intent handling
2. Survey integrations
3. Review config documentation
4. Check alpha testing guide
5. Review release notes naming
6. Check template empty states

### Phase 2: Analysis
- Identify naming patterns in use
- Find inconsistencies
- Note overly technical names

### Phase 3: Recommendations
- Propose naming convention
- Suggest specific names
- Identify groupings

---

## Session Progress

### 11:58 AM - Session Start
- Created session log
- Beginning capability discovery

### 12:00 PM - Discovery Phase

**Sources examined:**
- `services/intent_service/canonical_handlers.py` - 90+ methods handling intents
- `services/integrations/` - 7 integrations (slack, github, notion, calendar, demo, mcp, spatial)
- `config/PIPER.md` - Official capability documentation
- `docs/ALPHA_TESTING_GUIDE.md` - User-facing feature descriptions
- `docs/releases/RELEASE-NOTES-v0.8.*.md` - How features are named in releases
- `templates/*.html` - UI naming patterns

**Capability count**: 35+ distinct capabilities identified

### 12:15 PM - Analysis Phase

**5 naming patterns identified:**
1. Product Names (e.g., "Morning Standup") - ~3 features, most effective
2. Verb-First Actions (e.g., "Create issue") - ~15 features, generic but clear
3. Question Form (e.g., "What shipped?") - ~10 features, natural
4. Technical Names (e.g., "spatial intelligence") - ~8 features, confusing to users
5. Integration Names (e.g., "GitHub integration") - ~6 features, clear source

**Key inconsistencies:**
- Same capability with multiple names
- Technical terms exposed to users
- No standard verb form (Create vs Creating vs creation)

### 12:25 PM - Recommendations

**Proposed framework:**
- Tier 1: Flagship Features → Product Names (Morning Standup, Priority Coach)
- Tier 2: Actions → Verb-Noun (Create Issue, Upload Document)
- Tier 3: Queries → Natural Questions ("What shipped?", "What's my week like?")
- Tier 4: Categories → Domain groupings (GitHub Tools, Calendar Features)

### 12:30 PM - Report Complete

**Deliverable**: `dev/2026/01/12/capabilities-naming-analysis-report.md`

### 12:07 PM - PM Feedback Incorporated

**Key guidance received:**

1. **Avoid "Coach" terminology** - too loaded, prefer "Assistant" framing
2. **Naming Tone Spectrum** - new framework addition:
   - (a) Plain natural language - "What needs attention?"
   - (b) Industry-standard jargon - "Backlog", "Sprint", "Standup"
   - (c) Unique/clever but clear - "Don't Miss"
3. **GitHub framing** - position as agile/PM tool, not coding tool → "Backlog Tools"
4. **Learning Mode** - marketing feature to promote, not UI function
5. **Open for broader review** - CXO, PPM, Comms Chief before converging
6. **Validation** - A/B testing, alpha feedback, principles before specifics

**Updated proposals:**
- Priority Coach → **Focus Assistant**
- Standup Coach → **Standup Assistant**
- GitHub Tools → **Backlog Tools** (PM-centric framing)
- Learning Mode → Marketing feature, not settings toggle

**Report updated** with Section 6: PM Feedback & Guidance

---

## Session Status: 12:15 PM

**Status**: Initial analysis complete, PM feedback incorporated

**Key Outputs:**
1. Full capability inventory (35+ items)
2. Pattern analysis (5 patterns)
3. Naming convention framework (4-tier + tone spectrum)
4. Revised name proposals (assistant framing)
5. Open questions for CXO/PPM/Comms review

**Deliverable**: `dev/2026/01/12/capabilities-naming-analysis-report.md` (updated)

**Next Steps:**
1. Share with Communications Chief for messaging alignment
2. Share with Principal Product Manager for product positioning
3. Share with Chief Experience Officer for UX consistency
4. Reconvene after broader input to finalize naming decisions
