# Slack Integration Guide

## Overview

The Slack integration provides seamless communication between Piper Morgan and Slack workspaces, enabling spatial metaphor-based interactions and intelligent message consolidation.

## Core Components

### SlackResponseHandler

The primary component responsible for processing spatial events and generating Slack responses with intelligent message consolidation.

#### Key Features

**Message Consolidation (PM-079-SUB)**
- Groups related messages within a 5-second window
- Reduces message spam from 3-5 messages to 1-2 consolidated responses
- Preserves essential workflow information in a clean format
- Provides optional detailed breakdown via thread/reaction

**Consolidation Logic**
```python
# Messages are buffered by channel+thread combination
consolidation_key = f"{channel_id}:{thread_ts}"

# Consolidation triggers when 2+ messages within 5 seconds
if len(recent_messages) >= 2:
    send_consolidated_response()
```

**Example Consolidation**
**Before (3 separate messages)**:
```
🔔 Workflow completed successfully
✅ Task completed successfully
📊 Analysis complete
```

**After (1 consolidated message)**:
```
🤖 ✅ Task completed successfully
   📋 2 additional actions completed
   💬 Reply with 'details' for full breakdown
```

#### Methods

- `_get_consolidation_key()` - Generate unique keys for message grouping
- `_add_to_consolidation_buffer()` - Buffer messages for potential consolidation
- `_should_consolidate_messages()` - Determine if consolidation should occur
- `_format_consolidated_message()` - Format multiple messages into single response
- `_send_consolidated_response()` - Send consolidated response to Slack
- `get_detailed_message_breakdown()` - Provide detailed message breakdown

### SlackSpatialAdapter

Maps spatial events to Slack context, maintaining spatial metaphor purity.

### SlackClient

Handles direct communication with Slack API.

## Message Flow

1. **Spatial Event Reception** - Events received with integer positioning
2. **Context Mapping** - Spatial coordinates mapped to Slack context
3. **Intent Creation** - Intents created from spatial events
4. **Orchestration Processing** - Intents processed through orchestration engine
5. **Response Generation** - Responses generated with consolidation logic
6. **Slack Delivery** - Consolidated responses sent to appropriate channels/threads

## Configuration

### Consolidation Settings

```python
CONSOLIDATION_TIMEOUT = 5.0  # seconds
CONSOLIDATION_MAX_MESSAGES = 5  # per buffer
```

### Rate Limiting

```python
MAX_WORKFLOWS_PER_MINUTE = 3  # per user
```

## Error Handling

- **Duplicate Event Prevention** - Circuit breaker prevents runaway workflows
- **Rate Limiting** - Prevents spam and ensures quality responses
- **Graceful Degradation** - Falls back to individual messages if consolidation fails

## Testing

Comprehensive test suite available in `tests/integration/test_slack_message_consolidation.py`:

```bash
python -m pytest tests/integration/test_slack_message_consolidation.py -v
```

## Performance Monitoring

Handler statistics include consolidation metrics:

```python
stats = await response_handler.get_handler_stats()
consolidation_stats = stats["consolidation_stats"]
# {
#   "active_buffers": 2,
#   "total_buffered_messages": 6,
#   "consolidation_timeout": 5.0,
#   "max_messages_per_buffer": 5
# }
```

## Best Practices

1. **Message Consolidation** - Always use consolidation for related workflow messages
2. **Thread Targeting** - Preserve thread context for proper conversation flow
3. **Error Handling** - Implement graceful fallbacks for all Slack operations
4. **Rate Limiting** - Respect Slack API limits and user experience
5. **Monitoring** - Track consolidation effectiveness and user satisfaction

## Troubleshooting

### Common Issues

**Messages Not Consolidating**
- Check consolidation timeout settings
- Verify channel+thread key generation
- Ensure multiple messages within time window

**Consolidation Buffer Issues**
- Monitor buffer size limits
- Check for memory leaks in long-running sessions
- Verify buffer clearing logic

**Slack API Errors**
- Check authentication and permissions
- Verify channel/thread targeting
- Monitor rate limiting compliance
