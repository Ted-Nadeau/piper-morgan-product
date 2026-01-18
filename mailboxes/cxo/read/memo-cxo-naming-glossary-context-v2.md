# Memo: Naming Analysis & Glossary Updates

**To**: CXO (Chief Experience Officer)
**CC**: PPM, Communications Chief, Chief Architect
**From**: Lead Developer
**Date**: 2026-01-12
**Re**: Context for MUX Planning Discussions

---

## Summary

Two artifacts from today's v0.8.4 release work are relevant to the upcoming MUX (Modeled User Experience) planning discussions:

1. **Capabilities Naming Analysis** - Completed analysis of feature naming consistency
2. **Updated Glossary (v1.1)** - Now includes full domain models section

---

## 1. Capabilities Naming Analysis

Alpha tester feedback highlighted inconsistent feature naming across our documentation and UI. Terms like "Spatial Awareness," "Context Awareness," and "Environmental Sensing" appear to describe overlapping or identical capabilities.

**The analysis has been completed:**
- **Report**: `dev/2026/01/12/capabilities-naming-analysis-report.md`
- **Findings**: 35+ capabilities inventoried, 5 naming patterns identified, 4-tier naming framework proposed

**Key findings from completed analysis**:
- 35+ capabilities currently use inconsistent naming
- Proposed framework: Product Names → Actions → Queries → Categories
- PM guidance: Prefer "Assistant" framing over "Coach"; frame GitHub as PM/backlog tool, not dev tool
- Open questions flagged for CXO/PPM/Comms input (see Section 6 of report)

**Relevance to MUX**: Establishing clear capability names before MUX work prevents compounding the inconsistency.

---

## 2. Glossary Domain Models Section

The glossary has been updated to v1.1 (today) with a comprehensive Domain Models section. This documents:

- **User-Created Objects**: Project, List, Todo, File
- **Document & Knowledge**: Document, DocumentChunk, KnowledgeEntry
- **Conversation**: ConversationSession, ConversationTurn, Message
- **Work & Intent**: Intent, Task, Workflow, WorkflowStep
- **Spatial & Context**: SpatialContext, AttentionState, EnvironmentalContext
- **Integration**: Integration, IntegrationCredential, WebhookEvent
- **Ethics & Boundaries**: EthicalBoundary, PermissionScope

Each model includes its relationships to other models and to the broader Object Model.

**Relevance to MUX**: The Spatial & Context models (SpatialContext, AttentionState, EnvironmentalContext) are foundational to MUX's consciousness-aware interaction design. Having these documented provides a shared vocabulary for architecture discussions.

---

## Recommended Reading Order

1. Glossary Domain Models section (10 min) - establishes shared vocabulary
2. Capabilities naming report, especially Section 6 (15 min) - framework and open questions
3. Then proceed with MUX planning discussions

---

## Action Requested

Review the naming analysis report (Section 6: Open Questions) and provide input on:

1. **Naming tone balance** - How much plain language (a) vs. clever/memorable naming (c)?
2. **"Focus Assistant"** and **"Standup Assistant"** - Does this framing work?
3. **PM-centric framing for GitHub features** - "Backlog Tools" vs alternatives?
4. **"Don't Miss"** or similar unique naming - Should we establish a principle for this?

Your input will help us converge on naming conventions before MUX features add more capabilities to name.

---

*Prepared by Lead Developer for PM to share with leadership team*
