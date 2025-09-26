// Phase 2 UI Validation & Testing Framework
// Comprehensive before/after validation for web proxy implementation
// Run this in browser console at http://localhost:8081 (web interface)

console.log("=== PHASE 2 UI VALIDATION STARTED ===");
console.log("Time:", new Date().toISOString());
console.log("Mission: Validate Code Agent's web proxy implementation");

// Enhanced test results storage for before/after comparison
window.phase2ValidationResults = {
  beforeFix: {
    testResults: {},
    networkRequests: [],
    errors: [],
    timestamp: null,
    baselineComplete: false,
  },
  afterFix: {
    testResults: {},
    networkRequests: [],
    errors: [],
    timestamp: null,
    validationComplete: false,
  },
  comparison: {
    improvements: [],
    regressions: [],
    formatPreservation: {},
    networkRouting: {},
    performanceImpact: {},
  },
};

// Test cases for comprehensive validation
const phase2TestCases = {
  // Previously failing prompts that should now work
  complexCommands: [
    "help with my project",
    "show standup",
    "fixing bugs",
    "create a task",
    "debug this issue",
  ],

  // Simple prompts that should continue working
  simpleGreetings: ["hello", "good morning", "hi there"],

  // Edge cases for format validation
  formatValidation: [
    "intentionally trigger error", // Should preserve error format
    "test response format", // Should preserve success format
    "", // Empty input validation
  ],

  // Performance benchmarks
  performanceTests: [
    "quick response test",
    "longer processing test with multiple words and complexity",
  ],
};

// Enhanced network monitoring for proxy validation
let networkMonitor = [];
const originalFetch = window.fetch;

window.fetch = function (...args) {
  const startTime = performance.now();
  const requestInfo = {
    url: args[0],
    method: args[1]?.method || "GET",
    body: args[1]?.body,
    timestamp: new Date().toISOString(),
    startTime: startTime,
    phase: window.phase2ValidationResults.beforeFix.baselineComplete
      ? "afterFix"
      : "beforeFix",
  };

  console.log(`🌐 [${requestInfo.phase.toUpperCase()}] Network Request:`, {
    url: requestInfo.url,
    method: requestInfo.method,
    timestamp: requestInfo.timestamp,
  });

  return originalFetch
    .apply(this, args)
    .then((response) => {
      const endTime = performance.now();
      requestInfo.status = response.status;
      requestInfo.statusText = response.statusText;
      requestInfo.timing = endTime - startTime;
      requestInfo.success = response.ok;

      networkMonitor.push(requestInfo);
      window.phase2ValidationResults[requestInfo.phase].networkRequests.push(
        requestInfo
      );

      console.log(`✅ [${requestInfo.phase.toUpperCase()}] Network Response:`, {
        status: requestInfo.status,
        timing: requestInfo.timing.toFixed(2) + "ms",
        success: requestInfo.success,
      });

      return response;
    })
    .catch((error) => {
      const endTime = performance.now();
      requestInfo.status = "ERROR";
      requestInfo.error = error.message;
      requestInfo.timing = endTime - startTime;
      requestInfo.success = false;

      networkMonitor.push(requestInfo);
      window.phase2ValidationResults[requestInfo.phase].networkRequests.push(
        requestInfo
      );

      console.log(`❌ [${requestInfo.phase.toUpperCase()}] Network Error:`, {
        error: requestInfo.error,
        timing: requestInfo.timing.toFixed(2) + "ms",
      });

      throw error;
    });
};

// Enhanced console error monitoring
const originalConsoleError = console.error;
console.error = function (...args) {
  const phase = window.phase2ValidationResults.beforeFix.baselineComplete
    ? "afterFix"
    : "beforeFix";
  const errorInfo = {
    message: args.join(" "),
    timestamp: new Date().toISOString(),
    phase: phase,
    stack: new Error().stack,
  };

  window.phase2ValidationResults[phase].errors.push(errorInfo);
  console.log(`🚨 [${phase.toUpperCase()}] Console Error:`, errorInfo.message);

  originalConsoleError.apply(console, args);
};

// Test execution function with enhanced validation
async function runValidationTest(prompt, category = "general") {
  const phase = window.phase2ValidationResults.beforeFix.baselineComplete
    ? "afterFix"
    : "beforeFix";
  console.log(
    `\n🧪 [${phase.toUpperCase()}] Testing: "${prompt}" (${category})`
  );

  const startTime = performance.now();

  // Find UI elements
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
    return { error: "Input field not found", phase: phase };
  }

  // Clear and enter prompt
  messageInput.value = "";
  messageInput.value = prompt;
  messageInput.dispatchEvent(new Event("input", { bubbles: true }));

  // Submit message
  if (submitButton) {
    submitButton.click();
  } else {
    messageInput.dispatchEvent(
      new KeyboardEvent("keydown", {
        key: "Enter",
        code: "Enter",
        keyCode: 13,
        bubbles: true,
      })
    );
  }

  // Wait for response with enhanced monitoring
  return new Promise((resolve) => {
    const timeout = setTimeout(() => {
      const endTime = performance.now();
      const result = {
        prompt,
        category,
        phase,
        status: "TIMEOUT",
        timing: endTime - startTime,
        timestamp: new Date().toISOString(),
        uiState: document.querySelector(".thinking")
          ? "Thinking..."
          : "Unknown",
      };

      console.log(`⏰ [${phase.toUpperCase()}] TIMEOUT: "${prompt}"`);
      resolve(result);
    }, 20000); // 20 second timeout

    // Enhanced response monitoring
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === "childList") {
          mutation.addedNodes.forEach((node) => {
            if (
              node.nodeType === Node.ELEMENT_NODE &&
              (node.classList?.contains("bot-message") ||
                node.textContent?.includes("assistant") ||
                node.querySelector?.(".bot-message") ||
                node.classList?.contains("error"))
            ) {
              clearTimeout(timeout);
              observer.disconnect();
              const endTime = performance.now();

              // Get latest network request for status
              const latestRequest = networkMonitor[networkMonitor.length - 1];
              const isError =
                node.classList?.contains("error") ||
                node.textContent?.includes("Failed to process intent");

              const result = {
                prompt,
                category,
                phase,
                status: latestRequest?.status || (isError ? 500 : 200),
                timing: endTime - startTime,
                timestamp: new Date().toISOString(),
                response: node.textContent?.substring(0, 200) + "...",
                isError: isError,
                networkStatus: latestRequest?.status,
                uiElement: node.className,
              };

              console.log(
                `📋 [${phase.toUpperCase()}] Result: "${prompt}" -> ${
                  result.status
                } (${result.timing.toFixed(2)}ms)`
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

// Baseline documentation function
window.documentBaseline = async function () {
  console.log("\n🏁 === DOCUMENTING BASELINE (BEFORE FIX) ===");
  window.phase2ValidationResults.beforeFix.timestamp = new Date().toISOString();

  console.log("📊 Testing current broken state for comparison...");

  // Test complex commands that should be failing
  for (const prompt of phase2TestCases.complexCommands) {
    const result = await runValidationTest(prompt, "complex");
    window.phase2ValidationResults.beforeFix.testResults[prompt] = result;

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  // Test simple greetings that should be working
  for (const prompt of phase2TestCases.simpleGreetings) {
    const result = await runValidationTest(prompt, "simple");
    window.phase2ValidationResults.beforeFix.testResults[prompt] = result;

    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  window.phase2ValidationResults.beforeFix.baselineComplete = true;
  console.log("✅ BASELINE DOCUMENTATION COMPLETE");

  // Export baseline for reference
  console.log("\n📋 === BASELINE RESULTS ===");
  console.log(
    JSON.stringify(window.phase2ValidationResults.beforeFix, null, 2)
  );

  return window.phase2ValidationResults.beforeFix;
};

// Post-implementation validation function
window.validateImplementation = async function () {
  if (!window.phase2ValidationResults.beforeFix.baselineComplete) {
    console.error("❌ Must document baseline first! Run documentBaseline()");
    return;
  }

  console.log("\n🎯 === VALIDATING IMPLEMENTATION (AFTER FIX) ===");
  window.phase2ValidationResults.afterFix.timestamp = new Date().toISOString();

  console.log("🔍 Testing same prompts post-implementation...");

  // Test the same prompts that were tested in baseline
  const baselinePrompts = Object.keys(
    window.phase2ValidationResults.beforeFix.testResults
  );

  for (const prompt of baselinePrompts) {
    const result = await runValidationTest(prompt, "validation");
    window.phase2ValidationResults.afterFix.testResults[prompt] = result;

    // Compare with baseline immediately
    const beforeResult =
      window.phase2ValidationResults.beforeFix.testResults[prompt];
    const improvement =
      beforeResult.status >= 400 && result.status < 400
        ? "FIXED"
        : beforeResult.status < 400 && result.status >= 400
        ? "BROKEN"
        : "UNCHANGED";

    console.log(
      `📈 Comparison "${prompt}": ${beforeResult.status} -> ${result.status} (${improvement})`
    );

    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  window.phase2ValidationResults.afterFix.validationComplete = true;
  console.log("✅ IMPLEMENTATION VALIDATION COMPLETE");

  // Generate comparison report
  window.generateComparisonReport();

  return window.phase2ValidationResults.afterFix;
};

// Comparison report generation
window.generateComparisonReport = function () {
  console.log("\n📊 === GENERATING COMPARISON REPORT ===");

  const before = window.phase2ValidationResults.beforeFix.testResults;
  const after = window.phase2ValidationResults.afterFix.testResults;

  const improvements = [];
  const regressions = [];
  const unchanged = [];

  for (const prompt in before) {
    if (after[prompt]) {
      const beforeStatus = before[prompt].status;
      const afterStatus = after[prompt].status;

      if (beforeStatus >= 400 && afterStatus < 400) {
        improvements.push({
          prompt,
          before: beforeStatus,
          after: afterStatus,
          timingBefore: before[prompt].timing,
          timingAfter: after[prompt].timing,
        });
      } else if (beforeStatus < 400 && afterStatus >= 400) {
        regressions.push({
          prompt,
          before: beforeStatus,
          after: afterStatus,
          timingBefore: before[prompt].timing,
          timingAfter: after[prompt].timing,
        });
      } else {
        unchanged.push({
          prompt,
          status: afterStatus,
          timingBefore: before[prompt].timing,
          timingAfter: after[prompt].timing,
        });
      }
    }
  }

  window.phase2ValidationResults.comparison = {
    improvements,
    regressions,
    unchanged,
    totalTests: Object.keys(before).length,
    successRate: (
      ((improvements.length + unchanged.filter((u) => u.status < 400).length) /
        Object.keys(before).length) *
      100
    ).toFixed(1),
  };

  console.log("\n🎉 === COMPARISON REPORT ===");
  console.log(
    `Total Tests: ${window.phase2ValidationResults.comparison.totalTests}`
  );
  console.log(`Improvements: ${improvements.length}`);
  console.log(`Regressions: ${regressions.length}`);
  console.log(`Unchanged: ${unchanged.length}`);
  console.log(
    `Success Rate: ${window.phase2ValidationResults.comparison.successRate}%`
  );

  if (improvements.length > 0) {
    console.log("\n✅ IMPROVEMENTS:");
    improvements.forEach((imp) => {
      console.log(
        `  "${imp.prompt}": ${imp.before} -> ${imp.after} (${(
          imp.timingAfter - imp.timingBefore
        ).toFixed(2)}ms change)`
      );
    });
  }

  if (regressions.length > 0) {
    console.log("\n❌ REGRESSIONS:");
    regressions.forEach((reg) => {
      console.log(
        `  "${reg.prompt}": ${reg.before} -> ${reg.after} (${(
          reg.timingAfter - reg.timingBefore
        ).toFixed(2)}ms change)`
      );
    });
  }

  return window.phase2ValidationResults.comparison;
};

// Network routing validation
window.validateNetworkRouting = function () {
  console.log("\n🌐 === NETWORK ROUTING VALIDATION ===");

  const beforeRequests =
    window.phase2ValidationResults.beforeFix.networkRequests;
  const afterRequests = window.phase2ValidationResults.afterFix.networkRequests;

  console.log("Before Fix Routing:");
  beforeRequests.forEach((req) => {
    console.log(
      `  ${req.method} ${req.url} -> ${req.status} (${req.timing?.toFixed(
        2
      )}ms)`
    );
  });

  console.log("\nAfter Fix Routing:");
  afterRequests.forEach((req) => {
    console.log(
      `  ${req.method} ${req.url} -> ${req.status} (${req.timing?.toFixed(
        2
      )}ms)`
    );
  });

  // Analyze routing changes
  const routingAnalysis = {
    beforePorts: [...new Set(beforeRequests.map((r) => new URL(r.url).port))],
    afterPorts: [...new Set(afterRequests.map((r) => new URL(r.url).port))],
    proxyWorking: afterRequests.some(
      (r) => r.url.includes(":8081") && r.url.includes("intent")
    ),
    directBackend: afterRequests.some(
      (r) => r.url.includes(":8001") && r.url.includes("intent")
    ),
  };

  console.log("\n📊 Routing Analysis:");
  console.log(`Before ports: ${routingAnalysis.beforePorts.join(", ")}`);
  console.log(`After ports: ${routingAnalysis.afterPorts.join(", ")}`);
  console.log(
    `Proxy working: ${routingAnalysis.proxyWorking ? "✅ YES" : "❌ NO"}`
  );
  console.log(
    `Direct backend: ${
      routingAnalysis.directBackend ? "⚠️ YES (unexpected)" : "✅ NO (expected)"
    }`
  );

  window.phase2ValidationResults.comparison.networkRouting = routingAnalysis;
  return routingAnalysis;
};

// Export all results
window.exportPhase2Results = function () {
  const fullResults = {
    ...window.phase2ValidationResults,
    testCases: phase2TestCases,
    networkMonitor: networkMonitor,
    timestamp: new Date().toISOString(),
    userAgent: navigator.userAgent,
    url: window.location.href,
  };

  console.log("=== PHASE 2 VALIDATION RESULTS EXPORT ===");
  console.log(JSON.stringify(fullResults, null, 2));

  // Copy to clipboard if possible
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(JSON.stringify(fullResults, null, 2))
      .then(() => console.log("✅ Results copied to clipboard"))
      .catch(() => console.log("⚠️ Could not copy to clipboard"));
  }

  return fullResults;
};

console.log("🚀 Phase 2 Validation Framework loaded!");
console.log("📝 Usage:");
console.log("  1. documentBaseline() - Document current broken state");
console.log("  2. [Wait for Code Agent completion]");
console.log("  3. validateImplementation() - Test after fix");
console.log("  4. validateNetworkRouting() - Verify proxy routing");
console.log("  5. exportPhase2Results() - Export all results");
console.log("\n🎯 Ready for comprehensive UI validation!");
console.log(
  "⚠️  IMPORTANT: Run at http://localhost:8081 (web interface), not :8001"
);
