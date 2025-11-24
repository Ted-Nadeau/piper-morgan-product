# Piper Morgan Alpha - Quick Start

**Version**: 0.8.0
**Branch**: `production` (stable alpha releases)
**For**: Experienced developers who want to dive in fast
**Time**: 2-5 minutes (assumes everything works)

> 📍 **Branch Info**: This quickstart uses the `production` branch, which receives stable alpha releases. The `main` branch is for active development and may have bugs.

⚠️ **If you hit issues, see `ALPHA_TESTING_GUIDE.md` for comprehensive troubleshooting.**

---

## Prerequisites

- Python 3.9+, Docker, Git installed and working
- OpenAI or Anthropic API key ready
- Terminal comfort

---

## 5-Step Setup

```bash
# 1. Clone and setup (using production branch for alpha testing)
git clone -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python3.12 -m venv venv && source venv/bin/activate
# Requires Python 3.11 or 3.12 - verify with: python --version
pip install -r requirements.txt

# 2. Run interactive setup (5 mins)
python main.py setup
# → Follow prompts for:
#    - Username and email
#    - Secure password (min 8 chars, bcrypt-hashed)
#    - API keys (OpenAI/Anthropic)

# 3. Configure preferences (2 mins)
python main.py preferences
# → Answer 5 questions about your work style

# 4. Verify (30 secs)
python main.py status
# → Should show ✓ all green

# 5. Run
python main.py
# → Opens http://localhost:8001
```

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

### Via New UI Features (Nov 22-23, 2025)

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
python main.py setup  # Re-run setup
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

### Can't create lists/todos?

```bash
# Fixed Nov 23, 2025 (Issue #379)
# Make sure you're on latest commit:
git pull origin main  # or production branch
# Refresh browser page
```

### Files page shows "coming soon"?

```bash
# Files UI built Nov 23, 2025 (Issue #379)
# Update to latest:
git pull origin main
# Restart server: python main.py
```

### Logout button doesn't work?

```bash
# Fixed Nov 23, 2025 (Issue #379-14)
# Update to latest commit
# Logout now in user menu (top right)
```

---

## Key Commands Reference

```bash
python main.py setup       # Interactive setup wizard
python main.py preferences # Configure your preferences
python main.py status      # System health check
python main.py --verbose   # Show detailed logs
python main.py --no-browser # Don't auto-open browser
```

### UI Navigation (After Server Starts)

After `python main.py` starts the server at http://localhost:8001:

- **Lists** → http://localhost:8001/lists (manage lists)
- **Todos** → http://localhost:8001/todos (manage todos)
- **Projects** → http://localhost:8001/projects (manage projects)
- **Files** → http://localhost:8001/files (upload/download files)
- **Standup** → http://localhost:8001/standup (generate daily standup)
- **User Menu** (top right) → Logout, profile settings

---

## What's Working in 0.8.0

✅ Setup wizard with secure password setup, preferences, health checks
✅ Multi-user support, JWT auth with bcrypt, API keys
✅ Database (PostgreSQL via Docker) with UUID-based user IDs
✅ Token blacklist with CASCADE delete (Issue #291)
✅ File upload and document processing (PDF, DOCX, TXT, MD, JSON)
✅ Knowledge graph, boundary enforcement
✅ Audit logging, test coverage 100%

✅ **User Interface** (Nov 22-23, 2025):
   - Lists, Todos, Projects management with CRUD operations
   - Files upload/download/delete (10MB max, 5 formats)
   - Permission system (share resources, role-based access)
   - Conversational permission commands
   - Standup generation (2-3 sec)
   - Logout functionality
   - Breadcrumb navigation

✅ **SEC-RBAC Phase 1** (Nov 21, 2025):
   - Owner-based access control (owner_id validation)
   - Permission grants (shared_with JSONB)
   - Admin bypass pattern
   - 9 resource tables RBAC-aware

See [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) for complete status.

---

## Getting Help

- **Full Guide**: [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) (comprehensive setup)
- **Known Issues**: [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) (bugs and status)
- **Legal**: [ALPHA_AGREEMENT.md](ALPHA_AGREEMENT.md) (terms and conditions)
- **Version Info**: [VERSION_NUMBERING.md](VERSION_NUMBERING.md) (what 0.8.0 means)

---

## Remember

This is **alpha software** (0.8.0). Expect bugs. Don't use for production. You're responsible for API costs. See `ALPHA_AGREEMENT.md` for details.

---

**Happy testing!** 🚀

_Last Updated: November 23, 2025_
