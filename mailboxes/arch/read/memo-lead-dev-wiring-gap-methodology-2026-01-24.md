# Memo: Wiring Gap Methodology - Lessons from MUX-WIRE Epic

**From:** Lead Developer
**To:** Chief Architect
**Date:** 2026-01-24
**Re:** Methodology learnings from #670 MUX-WIRE remediation
**Response-Requested:** no (informational)

---

## Executive Summary

During the MUX-WIRE epic (#670), we remediated 6 issues where services had comprehensive test coverage but were unreachable by users. This memo documents the pattern, proposes detection mechanisms, and suggests architectural guardrails.

## The Wiring Gap Pattern

### Definition

A **wiring gap** occurs when:
1. A service is implemented with passing tests
2. The service has no route from user intent to invocation
3. The service appears "complete" by test metrics but is unusable

### Case Study: Issues #671-#676

| Issue | Service | Tests | User Symptom |
|-------|---------|-------|--------------|
| #671 | DiscoveryService | 50+ pass | "help" → GUIDANCE not DISCOVERY |
| #672 | ProjectRepository | 56 pass | /projects page shows 0 projects |
| #673 | TrustService | 45 pass | Trust queries → generic IDENTITY |
| #674 | UserHistoryService | 50+ pass | Memory queries unrecognized |
| #675 | PortfolioService | 56 pass | Portfolio ops → "no capability" |
| #676 | WorkflowUI | N/A | Spurious "Starting workflow..." |

### Root Cause Analysis

The pattern emerged from **layered architecture without vertical integration testing**:

```
Layer 4: [Service Layer]     ← Tests pass here
Layer 3: [Handler Layer]     ← Gap: No routing
Layer 2: [Intent Layer]      ← Gap: No patterns
Layer 1: [User Interface]    ← Users blocked
```

Services were developed with unit tests at Layer 4, but:
- No integration tests verified Layer 1 → Layer 4 flow
- No patterns in pre_classifier to recognize intents
- No handlers in canonical_handlers to route to services

## Detection Mechanisms

### Proposed: Service Reachability Audit

Add to CI pipeline:
```python
# For each registered service:
1. Extract public methods
2. Search pre_classifier for matching patterns
3. Search canonical_handlers for routing
4. Flag services with no user-reachable paths
```

### Proposed: Pattern Completeness Check

```python
# For each IntentCategory:
1. Verify patterns exist in pre_classifier
2. Verify handler exists in canonical_handlers
3. Verify handler routes to actual service
4. Fail build if any category is unrouted
```

## Architectural Recommendations

### 1. Vertical Slice Development

**Current**: Build service → test service → (forget wiring)

**Proposed**: Service + patterns + handler as atomic unit

```python
# New service checklist:
- [ ] Domain model
- [ ] Service implementation
- [ ] Unit tests (service layer)
- [ ] IntentCategory enum entry
- [ ] Pre-classifier patterns
- [ ] Canonical handler routing
- [ ] Integration test (intent → response)
```

### 2. Pattern-Driven Service Design

Start from user intent, work backward:

```
"What would a user say?" → Pattern → Category → Handler → Service
```

Rather than:

```
"What capability do we need?" → Service → ??? → User can't find it
```

### 3. Intent Coverage Metrics

Track coverage similar to code coverage:

```
Intent Categories: 15 total
  Routed: 13 (87%)
  Unrouted: 2 (PORTFOLIO, MEMORY) ← Alert!
```

## Implementation Effort

The actual fix for each wiring gap was small:
- Add enum value (~1 line)
- Add patterns (~10-20 lines)
- Add handler routing (~5 lines)
- Add handler method (~50-100 lines)

The investigation to find gaps was larger - hence the value of automated detection.

## Recommended Actions

1. **Short-term**: Add service reachability check to PR template
2. **Medium-term**: Add automated pattern completeness check
3. **Long-term**: Consider generating patterns from service annotations

## Appendix: Files Modified in MUX-WIRE

```
services/shared_types.py          - Added TRUST, MEMORY, PORTFOLIO
services/intent_service/pre_classifier.py - Added 3 pattern sets
services/intent_service/canonical_handlers.py - Added 3 handlers
services/intent/intent_service.py - Fixed workflow_id="" → None
web/api/routes/projects.py        - Added preference fallback
web/static/js/chat.js             - Fixed workflow_id check
```

---

*This memo documents learnings from a successful remediation. The pattern should inform future development practices.*
