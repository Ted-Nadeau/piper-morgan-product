"""
Slot-filling framework for natural multi-turn data collection.

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation
Epic: #762 GLUE - Conversational Glue Implementation

Provides reusable slot-filling that any workflow can use:
- SlotTemplate: Declarative slot specifications
- SlotExtractor: LLM-based multi-slot extraction
- SlotFillingManager: State machine for multi-turn collection
"""
