Hey [Name],

You mentioned interest in testing Piper Morgan - excited to have you as an early alpha tester!

Before we schedule setup, let's make sure you have everything needed. The good news: we've built a visual setup wizard that makes initial configuration much easier.

**PREREQUISITES CHECKLIST**

Technical Requirements:
- Comfortable using command line/terminal (for initial clone and install)
- Python 3.11 or 3.12 installed on your machine
- Docker installed and running
- Git installed and working
- About 200MB free disk space
- 30-45 minutes available for guided setup (includes Docker installation if needed)

Accounts & API Keys You'll Need:
- GitHub account
- At least one LLM API key:
  - OpenAI (GPT-4 preferred) -OR-
  - Anthropic (Claude) -OR-
  - Google Gemini
  (You can configure multiple providers)
- Budget $5-20 for API testing costs
- Notion account (optional but recommended)

**WHAT MAKES THIS EASY (New in 0.8.5.3)**

Our GUI setup wizard (`python main.py` → opens in browser) will:
- Check your system automatically (Docker, Python, ports, database)
- Show results visually with clear status indicators
- Guide you through API key configuration in a web form (much easier than CLI)
- Guide you through account creation with real-time validation
- Validate your API keys before storing them
- Set up the database and services for you
- Take about 10-15 minutes total (or 30-45 minutes if Docker installation is needed)

The visual interface makes API key management much easier - you can see what you're typing and get immediate feedback.

After setup, you can optionally configure your preferences (`python main.py preferences`) to personalize how Piper works for you.

**CRITICAL DISCLAIMERS**

This is ALPHA software (version 0.8.5.3). That means:
- It will have bugs and rough edges
- It might crash or lose data
- Security is not fully audited (data not yet encrypted at rest)
- You're responsible for your API charges
- Not for mission-critical work
- Not for employer machines (without permission)

**WHAT TO EXPECT**

Week 1: Guided setup call (30 mins) + initial testing
Week 2-3: You test, I fix bugs you find
Week 4+: Quick weekly check-ins

Setup, login, and the chat interface are stable in 0.8.5.3. **Focus your testing on workflows**: lists, todos, projects, file management, and integrations. The UI is now fully accessible (WCAG 2.1 AA compliant). The goal is finding PM workflows that delight you, despite the rough edges.

**STILL INTERESTED?**

Reply with:
1. Which LLM provider you'll use (OpenAI/Anthropic)
2. Your biggest PM pain point you hope Piper helps with
3. Best time for a 30-min setup call (recommended for first-time setup)

If this feels like too much technical setup, totally understand! We're planning a hosted version for later in 2026.

Best,
Christian

P.S. We're keeping the alpha cohort small so I can provide proper support.
