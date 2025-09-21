# Piper Morgan Backlog - Track/Epic Organization

**Last Updated**: September 7, 2025
**Taxonomy**: TRACK-EPIC: Story description format
**Current Sprint**: OPS-STAND fixes → UX-FTUX intelligence

---

## Issue Taxonomy Reference

### Naming Convention
`TRACK-EPIC: Story description` (numbers only for sub-tasks)

### Tracks
- **CORE** - Core capabilities (intent, orchestration, integrations)
- **FEAT** - Features (user-facing functionality)
- **OPS** - Operations (daily workflow tools)
- **INFR** - Infrastructure (technical foundations)
- **UX** - User Experience (conversational intelligence)
- **FLY** - Flywheel Methodology (excellence practices)

---

## 🎯 Priority Order (Next 2 Weeks)

### Week 1: OPS-STAND Epic (Sept 8-10) - TOMORROW'S FOCUS
- [ ] **OPS-STAND: Fix blank fields bug** (#151) - **HIGH PRIORITY**
- [ ] **OPS-STAND-CLI: Investigation & Repair** (#149) - **HIGH**
- [ ] **OPS-STAND: Human-readable metrics** (#155)
- [ ] **OPS-STAND-MVP: Implementation** (#119)

**Success Criteria**: Morning standup works perfectly in CLI and Web UI

### Week 2: UX-FTUX Epic (Sept 11-14) - CRITICAL PATH
- [ ] **UX-FTUX: Excellence Epic** (#95) - Parent epic
- [ ] **FEAT-INTENT: Conversational categories** (#96) - **P0**
- [ ] **UX-FTUX: Quick context loading** (#97) - **P0**
- [ ] **UX-FTUX: Document ingestion** (#98)
- [ ] **CORE-KNOW: Knowledge graph connection** (#99)
- [ ] **FEAT-PROJ: Portfolio awareness** (#100)
- [ ] **FEAT-TIME: Temporal context** (#101)
- [ ] **UX-GREET: Calendar scanning** (#102)
- [ ] **FEAT-PRIOR: Priority engine** (#103)
- [ ] **FEAT-TIME: Allocation analysis** (#104)

**Success Criteria**: Handles 5 canonical queries without errors

---

## Active Development by Track

### Track 1: Flywheel Methodology (FLY) ✅

**Status**: Ahead of schedule - methodology embedded

- [x] **FLY-IMP: Infrastructure verification** - COMPLETE TODAY
- [x] **FLY-IMP: Three-tier pyramid** (#146) - COMPLETE
- [x] **FLY-IMP: Handoff protocol** (#147) - COMPLETE
- [x] **FLY-IMP: Configuration extraction** (#148) - COMPLETE
- [ ] **FLY-IMP: Performance benchmarking** (#143)
- [ ] **FLY-AUDIT: Weekly docs** (#144) - Tomorrow

### Track 2: Operations (OPS) 🔄

**Status**: Primary focus for Week 1

- [ ] **OPS-STAND** epic (4 issues) - See priority section
- [ ] **OPS-KNOW: Knowledge operations** (#99)

### Track 3: User Experience (UX) 🎯

**Status**: Critical path for Week 2

- [ ] **UX-FTUX** epic (10 issues) - See priority section
- [ ] **UX-GREET: Greeting intelligence** (#102)
- [ ] **UX-PIPER: Personality** (#105)
- [ ] **UX-DESIGN: Design system** (#154)
- [ ] **UX-FTUX: Wizard** (#128)

### Track 4: Core Capabilities (CORE) 🔧

**Status**: Supporting infrastructure

**CORE-NOTN: Notion Integration**
- [ ] Integration (#134)
- [ ] Refactor values (#136)
- [ ] Audit codebase (#137)
- [ ] Design schema (#138)
- [ ] Refactor commands (#140)
- [ ] Testing/docs (#141)
- [ ] Fix validation (#142)

**CORE-INT: Integrations**
- [ ] Learning integration (#107)
- [ ] GitHub deprecation (#109)

### Track 5: Infrastructure (INFR) ⚙️

**Status**: May have blocking issues

**INFR-DATA: Database**
- [ ] AsyncSessionFactory (#113) - May block
- [ ] Remove legacy pool (#114)
- [ ] Fix anti-patterns (#115)
- [ ] Fix asyncio bug (#145)

**INFR-AGENT: Agent Systems**
- [ ] Multi-agent coordinator (#118)
- [ ] Session continuity (#152)
- [ ] Code permissions (#153)
- [ ] Environment config (#156)

### Track 6: Features (FEAT) ✨

**Status**: Intelligence features for UX

**Near-term (Supporting UX-FTUX)**
- [ ] **FEAT-INTENT: Categories** (#96) - CRITICAL
- [ ] **FEAT-TIME: Temporal** (#101, #104)
- [ ] **FEAT-PRIOR: Priority** (#103)
- [ ] **FEAT-PROJ: Portfolio** (#100)
- [ ] **FEAT-STRAT: Strategic** (#106)

**Future Vision (Post-MVP)**
- [ ] **FEAT-DOCS: Document context** (#56)
- [ ] **FEAT-MEET: Meeting analysis** (#57)
- [ ] **FEAT-DASH: Analytics** (#58)
- [ ] **FEAT-VISION: Visual analysis** (#65)
- [ ] **FEAT-PREDICT: Predictive** (#66)
- [ ] **FEAT-GRAPH: Knowledge UI** (#87)

---

## Blocked/Dependencies

### Potential Blockers
- **INFR-DATA** migrations may block other work
- **CORE-NOTN** configuration needed for multi-user

### Dependency Chain
```
OPS-STAND → UX-FTUX → FEAT-INTENT
         ↓
    CORE-KNOW → FEAT-PROJ → FEAT-TIME
```

---

## Definition of Done (MVP)

### Per Track MVP Lines
- **FLY**: ✅ Already sufficient
- **OPS**: All 4 standup issues working daily
- **UX**: Handles canonical queries without errors
- **CORE**: Notion configuration operational
- **INFR**: Database stable, agents coordinate
- **FEAT**: Intent categories recognize patterns

---

## Future Epics (Post-MVP)

### October 2025
- **CORE-OPT: Workflow optimization** (#63)
- **CORE-AUTO: Autonomous workflows** (#64)
- **OPS-FLOW: Workflow orchestration**
- **UX-VOICE: Voice interface**
- **INFR-SCALE: Auto-scaling**

### Vision Features (2026+)
- Advanced meeting analysis
- Predictive analytics
- Visual content pipeline
- Knowledge graph visualization

---

## Success Metrics

### This Week (Sept 8-14)
- [ ] Morning standup works perfectly (OPS-STAND)
- [ ] 5 canonical queries handled (UX-FTUX)
- [ ] Database migrations complete (INFR-DATA)
- [ ] "Play Piper" benchmark matched

### This Month (September)
- [ ] External user successfully onboards
- [ ] 2+ complete workflows daily use
- [ ] Response time <500ms consistently
- [ ] Zero "Failed to process" errors

---

**Next Review**: Monday Sept 9 after OPS-STAND progress
**Ownership**: Chief Architect maintains, PM approves changes
**Tracking**: GitHub Projects board with TRACK-EPIC views
