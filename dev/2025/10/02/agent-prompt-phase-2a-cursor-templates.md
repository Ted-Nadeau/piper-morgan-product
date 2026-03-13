# Cursor Agent Prompt: GREAT-3A Phase 2A - Template Extraction

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase 2A work.

## Mission
**Extract Templates**: Move 464 lines of embedded HTML from web/app.py routes into proper Jinja2 template files.

## Context

**Phase 1 Complete**: 100% config pattern compliance achieved
**Phase 2 Goal**: Refactor web/app.py (1,052 lines) for plugin architecture
**Phase 2A**: First step - extract templates (simple, low-risk wins)

**Current State**: Two routes have embedded HTML:
- `/` home page: 332 lines of HTML embedded in route
- `/standup` UI: 132 lines of HTML embedded in route

**Target State**: Templates in `templates/` directory, routes use Jinja2

## Your Tasks

### Task 1: Analyze Current HTML Embedding

```bash
cd ~/Development/piper-morgan

# Find the home route
grep -A 350 '@app.get("/"' web/app.py | head -360

# Find the standup route
grep -A 150 '@app.get("/standup"' web/app.py | head -160

# Check if templates/ directory exists
ls -la templates/ 2>/dev/null || echo "templates/ doesn't exist yet"
```

**Document**:
- Where does HTML start/end in each route?
- Are there any dynamic values being injected?
- Is Jinja2Templates already imported?

### Task 2: Create Templates Directory Structure

```bash
# Create directory
mkdir -p templates

# Verify
ls -la templates/
```

**Structure**:
```
templates/
├── home.html       # Home page template
└── standup.html    # Standup UI template
```

### Task 3: Extract Home Page Template

**Source**: Find HTML in `/` route (should be ~332 lines)

**Target**: `templates/home.html`

**Extraction Steps**:
1. Copy HTML from route (everything inside the string)
2. Create `templates/home.html`
3. Paste HTML
4. Look for any dynamic content ({{variables}})
5. Clean up any Python string formatting

**Example Pattern**:
```python
# BEFORE (in route)
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Piper Morgan</title>
    ...
</head>
<body>
    ...
</body>
</html>
"""
return HTMLResponse(html)
```

**AFTER (in template file)**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Piper Morgan</title>
    ...
</head>
<body>
    ...
</body>
</html>
```

### Task 4: Extract Standup Template

**Source**: Find HTML in `/standup` route (should be ~132 lines)

**Target**: `templates/standup.html`

Same extraction process as home page.

### Task 5: Update web/app.py Imports

**Add Jinja2 support**:
```python
from fastapi import FastAPI, Request  # Add Request if not present
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse  # Keep for other uses

# After app = FastAPI(...)
templates = Jinja2Templates(directory="templates")
```

### Task 6: Update Home Route

**Current Pattern**:
```python
@app.get("/")
async def home():
    html = """
    ... 332 lines ...
    """
    return HTMLResponse(html)
```

**New Pattern**:
```python
@app.get("/")
async def home(request: Request):
    """Render home page"""
    return templates.TemplateResponse("home.html", {"request": request})
```

**Changes**:
1. Add `request: Request` parameter (required by Jinja2Templates)
2. Replace HTML string with template rendering
3. Pass `request` in context dict
4. Keep route name and decorator

### Task 7: Update Standup Route

**Same pattern as home route**:
```python
@app.get("/standup")
async def standup_ui(request: Request):
    """Render standup UI"""
    return templates.TemplateResponse("standup.html", {"request": request})
```

### Task 8: Test Templates Work

```bash
# Test 1: Check imports work
python -c "from fastapi.templating import Jinja2Templates; print('Imports OK')"

# Test 2: Verify template files exist
ls -la templates/home.html templates/standup.html

# Test 3: Check template can be loaded
python -c "from fastapi.templating import Jinja2Templates; t = Jinja2Templates(directory='templates'); print('Templates loaded')"

# Test 4: Start server and check routes (manual test)
# uvicorn web.app:app --reload --port 8001
# Visit http://localhost:8001/ and http://localhost:8001/standup
```

### Task 9: Verify Line Count Reduction

```bash
# Count lines before
wc -l web/app.py

# Expected reduction: ~464 lines (332 + 132)
# Should go from ~1,052 to ~588 lines
```

### Task 10: Check for Dynamic Content

**Important**: Look for any Python variables that were being formatted into the HTML:

```python
# Example pattern to look for:
html = f"""
<div>User: {user_name}</div>
"""
```

**If found**: Convert to Jinja2 template variables:
```html
<!-- In template -->
<div>User: {{ user_name }}</div>
```

**And update route**:
```python
return templates.TemplateResponse("home.html", {
    "request": request,
    "user_name": user_name
})
```

## Deliverable

Create: `dev/2025/10/02/phase-2a-cursor-template-extraction.md`

Include:
1. **Current State Analysis**: Where HTML was embedded
2. **Templates Created**: home.html and standup.html
3. **Routes Updated**: Changes to both routes with diffs
4. **Line Count Reduction**: Before/after metrics
5. **Dynamic Content**: Any variables that needed conversion
6. **Test Results**: Verification templates render correctly

## Critical Requirements

- **DO extract** all HTML to template files
- **DO use** Jinja2Templates (FastAPI standard)
- **DO preserve** all functionality (pages look identical)
- **DO reduce** route functions to ~10-20 lines each
- **DON'T change** any HTML structure or content
- **DON'T break** any existing features

## Time Estimate
30 minutes

## Success Criteria
- [ ] templates/ directory created
- [ ] home.html template created (~332 lines)
- [ ] standup.html template created (~132 lines)
- [ ] Home route reduced to ~15 lines
- [ ] Standup route reduced to ~15 lines
- [ ] Both pages render correctly
- [ ] web/app.py reduced by ~464 lines
- [ ] No functionality changes

---

**Deploy at 4:58 PM**
**First phase of web/app.py refactoring**
