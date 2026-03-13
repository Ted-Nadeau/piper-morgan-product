# Gameplan: MUX-400 CONSCIOUSNESS

**Issue**: #400 MUX-VISION-CONSCIOUSNESS
**Created**: 2026-01-20
**Template**: v9.3

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] #399 complete: MUX infrastructure (302 tests)
- [x] #404 complete: Grammar application patterns (5 patterns, guides, checklist)
- [x] ADR-045: Object model vision
- [x] ADR-055: Implementation details
- [x] Morning Standup: `services/features/morning_standup.py`
- [ ] PM-070: Original embodied AI vision (July 2025) - needs location
- [ ] Nov 25 CXO session: Gap analysis - needs location

**My understanding of the task**:
- Create philosophy document explaining WHY consciousness matters
- Connect technical patterns to original embodied AI vision
- Document "soul preservation" principles for future developers
- NOT creating patterns or guides (already done in #404)

### Part A.2: Worktree Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes
- [ ] Multi-component work
- [ ] Exploratory/risky changes where easy rollback is valuable

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [x] Small fixes (<15 min)
- [x] Documentation-only work
- [ ] Time-critical work

**Assessment**:
- [x] **SKIP WORKTREE** - Documentation-only philosophy work, single document creation
- Rationale: Creating one philosophy document. No code changes. Sequential narrative work.

### Part B: Verification Commands

```bash
# Verify #399 complete
gh issue view 399 --repo mediajunkie/piper-morgan-product --json state
# Expected: CLOSED

# Verify #404 complete
gh issue view 404 --repo mediajunkie/piper-morgan-product --json state
# Expected: CLOSED

# Verify existing documentation exists
ls -la docs/internal/development/mux-implementation-guide.md
ls -la docs/internal/development/grammar-transformation-guide.md
ls -la docs/internal/development/grammar-onboarding-checklist.md
ls -la docs/internal/architecture/current/patterns/grammar-application-patterns.md
# Expected: All exist

# Look for PM-070 vision document
find . -name "*PM-070*" -o -name "*pm-070*" -o -name "*pm070*" 2>/dev/null
grep -r "PM-070" docs/ knowledge/ --include="*.md" 2>/dev/null | head -20
# Expected: Locate original vision

# Look for Nov 25 gap analysis
find dev/ -name "*nov*25*" -o -name "*2025-11-25*" 2>/dev/null
grep -r "Nov 25" docs/ dev/ --include="*.md" 2>/dev/null | head -10
grep -r "CXO session" docs/ dev/ --include="*.md" 2>/dev/null | head -10
# Expected: Locate gap analysis
```

### Part C: Proceed/Revise Decision

- [ ] **CONDITIONAL PROCEED** - May need PM help locating historical documents
- If PM-070 and Nov 25 gap analysis can't be found, ask PM for guidance

---

## Phase 0: Vision Archaeology

### Objective
Locate and study original embodied AI vision documents

### Tasks

1. **Locate PM-070 original vision** (July 2025)
   - Search codebase for PM-070 references
   - Check knowledge/, docs/, dev/ directories
   - If not found, ask PM for location

2. **Locate Nov 25 CXO session gap analysis**
   - Search for Nov 25, 2025 references
   - Check session logs from that date
   - If not found, ask PM for location

3. **Document what the original vision intended**
   - Extract key consciousness concepts
   - Note the "5 orientation queries" from original
   - Document embodied AI philosophy

4. **Identify where vision survived vs was flattened**
   - Morning Standup: survived
   - Other features: mostly flattened
   - Document the gap

### Deliverables
- Source material compilation
- Vision gap analysis notes
- Key quotes from original documents

---

## Phase 0.5-0.8: Conditional Phases

### Phase 0.5: Frontend-Backend Contract - **N/A**
- Philosophy documentation, no UI work

### Phase 0.6: Data Flow Verification - **N/A**
- No data flow, documentation only

### Phase 0.7: Conversation Design - **N/A**
- Not a conversational feature

### Phase 0.8: Post-Completion Integration - **N/A**
- Documentation work, no state changes

---

## Phase 1: Five Pillars Philosophy Document

### Objective
Create the consciousness philosophy document

### The Five Pillars of Consciousness

1. **Identity Awareness**
   - Piper knows itself as an entity with role and boundaries
   - "I notice...", "I should...", "I'm concerned..."
   - Not mechanical third-person reporting

2. **Time Consciousness**
   - Not clock time but lived time
   - Rhythms, deadlines, urgency
   - "This has been waiting...", "Coming up soon..."

3. **Spatial Awareness**
   - Understanding of digital spaces as places to inhabit
   - Navigation between contexts
   - "Over in GitHub...", "From your calendar..."

4. **Agency Recognition**
   - Knows what it can/cannot do
   - Asks permission appropriately
   - "I could...", "Would you like me to..."

5. **Predictive Modeling**
   - Sees patterns, has premonitions
   - Expresses concerns
   - "I'm concerned about...", "This might become..."

### Tasks

1. **Document each pillar** with:
   - Philosophy explanation
   - Why it matters for consciousness
   - Examples from Morning Standup
   - Anti-examples (flattened versions)

2. **Connect pillars to MUX protocols**
   - Identity → EntityProtocol
   - Time → MomentProtocol + Temporal Lens
   - Spatial → PlaceProtocol
   - Agency → Ownership model
   - Predictive → Lenses + Situation

3. **Explain the "Recognition over Articulation" principle**
   - Piper should recognize what users mean
   - Not require precise commands
   - Natural understanding

### Deliverables
- `docs/internal/architecture/current/consciousness-philosophy.md`
  - Introduction: Why consciousness matters
  - Part 1: The Five Pillars
  - Part 2: Connection to MUX grammar
  - Part 3: Recognition over Articulation

---

## Phase 2: Soul Preservation Principles

### Objective
Create guidelines preventing future flattening

### Tasks

1. **Document how flattening happens**
   - "Reasonable simplifications" accumulate
   - Implementation shortcuts
   - Performance optimizations that lose consciousness
   - Mechanical testing that misses soul

2. **Create "Cathedral Builder" mindset section**
   - We're building something with a soul
   - Each implementation decision matters
   - Future developers inherit our choices
   - Quote from original issue: "Study it like an archaeologist studying the only intact room of a ruined temple"

3. **Create warning signs of flattening**
   - Third-person mechanical language
   - Timestamps without context
   - IDs instead of names
   - "Query returned X" instead of "I noticed X"
   - No uncertainty expression
   - No concern expression

4. **Create PR review consciousness checklist**
   - Does Piper use "I" naturally?
   - Does Piper express appropriate uncertainty?
   - Does Piper show temporal consciousness?
   - Does Piper navigate spaces vs access endpoints?
   - Does Piper have premonitions vs just alerts?

### Deliverables
- Soul preservation section in philosophy doc
- PR review checklist (can be appendix or separate file)

---

## Phase Z: Integration & Cross-References

### Objective
Connect philosophy to existing documentation

### Tasks

1. **Update ADR-045** with philosophy reference
   - Add link to consciousness philosophy doc
   - Note this completes the "why" documentation

2. **Update ADR-055** with philosophy reference
   - Add link to philosophy doc
   - Cross-reference to patterns

3. **Update grammar-onboarding-checklist.md**
   - Add philosophy doc as recommended reading
   - Add to "Understand the Vision" section

4. **Update grammar-transformation-guide.md**
   - Add reference to philosophy doc
   - Note: understand WHY before HOW

5. **Final session log update**
   - Complete evidence
   - All links verified

### Deliverables
- Updated ADR-045
- Updated ADR-055
- Updated onboarding checklist
- Updated transformation guide
- Session log complete

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent Type | Work | Evidence Required |
|-------|------------|------|-------------------|
| 0 | Single (Haiku) | Vision archaeology | Source materials located |
| 1 | Single (Sonnet) | Philosophy document | 5 pillars documented |
| 2 | Single (Sonnet) | Soul preservation | Guidelines documented |
| Z | Lead Dev | Integration | Cross-references updated |

**Rationale for single-agent phases**:
- Philosophy writing requires consistent voice
- Sequential narrative development
- No parallel work opportunities
- Smaller scope after reduction

### Verification Gates

- [ ] Phase 0: Source materials located or alternatives identified
- [ ] Phase 1: Five pillars documented with examples
- [ ] Phase 2: Soul preservation principles documented
- [ ] Phase Z: All cross-references updated

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Vision archaeology | ❌ | [pending] |
| Five Pillars philosophy doc | ❌ | [pending] |
| Soul preservation principles | ❌ | [pending] |
| Cross-references updated | ❌ | [pending] |

**0/4 = 0%** - Starting point

---

## STOP Conditions

**Standard**:
- Infrastructure doesn't match assumptions
- Can't provide verification evidence
- Completion bias detected

**Domain-specific**:
- PM-070 document cannot be located (ask PM)
- Original vision unclear or contradictory
- Philosophy becomes too abstract to be useful
- Duplicating content already in #404 deliverables

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Evidence Requirements

For each deliverable:
- Document file path
- Word/section count
- Key content summary
- Cross-references verified

---

## Notes

- This is philosophy/narrative documentation
- Scope reduced from original - focus on WHY not HOW
- HOW is already covered in #404 (patterns, guides, checklist)
- Quality over speed - this is Piper's soul
- May need PM help locating historical documents

---

*Gameplan created: 2026-01-20*
*Issue: #400*
*Template: v9.3*
