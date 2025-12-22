# Screenshot Capture Checklist for Alpha Onboarding Docs

**Created**: December 11, 2025
**For**: v0.8.2 Alpha Documentation Update
**Purpose**: Capture GUI setup wizard screenshots for ALPHA_QUICKSTART.md and ALPHA_TESTING_GUIDE.md

---

## Overview

The updated Alpha documentation now includes placeholders for 5 screenshots showing the GUI setup wizard flow. These screenshots need to be captured and saved to `docs/assets/images/alpha-onboarding/`.

**Target Resolution**: 1200px width minimum (for clarity in documentation)
**Format**: PNG (for crisp UI elements and text)
**Naming Convention**: Lowercase, hyphen-separated (already defined in docs)

---

## Screenshot Checklist

### 1. Setup Wizard - Welcome Screen

**Filename**: `setup-wizard-welcome.png`
**Location**: Save to `docs/assets/images/alpha-onboarding/`

**How to Capture**:
1. Start fresh: Ensure no existing setup completed
2. Run: `python main.py`
3. Browser should open to: `http://localhost:8001/setup`
4. Capture: The welcome/landing screen of the setup wizard

**What to Show**:
- [ ] Piper Morgan branding/logo
- [ ] "Welcome" or "Get Started" heading
- [ ] Brief explanation of what setup will configure
- [ ] Clear "Get Started" or "Begin Setup" button
- [ ] Multi-step indicator (if visible)
- [ ] Professional, clean interface

**Notes**: This is the first screen users see. Should convey clarity and simplicity.

---

### 2. Setup Wizard - System Health Check

**Filename**: `setup-wizard-health-check.png`
**Location**: Save to `docs/assets/images/alpha-onboarding/`

**How to Capture**:
1. From welcome screen, click "Get Started" or equivalent
2. Wait for system health checks to complete
3. Capture: The health check results screen

**What to Show**:
- [ ] Visual indicators for each check (checkmarks, status icons)
- [ ] Four checks visible:
  - ✓ Docker installed and running
  - ✓ Python version correct (3.11 or 3.12)
  - ✓ Port 8001 available
  - ✓ Database accessible
- [ ] Clear success state (all green/checked)
- [ ] Progress indicator or "Continue" button

**Notes**: This demonstrates the automatic validation feature. All checks should show as passing.

---

### 3. Setup Wizard - API Key Configuration

**Filename**: `setup-wizard-api-keys.png`
**Location**: Save to `docs/assets/images/alpha-onboarding/`

**How to Capture**:
1. Proceed from health check screen
2. Arrive at API key configuration screen
3. **DO NOT enter real API keys** (use placeholder text like "sk-..." or leave blank)
4. Capture: The API key configuration form

**What to Show**:
- [ ] Form fields for API keys:
  - OpenAI API Key field
  - Anthropic API Key field
  - Google Gemini API Key field (if present)
- [ ] Clear labels and placeholders
- [ ] Validation indicators (if visible without real keys)
- [ ] Help text or instructions
- [ ] "Continue" or "Save" button

**Notes**: This is the **key improvement** in v0.8.2 - much easier than CLI. Emphasize the visual, form-based approach.

**Security**: Do NOT capture with real API keys. Use fake/placeholder text or blank fields.

---

### 4. Setup Wizard - User Account Creation

**Filename**: `setup-wizard-user-creation.png`
**Location**: Save to `docs/assets/images/alpha-onboarding/`

**How to Capture**:
1. Proceed from API key configuration
2. Arrive at user account creation screen
3. Fill in with placeholder data:
   - Username: "testuser" or similar
   - Email: "test@example.com"
   - Password: Use placeholder dots (don't reveal actual password)
4. Capture: The user creation form

**What to Show**:
- [ ] Username field with clear label
- [ ] Email field with validation (format checking)
- [ ] Password field (obscured with dots/asterisks)
- [ ] Password confirmation field
- [ ] Real-time validation feedback (if visible):
  - Password strength indicator
  - Format requirements (min 8 chars, etc.)
- [ ] Clear "Create Account" or "Continue" button

**Notes**: Should show the clean form interface with helpful validation feedback.

---

### 5. Setup Wizard - Setup Complete

**Filename**: `setup-wizard-success.png`
**Location**: Save to `docs/assets/images/alpha-onboarding/`

**How to Capture**:
1. Complete all previous steps
2. Arrive at setup completion/success screen
3. Capture: The final confirmation screen

**What to Show**:
- [ ] "Setup Complete!" or similar success message
- [ ] Summary of what was configured:
  - ✓ System verified
  - ✓ API keys configured
  - ✓ User account created
- [ ] Next steps guidance
- [ ] Clear call-to-action button:
  - "Start Using Piper" or
  - "Go to Login" or
  - "Continue to Dashboard"
- [ ] Professional, celebratory but matter-of-fact tone

**Notes**: This is the final screen before users start using Piper. Should feel like an accomplishment but not over-the-top.

---

## Capture Best Practices

### Technical Settings

- **Browser**: Use Chrome or Firefox (consistent rendering)
- **Window Size**: Full-screen or at least 1400px wide
- **Zoom Level**: 100% (no browser zoom)
- **Format**: PNG (lossless, good for UI screenshots)
- **Tool**: macOS Screenshot (Cmd+Shift+4) or built-in browser tools

### Visual Guidelines

- **Clean Interface**: Close unnecessary browser tabs/bookmarks
- **Hide Personal Info**: No real API keys, personal emails, or sensitive data
- **Focus on Content**: Capture the main content area, minimal chrome
- **Consistent Framing**: Similar framing/positioning across all 5 screenshots
- **Professional Quality**: Clear, in-focus, properly lit (if screen recording)

### After Capture

1. **Review Each Screenshot**:
   - [ ] All text readable at documentation size
   - [ ] No personal/sensitive information visible
   - [ ] Professional appearance
   - [ ] Matches description in checklist

2. **Save to Correct Location**:
   ```bash
   docs/assets/images/alpha-onboarding/
   ├── setup-wizard-welcome.png
   ├── setup-wizard-health-check.png
   ├── setup-wizard-api-keys.png
   ├── setup-wizard-user-creation.png
   └── setup-wizard-success.png
   ```

3. **Verify Documentation Links**:
   - Open `docs/ALPHA_QUICKSTART.md` in browser/preview
   - Open `docs/ALPHA_TESTING_GUIDE.md` in browser/preview
   - Confirm all 5 images display correctly
   - Check that paths are correct (relative to docs/)

---

## Timeline

**Recommended**: Capture all 5 screenshots in one session to ensure visual consistency.

**Estimated Time**: 15-20 minutes for full capture and review.

---

## Completion Checklist

After capturing all screenshots:

- [ ] All 5 screenshots saved to `docs/assets/images/alpha-onboarding/`
- [ ] Filenames match exactly (lowercase, hyphens)
- [ ] No personal/sensitive information in any screenshot
- [ ] All screenshots are PNG format
- [ ] Resolution is 1200px width minimum
- [ ] Screenshots display correctly in `ALPHA_QUICKSTART.md`
- [ ] Screenshots display correctly in `ALPHA_TESTING_GUIDE.md`
- [ ] Visual consistency across all 5 images
- [ ] Professional quality and appearance

---

**Next Steps**: After screenshots are captured and verified, update `docs/NAVIGATION.md` to document the new assets location.
