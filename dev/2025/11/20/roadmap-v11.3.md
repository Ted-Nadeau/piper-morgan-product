# Piper Morgan Roadmap v11.3
*Updated: November 20, 2025*
*Previous: v11.2 (November 20, earlier)*

## Critical Update: Security Blockers Discovered

Ted Nadeau's architectural review uncovered **two absolute blockers** that prevent multi-user operation:
- **No RBAC** = Any user can access any data
- **No Encryption** = Data breach exposes everything in plaintext

These must be addressed before external alpha testing can begin safely.

---

## Immediate Priority Shift

### SPRINT S1: Security Foundation (Nov 21-27)
**Must Complete Before External Users**

#### Track A: RBAC Implementation (#357)
**Lead: Primary Developer**
- Day 1-2: Design and models (8 hrs)
- Day 3-4: Core implementation (8 hrs)
- Day 5: Testing and validation (8 hrs)
- **Deliverable**: Secure multi-user support

#### Track B: Quick Wins (Parallel)
**Lead: Secondary Developer or Same Dev on breaks**
- ✅ Windows Clone Fix (#353) - 3 hrs
- ✅ Database Indexes (#356) - 6 hrs
- ✅ Document Handler Routing - 4 hrs (from test work)
- **Deliverable**: Unblock Windows devs, prevent performance cliff

**Sprint S1 Outcomes**:
- Users cannot access other users' data ✅
- Windows developers can contribute ✅
- Performance won't degrade at scale ✅

---

### SPRINT S2: Encryption & Scale (Nov 28 - Dec 4)

#### Track A: Encryption at Rest (#358)
**Lead: Primary Developer**
- Day 1-2: Encryption service (10 hrs)
- Day 3-4: Migration and testing (10 hrs)
- Day 5: Performance validation (4 hrs)
- **Deliverable**: GDPR/SOC2 compliance ready

#### Track B: Architecture Fixes
**Lead: Secondary Developer**
- Singleton Refactor (#361) - 16 hrs
- OS Detection (#359) - 6 hrs
- **Deliverable**: Horizontal scaling capability

**Sprint S2 Outcomes**:
- Data encrypted at rest ✅
- Can scale to multiple servers ✅
- Scripts work on all platforms ✅

---

## Continuing Work (In Parallel)

### TEST- Infrastructure (Ongoing)
- Continue test fixes per Claude Code's work
- Skip test cleanup ✅ (87/100 health)
- Document processing completion

### UX Track (When Possible)
- Accessibility (Tranche 3B)
- Design tokens prep
- Deferred until security complete

---

## December Sprints (Post-Security)

### SPRINT D1: Alpha Polish (Dec 5-11)
- Complete TEST- infrastructure
- Annotation Pattern (#360) - Ted's innovation!
- UX Tranche 3 completion
- First external alpha cohort

### SPRINT D2: Alpha Expansion (Dec 12-18)
- Performance optimization
- Document management
- Alpha feedback integration
- Second alpha cohort

### SPRINT D3: Beta Prep (Dec 19-31)
- Bug fixes from alpha
- Design system Phase 1
- Documentation
- Beta announcement

---

## Backlog Reorganization Needed

### High Priority (Security/Blocking)
1. #357: RBAC ⏳ (in progress)
2. #358: Encryption ⏱️ (next week)
3. #353: Windows ⏳ (quick win)
4. #356: Indexes ⏳ (quick win)

### Medium Priority (Architecture/Scale)
5. #361: Singleton refactor
6. #359: OS Detection
7. Document handler fixes
8. API Pattern-007 violation

### Innovation/Differentiators
9. #360: Annotation pattern
10. Skills MCP implementation
11. Learning system integration

### Lower Priority (Important but not blocking)
- Remaining UX improvements
- Performance optimizations
- Additional test coverage

---

## Success Metrics Update

### Security Readiness (by Dec 1)
- [ ] RBAC fully implemented
- [ ] Encryption at rest operational
- [ ] Security scan passes
- [ ] Multi-user testing successful

### Alpha Readiness (by Dec 15)
- [ ] All P0 bugs resolved
- [ ] Core features stable
- [ ] 5+ external testers active
- [ ] No security vulnerabilities

### MVP (January 2026)
- Previous criteria remain
- Plus: SOC2 readiness
- Plus: GDPR compliance

---

## Risk Assessment

### Critical Risks (Showstoppers)
- ❌ Without RBAC: Cannot have multiple users
- ❌ Without Encryption: Legal/compliance liability
- ✅ With both: Can proceed to alpha safely

### Mitigated Risks
- Windows compatibility ✅ (fixing this week)
- Performance at scale ✅ (indexes this week)
- Horizontal scaling ✅ (singleton next week)

### Accepted Risks (for MVP)
- Single region deployment (OK for alpha)
- Basic caching strategy (OK for <100 users)
- Manual deployment process (automate later)

---

## Resource Allocation

### Primary Developer
- Week 1: RBAC (24 hrs)
- Week 2: Encryption (24 hrs)
- Week 3: Alpha polish

### Secondary Developer (or same dev alternating)
- Week 1: Quick wins (9 hrs)
- Week 2: Architecture fixes (22 hrs)
- Week 3: Test infrastructure

### PM/Architect
- Issue prioritization
- Backlog grooming
- Alpha user coordination
- Architecture decisions

---

## Key Decisions

### Immediate
1. Start RBAC tomorrow (longest lead time)
2. Fix Windows bug TODAY (blocks contributors)
3. Defer UX work until security complete

### This Week
1. Assign developer(s) to security sprint
2. Create detailed RBAC design
3. Set up Windows test environment

### Next Week
1. Encryption approach (field vs table level)
2. Key management strategy
3. Alpha user selection

---

## Communication

### To Alpha Testers
"Security infrastructure work in progress. Alpha testing delayed 1-2 weeks but will be much more secure."

### To Team
"Critical security gaps discovered. All hands on fixing before external users."

### To Stakeholders
"Professional security review revealed issues. Fixing now vs. expensive breach later."

---

## Bottom Line

**Two weeks of security work now** prevents:
- Data breaches
- Legal liability
- Complete rebuild later
- Loss of user trust

**This is the right priority shift.**

---

*Changelog v11.3*:
- Prioritized security blockers (RBAC, Encryption)
- Added quick wins track
- Shifted alpha timeline by 2 weeks
- Incorporated Ted Nadeau's findings
- Clear sprint structure with outcomes
