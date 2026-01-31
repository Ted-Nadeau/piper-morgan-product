# Memo: Multi-Tenancy Isolation Architecture Guidance

**From**: Chief Architect
**To**: Lead Developer
**CC**: PM (xian)
**Date**: January 30, 2026
**Re**: Response to #734 Multi-Tenancy Guidance Request
**Priority**: High

---

## Executive Summary

Your discovery work on #734 is excellent. The systemic nature of this issue justifies the full domain-driven refactor that PM has approved. Below is architectural guidance on all 6 questions, plus a recommended implementation sequence.

**Key principle**: In alpha, we favor "break loudly now" over gradual migration. Build the proper foundation.

---

## Q1: OAuth Credential Separation Pattern

**Decision**: Option C - Separate services

**Rationale**: These are different bounded contexts:
- **App credentials** (client_id, client_secret) = system configuration → `IntegrationConfigService`
- **User tokens** (access_token, refresh_token) = user data → `UserTokenService`

**Implementation**:
- App credentials: Environment variables or system config table (no user scoping)
- User tokens: User-scoped data layer with mandatory `owner_id`

This separation makes the domain model explicit: app creds belong to the system, user tokens belong to users.

---

## Q2: RequestContext Activation Strategy

**Decision**: Option C - Boundary enforcement at route level

**Rationale**: Routes are the trust boundary where user identity is established. Services should trust they receive valid context from routes.

**Implementation**:
- Create middleware/dependency ensuring RequestContext exists for all authenticated routes
- Services needing user context: Receive as **required** parameter
- Services that are user-agnostic: Don't need it
- Background tasks: Separate pattern (see Q3c)

This avoids "None-checking everywhere" anti-pattern.

---

## Q3: Integration Adapter User Context

### Q3a: Config services per-request?

**Decision**: No. Keep singletons, pass user context to methods.

```python
# Current (broken)
config_service.get_calendar_token()

# Correct
config_service.get_user_calendar_token(user_id: str)
```

### Q3b: OAuth callbacks - user identification

**Decision**: Embed user_id in OAuth state parameter.

```python
# On OAuth initiation
state = {
    "user_id": current_user.id,
    "return_url": "/settings/integrations",
    "nonce": generate_secure_nonce()
}
encoded_state = base64url_encode(json.dumps(state))
# Pass encoded_state to OAuth provider

# On callback
decoded_state = json.loads(base64url_decode(state_param))
user_id = decoded_state["user_id"]
# Verify nonce, then proceed with user_id
```

**IMPORTANT**: PM requests a **Phase -1 investigation** before implementation to audit any existing OAuth state infrastructure. Document what exists before designing the new pattern.

### Q3c: Background tasks - user context

**Decision**: Depends on webhook type:

1. **User-initiated webhooks** (e.g., Slack message from user):
   - Extract user identifier from webhook payload
   - Lookup internal user_id from external ID mapping

2. **System webhooks** (e.g., GitHub push):
   - Store "who connected this integration" at setup time
   - Use that as the acting user for webhook processing

Consider a `JobContext` that captures user context at job creation and restores it at execution.

---

## Q4: Singleton Manager Refactor

**Decision**: Option A - Key by user_id

**Rationale**:
- `session_id` is ephemeral (browser tab) - wrong granularity
- `user_id` is the identity boundary - correct granularity

**Implementation**:
```python
# Current
self._sessions: Dict[str, OnboardingSession] = {}  # keyed by session_id

# Correct
self._sessions: Dict[str, OnboardingSession] = {}  # keyed by user_id
```

Database backing can be added later if restart persistence becomes important. For MVP, in-memory keyed by user_id is sufficient.

---

## Q5: Repository Isolation Pattern

**Decision**: Option A first, then Option B

**Phase 1**: Make `owner_id` required
- This catches missing context at test time rather than runtime
- "Fail fast" principle - better to break loudly than leak silently

**Phase 2**: Add `workspace_id`
- Second dimension for future multi-tenant (users within workspaces)
- Can be optional with default initially

**Consider**: A `TenantContext` dataclass bundling both:
```python
@dataclass
class TenantContext:
    owner_id: str
    workspace_id: str = "default"
```

---

## Q6: Sequencing Recommendation

**Modified sequence** (I've reordered from your proposal):

| Phase | Work | Rationale |
|-------|------|-----------|
| **-1** | OAuth state investigation | Audit existing infrastructure before designing |
| **1** | RequestContext enforcement | Foundation - all other work depends on this |
| **2** | Repository isolation (owner_id required) | **Moved up** - creates forcing function |
| **3** | OAuth state redesign | Now repos won't accept None owner_id |
| **4** | Credential storage separation | App vs user services |
| **5** | Config service method signatures | Pass user context to methods |
| **6** | Singleton manager refactor | Can run parallel with 4-5 |
| **7** | workspace_id activation | Last - needs all above in place |

**Rationale for reorder**: Making owner_id required early is a "forcing function" - any code path without proper user context fails immediately, revealing all hidden gaps at once rather than discovering them incrementally.

---

## Additional Architectural Considerations

### 1. Testing Strategy
Add integration tests verifying cross-user isolation:
- User A creates data → User B query returns empty (not User A's data)
- User A's tokens not accessible from User B's context

### 2. Error Messages
Handle "not found" vs "not authorized" carefully:
- Don't reveal that a resource exists but belongs to another user
- Return consistent "not found" for both cases

### 3. Audit Trail
Consider adding `acted_as_user_id` to sensitive operations for future audit requirements.

### 4. Background Job Context
Design a `JobContext` pattern:
```python
@dataclass
class JobContext:
    user_id: str
    workspace_id: str
    created_at: datetime
    # Captured at job creation, restored at execution
```

---

## ADR Recommendation

**Yes - create ADR-058: Multi-Tenancy Isolation Architecture**

This is a foundational architectural decision affecting:
- Data access patterns across the entire codebase
- Security boundaries and trust model
- Future scalability to teams/workspaces

Document the decisions in this memo as the ADR content.

---

## Green Light

You have green light to proceed with the revised gameplan incorporating this guidance.

**Immediate next steps**:
1. Create ADR-058 (can be brief, reference this memo)
2. Execute Phase -1: OAuth state investigation
3. Begin Phase 1: RequestContext enforcement

---

*Questions welcome. This is important foundational work - take the time to get it right.*
