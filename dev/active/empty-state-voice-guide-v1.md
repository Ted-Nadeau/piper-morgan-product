# Empty State Voice Guide: Piper's Tone in Oriented Empty States

**Document Type**: Voice & Tone Specification
**Author**: Chief Experience Officer
**Date**: January 4, 2026
**For**: Principal Product Manager, Lead Developer, Content/Copy Writers
**Implements**: PDR-001 requirement that "empty states are oriented, not empty"

---

## Overview

Empty states occur when a view has no content to display. Traditional apps show "No items yet" with perhaps a button to add one.

Piper's empty states are **teaching moments**. They orient users to what's possible without being a tutorial. The voice must be helpful without being condescending, inviting without being pushy.

---

## Voice Principles for Empty States

### 1. Colleague, Not System

**Don't**: "No todos found. Click 'Add Todo' to create one."
**Do**: "No todos yet. You can say 'add a todo' or I can pull from your GitHub issues—want to try?"

### 2. Show the Grammar

Empty states should demonstrate how to talk to Piper, not just what buttons to click.

**Don't**: "Your calendar is empty. [Add Event]"
**Do**: "Nothing on your calendar today. You can ask me 'what's my week look like?' or 'schedule a meeting with...' when you're ready."

### 3. One Suggestion, Not a Menu

Offer one clear path, maybe hint at a second. Don't overwhelm.

**Don't**: "No standup yet. You can: generate standup, view yesterday's standup, configure standup settings, learn about standups..."
**Do**: "No standup yet. Say 'generate my standup' when you're ready—I'll pull from your GitHub activity."

### 4. Confidence Without Pressure

Piper knows what it can do. State it simply. Don't apologize for the empty state or oversell the solution.

**Don't**: "Sorry, there's nothing here yet! But don't worry—we can fix that!"
**Do**: "Nothing here yet. Want me to help you get started?"

### 5. Contextual Awareness

If Piper knows why something is empty, say so helpfully.

**Don't**: "No GitHub issues to display."
**Do**: "No open issues assigned to you. Want to see the full repo, or create a new issue?"

---

## Empty State Templates by View

### Todos View

**State**: No todos exist

```
No todos yet.

Say "add a todo: [your task]" to create one, or I can suggest
some based on your open GitHub issues.
```

**State**: All todos completed

```
All caught up! 🎯

Your todo list is clear. Nice work.
```

---

### Standup View

**State**: No standup generated today

```
No standup yet today.

Say "generate my standup" and I'll pull from your GitHub
activity, calendar, and recent work.
```

**State**: No data sources connected

```
I'll need some context to generate a useful standup.

Connect GitHub or your calendar in Settings, then come back
and say "generate my standup."
```

---

### GitHub Issues View

**State**: No issues assigned to user

```
No issues assigned to you right now.

Want to see all open issues in the repo, or create a new one?
Just say "show all issues" or "create an issue about..."
```

**State**: GitHub not connected

```
GitHub isn't connected yet.

Once you add your GitHub token in Settings, I can help you
triage issues, track PRs, and generate release notes.
```

---

### Calendar View

**State**: No events today

```
Your calendar is clear today.

Ask me "what's my week look like?" for a broader view, or
"find time for..." if you need to schedule something.
```

**State**: Calendar not connected

```
Calendar isn't connected yet.

Connect Google Calendar in Settings and I can help you prep
for meetings, find free time, and avoid conflicts.
```

---

### Documents/Knowledge View

**State**: No documents indexed

```
No documents in your knowledge base yet.

You can upload files, connect Notion, or just paste content
into our chat—I'll remember it for later.
```

**State**: Search returned no results

```
Nothing matching "[search term]" in your docs.

Try different keywords, or ask me to search more broadly.
```

---

### Projects View

**State**: No projects created

```
No projects set up yet.

Projects help me understand your work context. Say "create a
project called..." to get started.
```

---

### Lists View

**State**: No lists created

```
No lists yet.

Say "create a list called..." to get started. Lists help you
group and organize related items.
```

---

### Slack Messages View

**State**: No relevant messages

```
No Slack messages needing your attention.

I'm watching your channels—I'll surface important threads
when they come up.
```

**State**: Slack not connected

```
Slack isn't connected yet.

Once connected, I can summarize channels, track mentions,
and help you stay on top of team conversations.
```

---

### Activity/History View

**State**: No recent activity

```
No recent activity to show.

This is where I'll track what we've worked on together.
Start a conversation and it'll populate.
```

---

## Formatting Guidelines

### Length

- **Headline**: 1 short sentence (the state)
- **Body**: 1-2 sentences (the invitation)
- **Total**: Under 40 words

### Structure

```
[What's true now - statement of state]

[What you can do - one clear suggestion]
[Optional: one alternative hint]
```

### Punctuation

- Periods at end of sentences
- No exclamation points (too eager)
- Em dashes for asides
- Question marks for genuine questions only

### Capitalization

- Sentence case throughout
- Capitalize proper nouns (GitHub, Slack, Settings)
- Don't capitalize feature names unless proper nouns

---

## Voice Calibration Examples

### Too Cold ❄️

> "No data available. Configure integrations to populate this view."

**Problem**: System-speak. No warmth, no guidance on *how*.

### Too Warm 🔥

> "Oops! Looks like there's nothing here yet! But don't worry—we can totally fix that together! 🎉"

**Problem**: Performative enthusiasm. Condescending. The emoji makes it worse.

### Just Right ✅

> "Nothing here yet. Say 'add a todo' to get started, or I can pull tasks from your GitHub issues."

**Problem**: None. States the situation, offers a clear path, hints at an alternative.

---

## Integration-Specific Messaging

When an empty state is caused by missing integration, the message should:

1. **Name the integration** specifically
2. **State what becomes possible** when connected
3. **Point to Settings** (don't deep-link, just mention)

**Template**:
```
[Integration] isn't connected yet.

[What I can do when connected - specific capabilities].
Connect it in Settings when you're ready.
```

**Example**:
```
Notion isn't connected yet.

Once connected, I can search your workspace, pull in docs,
and help you find information fast.
Connect it in Settings when you're ready.
```

---

## Error States vs. Empty States

**Empty state**: Nothing exists yet (neutral)
**Error state**: Something went wrong (needs recovery)

This guide covers empty states. Error states should:
- Acknowledge the problem simply
- Offer recovery path
- Not blame the user

**Example error state** (for reference, not this guide's scope):
```
Couldn't load your GitHub issues.

This might be a connection issue. Try refreshing, or check
your GitHub token in Settings if it keeps happening.
```

---

## Testing Empty State Copy

### The Colleague Test

Read the empty state aloud. Would a helpful colleague say this? If it sounds robotic or patronizing, revise.

### The First-Time Test

Imagine a user seeing this view for the first time. Do they know:
1. What this view is for?
2. How to populate it?
3. What to say to Piper?

### The Return-User Test

Imagine a user who cleared their todos. Does the empty state congratulate appropriately, or does it treat them like a newbie again?

---

## Summary Table

| View | Empty State Hook | Primary Invitation |
|------|------------------|-------------------|
| Todos | "No todos yet" | "Say 'add a todo: [task]'" |
| Standup | "No standup yet today" | "Say 'generate my standup'" |
| GitHub Issues | "No issues assigned" | "Say 'show all issues' or 'create an issue'" |
| Calendar | "Calendar is clear" | "Ask 'what's my week look like?'" |
| Documents | "No documents yet" | "Upload files or connect Notion" |
| Projects | "No projects set up" | "Say 'create a project called...'" |
| Lists | "No lists yet" | "Say 'create a list called...'" |
| Slack | "No messages needing attention" | (Passive—no action needed) |
| Activity | "No recent activity" | "Start a conversation" |

---

*Empty State Voice Guide v1 | January 4, 2026 | Chief Experience Officer*
