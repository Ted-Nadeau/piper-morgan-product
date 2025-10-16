# Piper Morgan - AI Product Management Assistant

[![Build Status](https://github.com/mediajunkie/piper-morgan-product/workflows/test/badge.svg)](https://github.com/mediajunkie/piper-morgan-product/actions)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://pmorgan.tech)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **NEW: Multi-User Configuration System** - Teams can now customize their GitHub repositories, PM number formats, and integration settings. Each user maintains their own configuration while sharing the same Piper Morgan instance.

## 🎯 What is Piper Morgan?

Piper Morgan is an intelligent product management assistant that transforms routine PM tasks into natural conversations while providing strategic insights through AI-powered analysis.

**Core Capabilities:**
- 🗣️ **Natural Language Processing**: Use "that issue", "the document", "my task"
- 🧠 **10-Turn Context Memory**: Remembers your conversation across interactions
- ⚡ **Sub-150ms Response Times**: Lightning-fast conversational AI
- 📊 **Issue Intelligence**: AI-powered GitHub issue analysis and prioritization
- 🎯 **Morning Standup**: Daily accomplishments with real data from all integrations
- 🌐 **Web Interface**: Dark mode UI with 4.6-5.1s generation (faster than CLI)
- 🔧 **Multi-User Configuration**: Teams can customize their own settings

## 🗣️ Natural Language Interface

Piper Morgan uses an intent classification system to understand and route natural language commands through multiple interfaces:

### Supported Interfaces
- **Web API**: POST to `/api/v1/intent` with natural language messages
- **Slack**: Direct messages and mentions in Slack workspace
- **CLI**: Command-line interface for local development
- **Direct**: Python API for programmatic access

### Intent Categories
The system recognizes 13 intent categories, routing to either fast canonical handlers (~1ms) or workflow orchestration (2-3 seconds):

**Quick Response Categories** (Canonical Handlers):
- Identity, Temporal, Status, Priority, Guidance

**Complex Operations** (Workflow Handlers):
- Execution, Analysis, Synthesis, Strategy, Learning, Query, Conversation, Unknown

### Example Usage

```bash
# Web API
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "What's on my calendar today?"}'

# CLI
piper ask "Create a GitHub issue for bug fix"

# Python
from services.intent.intent_service import IntentService
result = await intent_service.process_intent("Show my standup status")
```

### Architecture Documentation
- Full architecture: [ADR-032](docs/internal/architecture/current/adrs/adr-032-intent-classification-universal-entry.md)
- Pattern catalog: [Pattern-032](docs/internal/architecture/current/patterns/pattern-032-intent-pattern-catalog.md)
- Developer guide: [Intent Classification Guide](docs/guides/intent-classification-guide.md)

### Performance
- **Validated**: 126 tests passing, 5 load benchmarks met
- **Throughput**: 600K+ requests/second sustained
- **Cache**: 84.6% hit rate, 7.6x speedup
- **Production**: Deployed and stable

### Classification Accuracy

Piper Morgan's intent classifier achieves 95%+ accuracy for the three most common query types:
- Calendar/Schedule queries (TEMPORAL): 96.7%
- Work Status queries (STATUS): 96.7%
- Priority queries (PRIORITY): 100%

Validated with 140+ query variants across 5 canonical categories (GREAT-4F, October 2025).

---

## ⚠️ API Error Handling

Piper Morgan follows REST principles for error responses with proper HTTP status codes:

- **200 OK**: Request succeeded
- **422 Unprocessable Entity**: Validation error (invalid input)
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Unexpected server error

### Example Error Handling

```python
import requests

response = requests.post("/api/v1/intent", json={"message": "test"})

if response.status_code == 200:
    # Success
    data = response.json()
elif response.status_code == 422:
    # Validation error
    error = response.json()
    print(f"Validation failed: {error['message']}")
elif response.status_code == 404:
    # Not found
    error = response.json()
    print(f"Resource not found: {error['message']}")
elif response.status_code == 500:
    # Internal error
    error = response.json()
    error_id = error.get("details", {}).get("error_id")
    print(f"Server error (ID: {error_id})")
```

### Error Response Format

All errors follow this structure:
```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "User-friendly error message",
  "details": { /* Optional context */ }
}
```

**Documentation**:
- [Complete Error Handling Guide](docs/public/api-reference/api/error-handling.md)
- [Migration Guide](docs/public/migration/error-handling-migration.md)
- [Pattern 034 Reference](docs/internal/architecture/current/patterns/pattern-034-error-handling-standards.md)

---

## 🚀 Quick Start (30 seconds)

```bash
# Clone and setup
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python -m venv venv && source venv/bin/activate

# Install and configure
pip install -r requirements.txt
cp .env.example .env  # Add your API keys

# Launch
docker-compose up -d
python main.py
```

## 📚 Documentation

**Full documentation and guides available at [pmorgan.tech](https://pmorgan.tech)**

### Essential Links
- 🚀 [Getting Started Guide](https://pmorgan.tech) - 15-minute introduction
- ⌨️ [CLI Commands](https://pmorgan.tech) - Command-line interface reference
- 🔧 [Developer Documentation](https://pmorgan.tech) - API and integration guides
- 📖 [Complete Feature List](https://pmorgan.tech) - All capabilities and workflows

## 💬 Example Workflow

```
You: "Update that bug we discussed"
Piper: "✅ Updated issue #1247 (login timeout) status to done"

You: "Show me the latest requirements"
Piper: "📄 Here's requirements_v2.pdf (47 pages, updated 2 days ago)"

You: "Run my morning standup"
Piper: "🌅 Good morning! Here are your accomplishments from yesterday..."
```

## 🌅 Morning Standup Web Interface

**Quick Access**: Start your daily standup with a professional dark mode interface.

### Starting the Server
```bash
# Recommended: Use main.py (initializes services)
python main.py

# Server will start on http://127.0.0.1:8001
```

**Note**: Use `python main.py` instead of `uvicorn` directly. This ensures proper service initialization and dependency injection.

### Access Points
- **Web UI**: http://localhost:8001/standup (dark mode, mobile responsive)
- **API Endpoint**: http://localhost:8001/api/standup (JSON response)
- **API Documentation**: http://localhost:8001/docs (FastAPI auto-docs)

### Performance & Features
- **Generation Time**: 4.6-5.1 seconds (faster than CLI baseline)
- **Response Format**: JSON with comprehensive standup data and metadata
- **UI Features**: Dark mode, mobile responsive, error handling, performance metrics
- **Daily Usage**: Optimized for 6 AM daily standup routine

### What You Get
- ✅ Yesterday's accomplishments from all integrations
- 🎯 Today's priorities with context
- 🚫 Blockers identification
- 📊 Performance metrics and generation time
- 🐙 GitHub activity (commits, PRs, issues)
- 📁 Project context and repository information

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

## 🆘 Support

- **📚 Documentation**: [pmorgan.tech](https://pmorgan.tech)
- **🐛 Issues**: [GitHub Issues](https://github.com/mediajunkie/piper-morgan-product/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/mediajunkie/piper-morgan-product/discussions)

---

**Made with ❤️ by the Piper Morgan team**
