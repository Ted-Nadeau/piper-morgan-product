# Session Log: 2025-12-21-0654 - Lead Developer - Discovery Architecture Epic

**Role**: Lead Developer
**Model**: Claude Opus 4.5
**Date**: Sunday, December 21, 2025
**Time**: 6:54 AM

---

## Session Context

Continuing from overnight work on #487 (intent classification fix). Implementation complete, now creating architectural epic for P2 systemic fix.

**Previous Session Summary** (Dec 20):
- Investigated #487 using Five Whys protocol
- Identified systemic issue: command-oriented vs discovery-oriented design
- Implemented pattern-based fix (IDENTITY + GUIDANCE patterns)
- 31 tests passing

**Today's Focus**:
1. Create epic for P2 architectural change (discovery-oriented intent)
2. Link to Modeled UX (UX 2.0) superepic per PM direction
3. Manual verification of #487 fix

---

## Epic: Discovery-Oriented Intent Architecture

### Problem Statement

The current intent system is **command-oriented** - it assumes users know what to ask for. This creates friction for:
- New users discovering capabilities
- Alpha testers exploring features
- Anyone asking "what can you do?"

### Current State (Symptom-Based Patching)

We've been adding patterns case-by-case:
- #487: Added "what services", "help setup" patterns
- More gaps will appear as users try other discovery phrases

### Desired State (Systemic Solution)

A **discovery-oriented** intent path that:
1. Routes "what can you do?" type queries to a dedicated handler
2. Dynamically enumerates capabilities from PluginRegistry
3. Auto-updates as plugins are added/removed
4. Provides consistent discovery UX

### Architecture Components

```
User: "What can you do?"
        ↓
Pre-classifier: DISCOVERY pattern match
        ↓
Intent: DISCOVERY category
        ↓
Handler: _handle_discovery_intent()
        ↓
PluginRegistry.list_capabilities() → Dynamic capability list
        ↓
Response: Structured capability menu
```

### Implementation Phases

**Phase 1: DISCOVERY Intent Category**
- Add DISCOVERY to IntentCategory enum
- Add patterns to pre_classifier
- Create stub handler

**Phase 2: PluginRegistry Capability Enumeration**
- Add `list_user_capabilities()` method
- Bridge plugin metadata to user-facing descriptions
- Filter by enabled/configured plugins

**Phase 3: Discovery Handler Implementation**
- Build structured response from PluginRegistry
- Format for chat display
- Include examples/hints per capability

**Phase 4: Integration with Modeled UX**
- Align with UX 2.0 interaction patterns
- Consider guided onboarding flows
- Enable progressive disclosure

---

## Files to Create/Modify

| File | Change |
|------|--------|
| `services/shared_types.py` | Add DISCOVERY to IntentCategory |
| `services/intent_service/pre_classifier.py` | Add DISCOVERY_PATTERNS |
| `services/intent_service/canonical_handlers.py` | Add _handle_discovery_intent |
| `services/plugins/plugin_registry.py` | Add list_user_capabilities() |
| `tests/integration/test_discovery_intent.py` | E2E tests |

---

## Beads Summary (This Session)

| ID | Issue | Priority |
|----|-------|----------|
| piper-morgan-ti9 | Pre-classifier over-greedy matching | P2 |
| piper-morgan-3t7 | Plugin capabilities not bridged to intent | P2 |
| piper-morgan-d8f | No capability discovery tests | P2 |
| piper-morgan-e4k | test_bypass_prevention.py 401 error | P3 |

---

---

## Epic Created

**Issue #488**: [EPIC: Discovery-Oriented Intent Architecture - Bridge Plugin Capabilities to User Discovery](https://github.com/mediajunkie/piper-morgan-product/issues/488)

**Priority**: P2
**Labels**: epic, architecture

**MUX Placement** (7:23 AM):
- **Parent**: MUX-INTERACT: Interaction Design (#402)
- **Related**:
  - MUX-INTERACT-CANONICAL-ENHANCE (#410) - Evolve canonical queries to orientation
  - MUX-INTERACT-INTENT-BRIDGE (#412) - Bridge intent classification to recognition

Updated #488 body to include MUX parent linkage and related issues.

---

**Status**: ✅ Epic #488 created and linked to MUX-INTERACT hierarchy
