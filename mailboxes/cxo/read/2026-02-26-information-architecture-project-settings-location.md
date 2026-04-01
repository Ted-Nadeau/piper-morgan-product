# Memo: Information Architecture — Where Should Project Configuration Live?

**From**: Lead Developer
**Date**: 2026-02-26
**Re**: Settings vs Project Detail vs Both — needs product design guidance

## Context

While implementing #861 (Settings page — project integration management), we hit an information architecture question that needs product design guidance before we can resolve it properly.

## The Question

Users need to manage project-level configuration (linked repositories, tool integrations like Jira/Slack). Where should this UI live?

### Option A: Project Detail Page
- User navigates to Projects → selects project → sees Integrations/Repos tabs
- Pro: Configuration lives where the context is (the project itself)
- Pro: Natural for "I'm looking at my project, let me configure it"
- Con: Project detail page becomes complex

### Option B: Settings → Projects
- User navigates to Settings → Projects section → selects project → manages config
- Pro: All configuration in one place (Settings)
- Pro: Consistent with "Settings is where I configure things" mental model
- Con: Requires context-switching away from the project

### Option C: Both (with one as canonical)
- Project detail has a "Settings" link that deep-links to Settings → Projects → {this project}
- Or Settings → Projects links to project detail with config tab
- Pro: Multiple paths to same destination
- Con: More surface area to maintain

## Current Decision

For #861 we're implementing **Option B** (Settings → Projects) as the pragmatic interim path. This doesn't preclude any future IA decision.

## What We Need

Product design guidance on the long-term IA for project configuration. This affects:
- Navigation patterns
- Template architecture
- URL structure
- User mental model

No urgency — the interim solution works. But flagging early so it can be considered holistically alongside other IA decisions (e.g., the Product ↔ Project relationship question from the earlier memo today).

## Related
- #861 (Settings page — project integration management)
- #866 (Repository as first-class entity)
- Earlier memo: Domain model Product/Project/Repository relationships
