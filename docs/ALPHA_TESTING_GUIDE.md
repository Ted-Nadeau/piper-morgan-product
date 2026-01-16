# Piper Morgan Alpha Testing Guide

**Version**: 0.8.4.2
**Last Updated**: January 15, 2026
**For**: Alpha Testers

---

## Before You Begin - Prerequisites Checklist

**Required Software:**

- [ ] Git installed and configured
- [ ] Python 3.11 or higher
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

This is pre-release alpha software (version 0.8.4). By proceeding, you acknowledge:

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

## What's New in 0.8.4.1

**Bug Fixes**:
- Chat now auto-loads conversation on page refresh (#583)
- `/standup` command correctly routes to interactive handler (#585)
- UserContextService properly connects to database projects (#582)
- Chat sidebar sync with conversation selection (#581)
- Conversation history sidebar switching fixed (#574)

**Architecture Improvement**:
- New `RequestContext` model for unified identity handling (ADR-051, #584)
- Foundation for better user/session management across the codebase

## What's New in 0.8.4

**Integration Settings (Epic #543)** - All integration credentials can now be managed from Settings → Integrations:
- **Slack**: OAuth Connect/Disconnect button
- **Google Calendar**: OAuth Connect/Disconnect with sync preferences
- **GitHub**: Personal Access Token configuration with secure keychain fallback
- **Notion**: API Key configuration with workspace preferences
- **Disconnect All**: One-click to reset all integrations

**Portfolio Onboarding (#490)** - New users now experience conversational project setup:
- Triggered automatically on first greeting ("Hello!")
- Tell Piper about your projects in natural language
- Creates Project entities for better context in future conversations
- Multi-turn flow with confirmation before saving

**Bug Fixes**:
- Logout 403 "Not authenticated" error fixed
- Integration Test button now uses correct OAuth tokens (#562)
- Demo integration disabled by default (was confusing users)

## What's New in 0.8.3.2

**Interactive Standup Assistant** - The standup feature now supports conversational interactions. Start with "let's write a standup" or "/standup" and Piper will guide you through the process interactively:
- **Preference gathering**: Tell Piper your style preferences (concise, detailed, bullet points)
- **Iterative refinement**: Request changes until you're happy with the result
- **Version history**: Previous versions saved if you want to compare
- **Performance**: Sub-500ms response times with P95 at 0.03ms

**Standup Monitoring Dashboard** - Behind the scenes, all standup conversations are now tracked with structured logging for debugging and performance analysis.

**Epic #242 Complete** - The Interactive Standup Conversation feature (CONV-MCP-STANDUP-INTERACTIVE) is now fully implemented with:
- Issue #552: Conversation state management (7-state machine)
- Issue #553: Turn-based dialogue system
- Issue #554: Preference learning integration
- Issue #555: LLM workflow with Chain-of-Draft
- Issue #556: Performance monitoring (<500ms target met)

## What's New in 0.8.3

**Integration Health Dashboard** - New dashboard at Settings → Integrations showing real-time status of all integrations. One-click "Test" buttons let you verify each integration is working. Visual status indicators show healthy, degraded, or failed states with helpful fix suggestions.

**OAuth Connection Management** - Connect and disconnect Slack and Google Calendar directly from the Settings page. No more editing environment variables - just click "Connect" and authorize through the OAuth flow. Connected integrations show account details (workspace name, email).

**Notion in Setup Wizard** - The setup wizard now includes Notion API key configuration. Enter your key and see immediate validation with workspace name confirmation before saving.

**Stable Core Features** - Setup, login, chat, lists, todos, and file management are stable. **Focus your testing on the new integration features**: the dashboard, OAuth connections, and Notion setup.

**Bug Fixes** - Calendar OAuth now works reliably (state persistence fix). Toast notifications are visible and readable (7-second duration). Breadcrumb navigation no longer overlaps.

---

## Windows Alpha Tester Setup

**Best Option: Use the Automated Setup Script**

We've created a Windows batch file that automates the entire setup process:

```cmd
git clone -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
.\scripts\alpha-setup.bat
```

The script will:
- Check for Python 3.11/3.12 and Docker
- Create a virtual environment
- Install all dependencies
- Generate a secure JWT key
- Start Docker containers
- Launch the setup wizard at http://localhost:8001/setup

### Alternative: WSL2 (Windows Subsystem for Linux)

If you prefer a Linux-like environment on Windows, WSL2 provides a smooth setup experience:

```powershell
# 1. Run as Administrator
wsl --install
wsl --set-default-version 2
wsl --install -d Ubuntu-22.04

# 2. Inside Ubuntu terminal
sudo apt update && sudo apt upgrade -y
sudo apt install python3.11 python3.11-venv git

# 3. Clone and setup (uses bash script - faster)
git clone -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
./scripts/alpha-setup.sh
```

### Manual Setup (If You Prefer Full Control)

If you prefer not to use automated scripts, follow the guided setup below. On Windows, use:
- PowerShell or Command Prompt
- `venv\Scripts\Activate.ps1` to activate (Windows-style path)
- See [Windows Setup Guide](installation/windows-setup-guide.md) for troubleshooting

### Known Windows Issues for Alpha Testers

1. **Clone failures**: Ensure you have long path support enabled:
   ```powershell
   # Run as Administrator
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
     -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```

2. **Python not found**:
   - Reinstall from https://www.python.org/downloads
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Restart Command Prompt/PowerShell after installing

3. **Path errors in commands**: Use backslashes (Windows-native) or quotes with forward slashes:
   ```powershell
   python main.py setup              # Works on all platforms
   python -c "import sys; print(sys.version)"  # Also works
   ```

4. **Docker Desktop not running**: The setup script will fail if Docker Desktop isn't running
   - Start Docker Desktop before running the setup script
   - Wait for it to fully initialize (check system tray)

---

## Guided Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
```

**Note**: On Windows, use the WSL2 terminal or PowerShell with proper path handling

### Step 2: Create Virtual Environment

```bash
python3.12 -m venv venv
# Requires Python 3.11 or 3.12 - verify with: python --version
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start Server for First-Time Setup

**New in 0.8.2+**: Setup now uses a visual web interface by default.

```bash
python main.py
# → Opens http://localhost:8001/setup (GUI setup wizard)
```

The GUI setup wizard will automatically open in your browser and guide you through:

- ✅ System health checks (Docker, Python, Port, Database)
- ✅ API key configuration (OpenAI, Anthropic, Gemini)
- ✅ User account creation (username, email, password)
- ✅ Setup verification and confirmation

**See the Setup Wizard Walkthrough section below** for detailed screenshots and step-by-step guidance.

#### Alternative: Command-Line Setup

If you prefer the original command-line interface:

```bash
python main.py setup
```

This will run the CLI setup wizard with prompts in your terminal. Both methods configure the same settings - use whichever you're comfortable with.

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

## Setup Wizard Walkthrough (New in 0.8.2)

The GUI setup wizard provides a visual, step-by-step interface for configuration. Here's what to expect at each stage:

### Step 1: Welcome Screen

![Setup Wizard - Welcome](assets/images/alpha-onboarding/setup-wizard-welcome.png)

The welcome screen introduces the setup process and explains what will be configured. Click "Get Started" to begin.

### Step 2: System Health Check

![Setup Wizard - Health Check](assets/images/alpha-onboarding/setup-wizard-health-check.png)

Automatic validation of your system:
- ✓ Docker installed and running
- ✓ Python version correct (3.11 or 3.12)
- ✓ Port 8001 available
- ✓ Database accessible

If any checks fail, the wizard provides specific guidance on how to fix them.

### Step 3: API Key Configuration

![Setup Wizard - API Keys](assets/images/alpha-onboarding/setup-wizard-api-keys.png)

Configure your LLM API keys through a web form interface. This is **much easier** than the command-line method - you can see what you're typing, correct mistakes easily, and get immediate validation feedback.

Supports:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google Gemini

You can configure one, two, or all three providers. At least one is required.

### Step 4: User Account Creation

![Setup Wizard - User Creation](assets/images/alpha-onboarding/setup-wizard-user-creation.png)

Create your admin account:
- Username (alphanumeric, unique)
- Email address (valid format required)
- Secure password (min 8 chars, bcrypt-hashed)
- Password confirmation with validation

The form provides real-time feedback on password strength and format requirements.

### Step 5: Setup Complete

![Setup Wizard - Success](assets/images/alpha-onboarding/setup-wizard-success.png)

Setup confirmation screen with:
- Summary of what was configured
- Next steps and quick links
- "Start Using Piper" button to proceed to login

Click the button to go to the login page and start using Piper Morgan.

---

## Test Scenarios to Try

**Note for 0.8.4 Testers**: Setup, login, chat, and core workflows are stable. **Focus your testing on the new Integration Settings and Portfolio Onboarding** and continue validating the Interactive Standup Assistant.

### Priority Testing Areas

1. **Interactive Standup Assistant** - Try "let's write a standup" or "/standup" in chat
2. **Standup Conversations** - Test preference gathering, refinement requests, completing standups
3. **Integration Dashboard** - Settings → Integrations, test buttons, health status display
4. **OAuth Connections** - Connect/disconnect Slack and Calendar from Settings
5. **Workflow Management** - Lists, todos, projects (CRUD operations, sharing, permissions)

### Basic Functionality Tests

Start with these simple tests to verify everything works:

1. **Basic Chat**: "Hello, what can you help me with?"
2. **Task Creation**: "Add a todo: Review Q3 metrics"
3. **Information Query**: "What tasks do I have?"
4. **File Upload**: Upload a PDF or DOCX file (max 10MB) and ask for analysis
5. **Document Summary**: "Summarize the document I just uploaded"
6. **Preference Check**: "How do you prefer to communicate?" (should reflect your settings)
7. **Multi-User Test**: If testing with others, verify you can't see their data

---

## Exploring Piper's Features

### Lists, Todos, and Projects Management

1. **Create a List**
   - Navigate to http://localhost:8001/lists
   - Click "Create New List" button
   - Enter name: "Alpha Testing Tasks"
   - Enter description: "Testing the Lists feature"
   - Verify list appears in the list view

2. **Share a List**
   - Open the list you just created
   - Click "Share" button
   - Enter another user's email (if multi-user testing)
   - Select role: Editor
   - Verify sharing modal shows success

3. **Test Permission Badges**
   - Notice "Owner" badge on your list
   - If shared with another user, verify their role badge shows

4. **Repeat for Todos and Projects**
   - Navigate to /todos and /projects
   - Same CRUD operations available
   - Test that all three resource types work consistently

### File Management

1. **Upload a File**
   - Navigate to http://localhost:8001/files
   - Click "Upload File" or drag-and-drop a file
   - Supported formats: PDF, DOCX, TXT, MD, JSON (max 10MB)
   - Verify file appears in file list with correct metadata

2. **Download a File**
   - Click "Download" button on uploaded file
   - Verify file downloads correctly

3. **Delete a File**
   - Click "Delete" button on a file
   - Verify file is removed from list

4. **Test File Privacy**
   - Files are owner-based (private to you)
   - Other users should NOT see your files

### Permission System

1. **Conversational Permission Commands**
   Try these in the chat interface:
   - "share my Alpha Testing Tasks list with [email] as editor"
   - "who can access my Alpha Testing Tasks?"
   - "show me shared lists"
   - "give [email] viewer access to my project plan"

2. **Role-Based Access Testing** (requires 2 users)
   - Create a list as User A
   - Share with User B as "Viewer"
   - Log in as User B
   - Verify: Can view list but NOT edit/delete
   - Share same list with User C as "Editor"
   - Log in as User C
   - Verify: CAN edit and update list

### Interactive Standup Assistant (New in 0.8.3.2)

1. **Start a Standup Conversation**
   - In the chat, say "let's write a standup" or "/standup"
   - Piper should respond with initial guidance
   - Verify conversation flow starts properly

2. **Test Preference Gathering**
   - Tell Piper your preferences: "I prefer bullet points" or "keep it concise"
   - Verify Piper acknowledges and remembers your preference
   - Generate content should reflect your stated style

3. **Test Iterative Refinement**
   - Ask Piper to make changes: "add more detail about the bug fix" or "make it shorter"
   - Verify Piper updates the standup accordingly
   - Previous versions should be saved for comparison

4. **Complete the Standup**
   - Say "looks good, let's use this" or "finalize"
   - Verify standup is marked complete
   - Check that performance is fast (sub-500ms responses)

5. **Edge Cases to Test**
   - Abandon a standup mid-conversation (say "nevermind" or navigate away)
   - Start multiple standups in one session
   - Long conversations (10+ turns) - verify memory isn't growing unbounded

### Quick Standup Generation (Legacy)

1. **Generate a Standup**
   - Navigate to http://localhost:8001/standup
   - Click "Generate Standup" button
   - Wait 2-3 seconds for AI generation
   - Verify standup report appears with meaningful content
   - Note: First standup may be generic if no prior activity

2. **Test with Activity**
   - Create some lists, todos, upload files
   - Generate standup again
   - Verify it reflects your recent activity

### Authentication & Logout

1. **Test Logout**
   - Click user menu (top right corner of page)
   - Click "Logout" button
   - Verify you're redirected to login page
   - Verify session is cleared (can't access /lists without login)

2. **Test Login After Logout**
   - Enter your credentials on login page
   - Verify you can log back in
   - Verify your data is still there (lists, files, etc.)

### Navigation & Polish

1. **Test Breadcrumbs**
   - Navigate to /lists, /todos, /projects, /files, /standup
   - Verify each page shows breadcrumb: Home › [Page Name]
   - Click "Home" in breadcrumb, verify navigation works

2. **Test Page Consistency**
   - Check that Settings pages are on unified grid
   - Verify no "My Lists" prefix (should just be "Lists")
   - Check that Integrations page shows placeholder (not 404)
   - Check Privacy & Data settings has informative content

---

## Troubleshooting

### Setup Wizard Issues

**GUI setup wizard not loading?**

- Make sure you ran `python main.py` (not `python main.py setup`)
- Check that http://localhost:8001/setup opens in your browser
- If browser didn't auto-open, manually navigate to http://localhost:8001/setup
- Alternative: Use CLI setup with `python main.py setup`

**"Docker not installed" or "Docker not running"**

The setup wizard (GUI or CLI) will guide you through Docker installation with platform-specific instructions. If you encounter issues:

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

- Re-run GUI setup wizard: Navigate to http://localhost:8001/setup
- Or use CLI setup: `python main.py setup`
- Verify API keys are valid in your provider dashboard (OpenAI, Anthropic, Google)
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

### Feature-Specific Troubleshooting

**Can't create lists/todos/projects?**
- Make sure you're on the `production` branch: `git status`
- Update to latest: `git pull origin production`
- Refresh browser page
- Check browser console for errors (F12)
- Verify you're logged in (authentication required for CRUD operations)

**Files page not loading or shows errors?**
- Update to latest: `git pull origin production`
- Restart server: `python main.py`
- Clear browser cache if needed
- Check file size limit: 10MB maximum
- Verify supported formats: PDF, DOCX, TXT, MD, JSON

**Interactive Standup issues?**
- Conversation should respond in <500ms (P95 target)
- If conversation seems stuck, try "start over" or navigate away
- Each turn should build on previous context
- Preferences should be remembered within the conversation

**Quick Standup generation hangs or fails?**
- Should complete in 2-3 seconds
- If hanging, check API key configuration: `python main.py status`
- Verify you have activity data (lists, todos, files created)
- Try refreshing the page and generating again

**Logout not working?**
- Logout is in the user menu (top right corner)
- Click user menu → "Logout"
- Verify redirect to login page after logout
- If session persists, clear browser cookies

**Permission sharing not working?**
- Requires multi-user setup (2+ user accounts)
- Make sure other user exists in database
- Try conversational command: "share my [resource] with [email] as editor"
- Verify resource ownership (you must own the resource to share it)
- Check that SEC-RBAC is active: `python main.py status`

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
- Your LLM API keys are stored securely in system keychain, never transmitted
- Preference data is stored locally in your database
- You can opt out of analytics in settings
- Setup wizard completion statistics help us improve onboarding
- SEC-RBAC Phase 1 ensures owner-based access control
- Shared resources require explicit permission grants
- Your files, lists, todos, and projects are private by default
- **Note**: Data is not yet fully encrypted at rest (see `ALPHA_KNOWN_ISSUES.md` for details)

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

Remember: This is alpha software (version 0.8.4). The GUI setup wizard handles most complexity, but you're still testing early-stage software. Expect bugs and incomplete features.

If guided setup seems overwhelming, a hosted version is planned for 2026.

Thank you for being an early adopter and helping us improve! 🚀

---

## See Also

- `VERSION_NUMBERING.md` - Understanding Piper Morgan's version scheme
- `ALPHA_AGREEMENT_v2.md` - Legal terms and conditions
- `ALPHA_KNOWN_ISSUES.md` - Current bugs and limitations
- `ALPHA_QUICKSTART.md` - Quick 2-5 minute setup guide

---

_Last updated: January 13, 2026_
_Software version: 0.8.4.1_
