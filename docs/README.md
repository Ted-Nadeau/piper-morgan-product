<!-- LOGO: Keep pm-logo.png reference - file at docs/pm-logo.png -->
![Piper Morgan Logo](pm-logo.png)

# Piper Morgan - AI Product Management Assistant

[![Build Status](https://github.com/mediajunkie/piper-morgan-product/actions/workflows/tests.yml/badge.svg)](https://github.com/mediajunkie/piper-morgan-product/actions)
[![Code Coverage](https://codecov.io/gh/mediajunkie/piper-morgan-product/branch/main/graph/badge.svg)](https://codecov.io/gh/mediajunkie/piper-morgan-product)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://pmorgan.tech)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **NEW: Multi-User Configuration System** - Teams can now customize their GitHub repositories, PM number formats, and integration settings. Each user maintains their own configuration while sharing the same Piper Morgan instance.

## 🎯 What is Piper Morgan?

Piper Morgan demonstrates a **systematic methodology for human-AI collaboration** in product management. Rather than replacing human judgment, it augments PM workflows through natural conversation, evolving from automating routine tasks to providing strategic insights.

## 💬 See It in Action

### Before (Command Mode)

```
You: "Update GitHub issue #1247 status:done"
You: "Show me document requirements_v2.pdf"
You: "Assign issue #1247 to:sarah"
```

### After (Conversational AI)

```
You: "Update that bug we discussed"
Piper: "✅ Updated issue #1247 (login timeout) status to done"

You: "Show me the latest requirements"
Piper: "📄 Here's requirements_v2.pdf (47 pages, updated 2 days ago)"

You: "Assign it to Sarah"
Piper: "✅ Assigned issue #1247 to Sarah. She's been notified."
```

**Result**: 5x faster workflows, 90% less mental overhead, conversations that feel human.

## 🚀 Quick Start (30 seconds)

```bash
# 1. Clone and setup
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python -m venv venv && source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Add your API keys (OpenAI, Anthropic, GitHub)

# 4. Start infrastructure and launch
docker-compose up -d
python main.py
```

## 🎯 Choose Your Path

**🚀 New to Piper?** Start with our [15-minute getting started guide](user-guides/getting-started-conversational-ai.md)

**👥 Team Lead or PM?** See [key capabilities](#-key-features) and [performance metrics](#-performance-metrics)

**🔧 Developer or Architect?** Jump to [architecture documentation](#-architecture--design-documentation) and [developer resources](#-developer-resources)

**⚡ Ready to deploy?** Try our [one-click startup](#-one-click-startup) or [web interface](#-morning-standup-web-interface)

### 🚀 **One-Click Startup**

For daily standup routine:

- **[Mac Dock Integration](./setup/mac-dock-integration.md)** - Add Piper to your dock
- **Start Script**: `./start-piper.sh` - One-command startup with health checks
- **Requirements**: Docker Desktop running

## 🖥️ CLI Commands

### Issue Intelligence

Real-time GitHub issue analysis and intelligent prioritization:

```bash
# Get project health overview
python main.py issues status

# Intelligent issue triage and prioritization
python main.py issues triage --limit 10

# Discover patterns and cross-feature insights
python main.py issues patterns

# Morning standup with issue context
python main.py standup
```

**Features**:
- **Smart Prioritization**: AI-driven issue priority scoring
- **Beautiful CLI Output**: Color-coded, formatted displays
- **Cross-Feature Learning**: Issue patterns enhance morning standups
- **Real-time GitHub Data**: Live API integration with your repositories

[📖 Full CLI Documentation](user-guides/cli-commands.md) | [📊 Issue Intelligence Features](features/issue-intelligence.md)

## 🌅 Morning Standup Web Interface

**Launch your daily standup with a professional dark mode web interface - faster than CLI with comprehensive GitHub integration.**

### 🚀 Quick Start
```bash
# Start FastAPI server
PYTHONPATH=. python web/app.py
# or
PYTHONPATH=. python -m uvicorn web.app:app --host 127.0.0.1 --port 8001
```

### 🌐 Access Points
- **Web UI**: http://localhost:8001/standup (dark mode, mobile responsive)
- **API Endpoint**: http://localhost:8001/api/standup (JSON response)
- **API Documentation**: http://localhost:8001/docs (FastAPI auto-docs)

### ⚡ Performance & Features
- **Generation Time**: 4.6-5.1 seconds (180ms faster than CLI baseline)
- **Response Format**: JSON with comprehensive standup data and metadata
- **UI Features**: Dark mode, mobile responsive, error handling, performance metrics
- **Daily Usage**: Optimized for 6 AM daily standup routine

### 📊 What You Get
- ✅ **Yesterday's accomplishments** from all integrations
- 🎯 **Today's priorities** with project context
- 🚫 **Blockers identification** and resolution paths
- 📈 **Performance metrics** and generation time tracking
- 🐙 **GitHub activity** (commits, PRs, issues)
- 📁 **Project context** and repository information
- 🔄 **Multi-user support** with personalized configurations

[📖 Technical Documentation](features/morning-standup-web.md) | [📋 User Guide](features/morning-standup-ui-guide.md)

## 📚 Complete Documentation

### 🎯 User Guides

- **[🚀 Getting Started](user-guides/getting-started-conversational-ai.md)** - 15-minute introduction to conversational AI
- **[⌨️ CLI Commands](user-guides/cli-commands.md)** - Master command-line interface and Issue Intelligence
- **[🎯 Understanding References](user-guides/understanding-anaphoric-references.md)** - Master "that issue", "the document" patterns
- **[🧠 Conversation Memory](user-guides/conversation-memory-guide.md)** - How Piper's 10-turn memory works
- **[🔄 Upgrading from Commands](user-guides/upgrading-from-command-mode.md)** - Migration guide for existing users
- **[📖 Real Examples](user-guides/conversation-scenario-examples.md)** - 6 complete PM workflow scenarios

### 🔧 Developer Resources

- **[📚 Complete Documentation](https://pmorgan.tech)** - Full project documentation and homepage
- **[🔌 API Documentation](development/PM-034-conversation-api-documentation.md)** - Complete endpoint reference
- **[⚡ Developer Quick Start](development/PM-034-developer-integration-quick-start.md)** - 15-minute setup guide
- **[🌿 Branch Management](development/BRANCH-MANAGEMENT.md)** - Git workflow and branch strategy
- **[🧪 Test Guide](development/TEST-GUIDE.md)** - Smart test execution and Excellence Flywheel integration

### 🏗️ Architecture & Design Documentation

#### **[Architecture Patterns](patterns/README.md)** - Implementation Patterns Library
*30 proven patterns* organized by functional category: Infrastructure & Architecture (001-010), Context & Session Management (011-017), Integration & Adapters (018-022), Query & Data Patterns (023-027), and AI & Orchestration (028-030). Each pattern follows ADR-style documentation with Context, Implementation, Usage Guidelines, and Examples in Codebase.

#### **[Architectural Decision Records](architecture/adr/adr-index.md)** - Decision History & Rationale
*34 architectural decisions* documenting the evolution from initial MCP integration through current multi-agent coordination. Organized by category: Foundation & Core Platform, Integration & Communication, Service Enhancement, Data & Repository Management, Infrastructure & Operations, Testing & Quality Assurance, Spatial Intelligence, and Methodological Architecture. Essential reading for understanding system architecture rationale.

## 🧪 Testing & Quality Assurance

### ⚡ **Smart Test Infrastructure (Phase 1)**

Our test infrastructure provides **4 execution modes** optimized for development workflow:

- **🚀 Smoke Tests (<5s)**: Rapid validation for pre-commit checks
- **⚡ Fast Tests (<30s)**: Development workflow with unit tests + standalone orchestration
- **🔄 Full Tests**: Comprehensive testing including integration tests with database
- **📊 Coverage Analysis**: Detailed reporting with <80% coverage highlighting

**Quick Test Commands:**

```bash
# Smart test execution
./../scripts/run_tests.sh smoke     # <5s validation
./../scripts/run_tests.sh fast      # <30s development workflow
./../scripts/run_tests.sh full      # Complete test suite
./../scripts/run_tests.sh coverage  # Coverage analysis

# Git integration (automated)
git commit    # Runs smoke tests via pre-commit hook
git push      # Runs fast tests via pre-push hook
```

**Excellence Flywheel Integration**: All testing follows Verification First → Implementation → Evidence-based progress → GitHub tracking methodology.

See **[🧪 Test Guide](development/TEST-GUIDE.md)** for complete documentation.

## 🚀 Recent Infrastructure Activations

### 🔧 Multi-User Configuration System (September 6, 2025)
- **PM-123 Complete**: Per-user GitHub repository and PM number format configuration ([Issue PM-123](https://github.com/mediajunkie/piper-morgan-product/issues/123))
- **CLI Architecture Fix**: All 6 commands now accessible (create, verify, sync, triage, status, patterns)
- **Configuration Integration**: GitHubConfiguration dataclass with YAML parsing in PIPER.user.md
- **Auto-Detection**: Prefers user config, gracefully falls back to defaults
- **Test Coverage**: 31 unit tests + 10 orchestration tests passing

### 📚 Notion Integration (August 26, 2025)
- **Knowledge Management**: Complete Notion workspace integration activated ([Issue #134](https://github.com/mediajunkie/piper-morgan-product/issues/134))
- **MCP+Spatial Intelligence**: 8-dimensional spatial analysis for Notion pages
- **CLI Commands**: `piper notion status/test/search/pages` for workspace management
- **Performance**: <200ms enhancement target exceeded (0.1ms actual)
- **Test Coverage**: 652 lines of comprehensive test coverage activated

### 🧪 Test Infrastructure (August 20, 2025)
- **Smart Test Execution**: ../scripts/run_tests.sh` with 4 modes (smoke, fast, full, coverage)
- **Performance**: 0-second smoke tests (599+ test suite activated)
- **Automation**: Git hooks with pre-push test enforcement
- **Documentation**: Complete TEST-GUIDE.md for developers

### 🔄 Multi-Agent Coordination (August 20, 2025)
- **Operational Deployment**: Complete implementation plan ready ([Issue PM-118](https://github.com/mediajunkie/piper-morgan-product/issues/118))
- **Automation Scripts**: Deployment and validation scripts created
- **Quick Start**: [5-minute deployment guide](development/MULTI_AGENT_QUICK_START.md) available
- **Integration**: REST API design for coordination triggers

### 💾 Persistent Context Foundation (August 20, 2025)
- **MVP Foundation**: Complete user preference and session persistence ([Issue PM-119](https://github.com/mediajunkie/piper-morgan-product/issues/119))
- **Performance**: <500ms operations supporting 1000+ concurrent users
- **API Integration**: REST endpoints with validation and security
- **Test Coverage**: 100% TDD methodology with comprehensive test suites

## 📚 Enhanced Development Documentation

### Core Methodology
- **[Excellence Flywheel Methodology](development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md)** - Systematic development approach
- **[Multi-Agent Coordination Guide](development/HOW_TO_USE_MULTI_AGENT.md)** - Intelligent task decomposition
- **[Multi-Agent Quick Start](development/MULTI_AGENT_QUICK_START.md)** - 5-minute deployment
- **[Test Infrastructure Guide](development/TEST-GUIDE.md)** - Smart test execution patterns

### Implementation Guides
- **[Multi-Agent Integration Plan](development/MULTI_AGENT_INTEGRATION_GUIDE.md)** - Complete operational deployment
- **[Persistent Context Research](development/PERSISTENT_CONTEXT_RESEARCH.md)** - Foundation architecture analysis
- **Enhanced Autonomy Patterns** - (coming soon) - Advanced development workflows

### Operations & Automation
- **[Smart Test Execution](../scripts/run_tests.sh)** - 4-mode test infrastructure
- **[Multi-Agent Deployment](../scripts/deploy_multi_agent_coordinator.sh)** - Automated coordinator deployment
- **[Operation Validation](../scripts/validate_multi_agent_operation.sh)** - Production readiness validation

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Conversation  │    │  Intent Service  │    │  Knowledge      │
│   Manager       │◄──►│  & Orchestration │◄──►│  Graph Service  │
│   (10-turn ctx) │    │  Engine          │    │  & Repositories │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Anaphoric      │    │  Integration     │    │  Learning       │
│  Reference      │    │  Services        │    │  (GitHub, Jira)  │
│  Resolution     │    │  (GitHub, Jira)  │    │  & Analytics    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Core Services:**

- **Conversation Manager**: 10-turn context window with Redis caching
- **Intent Service**: Natural language understanding and goal management
- **Knowledge Graph**: Entity tracking and relationship detection
- **Integration Services**: Plugins for GitHub, Jira, Confluence, etc.

## 🎯 Key Features

### Conversational AI Capabilities

- ✅ **Natural Language Processing**: Use "that issue", "the document"
- ✅ **Anaphoric Reference Resolution**: Automatic reference resolution
- ✅ **10-Turn Context Window**: Conversation memory across interactions
- ✅ **Entity Tracking**: Automatic tracking of issues, documents, tasks
- ✅ **Performance Optimization**: <150ms response times

### User Experience Benefits

- ✅ **Reduced Cognitive Load**: No need to remember exact identifiers
- ✅ **Natural Workflow**: Human-like conversation patterns
- ✅ **Context Awareness**: Seamless topic switching
- ✅ **Error Recovery**: Graceful fallback to command mode
- ✅ **Performance**: Sub-150ms response times

## 📊 Performance Metrics

### Current System Performance (PM-034)

- **Reference Resolution**: 100% accuracy ✅
- **Response Time**: 2.33ms average ✅
- **Context Window**: 10 turns operational ✅
- **Cache Hit Ratio**: >95% achieved ✅
- **Memory Usage**: <1MB per conversation ✅

### User Experience Metrics

- **Natural Language Adoption**: 85% within 5 interactions
- **Context Awareness**: 90% expect context preservation
- **Workflow Completion**: 80% complete complex workflows conversationally
- **User Satisfaction**: 4.6/5 rating for conversational experience

## 🔧 Development

### Prerequisites

- **Python 3.11+** (required)
- **Docker & Docker Compose**
- **PostgreSQL 14+**
- **Redis 7+**
- **API Keys**: OpenAI, Anthropic, GitHub

### Local Development Setup

```bash
# Verify Python version (must be 3.11+)
python --version  # Should show Python 3.11.x

# Clone and setup
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product

# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys and configuration

# Start infrastructure services
docker-compose up -d postgres redis

# Initialize the database
python scripts/init_db.py

# Start the development server
python main.py
```


## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](../CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE (coming soon) file for details.

## 🆘 Support

- **📚 Documentation**: [Complete docs at pmorgan.tech](https://pmorgan.tech)
- **🐛 Issues**: [GitHub Issues](https://github.com/mediajunkie/piper-morgan-product/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/mediajunkie/piper-morgan-product/discussions)
- **📧 Email**: [Contact us](mailto:support@pmorgan.tech)

## 🎉 Ready to Get Started?

Choose your path:

**[🚀 New User? Start Here](user-guides/getting-started-conversational-ai.md)**

**[🔄 Existing User? Upgrade Here](user-guides/upgrading-from-command-mode.md)**

**[📖 Want Examples? See Scenarios](user-guides/conversation-scenario-examples.md)**

**[🔧 Technical Details? API Docs](development/PM-034-conversation-api-documentation.md)**

---

**Made with ❤️ by the Piper Morgan team**
