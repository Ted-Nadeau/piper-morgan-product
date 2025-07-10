# Logo Fix Instructions for Web UI

## Task: Add Logo Support to web/app.py

### VERIFY FIRST:
```bash
ls web/assets/pm-logo.png
# Confirm logo file exists in correct location
```

### OBJECTIVE:
Add static file serving to the web UI and display the Piper Morgan logo

### IMPLEMENTATION:

1. **Add imports at the top of web/app.py**:
```python
from fastapi.staticfiles import StaticFiles
```

2. **Mount static files directory** (add after `app = FastAPI(...)` line):
```python
# Mount static files
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
```

3. **Update HTML template** - Replace the emoji header:
```html
<!-- FIND THIS: -->
<h1>🤖 Piper Morgan</h1>

<!-- REPLACE WITH: -->
<h1><img src="/assets/pm-logo.png" alt="Piper Morgan" style="height: 60px; vertical-align: middle;"> Piper Morgan</h1>
```

### DO NOT:
- Change the API_BASE_URL configuration
- Modify any JavaScript functionality
- Create new directories
- Change file paths without verifying they exist

### VERIFY AFTER:
1. Restart the web UI server
2. Check browser console for 404 errors on logo
3. Confirm logo displays properly

### EXPECTED RESULT:
The Piper Morgan logo should appear in the header instead of the robot emoji

### PRO TIPS:
- The assets directory should be relative to where app.py is located
- If logo doesn't show, check browser DevTools Network tab for 404s
- FastAPI needs StaticFiles middleware to serve images
