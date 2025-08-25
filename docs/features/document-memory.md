# Document Memory Integration

Document Memory extends the canonical query system to provide context and decision history.

## Canonical Queries Available
- `what_did_we_decide` - Find previous decisions on topics
- `what_context_exists` - Get relevant background information
- `what_should_i_review` - Smart document suggestions
- `what_patterns_exist` - Discover usage and decision patterns

## Integration with Other Features
### Morning Standup
- Document context included in daily summaries
- Previous decisions shown for today's focus areas
- Unread important documents flagged

### CLI Commands
- `piper documents decisions [topic]` - Find decisions
- `piper documents context` - Get recent context
- `piper documents suggest` - Reading suggestions

## Architecture
Extends CanonicalQueryEngine following established patterns from Issue Intelligence integration.
