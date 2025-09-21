# Continuity Prompt Template

This template should be used when the current Claude Code session is approaching capacity (~80% full) to create a handoff prompt for the next session.

## Template

```markdown
# [EPIC-ID] Continuation - [Brief Description]

You are a distinguished principal technical architect guiding an enthusiastic PM building Piper Morgan. See project instructions for core approach.

## IMMEDIATE CONTEXT

We're in the middle of [specific task] to fix [specific issue].

**Current Status**: [Active Debugging | Testing | Implementing]
**Blocking Issue**: [If any, otherwise "None"]
**Last Action**: [What was just completed]
**Next Step**: [Specific next action needed]

## REFERENCE DOCUMENTS

Please review these in order:
1. **Session Log**: `development/session-logs/YYYY-MM-DD-log.md` - Current state and decisions
2. **Working Method**: `docs/development/working-method.md` - Step-by-step execution patterns
3. **Architecture Guidelines**: `docs/development/architectural-guidelines.md` - Antipatterns and best practices
4. **Project Instructions**: `CLAUDE.md` - Core approach and constraints

## SECURITY RESTRICTIONS

**NEVER ACCESS .env FILES**: Credentials must be provided through approved environment setup only. No access to .env, .env.*, or any environment credential files.

## CRITICAL CONTEXT

[2-3 bullets of absolutely essential context that might not be in docs]
- Example: "Workflow persistence was mocked in tests, causing false passes"
- Example: "Repository must return domain models via .to_domain()"
- Example: "We're using internal task handlers, not separate classes"

## FIRST ACTIONS

1. Verify you can access the session log and reference documents
2. [Specific technical action - e.g., "Run: `python -c 'from services.orchestration import engine'`"]
3. [Next step based on result]

## ACTIVE WARNINGS

[Any architectural concerns or patterns to enforce]
- Example: "Watch for POC code patterns (input_data/output_data fields)"
- Example: "Ensure all enums come from shared_types.py"
- Example: "Domain models must not depend on infrastructure"

## CONTEXT FOR DEBUGGING

[If debugging, include specific error details]
- **Error**: [Exact error message]
- **Location**: [File and line number]
- **Attempts**: [What was already tried]
- **Hypothesis**: [Current theory about root cause]

Remember: Follow working-method.md, especially the VERIFY → UNDERSTAND → IMPLEMENT → VALIDATE pattern.
```

## Usage Guidelines

### When to Use This Template
- Session is ~80% full (approaching token limit)
- Complex debugging session needs to continue
- Multi-session implementation work
- Need to hand off context to future sessions

### How to Fill Out the Template

1. **[EPIC-ID]** - Use project epic identifier (e.g., "PM-011")
2. **[Brief Description]** - One-line summary of current work
3. **Current Status** - Exactly where you are in the process
4. **Blocking Issue** - What's preventing progress (if anything)
5. **Last Action** - What was just completed successfully
6. **Next Step** - Specific next action needed
7. **Critical Context** - Essential info not in documents
8. **First Actions** - Immediate verification steps
9. **Active Warnings** - Architectural concerns to watch

### Example Usage

```markdown
# PM-011 Continuation - GitHub Integration Testing

We're in the middle of testing GitHub workflow integration to validate PM-011 completion.

**Current Status**: Testing
**Blocking Issue**: None
**Last Action**: Fixed JSON formatting and UI styling issues
**Next Step**: Test GitHub issue creation workflow

## REFERENCE DOCUMENTS
1. **Session Log**: `development/session-logs/2025-07-09a-log-json-formatting-fix.md`
2. **Working Method**: `docs/development/working-method.md`
3. **Architecture Guidelines**: `docs/development/architectural-guidelines.md`
4. **Project Instructions**: `CLAUDE.md`

## CRITICAL CONTEXT
- JSON mode implementation is complete and working
- UI styling fixed (no more italics on bot messages)
- Document summarization now uses clean markdown formatting
- GitHub integration exists but needs end-to-end testing

## FIRST ACTIONS
1. Review the completed JSON formatting work in session log
2. Check GitHub integration status: `grep -r "github" services/integrations/`
3. Test a simple GitHub issue creation workflow

## ACTIVE WARNINGS
- Don't modify domain models to fix integration tests
- Verify GitHub credentials are configured
- Follow TDD approach for any new GitHub functionality
```

## Best Practices

### Keep It Focused
- Reference documents rather than duplicating content
- Include only essential context not found elsewhere
- Be specific about next steps

### Update Session Logs
- Always update the session log before creating continuity prompt
- Include any architectural decisions made
- Note any patterns discovered

### Prepare for Handoff
- Create continuity prompt before hitting capacity limits
- Test that referenced documents exist and are current
- Verify next steps are clearly actionable

## Integration with Session Management

This template works with the session management approach defined in `working-method.md`:

1. **Create session log immediately** when starting work
2. **Update session log frequently** during work
3. **Prepare handoff early** using this template
4. **Reference session logs** in continuity prompts
5. **Verify context** when resuming work

The continuity prompt should always reference the current session log as the primary source of context, with this template providing the immediate tactical situation.
---
*Last Updated: July 09, 2025*

## Revision Log
- **July 09, 2025**: Added vertical resize feature to chat window for improved usability
