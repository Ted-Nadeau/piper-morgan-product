# Cursor Agent Prompt: GREAT-3C Phase 0 - Investigation

## Session Log Management
Create new session log: `dev/2025/10/04/2025-10-04-phase0-cursor-investigation.md`

Update with timestamped entries for your work.

## Mission
**Investigate Documentation Organization**: Determine best structure for pattern docs and developer guide, analyze what makes docs effective, and plan documentation deliverables.

## Context

**GREAT-3C Goal**: Document wrapper/adapter pattern and create developer resources.

**Current State** (from Phase -1):
- 4 plugins exist as thin wrappers (96-111 lines each)
- No pattern documentation exists
- services/plugins/README.md exists but may need enhancement
- STRUCTURE_PLAN mentions developer guides

## Your Tasks

### Task 1: Analyze Existing Documentation Structure

```bash
# See current docs organization
tree docs/ -L 2

# Check what's in each major section
ls -la docs/guides/ 2>/dev/null
ls -la docs/internal/architecture/

# Read structure plan
cat docs/STRUCTURE_PLAN.md
```

**Questions to Answer**:
1. Where do plugin docs fit in current structure?
2. Is there a "patterns" or "architecture" section?
3. Where should developer-facing guides live?
4. What's the existing documentation style/format?

### Task 2: Review services/plugins/README.md

```bash
cat services/plugins/README.md
```

**Assess Current Content**:
1. What topics are covered?
2. Is it user-facing or developer-facing?
3. Does it explain architecture?
4. What's the tone and style?
5. Should we enhance this file or create separate docs?

**Compare to Best Practices**:
- Is it scannable? (headers, lists, code examples)
- Is it actionable? (clear steps, copy-paste friendly)
- Is it complete? (all necessary info present)
- Is it maintainable? (not too detailed, not too vague)

### Task 3: Research Effective Documentation Patterns

Think about documentation you've found helpful. What makes good technical docs?

**Pattern Documentation Best Practices**:
- Start with "why" before "how"
- Use diagrams for architecture
- Show before/after examples
- Explain trade-offs
- Document alternatives considered

**Developer Guide Best Practices**:
- Quick start at top
- Step-by-step tutorials
- Runnable code examples
- Troubleshooting section
- Links to related docs

### Task 4: Plan Documentation Files

**Recommendation Format**:
```markdown
## Proposed: Pattern Documentation

**File**: `docs/internal/architecture/patterns/plugin-wrapper-pattern.md`
**Purpose**: Explain architectural decision and pattern
**Audience**: Architects, senior developers
**Sections**:
1. Overview
2. Why this pattern
3. Architecture diagram
4. Examples
5. Trade-offs
6. Future considerations

## Proposed: Developer Guide

**File**: `docs/guides/adding-integrations.md`
**Purpose**: Step-by-step guide for adding new integrations
**Audience**: All developers
**Sections**:
1. Quick start
2. File structure
3. Creating your router
4. Creating your plugin
5. Configuration
6. Testing
7. Common patterns
```

### Task 5: Architecture Diagram Planning

**What diagrams would help?**

Think about what's hard to understand without visuals:

1. **Plugin System Overview**
   - Components: PluginRegistry, Plugins, Routers, Config
   - Relationships and data flow

2. **Wrapper Pattern Detail**
   - Router ↔ Plugin relationship
   - How config flows
   - Auto-registration mechanism

3. **Lifecycle Flow**
   - Discovery → Config → Loading → Init → Operation → Shutdown

**Diagram Formats**:
- ASCII art (easy to maintain in markdown)
- Mermaid (renders in GitHub)
- Tool-generated (requires external tool)

**Recommendation**: What format and what diagrams?

### Task 6: Example Integration Design

**What makes a good example?**

Consider these options:

**Option A: Functional Mock ("Weather")**
- Simulates real API with mock data
- Shows HTTP requests, error handling
- More realistic but more complex

**Option B: Minimal Stub ("Example")**
- Bare minimum implementation
- Focus on structure over functionality
- Easier to understand and maintain

**Option C: Echo/Demo Service**
- Simple echo/status endpoints
- Shows request/response patterns
- Demonstrates plugin features

**Questions**:
1. Which option is best learning tool?
2. What's the maintenance burden?
3. Will developers copy-paste or read-and-adapt?
4. Should we have multiple examples?

### Task 7: Documentation Style Guide

**Analyze existing docs** to determine consistent style:

```bash
# Sample existing docs
head -30 docs/README.md
head -30 services/plugins/README.md
```

**Style Elements**:
- Heading levels (when to use #, ##, ###)
- Code block formatting
- Command examples format
- Link style
- Table of contents usage

**Recommendation**: Style guidelines for new docs to match existing.

## Deliverable

Create: `dev/2025/10/04/phase-0-cursor-investigation.md`

Include:
1. **Documentation Structure Analysis**: Current organization
2. **README Assessment**: What exists, quality evaluation
3. **Documentation Best Practices**: What makes docs effective
4. **File Organization Plan**: Where each doc should live
5. **Diagram Recommendations**: What diagrams, what format
6. **Example Integration Design**: Which option and why
7. **Style Guidelines**: Consistency recommendations

## Success Criteria
- [ ] Current docs structure understood
- [ ] Clear recommendations for file locations
- [ ] Diagram plan defined
- [ ] Example integration approach chosen
- [ ] Style guidelines documented
- [ ] All recommendations actionable

## Notes
- Focus on maintainability - docs rot quickly
- Consider the reader's journey (novice → expert)
- Balance completeness with conciseness
- Think about searchability and navigation

---

**Deploy at 12:25 PM**
**Coordinate with Code on content requirements**
