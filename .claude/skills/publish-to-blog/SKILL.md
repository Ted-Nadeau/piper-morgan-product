---
name: publish-to-blog
description: Publish a finished blog post from this repo to the pipermorgan.ai website
  repo. Use when PM says "publish this post", "push to the blog", or when a draft
  is marked ready in the editorial calendar. Bridges piper-morgan → piper-morgan-website.
scope: role-specific
version: 0.4
created: 2026-03-16
updated: 2026-03-30
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

## Mode Detection

Check if the website repo is accessible:
```bash
ls ../piper-morgan-website/data/blog-metadata.csv 2>/dev/null
```

- **Direct mode** (file exists): Write directly to the website repo. This is the default on local machines where both repos are checked out.
- **Remote mode** (file not found): Generate a publish package for PM to run locally. See "Remote Execution Mode" below.

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

### Step 4: Prepare Image

1. Find image in `dev/active/` (try multiple filename patterns)
2. Resize: `sips -Z 1200 "{image}"` (keeps aspect ratio, max 1200px)
3. Convert to webp: `cwebp -q 80 "{image}" -o "{slug}.webp"` (install via `brew install webp`)
4. Copy to website repo: `cp {slug}.webp ../piper-morgan-website/public/assets/blog-images/`

### Step 5: Update Website Repo (Direct Mode)

**5a. Add to blog-metadata.csv** (13 columns, this exact order):
```
slug,hashId,title,chatDate,imageSlug,imageAlt,imageCaption,workDate,pubDate,category,cluster,featured,notes
```
Use Python csv writer (never `echo >>`).

**5b. Add blog content** to `src/data/blog-content.json`:
```python
import json
content = json.load(open('../piper-morgan-website/src/data/blog-content.json'))
content[hashId] = {
    "title": title,
    "subtitle": "",
    "content": html_content
}
json.dump(content, open('../piper-morgan-website/src/data/blog-content.json', 'w'), indent=2)
```

**5c. Run sync and fetch**:
```bash
cd ../piper-morgan-website
node scripts/sync-csv-to-json.js
node scripts/fetch-blog-posts.js
```

**5d. Verify** the post appears in `src/data/medium-posts.json` with local URL `/blog/{slug}`.

**5e. Commit and push** the website repo:
```bash
cd ../piper-morgan-website
git add data/blog-metadata.csv src/data/blog-content.json src/data/medium-posts.json public/assets/blog-images/{imageSlug}
git commit -m "Add blog post: {title}"
git push origin main
```

### Step 6: Update Editorial Calendar (This Repo)

Use the `/update-calendar` skill or manually update `docs/internal/planning/comms/editorial-calendar.csv`:
- status → `published`
- pubDate → today
- canonicalSite → `distributed`
- blogURL → `https://pipermorgan.ai/blog/{slug}`
- blogPath → `/blog/{slug}`
- altText → from PM
- caption → from PM

### Step 7: Commit This Repo

```bash
git add dev/active/publish-package/ docs/internal/planning/comms/editorial-calendar.csv docs/public/comms/drafts/
git commit -m "docs: publish {title} to blog + CSV update"
```

### Step 8: Verify Deployment

After GitHub Pages deploys (usually 2-3 minutes after push):
- `https://pipermorgan.ai/blog/{slug}` loads with content and image
- Blog index shows the post with thumbnail
- Blog index links to `/blog/{slug}` (not Medium URL)

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
   - `publish-{slug}.sh` — self-contained script (see v0.3 for script template)
2. Merge to main so PM can pull
3. PM runs the script locally
4. PM reports back with verification + syndication URLs

**CRITICAL — Path Rules for scripts:**
- Use **relative paths from the script's working directory** (`$PWD`)
- NEVER hardcode `../piper-morgan-product/` — the local directory name varies
- Reference the website repo as `../piper-morgan-website`

## Website CSV Format (13 columns)

```
slug,hashId,title,chatDate,imageSlug,imageAlt,imageCaption,workDate,pubDate,category,cluster,featured,notes
```

**Do NOT confuse with our editorial calendar format (18 columns).** The website CSV and our editorial calendar have different schemas.

## Known Issues (as of v0.4)

1. **Blog-first dedup** (FIXED v0.4): `fetch-blog-posts.js` now detects syndicated duplicates of blog-first posts by slug matching and removes them. No longer overwrites blog-first URLs.
2. **Image discovery**: PM saves images with varying names in `dev/active/`. Try multiple filename patterns.
3. **Large file hook**: Images over 500KB may be rejected by pre-commit. Always compress with `sips -Z 1200` before committing.

## Anti-Patterns to Avoid

| Don't Do This | Why | Do This Instead |
|---------------|-----|-----------------|
| Publish to Medium first | Blog should be canonical | Blog first, then syndicate |
| Generate random hashId for Medium posts | Won't match RSS data | Extract real hashId from Medium URL |
| Use `echo >>` to append CSV rows | May corrupt CSV | Use Python csv writer |
| Use `sips` for webp conversion | macOS sips can't write webp | Use `cwebp` (brew install webp) |
| Assume wrong CSV column order | imageAlt/imageCaption are columns 6-7 | Always check actual header |
| Skip the editorial calendar update | Source of truth drifts | Use `/update-calendar` skill |

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

*v0.4 — Direct mode added (both repos local). Blog-first dedup fix in fetch-blog-posts.js (no longer a known issue). CSV column order corrected (imageAlt/imageCaption at positions 6-7, notes not extra). Remote execution mode preserved as fallback. Steps 4-7 collapsed in direct mode.*
