---
name: publish-to-blog
description: Publish a finished blog post from this repo to the pipermorgan.ai website
  repo. Use when PM says "publish this post", "push to the blog", or when a draft
  is marked ready in the editorial calendar. Bridges piper-morgan → piper-morgan-website.
scope: role-specific
version: 0.2
created: 2026-03-16
updated: 2026-03-17
---

# publish-to-blog

Publish a finished markdown blog post to the pipermorgan.ai website repository.

## When to Use

Use this skill when:
- PM says a draft is ready to publish to the blog
- A piece in the editorial calendar has status `ready`
- PM asks to "push to the blog" or "publish this post"

## Prerequisites

- The website repo must be cloned at `../piper-morgan-website` (relative to this repo root)
- The draft markdown file must exist in this repo (typically `docs/public/comms/drafts/`)
- The cartoon/featured image must be available (either in this repo or the website's `public/assets/blog-images/`)
- **Image conversion**: `cwebp` must be installed for PNG→webp conversion. macOS `sips` cannot output webp format. Install via `brew install webp` if needed.

## Procedure

### Step 1: Identify the Post

Confirm with PM:
1. Which draft file? (path in this repo)
2. Title (may differ from draft filename)
3. Category: `building` or `insight`
4. Cartoon/image slug (e.g., `robot-assembly`)
5. Any final title changes?

### Step 2: Pre-Flight Check — Is This Post Already on Medium?

**This step prevents hashId mismatches.** Most of our backlog was published to Medium first. If the post exists on Medium, we must use its real hashId.

```bash
cd ../piper-morgan-website

# Search for the post title in medium-posts.json
python3 -c "
import json
posts = json.load(open('src/data/medium-posts.json'))
matches = [p for p in posts if 'SEARCH_TERM' in p.get('title','').lower()]
for p in matches:
    print(f\"Title: {p['title']}\")
    print(f\"URL: {p.get('url','')}\")
    print(f\"HashId: {p['url'].split('/')[-1].split('?')[0].split('-')[-1] if 'medium.com' in p.get('url','') else 'N/A'}\")
"
```

**If found on Medium**: Extract the hashId from the Medium URL (the last segment after the final hyphen, e.g., `168e71571f6b` from `four-voices-one-spec-168e71571f6b`). Use this as the hashId in all subsequent steps.

**If NOT found on Medium**: Generate a unique hashId:
```bash
python3 -c "import uuid; print(uuid.uuid4().hex[:12])"
```

### Step 3: Verify the Website Repo

```bash
cd ../piper-morgan-website
git stash  # if needed
git checkout main
git pull origin main
```

### Step 4: Prepare the Image

If the image isn't already in the website repo:

```bash
# Convert to webp using cwebp (NOT sips — sips can't write webp)
cwebp /path/to/image.png -o ../piper-morgan-website/public/assets/blog-images/{slug}.webp

# If cwebp is not installed:
brew install webp

# Fallback: use PNG directly (less optimal but works)
cp /path/to/image.png ../piper-morgan-website/public/assets/blog-images/{slug}.png
```

### Step 5: Add to blog-metadata.csv

The website's source of truth is `data/blog-metadata.csv`. Add a row.

**IMPORTANT**: Do NOT use `echo >>` to append — it may not add a newline before the new row, causing CSV corruption. Instead, use Python or verify the file ends with a newline first:

```bash
cd ../piper-morgan-website

# Safe append: ensure newline before adding
python3 -c "
import csv, os
filepath = 'data/blog-metadata.csv'
# Read to check if file ends with newline
with open(filepath, 'rb') as f:
    f.seek(-1, 2)
    if f.read(1) != b'\n':
        with open(filepath, 'a') as fa:
            fa.write('\n')
# Now append the row
with open(filepath, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['{slug}', '{hashId}', '{title}', '{chatDate}', '{imageSlug}.webp', '{workDate}', '{pubDate}', '{category}', '', '', ''])
"
```

Fields:
- `slug`: URL-safe title (lowercase, hyphens, no special chars)
- `hashId`: From Step 2 (real Medium hashId if exists, otherwise generated)
- `title`: Display title
- `chatDate`: Date of the source chat session (M/D/YYYY)
- `imageSlug`: Filename of the featured image in blog-images/
- `workDate`: When the piece was written (YYYY-MM-DD)
- `pubDate`: Today's date (YYYY-MM-DD) — the canonical publication date
- `category`: `building` or `insight`
- `cluster`: Episode/cluster name if applicable (can be empty)
- `featured`: `true` if this should be featured, otherwise empty

### Step 6: Add Blog Content

Convert the markdown draft to HTML and add to `src/data/blog-content.json`:

```bash
cd ../piper-morgan-website

# Convert markdown to HTML and add to blog-content.json
python3 << 'PYEOF'
import json, re

# Read the markdown draft
with open('/path/to/draft.md') as f:
    md = f.read()

# Basic markdown → HTML conversion
# (Handles headers, paragraphs, bold, italic, lists, blockquotes, code blocks)
lines = md.split('\n')
html_parts = []
in_code_block = False
in_list = False

for line in lines:
    stripped = line.strip()
    if stripped.startswith('```'):
        in_code_block = not in_code_block
        html_parts.append('<pre><code>' if in_code_block else '</code></pre>')
        continue
    if in_code_block:
        html_parts.append(line)
        continue
    if not stripped:
        if in_list:
            html_parts.append('</ul>')
            in_list = False
        continue
    # Headers
    if stripped.startswith('# '):
        html_parts.append(f'<h1>{stripped[2:]}</h1>')
    elif stripped.startswith('## '):
        html_parts.append(f'<h2>{stripped[3:]}</h2>')
    elif stripped.startswith('### '):
        html_parts.append(f'<h3>{stripped[4:]}</h3>')
    elif stripped.startswith('> '):
        html_parts.append(f'<blockquote><p>{stripped[2:]}</p></blockquote>')
    elif stripped.startswith('- ') or stripped.startswith('* '):
        if not in_list:
            html_parts.append('<ul>')
            in_list = True
        html_parts.append(f'<li>{stripped[2:]}</li>')
    else:
        # Inline formatting
        text = stripped
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        html_parts.append(f'<p>{text}</p>')

if in_list:
    html_parts.append('</ul>')

html = '\n\n'.join(html_parts)

# Add to blog-content.json
with open('src/data/blog-content.json') as f:
    content = json.load(f)

content['{hashId}'] = {'content': html}

with open('src/data/blog-content.json', 'w') as f:
    json.dump(content, f, indent=2)

print('Done — added content for {hashId}')
PYEOF
```

Then run the sync script:
```bash
node scripts/sync-csv-to-json.js
```

### Step 7: Run fetch-blog-posts.js

This merges RSS (Medium posts) with CSV metadata and blog-first posts:

```bash
node scripts/fetch-blog-posts.js
```

Verify the post appears correctly in `src/data/medium-posts.json`:
```bash
python3 -c "
import json
posts = json.load(open('src/data/medium-posts.json'))
match = [p for p in posts if '{slug}' in p.get('slug','') or '{slug}' in p.get('url','')]
for p in match:
    print(f\"Title: {p['title']}\")
    print(f\"URL: {p['url']}\")
    print(f\"Slug: {p.get('slug','')}\")
"
```

**Expected**: URL should be `/blog/{slug}` (local), not a Medium URL.

### Step 8: Update Editorial Calendar (This Repo)

Back in piper-morgan, update `docs/internal/planning/comms/editorial-calendar.csv`:
- Set `status` to `published`
- Set `pubDate` to today
- Set `canonicalSite` to `distributed`
- Set `blogPath` to the slug (e.g., `/blog/{slug}`)
- Set `blogURL` to `https://pipermorgan.ai/blog/{slug}`

### Step 9: Commit Both Repos

```bash
# Website repo
cd ../piper-morgan-website
git add data/blog-metadata.csv src/data/medium-posts.json src/data/blog-content.json public/assets/blog-images/
git commit -m "Add blog post: {title}"
git push origin main

# This repo
cd ../piper-morgan
git add docs/internal/planning/comms/editorial-calendar.csv
git commit -m "editorial calendar: mark {title} as published"
```

### Step 10: Verify Deployment

```bash
# Watch the deploy workflow
cd ../piper-morgan-website
gh run list --limit 3

# Wait for both workflows to complete:
# 1. "Deploy Piper Morgan Website to GitHub Pages" (builds the site)
# 2. "pages build and deployment" (publishes to GitHub Pages)
gh run watch {run-id}
```

Then verify: `https://pipermorgan.ai/blog/{slug}` loads with correct content and image.

### Step 11: Syndicate (After Blog is Live)

Once the blog post is live on pipermorgan.ai:
1. **Medium**: Copy content to Medium, publish, add Medium URL to editorial calendar
2. **LinkedIn**: Cross-post if relevant, add LinkedIn URL to editorial calendar

## Anti-Patterns to Avoid

| Don't Do This | Why | Do This Instead |
|---------------|-----|-----------------|
| Publish to Medium first | Blog should be canonical | Blog first, then syndicate |
| Skip the pre-flight Medium check | HashId mismatch breaks slug mapping | Always check if post exists on Medium first |
| Use `echo >>` to append CSV rows | May not add newline, corrupts CSV | Use Python csv writer with newline check |
| Generate random hashId for Medium posts | Won't match RSS data, slug won't apply | Extract real hashId from Medium URL |
| Use `sips` for webp conversion | macOS sips can't write webp format | Use `cwebp` (install via `brew install webp`) |
| Skip the editorial calendar update | Source of truth drifts | Always update CSV in both repos |
| Commit to website without pulling first | Merge conflicts | Always pull before adding |
| Forget the image | Broken post on site | Verify image exists before committing |
| Push without verifying deploy | May not know about build failures | Watch the GitHub Actions workflow |

## Quality Checklist

After publishing:
- [ ] Blog post accessible at `https://pipermorgan.ai/blog/{slug}`
- [ ] Featured image loads correctly
- [ ] Blog index links to local post (not Medium URL)
- [ ] Editorial calendar updated with blogURL and status=published
- [ ] Website repo committed and pushed
- [ ] This repo's editorial calendar committed
- [ ] Deploy workflow completed successfully (both build + pages)

## Future Improvements

- [ ] Automate hashId lookup from Medium URL in medium-posts.json
- [ ] Script to sync editorial-calendar.csv ↔ blog-metadata.csv
- [ ] Lightweight CMS UI for editing/publishing from browser
- [ ] Webhook or CI trigger for deploy after commit
- [ ] Better markdown → HTML conversion (install `markdown` Python package or use pandoc)

---

*v0.2 — Updated with lessons from first real use (Mar 17, 2026). Key fixes: pre-flight Medium check, safe CSV append, cwebp dependency, deployment verification.*
