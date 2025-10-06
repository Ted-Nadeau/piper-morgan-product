# GREAT-3D Phase Set 3: ADR Documentation Prompts

## Phase 5: ADR-034 Creation/Update (Code Agent)

### Context
We need to document the plugin architecture implementation in ADR-034. This is the critical architectural record of what we built in GREAT-3A, 3B, and 3C.

### Your Task
Create or update `docs/adrs/adr-034-plugin-architecture.md` with the following structure:

```markdown
# ADR-034: Plugin Architecture Implementation

## Status
Implementation Status: Complete (October 2-4, 2025)

## Context
[Explain why plugin architecture was needed - monolith refactoring, configuration complexity, need for dynamic integration management]

## Decision
We chose a Wrapper/Adapter pattern where:
- Business logic remains in routers
- Plugins are thin adapters implementing PiperPlugin interface
- This provides plugin benefits without major refactoring

## Implementation Timeline
- GREAT-3A (Oct 2): Foundation - interface, registry, 4 operational plugins
- GREAT-3B (Oct 3): Dynamic loading - config control, discovery, lifecycle
- GREAT-3C (Oct 4): Documentation - guides, demo plugin, patterns
- GREAT-3D (Oct 4): Validation - contracts, performance, ADRs

## Architecture Details
[Describe the two-file pattern, auto-registration, config in PIPER.user.md]

## Performance Characteristics
[Reference the performance test results - <0.05ms overhead, etc.]

## Consequences
### Benefits
- Clean separation of concerns
- Easy to add new integrations
- Config-based enable/disable
- Minimal performance overhead

### Trade-offs
- Two files per integration (router + plugin)
- Not "pure" plugins (business logic in routers)

### Migration Path
[Describe how we could move to pure plugins if needed]

## Related ADRs
- ADR-038: Three Spatial Patterns
- ADR-013: Original spatial pattern (deprecated)
```

### Additional Instructions
- Keep it concise but comprehensive
- Include actual metrics from performance tests
- Reference the demo plugin as example
- Mark as "Implementation Status: Complete"

---

## Phase 6: Related ADR Updates (Cursor Agent)

### Context
Several ADRs may reference the old integration architecture or need updates to reflect the new plugin system.

### Your Task

1. **Find related ADRs**:
```bash
# Search for ADRs mentioning plugins, integrations, or routers
grep -l "plugin\|integration\|router" docs/adrs/*.md
```

2. **For each related ADR, add a note**:
```markdown
## Update October 2025
See ADR-034 for plugin architecture implementation that affects this decision.
```

3. **Specifically check and update**:
- ADR-038 (spatial patterns) - Add reference to plugin implementation
- ADR-013 (if it exists) - Mark as superseded by ADR-038
- Any ADRs about configuration - Reference PIPER.user.md plugin config

4. **Create summary file**:
Create `dev/2025/10/04/adr-updates-summary.md` listing:
- Which ADRs were updated
- What changes were made
- Which ADRs didn't need updates

### Additional Instructions
- Don't change the core content of other ADRs
- Just add update notes and cross-references
- Keep updates minimal and focused
- Put any working files in dev/2025/10/04/

---

## Success Criteria for Phase Set 3

- [ ] ADR-034 created/updated with complete implementation record
- [ ] All related ADRs have update notes
- [ ] Cross-references added where appropriate
- [ ] Summary file created in dev/2025/10/04/
- [ ] No files created in root directory

## Time Estimate
~1 hour for both agents working in parallel

---

*Execute Phase 5 and 6 in parallel. PM will return in ~1 hour to review.*
