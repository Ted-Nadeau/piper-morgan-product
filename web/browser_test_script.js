// Browser Testing Script for Phase 0 Frontend Investigation
// Run this in browser console at http://localhost:8001

console.log("=== PHASE 0 FRONTEND INVESTIGATION STARTED ===");
console.log("Time:", new Date().toISOString());

// Test configuration
const testPrompts = {
  working: ["hello", "good morning"],
  hanging: ["help", "show standup", "fixing bugs"],
};

// Results storage
window.testResults = {
  working: {},
  hanging: {},
  networkRequests: [],
  consoleErrors: [],
};

// Network request monitoring
const originalFetch = window.fetch;
window.fetch = function (...args) {
  const startTime = performance.now();
  console.log("🌐 Network Request:", args[0], args[1]);

  return originalFetch
    .apply(this, args)
    .then((response) => {
      const endTime = performance.now();
      const requestInfo = {
        url: args[0],
        method: args[1]?.method || "GET",
        status: response.status,
        timing: endTime - startTime,
        timestamp: new Date().toISOString(),
      };
      window.testResults.networkRequests.push(requestInfo);
      console.log("✅ Network Response:", requestInfo);
      return response;
    })
    .catch((error) => {
      const endTime = performance.now();
      const requestInfo = {
        url: args[0],
        method: args[1]?.method || "GET",
        status: "ERROR",
        error: error.message,
        timing: endTime - startTime,
        timestamp: new Date().toISOString(),
      };
      window.testResults.networkRequests.push(requestInfo);
      console.log("❌ Network Error:", requestInfo);
      throw error;
    });
};

// Console error monitoring
const originalConsoleError = console.error;
console.error = function (...args) {
  window.testResults.consoleErrors.push({
    message: args.join(" "),
    timestamp: new Date().toISOString(),
    stack: new Error().stack,
  });
  originalConsoleError.apply(console, args);
};

// Test execution function
async function runPromptTest(prompt, expectedCategory) {
  console.log(`\n🧪 Testing prompt: "${prompt}"`);
  const startTime = performance.now();

  // Find input field and submit button
  const messageInput =
    document.querySelector('textarea[placeholder*="message"]') ||
    document.querySelector('input[type="text"]') ||
    document.querySelector("#message-input") ||
    document.querySelector('[name="message"]');

  const submitButton =
    document.querySelector('button[type="submit"]') ||
    document.querySelector(".send-button") ||
    document.querySelector('[onclick*="send"]');

  if (!messageInput) {
    console.error("❌ Could not find message input field");
    return { error: "Input field not found" };
  }

  // Clear and enter prompt
  messageInput.value = "";
  messageInput.value = prompt;
  messageInput.dispatchEvent(new Event("input", { bubbles: true }));

  // Submit the message
  if (submitButton) {
    submitButton.click();
  } else {
    // Try Enter key
    messageInput.dispatchEvent(
      new KeyboardEvent("keydown", {
        key: "Enter",
        code: "Enter",
        keyCode: 13,
        bubbles: true,
      })
    );
  }

  // Wait for response or timeout
  return new Promise((resolve) => {
    const timeout = setTimeout(() => {
      const endTime = performance.now();
      resolve({
        prompt,
        status: "TIMEOUT",
        timing: endTime - startTime,
        uiState: document.querySelector(".thinking")
          ? "Thinking..."
          : "Unknown",
      });
    }, 15000); // 15 second timeout

    // Watch for response
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === "childList") {
          mutation.addedNodes.forEach((node) => {
            if (
              node.nodeType === Node.ELEMENT_NODE &&
              (node.classList?.contains("bot-message") ||
                node.textContent?.includes("assistant") ||
                node.querySelector?.(".bot-message"))
            ) {
              clearTimeout(timeout);
              observer.disconnect();
              const endTime = performance.now();
              resolve({
                prompt,
                status: "SUCCESS",
                timing: endTime - startTime,
                response: node.textContent?.substring(0, 100) + "...",
              });
            }
          });
        }
      });
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
  });
}

// Manual test runner - call this for each prompt
window.testPrompt = runPromptTest;

// Results export function
window.exportResults = function () {
  const results = {
    testResults: window.testResults,
    timestamp: new Date().toISOString(),
    userAgent: navigator.userAgent,
    url: window.location.href,
  };

  console.log("=== TEST RESULTS EXPORT ===");
  console.log(JSON.stringify(results, null, 2));

  // Also copy to clipboard if possible
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(JSON.stringify(results, null, 2))
      .then(() => console.log("✅ Results copied to clipboard"))
      .catch(() => console.log("⚠️ Could not copy to clipboard"));
  }

  return results;
};

console.log("🚀 Browser test script loaded!");
console.log("📝 Usage:");
console.log("  - testPrompt('hello') - Test a single prompt");
console.log("  - exportResults() - Export all captured data");
console.log("\n🎯 Ready to test prompts!");
