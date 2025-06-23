# Piper Morgan 1.0 - User Guide

## Getting Started

### System Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for AI services
- GitHub account (optional, for issue creation when implemented)

### Current Capabilities
✅ **Web Chat Interface**: Conversational interaction with real-time updates
✅ **Natural Language Understanding**: 95%+ accuracy on PM tasks with organizational context
✅ **Multi-Project Support**: Sophisticated context resolution across projects
✅ **Knowledge Base Integration**: Search 85+ organizational documents
✅ **Error Handling**: User-friendly error messages with recovery guidance

### Development Status
⚠️ **Important**: Piper Morgan is in active development with some workflows incomplete:
- **GitHub Integration**: Framework ready, issue creation 70% complete
- **Workflow Persistence**: State doesn't survive system restarts
- **Learning Mechanisms**: Event capture working, analysis in progress
- **Multi-User Support**: Single-user system currently

## Accessing Piper Morgan

### Web Interface (Primary Method)
1. **Navigate to**: `http://localhost:8001` (or configured domain)
2. **Chat Interface**: Conversational interaction in the main area
3. **File Upload**: Drag and drop documents to expand knowledge base
4. **Real-Time Updates**: Workflow status updates automatically

### Web Interface Features
- **Message History**: Full conversation context maintained
- **Typing Indicators**: Shows when AI is processing
- **Error Recovery**: Clear guidance when issues occur
- **File Management**: Upload documents directly to knowledge base
- **Status Tracking**: See workflow progress in real-time

## Core Capabilities

### 1. Natural Language Intent Understanding
Piper Morgan interprets PM requests using organizational context:

**Examples of what works well:**
- "Create a GitHub issue for the mobile app login crash affecting iOS users"
- "Search our documentation for API rate limiting decisions"
- "What project context should I use for this mobile bug report?"
- "List all active projects in the system"

**Quality**: 95%+ accuracy on PM-specific tasks when organizational context is available.

### 2. Multi-Project Context Resolution
The system intelligently determines which project you're working on:

**Resolution Hierarchy:**
1. **Explicit mention**: "Create a ticket in the Mobile App project"
2. **Session memory**: Remembers your last confirmed project choice
3. **AI inference**: Analyzes message content to infer project context
4. **Default fallback**: Uses configured default project

**Example Interaction:**
```
You: "Create a bug report for the login crash"
Piper: "I see you're referring to a login issue. Should I create this in the Mobile App project based on our previous conversation?"
You: "Yes"
Piper: [Creates issue in Mobile App project and remembers choice for session]
```

### 3. Knowledge Base Integration
Search and reference organizational knowledge automatically:

**Supported Formats**: PDF, DOCX, TXT, MD files
**Search Types**: 
- Semantic search (finds content by meaning)
- Keyword search (finds exact terms)
- Contextual search (considers current conversation)

**Knowledge Hierarchy:**
- **PM Fundamentals**: Core methodology and best practices
- **Business Context**: Company and industry specifics  
- **Product Context**: Product details and history
- **Task Context**: Specific implementation patterns

### 4. Error Handling & Recovery
When things go wrong, Piper Morgan provides actionable guidance:

**Example Error Response:**
```
Error: Project not found
Message: I couldn't find a project called "MobileApp". 
Try: "list projects" to see available options, or check the spelling.
Recovery Actions: [List Projects] [Create Project]
```

## Usage Patterns

### Starting a Conversation
**Good Opening Messages:**
- "List all active projects"
- "What was the main decision about user authentication?"
- "Create a bug report for the photo upload issue"
- "Search for documentation about our API rate limits"

**Less Effective:**
- "Help" (too vague)
- "Fix the bug" (missing context)
- "What should I do?" (no specific request)

### Creating GitHub Issues (In Development)
When GitHub integration is complete, you'll be able to:

```
You: "Create a GitHub issue for users reporting that the mobile app crashes when uploading photos larger than 10MB. This affects iOS and Android. Priority should be high since it blocks core functionality."

Piper: [Analyzes request, searches knowledge for context]
"I'll create a GitHub issue with the following details:
- Title: Mobile app crashes on large photo uploads (>10MB)  
- Description: [Structured format with acceptance criteria]
- Labels: bug, mobile, high-priority, ios, android
- Project: Mobile App (based on context)

Should I proceed with creating this issue?"
```

### Knowledge Base Management
**Uploading Documents:**
1. Use the file upload area in the web interface
2. Drag and drop supported file types
3. System automatically processes and indexes content
4. Documents become searchable within minutes

**Best Practices:**
- Upload well-structured documents with clear headings
- Include project and date information in filenames
- Remove outdated or contradictory information
- Use descriptive document titles

**Searching Knowledge:**
- "What did we decide about user authentication in Q3?"
- "Find documentation about mobile app architecture"
- "Search for previous decisions about API versioning"

## Advanced Features

### Project Context Management
**Switching Projects:**
```
You: "Switch to Mobile App project"
Piper: "I've switched context to the Mobile App project. Future requests will use this context unless specified otherwise."
```

**Creating New Projects:**
```
You: "Create a new project called Web Dashboard"
Piper: "I'll create a new project called Web Dashboard. Should this be set as your default project for this session?"
```

### Clarifying Questions
When requests are ambiguous, Piper Morgan asks for clarification:

```
You: "Create a ticket for the API issue"
Piper: "I found several API-related contexts in our knowledge base. Which API are you referring to:
1. User Authentication API
2. Payment Processing API  
3. File Upload API
Or would you like me to create a general API issue?"
```

### Workflow Status Tracking
The interface shows real-time progress for complex operations:
- **Processing**: AI analyzing your request
- **Searching**: Looking through knowledge base
- **Creating**: Building workflow steps
- **Executing**: Running external integrations
- **Complete**: Task finished with results

## Best Practices

### Writing Effective Requests

**✅ Good Examples:**
- "Create a bug report for mobile app crashes during photo upload on iOS, affecting 15% of users based on analytics"
- "Search our architecture docs for authentication flow decisions made in Q2"
- "What project should I use for reporting API rate limit issues?"

**❌ Poor Examples:**
- "Fix the app" (too vague, no context)
- "Create ticket" (missing problem description)
- "Help me" (no specific request)

### Providing Context
**Include relevant details:**
- Which platform/component is affected
- User impact and frequency
- Any error messages or symptoms
- Previous related work or decisions

**Reference organizational knowledge:**
- "Based on our previous mobile architecture decisions..."
- "Following the pattern we used for the payment flow..."
- "Similar to the issue we resolved in Q1..."

### Workflow Optimization
1. **Be specific**: Include requirements, constraints, and success criteria
2. **Verify results**: Always review AI-generated content before using
3. **Provide feedback**: Correct mistakes to improve future responses
4. **Use session memory**: Build on previous conversation context

## Troubleshooting

### Common Issues

1. **Web interface not loading**
   - Check if system is running: `docker-compose ps`
   - Verify API server: `curl http://localhost:8001/health`
   - Clear browser cache and refresh

2. **Slow responses (3-6 seconds)**
   - Normal for AI processing with knowledge search
   - Larger knowledge base searches take longer
   - Network latency affects external API calls

3. **Irrelevant search results**
   - Knowledge base search quality varies
   - Try more specific keywords
   - Upload more relevant documentation
   - Rephrase your request with different terms

4. **Project context confusion**
   - Explicitly specify project: "In the Mobile App project, create..."
   - List projects: "What projects are available?"
   - Reset context: "Switch to [project name]"

5. **Error messages**
   - Follow recovery actions suggested in error responses
   - Check if required services are running
   - Verify API keys are configured

### Getting Help

1. **System Status**: Check `http://localhost:8001/health`
2. **Service Logs**: `docker-compose logs -f`  
3. **Database Issues**: `python scripts/check_db.py`
4. **Knowledge Base**: Try uploading relevant documentation

## Current Limitations

### Workflow Limitations
- **GitHub Issues**: Can plan but not yet create actual issues
- **State Persistence**: Workflows lost on system restart
- **Multi-step Operations**: Complex workflows not fully implemented
- **Bulk Operations**: No batch processing capabilities

### Knowledge Limitations
- **Search Relevance**: Quality varies, requires tuning
- **Document Updates**: No automatic refresh when documents change
- **Version Control**: No tracking of document versions
- **Duplicate Handling**: May return similar content multiple times

### System Limitations
- **Single User**: No multi-user support or access controls
- **Session Memory**: Lost when browser refreshed
- **File Size**: Large document uploads may timeout
- **Concurrent Requests**: Not optimized for multiple simultaneous users

## Future Capabilities

### Planned Features (Next 4-8 Weeks)
- **Complete GitHub Integration**: End-to-end issue creation workflow
- **Workflow Persistence**: State survives system restarts
- **Learning Mechanisms**: Improvement through user feedback
- **Performance Optimization**: Faster response times

### Long-term Vision (3-6 Months)
- **Multi-User Support**: Team collaboration features
- **Advanced Workflows**: Complex multi-step automation
- **Additional Integrations**: Jira, Slack, analytics platforms
- **Strategic Insights**: AI-powered product recommendations
- **Predictive Analytics**: Timeline and risk prediction

## Feedback and Support

### Providing Feedback
The system is actively learning from usage patterns:
1. **Correct mistakes**: When AI responses are inaccurate
2. **Rate responses**: Indicate helpful vs. unhelpful results
3. **Report issues**: Document specific problems encountered
4. **Suggest improvements**: What features would be most valuable?

### Current Development Status
For current development status and roadmap:
- **Technical Progress**: [Project Report](../project/project-report.md)
- **Business Impact**: [Executive Summary](../project/executive-summary.md)
- **Development Details**: [Backlog](../planning/backlog.md)

### Known Issues
- Workflow state doesn't persist across system restarts
- GitHub integration incomplete (issue creation in progress)
- Search relevance inconsistent across different document types
- Performance varies with knowledge base size

This user guide will be updated as system capabilities evolve and mature.

---
*Last Updated: June 22, 2025*
*Reflects current web interface capabilities and development status*

## Revision Log
- **June 22, 2025**: Major rewrite to reflect PM-011 web interface completion, updated capabilities and limitations
- **June 21, 2025**: Added systematic documentation dating and revision tracking