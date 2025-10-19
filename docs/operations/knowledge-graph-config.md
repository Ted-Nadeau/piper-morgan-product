# Knowledge Graph Configuration Guide

## Environment Variables

### Core Settings

```bash
# Feature Flag
ENABLE_KNOWLEDGE_GRAPH=true    # Enable/disable KG enhancement

# Performance
KNOWLEDGE_GRAPH_TIMEOUT_MS=100  # Query timeout (milliseconds)
KNOWLEDGE_GRAPH_CACHE_TTL=300   # Cache TTL (seconds)
```

**Location**: `.env` file in project root

### Default Values

If not set, defaults are:
- `ENABLE_KNOWLEDGE_GRAPH`: `false` (safe default for gradual rollout)
- `KNOWLEDGE_GRAPH_TIMEOUT_MS`: `100`
- `KNOWLEDGE_GRAPH_CACHE_TTL`: `300`

### Applying Changes

```bash
# 1. Update .env file
nano .env

# 2. Restart service to apply changes
# (No code deployment needed)

# 3. Verify settings loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(f'KG={os.getenv(\"ENABLE_KNOWLEDGE_GRAPH\")}')"
```

## Boundary Configurations

Boundaries are defined in `services/knowledge/boundaries.py` and can be modified by editing the file.

### SEARCH Boundaries (Conversation)

```python
SEARCH = GraphBoundaries(
    max_depth=3,              # Shallow search for speed
    max_nodes_visited=500,    # Moderate node count
    max_time_ms=2000,         # 2 second max
    query_timeout_ms=100,     # 100ms quick queries
    max_result_size=50        # Top 50 results
)
```

**Use Case**: Real-time conversation context enhancement

**Characteristics**:
- Optimized for speed (<100ms target)
- Limited depth to prevent deep traversal
- Moderate node count for quick results
- Ideal for interactive conversation

### TRAVERSAL Boundaries (Exploration)

```python
TRAVERSAL = GraphBoundaries(
    max_depth=5,              # Deeper exploration
    max_nodes_visited=1000,   # More nodes allowed
    max_time_ms=5000,         # 5 second max
    query_timeout_ms=500,     # 500ms queries
    max_result_size=100       # Top 100 results
)
```

**Use Case**: Interactive graph exploration by users

**Characteristics**:
- Deeper traversal allowed
- More comprehensive results
- Moderate timeout for better coverage
- Suitable for exploration features

### ANALYSIS Boundaries (Admin)

```python
ANALYSIS = GraphBoundaries(
    max_depth=10,             # Deep analysis
    max_nodes_visited=5000,   # Many nodes allowed
    max_time_ms=10000,        # 10 second max
    query_timeout_ms=2000,    # 2000ms queries
    max_result_size=500       # Top 500 results
)
```

**Use Case**: Admin analytics and background reports

**Characteristics**:
- Maximum depth for comprehensive analysis
- Large node count for complete picture
- Longer timeout acceptable for background jobs
- Not for real-time user queries

## Tuning Guidelines

### If Queries Too Slow

**Symptoms**:
- Logs show timeouts
- Users experience lag
- Response time >500ms

**Solutions**:
1. **Reduce `max_depth`** (less traversal)
   - Try reducing by 1-2 levels
   - Most queries don't need depth >3

2. **Reduce `max_nodes_visited`** (less data)
   - Start with 50% reduction
   - Monitor partial result warnings

3. **Increase database indexes**
   - Verify indexes exist (see Database Configuration)
   - Add indexes on frequently queried fields

4. **Check cache hit rate**
   - Should be >80% for warm cache
   - If low, increase `KNOWLEDGE_GRAPH_CACHE_TTL`

### If Results Incomplete

**Symptoms**:
- Logs show "max nodes reached"
- Users report missing information
- Partial results warning

**Solutions**:
1. **Increase `max_nodes_visited`**
   - Try 2x current value
   - Monitor performance impact

2. **Increase `max_depth`**
   - Add 1-2 levels
   - Watch for performance degradation

3. **Increase `max_result_size`**
   - For queries returning many results
   - Consider pagination instead

4. **Refine queries to be more specific**
   - Use session filtering
   - Use node type filtering
   - Add search terms

### If Memory Issues

**Symptoms**:
- High memory usage
- OOM (Out of Memory) errors
- System slowdown

**Solutions**:
1. **Decrease `max_nodes_visited`**
   - Reduce to 50% of current
   - Critical for memory control

2. **Decrease `max_result_size`**
   - Limit data returned
   - Implement pagination

3. **Add pagination for large results**
   - Return results in batches
   - Offset/limit pattern

4. **Monitor boundary violations**
   - Track "max nodes reached" warnings
   - Tune based on actual usage patterns

## Database Configuration

### Indexes (Created in Phase 1)

PostgreSQL indexes for optimal performance:

```sql
-- Node queries
CREATE INDEX idx_nodes_type ON knowledge_nodes(node_type);
CREATE INDEX idx_nodes_session ON knowledge_nodes(session_id);

-- Edge queries
CREATE INDEX idx_edges_source ON knowledge_edges(source_node_id);
CREATE INDEX idx_edges_target ON knowledge_edges(target_node_id);
```

**Verification**:
```bash
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\di knowledge*"
```

### Query Performance

Expected query times with indexes:
- Single node by ID: 0.4-0.6ms
- Nodes by type: 3-5ms (cached)
- Nodes by session: 3-5ms (cached)
- Traverse relationships: 10-50ms (depth-dependent)

### Database Maintenance

```sql
-- Vacuum tables periodically
VACUUM ANALYZE knowledge_nodes;
VACUUM ANALYZE knowledge_edges;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE tablename LIKE 'knowledge%'
ORDER BY idx_scan DESC;
```

## Monitoring Configuration

### What to Log/Monitor

**Performance Metrics**:
- KG enhancement success/failure rate (should be >99%)
- Query performance (p50, p95, p99)
- Cache hit rate (should be >80%)
- Boundary violation frequency

**Resource Metrics**:
- Memory usage per query
- Database query times
- Connection pool utilization

**Operational Metrics**:
- Feature flag status
- Error rates
- Timeout frequency

### Log Levels

**INFO** (normal operation):
```
Knowledge Graph enhancement enabled
Knowledge Graph enhancement successful
Traversal complete: {stats}
Search hit node count limit - results may be partial
```

**WARNING** (expected occasionally):
```
Depth limit exceeded: 3 >= 3
Node count limit exceeded: 500 >= 500
Time limit exceeded: 105ms >= 100ms
```

**ERROR** (investigate):
```
Knowledge Graph enhancement failed: {error}
Search failed with boundaries: {error}
```

### Alerting Thresholds

**Critical**:
- Error rate >1% (indicates system issue)
- Query time p95 >1000ms (performance degradation)
- Cache hit rate <50% (cache not working)

**Warning**:
- Error rate >0.1% (monitor closely)
- Query time p95 >500ms (approaching limits)
- Boundary violations >10% of queries (may need tuning)

## Advanced Configuration

### Custom Boundary Profiles

Create custom boundaries for specific use cases:

```python
# In services/knowledge/boundaries.py

# Quick preview (minimal resources)
PREVIEW = GraphBoundaries(
    max_depth=2,
    max_nodes_visited=100,
    max_time_ms=1000,
    query_timeout_ms=50,
    max_result_size=20
)

# Deep investigation (admin tool)
INVESTIGATION = GraphBoundaries(
    max_depth=15,
    max_nodes_visited=10000,
    max_time_ms=30000,
    query_timeout_ms=5000,
    max_result_size=1000
)
```

### Session-Based Tuning

Different sessions may need different limits:

```python
# In KnowledgeGraphService
def __init__(self, ..., session_type=None):
    if session_type == "admin":
        self.kg_boundary_enforcer = KGBoundaryEnforcer(OperationBoundaries.ANALYSIS)
    elif session_type == "preview":
        self.kg_boundary_enforcer = KGBoundaryEnforcer(OperationBoundaries.SEARCH)
    else:
        # Default
        self.kg_boundary_enforcer = KGBoundaryEnforcer(OperationBoundaries.SEARCH)
```

### Dynamic Boundaries

Adjust boundaries based on load:

```python
# Pseudo-code example
current_load = get_system_load()
if current_load > 0.8:
    # Reduce limits under high load
    boundaries.max_nodes_visited = 250
    boundaries.max_depth = 2
else:
    # Normal limits
    boundaries.max_nodes_visited = 500
    boundaries.max_depth = 3
```

## Configuration Checklist

### Initial Setup

- [ ] Database tables created (Phase 1)
- [ ] Indexes verified
- [ ] `.env` file configured
- [ ] `ENABLE_KNOWLEDGE_GRAPH` set appropriately
- [ ] Service restarted
- [ ] Activation verified

### Performance Tuning

- [ ] Boundary limits reviewed
- [ ] Cache TTL configured
- [ ] Query timeout set
- [ ] Monitoring enabled
- [ ] Alert thresholds configured

### Production Deployment

- [ ] Feature flag tested (enable/disable)
- [ ] Rollback procedure documented
- [ ] Monitoring dashboards created
- [ ] Alert routing configured
- [ ] On-call runbook updated

## Troubleshooting Common Configurations

### Configuration Not Applied

**Problem**: Changes to .env don't take effect

**Solution**:
1. Verify file saved
2. Restart service completely
3. Check dotenv loading in code
4. Verify no environment variable override

### Boundaries Too Restrictive

**Problem**: Constant "max nodes reached" warnings

**Solution**:
1. Increase `max_nodes_visited` by 2x
2. Monitor memory usage
3. If still restrictive, increase `max_depth`
4. Consider query optimization instead

### Boundaries Too Permissive

**Problem**: Queries taking >1 second

**Solution**:
1. Reduce `max_depth` to 3 or less
2. Reduce `max_nodes_visited` by 50%
3. Decrease `max_time_ms` to force earlier cutoff
4. Review query patterns for inefficiency

## Configuration Best Practices

1. **Start Conservative**: Begin with restrictive limits, increase as needed
2. **Monitor First**: Collect baseline metrics before tuning
3. **Change One Thing**: Adjust one parameter at a time
4. **Document Changes**: Record what changed and why
5. **Test Before Production**: Validate changes in non-production first
6. **Have Rollback Ready**: Know how to revert quickly

---

*Last Updated: October 18, 2025*
*Sprint: A3 "Some Assembly Required"*
*Related: docs/features/knowledge-graph.md*
