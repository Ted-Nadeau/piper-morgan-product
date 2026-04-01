# Architecture Review Request: ADR-059 Workflow Dispatcher

**From**: Lead Developer
**To**: Chief Architect
**Date**: 2026-03-19
**Priority**: High (blocking #922 fix)
**Re**: ADR-059 — Workflow Dispatcher and Offer System Consolidation

---

## Request

Please review ADR-059 (`docs/internal/architecture/current/adrs/adr-059-workflow-dispatcher-offer-consolidation.md`) and provide guidance on the three architectural questions.

## Summary

We have three independent offer/acceptance systems (#824, #888, #852) that race for control of user affirmations. This caused #922 (critical UX bug: "Sure" → dead end). PM has directed:
1. Remove onboarding workflow (Gall's Law — simplify first)
2. Add a registry-based workflow dispatcher (thin routing, no business logic)
3. Consolidate where architecturally sound

## Questions Needing Your Input

**Q1: New component or fold into WorkflowOfferService?**

The dispatcher maps `workflow_type → entry_point`. Currently WorkflowOfferService handles offer presentation (should_offer, format_offer, throttling). My recommendation: separate component, same pattern as action_registry.py being separate from intent_service.py.

**Q2: Onboarding registration cleanup?**

Remove entirely for now (option a), or replace with generic "workflow in progress" adapter (option c)? I recommend (a) now, (c) later.

**Q3: Resume offers through dispatcher?**

Resume is conceptually "start workflow X with pre-existing state." Route through dispatcher with `resume_session` param? Or keep separate?

## Context You Should Know

- The CIO's methodology audit identified "extend without verifying" as a sub-pattern of Assembly Assumption (Pattern-062). This ADR addresses the structural cause.
- The action registry from #913 (34 entries, disposition-based) is working well. This dispatcher follows the same pattern.
- PM referenced the OpenClaw article's "thin Gateway" design principle — dispatcher should be dumb plumbing.
- Intent processing pipeline in intent_service.py is ~1700 lines. This refactor touches ~100 lines in the acceptance handling section (lines 440-610).

## Timeline

PM wants to proceed promptly. If you can review today, we can implement tomorrow. The meeting slot-filling path is the only currently-functional workflow, so the refactor risk is contained.

---

*Lead Developer, 2026-03-19*
