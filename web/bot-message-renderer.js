// Domain-driven bot message renderer and response abstractions
// DDD: This module encapsulates all message rendering and response logic for the web UI

/**
 * Render a bot message with domain logic
 * @param {string} content - The message content
 * @param {string} type - 'success', 'error', 'thinking'
 * @param {boolean} isThinking - Whether this is a thinking/loading state
 * @returns {string} - Rendered HTML
 */
function renderBotMessage(content, type = "success", isThinking = false) {
  if (!content) return "";
  // Always wrap in a div with correct classes
  let processedContent = content;
  if (type === "success" && !isThinking && typeof marked !== "undefined") {
    try {
      processedContent = marked.parse(content);
    } catch (error) {
      console.warn("Markdown parsing failed:", error);
      processedContent = content;
    }
  }
  const cssClasses = ["result", type];
  if (isThinking) cssClasses.push("thinking");
  return `<div class="${cssClasses.join(" ")}">${processedContent}</div>`;
}

/**
 * Handle direct API responses
 * @param {Object} result - API response object
 * @param {HTMLElement} element - DOM element to update
 */
function handleDirectResponse(result, element) {
  console.log("Direct response:", result.message);
  element.innerHTML = renderBotMessage(result.message, "success", false);
}

/**
 * Handle workflow completion responses
 * @param {Object} data - Workflow data object
 * @param {HTMLElement} element - DOM element to update
 */
function handleWorkflowResponse(data, element) {
  console.log("Workflow response:", data.message);
  if (data.type === "analyze_file" || data.type === "generate_report") {
    const message = data.message || "File analysis completed successfully!";
    element.innerHTML = renderBotMessage(message, "success", false);
  } else {
    const finalResult =
      data.tasks && data.tasks[data.tasks.length - 1]?.result?.issue;
    if (finalResult && finalResult.url) {
      element.innerHTML = `
                <div class="result success">
                    <strong>✅ GitHub Issue Created!</strong><br>
                    <strong>#${finalResult.number}:</strong> ${finalResult.title}<br>
                    <strong>URL:</strong> <a href="${finalResult.url}" target="_blank">View on GitHub</a>
                </div>`;
    } else {
      const message = data.message || "Workflow completed successfully!";
      element.innerHTML = renderBotMessage(message, "success", false);
    }
  }
}

/**
 * Handle error responses
 * @param {Error} error - Error object
 * @param {HTMLElement} element - DOM element to update
 */
function handleErrorResponse(error, element) {
  console.error("Error response:", error.message);
  element.innerHTML = renderBotMessage(error.message, "error", false);
}

// Export for use in browser and tests
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    renderBotMessage,
    handleDirectResponse,
    handleWorkflowResponse,
    handleErrorResponse,
  };
} else {
  window.renderBotMessage = renderBotMessage;
  window.handleDirectResponse = handleDirectResponse;
  window.handleWorkflowResponse = handleWorkflowResponse;
  window.handleErrorResponse = handleErrorResponse;
}
