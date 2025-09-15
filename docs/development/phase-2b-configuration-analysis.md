# Phase 2B: Configuration Analysis Report

**Agent**: Cursor Agent
**Date**: 2025-09-06 9:55 AM
**Mission**: Configuration points and hardcoding identification for Phase 3 repair

## User Configuration Needs Identified

### 1. Standup Questions Configuration

**Location**: `services/intent_service/canonical_handlers.py`
**Current Hardcoding**:

- "What's your name and role?"
- "What day is it?"
- "What am I working on?"
- "What's my top priority?"

**User Config Needed**:

```json
{
  "standup_questions": [
    "What's your name and role?",
    "What day is it?",
    "What should I focus on today?",
    "What am I working on?",
    "What's my top priority?"
  ]
}
```

### 2. Timing Configuration

**Location**: `services/queries/conversation_queries.py`
**Current Hardcoding**:

- Standup time: 5-7 AM (hardcoded range)
- Time zone: "PT" (Pacific Time)
- Default time: "6 AM PT"

**User Config Needed**:

```json
{
  "standup_timing": {
    "preferred_time": "06:00",
    "timezone": "America/Los_Angeles",
    "time_range_hours": 2
  }
}
```

### 3. Integration Preferences

**Location**: `cli/commands/standup.py`
**Current Hardcoding**:

- CLI flags: `--with-issues`, `--with-documents`, `--with-calendar`
- Default behavior: All integrations enabled

**User Config Needed**:

```json
{
  "integrations": {
    "github": true,
    "calendar": true,
    "issue_intelligence": true,
    "document_memory": true
  }
}
```

### 4. User Identity Configuration

**Location**: `services/features/morning_standup.py`
**Current Hardcoding**:

- Default user_id: "xian"
- User context: "Christian is a Product Manager/Developer"

**User Config Needed**:

```json
{
  "user_identity": {
    "user_id": "xian",
    "name": "Christian",
    "role": "Product Manager/Developer",
    "context": "working on Piper Morgan platform"
  }
}
```

## Hardcoded Values Detected

### 1. GitHub Repository Hardcoding (8 instances)

**Files**:

- `services/configuration/piper_config_loader.py` (2 instances)
- `services/config/github_config.py` (2 instances)
- `services/queries/query_router_spatial_migration.py` (2 instances)
- `services/mcp/consumer/github_adapter.py` (2 instances)

**Values**:

- Repository: "mediajunkie/piper-morgan-product"
- Owner: "mediajunkie"

### 2. Standup Content Hardcoding (1 instance)

**File**: `services/features/morning_standup.py`
**Value**: "🎯 Continue work on {repo}"

### 3. Time Zone Hardcoding (2 instances)

**Files**:

- `services/configuration/piper_config_loader.py`
- `services/intent_service/canonical_handlers.py`

**Values**:

- "6 AM PT"
- "PT" timezone

### 4. Priority Hardcoding (6 instances)

**Files**:

- `services/configuration/piper_config_loader.py` (2 instances)
- `services/intent_service/canonical_handlers.py` (4 instances)

**Values**:

- "Enhanced conversational context, MCP deployment, pattern validation"
- "VA Q4 Onramp system implementation and delivery"

## Configuration Injection Points

### 1. CLI Layer

**File**: `cli/commands/standup.py`
**Line**: 44-50 (StandupCommand.**init**)
**Injection Point**: User preferences loading
**Current**: Hardcoded service initialization
**Needed**: Load user configuration for integration selection

### 2. Orchestrator Layer

**File**: `services/features/morning_standup.py`
**Line**: 49-60 (MorningStandupWorkflow.**init**)
**Injection Point**: Integration selection and user context
**Current**: Hardcoded user_id = "xian"
**Needed**: Load user identity and integration preferences

### 3. Data Sources

**Files**:

- `services/integrations/github/github_agent.py`
- `services/features/issue_intelligence.py`
- `services/knowledge_graph/document_service.py`

**Injection Point**: Repository/service configuration
**Current**: Hardcoded repository references
**Needed**: Load GitHub configuration from user settings

### 4. Response Formatter

**File**: `services/intent_service/canonical_handlers.py`
**Injection Point**: Question customization and content
**Current**: Hardcoded questions and priorities
**Needed**: Load standup questions and user priorities

## Configuration Structure for Phase 3

```json
{
  "standup_questions": [
    "What's your name and role?",
    "What day is it?",
    "What should I focus on today?",
    "What am I working on?",
    "What's my top priority?"
  ],
  "standup_timing": {
    "preferred_time": "06:00",
    "timezone": "America/Los_Angeles",
    "time_range_hours": 2
  },
  "integrations": {
    "github": true,
    "calendar": true,
    "issue_intelligence": true,
    "document_memory": true
  },
  "user_identity": {
    "user_id": "xian",
    "name": "Christian",
    "role": "Product Manager/Developer",
    "context": "working on Piper Morgan platform"
  },
  "github_config": {
    "repository": "mediajunkie/piper-morgan-product",
    "owner": "mediajunkie"
  },
  "priorities": {
    "standing_priorities": [
      "Enhanced conversational context",
      "MCP deployment",
      "Pattern validation"
    ],
    "current_focus": "VA Q4 Onramp system implementation and delivery"
  }
}
```

## Summary

**User Config Required**: 4 categories (questions, timing, integrations, identity)
**Hardcoded Values Found**: 17 instances requiring extraction
**Injection Points**: 4 locations identified for configuration loading
**Configuration Structure**: Ready for Phase 3 implementation

**Critical Hardcoding**:

- Repository references: 8 instances
- Standup content: 1 instance
- Time zones: 2 instances
- User identity: 6 instances

**Next Steps**: Phase 3 configuration extraction and injection implementation
