// Issue #179 Error Reproduction Framework
// Date: September 18, 2025
// Mission: Capture exact error messages and UI symptoms
// Agent: Cursor Agent (Phase 0)

console.log("=== ISSUE #179 ERROR REPRODUCTION FRAMEWORK ===");
console.log("Date:", new Date().toISOString());
console.log("Mission: Capture exact error messages and UI symptoms");

// Results storage
window.errorReproduction = {
  workingIntents: {},
  failingIntents: {},
  networkData: [],
  uiStates: [],
  pm039Patterns: {},
  timestamp: new Date().toISOString(),
};

// Network request monitoring
const networkMonitor = [];
const originalFetch = window.fetch;

window.fetch = function (...args) {
  const startTime = performance.now();
  const requestInfo = {
    url: args[0],
    method: args[1]?.method || "GET",
    body: args[1]?.body,
    timestamp: new Date().toISOString(),
    startTime: startTime,
  };

  console.log(`🌐 [NETWORK] Request: ${requestInfo.method} ${requestInfo.url}`);

  return originalFetch
    .apply(this, args)
    .then((response) => {
      const endTime = performance.now();
      requestInfo.status = response.status;
      requestInfo.statusText = response.statusText;
      requestInfo.timing = endTime - startTime;
      requestInfo.success = response.ok;
      requestInfo.headers = Object.fromEntries(response.headers);

      networkMonitor.push(requestInfo);
      window.errorReproduction.networkData.push(requestInfo);

      console.log(
        `✅ [NETWORK] Response: ${
          requestInfo.status
        } (${requestInfo.timing.toFixed(2)}ms)`
      );

      return response;
    })
    .catch((error) => {
      const endTime = performance.now();
      requestInfo.status = "ERROR";
      requestInfo.error = error.message;
      requestInfo.timing = endTime - startTime;
      requestInfo.success = false;

      networkMonitor.push(requestInfo);
      window.errorReproduction.networkData.push(requestInfo);

      console.log(
        `❌ [NETWORK] Error: ${requestInfo.error} (${requestInfo.timing.toFixed(
          2
        )}ms)`
      );

      throw error;
    });
};

// Console error capture
window.addEventListener("error", (event) => {
  const errorInfo = {
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    stack: event.error?.stack,
    timestamp: new Date().toISOString(),
  };

  console.log("🚨 [JS ERROR]:", errorInfo);
  window.errorReproduction.uiStates.push({
    type: "javascript_error",
    data: errorInfo,
    timestamp: new Date().toISOString(),
  });
});

// Test working intents (baseline)
window.testWorkingIntents = async function () {
  console.log("\n🎯 === TESTING WORKING INTENTS (BASELINE) ===");

  const workingTests = ["hello", "good morning", "hi there"];

  for (const message of workingTests) {
    try {
      console.log(`\nTesting: "${message}"`);
      const startTime = performance.now();

      const response = await fetch("/api/v1/intent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          session_id: `working-test-${Date.now()}`,
        }),
      });

      const endTime = performance.now();
      const responseTime = Math.round(endTime - startTime);

      // Get response text first
      const responseText = await response.text();

      const result = {
        message: message,
        status: response.status,
        statusText: response.statusText,
        responseTime: responseTime,
        responseText: responseText,
        timestamp: new Date().toISOString(),
      };

      // Try to parse as JSON
      try {
        result.jsonResponse = JSON.parse(responseText);
        console.log(`✅ "${message}": ${response.status} (${responseTime}ms)`);
        console.log(
          `Response: ${JSON.stringify(result.jsonResponse, null, 2)}`
        );
      } catch (parseError) {
        result.parseError = parseError.message;
        console.log(
          `⚠️ "${message}": ${response.status} (${responseTime}ms) - JSON parse failed`
        );
        console.log(`Raw response: ${responseText}`);
      }

      window.errorReproduction.workingIntents[message] = result;
    } catch (error) {
      const errorResult = {
        message: message,
        error: error.message,
        stack: error.stack,
        timestamp: new Date().toISOString(),
      };

      console.log(`❌ "${message}": NETWORK ERROR - ${error.message}`);
      window.errorReproduction.workingIntents[message] = errorResult;
    }

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  console.log("\n📊 Working intents test complete");
  return window.errorReproduction.workingIntents;
};

// Test failing intents - capture EXACT error messages
window.testFailingIntents = async function () {
  console.log("\n🔥 === TESTING FAILING INTENTS (EXACT ERROR CAPTURE) ===");

  const failingTests = [
    "show standup",
    "show me my standup",
    "create task",
    "analyze project",
    "help with my project",
    "list projects",
  ];

  for (const message of failingTests) {
    try {
      console.log(`\nTesting: "${message}"`);
      const startTime = performance.now();

      const response = await fetch("/api/v1/intent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          session_id: `error-test-${Date.now()}`,
        }),
      });

      const endTime = performance.now();
      const responseTime = Math.round(endTime - startTime);

      // Get response text first
      const responseText = await response.text();

      const result = {
        message: message,
        status: response.status,
        statusText: response.statusText,
        responseTime: responseTime,
        responseText: responseText,
        headers: Object.fromEntries(response.headers),
        timestamp: new Date().toISOString(),
      };

      console.log(`Status: ${response.status} ${response.statusText}`);
      console.log(`Response time: ${responseTime}ms`);
      console.log(`Headers: ${JSON.stringify(result.headers, null, 2)}`);
      console.log(`Raw response: ${responseText}`);

      // Try to parse as JSON
      try {
        result.jsonResponse = JSON.parse(responseText);
        console.log(
          `Parsed JSON: ${JSON.stringify(result.jsonResponse, null, 2)}`
        );

        // Look for specific error patterns
        if (result.jsonResponse.detail) {
          console.log(`🚨 ERROR DETAIL: ${result.jsonResponse.detail}`);
        }
        if (result.jsonResponse.error) {
          console.log(`🚨 ERROR MESSAGE: ${result.jsonResponse.error}`);
        }
      } catch (parseError) {
        result.parseError = parseError.message;
        console.log(`JSON parse failed: ${parseError.message}`);
      }

      window.errorReproduction.failingIntents[message] = result;
    } catch (networkError) {
      const errorResult = {
        message: message,
        networkError: networkError.message,
        stack: networkError.stack,
        timestamp: new Date().toISOString(),
      };

      console.log(`❌ Network error for "${message}": ${networkError.message}`);
      window.errorReproduction.failingIntents[message] = errorResult;
    }

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  console.log("\n📊 Failing intents test complete");
  return window.errorReproduction.failingIntents;
};

// Document UI state during testing
window.documentUIState = function () {
  console.log("\n📋 === UI STATE DOCUMENTATION ===");

  const uiState = {
    timestamp: new Date().toISOString(),
    url: window.location.href,
    title: document.title,
    activeElement: document.activeElement?.tagName,
    thinkingElements: document.querySelectorAll(
      '[data-testid*="thinking"], .thinking, .loading'
    ).length,
    errorElements: document.querySelectorAll(
      '.error, [class*="error"], [data-testid*="error"]'
    ).length,
    responseElements: document.querySelectorAll(
      '.response, [class*="response"], [data-testid*="response"]'
    ).length,
    messageInput: !!document.querySelector(
      'textarea[placeholder*="message"], input[type="text"], #message-input'
    ),
    submitButton: !!document.querySelector(
      'button[type="submit"], .send-button'
    ),
  };

  console.log("Current UI State:", uiState);
  window.errorReproduction.uiStates.push({
    type: "ui_state_check",
    data: uiState,
    timestamp: new Date().toISOString(),
  });

  return uiState;
};

// Test PM-039 patterns that worked in July 2025
window.testPM039Patterns = async function () {
  console.log("\n🏛️ === PM-039 HISTORICAL PATTERN TESTING ===");
  console.log("Testing patterns that worked in July 2025...");

  const pm039Patterns = [
    "search for requirements files",
    "find technical specifications",
    "locate API documentation",
    "show me all project plans",
    "get all design docs",
    "find docs about onboarding",
  ];

  for (const pattern of pm039Patterns) {
    try {
      console.log(`\nTesting PM-039 pattern: "${pattern}"`);
      const startTime = performance.now();

      const response = await fetch("/api/v1/intent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: pattern,
          session_id: `pm039-${Date.now()}`,
        }),
      });

      const endTime = performance.now();
      const responseTime = Math.round(endTime - startTime);
      const responseText = await response.text();

      const result = {
        pattern: pattern,
        status: response.status,
        responseTime: responseTime,
        responseText: responseText,
        expectedAction: "search_documents",
        timestamp: new Date().toISOString(),
      };

      try {
        result.jsonResponse = JSON.parse(responseText);
        console.log(
          `PM-039 Pattern "${pattern}": ${response.status} (${responseTime}ms)`
        );
        console.log(`Expected: search_documents action`);
        console.log(`Actual: ${JSON.stringify(result.jsonResponse, null, 2)}`);

        // Check if it matches expected search_documents action
        if (result.jsonResponse.action === "search_documents") {
          console.log(`✅ Pattern working as expected`);
          result.working = true;
        } else {
          console.log(`⚠️ Pattern not working as expected`);
          result.working = false;
        }
      } catch (parseError) {
        result.parseError = parseError.message;
        result.working = false;
        console.log(`❌ JSON parse failed: ${parseError.message}`);
      }

      window.errorReproduction.pm039Patterns[pattern] = result;
    } catch (error) {
      const errorResult = {
        pattern: pattern,
        error: error.message,
        working: false,
        timestamp: new Date().toISOString(),
      };

      console.log(`❌ PM-039 Pattern "${pattern}": ERROR - ${error.message}`);
      window.errorReproduction.pm039Patterns[pattern] = errorResult;
    }

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  console.log("\n📊 PM-039 historical pattern testing complete");
  return window.errorReproduction.pm039Patterns;
};

// Run complete error reproduction suite
window.runCompleteErrorReproduction = async function () {
  console.log("\n🚀 === RUNNING COMPLETE ERROR REPRODUCTION SUITE ===");
  console.log("This will systematically test all patterns...");

  try {
    // Document initial UI state
    console.log("\n1️⃣ Documenting initial UI state...");
    documentUIState();

    // Test working intents first (baseline)
    console.log("\n2️⃣ Testing working intents (baseline)...");
    await testWorkingIntents();

    // Test failing intents (capture exact errors)
    console.log("\n3️⃣ Testing failing intents (exact error capture)...");
    await testFailingIntents();

    // Test PM-039 historical patterns
    console.log("\n4️⃣ Testing PM-039 historical patterns...");
    await testPM039Patterns();

    // Final UI state check
    console.log("\n5️⃣ Final UI state documentation...");
    documentUIState();

    console.log("\n✅ === COMPLETE ERROR REPRODUCTION SUITE FINISHED ===");

    const summary = {
      workingIntents: Object.keys(window.errorReproduction.workingIntents)
        .length,
      failingIntents: Object.keys(window.errorReproduction.failingIntents)
        .length,
      pm039Patterns: Object.keys(window.errorReproduction.pm039Patterns).length,
      networkRequests: window.errorReproduction.networkData.length,
      uiStateChecks: window.errorReproduction.uiStates.length,
      timestamp: new Date().toISOString(),
    };

    console.log("\n📊 SUMMARY:", summary);
    return summary;
  } catch (error) {
    console.error("❌ Error reproduction suite failed:", error);
    return { error: error.message };
  }
};

// Export all collected data
window.exportErrorReproductionData = function () {
  const fullData = {
    ...window.errorReproduction,
    networkRequests: networkMonitor,
    exportTimestamp: new Date().toISOString(),
    userAgent: navigator.userAgent,
    url: window.location.href,
    phase: "Phase 0 - Error Reproduction & Capture",
  };

  console.log("\n📋 === ERROR REPRODUCTION DATA EXPORT ===");
  console.log(JSON.stringify(fullData, null, 2));

  // Copy to clipboard if possible
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(JSON.stringify(fullData, null, 2))
      .then(() => console.log("✅ Error reproduction data copied to clipboard"))
      .catch(() => console.log("⚠️ Could not copy to clipboard"));
  }

  return fullData;
};

console.log("\n🎯 Error Reproduction Framework Loaded!");
console.log("📋 Usage:");
console.log("- runCompleteErrorReproduction() - Run all tests systematically");
console.log("- testWorkingIntents() - Test baseline working patterns");
console.log("- testFailingIntents() - Capture exact error messages");
console.log("- testPM039Patterns() - Test historical July patterns");
console.log("- documentUIState() - Check current UI state");
console.log("- exportErrorReproductionData() - Export all collected data");
console.log("\n🔍 Ready to capture exact error messages and UI symptoms!");
