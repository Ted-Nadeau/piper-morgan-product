# Blog Publishing Quick Guide

**Last Updated**: March 16, 2026

Your publishing flow, step by step.

---

## Writing → Blog → Medium → LinkedIn

### 1. Finish the Draft

Your drafts live in `docs/public/comms/drafts/`. Comms produces them, you download and edit.

```
docs/public/comms/drafts/draft-{title}.md
```

When you're happy with it, you're ready to publish.

### 2. Update the Editorial Calendar

Open `docs/internal/planning/comms/editorial-calendar.csv` and find the row for your piece. Update:

| Field | Set to |
|-------|--------|
| status | `published` |
| pubDate | today's date (YYYY-MM-DD) |
| canonicalSite | `distributed` |
| blogPath | `/blog/{slug}` |
| blogURL | `https://pipermorgan.ai/blog/{slug}` |

### 3. Publish to pipermorgan.ai

In the website repo (`../piper-morgan-website`):

```bash
cd ../piper-morgan-website
git pull origin main
```

**a. Add the image** (if not already there):
```bash
# Images go here as .webp:
cp ~/path/to/{cartoon}.png public/assets/blog-images/{cartoon}.webp
```

**b. Add a row to `data/blog-metadata.csv`**:
```
slug,hashId,title,chatDate,imageSlug,workDate,pubDate,category,cluster,featured,notes
your-post-slug,,Your Post Title,,cartoon-name.webp,2026-03-16,2026-03-16,building,,,
```

**c. Rebuild the JSON** (if the script works):
```bash
node scripts/sync-csv-to-json.js
```

**d. Commit and push**:
```bash
git add data/ src/data/ public/assets/blog-images/
git commit -m "Add blog post: Your Post Title"
git push
```

### 4. Syndicate to Medium

Once the blog post is live on pipermorgan.ai:
1. Copy content to Medium
2. Publish on Medium
3. Update `editorial-calendar.csv` with the Medium URL

### 5. Cross-post to LinkedIn (when relevant)

1. Post to LinkedIn
2. Update `editorial-calendar.csv` with the LinkedIn URL

### 6. Commit the calendar update

```bash
cd ../piper-morgan
git add docs/internal/planning/comms/editorial-calendar.csv
git commit -m "editorial calendar: mark {title} as published"
```

---

## Quick Reference

| What | Where |
|------|-------|
| Drafts | `docs/public/comms/drafts/` |
| Editorial calendar (source of truth) | `docs/internal/planning/comms/editorial-calendar.csv` |
| Website repo | `../piper-morgan-website` |
| Blog metadata | `../piper-morgan-website/data/blog-metadata.csv` |
| Blog images | `../piper-morgan-website/public/assets/blog-images/` |
| Publish skill (for agents) | `.claude/skills/publish-to-blog/SKILL.md` |

## Status Lifecycle

`queued` → `drafted` → `ready` → `published`

- **queued**: Comms produced it, title known
- **drafted**: Draft in `drafts/`, needs your editing pass
- **ready**: Your edits done, ready to go
- **published**: Live on blog (then Medium, then LinkedIn)
