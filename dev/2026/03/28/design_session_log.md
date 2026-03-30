# One Job Design Session - Card Deck Experience

**Date**: 2025-08-06
**Start Time**: 7:06 AM PST
**Focus**: Mobile-first card deck interface redesign

## Vision Summary
Transform One Job into a minimalist card deck experience optimized for iPhone, removing all text/UI chrome by default.

## Core Design Principles
- **Mobile-first**: iPhone optimized, larger viewports are elaborations
- **Decluttered**: All type off screen by default
- **Card deck metaphor**: Stack of playing cards taking up most viewport
- **Ceremonial interaction**: Cards start face-down, flip to reveal tasks

## Three-Element Viewport Structure
1. **Background canvas**: Minimal margin around main object
2. **Card stack**: Takes up most real estate, like playing card deck
3. **Menu affordance**: Access to add card, switch stacks, integrations

## Interaction Flow
- **Initial state**: Face-down deck with One Job logo on card back
- **Tap to reveal**: Card animates and flips to show current task
- **Swipe right**: Complete task (moves to Done stack) - existing behavior
- **Swipe left**: Defer task - card flips face-down and moves to bottom of stack

## Open Questions for Discussion
1. **Post-deferral behavior**: After swiping left, does next card auto-flip or wait for tap ceremony?
2. **Menu affordance design**: How to integrate add/navigate/configure options without cluttering UI?

## Decisions Made ✅
**7:11 AM - Core Interaction Patterns:**
1. **Auto-flip with timeout**: Cards auto-flip after defer/complete, then auto-close after ~1 minute of inactivity
2. **Long-press menu**: Hold deck to reveal floating action buttons (avoids edge gesture difficulty)
3. **Static logo**: No task count on card back - maintains focus on single task
4. **Consistent auto-flip**: Both defer and complete trigger next card to auto-flip
5. **Empty state**: Dashed outline, cheerful message, plus button (long-press reveals full menu)

## Design Questions to Explore
- Auto-close timing: 1 minute feels right, or different duration?
- Long-press menu layout: Floating buttons around deck or other pattern?

## Additional Decisions Made ✅
**7:16 AM - Expanded Interactions:**
6. **Card detail view**: Tap face-up card → expands to full viewport, stays open indefinitely
7. **Return from detail**: Tap outside card affordances → shrinks back, resumes timeout behavior
8. **Long-press discoverability**: Subtle pulse or shadow hint for teachability
9. **Menu items confirmed**: Add task, Switch stacks, Integrations, Settings
10. **Spatial navigation vision**: Stacks exist in domains (home/work/projects), each with main+done stacks
11. **V1 navigation scope**: Simple done/main stack switching, evolve spatial model later
12. **Animation variety**: Small menu of flip variations, energy-efficient implementation

## Spatial Model Vision (Future)
- Domains contain multiple stack types (home/work, projects)
- Each domain has main stack + done stack + substacks
- When opening substack, parent becomes canvas for substack's stacks
- Hierarchical spatial navigation vs. current flat tab system

## Implementation Notes
- [To be filled as we progress]
