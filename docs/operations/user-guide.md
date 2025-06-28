# Piper Morgan 1.0 - User Guide

## Getting Started

### System Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for AI services
- GitHub account for issue creation (when using GitHub features)

### Accessing Piper Morgan

#### Web Interface (PM-011 Release)
The primary way to interact with Piper Morgan is through the web chat interface:

1. Open your browser to `http://localhost:8501`
2. You'll see a chat interface with example prompts
3. Type or select a request to begin

#### API Access (Advanced Users)
For programmatic access or testing:
```bash
# Test system health
curl http://localhost:8001/health

# Submit a request via API
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message":"Create a GitHub issue for mobile app login problems"}'
```

## Using the Web Interface

### Chat Interaction
The web interface provides a conversational experience:

1. **Type your request** in natural language
2. **View AI response** with structured output
3. **See workflow progress** in real-time
4. **Review results** before taking action

### File Upload
Upload documents to build your knowledge base:

1. Click the **Upload Document** button
2. Select PDF, TXT, MD, or DOCX files (up to 50MB)
3. Wait for processing confirmation
4. Your documents are now searchable

### Example Interactions

**Creating GitHub Issues**:
- "Create a bug report for the mobile app crashing during photo upload"
- "Make a feature request for dark mode in the settings page"
- "Draft an issue about slow performance on the dashboard"

**Knowledge Queries**:
- "What did we decide about the authentication architecture?"
- "Summarize the Q3 product roadmap"
- "Find requirements for the payment integration"

**Project Analysis**:
- "Review recent GitHub issues and identify patterns"
- "What are the top priority items in our backlog?"
- "Analyze user feedback from the last sprint"

## Core Capabilities

### 1. Natural Language Understanding
Piper Morgan interprets PM requests with context awareness:
- Understands technical and business terminology
- Infers intent from conversational language
- Asks clarifying questions when needed
- Maintains context across conversations

**Current Accuracy**: 85-95% for common PM tasks

### 2. Knowledge Base Integration
Your organizational knowledge becomes searchable:
- **Document Types**: PDF, DOCX, TXT, Markdown
- **Smart Search**: Semantic understanding, not just keywords
- **Context Injection**: Relevant knowledge automatically included
- **Source Attribution**: Always shows where information came from

### 3. GitHub Integration (70% Complete)
Create and manage GitHub issues:
- **Issue Creation**: Professional formatting with structure
- **Smart Labels**: Automatic categorization
- **Priority Assignment**: Based on impact description
- **Technical Context**: Includes implementation guidance

**Note**: Full GitHub workflow automation coming in next release

### 4. Workflow Orchestration
Multi-step processes handled automatically:
- Parse natural language request
- Search relevant knowledge
- Generate structured output
- Execute external actions
- Provide status updates

## Best Practices

### Writing Effective Requests

✅ **Good Examples**:
- "Create a high-priority bug report: Users on iOS 15 experience crashes when uploading photos larger than 10MB. This affects 15% of our mobile users."
- "Review our API documentation and create issues for any missing authentication endpoints"
- "What were the key decisions from last week's architecture review?"

❌ **Poor Examples**:
- "Fix the app" (too vague)
- "Create ticket" (missing context)
- "Help" (no specific request)

### Knowledge Base Management

1. **Upload Quality Documents**:
   - Well-structured with clear headings
   - Up-to-date information
   - Consistent formatting

2. **Organize by Project**:
   - Use clear file names
   - Include dates in documents
   - Remove outdated versions

3. **Regular Maintenance**:
   - Review and update quarterly
   - Remove contradictory information
   - Add new decisions and learnings

### Maximizing Accuracy

1. **Provide Context**: Include project name, component, or team
2. **Be Specific**: Mention versions, percentages, user segments
3. **Use Consistent Terms**: Stick to your team's vocabulary
4. **Verify Output**: Always review AI-generated content

## Current Limitations

### System Constraints
- **Single User**: No authentication or multi-user support yet
- **Local Only**: Not accessible outside your machine
- **Learning**: Doesn't yet learn from your corrections
- **Integrations**: Only GitHub partially implemented

### Quality Considerations
- **Response Time**: 2-6 seconds for complex requests
- **Knowledge Search**: Relevance varies with document quality
- **Error Recovery**: Limited automatic retry mechanisms
- **Context Length**: Very long conversations may lose context

## Troubleshooting

### Web Interface Issues

**Page Won't Load**:
```bash
# Check if Streamlit is running
ps aux | grep streamlit

# Restart the web interface
cd web && python app.py
```

**Upload Failures**:
- Check file size (< 50MB)
- Verify file format (PDF, DOCX, TXT, MD)
- Ensure ChromaDB is running

**Slow Responses**:
- Normal for complex requests (2-6 seconds)
- Check API keys are valid
- Verify all Docker services are healthy

### Chat Issues

**"Service Unavailable"**:
1. Check API server: `curl http://localhost:8001/health`
2. Verify Docker services: `docker-compose ps`
3. Check logs: `docker-compose logs`

**Poor Quality Responses**:
1. Upload more relevant documents
2. Use more specific language
3. Break complex requests into steps
4. Check knowledge base quality

### Getting Help
1. Check system status in terminal logs
2. Review error messages in web interface
3. Consult [Deployment Guide](deployment.md) for setup issues
4. See [Configuration Guide](configuration.md) for settings

## Roadmap & Future Features

### Next Release (Q3 2025)
- ✅ User authentication and sessions
- ✅ Complete GitHub integration
- ✅ Multi-project support
- ✅ Learning from user feedback

### Future Vision
- **Multi-System Integration**: Jira, Slack, Analytics
- **Predictive Insights**: Sprint planning assistance
- **Team Collaboration**: Shared knowledge bases
- **Advanced Automation**: Complex workflow chains

## Providing Feedback

Your feedback shapes Piper Morgan's development:

1. **Report Issues**: Note specific errors or unexpected behavior
2. **Suggest Features**: What would make your PM work easier?
3. **Share Success**: What tasks work well?
4. **Accuracy Feedback**: Rate response quality

Currently, feedback is collected manually through GitHub issues or direct communication.

---
*Last Updated: June 27, 2025*

## Revision Log
- **June 27, 2025**: Complete rewrite for PM-011 web interface, removed API-only warnings, added chat UI documentation
