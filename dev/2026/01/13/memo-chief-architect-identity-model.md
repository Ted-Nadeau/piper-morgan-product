# Memo: Chief Architect Consultation - Identity Model Refactoring

**To**: Chief Architect
**From**: Lead Developer (Claude Code)
**Date**: 2026-01-13
**Re**: Request for architectural guidance on unified identity/context model
**Issue**: #584
**ADR**: ADR-051 (PROPOSED)

---

## Executive Summary

Investigation of Issue #584 revealed that the recurring `user_id`/`session_id` bugs are symptoms of a deeper architectural gap: **the codebase lacks a unified model for identity and request context**. I've documented the current state and drafted ADR-051 proposing a `RequestContext` pattern, but this is a foundational change that warrants your review before implementation.

## Background

PM observed (2026-01-12): *"there seem to be a lot of bugs around user_id and session_id and how to properly pass them"*

Investigation found this is not just a documentation gap - it's a **model problem**:
- 14 different ID concepts exist
- `user_id` has 5 different type representations
- `session_id` is overloaded for 3 different purposes
- No single source of truth for request context

## What I've Done

1. **Documented current state** in CLAUDE.md with warnings and patterns to follow
2. **Created ADR-051** proposing `RequestContext` as unified model
3. **Identified critical files** showing the inconsistencies

## What I Need From You

Your guidance on five specific questions in ADR-051:

### 1. Abstraction Design
Is `RequestContext` (single object with user + conversation + request metadata) the right abstraction? Or should these be separate concerns?

**Options**:
- A) Single `RequestContext` (proposed)
- B) Split into `UserContext` + `ConversationContext` + `RequestMetadata`
- C) Different pattern entirely

### 2. Type Strategy
For `user_id`, should we standardize on:
- A) `UUID` internally, `str` at boundaries (proposed)
- B) `str` everywhere for simplicity
- C) `UUID` everywhere with automatic serialization

### 3. Migration Approach
- A) Incremental 4-phase migration (proposed)
- B) Big-bang refactor in one sprint
- C) Opportunistic - fix as we touch files

### 4. Scope
Should this refactor address:
- A) Core three IDs only (`user_id`, `session_id`, `conversation_id`)
- B) All 14 ID concepts
- C) Start with core, expand later

### 5. Alternative Patterns
Are there patterns from your experience that handle this better than explicit context passing? (DI, contextvars, middleware, etc.)

## Risk Assessment

**If we proceed without review**: Risk of over-engineering or choosing wrong pattern, requiring another refactor later.

**If we do nothing**: Bugs will continue. The documentation I added helps but doesn't prevent the underlying issues.

**If we delay too long**: More features will be built on the broken foundation.

## Recommendation

I recommend a brief architecture review session before implementation. The proposed `RequestContext` pattern is straightforward but foundational - getting it right matters more than getting it fast.

## Artifacts for Review

- **ADR-051**: `docs/internal/architecture/current/adrs/adr-051-unified-user-session-context.md`
- **Current State Doc**: CLAUDE.md, "Identity Model" section
- **Investigation Data**: Agent exploration output (available on request)

## Timeline

No urgency - this is tech debt, not a blocking bug. The documentation I added provides interim guidance. Happy to proceed with your feedback whenever convenient.

---

_Memo created: 2026-01-13 13:30_
_Status: Awaiting Chief Architect response_
