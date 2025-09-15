# Piper Morgan - AI Product Management Assistant

[![Build Status](https://github.com/mediajunkie/piper-morgan-product/workflows/test/badge.svg)](https://github.com/mediajunkie/piper-morgan-product/actions)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://pmorgan.tech)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)

> **NEW: Issue Intelligence & CLI System** - Transform GitHub issues into actionable insights with AI-powered triage, pattern discovery, and conversational workflows.

## 🎯 What is Piper Morgan?

Piper Morgan is an intelligent product management assistant that transforms routine PM tasks into natural conversations while providing strategic insights through AI-powered analysis.

**Core Capabilities:**
- 🧠 **Issue Intelligence System** - AI-powered GitHub issue analysis with smart prioritization
- 💬 **Conversational AI with Memory** - Natural language workflows with 10-turn context
- ⚡ **CLI Commands** - Powerful command-line tools for daily PM workflows
- 📊 **Cross-Feature Learning** - Pattern discovery that improves over time
- 🔄 **Real-time GitHub Integration** - Live repository data and intelligent recommendations

## 🚀 Quick Demo - Issue Intelligence Workflow

Transform overwhelming GitHub backlogs into actionable insights:

```bash
# Morning standup with AI-enhanced context
piper standup

# Intelligent issue triage with priority scoring
piper issues triage --limit 15

# Discover patterns across your project
piper issues patterns

# Get project health overview
piper issues status
```

**Result**: Complete project visibility in under 30 seconds, with AI-powered recommendations for immediate actions.

## 🛠️ Get Started Fast

Choose your path based on your role:

### 🎯 Product Managers
```bash
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
./scripts/quick-start.sh
```
**Ready in 2 minutes** → [PM Quick Start Guide](getting-started/product-managers.md)

### 💻 Developers
```bash
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt && docker-compose up -d
python main.py
```
**Full dev environment** → [Developer Setup Guide](getting-started/developers.md)

### 🔧 System Administrators
**Production deployment** → [Production Setup Guide](getting-started/production.md)

## 🏗️ High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI Commands  │    │  Issue           │    │  GitHub         │
│   & Workflows   │◄──►│  Intelligence    │◄──►│  Integration    │
│                 │    │  Engine          │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Conversational │    │  Learning Loop   │    │  Real-time      │
│  AI Context     │    │  & Pattern       │    │  Data & API     │
│  (10-turn)      │    │  Discovery       │    │  Orchestration  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Built on proven foundations:** PostgreSQL, Redis, Docker, with 599+ tests and 85%+ coverage.

## 📚 Documentation Hub

### 🚀 Get Started (Role-Based)
- **[Product Managers](getting-started/product-managers.md)** - Non-technical setup and workflows
- **[Developers](getting-started/developers.md)** - Complete development environment
- **[API Integration](getting-started/api-integration.md)** - Integrate with your systems
- **[Production Deployment](getting-started/production.md)** - Enterprise deployment

### 📊 Current Status
- **[Status Dashboard](status/README.md)** - Real-time project health and metrics
- **[Achievements 2025](status/achievements-2025.md)** - Feature delivery and impact
- **[Roadmap Q4 2025](status/roadmap.md)** - Current milestones and priorities

### 🔧 Technical Documentation
- **[Architecture Guide](architecture/)** - System design and patterns
- **[API Documentation](api/)** - Complete endpoint reference
- **[Development Guide](development/)** - Contribution and testing

## 🎯 Current Focus - Q4 2025

**Issue Intelligence & Multi-Agent Coordination** - Transform GitHub workflows with AI-powered insights and agent federation.

### Recently Shipped ✅
- **Issue Intelligence System** - AI triage, pattern discovery, CLI commands
- **Enhanced Autonomy** - 4+ hour continuous AI agent operation
- **Test Infrastructure** - Smart test execution with <5 second feedback
- **Documentation Restructure** - Three-tier progressive disclosure

### Active Development 🔄
- **Multi-Agent Orchestration** - Code + Cursor agent coordination
- **UX Excellence Sprint** - Conversational AI with temporal context
- **MCP Ecosystem Hub** - Agent intelligence federation marketplace

## 🤝 Contributing

We welcome contributions! Here's how to get involved:

1. **Quick Start**: Follow the [Developer Setup Guide](getting-started/developers.md)
2. **Find an Issue**: Check our [GitHub Issues](https://github.com/mediajunkie/piper-morgan-product/issues)
3. **Review Guidelines**: See [Development Guide](development/) for patterns and testing
4. **Submit PR**: Follow our Excellence Flywheel methodology

**Key Resources:**
- [Branch Management](development/BRANCH-MANAGEMENT.md)
- [Test Guide](development/TEST-GUIDE.md)
- [Architecture Patterns](architecture/pattern-catalog.md)

## 📄 License & Support

**License**: MIT License - see [LICENSE](LICENSE) file for details.

**Support Channels:**
- **GitHub Issues**: Primary support and bug reports
- **Documentation**: [Complete docs at pmorgan.tech](https://pmorgan.tech)
- **Community**: [GitHub Discussions](https://github.com/mediajunkie/piper-morgan-product/discussions)

---

**Ready to transform your PM workflows?** → **[Get Started Now](getting-started/README.md)**

*Built with ❤️ using the Excellence Flywheel methodology - Verify first → Implement second → Evidence-based progress.*
