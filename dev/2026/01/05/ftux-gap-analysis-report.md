# FTUX Gap Analysis Report

**Date**: January 5, 2026
**Analyst**: Special Assignments Agent (spec-code-opus)
**Requested by**: Principal Product Manager via HOSR

---

## Executive Summary

Piper Morgan's current FTUX implementation has **strong technical foundations** (setup wizard, personality system, intent routing) but **significant gaps** against PDR-001's vision. The current experience is a traditional web wizard followed by generic empty states—not the conversational, recognition-pattern experience PDR-001 envisions.

**Critical Gaps**: 3 (blocking B1 conversational quality)
**Significant Gaps**: 5 (degrade experience noticeably)
**Minor Gaps**: 3 (polish items)
**Aligned Areas**: 3 (foundations in place)

**B1 Readiness Assessment**: NOT READY. Current FTUX does not meet B1 quality rubric for "conversational naturalness." The experience teaches setup mechanics, not how to work with Piper.

---

## Methodology

### Source Documents Reviewed

**Vision Documents**:
1. PDR-001-ftux-as-first-recognition-v3.md - Core FTUX philosophy (7 principles)
2. multi-entry-ftux-exploration-v1.md - Multi-entry point design
3. cross-session-greeting-ux-spec-v1.md - Return user experience (6 scenarios)
4. empty-state-voice-guide-v1.md - Empty state voice/tone (8 view templates)
5. contextual-hint-ux-spec-v1.md - Capability discovery hints (8 hint types)
6. B1-quality-rubric-v1.md - B1 quality gate criteria

**Implementation Analyzed**:
- Templates: setup.html, home.html, todos.html, projects.html, files.html, lists.html
- Components: empty-state.html, preference_suggestion.html
- Routes: web/api/routes/setup.py, intent.py, ui.py
- Services: intent_service/canonical_handlers.py, pre_classifier.py, prompts.py
- Static: web/static/js/setup.js

**GitHub Issues**: Searched for FTUX-related items (B1 sprint)

---

## Gap Analysis by PDR-001 Principle

| Principle | PDR-001 Requirement | Current State | Gap Severity | Notes |
|-----------|---------------------|---------------|--------------|-------|
| **1. Piper speaks first** | First screen shows Piper orienting, not a form | Setup wizard: "Step 1 of 4: System Requirements" | **Critical** | User sees technical checklist before meeting Piper |
| **2. Configuration is conversational** | Setup happens as dialogue with Piper | Traditional 4-step wizard with forms, validation, buttons | **Critical** | Zero conversational elements in setup |
| **3. Multiple entry points** | Web/Slack/CLI all valid starting points | Web wizard only; Slack/CLI require separate setup | **Significant** | No unified entry point experience |
| **4. Progressive reveal** | Features introduced as relevant | All setup front-loaded; features not introduced post-setup | **Significant** | No "Now that X is connected, I can..." moments |
| **5. Empty states are oriented** | Piper explains what's possible, offers guidance | Generic: "No todos yet. Create your first todo" | **Critical** | No Piper voice, no capability hints |
| **6. Onboarding IS the primer** | Preferences questionnaire teaches interaction model | Preferences questionnaire exists but disconnected from FTUX | **Significant** | User completes setup → lands on empty home, no questionnaire flow |
| **7. User can personalize** | Name preferences, communication style | Personality settings exist in /personality-preferences | Minor | Feature exists but not introduced during FTUX |

---

## Critical Gaps (Blocking B1)

### Gap 1: Setup is Form-First, Not Recognition-First

**PDR-001 Vision**:
> "Hi, I'm Piper. I'm here to help you with product management work. Let me help you get set up—I'll need a few things to connect to your tools."

**Current Reality** (templates/setup.html):
```
Step 1 of 4: System Requirements
✓ Docker running ● PostgreSQL ● Redis ● ChromaDB
```

**Impact**: User's first experience is a system health check, not meeting Piper. This violates the core premise that "first contact is first recognition."

**Evidence**: setup.html lines 1-50 show a wizard structure with progress indicators (step 1/2/3/4), not a conversational interface.

**B1 Rubric Violation**: Fails "Voice Consistency" (2.0 required) - setup has no Piper voice at all.

---

### Gap 2: No Conversational Configuration

**PDR-001 Vision**:
> "Rather than a multi-step form, Piper asks for what it needs in dialogue."

**Current Reality** (web/api/routes/setup.py):
- `/setup/validate-key` - Form-based API key validation
- `/setup/create-user` - Standard registration form
- `/setup/complete` - POST completion endpoint

All configuration is form→button→validate→next pattern with zero conversational wrapper.

**Impact**: Users learn "fill forms" not "talk to Piper" as the interaction model.

**Evidence**: setup.js shows standard form validation, no chat interface integration.

**B1 Rubric Violation**: Fails "Flow" (2.0 required) - experience is navigational, not conversational.

---

### Gap 3: Empty States Are Generic System Messages

**PDR-001 Vision** (from empty-state-voice-guide-v1.md):
> "No todos yet. Say 'add a todo: [your task]' to create one, or I can suggest some based on your open GitHub issues."

**Current Reality** (templates/todos.html):
```javascript
container.innerHTML = `
  <div class="empty-state">
    <h3>No todos yet</h3>
    <p>Create your first todo to get started</p>
  </div>
`;
```

Similar generic patterns in projects.html, files.html, lists.html.

**Impact**: After setup, users land in empty views with no guidance on how to interact with Piper. The promised "oriented empty states" are entirely absent.

**Evidence**: grep across templates shows no empty state matches the voice guide templates.

**B1 Rubric Violation**: Fails "Discovery" (2.0 required) - empty states don't demonstrate capability.

---

## Significant Gaps (Should Address for B1)

### Gap 4: No Multi-Entry Point Support

**PDR-001 Vision** (from multi-entry-ftux-exploration-v1.md):
> "Users should be able to engage from multiple directions... Web, Slack, CLI entry points all lead to same Piper"

**Current Reality**:
- Web: Full setup wizard
- Slack: Requires separate OAuth (no FTUX flow)
- CLI: `python main.py setup` runs different wizard (scripts/setup_wizard.py)

Each entry point has a completely different experience. There's no "same Piper, same context" as envisioned.

**Evidence**: CLI setup_wizard.py is 1,450 lines of terminal-based setup, completely separate from web.

---

### Gap 5: No Cross-Session Greeting Implementation

**PDR-001 Vision** (from cross-session-greeting-ux-spec-v1.md):
6 greeting scenarios (A-F) based on:
- Recency (same day, next day, week+, month+)
- Emotional context (frustration detection)
- Session substance (trivial vs. meaningful)

**Current Reality** (templates/home.html):
```javascript
const hour = new Date().getHours();
if (hour >= 12 && hour < 18) timeGreeting = "Good afternoon"
else if (hour >= 18) timeGreeting = "Good evening"
```

Time-of-day greeting only. No session history awareness, no context awareness, no emotional context detection.

**Evidence**: No UserContextService implementation for session history. No frustration signal detection.

---

### Gap 6: No Contextual Capability Hints

**PDR-001 Vision** (from contextual-hint-ux-spec-v1.md):
> "After successful task completion, Piper may offer one related capability"

8 hint types defined with throttling rules:
- Max 2 suggestions per 5 interactions
- Stop after 2 ignored suggestions

**Current Reality**:
Capability hints exist ONLY in GUIDANCE responses when user explicitly asks for focus recommendations:
```python
if recommendation["missing_integrations"]:
    suggestion = "Tip: Connect your calendar..."
```

No post-action hints. No contextual discovery. No hint throttling system.

**Evidence**: No hint_count tracking in session state. No UI component for hints below responses.

---

### Gap 7: Preferences Questionnaire Not Integrated into FTUX

**PDR-001 Vision**:
> "The preferences questionnaire itself becomes the conversation primer... users learn the interaction model while providing information"

**Current Reality**:
- Preferences questionnaire exists (`scripts/preferences_questionnaire.py`)
- Personality settings page exists (`/personality-preferences`)
- But neither is part of FTUX flow

User completes setup → lands on home page → never sees questionnaire unless they navigate to Settings.

**Evidence**: setup.py completion flow redirects to `/login`, not to questionnaire or orientation.

---

### Gap 8: No Integration Prompt Pattern in UI

**PDR-001 Vision** (from multi-entry-ftux-exploration-v1.md):
> When Piper needs an integration: "I'd need GitHub access to [specific thing]. → Connect GitHub (takes ~30 sec)"

**Current Reality**:
- Backend has integration detection in GUIDANCE handler
- But UI shows no conversational prompts when features need missing integrations
- Error states are silent or generic ("Calendar not connected")

**Evidence**: Empty state templates don't follow the Integration Prompt Pattern from multi-entry spec.

---

## Minor Gaps (Polish)

### Gap 9: No Post-Setup Orientation

After setup completes, user lands on home page with no "What's next?" guidance. The transition from setup to usage is abrupt.

**Recommendation**: Add brief "Here's what you can do now" message after setup completion.

---

### Gap 10: Trust Stage Not Displayed or Tracked

PDR-001 defines 4 trust stages. Current implementation doesn't:
- Display current trust level to user
- Track trust progression
- Modify behavior based on trust stage

**Evidence**: No trust_stage field in user model or session state.

---

### Gap 11: No User Rename Capability

PDR-001 v3 notes:
> "Users should be able to rename Piper if desired"

This is marked as a new feature request in PDR-001, not blocking.

---

## Aligned Areas (Celebrate)

### Aligned 1: Personality System Infrastructure

The 4-dimension personality system is fully implemented:
- Warmth Level (0.0-1.0)
- Confidence Style (numeric/descriptive/contextual/hidden)
- Action Orientation (high/medium/low)
- Technical Depth (detailed/balanced/simplified)

Web UI at `/personality-preferences` is polished and functional.

**Evidence**: personality-preferences.html (678 lines), personality.py routes, preference detection service (37 tests passing)

---

### Aligned 2: Integration OAuth Flows

Slack and Calendar OAuth work well:
- Setup wizard has OAuth buttons
- Settings pages have connect/disconnect flows
- Health monitoring shows integration status

**Evidence**: settings_integrations.py, settings_slack.html, settings_calendar.html all functional

---

### Aligned 3: Reusable Empty State Component

The empty-state.html component exists and is WCAG 2.2 AA accessible:
```html
<!-- Template with variables: icon, title, message, cta_text, cta_url -->
```

The infrastructure is there—just needs Piper voice content.

---

## Recommendations (Prioritized)

### P0 - Must Fix for B1

1. **Add Piper introduction to setup start**
   - Before Step 1, show Piper greeting: "Hi, I'm Piper..."
   - Simple text banner, doesn't require full conversational redesign
   - Effort: Small (1-2 hours)

2. **Replace empty state copy with voice guide templates**
   - Update todos.html, projects.html, files.html, lists.html
   - Use exact templates from empty-state-voice-guide-v1.md
   - Effort: Small (2-3 hours)

3. **Add post-setup orientation**
   - After setup completion, show "Here's how to start working with me"
   - Single modal/page with 3 suggested starting points
   - Effort: Small (2-3 hours)

### P1 - Should Fix for B1

4. **Implement basic cross-session greeting**
   - Start with scenarios A, B, F only (same day, next day, trivial)
   - Defer emotional context detection to post-B1
   - Effort: Medium (1-2 days)

5. **Add capability hints to response UI**
   - Implement hint container component per contextual-hint-ux-spec
   - Start with 2-3 hints only (standup_to_slack, issue_to_project)
   - Effort: Medium (1-2 days)

6. **Add preferences questionnaire to FTUX flow**
   - After setup complete, before home page
   - Frame as "Help me understand how you like to work"
   - Effort: Small-Medium (3-4 hours)

### P2 - Post-B1

7. **Multi-entry point unification** - Larger architectural work
8. **Trust stage tracking** - Requires UserContextService
9. **Full conversational setup** - Major redesign
10. **Frustration signal detection** - ML/heuristics work

---

## Open Questions (Requiring Human Input)

1. **B1/B1 Terminology**: Documents reference both "B1" and "B1" sprints. B1 issues link to GitHub. Is B1 the current target? Clarification on naming would help align priorities.

2. **CLI vs Web Priority**: Should CLI FTUX be unified with web, or is web-first acceptable for B1?

3. **Voice Guide Emoji Usage**: Empty state voice guide uses one emoji ("All caught up! 🎯"). Should Piper use emojis in empty states?

4. **Questionnaire Integration**: Should questionnaire be mandatory or skippable during FTUX?

5. **Current Empty State Component**: The templates/components/empty-state.html exists but isn't being used. Should we retrofit existing views to use it, or update inline HTML?

---

## Appendix: B1 Quality Rubric Mapping

| Dimension | Score Required | Current State | Assessment |
|-----------|---------------|---------------|------------|
| **Flow** | 2.0 | Setup is wizard, not conversation | FAIL |
| **Discovery** | 2.0 | Empty states generic, no hints | FAIL |
| **Proactivity Balance** | 1.5+ | Reactive only, no capability hints | FAIL |
| **Recovery** | 1.5+ | Basic error handling, no dead-end recovery | PARTIAL |
| **Voice Consistency** | 2.0 | Setup has no Piper voice | FAIL |

**B1 Gate Assessment**: 4 of 5 dimensions fail minimum threshold.

---

*Report prepared for HOSR review. HOSR will share with PPM for triage.*

---

*FTUX Gap Analysis Report | January 5, 2026 | Special Assignments Agent*
