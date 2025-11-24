# Learning System Component Locations

## Component 1: Knowledge Graph Reasoning Chains

### Source Files
- **Main Service**: `/Users/xian/Development/piper-morgan/services/knowledge/knowledge_graph_service.py`
  - get_relevant_context(): Lines 710-778
  - expand(): Lines 607-667
  - extract_reasoning_chains(): Lines 668-708

- **Edge Types**: `/Users/xian/Development/piper-morgan/services/shared_types.py`
  - EdgeType enum with BECAUSE, ENABLES, REQUIRES, PREVENTS, LEADS_TO, BEFORE, DURING, AFTER

- **Models**: `/Users/xian/Development/piper-morgan/services/domain/models.py`
  - KnowledgeEdge class with confidence, usage_count, last_accessed fields

### Integration Point
- **IntentClassifier**: `/Users/xian/Development/piper-morgan/services/intent_service/classifier.py`
  - _get_graph_context(): Lines 848-877
  - _extract_intent_hints_from_graph(): Lines 879-914
  - Knowledge graph service passed in constructor (line 44-56)

### Tests
- **File**: `/Users/xian/Development/piper-morgan/tests/integration/test_knowledge_graph_enhancement.py`
- **Test Count**: 40 tests, all passing

---

## Component 2: Preference Persistence

### Source Files
- **Main Service**: `/Users/xian/Development/piper-morgan/services/domain/user_preference_manager.py`
  - set_preference(): Lines 113-163
  - get_preference(): Lines 165-222
  - apply_preference_pattern(): Lines 745-807
  - Reminder preferences: Lines 467-648
  - Learning preferences: Lines 650-742

- **Constants**: Lines 18-45
  - STANDUP_REMINDER_ENABLED, STANDUP_REMINDER_TIME, etc.
  - LEARNING_ENABLED, LEARNING_MIN_CONFIDENCE, LEARNING_FEATURES

### Integration Point
- **QueryLearningLoop**: `/Users/xian/Development/piper-morgan/services/learning/query_learning_loop.py`
  - _apply_user_preference_pattern(): Lines 375-457
  - Instantiates UserPreferenceManager and calls apply_preference_pattern()

### Tests
- **File**: `/Users/xian/Development/piper-morgan/tests/integration/test_preference_learning.py`
- **Test Count**: 5 tests, all passing

---

## Component 3: Pattern Learning Handler

### Source Files
- **Main Service**: `/Users/xian/Development/piper-morgan/services/learning/query_learning_loop.py`
  - PatternType enum: Lines 25-38
  - LearnedPattern dataclass: Lines 49-63
  - PatternFeedback dataclass: Lines 66-75
  - learn_pattern(): Lines 178-223
  - apply_pattern(): Lines 225-282
  - _apply_user_preference_pattern(): Lines 375-457
  - provide_feedback(): Lines 659-711
  - get_learning_stats(): Lines 771-809

- **Storage**:
  - Patterns: `data/learning/learned_patterns.json`
  - Feedback: `data/learning/pattern_feedback.json`

### Integration Point
- **OrchestrationEngine**: `/Users/xian/Development/piper-morgan/services/orchestration/engine.py`
  - learning_loop initialization: Lines 99-101
  - Pattern learning during query handling: Lines 168-170

### Tests
- **File**: `/Users/xian/Development/piper-morgan/tests/integration/test_learning_system.py`
- **Test Count**: 9 tests, 7 passing, 2 skipped (known limitation)

---

## Full Integration Test Files

1. **Knowledge Graph Enhancement**
   - File: `/Users/xian/Development/piper-morgan/tests/integration/test_knowledge_graph_enhancement.py`
   - Classes: TestEdgeTypeEnhancements, TestConfidenceWeighting, TestGraphFirstRetrievalPattern, TestIntentClassifierGraphIntegration, TestReasoningChainExtraction, TestPerformanceCharacteristics, TestBackwardCompatibility, TestIntegrationFlow, TestCostSavingsPotential, TestDataModel
   - Tests: 40 passing

2. **Preference Learning**
   - File: `/Users/xian/Development/piper-morgan/tests/integration/test_preference_learning.py`
   - Class: TestPreferenceLearning
   - Tests: 5 passing

3. **Learning System Integration**
   - File: `/Users/xian/Development/piper-morgan/tests/integration/test_learning_system.py`
   - Class: TestLearningSystemIntegration
   - Tests: 7 passing, 2 skipped

---

## Session Logs Created

1. **Full Investigation Report**
   - File: `/Users/xian/Development/piper-morgan/dev/2025/10/26/2025-10-26-learning-system-archaeology.md`
   - Content: Complete archaeological investigation with all findings

2. **Quick Reference Verdict**
   - File: `/Users/xian/Development/piper-morgan/dev/2025/10/26/LEARNING-SYSTEM-VERDICT.md`
   - Content: TL;DR summary with test results

3. **Component Locations**
   - File: `/Users/xian/Development/piper-morgan/dev/2025/10/26/COMPONENT-LOCATIONS.md`
   - Content: This file - absolute paths to all components
