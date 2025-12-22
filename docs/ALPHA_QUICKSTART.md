# Piper Morgan Alpha - Quick Start

**Version**: 0.8.2
**Branch**: `production` (stable alpha releases)
**For**: Experienced developers who want to dive in fast
**Time**: 2-5 minutes setup, plus initial configuration

> 📍 **Branch Info**: This quickstart uses the `production` branch, which receives stable alpha releases. The `main` branch is for active development and may have bugs.

⚠️ **If you hit issues, see `ALPHA_TESTING_GUIDE.md` for comprehensive troubleshooting.**

---

## What's New in 0.8.2

**GUI Setup Wizard** - Initial setup now uses a visual interface instead of command-line prompts. Makes API key configuration easier.

**Stable Core** - Setup, login, and chat interface are stable. Focus your testing on workflows (lists, todos, file management, integrations).

**Quality Improvements** - 602 automated smoke tests validate core functionality. UI polish improvements throughout.

---

## Prerequisites

- Python 3.11 or 3.12, Docker, Git installed and working
- OpenAI or Anthropic API key ready
- Terminal comfort (for initial clone and install)

---

## Automated Setup (Recommended - 2 minutes)

**For macOS/Linux/WSL2:**
```bash
git clone -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
./scripts/alpha-setup.sh
# Script will:
# → Check requirements (Python 3.11/3.12, Docker, Git)
# → Create virtual environment
# → Install dependencies
# → Generate JWT secret automatically
# → Start Docker containers
# → Launch the setup wizard at http://localhost:8001/setup
```

**For Windows (Command Prompt or PowerShell):**
```cmd
git clone -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
.\scripts\alpha-setup.bat
REM Script will:
REM → Check requirements (Python 3.11/3.12, Docker, Git)
REM → Create virtual environment
REM → Install dependencies
REM → Generate JWT secret automatically
REM → Start Docker containers
REM → Launch the setup wizard at http://localhost:8001/setup
```

---

## Manual Setup (If You Prefer Full Control)

```bash
# 1. Clone and setup (using production branch for alpha testing)
git clone -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python3.12 -m venv venv && source venv/bin/activate
# Requires Python 3.11 or 3.12 - verify with: python --version
pip install -r requirements.txt

# 2. Configure environment variables (CRITICAL - 1 min)
cp .env.example .env
# Edit .env and set JWT_SECRET_KEY:
# Generate a secure key: openssl rand -hex 32
# Add to .env: JWT_SECRET_KEY=your-generated-key-here
# Note: .env is gitignored and survives git pull operations

# 3. Start Docker containers
docker-compose up -d

# 4. Start server for first-time setup
python main.py
# → Opens http://localhost:8001/setup (GUI setup wizard)

# 5. Complete setup wizard (web browser)
# → Navigate through visual setup screens
# → Configure API keys, create user account
# → See "Setup Wizard Walkthrough" below for details

# 6. Configure preferences (optional, 2 mins)
python main.py preferences
# → Answer 5 questions about your work style
# → Or skip and configure later via Settings page
```

---

## Setup Wizard Walkthrough (New in 0.8.2)

The GUI setup wizard guides you through configuration with a visual interface:

### Step 1: Welcome Screen

![Setup Wizard - Welcome](assets/images/alpha-onboarding/setup-wizard-welcome.png)

The setup wizard welcome screen explains what will be configured and gives you a clear starting point.

### Step 2: System Health Check

![Setup Wizard - Health Check](assets/images/alpha-onboarding/setup-wizard-health-check.png)

Automatic validation of your system:
- ✓ Docker installed and running
- ✓ Python version correct
- ✓ Port 8001 available
- ✓ Database accessible

### Step 3: API Key Configuration

![Setup Wizard - API Keys](assets/images/alpha-onboarding/setup-wizard-api-keys.png)

Configure your LLM API keys through a form interface. Much easier than pasting in the terminal - you can see what you're typing, correct mistakes, and get immediate validation feedback.

Supports:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google Gemini (new in 0.8.2)

### Step 4: User Account Creation

![Setup Wizard - User Creation](assets/images/alpha-onboarding/setup-wizard-user-creation.png)

Create your admin account:
- Username and email
- Secure password (min 8 chars, bcrypt-hashed)
- Confirmation and validation

### Step 5: Setup Complete

![Setup Wizard - Success](assets/images/alpha-onboarding/setup-wizard-success.png)

Setup confirmation with next steps and quick links to start using Piper.

---

## Alternative: Command-Line Setup

If you prefer the original command-line setup wizard:

```bash
python main.py setup
# → Follow prompts for:
#    - Username and email
#    - Secure password (min 8 chars, bcrypt-hashed)
#    - API keys (OpenAI/Anthropic/Gemini)
```

Both methods configure the same settings. Use whichever you're comfortable with.

---

## First Commands to Try

### Via Chat Interface
```bash
# In Piper's chat interface:
"Hello, what can you help me with?"
"Add a todo: Test Piper Morgan"
"What tasks do I have?"
"Upload a document and summarize it"
```

### Via UI Features

After logging in to http://localhost:8001:

1. **Lists Management** → Click "Lists" → "Create New List"
   - Add list name and description
   - Try sharing with another user (if multi-user testing)

2. **Todos Management** → Click "Todos" → "Create New Todo"
   - Full CRUD operations

3. **File Upload/Download** → Click "Files" → Upload a file
   - Supports: PDF, DOCX, TXT, MD, JSON (max 10MB)
   - Download and delete files

4. **Daily Standup** → Click "Standup" → "Generate Standup"
   - AI-powered standup generation (2-3 seconds)

5. **Logout** → Click user menu (top right) → "Logout"
   - Token revocation and logout working

6. **Permission Management** → Try conversational commands:
   - "share my project plan with alex@example.com as editor"
   - "who can access my shopping list?"

---

## Testing Focus for 0.8.2

**What's Stable** (light testing recommended):
- ✅ Setup wizard (GUI and CLI)
- ✅ Login/authentication
- ✅ Chat interface
- ✅ Basic navigation

**Where to Focus Testing** (these need your attention):
- 🔍 **Workflows**: Creating/managing lists, todos, projects
- 🔍 **File handling**: Upload, download, analysis
- 🔍 **Integrations**: Slack, GitHub, Notion connections
- 🔍 **Permission system**: Sharing resources, role-based access
- 🔍 **Learning system**: Preference detection, personalization

---

## If Something Breaks

### Docker not running?

```bash
docker --version  # Should show version
docker ps         # Should show containers
# If not: Start Docker Desktop
```

### Port 8001 taken?

```bash
lsof -i :8001     # See what's using it
kill -9 [PID]     # Kill it
```

### API key issues?

```bash
# Web UI method (easier):
# Navigate to http://localhost:8001/setup
# Re-enter your API keys in the form

# Or command-line method:
python main.py setup  # Re-run setup wizard
python main.py status # Verify keys
```

### Login issues?

```bash
# Forgot password? Re-run setup to create new account
python main.py setup

# Can't access http://localhost:8001?
# Check server is running: python main.py
# Try: http://127.0.0.1:8001
```

### Environment variables not loading after git pull?

```bash
# Your .env file is gitignored and NEVER deleted by git operations
# If you see JWT_SECRET_KEY warnings after pulling new code:

# 1. Verify .env exists:
ls -la .env

# 2. If missing, CREATE it (this is required for all setups):
cp .env.example .env

# Edit .env in your IDE or text editor and add:
# JWT_SECRET_KEY=<paste-generated-key-here>

# Generate the key:
openssl rand -hex 32

# 3. Restart server:
python main.py

# Note: .env survives git pull, checkout, merge - git never touches it
# If you never created .env, that's the issue - Step 2 above is mandatory
# The setup wizard stores API keys separately (in secure keyring)
```

---

## Key Commands Reference

```bash
python main.py              # Start server (opens browser automatically)
python main.py setup        # CLI setup wizard (alternative to GUI)
python main.py preferences  # Configure your preferences
python main.py status       # System health check
python main.py --verbose    # Show detailed logs
python main.py --no-browser # Don't auto-open browser
```

### UI Navigation (After Server Starts)

After `python main.py` starts the server at http://localhost:8001:

- **Setup** → http://localhost:8001/setup (first-time setup only)
- **Home** → http://localhost:8001/ (chat interface)
- **Lists** → http://localhost:8001/lists (manage lists)
- **Todos** → http://localhost:8001/todos (manage todos)
- **Projects** → http://localhost:8001/projects (manage projects)
- **Files** → http://localhost:8001/files (upload/download files)
- **Standup** → http://localhost:8001/standup (generate daily standup)
- **Settings** → http://localhost:8001/settings (preferences, integrations)
- **User Menu** (top right) → Logout, profile settings

---

## What's Working in 0.8.2

✅ **Setup & Onboarding** (Dec 11, 2025):
   - GUI setup wizard with visual interface
   - System health checks
   - API key validation (OpenAI, Anthropic, Gemini)
   - User account creation
   - CLI setup wizard (alternative method)

✅ **Authentication & Security**:
   - Multi-user support, JWT auth with bcrypt
   - Token blacklist with CASCADE delete
   - Secure password requirements
   - Session management

✅ **Core Features**:
   - Database (PostgreSQL via Docker) with UUID-based user IDs
   - File upload and document processing (PDF, DOCX, TXT, MD, JSON)
   - Knowledge graph, boundary enforcement
   - Audit logging

✅ **User Interface** (Stable):
   - Lists, Todos, Projects management with CRUD operations
   - Files upload/download/delete (10MB max, 5 formats)
   - Permission system (share resources, role-based access)
   - Conversational permission commands
   - Standup generation (2-3 sec)
   - Logout functionality
   - Breadcrumb navigation
   - Theme support (light/dark mode)

✅ **Quality Validation** (New in 0.8.2):
   - 602 automated smoke tests (<5 seconds)
   - CI/CD quality gates
   - UI stability improvements

✅ **SEC-RBAC Phase 1**:
   - Owner-based access control (owner_id validation)
   - Permission grants (shared_with JSONB)
   - Admin bypass pattern
   - 9 resource tables RBAC-aware

See [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) for complete status and known limitations.

---

## Getting Help

- **Full Guide**: [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) (comprehensive setup)
- **Known Issues**: [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) (bugs and status)
- **Legal**: [ALPHA_AGREEMENT_v2.md](ALPHA_AGREEMENT_v2.md) (terms and conditions)
- **Version Info**: [VERSION_NUMBERING.md](VERSION_NUMBERING.md) (what 0.8.2 means)

---

## Remember

This is **alpha software** (0.8.2). Expect bugs. Don't use for production. You're responsible for API costs. See `ALPHA_AGREEMENT_v2.md` for details.

**Testing Focus**: Setup, login, and chat are stable. Focus your testing on workflows, file handling, and integrations.

---

**Happy testing!** 🚀

_Last Updated: December 11, 2025_
