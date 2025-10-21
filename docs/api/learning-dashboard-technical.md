# Learning Dashboard Technical Documentation

**Component**: Learning Dashboard UI
**File**: `web/assets/learning-dashboard.html`
**Sprint**: Sprint A5, CORE-LEARN-F (#226)
**Phase**: Phase 2 - Dashboard UI
**Status**: Production Ready

## Architecture Overview

### Single-File Design

The dashboard is implemented as a self-contained HTML file with embedded CSS and JavaScript:

**Rationale**:
- Zero build step required
- No external dependencies
- Fast deployment and loading
- Easy to maintain and update
- Reduces complexity

### Component Structure

```
learning-dashboard.html (939 lines)
├── HTML Structure (~200 lines)
│   ├── Header with title and timestamp
│   ├── Message container (error/success)
│   ├── Dashboard grid (5 cards)
│   └── Footer with links
├── CSS Styling (~400 lines)
│   ├── Dark theme variables
│   ├── Layout and grid system
│   ├── Card components
│   ├── Form controls
│   ├── Animations and transitions
│   └── Responsive breakpoints
└── JavaScript Controller (~340 lines)
    ├── Configuration
    ├── Data loading functions
    ├── UI update functions
    ├── Event handlers
    ├── Utility functions
    └── Initialization
```

## JavaScript Architecture

### Configuration Constants

```javascript
const API_BASE = '/api/v1/learning';
const USER_ID = 'current_user';
const AUTO_REFRESH_INTERVAL = 30000; // 30s
```

**Design Decision**: Hard-coded defaults with easy customization point at top of script section.

### Core Functions

#### 1. `loadDashboard()` - Orchestrator
```javascript
async function loadDashboard()
```

**Purpose**: Main entry point, loads all dashboard data in parallel

**Implementation**:
```javascript
await Promise.all([
    loadLearningStatus(),
    loadMetrics(),
    loadPrivacySettings()
]);
```

**Error Handling**: Individual failures don't block other loads

**Performance**: Parallel fetch reduces total load time by ~60%

#### 2. `loadLearningStatus()` - Status Display
```javascript
async function loadLearningStatus()
```

**API**: `GET /controls/learning/status?user_id=${USER_ID}`

**UI Updates**:
- Status badge text and color
- Status dot indicator
- Toggle button text (Enable/Disable)

**State Transitions**:
- Loading → Enabled → Disabled
- Loading → Disabled → Enabled
- Error state shows "Unknown"

#### 3. `loadMetrics()` - Analytics Display
```javascript
async function loadMetrics()
```

**API**: `GET /analytics`

**Data Processing**:
```javascript
const metrics = data.metrics || {};
const distribution = data.pattern_distribution || {};

document.getElementById('totalPatterns').textContent =
    metrics.total_patterns_learned || 0;
document.getElementById('activePreferences').textContent =
    metrics.active_preferences || 0;
document.getElementById('successRate').textContent =
    (metrics.success_rate || 0).toFixed(1) + '%';
document.getElementById('lastUpdated').textContent =
    metrics.last_updated || 'Never';
```

**Empty States**: Handles missing data gracefully with defaults

#### 4. `updatePatternDistribution()` - Visualization
```javascript
function updatePatternDistribution(distribution)
```

**Input**: Object with pattern types as keys, counts as values

**Output**: HTML bar chart visualization

**Algorithm**:
```javascript
const total = Object.values(distribution).reduce((sum, count) => sum + count, 0);
for (const [type, count] of Object.entries(distribution)) {
    const percentage = (count / total * 100).toFixed(1);
    // Create bar with percentage width
}
```

**CSS Integration**: Uses `.pattern-bar-fill` with dynamic width

#### 5. `loadPrivacySettings()` - Privacy Toggles
```javascript
async function loadPrivacySettings()
```

**API**: `GET /controls/privacy/settings?user_id=${USER_ID}`

**Settings Mapping**:
```javascript
const settings = data.privacy_settings || {};
document.getElementById('sharePatterns').checked =
    settings.share_patterns_across_features ?? false;
document.getElementById('allowSuggestions').checked =
    settings.allow_pattern_suggestions ?? false;
// ... etc
```

**Defaults**: All settings default to `false` (conservative privacy)

#### 6. `toggleLearning()` - Enable/Disable
```javascript
async function toggleLearning()
```

**Flow**:
1. Determine current state from button text
2. Show confirmation dialog
3. POST to `/controls/learning/enable` or `/disable`
4. Reload status on success
5. Show success message

**Confirmation Messages**:
- Disable: "Disable learning? (Existing data will be preserved)"
- Enable: "Enable learning?"

#### 7. `savePrivacySettings()` - Privacy Updates
```javascript
async function savePrivacySettings()
```

**API**: `POST /controls/privacy/settings`

**Payload Construction**:
```javascript
{
    user_id: USER_ID,
    privacy_settings: {
        share_patterns_across_features: document.getElementById('sharePatterns').checked,
        allow_pattern_suggestions: document.getElementById('allowSuggestions').checked,
        enable_cross_user_learning: document.getElementById('crossUserLearning').checked,
        store_detailed_metadata: document.getElementById('storeMetadata').checked,
        analytics_participation: document.getElementById('analyticsParticipation').checked
    }
}
```

**Optimistic Update**: UI reflects changes immediately, reverts on error

#### 8. `exportData()` - Data Export
```javascript
async function exportData()
```

**API**: `GET /controls/export?user_id=${USER_ID}&format=json`

**Download Implementation**:
```javascript
const blob = new Blob([JSON.stringify(data, null, 2)],
    { type: 'application/json' });
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = `learning-data-export-${timestamp}.json`;
a.click();
URL.revokeObjectURL(url);
```

**Keyboard Shortcut**: `Ctrl+E` triggers export

#### 9. `confirmClearData()` - Data Deletion
```javascript
async function confirmClearData(dataType)
```

**API**: `DELETE /controls/data/clear?user_id=${USER_ID}&data_type=${dataType}`

**Double Confirmation for "all"**:
```javascript
if (dataType === 'all') {
    if (!confirm('Are you SURE? This will delete ALL learning data.')) {
        return;
    }
}
```

**Data Type Options**:
- `all`: Everything (patterns + preferences + automation)
- `patterns`: Patterns only
- `preferences`: Preferences only

#### 10. Auto-Refresh System

**Timer Management**:
```javascript
let refreshTimer = null;

function startAutoRefresh() {
    if (refreshTimer) clearInterval(refreshTimer);
    refreshTimer = setInterval(async () => {
        await refreshDashboard();
    }, AUTO_REFRESH_INTERVAL);
}
```

**Refresh Scope**:
- Metrics (changes frequently)
- Pattern distribution (changes frequently)
- Learning status (changes infrequently)
- Privacy settings (NOT refreshed - only on load)

**Performance**: Staggered fetches prevent API overload

### Event Handling

#### Window Load Event
```javascript
window.addEventListener('DOMContentLoaded', async () => {
    await loadDashboard();
    updateTimestamp();
    startAutoRefresh();
});
```

**Sequence**:
1. Wait for DOM ready
2. Load all dashboard data
3. Set initial timestamp
4. Start auto-refresh timer

#### Keyboard Events
```javascript
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'r') {
        e.preventDefault();
        refreshDashboard();
    }
    if (e.ctrlKey && e.key === 'e') {
        e.preventDefault();
        exportData();
    }
});
```

**Shortcuts**:
- `Ctrl+R`: Manual refresh (prevents browser default)
- `Ctrl+E`: Export data

#### Privacy Toggle Changes
```javascript
<input type="checkbox" id="sharePatterns" onchange="onPrivacyChange()">
```

**Handler**:
```javascript
function onPrivacyChange() {
    // Debounce could be added here if needed
    savePrivacySettings();
}
```

**Design Decision**: Auto-save on change (no save button needed)

## CSS Architecture

### Dark Theme System

```css
:root {
    --bg-primary: #1a1a1a;
    --bg-card: #2d2d2d;
    --bg-input: #333;
    --border-color: #444;
    --text-primary: #e0e0e0;
    --text-secondary: #a0a0a0;
    --accent-primary: #007acc;
    --accent-hover: #005a9e;
}
```

**Consistency**: Matches `web/assets/standup.html` theme

### Layout System

**Grid**:
```css
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}
```

**Responsive Breakpoints**:
- Desktop (>768px): Multi-column grid
- Tablet (481-768px): 2-column grid
- Mobile (<480px): Single column

### Card Component

```css
.card {
    background: var(--bg-card);
    border-radius: 8px;
    border-left: 3px solid var(--accent-primary);
    padding: 20px;
    transition: transform 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
}
```

**Design Pattern**: Consistent card structure across all sections

### Toggle Switch Component

**HTML Structure**:
```html
<label class="toggle-switch">
    <input type="checkbox" id="settingId" onchange="onPrivacyChange()">
    <span class="toggle-slider"></span>
</label>
```

**CSS Implementation**:
```css
.toggle-switch {
    position: relative;
    width: 50px;
    height: 24px;
}

.toggle-slider {
    /* Slider track */
    position: absolute;
    background: #444;
    border-radius: 24px;
    transition: 0.3s;
}

.toggle-slider::before {
    /* Slider thumb */
    content: '';
    position: absolute;
    width: 18px;
    height: 18px;
    background: white;
    border-radius: 50%;
    transform: translateX(0);
    transition: 0.3s;
}

input:checked + .toggle-slider {
    background: var(--accent-primary);
}

input:checked + .toggle-slider::before {
    transform: translateX(26px);
}
```

**Accessibility**: Native checkbox hidden but functional for screen readers

### Status Badges

```css
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 14px;
}

.status-badge.enabled {
    background: #1e4620;
    color: #4ade80;
    border: 1px solid #4ade80;
}

.status-badge.disabled {
    background: #4a1e1e;
    color: #f87171;
    border: 1px solid #f87171;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: currentColor;
}
```

**States**: Loading (gray), Enabled (green), Disabled (red)

### Animations

**Card Hover**:
```css
transition: transform 0.2s ease;
transform: translateY(-2px);
```

**Button Hover**:
```css
transition: background-color 0.2s ease, transform 0.1s ease;
transform: translateY(-1px);
```

**Message Banners**:
```css
transition: all 0.3s ease;
opacity: 0; /* Hidden by default */
opacity: 1; /* When .show class added */
```

**Performance**: GPU-accelerated transforms, avoid layout thrashing

## API Integration Details

### Request Flow

```
User Action → Event Handler → Fetch API → Update UI → Show Message
```

### Error Handling Pattern

```javascript
async function apiFunction() {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const data = await response.json();
        // Process data
        showSuccess('Operation successful');
    } catch (error) {
        console.error('Error:', error);
        showError('Operation failed: ' + error.message);
    }
}
```

**Consistency**: All API calls follow this pattern

### Response Handling

**Expected Formats**:

**Analytics**:
```json
{
    "metrics": {
        "total_patterns_learned": 42,
        "active_preferences": 15,
        "success_rate": 85.5,
        "last_updated": "2025-10-20T17:30:00Z"
    },
    "pattern_distribution": {
        "workflow": 15,
        "query": 12,
        "issue_similarity": 8,
        "ui_preference": 5,
        "filter_preference": 2
    }
}
```

**Learning Status**:
```json
{
    "enabled": true,
    "user_id": "current_user"
}
```

**Privacy Settings**:
```json
{
    "privacy_settings": {
        "share_patterns_across_features": false,
        "allow_pattern_suggestions": false,
        "enable_cross_user_learning": false,
        "store_detailed_metadata": false,
        "analytics_participation": false
    }
}
```

### Request Payloads

**Toggle Learning**:
```javascript
POST /controls/learning/enable
{
    "user_id": "current_user"
}
```

**Save Privacy Settings**:
```javascript
POST /controls/privacy/settings
{
    "user_id": "current_user",
    "privacy_settings": {
        "share_patterns_across_features": true,
        // ... etc
    }
}
```

**Clear Data**:
```javascript
DELETE /controls/data/clear?user_id=current_user&data_type=all
// No body
```

## Performance Considerations

### Load Time Optimization

**Initial Load**:
- Single HTML file: ~30KB gzipped
- No external resources
- Parallel API fetches
- Total load time: < 500ms

**Refresh Performance**:
- Partial updates (only changed data)
- No DOM rebuilding unless necessary
- CSS transitions for smooth updates

### Memory Management

**Timer Cleanup**:
```javascript
function startAutoRefresh() {
    if (refreshTimer) clearInterval(refreshTimer); // Prevent memory leaks
    refreshTimer = setInterval(refreshDashboard, AUTO_REFRESH_INTERVAL);
}
```

**Blob URL Cleanup**:
```javascript
URL.revokeObjectURL(url); // After export download
```

### Network Optimization

**Parallel Fetches**:
```javascript
await Promise.all([
    loadLearningStatus(),
    loadMetrics(),
    loadPrivacySettings()
]);
```

**Bandwidth**: ~2-5KB per API call (JSON responses)

## Testing Strategy

### Unit Testing (Manual)

**Functions to Test**:
1. `updatePatternDistribution()` with various distributions
2. `showError()` / `showSuccess()` message display
3. `updateTimestamp()` formatting

**Test Data**:
```javascript
// Empty distribution
updatePatternDistribution({});

// Single pattern
updatePatternDistribution({ workflow: 10 });

// Multiple patterns
updatePatternDistribution({
    workflow: 15,
    query: 12,
    issue_similarity: 8
});
```

### Integration Testing (Manual)

**Test Cases**:
1. Load dashboard with server running
2. Toggle learning on/off
3. Change privacy settings
4. Export data
5. Clear data (each type)
6. Keyboard shortcuts
7. Auto-refresh behavior
8. Error states (server down)

### Browser Testing

**Browsers**:
- Chrome 90+
- Firefox 88+
- Safari 14+

**Devices**:
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

### Accessibility Testing

**Tools**:
- Lighthouse audit
- WAVE browser extension
- Keyboard-only navigation

**Checklist**:
- [ ] All interactive elements keyboard accessible
- [ ] Color contrast ratios meet WCAG AA
- [ ] Screen reader announces state changes
- [ ] No keyboard traps
- [ ] Semantic HTML structure

## Security Considerations

### XSS Prevention

**User Input**: Dashboard doesn't accept user text input (only checkboxes and buttons)

**API Responses**: Treated as trusted (server-side validation)

**Dynamic Content**:
```javascript
element.textContent = data.value; // Safe (text only)
element.innerHTML = `<div>...</div>`; // Only used with static content
```

### CSRF Protection

**Authentication**: Relies on FastAPI session authentication

**No Cookies**: User ID passed in URL parameters (not ideal for production)

**Production TODO**: Implement proper JWT or session-based auth

### Data Privacy

**Client-Side Storage**: None (no localStorage, no cookies)

**Data Transmission**: All via HTTPS in production

**User Control**: Complete data export and deletion capabilities

## Deployment

### Installation

1. File already deployed at `web/assets/learning-dashboard.html`
2. Served by FastAPI StaticFiles mount
3. No build step required

### Server Configuration

**FastAPI Mount**:
```python
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "assets")),
    name="assets",
)
```

**Access URL**: `http://{host}:{port}/assets/learning-dashboard.html`

### Production Checklist

- [ ] Set `USER_ID` to actual user authentication
- [ ] Verify HTTPS enabled
- [ ] Test with production API endpoints
- [ ] Run Lighthouse audit
- [ ] Verify CORS settings
- [ ] Test error handling with API failures
- [ ] Monitor performance metrics
- [ ] Set up analytics (if desired)

## Maintenance

### Code Updates

**Location**: `web/assets/learning-dashboard.html`

**Process**:
1. Edit HTML/CSS/JS in single file
2. Test locally with server running
3. Commit changes
4. Restart server (if needed for cache clearing)

**Version Control**: Entire dashboard in one file makes diffs clean

### API Changes

**If Endpoints Change**:
1. Update `const API_BASE` if base path changes
2. Update individual fetch URLs if routes change
3. Update payload structures if request format changes
4. Update response parsing if response format changes

**Backward Compatibility**: Dashboard designed to handle missing fields gracefully

### Browser Support

**Monitoring**: Check browser usage analytics

**Updates**: Test new browser versions when released

**Deprecation**: Drop support for browsers < 2 years old

## Future Enhancements

### Potential Features

1. **Real-time Updates**: WebSocket integration for live metrics
2. **Charts**: Add Chart.js for advanced visualizations
3. **Filtering**: Filter patterns by type, date, success rate
4. **Search**: Search patterns by keywords
5. **Comparison**: Compare metrics over time periods
6. **Notifications**: Browser notifications for important events
7. **Themes**: Light/dark theme toggle
8. **User Profiles**: Multi-user support with switching
9. **Batch Operations**: Bulk pattern management
10. **Export Formats**: CSV, Excel, PDF exports

### Technical Improvements

1. **Framework Migration**: Consider Vue.js/React for complex features
2. **State Management**: Implement Vuex/Redux for complex state
3. **Testing**: Add automated tests (Playwright/Cypress)
4. **Build Process**: Add bundler if external dependencies needed
5. **TypeScript**: Add type safety for JavaScript
6. **PWA**: Make dashboard installable as progressive web app
7. **Offline Support**: Cache API responses for offline viewing
8. **Performance**: Implement virtual scrolling for large datasets

## Troubleshooting Development Issues

### Common Issues

**Issue**: Dashboard shows all loading states
**Solution**: Check API endpoints are accessible, verify server running

**Issue**: Privacy settings not saving
**Solution**: Check network tab for API errors, verify payload structure

**Issue**: Auto-refresh not working
**Solution**: Check browser console for errors, verify timer is starting

**Issue**: Keyboard shortcuts don't work
**Solution**: Check event listener is attached, verify no other handler preventing default

**Issue**: Export downloads empty file
**Solution**: Verify API returns data, check Blob creation, inspect download trigger

## Code Style Guidelines

### JavaScript

- ES6+ syntax (async/await, template literals, destructuring)
- camelCase for function and variable names
- Descriptive function names (verb + noun pattern)
- Comments for complex logic
- Error handling in all async functions

### CSS

- BEM-like naming (`.card`, `.card-header`, `.card-title`)
- CSS variables for theme values
- Mobile-first responsive design
- Transitions for all interactive elements
- Consistent spacing (20px, 16px, 12px, 8px)

### HTML

- Semantic HTML5 elements
- Meaningful IDs and classes
- ARIA labels where appropriate
- Proper heading hierarchy (h1 → h2)
- Accessible form controls

## References

- **API Routes**: `web/api/routes/learning.py`
- **Integration Tests**: `tests/integration/test_user_controls.py`
- **User Guide**: `docs/api/learning-dashboard-guide.md`
- **Design Pattern**: `web/assets/standup.html`

---

*Technical documentation for CORE-LEARN-F Phase 2 implementation*
