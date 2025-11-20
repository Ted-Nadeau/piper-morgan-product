# ARCH-SINGLETON: Remove ServiceContainer Singleton Pattern (#361)

**Priority**: P1 (Blocks horizontal scaling)
**Discovered by**: Ted Nadeau (architectural review)
**Effort**: 16-20 hours

## Problem

`ServiceContainer` uses singleton pattern (via `__new__`), preventing multiple instances and blocking horizontal scaling.

**Current implementation**:
```python
# services/container/service_container.py
class ServiceContainer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance  # Always same instance!
```

**This blocks**:
- Running multiple workers (`uvicorn --workers 4`)
- Horizontal pod scaling in Kubernetes
- Blue-green deployments
- Load balancer distribution
- Multi-region deployment

## Impact

### Scaling Limitations
- **Current**: Single process, single instance only
- **Cannot**: Scale beyond one server
- **Result**: Performance ceiling at ~1000 concurrent users

### Testing Limitations
- Cannot test multi-worker scenarios
- Cannot validate load balancing
- Cannot test failover behavior
- Cannot test distributed caching

### Deployment Limitations
- Cannot use container orchestration effectively
- Cannot achieve high availability
- Cannot do zero-downtime deployments
- Single point of failure

## Solution

Refactor to application-scoped container using FastAPI lifespan:

```python
# services/container/service_container.py
class ServiceContainer:
    """Application-scoped container (not singleton)"""

    def __init__(self):
        self.db = None
        self.config = None
        self.repositories = {}
        self.services = {}
        # Initialize per instance, not globally

    async def initialize(self, config: Config):
        """Initialize container for this app instance"""
        self.config = config
        self.db = await create_db_connection(config)
        await self._initialize_repositories()
        await self._initialize_services()

    async def shutdown(self):
        """Clean shutdown for this instance"""
        await self.db.close()

# main.py - FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Each worker gets its own container"""
    container = ServiceContainer()
    await container.initialize(config)
    app.state.container = container  # Attach to app, not global

    yield  # App runs

    await container.shutdown()

app = FastAPI(lifespan=lifespan)

# Access via request.app.state.container, not global
@app.get("/api/conversations")
async def get_conversations(request: Request):
    container = request.app.state.container  # Per-worker instance
    return await container.conversation_service.get_all()
```

## Acceptance Criteria

### Core Refactoring
- [ ] Remove singleton pattern from ServiceContainer
- [ ] Implement application-scoped container
- [ ] Use FastAPI lifespan for initialization
- [ ] Update all endpoints to use `request.app.state.container`
- [ ] Remove global container references

### Dependency Injection Updates
- [ ] Update all services to receive container via constructor
- [ ] Update all repositories to receive db via constructor
- [ ] No global imports of container
- [ ] Clear dependency flow

### Testing
- [ ] Test with `uvicorn --workers 4`
- [ ] Verify each worker has independent container
- [ ] No shared state between workers
- [ ] Memory usage scales linearly with workers
- [ ] Connection pools independent per worker

### Performance Validation
- [ ] Benchmark single worker (baseline)
- [ ] Benchmark 4 workers (should be ~3.5x throughput)
- [ ] Load test with 1000 concurrent connections
- [ ] Verify no resource contention

### Migration Safety
- [ ] No breaking changes to API
- [ ] Backward compatible deployment
- [ ] Rollback plan documented
- [ ] Zero downtime migration

## Implementation Steps

### Phase 1: Prepare (4 hours)
1. Audit all container usage points
2. Identify shared state risks
3. Plan refactoring sequence
4. Create test harness

### Phase 2: Refactor Core (8 hours)
1. Remove singleton pattern
2. Implement lifespan manager
3. Update container initialization
4. Fix dependency injection

### Phase 3: Update Consumers (6 hours)
1. Update all API endpoints
2. Update background tasks
3. Update CLI commands
4. Update tests

### Phase 4: Validate (2 hours)
1. Multi-worker testing
2. Performance benchmarking
3. Load testing
4. Rollback testing

## Risk Mitigation

### Shared State Issues
- Audit for accidental shared state
- Use threading.local() if needed
- Document per-worker vs shared resources

### Database Connections
- Each worker gets own connection pool
- Configure pool size per worker
- Monitor total connections

### Cache Coordination
- Move from in-memory to Redis (future)
- Document cache invalidation strategy
- Accept cache inconsistency (for now)

## Success Metrics

- ✅ Can run with 4+ workers
- ✅ Linear scaling up to 4 workers
- ✅ No shared state errors
- ✅ Passes load test (1000 users)
- ✅ Zero downtime deployment works

## Future Benefits

Once singleton is removed:
- Can deploy to Kubernetes
- Can use auto-scaling
- Can achieve high availability
- Can do blue-green deployments
- Can scale to 10,000+ users

---

*Note: This is a foundational change required for production deployment. Without it, Piper cannot scale beyond a single server.*
