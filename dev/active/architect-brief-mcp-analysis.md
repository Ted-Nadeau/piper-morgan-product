# Chief Architect Brief: MCP Code Execution Efficiency Analysis
**Date**: November 14, 2025  
**Requestor**: PM (xian)  
**Priority**: High - Strategic architecture decision  
**Estimated Time**: 2-3 hours analysis + recommendations

---

## Executive summary

Anthropic research has discovered a **98.7% token reduction** opportunity in MCP (Model Context Protocol) usage by shifting from traditional tool calling to code execution patterns. Given Piper Morgan's heavy MCP usage (GitHub, Slack, Calendar, Notion, Serena), this could dramatically improve economics and performance at scale.

**Your mission**: Analyze our current MCP usage patterns and provide a prioritized migration roadmap showing which workflows would benefit most from code execution approach.

---

## Background: The Anthropic discovery

### Traditional MCP pattern (what we likely do now)

**Problem**: Token multiplication through repeated data passing
```
1. Load ALL tool definitions → 1,304 tokens
2. User: "Analyze this document"
3. Model calls read_file → 30 tokens
4. Full document returns to model → 50,000 tokens
5. Model calls extract_keywords WITH full document → 50,000 tokens (again)
6. Model calls generate_summary WITH full document → 50,000 tokens (again)
7. Model formats response → model now holds 150K+ tokens

Total: ~150,000 tokens (document passed through context 3 times)
```

### Code execution pattern (new approach)

**Solution**: Model writes code, data stays in sandbox
```
1. Load minimal TypeScript API definitions → 184 tokens
2. Model writes code:
   const doc = await readFile(path);  // Stays in sandbox
   const keywords = await extractKeywords(doc.content);
   const summary = await generateSummary(doc.content);
   console.log("Done");
   → 285 tokens

3. Code executes in sandbox (document never enters model context)
4. Only logs return to model → 42 tokens

Total: ~511 tokens (98.7% reduction vs traditional)
```

**Key insight**: LLMs are better at writing code than calling tools. They've seen millions of open source projects but limited tool call examples.

---

## Our current MCP architecture

### MCP servers in use

1. **GitHub MCP**: Issue creation, reading, updating, labeling
2. **Slack MCP**: Message sending, channel management, user lookup
3. **Calendar MCP**: Event reading, creation, scheduling
4. **Notion MCP**: Page reading, updating, database queries
5. **Serena MCP**: Code navigation, symbol search, semantic queries

### Suspected usage patterns (need your verification)

**Pattern 1: Sequential tool calls** (likely common)
```python
# Example: GitHub issue workflow
1. Read issue #300 → full issue content to model
2. Analyze content → model processes
3. Create related issue #301 → content back to model
4. Update issue #300 with link → content again
```
**Token cost**: Each step returns full content → multiplicative

**Pattern 2: Large document processing** (confirmed in Issue #290)
```python
# Document analysis workflow
1. Upload PDF (50K tokens)
2. Extract text → full content to model
3. Analyze content → full content through model
4. Generate summary → full content through model again
```
**Token cost**: 150K+ tokens (document passes through 3+ times)

**Pattern 3: Multi-system coordination** (common in workflows)
```python
# Example: Standup → Issue → Slack → Notion
1. Read morning standup format
2. Create GitHub issue based on standup
3. Post to Slack with issue link
4. Update Notion page with progress
```
**Token cost**: Each tool's output becomes next tool's input through model

---

## Architectural questions for analysis

### Question 1: Current token usage baseline

**Please measure**:
- Add token counting to our current MCP calls
- Run typical workflows (document analysis, issue creation, multi-system)
- Capture: tokens per operation, total per workflow, most expensive operations

**Deliverable**: Baseline metrics showing where tokens are spent

---

### Question 2: High-value migration candidates

**Please identify** top 5 workflows by potential token savings:

**Criteria**:
- High token cost currently (>10K per workflow)
- Frequent usage (daily/weekly operations)  
- Chainable operations (multiple MCP calls in sequence)
- Large data payloads (documents, long issue bodies)

**Expected candidates**:
1. Document analysis (PDF → extract → analyze → summarize)
2. Issue creation workflows (read context → create → update → notify)
3. Multi-system updates (GitHub → Slack → Notion chains)
4. Batch operations (multiple similar operations)

**Deliverable**: Prioritized list with estimated token reduction per workflow

---

### Question 3: Hybrid architecture design

**Please design** hybrid approach mixing traditional MCP + code execution:

**Keep traditional MCP for**:
- Single tool calls (no chaining)
- Small data payloads (<1K tokens)
- Interactive user confirmation needed
- Rapid prototyping / experimentation

**Migrate to code execution for**:
- Chained tool sequences (3+ steps)
- Large documents (>10K tokens)
- Data transformation pipelines
- Repeated operations (batch processing)

**Deliverable**: Decision matrix - when to use each pattern

---

### Question 4: Implementation complexity

**Please assess** effort required to add code execution capability:

**Technical questions**:
- Do we need execution sandbox? (Security implications)
- How to expose MCP tools as code APIs? (API design)
- Error handling in generated code? (Debugging)
- Resource limits? (Timeout, memory, CPU)
- Testing strategy? (Validate generated code works)

**Deliverable**: Implementation roadmap with effort estimates (Size: Large/Medium/Small per phase)

---

### Question 5: Migration strategy

**Please recommend** phased rollout approach:

**Phase 1: Pilot** (validate approach)
- Pick ONE high-value workflow
- Implement code execution version
- A/B test: traditional vs code execution
- Measure: tokens, latency, accuracy, user experience

**Phase 2: Selective migration** (proven patterns)
- Convert workflows with >10K token reduction
- Keep simple operations as traditional MCP
- Document patterns for future work

**Phase 3: Optimization** (ongoing)
- Monitor token usage post-migration
- Identify new migration candidates
- Refine code execution patterns

**Deliverable**: Detailed phase plan with success criteria

---

## Context: Related strategic work

### File/artifact management (converging topic)

UX research agent independently identified document management gap:
- Users can upload files but can't browse them
- Piper creates artifacts (PRDs, summaries) but they disappear into chat
- Need file browser MVP (Sprint 5.5 in UX roadmap)

**Convergence point**: Document processing workflows (your analysis subject) directly feeds file management features. Code execution efficiency affects file feature economics.

**Coordinate with**: UX research agent recommendations (attached previously)

---

## Expected deliverables

### Primary output: Prioritized migration roadmap

```markdown
# MCP Code Execution Migration Roadmap

## Baseline Metrics
- Current token usage: [measured data]
- Most expensive workflows: [list with costs]
- Potential savings: [total reduction possible]

## Priority 1: High-value migrations (Phase 1 - 2 weeks)
1. Workflow X: [current tokens] → [projected tokens] = [reduction %]
2. Workflow Y: [similar breakdown]

## Priority 2: Medium-value migrations (Phase 2 - 4 weeks)
[continuing...]

## Keep as Traditional MCP
- Single tool calls
- Small payloads
- [rationale for each]

## Implementation Complexity
- Sandbox requirements: [details]
- API design: [approach]
- Effort estimate: [size per phase]

## Success Metrics
- Token reduction targets per workflow
- Performance benchmarks (latency)
- Quality gates (accuracy, error rates)
```

### Supporting artifacts

- Token usage measurements (spreadsheet or table)
- Decision matrix (when to use each pattern)
- Architecture diagrams (traditional vs code execution)
- Implementation checklist (technical requirements)

---

## Reference materials

### Attached documents

1. **Anthropic Article**: "We've Been Using MCP Wrong" (full text below)
2. **Chief of Staff Analysis**: Deep Dive #2 from work stream review
3. **Current MCP Usage**: Services/integrations using MCP tools

### Available for questions

- Session logs showing MCP usage patterns (Oct-Nov 2025)
- Issue #290 (document processing implementation)
- ADR-013 (MCP spatial intelligence integration)
- Services documentation (GitHub/Slack/Calendar/Notion integrations)

---

## Success criteria

**This analysis succeeds if**:
1. We understand where our token costs come from (baseline)
2. We know which workflows to migrate first (priorities)
3. We have a clear implementation plan (roadmap)
4. We can make data-driven decisions (metrics)
5. We avoid premature optimization (hybrid approach)

**This analysis fails if**:
- Recommendations are theoretical without measurement
- No clear action items or priorities
- Implementation complexity underestimated
- Migration strategy too aggressive (boil ocean)

---

## Timeline

**Requested by**: End of Sprint A9 (next 2 weeks)

**Check-ins**:
- Midpoint: Share baseline metrics + initial findings
- Final: Complete roadmap + recommendations
- Follow-up: Post-pilot review after Phase 1 test

---

## Questions for you

1. Do you need access to production logs to measure token usage?
2. Should we include Serena MCP in analysis or focus on GitHub/Slack/Notion first?
3. Any specific workflows you know are expensive that we should prioritize?
4. Do you have concerns about code execution security/sandboxing?

---

# APPENDIX: Full Anthropic Article

## "We've Been Using MCP Wrong: How Anthropic Reduced AI Agent Costs by 98.7%"

*By Pawel | Medium | November 6, 2025*

[Full article text included here - see attachment from PM for complete content]

Anthropic's recent paper explores the biggest issue with the MCP - their AI agents were processing 150,000 tokens just to load tool definitions before even reading a user's request. The same functionality could use 2,000 tokens — a 98.7% reduction.

This is critical, as AI agents scale from proof-of-concept to production, connecting them to dozens of MCP (Model Context Protocol) servers with hundreds of tools has become standard practice. But there's a problem hiding in plain sight: every tool definition loads into the context window upfront, and every intermediate result flows through the model.

The engineering teams at Anthropic and Cloudflare independently discovered the same solution: stop making models call tools directly. Instead, have them write code.

### The Traditional MCP Trap

[Article continues with full content as provided earlier...]

### The Code Execution Approach

Both Anthropic and Cloudflare arrived at the same insight: LLMs are exceptionally good at writing code, but mediocre at calling tools.

As Cloudflare's team put it:

"LLMs have seen a lot of code. They have not seen a lot of 'tool calls'. In fact, the tool calls they have seen are probably limited to a contrived training set constructed by the LLM's own developers. Whereas they have seen real-world code from millions of open source projects."

[Article continues...]

---

**End of Brief**

**Questions? Contact PM before starting analysis.**
**Clarifications needed? Review session logs or ask in Slack.**
**Ready to begin? Start with baseline token measurement.**
