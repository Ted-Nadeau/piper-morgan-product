# Version Tracking Investigation - 2025-11-24

## Current State

### ✅ What Exists
1. **pyproject.toml:7** - `version = "0.8.0-alpha"`
   - **Problem**: Out of date (production is v0.8.1)
   - **Location**: Single source of truth candidate
   - **Format**: Standard Python package versioning

2. **No Version API Endpoint**
   - Searched for version routes in FastAPI - none found
   - No `/api/v1/version` or `/version` endpoint

3. **No __version__ Variable**
   - Checked services/__init__.py - no version export
   - No standard Python `__version__` pattern

### ❌ What's Missing
1. **Synchronized version tracking** across:
   - pyproject.toml (currently: 0.8.0-alpha)
   - Production deployment (currently: v0.8.1)
   - Git tags (unknown status)

2. **Version API endpoint** for runtime introspection

3. **Automated version bumping** process

## Your Version Scheme

From conversation context:
- **Alpha releases**: 0.8.x.y series
  - Major updates: 0.8.2, 0.8.3, etc.
  - Minor updates: 0.8.1.1, 0.8.1.2, etc.
- **Beta releases**: 0.9.x series
- **MVP**: 1.0.0

**Current versions**:
- Production: v0.8.1 (deployed Nov 23)
- Main branch: 0.8.0-alpha (pyproject.toml - OUT OF DATE)
- Next deploy: v0.8.1.1 or v0.8.2 (with today's fixes)

## Recommendations

### Option 1: Minimal - Update pyproject.toml Only ⭐ RECOMMENDED
**What**: Keep pyproject.toml as single source, manually update

**Implementation**:
```toml
# pyproject.toml line 7
version = "0.8.1"  # Update to match production
```

**Pros**:
- Simple, no code changes
- Standard Python practice
- Works with pip/setuptools

**Cons**:
- Manual updates (error-prone)
- No runtime visibility
- No validation between code and deployment

**When to update**: Before each production deployment

---

### Option 2: Single Source + API Endpoint ⭐⭐ BEST PRACTICE
**What**: Read from pyproject.toml, expose via API

**Implementation**:

1. **Create version module** (`services/version.py`):
```python
"""Application version management"""
import tomli
from pathlib import Path

def get_version() -> str:
    """Read version from pyproject.toml"""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject = tomli.load(f)
    return pyproject["project"]["version"]

__version__ = get_version()
```

2. **Add API endpoint** (`web/app.py`):
```python
@app.get("/api/v1/version")
async def get_version():
    """Get application version"""
    from services.version import __version__
    return {
        "version": __version__,
        "environment": settings.ENVIRONMENT,
        "deployed_at": "2025-11-23"  # Could read from deployment metadata
    }
```

3. **Update pyproject.toml**:
```toml
version = "0.8.1"
```

**Pros**:
- Single source of truth (pyproject.toml)
- Runtime introspection via API
- Standard Python versioning
- No duplication

**Cons**:
- Requires tomli dependency (already have it?)
- Still manual version updates

**When to update**: Update pyproject.toml before deployment, API auto-syncs

---

### Option 3: Automated with Git Tags (Advanced)
**What**: Version derived from git tags, automated bumping

**Implementation**: Use tools like:
- `setuptools_scm` - Derives version from git tags
- `bump2version` - Automated version bumping

**Pros**:
- Fully automated
- Git tags = versions
- No manual updates

**Cons**:
- More complex setup
- Requires git tag discipline
- May be overkill for alpha

**Recommendation**: Defer until beta/MVP

---

## My Recommendation: Option 2

**Why**:
1. **Single source of truth** - pyproject.toml (your preference)
2. **Runtime visibility** - API endpoint for debugging
3. **Minimal complexity** - Simple Python code
4. **Standard practice** - Follows Python packaging conventions
5. **Future-proof** - Easy to add automation later

**Implementation effort**: 15-20 minutes

**What to do right now**:
1. Update pyproject.toml to `version = "0.8.1"` (matches production)
2. Consider adding version API endpoint before next deploy

## Version Update Workflow (Option 2)

### Before deploying to production:

```bash
# 1. Update version in pyproject.toml
# Edit line 7: version = "0.8.1.1"  (or 0.8.2 for major)

# 2. Commit version bump
git add pyproject.toml
git commit -m "chore: Bump version to 0.8.1.1"

# 3. Tag the release (optional but recommended)
git tag -a v0.8.1.1 -m "Alpha release 0.8.1.1 - LLM API fixes"

# 4. Deploy to production
git push origin main
git push origin v0.8.1.1  # If tagged

# 5. Verify version via API
curl https://production-url/api/v1/version
```

## Immediate Action Needed

**For current main branch**:
- [ ] Update pyproject.toml from `0.8.0-alpha` to `0.8.1`
- [ ] Commit: "chore: Update version to match production (0.8.1)"

**Before next production push**:
- [ ] Decide: v0.8.1.1 (minor fixes) or v0.8.2 (major updates)?
- [ ] Update pyproject.toml accordingly
- [ ] Optionally: Implement version API endpoint

## Questions for PM

1. **Which option** do you prefer? (1, 2, or 3)
2. **Next version number**: Should today's fixes be 0.8.1.1 or 0.8.2?
3. **Version API**: Want the endpoint now or defer?
4. **Git tags**: Should we tag releases? (Recommended for traceability)

## Related Files

- `pyproject.toml:7` - Current version definition
- `web/app.py` - Where to add version endpoint
- Would create: `services/version.py` - Version module

---

**Status**: Investigation complete, awaiting PM decision on approach
