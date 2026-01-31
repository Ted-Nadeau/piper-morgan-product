# User Context Flow Mapping - Issue #734 Investigation

**Date**: 2026-01-30
**Status**: Research Complete (Read-Only Audit)
**Scope**: Multi-tenancy isolation gaps in user context propagation

---

## EXECUTIVE SUMMARY

User context flows through the application in 4 phases:

1. **Entry Point** (Routes) - JWT extracted, RequestContext created
2. **Service Layer** - Context passed explicitly to services
3. **Repository Layer** - Owner filtering enforced
4. **Integration Layer** - External APIs have limited user context awareness

**CRITICAL GAPS IDENTIFIED**:
- Global singleton state in onboarding/standup managers (lines 21-57 in conversation_handler.py)
- Slack webhooks process events without explicit user_id context
- Background task execution loses user context
- RequestContext is optional in some service methods (migration in progress per ADR-051)

---

## PHASE 1: ENTRY POINTS (Routes)

### 1A: Authentication Dependency Injection

**Location**: `services/auth/auth_middleware.py` (lines 254-332)

```python
async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> JWTClaims:
    # Extract from Authorization header OR auth_token cookie
    # Returns JWTClaims with: user_id (UUID), user_email, username, scopes, session_id, workspace_id
```

**What provides auth**:
- Authorization header (Bearer token) - HTTP standard
- auth_token cookie - Web UI support
- HTTPBearer with auto_error=False for optional auth

**Auth Middleware Exclusions** (lines 56-82):
- Excluded paths: /login, /setup, /api/setup, /api/v1/intent, /api/v1/workflows, /api/v1/standup
- These can be accessed anonymously OR with authentication

### 1B: Route Patterns

**Pattern A: Required Authentication**
```python
# web/api/routes/todos.py line 80-82
@router.post("")
async def create_todo(
    request: CreateTodoRequest,
    current_user: JWTClaims = Depends(get_current_user),  # REQUIRED
    todo_repo=Depends(get_todo_repository),
) -> dict:
    new_todo = domain.Todo(
        text=request.title,
        owner_id=current_user.sub,  # ← User ID from JWT
    )
```

**Pattern B: Optional Authentication**
```python
# web/api/routes/intent.py line 197
@router.post("/intent")
async def process_intent(
    request: Request,
    current_user: Optional[JWTClaims] = Depends(get_current_user_optional),  # OPTIONAL
):
    user_id = current_user.sub if current_user else None

    # ADR-051 Phase 2: Create RequestContext at boundary
    ctx: Optional[RequestContext] = None
    if current_user:
        ctx = RequestContext.from_jwt_and_request(
            claims=current_user,
            conversation_id=session_id,
        )
```

### 1C: RequestContext Creation (ADR-051)

**Location**: `services/domain/models.py` lines 57-137

```python
@dataclass(frozen=True)
class RequestContext:
    """
    Single source of truth for identity during request processing.
    Immutable (frozen) to prevent modification.

    Fields:
    - user_id: UUID (authenticated user's database PK)
    - conversation_id: UUID (database PK for conversation)
    - request_id: UUID (unique per-request for tracing)
    - user_email: str (denormalized for logging)
    - timestamp: datetime
    - workspace_id: Optional[UUID] (future multi-tenant support)
    """

    @classmethod
    def from_jwt_and_request(
        cls,
        claims: "JWTClaims",
        conversation_id: str,
        request_id: Optional[UUID] = None,
    ) -> "RequestContext":
        # Converts string → UUID at boundary
        # Validates sub and conversation_id are present
        return cls(
            user_id=UUID(claims.sub),
            conversation_id=UUID(conversation_id),
            request_id=request_id or uuid4(),
            user_email=claims.user_email,
            timestamp=datetime.now(timezone.utc),
            workspace_id=UUID(claims.workspace_id) if claims.workspace_id else None,
        )
```

**STATUS**: ADR-051 approved, migration in progress. Some routes use it, others still use legacy params.

---

## PHASE 2: SERVICE LAYER

### 2A: Service Method Signatures

**Pattern A: New Style (ADR-051 Compliant)**
```python
# services/intent/intent_service.py lines 222-242
async def _process_intent_internal(
    self,
    message: str,
    session_id: str = "default_session",
    user_id: str = None,
    ctx: Optional[RequestContext] = None,  # ← Preferred
) -> IntentProcessingResult:
    """
    ctx is optional during migration;
    when present, user_id/session_id are extracted from it.
    """
```

**Pattern B: Legacy Style (Pre-ADR-051)**
```python
# Accepts individual params: user_id, session_id
# Services assume single-user context if params omitted
```

### 2B: Standup & Onboarding Handlers

**CRITICAL ISSUE IDENTIFIED**: Global singleton managers

**Location**: `services/conversation/conversation_handler.py` lines 21-57

```python
# Issue #490: Global module-level singletons
_onboarding_manager = None
_onboarding_handler = None

def _get_onboarding_components():
    """Lazy-load onboarding components to avoid circular imports."""
    global _onboarding_manager, _onboarding_handler
    if _onboarding_manager is None:
        _onboarding_manager = PortfolioOnboardingManager()  # ← CREATED ONCE, REUSED FOREVER
        _onboarding_handler = PortfolioOnboardingHandler(_onboarding_manager)
    return _onboarding_manager, _onboarding_handler

# Issue #585: Same pattern for standup
_standup_manager = None
_standup_handler = None

def _get_standup_components():
    global _standup_manager, _standup_handler
    if _standup_manager is None:
        _standup_manager = StandupConversationManager()  # ← CREATED ONCE, REUSED FOREVER
        _standup_handler = StandupConversationHandler(conversation_manager=_standup_manager)
    return _standup_manager, _standup_handler
```

**Manager Storage**:
```python
# services/onboarding/portfolio_manager.py line 66-68
class PortfolioOnboardingManager:
    def __init__(self) -> None:
        self._sessions: Dict[str, PortfolioOnboardingSession] = {}  # ← ALL USERS STORED HERE
```

**ISOLATION GAP**:
- One PortfolioOnboardingManager instance shared across ALL users
- Sessions stored by session_id key: `self._sessions[session.id] = session`
- If two users use same session_id (or session_id isn't user-scoped), data leaks
- No workspace_id filtering in session storage

---

## PHASE 3: REPOSITORY LAYER

### 3A: Owner Filtering Pattern

**Location**: `services/repositories/todo_repository.py` lines 40-50

```python
async def get_list_by_id(
    self,
    list_id: str,
    owner_id: Optional[str] = None,      # ← User ID to filter by
    is_admin: bool = False
) -> Optional[domain.TodoList]:
    """Get todo list by ID - optionally verify ownership"""
    filters = [TodoListDB.id == list_id]
    if owner_id and not is_admin:
        filters.append(TodoListDB.owner_id == owner_id)  # ← FILTERING ENFORCED

    result = await self.session.execute(select(TodoListDB).where(and_(*filters)))
    db_list = result.scalar_one_or_none()
    return db_list.to_domain() if db_list else None
```

**Key Points**:
- Owner filtering is OPTIONAL (only enforced if owner_id param provided)
- Admins can bypass ownership check (is_admin=True)
- Routes responsible for passing owner_id
- No automatic user context extraction from request

**Shared Resources** (lines 84-95):
```python
async def get_shared_lists(self, user_id: UUID) -> List[domain.TodoList]:
    """Get lists shared with a user"""
    result = await self.session.execute(
        select(TodoListDB)
        .where(
            and_(TodoListDB.shared_with.contains([user_id]), TodoListDB.is_archived == False)
        )
    )
    db_lists = result.scalars().all()
    return [db_list.to_domain() for db_list in db_lists]
```

### 3B: Universal List Repository

**Location**: `services/repositories/universal_list_repository.py` lines 39-76

```python
async def get_list_by_id(
    self,
    list_id: str,
    owner_id: Optional[str] = None,
    is_admin: bool = False
) -> Optional[domain.List]:
    """Get universal list by ID - optionally verify ownership"""
    filters = [ListDB.id == list_id]
    if owner_id and not is_admin:  # ← CONDITIONAL FILTERING
        filters.append(ListDB.owner_id == owner_id)

    result = await self.session.execute(select(ListDB).where(and_(*filters)))
    db_list = result.scalar_one_or_none()
    return db_list.to_domain() if db_list else None

async def get_list_for_read(
    self,
    list_id: str,
    user_id: Optional[str] = None
) -> Optional[domain.List]:
    """Get list for reading - allows both owner AND shared users"""
    result = await self.session.execute(select(ListDB).where(ListDB.id == list_id))
    db_list = result.scalar_one_or_none()

    if not db_list:
        return None

    if not user_id:
        return db_list.to_domain()  # ← NO FILTERING IF NO USER_ID

    domain_list = db_list.to_domain()
    if domain_list.owner_id == user_id or domain_list.user_can_read(user_id):
        return domain_list

    return None
```

**ISOLATION GAP**:
- If `user_id` parameter is not provided, ALL lists are returned
- Calling code must remember to pass user_id for filtering
- No automatic context extraction from request

---

## PHASE 4: INTEGRATION LAYER

### 4A: Slack Webhook Router

**Location**: `services/integrations/slack/webhook_router.py` lines 102-145

```python
async def handle_slack_events(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Direct method for handling Slack events.

    NOTE: No user_id or workspace filtering at this level.
    """
    event_correlation_id = correlation_id.set(f"slack_event_{int(time.time() * 1000)}")

    if event_data.get("type") == "event_callback":
        # Create tracked background task
        task = task_manager.create_tracked_task(
            self._process_event_callback_with_observability(event_data),
            name=f"process_slack_event_{event_data.get('event', {}).get('type', 'unknown')}",
            metadata={
                "correlation_id": correlation_id.get(),
                "event_type": event_data.get("event", {}).get("type", "unknown"),
                "slack_event_id": event_data.get("event", {}).get("ts", "unknown"),
            },
        )

        logger.info(f"Created tracked task {task} for Slack event processing")
        return {"status": "ok", "task_id": str(task)}
```

**ISOLATION GAPS**:
- No user_id extraction from Slack event
- Background tasks lose RequestContext
- No workspace_id filtering for multi-workspace setups
- Event processing happens asynchronously without explicit user context

### 4B: Calendar Integration Router

**Location**: `services/integrations/calendar/calendar_integration_router.py` lines 44-67

```python
def __init__(
    self,
    config_service: Optional[CalendarConfigService] = None,
    user_id: Optional[str] = None,          # ← User ID as optional parameter
):
    """Initialize router with feature flag checking and config service.

    Issue #586: Added user_id parameter for timezone-aware calendar queries.
    """
    self.use_spatial = FeatureFlags.should_use_spatial_calendar()
    self.allow_legacy = FeatureFlags.is_legacy_calendar_allowed()

    self.config_service = config_service or CalendarConfigService()
    self._user_id = user_id                 # ← Stored but may not be used

    if self.use_spatial:
        try:
            from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter
            self.spatial_calendar = GoogleCalendarMCPAdapter(self.config_service)
```

**ISOLATION GAP**:
- user_id is optional and only hints at timezone awareness
- CalendarConfigService loads credentials globally (not per-user)
- No RequestContext passed to external adapters

### 4C: Slack Configuration Service

**Location**: `services/integrations/slack/config_service.py` lines 86-110

```python
def get_config(self) -> SlackConfig:
    """Get Slack configuration with environment variable loading"""
    if self._config is None:
        self._config = self._load_config()  # ← GLOBAL CONFIGURATION
    return self._config

def _load_from_user_config(self) -> Dict[str, Any]:
    """
    Load Slack configuration from PIPER.user.md.

    Parses YAML blocks from markdown file and extracts slack section.
    Follows the same pattern as Calendar and Notion config loading.
    """
    # Loads from user config file (not per-workspace/per-user)
```

**ISOLATION GAP**:
- Configuration is loaded once and cached (singleton pattern)
- No workspace_id or user_id scoping
- All integrations share same credentials/tokens
- Works only for single-user deployments

---

## INTEGRATION POINT ANALYSIS

### 4D: External API Integration Flow

```
User Request
    ↓
Route Layer (get_current_user extracts JWT)
    ↓
RequestContext created (if authenticated)
    ↓
Service Layer (receives ctx)
    ↓
Integration Adapter (loses RequestContext)
    ↓
External API (Google Calendar, Slack, etc.)
    ├─ User determination: From config file (single workspace)
    ├─ Workspace determination: Not scoped
    └─ Tenant isolation: Not implemented
```

**Problem**: RequestContext not passed to integration adapters

---

## CONTEXT LOSS POINTS (Where user_id disappears)

### Loss Point 1: Background Task Execution
```
Slack webhook event arrives
    ↓
task_manager.create_tracked_task() called
    ├─ RequestContext lost
    ├─ User context lost
    └─ Event processed in isolated thread/process
```

### Loss Point 2: Global Singleton Managers
```
Intent processed
    ↓
_get_onboarding_components() called
    ↓
PortfolioOnboardingManager._sessions accessed
    ├─ Session keyed by: session_id (not user_id)
    ├─ No user filtering
    └─ Data leak if session_id not user-scoped
```

### Loss Point 3: Configuration Service Singletons
```
Integration API call needed
    ↓
SlackConfigService.get_config() called
    ├─ Returns cached config (created once)
    ├─ No user/workspace filtering
    └─ All requests use same credentials
```

### Loss Point 4: Optional RequestContext
```
Service method called
    ↓
if ctx is None:
    # Service may assume single-user context
    # Or use fallback logic that's not isolated
```

---

## WORKSPACE_ID / MULTI-TENANCY STATUS

### Defined But Not Used

```python
# services/domain/models.py line 97
workspace_id: Optional[UUID] = None  # "For future multi-tenant support"

# services/auth/jwt_service.py line 84
workspace_id: Optional[str] = None  # "For multi-tenant scenarios"
```

**Current State**:
- workspace_id is carried in JWT claims
- workspace_id included in RequestContext
- BUT: No filtering in repositories based on workspace_id
- BUT: Integration adapters don't use workspace_id
- BUT: Configuration not scoped to workspace

### Workspace Isolation Framework (Not yet integrated)

```python
# services/mux/workspace_isolation.py lines 26-38
class BoundaryType(Enum):
    HARD = "hard"    # Never cross - data isolation
    SOFT = "soft"    # Cross with summarization
    OPEN = "open"    # Free crossing

@dataclass
class CategorizedContext:
    workspace_id: str
    category: str  # "work", "personal", "client:acme"
    tags: Set[str]
```

**Status**: Framework defined but not connected to data access layer

---

## ROUTES WITHOUT AUTHENTICATION

These endpoints can be accessed unauthenticated:
- GET /workflows/{workflow_id} (lines 154-191)
- POST /api/v1/intent (with optional auth)
- GET /api/v1/standup (with optional auth)
- OAuth callbacks

**Issue**: No user validation, so multiple unauthenticated requests could interfere

---

## RECOMMENDATIONS FOR INVESTIGATION

1. **Test Case 1: Session ID Collision**
   - Create two users with same session_id
   - Check if onboarding state leaks between them
   - Expected: Isolated sessions per user
   - Actual: Unknown (requires testing)

2. **Test Case 2: Workspace Filtering**
   - Create lists in workspace_id=A with user_id=1
   - Login as user_id=2 with workspace_id=B
   - Check if user_2 can access user_1's lists
   - Expected: Forbidden
   - Actual: Unknown (repositories don't filter workspace_id)

3. **Test Case 3: Integration Credential Leakage**
   - Setup Slack for user_1
   - Login as user_2
   - Check which workspace's Slack credentials user_2 gets
   - Expected: user_2's credentials (or error)
   - Actual: Likely user_1's (shared config)

4. **Test Case 4: Background Task User Context**
   - Slack webhook arrives while user_1 is active
   - Background task processes webhook
   - Check if task has access to user_1 or user_2's context
   - Expected: No user context (webhook-scoped)
   - Actual: Unknown

---

## FILE REFERENCE SUMMARY

| File | Lines | Issue | Severity |
|------|-------|-------|----------|
| services/conversation/conversation_handler.py | 21-57 | Global singleton managers | HIGH |
| services/onboarding/portfolio_manager.py | 66-68 | Session storage not user-scoped | HIGH |
| services/integrations/slack/config_service.py | 86-90 | Config singleton (no user scope) | HIGH |
| services/repositories/universal_list_repository.py | 52-75 | Optional user_id filtering | MEDIUM |
| services/integrations/slack/webhook_router.py | 102-145 | No user context in background tasks | MEDIUM |
| services/intent/intent_service.py | 222-242 | RequestContext optional (migration) | MEDIUM |
| services/mux/workspace_isolation.py | 26-80 | Isolation framework not integrated | LOW |

---

## SUMMARY TABLE

| Layer | Component | Context Type | Isolation | Issue |
|-------|-----------|--------------|-----------|-------|
| Route | get_current_user | JWTClaims | Per-route | None |
| Route | RequestContext | Domain model | Optional | Partially implemented |
| Service | Intent Service | RequestContext? | Conditional | Optional context (migration) |
| Service | Onboarding Manager | Module singleton | SHARED | All users share one instance |
| Service | Standup Manager | Module singleton | SHARED | All users share one instance |
| Repo | TodoRepository | Optional owner_id | Conditional | Depends on route remembering |
| Repo | UniversalListRepository | Optional user_id | Conditional | Depends on route remembering |
| Integration | SlackConfigService | File-based config | GLOBAL | All workspaces use same config |
| Integration | CalendarRouter | Optional user_id | Weak | Parameter not enforced |
| Background | Slack Webhook | Event only | LOST | RequestContext not propagated |
