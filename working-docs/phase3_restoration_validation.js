// Phase 3 Restoration Validation Framework
// Date: September 18, 2025
// Mission: Validate OrchestrationEngine restoration success
// Agent: Cursor Agent (Phase 3)

console.log("=== PHASE 3 RESTORATION VALIDATION FRAMEWORK ===");
console.log("Date:", new Date().toISOString());
console.log("Mission: Validate OrchestrationEngine restoration success");

// Results storage for Phase 3 validation
window.phase3Validation = {
  restorationProgress: {},
  tier1Preservation: {},
  tier2Restoration: {},
  performanceComparison: {},
  pm039Patterns: {},
  errorHandling: {},
  timestamp: new Date().toISOString(),
};

// Enhanced network monitoring for restoration validation
const phase3NetworkMonitor = [];
let phase3OriginalFetch = null;

// Only override fetch if not already done for Phase 3
if (!window.phase3FetchOverridden) {
  phase3OriginalFetch = window.fetch;

  window.fetch = function (...args) {
    const startTime = performance.now();
    const requestInfo = {
      url: args[0],
      method: args[1]?.method || "GET",
      body: args[1]?.body,
      timestamp: new Date().toISOString(),
      startTime: startTime,
      phase: "Phase 3 Validation",
    };

    console.log(
      `🌐 [PHASE3] Request: ${requestInfo.method} ${requestInfo.url}`
    );

    return phase3OriginalFetch
      .apply(this, args)
      .then((response) => {
        const endTime = performance.now();
        requestInfo.status = response.status;
        requestInfo.statusText = response.statusText;
        requestInfo.timing = endTime - startTime;
        requestInfo.success = response.ok;
        requestInfo.headers = Object.fromEntries(response.headers);

        phase3NetworkMonitor.push(requestInfo);

        console.log(
          `✅ [PHASE3] Response: ${
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

        phase3NetworkMonitor.push(requestInfo);

        console.log(
          `❌ [PHASE3] Error: ${
            requestInfo.error
          } (${requestInfo.timing.toFixed(2)}ms)`
        );

        throw error;
      });
  };

  window.phase3FetchOverridden = true;
  console.log("✅ Phase 3 restoration validation monitoring enabled");
}

// Test individual intent pattern with comprehensive analysis
async function testIntentWithTiming(pattern) {
  const startTime = performance.now();

  try {
    const response = await fetch("/api/v1/intent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: pattern,
        session_id: `phase3-validation-${Date.now()}`,
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
      timestamp: new Date().toISOString(),
    };

    try {
      result.jsonResponse = JSON.parse(responseText);

      // Analyze response characteristics
      result.category = result.jsonResponse.intent?.category;
      result.action = result.jsonResponse.intent?.action;
      result.workflow_id = result.jsonResponse.workflow_id;
      result.message = result.jsonResponse.message;
      result.error = result.jsonResponse.detail;

      // Determine tier and success
      if (result.workflow_id === null && result.responseTime < 500) {
        result.tier = "tier1_bypass";
        result.success = !result.error;
      } else if (result.workflow_id !== null || result.responseTime >= 500) {
        result.tier = "tier2_orchestration";
        result.success =
          !result.error && result.jsonResponse.message !== undefined;
      } else {
        result.tier = "unknown";
        result.success = false;
      }

      // Check for restoration success
      if (result.error === "Failed to process intent") {
        result.restorationStatus = "still_broken";
      } else if (result.success) {
        result.restorationStatus = "restored";
      } else {
        result.restorationStatus = "partial";
      }
    } catch (parseError) {
      result.parseError = parseError.message;
      result.success = false;
      result.restorationStatus = "error";
    }

    return result;
  } catch (networkError) {
    const endTime = performance.now();
    return {
      pattern: pattern,
      networkError: networkError.message,
      responseTime: Math.round(endTime - startTime),
      success: false,
      restorationStatus: "network_error",
      timestamp: new Date().toISOString(),
    };
  }
}

// Validate Tier 1 bypass preservation
window.validateTier1Preservation = async function () {
  console.log("\n🔍 === VALIDATING TIER 1 BYPASS PRESERVATION ===");

  const tier1Patterns = [
    "hello",
    "hi",
    "good morning",
    "thank you",
    "goodbye",
    "help with my project",
  ];

  const results = {};
  let allPreserved = true;

  for (const pattern of tier1Patterns) {
    console.log(`\nTesting Tier 1 preservation: "${pattern}"`);
    const result = await testIntentWithTiming(pattern);

    // Validate bypass characteristics
    const issues = [];

    if (result.workflow_id !== null) {
      issues.push(`Has workflow_id: ${result.workflow_id} (should be null)`);
      allPreserved = false;
    }

    if (result.responseTime > 500) {
      issues.push(`Slow response: ${result.responseTime}ms (should be <500ms)`);
      allPreserved = false;
    }

    if (result.category && result.category !== "conversation") {
      issues.push(
        `Wrong category: ${result.category} (should be conversation)`
      );
    }

    if (result.error) {
      issues.push(`Has error: ${result.error}`);
      allPreserved = false;
    }

    results[pattern] = {
      ...result,
      issues: issues,
      preserved: issues.length === 0,
    };

    if (issues.length === 0) {
      console.log(
        `✅ "${pattern}": TIER 1 PRESERVED (${result.responseTime}ms)`
      );
    } else {
      console.log(`❌ "${pattern}": TIER 1 ISSUES - ${issues.join(", ")}`);
    }

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 500));
  }

  console.log(
    `\n📊 Tier 1 Preservation Summary: ${
      allPreserved ? "ALL PRESERVED ✅" : "ISSUES DETECTED ❌"
    }`
  );
  window.phase3Validation.tier1Preservation = { results, allPreserved };
  return results;
};

// Validate Tier 2 orchestration restoration
window.validateTier2Restoration = async function () {
  console.log("\n🔍 === VALIDATING TIER 2 ORCHESTRATION RESTORATION ===");

  const tier2Patterns = [
    { pattern: "show standup", expectedType: "report_generation" },
    { pattern: "show me my standup", expectedType: "report_generation" },
    { pattern: "list projects", expectedType: "query_execution" },
    { pattern: "create task", expectedType: "task_creation" },
    { pattern: "debug issue", expectedType: "analysis" },
    { pattern: "analyze project", expectedType: "analysis" },
  ];

  const results = {};
  let restoredCount = 0;

  for (const test of tier2Patterns) {
    console.log(`\nTesting Tier 2 restoration: "${test.pattern}"`);
    const result = await testIntentWithTiming(test.pattern);

    // Analyze restoration success
    const analysis = {
      ...result,
      expectedType: test.expectedType,
      issues: [],
    };

    if (result.error === "Failed to process intent") {
      analysis.issues.push("Still returning generic error");
      analysis.restored = false;
    } else if (result.workflow_id === null) {
      analysis.issues.push("Missing workflow_id (orchestration not triggered)");
      analysis.restored = false;
    } else if (result.responseTime > 5000) {
      analysis.issues.push(`Timeout: ${result.responseTime}ms`);
      analysis.restored = false;
    } else if (!result.success) {
      analysis.issues.push("Response indicates failure");
      analysis.restored = false;
    } else {
      analysis.restored = true;
      restoredCount++;
    }

    results[test.pattern] = analysis;

    if (analysis.restored) {
      console.log(`✅ "${test.pattern}": RESTORED (${result.responseTime}ms)`);
    } else {
      console.log(
        `❌ "${test.pattern}": STILL BROKEN - ${analysis.issues.join(", ")}`
      );
    }

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  const restorationRate = Math.round(
    (restoredCount / tier2Patterns.length) * 100
  );
  console.log(
    `\n📊 Tier 2 Restoration Summary: ${restoredCount}/${tier2Patterns.length} restored (${restorationRate}%)`
  );

  window.phase3Validation.tier2Restoration = {
    results,
    restoredCount,
    totalCount: tier2Patterns.length,
    restorationRate,
  };

  return results;
};

// Validate PM-039 historical pattern restoration
window.validatePM039Restoration = async function () {
  console.log("\n🎯 === VALIDATING PM-039 SEARCH PATTERN RESTORATION ===");
  console.log("Testing patterns that worked in July 2025...");

  const pm039Patterns = [
    "search for project documentation",
    "find technical specs",
    "search documents about architecture",
    "find meeting notes",
    "search for standup updates",
    "locate API documentation",
  ];

  const results = {};
  let workingCount = 0;

  for (const pattern of pm039Patterns) {
    console.log(`\nTesting PM-039 pattern: "${pattern}"`);
    const result = await testIntentWithTiming(pattern);

    // Analyze PM-039 restoration
    const analysis = {
      ...result,
      expectedAction: "search_documents",
      pm039Working: false,
    };

    if (result.success && result.action === "search_documents") {
      analysis.pm039Working = true;
      workingCount++;
      console.log(`✅ "${pattern}": PM-039 RESTORED - document search working`);
    } else if (result.success && result.message && !result.error) {
      analysis.pm039Working = "partial";
      console.log(
        `⚠️ "${pattern}": PM-039 PARTIAL - working but different action`
      );
    } else {
      analysis.pm039Working = false;
      console.log(
        `❌ "${pattern}": PM-039 NOT RESTORED - ${
          result.error || "no response"
        }`
      );
    }

    results[pattern] = analysis;

    // Small delay between tests
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  const pm039Rate = Math.round((workingCount / pm039Patterns.length) * 100);
  console.log(
    `\n📊 PM-039 Restoration Summary: ${workingCount}/${pm039Patterns.length} working (${pm039Rate}%)`
  );

  window.phase3Validation.pm039Patterns = {
    results,
    workingCount,
    totalCount: pm039Patterns.length,
    pm039Rate,
  };

  return results;
};

// Monitor restoration progress in real-time
window.monitorRestoration = function () {
  console.log("\n🔍 === STARTING RESTORATION MONITORING ===");
  console.log("Monitoring OrchestrationEngine restoration progress...");

  let monitoringInterval;

  const runMonitoringCycle = async () => {
    console.log(`\n⏰ Restoration check: ${new Date().toLocaleTimeString()}`);

    // Quick test of key patterns
    const keyTests = [
      { pattern: "hello", expected: "tier1_bypass" },
      { pattern: "show standup", expected: "tier2_restoration" },
    ];

    for (const test of keyTests) {
      const result = await testIntentWithTiming(test.pattern);

      if (test.expected === "tier1_bypass") {
        if (result.tier === "tier1_bypass" && result.success) {
          console.log(`✅ Tier 1 preserved: "${test.pattern}"`);
        } else {
          console.log(
            `⚠️ Tier 1 issue: "${test.pattern}" - ${result.restorationStatus}`
          );
        }
      } else if (test.expected === "tier2_restoration") {
        if (result.restorationStatus === "restored") {
          console.log(
            `🎉 Tier 2 restored: "${test.pattern}" - OrchestrationEngine working!`
          );
          clearInterval(monitoringInterval);
          console.log(
            "🚀 RESTORATION DETECTED - Running full validation suite..."
          );
          setTimeout(runPhase3ValidationSuite, 2000);
        } else {
          console.log(
            `⏳ Tier 2 pending: "${test.pattern}" - ${result.restorationStatus}`
          );
        }
      }
    }
  };

  // Run monitoring every 2 minutes
  monitoringInterval = setInterval(runMonitoringCycle, 2 * 60 * 1000);

  // Run first check immediately
  runMonitoringCycle();

  console.log(
    "📊 Monitoring started - checking every 2 minutes for restoration progress"
  );
  return monitoringInterval;
};

// Complete Phase 3 validation suite
window.runPhase3ValidationSuite = async function () {
  console.log("\n🚀 === RUNNING COMPLETE PHASE 3 VALIDATION SUITE ===");
  console.log("Comprehensive restoration validation starting...");

  try {
    // 1. Tier 1 Preservation Validation
    console.log("\n1️⃣ Validating Tier 1 bypass preservation...");
    await validateTier1Preservation();

    // 2. Tier 2 Restoration Validation
    console.log("\n2️⃣ Validating Tier 2 orchestration restoration...");
    await validateTier2Restoration();

    // 3. PM-039 Pattern Validation
    console.log("\n3️⃣ Validating PM-039 historical patterns...");
    await validatePM039Restoration();

    console.log("\n✅ === PHASE 3 VALIDATION SUITE COMPLETE ===");

    const summary = generateValidationSummary();
    console.log("\n📊 VALIDATION SUMMARY:", summary);

    return summary;
  } catch (error) {
    console.error("❌ Phase 3 validation suite failed:", error);
    return { error: error.message };
  }
};

// Generate comprehensive validation summary
function generateValidationSummary() {
  const tier1 = window.phase3Validation.tier1Preservation;
  const tier2 = window.phase3Validation.tier2Restoration;
  const pm039 = window.phase3Validation.pm039Patterns;

  return {
    tier1Preservation: tier1?.allPreserved ? "PRESERVED" : "ISSUES",
    tier2Restoration: tier2?.restorationRate || 0,
    pm039Patterns: pm039?.pm039Rate || 0,
    overallStatus: determineOverallStatus(),
    timestamp: new Date().toISOString(),
    networkRequests: phase3NetworkMonitor.length,
  };
}

function determineOverallStatus() {
  const tier1 = window.phase3Validation.tier1Preservation?.allPreserved;
  const tier2Rate =
    window.phase3Validation.tier2Restoration?.restorationRate || 0;

  if (tier1 && tier2Rate >= 80) {
    return "RESTORATION_SUCCESS";
  } else if (tier1 && tier2Rate >= 50) {
    return "RESTORATION_PARTIAL";
  } else if (!tier1) {
    return "REGRESSION_DETECTED";
  } else {
    return "RESTORATION_FAILED";
  }
}

// Export Phase 3 validation data
window.exportPhase3ValidationData = function () {
  const fullData = {
    ...window.phase3Validation,
    networkRequests: phase3NetworkMonitor,
    summary: generateValidationSummary(),
    exportTimestamp: new Date().toISOString(),
    userAgent: navigator.userAgent,
    url: window.location.href,
    phase: "Phase 3 - Restoration Validation & Testing",
  };

  console.log("\n📋 === PHASE 3 VALIDATION DATA EXPORT ===");
  console.log(JSON.stringify(fullData, null, 2));

  // Copy to clipboard if possible
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(JSON.stringify(fullData, null, 2))
      .then(() => console.log("✅ Phase 3 validation data copied to clipboard"))
      .catch(() => console.log("⚠️ Could not copy to clipboard"));
  }

  return fullData;
};

console.log("\n🎯 Phase 3 Restoration Validation Framework Loaded!");
console.log("📋 Usage:");
console.log("- monitorRestoration() - Start real-time restoration monitoring");
console.log("- runPhase3ValidationSuite() - Run complete validation suite");
console.log("- validateTier1Preservation() - Test Tier 1 bypass preservation");
console.log(
  "- validateTier2Restoration() - Test Tier 2 orchestration restoration"
);
console.log("- validatePM039Restoration() - Test PM-039 historical patterns");
console.log("- exportPhase3ValidationData() - Export all validation results");
console.log("\n🔍 Ready to validate OrchestrationEngine restoration success!");
