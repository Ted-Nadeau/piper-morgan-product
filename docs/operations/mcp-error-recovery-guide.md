# MCP Error Recovery Operations Guide

## Overview

Guide for operators on MCP error handling and recovery patterns.

## Error Scenarios and Responses

### Extraction Failures

- **Symptom**: PDF/file extraction errors
- **Automatic Response**: Falls back to filename search
- **Manual Action**: Check file corruption, disk space

### Performance Degradation

- **Symptom**: Search latency > 300ms
- **Automatic Response**: Progressive feature reduction
- **Manual Action**: Check system load, scale if needed

### Circuit Breaker Trips

- **Symptom**: Connection pool failures
- **Automatic Response**: Circuit opens, periodic retry
- **Manual Action**: Check MCP server status

## Alert Thresholds

- **Error Rate Warning**: 5%
- **Error Rate Critical**: 10%
- **Latency Warning**: 300ms
- **Latency Critical**: 500ms
- **Extraction Failure Rate**: 20%

## Recovery Procedures

### Extraction Failure

1. System falls back to filename search automatically.
2. Operator should check for file corruption or disk space issues.
3. If persistent, escalate to engineering.

### Performance Degradation

1. System disables TF-IDF scoring at 200ms latency.
2. Limits concurrent extractions at 400ms.
3. Switches to cache-only mode at 500ms.
4. Operator should check system load and consider scaling resources.

### Circuit Breaker

1. Circuit opens after repeated connection failures.
2. System attempts lightweight recovery operations periodically.
3. Operator should check MCP server/network status.
4. Once healthy, system resumes normal operation.

## Monitoring Dashboard

- **Error Rates**: Watch for spikes above warning/critical thresholds.
- **Performance**: Monitor p50/p95/p99 latency.
- **Health Status**: Should be 'healthy' or 'degraded'; investigate 'unhealthy'.
- **Recovery**: Track fallback and circuit breaker events, recovery success rate.
