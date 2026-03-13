# CORE-LEARN-F Implementation: Integration & Polish (SPRINT A5 FINALE!)

**Agent**: Claude Code (Programmer)
**Issue**: #226 CORE-LEARN-F - Integration & Polish
**Sprint**: A5 - Learning System (Extended - Issue 6 of 6 - FINAL!)
**Date**: October 20, 2025, 5:10 PM
**Duration**: 4.5 hours estimated (based on discovery)

---

## 🎊 SPRINT A5 FINALE - THE FINAL PUSH!

**Context**: This is the FINAL issue of Sprint A5! We're SO CLOSE!

Discovery found that CORE-LEARN-F infrastructure is **90% complete** (~7,500 lines exist).

**What exists (the incredible foundation)**:
- ✅ Intent System (185KB + 12 files) - COMPLETE integration!
- ✅ Plugin Architecture (58KB, 6 files) - COMPLETE system!
- ✅ Learning API (511 lines) - Complete foundation!
- ✅ Analytics API - Complete metrics collection!
- ✅ Documentation (27KB) - ALL requirements met!
- ✅ Performance optimization - Cache layer complete!

**What's needed (today's work - ~850 lines)**:
- ⚠️ User control endpoints (4 endpoints, ~150 lines)
- ⚠️ Privacy control settings (~100 lines)
- ⚠️ Dashboard UI components (~300 lines)
- ⚠️ Integration wiring (~100 lines)
- ⚠️ Tests (~200 lines)

**This is POLISH, not building!** ✨

---

## 🎯 STAY GROUNDED REMINDER

**Yes, we should be excited**:
- 6/6 discoveries perfect ✅
- 5/5 implementations complete ✅
- 91% average leverage ✅
- ONE DAY progress ✅

**But we must finish strong**:
- 4.5 hours of quality work remaining
- User controls are important
- Dashboard needs polish
- Testing must be thorough
- Can't cut corners on the finale!

**Celebrate progress, finish strong!** 🎯

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## Mission

**Complete the Learning System with polish and user controls!**

Discovery found 90% complete (~7,500 lines). **We need ~850 lines of work**:
- User control endpoints (~150 lines)
- Privacy settings (~100 lines)
- Dashboard UI components (~300 lines)
- Integration wiring (~100 lines)
- Tests (~200 lines)

**Order matters**: User controls first (most important!), then dashboard!

**NOT in scope**:
- Machine learning (use existing!)
- Complex analytics (use existing API!)
- Extensive documentation (already complete!)

---

## Discovery Report

**YOU HAVE**: `core-learn-f-discovery-report.md` uploaded by PM

**CRITICAL FINDINGS**:
- 90% infrastructure exists (~7,500 lines)
- Intent System: 185KB + 12 files (COMPLETE!)
- Plugin Architecture: 58KB (COMPLETE!)
- Learning API: 511 lines (foundation ready!)
- Analytics API: Complete metrics collection
- Documentation: 27KB (ALL requirements met!)
- Need ~850 lines: 4 endpoints + privacy + dashboard + tests

**Read the discovery report first!** It contains complete assessment.

---

## STOP Conditions

If ANY of these occur, STOP and escalate to PM immediately:

1. **Learning API doesn't exist** - Discovery said 511 lines
2. **Analytics endpoint doesn't work** - Discovery said complete
3. **Intent system doesn't exist** - Discovery said 185KB + 12 files
4. **Plugin architecture doesn't exist** - Discovery said 58KB
5. **Cannot provide verification evidence** - Must show endpoints work
6. **Tests don't pass** - Must maintain zero regressions
7. **More than 1,000 lines needed** - Discovery said ~850 lines
8. **Tempted to skip user controls** - STOP! Controls are important!

---

## Evidence Requirements

### For EVERY Claim You Make:

- **"User controls added"** → Show endpoint responses + tests
- **"Dashboard UI works"** → Show UI rendering + data flow
- **"Privacy settings work"** → Show settings + enforcement
- **"Tests pass"** → Show test output
- **"Zero regressions"** → Show all existing tests passing

### Working Files Location:

- ✅ web/api/routes/learning.py - For user control endpoints
- ✅ web/ui/ - For dashboard UI components
- ✅ services/domain/user_preference_manager.py - For privacy settings
- ✅ tests/integration/ - Integration tests
- ✅ dev/active/ - For test scripts, verification

---

## Implementation Plan (from Discovery)

### Phase 1: User Controls (2 hours - DO THIS FIRST!)

**CRITICAL**: User controls are the most important feature!

**Step 1: Add User Control Endpoints to Learning API** (2 hours)

Update `web/api/routes/learning.py` with 4 new endpoints:

#### 1. Enable/Disable Learning (30 min)

```python
@router.post("/controls/learning/enable")
async def enable_learning(
    user_id: str,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Enable learning for a user.

    Allows the learning system to collect patterns and preferences
    for this user.
    """
    preference_manager = UserPreferenceManager(session)

    await preference_manager.set_preference(
        key="learning_enabled",
        value=True,
        user_id=user_id
    )

    return {
        "status": "success",
        "learning_enabled": True,
        "user_id": user_id
    }


@router.post("/controls/learning/disable")
async def disable_learning(
    user_id: str,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Disable learning for a user.

    Stops the learning system from collecting new patterns
    and preferences. Existing data is preserved.
    """
    preference_manager = UserPreferenceManager(session)

    await preference_manager.set_preference(
        key="learning_enabled",
        value=False,
        user_id=user_id
    )

    return {
        "status": "success",
        "learning_enabled": False,
        "user_id": user_id,
        "note": "Existing learned data preserved"
    }


@router.get("/controls/learning/status")
async def get_learning_status(
    user_id: str,
    session: AsyncSession = Depends(get_db_session)
):
    """Get current learning status for a user."""
    preference_manager = UserPreferenceManager(session)

    enabled = await preference_manager.get_preference(
        key="learning_enabled",
        user_id=user_id
    )

    # Default to enabled if not set
    if enabled is None:
        enabled = True

    return {
        "user_id": user_id,
        "learning_enabled": enabled
    }
```

---

#### 2. Clear Learned Data (30 min)

```python
@router.delete("/controls/data/clear")
async def clear_learned_data(
    user_id: str,
    data_type: str = "all",  # "all", "patterns", "preferences", "automation"
    session: AsyncSession = Depends(get_db_session)
):
    """
    Clear learned data for a user.

    Args:
        user_id: User ID
        data_type: Type of data to clear (all, patterns, preferences, automation)

    Returns:
        Confirmation of data cleared
    """
    from services.learning.query_learning_loop import QueryLearningLoop
    from services.domain.user_preference_manager import UserPreferenceManager
    from services.automation.audit_trail import get_audit_trail

    results = {}

    if data_type in ["all", "patterns"]:
        # Clear learned patterns
        learning_loop = QueryLearningLoop(session)
        # Implementation: Clear patterns for user
        # This would require a method in QueryLearningLoop
        results["patterns_cleared"] = True

    if data_type in ["all", "preferences"]:
        # Clear user preferences
        preference_manager = UserPreferenceManager(session)
        # Implementation: Clear preferences for user
        # This would require a method in UserPreferenceManager
        results["preferences_cleared"] = True

    if data_type in ["all", "automation"]:
        # Clear automation audit trail for user
        audit_trail = get_audit_trail()
        # Implementation: Clear audit events for user
        results["automation_cleared"] = True

    return {
        "status": "success",
        "user_id": user_id,
        "data_type": data_type,
        "results": results,
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

#### 3. Export Preferences (30 min)

```python
@router.get("/controls/export")
async def export_preferences(
    user_id: str,
    format: str = "json",  # "json" or "csv"
    session: AsyncSession = Depends(get_db_session)
):
    """
    Export user's learned preferences and patterns.

    Args:
        user_id: User ID
        format: Export format (json or csv)

    Returns:
        Exported data in requested format
    """
    from services.domain.user_preference_manager import UserPreferenceManager
    from services.learning.query_learning_loop import QueryLearningLoop

    preference_manager = UserPreferenceManager(session)
    learning_loop = QueryLearningLoop(session)

    # Gather all user data
    export_data = {
        "user_id": user_id,
        "export_timestamp": datetime.utcnow().isoformat(),
        "preferences": {},
        "patterns": [],
        "automation_settings": {}
    }

    # Get all preferences
    # Implementation: Get all preferences for user
    export_data["preferences"] = await preference_manager.get_all_preferences(user_id)

    # Get learned patterns
    # Implementation: Get patterns for user
    patterns = await learning_loop.get_user_patterns(user_id)
    export_data["patterns"] = [
        {
            "pattern_type": p.pattern_type,
            "confidence": p.confidence,
            "usage_count": p.usage_count,
            "data": p.pattern_data
        }
        for p in patterns
    ]

    if format == "json":
        return export_data
    elif format == "csv":
        # Convert to CSV format
        # Implementation: CSV conversion
        return {
            "status": "success",
            "format": "csv",
            "note": "CSV export not yet implemented, returning JSON"
        }
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")
```

---

#### 4. Privacy Settings (30 min)

```python
@router.post("/controls/privacy/settings")
async def set_privacy_settings(
    user_id: str,
    settings: Dict[str, Any],
    session: AsyncSession = Depends(get_db_session)
):
    """
    Set privacy settings for user.

    Privacy settings:
    - share_patterns: Allow pattern sharing across features
    - share_across_users: Allow anonymized pattern sharing
    - data_retention_days: Days to retain learned data (0 = forever)
    - allow_automation: Allow intelligent automation
    - allow_predictive: Allow predictive assistance
    """
    preference_manager = UserPreferenceManager(session)

    # Validate settings
    valid_keys = {
        "share_patterns",
        "share_across_users",
        "data_retention_days",
        "allow_automation",
        "allow_predictive"
    }

    for key in settings:
        if key not in valid_keys:
            raise HTTPException(status_code=400, detail=f"Invalid setting: {key}")

    # Store privacy settings
    await preference_manager.set_preference(
        key="privacy_settings",
        value=settings,
        user_id=user_id
    )

    return {
        "status": "success",
        "user_id": user_id,
        "privacy_settings": settings
    }


@router.get("/controls/privacy/settings")
async def get_privacy_settings(
    user_id: str,
    session: AsyncSession = Depends(get_db_session)
):
    """Get current privacy settings for user."""
    preference_manager = UserPreferenceManager(session)

    settings = await preference_manager.get_preference(
        key="privacy_settings",
        user_id=user_id
    )

    # Default privacy settings
    if settings is None:
        settings = {
            "share_patterns": True,
            "share_across_users": False,  # Conservative default
            "data_retention_days": 0,  # Keep forever by default
            "allow_automation": True,
            "allow_predictive": True
        }

    return {
        "user_id": user_id,
        "privacy_settings": settings
    }
```

---

### Phase 2: Dashboard UI Components (2 hours)

**Step 1: Create Dashboard UI Components** (2 hours)

Create `web/ui/learning_dashboard.html` (or React component if using React):

```html
<!DOCTYPE html>
<html>
<head>
    <title>Learning System Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }

        .dashboard {
            max-width: 1200px;
            margin: 0 auto;
        }

        .card {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .metric {
            display: inline-block;
            margin-right: 30px;
        }

        .metric-value {
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        }

        .metric-label {
            font-size: 14px;
            color: #7f8c8d;
            margin-top: 5px;
        }

        .chart {
            height: 300px;
            background: #ecf0f1;
            border-radius: 4px;
            margin-top: 20px;
        }

        .controls {
            margin-top: 10px;
        }

        button {
            padding: 10px 20px;
            margin-right: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }

        .btn-primary {
            background: #3498db;
            color: white;
        }

        .btn-danger {
            background: #e74c3c;
            color: white;
        }

        .btn-success {
            background: #2ecc71;
            color: white;
        }

        .status {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }

        .status-enabled {
            background: #d4edda;
            color: #155724;
        }

        .status-disabled {
            background: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>Learning System Dashboard</h1>

        <!-- Learning Status Card -->
        <div class="card">
            <h2>Learning Status</h2>
            <div id="learning-status">
                <span class="status status-enabled">Enabled</span>
            </div>
            <div class="controls">
                <button class="btn-primary" onclick="toggleLearning()">Toggle Learning</button>
                <button class="btn-success" onclick="exportData()">Export Data</button>
                <button class="btn-danger" onclick="clearData()">Clear Data</button>
            </div>
        </div>

        <!-- Metrics Card -->
        <div class="card">
            <h2>Learning Metrics</h2>
            <div id="metrics">
                <div class="metric">
                    <div class="metric-value" id="total-patterns">0</div>
                    <div class="metric-label">Total Patterns</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="success-rate">0%</div>
                    <div class="metric-label">Success Rate</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="avg-confidence">0.0</div>
                    <div class="metric-label">Avg Confidence</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="recent-patterns">0</div>
                    <div class="metric-label">Recent (24h)</div>
                </div>
            </div>
        </div>

        <!-- Pattern Types Card -->
        <div class="card">
            <h2>Pattern Distribution</h2>
            <div class="chart" id="pattern-chart">
                <!-- Chart would be rendered here with a charting library -->
                <p style="text-align: center; padding-top: 130px; color: #7f8c8d;">
                    Pattern type distribution chart
                </p>
            </div>
        </div>

        <!-- Privacy Settings Card -->
        <div class="card">
            <h2>Privacy Settings</h2>
            <div id="privacy-settings">
                <label>
                    <input type="checkbox" id="share-patterns" checked>
                    Share patterns across features
                </label><br>
                <label>
                    <input type="checkbox" id="share-users">
                    Allow anonymized pattern sharing
                </label><br>
                <label>
                    <input type="checkbox" id="allow-automation" checked>
                    Allow intelligent automation
                </label><br>
                <label>
                    <input type="checkbox" id="allow-predictive" checked>
                    Allow predictive assistance
                </label><br><br>
                <button class="btn-primary" onclick="savePrivacySettings()">Save Settings</button>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = '/api/v1/learning';
        const USER_ID = 'current_user';  // Replace with actual user ID

        // Load dashboard data on page load
        window.addEventListener('load', async () => {
            await loadLearningStatus();
            await loadMetrics();
            await loadPrivacySettings();
        });

        async function loadLearningStatus() {
            const response = await fetch(`${API_BASE}/controls/learning/status?user_id=${USER_ID}`);
            const data = await response.json();

            const statusEl = document.getElementById('learning-status');
            if (data.learning_enabled) {
                statusEl.innerHTML = '<span class="status status-enabled">Enabled</span>';
            } else {
                statusEl.innerHTML = '<span class="status status-disabled">Disabled</span>';
            }
        }

        async function loadMetrics() {
            const response = await fetch(`${API_BASE}/analytics`);
            const data = await response.json();

            document.getElementById('total-patterns').textContent = data.total_patterns || 0;
            document.getElementById('success-rate').textContent =
                Math.round((data.success_rate || 0) * 100) + '%';
            document.getElementById('avg-confidence').textContent =
                (data.avg_confidence || 0).toFixed(2);
            document.getElementById('recent-patterns').textContent =
                data.recent_patterns_24h || 0;
        }

        async function loadPrivacySettings() {
            const response = await fetch(`${API_BASE}/controls/privacy/settings?user_id=${USER_ID}`);
            const data = await response.json();

            const settings = data.privacy_settings;
            document.getElementById('share-patterns').checked = settings.share_patterns;
            document.getElementById('share-users').checked = settings.share_across_users;
            document.getElementById('allow-automation').checked = settings.allow_automation;
            document.getElementById('allow-predictive').checked = settings.allow_predictive;
        }

        async function toggleLearning() {
            const statusResponse = await fetch(
                `${API_BASE}/controls/learning/status?user_id=${USER_ID}`
            );
            const statusData = await statusResponse.json();

            const endpoint = statusData.learning_enabled ? 'disable' : 'enable';
            const response = await fetch(
                `${API_BASE}/controls/learning/${endpoint}`,
                {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({user_id: USER_ID})
                }
            );

            await loadLearningStatus();
        }

        async function exportData() {
            const response = await fetch(
                `${API_BASE}/controls/export?user_id=${USER_ID}&format=json`
            );
            const data = await response.json();

            // Download as JSON file
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `learning-data-${USER_ID}-${Date.now()}.json`;
            a.click();
        }

        async function clearData() {
            if (!confirm('Are you sure you want to clear all learned data? This cannot be undone.')) {
                return;
            }

            const response = await fetch(
                `${API_BASE}/controls/data/clear?user_id=${USER_ID}&data_type=all`,
                {method: 'DELETE'}
            );
            const data = await response.json();

            alert('Learned data cleared successfully');
            await loadMetrics();
        }

        async function savePrivacySettings() {
            const settings = {
                share_patterns: document.getElementById('share-patterns').checked,
                share_across_users: document.getElementById('share-users').checked,
                data_retention_days: 0,
                allow_automation: document.getElementById('allow-automation').checked,
                allow_predictive: document.getElementById('allow-predictive').checked
            };

            const response = await fetch(
                `${API_BASE}/controls/privacy/settings`,
                {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        user_id: USER_ID,
                        settings: settings
                    })
                }
            );

            alert('Privacy settings saved successfully');
        }
    </script>
</body>
</html>
```

---

### Phase 3: Integration Testing (30 min)

**Step 1: Create Integration Tests** (30 min)

Create `tests/integration/test_user_controls.py`:

```python
"""
Integration tests for user controls and dashboard.

Tests user control endpoints, privacy settings, and dashboard functionality.
"""

import pytest
from services.domain.user_preference_manager import UserPreferenceManager


class TestUserControls:
    """Test user control endpoints."""

    @pytest.mark.asyncio
    async def test_enable_disable_learning(self, client, db_session):
        """Test enabling and disabling learning."""
        user_id = "test_user"

        # Enable learning
        response = await client.post(
            "/api/v1/learning/controls/learning/enable",
            json={"user_id": user_id}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["learning_enabled"] is True

        # Check status
        response = await client.get(
            f"/api/v1/learning/controls/learning/status?user_id={user_id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["learning_enabled"] is True

        # Disable learning
        response = await client.post(
            "/api/v1/learning/controls/learning/disable",
            json={"user_id": user_id}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["learning_enabled"] is False

        # Check status again
        response = await client.get(
            f"/api/v1/learning/controls/learning/status?user_id={user_id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["learning_enabled"] is False

    @pytest.mark.asyncio
    async def test_clear_learned_data(self, client, db_session):
        """Test clearing learned data."""
        user_id = "test_user"

        # Clear all data
        response = await client.delete(
            f"/api/v1/learning/controls/data/clear?user_id={user_id}&data_type=all"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data_type"] == "all"

        # Clear patterns only
        response = await client.delete(
            f"/api/v1/learning/controls/data/clear?user_id={user_id}&data_type=patterns"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data_type"] == "patterns"

    @pytest.mark.asyncio
    async def test_export_preferences(self, client, db_session):
        """Test exporting user preferences."""
        user_id = "test_user"

        # Export as JSON
        response = await client.get(
            f"/api/v1/learning/controls/export?user_id={user_id}&format=json"
        )
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "preferences" in data
        assert "patterns" in data
        assert data["user_id"] == user_id


class TestPrivacySettings:
    """Test privacy settings."""

    @pytest.mark.asyncio
    async def test_set_privacy_settings(self, client, db_session):
        """Test setting privacy settings."""
        user_id = "test_user"

        settings = {
            "share_patterns": True,
            "share_across_users": False,
            "data_retention_days": 90,
            "allow_automation": True,
            "allow_predictive": True
        }

        response = await client.post(
            "/api/v1/learning/controls/privacy/settings",
            json={"user_id": user_id, "settings": settings}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["privacy_settings"] == settings

    @pytest.mark.asyncio
    async def test_get_privacy_settings(self, client, db_session):
        """Test getting privacy settings."""
        user_id = "test_user"

        response = await client.get(
            f"/api/v1/learning/controls/privacy/settings?user_id={user_id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert "privacy_settings" in data
        assert "share_patterns" in data["privacy_settings"]

    @pytest.mark.asyncio
    async def test_invalid_privacy_setting(self, client, db_session):
        """Test invalid privacy setting rejected."""
        user_id = "test_user"

        settings = {
            "invalid_key": True
        }

        response = await client.post(
            "/api/v1/learning/controls/privacy/settings",
            json={"user_id": user_id, "settings": settings}
        )
        assert response.status_code == 400


class TestDashboardIntegration:
    """Test dashboard integration."""

    @pytest.mark.asyncio
    async def test_dashboard_loads_metrics(self, client, db_session):
        """Test dashboard can load metrics from analytics API."""
        response = await client.get("/api/v1/learning/analytics")
        assert response.status_code == 200
        data = response.json()

        # Verify required metrics exist
        assert "total_patterns" in data
        assert "success_rate" in data
        assert "avg_confidence" in data

    @pytest.mark.asyncio
    async def test_dashboard_loads_status(self, client, db_session):
        """Test dashboard can load learning status."""
        user_id = "test_user"

        response = await client.get(
            f"/api/v1/learning/controls/learning/status?user_id={user_id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert "learning_enabled" in data
```

---

## Verification Steps

### Step 1: Verify User Control Endpoints

```bash
# Test enable learning
curl -X POST http://localhost:8001/api/v1/learning/controls/learning/enable \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'

# Test learning status
curl http://localhost:8001/api/v1/learning/controls/learning/status?user_id=test_user

# Test disable learning
curl -X POST http://localhost:8001/api/v1/learning/controls/learning/disable \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'

# Test export
curl http://localhost:8001/api/v1/learning/controls/export?user_id=test_user&format=json
```

---

### Step 2: Run Integration Tests

```bash
# Run user control tests
pytest tests/integration/test_user_controls.py -v

# Should pass all tests!
```

---

### Step 3: Verify Dashboard UI

```bash
# Open dashboard in browser
open http://localhost:8001/ui/learning_dashboard.html

# OR if using React
npm run dev
open http://localhost:3000/dashboard
```

---

### Step 4: Verify All Tests Still Pass

```bash
# Run ALL tests (including existing ones)
pytest tests/ -v

# Should pass all tests with zero regressions!
```

---

## Success Criteria

CORE-LEARN-F is complete when:

- [ ] User control endpoints complete (4 endpoints: enable/disable/clear/export)
- [ ] Privacy settings endpoints complete (set/get)
- [ ] Dashboard UI components complete (~300 lines)
- [ ] Integration tests passing (6+ tests)
- [ ] All existing tests still passing (zero regressions)
- [ ] Manual testing demonstrates user controls work
- [ ] Dashboard displays metrics correctly
- [ ] Code committed with evidence
- [ ] Session log updated

---

## Files to Create/Modify

### Modify (Add Endpoints)

- `web/api/routes/learning.py` (~150 lines added) - User control endpoints

### Create (Dashboard UI)

- `web/ui/learning_dashboard.html` (~300 lines) - Dashboard UI
- OR `web/ui/components/LearningDashboard.jsx` (~300 lines) - React version

### Create (Tests)

- `tests/integration/test_user_controls.py` (~200 lines) - Integration tests

### Session Log

- Continue in existing log or create: `dev/2025/10/20/HHMM-prog-code-log.md`

---

## Expected Timeline

**Total**: 4.5 hours (from discovery)

**Phase-by-Phase**:
- 2h: User controls (4 endpoints + privacy settings)
- 2h: Dashboard UI (components + integration)
- 30 min: Integration testing

**More realistic** (if pattern holds): 2-3 hours!

---

## Remember

**THIS IS THE FINALE - FINISH STRONG!**

**Critical principles**:
1. ✅ User controls are IMPORTANT (enable/disable matters!)
2. ✅ Privacy settings are IMPORTANT (user trust!)
3. ✅ Dashboard should be POLISHED (first impression!)
4. ✅ Testing is IMPORTANT (verify everything works!)
5. ✅ Zero regressions (maintain quality!)

**This is the LAST issue of Sprint A5**:
- Complete Learning System delivery
- Clean, shippable milestone
- Sprint A6 ready to start
- Celebrate when done!

**Finish strong!** 🎯

---

**Ready to complete Sprint A5 with polish!** 🚀

*Discovery found 90% complete (~7,500 lines). Implementation is ~850 lines of careful polish work. Issue 6 of 6 - SPRINT A5 FINALE!*

**Stay grounded, work carefully, finish strong!** ✨
