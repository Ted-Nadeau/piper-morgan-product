# Piper Morgan - AI Product Management Assistant

**Status**: ⚡ **ALPHA** - Actively improving with your feedback
**Version**: 0.3-alpha (November 2025)

[![Build Status](https://github.com/mediajunkie/piper-morgan-product/workflows/test/badge.svg)](https://github.com/mediajunkie/piper-morgan-product/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Welcome to the Piper Morgan alpha!** 🚀 You're part of a small group testing the next generation of AI-powered product management. Your feedback shapes what we build next.

## What is Piper Morgan?

Piper Morgan is an AI-powered assistant that helps product managers work smarter, faster, and with better context. Talk to Piper in natural language, and it understands your intent, remembers context, and takes action across your tools.

### What You Can Do

- **🗣️ Natural Conversations**: Just ask—Piper understands "that issue we discussed" and "my highest priority task"
- **🧠 Remembers Context**: 10-turn context memory means you don't have to repeat yourself
- **⚡ Morning Standup**: Get your daily summary with real activity from GitHub, Calendar, and more
- **📊 Smart Analysis**: Let AI prioritize, summarize, and surface insights from your work
- **🌐 Works Everywhere**: Web interface, API, or CLI—use what works for you

### Alpha Features (November 2025)

- ✅ GitHub issue analysis and status updates
- ✅ Calendar and availability checking
- ✅ Morning standup with multi-integration context
- ✅ Web interface with dark mode
- ✅ Natural language intent understanding
- 🚧 Slack integration (coming soon)
- 🚧 Notion document management (coming soon)

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- Python 3.11+
- Docker (for database and services)
- OpenAI API key ([get one free](https://platform.openai.com))
- GitHub personal access token ([create one](https://github.com/settings/tokens))
- Calendar API credentials optional (Google Calendar or similar)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product

# 2. Run the setup wizard (recommended)
python main.py setup
```

The setup wizard will:
- ✅ Check your system (Python, Docker, ports)
- ✅ Ask for API keys (stored securely)
- ✅ Initialize the database
- ✅ Create your user account

### Start Using Piper

```bash
# Start the server
python main.py

# Open your browser
# Web: http://localhost:8001
# Morning Standup: http://localhost:8001/standup
# API Docs: http://localhost:8001/docs
```

### First Steps

1. **Try the Web Interface**: Open http://localhost:8001/standup for your morning summary
2. **Use the Chat Interface**: Ask natural language questions like:
   - "What are my top 5 priorities?"
   - "Show me open issues in my repos"
   - "What's on my calendar today?"
3. **Check the Examples**: See [Alpha Testing Guide](docs/ALPHA_TESTING_GUIDE.md) for test scenarios

### Example Conversations

```
You: "What's on my calendar today?"
Piper: "📅 You have 3 meetings: Stand-up at 10am, Product Review at 2pm, 1:1 with Alex at 4pm"

You: "Show me my open issues"
Piper: "🐙 15 open issues: 5 bugs, 4 features, 6 enhancements. Top priority: Critical login bug (P0)"

You: "Mark that login bug as done"
Piper: "✅ Updated GitHub issue #42 to closed status"
```

---

## 📋 Alpha Testing

### How to Report Issues

Found a bug or something doesn't work? Help us improve:

```bash
1. Check Known Issues: docs/ALPHA_KNOWN_ISSUES.md
2. File a GitHub Issue: https://github.com/mediajunkie/piper-morgan-product/issues
3. Include:
   - What you were trying to do
   - What happened instead
   - Steps to reproduce
   - System info (python --version, docker --version)
   - Any error messages
```

### Alpha Testing Guide

See [ALPHA_TESTING_GUIDE.md](docs/ALPHA_TESTING_GUIDE.md) for:
- Guided test scenarios
- What features to focus on
- How to provide feedback
- Weekly testing checklist

### Known Issues

See [ALPHA_KNOWN_ISSUES.md](docs/ALPHA_KNOWN_ISSUES.md) for current limitations and workarounds.

### Alpha Agreement

By participating in alpha testing, you agree to:
- Report bugs and issues
- Keep your feedback constructive
- Understand that features may change
- Not share with non-alpha testers (until public release)

[Read full agreement](docs/ALPHA_AGREEMENT_v2.md)

---

## 📚 Documentation

### For Alpha Testers
- **[Alpha Quick Start](docs/ALPHA_QUICKSTART.md)** - Get running in 5 minutes
- **[Alpha Testing Guide](docs/ALPHA_TESTING_GUIDE.md)** - What to test and how
- **[Known Issues](docs/ALPHA_KNOWN_ISSUES.md)** - Current limitations
- **[Testing Checklist](docs/ALPHA_TESTING_GUIDE.md#testing-checklist)** - Weekly focus areas

### For Developers
- **[Technical Reference](docs/TECHNICAL-DEVELOPERS.md)** - Complete developer guide
- **[Architecture Overview](docs/NAVIGATION.md)** - System design and patterns
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute code

### General Resources
- 📖 [Documentation Hub](docs/NAVIGATION.md) - Find what you need
- 🏠 [Main Project Hub](docs/HOME.md) - Project overview
- 🔧 [Version Info](docs/VERSION_NUMBERING.md) - Release versioning

---

## ❓ FAQ & Troubleshooting

### "Setup fails at database check"
**Fix**: Make sure Docker is running and port 5433 is available
```bash
docker ps  # Check if containers running
lsof -i :5433  # Check port availability
```

### "API keys not being accepted"
**Fix**: Keys are stored in your system keychain. Rerun setup or update manually
```bash
python main.py setup  # Run setup again
```

### "Standup page takes too long to load"
**Fix**: It aggregates data from multiple integrations. First load can take 5-10 seconds. Subsequent loads are faster (cached).

### "Changes not showing up"
**Fix**: Clear your browser cache (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows/Linux)

### For more help
See [Troubleshooting Guide](docs/TESTING.md) or file an issue with details.

---

## 🤝 Feedback & Support

### Report a Bug
- **GitHub Issues**: [File an issue](https://github.com/mediajunkie/piper-morgan-product/issues/new)
- **Include**: Reproduction steps, error message, system info

### Share Feedback
- **Email**: feedback@pmorgan.tech
- **Discussions**: [GitHub Discussions](https://github.com/mediajunkie/piper-morgan-product/discussions)
- **What we want to hear**:
  - Features you want
  - Workflows that work well
  - Pain points and rough edges
  - Ideas for improvement

### Get Help
- **Setup issues**: See [ALPHA_QUICKSTART.md](docs/ALPHA_QUICKSTART.md)
- **Usage questions**: Check [ALPHA_TESTING_GUIDE.md](docs/ALPHA_TESTING_GUIDE.md)
- **Technical problems**: See [TECHNICAL-DEVELOPERS.md](docs/TECHNICAL-DEVELOPERS.md)

---

## 📅 What's Next

**Coming in next alpha release** (December 2025):
- 🚧 Slack integration for notifications
- 🚧 Notion document linking
- 🚧 Jira integration
- 🚧 Performance improvements
- 🚧 Better error messages

Your feedback shapes our priorities! Tell us what matters most.

---

**Made with ❤️ by the Piper Morgan team**
# Test
