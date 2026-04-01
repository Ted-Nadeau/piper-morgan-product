# Memo: Regressions Found During Post-M0 CXO Review

**From**: CXO
**To**: Lead Developer
**Date**: February 21, 2026, 2:08 PM
**Re**: Two regressions discovered during live testing — please investigate and log issues
**Priority**: High

---

## Context

During the Post-M0 Vision Survival Assessment, PM and CXO conducted live testing with a fresh alpha account (username: `onemvp`). Two regressions were discovered that are **not M0 feature issues** but infrastructure problems that affect the testing environment.

We are continuing M0 feature testing on a different account, but these need investigation.

---

## Regression 1: Calendar Settings Showing Connected for New Account

**Observed behavior**:
- Fresh alpha account created
- User navigated to Settings to connect calendar
- Settings page showed calendar as *already connected*
- This is a new account — no calendar should be connected

**Expected behavior**:
- New account should show no integrations connected
- User should be prompted to connect calendar

**Potential causes**:
1. **Multi-tenancy / session isolation bug** — Server returning wrong user's data (echoes Feb 6 cross-user session bleed)
2. **Client-side state pollution** — localStorage/sessionStorage leaking across accounts in same browser
3. **Default configuration bug** — New accounts inheriting configuration from somewhere

**Diagnostic suggestion**:
- Test in incognito window with fresh account
- If still shows connected → server-side bug
- If clean → client-side state pollution

**Related history**: Cross-user session bleed was fixed in v0.8.5.2 (Feb 6). This may be a regression of that fix or a related but distinct issue.

---

## Regression 2: Conversation Not Appearing in History Sidebar

**Observed behavior**:
- User started new conversation from main chat screen
- Had multi-turn exchange with Piper (portfolio onboarding, ~8 turns)
- Navigated away from chat (to Settings, then back to main screen)
- History sidebar showed "No conversations yet. Start a new chat!"
- Page refresh did not fix — conversation still missing
- Starting a *new* chat caused only that new chat to appear in sidebar

**Expected behavior**:
- Conversations should appear in sidebar immediately or on refresh
- Previous conversation should be accessible

**Potential causes**:
1. **Conversation not persisted** — Database write failing silently
2. **Sidebar not refreshing** — UI state not updating
3. **User/conversation association bug** — Conversation created but not linked to user
4. **Filtering bug** — Conversation exists but filtered out incorrectly

**Diagnostic suggestion**:
- Check database: Does conversation exist? Is it linked to correct user_id?
- Check API response: What does `/api/conversations` return for this user?

**Related history**: History Sidebar was worked on Feb 6-8, including search, monthly grouping, and localStorage clear on logout. This may be related.

---

## Action Requested

1. **Create GitHub issues** for both regressions
2. **Initial triage** — Determine severity and root cause category
3. **Advise** — Are these blocking for alpha testing, or can we work around?

We are continuing M0 feature testing on PM's established alpha account (with working calendar and history). These bugs don't block that, but they would block any new user onboarding.

---

## Additional Finding (Not a Regression)

During testing, we also found an **M0-related issue**:

**"Information Flows Forward" violation in portfolio onboarding**:
- User said: "Yes, I have another one called Dynamic Atlas."
- Piper responded: "Sure! What other project would you like to tell me about?"
- User had to repeat the project name

This is a slot-filling extraction bug — the name embedded in a sentence wasn't parsed. PM may log this separately or include in your investigation queue.

---

*CXO Post-M0 Review — Live Testing Session*
