# Proposal: Design System Front Door

**Date**: 2026-01-08
**Author**: Documentation Manager
**Status**: Draft for PM review

---

## Problem

UX specs are scattered across dev/active/ with no central index. When an LLM agent (or human) needs to implement UI changes, they have no single place to:
1. Discover what guidelines exist
2. Understand the design philosophy
3. Find the authoritative spec for a given domain
4. Ensure their work aligns with established patterns

**Risk**: Without a front door, agents may "invent" solutions that contradict existing specs or duplicate work already done.

---

## Proposal: Create `docs/internal/design/README.md`

A structured index page that serves as the canonical entry point for all UX/design work.

---

## Proposed Structure

```markdown
# Piper Morgan Design System

## Purpose

This directory contains UX specifications, design briefs, and interaction
guidelines for Piper Morgan. All UI/UX work should consult these documents
before implementation.

## Design Philosophy

Piper Morgan's UX follows these core principles:

1. **Conversational First**: Piper is a colleague, not a tool
2. **Trust Gradient**: Behavior adapts based on relationship maturity
3. **Discovery Over Documentation**: Users learn by doing, not reading
4. **Contextual Intelligence**: Actions informed by what Piper knows
5. **Graceful Degradation**: Always provide value, even with limited context

## Document Hierarchy

When specs conflict, defer to higher-numbered authority:

1. PDRs (Product Decision Records) - Strategic intent
2. Design Briefs - Tactical direction
3. UX Specs - Implementation details
4. Voice Guides - Tone and copy

## Current Specifications

### Interaction Patterns
| Spec | Domain | Status | Consult When... |
|------|--------|--------|-----------------|
| [Cross-Session Greeting UX](specs/cross-session-greeting-ux-spec-v1.md) | Greetings | v1 Final | Implementing greeting logic |
| [Contextual Hint UX](specs/contextual-hint-ux-spec-v1.md) | Suggestions | v1 Final | Adding proactive hints |
| [Multi-Entry FTUX](specs/multi-entry-ftux-exploration-v1.md) | Onboarding | v1 Final | Modifying setup flow |
| [Empty State Voice Guide](specs/empty-state-voice-guide-v1.md) | Empty States | v1 Final | Writing empty state copy |

### Quality & Measurement
| Spec | Domain | Status | Consult When... |
|------|--------|--------|-----------------|
| [B1 Quality Rubric](specs/b1-quality-rubric-v1.md) | Quality Gates | v1 Final | Assessing feature readiness |

### Strategic Direction
| Brief | Domain | Status | Consult When... |
|-------|--------|--------|-----------------|
| [Conversational Glue](briefs/conversational-glue.md) | Conversation UX | Active | Designing conversation flows |
| [Discovery UX Strategy](briefs/discovery-ux-strategy.md) | Capability Discovery | Active | Helping users find features |

## For LLM Agents

**Before implementing any UI/UX changes:**

1. Read this README to understand the design philosophy
2. Check the spec table above for relevant documents
3. If your domain isn't covered, flag for PM/CXO review before proceeding
4. When in doubt, favor consistency with existing patterns over novelty

**Red flags that suggest you're going rogue:**
- Creating new interaction patterns not in specs
- Writing copy that doesn't match voice guide tone
- Adding UI elements without checking empty state guidance
- Implementing greetings without consulting greeting spec

## For Human Designers

- New specs go in `specs/` with naming: `[domain]-[type]-spec-v[n].md`
- New briefs go in `briefs/` with naming: `[domain]-brief.md`
- Update this README when adding new documents
- Version specs (v1, v2) rather than overwriting

## Related Resources

- [PDRs](../pdr/) - Product Decision Records (strategic)
- [ADRs](../architecture/current/adrs/) - Architecture Decision Records (technical)
- [Pattern Library](../architecture/current/patterns/) - Implementation patterns

---

*Last updated: 2026-01-08*
*Maintainer: CXO / Documentation Manager*
```

---

## Key Features for LLM Consumption

1. **Explicit "Consult When" Column**: Tells agents exactly when to read each spec
2. **Red Flags Section**: Warns agents about common deviation patterns
3. **Document Hierarchy**: Resolves conflicts before they happen
4. **Design Philosophy**: Grounds all work in core principles
5. **Version Tracking**: Prevents agents from using outdated specs

---

## Implementation Steps

1. Create `docs/internal/design/` directory
2. Create `docs/internal/design/specs/` subdirectory
3. Create `docs/internal/design/briefs/` subdirectory
4. Move specs from dev/active/ to specs/
5. Move briefs from dev/active/ to briefs/
6. Create README.md with above content
7. Update NAVIGATION.md
8. Add reference in CLAUDE.md under "Documentation" section

---

## PM Decision Points

1. **Design Philosophy**: Are the 5 principles above correct? Should CXO review?
2. **Document Hierarchy**: Is PDR > Brief > Spec > Voice Guide the right order?
3. **Maintainer**: CXO primary, Doc Manager secondary?
4. **CLAUDE.md Integration**: Add to "Common Development Tasks" section?

---

## Benefits

- **For Agents**: Single entry point prevents rogue implementations
- **For Humans**: Clear inventory of what exists
- **For PM**: Easier to identify gaps in design coverage
- **For CXO**: Authoritative home for design system

---

*End of Proposal*
