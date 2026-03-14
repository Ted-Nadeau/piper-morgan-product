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
 * Restored from commit 00e0b881 during #375 rewiring (was deleted in cleanup)
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
      credentials: "include",
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
        `Preference applied: ${result.dimension || "Your profile updated"}!`,
        "success"
      );

      // Log to analytics
      logPreferenceEvent("preference_accepted", {
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
    logPreferenceEvent("preference_accept_failed", {
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
      credentials: "include",
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

      // Log event
      logPreferenceEvent("preference_dismissed", {
        hint_id: hintId,
        session_id: sessionId,
      });
    } else {
      throw new Error(result.message || "Failed to dismiss suggestion");
    }
  } catch (error) {
    console.error("Error dismissing preference:", error);
    // Even if request fails, remove the suggestion from UI
    suggestionElement.classList.add("removing");
    setTimeout(() => {
      suggestionElement.remove();
    }, 300);

    // Log error
    logPreferenceEvent("preference_dismiss_failed", {
      hint_id: hintId,
      error: error.message,
      session_id: sessionId,
    });
  }
}

/**
 * Render preference suggestions into the chat after a bot response
 *
 * Called from chat.js when the intent API returns preferences
 * @param {Object} preferences - The preferences object from API response
 * @param {HTMLElement} afterElement - The bot message element to insert after
 */
function renderPreferenceSuggestions(preferences, afterElement) {
  if (!preferences || !preferences.has_suggestions || !preferences.hints) {
    return;
  }

  const hints = preferences.hints;
  if (!Array.isArray(hints) || hints.length === 0) {
    return;
  }

  hints.forEach((hint) => {
    const suggestionEl = createSuggestionElement(hint);
    if (afterElement && afterElement.parentNode) {
      afterElement.parentNode.insertBefore(
        suggestionEl,
        afterElement.nextSibling
      );
    }
  });
}

/**
 * Create a preference suggestion DOM element from hint data
 *
 * @param {Object} hint - Hint object with id, dimension, explanation, confidence_score, etc.
 * @returns {HTMLElement} The suggestion element
 */
function createSuggestionElement(hint) {
  const wrapper = document.createElement("div");
  wrapper.className = "preference-suggestion";
  wrapper.id = `pref-hint-${hint.id}`;
  wrapper.setAttribute("data-hint-id", hint.id);

  const dimension = (hint.dimension || "").replace(/_/g, " ");
  const dimensionTitle =
    dimension.charAt(0).toUpperCase() + dimension.slice(1);
  const confidencePct = Math.round((hint.confidence_score || 0) * 100);
  const detectionMethod = (hint.detection_method || "conversation analysis")
    .replace(/_/g, " ")
    .toLowerCase();

  wrapper.innerHTML = `
    <div class="suggestion-container">
      <div class="suggestion-header">
        <div class="suggestion-icon">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10 2C6.13 2 3 5.13 3 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.87-3.13-7-7-7zm0 14c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1z" fill="currentColor"/>
          </svg>
        </div>
        <div class="suggestion-title-group">
          <h4 class="suggestion-title">We noticed something</h4>
          <p class="suggestion-dimension">${dimensionTitle}</p>
        </div>
      </div>
      <div class="suggestion-content">
        <p class="suggestion-text">${hint.explanation || "We detected a preference in your conversation style."}</p>
      </div>
      <div class="suggestion-meta">
        <div class="confidence-badge">
          <span class="confidence-label">Confidence:</span>
          <span class="confidence-value">${confidencePct}%</span>
        </div>
        <div class="confidence-bar">
          <div class="confidence-fill" style="width: ${confidencePct}%"></div>
        </div>
      </div>
      <div class="suggestion-actions">
        <button class="btn btn-accept" onclick="acceptPreference('${hint.id}', event)"
                title="Apply this preference to your profile"
                aria-label="Apply preference: ${dimensionTitle}">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M13.78 4.22a.75.75 0 010 1.06l-7.5 7.5a.75.75 0 01-1.06 0l-3.5-3.5a.75.75 0 011.06-1.06L5.5 10.94l6.72-6.72a.75.75 0 011.06 0z"/>
          </svg>
          Apply
        </button>
        <button class="btn btn-dismiss" onclick="dismissPreference('${hint.id}', event)"
                title="Dismiss this suggestion"
                aria-label="Dismiss preference suggestion">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M3.72 3.72a.75.75 0 011.06 0L8 6.94l3.22-3.22a.75.75 0 111.06 1.06L9.06 8l3.22 3.22a.75.75 0 11-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 11-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 010-1.06z"/>
          </svg>
          Dismiss
        </button>
      </div>
      <div class="suggestion-source">
        <small>Based on ${detectionMethod}</small>
      </div>
    </div>
  `;

  return wrapper;
}

/**
 * Get current session ID from page context
 */
function getCurrentSessionId() {
  if (window.sessionId) {
    return window.sessionId;
  }
  const sessionId = document.body.getAttribute("data-session-id");
  if (sessionId) {
    return sessionId;
  }
  let storedSessionId = localStorage.getItem("session_id");
  if (storedSessionId) {
    return storedSessionId;
  }
  const tempSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  localStorage.setItem("session_id", tempSessionId);
  return tempSessionId;
}

/**
 * Log preference event (uses toast.js showToast if available)
 */
function logPreferenceEvent(eventName, data) {
  try {
    if (window.DEBUG_MODE) {
      console.debug(`Preference event: ${eventName}`, data);
    }
  } catch (error) {
    console.error("Error logging preference event:", error);
  }
}

// Add CSS for preference suggestions and animations
(function addPreferenceStyles() {
  if (document.getElementById("preference-styles")) {
    return;
  }

  const style = document.createElement("style");
  style.id = "preference-styles";
  style.textContent = `
    .preference-suggestion {
      margin: 16px 0;
      animation: prefSlideIn 0.3s ease-out;
    }

    @keyframes prefSlideIn {
      from { opacity: 0; transform: translateY(-8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .suggestion-container {
      border-left: 4px solid #667eea;
      background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
      border-radius: 8px;
      padding: 14px 16px;
      box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
      transition: all 0.2s ease;
    }

    .preference-suggestion:hover .suggestion-container {
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }

    .suggestion-header {
      display: flex; align-items: flex-start; gap: 12px; margin-bottom: 12px;
    }

    .suggestion-icon {
      display: flex; align-items: center; justify-content: center;
      width: 36px; height: 36px; background: white; border-radius: 50%;
      color: #667eea; flex-shrink: 0;
      box-shadow: 0 2px 4px rgba(102, 126, 234, 0.1);
    }

    .suggestion-title-group { flex: 1; min-width: 0; }

    .suggestion-title {
      margin: 0 0 4px 0; font-size: 14px; font-weight: 600;
      color: #1f2937; line-height: 1.4;
    }

    .suggestion-dimension {
      margin: 0; font-size: 12px; color: #667eea; font-weight: 500;
      text-transform: uppercase; letter-spacing: 0.5px;
    }

    .suggestion-content { margin-bottom: 12px; }

    .suggestion-text {
      margin: 0; font-size: 13px; color: #374151; line-height: 1.5;
    }

    .suggestion-meta { margin-bottom: 12px; }

    .confidence-badge {
      display: flex; align-items: center; gap: 6px; margin-bottom: 6px;
    }

    .confidence-label { font-size: 12px; color: #6b7280; font-weight: 500; }
    .confidence-value { font-size: 12px; color: #667eea; font-weight: 600; }

    .confidence-bar {
      height: 6px; background: #e5e7eb; border-radius: 3px;
      overflow: hidden; position: relative;
    }

    .confidence-fill {
      height: 100%; background: linear-gradient(90deg, #667eea, #764ba2);
      border-radius: 3px; transition: width 0.3s ease;
    }

    .suggestion-actions { display: flex; gap: 8px; margin-bottom: 8px; }

    .suggestion-actions .btn {
      padding: 8px 14px; border: 1px solid #d1d5db; border-radius: 6px;
      font-size: 13px; font-weight: 500; cursor: pointer;
      transition: all 0.2s ease; display: flex; align-items: center;
      gap: 6px; white-space: nowrap; line-height: 1; flex: 1;
    }

    .suggestion-actions .btn:hover { transform: translateY(-2px); }
    .suggestion-actions .btn:active { transform: translateY(0); }

    .suggestion-actions .btn-accept {
      background: #667eea; color: white; border-color: #667eea;
    }
    .suggestion-actions .btn-accept:hover {
      background: #5568d3; border-color: #5568d3;
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .suggestion-actions .btn-accept:disabled,
    .suggestion-actions .btn-dismiss:disabled {
      opacity: 0.6; cursor: not-allowed; transform: none;
    }

    .suggestion-actions .btn-dismiss {
      background: white; color: #6b7280; border-color: #d1d5db;
    }
    .suggestion-actions .btn-dismiss:hover {
      background: #f9fafb; color: #374151; border-color: #bfdbfe;
    }

    .suggestion-source {
      padding-top: 8px; border-top: 1px solid rgba(102, 126, 234, 0.1);
      color: #9ca3af; font-size: 11px; text-align: center;
    }

    .preference-suggestion.removing {
      animation: prefFadeOut 0.3s ease-out forwards;
    }

    @keyframes prefFadeOut {
      from { opacity: 1; transform: translateY(0); }
      to { opacity: 0; transform: translateY(-8px); }
    }

    @media (max-width: 600px) {
      .suggestion-container { padding: 12px 14px; }
      .suggestion-actions { flex-direction: column; }
      .suggestion-actions .btn { width: 100%; justify-content: center; }
    }

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
      .suggestion-container {
        background: linear-gradient(135deg, #1e1e2e 0%, #252540 100%);
        border-left-color: #818cf8;
      }
      .suggestion-title { color: #e5e7eb; }
      .suggestion-text { color: #d1d5db; }
      .suggestion-icon { background: #374151; color: #818cf8; }
      .suggestion-dimension { color: #818cf8; }
      .confidence-bar { background: #374151; }
      .suggestion-actions .btn-dismiss {
        background: #374151; color: #d1d5db; border-color: #4b5563;
      }
      .suggestion-source { border-top-color: rgba(129, 140, 248, 0.15); }
    }
  `;
  document.head.appendChild(style);
})();
