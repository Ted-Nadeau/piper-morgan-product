# Verification Gameplan: #843-846 (B2 Test Session Bugs)

## Premise

These four bugs were filed from the CXO Post-M0 Vision Survival Assessment (Feb 22).
No commit directly targets any of them. Recent work (#838 formality, #849 keychain scoping,
#824 accept/decline cycle) *might* have incidentally improved some, but we should not assume.

**Approach**: Investigate each from first principles. For each bug:
1. Trace the code path the failing input takes
2. Identify where and why it fails
3. Determine if recent changes actually fix it
4. If not fixed: identify the minimal fix and implement it

This is investigation, not confirmation.

---

## Bug #843: Calendar queries fail silently

**Symptom**: "What's on my calendar tomorrow?" → "I wasn't able to check on your calendar right now"
**Possible root causes** (ordered by likelihood):
1. Keychain retrieval fails silently → #849 may fix this (user-scoped keys now correct)
2. Calendar router not receiving user_id → #849 Category A fixed this
3. MCP adapter connection/invocation failure → unrelated to any fix
4. Intent routing not reaching calendar handler at all → unrelated

**Verification steps**:
- [ ] Trace intent classification for "What's on my calendar tomorrow?" through pre_classifier
- [ ] Check if calendar intent routes to the correct handler
- [ ] Read calendar handler code to verify it calls keychain with username param (post-#849)
- [ ] Check if MCP adapter receives and uses user_id
- [ ] Check error handling — is the "I wasn't able to check" message the catch-all?

---

## Bug #844: Soft invocation not triggering for implied needs

**Symptom**: "I really need to get the team aligned on our Q3 planning process" → generic guidance
**Possible root causes**:
1. SoftInvocationDetector patterns don't cover "implied need" expressions
2. Detection happens but confidence is below threshold
3. Formality framework (#838) changed thresholds
4. Result not surfaced in response even if detected

**Verification steps**:
- [ ] Read SoftInvocationDetector trigger patterns — does "I really need to" match anything?
- [ ] Read detection threshold logic — what's the minimum confidence?
- [ ] Check if formality framework changes affect detection sensitivity
- [ ] Trace what happens when detect() returns low/no confidence
- [ ] If patterns are the gap: this overlaps with #850 (GLUE-SOFTINVOKE coverage)

---

## Bug #845: "Open issues" classified as projects domain

**Symptom**: "How many open issues do I have?" → returns project information
**Possible root causes**:
1. Pre-classifier maps "issues" to portfolio/projects domain
2. No "issues" or "github" intent pattern exists
3. "issues" keyword collides with "projects" patterns (both are work-related)
4. Intent fallback defaults to projects for work-related queries

**Verification steps**:
- [ ] Read pre_classifier patterns — what does "issues" match?
- [ ] Check if a github_issues intent exists at all
- [ ] Check intent routing — where does the classified intent go?
- [ ] If no issues pattern: this overlaps with #851 (INTENT-COVERAGE)

---

## Bug #846: "Yes" interpreted as greeting

**Symptom**: After Piper offers help, user says "yes" → "I'm doing well, thanks for asking!"
**Possible root causes**:
1. "yes" classified as greeting by pre-classifier (no context awareness)
2. Pending offer state not checked before classification
3. Accept/decline cycle (#824) doesn't intercept early enough
4. ConversationContext doesn't track the last offer → #852 filed for this

**Verification steps**:
- [ ] Read pre_classifier — does it classify "yes" as greeting?
- [ ] Read accept/decline detection — does detect_offer_response() get called?
- [ ] Check the order of operations in intent_service — does offer detection run before classification?
- [ ] Check if the #824 accept/decline cycle actually intercepts bare "yes"
- [ ] If not: this is exactly what #852 (CONV-CONTEXT-OFFER) is designed to fix

---

## Execution Plan

**Phase 1: Code Path Tracing** (all 4 bugs, parallel investigation)
- Read pre_classifier, intent_service, and relevant handlers
- Map the exact code path for each failing input
- Determine which root cause applies

**Phase 2: Assessment**
- For each bug: is it fixed by recent work, fixable now, or needs a new issue?
- Present findings to PM before implementing

**Phase 3: Implementation** (only after Phase 2 assessment)
- Fix bugs that are fixable within current scope
- Note which bugs are actually #850/#851/#852 in disguise

---

## Anti-Confirmation-Bias Checks

- Do NOT assume a bug is fixed because a related commit exists
- If a code path "looks like it should work," verify with an actual trace
- If a pattern "looks like it covers" the input, check the regex/matching logic
- Report "still broken" findings honestly — these inform PM's testing priorities
