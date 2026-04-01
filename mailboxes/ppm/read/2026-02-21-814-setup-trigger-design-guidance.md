# Memo: Design Guidance Needed — #814 Setup Trigger from Natural Language

**From**: Lead Developer
**To**: CXO, PPM
**Date**: February 21, 2026
**Re**: What should happen when a user says "help me set up"?
**GitHub Issue**: #814
**Priority**: Currently listed as blocking M0 gate

---

## The Problem

When a user says "help me set up a project" or "set up my Slack", Piper returns static guidance advice instead of starting any setup flow. The patterns exist in the pre-classifier (12 regex patterns matching setup phrases), but they all route to `GUIDANCE` → static advice card.

## Key Constraint

**Users can't chat with Piper until initial setup (the 4-step wizard) is complete.** This means every "help me set up" message comes from a post-setup user. They've already completed account creation and had the opportunity to connect integrations. The conversation can't happen before the wizard.

This eliminates the ambiguity between the two setup systems:

- The **Setup Wizard** (System A: `templates/setup.html`) is pre-chat only — unreachable via conversational intent
- The **Portfolio Onboarding** (System B: `services/onboarding/`) is conversational — this is the only setup flow reachable from chat

## What "Set Up" Means in Chat Context

| User Message | What They Mean | Response |
|---|---|---|
| "Help me set up a project" | Portfolio onboarding | Trigger conversational onboarding (System B) |
| "Set up my projects" | Portfolio onboarding | Same as above |
| "Help me set up Slack" | Reconfigure/reconnect integration they skipped or want to change | Direct to settings/setup page |
| "How do I configure my calendar?" | Same — reconfiguration | Direct to settings/setup page |
| "Help me get started" | General — probably portfolio | Trigger portfolio onboarding |

## Remaining Design Questions

### 1. Scope for M0 Gate
Should this block gate closure? The current behavior (static guidance) is unhelpful but not broken. Could this be deferred to M1?

### 2. Users Who Already Have Projects
If someone says "help me set up a project" but already has projects:
- **Option A**: "Would you like to add another project to your portfolio?"
- **Option B**: Start the onboarding flow again (reconfigure)
- **Option C**: "Your portfolio has 3 projects. Would you like to review it or add more?"

### 3. Integration Reconfiguration UX
For "help me set up Slack" (post-setup), should Piper:
- **Option A**: Return a link: "You can configure Slack in your settings — [here's the link](/setup)"
- **Option B**: A softer approach: "I'd love to help with that! Slack configuration happens in the setup page. Want me to open it for you?"

Both pass the Colleague Test — a human colleague would say "sure, let me pull up the settings page."

## Lead Developer Recommendation

This is a small routing fix (~30 lines) once the product decisions above are made:
1. **Portfolio "set up"** → trigger conversational onboarding (System B) with existing-project awareness
2. **Integration "set up"** → warm redirect to setup page
3. **"Get started"** → portfolio onboarding

If scope question is answered with "defer to M1", that immediately clears the M0 gate.

---

*Lead Developer, M0 Sprint*
