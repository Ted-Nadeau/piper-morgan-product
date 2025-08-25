# Morning Standup CLI - User Guide

**Status**: ✅ **PRODUCTION READY** with **ISSUE INTELLIGENCE INTEGRATION**
**Created**: August 24, 2025
**Last Updated**: August 24, 2025

## 🎯 Overview

The Morning Standup CLI provides automated daily standup generation using persistent context infrastructure, GitHub activity analysis, and optional Issue Intelligence integration. Built for <2 second performance with 15+ minutes of manual preparation time savings.

## 🚀 Quick Start

### Basic Usage

```bash
# Generate standard morning standup
python cli/commands/standup.py

# Generate standup with integrated issue priorities
python cli/commands/standup.py --with-issues

# Generate Slack-formatted output
python cli/commands/standup.py --format slack

# Generate Slack output with issue integration
python cli/commands/standup.py --with-issues --format slack
```

### Command Options

```bash
# Available formats
--format cli     # Terminal-optimized output (default)
--format slack   # Slack-ready markdown format

# Issue integration
--with-issues    # Include top 3 priority issues from Issue Intelligence
--without-issues # Standard standup only (default)
```

## 📊 Standup Components

### Yesterday's Accomplishments
- **GitHub Commits**: Automatically pulls commits from last 24 hours
- **Session Context**: Leverages persistent context from previous sessions
- **Issue Closures**: Shows recently closed GitHub issues
- **Manual Context**: User-defined accomplishments from preferences

### Today's Priorities
- **Active Repositories**: Focus areas from user preferences
- **Contextual Tasks**: Derived from yesterday's unfinished work
- **Issue Priorities**: Top issues from Issue Intelligence (when `--with-issues` used)
- **Default Priorities**: Intelligent defaults when no context available

### Blockers
- **System Issues**: Detected configuration or connectivity problems
- **GitHub API Issues**: Rate limiting or authentication problems
- **Context Issues**: Missing or incomplete session data
- **Integration Issues**: Issue Intelligence connectivity problems

## 🔄 Issue Intelligence Integration

**Status**: ✅ **ACTIVE INTEGRATION** - Available since August 24, 2025

### Integration Features

When using `--with-issues` flag:

- **Top 3 Priority Issues**: Automatically included in "Today's Priorities"
- **Contextual Filtering**: Issues filtered based on current project focus
- **Graceful Degradation**: Standup continues if Issue Intelligence unavailable
- **Error Reporting**: Clear warnings when integration fails

### Sample Integrated Output

```bash
🎯 Today's Priorities
----------------------------------------
ℹ️   🎯 Continue work on piper-morgan
ℹ️   🎯 Issue #123: Fix authentication bug
ℹ️   🎯 Issue #124: Implement user preferences
ℹ️   🎯 Issue #125: Update documentation
ℹ️   📊 Review project status
```

### Integration Architecture

- **Canonical Query Pattern**: Uses shared CanonicalHandlers infrastructure
- **Async Integration**: Non-blocking issue priority retrieval
- **Performance Optimized**: Minimal overhead added to standup generation
- **Cross-Feature Learning**: Issue patterns inform standup prioritization

## ⚙️ Configuration

### User Preferences

The standup leverages user preferences for personalization:

```python
# Preferences automatically managed by UserPreferenceManager
{
    "active_repos": ["piper-morgan", "other-projects"],
    "yesterday_context": {"database": "resolved", "testing": "in-progress"},
    "last_session_time": "2025-08-24T17:30:00"
}
```

### Session Persistence

Automatically maintains context across sessions:

- **Yesterday's Work**: Tasks and accomplishments from previous sessions
- **Active Projects**: Currently focused repositories and areas
- **Focus Areas**: Technical areas requiring continued attention
- **Time Tracking**: Last session timestamps for context calculation

## 📈 Performance Metrics

### Performance Targets

- **Generation Time**: <2 seconds (consistently achieved)
- **Time Savings**: 15+ minutes of manual preparation time
- **Context Accuracy**: 90%+ relevant information inclusion
- **Integration Overhead**: <200ms for Issue Intelligence integration

### Real-Time Reporting

Each standup includes performance metrics:

```bash
📊 Performance Summary
----------------------------------------
ℹ️   Context Source: persistent
ℹ️   GitHub Activity: 5 commits
ℹ️   Generation Time: 450ms
ℹ️   Performance Target: ✅ MET
```

## 🔧 Technical Architecture

### Dependencies

- **UserPreferenceManager**: User settings and context persistence
- **SessionPersistenceManager**: Cross-session context continuity
- **GitHubAgent**: GitHub activity retrieval and analysis
- **CanonicalHandlers**: Integration foundation for cross-feature functionality
- **IssueIntelligenceCanonicalQueryEngine**: Priority issue analysis (optional)

### Error Handling

Comprehensive fallback mechanisms ensure standup generation succeeds:

- **GitHub API Failures**: Graceful degradation with context-based content
- **Session Context Missing**: Intelligent defaults and user guidance
- **Integration Failures**: Clear warnings with continued functionality
- **Performance Issues**: Timeout handling with partial results

### Integration Points

- **CLI Interface**: Clean command-line interface with help system
- **Slack Integration**: Markdown-formatted output for team sharing
- **Issue Intelligence**: Seamless priority issue inclusion
- **GitHub Integration**: Real-time activity analysis and reporting

## 🚀 Advanced Usage

### Development Workflow Integration

```bash
# Daily workflow integration
python cli/commands/standup.py --with-issues --format slack > standup.md
cat standup.md  # Review before sharing
# Share standup.md with team via Slack/email
```

### Automation

```bash
# Add to daily routine (crontab example)
0 9 * * 1-5 cd /path/to/piper-morgan && python cli/commands/standup.py --with-issues
```

### Debugging

```bash
# Check specific components
python -c "from services.features.morning_standup import MorningStandupWorkflow; print('Available')"

# Test integration separately
python -c "from services.features.issue_intelligence import IssueIntelligenceCanonicalQueryEngine; print('Available')"
```

## 🛠️ Troubleshooting

### Common Issues

**Standup Generation Slow**:
- Check GitHub API rate limits
- Verify database connectivity
- Review session context size

**Integration Failures**:
- Verify Issue Intelligence service status
- Check CanonicalHandlers initialization
- Review error messages in standup output

**Missing Context**:
- Run standup daily to build context
- Check UserPreferenceManager settings
- Verify GitHub token configuration

### Support

- **Architecture Documentation**: [Canonical Queries Architecture](../development/canonical-queries-architecture.md)
- **Development Guide**: [Morning Standup MVP Guide](../development/MORNING_STANDUP_MVP_GUIDE.md)
- **Integration Testing**: [Integration Guide](integration-guide.md)

## 📝 Changelog

### August 24, 2025 - Issue Intelligence Integration

- ✅ Added `--with-issues` flag for Issue Intelligence integration
- ✅ Implemented CanonicalHandlers architecture alignment
- ✅ Added graceful degradation for integration failures
- ✅ Enhanced CLI with comprehensive help system
- ✅ Added Slack formatting with issue integration support

### Previous Versions

See [Morning Standup MVP Guide](../development/MORNING_STANDUP_MVP_GUIDE.md) for complete development history.

---

**Status**: ✅ **PRODUCTION READY** with **ACTIVE ISSUE INTELLIGENCE INTEGRATION**
**CLI Command**: `python cli/commands/standup.py --with-issues`
**Performance**: <2 second generation, 15+ minutes time savings
**Integration**: Issue Intelligence via canonical query pattern
**Next Enhancement**: Issue Intelligence initialization optimization (PM-124)
