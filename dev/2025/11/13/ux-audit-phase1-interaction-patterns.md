# Phase 1.2: Interaction Pattern Inventory
**UX Investigation - Piper Morgan**
**Date**: November 13, 2025
**Investigator**: Claude Code (UXR)

---

## Executive Summary

This document catalogs all interaction patterns observed across Piper Morgan's touchpoints. Interaction patterns include user input methods, feedback mechanisms, navigation behaviors, form handling, and state transitions.

**Key Finding**: While individual touchpoints have well-thought-out interaction patterns, there is **no consistency across touchpoints**. Each interface implements its own approach to common interactions like loading states, error handling, and confirmations.

---

## Input Patterns

### 1. Text Input

#### Chat Input (Web Chat)
```html
<input
  type="text"
  class="chat-input"
  placeholder="e.g., Users are complaining about the login page being slow..."
  required
/>
```

**Characteristics**:
- Single-line text input
- Full-width with margin
- Placeholder provides example
- Required field validation
- Submit on button click only (no Enter key observed)
- Clears after submission

**Visual Feedback**:
- Focus state: Border color changes (`#ecf0f1` → `#3498db`)
- No character count
- No input validation until submit

---

#### File Input (Web Chat)
```html
<input
  type="file"
  accept=".txt,.pdf,.docx,.md,.json"
  required
/>
```

**Characteristics**:
- File picker dialog
- Whitelist of file types
- Client-side validation (type and size)
- Max size: 10MB
- Upload on separate button click
- Progress bar during upload

**Validation Messages**:
- "Please select a file" - Missing file
- "File too large (X MB). Maximum is 10MB." - Size exceeded
- "Unsupported file type. Allowed: .txt, .pdf, .docx, .md, .json" - Type invalid

---

### 2. Button Interactions

#### Primary Action Button (Light Theme)
```css
.submit-btn {
  background: #3498db;
  padding: 15px 30px;
  border-radius: 8px;
  cursor: pointer;
}
.submit-btn:hover {
  background: #2980b9;
}
```

**Behavior**:
- Hover effect (color darkens)
- Cursor changes to pointer
- Click triggers action immediately
- No loading state on button itself (see "Thinking..." message instead)

**Examples**:
- "Send" (chat form)
- "Upload" (file upload)
- "Generate Standup" (standup page)

---

#### Primary Action Button (Dark Theme)
```css
button {
  background: #007acc;
  padding: 12px 24px;
  border-radius: 8px;
  transition: all 0.2s ease;
}
button:hover:not(:disabled) {
  background: #005a9e;
  transform: translateY(-1px);
}
```

**Behavior**:
- Hover effect (color darkens + lift animation)
- Smooth transitions
- Disabled state prevents hover effects
- Click triggers action

**Examples**:
- "Toggle Learning" (learning dashboard)
- "Save Preferences" (personality prefs)
- "Export My Data" (learning dashboard)

---

#### Button Variants (Dark Theme Only)

**Secondary Button**:
```css
button.secondary {
  background: #555;
}
button.secondary:hover:not(:disabled) {
  background: #666;
}
```
- Examples: "↻ Refresh", "🔄 Reset to Defaults"

**Danger Button**:
```css
button.danger {
  background: #dc2626;
}
button.danger:hover:not(:disabled) {
  background: #b91c1c;
}
```
- Examples: "Disable Learning", "🗑 Clear All Data"

**Success Button**:
```css
button.success {
  background: #16a34a;
}
button.success:hover:not(:disabled) {
  background: #15803d;
}
```
- Examples: "Enable Learning", "Save Privacy Settings"

**❗ INCONSISTENCY**: Light theme has no button variants - only one style for all actions.

---

#### Toggle Button (Dark Theme)
```html
<button class="upload-toggle">
  📄 Upload a document to the knowledge base
</button>
```

**Behavior**:
- Click toggles visibility of hidden section
- Text doesn't change to indicate state
- No visual indicator of expanded/collapsed state
- Full-width button

**Location**: Web chat (light theme, but uses darker color: `#7f8c8d`)

---

### 3. Sliders

#### Range Slider (Personality Preferences)
```html
<input
  type="range"
  min="0"
  max="1"
  step="0.1"
  value="0.7"
  class="slider"
/>
```

**Characteristics**:
- Custom styled range input
- Live value display updates as you drag
- Smooth CSS styling (custom thumb)
- Immediate feedback (live preview updates)
- No "Apply" button needed

**Visual Design**:
```css
.slider {
  width: 100%;
  height: 6px;
  background: #444;
  border-radius: 3px;
}
.slider::-webkit-slider-thumb {
  width: 20px;
  height: 20px;
  background: #007acc;
  border-radius: 50%;
  cursor: pointer;
}
```

**Labels**:
- Min/Max labels on left/right
- Current value displayed in center with highlight color

---

### 4. Radio Buttons

#### Custom Radio Cards (Personality Preferences)
```html
<div class="radio-option selected" data-value="contextual">
  <input type="radio" name="confidence" value="contextual" checked />
  <label>Contextual (based on patterns...)</label>
</div>
```

**Characteristics**:
- Native radio hidden with `display: none`
- Styled as cards with background color
- Click entire card to select
- Selected state: Blue background (`#007acc`)
- Hover state: Lighter background (`#3a3a3a`)

**Behavior**:
- Single selection only
- Immediate feedback (selection changes instantly)
- No "Apply" button in some cases
- Changes trigger save button to appear in others

**Visual Design**:
```css
.radio-option {
  background: #333;
  padding: 12px 18px;
  border-radius: 6px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}
.radio-option.selected {
  background: #007acc;
  border-color: #005a9e;
}
```

**❗ NOTE**: Only found in dark theme interfaces. Light theme would use native radio buttons.

---

### 5. Toggle Switches

#### Privacy Toggle (Learning Dashboard)
```html
<label class="toggle-switch">
  <input type="checkbox" onchange="onPrivacyChange()">
  <span class="toggle-slider"></span>
</label>
```

**Characteristics**:
- Custom styled checkbox as toggle switch
- Native checkbox hidden
- Animated slider transition
- Color changes: Gray (#555) → Blue (#007acc)
- Changes trigger "unsaved changes" state

**Visual Design**:
```css
.toggle-slider {
  width: 50px;
  height: 26px;
  background-color: #555;
  border-radius: 26px;
  transition: 0.3s;
}
.toggle-slider:before {
  content: "";
  height: 18px;
  width: 18px;
  background-color: white;
  border-radius: 50%;
  transition: 0.3s;
}
input:checked + .toggle-slider {
  background-color: #007acc;
}
input:checked + .toggle-slider:before {
  transform: translateX(24px);
}
```

**Behavior**:
- Immediate visual feedback
- Shows "Save Privacy Settings" button when changed
- Requires explicit save action
- No auto-save

---

### 6. Collapsible Sections

#### Upload Section (Web Chat)
```javascript
document.getElementById("upload-toggle-btn").addEventListener("click", () => {
  const container = document.getElementById("upload-form-container");
  container.style.display = container.style.display === "none" ? "block" : "none";
});
```

**Characteristics**:
- Toggle button controls visibility
- No animation (instant show/hide)
- No indicator of current state (no arrow or icon rotation)
- Content hidden by default

**❗ ISSUE**: No visual feedback that section is expandable/collapsible.

---

## Feedback Patterns

### 1. Loading States

#### Text-Based Loading (Web Chat)
```javascript
const thinkingDiv = appendMessage("Thinking...");
thinkingDiv.classList.add("thinking");
```

```css
.bot-message.thinking {
  color: #7f8c8d;
  font-style: italic;
}
```

**Characteristics**:
- Italicized gray text
- Message says "Thinking..."
- Appears in chat window as message
- Removed when response arrives
- No animation

---

#### Button State Loading (Standup)
```javascript
loadBtn.disabled = true;
loadBtn.textContent = "Loading...";
// ... after completion ...
loadBtn.disabled = false;
loadBtn.textContent = "Generate Standup";
```

**Characteristics**:
- Button becomes disabled
- Text changes to "Loading..."
- Button color changes to gray (`#bdc3c7`)
- No spinner or animation
- Button restores after completion

---

#### Spinner Loading (Learning Dashboard)
```css
.spinner {
  border: 3px solid #333;
  border-top: 3px solid #007acc;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

**Characteristics**:
- Animated spinner (CSS keyframes)
- Circular border animation
- Accompanied by "Loading..." text
- Centered in container

---

#### Progress Bar (File Upload)
```html
<div id="upload-progress">
  <div id="upload-progress-fill">0%</div>
</div>
```

```css
#upload-progress-fill {
  width: 0%;
  background: linear-gradient(90deg, #27ae60, #2ecc71);
  transition: width 0.3s ease;
}
```

**Characteristics**:
- Linear progress bar
- Percentage text inside bar
- Green gradient background
- Smooth width transitions
- Simulated progress (not true upload progress)

---

#### Status Badge Loading (Learning Dashboard)
```html
<div class="status-badge loading">
  <span class="status-dot"></span>
  <span>Loading...</span>
</div>
```

```css
.status-badge.loading {
  background: #4a4a1e;
  color: #fbbf24;
  border: 1px solid #fbbf24;
}
.status-dot {
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

**Characteristics**:
- Badge format with pulsing dot
- Yellow color scheme
- Dot pulses slowly
- Text says "Loading..."

---

### 2. Success States

#### Success Message (Web Chat)
```css
.success {
  background: #d4edda;
  border-color: #c3e6cb;
  color: #155724;
}
```

**Examples**:
- "✅ Standup generated successfully!"
- "✅ Document Uploaded! (ID: ...)"
- Emoji + descriptive message
- Green color scheme
- Box with border

---

#### Success Message (Learning Dashboard)
```css
.message.success {
  background: #1b2d1b;
  color: #4ade80;
  border-left: 4px solid #4ade80;
}
```

**Examples**:
- "Dashboard loaded successfully"
- "Learning enabled successfully"
- "Privacy settings saved successfully"
- Dark green background
- Left border accent
- Auto-dismisses after 3-5 seconds

---

#### Success Badge (Learning Dashboard)
```html
<div class="status-badge enabled">
  <span class="status-dot"></span>
  <span>Enabled</span>
</div>
```

```css
.status-badge.enabled {
  background: #1e4620;
  color: #4ade80;
  border: 1px solid #4ade80;
}
```

**Characteristics**:
- Badge format with animated dot
- Green color scheme
- Persistent (doesn't auto-dismiss)
- Part of status display

---

### 3. Error States

#### Error Message (Web Chat - Light)
```css
.error {
  background: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
}
```

**Examples**:
- "❌ Error generating standup: [details]"
- "❌ Network error: [message]"
- "An API error occurred"

**Characteristics**:
- Light red background
- Red text
- Border accent
- Emoji prefix (sometimes)
- Persistent until next action

---

#### Error Message (Learning Dashboard - Dark)
```css
.message.error {
  background: #2d1b1b;
  color: #ff6b6b;
  border-left: 4px solid #ff6b6b;
}
```

**Examples**:
- "Failed to load dashboard: [error]"
- "❌ Upload failed: [details]"
- "❌ Network error: [message]"

**Characteristics**:
- Dark red background
- Light red text
- Left border accent
- May auto-dismiss or persist

---

#### Error Badge (Learning Dashboard)
```html
<div class="status-badge disabled">
  <span class="status-dot"></span>
  <span>Disabled</span>
</div>
```

```css
.status-badge.disabled {
  background: #4a1e1e;
  color: #f87171;
  border: 1px solid #f87171;
}
```

**Characteristics**:
- Badge format
- Red color scheme
- Not necessarily an "error" but indicates "off" state

---

### 4. Empty States

#### Chat Window Empty (Web Chat)
```html
<div class="message bot-message">
  Hello! How can I help you today?
</div>
```

**Characteristics**:
- Welcoming message
- Encourages first interaction
- No graphic or illustration

**❗ MISSING**: No empty state for when chat history is cleared.

---

#### Pattern Distribution Empty (Learning Dashboard)
```javascript
if (Object.keys(distribution).length === 0) {
  container.innerHTML = `
    <div class="empty-state">
      <div class="empty-state-icon">📊</div>
      <p>No patterns learned yet</p>
    </div>
  `;
}
```

**Characteristics**:
- Centered layout
- Large emoji icon (📊)
- Brief explanatory text
- Neutral color (gray)

**❗ GOOD PRACTICE**: Provides context for why section is empty.

---

### 5. Info/Warning States

#### Info Message (File Upload)
```css
#upload-status.info {
  background: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}
```

**Examples**:
- "📤 Uploading [filename] ([size])..."

**Characteristics**:
- Light blue background
- Dark blue text
- Border accent
- Emoji prefix
- Shows during in-progress action

**❗ NOTE**: Only found in file upload. No general "info" message pattern elsewhere.

---

## Confirmation Patterns

### 1. Native Confirm Dialog

#### Destructive Actions (Learning Dashboard)
```javascript
if (!confirm('⚠️ WARNING: This will permanently delete your learned data. Continue?')) return;
if (!confirm('Are you absolutely sure? This cannot be undone.')) return;
```

**Used For**:
- Clearing all data (double confirmation)
- Disabling learning
- Enabling learning

**Characteristics**:
- Native browser confirm dialog
- Blocks UI until response
- Two confirmations for highly destructive actions
- Emoji in message text (⚠️)

**❗ INCONSISTENCY**: Uses native confirm in dark theme interfaces. Would break visual consistency.

---

### 2. Implicit Confirmation

#### Save Button Appears When Needed
```javascript
function onPrivacyChange() {
  privacySettingsChanged = true;
  document.getElementById('savePrivacyBtn').style.display = 'block';
}
```

**Used For**:
- Privacy settings changes

**Characteristics**:
- Button hidden by default
- Appears when settings change
- User must explicitly click "Save"
- Provides opportunity to review changes

**❗ GOOD PRACTICE**: Prevents accidental saves, gives user control.

---

### 3. No Confirmation

**Actions that proceed immediately**:
- Sending chat message
- Uploading file (after selection)
- Generating standup
- Refreshing dashboard
- Exporting data

**❗ INCONSISTENCY**: Some potentially irreversible actions (like sending messages) have no confirmation, while others (like clearing data) have double confirmation.

---

## Navigation Patterns

### 1. Direct URL Entry

**Current State**: Only way to navigate between touchpoints
- Type URL manually
- Bookmark URLs
- No global navigation menu
- No breadcrumbs
- No "back" button

**URLs**:
- `/` - Home (chat)
- `/standup` - Standup report
- `/assets/learning-dashboard.html` - Learning dashboard
- `/assets/personality-preferences.html` - Personality preferences

**❗ CRITICAL ISSUE**: Poor discoverability. Users won't know features exist.

---

### 2. In-Page Navigation

#### Keyboard Shortcuts (Learning Dashboard Only)
```javascript
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey || e.metaKey) {
    if (e.key === 'r' || e.key === 'R') {
      e.preventDefault();
      refreshDashboard();
    } else if (e.key === 'e' || e.key === 'E') {
      e.preventDefault();
      exportData();
    }
  }
});
```

**Shortcuts**:
- `Cmd+R` or `Ctrl+R`: Refresh dashboard
- `Cmd+E` or `Ctrl+E`: Export data

**❗ GOOD PRACTICE**: Keyboard shortcuts for power users.

**❗ ISSUE**: Only in learning dashboard. No shortcuts elsewhere. No shortcut documentation visible to user.

---

### 3. Section Toggling

**Upload section toggle**:
- Click button to show/hide form
- No smooth animation
- Instant show/hide

**❗ ISSUE**: Could benefit from smooth transitions.

---

## Form Handling Patterns

### 1. Inline Validation

#### File Upload
```javascript
if (file.size > UPLOAD_CONFIG.MAX_SIZE) {
  showUploadStatus(`File too large...`, "error");
  return;
}
if (!UPLOAD_CONFIG.ALLOWED_TYPES.includes(file.type)) {
  showUploadStatus(`Unsupported file type...`, "error");
  return;
}
```

**Characteristics**:
- Client-side validation before submission
- Immediate feedback
- Prevents invalid submissions
- Error message shows specific issue

---

#### Chat Input
```html
<input type="text" required />
```

**Characteristics**:
- HTML5 required attribute
- Browser handles validation
- Generic error message from browser
- No custom styling

**❗ INCONSISTENCY**: Mix of custom and browser validation.

---

### 2. Form Submission

#### Chat Form
```javascript
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  appendMessage(message, true);
  input.value = "";

  const thinkingDiv = appendMessage("Thinking...");
  // ... API call ...
});
```

**Characteristics**:
- Prevents default form submission
- Clears input immediately
- Shows optimistic UI (message appears before API responds)
- Shows loading state
- Handles success/error

---

#### File Upload Form
```javascript
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  // Validation
  // Show uploading status
  // Simulate progress
  // API call
  // Show success/error
  // Clear form after delay
});
```

**Characteristics**:
- Prevents default
- Validates before submission
- Shows progress
- Clears form after success
- Keeps form visible on error

---

### 3. Auto-Save vs Manual Save

**Auto-Save**: None observed

**Manual Save**:
- Personality preferences: Explicit "Save Preferences" button
- Privacy settings: "Save Privacy Settings" button appears when changed
- Learning settings: Actions take effect immediately (toggle learning)

**❗ INCONSISTENCY**: Mix of immediate actions and explicit save requirements.

---

## State Transition Patterns

### 1. Button State Transitions

#### Standup Button
```
[Initial] "Generate Standup" (blue, enabled)
    ↓ (click)
[Loading] "Loading..." (gray, disabled)
    ↓ (API completes)
[Success] "Generate Standup" (blue, enabled)
    ↓ (can click again)
```

---

#### Learning Toggle
```
[Enabled] "Disable Learning" (red/danger)
    ↓ (click + confirm)
[Loading] "Disable Learning" (gray, disabled)
    ↓ (API completes)
[Disabled] "Enable Learning" (green/success)
    ↓ (click + confirm)
[Loading] "Enable Learning" (gray, disabled)
    ↓ (API completes)
[Enabled] "Disable Learning" (red/danger)
```

**❗ GOOD PRACTICE**: Button text and color reflect current state and available action.

---

### 2. Message State Transitions

#### Chat Message Flow
```
[User Types] → [User Submits]
    ↓
[User Message] (blue bubble, right-aligned)
    ↓
[Thinking Message] (gray, italic, "Thinking...")
    ↓ (API responds)
[Bot Message] (gray bubble, left-aligned, markdown rendered)
    ↓ (if workflow started)
[Workflow Status Message] ("Starting workflow...")
    ↓ (polling)
[Workflow Complete] (rendered results)
```

---

#### File Upload Flow
```
[Select File]
    ↓ (client validation)
[Valid?] → No → [Error Message] (red)
    ↓ Yes
[Click Upload]
    ↓
[Info Message] "Uploading..." (blue)
[Progress Bar] 0% → 100%
    ↓ (API completes)
[Success Message] "Uploaded!" (green)
[Chat Message] "📎 Document uploaded..."
    ↓ (after 2s delay)
[Form Clears] (ready for next upload)
```

---

### 3. Status Badge Transitions

#### Learning Status
```
[Initial] "Loading..." (yellow badge, pulsing dot)
    ↓ (API loads)
[Enabled] "Enabled" (green badge, pulsing dot)
  OR
[Disabled] "Disabled" (red badge, pulsing dot)
    ↓ (user toggles)
[Same state maintained until next toggle]
```

---

## Polling Patterns

### 1. Workflow Status Polling (Web Chat)
```javascript
const intervalId = setInterval(async () => {
  pollCount++;
  const response = await fetch(`/api/v1/workflows/${workflowId}`);
  const data = await response.json();

  if (data.status === "completed") {
    // Render results
    clearInterval(intervalId);
  } else if (pollCount >= maxPolls) {
    // Timeout
    clearInterval(intervalId);
  }
}, 2000); // Poll every 2 seconds
```

**Characteristics**:
- Poll interval: 2 seconds
- Max polls: 30 (60 seconds total)
- Stops when: Completed, failed, or timeout
- User sees: "Starting workflow..." message updated with results

**❗ NOTE**: Polling instead of WebSocket. Acceptable for low-frequency updates but not ideal for high-traffic.

---

### 2. Auto-Refresh (Learning Dashboard)
```javascript
autoRefreshTimer = setInterval(refreshDashboard, AUTO_REFRESH_INTERVAL);
// AUTO_REFRESH_INTERVAL = 30000 (30 seconds)
```

**Characteristics**:
- Refresh interval: 30 seconds
- Refreshes: Entire dashboard (status, metrics, privacy settings)
- Stops when: User leaves page
- User sees: Timestamp updates, data may change

**❗ GOOD PRACTICE**: Keeps data fresh without user action.

**❗ ISSUE**: No visual indicator that auto-refresh is happening. Could confuse user if data changes unexpectedly.

---

## Animation Patterns

### 1. CSS Transitions

**Button Hover (Dark Theme)**:
```css
button {
  transition: all 0.2s ease;
}
button:hover:not(:disabled) {
  transform: translateY(-1px);
}
```

**Progress Bar**:
```css
#upload-progress-fill {
  transition: width 0.3s ease;
}
```

**Toggle Switch**:
```css
.toggle-slider, .toggle-slider:before {
  transition: 0.3s;
}
```

**Characteristics**:
- Short durations (0.2s - 0.3s)
- Ease timing function
- Smooth, not abrupt

---

### 2. CSS Animations

**Spinner**:
```css
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.spinner {
  animation: spin 1s linear infinite;
}
```

**Pulsing Dot**:
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
.status-dot {
  animation: pulse 2s infinite;
}
```

**Characteristics**:
- Infinite loops for loading indicators
- Linear or ease timing
- Smooth, continuous motion

---

### 3. No Animation

**Collapsible Sections**:
```javascript
container.style.display = container.style.display === "none" ? "block" : "none";
```

**Characteristics**:
- Instant show/hide
- No slide or fade
- Jarring transition

**❗ ISSUE**: Could benefit from smooth slide-down/up animation.

---

## Async Operation Patterns

### 1. Optimistic UI Updates

#### Chat Message
```javascript
// Add message immediately
appendMessage(message, true);
input.value = "";

// Then make API call
const response = await fetch(...);
```

**Characteristics**:
- User message appears instantly
- Input clears immediately
- Better perceived performance
- If API fails, error shown but message remains

**❗ GOOD PRACTICE**: Feels fast and responsive.

---

### 2. Pessimistic UI Updates

#### File Upload
```javascript
// Show status AFTER starting upload
const response = await fetch(...);

if (response.ok) {
  showUploadStatus("✅ Uploaded!", "success");
} else {
  showUploadStatus("❌ Upload failed", "error");
}
```

**Characteristics**:
- Status shows after API call starts
- Success/error based on actual response
- More accurate but feels slower

---

### 3. Progress Simulation

#### File Upload Progress
```javascript
let progress = 0;
const progressInterval = setInterval(() => {
  progress += Math.random() * 30;
  if (progress < 90) {
    progressFill.style.width = progress + "%";
  }
}, 300);

// After API completes
clearInterval(progressInterval);
progressFill.style.width = "100%";
```

**Characteristics**:
- Simulated progress (not real upload progress)
- Randomized increments
- Never reaches 100% until API confirms
- Stops at ~90% to avoid lying to user

**❗ NOTE**: Not true progress tracking. Could be misleading for large files.

---

## Data Display Patterns

### 1. Metrics Display

#### Standup Metrics
```html
<div class="metrics">
  <div class="metric">
    <div class="metric-value">123ms</div>
    <div class="metric-label">Generation Time</div>
  </div>
</div>
```

**Characteristics**:
- Large numeric value (2em, green)
- Small label below (gray)
- Centered alignment
- Grid layout (responsive)

---

#### Learning Dashboard Metrics
```html
<div class="metrics-grid">
  <div class="metric">
    <div class="metric-value">47</div>
    <div class="metric-label">Total Patterns</div>
  </div>
</div>
```

**Characteristics**:
- Very large numeric value (2.5em, blue)
- Small uppercase label (gray)
- Centered alignment
- Grid layout (2 or 4 columns)

**❗ SIMILARITY**: Both use similar metric card pattern with different styling.

---

### 2. Data Visualization

#### Pattern Distribution (Learning Dashboard)
```html
<div class="pattern-bar">
  <div class="pattern-label">workflow automation</div>
  <div class="pattern-bar-bg">
    <div class="pattern-bar-fill" style="width: 45%">
      <span class="pattern-count">12</span>
    </div>
  </div>
</div>
```

**Characteristics**:
- Horizontal bar chart
- Label on left
- Bar fills from left to right
- Count displayed inside bar
- Blue gradient background
- Smooth width transitions

**❗ NOTE**: Only visualization found. No pie charts, line graphs, etc.

---

### 3. List Display

#### Chat Messages
```html
<div class="message-container">
  <div class="message user-message">User text</div>
</div>
<div class="message-container">
  <div class="message bot-message">Bot response with <strong>markdown</strong></div>
</div>
```

**Characteristics**:
- Vertical list (newest at bottom)
- Different alignment for user vs bot
- Auto-scroll to newest message
- Markdown rendering in bot messages only

---

#### Standup Sections
```html
<div class="section">
  <h2>📋 Yesterday's Accomplishments</h2>
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
</div>
```

**Characteristics**:
- Sections with emoji icons
- Unordered lists
- Light background boxes
- Clear hierarchy

---

### 4. Debug Information

#### JSON Response Display
```html
<div class="section">
  <h2>📊 Full Response</h2>
  <pre>${JSON.stringify(data, null, 2)}</pre>
</div>
```

**Characteristics**:
- Raw JSON in `<pre>` tag
- Dark background (for light theme)
- Monospace font
- Formatted with 2-space indent
- Scrollable if needed

**❗ NOTE**: Debug info visible in production. Good for alpha testing, should be hidden/togglable later.

---

## Summary of Pattern Inconsistencies

### High Inconsistency Areas

1. **Button Variants**: Light theme has one style, dark theme has 4 variants
2. **Loading Indicators**: 4 different patterns (text, button text, spinner, progress bar)
3. **Error Display**: Different colors, formats, and behaviors across touchpoints
4. **Confirmations**: Mix of native confirm, implicit, and none
5. **Save Behavior**: Mix of immediate, auto-save, and manual save

### Areas of Good Consistency

1. **Typography**: System fonts used throughout
2. **Border Radius**: Mostly 8px (with some 10px, 12px variations)
3. **Animation Timing**: Consistently short (0.2s - 0.3s)
4. **Metrics Display**: Similar card-based approach

---

## Recommendations for Phase 3 (Design System)

Based on this inventory, the design system should include:

### Core Components Needed
1. **Button** (primary, secondary, danger, success)
2. **Input** (text, file, with validation states)
3. **Slider** (range input)
4. **Radio** (card-style)
5. **Toggle** (switch style)
6. **Message** (success, error, info, warning)
7. **Loading** (spinner, text, progress bar, button state)
8. **Empty State** (icon + text)
9. **Metric Card** (value + label)
10. **Status Badge** (enabled, disabled, loading)

### Interaction Patterns to Standardize
1. **Loading States**: Pick one primary pattern, use consistently
2. **Error Handling**: Unified format and behavior
3. **Confirmations**: Define when to use native vs custom
4. **Save Behavior**: Establish auto-save vs manual save rules
5. **Navigation**: Add global nav system
6. **Keyboard Shortcuts**: Document and expand

### Animation Patterns to Define
1. **Transitions**: Standard timing and easing
2. **Loading Animations**: Spinner style and speed
3. **Collapsible Sections**: Add slide animation
4. **Button Effects**: Standardize hover effects

---

**Document Version**: 1.0
**Last Updated**: 2025-11-13 18:15 PT
**Next**: Phase 1.3 - Visual Design Audit (detailed color/spacing tokens)
