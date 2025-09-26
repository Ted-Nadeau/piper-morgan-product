// Phase 3C Workflow Registry Validation Framework
// Date: September 18, 2025 - 17:22
// Mission: TDD support for workflow registry restoration
// Agent: Cursor Agent (Phase 3C TDD Support)

console.log("=== PHASE 3C WORKFLOW REGISTRY VALIDATION FRAMEWORK ===");
console.log("Date:", new Date().toISOString());
console.log("Mission: TDD support for workflow registry restoration");
console.log(
  "Context: Code Agent Phase 3C Step 4 - PM-039 registry patterns investigation"
);

// Results storage for Phase 3C validation
window.phase3cValidation = {
  baselineResults: {},
  registryRestoration: {},
  performanceImpact: {},
  realTimeMonitoring: [],
  beforeAfterComparison: {},
  timestamp: new Date().toISOString(),
};

// Enhanced network monitoring for registry validation
const phase3cNetworkMonitor = [];
let phase3cOriginalFetch = null;

// Registry-specific fetch monitoring
if (!window.phase3cFetchOverridden) {
  phase3cOriginalFetch = window.fetch;

  window.fetch = function (...args) {
    const startTime = performance.now();
    const requestInfo = {
      url: args[0],
      method: args[1]?.method || "GET",
      body: args[1]?.body,
      timestamp: new Date().toISOString(),
      startTime: startTime,
      phase: "Phase 3C Registry Validation",
    };

    console.log(
      `🔧 [REGISTRY] Request: ${requestInfo.method} ${requestInfo.url}`
    );

    return phase3cOriginalFetch
      .apply(this, args)
      .then((response) => {
        const endTime = performance.now();
        requestInfo.status = response.status;
        requestInfo.statusText = response.statusText;
        requestInfo.timing = endTime - startTime;
        requestInfo.success = response.ok;
        requestInfo.headers = Object.fromEntries(response.headers);

        phase3cNetworkMonitor.push(requestInfo);

        console.log(
          `✅ [REGISTRY] Response: ${
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

        phase3cNetworkMonitor.push(requestInfo);

        console.log(
          `❌ [REGISTRY] Error: ${
            requestInfo.error
          } (${requestInfo.timing.toFixed(2)}ms)`
        );

        throw error;
      });
  };

  window.phase3cFetchOverridden = true;
  console.log("✅ Phase 3C registry validation monitoring enabled");
}

// Core testing function with workflow tracking
async function testIntentWithWorkflowTracking(message) {
  const startTime = performance.now();

  try {
    const response = await fetch("/api/v1/intent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: message,
        context: {},
        session_id: `registry-test-${Date.now()}`,
      }),
    });

    const endTime = performance.now();
    const responseTime = Math.round(endTime - startTime);
    const responseText = await response.text();

    const result = {
      message: message,
      status: response.status,
      responseTime: responseTime,
      responseText: responseText,
      timestamp: new Date().toISOString(),
    };

    try {
      result.jsonResponse = JSON.parse(responseText);

      // Extract key workflow registry indicators
      result.workflow_id = result.jsonResponse.workflow_id;
      result.category = result.jsonResponse.intent?.category;
      result.action = result.jsonResponse.intent?.action;
      result.confidence = result.jsonResponse.intent?.confidence;
      result.message_response = result.jsonResponse.message;
      result.error = result.jsonResponse.detail || result.jsonResponse.error;

      // Determine workflow creation success
      result.workflowCreated =
        result.workflow_id !== null && result.workflow_id !== undefined;
      result.success = response.ok && !result.error;

      // Registry-specific analysis
      if (result.workflowCreated) {
        result.registryStatus = "workflow_created";
      } else if (result.success && result.message_response) {
        result.registryStatus = "response_without_workflow";
      } else if (result.error) {
        result.registryStatus = "error";
      } else {
        result.registryStatus = "unknown";
      }
    } catch (parseError) {
      result.parseError = parseError.message;
      result.success = false;
      result.registryStatus = "parse_error";
    }

    return result;
  } catch (networkError) {
    const endTime = performance.now();
    return {
      message: message,
      networkError: networkError.message,
      responseTime: Math.round(endTime - startTime),
      success: false,
      registryStatus: "network_error",
      timestamp: new Date().toISOString(),
    };
  }
}

// Test current broken state (baseline)
window.testCurrentWorkflowMappings = async function () {
  console.log("\n🔍 === TESTING CURRENT WORKFLOW MAPPINGS (BASELINE) ===");
  console.log(
    "Documenting current broken state for before/after comparison..."
  );

  const failingPatterns = [
    "show standup",
    "show me my standup",
    "list projects",
    "create task",
    "debug issue",
    "analyze project",
  ];

  const results = {};

  for (const pattern of failingPatterns) {
    console.log(`\nTesting baseline: "${pattern}"`);
    const result = await testIntentWithWorkflowTracking(pattern);

    console.log(`  Status: ${result.status}`);
    console.log(`  Response Time: ${result.responseTime}ms`);
    console.log(`  Workflow ID: ${result.workflow_id}`);
    console.log(`  Registry Status: ${result.registryStatus}`);

    if (result.workflow_id !== null) {
      console.warn(
        `⚠️ Unexpected: ${pattern} has workflow_id ${result.workflow_id}`
      );
    } else {
      console.log(
        `✅ Expected: ${pattern} has no workflow_id (baseline confirmed)`
      );
    }

    results[pattern] = result;

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 500));
  }

  console.log(
    `\n📊 Baseline Documentation Complete - ${
      Object.keys(results).length
    } patterns tested`
  );
  window.phase3cValidation.baselineResults = results;
  return results;
};

// Validate workflow registry restoration
window.validateWorkflowRegistryRestoration = async function () {
  console.log("\n🔍 === VALIDATING WORKFLOW REGISTRY RESTORATION ===");
  console.log(
    "Testing for actual workflow creation after Code's registry changes..."
  );

  const testCases = [
    {
      pattern: "show standup",
      expectedCategory: "query",
      expectedAction: "show_standup",
      expectWorkflowId: true,
      description: "Standup generation workflow",
    },
    {
      pattern: "show me my standup",
      expectedCategory: "query",
      expectedAction: "show_standup",
      expectWorkflowId: true,
      description: "Alternative standup request",
    },
    {
      pattern: "list projects",
      expectedCategory: "query",
      expectedAction: "list_projects",
      expectWorkflowId: true,
      description: "Project listing workflow",
    },
    {
      pattern: "create task",
      expectedCategory: "execution",
      expectedAction: "create_task",
      expectWorkflowId: true,
      description: "Task creation workflow",
    },
  ];

  const results = {};
  let successCount = 0;

  for (const testCase of testCases) {
    console.log(`\nTesting registry restoration: "${testCase.pattern}"`);
    console.log(`  Expected: ${testCase.description}`);

    const result = await testIntentWithWorkflowTracking(testCase.pattern);

    console.log(
      `  Category: ${result.category} (expected: ${testCase.expectedCategory})`
    );
    console.log(
      `  Action: ${result.action} (expected: ${testCase.expectedAction})`
    );
    console.log(`  Workflow ID: ${result.workflow_id}`);
    console.log(`  Response Time: ${result.responseTime}ms`);

    // Validation checks
    const categoryMatch = result.category === testCase.expectedCategory;
    const actionMatch = result.action === testCase.expectedAction;
    const workflowCreated = testCase.expectWorkflowId
      ? result.workflow_id !== null && result.workflow_id !== undefined
      : result.workflow_id === null;

    const testPassed =
      categoryMatch && actionMatch && workflowCreated && result.success;

    console.log(`  Result: ${testPassed ? "✅ PASSED" : "❌ FAILED"}`);

    if (!testPassed) {
      console.log(`  Issues:`);
      if (!categoryMatch)
        console.log(
          `    - Category mismatch: got ${result.category}, expected ${testCase.expectedCategory}`
        );
      if (!actionMatch)
        console.log(
          `    - Action mismatch: got ${result.action}, expected ${testCase.expectedAction}`
        );
      if (!workflowCreated)
        console.log(
          `    - Workflow not created: workflow_id is ${result.workflow_id}`
        );
      if (!result.success) console.log(`    - Request failed: ${result.error}`);
    } else {
      successCount++;
    }

    results[testCase.pattern] = {
      ...result,
      testCase: testCase,
      testPassed: testPassed,
      issues: !testPassed
        ? {
            categoryMatch,
            actionMatch,
            workflowCreated,
            requestSuccess: result.success,
          }
        : null,
    };

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  const successRate = Math.round((successCount / testCases.length) * 100);
  console.log(
    `\n📊 Registry Restoration Summary: ${successCount}/${testCases.length} restored (${successRate}%)`
  );

  window.phase3cValidation.registryRestoration = {
    results,
    successCount,
    totalCount: testCases.length,
    successRate,
  };

  return results;
};

// Validate performance impact
window.validatePerformanceImpact = async function () {
  console.log("\n⏱️ === VALIDATING PERFORMANCE IMPACT ===");
  console.log("Ensuring registry restoration doesn't break performance...");

  // Test Tier 1 (should remain fast)
  console.log("\n🚀 Testing Tier 1 performance preservation:");
  const tier1Patterns = ["hello", "thank you", "goodbye"];
  const tier1Results = {};

  for (const pattern of tier1Patterns) {
    const result = await testIntentWithWorkflowTracking(pattern);

    console.log(`  ${pattern}: ${result.responseTime}ms`);

    if (result.responseTime > 500) {
      console.warn(
        `  ⚠️ Tier 1 performance regression: ${pattern} took ${result.responseTime}ms (should be <500ms)`
      );
    } else {
      console.log(`  ✅ Good performance: ${pattern} within acceptable range`);
    }

    tier1Results[pattern] = result;
  }

  // Test Tier 2 (should be reasonable, not timeout)
  console.log("\n🔧 Testing Tier 2 performance improvement:");
  const tier2Patterns = ["show standup", "list projects", "create task"];
  const tier2Results = {};

  for (const pattern of tier2Patterns) {
    const result = await testIntentWithWorkflowTracking(pattern);

    console.log(`  ${pattern}: ${result.responseTime}ms`);

    if (result.responseTime > 10000) {
      console.warn(
        `  ⚠️ Tier 2 timeout risk: ${pattern} took ${result.responseTime}ms`
      );
    } else if (result.responseTime < 5000) {
      console.log(
        `  ✅ Good performance: ${pattern} completed in ${result.responseTime}ms`
      );
    } else {
      console.log(`  ⏳ Acceptable: ${pattern} within normal range`);
    }

    tier2Results[pattern] = result;
  }

  console.log(`\n📊 Performance Impact Analysis Complete`);

  window.phase3cValidation.performanceImpact = {
    tier1: tier1Results,
    tier2: tier2Results,
    timestamp: new Date().toISOString(),
  };

  return { tier1: tier1Results, tier2: tier2Results };
};

// Real-time monitoring for Code's implementation
window.monitorRegistryRestoration = function () {
  console.log("\n🔍 === STARTING REGISTRY RESTORATION MONITORING ===");
  console.log("Monitoring for workflow registry restoration progress...");
  console.log("Checking every 30 seconds for workflow_id creation...");

  let monitoringInterval;
  let checkCount = 0;

  const runMonitoringCheck = async () => {
    checkCount++;
    console.log(
      `\n⏰ Registry check #${checkCount}: ${new Date().toLocaleTimeString()}`
    );

    // Test key registry patterns
    const keyPatterns = ["show standup", "list projects"];
    let restorationDetected = false;

    for (const pattern of keyPatterns) {
      const result = await testIntentWithWorkflowTracking(pattern);

      if (result.workflow_id !== null && result.workflow_id !== undefined) {
        console.log(
          `🎉 BREAKTHROUGH: "${pattern}" now has workflow_id: ${result.workflow_id}!`
        );
        restorationDetected = true;
      } else {
        console.log(
          `⏳ Still pending: "${pattern}" - workflow_id: ${result.workflow_id}`
        );
      }

      // Store monitoring result
      window.phase3cValidation.realTimeMonitoring.push({
        checkNumber: checkCount,
        pattern: pattern,
        result: result,
        timestamp: new Date().toISOString(),
      });
    }

    if (restorationDetected) {
      console.log(
        "🚀 REGISTRY RESTORATION DETECTED - Running full validation suite..."
      );
      clearInterval(monitoringInterval);

      // Run complete validation
      setTimeout(async () => {
        await validateWorkflowRegistryRestoration();
        await validatePerformanceImpact();
        console.log("✅ Complete registry validation finished!");
      }, 2000);
    }
  };

  // Run monitoring every 30 seconds
  monitoringInterval = setInterval(runMonitoringCheck, 30 * 1000);

  // Run first check immediately
  runMonitoringCheck();

  // Auto-stop after 20 minutes
  setTimeout(() => {
    if (monitoringInterval) {
      clearInterval(monitoringInterval);
      console.log("⏰ Monitoring timeout - manual validation required");
    }
  }, 20 * 60 * 1000);

  console.log("📊 Registry monitoring started - will check every 30 seconds");
  return monitoringInterval;
};

// Generate before/after comparison
window.generateBeforeAfterComparison = function () {
  const baseline = window.phase3cValidation.baselineResults;
  const restoration = window.phase3cValidation.registryRestoration?.results;

  if (!baseline || !restoration) {
    console.warn(
      "⚠️ Cannot generate comparison - missing baseline or restoration data"
    );
    return null;
  }

  console.log("\n📊 === BEFORE/AFTER COMPARISON ===");

  const comparison = {};

  for (const pattern in baseline) {
    if (restoration[pattern]) {
      const before = baseline[pattern];
      const after = restoration[pattern];

      comparison[pattern] = {
        before: {
          workflow_id: before.workflow_id,
          responseTime: before.responseTime,
          registryStatus: before.registryStatus,
          success: before.success,
        },
        after: {
          workflow_id: after.workflow_id,
          responseTime: after.responseTime,
          registryStatus: after.registryStatus,
          success: after.success,
        },
        improvement: {
          workflowCreated:
            before.workflow_id === null && after.workflow_id !== null,
          performanceChange: after.responseTime - before.responseTime,
          statusImproved:
            before.registryStatus !== "workflow_created" &&
            after.registryStatus === "workflow_created",
        },
      };

      console.log(`\n"${pattern}":`);
      console.log(
        `  Before: workflow_id=${before.workflow_id}, ${before.responseTime}ms, ${before.registryStatus}`
      );
      console.log(
        `  After:  workflow_id=${after.workflow_id}, ${after.responseTime}ms, ${after.registryStatus}`
      );

      if (comparison[pattern].improvement.workflowCreated) {
        console.log(`  ✅ RESTORED: Workflow now created`);
      } else {
        console.log(`  ❌ NOT RESTORED: Still no workflow creation`);
      }
    }
  }

  window.phase3cValidation.beforeAfterComparison = comparison;
  return comparison;
};

// Export all Phase 3C validation data
window.exportPhase3cValidationData = function () {
  const fullData = {
    ...window.phase3cValidation,
    networkRequests: phase3cNetworkMonitor,
    beforeAfterComparison: generateBeforeAfterComparison(),
    exportTimestamp: new Date().toISOString(),
    userAgent: navigator.userAgent,
    url: window.location.href,
    phase: "Phase 3C - Workflow Registry Validation & TDD Support",
  };

  console.log("\n📋 === PHASE 3C VALIDATION DATA EXPORT ===");
  console.log(JSON.stringify(fullData, null, 2));

  // Copy to clipboard if possible
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(JSON.stringify(fullData, null, 2))
      .then(() =>
        console.log("✅ Phase 3C validation data copied to clipboard")
      )
      .catch(() => console.log("⚠️ Could not copy to clipboard"));
  }

  return fullData;
};

console.log("\n🔧 Phase 3C Workflow Registry Validation Framework Loaded!");
console.log("📋 Usage Instructions:");
console.log(
  "- testCurrentWorkflowMappings() - Document current broken state (baseline)"
);
console.log(
  "- monitorRegistryRestoration() - Start real-time monitoring (30-second checks)"
);
console.log(
  "- validateWorkflowRegistryRestoration() - Test registry restoration success"
);
console.log(
  "- validatePerformanceImpact() - Ensure no performance regressions"
);
console.log("- generateBeforeAfterComparison() - Create before/after evidence");
console.log("- exportPhase3cValidationData() - Export all validation results");
console.log(
  "\n🎯 Ready to provide TDD support for Code Agent's workflow registry restoration!"
);
