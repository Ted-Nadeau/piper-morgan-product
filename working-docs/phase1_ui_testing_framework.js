// Phase 1 UI Testing Framework - Workaround System Analysis
// Date: September 18, 2025
// Mission: Document UI behavior for working vs failing patterns
// Agent: Cursor Agent (Phase 1A)

console.log("=== PHASE 1 UI TESTING FRAMEWORK ===");
console.log("Date:", new Date().toISOString());
console.log("Mission: Document UI behavior for working vs failing patterns");

// Results storage for Phase 1
window.phase1Analysis = {
  workingPatterns: {},
  failingPatterns: {},
  edgeCases: {},
  uiBehavior: [],
  networkAnalysis: [],
  bypassMechanisms: [],
  timestamp: new Date().toISOString(),
};

// Enhanced network monitoring for Phase 1
const phase1NetworkMonitor = [];
let phase1OriginalFetch = null;

// Only override fetch if not already done
if (!window.phase1FetchOverridden) {
  phase1OriginalFetch = window.fetch;

  window.fetch = function (...args) {
    const startTime = performance.now();
    const requestInfo = {
      url: args[0],
      method: args[1]?.method || "GET",
      body: args[1]?.body,
      timestamp: new Date().toISOString(),
      startTime: startTime,
      phase: "Phase 1",
    };

    console.log(
      `🌐 [PHASE1] Request: ${requestInfo.method} ${requestInfo.url}`
    );

    return phase1OriginalFetch
      .apply(this, args)
      .then((response) => {
        const endTime = performance.now();
        requestInfo.status = response.status;
        requestInfo.statusText = response.statusText;
        requestInfo.timing = endTime - startTime;
        requestInfo.success = response.ok;
        requestInfo.headers = Object.fromEntries(response.headers);

        phase1NetworkMonitor.push(requestInfo);
        window.phase1Analysis.networkAnalysis.push(requestInfo);

        console.log(
          `✅ [PHASE1] Response: ${
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

        phase1NetworkMonitor.push(requestInfo);
        window.phase1Analysis.networkAnalysis.push(requestInfo);

        console.log(
          `❌ [PHASE1] Error: ${
            requestInfo.error
          } (${requestInfo.timing.toFixed(2)}ms)`
        );

        throw error;
      });
  };

  window.phase1FetchOverridden = true;
  console.log("✅ Phase 1 network monitoring enabled");
}

// Test working patterns (Tier 1: Direct Response System)
window.testWorkingPatterns = async function () {
  console.log("\n🎯 === TESTING WORKING PATTERNS (TIER 1) ===");

  const workingTests = [
    { message: "hello", expected: "greeting" },
    { message: "hi", expected: "greeting" },
    { message: "good morning", expected: "greeting" },
    { message: "help with my project", expected: "clarification" },
    {
      message: "I need help understanding the system",
      expected: "clarification",
    },
  ];

  for (const test of workingTests) {
    try {
      console.log(`\nTesting working pattern: "${test.message}"`);
      const startTime = performance.now();

      const response = await fetch("/api/v1/intent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: test.message,
          session_id: `phase1-working-${Date.now()}`,
        }),
      });

      const endTime = performance.now();
      const responseTime = Math.round(endTime - startTime);
      const responseText = await response.text();

      const result = {
        message: test.message,
        expected: test.expected,
        status: response.status,
        responseTime: responseTime,
        responseText: responseText,
        timestamp: new Date().toISOString(),
      };

      try {
        result.jsonResponse = JSON.parse(responseText);
        console.log(
          `✅ "${test.message}": ${response.status} (${responseTime}ms)`
        );
        console.log(`Category: ${result.jsonResponse.intent?.category}`);
        console.log(`Action: ${result.jsonResponse.intent?.action}`);
        console.log(`Workflow ID: ${result.jsonResponse.workflow_id}`);
        console.log(
          `Message: ${result.jsonResponse.message?.substring(0, 100)}...`
        );

        // Analyze bypass mechanism
        if (result.jsonResponse.workflow_id === null) {
          console.log(`🔄 BYPASS CONFIRMED: No orchestration required`);
          result.bypassMechanism = "direct_response";
        }
      } catch (parseError) {
        result.parseError = parseError.message;
        console.log(`⚠️ JSON parse failed: ${parseError.message}`);
      }

      window.phase1Analysis.workingPatterns[test.message] = result;
    } catch (error) {
      console.log(`❌ Error testing "${test.message}": ${error.message}`);
      window.phase1Analysis.workingPatterns[test.message] = {
        message: test.message,
        error: error.message,
        timestamp: new Date().toISOString(),
      };
    }

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  console.log("\n📊 Working patterns analysis complete");
  return window.phase1Analysis.workingPatterns;
};

// Test failing patterns (Tier 2: Orchestration-Dependent System)
window.testFailingPatterns = async function () {
  console.log("\n🔥 === TESTING FAILING PATTERNS (TIER 2) ===");

  const failingTests = [
    {
      message: "show standup",
      category: "QUERY",
      expected: "orchestration_required",
    },
    {
      message: "show me my standup",
      category: "QUERY",
      expected: "orchestration_required",
    },
    {
      message: "create task",
      category: "EXECUTION",
      expected: "orchestration_required",
    },
    {
      message: "debug issue",
      category: "EXECUTION",
      expected: "orchestration_required",
    },
    {
      message: "analyze project",
      category: "ANALYSIS",
      expected: "orchestration_required",
    },
    {
      message: "list projects",
      category: "QUERY",
      expected: "orchestration_required",
    },
  ];

  for (const test of failingTests) {
    try {
      console.log(
        `\nTesting failing pattern: "${test.message}" (${test.category})`
      );
      const startTime = performance.now();

      const response = await fetch("/api/v1/intent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: test.message,
          session_id: `phase1-failing-${Date.now()}`,
        }),
      });

      const endTime = performance.now();
      const responseTime = Math.round(endTime - startTime);
      const responseText = await response.text();

      const result = {
        message: test.message,
        category: test.category,
        expected: test.expected,
        status: response.status,
        responseTime: responseTime,
        responseText: responseText,
        timestamp: new Date().toISOString(),
      };

      try {
        result.jsonResponse = JSON.parse(responseText);
        console.log(
          `❌ "${test.message}": ${response.status} (${responseTime}ms)`
        );
        console.log(`Response: ${responseText}`);

        // Analyze failure pattern
        if (result.jsonResponse.detail === "Failed to process intent") {
          console.log(
            `🚨 ORCHESTRATION FAILURE: Generic error indicates orchestration dependency`
          );
          result.failureType = "orchestration_required";
        }
      } catch (parseError) {
        result.parseError = parseError.message;
        console.log(`⚠️ JSON parse failed: ${parseError.message}`);
      }

      window.phase1Analysis.failingPatterns[test.message] = result;
    } catch (error) {
      console.log(`❌ Error testing "${test.message}": ${error.message}`);
      window.phase1Analysis.failingPatterns[test.message] = {
        message: test.message,
        error: error.message,
        timestamp: new Date().toISOString(),
      };
    }

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  console.log("\n📊 Failing patterns analysis complete");
  return window.phase1Analysis.failingPatterns;
};

// Test edge cases to understand bypass boundaries
window.testEdgeCases = async function () {
  console.log("\n🔍 === TESTING EDGE CASES (BYPASS BOUNDARIES) ===");

  const edgeCases = [
    {
      message: "help me create a task",
      description: "Help request with execution intent",
    },
    {
      message: "what is standup",
      description: "Question about standup (not show standup)",
    },
    {
      message: "how do I debug",
      description: "Learning question vs execution",
    },
    {
      message: "explain project analysis",
      description: "Explanation vs analysis execution",
    },
    { message: "thank you", description: "Simple social response" },
    { message: "goodbye", description: "Simple farewell" },
  ];

  for (const test of edgeCases) {
    try {
      console.log(`\nTesting edge case: "${test.message}"`);
      console.log(`Description: ${test.description}`);
      const startTime = performance.now();

      const response = await fetch("/api/v1/intent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: test.message,
          session_id: `phase1-edge-${Date.now()}`,
        }),
      });

      const endTime = performance.now();
      const responseTime = Math.round(endTime - startTime);
      const responseText = await response.text();

      const result = {
        message: test.message,
        description: test.description,
        status: response.status,
        responseTime: responseTime,
        responseText: responseText,
        timestamp: new Date().toISOString(),
      };

      try {
        result.jsonResponse = JSON.parse(responseText);
        console.log(
          `🔍 "${test.message}": ${response.status} (${responseTime}ms)`
        );

        if (result.jsonResponse.intent) {
          console.log(`Category: ${result.jsonResponse.intent.category}`);
          console.log(`Action: ${result.jsonResponse.intent.action}`);
          console.log(`Workflow ID: ${result.jsonResponse.workflow_id}`);

          // Determine tier
          if (result.jsonResponse.workflow_id === null) {
            console.log(`📍 TIER 1: Direct response (bypasses orchestration)`);
            result.tier = "tier1_bypass";
          } else {
            console.log(`📍 TIER 2: Orchestration required`);
            result.tier = "tier2_orchestration";
          }
        } else if (result.jsonResponse.detail === "Failed to process intent") {
          console.log(`📍 TIER 2: Orchestration failure`);
          result.tier = "tier2_failed";
        }
      } catch (parseError) {
        result.parseError = parseError.message;
        console.log(`⚠️ JSON parse failed: ${parseError.message}`);
      }

      window.phase1Analysis.edgeCases[test.message] = result;
    } catch (error) {
      console.log(`❌ Error testing "${test.message}": ${error.message}`);
      window.phase1Analysis.edgeCases[test.message] = {
        message: test.message,
        error: error.message,
        timestamp: new Date().toISOString(),
      };
    }

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  console.log("\n📊 Edge case analysis complete");
  return window.phase1Analysis.edgeCases;
};

// Document UI behavior during testing
window.documentUIBehavior = function () {
  console.log("\n📋 === UI BEHAVIOR DOCUMENTATION ===");

  const uiBehavior = {
    timestamp: new Date().toISOString(),
    url: window.location.href,
    title: document.title,
    activeElement: document.activeElement?.tagName,

    // UI state elements
    inputElements: {
      messageInput: !!document.querySelector(
        'textarea[placeholder*="message"], input[type="text"], #message-input'
      ),
      submitButton: !!document.querySelector(
        'button[type="submit"], .send-button'
      ),
    },

    // Response display elements
    responseElements: {
      messageContainer: document.querySelectorAll(
        '.message, [class*="message"], [data-testid*="message"]'
      ).length,
      responseContainer: document.querySelectorAll(
        '.response, [class*="response"], [data-testid*="response"]'
      ).length,
      errorContainer: document.querySelectorAll(
        '.error, [class*="error"], [data-testid*="error"]'
      ).length,
    },

    // Loading/thinking states
    loadingElements: {
      thinkingElements: document.querySelectorAll(
        '[data-testid*="thinking"], .thinking, .loading'
      ).length,
      spinnerElements: document.querySelectorAll(
        '.spinner, [class*="spinner"], .loading-spinner'
      ).length,
    },
  };

  console.log("Current UI State:", uiBehavior);
  window.phase1Analysis.uiBehavior.push({
    type: "ui_behavior_check",
    data: uiBehavior,
    timestamp: new Date().toISOString(),
  });

  return uiBehavior;
};

// Run complete Phase 1A testing suite
window.runPhase1ATesting = async function () {
  console.log("\n🚀 === RUNNING COMPLETE PHASE 1A TESTING SUITE ===");
  console.log(
    "This will test working patterns, failing patterns, and edge cases..."
  );

  try {
    // Document initial UI state
    console.log("\n1️⃣ Documenting initial UI state...");
    documentUIBehavior();

    // Test working patterns (Tier 1)
    console.log("\n2️⃣ Testing working patterns (Tier 1: Direct Response)...");
    await testWorkingPatterns();

    // Test failing patterns (Tier 2)
    console.log(
      "\n3️⃣ Testing failing patterns (Tier 2: Orchestration-Dependent)..."
    );
    await testFailingPatterns();

    // Test edge cases (Bypass boundaries)
    console.log("\n4️⃣ Testing edge cases (Bypass boundaries)...");
    await testEdgeCases();

    // Final UI state check
    console.log("\n5️⃣ Final UI behavior documentation...");
    documentUIBehavior();

    console.log("\n✅ === PHASE 1A TESTING SUITE COMPLETE ===");

    const summary = {
      workingPatterns: Object.keys(window.phase1Analysis.workingPatterns)
        .length,
      failingPatterns: Object.keys(window.phase1Analysis.failingPatterns)
        .length,
      edgeCases: Object.keys(window.phase1Analysis.edgeCases).length,
      networkRequests: window.phase1Analysis.networkAnalysis.length,
      uiBehaviorChecks: window.phase1Analysis.uiBehavior.length,
      timestamp: new Date().toISOString(),
    };

    console.log("\n📊 PHASE 1A SUMMARY:", summary);
    return summary;
  } catch (error) {
    console.error("❌ Phase 1A testing suite failed:", error);
    return { error: error.message };
  }
};

// Export Phase 1 analysis data
window.exportPhase1Data = function () {
  const fullData = {
    ...window.phase1Analysis,
    networkRequests: phase1NetworkMonitor,
    exportTimestamp: new Date().toISOString(),
    userAgent: navigator.userAgent,
    url: window.location.href,
    phase: "Phase 1A - Current Functionality Mapping",
  };

  console.log("\n📋 === PHASE 1A DATA EXPORT ===");
  console.log(JSON.stringify(fullData, null, 2));

  // Copy to clipboard if possible
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(JSON.stringify(fullData, null, 2))
      .then(() => console.log("✅ Phase 1A data copied to clipboard"))
      .catch(() => console.log("⚠️ Could not copy to clipboard"));
  }

  return fullData;
};

console.log("\n🎯 Phase 1 UI Testing Framework Loaded!");
console.log("📋 Usage:");
console.log("- runPhase1ATesting() - Run complete Phase 1A testing suite");
console.log("- testWorkingPatterns() - Test Tier 1 working patterns");
console.log("- testFailingPatterns() - Test Tier 2 failing patterns");
console.log("- testEdgeCases() - Test bypass boundary edge cases");
console.log("- documentUIBehavior() - Check current UI state");
console.log("- exportPhase1Data() - Export all Phase 1 analysis data");
console.log("\n🔍 Ready for comprehensive workaround system analysis!");
