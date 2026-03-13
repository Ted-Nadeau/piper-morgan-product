# B1 Quick Win Issues - Ready for GitHub Creation

*Drafted by Chief Architect, January 5, 2026*

---

## Issue 1: FTUX-PIPER-INTRO

### Title
FTUX-PIPER-INTRO: Add Piper greeting to setup wizard start

### Labels
- `priority: high`
- `component: ui`
- `type: enhancement`
- `sprint: B1`

### Description

**Problem**
The setup wizard currently shows "Step 1 of 4: System Requirements" as the first thing users see. Per PDR-001, first contact should be first recognition - users should meet Piper before seeing a system checklist.

**Gap Analysis Reference**: Gap 1 (Critical) - Setup is Form-First, Not Recognition-First

**Solution**
Add a Piper introduction panel before Step 1 that:
- Introduces Piper with personality
- Sets expectations for what setup will accomplish
- Creates conversational framing for the technical steps that follow

### Acceptance Criteria

- [ ] User sees Piper greeting before Step 1 system requirements
- [ ] Greeting follows voice guide tone (colleague, not system)
- [ ] Single "Let's get started" CTA to proceed to Step 1
- [ ] No new navigation step (overlay or panel, not new wizard step)
- [ ] Mobile responsive

### Proposed Copy

```
Hi, I'm Piper! 👋

I'm here to help you with product management work—tracking tasks,
managing GitHub issues, prepping for standups, and staying on top
of your calendar.

Let me help you get set up. I'll need to check a few things and
connect to your tools.

[Let's get started →]
```

### Implementation Notes

- Modify `templates/setup.html` to show intro panel on first load
- Store "intro seen" in sessionStorage to not re-show on refresh
- Estimated effort: 1-2 hours

### References

- PDR-001: First Contact is First Recognition (Principle 1: "Piper speaks first")
- FTUX Gap Analysis Report (January 5, 2026)
- empty-state-voice-guide-v1.md (tone reference)

---

## Issue 2: FTUX-EMPTY-STATES

### Title
FTUX-EMPTY-STATES: Replace empty state copy with voice guide templates

### Labels
- `priority: high`
- `component: ui`
- `type: enhancement`
- `sprint: B1`

### Description

**Problem**
Current empty states use generic system messages like "No todos yet. Create your first todo to get started." Per PDR-001, empty states should be oriented - teaching users how to interact with Piper, not just showing buttons.

**Gap Analysis Reference**: Gap 3 (Critical) - Empty States Are Generic System Messages

**Solution**
Replace empty state copy in all primary views with templates from `empty-state-voice-guide-v1.md`.

### Acceptance Criteria

- [ ] Todos view: Updated per voice guide template
- [ ] Projects view: Updated per voice guide template
- [ ] Files/Documents view: Updated per voice guide template
- [ ] Lists view: Updated per voice guide template
- [ ] Copy demonstrates Piper grammar (e.g., "Say 'add a todo: [task]'")
- [ ] Tone is colleague, not system (no "Click button to...")

### Copy Templates (from Voice Guide)

**Todos (empty)**:
```
No todos yet.

Say "add a todo: [your task]" to create one, or I can suggest
some based on your open GitHub issues.
```

**Todos (all complete)**:
```
All caught up! 🎯

Your todo list is clear. Nice work.
```

**Projects (empty)**:
```
No projects set up yet.

Projects help me understand your work context. Say "create a
project called..." to get started.
```

**Files/Documents (empty)**:
```
No documents in your knowledge base yet.

You can upload files, connect Notion, or just paste content
into our chat—I'll remember it for later.
```

### Implementation Notes

- Update `templates/todos.html`, `projects.html`, `files.html`, `lists.html`
- Consider using `templates/components/empty-state.html` component (exists but unused)
- Estimated effort: 2-3 hours

### References

- PDR-001: First Contact is First Recognition (Principle 5: "Empty states are oriented")
- empty-state-voice-guide-v1.md (authoritative copy source)
- FTUX Gap Analysis Report (January 5, 2026)

---

## Issue 3: FTUX-POST-SETUP

### Title
FTUX-POST-SETUP: Add post-setup orientation

### Labels
- `priority: high`
- `component: ui`
- `type: enhancement`
- `sprint: B1`

### Description

**Problem**
After completing the setup wizard, users are redirected to `/login` and then land on an empty home page with no guidance. The transition from setup to usage is abrupt.

**Gap Analysis Reference**: Gap 9 (Minor) - No Post-Setup Orientation

**Solution**
Add a brief orientation after setup completion that:
- Celebrates successful setup
- Suggests 2-3 starting points based on what was configured
- Creates a bridge from "setup complete" to "here's how to work with me"

### Acceptance Criteria

- [ ] User sees orientation after first successful login post-setup
- [ ] Orientation shows 2-3 contextual starting suggestions
- [ ] Suggestions are based on connected integrations
- [ ] Single dismissal takes user to home (not shown again)
- [ ] Can be skipped/dismissed immediately
- [ ] Mobile responsive

### Proposed Copy

```
You're all set! 🎉

Here are some things we can do together:

[If GitHub connected]
📋 "Show me my open issues" - See what needs attention

[If Calendar connected]
📅 "What's on my calendar today?" - Check your schedule

[Always available]
✅ "Add a todo: [task]" - Start tracking work

[Get started →]
```

### Implementation Notes

- Could be modal overlay on home page or dedicated `/welcome` route
- Check `user.setup_complete` + `user.orientation_seen` flags
- Store "orientation seen" in user preferences (persistent, not session)
- Estimated effort: 2-3 hours

### References

- PDR-001: First Contact is First Recognition
- multi-entry-ftux-exploration-v1.md (entry point patterns)
- FTUX Gap Analysis Report (January 5, 2026)

---

## Summary

| Issue | Title | Effort | B1 Priority |
|-------|-------|--------|-------------|
| FTUX-PIPER-INTRO | Add Piper greeting to setup | 1-2 hours | P0 |
| FTUX-EMPTY-STATES | Replace empty state copy | 2-3 hours | P0 |
| FTUX-POST-SETUP | Add post-setup orientation | 2-3 hours | P0 |

**Total additional B1 effort**: ~7 hours

**Impact**: Addresses 2 Critical gaps and 1 Minor gap from FTUX Gap Analysis. Raises B1 Quality Rubric floor significantly with minimal effort.

---

*Ready for GitHub creation. PM to assign issue numbers.*
