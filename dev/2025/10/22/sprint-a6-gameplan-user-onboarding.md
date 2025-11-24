# Sprint A6 Gameplan: User Onboarding & Infrastructure

**Sprint**: A6
**Theme**: "Alpha-Ready Infrastructure"
**Duration**: 2-3 days estimated (likely 1-2 days actual based on patterns)
**Context**: Final sprint before Alpha testing

---

## Executive Summary

Sprint A6 delivers the critical user onboarding infrastructure needed for Alpha testing. This includes secure API key management, production database configuration, JWT security, and the onboarding wizard. Based on patterns from previous sprints, we expect to find 70-90% of infrastructure already exists.

---

## Sprint Goals

1. **Enable user self-onboarding** for Alpha testers
2. **Secure production infrastructure** (database, API keys, JWT)
3. **Complete 4-provider LLM** integration
4. **Deliver Alpha-ready system**

---

## Issue Priority & Sequencing

### Recommended Order

1. **CORE-LLM-SUPPORT** (#237) - Quick win, mostly exists
2. **CORE-USERS-JWT** (#227) - Security foundation
3. **CORE-USERS-API** (#228) - API key management
4. **CORE-USERS-PROD** (#229) - Database configuration
5. **CORE-USERS-ONBOARD** (#218) - Onboarding wizard (uses 2-4)

This order builds dependencies correctly: LLM first (independent), then security infrastructure, then database, finally the onboarding that uses them all.

---

## Issue-by-Issue Breakdown

### Issue #237: CORE-LLM-SUPPORT - Complete 4-Provider Integration

**Status**: 90% complete (documentation confirms)
**Existing**:
- LLMConfigService (641 lines)
- ProviderSelector (intelligent routing)
- Anthropic & OpenAI adapters
- Pattern-012 documentation

**Work Required**:
1. Wire ProviderSelector into LLMClient (1 hour)
2. Implement Gemini adapter (30-45 min)
3. Implement Perplexity adapter (30-45 min)
4. Testing (30 min)

**Realistic Estimate**: 2-3 hours (vs 2.5-3h documented)

---

### Issue #227: CORE-USERS-JWT - Token Blacklist

**Discovery Needed**: Check for existing Redis/cache infrastructure

**Implementation Path**:
1. Discovery phase (15 min)
2. Redis-based blacklist (1-2 hours)
3. Database fallback (30 min)
4. Integration with logout (30 min)
5. Testing (30 min)

**Realistic Estimate**: 3-4 hours (vs 1 day estimate)

---

### Issue #228: CORE-USERS-API - Secure API Key Management

**Discovery Needed**: Check for existing keychain/secrets code

**Expected Findings**:
- Likely some encryption utilities exist
- UserPreferenceManager could be extended
- Security patterns from Ethics implementation

**Implementation Path**:
1. Discovery phase (20 min)
2. OS keychain integration (2-3 hours)
3. Encrypted file fallback (1 hour)
4. Migration from plaintext (30 min)
5. Testing (1 hour)

**Realistic Estimate**: 4-6 hours (vs 1-2 days estimate)

---

### Issue #229: CORE-USERS-PROD - PostgreSQL Configuration

**Discovery Needed**: Check existing database infrastructure

**Expected Findings**:
- AsyncSessionFactory exists
- Some connection management likely exists
- Migration patterns from other systems

**Implementation Path**:
1. Discovery phase (20 min)
2. PostgreSQL configuration (1-2 hours)
3. Connection pooling (1 hour)
4. Alembic setup (1-2 hours)
5. Migration scripts (1 hour)
6. Testing (1 hour)

**Realistic Estimate**: 5-7 hours (vs 2 days estimate)

---

### Issue #218: CORE-USERS-ONBOARD - Alpha Onboarding

**Dependencies**: Needs JWT, API, PROD complete first

**Implementation Path**:
1. Discovery phase (30 min)
2. CLI wizard framework (2-3 hours)
3. Configuration validation (1 hour)
4. Health checks (1 hour)
5. Integration with API/JWT/DB (1 hour)
6. Documentation (1-2 hours)
7. Testing (1 hour)

**Realistic Estimate**: 7-9 hours (vs 2-3 days estimate)

---

## Day-by-Day Plan

### Day 1 (Today - Tuesday)

**Morning** (2-3 hours):
- CORE-LLM-SUPPORT discovery & implementation
- Complete 4-provider integration
- Close #237

**Afternoon** (4-5 hours):
- CORE-USERS-JWT discovery & implementation
- CORE-USERS-API discovery & implementation
- Close #227 and #228

### Day 2 (Wednesday)

**Morning** (3-4 hours):
- CORE-USERS-PROD discovery & implementation
- PostgreSQL setup and migration
- Close #229

**Afternoon** (4-5 hours):
- CORE-USERS-ONBOARD implementation
- Onboarding wizard and health checks
- Close #218

### Day 3 (Thursday - if needed)

**Buffer for**:
- Extended testing
- Documentation polish
- Integration issues
- Alpha preparation

---

## Discovery Phase Questions

### For Each Issue

**CORE-LLM-SUPPORT**:
- Is ProviderSelector already wired anywhere?
- Do Gemini/Perplexity configs exist?
- Any existing adapter code?

**CORE-USERS-JWT**:
- Redis infrastructure exists?
- Cache patterns in use?
- Existing blacklist implementations?

**CORE-USERS-API**:
- Keychain integration code?
- Encryption utilities?
- Secret management patterns?

**CORE-USERS-PROD**:
- PostgreSQL dependencies installed?
- Connection pool implementations?
- Existing migration scripts?

**CORE-USERS-ONBOARD**:
- CLI wizard frameworks?
- Setup utilities?
- First-run detection code?

---

## Risk Assessment

### Low Risk
- **CORE-LLM-SUPPORT**: Documentation confirms 90% complete
- **CORE-USERS-JWT**: Standard Redis pattern

### Medium Risk
- **CORE-USERS-API**: OS keychain complexity
- **CORE-USERS-PROD**: Database migration

### Mitigation
- Start with quick wins (LLM-SUPPORT)
- Use simple implementations first
- Defer complex features to post-Alpha
- Focus on critical path

---

## Success Metrics

### Sprint Success
- All 5 issues complete
- Alpha users can self-onboard
- Security infrastructure operational
- 4-provider LLM working
- No critical bugs

### Quality Targets
- Test coverage >80%
- All security tests passing
- Onboarding <5 minutes
- Zero plaintext secrets

---

## Definition of Done

**Sprint A6 Complete When**:
1. 4-provider LLM integration working
2. JWT blacklist operational
3. API keys secure
4. PostgreSQL configured
5. Onboarding wizard functional
6. All tests passing
7. Documentation complete
8. Alpha-ready system

---

## Velocity Predictions

Based on Sprint A3-A5 patterns:

**Original Estimates**: 7-9 days total
**Realistic Projection**: 2-3 days
**Confidence**: High (based on 75-95% existing pattern)

**Why It Will Be Fast**:
- Infrastructure investment payoff continues
- Security patterns from Ethics implementation
- Database patterns from existing repos
- UserPreferenceManager extensible
- Discovery phase will reveal treasures

---

## Next Steps

1. **Start with CORE-LLM-SUPPORT** (quick win)
2. **Discovery phases** for each issue
3. **Build security infrastructure** (JWT, API)
4. **Database migration**
5. **Onboarding wizard** last (uses others)

---

## Notes for Lead Developer

- Expect to find 75-90% infrastructure exists
- Use discovery-first approach (proven successful)
- Don't skip work - complete properly
- Verification discipline throughout
- Ask PM before any scope changes

---

*Sprint A6 gameplan ready for execution!*
