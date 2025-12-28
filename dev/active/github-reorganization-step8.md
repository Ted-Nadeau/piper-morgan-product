# Step 8: GitHub Issue Reorganization Instructions

## New Issues to Create (12 total)

### Alpha Critical Sprint (January Week 1-2)
1. **ALPHA-SETUP-NOTION**: Add Notion integration to setup wizard
   - Milestone: MVP
   - Sprint: A13 - Alpha Setup
   - Estimate: 4 hours

2. **ALPHA-SETUP-SLACK**: Add Slack OAuth to setup wizard
   - Milestone: MVP
   - Sprint: A13 - Alpha Setup
   - Estimate: 6 hours

3. **ALPHA-SETUP-CALENDAR**: Add Google Calendar to setup wizard
   - Milestone: MVP
   - Sprint: A13 - Alpha Setup
   - Estimate: 4 hours

4. **ALPHA-SETUP-VERIFY**: Integration health check dashboard
   - Milestone: MVP
   - Sprint: A13 - Alpha Setup
   - Estimate: 3 hours

### MUX Gate Issues (February-March)
5. **MUX-GATE-1**: Foundation Phase Complete
   - Milestone: MVP
   - Sprint: MUX-V1 Foundation
   - Type: Gate/Milestone

6. **MUX-GATE-2**: Core Implementation Complete
   - Milestone: MVP
   - Sprint: MUX-X1 Core
   - Type: Gate/Milestone

7. **MUX-GATE-3**: Integration Phase Complete
   - Milestone: MVP
   - Sprint: MUX-Integration
   - Type: Gate/Milestone

8. **MUX-GATE-4**: Interaction Design Complete
   - Milestone: MVP
   - Sprint: MUX-Interaction
   - Type: Gate/Milestone

---

## Existing Issue Reassignments

### Move TO A13 - Alpha Setup (January Week 1-2)
Keep in current sprint:
- #440 ALPHA-SETUP-TEST (already in A11)
- #358 SEC-ENCRYPT-ATREST (S2 → A13)
- #322 ARCH-FIX-SINGLETON (S2 → A13)
- #484 ARCH-SCHEMA-VALID (S2 → A13)

Add quick wins:
- #449 FLY-MAINT-CLEANUP (move to A13)
- #486 BUG: test_intent_enricher (move to A13)

### Move TO Beta Enablers Sprint (January Week 3-4)
- #519 Canonical Queries B-1 (unassigned → Beta Enablers)
- #520 Canonical Queries B-2 (unassigned → Beta Enablers)
- #522 Canonical Queries B-4 (unassigned → Beta Enablers)
- #517 Update multi-agent protocols (unassigned → Beta Enablers)
- #488 MUX-INTERACT-DISCOVERY (I1 → Beta Enablers)
- #102 CONV-UX-GREET (M2 → Beta Enablers)
- #242 CONV-MCP-STANDUP-INTERACTIVE (M2 → Beta Enablers)
- #365 SLACK-ATTENTION-DECAY (M2 → Beta Enablers)

### MUX Sprint Reorganization

**MUX-V1 Foundation (February Week 1-2)**
Keep these in V1:
- #401 MUX-VISION
- #399 MUX-VISION-OBJECT-MODEL
- #404 MUX-VISION-GRAMMAR-CORE
- #400 MUX-VISION-CONSCIOUSNESS
- #405 MUX-VISION-METAPHORS
- #477 Refine todo list UX

**MUX-X1 Core (February Week 3-4)**
Reassign from X1 to this sprint:
- #432 MUX-TECH (meta)
- #433 MUX-TECH-PHASE1-GRAMMAR
- #434 MUX-TECH-PHASE2-ENTITY
- #435 MUX-TECH-PHASE3-OWNERSHIP

**MUX-Integration (March Week 1-2)**
Create new sprint, move:
- #406 MUX-VISION-FEATURE-MAP (V2 → Integration)
- #407 MUX-VISION-STANDUP-EXTRACT (V2 → Integration)
- #408 MUX-VISION-LIFECYCLE-SPEC (V2 → Integration)
- #431 MUX-VISION-LEARN (V2 → Integration)
- #474 Enable full list management (V2 → Integration)
- #436 MUX-TECH-PHASE4-COMPOSTING (X1 → Integration)

**MUX-Interaction (March Week 3-4)**
Reassign from I1/I2/I3 to this sprint:
- #402 MUX-INTERACT (meta)
- #410 MUX-INTERACT-CANONICAL-ENHANCE
- #411 MUX-INTERACT-RECOGNITION
- #412 MUX-INTERACT-INTENT-BRIDGE
- #413 MUX-INTERACT-TRUST-LEVELS
- #414 MUX-INTERACT-DELEGATION
- #415 MUX-INTERACT-PREMONITION
- #416 MUX-INTERACT-WORKSPACE
- #417 MUX-INTERACT-ATTENTION
- #418 MUX-INTERACT-MOMENT-UI

**MUX-Polish (April Week 1-2)**
Reassign from P1-P4 to this sprint:
- All P1-P4 issues (#403, #419-430)

---

## Issues to CLOSE

- #524 Pattern Sweep 2.0 - CLOSE with evidence from today's results
- #503 FLY-AUDIT Dec 22 - If complete, close
- #480 FLY-AUDIT Dec 8 - If complete, close

---

## Sprint Structure Summary

### New Sprint Names & Dates

1. **A13 - Alpha Setup** (January Week 1-2)
   - 8 issues (4 new setup + 4 existing)

2. **Beta Enablers** (January Week 3-4)
   - 8-9 issues (conversational + queries)

3. **MUX-V1 Foundation** (February Week 1-2)
   - 6 issues + Gate-1

4. **MUX-X1 Core** (February Week 3-4)
   - 4 issues + Gate-2

5. **MUX-Integration** (March Week 1-2)
   - 6 issues + Gate-3

6. **MUX-Interaction** (March Week 3-4)
   - 10 issues + Gate-4

7. **MUX-Polish** (April Week 1-2)
   - 13 issues

8. **MVP-Beta** (April Week 3-4)
   - Final integration and launch

---

## Milestone Updates

All issues should be in **MVP** milestone except:
- Enterprise features → **Enterprise** milestone
- Fast Follow items → **Fast Follow** milestone

---

## Labels to Add

For new issues:
- `alpha-critical` for setup issues
- `gate` for MUX gate issues
- `quick-win` for #449, #486, #102, #242, #365

---

## Notes for Manual Implementation

1. Create new issues first
2. Update existing issue sprint assignments
3. Create new sprints if needed
4. Add gates to each MUX sprint
5. Close completed pattern sweep issues
6. Update labels for clarity

Total changes:
- 8 new issues to create
- ~50 issues to reassign to new sprints
- 3 issues to close
- 5 new sprint names to create/update

---

*This completes Step 8 planning. Ready for manual GitHub updates.*
