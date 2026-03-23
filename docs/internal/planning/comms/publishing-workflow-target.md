# Publishing Workflow: Blog-First Target State

*One-pager for re-orientation. Discussion started Mar 22, 2026.*

---

## The Goal

Make pipermorgan.ai the canonical home for all published content. Medium and LinkedIn become syndication channels, not primary publishing surfaces.

## Why

- Blog posts already have infrastructure (269 entries in blog-metadata.csv, images in webp, fetch/sync scripts working)
- Medium currently serves as both editing surface and publishing platform — these should separate
- Only 1 post is actually blog-hosted today ("Four Voices, One Spec") despite infrastructure being ready
- PM wants to edit markdown → publish, not context-switch to Medium's editor for final polish

## Current Workflows (As Of Mar 22, 2026)

| Type | Draft | Final Edit | Image | Primary Publish | Syndication | Track |
|------|-------|-----------|-------|----------------|-------------|-------|
| Narrative | Repo draft | Medium editor | ChatGPT cartoon | Medium | — | Editorial calendar CSV |
| Insight | Repo draft | Medium editor | ChatGPT cartoon | Medium | LinkedIn | Editorial calendar CSV |
| Weekly Ship | CoS synthesis | — | — | LinkedIn newsletter | — | Editorial calendar CSV |

## Target Workflow (All Content Types)

```
1. Finalize markdown draft in repo (docs/public/comms/drafts/)
2. Generate cartoon via ChatGPT (narrative + insight only)
3. Publish to pipermorgan.ai    →  /publish-to-blog skill
4. Syndicate to Medium          →  manual paste, set canonical URL to blog
5. Cross-post to LinkedIn       →  manual (or newsletter for Ships)
6. Update editorial calendar    →  CSV in both repos
```

The `/publish-to-blog` skill (v0.2) already handles step 3 mechanically. Steps 4-5 remain manual for now.

## Key Decisions Made

- **Editing surface**: Markdown in this repo, not Medium's editor
- **Canonical URL**: pipermorgan.ai/blog/{slug}
- **Medium's new role**: Syndication only (import with canonical link back)
- **LinkedIn**: Unchanged — still manual cross-post or newsletter

## Open Threads (For Future Sessions)

1. **Weekly Ship on the blog**: Needs its own section/category on pipermorgan.ai. Currently LinkedIn-only.
2. **Medium era/cluster refactoring**: The blog's era categorization (based on past omnibus cluster analysis) is overdue for an update.
3. **Website navigation**: Cosmetic and structural presentation issues to resolve (separate from workflow).
4. **Automation boundary**: How much of steps 4-6 can be scripted without building a CMS? Medium import API? LinkedIn API? Or keep manual with a checklist?
5. **Backlog migration**: 269 posts have metadata but 0 are blog-hosted (render via Medium RSS). Strategy for migrating high-value posts to blog-hosted content.
6. **Draft preview**: How does PM preview the final rendered post before publishing? Local dev server? Staging deploy?

## Existing Infrastructure

| Component | Location | Status |
|-----------|----------|--------|
| `/publish-to-blog` skill | `.claude/skills/publish-to-blog/SKILL.md` | v0.2, working |
| Blog metadata CSV | `../piper-morgan-website/data/blog-metadata.csv` | 269 entries |
| Blog content JSON | `../piper-morgan-website/src/data/blog-content.json` | Stores HTML for blog-hosted posts |
| Editorial calendar | `docs/internal/planning/comms/editorial-calendar.csv` | 305 entries, source of truth for this repo |
| Fetch/sync scripts | `../piper-morgan-website/scripts/` | `fetch-blog-posts.js`, `sync-csv-to-json.js` |
| Draft location | `docs/public/comms/drafts/` | Markdown drafts ready for editing |

## Success Criteria

- [ ] PM can finalize a markdown draft and say "publish this" — one skill invocation gets it on pipermorgan.ai
- [ ] Medium syndication has a documented manual checklist (or partial automation)
- [ ] Weekly Ships appear on pipermorgan.ai in their own section
- [ ] Editorial calendar reflects canonical blog URLs for new publications
- [ ] No new content goes to Medium first

---

*Discussion started: Mar 22, 2026 (Docs session)*
*Next: Continue in future session — refine publish-to-blog skill, address Weekly Ship section, discuss Medium syndication checklist*
