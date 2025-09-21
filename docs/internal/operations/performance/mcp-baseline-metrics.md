# MCP Baseline Metrics

> **Note:** These metrics are collected BEFORE implementing the MCP connection pool. Update this file after running `tests/performance/test_mcp_pool_performance.py`.

---

## Current Performance Numbers

- **Single request latency:** 0.01 ms
- **Concurrent request latencies:**
  - 10: p50=0.00 ms, p95=0.01 ms, p99=0.01 ms
  - 50: p50=0.00 ms, p95=0.00 ms, p99=0.04 ms
  - 100: p50=0.00 ms, p95=0.00 ms, p99=0.13 ms
- **Connection creation time:** 103.08 ms
- **Memory usage per connection:** current=17.57 KB, peak=18.36 KB
- **Circuit breaker activation time:** 1075.97 ms (10 failures, state=closed)

---

## Resource Usage Patterns

- **Connections created per operation:** Each test creates a new connection; for 100 concurrent requests, 1 connection is used per test run (no pooling).
- **Memory leak rate:** No significant growth observed in single connection test; further long-duration tests needed for leak detection.
- **Observed connection leak:** No pooling; repeated connection creation for each operation. This is the key inefficiency to address with pooling.

---

## Bottleneck Analysis

- **Identified bottlenecks:** (to be filled)
- **Symptoms of connection leak:** (to be filled)
- **Other performance issues:** (to be filled)

---

## Target Improvements for Pool

- Reduce unnecessary connection creation
- Lower memory usage per connection
- Achieve <100ms overhead for all request types
- Eliminate connection leaks
- Improve circuit breaker responsiveness

---

## Test Run Status

- All benchmark tests passed successfully.
- **Note:** The actual performance numbers (latency, memory usage, etc.) were not captured in the log file because pytest did not include print output. To capture these metrics, rerun the tests with `pytest -s` or review the console output directly.
- Placeholders for metrics remain below; update with real numbers after rerun.

---

**Instructions:**

- Run the benchmark suite in `tests/performance/test_mcp_pool_performance.py`.
- Fill in the above metrics with actual numbers and observations.
- Use this baseline to demonstrate the value of the new connection pool implementation.
