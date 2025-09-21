# Persistent Context Foundation Research & Architecture Planning

**Purpose**: Comprehensive analysis of existing patterns and requirements for building persistent context infrastructure in Piper Morgan.

**Investigation Date**: August 20, 2025 - 3:07 PM Pacific
**Investigator**: Cursor Agent
**Methodology**: Excellence Flywheel - Systematic Verification First

## 🔍 **EXISTING PERSISTENCE PATTERNS ANALYSIS**

### **Current Session Management Infrastructure**

✅ **SessionManager** (`services/session/session_manager.py`):

- In-memory session storage with TTL (30 minutes default)
- `ConversationSession` class with rich context tracking
- Session history, clarification state, file metadata
- **Key Limitation**: Sessions lost on restart - no persistence

### **Database Context Storage Patterns**

✅ **Existing Context Fields**:

- `Intent.context` (JSON) - Intent-specific context data
- `Workflow.context` (JSON) - Workflow execution context
- `FeedbackDB.conversation_context` (JSON) - User feedback context
- `FeedbackDB.context` (JSON) - Additional feedback context

### **File Context Storage**

✅ **File Storage Infrastructure**:

- `UploadedFile` model with session_id tracking
- File metadata persistence in database
- Session-based file organization

### **User Preference Patterns**

✅ **Existing Preference Handling**:

- File type preferences in `FileResolver`
- Hierarchy preferences in knowledge graph ingestion
- Intent enrichment with user preferences

## 🏗️ **INTEGRATION ANALYSIS**

### **Domain Model Integration Points**

✅ **Ready for Extension**:

- `ConversationSession.context: Dict = {}` - Empty dict ready for user preferences
- `Intent.context` - Can store user-specific intent preferences
- `Workflow.context` - Can store workflow-specific user settings

### **Session Management Integration**

✅ **Current Architecture**:

- Session-based context storage in memory
- TTL-based cleanup (30 minutes)
- File upload tracking per session
- Clarification state management

### **Database Integration Points**

✅ **Existing Infrastructure**:

- JSON columns for flexible context storage
- Session_id indexing for efficient queries
- Timestamp tracking for context freshness

## 🎯 **ARCHITECTURE REQUIREMENTS**

### **Simple JSON Storage Approach Assessment**

✅ **Recommended Approach**: Extend existing JSON context fields

- **Pros**:
  - Leverages existing database schema
  - Flexible structure for different preference types
  - No schema migrations required
  - Consistent with current patterns
- **Cons**:
  - No schema validation
  - Potential for inconsistent data structures
  - Query performance on JSON fields

### **Database Integration Considerations**

✅ **Current Database Support**:

- PostgreSQL with JSON column support
- Existing JSON context fields working
- Session_id indexing for performance
- TTL-based cleanup patterns

### **Future Extensibility Planning**

✅ **Scalable Architecture**:

- JSON context allows gradual schema evolution
- Session-based approach supports user isolation
- Context inheritance from session to intent to workflow
- Preference merging and conflict resolution

## 📋 **IMPLEMENTATION CHECKLIST FOR CODE AGENT**

### **Phase 1: Core Infrastructure (2 hours)**

- [ ] **Extend ConversationSession.context**:
  - Add user preference storage methods
  - Implement preference getter/setter with defaults
  - Add preference validation and type checking
- [ ] **Create UserPreferenceManager**:
  - Simple JSON-based preference storage
  - Preference inheritance (global → user → session)
  - Preference merging and conflict resolution
- [ ] **Database Integration**:
  - Extend existing context fields for user preferences
  - Add preference-specific indexes if needed
  - Implement preference persistence methods

### **Phase 2: Context Persistence (1 hour)**

- [ ] **Session Persistence**:
  - Save session context to database on updates
  - Load session context from database on restore
  - Implement context versioning for conflict resolution
- [ ] **Context Inheritance**:
  - Global system preferences
  - User-specific preferences
  - Session-specific overrides
- [ ] **Context Merging**:
  - Handle preference conflicts
  - Implement precedence rules
  - Add conflict resolution strategies

### **Phase 3: Integration & Testing (1 hour)**

- [ ] **Existing Service Integration**:
  - Integrate with SessionManager
  - Connect to Intent context handling
  - Link with Workflow context storage
- [ ] **API Endpoints**:
  - User preference CRUD operations
  - Context retrieval and update
  - Preference export/import
- [ ] **Comprehensive Testing**:
  - Use activated test infrastructure
  - Test preference persistence across sessions
  - Validate context inheritance and merging

## 🚧 **POTENTIAL BLOCKERS & COMPLEXITIES**

### **Technical Challenges**

⚠️ **JSON Schema Validation**:

- No built-in schema validation for JSON fields
- **Solution**: Implement custom validation in UserPreferenceManager
- **Impact**: Medium - requires careful validation logic

⚠️ **Context Versioning**:

- Need to handle preference changes over time
- **Solution**: Add version field to context JSON
- **Impact**: Low - simple timestamp-based versioning

⚠️ **Performance on JSON Queries**:

- JSON field queries may be slower than structured fields
- **Solution**: Add specific indexes for common preference queries
- **Impact**: Low - only affects preference-specific searches

### **Architectural Decisions Needed**

❓ **Preference Scope**:

- **Question**: Should preferences be global, user-specific, or session-specific?
- **Recommendation**: Hierarchical approach (global → user → session)
- **Rationale**: Allows system defaults with user customization

❓ **Context Inheritance Strategy**:

- **Question**: How should preferences cascade from global to session?
- **Recommendation**: Deep merge with session overrides
- **Rationale**: Provides flexibility while maintaining consistency

❓ **Conflict Resolution**:

- **Question**: How to handle conflicting preferences?
- **Recommendation**: Session preferences override user preferences
- **Rationale**: Session context is most relevant for current work

## 🎯 **IMPLEMENTATION PATH MAPPING**

### **Immediate Implementation (Code Agent - 4 hours)**

1. **Hour 1-2**: Core UserPreferenceManager and preference storage
2. **Hour 3**: Session persistence and context inheritance
3. **Hour 4**: Integration testing and API endpoints

### **Future Enhancements (Post-MVP)**

- **Preference Analytics**: Track preference usage and effectiveness
- **Preference Templates**: Predefined preference sets for common workflows
- **Preference Sharing**: Allow users to share preference configurations
- **Advanced Validation**: Schema-based preference validation
- **Performance Optimization**: Preference caching and query optimization

## 🔧 **TECHNICAL SPECIFICATIONS**

### **UserPreferenceManager Interface**

```python
class UserPreferenceManager:
    async def get_preference(self, key: str, user_id: str = None,
                           session_id: str = None, default: Any = None) -> Any
    async def set_preference(self, key: str, value: Any, user_id: str = None,
                           session_id: str = None) -> bool
    async def get_all_preferences(self, user_id: str = None,
                                session_id: str = None) -> Dict[str, Any]
    async def merge_preferences(self, user_id: str, session_id: str) -> Dict[str, Any]
    async def clear_session_preferences(self, session_id: str) -> bool
```

### **Context Storage Schema**

```json
{
  "user_preferences": {
    "ui_theme": "dark",
    "notification_frequency": "daily",
    "default_file_types": ["md", "py", "json"]
  },
  "session_preferences": {
    "current_project": "piper-morgan",
    "preferred_agent": "cursor",
    "workflow_style": "agile"
  },
  "context_version": "1.0",
  "last_updated": "2025-08-20T15:07:00Z"
}
```

### **Database Extensions**

```sql
-- Add preference-specific indexes if needed
CREATE INDEX idx_intent_context_preferences ON intents USING GIN (context);
CREATE INDEX idx_workflow_context_preferences ON workflows USING GIN (context);

-- Add preference validation constraints
ALTER TABLE intents ADD CONSTRAINT valid_context_json
  CHECK (jsonb_typeof(context) = 'object');
```

## 📊 **SUCCESS METRICS**

### **Functional Requirements**

- [ ] User preferences persist between sessions
- [ ] Context carries over between conversations
- [ ] Preferences can be set at global, user, and session levels
- [ ] Context inheritance works correctly
- [ ] API endpoints for preference management

### **Performance Requirements**

- [ ] Preference retrieval <100ms
- [ ] Context persistence <500ms
- [ ] Session restoration <1 second
- [ ] Support for 1000+ concurrent sessions

### **Quality Requirements**

- [ ] Comprehensive test coverage (>90%)
- [ ] No data loss on system restart
- [ ] Graceful handling of corrupted preferences
- [ ] Backward compatibility with existing context

## 🚀 **READY FOR IMPLEMENTATION**

**Status**: ✅ **RESEARCH COMPLETE** - Code Agent can start implementation immediately
**Confidence**: High - existing patterns provide solid foundation
**Risk Level**: Low - leverages proven infrastructure
**Timeline**: 4 hours achievable with clear implementation path

**Next Steps**: Code Agent should proceed with Phase 1 implementation using the UserPreferenceManager approach and existing JSON context fields.
