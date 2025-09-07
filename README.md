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
- 🔧 **Multi-User Configuration**: Teams can customize their own settings

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

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

## 🆘 Support

- **📚 Documentation**: [pmorgan.tech](https://pmorgan.tech)
- **🐛 Issues**: [GitHub Issues](https://github.com/mediajunkie/piper-morgan-product/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/mediajunkie/piper-morgan-product/discussions)

---

**Made with ❤️ by the Piper Morgan team**
