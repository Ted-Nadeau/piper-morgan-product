# Static Files Directory

⚠️ **IMPORTANT: This directory is NOT served by the web application.**

## Correct Location for Web Static Files

All web application static files (CSS, JavaScript, images) must be placed in:

```
web/static/
```

FastAPI is configured to serve static files from `web/static/`, not the project root `static/` directory.

## Why This Directory Exists

This root `static/` directory may be used for:
- Non-web static assets (documentation images, etc.)
- Build artifacts that aren't served directly
- Other non-HTTP-served resources

## Common Mistake

❌ **WRONG:** Creating files in `static/css/` or `static/js/`
✅ **CORRECT:** Creating files in `web/static/css/` or `web/static/js/`

## How to Verify

Check `web/app.py` for the static files mount point:

```python
app.mount("/static", StaticFiles(directory="web/static"), name="static")
```

This configuration shows that `/static` URL paths are served from `web/static/` directory.

## Reference

- See Issue #396, Bug #6: Static file path mismatch during Michelle's onboarding
- Fixed on 2025-11-24: Moved auth.css and auth.js from root static/ to web/static/
