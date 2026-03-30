---
name: publish-to-blog
description: Publish a finished blog post from this repo to the pipermorgan.ai website
  repo. Use when PM says "publish this post", "push to the blog", or when a draft
  is marked ready in the editorial calendar. Bridges piper-morgan → piper-morgan-website.
scope: role-specific
version: 0.3
created: 2026-03-16
updated: 2026-03-29
---

# publish-to-blog

Publish a finished markdown blog post to the pipermorgan.ai website repository.

## When to Use

Use this skill when:
- PM says a draft is ready to publish to the blog
- A piece in the editorial calendar has status `ready` or `queued` with today's pubDate
- PM asks to "push to the blog" or "publish this post"

## Prerequisites

- The draft markdown file must exist in this repo (typically `docs/public/comms/drafts/`)
- The cartoon/featured image must be available in `dev/active/` (PM provides)
- The PM has provided: alt text, caption, and the next post title (for footer teaser)

### Environment Note

The website repo (`piper-morgan-website`) may not be accessible from this environment (e.g., Claude Code web). In that case, generate a **publish package** (script + HTML + metadata) that PM runs locally. See "Remote Execution Mode" below.

## Procedure

### Step 1: Gather Inputs from PM

Confirm or look up:
1. Which draft file? (check `docs/public/comms/drafts/`)
2. Title and dateline
3. Category: `building` or `insight`
4. Image file location in `dev/active/`
5. Alt text and caption
6. Next post title (for footer teaser — check editorial calendar)

### Step 2: Pre-Flight — Is This Post Already on Medium?

**Blog-first posts** (not yet on Medium): Generate a hashId:
```bash
python3 -c "import uuid; print(uuid.uuid4().hex[:12])"
```

**Backlog posts** (already on Medium): The hashId MUST match the Medium URL. Extract from the last segment after the final hyphen (e.g., `978f3ec50a57` from `discovery-is-the-bottleneck-978f3ec50a57`).

### Step 3: Convert Markdown to HTML

Strip the H1 title and dateline (metadata handles these). Handle:
- Headers (h2, h3)
- Paragraphs with inline formatting (bold, italic, code)
- Blockquotes
- Ordered and unordered lists
- Horizontal rules
- Smart quotes (`"` → `&ldquo;`/`&rdquo;`)

Save to `dev/active/publish-package/{slug}-content.html`.

### Step 4: Generate Publish Script

Create `dev/active/publish-package/publish-{slug}.sh`.

**CRITICAL — Path Rules:**
- Use **relative paths from the script's working directory** (`$PWD`)
- NEVER hardcode `../piper-morgan-product/` — the local directory name varies
- Reference files in this repo as `dev/active/...`, `docs/public/...` etc.
- Reference the website repo as `../piper-morgan-website`

The script should:

1. **Verify website repo** exists at `../piper-morgan-website`
2. **Find and convert image**: Look in `dev/active/` for the image file. Use `sips -Z 1200` to resize, then `cwebp` to convert to webp. Fall back to PNG if cwebp unavailable.
3. **Add to blog-metadata.csv** (13 columns):
   ```
   slug,hashId,title,chatDate,imageSlug.webp,workDate,pubDate,category,cluster,featured,extra,imageAlt,imageCaption
   ```
   Use Python csv writer with newline check (never `echo >>`).
4. **Add blog content** to `src/data/blog-content.json` — read HTML from the content file in this repo's publish-package directory.
5. **Run sync and fetch**: `node scripts/sync-csv-to-json.js && node scripts/fetch-blog-posts.js`
6. **Verify** the post appears in `src/data/medium-posts.json` with local URL.
7. **Commit and push** the website repo.

### Step 5: Update Editorial Calendar (This Repo)

Use the `/update-calendar` skill or manually update `docs/internal/planning/comms/editorial-calendar.csv`:
- status → `published`
- pubDate → today
- canonicalSite → `distributed`
- blogURL → `https://pipermorgan.ai/blog/{slug}`
- blogPath → `/blog/{slug}`
- altText → from PM
- caption → from PM

### Step 6: Commit This Repo

```bash
git add dev/active/publish-package/ docs/internal/planning/comms/editorial-calendar.csv docs/public/comms/drafts/
git commit -m "docs: publish package for {title} + CSV update"
```

Merge to main so PM can pull:
```bash
git checkout main && git merge {branch} --no-edit && git push origin main
git checkout {branch}
```

### Step 7: PM Runs Locally

PM pulls and runs:
```bash
git pull origin main
bash dev/active/publish-package/publish-{slug}.sh
```

### Step 8: Verify Deployment

After PM reports the script succeeded, verify:
- `https://pipermorgan.ai/blog/{slug}` loads with content and image
- Blog index shows the post with thumbnail
- Blog index links to `/blog/{slug}` not Medium URL

If the blog index links to Medium, the `fetch-blog-posts.js` script is overwriting `source: "blog-first"` entries. This is a known issue tracked in a memo to the web team.

### Step 9: Syndicate

PM does manually:
1. **Medium**: Paste content, publish, set canonical URL to `https://pipermorgan.ai/blog/{slug}`
2. **LinkedIn**: Cross-post (may adjust title)
3. PM provides URLs → Docs updates CSV via `/update-calendar`

### Step 10: Post-Publish CSV Update

When PM provides syndication URLs:
```
/update-calendar
```
Add mediumURL, liPubDate, linkedinURL to the row.

## Remote Execution Mode

When the website repo is not accessible (Claude Code web, cloud environments):

1. Prepare the **publish package** in `dev/active/publish-package/`:
   - `{slug}-content.html` — converted HTML
   - `publish-{slug}.sh` — self-contained script using relative paths
2. Merge to main so PM can pull
3. PM runs the script locally
4. PM reports back with verification + syndication URLs

## Website CSV Format (13 columns)

The website's `data/blog-metadata.csv` has a DIFFERENT schema from our editorial calendar (18 columns):

```
slug,hashId,title,chatDate,imageSlug,workDate,pubDate,category,cluster,featured,extra,imageAlt,imageCaption
```

**Do NOT confuse with our editorial calendar format.** The publish script writes to the website CSV; the `/update-calendar` skill writes to ours.

## Known Issues (as of v0.3)

1. **fetch-blog-posts.js overwrites blog-first URLs**: After Medium syndication, running the fetch script replaces local `/blog/{slug}` URLs with Medium URLs. Web team memo filed (Mar 29). Workaround: web team needs to respect `source: "blog-first"` entries.
2. **Image discovery**: PM saves images with varying names in `dev/active/`. The publish script should try multiple filename patterns.
3. **Large file hook**: Images over 500KB are rejected by pre-commit. Always compress with `sips -Z 1200` before committing.

## Anti-Patterns to Avoid

| Don't Do This | Why | Do This Instead |
|---------------|-----|-----------------|
| Hardcode `../piper-morgan-product/` in scripts | Local dir name varies (`piper`, `piper-morgan`, etc.) | Use relative paths from `$PWD` |
| Publish to Medium first | Blog should be canonical | Blog first, then syndicate |
| Generate random hashId for Medium posts | Won't match RSS data | Extract real hashId from Medium URL |
| Use `echo >>` to append CSV rows | May corrupt CSV | Use Python csv writer with newline check |
| Use `sips` for webp conversion | macOS sips can't write webp | Use `cwebp` (install via `brew install webp`) |
| Assume 11-column website CSV | Now 13 columns (imageAlt, imageCaption added) | Always use 13-column format |
| Skip the editorial calendar update | Source of truth drifts | Use `/update-calendar` skill |
| Push without merging to main | PM can't pull the publish package | Always merge to main before telling PM to run |

## Quality Checklist

After publishing:
- [ ] Blog post accessible at `https://pipermorgan.ai/blog/{slug}`
- [ ] Featured image loads correctly
- [ ] Blog index shows post with thumbnail
- [ ] Blog index links to local `/blog/{slug}` (not Medium URL)
- [ ] Editorial calendar updated (this repo) via `/update-calendar`
- [ ] Website repo committed and pushed
- [ ] Deploy workflow completed (GitHub Pages)
- [ ] After syndication: Medium and LinkedIn URLs added to calendar

---

*v0.3 — Updated with lessons from first two blog-canonical publishes (Mar 28-29, 2026). Key changes: relative paths in scripts, 13-column website CSV, remote execution mode, `/update-calendar` integration, known issues documented, image discovery patterns.*
