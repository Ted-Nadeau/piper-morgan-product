# Workstream Reorganization Decision

**Date**: December 4, 2025
**Decision makers**: xian (CEO), Chief of Staff
**Effective**: Immediately (Weekly Ship #020 onwards)
**Status**: Active

---

## Decision Summary

Piper Morgan project workstreams reorganized from 7 to 6 streams to reflect organizational complexity, role proliferation, and emerging constitutional work. New structure aligns workstreams with organizational functions and clarifies ownership.

---

## Context: Why Reorganization Was Needed

### Scale Changes (Nov 28 → Dec 3)

**Role proliferation**:
- Nov 28: 4 roles (SecOps, CXO, Chief Architect, Chief of Staff)
- Dec 3: 8-10 roles (added PPM, Exec Coach, Lead Dev shifts, specialized agents, Mobile)

**Coordination complexity**:
- Single-session days → 15-session days (Dec 1: 7 unique roles)
- Simple handoffs → triads (PPM + CXO + Architect feedback cycles)
- Internal only → external participants (Ted, Sam advisors; Michelle, alfwine alpha users)

**Work types emerging that didn't fit old structure**:
- Constitutional/meta-work (PDR pattern, governance formalization)
- Advisor integration (processing external feedback)
- Methodology innovation (Agent Ops, coordination patterns)
- Strategic content management (vs execution-only writing)

### Old Structure Strains

| Old Workstream | Strain Signal |
|----------------|---------------|
| **Core Build** | Role proliferation within stream, integration testing unclear |
| **Architecture** | Mixed system architecture with work architecture (how we collaborate) |
| **Documentation** | Manual session log assembly (PM's spreadsheet workaround) |
| **Learning Curation** | No clear owner, monthly sweeps but daily patterns emerging |
| **Kind Systems** | Too lightweight for dedicated stream |
| **Public Content** | Comms Director underutilized strategically |
| **Running Piper** | Premature - still in alpha, not operations |

---

## New Structure: 6 Workstreams

### 1. Product & Experience

**Owner**: Principal Product Manager
**Collaborators**: CXO, Mobile Consultant, xian (CPO)

**Scope**:
- Product strategy and roadmap
- PDRs (Product Decision Records)
- UX vision and MUX track
- Mobile strategy
- Feature prioritization
- User research and alpha testing insights

**Why this workstream**:
- Formalizes product governance (was implicit in xian's head)
- Unifies product thinking (what/why) with experience design (how it feels)
- PPM + CXO collaboration now has dedicated stream

**Calved from**: Architecture (where product decisions were mixed with system architecture)

---

### 2. Engineering & Architecture

**Owner**: Chief Architect
**Collaborators**: Lead Developer, specialized agents (Programmer, Testing, SecOps, Docs)

**Scope**:
- System architecture and ADRs
- Core feature development
- Bug fixes and integration testing
- Production deployments
- Security operations
- Technical debt management

**Why this workstream**:
- Largest organizational division (Chief Arch → Lead Dev → 6 specialized roles)
- Focuses on system architecture (how things work), distinct from methodology (how we work)
- Integration testing explicitly part of feature building

**Renamed from**: Core Build + Architecture (system parts only)

---

### 3. Methodology & Process Innovation

**Owner**: Chief Architect (interim, until HOSR created)
**Collaborators**: Agent Ops function, xian, Chief of Staff (involved, not decider)

**Scope**:
- Excellence Flywheel evolution
- Coordination patterns (Queue, Advisor Mailbox)
- Agent coordination protocols
- Process debt and constitutional design
- Integration testing discipline
- Role recovery and drift prevention
- Pattern capture and methodology documentation

**Why this workstream**:
- Was completely orphaned - no dedicated owner
- "How we work" is distinct from "what we build"
- Agent Ops (under future HOSR) manages these processes
- Constitutional design work needs explicit tracking

**New workstream**: Carved out from Architecture + implicit PM work

---

### 4. Governance & Operations

**Owner**: Chief of Staff
**Collaborators**: Doc specialists, xian

**Scope**:
- Weekly Ships and workstream tracking
- Session log assembly and omnibus creation
- Role coordination and handoffs
- Weekly retrospectives
- Operational decisions
- Resource allocation visibility
- Documentation hygiene (weekly audits)

**Why this workstream**:
- Core Chief of Staff function - keeping ensemble visible and coordinated
- Distinct from execution, distinct from methodology innovation
- "Meta-level" work that enables all other streams

**Renamed from**: Documentation (significantly expanded scope)

---

### 5. External Relations & Community

**Owner**: Communications Director (expanded scope)
**Collaborators**: Advisor liaison function, xian

**Scope**:
- Editorial strategy (not just execution)
- Advisor integration (Ted, Sam synthesis for public)
- Public content strategy and publishing
- Newsletter and blog posts
- Speaking engagements (IAC 2026)
- Community engagement
- Kind Systems relationship context

**Why this workstream**:
- Unifies all external-facing work
- Recognizes Comms Director's growth and capabilities
- Strategic coordination needed across advisors, content, community
- Kind context tracked here (lightweight but important)

**Expanded from**: Public Content + Kind Systems + advisor synthesis

---

### 6. Learning & Knowledge

**Owner**: TBD (HOSR candidate when role created)
**Collaborators**: Chief Architect, PPM, CXO (all feed inputs)

**Scope**:
- Pattern sweeps (monthly cadence)
- Real-time insight capture
- Composting → Learning pipeline
- Knowledge curation
- Cross-project learning
- Methodology evolution inputs
- Breakthrough detection

**Why this workstream**:
- Explicitly owns "what are we learning?" question
- Feeds Methodology (#3) and informs Product (#1)
- Critical capability for institutional memory
- HOSR (Head of Sapient Resources) is natural long-term owner

**Status**: Holding for HOSR role creation; interim distributed with Chief of Staff synthesis

**Renamed from**: Learning Curation (with explicit owner TBD)

---

## Mapping: Old → New

| Old Workstream (7 total) | New Workstream(s) | Primary Change |
|--------------------------|-------------------|----------------|
| Core Build | Engineering & Architecture | Focused on execution + system design |
| Architecture | Engineering & Architecture + Methodology | System vs process separated |
| Documentation | Governance & Operations | Operational coordination, not just docs |
| Learning Curation | Learning & Knowledge | Explicit ownership (HOSR future) |
| Kind Systems | External Relations & Community | Part of broader external function |
| Public Content | External Relations & Community | Strategy + execution unified |
| Running Piper | **Deferred** | Premature; lives in Product + Engineering for now |
| *(implicit)* | **Product & Experience** | Formalized with PPM + CXO roles |

**Net change**: 7 → 6 workstreams, with clearer ownership and scope

---

## Role Ownership Matrix

| Workstream | Primary Owner | Interim/Future Notes |
|------------|---------------|----------------------|
| Product & Experience | Principal Product Manager | ✅ Established |
| Engineering & Architecture | Chief Architect | ✅ Established |
| Methodology & Process | Chief Architect | Interim until HOSR created |
| Governance & Operations | Chief of Staff | ✅ Core role |
| External Relations & Community | Communications Director | Expansion brief issued Dec 4 |
| Learning & Knowledge | TBD | HOSR candidate; holding pattern |

---

## Decision Rationale

### 1. Why 6 instead of 7?
- "Running Piper" was premature - we're in alpha testing, not operations
- Alpha testing activities distributed across Product (user insights) and Engineering (bug fixes)
- One workstream removed without losing coverage

### 2. Why separate Product from Engineering?
- Product thinking (what/why/for whom) is distinct from system design (how it works)
- PPM + CXO collaboration needed dedicated space
- Product governance was implicit, now explicit (PDR pattern)

### 3. Why explicit Methodology stream?
- "How we work" was orphaned - Architecture owned system design, no one owned process innovation
- Agent Ops needs dedicated tracking (coordination patterns, constitutional design)
- Excellence Flywheel evolution is real work that wasn't being tracked

### 4. Why expand Comms Director to External Relations?
- Comms demonstrated synthesis, judgment, pattern recognition over 26+ posts
- Strategic coordination needed across advisors, content, community, speaking
- Editorial strategy was in xian's head; now delegated with approval

### 5. Why hold Learning stream ownership?
- HOSR (Head of Sapient Resources) is natural owner - learning how sapients collaborate
- Role doesn't exist yet, but learning work is happening
- Interim: distributed capture with Chief of Staff synthesis in Weekly Ships

### 6. Why Chief Architect owns Methodology interim?
- Leans technical (coordination patterns, Agent Ops protocols)
- Chief Architect already doing this work (Queue, Mailbox design)
- Chief of Staff involved (coordination visibility) but not decider (technical choices)

---

## Implementation

### Immediate (Dec 4, 2025)
- ✅ Weekly Ship #020 will use new 6-workstream structure
- ✅ Communications Director receives expansion brief
- ✅ Chief of Staff updates tracking templates and processes

### Short-term (Next 2-4 weeks)
- Communications Director establishes editorial calendar and backlog grooming
- Chief Architect documents methodology patterns emerging
- Learning stream interim process established (distributed capture + CoS synthesis)

### Medium-term (Next 1-3 months)
- Evaluate HOSR role creation timing
- Assess if Methodology should stay with Chief Architect or move to HOSR
- Review workstream effectiveness in Weekly Ship retros

---

## Success Criteria

This reorganization succeeds if:

1. **Clearer ownership** - No orphaned work, everyone knows who owns what
2. **Better coordination** - Role handoffs and collaboration smoother
3. **Strategic leverage** - xian focuses on vision, roles own execution + strategy
4. **Visible operations** - Weekly Ships reflect actual work happening
5. **Scalable structure** - Can add roles/complexity without reorganizing again soon

---

## Open Questions

1. **HOSR creation timing** - When? What triggers this?
2. **Learning interim process** - Distributed capture working, or need dedicated owner sooner?
3. **Comms Director expansion** - Will strategic responsibility work as hoped?
4. **Methodology ownership** - Does Chief Architect interim work long-term?

These will be assessed in weekly retros and adjusted as needed.

---

## Related Documents

- **Communications Director Expansion Brief** (Dec 4, 2025)
- **PM's Org Chart** (Sapient Resources concept, ascii doodles)
- **Weekly Ship #020** (first using new structure)
- **Session log**: 2025-12-04-0900-exec-sonnet-log.md

---

**Approved by**: xian (CEO)
**Prepared by**: Chief of Staff
**Filed in**: Project Knowledge
**Review date**: Weekly Ships through end of December 2025
