# Blog-First Publish Checklist

*Reference card for publishing to pipermorgan.ai → Medium → LinkedIn*

---

## Before You Start

- [ ] Draft edited and pushed to `docs/public/comms/drafts/`
- [ ] Dateline added (e.g., `*March 12 to 13, 2026*`)
- [ ] Footer has next-post teaser and reader question
- [ ] Image created (ChatGPT cartoon)

## Image Prep

- [ ] Save image to `dev/active/` as `{descriptive-name}.png`
- [ ] Compress: `sips -Z 1200 {name}.png --out {name}-compressed.png`
- [ ] Note alt text and caption

## Tell Docs Agent

Provide:
1. "Ready to publish [title]"
2. Alt text for image
3. Caption for image
4. Next post title (for footer teaser — Docs can look this up)

Docs agent will: generate HTML, create publish script, update editorial calendar.

## Run Publish Script

```bash
git pull origin main
bash dev/active/publish-package/publish-{slug}.sh
```

## Verify

- [ ] `https://pipermorgan.ai/blog/{slug}` loads with content
- [ ] Image displays
- [ ] Blog index shows the post with image thumbnail

## Syndicate

- [ ] **Medium**: Paste content, publish, set canonical URL to `https://pipermorgan.ai/blog/{slug}`
- [ ] **LinkedIn**: Cross-post (adjust title if needed)
- [ ] Give Docs agent the Medium and LinkedIn URLs

## Done!

Docs agent updates the editorial calendar. You're finished.

---

*v1.0 — Mar 29, 2026. Refine after each publish.*
