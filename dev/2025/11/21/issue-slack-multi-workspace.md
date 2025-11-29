# GitHub Issue: SLACK-MULTI-WORKSPACE

**Title**: SLACK-MULTI-WORKSPACE: Support attention across multiple workspaces

**Labels**: `slack`, `integration`, `enterprise-feature`, `enhancement`

**Milestone**: Enterprise (Post-Alpha)

**Priority**: P2

---

## Context

Deferred from SLACK-SPATIAL Phase 4 (Issue #361) during alpha preparation. This feature requires infrastructure for multiple Slack workspace installations that is not needed for initial alpha testing.

**Related Issue**: #361 (SLACK-SPATIAL)
**Deferred Date**: November 21, 2025
**Reason**: Requires multiple OAuth installations per user

---

## Description

Enable attention prioritization and navigation across multiple Slack workspace installations. Currently, the system handles a single Slack workspace per user, but Enterprise customers often have multiple workspaces (e.g., company workspace, partner workspaces, client workspaces) that need coordinated attention management.

---

## Current Behavior

**Single Workspace Support**:
- User can connect one Slack workspace via OAuth
- Spatial territory created for that workspace
- Attention scoring works within that workspace
- Navigation limited to single workspace

**Limitations**:
- Cannot compare attention across workspaces
- No unified workspace territory management
- User must manually switch workspaces in Slack
- No cross-workspace pattern recognition

---

## Desired Behavior

**Multi-Workspace Support**:
- User can connect multiple Slack workspaces
- Each workspace has its own spatial territory
- Attention scoring works across all workspaces
- Unified attention prioritization shows highest-priority items regardless of workspace
- Smart workspace switching based on attention
- Cross-workspace pattern recognition

**Example Use Case**:
> User has 3 workspaces: Company (high activity), Partner (occasional), Client (urgent).
>
> Without this feature: User must check each workspace manually.
>
> With this feature: Piper shows urgent Client message has higher attention than routine Company messages, prompting user to switch workspaces.

---

## Requirements

### Functional Requirements

1. **Multiple OAuth Installations**
   - Support multiple Slack OAuth tokens per user
   - Each token represents a different workspace
   - Secure token storage and management
   - Token refresh for each workspace

2. **Unified Workspace Territory**
   - Spatial territory for each connected workspace
   - Unified navigation across territories
   - Workspace metadata (name, icon, member count)
   - Territory activation/deactivation

3. **Cross-Workspace Attention Scoring**
   - Calculate attention across all workspaces
   - Prioritize items by attention regardless of workspace
   - Normalize attention scores across workspaces
   - Handle workspace-specific attention patterns

4. **Smart Workspace Switching**
   - Suggest workspace switches based on attention
   - Deep linking to specific channels/messages
   - Workspace context in Piper UI
   - Recent workspace history

5. **User Interface**
   - Workspace selector in UI
   - Visual indication of workspace for each item
   - Multi-workspace attention dashboard
   - Workspace management settings

### Technical Requirements

1. **OAuth Infrastructure**
   - Support multiple OAuth installations per user
   - Database schema for multiple tokens
   - OAuth refresh flow per workspace
   - Secure token encryption

2. **Spatial System**
   - Multiple territories per integration type
   - Territory identification by workspace_id
   - Cross-territory navigation
   - Territory metadata storage

3. **Attention System**
   - Cross-territory attention calculation
   - Workspace-specific attention weights
   - Attention normalization across workspaces
   - Performance optimization for multiple workspaces

4. **Testing**
   - Mock multiple OAuth installations
   - Test cross-workspace attention
   - Test territory isolation
   - Test workspace switching flows

---

## Test Coverage

**Skipped Test**: `test_multi_workspace_attention_prioritization`
- **Location**: `tests/unit/services/integrations/slack/test_spatial_system_integration.py`
- **What it tests**: Complex cross-workspace attention management and navigation across multiple territories
- **Why skipped**: Requires multiple Slack installation infrastructure
- **Status**: Test exists but marked as skipped

**Additional Tests Needed**:
- Multiple OAuth token storage
- Cross-workspace attention calculation
- Workspace territory isolation
- Smart workspace switching logic
- UI workspace selector

---

## Implementation Considerations

### Architecture Impact

**Database Schema**:
- Add `workspace_id` to OAuth tokens table
- Support multiple tokens per user per integration
- Add workspace metadata table
- Update spatial territory schema

**API Changes**:
- Multi-workspace OAuth flow
- Workspace selection endpoint
- Cross-workspace attention query
- Workspace management CRUD

**UI Changes**:
- Workspace selector component
- Multi-workspace attention view
- Workspace settings page
- Workspace indicators on items

### Performance Considerations

- Query optimization for multiple workspaces
- Caching strategy for workspace data
- Attention calculation performance with N workspaces
- Rate limiting per workspace

### Security Considerations

- Token isolation between workspaces
- Permission validation per workspace
- Secure workspace switching
- Audit logging for multi-workspace actions

---

## Success Criteria

**Feature is complete when**:
- ✅ User can connect multiple Slack workspaces
- ✅ Attention scoring works across all workspaces
- ✅ UI shows unified attention view with workspace context
- ✅ User can switch to highest-attention workspace
- ✅ `test_multi_workspace_attention_prioritization` passes
- ✅ Performance acceptable with 3+ workspaces
- ✅ Enterprise customers can use feature

---

## Dependencies

**Blocked By**:
- Multiple OAuth installation infrastructure
- Workspace metadata storage system
- UI workspace selector component

**Blocks**:
- Enterprise customer onboarding
- Large organization support
- Cross-company collaboration features

---

## Estimated Effort

**Size**: Large (2-3 weeks)

**Breakdown**:
- OAuth infrastructure: 3-5 days
- Spatial system updates: 2-3 days
- Attention system changes: 2-3 days
- UI implementation: 3-5 days
- Testing and QA: 2-3 days

---

## Priority Justification

**P2 (High Priority for Enterprise)**:
- Critical for Enterprise customers
- Differentiator for large organizations
- Common request from alpha users with multiple workspaces
- Blocks Enterprise sales

**Not P0/P1**:
- Not required for alpha launch
- Single workspace sufficient for initial users
- Can be added post-alpha without breaking changes

---

## References

- **Parent Issue**: #361 (SLACK-SPATIAL)
- **Gameplan**: `gameplan-slack-spatial-phase4-final.md`
- **Test**: `tests/unit/services/integrations/slack/test_spatial_system_integration.py::test_multi_workspace_attention_prioritization`
- **Milestone**: Enterprise (Post-Alpha)

---

## Notes

This feature was deliberately deferred during alpha preparation to focus on core single-workspace functionality. The test exists and documents expected behavior. Implementation should be straightforward once multi-OAuth infrastructure is in place.

**Alpha Impact**: Not required for alpha testing with single-workspace users.

**Enterprise Impact**: Critical for Enterprise milestone.
