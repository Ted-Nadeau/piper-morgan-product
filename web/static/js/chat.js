// Chat Widget - Modular chat functionality
(function() {
  'use strict';

  const API_BASE_URL = window.API_BASE_URL || "";
  const chatWindow = document.getElementById("chat-window");
  let sessionId = null;

  /**
   * Toggle chat widget expanded/collapsed state
   * Updates widget container class and manages focus/icon
   */
  function toggleChatWidget() {
    const container = document.querySelector('.chat-widget-container');
    if (container) {
      container.classList.toggle('expanded');

      // Update toggle button icon when expanded
      const toggle = container.querySelector('.chat-widget-toggle');
      if (toggle) {
        toggle.innerHTML = container.classList.contains('expanded') ? '✕' : '💬';
      }

      // Focus input when expanded for better UX
      if (container.classList.contains('expanded')) {
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

  // Initialize session ID if not already set
  if (!sessionId) {
    sessionId = crypto.randomUUID ? crypto.randomUUID() : generateSessionId();
  }

  /**
   * Generate a fallback session ID for browsers without crypto API
   */
  function generateSessionId() {
    return 'session-' + Math.random().toString(36).substr(2, 9) +
           '-' + Date.now().toString(36);
  }

  /**
   * Append a message to the chat window
   * @param {string} html - The HTML content of the message
   * @param {boolean} isUser - Whether this is a user message
   * @returns {HTMLElement} The message element
   */
  function appendMessage(html, isUser = false) {
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
    return msgDiv;
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
   * Initialize the chat widget
   */
  function initChat() {
    const form = document.getElementById("chatForm");
    if (!form) return; // Chat form not found, widget not initialized

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
    init: initChat
  };
})();
