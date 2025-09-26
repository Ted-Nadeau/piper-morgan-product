// Phase 1 Edge Case Testing Framework
// Enhanced browser testing for pipeline validation
// Run this in browser console at http://localhost:8001

console.log("=== PHASE 1 EDGE CASE TESTING STARTED ===");
console.log("Time:", new Date().toISOString());
console.log(
  "Mission: Validate pipeline boundaries and correlate with Code Agent findings"
);

// Enhanced test configuration for edge cases
const edgeCasePrompts = {
  // Simple variations to test boundary
  simple_plus: [
    "hi there",
    "hello help me",
    "good morning, show standup",
    "hi",
    "hey",
  ],

  // Complexity gradients
  help_variants: [
    "help",
    "help me",
    "help me please",
    "can you help me with something",
    "I need help with my project",
    "please help me understand this",
  ],

  // Different intent types
  command_variants: [
    "show standup",
    "show me standup",
    "display standup",
    "get standup",
    "standup please",
    "what is my standup",
  ],

  // Potential working alternatives
  alternative_commands: [
    "what is the weather",
    "create a task",
    "show my calendar",
    "debug this issue",
    "list my projects",
    "what can you do",
  ],

  // Mixed complexity
  mixed_patterns: [
    "fixing bugs in my code",
    "help fixing bugs",
    "good morning, fixing bugs",
    "hello, can you help me fix bugs",
  ],
};

// Enhanced results storage with categorization
window.phase1Results = {
  immediate_success: [], // <100ms, 200 status
  processing_delay: [], // >1s, eventual success
  timeout_failure: [], // >5s, 500/timeout
  immediate_failure: [], // <1s, 500 status
  networkRequests: [],
  consoleErrors: [],
  testingSummary: {
    total: 0,
    success: 0,
    failure: 0,
    patterns: {},
  },
};

// Enhanced network monitoring with detailed logging
const originalFetch = window.fetch;
window.fetch = function (...args) {
  const startTime = performance.now();
  console.log("🌐 ENHANCED Network Request:", {
    url: args[0],
    method: args[1]?.method || "GET",
    body: args[1]?.body,
    timestamp: new Date().toISOString(),
  });

  return originalFetch
    .apply(this, args)
    .then((response) => {
      const endTime = performance.now();
      const requestInfo = {
        url: args[0],
        method: args[1]?.method || "GET",
        status: response.status,
        statusText: response.statusText,
        timing: endTime - startTime,
        timestamp: new Date().toISOString(),
        body: args[1]?.body,
      };
      window.phase1Results.networkRequests.push(requestInfo);
      console.log("✅ ENHANCED Network Response:", requestInfo);
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
      window.phase1Results.networkRequests.push(requestInfo);
      console.log("❌ ENHANCED Network Error:", requestInfo);
      throw error;
    });
};

// Enhanced console error monitoring
const originalConsoleError = console.error;
console.error = function (...args) {
  window.phase1Results.consoleErrors.push({
    message: args.join(" "),
    timestamp: new Date().toISOString(),
    stack: new Error().stack,
  });
  originalConsoleError.apply(console, args);
};

// Categorization function
function categorizePromptResult(prompt, timing, status, response) {
  const result = {
    prompt,
    timing,
    status,
    response: response?.substring(0, 100),
    timestamp: new Date().toISOString(),
  };

  if (status === 200 && timing < 100) {
    window.phase1Results.immediate_success.push(result);
    console.log("📈 IMMEDIATE SUCCESS:", prompt);
  } else if (status === 200 && timing > 1000) {
    window.phase1Results.processing_delay.push(result);
    console.log("⏳ PROCESSING DELAY:", prompt);
  } else if (status === 500 && timing > 5000) {
    window.phase1Results.timeout_failure.push(result);
    console.log("⏰ TIMEOUT FAILURE:", prompt);
  } else if (status === 500 && timing < 5000) {
    window.phase1Results.immediate_failure.push(result);
    console.log("❌ IMMEDIATE FAILURE:", prompt);
  }

  window.phase1Results.testingSummary.total++;
  if (status === 200) {
    window.phase1Results.testingSummary.success++;
  } else {
    window.phase1Results.testingSummary.failure++;
  }
}

// Enhanced test execution function
async function runEdgeCaseTest(prompt) {
  console.log(`\n🧪 EDGE CASE Testing: "${prompt}"`);
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
      const result = {
        prompt,
        status: "TIMEOUT",
        timing: endTime - startTime,
        uiState: document.querySelector(".thinking")
          ? "Thinking..."
          : "Unknown",
      };
      categorizePromptResult(prompt, result.timing, "TIMEOUT", "Timeout");
      resolve(result);
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

              // Determine status from latest network request
              const latestRequest =
                window.phase1Results.networkRequests[
                  window.phase1Results.networkRequests.length - 1
                ];
              const status = latestRequest?.status || 200;

              const result = {
                prompt,
                status: status,
                timing: endTime - startTime,
                response: node.textContent?.substring(0, 100) + "...",
              };

              categorizePromptResult(
                prompt,
                result.timing,
                status,
                node.textContent
              );
              resolve(result);
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

// Batch testing function for categories
window.testCategory = async function (categoryName, prompts) {
  console.log(`\n🎯 Testing Category: ${categoryName.toUpperCase()}`);
  console.log(`Prompts to test: ${prompts.length}`);

  for (const prompt of prompts) {
    await runEdgeCaseTest(prompt);
    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  console.log(`✅ Category ${categoryName} testing complete`);
};

// Test all edge cases
window.runAllEdgeCases = async function () {
  console.log("\n🚀 STARTING COMPREHENSIVE EDGE CASE TESTING");

  for (const [categoryName, prompts] of Object.entries(edgeCasePrompts)) {
    await window.testCategory(categoryName, prompts);
  }

  console.log("\n🎉 ALL EDGE CASE TESTING COMPLETE");
  window.exportPhase1Results();
};

// Enhanced results export
window.exportPhase1Results = function () {
  const results = {
    phase1Results: window.phase1Results,
    edgeCasePrompts: edgeCasePrompts,
    timestamp: new Date().toISOString(),
    userAgent: navigator.userAgent,
    url: window.location.href,
    testingSummary: window.phase1Results.testingSummary,
  };

  console.log("=== PHASE 1 EDGE CASE RESULTS EXPORT ===");
  console.log(JSON.stringify(results, null, 2));

  // Analysis summary
  console.log("\n=== BOUNDARY ANALYSIS SUMMARY ===");
  console.log(`Total tests: ${results.testingSummary.total}`);
  console.log(`Successes: ${results.testingSummary.success}`);
  console.log(`Failures: ${results.testingSummary.failure}`);
  console.log(
    `Success rate: ${(
      (results.testingSummary.success / results.testingSummary.total) *
      100
    ).toFixed(1)}%`
  );

  console.log("\n=== PATTERN CATEGORIES ===");
  console.log(
    `Immediate Success (<100ms, 200): ${results.phase1Results.immediate_success.length}`
  );
  console.log(
    `Processing Delay (>1s, 200): ${results.phase1Results.processing_delay.length}`
  );
  console.log(
    `Immediate Failure (<5s, 500): ${results.phase1Results.immediate_failure.length}`
  );
  console.log(
    `Timeout Failure (>5s): ${results.phase1Results.timeout_failure.length}`
  );

  // Copy to clipboard if possible
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(JSON.stringify(results, null, 2))
      .then(() => console.log("✅ Results copied to clipboard"))
      .catch(() => console.log("⚠️ Could not copy to clipboard"));
  }

  return results;
};

// Individual test function
window.testEdgeCase = runEdgeCaseTest;

console.log("🚀 Phase 1 Edge Case Testing Framework loaded!");
console.log("📝 Usage:");
console.log("  - testEdgeCase('prompt') - Test individual prompt");
console.log(
  "  - testCategory('simple_plus', edgeCasePrompts.simple_plus) - Test category"
);
console.log("  - runAllEdgeCases() - Run complete edge case suite");
console.log("  - exportPhase1Results() - Export all results");
console.log("\n🎯 Ready for enhanced edge case testing!");
console.log(
  "⏳ Waiting for Code Agent's pipeline analysis to correlate findings..."
);
