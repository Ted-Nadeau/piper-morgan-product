# Code Agent Prompt: Polish Sprint - UX Refinements
## Foundation for Professional User Experience

**Date**: November 15, 2025, 10:25 AM PT  
**Assigned By**: Xian (PM)  
**Agent Role**: Code Agent (Implementation)  
**Context**: Quick Wins (G1, G8, G50, G2, G4) completed - now adding polish to transform from functional to professional  
**Timeline**: 1-2 weeks (flexible, working in parallel with strategic planning)  
**Environment**: Sandbox/branch (can work with autonomy)

---

## 🎯 Mission: Transform from Functional to Polished

You've successfully implemented the Quick Wins (navigation, user indicator, settings). Now we're adding the **professional polish** that makes Piper feel complete:

- **Toast notifications** → Users know their actions succeeded
- **Loading states** → Async operations feel fast and responsive  
- **Empty states** → Guidance when no content exists yet
- **Contextual help** → Features are self-explanatory
- **Keyboard shortcuts** → Power users can navigate efficiently

**Why This Matters**: Alpha users (Beatrice, Michelle, +others) are testing now. These improvements reduce support questions and increase satisfaction without requiring architectural changes.

---

## 🚨 CRITICAL: Accessibility Requirements

**BEFORE implementing ANY feature, you MUST**:

1. **Read CLAUDE.md** in the Piper Morgan repository:
   - Path: `/path/to/piper-morgan/CLAUDE.md`
   - Contains: WCAG 2.2 AA requirements, accessibility patterns
   - **Read this FIRST before writing any code**

2. **Follow WCAG 2.2 Level AA** for everything:
   - Color contrast: 4.5:1 for text, 3:1 for interactive elements
   - Keyboard navigation: Tab, Enter, Escape must work
   - Screen reader support: Proper ARIA labels and roles
   - Focus indicators: 2px outline, visible on all interactive elements

3. **Test accessibility** before marking complete:
   - Keyboard only (no mouse)
   - Tab through all interactive elements
   - Enter/Escape trigger expected actions
   - ARIA labels present on all dynamic content

**If CLAUDE.md conflicts with this prompt, CLAUDE.md wins.**

---

## 📋 Work Breakdown: Week 1 (Priority) + Week 2 (If Time)

### Week 1 Priority (Core Polish - 3-4 days)

**These three features are foundational** - they improve every existing feature:

1. **G23: Toast Notifications System** (Score: 420, Effort: 1-2 days)
2. **G29: Loading States & Spinners** (Score: 320, Effort: 1 day)
3. **G30: Empty States** (Score: 288, Effort: 1 day)

### Week 2 Stretch Goals (If Budget/Time Allows - 3-4 days)

**These add discoverability and power-user features**:

4. **G5: Contextual Help Links** (Score: 360, Effort: 1-2 days)
5. **G61: Keyboard Shortcuts** (Score: 252, Effort: 1-2 days)
6. **G43: Form Validation** (Score: 240, Effort: 1-2 days) - Optional
7. **G52: Session Timeout Handling** (Score: 315, Effort: 2 days) - Optional

**Start with Week 1, assess progress, then tackle Week 2 if able.**

---

## Feature 1: Toast Notifications System (G23)

**Score**: 420 (Impact: 7, Frequency: 10, Effort: 6)  
**Effort**: 1-2 days  
**Priority**: CRITICAL - Foundation for all user feedback

### Problem Statement

Users have no feedback when actions complete. Examples:
- Settings saved → No confirmation (did it work?)
- File uploaded → Silence (is it uploading? did it finish?)
- Standup submitted → No success message (should I refresh?)

**Impact**: Users feel uncertain, refresh pages unnecessarily, don't trust the system.

### Specification

**Create**: Toast notification system with 4 types (success, error, warning, info)

#### Component Structure

**File**: `/web/templates/components/toast.html`

```html
<!-- Toast Container (add to base.html or component) -->
<div class="toast-container" id="toast-container" aria-live="polite" aria-atomic="true">
  <!-- Toasts will be injected here dynamically -->
</div>

<!-- Toast Template (hidden, cloned by JS) -->
<template id="toast-template">
  <div class="toast" role="status">
    <div class="toast-icon">
      <!-- Icon will be set by JS based on type -->
    </div>
    <div class="toast-content">
      <div class="toast-title"></div>
      <div class="toast-message"></div>
    </div>
    <button class="toast-close" aria-label="Close notification">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
      </svg>
    </button>
  </div>
</template>
```

#### Styling

**File**: `/web/styles/components/toast.css` (or inline in toast.html)

```css
.toast-container {
  position: fixed;
  top: 80px; /* Below navigation */
  right: 24px;
  z-index: 1100; /* Above navigation (1000) */
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 400px;
  pointer-events: none; /* Allow clicks through container */
}

.toast {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-left: 4px solid;
  pointer-events: auto; /* Re-enable for toast itself */
  animation: toast-slide-in 0.3s ease-out;
  min-width: 320px;
}

@keyframes toast-slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.toast.toast-exit {
  animation: toast-slide-out 0.2s ease-in;
}

@keyframes toast-slide-out {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}

/* Toast Types */
.toast.toast-success {
  border-left-color: #27ae60;
}

.toast.toast-error {
  border-left-color: #e74c3c;
}

.toast.toast-warning {
  border-left-color: #f39c12;
}

.toast.toast-info {
  border-left-color: #3498db;
}

.toast-icon {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
}

.toast-success .toast-icon {
  color: #27ae60;
}

.toast-error .toast-icon {
  color: #e74c3c;
}

.toast-warning .toast-icon {
  color: #f39c12;
}

.toast-info .toast-icon {
  color: #3498db;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-weight: 600;
  font-size: 14px;
  color: #2c3e50;
  margin-bottom: 4px;
}

.toast-message {
  font-size: 14px;
  color: #7f8c8d;
  line-height: 1.4;
}

.toast-close {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  padding: 0;
  background: none;
  border: none;
  color: #7f8c8d;
  cursor: pointer;
  transition: color 0.2s;
}

.toast-close:hover {
  color: #2c3e50;
}

.toast-close:focus {
  outline: 2px solid #3498db;
  outline-offset: 2px;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .toast-container {
    right: 16px;
    left: 16px;
    max-width: none;
  }
  
  .toast {
    min-width: 0;
  }
}
```

#### JavaScript Implementation

**File**: `/web/static/js/toast.js`

```javascript
/**
 * Toast Notification System
 * 
 * Usage:
 *   Toast.success('Settings saved!', 'Your preferences have been updated')
 *   Toast.error('Upload failed', 'File size must be less than 10MB')
 *   Toast.warning('Session expiring', 'You will be logged out in 5 minutes')
 *   Toast.info('New feature', 'Dark mode is now available in settings')
 */

const Toast = {
  // Icons for each toast type (SVG paths)
  icons: {
    success: '<svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor"><path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/></svg>',
    error: '<svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg>',
    warning: '<svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>',
    info: '<svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/></svg>'
  },

  // Default duration (ms)
  defaultDuration: 5000,

  // Show toast notification
  show(type, title, message, duration = null) {
    const container = document.getElementById('toast-container');
    const template = document.getElementById('toast-template');
    
    if (!container || !template) {
      console.error('Toast container or template not found');
      return;
    }

    // Clone template
    const toast = template.content.cloneNode(true).querySelector('.toast');
    
    // Set type
    toast.classList.add(`toast-${type}`);
    
    // Set icon
    toast.querySelector('.toast-icon').innerHTML = this.icons[type];
    
    // Set content
    toast.querySelector('.toast-title').textContent = title;
    toast.querySelector('.toast-message').textContent = message;
    
    // Close button handler
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => this.dismiss(toast));
    
    // Add to container
    container.appendChild(toast);
    
    // Auto-dismiss after duration
    const dismissDuration = duration || this.defaultDuration;
    setTimeout(() => this.dismiss(toast), dismissDuration);
    
    // Keyboard support
    closeBtn.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.dismiss(toast);
      }
    });
  },

  // Dismiss toast
  dismiss(toast) {
    toast.classList.add('toast-exit');
    setTimeout(() => {
      toast.remove();
    }, 200); // Match animation duration
  },

  // Convenience methods
  success(title, message, duration) {
    this.show('success', title, message, duration);
  },

  error(title, message, duration) {
    this.show('error', title, message, duration);
  },

  warning(title, message, duration) {
    this.show('warning', title, message, duration);
  },

  info(title, message, duration) {
    this.show('info', title, message, duration);
  }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Toast;
}
```

#### Integration Examples

**In Settings Save**:
```javascript
// personality-preferences.html
document.getElementById('save-settings').addEventListener('click', async () => {
  try {
    const response = await fetch('/settings/personality', {
      method: 'POST',
      body: JSON.stringify(formData)
    });
    
    if (response.ok) {
      Toast.success('Settings saved', 'Your personality preferences have been updated');
    } else {
      Toast.error('Save failed', 'Please try again or contact support');
    }
  } catch (error) {
    Toast.error('Network error', 'Unable to save settings. Check your connection.');
  }
});
```

**In File Upload**:
```javascript
// File upload handler
async function handleUpload(file) {
  try {
    Toast.info('Uploading', `Uploading ${file.name}...`);
    
    const response = await uploadFile(file);
    
    if (response.ok) {
      Toast.success('Upload complete', `${file.name} has been uploaded`);
    } else {
      Toast.error('Upload failed', 'File size must be less than 10MB');
    }
  } catch (error) {
    Toast.error('Upload error', error.message);
  }
}
```

**In Standup Submission**:
```javascript
// standup.html
async function submitStandup(data) {
  try {
    const response = await fetch('/standup', {
      method: 'POST',
      body: JSON.stringify(data)
    });
    
    if (response.ok) {
      Toast.success('Standup submitted', 'Your standup has been saved and shared');
    } else {
      Toast.error('Submission failed', 'Please try again');
    }
  } catch (error) {
    Toast.error('Network error', 'Unable to submit standup');
  }
}
```

### Accessibility Requirements (CRITICAL)

**ARIA Attributes** (already in component):
- `role="status"` on toast (polite announcement)
- `aria-live="polite"` on container (announces new toasts)
- `aria-atomic="true"` (announces entire toast content)
- `aria-label="Close notification"` on close button

**Keyboard Navigation**:
- Close button focusable (Tab)
- Escape key dismisses toast
- Focus returns to trigger element after dismiss

**Screen Reader Support**:
- Success: "Settings saved. Your preferences have been updated."
- Error: "Upload failed. File size must be less than 10MB."
- Screen reader announces automatically when toast appears

**Color Contrast**:
- Border colors: 3:1 against white background ✅
- Icon colors: Same as borders ✅
- Text: #2c3e50 on white = 12.6:1 ✅
- Close button: #7f8c8d = 4.5:1 ✅

### Acceptance Criteria

- [ ] Toast component created in `/web/templates/components/toast.html`
- [ ] CSS styling in `/web/styles/components/toast.css`
- [ ] JavaScript in `/web/static/js/toast.js`
- [ ] Toast container added to base template (visible on all pages)
- [ ] 4 toast types work: success, error, warning, info
- [ ] Toasts auto-dismiss after 5 seconds
- [ ] Close button dismisses toast immediately
- [ ] Escape key dismisses toast
- [ ] Multiple toasts stack vertically
- [ ] Animations smooth (slide in/out)
- [ ] Mobile responsive (full width on small screens)
- [ ] Keyboard accessible (Tab to close button, Escape dismisses)
- [ ] Screen reader announces toast content
- [ ] Integrated in: Settings save, file upload, standup submit (minimum)

### Testing

**Manual Tests**:
1. Save settings → Toast appears: "Settings saved"
2. Upload file → Toast appears: "Upload complete"
3. Submit standup → Toast appears: "Standup submitted"
4. Trigger error (invalid input) → Error toast appears
5. Tab to close button → Focus visible
6. Press Escape → Toast dismisses
7. Multiple actions → Toasts stack (don't overlap)
8. Wait 5 seconds → Toast auto-dismisses
9. Resize to mobile → Toast full width
10. Test with screen reader → Content announced

**Files to Create/Modify**:
- Create: `/web/templates/components/toast.html`
- Create: `/web/styles/components/toast.css`
- Create: `/web/static/js/toast.js`
- Modify: `/web/templates/base.html` (add toast container)
- Modify: `/web/templates/personality-preferences.html` (add success toast)
- Modify: `/web/templates/standup.html` (add success toast)
- Modify: Any file upload handlers (add upload toasts)

---

## Feature 2: Loading States & Spinners (G29)

**Score**: 320 (Impact: 8, Frequency: 8, Effort: 5)  
**Effort**: 1 day  
**Priority**: HIGH - Makes async operations feel responsive

### Problem Statement

No visual feedback during async operations:
- File uploading → No spinner (is it working?)
- Standup submitting → Button stays enabled (can I click again?)
- Settings loading → Blank page (is it loading or broken?)

**Impact**: Users think app is frozen, click multiple times, lose trust.

### Specification

**Create**: Reusable loading spinner component + button loading states

#### Spinner Component

**File**: `/web/templates/components/spinner.html`

```html
<!-- Inline Spinner (for buttons, small spaces) -->
<svg class="spinner spinner-sm" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <circle class="spinner-track" cx="12" cy="12" r="10" fill="none" stroke-width="3"/>
  <circle class="spinner-head" cx="12" cy="12" r="10" fill="none" stroke-width="3"/>
</svg>

<!-- Page Spinner (for full-page loading) -->
<div class="spinner-container" role="status" aria-live="polite">
  <svg class="spinner spinner-lg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <circle class="spinner-track" cx="12" cy="12" r="10" fill="none" stroke-width="2"/>
    <circle class="spinner-head" cx="12" cy="12" r="10" fill="none" stroke-width="2"/>
  </svg>
  <span class="spinner-text">Loading...</span>
</div>

<!-- Overlay Spinner (for blocking interactions) -->
<div class="spinner-overlay" role="status" aria-live="polite">
  <div class="spinner-overlay-content">
    <svg class="spinner spinner-lg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <circle class="spinner-track" cx="12" cy="12" r="10" fill="none" stroke-width="2"/>
      <circle class="spinner-head" cx="12" cy="12" r="10" fill="none" stroke-width="2"/>
    </svg>
    <span class="spinner-text">Uploading file...</span>
  </div>
</div>
```

#### Styling

**File**: `/web/styles/components/spinner.css`

```css
/* Base Spinner */
.spinner {
  animation: spinner-rotate 1s linear infinite;
}

@keyframes spinner-rotate {
  to {
    transform: rotate(360deg);
  }
}

.spinner-track {
  stroke: #ecf0f1;
  opacity: 0.3;
}

.spinner-head {
  stroke: #3498db;
  stroke-linecap: round;
  stroke-dasharray: 50;
  stroke-dashoffset: 0;
  animation: spinner-dash 1.5s ease-in-out infinite;
  transform-origin: center;
}

@keyframes spinner-dash {
  0% {
    stroke-dashoffset: 50;
  }
  50% {
    stroke-dashoffset: 12.5;
  }
  100% {
    stroke-dashoffset: 50;
  }
}

/* Sizes */
.spinner-sm {
  width: 16px;
  height: 16px;
}

.spinner-md {
  width: 24px;
  height: 24px;
}

.spinner-lg {
  width: 48px;
  height: 48px;
}

/* Page Spinner Container */
.spinner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 48px 24px;
}

.spinner-text {
  font-size: 14px;
  color: #7f8c8d;
}

/* Overlay Spinner */
.spinner-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000; /* Above everything */
}

.spinner-overlay-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 32px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Button Loading State */
.btn-loading {
  position: relative;
  color: transparent !important;
  pointer-events: none;
}

.btn-loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 16px;
  height: 16px;
  margin: -8px 0 0 -8px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spinner-rotate 0.6s linear infinite;
}

/* Specific button states */
.btn-primary.btn-loading::after {
  border-top-color: white;
}

.btn-secondary.btn-loading::after {
  border-top-color: #3498db;
}
```

#### JavaScript Utilities

**File**: `/web/static/js/loading.js`

```javascript
/**
 * Loading State Utilities
 * 
 * Usage:
 *   Loading.button(buttonElement, true) // Start loading
 *   Loading.button(buttonElement, false) // Stop loading
 *   Loading.page(true, 'Loading settings...') // Show page spinner
 *   Loading.overlay(true, 'Uploading file...') // Show overlay
 */

const Loading = {
  // Button loading state
  button(button, isLoading) {
    if (isLoading) {
      button.classList.add('btn-loading');
      button.disabled = true;
      button.setAttribute('aria-busy', 'true');
    } else {
      button.classList.remove('btn-loading');
      button.disabled = false;
      button.setAttribute('aria-busy', 'false');
    }
  },

  // Page spinner
  page(show, message = 'Loading...') {
    let container = document.getElementById('page-spinner');
    
    if (show) {
      if (!container) {
        container = document.createElement('div');
        container.id = 'page-spinner';
        container.className = 'spinner-container';
        container.setAttribute('role', 'status');
        container.setAttribute('aria-live', 'polite');
        container.innerHTML = `
          <svg class="spinner spinner-lg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <circle class="spinner-track" cx="12" cy="12" r="10" fill="none" stroke-width="2"/>
            <circle class="spinner-head" cx="12" cy="12" r="10" fill="none" stroke-width="2"/>
          </svg>
          <span class="spinner-text">${message}</span>
        `;
        document.body.appendChild(container);
      }
      container.style.display = 'flex';
    } else {
      if (container) {
        container.style.display = 'none';
      }
    }
  },

  // Overlay spinner (blocks interaction)
  overlay(show, message = 'Loading...') {
    let overlay = document.getElementById('loading-overlay');
    
    if (show) {
      if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'spinner-overlay';
        overlay.setAttribute('role', 'status');
        overlay.setAttribute('aria-live', 'polite');
        overlay.innerHTML = `
          <div class="spinner-overlay-content">
            <svg class="spinner spinner-lg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <circle class="spinner-track" cx="12" cy="12" r="10" fill="none" stroke-width="2"/>
              <circle class="spinner-head" cx="12" cy="12" r="10" fill="none" stroke-width="2"/>
            </svg>
            <span class="spinner-text">${message}</span>
          </div>
        `;
        document.body.appendChild(overlay);
      } else {
        overlay.querySelector('.spinner-text').textContent = message;
      }
      overlay.style.display = 'flex';
    } else {
      if (overlay) {
        overlay.style.display = 'none';
      }
    }
  }
};

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Loading;
}
```

#### Integration Examples

**Button Loading State**:
```javascript
// Save button in settings
const saveBtn = document.getElementById('save-settings');

saveBtn.addEventListener('click', async () => {
  Loading.button(saveBtn, true); // Start loading
  
  try {
    await saveSettings();
    Toast.success('Saved', 'Settings updated');
  } catch (error) {
    Toast.error('Error', error.message);
  } finally {
    Loading.button(saveBtn, false); // Stop loading
  }
});
```

**File Upload with Overlay**:
```javascript
async function uploadFile(file) {
  Loading.overlay(true, `Uploading ${file.name}...`);
  
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/upload', {
      method: 'POST',
      body: formData
    });
    
    if (response.ok) {
      Toast.success('Upload complete', `${file.name} uploaded`);
    } else {
      throw new Error('Upload failed');
    }
  } catch (error) {
    Toast.error('Upload failed', error.message);
  } finally {
    Loading.overlay(false);
  }
}
```

**Page Load Spinner**:
```javascript
// When loading settings page
document.addEventListener('DOMContentLoaded', async () => {
  Loading.page(true, 'Loading settings...');
  
  try {
    const settings = await fetchSettings();
    renderSettings(settings);
  } catch (error) {
    Toast.error('Load failed', 'Unable to load settings');
  } finally {
    Loading.page(false);
  }
});
```

### Accessibility Requirements

**ARIA Attributes**:
- `aria-busy="true"` on loading buttons
- `role="status"` on spinner containers
- `aria-live="polite"` on spinner containers
- `aria-hidden="true"` on decorative SVG

**Screen Reader Support**:
- Loading message announced: "Loading settings..."
- Button state announced: "Save button, busy"
- Completion announced via toast

**Keyboard Navigation**:
- Buttons disabled while loading (prevent double-click)
- Overlay blocks all interaction (focus trapped if needed)

**Color Contrast**:
- Spinner color (#3498db): 3:1 against background ✅
- Loading text (#7f8c8d): 4.5:1 ✅

### Acceptance Criteria

- [ ] Spinner component created
- [ ] CSS styling complete
- [ ] JavaScript utilities created
- [ ] Button loading states work (text hidden, spinner visible)
- [ ] Page spinner shows/hides
- [ ] Overlay spinner blocks interaction
- [ ] Integrated in: Settings save, file upload, standup submit
- [ ] Keyboard accessible (buttons disabled while loading)
- [ ] Screen reader announces loading state
- [ ] Animations smooth (60fps)

### Testing

**Manual Tests**:
1. Click save button → Spinner appears, button disabled
2. Upload file → Overlay appears with progress message
3. Load settings page → Page spinner shows until loaded
4. Tab to loading button → Cannot focus (disabled)
5. Test with screen reader → "Busy" state announced
6. Multiple rapid clicks → Only one request sent

**Files to Create/Modify**:
- Create: `/web/templates/components/spinner.html`
- Create: `/web/styles/components/spinner.css`
- Create: `/web/static/js/loading.js`
- Modify: All pages with async actions (settings, standup, upload)

---

## Feature 3: Empty States (G30)

**Score**: 288 (Impact: 6, Frequency: 8, Effort: 7)  
**Effort**: 1 day  
**Priority**: MEDIUM - Polish for new users

### Problem Statement

When no content exists, pages show:
- Blank white space (is it broken?)
- Generic "No items" text (what should I do?)
- No guidance on next steps

**Impact**: New users confused, unsure how to proceed.

### Specification

**Create**: Empty state component with guidance for common scenarios

#### Component Template

**File**: `/web/templates/components/empty-state.html`

```html
<!-- Empty State Component -->
<div class="empty-state" role="status">
  <div class="empty-state-icon">
    <!-- Icon slot (filled by usage) -->
    {{ icon | safe }}
  </div>
  
  <h3 class="empty-state-title">{{ title }}</h3>
  
  <p class="empty-state-message">{{ message }}</p>
  
  {% if cta_text %}
  <a href="{{ cta_url }}" class="btn btn-primary empty-state-cta">
    {{ cta_text }}
  </a>
  {% endif %}
  
  {% if help_link %}
  <a href="{{ help_link }}" class="empty-state-help">
    Learn more →
  </a>
  {% endif %}
</div>
```

#### Styling

**File**: `/web/styles/components/empty-state.css`

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 64px 24px;
  max-width: 480px;
  margin: 0 auto;
}

.empty-state-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 24px;
  color: #bdc3c7;
}

.empty-state-icon svg {
  width: 100%;
  height: 100%;
}

.empty-state-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 12px 0;
}

.empty-state-message {
  font-size: 16px;
  color: #7f8c8d;
  line-height: 1.5;
  margin: 0 0 24px 0;
}

.empty-state-cta {
  margin-bottom: 16px;
}

.empty-state-help {
  font-size: 14px;
  color: #3498db;
  text-decoration: none;
  transition: color 0.2s;
}

.empty-state-help:hover {
  color: #2980b9;
  text-decoration: underline;
}

@media (max-width: 768px) {
  .empty-state {
    padding: 48px 16px;
  }
  
  .empty-state-icon {
    width: 64px;
    height: 64px;
  }
}
```

#### Usage Examples

**Standup History (No Standups Yet)**:

```jinja2
{% if standups|length == 0 %}
  {% set icon %}
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
    </svg>
  {% endset %}
  
  {% include 'components/empty-state.html' with context only %}
  {% set title = "No standups yet" %}
  {% set message = "Create your first standup to track your daily progress and share updates with your team" %}
  {% set cta_text = "Create Standup" %}
  {% set cta_url = "/standup" %}
{% endif %}
```

**File Browser (No Files)**:

```jinja2
{% if files|length == 0 %}
  {% set icon %}
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
    </svg>
  {% endset %}
  
  {% set title = "No documents yet" %}
  {% set message = "Upload documents to your knowledge base or generate new content with Piper" %}
  {% set cta_text = "Upload Document" %}
  {% set cta_url = "#upload-modal" %}
  {% set help_link = "/docs/files" %}
{% endif %}
```

**Conversation History (No Conversations)**:

```jinja2
{% if conversations|length == 0 %}
  {% set icon %}
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
    </svg>
  {% endset %}
  
  {% set title = "Start a conversation" %}
  {% set message = "Ask Piper anything! Get help with product management tasks, create documents, or analyze data" %}
  {% set cta_text = "New Chat" %}
  {% set cta_url = "/" %}
{% endif %}
```

**Learning Patterns (No Patterns)**:

```jinja2
{% if patterns|length == 0 %}
  {% set icon %}
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
    </svg>
  {% endset %}
  
  {% set title = "No patterns discovered yet" %}
  {% set message = "As you use Piper, we'll learn your preferences and suggest patterns to make you more productive" %}
  {% set help_link = "/docs/learning" %}
{% endif %}
```

### Accessibility Requirements

**ARIA Attributes**:
- `role="status"` on container
- Proper heading hierarchy (h3 for title)
- Actionable CTA button (not just text)

**Screen Reader Support**:
- Title and message read together
- CTA button announced with purpose
- Help link announced separately

**Color Contrast**:
- Title (#2c3e50): 12.6:1 ✅
- Message (#7f8c8d): 4.5:1 ✅
- Icon (#bdc3c7): 3:1 (decorative, acceptable) ✅

### Acceptance Criteria

- [ ] Empty state component created
- [ ] CSS styling complete
- [ ] Integrated in 4+ locations:
  - [ ] Standup history (no standups)
  - [ ] File browser (no files)
  - [ ] Conversation history (no conversations)
  - [ ] Learning dashboard (no patterns)
- [ ] Icons appropriate for each context
- [ ] CTAs lead to correct actions
- [ ] Help links (where applicable)
- [ ] Keyboard accessible
- [ ] Screen reader friendly
- [ ] Mobile responsive

### Testing

**Manual Tests**:
1. New user → See empty states everywhere
2. Each empty state has helpful message
3. CTA button works (opens modal, navigates, etc.)
4. Help link works (if present)
5. Tab through elements → Logical focus order
6. Test with screen reader → Content clear

**Files to Create/Modify**:
- Create: `/web/templates/components/empty-state.html`
- Create: `/web/styles/components/empty-state.css`
- Modify: `/web/templates/standup-history.html` (if exists)
- Modify: `/web/templates/files.html` (if exists)
- Modify: `/web/templates/conversations.html` (if exists)
- Modify: `/web/templates/learning-dashboard.html`

---

## Week 2 Features (Stretch Goals)

### Feature 4: Contextual Help Links (G5)

**Score**: 360 (Impact: 6, Frequency: 10, Effort: 7)  
**Effort**: 1-2 days  
**Priority**: MEDIUM - Reduces support burden

**Quick Spec**:
- Add `?` help icon next to key features
- Tooltip on hover with brief explanation
- Link to full docs if available
- Example: "Personality settings" + ? → "Customize how Piper responds to you. Learn more →"

**Files to Create**:
- `/web/templates/components/help-tooltip.html`
- `/web/styles/components/tooltip.css`
- `/web/static/js/tooltip.js`

**Integration Points**:
- Personality settings page
- Learning dashboard
- Standup page
- File upload

**ARIA Requirements**:
- `aria-describedby` linking button to tooltip
- `role="tooltip"` on tooltip element
- Keyboard accessible (focus shows tooltip)

---

### Feature 5: Keyboard Shortcuts (G61)

**Score**: 252 (Impact: 7, Frequency: 6, Effort: 8)  
**Effort**: 1-2 days  
**Priority**: LOW - Power user feature

**Quick Spec**:
- `/` → Focus search (if exists)
- `g h` → Go to home
- `g s` → Go to standup
- `g f` → Go to files
- `g l` → Go to learning
- `?` → Show keyboard shortcuts help

**Files to Create**:
- `/web/static/js/keyboard-shortcuts.js`
- `/web/templates/modals/shortcuts-help.html`
- `/web/styles/components/shortcuts.css`

**ARIA Requirements**:
- Modal has `role="dialog"`
- Shortcuts list has `role="list"`
- Keyboard trap in modal (Escape closes)

---

### Feature 6: Form Validation (G43)

**Score**: 240 (Impact: 6, Frequency: 8, Effort: 5)  
**Effort**: 1-2 days  
**Priority**: MEDIUM - Prevents errors

**Quick Spec**:
- Real-time validation on blur
- Clear error messages inline
- Submit button disabled if invalid
- Visual indicators (red border, error icon)

**Files to Create**:
- `/web/static/js/form-validation.js`
- `/web/styles/components/forms.css`

**ARIA Requirements**:
- `aria-invalid="true"` on invalid fields
- `aria-describedby` linking to error message
- `role="alert"` on error messages

---

### Feature 7: Session Timeout Handling (G52)

**Score**: 315 (Impact: 9, Frequency: 7, Effort: 5)  
**Effort**: 2 days  
**Priority**: MEDIUM - Data loss prevention

**Quick Spec**:
- Detect session expiry (401 response)
- Show modal: "Session expired. Log in again?"
- Option to refresh or navigate to login
- Auto-save draft before redirect

**Files to Create**:
- `/web/static/js/session-monitor.js`
- `/web/templates/modals/session-expired.html`

**ARIA Requirements**:
- Modal has `role="alertdialog"`
- Focus trapped in modal
- Message announced immediately

---

## What NOT to Work On (Conflicts with Strategic Planning)

### Avoid These Areas

**Learning System UI** (Xian + Chief Architect working on this):
- Learning dashboard redesign
- Pattern suggestion UI changes
- Learning preferences advanced features

**MCP/Skills Integration** (Architectural work in progress):
- Skills layer implementation
- MCP server connections
- Tool federation

**Design System Migration** (Needs strategic synthesis first):
- Converting to design tokens
- Theme toggle implementation
- Comprehensive visual overhaul

**Cross-Channel Features** (Requires architectural decisions):
- Slack/CLI integration
- Unified conversation history across channels
- Cross-channel memory sync

**Document Domain Model** (Strategic decision pending):
- Canonical PM templates (PRD, roadmap, etc.)
- Document type taxonomy
- Workflow automation

**Database Schema Changes** (Coordinate with Chief Architect):
- New tables or major migrations
- Persistence layer modifications

### If Unsure, Ask

**Before starting work on anything not in this prompt**, check with PM (Xian) to confirm it won't conflict with ongoing strategic work.

---

## Development Workflow

### Step 1: Read CLAUDE.md FIRST

**CRITICAL**: Before writing ANY code:
1. Locate and read `/path/to/piper-morgan/CLAUDE.md`
2. Understand WCAG 2.2 AA requirements
3. Note accessibility patterns
4. Use these as baseline for all work

**If CLAUDE.md is not in your sandbox**, ask PM for the path or key requirements.

### Step 2: Work Sequentially

**Week 1 Order**:
1. Toast Notifications (foundation for other features)
2. Loading States (complements toasts)
3. Empty States (polish existing pages)

**Don't parallelize** - each builds on previous:
- Toasts needed for loading completion feedback
- Loading states needed before empty states make sense
- Empty states reference toasts/loading patterns

### Step 3: Test Accessibility Thoroughly

**After each feature**:
- [ ] Keyboard only test (unplug mouse)
- [ ] Tab through all interactive elements
- [ ] Enter/Escape trigger expected actions
- [ ] ARIA labels present (inspect element)
- [ ] Color contrast validated (browser DevTools)
- [ ] Screen reader test (if available)

**Tools**:
- Chrome DevTools → Lighthouse → Accessibility audit
- axe DevTools extension
- WAVE extension
- Browser developer tools → Accessibility panel

### Step 4: Document Progress

**Create**: `/docs/polish-sprint-progress.md`

Track:
```markdown
# Polish Sprint Progress

## Feature 1: Toast Notifications (G23)
- Status: ✅ Complete
- Time: 1.5 days
- Files Created: 3
- Issues: None
- Screenshots: [link]
- Accessibility: ✅ Passed keyboard + screen reader

## Feature 2: Loading States (G29)
- Status: 🔄 In Progress
- Time: 0.5 days so far
- Files Created: 2 of 3
- Issues: Spinner animation choppy on Safari (investigating)
- Screenshots: [link]

[etc.]
```

### Step 5: Integration Testing

**After all Week 1 features complete**:
- [ ] Test entire user journey (onboarding → standup → settings)
- [ ] Verify toasts + loading + empty states work together
- [ ] No console errors
- [ ] No visual bugs
- [ ] Regression test (Quick Wins still work)

---

## Success Criteria

### Week 1 Complete When:
- [ ] Toast notifications work on all major actions
- [ ] Loading states visible for async operations
- [ ] Empty states guide users when no content
- [ ] All features keyboard accessible
- [ ] All features work with screen reader
- [ ] Zero console errors
- [ ] Documentation updated (progress.md)

### Week 2 Complete When (If Attempted):
- [ ] Help tooltips on 5+ key features
- [ ] Keyboard shortcuts working (minimum: g h, g s, g f)
- [ ] Form validation on settings pages
- [ ] Session timeout handled gracefully
- [ ] All accessibility requirements met
- [ ] Integration testing passed

### Definition of Done (Per Feature):
- [ ] Code implemented following CLAUDE.md guidelines
- [ ] Accessibility validated (keyboard + screen reader)
- [ ] Responsive on mobile (320px - 1920px)
- [ ] Cross-browser tested (Chrome + Firefox minimum)
- [ ] Screenshots captured (desktop + mobile)
- [ ] Progress documented in `polish-sprint-progress.md`
- [ ] No regression (existing features still work)
- [ ] Integrated in 3+ locations (where applicable)

---

## Common Patterns to Follow

### Component Structure
```
web/
├── templates/
│   └── components/
│       ├── toast.html
│       ├── spinner.html
│       └── empty-state.html
├── styles/
│   └── components/
│       ├── toast.css
│       ├── spinner.css
│       └── empty-state.css
└── static/
    └── js/
        ├── toast.js
        ├── loading.js
        └── validation.js (if implementing)
```

### Accessibility Checklist (Every Feature)
- [ ] Semantic HTML (not `<div>` for everything)
- [ ] ARIA labels on dynamic content
- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] Focus indicators visible (2px outline)
- [ ] Color contrast validated (4.5:1, 3:1)
- [ ] Screen reader announcements
- [ ] Status updates via `aria-live`

### Testing Checklist (Every Feature)
- [ ] Visual: Component appears correctly
- [ ] Functional: All interactions work
- [ ] Keyboard: Tab/Enter/Escape navigation
- [ ] Screen Reader: Proper announcements
- [ ] Mobile: Responsive (320px+)
- [ ] Cross-browser: Chrome, Firefox
- [ ] Integration: Works with other features

---

## Questions & Escalation

### If You Get Stuck

**Check CLAUDE.md first**:
- Accessibility requirement unclear? → Check CLAUDE.md
- Color contrast requirement? → Check CLAUDE.md
- ARIA pattern needed? → Check CLAUDE.md

**Check existing code**:
- How do buttons work? → Look at existing buttons
- How do modals work? → Look at existing modals
- How does styling work? → Look at existing CSS

**Escalate to PM if**:
- CLAUDE.md not accessible or unclear
- Specification contradicts CLAUDE.md
- Architectural decision needed
- Blocker preventing progress
- Unsure if work conflicts with strategic planning

### Don't Escalate For:
- Implementing patterns (follow examples in this prompt)
- Writing CSS (follow component examples)
- Testing manually (follow test scenarios)
- ARIA attributes (check CLAUDE.md)

---

## Timeline & Reporting

### Week 1 (Priority Features)
- Day 1: Toast Notifications (setup + core implementation)
- Day 2: Toast Notifications (integration + testing)
- Day 3: Loading States (implementation + integration)
- Day 4: Empty States (all variations)
- Day 5: Testing, polish, documentation

### Week 2 (Stretch Goals - If Time)
- Day 1-2: Contextual Help Links
- Day 3-4: Keyboard Shortcuts
- Day 5: Integration testing, final polish

### Daily Updates (Optional but Helpful):
- What did you complete?
- What are you working on?
- Any blockers or questions?
- Screenshots of progress

---

## Final Reminders

### Critical Success Factors

1. **Read CLAUDE.md first** - accessibility is non-negotiable
2. **Follow specifications exactly** - don't improvise patterns
3. **Test accessibility** - keyboard and screen reader
4. **Work sequentially** - toasts → loading → empty states
5. **Document progress** - screenshots and notes
6. **Ask questions early** - don't guess on accessibility

### What Good Looks Like

**After Week 1**:
- User saves settings → Toast appears: "Settings saved" → Confident
- User uploads file → Loading spinner → Progress clear → Toast confirms → Satisfied
- New user lands on empty page → Clear message + CTA → Knows what to do → Guided

**Overall Impact**: Experience transforms from "functional" to "professional"

### You Have Access To

- ✅ This comprehensive specification
- ✅ CLAUDE.md (accessibility requirements)
- ✅ Full codebase (for patterns and integration)
- ✅ Sandbox environment (safe to experiment)

### You Are Expected To

- Read CLAUDE.md before starting
- Follow specifications precisely
- Test thoroughly (manual + accessibility)
- Document progress
- Ask questions when stuck
- Deliver production-quality code

### You Will Succeed By

- Reading docs before coding
- Following existing patterns
- Testing before marking complete
- Maintaining focus on accessibility
- Communicating progress clearly

---

**Let's transform Piper from functional to polished!** ✨

**Start with Toast Notifications (G23) - it's the foundation for user feedback throughout the app.**

Good luck! 💪
