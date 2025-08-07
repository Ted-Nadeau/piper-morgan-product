# PM-034 User Guide: Enhanced QueryRouter with LLM Intent Classification

**Project**: PM-034 Intent Classification Enhancement
**Date**: August 5, 2025
**Status**: ✅ Production Ready

## Overview

PM-034 enhances the QueryRouter with sophisticated LLM-based intent classification while maintaining backward compatibility and exceptional performance. This guide explains how to use the enhanced QueryRouter for A/B testing, performance monitoring, and gradual rollout of LLM capabilities.

## Key Features

### 🚀 Enhanced Intent Classification

- **LLM-based Classification**: Advanced natural language understanding
- **Rule-based Fallback**: Fast, reliable pattern matching
- **A/B Testing**: Gradual rollout with session consistency
- **Performance Monitoring**: Real-time metrics and target validation

### 🛡️ Graceful Degradation

- **Automatic Fallback**: Seamless transition to rule-based classification
- **Exception Handling**: Robust error handling and recovery
- **Performance Protection**: Circuit breaker patterns for reliability

### 📊 Comprehensive Monitoring

- **Real-time Metrics**: Detailed performance tracking
- **A/B Testing Analytics**: Rollout percentage and assignment tracking
- **Target Violation Detection**: Automatic performance issue identification

## Basic Usage

### Creating an Enhanced QueryRouter

```python
from services.queries.query_router import QueryRouter
from services.intent_service.llm_classifier import LLMIntentClassifier
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.knowledge.semantic_indexing_service import SemanticIndexingService

# Create enhanced QueryRouter with LLM capabilities
router = QueryRouter(
    project_query_service=project_service,
    conversation_query_service=conversation_service,
    file_query_service=file_service,

    # PM-034: LLM Intent Classification Integration
    llm_classifier=llm_classifier,
    knowledge_graph_service=knowledge_graph_service,
    semantic_indexing_service=semantic_indexing_service,
    enable_llm_classification=True,
    llm_rollout_percentage=0.5,  # 50% rollout
    performance_targets={
        "rule_based": 50.0,      # <50ms for rule-based
        "llm_classification": 200.0  # <200ms for LLM
    }
)
```

### Basic Classification and Routing

```python
# Enhanced classification with A/B testing
result = await router.classify_and_route(
    message="list all projects",
    user_context={"user_id": "user123"},
    session_id="session_456"
)
```

## A/B Testing Configuration

### Rollout Management

The enhanced QueryRouter supports gradual rollout of LLM classification:

```python
# Start with 0% LLM rollout (rule-based only)
router.update_rollout_percentage(0.0)

# Gradually increase rollout
router.update_rollout_percentage(0.25)  # 25% of users get LLM
router.update_rollout_percentage(0.50)  # 50% of users get LLM
router.update_rollout_percentage(0.75)  # 75% of users get LLM
router.update_rollout_percentage(1.0)   # 100% of users get LLM
```

### Session Consistency

A/B testing ensures consistent user experience:

```python
# Same session ID always gets same classification method
session_id = "user_123_session"

# First request
result1 = await router.classify_and_route("hello", {}, session_id)

# Second request (same session, same classification method)
result2 = await router.classify_and_route("help", {}, session_id)

# Both requests use the same classification method (LLM or rule-based)
```

### Rollout Percentage Validation

```python
# Valid percentages (0.0 to 1.0)
router.update_rollout_percentage(0.0)   # ✅ Valid
router.update_rollout_percentage(0.5)   # ✅ Valid
router.update_rollout_percentage(1.0)   # ✅ Valid

# Invalid percentages (rejected)
try:
    router.update_rollout_percentage(1.5)  # ❌ ValueError
except ValueError as e:
    print(f"Invalid rollout percentage: {e}")
```

## Performance Monitoring

### Getting Performance Metrics

```python
# Get comprehensive performance metrics
metrics = router.get_performance_metrics()

print(f"Total Requests: {metrics['total_requests']}")
print(f"LLM Classifications: {metrics['llm_classifications']}")
print(f"Rule-based Classifications: {metrics['rule_based_classifications']}")
print(f"Average LLM Latency: {metrics['average_llm_latency_ms']:.2f}ms")
print(f"Average Rule-based Latency: {metrics['average_rule_based_latency_ms']:.2f}ms")
print(f"Target Violations: {metrics['target_violations']}")
print(f"LLM Rollout Percentage: {metrics['llm_rollout_percentage']:.1%}")
```

### Performance Target Monitoring

```python
# Check if performance targets are being met
metrics = router.get_performance_metrics()

if metrics['target_violations'] > 0:
    print(f"⚠️ Performance target violations detected: {metrics['target_violations']}")

    # Check specific latencies
    if metrics['average_llm_latency_ms'] > metrics['performance_targets']['llm_classification']:
        print("⚠️ LLM classification exceeding target latency")

    if metrics['average_rule_based_latency_ms'] > metrics['performance_targets']['rule_based']:
        print("⚠️ Rule-based classification exceeding target latency")
```

### Real-time Monitoring Example

```python
import asyncio
import time

async def monitor_performance(router, duration_seconds=60):
    """Monitor performance for specified duration"""
    start_time = time.time()

    while time.time() - start_time < duration_seconds:
        metrics = router.get_performance_metrics()

        print(f"\n📊 Performance Snapshot ({time.strftime('%H:%M:%S')})")
        print(f"  Total Requests: {metrics['total_requests']}")
        print(f"  LLM Success Rate: {metrics['llm_success_rate']:.1%}")
        print(f"  Rule-based Success Rate: {metrics['rule_based_success_rate']:.1%}")
        print(f"  Target Violations: {metrics['target_violations']}")

        await asyncio.sleep(10)  # Update every 10 seconds

# Usage
await monitor_performance(router, duration_seconds=300)  # Monitor for 5 minutes
```

## Graceful Degradation

### Automatic Fallback

The enhanced QueryRouter automatically handles failures:

```python
# LLM classifier becomes unavailable
router.llm_classifier = None

# System automatically falls back to rule-based classification
result = await router.classify_and_route("hello", {}, "test_session")
# ✅ No error - automatic fallback to rule-based

# LLM classifier throws exception
router.llm_classifier.classify.side_effect = Exception("Service unavailable")

# System automatically falls back to rule-based classification
result = await router.classify_and_route("help", {}, "test_session")
# ✅ No error - automatic fallback to rule-based
```

### Performance Violation Detection

```python
# System automatically detects performance violations
metrics = router.get_performance_metrics()

if metrics['target_violations'] > 0:
    print(f"🚨 Performance violations detected: {metrics['target_violations']}")

    # Consider reducing rollout percentage
    current_rollout = metrics['llm_rollout_percentage']
    if current_rollout > 0.0:
        new_rollout = max(0.0, current_rollout - 0.25)
        router.update_rollout_percentage(new_rollout)
        print(f"📉 Reduced rollout to {new_rollout:.1%}")
```

## Deployment Strategies

### Phase 1: Safe Deployment (0% LLM)

```python
# Deploy with 0% LLM rollout for safety
router = QueryRouter(
    # ... other services ...
    enable_llm_classification=True,
    llm_rollout_percentage=0.0,  # Start with 0% LLM
)

# Monitor rule-based performance
metrics = router.get_performance_metrics()
print(f"Rule-based performance: {metrics['average_rule_based_latency_ms']:.2f}ms")
```

### Phase 2: Gradual Rollout

```python
# Gradually increase LLM rollout
rollout_stages = [0.25, 0.50, 0.75, 1.0]

for rollout in rollout_stages:
    print(f"🚀 Increasing rollout to {rollout:.0%}")
    router.update_rollout_percentage(rollout)

    # Monitor for 5 minutes
    await monitor_performance(router, duration_seconds=300)

    # Check for issues
    metrics = router.get_performance_metrics()
    if metrics['target_violations'] > 5:
        print(f"⚠️ Too many violations, rolling back to {rollout - 0.25:.0%}")
        router.update_rollout_percentage(rollout - 0.25)
        break
```

### Phase 3: Production Monitoring

```python
# Continuous monitoring in production
async def production_monitor(router):
    while True:
        metrics = router.get_performance_metrics()

        # Alert on performance issues
        if metrics['target_violations'] > 10:
            print("🚨 CRITICAL: High number of performance violations")
            # Send alert to monitoring system

        # Alert on high latency
        if metrics['average_llm_latency_ms'] > 150:
            print("⚠️ WARNING: LLM latency approaching target")

        await asyncio.sleep(30)  # Check every 30 seconds

# Start monitoring
asyncio.create_task(production_monitor(router))
```

## Backward Compatibility

### Existing Code Compatibility

The enhanced QueryRouter maintains full backward compatibility:

```python
# Existing code continues to work unchanged
router = QueryRouter(
    project_query_service=project_service,
    conversation_query_service=conversation_service,
    file_query_service=file_service,
    test_mode=False,
    # No LLM parameters = backward compatible mode
)

# Existing methods work as before
result = await router.route_query(intent)
```

### Test Mode Compatibility

```python
# Test mode continues to work
router = QueryRouter(
    # ... services ...
    test_mode=True,  # PM-063: Backward compatibility
    enable_llm_classification=False,  # Disable LLM in test mode
)

# Test mode behavior preserved
result = await router.route_query(intent)
```

## Best Practices

### 1. Gradual Rollout

- Start with 0% LLM rollout
- Increase gradually (25%, 50%, 75%, 100%)
- Monitor performance at each stage
- Be prepared to rollback if issues arise

### 2. Performance Monitoring

- Monitor target violations continuously
- Set up alerts for performance issues
- Track success rates for both classification methods
- Monitor latency trends over time

### 3. Session Management

- Always provide session_id for consistent A/B testing
- Use stable session identifiers (user ID, session token)
- Avoid changing session IDs within user sessions

### 4. Error Handling

- Trust the automatic fallback mechanisms
- Monitor for graceful degradation events
- Have manual rollback procedures ready
- Log degradation events for analysis

### 5. Configuration Management

- Validate rollout percentages (0.0-1.0)
- Use environment variables for configuration
- Document configuration changes
- Test configuration changes in staging

## Troubleshooting

### Common Issues

#### High Target Violations

```python
# Check performance metrics
metrics = router.get_performance_metrics()

if metrics['target_violations'] > 0:
    # Reduce rollout percentage
    current = metrics['llm_rollout_percentage']
    router.update_rollout_percentage(max(0.0, current - 0.25))

    # Check if LLM service is healthy
    if not metrics['llm_classifier_available']:
        print("🚨 LLM classifier unavailable")
```

#### Inconsistent A/B Testing

```python
# Ensure session_id is provided
result = await router.classify_and_route(
    message="test",
    user_context={},
    session_id="consistent_session_id"  # ✅ Required for consistency
)

# Check rollout percentage
metrics = router.get_performance_metrics()
print(f"Current rollout: {metrics['llm_rollout_percentage']:.1%}")
```

#### Performance Degradation

```python
# Monitor latency trends
metrics = router.get_performance_metrics()

if metrics['average_llm_latency_ms'] > 150:
    print("⚠️ LLM latency high, consider reducing rollout")
    router.update_rollout_percentage(0.0)  # Fallback to rule-based
```

## Conclusion

The enhanced QueryRouter provides powerful LLM-based intent classification while maintaining exceptional performance and reliability. Use the gradual rollout strategy and comprehensive monitoring to safely deploy and operate the enhanced system.

**Key Takeaways**:

- ✅ Start with 0% LLM rollout for safety
- ✅ Use session IDs for consistent A/B testing
- ✅ Monitor performance metrics continuously
- ✅ Trust automatic fallback mechanisms
- ✅ Maintain backward compatibility

**Status**: ✅ **PRODUCTION READY**
**Next Steps**: Deploy with 0% rollout and gradually increase based on monitoring results.
