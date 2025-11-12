# Piper Morgan Alpha Testing Guide

**Version**: 0.8.0 (First Alpha Release)
**Last Updated**: October 24, 2025
**For**: Alpha Wave 2 Testers

---

## Before You Begin - Prerequisites Checklist

**Required Software:**

- [ ] Git installed and configured
- [ ] Python 3.9 or higher
- [ ] Docker installed and running
- [ ] A code editor (VS Code recommended)
- [ ] Terminal/command line access

**Required Accounts & Keys:**

- [ ] **GitHub account with SSH key configured** (required BEFORE cloning)

  - **Why needed**: You must authenticate to GitHub to clone the repository
  - **If you already have SSH keys**: Test with `ssh -T git@github.com`
    - ✅ Success: "Hi username! You've successfully authenticated..."
    - ❌ Failure: See setup guide below
  - **If you need to set up SSH keys**: Follow GitHub's official guides:
    - 📖 [Generating SSH Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
    - 📖 [Adding SSH Key to GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
  - **Note**: This MUST be done before Step 1 (cloning repository)

- [ ] At least one LLM API key:
  - OpenAI API key (GPT-4 access preferred), OR
  - Anthropic API key (Claude access)
- [ ] Budget $5-20 for LLM API testing costs

**Optional but Recommended:**

- [ ] Notion API key (for document management features)
- [ ] Slack workspace (for notification features)
- [ ] GitHub personal access token (for issue creation features)

**Time Commitment:**

- [ ] 45-60 minutes for guided setup and initial exploration (includes Docker installation if needed)
- [ ] 15-30 minutes weekly for feedback during alpha period

---

## Important Disclaimers - Please Read

**⚠️ ALPHA SOFTWARE WARNING ⚠️**

This is pre-release alpha software (version 0.8.0). By proceeding, you acknowledge:

1. **Expected Issues**: Bugs, crashes, and incomplete features are normal
2. **Data Loss Risk**: Your data may be lost at any time without warning
3. **No Production Use**: Do NOT use for mission-critical or time-sensitive work
4. **Employer Systems**: Do NOT install on employer hardware without written permission
5. **API Charges**: You are responsible for all LLM API costs incurred
6. **Security**: Not security audited - use test data only, no sensitive information
7. **No Warranty**: Software provided "as-is" without any warranty whatsoever
8. **No Support SLA**: Best-effort support only, no guaranteed response times

See `ALPHA_AGREEMENT.md` for complete legal terms.

---

## Guided Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/Codewarrior1988/piper-morgan.git
cd piper-morgan
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Interactive Setup Wizard

**This is the key difference from manual setup!**

```bash
python main.py setup
```

The setup wizard will:

- ✅ Check your system (Docker, Python 3.9+, port 8001, database)
- ✅ Guide you through creating your user account (username, email, password)
- ✅ Set up secure password (min 8 chars, bcrypt-hashed)
- ✅ Collect and validate your API keys
- ✅ Initialize the database and services
- ✅ Verify everything is working

**Expected output:**

```
==================================================
Welcome to Piper Morgan Alpha!
==================================================

Let's get you set up (takes about 5 minutes)

1. System Check
   ✓ Docker installed
   ✓ Python 3.9+
   ✓ Port 8001 available
   ✓ Database accessible

2. User Account Setup
   Username: [you'll enter this]
   Email: [you'll enter this]
   Password: [secure, hidden input - min 8 chars]
   Confirm password: [must match]
   ✓ Password set securely
   ✓ Account created

3. API Key Configuration
   [Guided prompts for OpenAI/Anthropic keys]
   ✓ API keys validated and stored

✅ Setup Complete!
```

### Step 5: Configure Your Preferences

After setup, personalize your experience:

```bash
python main.py preferences
```

This 2-minute questionnaire configures:

- **Communication Style**: concise, balanced, detailed
- **Work Style**: structured, flexible, exploratory
- **Decision Making**: data-driven, intuitive, collaborative
- **Learning Style**: examples, explanations, exploration
- **Feedback Level**: minimal, moderate, detailed

### Step 6: Verify Installation

```bash
python main.py status
```

You should see:

```
==================================================
Piper Morgan System Status
==================================================

Database:
  ✓ PostgreSQL connected
     Users: 1, Size: 15.2 MB

API Keys:
User: [your-username]
  ✓ openai: Valid
  ✓ anthropic: Valid (or ○ Not configured)

Performance:
  ✓ Database response: 12ms

Recommendations:
  ✓ All systems operational!
```

### Step 7: First Run

```bash
python main.py
```

The server will start and automatically open http://localhost:8001 in your browser.

**Login with your credentials:**

- Username: [from setup wizard]
- Password: [from setup wizard]

After login, you'll see the Piper Morgan chat interface.

---

## Test Scenarios to Try

Start with these simple tests to verify everything works:

1. **Basic Chat**: "Hello, what can you help me with?"
2. **Task Creation**: "Add a todo: Review Q3 metrics"
3. **Information Query**: "What tasks do I have?"
4. **File Upload**: Upload a PDF or DOCX file (max 10MB) and ask for analysis
5. **Document Summary**: "Summarize the document I just uploaded"
6. **Preference Check**: "How do you prefer to communicate?" (should reflect your settings)
7. **Multi-User Test**: If testing with others, verify you can't see their data

---

## Troubleshooting

### Setup Wizard Issues

**"Docker not installed" or "Docker not running"**

The setup wizard will guide you through Docker installation with platform-specific instructions. If you encounter issues:

- Make sure Docker Desktop is running (look for whale icon in system tray/menu bar)
- Restart Docker Desktop if it seems stuck
- On macOS: Check Applications folder for Docker Desktop
- On Windows: Check if Docker Desktop service is running
- Test manually with: `docker --version`

**"Python 3.9+ not found"**

- Install Python 3.9+: https://www.python.org/downloads/
- Recommended: Python 3.11+ for best compatibility
- Test with: `python --version`

**"Port 8001 not available"**

- Another service is using port 8001
- Find what's using it: `lsof -i :8001`
- Stop other Piper Morgan instances or change port

**"Database not accessible"**

- Ensure database is running: `docker-compose up -d db`
- Wait 10 seconds for database to start
- Check Docker containers: `docker ps`

### Runtime Issues

**"No LLM provider configured"**

- Re-run setup wizard: `python main.py setup`
- Verify API keys are valid in your provider dashboard
- Check status: `python main.py status`

**High API costs**

- Piper uses GPT-4/Claude by default for best results
- Monitor usage in your provider's dashboard
- Configure preferences for more concise responses

**Preference changes not taking effect**

- Re-run: `python main.py preferences`
- Restart Piper Morgan after preference changes
- Check status shows your username correctly

**Login issues**

- Forgot password? Run `python main.py setup` to create a new account
- Can't access http://localhost:8001? Try http://127.0.0.1:8001
- Check server is running: Look for "Server ready" message
- Browser didn't open? Manually navigate to http://localhost:8001

**File upload issues**

- Supported formats: PDF, DOCX, TXT, MD, JSON
- Max file size: 10MB
- Check file isn't corrupted or password-protected
- Verify you're logged in (file upload requires authentication)

---

## Providing Feedback

We need your feedback to improve! Please report:

### What to Report

- Bugs and crashes (with error messages)
- Setup wizard issues or confusing steps
- Preference system problems
- Missing features you expected
- Performance issues
- Successful workflows that delighted you

### How to Report

1. **GitHub Issues**: Preferred for bugs (if comfortable with GitHub)
2. **Email**: christian@[domain] for private feedback
3. **Weekly Check-in**: Optional 15-minute calls available

### Helpful Feedback Format

```
SETUP METHOD: [wizard/manual]
WHAT I TRIED: [specific action]
WHAT I EXPECTED: [expected result]
WHAT HAPPENED: [actual result]
ERROR MESSAGE: [if any]
SYSTEM STATUS: [output of `python main.py status`]
SEVERITY: [blocker/major/minor]
```

---

## Privacy & Data Collection

- We collect anonymous usage analytics to improve the product
- Error logs may be transmitted (no personal data included)
- Your LLM API keys are stored locally in system keychain, never transmitted
- Preference data is stored locally in your database
- You can opt out of analytics in settings
- Setup wizard completion statistics help us improve onboarding

---

## Advanced: Manual Setup (If Wizard Fails)

If the setup wizard fails, you can fall back to manual configuration:

1. **Environment Variables**: Copy `.env.example` to `.env` and edit
2. **Database**: Run `docker-compose up -d db`
3. **API Keys**: Manually add to `.env` file
4. **Database Migration**: Run database setup scripts

See original testing guide for detailed manual steps.

---

## Questions?

Remember: This is alpha software (version 0.8.0) with a guided setup experience. The wizard handles most complexity, but you're still testing early prototype software.

If guided setup seems overwhelming, a hosted version is planned for 2026.

Thank you for being an early adopter and helping us perfect the onboarding experience! 🚀

---

## See Also

- `VERSION_NUMBERING.md` - Understanding Piper Morgan's version scheme
- `ALPHA_AGREEMENT.md` - Legal terms and conditions
- `ALPHA_KNOWN_ISSUES.md` - Current bugs and limitations
- `ALPHA_QUICKSTART.md` - Minimal 2-minute setup guide

---

_Last updated: November 11, 2025_
_Software version: 0.8.0_
_Guide version: 2.1 (Guided Setup with Password)_
