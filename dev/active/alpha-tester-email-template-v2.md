# Alpha Tester Pre-Qualification Email Template v2.0

## Subject Lines (A/B test these)

- "Ready to test Piper Morgan? Check requirements first"
- "Piper Morgan alpha access - Prerequisites inside"
- "[Name], before we set up Piper Morgan..."

## Email Template

```
Hey [Name],

You mentioned interest in testing Piper Morgan - excited to have you as an early alpha tester!

Before we schedule setup, let's make sure you have everything needed. The good news: we've built an interactive setup wizard that handles most of the complexity for you.

**PREREQUISITES CHECKLIST**

Technical Requirements:
□ Comfortable using command line/terminal
□ Python 3.9+ installed on your machine
□ Docker installed and running
□ Git installed and working
□ About 1GB free disk space
□ 45-60 minutes available for guided setup (includes Docker installation if needed)

Accounts & API Keys You'll Need:
□ GitHub account
□ At least one LLM API key:
  - OpenAI (GPT-4 preferred) -OR-
  - Anthropic (Claude)
□ Budget $5-20 for API testing costs
□ Notion account (optional but recommended)

**WHAT MAKES THIS EASY**

Our setup wizard (`python main.py setup`) will:
- Check your system automatically (Docker, Python, ports)
- Guide you through Docker installation if needed (with platform-specific instructions)
- Guide you through account creation
- Validate your API keys before storing them
- Set up the database and services for you
- Take about 15-20 minutes total (or 45-60 minutes if Docker installation is needed)

After setup, you'll configure your preferences (`python main.py preferences`) to personalize how Piper works for you.

**CRITICAL DISCLAIMERS**

This is ALPHA software. That means:
- It will have bugs and rough edges
- It might crash or lose data
- Security is not fully audited
- You're responsible for your API charges
- Not for mission-critical work
- Not for employer machines (without permission)

**WHAT TO EXPECT**

Week 1: Guided setup call (30 mins) + initial testing
Week 2-3: You test, I fix bugs you find
Week 4+: Quick weekly check-ins

The goal is finding PM workflows that delight you, despite the rough edges.

**STILL INTERESTED?**

Reply with:
1. Which LLM provider you'll use (OpenAI/Anthropic)
2. Your biggest PM pain point you hope Piper helps with
3. Best time for a 30-min setup call (recommended for first-time setup)

If this feels like too much technical setup, totally understand! We're planning a hosted version for early 2026.

Best,
Christian

P.S. You'll be tester #[2/3/4] - keeping it small so I can provide proper support.
```

## Follow-up After Confirmation

```
[Name],

Perfect! You're confirmed for Piper Morgan alpha access.

**NEXT STEPS:**

1. Review the attached Alpha Testing Guide (streamlined setup instructions)
2. Read and acknowledge the Alpha Agreement (legal stuff)
3. Gather your API keys
4. Our setup call is [DATE/TIME] (calendar invite coming)

**WHAT TO PREPARE:**
- Your LLM API key ready to paste
- A test PM task/project (nothing sensitive)
- Questions about what Piper can/can't do
- Patience for alpha software quirks

**SETUP PREVIEW:**
We'll run `python main.py setup` together, which handles:
- System verification (Docker, Python, database)
- Account creation
- API key configuration and validation
- Service initialization

Then `python main.py preferences` to personalize your experience.

Looking forward to your feedback! You're helping shape the future of AI-assisted PM work.

Best,
Christian

Attachments:
- ALPHA_TESTING_GUIDE_v2.pdf
- ALPHA_AGREEMENT_v2.pdf
- Setup checklist
```
