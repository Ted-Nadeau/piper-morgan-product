# Memo: Naming Analysis & Glossary Updates

**To**: CXO (Chief Experience Officer)
**From**: Lead Developer
**Date**: 2026-01-12
**Re**: Context for MUX Planning Discussions

---

## Summary

Two artifacts from today's v0.8.4 release work are relevant to the upcoming MUX (Modeled User Experience) planning discussions:

1. **Capabilities Naming Analysis Prompt** - Ready for deep-dive on feature naming consistency
2. **Updated Glossary (v1.1)** - Now includes full domain models section

---

## 1. Capabilities Naming Analysis

Alpha tester feedback highlighted inconsistent feature naming across our documentation and UI. Terms like "Spatial Awareness," "Context Awareness," and "Environmental Sensing" appear to describe overlapping or identical capabilities.

A prompt has been prepared for a dedicated analysis session:
- **Location**: `dev/2026/01/12/agent-prompt-capabilities-naming-analysis.md`
- **Scope**: Audit all capability names, identify overlaps, propose canonical naming
- **Relevance to MUX**: Establishing clear capability names before MUX work prevents compounding the inconsistency

**Recommendation**: Run this analysis before or in parallel with MUX kickoff to establish naming conventions that MUX features will follow.

---

## 2. Glossary Domain Models Section

The glossary (`knowledge/piper-morgan-glossary-v1.md`) has been updated to v1.1 with a comprehensive Domain Models section. This documents:

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
2. Capabilities naming prompt (5 min) - understand the consistency problem
3. Then proceed with MUX planning discussions

---

*Prepared for PM to share with leadership team*
