/**
 * Preference Suggestion Handler
 *
 * Handles user interaction with preference suggestions:
 * - Accept preference (Apply button)
 * - Dismiss preference (Dismiss button)
 * - Show/hide feedback messages
 * - Update UI after action
 *
 * Issue #248: CONV-LEARN-PREF
 */

/**
 * Accept a preference suggestion
 *
 * Called when user clicks "Apply" button on preference suggestion
 * @param {string} hintId - The hint ID to accept
 * @param {Event} event - Click event (prevents default)
 */
async function acceptPreference(hintId, event) {
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }

  const suggestionElement = document.getElementById(`pref-hint-${hintId}`);
  if (!suggestionElement) {
    console.warn(`Preference suggestion element not found: ${hintId}`);
    return;
  }

  // Get session ID from page context
  const sessionId = getCurrentSessionId();

  // Disable buttons during request
  const buttons = suggestionElement.querySelectorAll("button");
  buttons.forEach((btn) => (btn.disabled = true));

  try {
    const response = await fetch(`/api/v1/preferences/hints/${hintId}/accept`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        hint_id: hintId,
        session_id: sessionId,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to apply preference");
    }

    const result = await response.json();

    if (result.success) {
      // Add removal animation
      suggestionElement.classList.add("removing");

      // Remove element after animation
      setTimeout(() => {
        suggestionElement.remove();
      }, 300);

      // Show success toast
      showToast(
        `Preference applied: ${result.dimension || "Your profile updated"}! 🎉`,
        "success"
      );

      // Log to analytics
      logEvent("preference_accepted", {
        hint_id: hintId,
        dimension: result.dimension,
        session_id: sessionId,
      });
    } else {
      throw new Error(result.message || "Failed to apply preference");
    }
  } catch (error) {
    console.error("Error accepting preference:", error);
    showToast(
      `Error: ${error.message || "Failed to apply preference"}`,
      "error"
    );

    // Re-enable buttons
    buttons.forEach((btn) => (btn.disabled = false));

    // Log error
    logEvent("preference_accept_failed", {
      hint_id: hintId,
      error: error.message,
      session_id: sessionId,
    });
  }
}

/**
 * Dismiss a preference suggestion
 *
 * Called when user clicks "Dismiss" button on preference suggestion
 * @param {string} hintId - The hint ID to dismiss
 * @param {Event} event - Click event (prevents default)
 */
async function dismissPreference(hintId, event) {
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }

  const suggestionElement = document.getElementById(`pref-hint-${hintId}`);
  if (!suggestionElement) {
    console.warn(`Preference suggestion element not found: ${hintId}`);
    return;
  }

  // Get session ID from page context
  const sessionId = getCurrentSessionId();

  // Disable buttons during request
  const buttons = suggestionElement.querySelectorAll("button");
  buttons.forEach((btn) => (btn.disabled = true));

  try {
    const response = await fetch(`/api/v1/preferences/hints/${hintId}/dismiss`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        hint_id: hintId,
        session_id: sessionId,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to dismiss suggestion");
    }

    const result = await response.json();

    if (result.success) {
      // Add removal animation
      suggestionElement.classList.add("removing");

      // Remove element after animation
      setTimeout(() => {
        suggestionElement.remove();
      }, 300);

      // Optional: Show subtle feedback
      logEvent("preference_dismissed", {
        hint_id: hintId,
        session_id: sessionId,
      });
    } else {
      throw new Error(result.message || "Failed to dismiss suggestion");
    }
  } catch (error) {
    console.error("Error dismissing preference:", error);
    // Even if request fails, remove the suggestion from UI
    // (user can see their preference was recorded)
    suggestionElement.classList.add("removing");
    setTimeout(() => {
      suggestionElement.remove();
    }, 300);

    // Log error
    logEvent("preference_dismiss_failed", {
      hint_id: hintId,
      error: error.message,
      session_id: sessionId,
    });
  }
}

/**
 * Get current session ID from page context
 *
 * Tries to find session ID from:
 * 1. window.sessionId (set globally)
 * 2. data-session-id attribute on body
 * 3. localStorage session
 * 4. Generate new temporary ID
 *
 * @returns {string} Session ID
 */
function getCurrentSessionId() {
  // Check window context
  if (window.sessionId) {
    return window.sessionId;
  }

  // Check DOM attribute
  const sessionId = document.body.getAttribute("data-session-id");
  if (sessionId) {
    return sessionId;
  }

  // Check localStorage
  let storedSessionId = localStorage.getItem("session_id");
  if (storedSessionId) {
    return storedSessionId;
  }

  // Generate temporary session ID
  const tempSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  localStorage.setItem("session_id", tempSessionId);
  return tempSessionId;
}

/**
 * Show toast notification
 *
 * Displays a brief notification message to user
 * @param {string} message - Toast message
 * @param {string} type - Type: 'success', 'error', 'info' (default: 'info')
 * @param {number} duration - Duration in ms (default: 3000)
 */
function showToast(message, type = "info", duration = 3000) {
  // Check if toast container exists
  let toastContainer = document.getElementById("toast-container");
  if (!toastContainer) {
    toastContainer = document.createElement("div");
    toastContainer.id = "toast-container";
    toastContainer.style.cssText =
      "position: fixed; top: 20px; right: 20px; z-index: 9999;";
    document.body.appendChild(toastContainer);
  }

  // Create toast element
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.style.cssText = `
    background: ${getToastColor(type)};
    color: white;
    padding: 12px 16px;
    border-radius: 6px;
    margin-bottom: 8px;
    font-size: 14px;
    animation: slideInRight 0.3s ease-out;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    max-width: 400px;
    word-wrap: break-word;
  `;

  toast.textContent = message;
  toastContainer.appendChild(toast);

  // Auto-remove after duration
  setTimeout(() => {
    toast.style.animation = "slideOutRight 0.3s ease-out forwards";
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, duration);
}

/**
 * Get color for toast type
 *
 * @param {string} type - Toast type
 * @returns {string} Color value
 */
function getToastColor(type) {
  const colors = {
    success: "#10b981", // Green
    error: "#ef4444", // Red
    info: "#3b82f6", // Blue
    warning: "#f59e0b", // Amber
  };
  return colors[type] || colors.info;
}

/**
 * Log event to analytics
 *
 * Sends event data to analytics endpoint for tracking
 * @param {string} eventName - Name of the event
 * @param {Object} data - Event data
 */
function logEvent(eventName, data = {}) {
  try {
    // If analytics endpoint exists, send data
    if (window.analyticsEndpoint) {
      navigator.sendBeacon(window.analyticsEndpoint, JSON.stringify({
        event: eventName,
        timestamp: new Date().toISOString(),
        ...data,
      }));
    }

    // Also log to console in development
    if (window.DEBUG_MODE) {
      console.debug(`Event: ${eventName}`, data);
    }
  } catch (error) {
    console.error("Error logging event:", error);
  }
}

// Add CSS animations if not already present
(function addAnimationStyles() {
  if (document.getElementById("preference-animations")) {
    return; // Already added
  }

  const style = document.createElement("style");
  style.id = "preference-animations";
  style.textContent = `
    @keyframes slideInRight {
      from {
        opacity: 0;
        transform: translateX(20px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }

    @keyframes slideOutRight {
      from {
        opacity: 1;
        transform: translateX(0);
      }
      to {
        opacity: 0;
        transform: translateX(20px);
      }
    }
  `;
  document.head.appendChild(style);
})();

// Export functions for use in other scripts
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    acceptPreference,
    dismissPreference,
    getCurrentSessionId,
    showToast,
    logEvent,
  };
}
