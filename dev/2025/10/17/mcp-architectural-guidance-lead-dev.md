# Architectural Guidance: MCP Migration Approach

**To**: Lead Developer (Sonnet 4.5)
**From**: Chief Architect
**Date**: October 17, 2025, 1:45 PM
**Re**: Sprint A3 MCP Migration - Architectural Direction

---

## Context for New Lead Developer

You've just completed Phase -1 discovery for CORE-MCP-MIGRATION (#198) and found that MCP implementations exist but are inconsistent and incomplete across our integrations. This is another instance of our recurring "75% pattern" - systems that are mostly built but need completion and standardization.

Your discovery revealed:
- Calendar: 95% complete (tool-based)
- GitHub: 90% complete (tool-based)
- Notion: 60% complete (server-based)
- Slack: 40% complete (basic structure)

## Architectural Decision

After reviewing your Phase -1 report and Code's discovery, I'm providing clear architectural direction:

**PRIMARY DECISION: Standardize on tool-based MCP implementation**

This means:
1. Tool-based MCP (like GitHub and Calendar have) is our standard pattern
2. Server-based MCP (like Notion has) should be migrated to tool-based
3. All future integrations must use tool-based approach
4. This decision should be documented as an ADR before proceeding

## Your Implementation Approach

### Phase 0.5: Document Architectural Decision (30 minutes - IMMEDIATE)

Create an ADR (Architectural Decision Record) documenting:

```markdown
# ADR-XXX: Standardize on Tool-Based MCP Implementation

## Status
Accepted

## Context
Phase -1 discovery revealed two competing MCP patterns:
- Tool-based (GitHub, Calendar) - Direct tool definitions
- Server-based (Notion) - Separate MCP servers

## Decision
We will standardize on tool-based MCP implementation across all integrations.

## Consequences
- Simpler architecture (no separate servers)
- Consistent pattern across all services
- Existing server-based implementations need migration
- Clear pattern for future integrations

## Migration Path
Server-based implementations will be migrated to tool-based following the pattern established by GitHub and Calendar.
```

Place this in: `docs/architecture/decisions/adr-xxx-mcp-standardization.md`

### Phase 1: Complete High-Value Integrations (3-4 hours)

**Start with the most complete implementations to establish patterns:**

#### Step 1.1: Complete Calendar Integration (95% → 100%)
Since Calendar is nearest to completion:
1. Review existing calendar MCP adapter
2. Complete the configuration loading (the missing 5%)
3. Wire to orchestration layer
4. Test with simple calendar operations
5. Document the pattern you observe

Expected work:
- Add configuration loading from PIPER.user.md
- Ensure all calendar tools are properly registered
- Test calendar event creation and retrieval

#### Step 1.2: Complete GitHub Integration (90% → 100%)
Using patterns learned from Calendar:
1. Review existing GitHub MCP implementation
2. Complete the integration wiring (the missing 10%)
3. Ensure all 15 GitHub tools are accessible
4. Test with GitHub issue creation
5. Document any variations from Calendar pattern

Expected work:
- Wire MCP tools to orchestration engine
- Ensure proper authentication flow
- Test issue creation, PR operations

**Phase 1 Success Criteria:**
- Calendar MCP 100% functional
- GitHub MCP 100% functional
- Pattern document created showing standard approach
- Both integrations tested with real operations

### Phase 2: Migrate Server-Based to Tool-Based (3-4 hours)

#### Step 2.1: Migrate Notion from Server to Tools (60% → 100%)

This is the complex migration that establishes our server→tool conversion pattern:

1. Study existing Notion MCP server implementation
2. Extract tool definitions from server
3. Convert to tool-based pattern (following Calendar/GitHub examples)
4. Remove server-based code
5. Complete the missing 40% functionality
6. Test thoroughly
7. Document migration pattern for future use

Expected work:
- Convert `notion_mcp_server.py` to tool-based approach
- Implement missing database operations
- Ensure page creation and updates work
- Create migration guide for future conversions

**Phase 2 Success Criteria:**
- Notion migrated from server to tool-based
- Migration guide documented
- All Notion operations functional
- Pattern reusable for other server→tool migrations

### Phase 3: Complete Remaining Integration (2-3 hours)

#### Step 3.1: Complete Slack Integration (40% → 100%)

Using established patterns:
1. Review basic Slack MCP structure
2. Implement full tool set following GitHub/Calendar pattern
3. Integrate with existing Slack spatial intelligence
4. Test message sending and channel operations
5. Ensure compatibility with webhook system

Expected work:
- Build out from basic structure to full implementation
- Add all Slack operations as tools
- Test with real Slack workspace
- Ensure spatial intelligence compatibility

**Phase 3 Success Criteria:**
- Slack MCP 100% functional
- All patterns consistent with other integrations
- Tested with real Slack operations
- Documentation complete

## Critical Implementation Guidelines

### 1. Maintain Backwards Compatibility
- Don't break existing functionality while migrating
- Test each service after changes
- Keep old code commented until new code verified

### 2. Pattern Consistency
- Every integration should follow the same tool-based pattern
- Use Calendar as the reference implementation
- Document any necessary deviations

### 3. Testing Requirements
- Each phase must include real integration tests
- Don't just test mocked - test with actual services
- Verify orchestration layer can access all tools

### 4. Documentation Standards
- Update MCP documentation as you go
- Create troubleshooting guides
- Document configuration requirements

## Why This Approach Over Alternatives

You presented three options in your brief. Here's why we're choosing this modified approach:

1. **Option A (Complete Existing)** - Would perpetuate inconsistency
2. **Option B (Full Standardization)** - Too time-consuming for sprint
3. **Our Approach (Strategic Completion)** - Balances standardization with efficiency

Our approach:
- Gets two integrations working quickly (Calendar, GitHub)
- Establishes patterns through easy wins
- Tackles complex migration (Notion) with patterns in hand
- Completes everything within sprint timeline (8-10 hours)

## Parallel Work Opportunity

If you want to use multiple agents:
- **After Phase 1**: Can parallelize Phase 2 (Notion) and Phase 3 (Slack)
- **Agent 1**: Notion migration (more complex)
- **Agent 2**: Slack completion (simpler)
- Both follow patterns established in Phase 1

## Definition of Done

The MCP migration is complete when:
1. ✅ ADR created and accepted
2. ✅ All four integrations at 100% functionality
3. ✅ All using tool-based pattern
4. ✅ Orchestration layer can access all tools
5. ✅ Real integration tests passing
6. ✅ Documentation updated
7. ✅ Migration guide created for future services

## Questions to Consider

Before starting, consider:
1. Do we have API credentials for testing each service?
2. Is the orchestration layer ready to accept MCP tools?
3. Should we version the old implementations before changing?
4. How do we handle configuration securely?

## Time Budget

Total estimated: 8-10 hours
- Phase 0.5: 30 minutes (ADR)
- Phase 1: 3-4 hours (Calendar + GitHub)
- Phase 2: 3-4 hours (Notion migration)
- Phase 3: 2-3 hours (Slack completion)

This is achievable within Sprint A3 alongside other work.

## Next Steps

1. Create the ADR (Phase 0.5) - 30 minutes
2. Report back with ADR number and any concerns
3. Begin Phase 1 with Calendar completion
4. Keep session log of patterns discovered
5. Check in after each phase completion

## Remember

You're not building from scratch - you're completing and standardizing existing implementations. This is detective work plus integration work, not greenfield development. The 75% pattern means most of the hard work is already done.

Trust the existing code quality (it's been good so far), complete what's missing, standardize the patterns, and document everything.

Good luck! Report back after creating the ADR.

---

**Chief Architect**
*October 17, 2025, 1:45 PM*
