# Grammar Audit: #639 Setup Template (setup.html)

## Issue Guidelines (from #639)
- Voice: "Confident, welcoming, competent. Like a new colleague showing you around on your first day."
- Avoid: "just" minimizers, exclamation overuse, "Easy!", "Yay!", overpromising
- Good: "Hi, I'm Piper Morgan. Let's get you set up."
- Bad: "Hi! I'm Piper Morgan, your AI PM assistant! I'm SO excited to work with you!"

## Contractor Test
"Would a competent contractor you hired talk this way?"

---

## Copy Inventory

### Header Section (lines 318-322)

| Line | Current | Issue | Action |
|------|---------|-------|--------|
| 320 | `Welcome to Piper Morgan` | OK | Keep |
| 321 | `Let's get you set up in just a few steps` | Uses "just" minimizer | Transform |

### Piper Introduction Panel (lines 325-343)

| Line | Current | Issue | Action |
|------|---------|-------|--------|
| 328 | `Hi, I'm Piper Morgan, your PM assistant! You can call me Piper.` | Exclamation, chatty | Transform |
| 330-333 | `I'm here to help you with product management work—tracking tasks...` | OK but chatty | Light transform |
| 335-337 | `Let me help you get set up. I'll need to check a few things...` | OK | Keep |
| 340 | `Let's get started` | OK | Keep |

### Step 1: System Requirements (lines 354-360)

| Line | Current | Issue | Action |
|------|---------|-------|--------|
| 355 | `System Requirements` | OK | Keep |
| 356 | `Click the button below to verify all required services are running.` | Mechanical instruction | Transform |
| 358 | `Check System` button | OK | Keep |
| 359 | `Continue` button | OK | Keep |

### Step 2: API Keys (lines 363-493)

| Line | Current | Issue | Action |
|------|---------|-------|--------|
| 364 | `API Keys` | OK | Keep |
| 365 | `Enter your API keys to enable AI features.` | Mechanical | Transform |
| 368 | `OpenAI API Key (required for alpha)` | OK - technical label | Keep |
| 378 | `Anthropic API Key (optional)` | OK | Keep |
| 388 | `Google Gemini API Key (optional)` | OK | Keep |
| 398 | `Notion API Key (optional)` | OK | Keep |
| 411 | `Slack Integration (optional)` | OK | Keep |
| 415 | `Configure Slack App` | OK | Keep |
| 416-419 | Help text for Slack | OK - instructional | Keep |
| 435 | `Connect your Slack workspace to enable messaging` | OK | Keep |
| 453 | `Google Calendar (optional)` | OK | Keep |
| 457 | `Configure Google Calendar App` | OK | Keep |
| 458-461 | Help text for Calendar | OK - instructional | Keep |
| 477 | `Connect your Google Calendar for scheduling awareness` | OK | Keep |

### Step 3: Account Creation (lines 496-517)

| Line | Current | Issue | Action |
|------|---------|-------|--------|
| 497 | `Create Your Account` | OK | Keep |
| 510 | `At least 8 characters` | OK - validation hint | Keep |
| 516 | `Create Account` button | OK | Keep |

### Step 4: Complete (lines 520-525)

| Line | Current | Issue | Action |
|------|---------|-------|--------|
| 522 | `Setup Complete!` | Exclamation | Transform |
| 523 | `Your Piper Morgan is ready to use.` | "Your Piper Morgan" sounds odd | Transform |
| 524 | `Log In` button | OK | Keep |

---

## Transformation Plan

### Items to Transform (6 total)

1. **Line 321**: `Let's get you set up in just a few steps`
   - Issue: "just" minimizer
   - Target: `Let's get you set up.`

2. **Line 328**: `Hi, I'm Piper Morgan, your PM assistant! You can call me Piper.`
   - Issue: Exclamation, chatty "You can call me Piper"
   - Target: `Hi, I'm Piper Morgan. I'll be helping you with project management.`

3. **Lines 330-333**: Description paragraph
   - Issue: Overly detailed for intro
   - Target: Keep but streamline to match colleague tone

4. **Line 356**: `Click the button below to verify all required services are running.`
   - Issue: Mechanical instruction
   - Target: `Let's make sure everything's ready to go.`

5. **Line 365**: `Enter your API keys to enable AI features.`
   - Issue: Mechanical
   - Target: `I'll need API keys to connect to your AI services.`

6. **Lines 522-523**: Completion message
   - Issue: Exclamation, "Your Piper Morgan" awkward
   - Target: `Setup Complete` / `You're all set. Piper is ready to help.`

---

## Summary

- **Total copy items reviewed**: 25+
- **Items needing transformation**: 6
- **Items OK as-is**: ~20
- **Approach**: In-place edits to setup.html
