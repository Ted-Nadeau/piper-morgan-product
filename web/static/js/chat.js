// Chat Widget - Modular chat functionality
(function() {
  'use strict';

  const API_BASE_URL = window.API_BASE_URL || "";
  const chatWindow = document.getElementById("chat-window");
  let sessionId = null;

  // Storage keys for session persistence
  const STORAGE_KEYS = {
    SESSION_ID: 'piper_chat_session_id',
    CHAT_HISTORY: 'piper_chat_history',
    WIDGET_STATE: 'piper_chat_widget_expanded'
  };

  // Check if localStorage is available (graceful degradation for private browsing)
  let storageAvailable = false;
  try {
    const testKey = '__storage_test__';
    localStorage.setItem(testKey, testKey);
    localStorage.removeItem(testKey);
    storageAvailable = true;
  } catch (e) {
    console.warn('localStorage not available, session persistence disabled');
  }

  /**
   * Toggle chat widget expanded/collapsed state
   * Updates widget container class and manages focus/icon
   * Persists state to localStorage for cross-page consistency
   */
  function toggleChatWidget() {
    const container = document.querySelector('.chat-widget-container');
    if (container) {
      container.classList.toggle('expanded');
      const isExpanded = container.classList.contains('expanded');

      // Persist expanded state
      if (storageAvailable) {
        try {
          localStorage.setItem(STORAGE_KEYS.WIDGET_STATE, isExpanded ? 'true' : 'false');
        } catch (e) {
          // Ignore storage errors
        }
      }

      // Update toggle button icon when expanded
      const toggle = container.querySelector('.chat-widget-toggle');
      if (toggle) {
        toggle.innerHTML = isExpanded ? '✕' : '💬';
      }

      // Focus input when expanded for better UX
      if (isExpanded) {
        const input = container.querySelector('.chat-input');
        if (input) {
          // Use setTimeout to ensure focus after DOM update
          setTimeout(() => input.focus(), 50);
        }
      }
    }
  }

  // Make toggle globally available for onclick handlers
  window.toggleChatWidget = toggleChatWidget;

  /**
   * Generate a fallback session ID for browsers without crypto API
   */
  function generateSessionId() {
    return 'session-' + Math.random().toString(36).substr(2, 9) +
           '-' + Date.now().toString(36);
  }

  /**
   * Get or create a persistent session ID
   * Stored in localStorage for cross-page persistence
   */
  function getOrCreateSessionId() {
    if (storageAvailable) {
      try {
        const storedId = localStorage.getItem(STORAGE_KEYS.SESSION_ID);
        if (storedId) {
          return storedId;
        }
      } catch (e) {
        // Ignore storage errors
      }
    }

    // Create new session ID
    const newId = crypto.randomUUID ? crypto.randomUUID() : generateSessionId();

    // Persist if possible
    if (storageAvailable) {
      try {
        localStorage.setItem(STORAGE_KEYS.SESSION_ID, newId);
      } catch (e) {
        // Ignore storage errors
      }
    }

    return newId;
  }

  // Initialize session ID (persisted across pages)
  sessionId = getOrCreateSessionId();

  /**
   * Save chat history to localStorage
   * @param {Array} history - Array of message objects
   */
  function saveChatHistory(history) {
    if (!storageAvailable) return;
    try {
      // Limit history to last 50 messages to avoid quota issues
      const trimmedHistory = history.slice(-50);
      localStorage.setItem(STORAGE_KEYS.CHAT_HISTORY, JSON.stringify(trimmedHistory));
    } catch (e) {
      console.warn('Failed to save chat history:', e);
    }
  }

  /**
   * Load chat history from localStorage
   * @returns {Array} Array of message objects or empty array
   */
  function loadChatHistory() {
    if (!storageAvailable) return [];
    try {
      const stored = localStorage.getItem(STORAGE_KEYS.CHAT_HISTORY);
      return stored ? JSON.parse(stored) : [];
    } catch (e) {
      console.warn('Failed to load chat history:', e);
      return [];
    }
  }

  /**
   * Clear chat history from localStorage
   */
  function clearChatHistory() {
    if (!storageAvailable) return;
    try {
      localStorage.removeItem(STORAGE_KEYS.CHAT_HISTORY);
    } catch (e) {
      // Ignore
    }
  }

  // Track messages for persistence
  let chatHistory = loadChatHistory();

  /**
   * Append a message to the chat window
   * @param {string} html - The HTML content of the message
   * @param {boolean} isUser - Whether this is a user message
   * @param {boolean} persist - Whether to save to history (default true)
   * @returns {HTMLElement} The message element
   */
  function appendMessage(html, isUser = false, persist = true) {
    const msgContainer = document.createElement("div");
    msgContainer.className = "message-container";
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${isUser ? "user-message" : "bot-message"}`;

    // If it's a user message, use textContent; if bot message, use innerHTML for markdown
    if (isUser) {
      msgDiv.textContent = html;
    } else {
      msgDiv.innerHTML = html;
    }

    msgContainer.appendChild(msgDiv);
    chatWindow.appendChild(msgContainer);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Save to history for persistence (skip temporary messages like "Thinking...")
    if (persist && html && !html.includes('Thinking...')) {
      chatHistory.push({ content: html, isUser, timestamp: Date.now() });
      saveChatHistory(chatHistory);
    }

    return msgDiv;
  }

  /**
   * Restore chat history from localStorage
   * Called on initialization to restore previous conversation
   */
  function restoreChatHistory() {
    if (!chatWindow) return;
    const history = loadChatHistory();
    if (history.length === 0) return;

    // Clear any existing default messages
    chatWindow.innerHTML = '';

    // Restore each message
    history.forEach(msg => {
      appendMessage(msg.content, msg.isUser, false); // false = don't re-persist
    });
  }

  /**
   * Set an example from the examples list into the chat input
   * @param {HTMLElement} element - The example element clicked
   */
  function setExample(element) {
    const input = document.querySelector(".chat-input");
    if (input) {
      input.value = element.textContent.trim();
    }
  }

  /**
   * Poll workflow status until completion or timeout
   * @param {string} workflowId - The workflow ID to poll
   * @param {HTMLElement} elementToUpdate - The element to update with status
   */
  async function pollWorkflowStatus(workflowId, elementToUpdate) {
    let pollCount = 0;
    const maxPolls = 30; // Stop after 60 seconds (2s intervals)

    const intervalId = setInterval(async () => {
      pollCount++;

      try {
        const response = await fetch(
          `${API_BASE_URL}/api/v1/workflows/${workflowId}`,
          { credentials: "include" }
        );

        if (!response.ok) {
          // If 404 and we've seen success before, assume it completed
          if (
            response.status === 404 &&
            elementToUpdate.textContent.includes("completed")
          ) {
            clearInterval(intervalId);
            return; // Keep the success message
          }

          // Otherwise show error and stop
          elementToUpdate.innerHTML = `<div class="result error">Error checking status.</div>`;
          clearInterval(intervalId);
          return;
        }

        const data = await response.json();
        // Use DDD handler for workflow responses
        if (data.status === "completed") {
          elementToUpdate.classList.remove("thinking");
          elementToUpdate.classList.add("reply");
          handleWorkflowResponse(data, elementToUpdate);
          clearInterval(intervalId);
        } else if (data.status === "failed") {
          elementToUpdate.classList.remove("thinking");
          elementToUpdate.classList.add("error");
          elementToUpdate.innerHTML = renderBotMessage(
            `Workflow Failed: ${data.message}`,
            "error",
            false
          );
          clearInterval(intervalId);
        }

        // Stop polling after max attempts
        if (pollCount >= maxPolls) {
          clearInterval(intervalId);
          elementToUpdate.innerHTML = `<div class="result error">Workflow status check timed out.</div>`;
        }
      } catch (error) {
        console.error("Polling error:", error);
        elementToUpdate.innerHTML = `<div class="result error">Could not connect to API to check status.</div>`;
        clearInterval(intervalId);
      }
    }, 2000); // Poll every 2 seconds
  }

  /**
   * Handle direct response from the API
   * Uses the bot message renderer if available
   */
  function handleDirectResponse(result, element) {
    if (typeof renderBotMessage === 'function') {
      // Use DDD bot message renderer if available
      const html = renderBotMessage(result.message || result.reply || "", "reply", false);
      element.innerHTML = html;
    } else {
      // Fallback: render markdown manually
      if (typeof marked !== 'undefined') {
        element.innerHTML = marked.parse(result.message || result.reply || "");
      } else {
        element.textContent = result.message || result.reply || "";
      }
    }
  }

  /**
   * Handle error response from the API
   */
  function handleErrorResponse(error, element) {
    const errorMsg = error.message || "An unknown error occurred";
    element.innerHTML = `<div class="result error">${errorMsg}</div>`;
    element.classList.add("error");
  }

  /**
   * Restore widget expanded state from localStorage
   */
  function restoreWidgetState() {
    if (!storageAvailable) return;
    try {
      const wasExpanded = localStorage.getItem(STORAGE_KEYS.WIDGET_STATE);
      if (wasExpanded === 'true') {
        const container = document.querySelector('.chat-widget-container');
        if (container) {
          container.classList.add('expanded');
          const toggle = container.querySelector('.chat-widget-toggle');
          if (toggle) {
            toggle.innerHTML = '✕';
          }
        }
      }
    } catch (e) {
      // Ignore
    }
  }

  /**
   * Initialize the chat widget
   */
  function initChat() {
    const form = document.getElementById("chatForm");
    if (!form) return; // Chat form not found, widget not initialized

    // Restore previous state
    restoreChatHistory();
    restoreWidgetState();

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const input = form.querySelector(".chat-input");
      const message = input.value.trim();
      if (!message) return;

      appendMessage(message, true);
      input.value = "";

      // Show a temporary 'thinking' message
      const thinkingDiv = appendMessage("Thinking...");
      thinkingDiv.classList.add("thinking");

      try {
        // First, try to process as a permission intent
        if (typeof processPermissionIntent === 'function') {
          const permissionResult = await processPermissionIntent(message);
          if (permissionResult) {
            // Permission intent was handled
            if (permissionResult.success) {
              const botDiv = appendMessage(permissionResult.message, false);
              botDiv.classList.add("reply");
            } else {
              const errorDiv = appendMessage(permissionResult.message, false);
              errorDiv.classList.add("error");
            }
            thinkingDiv.remove();
            return;
          }
        }

        // Not a permission intent, send to conversational AI
        const response = await fetch(`${API_BASE_URL}/api/v1/intent`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: message,
            session_id: sessionId,
          }),
          credentials: "include",
        });

        const result = await response.json();

        if (!response.ok) {
          throw new Error(result.detail || "An API error occurred");
        }

        // Replace the 'thinking' message with a new bot message (with 'reply' class)
        const botDiv = appendMessage("", false);
        botDiv.classList.add("reply");
        handleDirectResponse(result, botDiv);
        // Remove the old thinking message
        thinkingDiv.remove();

        if (result.workflow_id) {
          // If a workflow was started, create a new message bubble to poll for its status
          const statusDiv = appendMessage("Starting workflow...");
          statusDiv.classList.add("thinking");
          pollWorkflowStatus(result.workflow_id, statusDiv);
        }

        if (result.session_id) {
          sessionId = result.session_id;
        }
      } catch (error) {
        // Replace the 'thinking' message with a new error message (with 'error' class)
        const errorDiv = appendMessage("", false);
        errorDiv.classList.add("error");
        handleErrorResponse(error, errorDiv);
        thinkingDiv.remove();
      }
    });
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChat);
  } else {
    initChat();
  }

  // Export for testing if needed
  window.ChatWidget = {
    appendMessage,
    setExample,
    pollWorkflowStatus,
    handleDirectResponse,
    handleErrorResponse,
    clearHistory: clearChatHistory,
    getSessionId: () => sessionId,
    init: initChat
  };
})();
