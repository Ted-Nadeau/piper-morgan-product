# Framework Recommendations - Priority & Sequencing

**Date**: November 22, 2025
**For**: Proposal preparation + implementation planning

---

## Recommended Implementation Sequence

Based on research + Piper's current state, recommend this sequence:

### Phase 0: Decision & Prioritization (This Week)
**Time**: 2-4 hours with Chief Architect
**Outcome**: Agree on which frameworks to implement + in what order

**Questions to Resolve**:
1. Does CMM maturity assessment feel useful as a lens?
2. Would wiki/blog hybrid replace current blog approach, or extend it?
3. Should event stream be async-first (resilient) or sync-first (immediate)?
4. Who is the owner/champion for each framework?

---

## Recommended Priority Order: "Foundation First"

### Priority 1: KPI Dashboard + Notation Standard (START HERE)
**Why First**:
- Lowest complexity to implement
- Immediate stakeholder value (xian sees metrics at a glance)
- Provides concrete structure for other frameworks

**Timeline**: 2 weeks
**Deliverables**:
- [ ] KPI notation standard (already researched)
- [ ] Static HTML dashboard template
- [ ] 12 KPIs populated with Piper data
- [ ] Color coding (green/yellow/red)
- [ ] Baseline/target/current clearly marked

**Quick Win**: Show xian this dashboard by Dec 1 → Gets buy-in for other frameworks

**How It Helps Others**:
- CMM assessments will reference KPI trends
- Event stream will trigger dashboard updates
- Multi-perspective reports will include KPI section
- Wiki will document KPI baseline sources

---

### Priority 2: Wiki/Blog Hybrid Architecture (STRUCTURE)
**Why Second**:
- Provides container for all other frameworks
- Living knowledge base prevents framework knowledge decay
- Team reference point (reduces questions about "how do we detect X?")

**Timeline**: 2-3 weeks (parallel with KPI dashboard)
**Deliverables**:
- [ ] Directory structure (docs/patterns/ + dev/YYYY/MM/DD/)
- [ ] Migration of existing pattern definitions
- [ ] 5 initial wiki articles:
  - Breakthrough Detection Pattern
  - Velocity Analysis Method
  - Semantic Emergence Detection
  - Coordination Scoring
  - CMM Levels Applied to Pattern Sweep
- [ ] Blog template for monthly reports
- [ ] Unified search across wiki + blog

**How It Helps Others**:
- Event listeners will know where to update wiki
- CMM assessments will live in wiki + be versioned
- Multi-perspective templates will reference wiki entries
- Artifacts will link to wiki definitions

---

### Priority 3: CMM Maturity Assessment Framework (DIAGNOSTIC)
**Why Third**:
- Builds on wiki structure (definitions are formalized)
- Provides diagnostic lens for roadmap planning
- Helps explain what's needed for next level

**Timeline**: 3 weeks
**Deliverables**:
- [ ] CMM 5-level reference (already researched)
- [ ] Current maturity assessment:
  - Code Pattern Detection: Level 3
  - Semantic Analysis: Level 2
  - Breakthrough Detection: Level 2
  - Coordination Analysis: Level 2
  - Dashboard Reporting: Level 2
- [ ] Gap analysis: What's needed for Level 3?
- [ ] 3-week plan to formalize definitions + training
- [ ] CMM progression roadmap through Q1 2026

**Quick Win**: "By Dec 2025, we reach Level 3 consistency" → Shows progress

**How It Helps Others**:
- Multi-perspective reports assess team phase (exploration vs. execution)
- Event stream validity scores tied to CMM confidence levels
- Dashboard tracks maturity progression (another KPI)
- Wiki documents maturity criteria

---

### Priority 4: Event-Driven Artifact Attribution (INFRASTRUCTURE)
**Why Fourth**:
- Builds on all previous frameworks
- Enables async workflows (not blocking other work)
- Powers cost tracking + validation loops

**Timeline**: 3-4 weeks
**Deliverables**:
- [ ] Event schema (JSON template)
- [ ] 5 listener implementations:
  1. Cost tracker (accumulate analysis hours)
  2. Notifier (alert leadership)
  3. Validator (ask for confirmation)
  4. Blog trigger (queue narrative)
  5. Wiki updater (schedule baseline refresh)
- [ ] Event stream architecture (pub/sub)
- [ ] Graceful degradation (system works if listener fails)
- [ ] Event archive + queryability

**How It Helps Others**:
- Feeds cost data to dashboard (another KPI)
- Populates wiki with metadata (who/when/why)
- Triggers multi-perspective report generation
- Provides feedback loop for validation

---

### Priority 5: Multi-Perspective Framework (SYNTHESIS)
**Why Last**:
- Depends on all other frameworks being in place
- Provides unified report template
- Ensures all stakeholders see relevant view

**Timeline**: 1-2 weeks
**Deliverables**:
- [ ] 4-lens report template:
  1. Code Perspective (metrics)
  2. Text Perspective (rules + assumptions)
  3. Workflow Perspective (procedures)
  4. Strategic Perspective (implications)
- [ ] Integration instructions (how to populate each lens)
- [ ] Example report (using Nov 16-18 breakthrough)
- [ ] Role-based reading guide (xian sees strategic, architect sees code, etc.)

**How It Helps Others**:
- Synthesis layer for all frameworks
- Ensures complete analysis (not single-perspective tunnel vision)
- Makes patterns understandable to diverse audiences

---

## Alternative Sequence: "Leadership First"

If xian needs immediate decision support, reverse order:

1. **KPI Dashboard** (immediate insight)
2. **Multi-Perspective Template** (context for metrics)
3. **CMM Assessment** (maturity diagnosis)
4. **Wiki/Blog Hybrid** (knowledge preservation)
5. **Event Stream** (automation + efficiency)

**Tradeoff**: Faster initial delivery, but rework needed when event stream integration required.

---

## Integration Checkpoints

### Checkpoint 1: After Priority 1+2 (Dec 1)
**Show**: Dashboard + Wiki structure to xian + Chief Architect
**Validate**:
- Is notation standard working?
- Is wiki discoverable/useful?
- What's missing?

**Go/No-Go Decision**: Proceed to CMM formalization?

### Checkpoint 2: After Priority 3 (Dec 8)
**Show**: CMM assessment + roadmap to Chief Architect
**Validate**:
- Agree on current levels?
- Is progression plan realistic?
- Who owns each improvement?

**Go/No-Go Decision**: Proceed to event stream implementation?

### Checkpoint 3: After Priority 4 (Dec 15)
**Show**: Event stream working + 5 listeners active
**Validate**:
- Is async approach performant?
- Are listeners responding correctly?
- Are edge cases handled?

**Go/No-Go Decision**: Release to team + production usage?

### Checkpoint 4: After Priority 5 (Dec 22)
**Show**: Multi-perspective report template + example
**Validate**:
- Does template cover all stakeholder needs?
- Is it useful to write/read?
- What sections need refinement?

**Go/No-Go Decision**: Make template standard for all reports?

---

## Quick Decision Matrix

**Choose this sequence if you prioritize...**

| Priority | Sequence | Rationale |
|----------|----------|-----------|
| **Stakeholder buy-in** | KPI → Multi → CMM → Wiki → Event | Show value first; build infrastructure second |
| **Sustainable infrastructure** | Wiki → CMM → KPI → Event → Multi | Build foundations first; add features second |
| **Fastest implementation** | KPI → Event → Multi → Wiki → CMM | Focus on connected systems; docs last |
| **Least risk to current work** | KPI → Wiki → CMM → Multi → Event | Parallel safe additions; event stream last (biggest change) |
| **Long-term quality** | Wiki → CMM → Event → KPI → Multi | Invest in knowledge + process; reporting follows |

---

## Effort Estimates (Weekly Breakdown)

### Week 1 (Nov 25 - Dec 1)
- **KPI Dashboard**: 8 hours (notation + static HTML + data population)
- **Wiki Structure**: 6 hours (directory setup + 2 initial articles)
- **Total**: 14 hours (1.75 days)

### Week 2 (Dec 2 - 8)
- **Wiki Articles**: 8 hours (3 more detailed articles)
- **CMM Assessment**: 6 hours (current state assessment + gap analysis)
- **Total**: 14 hours

### Week 3 (Dec 9 - 15)
- **Event Stream**: 10 hours (schema + 2-3 listeners)
- **CMM Training Materials**: 4 hours
- **Total**: 14 hours

### Week 4 (Dec 16 - 22)
- **Multi-Perspective Template**: 6 hours
- **Example Report**: 4 hours
- **Refinement + Testing**: 4 hours
- **Total**: 14 hours

**Grand Total**: ~56 hours (1.4 weeks of full-time effort)

---

## Risks & Mitigations

### Risk 1: "Frameworks feel abstract; hard to get momentum"
**Mitigation**: Start with KPI dashboard (concrete, visual)
**Success Signal**: "That dashboard is useful; what's next?"

### Risk 2: "Event stream too complex; delays everything"
**Mitigation**: Implement as "nice to have" in Phase 4; other frameworks work without it
**Success Signal**: Dashboards + Wiki + CMM assessments work; event stream is force multiplier

### Risk 3: "Wiki becomes outdated; loses credibility"
**Mitigation**: Event stream triggers wiki updates; establish update SLA (48 hours after pattern detection)
**Success Signal**: Wiki has "last updated" metadata; team trusts freshness

### Risk 4: "Multi-perspective template too much overhead"
**Mitigation**: Start with 2 lenses (Strategic + Code); add others if valuable
**Success Signal**: "This template helps me understand patterns faster"

---

## Recommendation Summary

**Recommended approach**:
1. Start with **KPI Dashboard + Wiki Structure** (Weeks 1-2)
2. Add **CMM Assessment** (Week 3)
3. Implement **Event Stream** (Week 4)
4. Synthesize with **Multi-Perspective Template** (Week 4)
5. Evaluate + iterate (Week 5+)

**Why this sequence**:
- Builds on concrete deliverables (dashboard, wiki)
- Adds diagnostic capability (CMM)
- Automates workflows (event stream)
- Synthesizes insights (multi-perspective)
- Allows go/no-go decisions at each checkpoint

**If time is constrained** (2 weeks instead of 4):
- Focus on KPI Dashboard + Wiki Structure
- Defer CMM formalization to January
- Skip event stream for now; add manually
- Do multi-perspective template in spike sprint

**Expected outcome**: By Dec 22, 2025:
- Xian has KPI dashboard driving decisions
- Chief Architect has CMM assessment + improvement plan
- Team has wiki reference for pattern detection
- Next phase: Automate via event stream + optimize

---

## Decision Template for Meeting

**Recommendation for implementation:**

```
We propose implementing 5 frameworks in this sequence:

PHASE 1: FOUNDATION (Weeks 1-2)
→ KPI Dashboard (deadline: Dec 1)
→ Wiki/Blog Architecture (deadline: Dec 8)

PHASE 2: ASSESSMENT (Week 3)
→ CMM Maturity Framework (deadline: Dec 15)

PHASE 3: AUTOMATION (Week 4)
→ Event Stream + Listeners (deadline: Dec 22)

PHASE 4: SYNTHESIS (Week 4-5)
→ Multi-Perspective Template (deadline: Dec 22)

Total effort: ~56 hours
Critical path: 4 weeks to full integration
Quick wins: Dashboard by Dec 1, Wiki by Dec 8

Questions for discussion:
1. Does this sequence align with your priorities?
2. Are there frameworks you'd prioritize differently?
3. Who should own each framework?
4. Are there constraints we've missed?
```
