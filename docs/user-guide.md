# Piper Morgan 1.0 - User Guide

## Getting Started

### System Requirements

- Web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for AI services
- GitHub account for issue creation

### Current Limitations

⚠️ **Important**: Piper Morgan is currently in development phase with some limitations:

- Database persistence issues (workflows lost on restart)
- GitHub integration not implemented
- Single-user system only

#### Web Interface (Current)

**New Feature:** The chat window is now vertically resizable. You can drag the bottom edge of the chat window to adjust its height, with a minimum and maximum limit. If the content exceeds the visible area, a scrollbar will appear automatically.

Piper Morgan now includes a DDD-compliant, test-driven web chat interface:

- Chat-based conversational UI for natural language requests
- Real-time workflow status and progress updates
- File upload for knowledge base documents
- Unified feedback and actionable error messages

To use the web interface:

1. Open your browser and navigate to the Piper Morgan web UI (URL provided by your deployment).
2. Enter your request in the chat box (e.g., "Create a ticket for the login bug affecting mobile users").
3. View real-time responses, workflow progress, and results directly in the chat window.
4. Upload documents to the knowledge base using the upload section.

**Technical Note:**
All bot message rendering and response handling is unified in a shared domain module (`bot-message-renderer.js`), ensuring a consistent user experience and robust error handling. The UI is fully covered by automated tests (TDD).

## Core Capabilities

### 1. Natural Language Intent Understanding

Piper Morgan can interpret PM requests like:

- "Create a ticket for the login bug affecting mobile users"
- "Review the requirements document and summarize key points"
- "What were the main decisions from the Q3 retrospective?"

**Quality Note**: Intent classification accuracy varies 60-85% depending on request clarity.

### 2. Knowledge Base Integration

The system can:

- Ingest documents (PDF, DOCX, TXT, MD)
- Search organizational knowledge for context
- Reference historical decisions and documentation

**Quality Note**: Search relevance inconsistent and requires tuning.

### 3. Workflow Orchestration (Planned)

When complete, the system will:

- Create GitHub issues from natural language
- Execute multi-step PM workflows
- Coordinate across multiple external systems

**Status**: Framework exists but execution loop incomplete.

## Usage Patterns

### Document Upload and Knowledge Building

```bash
# Upload document (when web UI available)
# Currently requires manual file placement in knowledge base directory
```

### GitHub Issue Creation

```bash
# Request issue creation
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Users report that the mobile app crashes when uploading photos larger than 10MB. This affects iOS and Android. Priority should be high since it blocks core functionality."
  }'
```

Expected output (when GitHub integration complete):

- Professional GitHub issue title
- Structured description with acceptance criteria
- Appropriate labels and priority assignment
- Technical implementation guidance

### Knowledge Queries

```bash
# Query organizational knowledge
curl "http://localhost:8001/api/v1/knowledge/search?q=mobile+login+architecture&k=3"
```

## Best Practices

### Writing Effective Requests

**Good Examples:**

- "Create a bug report for mobile app crashes during photo upload on iOS, affecting 15% of users"
- "Review the API documentation and identify missing authentication requirements"

**Poor Examples:**

- "Fix the app" (too vague)
- "Create ticket" (missing context)

### Knowledge Base Management

1. **Document Quality**: Upload well-structured documents with clear headings
2. **Metadata**: Include project, date, and document type information
3. **Regular Updates**: Keep knowledge base current with recent decisions
4. **Curation**: Remove outdated or contradictory information

### Workflow Optimization

1. **Context Provision**: Include relevant background in requests
2. **Specificity**: Be specific about requirements and constraints
3. **Verification**: Always review AI-generated content before use
4. **Feedback**: Provide corrections to improve future suggestions

## Troubleshooting

### Common Issues

1. **System Unavailable**: Check if Docker services are running
2. **Slow Responses**: AI processing can take 3-6 seconds
3. **Irrelevant Results**: Knowledge base search quality varies
4. **Failed Workflows**: Workflow persistence currently broken

### Getting Help

1. Check system health: `curl http://localhost:8001/health`
2. Review Docker logs: `docker-compose logs`
3. Verify API keys in environment configuration
4. See [Deployment Guide](../operations/deployment.md) for setup issues

## Future Capabilities

### Planned Features

- **Web User Interface**: Chat-based interaction
- **Learning Mechanisms**: Improvement through user feedback
- **Multi-System Integration**: Jira, Slack, analytics platforms
- **Advanced Workflows**: Complex multi-step automation

### Long-term Vision

- **Strategic Insights**: AI-powered product recommendations
- **Predictive Analytics**: Timeline and risk prediction
- **Autonomous Operation**: Self-improving workflow execution
- **Organizational Learning**: Cross-team knowledge sharing

## Feedback and Support

### Providing Feedback

Current system limitations make user feedback collection manual:

1. Document specific issues encountered
2. Note accuracy of AI responses
3. Record time saved or lost using the system
4. Suggest specific improvements needed

### System Status

For current development status, see:

- [One-Page Summary](../one-pager.md) - Current capabilities and gaps
- [Roadmap](../development/roadmap.md) - Development timeline
- [Backlog](../development/backlog.md) - Detailed feature status

This user guide will be updated as system capabilities evolve and mature.

---

_Last Updated: June 27, 2025_

## Revision Log

- **June 27, 2025**: Added systematic documentation dating and revision tracking
