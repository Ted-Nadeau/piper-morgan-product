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
cd piper-morgan
python -m venv venv && source venv/bin/activate
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

```bash
# In Piper's chat interface:
"Hello, what can you help me with?"
"Add a todo: Test Piper Morgan"
"What tasks do I have?"
"Upload a document and summarize it"  # Use file upload feature
```

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

---

## Key Commands Reference

```bash
python main.py setup       # Interactive setup wizard
python main.py preferences # Configure your preferences
python main.py status      # System health check
python main.py --verbose   # Show detailed logs
python main.py --no-browser # Don't auto-open browser
```

---

## What's Working in 0.8.0

✅ Setup wizard with secure password setup, preferences, health checks
✅ Multi-user support, JWT auth with bcrypt, API keys
✅ Database (PostgreSQL via Docker) with UUID-based user IDs
✅ Token blacklist with CASCADE delete (Issue #291)
✅ File upload and document processing (PDF, DOCX, TXT, MD, JSON)
✅ Knowledge graph, boundary enforcement
✅ Audit logging, test coverage 100%

See `ALPHA_KNOWN_ISSUES.md` for complete status.

---

## Getting Help

- **Full Guide**: `ALPHA_TESTING_GUIDE.md` (comprehensive setup)
- **Known Issues**: `ALPHA_KNOWN_ISSUES.md` (bugs and status)
- **Legal**: `ALPHA_AGREEMENT.md` (terms and conditions)
- **Version Info**: `VERSION_NUMBERING.md` (what 0.8.0 means)

---

## Remember

This is **alpha software** (0.8.0). Expect bugs. Don't use for production. You're responsible for API costs. See `ALPHA_AGREEMENT.md` for details.

---

**Happy testing!** 🚀

_Last Updated: November 11, 2025_
